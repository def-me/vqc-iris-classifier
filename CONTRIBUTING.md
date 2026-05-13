# Contributing to VQC Iris Classifier

Thank you for your interest in contributing! Here are guidelines for contributing to this project.

## Code of Conduct

Be respectful and inclusive to all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title describing the bug
   - Detailed description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS information

### Suggesting Enhancements

1. Check if the enhancement has been suggested already
2. Create an issue with:
   - Clear title and description
   - Use case and motivation
   - Possible implementation approach (if applicable)

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write or update tests
5. Run tests: `pytest tests/ -v`
6. Ensure code is formatted: `black . --line-length=120`
7. Check imports: `isort .`
8. Commit: `git commit -m 'Add my feature'`
9. Push: `git push origin feature/my-feature`
10. Create a Pull Request with description

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/vqc-iris-classifier.git
cd vqc-iris-classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with extras
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black . --line-length=120
isort .

# Check code quality
flake8 .
