@echo off
echo ========================================
echo DEPLOYING SPECIAL EDITION AUDIO FIX
echo ========================================

cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo Checking git status...
git status

echo.
echo Adding all changes...
git add .

echo.
echo Committing the special edition audio fix...
git commit -m "Deploy: Fix special edition audio link for California's Heritage Of Estates"

echo.
echo Pushing to GitHub Pages...
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Failed to push to GitHub
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Special edition audio fix deployed!
echo ========================================
echo.
echo The live website will update within 2-5 minutes at:
echo https://infosquawk.github.io/ca-probate-appellate-repository/
echo.
echo The "California's Heritage Of Estates" episode should now show:
echo 🎧 Listen Now (working audio button)
echo.
pause
