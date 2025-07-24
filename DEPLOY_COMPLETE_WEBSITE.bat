@echo off
echo ========================================
echo ProBrep.com Complete Website Deployment
echo ========================================
echo.
echo This script will:
echo - Upload the fixed website with working file links
echo - Upload all PDF documents (published and unpublished)
echo - Upload all text files and case briefs
echo - Upload cover images
echo - Create proper directory structure
echo - Verify successful deployment
echo.
echo Target: probrep.com via FTP
echo.

pause

echo.
echo Starting deployment...
echo.

python deploy_complete_website.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 🎉 DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Your website is now live with working file links!
    echo Visit: https://probrep.com
    echo.
    echo What's new:
    echo ✅ Episodes show working file download buttons
    echo ✅ PDFs, case briefs, and text files accessible
    echo ✅ Professional legal industry appearance
    echo ✅ Real-time database integration maintained
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ DEPLOYMENT HAD ISSUES
    echo ========================================
    echo.
    echo Check the output above for specific errors.
    echo You may need to:
    echo - Verify FTP credentials in godaddy_config.ini
    echo - Check internet connection
    echo - Ensure target directories are writable
    echo.
)

pause