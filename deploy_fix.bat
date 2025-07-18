@echo off
echo ========================================
echo Deploying Website Link Fixes to GitHub Pages
echo ========================================
echo.

echo Setting upstream branch and pushing to GitHub...
git push --set-upstream origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Git push failed
    echo.
    echo Possible solutions:
    echo 1. Check your GitHub authentication
    echo 2. Verify the remote origin is correct: git remote -v
    echo 3. Try: git push origin main --force (if needed)
    echo.
    pause
    exit /b %errorlevel%
)

echo.
echo ✅ SUCCESS: Website deployed to GitHub Pages!
echo.
echo 🌐 Your live website will be updated within 2-5 minutes at:
echo    https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo ✅ All Opinion posts now have PDF and text links
echo ✅ All Brief posts now have case brief text links  
echo ✅ D085918 "Estate of EDEN AHBEZ" is now properly linked
echo.
echo You can check the live site in a few minutes to verify the fixes!
echo.
pause
