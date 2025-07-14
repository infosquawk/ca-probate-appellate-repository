@echo off
echo ========================================
echo SCHOLAR PODCAST WEBSITE DEPLOYMENT
echo ========================================
echo Starting automated website deployment...
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/4] Updating website content...
call run_website_update.bat
if errorlevel 1 (
    echo ERROR: Website update failed!
    pause
    exit /b 1
)
echo ✅ Website content updated successfully!
echo.

echo [2/4] Adding files to Git...
git add .
if errorlevel 1 (
    echo ERROR: Git add failed!
    pause
    exit /b 1
)
echo ✅ Files added to Git successfully!
echo.

echo [3/4] Committing changes...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Auto-update website content - %timestamp%"
if errorlevel 1 (
    echo WARNING: Nothing to commit (no changes detected)
    echo.
) else (
    echo ✅ Changes committed successfully!
    echo.
)

echo [4/4] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Git push failed!
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
