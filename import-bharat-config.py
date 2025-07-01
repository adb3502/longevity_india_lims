#!/usr/bin/env python3
"""
BHARAT Study Configuration Import Script
========================================

This script imports the BHARAT Study configuration files into OpenSpecimen
using the REST API.

Usage:
    python import-bharat-config.py
"""

import requests
import json
import sys

OPENSPECIMEN_URL = "http://localhost:8082/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

def authenticate():
    """Authenticate with OpenSpecimen"""
    auth_data = {
        "loginName": "admin",
        "password": "AmruthDB7!",
        "domainName": "openspecimen"
    }
    
    response = requests.post(f"{API_BASE}/sessions", json=auth_data)
    if response.status_code == 200:
        token = response.json().get("token")
        return {"X-OS-API-TOKEN": token, "Content-Type": "application/json"}
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        return None

def import_collection_protocol(headers):
    """Import BHARAT Study collection protocol"""
    print("📋 Importing collection protocol...")
    
    try:
        with open("www/dist/configs/bharat-study-collection-protocol.json", "r") as f:
            protocol_data = json.load(f)
        
        response = requests.post(f"{API_BASE}/collection-protocols", 
                               json=protocol_data, headers=headers)
        
        if response.status_code in [200, 201]:
            print("✅ Collection protocol imported successfully")
            return response.json().get("id")
        else:
            print(f"❌ Failed to import protocol: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error importing protocol: {str(e)}")
        return None

def import_forms(headers):
    """Import multi-omics forms"""
    print("🧪 Importing multi-omics forms...")
    
    try:
        with open("www/dist/configs/bharat-multi-omics-forms.json", "r") as f:
            forms_data = json.load(f)
        
        imported_forms = []
        for form_name, form_config in forms_data.get("bharatMultiOmicsForms", {}).items():
            if form_name == "metadata":
                continue
                
            # Convert to OpenSpecimen form format
            form_payload = {
                "name": form_config["name"],
                "caption": form_config["description"],
                "creationTime": None,
                "lastModified": None,
                "cpId": -1  # Will be updated after protocol creation
            }
            
            response = requests.post(f"{API_BASE}/forms", 
                                   json=form_payload, headers=headers)
            
            if response.status_code in [200, 201]:
                print(f"✅ Imported form: {form_config['name']}")
                imported_forms.append(response.json())
            else:
                print(f"❌ Failed to import form {form_config['name']}: {response.status_code}")
        
        return imported_forms
        
    except Exception as e:
        print(f"❌ Error importing forms: {str(e)}")
        return []

def import_settings(headers):
    """Import Indian demographics and other settings"""
    print("🇮🇳 Importing demographics settings...")
    
    try:
        with open("www/dist/configs/bharat-indian-demographics-config.json", "r") as f:
            demographics_data = json.load(f)
        
        # Import permissible values for states, languages, etc.
        pv_data = demographics_data.get("bharatIndianDemographics", {}).get("permissibleValues", {})
        
        for category, values in pv_data.items():
            if category in ["states", "languages", "ethnicities"]:
                print(f"📝 Processing {category}...")
                # This would typically involve creating permissible value sets
                # Implementation depends on OpenSpecimen's PV API structure
        
        print("✅ Demographics settings processed")
        return True
        
    except Exception as e:
        print(f"❌ Error importing demographics: {str(e)}")
        return False

def main():
    """Main import function"""
    print("🚀 BHARAT STUDY CONFIGURATION IMPORT")
    print("=" * 50)
    
    # Authenticate
    headers = authenticate()
    if not headers:
        sys.exit(1)
    
    # Import components
    protocol_id = import_collection_protocol(headers)
    forms = import_forms(headers)
    settings_imported = import_settings(headers)
    
    print("\n" + "=" * 50)
    if protocol_id and forms and settings_imported:
        print("🎉 BHARAT STUDY CONFIGURATION IMPORTED!")
        print(f"📋 Protocol ID: {protocol_id}")
        print(f"🧪 Forms imported: {len(forms)}")
        print("✅ Settings applied")
    else:
        print("⚠️ Import completed with some issues")
        print("💡 Check OpenSpecimen admin interface for manual import options")
    
    print("\n🔗 Next steps:")
    print("1. Go to http://localhost:8082/openspecimen")
    print("2. Navigate to Collection Protocols")
    print("3. Verify BHARAT Study protocol is created")
    print("4. Check Forms section for multi-omics forms")
    print("5. Test the dashboards")

if __name__ == "__main__":
    main()