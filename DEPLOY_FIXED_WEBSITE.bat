@echo off
echo ========================================
echo DEPLOYING FIXED WEBSITE TO PROBREP.COM
echo ========================================
echo.
echo Deploying updated content with working audio links...
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

python deploy_full_website_to_godaddy.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo FIXED WEBSITE DEPLOYED SUCCESSFULLY!
    echo ========================================
    echo.
    echo ✅ ProBRep.com has been updated with:
    echo    - Working audio links to Podbean
    echo    - 12 episodes with audio content
    echo    - Fixed episode descriptions
    echo    - Proper file links
    echo.
    echo 🌐 Visit https://probrep.com to test the fix
    echo.
) else (
    echo.
    echo ========================================
    echo DEPLOYMENT FAILED!
    echo ========================================
    echo Check the output above for error details.
)

echo.
echo Press any key to exit...
pause >nul
