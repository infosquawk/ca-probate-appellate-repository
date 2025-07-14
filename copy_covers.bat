@echo off
echo 🎨 COPYING PODCAST COVER IMAGES TO WEBSITE
echo ==========================================
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast"

echo Copying cover images to website directory...

copy "cover.png" "website\covers\cover_opinions.png"
if errorlevel 1 (
    echo ❌ Failed to copy opinion cover
) else (
    echo ✅ Opinion cover copied successfully
)

copy "cover_briefing.png" "website\covers\cover_briefs.png"
if errorlevel 1 (
    echo ❌ Failed to copy briefing cover
) else (
    echo ✅ Case brief cover copied successfully
)

copy "cover_special_edition.png" "website\covers\cover_special.png"
if errorlevel 1 (
    echo ❌ Failed to copy special edition cover
) else (
    echo ✅ Special edition cover copied successfully
)

echo.
echo 🎉 All podcast covers copied to website/covers/
echo Ready to update website with clickable cover navigation!
echo.
pause
