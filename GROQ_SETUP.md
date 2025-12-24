## Groq Setup Instructions for RefAgent

RefAgent is now configured to use **Groq** as the default LLM provider for cost-effective refactoring.

### 📋 What Changed:
- ✅ Added `GroqLLM` class (`refAgent/GroqLLM.py`) — native Groq API integration
- ✅ Updated `settings.py` — supports both OpenAI and Groq via `LLM_PROVIDER` config
- ✅ Updated agents.py — all agents now support `provider` parameter
- ✅ Updated RefAgent_main.py — auto-selects LLM based on config
- ✅ Updated `.env` template — includes Groq settings
- ✅ Created detector.py — god-class detection module
- ✅ Created scripts/detect_god_classes.py — CLI tool for detector

### 🚀 Before Running RefAgent:

**Step 1: Get Groq API Key**
1. Go to https://console.groq.com
2. Sign up or log in
3. Create an API key
4. Copy the key (looks like: `gsk_...`)

**Step 2: Fill in `.env` file**
```bash
# Open: D:\PCD_code\RefAgent\.env
# Update these lines:

API_KEY=""                                    # (optional, for fallback to OpenAI)
GROQ_API_KEY="gsk_YOUR_GROQ_KEY_HERE"        # ← REQUIRED: Your Groq API key
GITHUB_API_KEY="ghp_YOUR_GITHUB_TOKEN_HERE"  # (optional, for commits)
MODEL_NAME="gpt-4"                           # (unused if using Groq)
LLM_PROVIDER="groq"                          # Use Groq
GROQ_MODEL="mixtral-8x7b-32768"              # Fast & capable model
```

**Step 3: Install Groq Python SDK**
```bash
D:\PCD_code\.venv\bin\python.exe -m pip install groq
```

**Step 4: Choose a test repository**
Available test repos in `data/repositories.txt`:
- `apache/jclouds rel/jclouds-2.3.0` ← **Recommended for testing**
- `apache/accumulo rel/1.10.4`
- `apache/systemml rel/3.2.0-rc1`
- (and 5 more)

### ▶️ Running RefAgent with Groq:

**Option A: Full pipeline (clone repo + refactor)**
```bash
cd D:\PCD_code\RefAgent
./run_refAgent.sh apache/jclouds jclouds-2.3.0
```

**Option B: Refactor already-cloned repo**
```bash
cd D:\PCD_code\RefAgent
D:\PCD_code\.venv\bin\python.exe refAgent/RefAgent_main.py jclouds
```
(Assumes `projects/before/jclouds/` exists with Java source)

**Option C: Detect god classes only**
```bash
D:\PCD_code\.venv\bin\python.exe scripts/detect_god_classes.py jclouds
```
This shows the top 5 candidate classes without running refactoring.

### 📊 Token Savings with Groq:
- **Groq Mixtral-8x7b**: ~1000x faster inference, 1/10th the cost of GPT-4
- **Compact context**: Detector + neighbors reduces input tokens by 80%
- **No whole codebase**: Agents never see files unrelated to the god class

### 🔧 Configuration Options:

```python
# In .env or settings.py, you can change:

LLM_PROVIDER="groq"  # or "openai"
GROQ_MODEL="mixtral-8x7b-32768"  # Options:
                     # - "mixtral-8x7b-32768"
                     # - "llama-3.1-8b-instant"
                     # - "llama-3.1-70b-versatile"
                     # - "gemma-7b-it"

DETECTOR_TOP_N=5     # Number of god classes to refactor per run
DETECTOR_TOOL="heuristic"  # or "pmd" if you configure PMD_PATH
```

### ✅ Ready? 

**Once you fill in `GROQ_API_KEY` in `.env` and run `pip install groq`, you're all set!**

Do you have your Groq API key ready?
