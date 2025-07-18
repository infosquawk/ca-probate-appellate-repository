@echo off
echo ==========================================
echo Deploy Final Episode Title Fixes
echo ==========================================
echo.
echo Deploying the final episode title fixes:
echo   • B341350: "In re Dominic H (B341350)"  
echo   • C102321: "Conservatorship of the Person of C (C102321)"
echo   • S282314: "In re Discipline (S282314)"
echo.

REM Change to website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo Step 1: Adding changes to Git...
git add index.html

echo.
echo Step 2: Committing the episode title fixes...
git commit -m "Fix remaining episode titles - B341350, C102321, S282314 now have proper case names"

echo.
echo Step 3: Pushing to GitHub Pages...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Push failed! 
    echo Your local fixes are applied, but the live website wasn't updated.
    echo Try running this script again in a few minutes.
    pause
    exit /b 1
) else (
    echo.
    echo ✅ Successfully deployed to GitHub Pages!
)

echo.
echo ==========================================
echo Episode Title Fixes Deployed!
echo ==========================================
echo.
echo ✅ Your live website will show these fixes in 2-3 minutes:
echo.
echo   BEFORE → AFTER:
echo   • "Case B341350" → "In re Dominic H (B341350)"
echo   • "Case C102321" → "Conservatorship of the Person of C (C102321)"  
echo   • "S282314" → "In re Discipline (S282314)"
echo.
echo 🌐 Check your website: https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo 🎉 All "unknown" case issues should now be resolved!
echo.
pause
