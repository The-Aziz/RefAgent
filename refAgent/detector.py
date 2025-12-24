import os
import subprocess
from utilities import get_all_java_files, parse_java_code, extract_class_name
from settings import Settings
import javalang

class Detector:
    """Detector that finds candidate god classes.

    Strategy:
    - If config.DETECTOR_TOOL == 'pmd' and PMD_PATH is set, attempt to run PMD and parse results.
    - Otherwise fall back to a lightweight heuristic: rank classes by LOC and method count.
    """

    def __init__(self, config: Settings = None):
        self.config = config or Settings()

    def _heuristic_rank(self, project_dir: str):
        candidates = []
        files = get_all_java_files(project_dir)
        for f in files:
            try:
                code = parse_java_code(f)
                # compute simple heuristics
                loc = len([l for l in code.splitlines() if l.strip() != ""]) 
                methods = 0
                try:
                    tree = javalang.parse.parse(code)
                    for _, node in tree.filter(javalang.tree.MethodDeclaration):
                        methods += 1
                except Exception:
                    # parsing may fail for some files; ignore and continue with LOC only
                    pass

                score = loc + methods * 20
                cname = extract_class_name(f)
                candidates.append((cname, f, score, loc, methods))
            except Exception:
                continue

        candidates = [c for c in candidates if c[0]]
        candidates.sort(key=lambda x: x[2], reverse=True)
        return candidates

    def detect_god_classes(self, project_dir: str, top_n: int = 5):
        top_n = top_n or self.config.DETECTOR_TOP_N
        tool = (self.config.DETECTOR_TOOL or "heuristic").lower()

        # Try PMD if configured
        if tool == 'pmd' and self.config.PMD_PATH:
            try:
                cmd = [self.config.PMD_PATH, "-d", project_dir, "-f", "text", "-R", "category/java/design.xml"]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                output = proc.stdout + proc.stderr
                # PMD text output contains lines like: path:line: rule: message
                results = {}
                for line in output.splitlines():
                    parts = line.split(":")
                    if len(parts) >= 3:
                        path = parts[0]
                        cname = extract_class_name(path) if os.path.exists(path) else None
                        if cname:
                            results[cname] = results.get(cname, 0) + 1
                sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
                return [r[0] for r in sorted_results[:top_n]]
            except Exception:
                # fallback to heuristic
                pass

        # Default: heuristic
        candidates = self._heuristic_rank(project_dir)
        return [c[0] for c in candidates[:top_n]]

    def find_file_for_class(self, project_dir: str, class_name: str):
        files = get_all_java_files(project_dir)
        for f in files:
            if extract_class_name(f) == class_name:
                return f
        return None
