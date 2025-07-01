#!/bin/bash
#
# Apply BHARAT Branding to Post-Login Vue.js UI
#

echo "🚀 APPLYING POST-LOGIN BRANDING"
echo "==============================="

OPENSPECIMEN_DIR="/opt/tomcat9/webapps/openspecimen"

# 1. Add branding to the main Vue.js app CSS
echo "🎨 Adding branding to Vue.js CSS files..."

# Target the main app CSS file
if [ -f "$OPENSPECIMEN_DIR/ui-app/css/app.ab7d7dc6.css" ]; then
    echo "
/* BHARAT STUDY POST-LOGIN BRANDING */
/* Logo replacement for Vue.js app */
img[src*='logo'], img[src*='os_'], .navbar-brand img, nav img {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
    height: 40px !important;
    width: auto !important;
    max-width: 200px !important;
}

/* Header and navigation */
.v-app-bar, .v-toolbar, .navbar, nav, .app-header, header,
.v-navigation-drawer, .sidebar, .nav-drawer {
    background: linear-gradient(135deg, #4169E1 0%, #20B2AA 100%) !important;
    background-color: #4169E1 !important;
}

/* Vue.js specific button styling */
.v-btn--contained.v-btn--has-bg, .v-btn.v-btn--contained,
.btn-primary, .primary, button.primary {
    background-color: #4169E1 !important;
    border-color: #4169E1 !important;
    color: white !important;
}

.v-btn--contained:hover, .btn-primary:hover {
    background-color: #20B2AA !important;
    border-color: #20B2AA !important;
}

/* Vue.js links and text */
.v-btn--text, .v-btn--plain, a {
    color: #4169E1 !important;
}

.v-btn--text:hover, a:hover {
    color: #20B2AA !important;
}

/* Headers and titles */
.v-toolbar-title, .v-card-title, h1, h2, h3, h4, h5, h6,
.headline, .title, .subtitle-1, .subtitle-2 {
    color: #4169E1 !important;
}

/* Active states */
.v-btn--active, .v-list-item--active, .active, .selected {
    background-color: #4169E1 !important;
    color: white !important;
}

/* Navigation menu items */
.v-list-item:hover, .v-navigation-drawer .v-list-item:hover {
    background-color: rgba(65, 105, 225, 0.1) !important;
}

.v-navigation-drawer .v-list-item--active {
    background-color: #4169E1 !important;
    color: white !important;
}

/* Form controls */
.v-input--is-focused .v-input__control, .v-text-field--focused .v-input__control {
    color: #4169E1 !important;
}

.v-input--is-focused .v-text-field__details, .v-text-field--focused .v-label {
    color: #4169E1 !important;
}

/* Override any Vuetify primary colors */
.primary, .v-btn.primary {
    background-color: #4169E1 !important;
    border-color: #4169E1 !important;
}

/* Menu and dropdown styling */
.v-menu__content, .v-select__content, .v-autocomplete__content {
    border: 1px solid #4169E1 !important;
}

/* Data tables */
.v-data-table .v-data-table-header {
    background-color: #f8f9fa !important;
}

.v-data-table tr:hover {
    background-color: rgba(65, 105, 225, 0.05) !important;
}
" >> "$OPENSPECIMEN_DIR/ui-app/css/app.ab7d7dc6.css"
    echo "✅ Added branding to main Vue.js CSS"
fi

# 2. Add branding to chunk-vendors CSS (contains Vuetify styles)
if [ -f "$OPENSPECIMEN_DIR/ui-app/css/chunk-vendors.cb7df6a1.css" ]; then
    echo "
/* BHARAT VUETIFY OVERRIDES */
.v-application .primary {
    background-color: #4169E1 !important;
    border-color: #4169E1 !important;
}
.v-application .primary--text {
    color: #4169E1 !important;
}
.v-application .secondary {
    background-color: #20B2AA !important;
    border-color: #20B2AA !important;
}
.v-theme--light.v-btn--variant-contained {
    background-color: #4169E1 !important;
}
" >> "$OPENSPECIMEN_DIR/ui-app/css/chunk-vendors.cb7df6a1.css"
    echo "✅ Added branding to Vuetify CSS"
fi

# 3. Create a specific post-login CSS file
echo "📄 Creating post-login specific CSS..."
cat > "$OPENSPECIMEN_DIR/ui-app/css/bharat-post-login.css" <<'EOF'
/* BHARAT Study Post-Login Branding */

/* Force logo replacement in Vue.js app */
img[src*="os_logo"], 
img[src*="logo"],
.v-img img,
.navbar-brand img,
.brand img {
    content: url('/openspecimen/images/longevity-india-logo-web.png') !important;
    height: 40px !important;
    width: auto !important;
    max-width: 200px !important;
}

/* Vue.js App Bar and Navigation */
.v-app-bar,
.v-system-bar,
.v-toolbar {
    background: linear-gradient(135deg, #4169E1 0%, #20B2AA 100%) !important;
    color: white !important;
}

/* Side Navigation */
.v-navigation-drawer {
    border-right: 1px solid #e0e0e0 !important;
}

.v-navigation-drawer .v-list-item {
    border-radius: 8px !important;
    margin: 2px 8px !important;
}

.v-navigation-drawer .v-list-item:hover {
    background-color: rgba(65, 105, 225, 0.1) !important;
}

.v-navigation-drawer .v-list-item--active {
    background-color: #4169E1 !important;
    color: white !important;
}

/* Buttons */
.v-btn.v-btn--contained:not(.v-btn--disabled) {
    background-color: #4169E1 !important;
    color: white !important;
}

.v-btn.v-btn--contained:hover {
    background-color: #20B2AA !important;
}

/* Links and text buttons */
.v-btn--text {
    color: #4169E1 !important;
}

/* Form inputs */
.v-input--is-focused .v-field__outline {
    color: #4169E1 !important;
    border-color: #4169E1 !important;
}

.v-input--is-focused .v-label {
    color: #4169E1 !important;
}

/* Headers */
.v-card-title,
.v-toolbar-title,
h1, h2, h3, h4, h5, h6 {
    color: #4169E1 !important;
}

/* Data tables */
.v-table .v-table__wrapper table thead tr th {
    background-color: #f5f5f5 !important;
    color: #4169E1 !important;
    font-weight: 600 !important;
}

/* Tabs */
.v-tabs .v-tab--selected {
    color: #4169E1 !important;
}

.v-tabs .v-tabs-slider {
    background-color: #4169E1 !important;
}

/* Chips and badges */
.v-chip {
    background-color: #f0f7ff !important;
    color: #4169E1 !important;
}

.v-chip--variant-contained {
    background-color: #4169E1 !important;
    color: white !important;
}
EOF

# 4. Add the CSS file to the Vue.js app
echo "🔗 Linking post-login CSS to Vue.js app..."
if ! grep -q "bharat-post-login.css" "$OPENSPECIMEN_DIR/ui-app/index.html"; then
    sed -i 's|</head>|<link rel="stylesheet" href="css/bharat-post-login.css">\n</head>|' "$OPENSPECIMEN_DIR/ui-app/index.html"
    echo "✅ Linked post-login CSS to Vue.js app"
fi

# 5. Also replace any Vue.js specific logo files
echo "🖼️ Replacing Vue.js logo assets..."
find "$OPENSPECIMEN_DIR/ui-app" -name "*.png" -o -name "*.svg" | grep -i logo | while read logofile; do
    if [[ ! "$logofile" == *"longevity"* ]]; then
        echo "Replacing Vue.js logo: $logofile"
        cp "/home/adb/openspecimen/images/longevity-india-logo-web.png" "$logofile" 2>/dev/null
    fi
done

echo ""
echo "==============================="
echo "🎉 POST-LOGIN BRANDING APPLIED!"
echo "==============================="
echo ""
echo "✅ Vue.js CSS files updated"
echo "✅ Vuetify theme overridden"
echo "✅ Post-login specific CSS created"
echo "✅ Logo assets replaced"
echo ""
echo "🔄 To see post-login changes:"
echo "   1. Clear browser cache completely"
echo "   2. Login to OpenSpecimen"
echo "   3. You should now see branding after login"
echo ""
echo "💡 If still not working:"
echo "   1. Use browser dev tools (F12)"
echo "   2. Check if CSS files are loading"
echo "   3. Look for any JavaScript errors"
echo "==============================="