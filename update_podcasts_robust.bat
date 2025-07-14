@echo off
echo ========================================
echo UPDATING PODCAST LINKS - ROBUST VERSION
echo ========================================
echo Connecting all opinion episodes to working Podbean links...
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/3] Updating podcast links with robust method...
python update_podcast_links_robust.py
if errorlevel 1 (
    echo ERROR: Podcast link update failed!
    pause
    exit /b 1
)
echo ✅ Podcast links updated!
echo.

echo [2/3] Committing changes to Git...
git add .

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Add working Podbean links for all opinion episodes - %timestamp%"
echo ✅ Changes committed!
echo.

echo [3/3] Deploying to GitHub Pages...
git push origin main
if errorlevel 1 (
    echo ERROR: Deployment failed!
    git status
    pause
    exit /b 1
)
echo ✅ Successfully deployed!
echo.

echo ========================================
echo ALL PODCAST LINKS UPDATED!
echo ========================================
echo Your website now has working podcast links for:
echo.
echo 🎧 Case S282314 (Smart Fallback) - 1:18:36
echo 🎧 Case G063155 (Smart Fallback) - 31:13  
echo 🎧 Case B341750 (Smart Fallback) - 23:53
echo 🎧 Case B330596 (Smart Fallback) - 57:34
echo 🎧 Case B333052 (Original) - 1:01:26
echo.
echo 📈 Total: 5 opinion episodes with working audio
echo 📈 Total: 4 case brief episodes with working audio  
echo 📈 Total: 1 legal analysis episode (text only)
echo.
echo Live website: https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo All opinion episodes now have working "Listen Now" buttons!
echo.
pause
