#!/bin/bash
#
# Replace ALL OpenSpecimen logos with Longevity India branding
#

echo "🔄 REPLACING ALL OPENSPECIMEN LOGOS"
echo "===================================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"
SOURCE_DIR="/home/adb/openspecimen"

# 1. Find and replace all OpenSpecimen logo files
echo "🔍 Finding all logo files..."
logo_files=$(find "$OPENSPECIMEN_DIR" -name "*logo*.png" -o -name "*logo*.jpg" -o -name "os_*.png" 2>/dev/null)

for logo in $logo_files; do
    if [[ "$logo" == *"longevity"* ]]; then
        continue  # Skip our own logos
    fi
    
    echo "📝 Replacing: $logo"
    
    # Determine which replacement to use based on size/name
    if [[ "$logo" == *"email"* ]] || [[ "$logo" == *"small"* ]]; then
        # Use icon for small/email logos
        cp -f "$SOURCE_DIR/images/longevity-india-icon.png" "$logo"
    else
        # Use web logo for main logos
        cp -f "$SOURCE_DIR/images/longevity-india-logo-web.png" "$logo"
    fi
done

# 2. Replace the specific OpenSpecimen logo file
echo "🎯 Targeting specific logo files..."
if [ -f "$OPENSPECIMEN_DIR/images/os_logo.a585165a.png" ]; then
    cp -f "$SOURCE_DIR/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/images/os_logo.a585165a.png"
    echo "✅ Replaced os_logo.a585165a.png"
fi

# 3. Find and update logo references in JavaScript files
echo "📜 Updating JavaScript references..."
js_files=$(find "$OPENSPECIMEN_DIR/ui-app" -name "*.js" 2>/dev/null)

for js in $js_files; do
    # Replace logo references
    sed -i 's|os_logo\.[a-f0-9]*\.png|longevity-india-logo-web.png|g' "$js" 2>/dev/null
    sed -i 's|/images/os_logo\.png|/images/longevity-india-logo-web.png|g' "$js" 2>/dev/null
done

# 4. Create CSS injection to force logo replacement
echo "💉 Creating CSS injection..."
cat > "$OPENSPECIMEN_DIR/ui-app/longevity-inject.css" <<'EOF'
/* Force Longevity India Logo */
img[src*="os_logo"] {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
}

.os-logo img,
.navbar-brand img,
img[alt="OpenSpecimen"] {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
    height: 40px !important;
    width: auto !important;
}

/* Navigation bar styling */
.navbar,
.os-navbar,
nav[role="navigation"] {
    background-color: #4169E1 !important;
}

.navbar-brand {
    padding: 5px 15px !important;
}

/* Override any inline styles */
[style*="background-color"] {
    background-color: #4169E1 !important;
}

/* Button overrides */
.btn-primary,
button.primary {
    background-color: #4169E1 !important;
    border-color: #4169E1 !important;
}

.btn-primary:hover {
    background-color: #20B2AA !important;
    border-color: #20B2AA !important;
}
EOF

# 5. Inject CSS into all HTML files
echo "📄 Injecting CSS into HTML files..."
html_files=$(find "$OPENSPECIMEN_DIR" -name "index.html" 2>/dev/null)

for html in $html_files; do
    if ! grep -q "longevity-inject.css" "$html"; then
        sed -i 's|</head>|<link rel="stylesheet" href="/openspecimen/ui-app/longevity-inject.css">\n</head>|' "$html"
        echo "✅ Injected CSS into: $html"
    fi
done

# 6. Replace favicon in all locations
echo "🌟 Replacing favicons..."
find "$OPENSPECIMEN_DIR" -name "favicon.ico" -exec cp -f "$SOURCE_DIR/images/longevity-india-favicon.ico" {} \;

# 7. Create a JavaScript override
echo "📝 Creating JavaScript override..."
cat > "$OPENSPECIMEN_DIR/ui-app/longevity-override.js" <<'EOF'
// Longevity India Branding Override
document.addEventListener('DOMContentLoaded', function() {
    // Replace all logo images
    var logos = document.querySelectorAll('img[src*="logo"], img[src*="os_"]');
    logos.forEach(function(img) {
        if (!img.src.includes('longevity')) {
            img.src = '/openspecimen/images/longevity-india-logo-web.png';
            img.style.height = '40px';
            img.style.width = 'auto';
        }
    });
    
    // Update page title
    document.title = 'BHARAT Study - Longevity India';
    
    // Force navbar color
    var navbars = document.querySelectorAll('.navbar, nav');
    navbars.forEach(function(nav) {
        nav.style.backgroundColor = '#4169E1';
    });
});
EOF

# Inject JS into HTML files
for html in $html_files; do
    if ! grep -q "longevity-override.js" "$html"; then
        sed -i 's|</body>|<script src="/openspecimen/ui-app/longevity-override.js"></script>\n</body>|' "$html"
        echo "✅ Injected JS into: $html"
    fi
done

echo ""
echo "===================================="
echo "🎉 LOGO REPLACEMENT COMPLETE!"
echo "===================================="
echo ""
echo "✅ All logo files replaced"
echo "✅ CSS overrides created"
echo "✅ JavaScript overrides created"
echo "✅ HTML files updated"
echo ""
echo "🔄 IMPORTANT: Clear browser cache completely:"
echo "   1. Press Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)"
echo "   2. Select 'Cached images and files'"
echo "   3. Clear browsing data"
echo "   4. Refresh the page"
echo ""
echo "💡 If logo still appears:"
echo "   1. Try incognito/private browsing mode"
echo "   2. Restart Tomcat: sudo systemctl restart tomcat9"
echo "===================================="