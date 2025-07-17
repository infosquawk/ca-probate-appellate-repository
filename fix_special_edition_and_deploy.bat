@echo off
echo ========================================
echo URGENT FIX: Special Edition Audio Link
echo ========================================

cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo Running comprehensive website updater with FIXED special edition audio...
python comprehensive_website_updater.py

if %errorlevel% neq 0 (
    echo ERROR: Website updater failed
    pause
    exit /b 1
)

echo.
echo Website updated successfully! Now deploying to GitHub Pages...
echo.

echo Adding changes...
git add .

echo Committing changes...
git commit -m "Fix: Add working audio link for California's Heritage Of Estates special edition"

echo Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Git push failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Special edition audio fix deployed!
echo ========================================
echo The live website will update within 2-5 minutes.
echo Check: https://infosquawk.github.io/ca-probate-appellate-repository/
echo.
pause
