@echo off
echo ==========================================
echo Fix Git Deployment Issue
echo ==========================================
echo.
echo The previous push failed due to remote/local sync issues.
echo This script will resolve the conflict and deploy your fixes.
echo.

REM Change to website directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo Step 1: Checking current Git status...
git status

echo.
echo Step 2: Fetching remote changes...
git fetch origin

echo.
echo Step 3: Pulling remote changes (may require merge)...
git pull origin main

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Git pull had conflicts or issues.
    echo Please resolve any conflicts manually, then run this script again.
    echo.
    echo Common solutions:
    echo   1. If there are merge conflicts, edit the conflicted files
    echo   2. Run: git add .
    echo   3. Run: git commit -m "Resolve merge conflicts"
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo Step 4: Ensuring your changes are staged...
git add .

echo.
echo Step 5: Checking if we need to commit changes...
git status

echo.
echo Step 6: Pushing to GitHub Pages...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Push still failed. Let's try force push with lease (safer)...
    git push --force-with-lease origin main
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Force push also failed. Manual intervention required.
        echo.
        echo Possible solutions:
        echo   1. Check GitHub repository for issues
        echo   2. Verify Git credentials are working
        echo   3. Try: git reset --hard origin/main (WARNING: loses local changes)
        echo.
        pause
        exit /b 1
    ) else (
        echo ✅ Force push successful!
    )
) else (
    echo ✅ Normal push successful!
)

echo.
echo ==========================================
echo Git Deployment Fixed!
echo ==========================================
echo.
echo ✅ Your targeted fixes are now live!
echo 🌐 Check your website in 2-3 minutes:
echo    https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo The following case names should now be fixed:
echo   • B341350: "In re Dominic H"
echo   • C102321: "Conservatorship of the Person of C"  
echo   • S282314: "In re Discipline"
echo.
pause
