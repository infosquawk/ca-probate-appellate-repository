@echo off
echo ========================================
echo Copying Missing PDF Files to Website
echo ========================================

cd /d "%~dp0"

echo Creating directories...
if not exist "pdfs\published" mkdir "pdfs\published"
if not exist "pdfs\unpublished" mkdir "pdfs\unpublished"

echo.
echo Copying Published PDFs...
if exist "..\probate_cases\pdfs\published\B333052_Conservatorship_of_ANNE_S_published.pdf" (
    copy "..\probate_cases\pdfs\published\B333052_Conservatorship_of_ANNE_S_published.pdf" "pdfs\published\"
    echo Copied B333052_Conservatorship_of_ANNE_S_published.pdf
) else (
    echo B333052_Conservatorship_of_ANNE_S_published.pdf not found in source
)

if exist "..\probate_cases\pdfs\published\G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf" (
    copy "..\probate_cases\pdfs\published\G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf" "pdfs\published\"
    echo Copied G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf
) else (
    echo G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf not found in source
)

if exist "..\probate_cases\pdfs\published\S282314_In_re_Discipline_published.pdf" (
    copy "..\probate_cases\pdfs\published\S282314_In_re_Discipline_published.pdf" "pdfs\published\"
    echo Copied S282314_In_re_Discipline_published.pdf
) else (
    echo S282314_In_re_Discipline_published.pdf not found in source
)

echo.
echo Copying Missing Unpublished PDFs...
if exist "..\probate_cases\pdfs\unpublished\B341350_a_Minor_ISMAEL_H_et_al_v_BERNARDINO_G_unpublished.pdf" (
    copy "..\probate_cases\pdfs\unpublished\B341350_a_Minor_ISMAEL_H_et_al_v_BERNARDINO_G_unpublished.pdf" "pdfs\unpublished\"
    echo Copied B341350_a_Minor_ISMAEL_H_et_al_v_BERNARDINO_G_unpublished.pdf
) else (
    echo B341350_a_Minor_ISMAEL_H_et_al_v_BERNARDINO_G_unpublished.pdf not found in source
)

if exist "..\probate_cases\pdfs\unpublished\C102321_Conservatorship_of_the_Person_of_C_unpublished.pdf" (
    copy "..\probate_cases\pdfs\unpublished\C102321_Conservatorship_of_the_Person_of_C_unpublished.pdf" "pdfs\unpublished\"
    echo Copied C102321_Conservatorship_of_the_Person_of_C_unpublished.pdf
) else (
    echo C102321_Conservatorship_of_the_Person_of_C_unpublished.pdf not found in source
)

echo.
echo ========================================
echo PDF Copy Complete!
echo ========================================
echo.
echo Updated files in website pdfs directory:
dir pdfs\published /B
dir pdfs\unpublished /B

pause
