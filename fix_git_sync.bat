@echo off
echo ========================================
echo FIXING GIT SYNCHRONIZATION
echo ========================================
echo Resolving local/remote repository conflicts...
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/4] Checking current status...
git status
echo.

echo [2/4] Pulling latest changes from GitHub...
git pull origin main --allow-unrelated-histories
if errorlevel 1 (
    echo WARNING: Pull had conflicts, trying alternative approach...
    echo.
    echo [2b/4] Fetching and merging manually...
    git fetch origin
    git merge origin/main --allow-unrelated-histories -X ours
    if errorlevel 1 (
        echo ERROR: Could not resolve conflicts automatically.
        echo You may need to resolve conflicts manually.
        pause
        exit /b 1
    )
)
echo ✅ Successfully synchronized with remote!
echo.

echo [3/4] Adding any new changes...
git add .
echo ✅ Files added!
echo.

echo [4/4] Committing and pushing...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Sync and update website content - %timestamp%"
if errorlevel 1 (
    echo INFO: Nothing new to commit
) else (
    echo ✅ New changes committed!
)

git push origin main
if errorlevel 1 (
    echo ERROR: Push still failed!
    echo Showing detailed status...
    git status
    git log --oneline -5
    pause
    exit /b 1
)
echo ✅ Successfully pushed to GitHub!
echo.

echo ========================================
echo SYNCHRONIZATION COMPLETE!
echo ========================================
echo Your website should be updated at:
echo https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo GitHub Pages deployment usually takes 1-5 minutes.
echo.
pause
