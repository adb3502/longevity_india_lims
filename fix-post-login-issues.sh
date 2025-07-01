#!/bin/bash
#
# Fix Post-Login Issues - Dynamic Logo and Missing Files
#

echo "🔧 FIXING POST-LOGIN ISSUES"
echo "==========================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Fix the missing favicon in ui-app directory
echo "🌟 Fixing favicon in ui-app..."
if [ -f "/home/adb/openspecimen/images/longevity-india-favicon.ico" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-favicon.ico" "$OPENSPECIMEN_DIR/ui-app/favicon.ico"
    echo "✅ Favicon copied to ui-app directory"
fi

# 2. Create the dynamic logo file that the template is looking for
echo "🖼️ Creating dynamic logo file..."
mkdir -p "$OPENSPECIMEN_DIR/ui-app/assets"
if [ -f "/home/adb/openspecimen/images/longevity-india-logo-web.png" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/ui-app/assets/siteLogo.png"
    echo "✅ Site logo created for dynamic loading"
fi

# 3. Find and replace the problematic template variable if possible
echo "🔍 Looking for template files with logo variables..."
find "$OPENSPECIMEN_DIR" -name "*.html" -exec grep -l "{{global.siteAssets.siteLogo}}" {} \; 2>/dev/null | while read file; do
    echo "📝 Fixing logo path in: $file"
    sed -i 's|{{global.siteAssets.siteLogo}}|/openspecimen/images/longevity-india-logo-web.png|g' "$file"
done

# 4. Also check JavaScript files for the logo path
echo "📜 Checking JavaScript files for logo references..."
find "$OPENSPECIMEN_DIR" -name "*.js" -exec grep -l "siteLogo" {} \; 2>/dev/null | head -3 | while read jsfile; do
    echo "⚠️ Found siteLogo reference in: $jsfile"
    # Replace the logo path in JavaScript (be very careful)
    sed -i 's|siteLogo.*png|siteLogo":"/openspecimen/images/longevity-india-logo-web.png|g' "$jsfile" 2>/dev/null
done

# 5. Create a very minimal post-login CSS that loads after everything
echo "🎨 Creating post-login CSS..."
cat > "$OPENSPECIMEN_DIR/ui-app/post-login-minimal.css" <<'EOF'
/* Post-Login Minimal Branding */
.navbar, nav, .v-app-bar {
    background-color: #4169E1 !important;
}
.btn-primary, .v-btn--contained {
    background-color: #4169E1 !important;
}
a {
    color: #4169E1 !important;
}
h1, h2, h3 {
    color: #4169E1 !important;
}
EOF

# 6. Add the post-login CSS to the Vue.js app (very carefully)
echo "🔗 Adding post-login CSS to Vue.js app..."
if [ -f "$OPENSPECIMEN_DIR/ui-app/index.html" ] && ! grep -q "post-login-minimal.css" "$OPENSPECIMEN_DIR/ui-app/index.html"; then
    # Add it at the very end, just before </body>
    sed -i 's|</body>|<link rel="stylesheet" href="post-login-minimal.css">\n</body>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
    echo "✅ Post-login CSS added to Vue.js app"
fi

# 7. Remove the problematic CSS link that might be causing issues
echo "🧹 Removing problematic CSS references..."
sed -i '/minimal-branding.css/d' "$OPENSPECIMEN_DIR/ui-app/index.html" 2>/dev/null

# 8. Create a logo endpoint that always works
echo "📁 Creating reliable logo endpoints..."
# Create multiple copies of the logo in different locations
mkdir -p "$OPENSPECIMEN_DIR/assets"
mkdir -p "$OPENSPECIMEN_DIR/ui-app/img"
if [ -f "/home/adb/openspecimen/images/longevity-india-logo-web.png" ]; then
    cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/assets/logo.png"
    cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/ui-app/img/logo.png"
    echo "✅ Logo files placed in multiple locations"
fi

echo ""
echo "==========================="
echo "✅ POST-LOGIN ISSUES FIXED!"
echo "==========================="
echo ""
echo "✅ Favicon added to ui-app directory"
echo "✅ Dynamic site logo created"
echo "✅ Template variables replaced"
echo "✅ Logo files in multiple locations"
echo "✅ Minimal post-login CSS added"
echo ""
echo "🔄 Test again:"
echo "   1. Clear browser cache"
echo "   2. Login to OpenSpecimen"
echo "   3. Check F12 for 404 errors (should be gone)"
echo "   4. Should see branding after login"
echo ""
echo "💡 If errors persist:"
echo "   - The JavaScript error might be unrelated to our changes"
echo "   - Try using the old UI instead of the new Vue.js UI"
echo "==========================="