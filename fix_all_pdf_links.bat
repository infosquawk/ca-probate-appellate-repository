@echo off
echo ========================================
echo Fixing All PDF Links in Website
echo ========================================

cd /d "%~dp0"

echo Step 1: Copy missing PDF files...
call copy_missing_pdfs.bat

echo.
echo Step 2: Update website episode data...
python fix_pdf_links.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo PDF Links Fix Complete!
    echo ========================================
    echo.
    echo Updated episodes with PDF links:
    echo - B341350: pdfs/unpublished/B341350_a_Minor_ISMAEL_H_et_al_v_BERNARDINO_G_unpublished.pdf
    echo - C102321: pdfs/unpublished/C102321_Conservatorship_of_the_Person_of_C_unpublished.pdf  
    echo - G063155: pdfs/published/G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf
    echo - B333052: pdfs/published/B333052_Conservatorship_of_ANNE_S_published.pdf
    echo - S282314: pdfs/published/S282314_In_re_Discipline_published.pdf
) else (
    echo ERROR: Failed to update PDF links
)

pause
