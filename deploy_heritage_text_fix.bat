@echo off
echo ========================================
echo Deploying Heritage Text Link Fix
echo ========================================
echo.
echo Changes being deployed:
echo - Updated special edition to link to formatted HTML version
echo - Changed button text from "Case Brief" to "Text" for analysis episodes
echo.

cd /d "%~dp0"

echo Adding changes to git...
git add index.html

echo Committing changes...
git commit -m "Fix: Update California's Heritage of Estates to link to formatted HTML version and change button text to 'Text'"

echo Pushing to GitHub Pages...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Heritage Text Fix Deployment Successful!
    echo ========================================
    echo.
    echo Changes will be live in 2-5 minutes at:
    echo https://infosquawk.github.io/ca-probate-appellate-repository
    echo.
    echo What was fixed:
    echo - Special edition now links to beautifully formatted HTML version
    echo - Button text changed from "Case Brief" to "Text" for analysis
    echo - Formatted version includes site colors and professional styling
) else (
    echo.
    echo ========================================
    echo Deployment Failed!
    echo ========================================
    echo Check git status and try again manually.
)

echo.
echo Press any key to exit...
pause >nul
