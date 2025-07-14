@echo off
echo ========================================
echo 🎯 DEPLOYING HERO COVER IMAGES UPDATE
echo ========================================

REM Set directories
set SCHOLAR_DIR=C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast
set WEBSITE_DIR=%SCHOLAR_DIR%\website
set COVERS_DIR=%WEBSITE_DIR%\covers

echo 📸 Step 1: Copying podcast cover images...
echo.

REM Copy cover images with correct names
echo Copying main opinion cover (cover.png → cover_opinions.png)...
copy "%SCHOLAR_DIR%\cover.png" "%COVERS_DIR%\cover_opinions.png" >nul
if %errorlevel% equ 0 (
    echo ✅ Opinion cover copied successfully
) else (
    echo ❌ Failed to copy opinion cover
)

echo Copying case brief cover (cover_briefing.png → cover_briefs.png)...
copy "%SCHOLAR_DIR%\cover_briefing.png" "%COVERS_DIR%\cover_briefs.png" >nul
if %errorlevel% equ 0 (
    echo ✅ Brief cover copied successfully
) else (
    echo ❌ Failed to copy brief cover
)

echo Copying special edition cover (cover_special_edition.png → cover_special.png)...
copy "%SCHOLAR_DIR%\cover_special_edition.png" "%COVERS_DIR%\cover_special.png" >nul
if %errorlevel% equ 0 (
    echo ✅ Special edition cover copied successfully
) else (
    echo ❌ Failed to copy special edition cover
)

echo.
echo 🚀 Step 2: Deploying website to GitHub Pages...
echo.

REM Change to website directory
cd /d "%WEBSITE_DIR%"

REM Add all changes
git add .
echo ✅ Changes staged for commit

REM Commit with timestamp
for /f "tokens=1-4 delims=/ " %%i in ('date /t') do set mydate=%%j-%%k-%%l
for /f "tokens=1-2 delims=: " %%i in ('time /t') do set mytime=%%i:%%j
git commit -m "Deploy hero cover images update - %mydate% %mytime%"
echo ✅ Changes committed

REM Push to GitHub
git push origin main
if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub Pages
    echo.
    echo 🌐 Website URL: https://infosquawk.github.io/ca-probate-appellate-repository
    echo ⏱️  Changes will be live in 1-3 minutes
    echo.
    echo 🎯 Hero Section Features Now Live:
    echo    • Clickable podcast cover gallery
    echo    • Professional forest green design
    echo    • Interactive filtering by cover type
    echo    • Smooth animations and hover effects
) else (
    echo ❌ Failed to push to GitHub
    echo Please check your internet connection and Git configuration
)

echo.
echo ========================================
echo 🎉 DEPLOYMENT COMPLETE
echo ========================================
pause
