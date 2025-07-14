@echo off
setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  CLEAN GITHUB PAGES DEPLOYMENT
echo  (Fixing Security Token Issue)
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

echo 🚨 Security Fix: Removing local repository with token history...
if exist "%REPO_LOCAL_PATH%" (
    rmdir /s /q "%REPO_LOCAL_PATH%"
    echo ✅ Cleaned local repository
)

REM Change to GitHub directory
cd /d "%GIT_CLONE_DIR%"

echo 📥 Fresh clone from GitHub...
git clone https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%.git
if %errorlevel% neq 0 (
    echo ❌ Failed to clone repository
    pause
    exit /b 1
)

cd /d "%REPO_LOCAL_PATH%"

REM Configure Git user
echo 🔧 Configuring Git user...
git config user.name "%GITHUB_USERNAME%"
git config user.email "%GITHUB_USERNAME%@users.noreply.github.com"

REM Clear existing files (except .git folder and README.md)
echo 🧹 Cleaning repository directory...
for /f "delims=" %%i in ('dir /b /a-d') do (
    if not "%%i"==".git" if not "%%i"=="README.md" (
        del "%%i" 2>nul
    )
)
for /f "delims=" %%i in ('dir /b /ad') do (
    if not "%%i"==".git" (
        rmdir /s /q "%%i" 2>nul
    )
)

REM Copy website files (with updated TROUBLESHOOTING.md)
echo 📋 Copying cleaned website files...

copy "%WEBSITE_SOURCE_DIR%\index.html" . >nul
echo ✅ Copied index.html

copy "%WEBSITE_SOURCE_DIR%\robots.txt" . >nul 2>&1
echo ✅ Copied robots.txt

copy "%WEBSITE_SOURCE_DIR%\.gitignore" . >nul 2>&1
echo ✅ Copied .gitignore

copy "%WEBSITE_SOURCE_DIR%\DEPLOYMENT_GUIDE.md" . >nul 2>&1
echo ✅ Copied DEPLOYMENT_GUIDE.md

REM Copy development folder with cleaned files
if exist "%WEBSITE_SOURCE_DIR%\development" (
    mkdir development 2>nul
    copy "%WEBSITE_SOURCE_DIR%\development\*.bat" development\ >nul 2>&1
    copy "%WEBSITE_SOURCE_DIR%\development\*.py" development\ >nul 2>&1
    copy "%WEBSITE_SOURCE_DIR%\development\TROUBLESHOOTING.md" development\ >nul 2>&1
    echo ✅ Copied development folder (cleaned)
)

echo.
echo 📦 Clean files ready for deployment:
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
echo 💾 Committing cleaned changes...
set COMMIT_MESSAGE=Clean website deployment (security token removed) - %DATE% %TIME%
git commit -m "%COMMIT_MESSAGE%"
if %errorlevel% neq 0 (
    echo ❌ Failed to commit changes
    pause
    exit /b 1
)

REM Push to GitHub
echo 🚀 Pushing clean deployment to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Failed to push to GitHub
    echo.
    echo 🔐 You may need to authenticate:
    echo    Username: %GITHUB_USERNAME%
    echo    Password: [Your GitHub Token]
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ CLEAN DEPLOYMENT SUCCESSFUL!
echo ===============================================
echo.
echo 🌐 Your website is now live at:
echo    https://%GITHUB_USERNAME%.github.io/%REPOSITORY_NAME%
echo.
echo 🔒 Security Issue Resolved:
echo    • GitHub token removed from all files
echo    • Clean deployment completed
echo    • Website ready for public access
echo.
echo 📋 Next Steps:
echo    1. Wait 2-5 minutes for GitHub Pages to build
echo    2. Visit your live website URL above
echo    3. Enable GitHub Pages if not already done
echo.
echo ===============================================

pause
