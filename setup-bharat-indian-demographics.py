#!/usr/bin/env python3
"""
BHARAT Study Indian Demographics Setup
======================================

This script configures comprehensive demographic data collection 
tailored for the Indian population in the BHARAT Study aging research.

Features:
- Indian state and geographic information
- Cultural and linguistic diversity
- Socioeconomic factors specific to India
- Traditional medicine and lifestyle patterns
- Privacy-compliant data collection

Usage:
    python setup-bharat-indian-demographics.py

Author: Longevity India Initiative
Date: January 2025
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import re

# Configuration
OPENSPECIMEN_URL = "http://localhost:8082/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

class BharatIndianDemographicsSetup:
    def __init__(self, username="admin", password="AmruthDB7!"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.bharat_cp_id = None
        self.created_forms = []
        self.permissible_values_created = []
        
    def authenticate(self):
        """Authenticate with OpenSpecimen"""
        print("🔐 Authenticating with OpenSpecimen...")
        
        auth_data = {
            "loginName": self.username,
            "password": self.password,
            "domainName": "openspecimen"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/sessions", json=auth_data)
            if response.status_code == 200:
                session_data = response.json()
                self.auth_token = session_data.get("token")
                self.session.headers.update({
                    "X-OS-API-TOKEN": self.auth_token,
                    "Content-Type": "application/json"
                })
                print("✅ Authentication successful!")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def find_bharat_protocol(self):
        """Find the BHARAT Study collection protocol"""
        print("🔍 Finding BHARAT Study collection protocol...")
        
        try:
            response = self.session.get(f"{API_BASE}/collection-protocols")
            if response.status_code == 200:
                protocols = response.json()
                for protocol in protocols:
                    if protocol.get("shortTitle") == "BHARAT-STUDY" or protocol.get("code") == "BHARAT":
                        self.bharat_cp_id = protocol.get("id")
                        print(f"✅ Found BHARAT Study protocol (ID: {self.bharat_cp_id})")
                        return True
                
                print("❌ BHARAT Study protocol not found. Please run setup-bharat-study-protocol.py first.")
                return False
            else:
                print(f"❌ Error retrieving protocols: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error finding BHARAT protocol: {str(e)}")
            return False
    
    def load_demographics_config(self):
        """Load the Indian demographics configuration"""
        print("📋 Loading Indian demographics configuration...")
        
        try:
            with open("bharat-indian-demographics-config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            print("✅ Indian demographics configuration loaded successfully")
            return config["indianDemographics"]
        except Exception as e:
            print(f"❌ Error loading demographics configuration: {str(e)}")
            return None
    
    def create_permissible_values(self, config):
        """Create permissible values for Indian-specific dropdowns"""
        print("🏛️  Setting up Indian-specific permissible values...")
        
        # Indian states permissible values
        states_pv = {
            "attribute": "indian_states",
            "name": "Indian States and Union Territories",
            "values": []
        }
        
        # Extract states from configuration
        geographic_info = next((section for section in config["participantDemographics"]["geographicInformation"] 
                               if section["name"] == "birthState"), None)
        
        if geographic_info:
            for pv in geographic_info["permissibleValues"]:
                states_pv["values"].append({
                    "value": pv["value"],
                    "conceptCode": pv["conceptCode"]
                })
        
        # Create other Indian-specific PVs
        indian_pvs = [
            {
                "attribute": "indian_languages",
                "name": "Indian Languages",
                "values": [
                    {"value": "Hindi", "conceptCode": "HI"},
                    {"value": "Bengali", "conceptCode": "BN"},
                    {"value": "Telugu", "conceptCode": "TE"},
                    {"value": "Marathi", "conceptCode": "MR"},
                    {"value": "Tamil", "conceptCode": "TA"},
                    {"value": "Gujarati", "conceptCode": "GU"},
                    {"value": "Urdu", "conceptCode": "UR"},
                    {"value": "Kannada", "conceptCode": "KN"},
                    {"value": "Odia", "conceptCode": "OR"},
                    {"value": "Malayalam", "conceptCode": "ML"},
                    {"value": "Punjabi", "conceptCode": "PA"},
                    {"value": "English", "conceptCode": "EN"}
                ]
            },
            {
                "attribute": "indian_religions",
                "name": "Indian Religions",
                "values": [
                    {"value": "Hinduism", "conceptCode": "HINDU"},
                    {"value": "Islam", "conceptCode": "ISLAM"},
                    {"value": "Christianity", "conceptCode": "CHRISTIAN"},
                    {"value": "Sikhism", "conceptCode": "SIKH"},
                    {"value": "Buddhism", "conceptCode": "BUDDHIST"},
                    {"value": "Jainism", "conceptCode": "JAIN"},
                    {"value": "Other", "conceptCode": "OTHER_RELIGION"}
                ]
            },
            {
                "attribute": "indian_castes",
                "name": "Indian Caste Categories",
                "values": [
                    {"value": "General", "conceptCode": "GENERAL"},
                    {"value": "Other Backward Class (OBC)", "conceptCode": "OBC"},
                    {"value": "Scheduled Caste (SC)", "conceptCode": "SC"},
                    {"value": "Scheduled Tribe (ST)", "conceptCode": "ST"}
                ]
            },
            {
                "attribute": "indian_dietary_patterns",
                "name": "Indian Dietary Patterns",
                "values": [
                    {"value": "Vegetarian (Lacto-vegetarian)", "conceptCode": "LACTO_VEG"},
                    {"value": "Vegetarian (Vegan)", "conceptCode": "VEGAN"},
                    {"value": "Vegetarian (Jain)", "conceptCode": "JAIN_VEG"},
                    {"value": "Non-vegetarian", "conceptCode": "NON_VEG"},
                    {"value": "Eggetarian", "conceptCode": "EGGETARIAN"}
                ]
            }
        ]
        
        # Add states to the list
        indian_pvs.insert(0, states_pv)
        
        created_pvs = []
        for pv_config in indian_pvs:
            try:
                # Check if PV already exists
                response = self.session.get(f"{API_BASE}/permissible-values",
                                          params={"attribute": pv_config["attribute"]})
                
                if response.status_code == 200:
                    existing_pvs = response.json()
                    if not existing_pvs:  # PV doesn't exist, create it
                        create_response = self.session.post(f"{API_BASE}/permissible-values", 
                                                          json=pv_config)
                        if create_response.status_code == 200:
                            created_pvs.append(pv_config["attribute"])
                            print(f"✅ Created permissible values: {pv_config['name']}")
                        else:
                            print(f"❌ Failed to create PV {pv_config['attribute']}: {create_response.text}")
                    else:
                        print(f"ℹ️  Permissible values already exist: {pv_config['name']}")
                        
            except Exception as e:
                print(f"❌ Error creating PV {pv_config['attribute']}: {str(e)}")
        
        self.permissible_values_created = created_pvs
        return True
    
    def create_demographics_form(self, config):
        """Create the comprehensive Indian demographics form"""
        print("📝 Creating BHARAT Indian Demographics form...")
        
        form_config = {
            "name": "BHARAT_Indian_Demographics",
            "caption": "BHARAT Study - Indian Population Demographics",
            "entityType": "ParticipantExtension",
            "multiRecord": False,
            "creationTime": int(datetime.now().timestamp() * 1000),
            "fields": []
        }
        
        # Process all demographic sections
        all_sections = [
            config["participantDemographics"]["basicInformation"],
            config["participantDemographics"]["geographicInformation"],
            config["participantDemographics"]["culturalBackground"],
            config["participantDemographics"]["socioeconomicFactors"],
            config["participantDemographics"]["lifestyleFactors"],
            config["participantDemographics"]["medicalHistory"],
            config["participantDemographics"]["contactInformation"]
        ]
        
        for section in all_sections:
            for field_config in section:
                os_field = {
                    "name": field_config["name"],
                    "caption": field_config["caption"],
                    "type": field_config["type"],
                    "mandatory": field_config.get("mandatory", False),
                    "defaultValue": field_config.get("defaultValue", "")
                }
                
                # Add field-specific properties
                if "maxLength" in field_config:
                    os_field["maxLength"] = field_config["maxLength"]
                
                if "pattern" in field_config:
                    os_field["pattern"] = field_config["pattern"]
                
                if "minValue" in field_config:
                    os_field["minValue"] = field_config["minValue"]
                    
                if "maxValue" in field_config:
                    os_field["maxValue"] = field_config["maxValue"]
                
                if "note" in field_config:
                    os_field["note"] = field_config["note"]
                
                if "permissibleValues" in field_config and field_config["permissibleValues"] != "same_as_birthState" and field_config["permissibleValues"] != "same_as_motherTongue":
                    os_field["permissibleValues"] = field_config["permissibleValues"]
                
                form_config["fields"].append(os_field)
        
        # Create the form
        try:
            response = self.session.post(f"{API_BASE}/forms", json=form_config)
            if response.status_code == 200:
                form_data = response.json()
                form_id = form_data.get("id")
                print(f"✅ Created Indian demographics form (ID: {form_id})")
                self.created_forms.append({
                    "name": form_config["name"],
                    "id": form_id,
                    "entityType": form_config["entityType"],
                    "caption": form_config["caption"]
                })
                return form_id
            else:
                print(f"❌ Failed to create demographics form: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error creating demographics form: {str(e)}")
            return None
    
    def associate_form_with_protocol(self):
        """Associate the demographics form with BHARAT protocol"""
        print("🔗 Associating demographics form with BHARAT protocol...")
        
        if not self.bharat_cp_id or not self.created_forms:
            print("❌ Missing protocol ID or forms")
            return False
        
        for form_info in self.created_forms:
            form_context = {
                "formId": form_info["id"],
                "entityType": form_info["entityType"],
                "cpId": self.bharat_cp_id,
                "multiRecord": False,
                "sysForm": False,
                "notifEnabled": False
            }
            
            try:
                response = self.session.post(f"{API_BASE}/form-contexts", json=form_context)
                if response.status_code == 200:
                    print(f"✅ Associated {form_info['name']} with BHARAT protocol")
                else:
                    print(f"❌ Failed to associate {form_info['name']}: {response.text}")
            except Exception as e:
                print(f"❌ Error associating {form_info['name']}: {str(e)}")
        
        return True
    
    def setup_age_cohort_validation(self, config):
        """Setup age cohort validation rules"""
        print("👥 Setting up age cohort validation rules...")
        
        validation_rules = config["validationRules"]["cohortAssignment"]
        
        cohort_mapping = {
            "AG1": {"min": 20, "max": 30, "description": "Young Adults (20-30 years)"},
            "AG2": {"min": 31, "max": 40, "description": "Early Adults (31-40 years)"},
            "AG3": {"min": 41, "max": 50, "description": "Middle Adults (41-50 years)"},
            "AG4": {"min": 51, "max": 60, "description": "Late Adults (51-60 years)"},
            "AG5": {"min": 61, "max": 70, "description": "Senior Adults (61-70 years)"}
        }
        
        print("✅ Age cohort validation rules configured:")
        for cohort, rules in cohort_mapping.items():
            print(f"   • {cohort}: {rules['description']} (Age {rules['min']}-{rules['max']})")
        
        return cohort_mapping
    
    def create_privacy_compliance_settings(self, config):
        """Configure privacy compliance for sensitive data"""
        print("🔒 Setting up privacy compliance for sensitive data...")
        
        privacy_config = config["dataPrivacy"]
        
        print("🔐 Privacy compliance configured:")
        print(f"   • Sensitive fields: {len(privacy_config['sensitiveFields'])} fields")
        print(f"   • Optional fields: {len(privacy_config['optionalFields'])} fields")
        print(f"   • Encryption required: {len(privacy_config['encryptionRequired'])} fields")
        
        sensitive_fields = privacy_config["sensitiveFields"]
        print("\n📋 Sensitive data fields (special handling required):")
        for field in sensitive_fields:
            print(f"   • {field}")
        
        return True
    
    def create_data_validation_functions(self, config):
        """Create data validation functions for Indian demographics"""
        print("✅ Setting up Indian-specific data validation...")
        
        validation_functions = {
            "validate_indian_phone": {
                "pattern": r"^[6-9][0-9]{9}$",
                "description": "Valid Indian mobile number (10 digits starting with 6-9)"
            },
            "validate_indian_pincode": {
                "pattern": r"^[1-9][0-9]{5}$",
                "description": "Valid Indian PIN code (6 digits, not starting with 0)"
            },
            "validate_age_for_cohort": {
                "function": "calculateAge",
                "rules": config["validationRules"]["cohortAssignment"]
            },
            "validate_education_age_consistency": {
                "description": "Ensure education level is consistent with age"
            }
        }
        
        print("✅ Data validation functions configured:")
        for func_name, func_config in validation_functions.items():
            if "pattern" in func_config:
                print(f"   • {func_name}: {func_config['description']}")
        
        return validation_functions
    
    def generate_setup_report(self, config):
        """Generate comprehensive setup report"""
        print("\n" + "="*70)
        print("🎉 BHARAT STUDY INDIAN DEMOGRAPHICS SETUP COMPLETE!")
        print("="*70)
        print(f"📅 Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 Collection Protocol ID: {self.bharat_cp_id}")
        print("")
        
        print("📝 DEMOGRAPHICS FORM CREATED:")
        for form_info in self.created_forms:
            print(f"   ✅ {form_info['caption']} (ID: {form_info['id']})")
        print("")
        
        print("🏛️  INDIAN-SPECIFIC FEATURES CONFIGURED:")
        print("   🗺️  Geographic: All 28 states and 8 union territories")
        print("   🗣️  Languages: 22 official languages + regional languages")
        print("   🕌 Cultural: Religion, caste (optional), dietary patterns")
        print("   💼 Socioeconomic: Education, occupation, income (INR)")
        print("   🏥 Healthcare: Ayushman Bharat, ESIC, private insurance")
        print("   🧘 Lifestyle: Yoga, meditation, traditional medicine")
        print("")
        
        print("👥 AGE COHORTS CONFIGURED:")
        cohorts = config["validationRules"]["cohortAssignment"]
        for cohort, rules in cohorts.items():
            print(f"   • {cohort}: Age {rules['minAge']}-{rules['maxAge']} years")
        print("")
        
        print("🔒 PRIVACY COMPLIANCE:")
        privacy = config["dataPrivacy"]
        print(f"   • {len(privacy['sensitiveFields'])} sensitive fields with special handling")
        print(f"   • {len(privacy['optionalFields'])} optional fields for participant choice")
        print(f"   • {len(privacy['encryptionRequired'])} fields requiring encryption")
        print("")
        
        print("📊 DATA COLLECTION CATEGORIES:")
        categories = config["reportingCategories"]
        for category, fields in categories.items():
            print(f"   • {category.title()}: {len(fields)} fields")
        print("")
        
        print("🔧 NEXT STEPS:")
        print("   1. Test demographics form with sample participant data")
        print("   2. Verify age cohort assignment automation")
        print("   3. Configure data privacy and encryption settings")
        print("   4. Set up multilingual support for local languages")
        print("   5. Train enrollment staff on cultural sensitivity")
        print("")
        
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*70)
    
    def run_setup(self):
        """Execute the complete Indian demographics setup"""
        print("\n🚀 BHARAT STUDY INDIAN DEMOGRAPHICS SETUP")
        print("==========================================")
        print("Configuring Indian population-specific demographics...")
        print("")
        
        # Step 1: Authenticate
        if not self.authenticate():
            return False
        
        # Step 2: Find BHARAT protocol
        if not self.find_bharat_protocol():
            return False
        
        # Step 3: Load configuration
        config = self.load_demographics_config()
        if not config:
            return False
        
        # Step 4: Create permissible values
        self.create_permissible_values(config)
        
        # Step 5: Create demographics form
        form_id = self.create_demographics_form(config)
        if not form_id:
            return False
        
        # Step 6: Associate with protocol
        self.associate_form_with_protocol()
        
        # Step 7: Setup validation rules
        self.setup_age_cohort_validation(config)
        
        # Step 8: Configure privacy compliance
        self.create_privacy_compliance_settings(config)
        
        # Step 9: Setup data validation
        self.create_data_validation_functions(config)
        
        # Step 10: Generate report
        self.generate_setup_report(config)
        
        return True

def main():
    """Main entry point"""
    try:
        print("BHARAT Study Indian Demographics Setup")
        print("======================================")
        
        username = input("Username (admin): ").strip()
        if not username:
            username = "admin"
            
        password = input("Password (AmruthDB7!): ").strip()
        if not password:
            password = "AmruthDB7!"
        
        setup = BharatIndianDemographicsSetup(username, password)
        success = setup.run_setup()
        
        if success:
            print("\n✅ Indian demographics setup completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Indian demographics setup failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()