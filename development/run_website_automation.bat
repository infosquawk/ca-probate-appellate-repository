@echo off
echo.
echo ===============================================
echo  WEBSITE AUTOMATION SCRIPT
echo  California Probate Code Appellate Repository
echo ===============================================
echo.

cd /d "%~dp0"
cd ..

echo Starting website automation...
echo.

python "website\development\website_automation_script.py"

echo.
echo ===============================================
echo  Website automation completed
echo ===============================================
echo.

pause
