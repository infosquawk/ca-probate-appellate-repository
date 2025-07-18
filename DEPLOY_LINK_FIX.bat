@echo off
echo.
echo ===============================================
echo  DEPLOYING LINK FIX TO GITHUB PAGES
echo ===============================================
echo.

cd /d "%~dp0"

echo 🚀 Deploying fix for Opinion post link labels...
echo.

REM Run the full deployment script
call "DEPLOY_WEBSITE.bat"

if %errorlevel% neq 0 (
    echo ❌ Deployment failed - see errors above
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ LINK FIX DEPLOYED SUCCESSFULLY!
echo ===============================================
echo.
echo 📋 What was fixed:
echo    • Opinion posts: "Case Brief" → "Case Text"
echo    • Brief posts: "Case Brief" (unchanged)
echo    • Analysis posts: "Text" (unchanged)
echo.
echo 🌐 Website will update in 2-5 minutes at:
echo    https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo ✨ Opinion post links now accurately reflect their content!
echo.

pause
