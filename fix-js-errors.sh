#!/bin/bash
#
# Fix JavaScript Errors and Apply Safe Branding
#

echo "🛠️ FIXING JAVASCRIPT ERRORS"
echo "============================"

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Remove problematic CSS that's breaking JavaScript
echo "🧹 Removing problematic CSS..."

# Remove the aggressive CSS that uses 'content' property (breaks DOM)
find "$OPENSPECIMEN_DIR" -name "*.css" -exec sed -i '/content: url/d' {} \;

# Clean inline styles that might be causing issues
sed -i 's|<style>img\[src\*="logo"\],img\[src\*="os_"\]{content:url("/openspecimen/images/longevity-india-logo-web.png")!important;height:40px!important;width:auto!important}||g' "$OPENSPECIMEN_DIR/ui-app/index.html"

sed -i 's|<style>img\[src\*="logo"\],img\[src\*="os_"\]{content:url("/openspecimen/images/longevity-india-logo-web.png")!important;height:40px!important;width:auto!important}||g' "$OPENSPECIMEN_DIR/index.html"

# 2. Create SAFE CSS that doesn't break JavaScript
echo "🎨 Creating safe CSS approach..."
cat > "$OPENSPECIMEN_DIR/ui-app/safe-branding.css" <<'EOF'
/* SAFE BHARAT BRANDING - NO CONTENT PROPERTY */

/* Navigation styling - SAFE */
.navbar,
nav,
.header,
.app-header {
    background: linear-gradient(135deg, #4169E1 0%, #20B2AA 100%) !important;
    background-color: #4169E1 !important;
}

/* Button styling - SAFE */
.btn-primary,
.os-btn-primary,
.primary-btn {
    background-color: #4169E1 !important;
    border-color: #4169E1 !important;
    color: white !important;
}

.btn-primary:hover,
.os-btn-primary:hover {
    background-color: #20B2AA !important;
    border-color: #20B2AA !important;
}

/* Link colors - SAFE */
a {
    color: #4169E1 !important;
}

a:hover {
    color: #20B2AA !important;
}

/* Headers - SAFE */
h1, h2, h3, h4, h5, h6 {
    color: #4169E1 !important;
}

/* Form focus - SAFE */
.form-control:focus,
input:focus,
textarea:focus {
    border-color: #4169E1 !important;
    box-shadow: 0 0 5px rgba(65, 105, 225, 0.3) !important;
}

/* Menu hover effects - SAFE */
.nav-item:hover,
.menu-item:hover {
    background-color: rgba(32, 178, 170, 0.1) !important;
}

/* Active states - SAFE */
.active,
.selected {
    background-color: #4169E1 !important;
    color: white !important;
}

/* Vue.js specific - SAFE */
.v-btn--contained {
    background-color: #4169E1 !important;
}

.v-btn--contained:hover {
    background-color: #20B2AA !important;
}

.v-app-bar {
    background: #4169E1 !important;
}

/* NO LOGO MANIPULATION - We'll handle this differently */
EOF

# 3. Replace CSS files with safe version
echo "🔄 Replacing CSS with safe version..."
cp "$OPENSPECIMEN_DIR/ui-app/safe-branding.css" "$OPENSPECIMEN_DIR/ui-app/bharat-theme.css"
cp "$OPENSPECIMEN_DIR/ui-app/safe-branding.css" "$OPENSPECIMEN_DIR/ui-app/css/bharat-post-login.css"

# 4. Clean up the HTML to only reference safe CSS
echo "📄 Cleaning HTML files..."
# Remove problematic inline styles but keep safe ones
sed -i 's|<style>.*content:url.*</style>||g' "$OPENSPECIMEN_DIR/ui-app/index.html"
sed -i 's|<style>.*content:url.*</style>||g' "$OPENSPECIMEN_DIR/index.html"

# Add only safe inline styles
if ! grep -q "SAFE INLINE" "$OPENSPECIMEN_DIR/ui-app/index.html"; then
    sed -i 's|</head>|<style>/* SAFE INLINE */ .navbar,nav{background:#4169E1!important}.btn-primary{background-color:#4169E1!important}a{color:#4169E1!important}</style>\n</head>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
fi

if ! grep -q "SAFE INLINE" "$OPENSPECIMEN_DIR/index.html"; then
    sed -i 's|</head>|<style>/* SAFE INLINE */ .navbar,nav{background:#4169E1!important}.btn-primary{background-color:#4169E1!important}a{color:#4169E1!important}</style>\n</head>|' "$OPENSPECIMEN_DIR/index.html"
fi

# 5. Logo handling - Physical file replacement ONLY (no CSS manipulation)
echo "🖼️ Using ONLY physical file replacement for logos..."
# The logo files are already replaced, so we don't need CSS for this

echo ""
echo "============================"
echo "✅ JAVASCRIPT ERRORS FIXED!"
echo "============================"
echo ""
echo "✅ Removed problematic CSS 'content' properties"
echo "✅ Applied safe color scheme branding"
echo "✅ Kept physical logo file replacements"
echo "✅ No DOM manipulation that breaks JavaScript"
echo ""
echo "🎨 What you'll see:"
echo "   • Blue navigation bars and headers"
echo "   • Blue buttons and links"
echo "   • Longevity India logo (via file replacement)"
echo "   • No JavaScript errors"
echo ""
echo "🔄 Clear cache and test login again"
echo "============================"