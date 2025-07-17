@echo off
echo ========================================
echo COMPREHENSIVE BRIEF LINKS FIX
echo ========================================

cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo.
echo Step 1: Checking current brief files in website/texts/...
echo.
echo Brief files currently available:
dir "texts\*_(Case_Brief)_*.txt" /B

echo.
echo Original court opinion files available:
dir "texts\B333052*.txt" /B
dir "texts\G063155*.txt" /B  
dir "texts\B341750*.txt" /B
dir "texts\B330596*.txt" /B

echo.
echo ========================================
echo Step 2: Running website updater to fix path conversion...
echo ========================================
python comprehensive_website_updater.py

if %errorlevel% neq 0 (
    echo ERROR: Website updater failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 3: Deploying fixes to GitHub Pages...
echo ========================================

git add .
git commit -m "Fix: Brief links and path conversion for missing episodes"
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Git deployment failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Brief links fix deployed!
echo ========================================
echo.
echo Fixed Issues:
echo ✅ Path conversion logic updated
echo ❌ B341750 brief still missing (requires manual generation)
echo.
echo Episodes that should now work:
echo - B341350 brief: texts/B341350_(Case_Brief)_Unknown_(unpublished).txt
echo - C102321 brief: texts/C102321_(Case_Brief)_Unknown_(unpublished).txt
echo - B333052 original text: should now be detected
echo.
echo Still Missing:
echo - B341750_(Case_Brief)_* file (needs to be regenerated)
echo.
echo Live website will update in 2-5 minutes.
echo.
pause
