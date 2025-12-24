# Getting Started with RefAgent

Welcome! This guide will help you set up and run RefAgent in 5 minutes.

## ⏱️ 5-Minute Quick Start

### Step 1: Get API Key (2 min)
1. Go to https://console.groq.com/keys
2. Sign up (free) or log in
3. Create new API key
4. Copy key (looks like: `gsk_xxx...`)

### Step 2: Setup RefAgent (2 min)
```bash
# Clone repo
git clone https://github.com/yourusername/RefAgent.git
cd RefAgent

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirment.txt

# Copy example config
cp .env.example .env
```

### Step 3: Add Your Key (1 min)
Edit `.env`:
```
GROQ_API_KEY=gsk_YOUR_KEY_HERE
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.1-8b-instant
```

### Step 4: Prepare Project (variable)
```bash
cd projects/before
git clone https://github.com/apache/jclouds.git jclouds
cd ../..
```

### Step 5: Run! (variable)
```bash
python refAgent/RefAgent_main.py jclouds
```

Done! 🎉 Check `results/jclouds/` for refactored code.

---

## 📖 Detailed Setup

### Prerequisites Check
```bash
# Python 3.9 or higher?
python --version

# Git installed?
git --version

# Groq account created?
# Visit: https://console.groq.com
```

### Environment Setup

#### Option A: Virtual Environment (Recommended)
```bash
# Create
python -m venv .venv

# Activate (choose based on OS)
# Windows:
.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# Install
pip install -r requirment.txt

# Deactivate (when done)
deactivate
```

#### Option B: Conda Environment
```bash
conda create -n refagent python=3.9
conda activate refagent
pip install -r requirment.txt
```

#### Option C: Docker
```bash
docker build -t refagent:latest .
docker run -it \
  -e GROQ_API_KEY=gsk_xxx \
  -v $(pwd)/projects/before:/app/projects \
  -v $(pwd)/results:/app/results \
  refagent:latest \
  jclouds
```

### API Key Setup

#### Get Groq API Key
1. **Visit**: https://console.groq.com
2. **Sign up** (free tier available - 30 requests/minute)
3. **Go to**: "API Keys" section
4. **Click**: "Create API Key"
5. **Copy** the full key

#### Add to RefAgent
```bash
# Option 1: Edit .env file
cp .env.example .env
# Edit .env in your editor, replace gsk_YOUR_KEY with actual key

# Option 2: Environment variable
export GROQ_API_KEY=gsk_YOUR_KEY  # Linux/Mac
set GROQ_API_KEY=gsk_YOUR_KEY     # Windows CMD
$env:GROQ_API_KEY="gsk_YOUR_KEY"  # Windows PowerShell

# Option 3: Inline (for testing)
GROQ_API_KEY=gsk_xxx python refAgent/RefAgent_main.py jclouds
```

#### Verify Setup
```bash
python -c "
from settings import settings
print(f'Provider: {settings.LLM_PROVIDER}')
print(f'Model: {settings.GROQ_MODEL}')
print(f'API Key configured: {bool(settings.GROQ_API_KEY)}')
"
```

---

## 🔍 Your First Refactoring

### Example 1: Small Java Project

```bash
# Clone a small project
cd projects/before
git clone https://github.com/google/guava.git
cd ../..

# Run RefAgent
python refAgent/RefAgent_main.py guava

# Results in results/guava/
# Should complete in 5-10 minutes
```

### Example 2: Specific Target Class

```bash
# To refactor specific class (edit RefAgent_main.py)
# Line ~42, change:
# target_classes = detect_god_classes(project_path, top_n=5)
# to:
# target_classes = [{'name': 'YourClassName', 'file': 'path/to/Class.java'}]

python refAgent/RefAgent_main.py myproject
```

### Example 3: Using Different LLM

```bash
# Edit settings.py:
LLM_PROVIDER = 'openai'  # Change from 'groq'

# Ensure OpenAI key set:
export API_KEY=sk_xxx...

python refAgent/RefAgent_main.py jclouds
```

---

## 📊 Understanding Results

After running, check `results/project_name/`:

```
results/jclouds/
├── VirtualMachine/
│   ├── original_java_code.java      # Your original code
│   ├── improved_java_code.java      # Refactored version
│   └── metrics                      # Statistics
├── EC2HardwareBuilder/
│   ├── original_java_code.java
│   ├── improved_java_code.java
│   └── metrics
└── ...
```

### Metrics File Example
```json
{
  "original": {
    "lines_of_code": 245,
    "methods": 18,
    "complexity": 8.2
  },
  "improved": {
    "lines_of_code": 180,
    "methods": 12,
    "complexity": 5.1
  },
  "refactoring_suggestions": [
    "Extract method: parseConfiguration",
    "Create builder pattern",
    "Reduce cyclomatic complexity"
  ]
}
```

### Review Refactored Code
1. Open `improved_java_code.java`
2. Read RefactoringGenerator's suggestions (in comments)
3. Compare with `original_java_code.java`
4. Test in your IDE before committing

---

## ⚙️ Configuration

### Token Budgets
Adjust in `settings.py` for speed/quality tradeoff:

```python
# Faster, cheaper (default)
DEFAULT_MAX_TOKENS = 4096

# Slower, better quality
DEFAULT_MAX_TOKENS = 8192

# Very expensive, best quality
DEFAULT_MAX_TOKENS = 16384
```

### Model Selection
```python
# Fastest (default)
GROQ_MODEL = "llama-3.1-8b-instant"

# Better quality
GROQ_MODEL = "mixtral-8x7b-32768"

# Best quality (expensive)
GROQ_MODEL = "llama-3.1-70b-versatile"
```

### Iteration Limits
In `RefAgent_main.py` (line ~112):
```python
# More iterations = better refactoring but slower
for iteration in range(20):  # Max 20 iterations
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| `GROQ_API_KEY not found` | Ensure .env in RefAgent directory, run from there |
| `ModuleNotFoundError: groq` | Run `pip install -r requirment.txt` |
| `413 Request too large` | Use larger model, or edit settings to reduce token limit |
| `No Java files found` | Ensure project is in `projects/before/project_name/` |
| `Compilation failed` | Check Maven/JDK installed: `mvn --version` |
| `Rate limit (429)` | Wait 60 seconds or reduce DEFAULT_MAX_TOKENS |
| `Empty results` | No god classes detected - try larger project |

### Debug Mode
```bash
# Enable verbose logging
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('refAgent/RefAgent_main.py').read())
" jclouds
```

### Test LLM Connection
```bash
python -c "
from refAgent.GroqLLM import GroqLLM
llm = GroqLLM()
response = llm.query_llm(
    'What is Java?',
    model='llama-3.1-8b-instant',
    max_tokens=100
)
print(response)
"
```

---

## 📚 Next Steps

1. **Understand Architecture**: Read [README.md](README.md)
2. **See Code Examples**: Check `results/` from previous runs
3. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Report Issues**: Open GitHub issue with error details
5. **Advanced Config**: Edit `settings.py` for custom behavior

---

## 💡 Tips & Tricks

### Process Multiple Projects
```bash
for project in jclouds camel tomcat; do
  echo "Processing $project..."
  python refAgent/RefAgent_main.py $project
done
```

### Compare Before/After
```bash
# Save results before running again
cp -r results results.v1
python refAgent/RefAgent_main.py jclouds
# Compare: results.v1 vs results
```

### Use Generated Code
```bash
# Refactored code ready at:
projects/after/jclouds/

# Copy to your project:
cp projects/after/jclouds/src/main/java/com/VirtualMachine.java \
   ../my-jclouds-fork/src/main/java/com/VirtualMachine.java
```

### Schedule Runs
```bash
# Run daily analysis (Linux/Mac)
0 2 * * * cd /path/to/RefAgent && python refAgent/RefAgent_main.py jclouds

# Run weekly (Windows Task Scheduler)
# Trigger: Every Sunday at 2:00 AM
# Action: python.exe RefAgent_main.py jclouds
```

---

## 🆘 Getting Help

- 📖 **Read**: [README.md](README.md) for architecture
- 🔒 **Security**: See [SECURITY.md](SECURITY.md)
- 📝 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- 🗑️ **What Changed**: See [CHANGELOG.md](CHANGELOG.md)
- ❓ **Questions**: Open GitHub Discussions tab
- 🐛 **Bug Report**: Open GitHub Issues tab with error + steps

---

## 🎓 Learning Path

**Beginner:**
1. Complete this guide (you are here!)
2. Run on jclouds project
3. Review generated results

**Intermediate:**
1. Try different projects
2. Adjust settings.py parameters
3. Compare model outputs

**Advanced:**
1. Add custom refactoring rules
2. Integrate into CI/CD pipeline
3. Extend to other languages (Python, C#)

---

**Happy refactoring! 🚀**

Questions? Start a discussion: https://github.com/yourusername/RefAgent/discussions
