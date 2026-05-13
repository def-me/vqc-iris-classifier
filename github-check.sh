#!/bin/bash
# GitHub Publishing Checklist
# Run this script to verify everything is ready for GitHub

echo "=================================="
echo "VQC Iris Classifier - GitHub Checklist"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1"
        ((FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1/"
        ((FAILED++))
    fi
}

echo "📋 Checking Project Structure..."
echo ""

# Root files
echo "Core Files:"
check_file "vqc_iris.py"
check_file "requirements.txt"
check_file "setup.py"
check_file "pyproject.toml"

echo ""
echo "Documentation:"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "CONTRIBUTING.md"
check_file "CONTRIBUTORS.md"
check_file "CHANGELOG.md"
check_file "SECURITY.md"
check_file "LICENSE"

echo ""
echo "Configuration:"
check_file ".gitignore"
check_file ".gitattributes"
check_file ".pre-commit-config.yaml"
check_file "Makefile"

echo ""
echo "Docker:"
check_file "Dockerfile"
check_file "docker-compose.yml"

echo ""
echo "Directories:"
check_dir ".github"
check_dir "tests"
check_dir "notebooks"

echo ""
echo "GitHub Configuration:"
check_file ".github/workflows/ci.yml"
check_file ".github/CODEOWNERS"
check_file ".github/dependabot.yml"
check_file ".github/pull_request_template.md"
check_dir ".github/ISSUE_TEMPLATE"

echo ""
echo "Test Files:"
check_file "tests/__init__.py"
check_file "tests/test_circuit.py"
check_file "tests/test_data.py"
check_file "tests/test_model.py"

echo ""
echo "Notebooks:"
check_file "notebooks/vqc_exploration.ipynb"

echo ""
echo "=================================="
echo "Pre-commit Actions"
echo "=================================="
echo ""

# Check if pre-commit is installed
if command -v pre-commit &> /dev/null; then
    echo -e "${GREEN}✓${NC} pre-commit is installed"
    ((PASSED++))
else
    echo -e "${YELLOW}ℹ${NC} pre-commit not installed (optional)"
    echo "  Install with: pip install pre-commit"
fi

echo ""
echo "=================================="
echo "Code Quality Checks"
echo "=================================="
echo ""

# Check if pytest is available
if python -m pytest --version &> /dev/null; then
    echo -e "${GREEN}✓${NC} pytest is available"
    echo "  Running tests..."
    python -m pytest tests/ -q
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} All tests passed"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} Some tests failed"
        ((FAILED++))
    fi
else
    echo -e "${YELLOW}ℹ${NC} pytest not available (optional)"
fi

echo ""
echo "=================================="
echo "Next Steps for GitHub"
echo "=================================="
echo ""
echo "1. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: vqc-iris-classifier"
echo "   - Make it public or private"
echo "   - Do NOT initialize with README (we have one)"
echo ""

echo "2. Initialize git and push:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: VQC Iris Classifier v1.0.0'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/vqc-iris-classifier.git"
echo "   git push -u origin main"
echo ""

echo "3. Customize GitHub settings:"
echo "   - Add repository description"
echo "   - Add topics: quantum, machine-learning, quantum-computing, pennylane"
echo "   - Enable GitHub Actions"
echo "   - Enable Dependabot alerts"
echo "   - Set branch protection rules for 'main'"
echo ""

echo "4. Set up additional features (optional):"
echo "   - GitHub Pages for documentation"
echo "   - Code scanning with CodeQL"
echo "   - Codecov integration for coverage"
echo "   - Zenodo integration for DOI/citation"
echo ""

echo "=================================="
echo "Summary"
echo "=================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready for GitHub!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please fix before pushing to GitHub.${NC}"
    exit 1
fi
