@echo off
echo ========================================
echo FIXING WEBSITE LINKS
echo ========================================
echo Making website links functional...
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/2] Running link fix script...
python fix_website_links.py
if errorlevel 1 (
    echo ERROR: Link fix failed!
    pause
    exit /b 1
)
echo ✅ Links fixed!
echo.

echo [2/2] Deploying to GitHub...
call deploy_website_to_github_FIXED.bat
if errorlevel 1 (
    echo ERROR: Deployment failed!
    pause
    exit /b 1
)

echo ========================================
echo LINKS FIXED AND DEPLOYED!
echo ========================================
echo Your website now has properly working links:
echo - Working audio links will open Podbean
echo - Broken links show "Coming Soon" and are disabled
echo - Navigation should work properly
echo.
echo Live at: https://infosquawk.github.io/ca-probate-appellate-repository
echo.
pause
