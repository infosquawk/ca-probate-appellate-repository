@echo off
setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  AUTOMATED GITHUB PAGES DEPLOYMENT SCRIPT
echo  California Probate Code Appellate Repository
echo ===============================================
echo.

REM Configuration
set GITHUB_USERNAME=infosquawk
set REPOSITORY_NAME=ca-probate-appellate-repository
set WEBSITE_SOURCE_DIR=C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website
set GIT_CLONE_DIR=C:\Users\Ryan\GitHub
set REPO_LOCAL_PATH=%GIT_CLONE_DIR%\%REPOSITORY_NAME%

echo 🔧 Configuration:
echo    Username: %GITHUB_USERNAME%
echo    Repository: %REPOSITORY_NAME%
echo    Source Directory: %WEBSITE_SOURCE_DIR%
echo    Target Directory: %REPO_LOCAL_PATH%
echo.

REM Check if Git is installed
echo 📋 Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo    Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)
echo ✅ Git is installed

REM Check if source directory exists
if not exist "%WEBSITE_SOURCE_DIR%" (
    echo ❌ Website source directory not found: %WEBSITE_SOURCE_DIR%
    pause
    exit /b 1
)
echo ✅ Website source directory found

REM Create GitHub directory if it doesn't exist
if not exist "%GIT_CLONE_DIR%" (
    echo 📁 Creating GitHub directory: %GIT_CLONE_DIR%
    mkdir "%GIT_CLONE_DIR%"
)

REM Change to GitHub directory
cd /d "%GIT_CLONE_DIR%"

REM Check if repository already exists locally
if exist "%REPO_LOCAL_PATH%" (
    echo 📂 Repository already exists locally
    cd /d "%REPO_LOCAL_PATH%"
    
    echo 🔄 Pulling latest changes...
    git pull origin main
    if %errorlevel% neq 0 (
        echo ⚠️  Warning: Could not pull latest changes
    )
) else (
    echo 📥 Cloning repository from GitHub...
    git clone https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%.git
    if %errorlevel% neq 0 (
        echo ❌ Failed to clone repository
        echo    Please check:
        echo    1. Repository exists: https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%
        echo    2. You have access to the repository
        echo    3. Your internet connection
        pause
        exit /b 1
    )
    
    cd /d "%REPO_LOCAL_PATH%"
)

echo ✅ Repository ready: %REPO_LOCAL_PATH%

REM Configure Git user (if not already configured)
echo 🔧 Configuring Git user...
git config user.name "%GITHUB_USERNAME%"
git config user.email "%GITHUB_USERNAME%@users.noreply.github.com"

REM Clear existing files (except .git folder)
echo 🧹 Cleaning repository directory...
for /f "delims=" %%i in ('dir /b /a-d') do (
    if not "%%i"==".git" (
        del "%%i" 2>nul
    )
)
for /f "delims=" %%i in ('dir /b /ad') do (
    if not "%%i"==".git" (
        rmdir /s /q "%%i" 2>nul
    )
)

REM Copy website files
echo 📋 Copying website files...

REM Copy main files
copy "%WEBSITE_SOURCE_DIR%\index.html" . >nul
if %errorlevel% neq 0 (
    echo ❌ Failed to copy index.html
    pause
    exit /b 1
)
echo ✅ Copied index.html

copy "%WEBSITE_SOURCE_DIR%\README.md" . >nul 2>&1
echo ✅ Copied README.md

copy "%WEBSITE_SOURCE_DIR%\robots.txt" . >nul 2>&1
echo ✅ Copied robots.txt

copy "%WEBSITE_SOURCE_DIR%\.gitignore" . >nul 2>&1
echo ✅ Copied .gitignore

copy "%WEBSITE_SOURCE_DIR%\DEPLOYMENT_GUIDE.md" . >nul 2>&1
echo ✅ Copied DEPLOYMENT_GUIDE.md

REM Copy development folder if it exists
if exist "%WEBSITE_SOURCE_DIR%\development" (
    xcopy "%WEBSITE_SOURCE_DIR%\development" development\ /E /I /Q >nul 2>&1
    echo ✅ Copied development folder
)

echo.
echo 📦 Files ready for deployment:
dir /b
echo.

REM Add all files to git
echo 📤 Adding files to Git...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files to Git
    pause
    exit /b 1
)

REM Check if there are changes to commit
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo ℹ️  No changes detected - repository is already up to date
    echo 🌐 Your website is live at: https://%GITHUB_USERNAME%.github.io/%REPOSITORY_NAME%
    pause
    exit /b 0
)

REM Commit changes
echo 💾 Committing changes...
set COMMIT_MESSAGE=Website deployment - %DATE% %TIME%
git commit -m "%COMMIT_MESSAGE%"
if %errorlevel% neq 0 (
    echo ❌ Failed to commit changes
    pause
    exit /b 1
)

REM Push to GitHub
echo 🚀 Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Failed to push to GitHub
    echo    This might be due to:
    echo    1. Authentication issues
    echo    2. Network connectivity
    echo    3. Repository permissions
    echo.
    echo    You may need to authenticate with GitHub
    echo    Run: git push origin main
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ DEPLOYMENT SUCCESSFUL!
echo ===============================================
echo.
echo 🌐 Your website is now live at:
echo    https://%GITHUB_USERNAME%.github.io/%REPOSITORY_NAME%
echo.
echo 📋 What happens next:
echo    • GitHub Pages will build your site (2-5 minutes)
echo    • Website will be available at the URL above
echo    • Any future changes can be deployed with this script
echo.
echo 🔧 To update the website in the future:
echo    • Run this script again
echo    • Or use the website automation script
echo.
echo ===============================================

pause
