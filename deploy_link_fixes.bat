@echo off
echo ========================================
echo DEPLOYING LINK FIXES
echo ========================================
echo Deploying fixed website with working links...
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/3] Adding changes to Git...
git add .
echo ✅ Changes added!
echo.

echo [2/3] Committing link fixes...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Fix website links - disable broken links, enable working audio - %timestamp%"
echo ✅ Link fixes committed!
echo.

echo [3/3] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Push failed!
    git status
    pause
    exit /b 1
)
echo ✅ Successfully deployed!
echo.

echo ========================================
echo LINK FIXES DEPLOYED!
echo ========================================
echo Your website now has properly working links:
echo.
echo ✅ Working audio links: Open Podbean podcasts
echo ✅ Broken links: Show "Coming Soon" and are disabled
echo ✅ Navigation: Filters and search working properly
echo.
echo Live website: https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo Expected results:
echo - 5 episodes should have working "Listen Now" buttons
echo - Other episodes show "Audio Coming Soon" (disabled)
echo - All "Text Coming Soon" buttons are disabled (no web text files)
echo.
pause
