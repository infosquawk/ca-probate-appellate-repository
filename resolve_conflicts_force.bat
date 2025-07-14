@echo off
echo ========================================
echo RESOLVING GIT CONFLICTS
echo ========================================
echo Resolving merge conflicts by keeping local content...
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/6] Checking conflict status...
git status
echo.

echo [2/6] Resetting merge state...
git merge --abort
echo ✅ Merge state reset!
echo.

echo [3/6] Using force push strategy (keeping local content)...
echo This will prioritize your local website with 10 episodes.
echo.

echo [4/6] Adding all files...
git add .
echo ✅ All files added!
echo.

echo [5/6] Creating commit with local content...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Website update with 10 episodes - local content priority - %timestamp%"
echo ✅ Local content committed!
echo.

echo [6/6] Force pushing to GitHub (will overwrite remote)...
echo This will make your 10-episode website the definitive version.
git push origin main --force
if errorlevel 1 (
    echo ERROR: Force push failed!
    echo Checking status...
    git status
    pause
    exit /b 1
)
echo ✅ Successfully force-pushed to GitHub!
echo.

echo ========================================
echo CONFLICTS RESOLVED!
echo ========================================
echo Your website with 10 episodes is now live at:
echo https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo GitHub Pages will deploy your changes in 1-5 minutes.
echo Your local content (with updated episodes) is now the master version.
echo.
pause
