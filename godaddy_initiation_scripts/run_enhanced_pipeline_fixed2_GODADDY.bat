@echo off
REM ========================================
REM Enhanced Pipeline with ProBRep.com Deployment
REM Updated version of run_enhanced_pipeline_fixed2.bat
REM ========================================

echo ========================================
echo Scholar Podcast Pipeline with ProBRep.com Deployment
echo Starting Enhanced Pipeline with Comprehensive Naming
echo ========================================

REM Set the working directory
cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast"

REM Activate the virtual environment
echo Activating StyleTTS2 environment...
call "styletts2_env\Scripts\activate.bat"

REM Phase 1: Enhanced Smart Fallback Pipeline
echo.
echo ========================================
echo Phase 1: Enhanced Smart Fallback Pipeline
echo ========================================
python "enhanced_integrated_pipeline_smart_fallback_PODBEAN_ENHANCED_NAMING.py"

if %errorlevel% neq 0 (
    echo ERROR: Phase 1 failed with exit code %errorlevel%
    echo Pipeline terminated to prevent inconsistent state.
    pause
    exit /b %errorlevel%
)

echo Phase 1 completed successfully.

REM Phase 2: Comprehensive Case Name Extraction
echo.
echo ========================================
echo Phase 2: Comprehensive Case Name Extraction
echo ========================================
python "pdf_renamer_utility_comprehensive_final_fixed.py" --auto

if %errorlevel% neq 0 (
    echo WARNING: Phase 2 failed with exit code %errorlevel%
    echo Continuing with remaining phases...
    set PHASE2_FAILED=1
) else (
    echo Phase 2 completed successfully.
    set PHASE2_FAILED=0
)

REM Phase 3: Case Brief Generation and Audio Conversion
echo.
echo ========================================
echo Phase 3: Case Brief Generation and Audio Conversion
echo ========================================
python "case_brief_pipeline_integrated.py"

if %errorlevel% neq 0 (
    echo WARNING: Phase 3 failed with exit code %errorlevel%
    echo Continuing with remaining phases...
    set PHASE3_FAILED=1
) else (
    echo Phase 3 completed successfully.
    set PHASE3_FAILED=0
)

REM Phase 4: Special Edition Document Processing
echo.
echo ========================================
echo Phase 4: Special Edition Document Processing
echo ========================================
python "special_edition_pipeline.py"

if %errorlevel% neq 0 (
    echo WARNING: Phase 4 failed with exit code %errorlevel%
    echo Continuing with website deployment...
    set PHASE4_FAILED=1
) else (
    echo Phase 4 completed successfully.
    set PHASE4_FAILED=0
)

REM Phase 5: Website Integration & ProBRep.com Deployment
echo.
echo ========================================
echo Phase 5: Website Integration & ProBRep.com Deployment
echo ========================================
cd website

REM Check if GoDaddy configuration exists
if not exist "godaddy_config.ini" (
    echo ERROR: ProBRep.com configuration file not found!
    echo Please create website/godaddy_config.ini with your FTP credentials.
    echo See documentation for configuration template.
    echo.
    echo Skipping website deployment...
    set PHASE5_FAILED=1
    goto :SUMMARY
)

REM Execute GoDaddy website deployment
python "godaddy_initiation_scripts\website_integration_pipeline_godaddy.py"

if %errorlevel% neq 0 (
    echo WARNING: Website deployment to ProBRep.com failed with exit code %errorlevel%
    echo Content has been created but website was not updated.
    echo Website can be manually updated later using:
    echo   cd website
    echo   python godaddy_initiation_scripts\godaddy_deployment_pipeline.py
    set PHASE5_FAILED=1
) else (
    echo Phase 5: ProBRep.com deployment completed successfully.
    set PHASE5_FAILED=0
)

REM Return to main directory
cd ..

:SUMMARY
echo.
echo ========================================
echo Pipeline Execution Summary
echo ========================================

REM Calculate final exit code based on which phases failed
set FINAL_EXIT_CODE=0

if %PHASE2_FAILED%==1 (
    echo Phase 2: Comprehensive Naming - FAILED
    set /a FINAL_EXIT_CODE+=2
) else (
    echo Phase 2: Comprehensive Naming - SUCCESS
)

if %PHASE3_FAILED%==1 (
    echo Phase 3: Case Brief Generation - FAILED
    set /a FINAL_EXIT_CODE+=4
) else (
    echo Phase 3: Case Brief Generation - SUCCESS
)

if %PHASE4_FAILED%==1 (
    echo Phase 4: Special Edition Processing - FAILED
    set /a FINAL_EXIT_CODE+=8
) else (
    echo Phase 4: Special Edition Processing - SUCCESS
)

if %PHASE5_FAILED%==1 (
    echo Phase 5: ProBRep.com Deployment - FAILED
    set /a FINAL_EXIT_CODE+=16
) else (
    echo Phase 5: ProBRep.com Deployment - SUCCESS
)

echo.
if %FINAL_EXIT_CODE%==0 (
    echo ========================================
    echo ALL PHASES COMPLETED SUCCESSFULLY!
    echo ========================================
    echo - New podcast episodes created and uploaded
    echo - Case briefs generated with AI analysis
    echo - Special edition content processed
    echo - Website updated and deployed to ProBRep.com hosting
    echo.
    echo Your legal content platform is now live at https://probrep.com!
) else (
    echo ========================================
    echo PIPELINE COMPLETED WITH WARNINGS
    echo ========================================
    echo Some phases failed but core content was created.
    echo Check logs in the respective directories for detailed error information.
    echo.
    if %PHASE5_FAILED%==1 (
        echo NOTE: Website deployment failed. You can manually deploy using:
        echo   cd website
        echo   python godaddy_initiation_scripts\godaddy_deployment_pipeline.py
    )
)

echo.
echo Execution completed at %date% %time%
echo Check individual phase logs for detailed information.
echo.

REM Deactivate virtual environment
call deactivate

REM Keep window open for review
pause

REM Exit with appropriate code
exit /b %FINAL_EXIT_CODE%
