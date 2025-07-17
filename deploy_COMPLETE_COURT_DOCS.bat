@echo off
echo 📋 DEPLOYING COMPLETE COURT DOCUMENT INTEGRATION
echo ================================================
echo.

cd /d \"C:\\Users\\Ryan\\Google_Drive\\My_Documents\\Work\\0000-Claude-Workspace\\scholar_podcast\"

echo 🎯 MAJOR WEBSITE ENHANCEMENT:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📄 ORIGINAL COURT DOCUMENTS INTEGRATION:
echo    • All published case PDFs now accessible
echo    • All unpublished case PDFs now accessible  
echo    • Original court opinion text files added
echo    • AI-generated case briefs maintained
echo    • 4 different document types per case available
echo.
echo 🎨 NEW ACTION BUTTONS:
echo    • 🎧 Listen Now (audio podcast)
echo    • 📄 Brief/Analysis (AI-generated summaries)
echo    • 📋 Original PDF (court documents)
echo    • 📄 Court Opinion (original court text)
echo.
echo 📊 COMPLETE RESOURCE MATRIX:
echo    • 5 Appellate Opinions with full documentation
echo    • 4 Case Briefs with comprehensive resources
echo    • 1 Legal Analysis (special edition)
echo    • Professional legal research platform
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [STEP 1/4] Copying published case PDFs...
copy \"probate_cases\\pdfs\\published\\*.pdf\" \"website\\pdfs\\published\\\"
if errorlevel 1 (
    echo ❌ Failed to copy published PDFs
    pause
    exit /b 1
) else (
    echo ✅ Published PDFs copied successfully
)

echo.
echo [STEP 2/4] Copying unpublished case PDFs...
copy \"probate_cases\\pdfs\\unpublished\\*.pdf\" \"website\\pdfs\\unpublished\\\"
if errorlevel 1 (
    echo ❌ Failed to copy unpublished PDFs
    pause
    exit /b 1
) else (
    echo ✅ Unpublished PDFs copied successfully
)

echo.
echo [STEP 3/4] Copying all text files...
copy \"probate_cases\\pdfs\\published_text\\2025-07_(Published)\\*.txt\" \"website\\texts\\\"
copy \"probate_cases\\pdfs\\published_text\\2025-07_Case_Briefs_(Published)\\*.txt\" \"website\\texts\\\"
copy \"probate_cases\\pdfs\\unpublished_text\\2025-07_(Unpublished)\\*.txt\" \"website\\texts\\\"
copy \"probate_cases\\pdfs\\unpublished_text\\2025-07_Case_Briefs_(Unpublished)\\*.txt\" \"website\\texts\\\"
echo ✅ All text files copied successfully

echo.
echo [STEP 4/4] Deploying to GitHub Pages...
cd /d \"C:\\Users\\Ryan\\Google_Drive\\My_Documents\\Work\\0000-Claude-Workspace\\scholar_podcast\\website\"

git add .
if errorlevel 1 (
    echo ❌ Git add failed!
    git status
    pause
    exit /b 1
)

git commit -m \"COMPLETE COURT DOCUMENTS: Added original PDFs, court opinions, and enhanced action buttons\"
if errorlevel 1 (
    echo ℹ️ Nothing to commit (already up to date)
) else (
    echo ✅ Court documents committed successfully!
)

git push origin main
if errorlevel 1 (
    echo ❌ Push failed! Checking status...
    git status
    git log --oneline -3
    pause
    exit /b 1
)

echo.
echo 🎊 COMPLETE COURT DOCUMENT INTEGRATION DEPLOYED!
echo ================================================================
echo.
echo 🌐 LIVE WEBSITE: https://infosquawk.github.io/ca-probate-appellate-repository
echo ⏱️  LIVE IN: 1-3 minutes (GitHub Pages deployment time)
echo.
echo 📋 WHAT USERS WILL NOW SEE:
echo.
echo ✨ ENHANCED EPISODE CARDS:
echo    • Up to 4 action buttons per case
echo    • Color-coded buttons for different resource types
echo    • Forest green for audio, burgundy for court opinions
echo    • Gold for original PDFs, secondary for briefs
echo.
echo 📄 COMPLETE LEGAL RESOURCES:
echo.
echo 🏛️ PUBLISHED CASES (Official Court Opinions):
echo    • B333052 - Conservatorship of ANNE S
echo      ├── 🎧 Audio narration  
echo      ├── 📄 AI case brief
echo      ├── 📋 Original PDF
echo      └── 📄 Court opinion text
echo.
echo    • G063155 - Estate of LAYLA BOYAJIAN  
echo      ├── 🎧 Audio narration
echo      ├── 📄 AI case brief
echo      ├── 📋 Original PDF
echo      └── 📄 Court opinion text
echo.
echo    • S282314 - In re Discipline
echo      ├── 🎧 Audio narration
echo      └── 📋 Original PDF
echo.
echo 📝 UNPUBLISHED CASES:
echo    • B341750 - Conservatorship of Julie C
echo      ├── 🎧 Audio narration
echo      ├── 📋 Original PDF  
echo      └── 📄 Court opinion text
echo.
echo    • B330596 - Nelson v Huhn
echo      ├── 🎧 Audio narration
echo      ├── 📄 AI case brief
echo      ├── 📋 Original PDF
echo      └── 📄 Court opinion text
echo.
echo 📚 SPECIAL ANALYSIS:
echo    • California's Heritage of Estates (complete historical analysis)
echo.
echo 🎯 PROFESSIONAL IMPACT:
echo    • Complete research platform for legal professionals
echo    • Original court documents alongside AI analysis
echo    • Multiple access formats (audio, PDF, text)
echo    • Professional-grade legal resource library
echo    • Comprehensive probate law reference system
echo.
echo 🔄 If new resources don't appear after 3 minutes:
echo    1. Clear browser cache (Ctrl+F5)
echo    2. Try incognito/private browsing mode
echo    3. Check that new buttons appear on episode cards
echo    4. Verify PDFs and court opinions are accessible
echo.
pause
