@echo off
echo.
echo ===============================================
echo  GITHUB PAGES DIAGNOSTIC & FIX
echo ===============================================
echo.

set GITHUB_USERNAME=infosquawk
set REPOSITORY_NAME=ca-probate-appellate-repository
set EXPECTED_URL=https://%GITHUB_USERNAME%.github.io/%REPOSITORY_NAME%

echo 🔍 Diagnostic Information:
echo.
echo Repository: https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%
echo Expected Website URL: %EXPECTED_URL%
echo.

echo 📋 Manual Steps to Fix 404:
echo.
echo 1. Go to: https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%
echo 2. Click "Settings" tab
echo 3. Scroll to "Pages" in left sidebar
echo 4. Configure:
echo    - Source: "Deploy from a branch"
echo    - Branch: "main"
echo    - Folder: "/ (root)"
echo 5. Click "Save"
echo.

echo 🕐 After enabling Pages:
echo    - Wait 2-5 minutes for GitHub to build
echo    - Check "Actions" tab for build status
echo    - Visit: %EXPECTED_URL%
echo.

echo 🔧 Common Issues:
echo    • Pages not enabled (most common)
echo    • Wrong branch selected
echo    • Build still in progress
echo    • Repository name mismatch
echo.

echo 📱 Opening browser windows for you...
echo.

REM Open repository settings page
start https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%/settings/pages

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Open the expected website URL
start %EXPECTED_URL%

echo ✅ Browser windows opened:
echo    1. Repository Pages settings
echo    2. Expected website URL
echo.
echo 📋 Follow the manual steps above to configure Pages
echo    then refresh the website URL window.
echo.

pause
