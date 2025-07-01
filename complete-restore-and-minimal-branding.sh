#!/bin/bash
#
# Complete Restore and Apply Minimal Safe Branding
#

echo "🔄 COMPLETE RESTORE AND MINIMAL BRANDING"
echo "========================================"

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Completely remove the deployment and redeploy fresh
echo "🗑️ Removing corrupted deployment..."
rm -rf "$OPENSPECIMEN_DIR"

# 2. Wait for Tomcat to auto-redeploy from WAR
echo "⏳ Waiting for fresh auto-deployment..."
sleep 10

# 3. Check if redeployed
if [ ! -d "$OPENSPECIMEN_DIR" ]; then
    echo "⚠️ Auto-deployment not complete, waiting longer..."
    sleep 20
fi

# 4. Only apply the absolute minimal branding that won't break anything
echo "🎨 Applying MINIMAL safe branding..."

# Wait for deployment to complete
while [ ! -f "$OPENSPECIMEN_DIR/index.html" ]; do
    echo "⏳ Waiting for deployment to complete..."
    sleep 5
done

# 5. ONLY replace logo files (safest approach)
echo "🖼️ Replacing logo files only..."
if [ -f "/home/adb/openspecimen/images/longevity-india-logo-web.png" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/images/os_logo.a585165a.png" 2>/dev/null
    echo "✅ Logo file replaced"
fi

# 6. Update favicon only
echo "🌟 Updating favicon..."
if [ -f "/home/adb/openspecimen/images/longevity-india-favicon.ico" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-favicon.ico" "$OPENSPECIMEN_DIR/favicon.ico" 2>/dev/null
    sed -i 's|favicon.ico|longevity-india-favicon.ico|g' "$OPENSPECIMEN_DIR"/*.html 2>/dev/null
    echo "✅ Favicon updated"
fi

# 7. Update page titles only (safest text change)
echo "📄 Updating page titles only..."
sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title>|g' "$OPENSPECIMEN_DIR"/*.html 2>/dev/null
sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title>|g' "$OPENSPECIMEN_DIR"/ui-app/*.html 2>/dev/null

# 8. Create external CSS file that loads after everything else
echo "🎨 Creating external CSS file..."
cat > "$OPENSPECIMEN_DIR/minimal-branding.css" <<'EOF'
/* Minimal BHARAT Branding - Loaded Last */
.navbar { background-color: #4169E1 !important; }
.btn-primary { background-color: #4169E1 !important; }
a { color: #4169E1 !important; }
h1, h2, h3 { color: #4169E1 !important; }
EOF

# 9. Add CSS as external file only (no inline styles)
echo "🔗 Adding external CSS link..."
if [ -f "$OPENSPECIMEN_DIR/index.html" ]; then
    sed -i 's|</body>|<link rel="stylesheet" href="minimal-branding.css">\n</body>|' "$OPENSPECIMEN_DIR/index.html"
fi

if [ -f "$OPENSPECIMEN_DIR/ui-app/index.html" ]; then
    sed -i 's|</body>|<link rel="stylesheet" href="../minimal-branding.css">\n</body>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
fi

echo ""
echo "========================================"
echo "✅ MINIMAL SAFE BRANDING APPLIED!"
echo "========================================"
echo ""
echo "✅ Fresh OpenSpecimen deployment"
echo "✅ Logo file physically replaced"
echo "✅ Favicon updated"
echo "✅ Page titles updated"
echo "✅ Minimal CSS (external file only)"
echo ""
echo "🚫 What we DIDN'T do (to avoid JS errors):"
echo "   • No inline styles"
echo "   • No CSS content property"
echo "   • No DOM manipulation"
echo "   • No JavaScript modifications"
echo ""
echo "🔄 Test now:"
echo "   1. Clear browser cache"
echo "   2. Login to OpenSpecimen"
echo "   3. Should work without JS errors"
echo "   4. Should see logo and blue colors"
echo "========================================"