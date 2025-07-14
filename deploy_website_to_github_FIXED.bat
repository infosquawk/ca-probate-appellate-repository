@echo off
echo ========================================
echo SCHOLAR PODCAST WEBSITE DEPLOYMENT
echo ========================================
echo Starting automated website deployment...
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/5] Updating website content...
call run_website_update.bat
if errorlevel 1 (
    echo ERROR: Website update failed!
    pause
    exit /b 1
)
echo ✅ Website content updated successfully!
echo.

echo [2/5] Synchronizing with GitHub (pulling latest)...
git pull origin main --allow-unrelated-histories
if errorlevel 1 (
    echo WARNING: Pull had issues, trying fetch and merge...
    git fetch origin
    git merge origin/main --allow-unrelated-histories -X ours
    if errorlevel 1 (
        echo WARNING: Merge conflicts detected, prioritizing local changes...
    )
)
echo ✅ Synchronized with remote repository!
echo.

echo [3/5] Adding files to Git...
git add .
if errorlevel 1 (
    echo ERROR: Git add failed!
    pause
    exit /b 1
)
echo ✅ Files added to Git successfully!
echo.

echo [4/5] Committing changes...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Auto-update website content - %timestamp%"
if errorlevel 1 (
    echo INFO: Nothing to commit (no changes detected)
    echo.
) else (
    echo ✅ Changes committed successfully!
    echo.
)

echo [5/5] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Git push failed!
    echo Showing repository status for debugging...
    git status
    echo.
    echo Recent commits:
    git log --oneline -3
    echo.
    echo Please check your internet connection and GitHub credentials.
    pause
    exit /b 1
)
echo ✅ Successfully pushed to GitHub!
echo.

echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo Your website will be live at:
echo https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo GitHub Pages deployment usually takes 1-5 minutes.
echo Check the Actions tab for deployment status:
echo https://github.com/infosquawk/ca-probate-appellate-repository/actions
echo.
pause
