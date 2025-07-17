@echo off
echo ========================================
echo Deploying PDF Links Fix to Live Website
echo ========================================
echo.
echo Changes being deployed:
echo - Fixed all missing PDF case opinion links
echo - Copied PDF files to website directories
echo - Updated episode data with working PDF URLs
echo.

cd /d "%~dp0"

echo Adding changes to git...
git add .

echo Committing changes...
git commit -m "Fix: Add missing PDF case opinion links for all episodes

- Copy missing PDF files from probate_cases to website/pdfs
- Update episode data with correct PDF URLs for:
  * B341350: unpublished PDF
  * C102321: unpublished PDF  
  * G063155: published PDF
  * B333052: published PDF
  * S282314: published PDF
  * B330596: unpublished PDF (already existed)
  * B341750: unpublished PDF (already existed)
- All case opinions now have working PDF document links"

echo Pushing to GitHub Pages...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo PDF Links Fix Deployment Successful!
    echo ========================================
    echo.
    echo Changes will be live in 2-5 minutes at:
    echo https://infosquawk.github.io/ca-probate-appellate-repository
    echo.
    echo What was fixed:
    echo - All case opinions now have working PDF download links
    echo - PDF files copied to website directories
    echo - Professional document access for legal practitioners
) else (
    echo.
    echo ========================================
    echo Deployment Failed!
    echo ========================================
    echo Check git status and try again manually.
)

echo.
echo Press any key to exit...
pause >nul
