@echo off
echo Copying podcast cover images to website covers directory...

set SOURCE_DIR=C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast
set DEST_DIR=C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\covers

echo Copying main opinion cover...
copy "%SOURCE_DIR%\cover.png" "%DEST_DIR%\cover_opinions.png"

echo Copying case brief cover...
copy "%SOURCE_DIR%\cover_briefing.png" "%DEST_DIR%\cover_briefs.png"

echo Copying special edition cover...
copy "%SOURCE_DIR%\cover_special_edition.png" "%DEST_DIR%\cover_special.png"

echo ✅ All covers copied successfully!
pause
