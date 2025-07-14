@echo off
echo ========================================
echo ALTERNATIVE: CLONE AND UPDATE METHOD
echo ========================================
echo This method clones your GitHub repo and updates it with current content
echo.

REM Go to parent directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast"

echo [1/5] Creating backup of current website...
if exist "website_backup" rmdir /s /q "website_backup"
xcopy "website" "website_backup\" /E /I /Q
echo ✅ Backup created!
echo.

echo [2/5] Removing current website directory...
if exist "website_git" rmdir /s /q "website_git"
echo ✅ Cleaned up!
echo.

echo [3/5] Cloning GitHub repository...
git clone https://github.com/infosquawk/ca-probate-appellate-repository.git website_git
if errorlevel 1 (
    echo ERROR: Failed to clone repository!
    pause
    exit /b 1
)
echo ✅ Repository cloned!
echo.

echo [4/5] Copying updated files to Git repository...
xcopy "website_backup\*" "website_git\" /E /Y /Q
echo ✅ Files copied!
echo.

echo [5/5] Repository is ready!
echo ✅ Your Git-connected website is now in: website_git\
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Go to: cd website_git
echo 2. Run: deploy_website_to_github.bat
echo.
echo Your updated content (10 episodes) is ready to deploy!
echo.
pause
