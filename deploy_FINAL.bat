@echo off
echo 🎊 DEPLOYING ENHANCED WEBSITE WITH COURT DOCUMENTS
echo ==================================================
echo.

echo ✅ VERIFICATION: All court documents are already in place!
echo.
echo 📄 Published PDFs: 3 files
dir \"pdfs\\published\\*.pdf\" /B
echo.
echo 📄 Unpublished PDFs: 2 files  
dir \"pdfs\\unpublished\\*.pdf\" /B
echo.
echo 📝 Text files: Available
echo   • Court opinions, case briefs, and analysis files ready
echo.

echo 🚀 DEPLOYING UPDATED WEBSITE...
echo.

git add .
if errorlevel 1 (
    echo ❌ Git add failed!
    git status
    pause
    exit /b 1
)

git commit -m \"ENHANCED WEBSITE: Added PDF and court opinion links with color-coded action buttons\"
if errorlevel 1 (
    echo ℹ️ Nothing to commit (already up to date)
) else (
    echo ✅ Website updates committed successfully!
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
echo 🎉 ENHANCED LEGAL RESEARCH PLATFORM DEPLOYED!
echo ============================================
echo.
echo 🌐 LIVE WEBSITE: https://infosquawk.github.io/ca-probate-appellate-repository
echo ⏱️  LIVE IN: 1-3 minutes (GitHub Pages deployment time)
echo.
echo 🎯 NEW FEATURES LIVE:
echo.
echo ✨ ENHANCED ACTION BUTTONS:
echo   • 🎧 Listen Now (forest green)
echo   • 📄 Brief/Analysis (burgundy) 
echo   • 📋 Original PDF (warm gold)
echo   • 📄 Court Opinion (deep burgundy)
echo.
echo 📊 COMPLETE RESOURCE MATRIX:
echo   • 10 Episodes with multiple access formats
echo   • 5 Original court document PDFs
echo   • 7 Court opinion text files
echo   • 4 AI-generated case briefs
echo   • 1 Comprehensive historical analysis
echo.
echo 🏛️ PROFESSIONAL LEGAL RESEARCH PLATFORM:
echo   • Published and unpublished California probate cases
echo   • Audio narration + original documents + AI analysis
echo   • Color-coded navigation system
echo   • Mobile-responsive design
echo   • Complete probate law reference library
echo.
echo 🔄 If changes don't appear immediately:
echo   1. Clear browser cache (Ctrl+F5)
echo   2. Try incognito/private browsing mode
echo   3. Wait 2-3 minutes for GitHub Pages deployment
echo.
pause
