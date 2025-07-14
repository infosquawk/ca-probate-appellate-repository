@echo off
echo ========================================
echo GIT PUSH TO GITHUB
echo ========================================
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/3] Adding files to Git...
git add .
if errorlevel 1 (
    echo ERROR: Git add failed!
    pause
    exit /b 1
)
echo ✅ Files added successfully!
echo.

echo [2/3] Committing changes...
set /p commit_msg="Enter commit message (or press Enter for auto-timestamp): "
if "%commit_msg%"=="" (
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
    set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
    set "commit_msg=Website update - %timestamp%"
)

git commit -m "%commit_msg%"
if errorlevel 1 (
    echo WARNING: Nothing to commit (no changes detected)
    echo.
) else (
    echo ✅ Changes committed successfully!
    echo.
)

echo [3/3] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Git push failed!
    pause
    exit /b 1
)
echo ✅ Successfully pushed to GitHub!
echo.

echo Website will be live at:
echo https://infosquawk.github.io/ca-probate-appellate-repository
echo.
pause
