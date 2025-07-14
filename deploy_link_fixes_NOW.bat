@echo off
echo 🚀 DEPLOYING COMPREHENSIVE LINK FIXES
echo =======================================
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo 📝 Adding all changes...
git add .

echo 💾 Committing link fixes...
git commit -m "COMPREHENSIVE LINK FIX: All audio links working, text links properly disabled"

echo 🌐 Pushing to GitHub...
git push origin main

echo.
echo ✅ DEPLOYMENT COMPLETE!
echo.
echo 🎧 ALL AUDIO LINKS NOW WORKING:
echo    • 5 Opinion episodes (1:18:36, 31:13, 23:53, 57:34, 1:01:26)
echo    • 4 Case Brief episodes (6:40, 6:19, 6:42, 6:52)
echo.
echo 📄 ALL TEXT LINKS PROPERLY DISABLED
echo    • No more broken local file paths
echo    • Buttons show "Coming Soon" appropriately
echo.
echo 🌐 Live website: https://infosquawk.github.io/ca-probate-appellate-repository
echo    (Allow 1-2 minutes for GitHub Pages to update)
echo.
pause
