@echo off
echo.
echo ===============================================
echo  GITHUB ACCOUNT VERIFICATION
echo ===============================================
echo.

echo 🔍 TROUBLESHOOTING: Missing Settings Tab
echo.
echo This usually means permission issues.
echo Let's check your GitHub account status:
echo.

echo 📋 CHECK YOUR GITHUB LOGIN:
echo.
echo 1. Look at the TOP-RIGHT corner of GitHub
echo 2. What do you see there?
echo.
echo Option A: You see "infosquawk" with profile picture
echo    → You're logged in correctly!
echo    → Try the direct Pages URL below
echo.
echo Option B: You see a DIFFERENT username
echo    → You're logged into the wrong account
echo    → Sign out and sign back in as "infosquawk"
echo.
echo Option C: You see "Sign in" button
echo    → You're not logged in at all
echo    → Sign in as "infosquawk"
echo.

echo 🌐 Opening verification pages...
echo.

REM Open GitHub main page to check login
start https://github.com

timeout /t 2 /nobreak >nul

REM Open repository page
start https://github.com/infosquawk/ca-probate-appellate-repository

timeout /t 2 /nobreak >nul

REM Try direct Pages settings URL
start https://github.com/infosquawk/ca-probate-appellate-repository/settings/pages

echo.
echo ✅ Three browser windows opened:
echo.
echo Window 1: GitHub main page
echo    → Check login status in top-right corner
echo.
echo Window 2: Your repository
echo    → Should show Settings tab if logged in correctly
echo.
echo Window 3: Direct Pages settings URL
echo    → Should work if you have permissions
echo.

echo 📋 What to report back:
echo    • What username do you see in top-right corner?
echo    • Can you access the direct Pages URL?
echo    • Any error messages?
echo.

pause
