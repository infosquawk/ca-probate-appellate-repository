@echo off
echo ========================================
echo INITIALIZING GIT REPOSITORY
echo ========================================
echo Setting up Git repository connection...
echo.

REM Change to the website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo [1/6] Initializing Git repository...
git init
if errorlevel 1 (
    echo ERROR: Git init failed!
    pause
    exit /b 1
)
echo ✅ Git repository initialized!
echo.

echo [2/6] Adding remote repository...
git remote add origin https://github.com/infosquawk/ca-probate-appellate-repository.git
if errorlevel 1 (
    echo WARNING: Remote might already exist, removing and re-adding...
    git remote remove origin
    git remote add origin https://github.com/infosquawk/ca-probate-appellate-repository.git
)
echo ✅ Remote repository added!
echo.

echo [3/6] Fetching from remote...
git fetch origin
if errorlevel 1 (
    echo ERROR: Failed to fetch from remote!
    echo Please check your internet connection and GitHub repository.
    pause
    exit /b 1
)
echo ✅ Fetched from remote successfully!
echo.

echo [4/6] Creating and switching to main branch...
git checkout -b main
git branch --set-upstream-to=origin/main main
echo ✅ Main branch configured!
echo.

echo [5/6] Adding all files...
git add .
echo ✅ Files added to Git!
echo.

echo [6/6] Making initial commit...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

git commit -m "Initialize local repository with updated website content - %timestamp%"
echo ✅ Initial commit created!
echo.

echo ========================================
echo GIT SETUP COMPLETE!
echo ========================================
echo Your repository is now connected to:
echo https://github.com/infosquawk/ca-probate-appellate-repository
echo.
echo You can now use deploy_website_to_github.bat
echo to push updates to your live website!
echo.
pause
