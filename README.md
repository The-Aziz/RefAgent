# RefAgent - Automated Java Code Refactoring with LLMs

An intelligent multi-agent system for **detecting and refactoring God Classes** in Java projects using Large Language Models (LLMs).

## 🎯 Overview

RefAgent automatically identifies problematic classes in Java codebases and applies iterative refactoring through a 4-agent feedback loop.

**Key Innovation**: Uses smart god-class detection + dependency extraction to reduce token usage by **50-100x** compared to whole-codebase approaches, and **10x cheaper** than GPT-4.

## ✨ Key Features

- 🔍 **Automated God-Class Detection**: Identifies classes with high code smell metrics using heuristic ranking
- 🧠 **4-Agent Architecture**: 
  - **Planner**: Analyzes code and suggests improvements
  - **Generator**: Refactors code based on plan
  - **Compiler**: Validates compilation
  - **Tester**: Runs and validates tests
- 💰 **Cost-Optimized**: Uses Groq LLM (0.07¢ per 1M tokens) instead of GPT-4 ($30 per 1M)
- 🔄 **Iterative Feedback**: Up to 20 refinement iterations with compiler/test feedback
- 📊 **Detailed Results**: Original code, refactored code, and metrics per class
- 🌍 **Multi-Provider Support**: Groq (recommended) and OpenAI

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- Groq API key (free: https://console.groq.com)

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/RefAgent.git
cd RefAgent

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirment.txt
```

### 2. Configure Credentials
```bash
# Copy template
cp .env.example .env

# Edit .env with your Groq API key
# Get key from: https://console.groq.com/keys
```

Example `.env`:
```
GROQ_API_KEY="gsk_YOUR_KEY_HERE"
LLM_PROVIDER="groq"
GROQ_MODEL="llama-3.1-8b-instant"
```

### 3. Prepare Java Project
```bash
cd projects/before
git clone https://github.com/apache/jclouds.git jclouds
cd ../..
```

### 4. Run RefAgent
```bash
python refAgent/RefAgent_main.py jclouds
```

### 5. Review Results
```
results/jclouds/
├── VirtualMachine/
│   ├── original_java_code.java
│   ├── improved_java_code.java
│   └── metrics
└── EC2HardwareBuilder/
    ├── original_java_code.java
    └── ...

projects/after/jclouds/  # Refactored code ready for compilation
```

## 📚 Architecture

### God-Class Detection Algorithm
```
Input: Java Project
  ↓
Scan all classes
  ↓
Score each: LOC + (method_count × 20)
  ↓
Return: Top N god classes sorted by score
```

### Refactoring Pipeline
```
For each god class:
  ├─ Extract dependency neighborhood
  ├─ Truncate large files (>50KB)
  ├─ Planner analyzes code → suggestions
  ├─ Loop up to 20 iterations:
  │  ├─ Generator refactors code
  │  ├─ Compiler validates (if fail → feedback)
  │  ├─ TestAgent runs tests (if fail → feedback)
  │  └─ Success → save results
  └─ Output: original + refactored code
```

## 🔧 Configuration

### settings.py Options

```python
# How many god classes to process
DETECTOR_TOP_N: int = 5

# Token limits (lower = faster/cheaper)
DEFAULT_MAX_TOKENS: int = 8192
REFRACTORING_GENERATOR_MAX_TOKENS: int = 8192
PLANNER_MAX_TOKENS: int = 4096
COMPILER_MAX_TOKENS: int = 4096
TEST_MAX_TOKENS: int = 4096

# LLM Provider
LLM_PROVIDER: str = 'groq'
GROQ_MODEL: str = 'llama-3.1-8b-instant'
```

### Model Selection

| Model | Speed | Quality | Context | Cost | Best For |
|-------|-------|---------|---------|------|----------|
| llama-3.1-8b-instant | ⚡⚡⚡ | ⭐⭐⭐ | 8K | $0.07 | Default choice |
| mixtral-8x7b-32768 | ⚡⚡ | ⭐⭐⭐⭐ | 32K | $0.27 | Large classes |
| llama-3.1-70b-versatile | ⚡ | ⭐⭐⭐⭐⭐ | 8K | $0.59 | Maximum quality |

## 📁 Project Structure

```
RefAgent/
├── refAgent/
│   ├── detector.py              # God-class detection logic
│   ├── dependency_graph.py      # Dependency analysis
│   ├── agents.py                # 4-agent framework
│   ├── RefAgent_main.py         # Main orchestrator
│   ├── GroqLLM.py               # Groq API wrapper
│   ├── OpenaiLLM.py             # OpenAI API wrapper
│   └── ...
├── settings.py                  # Configuration
├── utilities.py                 # Helpers
├── .env.example                 # Configuration template (copy to .env)
├── .gitignore                   # Git ignore (no .env!)
└── requirment.txt               # Dependencies
```

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- [ ] PMD/JDeodorant integration for detection
- [ ] Support other languages (Python, C#)
- [ ] Improved refactoring patterns library
- [ ] Better test case generation
- [ ] Performance optimizations
- [ ] More documentation

### Development

```bash
# Install
pip install -r requirment.txt

# Test
pytest tests/

# Code quality
pylint refAgent/
```

## ⚠️ Limitations

- Large files (>2000 lines) are truncated to prevent token overflow
- Requires Maven/Gradle for compilation testing
- Java-specific (extensible to other languages)
- API rate limits apply

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| "413 Request too large" | Use larger model or reduce MAX_CODE_SIZE |
| "GROQ_API_KEY not found" | Ensure .env in RefAgent directory |
| "Project not found" | Clone to projects/before/{name} |
| ModuleNotFoundError | Run pip install -r requirment.txt |


## 💬 Support

- Open an issue for bugs/feature requests
- Discussions for questions
- See CONTRIBUTING.md for guidelines

---

## 🙏 Credits & Acknowledgments

This project is built upon and significantly extends the **original RefAgent repository** by anonymAgent.

**Original Project:**
- Repository: [anonymAgent/RefAgent](https://github.com/anonymAgent/RefAgent)
- Original concept: Multi-agent LLM-based framework for automatic software refactoring

**Key Enhancements in This Fork:**
- ✨ Automated god-class detection with heuristic ranking
- 💰 Integrated Groq LLM provider (100x cheaper than GPT-4)
- 🧠 Token optimization and aggressive context pruning
- 📚 Comprehensive documentation (6 guides + checklist)
- 🔄 Multi-provider architecture (Groq + OpenAI)
- 🎯 Focused neighborhood extraction for targeted refactoring
- 🔐 Security hardening and credential protection
---

**⭐ Star us if you find this useful!**
    Fill in the required API keys before running the framework.

    > ✅ If you want to use the framework with **DeepSeek models**, set `MODEL_NAME` to either `deepseek-coder` or `deepseek-chat`.  
    > The endpoint for DeepSeek is:  
    > `https://api.deepseek.com/v1/chat/completions`

2. **Hardware**:
   - Ideally runs on a **GPU** for efficiency
   - If using **open-source LLMs** (e.g., StarCoder, DeepSeek), ensure you are running with GPU support

# RefAgent — Multi-agent LLM-based Refactoring Framework

RefAgent is a multi-agent system that uses Large Language Models (LLMs) to analyze, suggest, and apply refactorings to Java projects. The pipeline can clone a repository tag, apply model-guided refactorings, compile and test, and optionally commit improvements back to the repository.

This README gives a compact, practical guide to set up and run the project.

---

## Quick start

- Run the full pipeline (clone → build → refactor):

```bash
./run_refAgent.sh <org/repo-name> <tag>
# e.g. ./run_refAgent.sh apache/maven v3.8.6
```

- Or run the Python pipeline directly when the project is already present in `projects/after/`:

```bash
python3 refAgent/RefAgent_main.py <project-name>
# e.g. python3 refAgent/RefAgent_main.py jclouds
```

---

## Prerequisites

- Python 3.9+
- Java (JDK) compatible with the target project
- Maven installed and on PATH (or the project's `mvnw` wrapper)
- Git
- LLM API credentials (OpenAI or another adapter supported by `refAgent/OpenaiLLM.py`)

Recommended Java versions
- For best compatibility with the built-in Python parser (`javalang`) and the tooling in this repo,
  we recommend using Java 8, 9, or 12 for projects you plan to analyze and refactor. If your project
  uses newer Java language features (post-Java 12), consider using a Java-based parser (e.g. JavaParser)
  or building with the project's `mvnw` wrapper and double-checking parsing results.

Important note about CompilerAgent & TestAgent
- The `CompilerAgent` and `TestAgent` are agents whose sole purpose is to compile and run
   Maven-based Java projects. They do not modify environment settings or install toolchains.
- It is critical that the Java (JDK) version and the Maven version (or the project's `mvnw` wrapper)
   exactly match what the target project expects. Mismatched Java/Maven versions are the most
   common cause of build and test failures and can produce misleading LLM diagnostics.
- The provided `run_refAgent.sh` performs a basic verification, but you should always confirm the
   JDK and Maven versions locally before running RefAgent. If the project provides `mvnw`,
   prefer using it (see Troubleshooting below).

Optional: GPU when running large local models.

## Configuration (.env)

Create a `.env` file in the repository root (read by `settings.py`):

```env
API_KEY="<your-llm-api-key>"
GITHUB_API_KEY="<your-github-token>"  # optional, used for commits
MODEL_NAME="gpt-4"
```

The `Settings` class (in `settings.py`) reads `.env` automatically.

## Install dependencies

Install Python dependencies into a virtualenv and activate it:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirment.txt
```

Note: the repository currently includes `requirment.txt` (typo preserved). Rename to `requirements.txt` if you prefer standard naming and update commands accordingly.

## How it works (high level)

- The main pipeline (`refAgent/RefAgent_main.py`) iterates over Java files in `projects/before/<project>`.  

- New targeted mode: RefAgent can run in a god-class-targeted mode where an external detector (PMD/Deodorant/FindBugs) or a local heuristic selects candidate "god classes". The pipeline then extracts the detected class plus its dependency neighborhood (incoming & outgoing neighbors) and runs a focused planner → refactoring generator → compile/test feedback loop on that compact bundle (avoids sending the entire codebase to the LLM). Configure with `.env` (`DETECTOR_TOOL`, `PMD_PATH`, `DETECTOR_TOP_N`).
- Agents:
   - `PlannerAgent`: decides which methods need refactoring based on CKOO metrics.
   - `RefactoringGeneratorAgent`: asks the LLM to produce refactored Java code following the plan.
   - `CompilerAgent`: compiles the Maven project and asks the LLM to summarize compilation errors when compilation fails.
   - `TestAgent`: runs Maven tests, summarizes failing tests per-test, and can combine all failures into a single LLM-produced summary.
- Summaries from compiler/test failures are appended in-memory to `refactoring_generator.llm.message_history` so the `refactoring_generator` includes them as context in subsequent calls.

## Useful scripts

- `run_refAgent.sh <org/repo> <tag>` — clones the repo tag, copies to `projects/after/`, builds, and runs the Python pipeline. The script resolves its own directory so it reliably finds `refAgent/RefAgent_main.py`.

## Troubleshooting

- Can't find `RefAgent_main.py` from the shell script:
   - Ensure the script is executable (`chmod +x run_refAgent.sh`). The script now computes its own directory and runs the Python file by absolute path.
- Maven build issues:
   - Check Java version compatibility with the target project. Prefer using the project's `mvnw` wrapper where available.
   - Reminder: because `CompilerAgent` and `TestAgent` only invoke the build/test tools, they cannot
      recover from an incompatible JDK or Maven version. If you see cryptic compile errors, first verify
      you are using the correct Java and Maven versions that are known to build the project locally.
      The `.sh` script performs a basic check, but you should double-check manually with `java -version`
      and `mvn -v` (or `./mvnw -v`).
- LLM failures or rate limits:
   - Verify `.env` API keys and quotas.

## Development notes & suggestions

- Message history and context:
   - The current design keeps summaries in-memory per-agent (`OpenaiLLM.message_history`). If you want summaries available to multiple agents, either append the summary to each agent's history or use a shared LLM wrapper instance.
   - If you want summaries to persist across runs, save them into `results/<project>/` and reload them when the pipeline starts.


## License

MIT
