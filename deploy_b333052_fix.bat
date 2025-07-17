@echo off
echo ========================================
echo DEPLOYING B333052 OPINION TEXT LINK FIX
echo ========================================

cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo Fixed Issue:
echo ✅ Episode 10 (B333052 opinion) now links to: texts/B333052_Conservatorship_of_ANNE_S_published.txt
echo.

echo Adding changes to git...
git add index.html

echo Committing the fix...
git commit -m "Fix: Add missing court opinion text link for B333052 case"

echo Pushing to GitHub Pages...
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Git push failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: B333052 opinion text link fix deployed!
echo ========================================
echo.
echo Fixed:
echo ✅ Episode 10: "Case B333052 - Unknown" now has working court opinion text link
echo.
echo Still Missing (requires brief file regeneration):
echo ❌ Episode 7: "Brief: Conservatorship of Julie C" - missing brief file B341750_(Case_Brief)_*
echo.
echo Live website will update in 2-5 minutes at:
echo https://infosquawk.github.io/ca-probate-appellate-repository/
echo.
echo To verify the fix:
echo 1. Visit the live website
echo 2. Search for "B333052" or scroll to Episode 10
echo 3. Click the "📄 Court Opinion Text" button
echo 4. Should open: texts/B333052_Conservatorship_of_ANNE_S_published.txt
echo.
pause
