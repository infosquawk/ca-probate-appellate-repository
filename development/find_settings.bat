@echo off
echo.
echo ===============================================
echo  GITHUB SETTINGS FINDER
echo ===============================================
echo.

set GITHUB_USERNAME=infosquawk
set REPOSITORY_NAME=ca-probate-appellate-repository

echo 🎯 Opening GitHub pages to help you find Settings...
echo.

echo 📋 What you should see:
echo.
echo 1. Repository page with tabs at the top:
echo    [Code] [Issues] [Pull requests] [Actions] [Projects] [Security] [Insights] [Settings]
echo.
echo 2. Settings tab should be the LAST tab on the right
echo.
echo 3. If you don't see Settings tab:
echo    • Make sure you're logged in as: %GITHUB_USERNAME%
echo    • Look for "..." menu if on small screen
echo    • Use the direct Pages URL (opening below)
echo.

echo 🌐 Opening browser windows...
echo.

REM Open main repository page
echo Opening repository page...
start https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Open direct Pages settings URL
echo Opening Pages settings directly...
start https://github.com/%GITHUB_USERNAME%/%REPOSITORY_NAME%/settings/pages

echo.
echo ✅ Two browser windows opened:
echo.
echo Window 1: Main repository page
echo   → Look for Settings tab at the top (far right)
echo.
echo Window 2: Direct Pages settings
echo   → If first window doesn't work, use this one
echo.

echo 📋 In the Pages settings, configure:
echo   • Source: "Deploy from a branch"
echo   • Branch: "main"  
echo   • Folder: "/ (root)"
echo   • Click "Save"
echo.

pause
