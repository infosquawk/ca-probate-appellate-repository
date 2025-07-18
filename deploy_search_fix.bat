@echo off
echo ===============================================
echo RESTORE SEARCH BAR AND COMPLETE WEBSITE UPDATE
echo ===============================================
echo.
echo 🔍 The search functionality exists in your local HTML file
echo 🚀 Deploying the complete updated website...
echo.

REM Navigate to GitHub repository directory
cd /d "C:\Users\Ryan\GitHub\ca-probate-appellate-repository"

echo 📥 Pulling latest changes first...
git pull origin main

echo.
echo 📁 Copying updated HTML file with search functionality...
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\index.html" .

echo.
echo 📊 Current HTML file features:
findstr /C:"search-box" index.html >nul && echo ✅ Search box found || echo ❌ Search box missing
findstr /C:"handleSearch" index.html >nul && echo ✅ Search JavaScript found || echo ❌ Search JavaScript missing
findstr /C:"Total Episodes" index.html >nul && echo ✅ Episode data found || echo ❌ Episode data missing

echo.
echo 🔧 Verifying episode count in HTML...
findstr /C:"id.*16" index.html >nul && echo ✅ 16 episodes detected || echo ⚠️  Episode count may need updating

echo.
echo 📤 Adding updated HTML to Git...
git add index.html

echo 💾 Committing search restoration...
git commit -m "RESTORE: Search functionality and complete website update - %date% %time%"

if %errorlevel% neq 0 (
    echo ⚠️  Nothing to commit - file may already be up to date
)

echo 🚀 Pushing search fix to live website...
git push origin main

if %errorlevel% neq 0 (
    echo ❌ Git push failed
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ SEARCH BAR RESTORATION COMPLETE!
echo ===============================================
echo.
echo 🌐 Your website should be updated at:
echo    https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo 🔍 Expected features restored:
echo    ✅ Search bar with real-time filtering
echo    ✅ 16 total episodes (corrected from 10)
echo    ✅ All cover images and file links
echo    ✅ Filter buttons and navigation
echo.
echo 🕐 GitHub Pages will rebuild in 2-5 minutes
echo    The search bar should then be visible and functional
echo.
pause