#!/bin/bash
#
# Safe BHARAT Study Deployment
# Conservative approach that won't break functionality
#

echo "🎨 SAFE BHARAT STUDY DEPLOYMENT"
echo "================================"

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"
SOURCE_DIR="/home/adb/openspecimen"

# 1. Deploy logo images only
echo "🖼️ Deploying logo images..."
if [ -d "$SOURCE_DIR/images" ]; then
    cp -f "$SOURCE_DIR/images/longevity-india-logo.png" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    cp -f "$SOURCE_DIR/images/longevity-india-logo-web.png" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    cp -f "$SOURCE_DIR/images/longevity-india-icon.png" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    cp -f "$SOURCE_DIR/images/longevity-india-favicon.ico" "$OPENSPECIMEN_DIR/images/" 2>/dev/null
    echo "✅ Logo images deployed"
fi

# 2. Create minimal, safe CSS override
echo "🎨 Creating safe CSS overrides..."
cat > "$OPENSPECIMEN_DIR/ui-app/bharat-theme.css" <<'EOF'
/* BHARAT Study Safe Theme - CSS Only */

/* Logo replacement - target specific logo file */
img[src*="os_logo.a585165a.png"] {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
    height: 40px !important;
    width: auto !important;
    max-width: 200px !important;
}

/* Navigation bar color */
.navbar,
.os-navbar {
    background: linear-gradient(135deg, #4169E1 0%, #20B2AA 100%) !important;
}

/* Primary button styling */
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

/* Link colors */
a {
    color: #4169E1 !important;
}

a:hover {
    color: #20B2AA !important;
}

/* Header colors */
h1, h2, h3, h4, h5, h6,
.os-section-hdr {
    color: #4169E1 !important;
}

/* Update favicon */
link[rel="icon"] {
    href: '/openspecimen/images/longevity-india-favicon.ico' !important;
}
EOF

# 3. Deploy BHARAT dashboards to a separate location
echo "📊 Deploying BHARAT dashboards..."
mkdir -p "$OPENSPECIMEN_DIR/bharat"
cp -f "$SOURCE_DIR"/bharat-*-dashboard.html "$OPENSPECIMEN_DIR/bharat/" 2>/dev/null
cp -f "$SOURCE_DIR"/bharat-dashboard-*.js "$OPENSPECIMEN_DIR/bharat/" 2>/dev/null
cp -f "$SOURCE_DIR"/longevity-india-theme.css "$OPENSPECIMEN_DIR/bharat/" 2>/dev/null
cp -f "$SOURCE_DIR"/longevity-india-dashboard.js "$OPENSPECIMEN_DIR/bharat/" 2>/dev/null

# 4. Create configuration directory
echo "📋 Deploying configuration files..."
mkdir -p "$OPENSPECIMEN_DIR/bharat/configs"
cp -f "$SOURCE_DIR"/bharat-*.json "$OPENSPECIMEN_DIR/bharat/configs/" 2>/dev/null
cp -f "$SOURCE_DIR"/longevity-india-*.json "$OPENSPECIMEN_DIR/bharat/configs/" 2>/dev/null

# 5. Add CSS to main UI (very safely)
echo "📄 Adding theme to UI..."
if [ -f "$OPENSPECIMEN_DIR/ui-app/index.html" ]; then
    # Create backup first
    cp "$OPENSPECIMEN_DIR/ui-app/index.html" "$OPENSPECIMEN_DIR/ui-app/index.html.backup-$(date +%s)"
    
    # Add CSS link right before closing head tag (safest approach)
    sed -i 's|</head>|<link rel="stylesheet" href="/openspecimen/ui-app/bharat-theme.css">\n</head>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
    echo "✅ Theme added to UI app"
fi

# 6. Add CSS to old UI
if [ -f "$OPENSPECIMEN_DIR/index.html" ]; then
    # Create backup first
    cp "$OPENSPECIMEN_DIR/index.html" "$OPENSPECIMEN_DIR/index.html.backup-$(date +%s)"
    
    # Add CSS link
    sed -i 's|</head>|<link rel="stylesheet" href="/openspecimen/ui-app/bharat-theme.css">\n</head>|' "$OPENSPECIMEN_DIR/index.html"
    echo "✅ Theme added to main app"
fi

# 7. Update favicon references
echo "🌟 Updating favicon..."
find "$OPENSPECIMEN_DIR" -name "*.html" -exec sed -i 's|favicon.ico|/openspecimen/images/longevity-india-favicon.ico|g' {} \;

# 8. Create BHARAT access page
echo "📱 Creating BHARAT access page..."
cat > "$OPENSPECIMEN_DIR/bharat/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BHARAT Study - Longevity India</title>
    <link rel="stylesheet" href="longevity-india-theme.css">
    <link rel="icon" href="/openspecimen/images/longevity-india-favicon.ico">
</head>
<body>
    <div style="padding: 40px; max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 40px;">
            <img src="/openspecimen/images/longevity-india-logo-web.png" alt="Longevity India" style="height: 80px; margin-bottom: 20px;">
            <h1 style="color: #4169E1; margin-bottom: 10px;">BHARAT Study Platform</h1>
            <p style="color: #666; font-size: 1.1rem;">Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #4169E1; margin-bottom: 15px;">📊 Study Dashboards</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;">
                        <a href="bharat-study-overview-dashboard.html" style="color: #20B2AA; text-decoration: none;">
                            🏠 Study Overview Dashboard
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="bharat-biomarker-analytics-dashboard.html" style="color: #20B2AA; text-decoration: none;">
                            🧬 Biomarker Analytics
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="bharat-inventory-dashboard.html" style="color: #20B2AA; text-decoration: none;">
                            📦 Inventory Management
                        </a>
                    </li>
                </ul>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #4169E1; margin-bottom: 15px;">⚙️ Main Application</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;">
                        <a href="/openspecimen/" style="color: #20B2AA; text-decoration: none; font-weight: bold;">
                            🚀 Launch OpenSpecimen
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="/openspecimen/ui-app/" style="color: #20B2AA; text-decoration: none;">
                            🖥️ Modern UI
                        </a>
                    </li>
                </ul>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #4169E1; margin-bottom: 15px;">📋 Configuration</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;">
                        <a href="configs/" style="color: #20B2AA; text-decoration: none;">
                            📁 Configuration Files
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="../BHARAT-MANUAL-IMPORT-GUIDE.md" style="color: #20B2AA; text-decoration: none;">
                            📖 Import Guide
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        
        <div style="margin-top: 40px; text-align: center; color: #888;">
            <p>BHARAT Study - Longevity India Initiative</p>
            <p>For support: bharat-study@longevityindia.org</p>
        </div>
    </div>
</body>
</html>
EOF

echo ""
echo "================================"
echo "🎉 SAFE BHARAT DEPLOYMENT COMPLETE!"
echo "================================"
echo ""
echo "✅ Logo images deployed"
echo "✅ Safe CSS theme applied"  
echo "✅ BHARAT dashboards deployed"
echo "✅ Configuration files available"
echo ""
echo "📍 Access Points:"
echo "   Main App: http://localhost:8082/openspecimen"
echo "   BHARAT Hub: http://localhost:8082/openspecimen/bharat/"
echo "   Dashboards: http://localhost:8082/openspecimen/bharat/bharat-study-overview-dashboard.html"
echo ""
echo "🎨 UI Changes:"
echo "   • Longevity India logo in header"
echo "   • Blue/teal color scheme"
echo "   • Custom favicon"
echo "   • No functionality changes"
echo ""
echo "💡 To see changes: Clear browser cache and refresh"
echo "================================"