@echo off
echo ========================================
echo ProBRep.com Full Website Deployment
echo ========================================
echo.
echo Deploying complete website to GoDaddy hosting...
echo Account: sysop2@probrep.com
echo Target: https://probrep.com
echo.

REM Change to website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

REM Run the deployment script
python deploy_full_website_to_godaddy.py

echo.
if %errorlevel% equ 0 (
    echo ✅ DEPLOYMENT SUCCESSFUL!
    echo Your website is live at https://probrep.com
) else (
    echo ❌ DEPLOYMENT FAILED!
    echo Check the logs for error details
)

echo.
echo Press any key to exit...
pause > nul
