#!/bin/bash
#
# Logo-Only Solution - Keep Functionality, Logo Only
#

echo "🎯 LOGO-ONLY SOLUTION"
echo "====================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Remove ALL CSS that we added (this is causing the JS errors)
echo "🧹 Removing ALL custom CSS that might break JavaScript..."

# Remove all our CSS files
rm -f "$OPENSPECIMEN_DIR/minimal-branding.css" 2>/dev/null
rm -f "$OPENSPECIMEN_DIR/ui-app/post-login-minimal.css" 2>/dev/null
rm -f "$OPENSPECIMEN_DIR/ui-app/bharat-theme.css" 2>/dev/null
rm -f "$OPENSPECIMEN_DIR/ui-app/safe-branding.css" 2>/dev/null

# Remove CSS references from HTML files
sed -i '/minimal-branding.css/d' "$OPENSPECIMEN_DIR"/*.html 2>/dev/null
sed -i '/post-login-minimal.css/d' "$OPENSPECIMEN_DIR"/ui-app/*.html 2>/dev/null
sed -i '/bharat-theme.css/d' "$OPENSPECIMEN_DIR"/ui-app/*.html 2>/dev/null

# 2. Keep ONLY the logo and favicon changes (these work without breaking JS)
echo "🖼️ Keeping only logo and favicon changes..."

# Ensure logo files are in place
if [ -f "/home/adb/openspecimen/images/longevity-india-logo-web.png" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/images/os_logo.a585165a.png"
    echo "✅ Logo file confirmed in place"
fi

# Ensure favicon is in place
if [ -f "/home/adb/openspecimen/images/longevity-india-favicon.ico" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-favicon.ico" "$OPENSPECIMEN_DIR/favicon.ico"
    cp "/home/adb/openspecimen/images/longevity-india-favicon.ico" "$OPENSPECIMEN_DIR/ui-app/favicon.ico"
    echo "✅ Favicon confirmed in place"
fi

# 3. Keep only page title changes (safe)
echo "📄 Keeping only page title changes..."
if ! grep -q "BHARAT Study" "$OPENSPECIMEN_DIR/index.html" 2>/dev/null; then
    sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title>|g' "$OPENSPECIMEN_DIR"/*.html 2>/dev/null
    sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title>|g' "$OPENSPECIMEN_DIR"/ui-app/*.html 2>/dev/null
fi

# 4. Remove any CSS links we added that might be causing issues
echo "🔗 Cleaning up HTML files..."
sed -i '/<link rel="stylesheet" href=".*post-login.*css">/d' "$OPENSPECIMEN_DIR"/ui-app/index.html 2>/dev/null
sed -i '/<link rel="stylesheet" href=".*minimal.*css">/d' "$OPENSPECIMEN_DIR"/*.html 2>/dev/null

# 5. Restore clean HTML structure
echo "📄 Ensuring clean HTML structure..."
# Make sure the ui-app index.html is clean
if [ -f "$OPENSPECIMEN_DIR/ui-app/index.html.backup" ]; then
    echo "🔄 Restoring from backup..."
    cp "$OPENSPECIMEN_DIR/ui-app/index.html.backup" "$OPENSPECIMEN_DIR/ui-app/index.html"
    # Re-apply only safe changes
    sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title>|g' "$OPENSPECIMEN_DIR/ui-app/index.html"
fi

echo ""
echo "====================="
echo "✅ LOGO-ONLY SOLUTION APPLIED!"
echo "====================="
echo ""
echo "✅ Removed all custom CSS (cause of JS errors)"
echo "✅ Kept logo file replacement (works perfectly)"
echo "✅ Kept favicon changes"
echo "✅ Kept page title changes"
echo "❌ Removed color scheme (to prevent JS errors)"
echo ""
echo "🎯 Result:"
echo "   • OpenSpecimen should work normally"
echo "   • Longevity India logo visible"
echo "   • BHARAT Study in page title"
echo "   • No custom colors (to avoid breaking JS)"
echo ""
echo "🔄 Test now:"
echo "   1. Clear browser cache"
echo "   2. Login - should work without white screen"
echo "   3. Logo should be visible and functional"
echo ""
echo "💡 Next steps if this works:"
echo "   • We can add colors later using a different approach"
echo "   • Or use external CSS loaded after page loads"
echo "   • Focus on functionality first, aesthetics second"
echo "====================="