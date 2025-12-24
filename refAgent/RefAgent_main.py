import sys
import os

# Add parent directory to path so relative imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from refAgent.java_metrics_calculator import JavaMetricsCalculator
from refAgent.dependency_graph import JavaClassDependencyAnalyzer, draw_dependency_graph
from utilities import *
from settings import Settings
import argparse
from refAgent.agents import PlannerAgent, RefactoringGeneratorAgent, CompilerAgent, TestAgent

# === Parse project name argument ===
parser = argparse.ArgumentParser(description="Refactor Java Project")
parser.add_argument("project_name", type=str, help="Name of the project folder (e.g. accumulo-2.1)")
args = parser.parse_args()

protject_name = args.project_name

config = Settings()

# Example usage
if __name__ == "__main__":
    print("Starting RefAgent pipeline...")
    
    #Prepare needed folders
    results = {}
    os.makedirs(f"results/{protject_name}", exist_ok=True)
    os.makedirs(f"data/paths/{protject_name}", exist_ok=True)
    print(f"Created result directories for project: {protject_name}")

    # Use detector-based workflow: detect god classes and process only god class + neighbors
    import sys
    try:
        from refAgent.detector import Detector
        detector = Detector(config)
    except Exception as e:
        print("Detector not available:", e)
        detector = None

    if detector:
        project_directory = f"projects/before/{protject_name}"
        god_classes = detector.detect_god_classes(project_directory, top_n=config.DETECTOR_TOP_N)
        print(f"Detected god classes: {god_classes}")

        for target_class in god_classes:
            try:
                if not target_class:
                    continue
                os.makedirs(f"results/{protject_name}/{target_class}", exist_ok=True)
                graph_path = f"data/graphs/{protject_name}/{target_class}_dependency_graph.json"
                analyzer = JavaClassDependencyAnalyzer(target_class)
                analyzer.analyze_project(project_directory)
                analyzer.export_to_json(graph_path)
                draw_dependency_graph(analyzer.dependencies, filename=f"data/graphs/{protject_name}/{target_class}_dependency_graph.png")

                graph_dep = read_json_file(graph_path)
                neighbor_classes = extract_ids(graph_dep)

                # Map class names to file paths and build a compact code bundle
                all_files = get_all_java_files(project_directory)
                class_to_file = {}
                for fpath in all_files:
                    cname = extract_class_name(fpath)
                    if cname:
                        class_to_file[cname] = fpath

                bundle_files = [class_to_file.get(c) for c in neighbor_classes if class_to_file.get(c)]
                bundle_code = "\n// ----- SEPARATOR -----\n".join([parse_java_code(fp) for fp in bundle_files])

                target_file = class_to_file.get(target_class)
                if not target_file:
                    print(f"Could not locate source file for {target_class}, skipping")
                    continue

                before_code = parse_java_code(target_file)
                
                # Truncate very large files to avoid token overflow
                MAX_CODE_SIZE = 50000  # ~12.5K tokens
                if len(before_code) > MAX_CODE_SIZE:
                    # Keep only the class declaration and first N methods
                    lines = before_code.split('\n')
                    truncated = '\n'.join(lines[:min(len(lines), 1500)])  # Keep first 1500 lines
                    before_code = truncated + "\n// ... (file truncated for analysis) ..."
                
                print(f"\n=== Processing god class: {target_class} ===")
                print(f"Target file: {target_file}")
                print(f"Code size: {len(before_code)} chars, {len(bundle_files)} neighbor files")

                # Initialize agents with Groq provider
                if config.LLM_PROVIDER == 'groq':
                    api_key = config.GROQ_API_KEY
                    model = config.GROQ_MODEL
                    provider = 'groq'
                else:
                    api_key = config.API_KEY
                    model = config.MODEL_NAME
                    provider = 'openai'
                
                print(f"Using provider: {provider}, model: {model}")
                planner = PlannerAgent(api_key, model=model, provider=provider)
                refactoring_generator = RefactoringGeneratorAgent(api_key, model=model, provider=provider)
                compiler = CompilerAgent(api_key, model=model, provider=provider)
                test_agent = TestAgent(api_key, model=model, provider=provider)

                # Send ONLY target class to planner (neighbors can be referenced by name)
                neighbor_names = ", ".join([f for f in neighbor_classes[:5]])
                instruction_input = f"Target class code:\n{before_code}\n\nNeighboring classes: {neighbor_names}"
                print(f"Calling planner.analyze_methods()...")
                Instruction = planner.analyze_methods(before_code, instruction_input)
                print(f"Got instructions: {Instruction[:100] if Instruction else 'None'}...")
                results["Instruction"] = Instruction

                query_decision = f"Output: True or False\nFrom this set of instruction: {Instruction} does at least one method need improvement?\nReturn True or False only."
                do_instruct = planner.send(None, query_decision)

                if do_instruct and str(do_instruct).strip().lower() in ("true","yes","1"):
                    for i in range(20):
                        # Use target class code, not full bundle for refactoring
                        gen_query = f"Plan: {Instruction}\n\nTask: Apply the plan by refactoring the Java class:\n{before_code}\n\nReturn ONLY the full Java source of the refactored class in a single fenced `java` code block."
                        improvement = refactoring_generator.run(gen_query, use_refactoring_generator_prompt=True)

                        target_after_path = target_file.replace("projects/before/", "projects/after/")
                        write_to_java_file(file_path=target_after_path, java_code=improvement)

                        write_to_java_file(file_path=f"results/{protject_name}/{target_class}/original_java_code.java", java_code=before_code)
                        write_to_java_file(file_path=f"results/{protject_name}/{target_class}/improved_java_code.java", java_code=improvement)

                        project_after_dir = f"projects_after/{protject_name}"
                        is_compiled, compile_summary = compiler.compile_and_summarize(project_after_dir, before_code, improvement)
                        if not is_compiled:
                            results["Compilation"] = False
                            results["Test passed"] = False
                            results["is improved"] = False
                            write_to_java_file(file_path=target_after_path, java_code=before_code)
                            try:
                                refactoring_generator.llm.message_history.append({"role": "user", "content": compile_summary})
                            except Exception:
                                pass
                            print("Compilation summary (LLM):")
                            print(compile_summary)
                            continue

                        files = extract_ids(graph_dep)
                        tests = find_test_files(files)

                        test_summaries = []
                        for test in tests:
                            if test != "TestCase":
                                rcode, test_summary = test_agent.run_test_and_summarize(
                                    test,
                                    project_dir=project_after_dir,
                                    verify=False,
                                    original_code=before_code,
                                    refactored_code=improvement,
                                )
                                if rcode.returncode != 0:
                                    test_summaries.append(test_summary or rcode.stderr)
                                    continue

                        if test_summaries:
                            combined_summary = test_agent.combine_summaries(test_summaries, original_code=before_code, refactored_code=improvement)
                            results["Compilation"] = True
                            results["Test passed"] = False
                            results["is improved"] = False
                            try:
                                refactoring_generator.llm.message_history.append({"role": "user", "content": combined_summary})
                            except Exception:
                                pass
                            print("Combined test failure summary (LLM):")
                            print(combined_summary)
                            continue

                        results["Compilation"] = True
                        results["Test passed"] = True
                        results["is improved"] = True

                        repo_path = f'projects/after/{protject_name}'
                        file_path = target_file.replace(f"projects/before/{protject_name}/", "")
                        commit_message = f'Refactored {file_path} using RefAgent'
                        commit_file_to_github(repo_path, file_path, commit_message)

                        break

                    write_to_java_file(file_path=target_after_path, java_code=before_code)
                    export_dict_to_json(results, f"results/{protject_name}/{target_class}/metrics")

            except Exception as e:
                print(f"Error while processing {target_class}: {e}")
                continue

        # We've processed detected classes. Exit to avoid double-processing the original file-based loop.
        sys.exit(0)

    #Identify the .java files in  REPO
    export_java_files_to_json(f"projects/before/{protject_name}", f"data/paths/{protject_name}/{protject_name}_files.json")
    files = read_json_file(f"data/paths/{protject_name}/{protject_name}_files.json")
    files = find_non_test_files(files)
    for file in files:
        try:
            project_directory = f"projects/before/{protject_name}"
            target_class = extract_class_name(file)
            class_directory = os.path.dirname(file)

            if target_class == None:
                continue
            os.makedirs(f"results/{protject_name}/{target_class}", exist_ok=True)

            graph_path = f"data/graphs/{protject_name}/{target_class}_dependency_graph.json"
            
            analyzer = JavaClassDependencyAnalyzer(target_class)
            analyzer.analyze_project(project_directory)
            analyzer.export_to_json(graph_path)
            draw_dependency_graph(analyzer.dependencies, filename=f"data/graphs/{protject_name}/{target_class}_dependency_graph.png")
            
            # 1. For a single file
            input_path = "code_smells/project/before"  # Path to the Java code directory
            output_path = "./code_smells/tmp/before"   # Path to store metrics
            designite_jar = "./code_smells/DesigniteJava.jar"  # Path to DesigniteJava.jar

            copy_file(class_directory, input_path, target_class+".java")

            before_calculator = JavaMetricsCalculator(input_path, output_path, designite_jar)
            before_calculator.parse_java_code(file)
            before_metrics = before_calculator.compute_metrics_for_class()
            before_calculator.clean_repository()

            path_to_java_file = file
            path_to_java_file_after = path_to_java_file.replace("before","after")

            Before_java_code = before_calculator.java_code

            #Export the CKO metrics of the original class to results folder
            results["CKO metrics"] = before_metrics

            # Example usage with agents:
            api_key = config.API_KEY
            planner = PlannerAgent(api_key, model=config.MODEL_NAME)
            refactoring_generator = RefactoringGeneratorAgent(api_key, model=config.MODEL_NAME)
            compiler = CompilerAgent(api_key, model=config.MODEL_NAME)
            test_agent = TestAgent(api_key, model=config.MODEL_NAME)

            # Build instruction query via PlannerAgent
            Instruction = planner.analyze_methods(before_calculator.java_code, before_calculator.as_string())
            results["Instruction"] = Instruction

            # Decision Node: ask planner (or the base send) to decide if any method needs improvement
            query_decisition = f"""
                            Output: True or false

                            From this set of instructoin to improve all these methods does as least one method need improvement:

                            Instruction: {Instruction}

                            Don't return any natural language explanation
                            """
            do_instrect = planner.send(None, query_decisition)

            if do_instrect:
                for i in range(20):
                    query = f"""
                                Following the instruction Instructions:{Instruction}  and CKO metrics {before_metrics} and dependent calsses, improve the provided java code {Before_java_code} and improve the
                                CKO metrics. You can assume that the given class and methods are functionally correct. Ensure that you do not
                                Alter the behaviour of the external method while maintaining the behaviour of the method, maintaining both syntactic
                                and semantic corectness. Don't remove any comments or annotations.
                                Provide the java class within code block. Avoid using natural langiage explanations
                                """
                    # RefactoringGeneratorAgent.run will use REFRACTORING_GENERATOR_MAX_TOKENS as the system prompt and strip fences
                    improvement = refactoring_generator.run(query, use_refactoring_generator_prompt=True)

                    print(f"------------ Start making the improvement to compile and test Itteration {i}-----------------")
                    print(f"=============================================================================================")

                    write_to_java_file(file_path=path_to_java_file_after, java_code=improvement)

                    #Write the improved code in the results file
                    write_to_java_file(file_path=f"results/{protject_name}/{target_class}/original_java_code.java", java_code=Before_java_code)
                    write_to_java_file(file_path=f"results/{protject_name}/{target_class}/improved_java_code.java", java_code=improvement)


                    print("-------------------- Compile the improved code ---------------------------------------")

                    project_directory = f"projects_after/{protject_name}"
                    # Use CompilerAgent to compile and (on failure) generate an LLM summary of the error.
                    is_compiled, compile_summary = compiler.compile_and_summarize(project_directory, Before_java_code, improvement)
                    if not is_compiled:
                        results["Compilation"] = False
                        results["Test passed"] = False
                        results["is improved"] = False
                        # Restore original code on failed compilation
                        write_to_java_file(file_path=path_to_java_file_after, java_code=Before_java_code)
                        # Add the compiler LLM summary to the refactoring_generator's message history for context (in-memory only).
                        try:
                            refactoring_generator.llm.message_history.append({"role": "user", "content": compile_summary})
                        except Exception:
                            pass
                        # Print the summary for the user, but do not persist it to disk.
                        print("Compilation summary (LLM):")
                        print(compile_summary)
                        continue

                    print("------------ Test the improved code ---------------------------------------")
                    graph_dep = read_json_file(graph_path)
                    files = extract_ids(graph_dep)
                    tests = find_test_files(files)

                    # Collect per-test summaries and produce one combined summary at the end
                    test_summaries = []
                    for test in tests:
                        if test != "TestCase":
                            rcode, test_summary = test_agent.run_test_and_summarize(
                                test,
                                project_dir=project_directory,
                                verify=False,
                                original_code=Before_java_code,
                                refactored_code=improvement,
                            )
                            if rcode.returncode != 0:
                                # collect the LLM summary when available, otherwise raw stderr
                                test_summaries.append(test_summary or rcode.stderr)
                                # continue checking other tests to aggregate all failures
                                continue

                    # If any tests failed, synthesize one summary for all failures and skip commit/metrics
                    if test_summaries:
                        combined_summary = test_agent.combine_summaries(test_summaries, original_code=Before_java_code, refactored_code=improvement)
                        results["Compilation"] = True
                        results["Test passed"] = False
                        results["is improved"] = False
                        # keep combined summary in-memory for context
                        try:
                            refactoring_generator.llm.message_history.append({"role": "user", "content": combined_summary})
                        except Exception:
                            pass
                        # Print the combined summary for visibility
                        print("Combined test failure summary (LLM):")
                        print(combined_summary)
                        continue
                    print("------------- Commit the code changes to github-------------------")

                    repo_path = f'projects/after/{protject_name}'
                    file_path = file.replace(f"projects/before/{protject_name}/", "")

                    commit_message = f'Your changing file {file_path}'
                    commit_file_to_github(repo_path, file_path, commit_message)   

                    #Compute CKO metrics
                    # 1. For a single file
                    input_path = "code_smells/project/after"  # Path to the Java code directory
                    output_path = "./code_smells/tmp/after"   # Path to store metrics

                    write_to_java_file(file_path=input_path+"/"+target_class+".java", java_code=improvement)


                    after_calculator = JavaMetricsCalculator(input_path, output_path, designite_jar)
                    after_calculator.parse_java_code(file)
                    after_metrics = before_calculator.compute_metrics_for_class()
                    after_calculator.clean_repository()

                    # Check there was an improvement
                    query = """
                            Given the Java code before and after the proposed changes, along with their corresponding CKO metrics, 
                            assess whether the code has improved. Analyze both versions of the code and compare the CKO metrics.
                            Determine if the changes resulted in better code quality, readability, maintainability, and performance.
                            Java code before improvement :{}
                            CKO metrics before improvement : {}
                            
                            Java code after Improvement: {}
                            CKO metrics after Improvement: {}

                            Return True or False.
                            Avoid using natural lanquage explanation
                            """.format(Before_java_code, after_metrics,improvement, after_metrics)
                    
                    is_improvement_resp = planner.send(None, query)
                    try:
                        is_improvement = str(is_improvement_resp).strip().lower() in ("true", "yes", "1")
                    except Exception:
                        is_improvement = False

                    if not is_improvement:
                        results["Compilation"] = True
                        results["Test passed"] = True
                        results["is improved"] = False
                        continue
                            
                    results["Compilation"] = True
                    results["Test passed"] = True
                    results["is improved"] = True
                    results["CKO metrics After"] = after_metrics

                    break
                
                write_to_java_file(file_path=path_to_java_file_after, java_code=Before_java_code)
                export_dict_to_json(results, f"results/{protject_name}/{target_class}/metrics")
        except:
            continue
            








        
