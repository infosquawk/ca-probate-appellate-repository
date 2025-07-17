@echo off
echo ========================================
echo DEPLOYING FOOTER TEXT REMOVAL
echo ========================================

cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo Change Made:
echo ❌ Removed: "This repository provides professional access to California probate law appellate decisions and analysis..."
echo ✅ Kept: Copyright notice only
echo.

echo Adding changes to git...
git add index.html

echo Committing the change...
git commit -m "Remove: Detailed description text from footer, keep copyright only"

echo Pushing to GitHub Pages...
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Git push failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Footer text removal deployed!
echo ========================================
echo.
echo The footer now only contains:
echo ✅ "About This Repository" heading
echo ✅ Copyright notice
echo.
echo Live website will update in 2-5 minutes at:
echo https://infosquawk.github.io/ca-probate-appellate-repository/
echo.
pause
