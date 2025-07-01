#!/bin/bash
#
# Restore JavaScript functionality by reverting problematic text replacements
#

echo "🛠️ RESTORING JAVASCRIPT FUNCTIONALITY"
echo "====================================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Restore critical JavaScript files that might have been broken
echo "🔧 Checking for broken JavaScript references..."

# Only revert replacements in critical areas that might break functionality
find "$OPENSPECIMEN_DIR" -name "*.js" -path "*/ui-app/*" -exec grep -l "liims" {} \; | while read jsfile; do
    echo "⚠️ Checking: $jsfile"
    
    # Revert specific patterns that might break URLs or API calls
    sed -i 's|"/liims/|"/openspecimen/|g' "$jsfile"
    sed -i 's|/liims/rest/|/openspecimen/rest/|g' "$jsfile"
    sed -i 's|liims\.js|openspecimen.js|g' "$jsfile"
    sed -i "s|'liims'|'openspecimen'|g" "$jsfile"
    sed -i 's|"liims"|"openspecimen"|g' "$jsfile"
done

# 2. Clean up any remaining problematic files
echo "🧹 Removing any remaining problematic overrides..."
rm -f "$OPENSPECIMEN_DIR/ui-app/liims-complete.css" 2>/dev/null
rm -f "$OPENSPECIMEN_DIR/ui-app/post-login-override.css" 2>/dev/null

# 3. Ensure HTML files only have safe CSS
echo "📄 Cleaning HTML files..."
find "$OPENSPECIMEN_DIR" -name "*.html" -exec sed -i '/liims-complete.css/d; /post-login-override.css/d' {} \;

# 4. Add only the safe CSS to main files
echo "✅ Adding safe CSS branding..."
html_files=("/opt/tomcat9/webapps/openspecimen/ui-app/index.html" "/opt/tomcat9/webapps/openspecimen/index.html")

for html in "${html_files[@]}"; do
    if [ -f "$html" ] && ! grep -q "safe-liims-branding.css" "$html"; then
        sed -i 's|</head>|<link rel="stylesheet" href="/openspecimen/ui-app/safe-liims-branding.css">\n</head>|' "$html"
        echo "✅ Added safe CSS to: $html"
    fi
done

echo ""
echo "====================================="
echo "🎉 JAVASCRIPT FUNCTIONALITY RESTORED!"
echo "====================================="
echo ""
echo "✅ Removed problematic JavaScript overrides"
echo "✅ Kept safe CSS-only branding"
echo "✅ Restored critical API and URL references"
echo ""
echo "🔄 Now try:"
echo "   1. Clear browser cache"
echo "   2. Login to http://localhost:8082/openspecimen"
echo "   3. The application should work normally with LIIMS branding"
echo "====================================="