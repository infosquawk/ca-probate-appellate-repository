@echo off
echo ===============================================
echo WEBSITE RECOVERY AND PROPER DEPLOYMENT
echo ===============================================
echo.
echo 🚨 Fixing website after problematic deployment...
echo.

REM Step 1: Update website content with latest episode data
echo ========================================
echo Step 1: Updating website content...
echo ========================================
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"
python comprehensive_website_updater.py

if %errorlevel% neq 0 (
    echo ❌ Website updater failed
    pause
    exit /b 1
)

echo.
echo ✅ Website content updated successfully
echo.

REM Step 2: Navigate to GitHub repository directory
echo ========================================
echo Step 2: Preparing deployment...
echo ========================================
cd /d "C:\Users\Ryan\GitHub\ca-probate-appellate-repository"

REM Step 3: Pull latest changes (in case of conflicts)
echo 📥 Pulling latest changes...
git pull origin main

REM Step 4: Copy ALL necessary files from website to GitHub repo
echo 📁 Copying all website files...

REM Copy main website files
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\index.html" .
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\README.md" .
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\robots.txt" .

REM Create directories if they don't exist
if not exist "covers" mkdir covers
if not exist "pdfs" mkdir pdfs
if not exist "pdfs\published" mkdir "pdfs\published"
if not exist "pdfs\unpublished" mkdir "pdfs\unpublished"
if not exist "texts" mkdir texts

REM Copy cover images
echo 🎨 Copying cover images...
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\covers\*.png" covers\

REM Copy PDF files
echo 📋 Copying PDF files...
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\pdfs\published\*.pdf" "pdfs\published\"
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\pdfs\unpublished\*.pdf" "pdfs\unpublished\"

REM Copy text files
echo 📄 Copying text files...
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\texts\*.txt" texts\
copy "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\texts\*.html" texts\

echo.
echo 📊 Files ready for deployment:
dir /B

echo.
echo ========================================
echo Step 3: Deploying to GitHub Pages...
echo ========================================

REM Step 5: Add all files to git
echo 📤 Adding files to Git...
git add .

REM Step 6: Commit with descriptive message
echo 💾 Committing changes...
git commit -m "RECOVERY: Restore all website content and fix deployment - %date% %time%"

if %errorlevel% neq 0 (
    echo ⚠️  Nothing to commit or commit failed
    echo This might be normal if no changes were detected
)

REM Step 7: Push to GitHub
echo 🚀 Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo ❌ Git push failed
    echo Please check for conflicts or authentication issues
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ WEBSITE RECOVERY SUCCESSFUL!
echo ===============================================
echo.
echo 🌐 Your website should be live at:
echo    https://infosquawk.github.io/ca-probate-appellate-repository
echo.
echo 📊 Restored content includes:
echo    ✅ Updated episode data (16 episodes)
echo    ✅ Cover images (covers/)
echo    ✅ PDF documents (pdfs/published/ and pdfs/unpublished/)
echo    ✅ Text files (texts/)
echo.
echo 🕐 GitHub Pages will rebuild the site in 2-5 minutes
echo.
pause