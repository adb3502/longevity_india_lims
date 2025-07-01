#!/bin/bash
#
# Force BHARAT Branding - Multiple Approaches
#

echo "🚀 FORCING BHARAT BRANDING"
echo "=========================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Replace all logo files directly
echo "🖼️ Replacing logo files directly..."
find "$OPENSPECIMEN_DIR" -name "*logo*.png" -not -path "*/longevity*" | while read logofile; do
    echo "Replacing: $logofile"
    cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$logofile"
done

# 2. Add CSS with maximum priority to main app CSS
echo "🎨 Adding branding to main CSS files..."
echo "
/* BHARAT STUDY BRANDING - HIGHEST PRIORITY */
img[src*='logo'], img[src*='os_'] { 
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important; 
    height: 40px !important; 
    width: auto !important; 
}
.navbar, nav, .header { 
    background: #4169E1 !important; 
    background-image: linear-gradient(135deg, #4169E1 0%, #20B2AA 100%) !important; 
}
.btn-primary { 
    background-color: #4169E1 !important; 
    border-color: #4169E1 !important; 
}
.btn-primary:hover { 
    background-color: #20B2AA !important; 
}
a { color: #4169E1 !important; }
h1, h2, h3 { color: #4169E1 !important; }
" >> "$OPENSPECIMEN_DIR/ui-app/css/app.ab7d7dc6.css"

# 3. Add to legacy CSS too
echo "
/* BHARAT STUDY BRANDING */
.navbar { background-color: #4169E1 !important; }
.btn-primary { background-color: #4169E1 !important; }
a { color: #4169E1 !important; }
" >> "$OPENSPECIMEN_DIR/styles/app.52f4e9fc.css"

# 4. Create a forced inline style injection
echo "📄 Adding forced inline styles..."
sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title><style>img[src*="logo"],img[src*="os_"]{content:url("/openspecimen/images/longevity-india-logo-web.png")!important;height:40px!important;width:auto!important}.navbar,nav{background:#4169E1!important}.btn-primary{background-color:#4169E1!important}a{color:#4169E1!important}</style>|' "$OPENSPECIMEN_DIR/ui-app/index.html"

sed -i 's|<title>OpenSpecimen</title>|<title>BHARAT Study - Longevity India</title><style>img[src*="logo"],img[src*="os_"]{content:url("/openspecimen/images/longevity-india-logo-web.png")!important;height:40px!important;width:auto!important}.navbar,nav{background:#4169E1!important}.btn-primary{background-color:#4169E1!important}a{color:#4169E1!important}</style>|' "$OPENSPECIMEN_DIR/index.html"

echo ""
echo "=========================="
echo "🎉 FORCED BRANDING APPLIED!"
echo "=========================="
echo ""
echo "✅ Logo files physically replaced"
echo "✅ CSS injected into main stylesheets" 
echo "✅ Inline styles added to HTML"
echo "✅ Page titles updated"
echo ""
echo "🔄 Now:"
echo "   1. Clear browser cache completely"
echo "   2. Hard refresh (Ctrl+F5)"
echo "   3. Try incognito mode"
echo "   4. You SHOULD see the changes now"
echo "=========================="