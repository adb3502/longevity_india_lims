#!/bin/bash
#
# Apply Longevity India Branding to OpenSpecimen
# This script integrates the custom UI changes into the deployed application
#

echo "🎨 APPLYING LONGEVITY INDIA BRANDING TO OPENSPECIMEN"
echo "===================================================="

# Define paths
OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"
SOURCE_DIR="/home/adb/openspecimen"

# Check if OpenSpecimen is deployed
if [ ! -d "$OPENSPECIMEN_DIR" ]; then
    echo "❌ Error: OpenSpecimen not found at $OPENSPECIMEN_DIR"
    exit 1
fi

# 1. Copy logo images
echo "🖼️ Copying logo images..."
if [ -d "$SOURCE_DIR/images" ]; then
    cp -f "$SOURCE_DIR/images/longevity-india-logo.png" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    cp -f "$SOURCE_DIR/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    cp -f "$SOURCE_DIR/images/longevity-india-icon.png" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    cp -f "$SOURCE_DIR/images/longevity-india-favicon.ico" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    echo "✅ Logo images copied"
fi

# 2. Apply custom CSS by appending to main app CSS
echo "🎨 Applying custom CSS theme..."
if [ -f "$SOURCE_DIR/longevity-india-theme.css" ]; then
    # Append custom CSS to the main app CSS file
    echo "" >> "$OPENSPECIMEN_DIR/ui-app/css/app.ab7d7dc6.css"
    echo "/* Longevity India Custom Theme */" >> "$OPENSPECIMEN_DIR/ui-app/css/app.ab7d7dc6.css"
    cat "$SOURCE_DIR/longevity-india-theme.css" >> "$OPENSPECIMEN_DIR/ui-app/css/app.ab7d7dc6.css"
    echo "✅ Custom CSS theme applied"
fi

# 3. Update index.html to include branding
echo "📄 Updating index.html..."
if [ -f "$OPENSPECIMEN_DIR/index.html" ]; then
    # Backup original
    cp "$OPENSPECIMEN_DIR/index.html" "$OPENSPECIMEN_DIR/index.html.backup"
    
    # Add custom branding to index.html
    sed -i 's|<title>.*</title>|<title>BHARAT Study - Longevity India OpenSpecimen</title>|' "$OPENSPECIMEN_DIR/index.html"
    sed -i 's|<link rel="icon".*>|<link rel="icon" href="/openspecimen/images/longevity-india-favicon.ico">|' "$OPENSPECIMEN_DIR/index.html"
    echo "✅ Index.html updated"
fi

# 4. Update UI app index.html
echo "📄 Updating UI app index.html..."
if [ -f "$OPENSPECIMEN_DIR/ui-app/index.html" ]; then
    # Backup original
    cp "$OPENSPECIMEN_DIR/ui-app/index.html" "$OPENSPECIMEN_DIR/ui-app/index.html.backup"
    
    # Add custom branding
    sed -i 's|<title>.*</title>|<title>BHARAT Study - Longevity India</title>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
    sed -i 's|favicon.ico|/openspecimen/images/longevity-india-favicon.ico|' "$OPENSPECIMEN_DIR/ui-app/index.html"
    
    # Add custom CSS link
    sed -i 's|</head>|<style>:root{--os-primary-color:#4169E1 !important;--os-secondary-color:#20B2AA !important;--os-accent-color:#00CED1 !important;}.os-navbar{background-color:#4169E1 !important;}.os-nav-item:hover{background-color:#20B2AA !important;}</style></head>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
    echo "✅ UI app index.html updated"
fi

# 5. Create a custom CSS override file
echo "🎨 Creating CSS override file..."
cat > "$OPENSPECIMEN_DIR/ui-app/css/longevity-override.css" <<EOF
/* Longevity India Branding Override */
:root {
    --os-primary-color: #4169E1 !important;
    --os-secondary-color: #20B2AA !important;
    --os-accent-color: #00CED1 !important;
    --os-text-color: #212121 !important;
    --os-background: #FAFAFA !important;
}

/* Navigation Bar */
.os-navbar,
.navbar {
    background-color: #4169E1 !important;
}

/* Buttons */
.btn-primary,
.os-btn-primary {
    background-color: #4169E1 !important;
    border-color: #4169E1 !important;
}

.btn-primary:hover,
.os-btn-primary:hover {
    background-color: #20B2AA !important;
    border-color: #20B2AA !important;
}

/* Links */
a {
    color: #4169E1 !important;
}

a:hover {
    color: #20B2AA !important;
}

/* Headers */
h1, h2, h3, h4, h5, h6,
.os-section-hdr {
    color: #4169E1 !important;
}

/* Logo in header */
.os-navbar-brand img {
    display: none;
}

.os-navbar-brand::before {
    content: url('/openspecimen/images/longevity-india-logo-web.png');
    display: inline-block;
    height: 40px;
}
EOF
echo "✅ CSS override file created"

# 6. Copy dashboard files
echo "📊 Copying dashboard files..."
mkdir -p "$OPENSPECIMEN_DIR/dashboards"
cp -f "$SOURCE_DIR"/bharat-*-dashboard.html "$OPENSPECIMEN_DIR/dashboards/" 2>/dev/null
cp -f "$SOURCE_DIR"/bharat-dashboard-*.js "$OPENSPECIMEN_DIR/dashboards/" 2>/dev/null
echo "✅ Dashboard files copied"

# 7. Update old UI CSS files
echo "🎨 Updating legacy UI styles..."
if [ -d "$OPENSPECIMEN_DIR/styles" ]; then
    # Add branding to main app.css
    echo "" >> "$OPENSPECIMEN_DIR/styles/app.css"
    echo "/* Longevity India Branding */" >> "$OPENSPECIMEN_DIR/styles/app.css"
    echo ".os-brand { background-color: #4169E1; }" >> "$OPENSPECIMEN_DIR/styles/app.css"
    echo ".btn-primary { background-color: #4169E1; border-color: #4169E1; }" >> "$OPENSPECIMEN_DIR/styles/app.css"
    echo ".btn-primary:hover { background-color: #20B2AA; border-color: #20B2AA; }" >> "$OPENSPECIMEN_DIR/styles/app.css"
    echo "✅ Legacy UI styles updated"
fi

echo ""
echo "===================================================="
echo "🎉 LONGEVITY INDIA BRANDING APPLIED!"
echo "===================================================="
echo ""
echo "✅ Logo images installed"
echo "✅ Custom CSS theme applied"
echo "✅ Index files updated"
echo "✅ Dashboard files deployed"
echo ""
echo "🔄 IMPORTANT: Restart Tomcat to see all changes:"
echo "   sudo systemctl restart tomcat9"
echo ""
echo "📍 Access Points:"
echo "   Main App: http://localhost:8082/openspecimen"
echo "   Dashboards: http://localhost:8082/openspecimen/dashboards/"
echo ""
echo "⚠️ Note: Clear browser cache to see all UI changes"
echo "===================================================="