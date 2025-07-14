@echo off
echo ========================================
echo GENTLE CONFLICT RESOLUTION
echo ========================================
echo Manually resolving conflicts by keeping local files...
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/5] Checking current conflict status...
git status
echo.

echo [2/5] Resolving README.md conflict (keeping local version)...
git checkout --ours README.md
git add README.md
echo ✅ README.md resolved!
echo.

echo [3/5] Resolving index.html conflict (keeping local version)...
git checkout --ours index.html
git add index.html
echo ✅ index.html resolved!
echo.

echo [4/5] Adding any other files...
git add .
echo ✅ All files added!
echo.

echo [5/5] Completing merge and pushing...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Resolve conflicts, keep local website content - %timestamp%"
if errorlevel 1 (
    echo ERROR: Commit failed!
    git status
    pause
    exit /b 1
)

git push origin main
if errorlevel 1 (
    echo ERROR: Push failed!
    git status
    pause
    exit /b 1
)
echo ✅ Successfully pushed resolved conflicts!
echo.

echo ========================================
echo CONFLICTS RESOLVED SUCCESSFULLY!
echo ========================================
echo Your website with 10 episodes is now live at:
echo https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo The conflicts have been resolved by keeping your local content.
echo GitHub Pages will deploy in 1-5 minutes.
echo.
pause
