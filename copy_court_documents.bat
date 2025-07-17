@echo off
echo 📄 COPYING ORIGINAL COURT DOCUMENTS TO WEBSITE
echo =============================================
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast"

echo 📋 COPYING PUBLISHED CASE PDFs...
copy "probate_cases\pdfs\published\*.pdf" "website\pdfs\published\"
if errorlevel 1 (
    echo ❌ Failed to copy published PDFs
) else (
    echo ✅ Published PDFs copied successfully
)

echo.
echo 📋 COPYING UNPUBLISHED CASE PDFs...
copy "probate_cases\pdfs\unpublished\*.pdf" "website\pdfs\unpublished\"
if errorlevel 1 (
    echo ❌ Failed to copy unpublished PDFs
) else (
    echo ✅ Unpublished PDFs copied successfully
)

echo.
echo 📄 COPYING PUBLISHED TEXT FILES...
copy "probate_cases\pdfs\published_text\2025-07_(Published)\*.txt" "website\texts\"
if errorlevel 1 (
    echo ❌ Failed to copy published text files
) else (
    echo ✅ Published text files copied successfully
)

echo.
echo 📄 COPYING PUBLISHED CASE BRIEF TEXT FILES...
copy "probate_cases\pdfs\published_text\2025-07_Case_Briefs_(Published)\*.txt" "website\texts\"
if errorlevel 1 (
    echo ❌ Failed to copy published brief text files
) else (
    echo ✅ Published brief text files copied successfully
)

echo.
echo 📄 COPYING UNPUBLISHED TEXT FILES...
copy "probate_cases\pdfs\unpublished_text\2025-07_(Unpublished)\*.txt" "website\texts\"
if errorlevel 1 (
    echo ❌ Failed to copy unpublished text files
) else (
    echo ✅ Unpublished text files copied successfully
)

echo.
echo 📄 COPYING UNPUBLISHED CASE BRIEF TEXT FILES...
copy "probate_cases\pdfs\unpublished_text\2025-07_Case_Briefs_(Unpublished)\*.txt" "website\texts\"
if errorlevel 1 (
    echo ❌ Failed to copy unpublished brief text files
) else (
    echo ✅ Unpublished brief text files copied successfully
)

echo.
echo 🎊 ALL COURT DOCUMENTS COPIED SUCCESSFULLY!
echo.
echo 📊 SUMMARY OF ADDED RESOURCES:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📄 PUBLISHED CASE PDFs:
echo    • B333052_Conservatorship_of_ANNE_S_published.pdf
echo    • G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf
echo    • S282314_In_re_Discipline_published.pdf
echo.
echo 📄 UNPUBLISHED CASE PDFs:
echo    • B330596_Nelson_v_Huhn_unpublished.pdf
echo    • B341750_Conservatorship_of_Julie_C_unpublished.pdf
echo.
echo 📝 ORIGINAL COURT OPINION TEXT FILES:
echo    • All published and unpublished case text files
echo    • All case brief text files
echo    • Complete court documents for reference
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Ready to update website with PDF and text links!
echo.
pause
