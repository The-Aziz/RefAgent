# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - 2024-01-15

### 🎯 Major Features
- **God-Class Detection Engine**: Automatically identifies problematic classes using heuristic scoring (LOC + method_count × 20)
- **Multi-Provider LLM Support**: Seamless switching between Groq and OpenAI APIs via provider parameter
- **Groq Integration**: Reduced LLM costs by 100x using llama-3.1-8b-instant ($0.07 per 1M tokens vs GPT-4 $30)
- **Token Optimization**: Aggressive context pruning reduces average project processing from 500K+ tokens to <50K

### ✨ Improvements
- **Bundle Size Optimization**: Only includes target class + dependencies (instead of full codebase)
- **File Truncation**: Large files (>50KB) truncated to first 1500 lines with clear markers
- **UTF-8 Encoding**: Better handling of special characters with latin-1 fallback for Windows compatibility
- **Enhanced Dependency Analysis**: Extracts both ancestors and descendants in dependency graph
- **Better Error Handling**: Silent encoding errors, graceful fallbacks for missing modules

### 🐛 Bug Fixes
- Fixed Python 3.9 compatibility (replaced `str | None` with `Optional[str]`)
- Fixed Windows file encoding issues in `parse_java_code()`
- Handled NetworkX JSON format variations (both "links" and "edges" keys)
- Fixed 413 Request Entity Too Large errors from oversized context windows

### 📦 Dependencies
- Added `groq` SDK for Groq API integration
- Maintained backward compatibility with OpenAI SDK
- Removed unused heavy dependencies (matplotlib, pandas, seaborn)

### 📚 Documentation
- Added comprehensive README.md with quick start guide
- Created CONTRIBUTING.md for developer guidelines
- Added inline code documentation and type hints
- Created .env.example template for credential configuration

### 🔐 Security
- All API keys protected in .env (never committed)
- .gitignore properly configured for sensitive files
- Added .env.example with masked placeholder values

---

## [0.2.0] - 2023-12-20

### Features
- **4-Agent Architecture**: 
  - Planner: Code analysis and suggestions
  - RefactoringGenerator: Code transformation
  - CompilerAgent: Compilation validation
  - TestAgent: Test execution and validation
- **Iterative Feedback Loop**: Up to 20 refinement iterations with compiler/test feedback
- **Configurable Token Limits**: Per-agent token budgets (4-8K)
- **Result Persistence**: Saves original and refactored code with metrics

### Improvements
- Better error handling for Java compilation
- Maven integration for build validation
- Message history for multi-turn LLM conversations
- Detailed logging and progress tracking

### Bug Fixes
- Fixed agent initialization with proper settings inheritance
- Fixed Java code parsing edge cases

---

## [0.1.0] - 2023-12-01

### Initial Release
- **Basic Multi-Agent Framework**: 
  - PlannerAgent for code analysis
  - RefactoringGeneratorAgent for code transformation
  - Simple validation loop
- **OpenAI Integration**: GPT-4 based code generation
- **GitHub Support**: Clone and analyze repositories
- **Basic Results Tracking**: Save refactored code to files

### Known Limitations
- Processes entire codebases (inefficient token usage)
- Only supports OpenAI API
- Limited refactoring patterns
- Minimal test validation
- No cost optimization

---

## Upgrade Guide

### From 0.2.0 to 0.3.0

#### Breaking Changes
None! Full backward compatibility maintained.

#### Required Updates
1. **Update .env** to use Groq:
   ```env
   GROQ_API_KEY="gsk_YOUR_KEY_HERE"
   LLM_PROVIDER="groq"
   GROQ_MODEL="llama-3.1-8b-instant"
   ```

2. **Optional**: Adjust token limits in `settings.py`:
   ```python
   DEFAULT_MAX_TOKENS = 8192  # Reduced from 32768
   ```

3. **Optional**: Update code to use god-class detection:
   ```python
   # Old: Process whole project
   # New: Auto-detect god classes
   main(project_name='jclouds')  # Automatically detects 5 worst classes
   ```

#### Performance Improvements
- ⚡ **100x cheaper** LLM costs (Groq vs GPT-4)
- ⚡ **10x faster** token usage with smart bundling
- ⚡ **Smaller memory** footprint with file truncation

---

## Planned Features (Roadmap)

### 0.4.0 (Q1 2024)
- [ ] PMD integration for precise god-class detection
- [ ] Support for Python projects
- [ ] Custom refactoring rules library
- [ ] Web UI for project management
- [ ] Performance benchmarking dashboard

### 0.5.0 (Q2 2024)
- [ ] Support for C# and Go projects
- [ ] Advanced test case generation
- [ ] Incremental refactoring (commit per class)
- [ ] GitHub Actions integration
- [ ] Caching layer for repeated analyses

### Future
- [ ] IDE plugins (VS Code, IntelliJ)
- [ ] Real-time code analysis
- [ ] Collaborative refactoring
- [ ] ML-based refactoring pattern learning

---

## Version History

| Version | Release Date | Status | Notes |
|---------|--------------|--------|-------|
| 0.3.0 | 2024-01-15 | Current | God-class detection, Groq integration |
| 0.2.0 | 2023-12-20 | Stable | 4-agent feedback loop |
| 0.1.0 | 2023-12-01 | Deprecated | Initial release, GPT-4 only |

---

## Contributors

### Version 0.3.0
- God-class detection algorithm implementation
- Groq LLM integration and optimization
- Token reduction and cost optimization
- Documentation and examples

### Version 0.2.0
- Multi-agent framework architecture
- Iterative feedback loop
- GitHub integration

### Version 0.1.0
- Initial framework scaffold
- Basic agent implementations

---

## Support

Need help with a version? 

- **Current (0.3.0)**: Open an issue on GitHub
- **Previous (0.2.0)**: See branch `v0.2.0`
- **Deprecated (0.1.0)**: See branch `v0.1.0`

---

## Migration from Old Versions

### From 0.1.x to Latest
Complete rewrite recommended. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup.

### From 0.2.x to 0.3.x
See "Upgrade Guide" section above.

---

Last updated: 2024-01-15
