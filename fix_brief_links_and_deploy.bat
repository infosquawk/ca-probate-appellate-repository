@echo off
echo ========================================
echo FIXING BRIEF LINKS - DIRECT APPROACH
echo ========================================

cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo.
echo Current files in website/texts/ that should work:
echo ✅ B333052_Conservatorship_of_ANNE_S_published.txt (for opinion episodes)
echo ✅ B341350_(Case_Brief)_Unknown_(unpublished).txt (for brief episodes)  
echo ✅ C102321_(Case_Brief)_Unknown_(unpublished).txt (for brief episodes)
echo ❌ B341750_(Case_Brief)_* (MISSING - this is why brief doesn't work)

echo.
echo Running Python fix script...
python fix_episode_links_direct.py

if %errorlevel% neq 0 (
    echo.
    echo Python script had issues. Running comprehensive website updater instead...
    python comprehensive_website_updater.py
)

echo.
echo ========================================
echo Deploying fixes to live website...
echo ========================================

git add .
git commit -m "Fix: Correct episode links for existing brief and court opinion files"
git push origin main

if %errorlevel% neq 0 (
    echo ERROR: Git push failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Brief links fix deployed!
echo ========================================
echo.
echo Fixed Issues:
echo ✅ B333052 opinion episodes should now link to court opinion text
echo ✅ Existing brief files should be properly linked
echo.
echo Still Missing (requires manual attention):
echo ❌ B341750 case brief file (Episode 7 will still show no brief)
echo.
echo Live website will update in 2-5 minutes.
echo Check: https://infosquawk.github.io/ca-probate-appellate-repository/
echo.
pause
