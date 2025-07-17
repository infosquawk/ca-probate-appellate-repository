@echo off
echo 📄 MANUAL COPY OF COURT DOCUMENTS
echo ================================
echo.

echo Current directory: %CD%
echo.

echo [DEBUG] Checking file structure...
echo Looking for: ..\probate_cases\pdfs\published\
dir "..\probate_cases\pdfs\published\" 2>nul
if errorlevel 1 (
    echo ❌ Path not found, trying alternative...
    dir "..\..\probate_cases\pdfs\published\" 2>nul
    if errorlevel 1 (
        echo ❌ Still not found. Let's check what directories exist:
        echo.
        echo Contents of parent directory:
        dir ".." /AD
        echo.
        echo Contents of current directory:
        dir "." /AD
        pause
        exit /b 1
    ) else (
        echo ✅ Found at alternative path: ..\..\probate_cases\pdfs\published\
        set "SOURCE_PATH=..\.."
    )
) else (
    echo ✅ Found at path: ..\probate_cases\pdfs\published\
    set "SOURCE_PATH=.."
)

echo.
echo [STEP 1] Creating directories if needed...
if not exist "pdfs\published" mkdir "pdfs\published"
if not exist "pdfs\unpublished" mkdir "pdfs\unpublished"
if not exist "texts" mkdir "texts"

echo.
echo [STEP 2] Copying published PDFs...
copy "%SOURCE_PATH%\probate_cases\pdfs\published\*.pdf" "pdfs\published\"
echo Files copied to pdfs\published\:
dir "pdfs\published\*.pdf"

echo.
echo [STEP 3] Copying unpublished PDFs...
copy "%SOURCE_PATH%\probate_cases\pdfs\unpublished\*.pdf" "pdfs\unpublished\"
echo Files copied to pdfs\unpublished\:
dir "pdfs\unpublished\*.pdf"

echo.
echo [STEP 4] Copying text files...
copy "%SOURCE_PATH%\probate_cases\pdfs\published_text\2025-07_(Published)\*.txt" "texts\"
copy "%SOURCE_PATH%\probate_cases\pdfs\published_text\2025-07_Case_Briefs_(Published)\*.txt" "texts\"
copy "%SOURCE_PATH%\probate_cases\pdfs\unpublished_text\2025-07_(Unpublished)\*.txt" "texts\"
copy "%SOURCE_PATH%\probate_cases\pdfs\unpublished_text\2025-07_Case_Briefs_(Unpublished)\*.txt" "texts\"

echo.
echo ✅ COPY PROCESS COMPLETE!
echo.
echo 📊 SUMMARY OF COPIED FILES:
echo.
echo PDFs in pdfs\published\:
dir "pdfs\published\*.pdf" /B 2>nul
echo.
echo PDFs in pdfs\unpublished\:
dir "pdfs\unpublished\*.pdf" /B 2>nul
echo.
echo Text files in texts\:
dir "texts\*.txt" /B 2>nul | findstr /V "brief\|heritage"
echo.
echo Now you can run the deployment script!
echo.
pause
