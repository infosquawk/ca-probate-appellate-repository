@echo off
echo ===============================================
echo FORCE DEPLOY: Search Bar and 16 Episodes
echo ===============================================
echo.

REM Navigate to GitHub repository directory
cd /d "C:\Users\Ryan\GitHub\ca-probate-appellate-repository"

echo 🔧 Current repository status:
git status

echo.
echo 📁 Forcing copy of updated HTML...
copy /Y "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\index.html" .

echo.
echo 🔍 Checking file differences...
echo File size comparison:
dir index.html
echo.
echo Checking for search box in repository file:
findstr /C:"search-box" index.html >nul && echo ✅ Search box found in repo || echo ❌ Search box missing in repo

echo Checking for episode count in repository file:
findstr /C:"16</div>" index.html >nul && echo ✅ 16 episodes found in repo || echo ❌ Still showing old episode count

echo.
echo 🔧 Forcing Git to recognize changes...
git add index.html --force

echo 📄 Checking Git status after force add...
git status

echo.
echo 💾 Force committing with timestamp...
git commit -m "FORCE UPDATE: Restore search functionality and 16 episodes - %date% %time%" --allow-empty

echo.
echo 🚀 Force pushing to GitHub...
git push origin main --force

if %errorlevel% neq 0 (
    echo ❌ Force push failed
    echo 🔧 Trying alternative approach...
    echo.
    echo 📝 Creating a small change to force update...
    echo ^<!-- Force update: %date% %time% --^> >> index.html
    git add index.html
    git commit -m "FORCE: Add timestamp to trigger deployment - %date% %time%"
    git push origin main
)

echo.
echo ===============================================
echo ✅ FORCE DEPLOYMENT COMPLETE!
echo ===============================================
echo.
echo 🌐 Check your website in 3-5 minutes:
echo    https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo 🔍 Expected results:
echo    ✅ Search bar should appear at the top
echo    ✅ Episode count should show 16
echo    ✅ All filter functionality should work
echo.
pause