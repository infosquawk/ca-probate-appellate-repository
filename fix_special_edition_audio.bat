@echo off
echo ========================================
echo FIXING Special Edition Audio Link
echo ========================================
cd "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"
echo Running comprehensive website updater with special edition audio fix...
python comprehensive_website_updater.py
echo.
if %errorlevel% equ 0 (
    echo ✅ SUCCESS: Special edition audio link should now be working!
    echo The website now includes the Podbean URL for California's Heritage of Estates
) else (
    echo ❌ Error occurred during website update
)
echo.
echo Special Edition: California's Heritage of Estates
echo - Audio URL: https://www.podbean.com/ew/pb-thdza-1904721
echo - Text URL: texts/2025-07-13_Californias_Heritage_of_Estates_analysis.txt
echo - Status: Both audio and text links should now work!
echo.
pause