#!/bin/bash
#
# Restore Original OpenSpecimen Functionality
#

echo "🔄 RESTORING ORIGINAL OPENSPECIMEN"
echo "=================================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Restore original HTML files from backup if they exist
echo "📄 Restoring HTML files..."
if [ -f "$OPENSPECIMEN_DIR/index.html.backup" ]; then
    cp "$OPENSPECIMEN_DIR/index.html.backup" "$OPENSPECIMEN_DIR/index.html"
    echo "✅ Restored main index.html"
fi

if [ -f "$OPENSPECIMEN_DIR/ui-app/index.html.backup" ]; then
    cp "$OPENSPECIMEN_DIR/ui-app/index.html.backup" "$OPENSPECIMEN_DIR/ui-app/index.html"
    echo "✅ Restored ui-app index.html"
fi

# 2. Remove all custom CSS and JS references
echo "🧹 Cleaning HTML files..."
find "$OPENSPECIMEN_DIR" -name "*.html" -exec sed -i '/longevity/d; /liims/d; /LIIMS/d' {} \;

# 3. Restore original JavaScript files by reverting text changes
echo "📜 Reverting JavaScript changes..."
find "$OPENSPECIMEN_DIR" -name "*.js" -exec sed -i 's/LIIMS/OpenSpecimen/g; s/liims/openspecimen/g' {} \;

# 4. Remove all custom files
echo "🗑️ Removing custom files..."
rm -f "$OPENSPECIMEN_DIR"/ui-app/*longevity* 2>/dev/null
rm -f "$OPENSPECIMEN_DIR"/ui-app/*liims* 2>/dev/null
rm -f "$OPENSPECIMEN_DIR"/ui-app/*LIIMS* 2>/dev/null
rm -f "$OPENSPECIMEN_DIR"/*longevity* 2>/dev/null
rm -f "$OPENSPECIMEN_DIR"/*liims* 2>/dev/null

# 5. Restore any original logo files if they got overwritten
echo "🖼️ Checking logo files..."
if [ -f "/home/adb/openspecimen/images/longevity-india-logo-web.png" ]; then
    # We have custom logos, but let's restore original OpenSpecimen logos
    echo "⚠️ Custom logos present but not restoring to avoid breaking"
fi

# 6. Clean up CSS overrides
echo "🎨 Removing CSS overrides..."
find "$OPENSPECIMEN_DIR" -name "*.css" -exec sed -i '/Longevity India/,+10d' {} \; 2>/dev/null

echo ""
echo "=================================="
echo "✅ RESTORATION COMPLETE"
echo "=================================="
echo ""
echo "🔄 Now:"
echo "   1. Restart Tomcat: sudo systemctl restart tomcat9"
echo "   2. Clear browser cache completely"
echo "   3. Try logging in again"
echo ""
echo "💡 If it still doesn't work:"
echo "   1. Check Tomcat logs: sudo tail -f /opt/tomcat9/logs/catalina.out"
echo "   2. May need to redeploy the WAR file"
echo "=================================="