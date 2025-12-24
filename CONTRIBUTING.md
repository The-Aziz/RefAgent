# Contributing to RefAgent

Thank you for considering contributing to RefAgent! This document provides guidelines and instructions for getting involved.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions. We're building this together!

## How to Contribute

### Reporting Bugs

Found a bug? Please open an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, GPU info)
- Stack trace/logs if applicable

**Example**:
```
Title: "Error 413 with large Java files"
Description: When processing VirtualMachine.java (2700+ lines), 
the system fails with "Request too large" error.
Steps: 1. Clone jclouds 2. Run RefAgent 3. Select VirtualMachine
Expected: Truncates file and processes successfully
Actual: Crashes with 413 error
```

### Suggesting Enhancements

Have an idea? Open an issue with:
- Clear description of the improvement
- Why it would be useful
- Possible implementation approach
- Relevant examples

**Ideas we'd love**:
- Better god-class detection algorithms (PMD/JDeodorant)
- Support for Python, C#, Go codebases
- Plugin architecture for custom refactoring rules
- Web UI for easier project management
- Performance optimizations

### Submitting Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/RefAgent.git
   cd RefAgent
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make your changes**
   - Follow PEP 8 style guide
   - Add type hints where possible
   - Keep functions focused and well-documented

4. **Test thoroughly**
   ```bash
   # Install dev dependencies
   pip install -r requirment.txt pytest pylint
   
   # Run tests
   pytest tests/
   
   # Check code quality
   pylint refAgent/ --disable=C0111,W0612
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Fix: Handle encoding errors in Windows file parsing
   
   - Added UTF-8 with latin-1 fallback in parse_java_code()
   - Fixes #42
   - Tested on Windows 10 with special characters"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub with:
   - Clear description of changes
   - Link to related issues (fixes #123)
   - Before/after screenshots if applicable
   - Test results

## Development Setup

### Local Environment
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Install all dependencies
pip install -r requirment.txt

# Optional: Install dev tools
pip install pytest pylint black
```

### Project Structure
```
refAgent/
├── detector.py           # God-class detection
├── agents.py             # Multi-agent orchestration
├── dependency_graph.py   # Dependency analysis
├── RefAgent_main.py      # Main entry point
├── GroqLLM.py           # Groq provider
├── OpenaiLLM.py         # OpenAI provider
└── ...
```

### Adding New Features

**Example: Add a new refactoring agent**

```python
# In refAgent/agents.py
class NewRefactoringAgent(BaseAgent):
    """Custom refactoring for specific patterns"""
    
    def analyze(self, code: str) -> Dict[str, str]:
        """Analyze code and return refactoring suggestions"""
        prompt = f"""Refactor this code focusing on [specific pattern]:
        {code}
        Return: JSON with keys 'suggestions' and 'refactored_code'"""
        return self.llm.query(prompt)

# In RefAgent_main.py
new_agent = NewRefactoringAgent(provider='groq')
suggestions = new_agent.analyze(target_code)
```

**Example: Improve god-class detection**

```python
# In refAgent/detector.py
def enhanced_heuristic_rank(classes):
    """Score classes with additional metrics"""
    scores = {}
    for class_info in classes:
        score = (
            class_info['loc'] +  # Lines of code
            (class_info['methods'] * 20) +  # Method count
            (class_info['fields'] * 5) +  # Field count
            (class_info['cyclomatic_complexity'] * 2)  # Complexity
        )
        scores[class_info['name']] = score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

## Code Style Guide

### Python
- Follow **PEP 8** (use `black` formatter)
- Type hints for all functions
- Docstrings for classes and complex methods
- Max line length: 100 characters

```python
# Good
def detect_god_classes(project_path: str, top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Detect god classes in a Java project.
    
    Args:
        project_path: Path to Java project root
        top_n: Number of top classes to return
        
    Returns:
        List of god class metadata sorted by score
    """
```

### Java
- Follow Google Java Style Guide
- Use meaningful variable names
- Add Javadoc for public methods

## Testing

We use pytest for unit tests.

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_detector.py

# Run with coverage
pytest --cov=refAgent

# Run specific test
pytest tests/test_agents.py::TestPlanner::test_analyze_methods
```

### Writing Tests
```python
# tests/test_detector.py
import unittest
from refAgent.detector import detect_god_classes

class TestDetector(unittest.TestCase):
    def test_detect_empty_project(self):
        result = detect_god_classes("empty_project/")
        self.assertEqual(result, [])
    
    def test_score_calculation(self):
        # Test LOC + (methods * 20) formula
        result = detect_god_classes("test_project/")
        self.assertGreater(result[0]['score'], 0)
```

## Documentation

Help us improve docs!

- Found an unclear section? Improve it
- Have a use-case example? Share it
- API documentation missing? Add it

```bash
# Run locally to see changes
# (if we add Sphinx/MkDocs in future)
```

## Performance Optimization

Areas we're optimizing:

- **Bundle size**: Reduce context sent to LLM
- **Token usage**: Implement smart chunking
- **Compilation time**: Cache compilation results
- **API calls**: Batch requests where possible

If you have ideas for speedups, please share!

## Debugging Tips

### Enable verbose logging
```bash
# In RefAgent_main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test specific class
```bash
python -c "
from refAgent.RefAgent_main import main
main('project_name', target_class='YourClassName')
"
```

### Check dependency graph
```bash
python -c "
from refAgent.dependency_graph import extract_neighbors
neighbors = extract_neighbors('path/to/graph.json', 'ClassName')
print(neighbors)
"
```

## Release Process

1. Update version in `settings.py`
2. Update `CHANGELOG.md` with changes
3. Create annotated tag: `git tag -a v0.2.0 -m "Version 0.2.0"`
4. Push to GitHub: `git push origin --tags`
5. GitHub Actions will build and publish

## Questions?

- 📖 Check [README.md](README.md)
- 🔍 Search existing [issues](https://github.com/yourusername/RefAgent/issues)
- 💬 Open a [discussion](https://github.com/yourusername/RefAgent/discussions)
- 📧 Contact maintainers

---

**Thank you for contributing! 🎉**
