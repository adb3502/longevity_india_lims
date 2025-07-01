#!/bin/bash
#
# Complete LIIMS (Longevity India Information Management System) Branding
#

echo "🚀 COMPLETE LIIMS BRANDING TRANSFORMATION"
echo "=========================================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"
SOURCE_DIR="/home/adb/openspecimen"

# 1. Replace text in all JavaScript files
echo "📝 Replacing 'OpenSpecimen' with 'LIIMS' in JavaScript files..."
find "$OPENSPECIMEN_DIR" -name "*.js" -type f -exec sed -i 's/OpenSpecimen/LIIMS/g' {} \; 2>/dev/null
find "$OPENSPECIMEN_DIR" -name "*.js" -type f -exec sed -i 's/openspecimen/liims/g' {} \; 2>/dev/null

# 2. Replace text in HTML files
echo "📄 Updating HTML files..."
find "$OPENSPECIMEN_DIR" -name "*.html" -type f -exec sed -i 's/OpenSpecimen/LIIMS/g' {} \; 2>/dev/null
find "$OPENSPECIMEN_DIR" -name "*.html" -type f -exec sed -i 's/<title>.*<\/title>/<title>LIIMS - Longevity India Information Management System<\/title>/g' {} \; 2>/dev/null

# 3. Create comprehensive CSS override for post-login
echo "🎨 Creating comprehensive CSS override..."
cat > "$OPENSPECIMEN_DIR/ui-app/liims-complete.css" <<'EOF'
/* LIIMS Complete Branding Override */

/* Force logo replacement everywhere */
img[src*="logo"],
img[src*="os_"],
.os-logo img,
.navbar-brand img,
.brand img,
img[alt*="OpenSpecimen"],
img[alt*="openspecimen"],
.logo img {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
    height: 40px !important;
    width: auto !important;
    max-width: 200px !important;
}

/* Navigation styling */
.navbar,
.os-navbar,
nav[role="navigation"],
.nav-header,
.app-header,
.header {
    background-color: #4169E1 !important;
}

/* Override any background colors */
[style*="background-color: rgb(255, 255, 255)"],
[style*="background-color: #ffffff"],
[style*="background-color: white"] {
    background-color: #4169E1 !important;
}

/* Sidebar and menu styling */
.os-nav-menu,
.sidebar,
.side-menu {
    background-color: #f8f9fa !important;
}

.os-nav-item:hover,
.nav-item:hover,
.menu-item:hover {
    background-color: #20B2AA !important;
}

/* Button styling */
.btn-primary,
.os-btn-primary,
button.primary,
input[type="submit"] {
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
h1, h2, h3, h4, h5, h6 {
    color: #4169E1 !important;
}

/* Hide any OpenSpecimen text */
*:contains("OpenSpecimen") {
    visibility: hidden;
    position: relative;
}

*:contains("OpenSpecimen"):after {
    content: "LIIMS";
    visibility: visible;
    position: absolute;
    left: 0;
}
EOF

# 4. Create aggressive JavaScript override
echo "📜 Creating JavaScript override for post-login..."
cat > "$OPENSPECIMEN_DIR/ui-app/liims-override.js" <<'EOF'
// LIIMS Complete Branding Override
(function() {
    function replaceBranding() {
        // Replace all text occurrences
        document.body.innerHTML = document.body.innerHTML.replace(/OpenSpecimen/g, 'LIIMS');
        document.body.innerHTML = document.body.innerHTML.replace(/openspecimen/g, 'liims');
        
        // Force logo replacement
        var logos = document.querySelectorAll('img');
        logos.forEach(function(img) {
            if (img.src && (img.src.includes('logo') || img.src.includes('os_')) && !img.src.includes('longevity')) {
                img.src = '/openspecimen/images/longevity-india-logo-web.png';
                img.style.height = '40px';
                img.style.width = 'auto';
                img.style.maxWidth = '200px';
            }
        });
        
        // Update title
        document.title = 'LIIMS - Longevity India Information Management System';
        
        // Force navbar styling
        var navbars = document.querySelectorAll('.navbar, nav, .header, .app-header');
        navbars.forEach(function(nav) {
            nav.style.backgroundColor = '#4169E1';
        });
        
        // Replace text in specific elements
        var textElements = document.querySelectorAll('span, div, p, h1, h2, h3, h4, h5, h6, a, button');
        textElements.forEach(function(el) {
            if (el.textContent.includes('OpenSpecimen')) {
                el.textContent = el.textContent.replace(/OpenSpecimen/g, 'LIIMS');
            }
        });
    }
    
    // Run immediately
    replaceBranding();
    
    // Run after DOM changes
    var observer = new MutationObserver(function(mutations) {
        replaceBranding();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Run periodically to catch dynamic content
    setInterval(replaceBranding, 1000);
})();
EOF

# 5. Update all index.html files to include new resources
echo "📄 Updating all index.html files..."
html_files=$(find "$OPENSPECIMEN_DIR" -name "index.html" 2>/dev/null)

for html in $html_files; do
    # Remove old injections first
    sed -i '/longevity-inject.css/d' "$html" 2>/dev/null
    sed -i '/longevity-override.js/d' "$html" 2>/dev/null
    
    # Add new CSS
    if ! grep -q "liims-complete.css" "$html"; then
        sed -i 's|</head>|<link rel="stylesheet" href="/openspecimen/ui-app/liims-complete.css">\n</head>|' "$html"
    fi
    
    # Add new JS
    if ! grep -q "liims-override.js" "$html"; then
        sed -i 's|</body>|<script src="/openspecimen/ui-app/liims-override.js"></script>\n</body>|' "$html"
    fi
    
    echo "✅ Updated: $html"
done

# 6. Replace text in JSON language files
echo "🌐 Updating language files..."
find "$OPENSPECIMEN_DIR" -name "*.json" -path "*/i18n/*" -type f -exec sed -i 's/OpenSpecimen/LIIMS/g' {} \; 2>/dev/null

# 7. Create a post-login specific override
echo "🔒 Creating post-login specific overrides..."
cat > "$OPENSPECIMEN_DIR/ui-app/post-login-override.css" <<'EOF'
/* Post-login specific overrides */
.os-home-panel img,
.home-logo img,
img.brand-logo {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
    height: 40px !important;
}

/* Home page branding */
.os-welcome-msg:before {
    content: "Welcome to LIIMS - " !important;
}

/* Replace any remaining OpenSpecimen text */
.os-brand-name {
    font-size: 0 !important;
}

.os-brand-name:after {
    content: "LIIMS" !important;
    font-size: 1.2rem !important;
    color: #4169E1 !important;
}
EOF

# 8. Update Angular app configuration if present
echo "🔧 Updating Angular configuration..."
if [ -d "$OPENSPECIMEN_DIR/ui-app/modules" ]; then
    find "$OPENSPECIMEN_DIR/ui-app/modules" -name "*.js" -exec sed -i "s/'OpenSpecimen'/'LIIMS'/g" {} \; 2>/dev/null
    find "$OPENSPECIMEN_DIR/ui-app/modules" -name "*.js" -exec sed -i 's/"OpenSpecimen"/"LIIMS"/g' {} \; 2>/dev/null
fi

# 9. Create a service worker for persistent branding
echo "⚙️ Creating service worker..."
cat > "$OPENSPECIMEN_DIR/liims-worker.js" <<'EOF'
// LIIMS Service Worker
self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request).then(function(response) {
            if (response.headers.get('content-type') && response.headers.get('content-type').includes('text/html')) {
                return response.text().then(function(text) {
                    var modifiedText = text.replace(/OpenSpecimen/g, 'LIIMS');
                    return new Response(modifiedText, {
                        status: response.status,
                        statusText: response.statusText,
                        headers: response.headers
                    });
                });
            }
            return response;
        })
    );
});
EOF

echo ""
echo "=========================================="
echo "🎉 LIIMS BRANDING COMPLETE!"
echo "=========================================="
echo ""
echo "✅ Replaced 'OpenSpecimen' with 'LIIMS' throughout"
echo "✅ Logo override for post-login pages"
echo "✅ Complete CSS and JS overrides"
echo "✅ Language files updated"
echo ""
echo "🔄 CRITICAL STEPS:"
echo "   1. Clear ALL browser data:"
echo "      - Press Ctrl+Shift+Delete"
echo "      - Select 'All time' for time range"
echo "      - Check all boxes (cookies, cache, etc.)"
echo "      - Clear data"
echo ""
echo "   2. Restart Tomcat:"
echo "      sudo systemctl restart tomcat9"
echo ""
echo "   3. Use a new incognito window to test"
echo ""
echo "📍 The system is now branded as:"
echo "   LIIMS - Longevity India Information Management System"
echo "=========================================="