# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, **please do NOT open a public GitHub issue**. Instead:

1. **Email**: Send details to the maintainers privately
2. **Do not share**: Don't post exploits or detailed vulnerability info publicly
3. **Timeline**: We'll aim to patch within 48 hours of report

### What to Include
- Vulnerability description
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

---

## Security Best Practices

### 1. API Keys & Credentials

⚠️ **NEVER commit API keys, tokens, or passwords!**

**Protect your .env file:**
```bash
# .env is in .gitignore (protected)
# Copy .env.example instead:
cp .env.example .env

# Never commit .env
git add .env.example  ✅
git add .env          ❌ (blocked by .gitignore)
```

**If you accidentally exposed a key:**
1. Regenerate it immediately in provider console
2. Rotate all credentials
3. Scan git history for exposure
```bash
git log --all --oneline -- .env  # Check if ever committed
```

### 2. Code Injection Prevention

RefAgent processes **untrusted Java code** from repositories. Security measures:

✅ **Safe Practices:**
- Code analysis only (no execution of user input)
- LLM prompts properly formatted (no prompt injection)
- Compilation runs in isolated Maven environment
- Tests run with Maven sandboxing

⚠️ **Caution Areas:**
- Compiling untrusted Java (use Docker in production)
- Executing generated code (validate first)
- Large file processing (DOS prevention via truncation)

### 3. API Rate Limiting

RefAgent makes requests to Groq/OpenAI APIs. Safeguards:

- **Token limits**: Per-agent budgets (4-8K tokens)
- **Bundle size**: Limited context to reduce API payloads
- **Retry logic**: Exponential backoff (see `GroqLLM.py`)
- **Timeout**: 30-second request timeout

**To avoid rate limits:**
```python
# settings.py - Adjust these if getting 429 errors:
DEFAULT_MAX_TOKENS = 4096  # Reduce if rate-limited
MAX_CODE_SIZE = 50000  # Limit file sizes
```

### 4. File System Safety

RefAgent writes to local directories:

✅ **Protected:**
- Results written to `results/` (safe location)
- Project clone to `projects/before/` (isolated)
- Refactored code to `projects/after/` (reviewed before use)

⚠️ **Caution:**
- Check `results/` before committing (may contain sensitive code)
- Don't run RefAgent on private repositories you don't own
- Review generated code before applying to production

### 5. Dependency Security

All dependencies should be kept up-to-date:

```bash
# Check for vulnerable dependencies
pip list --outdated

# Update dependencies
pip install --upgrade -r requirment.txt

# Security audit
pip install safety
safety check
```

**Critical dependencies:**
- `groq`: Official Groq SDK
- `openai`: Official OpenAI SDK
- `javalang`: Java parser (vetted)
- `networkx`: Graph analysis (stable)

---

## Container Security (Production)

If running RefAgent in production, use containers:

```dockerfile
# Dockerfile.secure
FROM python:3.11-slim

# Don't run as root
RUN useradd -m refagent
USER refagent

# Install dependencies only
COPY requirment.txt .
RUN pip install --no-cache-dir -r requirment.txt

# Mount volumes (readonly for source, writeonly for results)
VOLUME ["/app/projects:ro", "/app/results:rw"]

ENTRYPOINT ["python", "-m", "refAgent.RefAgent_main"]
```

```bash
# Run securely with limited resources
docker run \
  --memory=2g \
  --cpus=2 \
  --pids-limit=100 \
  -v $(pwd)/projects/before:/app/projects:ro \
  -v $(pwd)/results:/app/results:rw \
  --env-file .env \
  refagent:latest jclouds
```

---

## Secure API Usage

### Groq API (Current Primary)

**Security considerations:**
- API key transmitted over HTTPS ✅
- Key in environment variable (not hardcoded) ✅
- Rate limiting by Groq protects against abuse ✅

**To rotate key:**
```bash
# 1. Generate new key in console.groq.com
# 2. Update .env
GROQ_API_KEY="gsk_NEW_KEY_HERE"

# 3. Test connection
python -c "from refAgent.GroqLLM import GroqLLM; llm = GroqLLM()"

# 4. Delete old key from console
```

### OpenAI API (Fallback)

**Equivalent security practices apply.**

**Cost control:**
```python
# Prevent runaway costs
DEFAULT_MAX_TOKENS = 4096  # Strict limit
TIMEOUT = 30  # seconds
```

---

## Data Privacy

### What Data We Collect

RefAgent **does NOT** collect analytics. However:

- ✅ **Local only**: All analysis happens locally
- ⚠️ **Sent to LLM**: Source code sent to Groq/OpenAI for analysis
- ⚠️ **Review vendor policies**:
  - Groq: https://console.groq.com/terms
  - OpenAI: https://openai.com/privacy

### What You Control

- **Code privacy**: You choose what projects to analyze
- **Data retention**: You control .env, results/ directories
- **API choice**: Pick provider (Groq vs OpenAI)
- **Deletion**: Delete results/ anytime

---

## Known Vulnerabilities & Mitigations

### Current Version (0.3.0)

| Issue | Severity | Mitigation |
|-------|----------|-----------|
| Code sent to LLM | Medium | Use Groq (private deployment) or on-premises LLM |
| File truncation | Low | Truncated files marked clearly, user reviews results |
| No code signing | Low | Verify releases from trusted source |

---

## Security Testing Checklist

Before deploying RefAgent:

- [ ] .env file NOT committed to git
- [ ] .env.example contains only placeholder values
- [ ] API keys rotated if ever exposed
- [ ] Dependencies up-to-date (`pip list --outdated`)
- [ ] No hardcoded secrets in code
- [ ] Review generated code before using in production
- [ ] Test with non-sensitive project first
- [ ] Network isolation if processing private code

---

## Questions & Responsible Disclosure

- 🔒 Security concerns? Email maintainers privately
- 📋 Have a patch? Open a PR with `[SECURITY]` prefix
- 📚 Want to audit our code? Welcome! See CONTRIBUTING.md

---

**Last Updated**: 2024-01-15

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [API Security](https://owasp.org/www-community/API_Security)
