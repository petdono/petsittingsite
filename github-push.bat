@echo off
REM GitHub Push Script for Pet Sitting Website
echo 🚀 Pet Sitting Website - GitHub Setup
echo ======================================

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if we're in a git repository
if not exist .git (
    echo 📝 Initializing Git repository...
    git init
)

REM Ask for GitHub repository URL
set /p repo_url="Enter your GitHub repository URL: "

REM Add remote if it doesn't exist
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔗 Adding remote repository...
    git remote add origin %repo_url%
) else (
    echo 🔄 Remote repository already exists. Updating...
    git remote set-url origin %repo_url%
)

REM Configure git user if not set
for /f "tokens=*" %%i in ('git config --global user.name') do set git_user=%%i
if "%git_user%"=="" (
    set /p git_name="Enter your Git name: "
    set /p git_email="Enter your Git email: "
    git config --global user.name "%git_name%"
    git config --global user.email "%git_email%"
)

REM Add all files
echo 📁 Adding files to Git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Initial commit: Pet sitting website with Docker support"

REM Push to GitHub
echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub!
    echo 🌐 Repository: %repo_url%
    echo.
    echo 📋 Next steps:
    echo 1. Go to your GitHub repository
    echo 2. Check that all files are uploaded
    echo 3. Consider enabling GitHub Actions for automated deployment
    echo 4. Follow GITHUB_SETUP.md for Docker deployment instructions
) else (
    echo ❌ Failed to push to GitHub. Please check your repository URL and credentials.
)

echo.
pause