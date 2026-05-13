@echo off
REM VQC Project - Git Setup Script for Windows
REM This script initializes git and makes the initial commit

echo.
echo ======================================================================
echo VQC Iris Classifier - Git Setup Script
echo ======================================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Git is not installed or not in PATH
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Or if already installed, add it to your PATH environment variable
    echo.
    pause
    exit /b 1
)

echo ✅ Git found: 
git --version
echo.

REM Configure git (ask user)
echo Configure Git user information? (y/n)
set /p config_git="Enter choice (y/n): "
if /i "%config_git%"=="y" (
    set /p git_name="Enter your name: "
    set /p git_email="Enter your email: "
    git config --global user.name "%git_name%"
    git config --global user.email "%git_email%"
    echo ✅ Git configured
    echo.
)

REM Initialize repository
echo Initializing git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to initialize git repository
    pause
    exit /b 1
)
echo ✅ Repository initialized
echo.

REM Add all files
echo Adding all files to staging area...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo ✅ Files added
echo.

REM Show files to be committed
echo Files to be committed:
echo ======================================================================
git diff --cached --name-only
echo ======================================================================
echo.

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: VQC Iris Classifier v1.0.0

- Complete Variational Quantum Classifier implementation
- 4-qubit quantum circuit with PennyLane
- 83.3%% accuracy on Iris dataset
- Pure NumPy fallback simulator
- 750+ lines of comprehensive tests
- Full documentation and examples
- GitHub Actions CI/CD pipeline
- Docker support
- Results generated (metrics, training history, confusion matrix)"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)
echo ✅ Initial commit created
echo.

REM Display repository status
git log --oneline -1
echo.

REM Next steps
echo ======================================================================
echo ✅ NEXT STEPS - Publish to GitHub
echo ======================================================================
echo.
echo 1. Create a GitHub repository at https://github.com/new
echo    - Repository name: vqc-iris-classifier
echo    - Do NOT initialize with README/License/gitignore
echo.
echo 2. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/vqc-iris-classifier.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Add topics to your GitHub repository:
echo    - quantum-computing
echo    - machine-learning
echo    - quantum-machine-learning
echo    - pennylane
echo.
echo ======================================================================
echo.

pause
