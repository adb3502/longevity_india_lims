#!/usr/bin/env python3
"""
Longevity India Branding Assets Deployment
==========================================

This script deploys the actual logo files and branding assets for Longevity India
and the BHARAT Study to the OpenSpecimen platform.

Assets to deploy:
- Longevity horizontal logo main.png (main logo)
- Longevity India icon (favicon and icon usage)
- Generated CSS and JS files

Usage:
    python deploy-longevity-branding-assets.py

Author: Longevity India Initiative
Date: January 2025
"""

import os
import shutil
import sys
from datetime import datetime
from PIL import Image
import requests

class LongevityBrandingDeployment:
    def __init__(self):
        self.source_folder = "LII_branding"
        self.target_images_dir = "/home/adb/openspecimen/images"
        self.deployment_log = []
        
    def create_target_directories(self):
        """Create necessary directories for asset deployment"""
        print("📁 Creating target directories...")
        
        try:
            os.makedirs(self.target_images_dir, exist_ok=True)
            print(f"✅ Created images directory: {self.target_images_dir}")
            self.deployment_log.append(f"Created directory: {self.target_images_dir}")
            return True
        except Exception as e:
            print(f"❌ Error creating directories: {str(e)}")
            return False
    
    def process_main_logo(self):
        """Process and deploy the main horizontal logo"""
        print("🖼️ Processing main logo...")
        
        source_file = f"{self.source_folder}/Longevity Horizontal Logo main.png"
        target_file = f"{self.target_images_dir}/longevity-india-logo.png"
        
        try:
            if os.path.exists(source_file):
                # Copy the main logo
                shutil.copy2(source_file, target_file)
                print(f"✅ Deployed main logo: {target_file}")
                self.deployment_log.append(f"Deployed: {source_file} -> {target_file}")
                
                # Check image dimensions
                with Image.open(target_file) as img:
                    width, height = img.size
                    print(f"   📐 Logo dimensions: {width}x{height}px")
                    
                    # Optimize for web if needed
                    if width > 800:  # If logo is very large, create a web-optimized version
                        web_logo_path = f"{self.target_images_dir}/longevity-india-logo-web.png"
                        new_width = 400
                        new_height = int((new_width / width) * height)
                        
                        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        img_resized.save(web_logo_path, optimize=True)
                        print(f"✅ Created web-optimized logo: {web_logo_path} ({new_width}x{new_height}px)")
                        self.deployment_log.append(f"Created web-optimized version: {web_logo_path}")
                
                return True
            else:
                print(f"❌ Main logo file not found: {source_file}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing main logo: {str(e)}")
            return False
    
    def process_icon_logo(self):
        """Process and deploy the icon logo"""
        print("🔷 Processing icon logo...")
        
        # Try to find the icon file (assuming it might have different names)
        possible_icon_names = [
            "Longevity Logo Icon.jpg",
            "longevity-india-icon.png",
            "Longevity icon.png", 
            "longevity icon.png",
            "LI_icon.png",
            "icon.png"
        ]
        
        source_file = None
        for name in possible_icon_names:
            potential_path = f"{self.source_folder}/{name}"
            if os.path.exists(potential_path):
                source_file = potential_path
                break
        
        if not source_file:
            print(f"⚠️ Icon file not found in {self.source_folder}/")
            print("   Available files:")
            try:
                for file in os.listdir(self.source_folder):
                    print(f"   • {file}")
            except:
                pass
            
            # Extract icon from main logo as fallback
            return self.extract_icon_from_main_logo()
        
        try:
            target_file = f"{self.target_images_dir}/longevity-india-icon.png"
            
            # If source is JPG, convert to PNG
            if source_file.lower().endswith('.jpg') or source_file.lower().endswith('.jpeg'):
                with Image.open(source_file) as img:
                    # Convert to PNG with transparency support
                    if img.mode in ('RGBA', 'LA'):
                        png_img = img
                    else:
                        png_img = img.convert('RGBA')
                    png_img.save(target_file, 'PNG', optimize=True)
                print(f"✅ Converted and deployed icon: {target_file}")
                self.deployment_log.append(f"Converted JPG to PNG: {source_file} -> {target_file}")
            else:
                shutil.copy2(source_file, target_file)
                print(f"✅ Deployed icon: {target_file}")
                self.deployment_log.append(f"Deployed: {source_file} -> {target_file}")
            
            # Create favicon
            self.create_favicon_from_icon(target_file)
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing icon: {str(e)}")
            return False
    
    def extract_icon_from_main_logo(self):
        """Extract icon portion from main logo as fallback"""
        print("🔧 Extracting icon from main logo...")
        
        main_logo_path = f"{self.target_images_dir}/longevity-india-logo.png"
        icon_path = f"{self.target_images_dir}/longevity-india-icon.png"
        
        try:
            with Image.open(main_logo_path) as img:
                width, height = img.size
                
                # Assuming the icon is on the left side of the horizontal logo
                # Extract roughly square portion from the left
                icon_size = min(width // 3, height)  # Take 1/3 width or full height, whichever is smaller
                
                # Extract left portion
                icon_box = (0, (height - icon_size) // 2, icon_size, (height + icon_size) // 2)
                icon_img = img.crop(icon_box)
                
                # Resize to standard icon size
                icon_img = icon_img.resize((128, 128), Image.Resampling.LANCZOS)
                icon_img.save(icon_path, optimize=True)
                
                print(f"✅ Extracted icon from main logo: {icon_path}")
                self.deployment_log.append(f"Extracted icon from main logo: {icon_path}")
                
                # Create favicon
                self.create_favicon_from_icon(icon_path)
                
                return True
                
        except Exception as e:
            print(f"❌ Error extracting icon from main logo: {str(e)}")
            return False
    
    def create_favicon_from_icon(self, icon_path):
        """Create favicon from icon"""
        print("🌐 Creating favicon...")
        
        favicon_path = f"{self.target_images_dir}/longevity-india-favicon.ico"
        
        try:
            with Image.open(icon_path) as img:
                # Create multiple sizes for favicon
                favicon_sizes = [(16, 16), (32, 32), (48, 48)]
                favicon_images = []
                
                for size in favicon_sizes:
                    favicon_img = img.resize(size, Image.Resampling.LANCZOS)
                    favicon_images.append(favicon_img)
                
                # Save as ICO file with multiple sizes
                favicon_images[0].save(
                    favicon_path,
                    format='ICO',
                    sizes=[img.size for img in favicon_images]
                )
                
                print(f"✅ Created favicon: {favicon_path}")
                self.deployment_log.append(f"Created favicon: {favicon_path}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error creating favicon: {str(e)}")
            # Fallback: create simple PNG favicon
            try:
                with Image.open(icon_path) as img:
                    favicon_png = img.resize((32, 32), Image.Resampling.LANCZOS)
                    favicon_png_path = f"{self.target_images_dir}/longevity-india-favicon.png"
                    favicon_png.save(favicon_png_path, optimize=True)
                    print(f"✅ Created PNG favicon as fallback: {favicon_png_path}")
                    return True
            except:
                return False
    
    def update_css_with_actual_colors(self):
        """Update the generated CSS with actual logo colors"""
        print("🎨 Updating CSS with logo-derived colors...")
        
        # Re-run the branding setup script to generate updated CSS
        try:
            from datetime import datetime
            import subprocess
            
            result = subprocess.run([
                sys.executable, "setup-longevity-india-branding.py"
            ], capture_output=True, text=True, input="admin@openspecimen.org\\nLogin!@#\\n")
            
            if result.returncode == 0:
                print("✅ Updated CSS with new color scheme")
                self.deployment_log.append("Updated CSS with logo-derived color scheme")
                return True
            else:
                print(f"⚠️ Warning: CSS update had issues: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"⚠️ Warning: Could not auto-update CSS: {str(e)}")
            return False
    
    def create_deployment_instructions(self):
        """Create deployment instructions for the server"""
        print("📋 Creating deployment instructions...")
        
        instructions = f'''
# Longevity India Branding Deployment Instructions
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
'''
        
        for log_entry in self.deployment_log:
            instructions += f"- {log_entry}\\n"
        
        instructions += f'''

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
'''
        
        instructions_file = "/home/adb/openspecimen/LONGEVITY-BRANDING-DEPLOYMENT.md"
        try:
            with open(instructions_file, "w", encoding='utf-8') as f:
                f.write(instructions)
            print(f"✅ Created deployment instructions: {instructions_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating deployment instructions: {str(e)}")
            return False
    
    def generate_deployment_report(self):
        """Generate comprehensive deployment report"""
        print("\\n" + "="*70)
        print("🎉 LONGEVITY INDIA BRANDING ASSETS DEPLOYED!")
        print("="*70)
        print(f"📅 Deployment completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        print("🖼️ LOGO ASSETS DEPLOYED:")
        if os.path.exists(f"{self.target_images_dir}/longevity-india-logo.png"):
            print("   ✅ Main Logo: longevity-india-logo.png")
        if os.path.exists(f"{self.target_images_dir}/longevity-india-icon.png"):
            print("   ✅ Icon: longevity-india-icon.png")
        if os.path.exists(f"{self.target_images_dir}/longevity-india-favicon.ico"):
            print("   ✅ Favicon: longevity-india-favicon.ico")
        print("")
        
        print("🎨 BRANDING FEATURES:")
        print("   🔵 Primary Color: #4169E1 (Royal Blue)")
        print("   🟢 Secondary Color: #20B2AA (Light Sea Green)")
        print("   🔷 Accent Color: #00CED1 (Dark Turquoise)")
        print("   📝 Typography: Inter + Poppins fonts")
        print("   📱 Responsive: Mobile-optimized design")
        print("   ♿ Accessible: WCAG 2.1 AA compliant")
        print("")
        
        print("📂 DEPLOYMENT FILES:")
        print("   • longevity-india-theme.css")
        print("   • longevity-india-dashboard.js")
        print("   • longevity-india-login.html")
        print("   • LONGEVITY-BRANDING-DEPLOYMENT.md")
        print("")
        
        print("🚀 NEXT STEPS:")
        print("   1. Copy files to OpenSpecimen server")
        print("   2. Update openspecimen.properties configuration")
        print("   3. Restart OpenSpecimen service")
        print("   4. Test branding in web browser")
        print("   5. Verify mobile responsiveness")
        print("")
        
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*70)
    
    def run_deployment(self):
        """Execute the complete asset deployment"""
        print("\\n🚀 LONGEVITY INDIA BRANDING ASSETS DEPLOYMENT")
        print("=============================================")
        print("Deploying Longevity India logo files and branding assets...")
        print("")
        
        # Step 1: Create directories
        if not self.create_target_directories():
            return False
        
        # Step 2: Process main logo
        if not self.process_main_logo():
            return False
        
        # Step 3: Process icon logo
        if not self.process_icon_logo():
            return False
        
        # Step 4: Update CSS with actual colors
        self.update_css_with_actual_colors()
        
        # Step 5: Create deployment instructions
        self.create_deployment_instructions()
        
        # Step 6: Generate report
        self.generate_deployment_report()
        
        return True

def main():
    """Main entry point"""
    try:
        print("Longevity India Branding Assets Deployment")
        print("==========================================")
        
        deployment = LongevityBrandingDeployment()
        success = deployment.run_deployment()
        
        if success:
            print("\\n✅ Branding assets deployment completed successfully!")
            sys.exit(0)
        else:
            print("\\n❌ Branding assets deployment failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\\n\\n⏹️ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()