@echo off
echo.
echo ===============================================
echo  QUICK GITHUB PAGES DEPLOYMENT
echo ===============================================
echo.

cd /d "%~dp0"

echo 🚀 Running automated GitHub Pages deployment...
echo.

:: Navigate to development folder and run the deployment script
call "development\deploy_to_github_pages.bat"

echo.
echo 🎉 Deployment script completed!
echo.
pause
