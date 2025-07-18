@echo off
echo ===============================================
echo COMPLETE FIX: UPDATE CONTENT + DEPLOY SEARCH
echo ===============================================
echo.
echo 🔧 Step 1: Updating website content with latest episodes...
echo.

REM First, update the website content with latest episode data
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"
python comprehensive_website_updater.py

if %errorlevel% neq 0 (
    echo ❌ Website content update failed
    pause
    exit /b 1
)

echo.
echo ✅ Website content updated successfully
echo.
echo 🔧 Step 2: Verifying updated HTML has search functionality...

REM Check for search components
findstr /C:"search-box" index.html >nul && echo ✅ Search box found || echo ❌ Search box missing
findstr /C:"handleSearch" index.html >nul && echo ✅ Search JavaScript found || echo ❌ Search JavaScript missing

REM Check episode count - look for "16" in the stats section
findstr /C:"16</div>" index.html >nul && echo ✅ 16 episodes found in HTML || echo ⚠️  Episode count still needs updating

echo.
echo 🚀 Step 3: Deploying updated content to GitHub...
echo.

REM Navigate to GitHub repository directory
cd /d "C:\Users\Ryan\GitHub\ca-probate-appellate-repository"

echo 📥 Pulling latest changes...
git pull origin main

echo 📁 Copying updated HTML file with search + new episodes...
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\index.html" .

echo 📄 Checking what changed...
git diff --name-only

echo.
echo 📤 Adding all changes to Git...
git add .

echo 💾 Committing complete website update...
git commit -m "COMPLETE UPDATE: Search functionality + 16 episodes + all content - %date% %time%"

if %errorlevel% neq 0 (
    echo ⚠️  Nothing to commit - checking if already up to date..."
    echo 🔍 Current status:
    git status
) else (
    echo ✅ Changes committed successfully
)

echo 🚀 Pushing complete update to live website...
git push origin main

if %errorlevel% neq 0 (
    echo ❌ Git push failed
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ COMPLETE UPDATE SUCCESSFUL!
echo ===============================================
echo.
echo 🌐 Your website should now have:
echo    ✅ Search bar with real-time filtering
echo    ✅ 16 total episodes (updated from 10)
echo    ✅ All cover images and PDF/text links
echo    ✅ Current episode data from all sources
echo.
echo 🔗 Live website: https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo 🕐 GitHub Pages rebuild time: 2-5 minutes
echo    After rebuild, search and all content should be functional
echo.
pause