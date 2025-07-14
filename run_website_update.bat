@echo off
echo ==========================================
echo  California Probate Repository
echo  Comprehensive Website Update Script
echo ==========================================
echo.

cd /d "%~dp0"

echo Starting comprehensive website update...
echo.

python comprehensive_website_updater.py

echo.
echo ==========================================
echo  Update Complete!
echo ==========================================
echo.
echo Press any key to continue...
pause >nul
