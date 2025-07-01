#!/usr/bin/env python3
"""
Manual BHARAT Study Customizations Deployment
=============================================

This script manually deploys the BHARAT Study customizations by copying
files to the appropriate locations in the OpenSpecimen deployment.

Usage:
    python deploy-bharat-customizations.py
"""

import os
import shutil
from pathlib import Path

def deploy_customizations():
    print("🚀 DEPLOYING BHARAT STUDY CUSTOMIZATIONS")
    print("=" * 50)
    
    # Define source and target paths
    base_dir = Path("/home/adb/openspecimen")
    www_dir = base_dir / "www"
    dist_dir = www_dir / "dist"
    
    # Create dist directory if it doesn't exist
    dist_dir.mkdir(exist_ok=True)
    
    # Deploy branding assets
    print("🎨 Deploying branding assets...")
    
    # Copy CSS theme
    if (base_dir / "longevity-india-theme.css").exists():
        shutil.copy2(base_dir / "longevity-india-theme.css", dist_dir)
        print("✅ Deployed longevity-india-theme.css")
    
    # Copy dashboard JavaScript
    if (base_dir / "longevity-india-dashboard.js").exists():
        shutil.copy2(base_dir / "longevity-india-dashboard.js", dist_dir)
        print("✅ Deployed longevity-india-dashboard.js")
    
    # Copy logo images
    images_dir = dist_dir / "images"
    images_dir.mkdir(exist_ok=True)
    
    logo_files = [
        "longevity-india-logo.png",
        "longevity-india-logo-web.png", 
        "longevity-india-icon.png",
        "longevity-india-favicon.ico"
    ]
    
    for logo_file in logo_files:
        src = base_dir / "images" / logo_file
        if src.exists():
            shutil.copy2(src, images_dir)
            print(f"✅ Deployed {logo_file}")
    
    # Deploy dashboard HTML files
    print("📊 Deploying dashboard files...")
    
    dashboard_files = [
        "bharat-study-overview-dashboard.html",
        "bharat-biomarker-analytics-dashboard.html", 
        "bharat-inventory-dashboard.html",
        "bharat-dashboard-charts.js"
    ]
    
    for dashboard_file in dashboard_files:
        src = base_dir / dashboard_file
        if src.exists():
            shutil.copy2(src, dist_dir)
            print(f"✅ Deployed {dashboard_file}")
    
    # Copy configuration files to a configs directory
    configs_dir = dist_dir / "configs"
    configs_dir.mkdir(exist_ok=True)
    
    config_files = [
        "bharat-study-collection-protocol.json",
        "bharat-study-labeling-config.json",
        "bharat-multi-omics-forms.json",
        "bharat-indian-demographics-config.json", 
        "bharat-aging-dashboards-config.json",
        "bharat-kit-tracking-config.json",
        "longevity-india-branding-config.json"
    ]
    
    print("📋 Deploying configuration files...")
    for config_file in config_files:
        src = base_dir / config_file
        if src.exists():
            shutil.copy2(src, configs_dir)
            print(f"✅ Deployed {config_file}")
    
    # Create an index file for easy access
    create_access_page(dist_dir)
    
    print("\n" + "=" * 50)
    print("🎉 BHARAT STUDY CUSTOMIZATIONS DEPLOYED!")
    print("=" * 50)
    print(f"📂 Files deployed to: {dist_dir}")
    print("🌐 Access via: http://localhost:8082/openspecimen/dist/")
    print("📊 Main dashboard: http://localhost:8082/openspecimen/dist/bharat-study-overview-dashboard.html")
    print("⚙️ Configuration files: http://localhost:8082/openspecimen/dist/configs/")

def create_access_page(dist_dir):
    """Create a simple access page for the BHARAT Study customizations"""
    
    access_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BHARAT Study - Longevity India</title>
    <link rel="stylesheet" href="longevity-india-theme.css">
    <link rel="icon" href="images/longevity-india-favicon.ico">
</head>
<body>
    <div style="padding: 40px; max-width: 1200px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 40px;">
            <img src="images/longevity-india-logo-web.png" alt="Longevity India" style="height: 80px; margin-bottom: 20px;">
            <h1 style="color: #4169E1; margin-bottom: 10px;">BHARAT Study Customizations</h1>
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
                <h3 style="color: #4169E1; margin-bottom: 15px;">⚙️ Configuration Files</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;">
                        <a href="configs/bharat-study-collection-protocol.json" style="color: #20B2AA; text-decoration: none;">
                            📋 Collection Protocol
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="configs/bharat-multi-omics-forms.json" style="color: #20B2AA; text-decoration: none;">
                            🧪 Multi-Omics Forms
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="configs/bharat-indian-demographics-config.json" style="color: #20B2AA; text-decoration: none;">
                            🇮🇳 Indian Demographics
                        </a>
                    </li>
                </ul>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #4169E1; margin-bottom: 15px;">🎨 Branding Assets</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 10px;">
                        <a href="longevity-india-theme.css" style="color: #20B2AA; text-decoration: none;">
                            🎨 Theme CSS
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="images/longevity-india-logo.png" style="color: #20B2AA; text-decoration: none;">
                            🖼️ Main Logo
                        </a>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <a href="images/longevity-india-icon.png" style="color: #20B2AA; text-decoration: none;">
                            🔷 Icon Logo
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #F8F9FA; border-radius: 8px; border-left: 4px solid #4169E1;">
            <h3 style="color: #4169E1; margin-bottom: 15px;">🚀 Next Steps</h3>
            <ol style="color: #666;">
                <li>Access the OpenSpecimen admin interface</li>
                <li>Run the setup scripts to create protocols and forms</li>
                <li>Import the study configuration files</li>
                <li>Test the dashboards and functionality</li>
                <li>Configure user permissions and roles</li>
            </ol>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 0.9rem;">
            <p>BHARAT Study - Longevity India Initiative</p>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
    
    with open(dist_dir / "index.html", "w") as f:
        f.write(access_page.format(datetime=__import__('datetime')))
    
    print("✅ Created access page: index.html")

if __name__ == "__main__":
    deploy_customizations()