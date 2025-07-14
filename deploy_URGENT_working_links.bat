@echo off
echo 🚀 DEPLOYING WORKING AUDIO LINKS TO LIVE WEBSITE
echo ================================================
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo 📝 Current status: 9 working Podbean URLs in local file
echo 🎯 Goal: Deploy to GitHub Pages so buttons work
echo.

echo [1/3] Adding changes to Git...
git add index.html
if errorlevel 1 (
    echo ❌ Git add failed! Checking status...
    git status
    pause
    exit /b 1
)

echo [2/3] Committing fixes...
git commit -m "URGENT: Deploy working audio links - 9 Podbean URLs ready"
if errorlevel 1 (
    echo ℹ️ Nothing to commit (already up to date locally)
) else (
    echo ✅ Committed successfully!
)

echo [3/3] Pushing to GitHub Pages...
git push origin main
if errorlevel 1 (
    echo ❌ Push failed! Trying to resolve...
    echo.
    echo Checking current status:
    git status
    echo.
    echo Recent log:
    git log --oneline -3
    pause
    exit /b 1
)

echo.
echo 🎉 DEPLOYMENT COMPLETE!
echo =====================================================
echo.
echo ✅ 9 WORKING AUDIO LINKS NOW DEPLOYING:
echo    📢 5 Opinion Episodes (1:18:36, 31:13, 23:53, 57:34, 1:01:26)
echo    📋 4 Case Brief Episodes (6:40, 6:19, 6:42, 6:52)
echo.
echo 🌐 Live Website: https://infosquawk.github.io/ca-probate-appellate-repository
echo ⏱️  GitHub Pages Update: 1-3 minutes (then refresh your browser)
echo.
echo 🔄 If still showing "Coming Soon" after 3 minutes:
echo    1. Clear browser cache (Ctrl+F5)
echo    2. Try incognito/private browsing
echo    3. Wait another 2-3 minutes for full deployment
echo.
pause
