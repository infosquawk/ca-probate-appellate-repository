@echo off
setlocal EnableDelayedExpansion

echo.
echo ========================================================================
echo              PROBREP.COM DEPLOYMENT INTERFACE
echo ========================================================================
echo.
echo 🌐 Deploy California Probate Repository to https://probrep.com
echo 🔧 User-friendly interface for FTP deployment operations
echo 📁 Current directory: %CD%
echo.

:MAIN_MENU
echo ========================================================================
echo                        DEPLOYMENT MENU
echo ========================================================================
echo.
echo Please select an option:
echo.
echo   [1] 🔍 Test FTP Connection
echo   [2] 🚀 Deploy Website to ProBrep.com  
echo   [3] ✅ Verify Deployment
echo   [4] 📊 Show Status
echo   [5] 🔄 Full Deployment (Deploy + Verify)
echo   [6] ❌ Exit
echo.
echo ========================================================================

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto TEST_CONNECTION
if "%choice%"=="2" goto DEPLOY_WEBSITE
if "%choice%"=="3" goto VERIFY_DEPLOYMENT  
if "%choice%"=="4" goto SHOW_STATUS
if "%choice%"=="5" goto FULL_DEPLOYMENT
if "%choice%"=="6" goto EXIT_PROGRAM

echo.
echo ❌ Invalid choice. Please enter a number between 1-6.
echo.
pause
goto MAIN_MENU

:TEST_CONNECTION
echo.
echo ========================================================================
echo 🔍 TESTING FTP CONNECTION TO PROBREP.COM
echo ========================================================================
echo.
echo 📡 Attempting to connect to ProBrep.com FTP server...
echo 🔐 Testing authentication credentials...
echo 📁 Verifying directory access...
echo.

python deploy_probrep_standalone.py test

if %errorlevel% equ 0 (
    echo.
    echo ✅ CONNECTION TEST SUCCESSFUL!
    echo 🎯 FTP connection is working properly
    echo 🔧 Ready for deployment operations
) else (
    echo.
    echo ❌ CONNECTION TEST FAILED!
    echo 🛠️  TROUBLESHOOTING STEPS:
    echo    1. Check internet connectivity
    echo    2. Verify FTP credentials in godaddy_config.json
    echo    3. Confirm ProBrep.com hosting account is active
    echo    4. Check firewall settings
)

echo.
pause
goto MAIN_MENU

:DEPLOY_WEBSITE
echo.
echo ========================================================================
echo 🚀 DEPLOYING WEBSITE TO PROBREP.COM
echo ========================================================================
echo.
echo ⚠️  This will upload all website files to ProBrep.com
echo 📁 Source: Current website directory
echo 🌐 Destination: https://probrep.com
echo.

set /p confirm="Continue with deployment? (Y/N): "

if /i "%confirm%" neq "Y" (
    echo.
    echo 🔄 Deployment cancelled by user
    echo.
    pause
    goto MAIN_MENU
)

echo.
echo 📤 Starting deployment process...
echo 🔄 This may take several minutes depending on content size
echo.

python deploy_probrep_standalone.py deploy

if %errorlevel% equ 0 (
    echo.
    echo ✅ DEPLOYMENT SUCCESSFUL!
    echo 🌐 Website has been uploaded to ProBrep.com
    echo 🔗 Visit: https://probrep.com to view your site
) else (
    echo.
    echo ❌ DEPLOYMENT FAILED!
    echo 🛠️  TROUBLESHOOTING STEPS:
    echo    1. Check FTP connection (Option 1)
    echo    2. Verify sufficient disk space on hosting account
    echo    3. Check file permissions and access rights
    echo    4. Review deployment logs for specific errors
)

echo.
pause
goto MAIN_MENU

:VERIFY_DEPLOYMENT
echo.
echo ========================================================================
echo ✅ VERIFYING DEPLOYMENT
echo ========================================================================
echo.
echo 🌐 Testing website accessibility...
echo 📋 Checking content integrity...
echo 🔍 Validating key elements...
echo.

python deploy_probrep_standalone.py verify

if %errorlevel% equ 0 (
    echo.
    echo ✅ VERIFICATION SUCCESSFUL!
    echo 🌐 Website is accessible and functioning properly
    echo 📊 Content appears to be intact
) else (
    echo.
    echo ❌ VERIFICATION FAILED!
    echo 🛠️  POSSIBLE ISSUES:
    echo    1. Website may not be fully uploaded
    echo    2. DNS propagation might be in progress
    echo    3. Hosting server may be temporarily unavailable
    echo    4. Content may need time to be processed
)

echo.
pause
goto MAIN_MENU

:SHOW_STATUS  
echo.
echo ========================================================================
echo 📊 DEPLOYMENT STATUS
echo ========================================================================
echo.

python deploy_probrep_standalone.py status

echo.
pause
goto MAIN_MENU

:FULL_DEPLOYMENT
echo.
echo ========================================================================
echo 🔄 FULL DEPLOYMENT PROCESS
echo ========================================================================
echo.
echo 🎯 This will perform a complete deployment workflow:
echo    1. Deploy website to ProBrep.com
echo    2. Verify deployment success
echo    3. Report final status
echo.

set /p confirm="Continue with full deployment? (Y/N): "

if /i "%confirm%" neq "Y" (
    echo.
    echo 🔄 Full deployment cancelled by user
    echo.
    pause
    goto MAIN_MENU
)

echo.
echo ========================================================================
echo STEP 1: DEPLOYING WEBSITE
echo ========================================================================

python deploy_probrep_standalone.py deploy

if %errorlevel% neq 0 (
    echo.
    echo ❌ Deployment failed - stopping full deployment process
    echo.
    pause
    goto MAIN_MENU
)

echo.
echo ========================================================================  
echo STEP 2: VERIFYING DEPLOYMENT
echo ========================================================================

REM Wait a moment for deployment to propagate
timeout /t 5 /nobreak > nul

python deploy_probrep_standalone.py verify

if %errorlevel% equ 0 (
    echo.
    echo ========================================================================
    echo ✅ FULL DEPLOYMENT COMPLETED SUCCESSFULLY!
    echo ========================================================================
    echo.
    echo 🎉 DEPLOYMENT SUMMARY:
    echo    ✅ Website successfully uploaded to ProBrep.com
    echo    ✅ Deployment verification passed
    echo    🌐 Site is accessible at https://probrep.com
    echo    📊 All content appears to be functioning properly
    echo.
    echo 🎯 NEXT STEPS:
    echo    1. Visit https://probrep.com to review your site
    echo    2. Test episode playback and navigation
    echo    3. Verify all links and content are working
    echo    4. Monitor site performance and analytics
    echo.
) else (
    echo.
    echo ========================================================================
    echo ⚠️  DEPLOYMENT COMPLETED WITH WARNINGS
    echo ========================================================================
    echo.
    echo 📊 DEPLOYMENT SUMMARY:
    echo    ✅ Website successfully uploaded to ProBrep.com
    echo    ⚠️  Verification encountered issues
    echo    🔍 Manual verification may be required
    echo.
    echo 🛠️  RECOMMENDED ACTIONS:
    echo    1. Wait 5-10 minutes for DNS propagation
    echo    2. Try verification again (Option 3)
    echo    3. Manually visit https://probrep.com
    echo    4. Check hosting account for any issues
    echo.
)

echo.
pause
goto MAIN_MENU

:EXIT_PROGRAM
echo.
echo ========================================================================
echo 👋 EXITING PROBREP.COM DEPLOYMENT INTERFACE
echo ========================================================================
echo.
echo 📋 Session Summary:
echo    🕒 Session started: %date% %time%
echo    📁 Working directory: %CD%
echo    🌐 Target: https://probrep.com
echo.
echo 🔗 For additional support:
echo    📄 Check deployment logs in the logs directory  
echo    📚 Review documentation files for troubleshooting
echo    🌐 Visit https://probrep.com to verify site status
echo.
echo Thank you for using the ProBrep.com Deployment Interface!
echo.
pause
exit /b 0

:ERROR_HANDLER
echo.
echo ========================================================================
echo ❌ AN ERROR OCCURRED
echo ========================================================================
echo.
echo 🔍 Error Code: %errorlevel%
echo 📋 An unexpected error occurred during execution
echo.
echo 🛠️  TROUBLESHOOTING STEPS:
echo    1. Check that Python is installed and accessible
echo    2. Verify deploy_probrep_standalone.py exists in current directory
echo    3. Check file permissions and access rights
echo    4. Review any error messages above
echo    5. Try running individual commands manually
echo.
echo 📧 If problems persist, check the logs directory for detailed information
echo.
pause
goto MAIN_MENU
