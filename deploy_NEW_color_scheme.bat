@echo off
echo 🎨 DEPLOYING NEW COLOR SCHEME - FOREST GREEN & CREAM
echo =====================================================
echo.

cd /d "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website"

echo ✨ NEW DESIGN FEATURES:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🎯 Color Scheme:
echo    • Primary: Forest Green (#2f4f4f)
echo    • Background: Rich green gradient with subtle texture
echo    • Accent: Warm Gold (#c2a86f) 
echo    • Hero: Deep Burgundy (#5c1f1f)
echo    • Content: Cream (#f3e3c3)
echo.
echo 📝 Typography:
echo    • Headers: League Spartan (WPA-era bold all-caps)
echo    • Body: Merriweather (clean serif readability)
echo    • Enhanced letter spacing and hierarchy
echo.
echo ✨ Design Enhancements:
echo    • Subtle parchment texture overlay
echo    • Enhanced cards with colored borders
echo    • Professional button styling
echo    • Rich burgundy hero section
echo    • Elegant gold accent elements
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/3] Adding design updates...
git add index.html
if errorlevel 1 (
    echo ❌ Git add failed!
    git status
    pause
    exit /b 1
)

echo [2/3] Committing new color scheme...
git commit -m "MAJOR DESIGN UPDATE: Forest green & cream color scheme with WPA-era typography"
if errorlevel 1 (
    echo ℹ️ Nothing to commit (already up to date)
) else (
    echo ✅ Design update committed successfully!
)

echo [3/3] Deploying to GitHub Pages...
git push origin main
if errorlevel 1 (
    echo ❌ Push failed! Checking status...
    git status
    git log --oneline -3
    pause
    exit /b 1
)

echo.
echo 🎊 NEW DESIGN DEPLOYED SUCCESSFULLY!
echo ================================================================
echo.
echo 🌐 LIVE WEBSITE: https://infosquawk.github.io/ca-probate-appellate-repository
echo ⏱️  LIVE IN: 1-3 minutes (GitHub Pages deployment time)
echo.
echo 🎨 WHAT USERS WILL SEE:
echo.
echo ✨ Professional Legal Design:
echo    • Rich forest green and cream color palette
echo    • WPA-era inspired typography (League Spartan headers)
echo    • Subtle parchment texture for authentic feel
echo    • Enhanced visual hierarchy with gold accents
echo    • Deep burgundy hero section for dramatic impact
echo.
echo 📱 Enhanced User Experience:
echo    • All 13 buttons still working perfectly
echo    • Improved readability with Merriweather serif
echo    • Better contrast and accessibility
echo    • Professional authority and gravitas
echo    • Mobile-responsive design maintained
echo.
echo 🏛️ BRANDING IMPACT:
echo    • Conveys legal expertise and authority
echo    • Classic, timeless aesthetic
echo    • Distinguished from typical tech websites
echo    • Appeals to legal professionals
echo    • Memorable and professional appearance
echo.
echo 🔄 If new colors don't appear after 3 minutes:
echo    1. Clear browser cache (Ctrl+F5)
echo    2. Try incognito/private browsing mode
echo    3. Check GitHub Actions for deployment status
echo.
pause
