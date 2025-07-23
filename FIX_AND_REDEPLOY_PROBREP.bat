@echo off
echo ========================================
echo FIX AND REDEPLOY PROBREP.COM WEBSITE
echo ========================================
echo.
echo This script will:
echo 1. Update website content with latest episode data
echo 2. Deploy updated content to ProBRep.com
echo 3. Verify deployment success
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

python fix_and_redeploy.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo FIX AND REDEPLOY COMPLETED SUCCESSFULLY!
    echo ========================================
    echo Please visit https://probrep.com to verify
    echo that the website is now working correctly.
) else (
    echo.
    echo ========================================
    echo ERROR: Fix and redeploy failed!
    echo ========================================
    echo Check the output above for error details.
)

echo.
echo Press any key to exit...
pause >nul
