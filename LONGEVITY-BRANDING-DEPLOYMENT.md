
# Longevity India Branding Deployment Instructions
# Generated on 2025-06-24 19:10:37

## Files to Deploy to OpenSpecimen Server

### 1. Logo Assets (copy to OpenSpecimen images directory)
- longevity-india-logo.png (main horizontal logo)
- longevity-india-icon.png (icon version)
- longevity-india-favicon.ico (browser favicon)

### 2. CSS and JavaScript (copy to OpenSpecimen web directory)
- longevity-india-theme.css
- longevity-india-dashboard.js
- longevity-india-login.html

### 3. Server Deployment Commands

```bash
# Create images directory
mkdir -p /path/to/openspecimen/tomcat/webapps/openspecimen/images/

# Copy logo assets
cp images/longevity-india-logo.png /path/to/openspecimen/tomcat/webapps/openspecimen/images/
cp images/longevity-india-icon.png /path/to/openspecimen/tomcat/webapps/openspecimen/images/
cp images/longevity-india-favicon.ico /path/to/openspecimen/tomcat/webapps/openspecimen/images/

# Copy CSS and JS files
cp longevity-india-theme.css /path/to/openspecimen/tomcat/webapps/openspecimen/
cp longevity-india-dashboard.js /path/to/openspecimen/tomcat/webapps/openspecimen/
cp longevity-india-login.html /path/to/openspecimen/tomcat/webapps/openspecimen/

# Update OpenSpecimen configuration
# Add to openspecimen.properties:
app.title=BHARAT Study Portal - Longevity India
institute.name=Longevity India
custom.css.url=/longevity-india-theme.css
custom.js.url=/longevity-india-dashboard.js
logo.url=/images/longevity-india-logo.png
favicon.url=/images/longevity-india-favicon.ico

# Restart OpenSpecimen
sudo systemctl restart openspecimen
```

### 4. Verification Steps

1. Check login page shows Longevity India logo
2. Verify header uses blue color scheme (#4169E1)
3. Confirm dashboard hero section displays correctly
4. Test responsive design on mobile devices
5. Validate favicon appears in browser tabs

### 5. File Deployment Log
- Created directory: /home/adb/openspecimen/images\n- Deployed: LII_branding/Longevity Horizontal Logo main.png -> /home/adb/openspecimen/images/longevity-india-logo.png\n- Created web-optimized version: /home/adb/openspecimen/images/longevity-india-logo-web.png\n- Converted JPG to PNG: LII_branding/Longevity Logo Icon.jpg -> /home/adb/openspecimen/images/longevity-india-icon.png\n- Created favicon: /home/adb/openspecimen/images/longevity-india-favicon.ico\n

### 6. Color Scheme Applied
- Primary Blue: #4169E1 (Royal Blue)
- Secondary Teal: #20B2AA (Light Sea Green) 
- Accent Turquoise: #00CED1 (Dark Turquoise)

### 7. Logo Specifications
- Main Logo: Horizontal layout with text
- Icon: Circular blue/teal overlapping design
- Favicon: Multi-size ICO format
- Web Optimization: Responsive sizing

### 8. Support Contact
- Technical: openspecimen-support@longevityindia.org
- Branding: design@longevityindia.org
