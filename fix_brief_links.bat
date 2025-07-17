@echo off
echo ========================================
echo Brief Links Fix - Website Updater
echo ========================================
cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"
echo Running comprehensive website updater...
python comprehensive_website_updater.py
echo.
if %errorlevel% equ 0 (
    echo ✅ SUCCESS: Brief links should now be working!
    echo The website has been updated with the newly available brief files.
) else (
    echo ❌ Error occurred during website update
)
echo.
echo The following brief files were added and should now have working links:
echo - B341350_(Case_Brief)_Unknown_(unpublished).txt
echo - C102321_(Case_Brief)_Unknown_(unpublished).txt
echo.
pause