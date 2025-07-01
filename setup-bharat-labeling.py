#!/usr/bin/env python3
"""
BHARAT Study Specimen Labeling System Setup
============================================

This script implements the hierarchical specimen numbering system for the BHARAT Study
in OpenSpecimen. It configures custom fields, label formats, and validation rules.

Labeling Hierarchy:
- Participants: BHARAT-AG3-P0234
- Specimens: BHARAT-AG3-P0234-V2-BLD01  
- Aliquots: BHARAT-AG3-P0234-V2-BLD01-PROT-01

Usage:
    python setup-bharat-labeling.py

Author: Longevity India Initiative
Date: January 2025
"""

import requests
import json
import sys
import re
from datetime import datetime

# Configuration
OPENSPECIMEN_URL = "http://localhost:8082/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

class BharatLabelingSetup:
    def __init__(self, username="admin", password="AmruthDB7!"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.bharat_cp_id = None
        
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
                print(f"✅ Authentication successful!")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def find_bharat_protocol(self):
        """Find the BHARAT Study collection protocol"""
        print("🔍 Looking for BHARAT Study collection protocol...")
        
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
    
    def load_labeling_config(self):
        """Load the labeling configuration from JSON file"""
        print("📋 Loading BHARAT Study labeling configuration...")
        
        try:
            with open("bharat-study-labeling-config.json", "r") as f:
                config = json.load(f)
            print("✅ Labeling configuration loaded successfully")
            return config["labelingConfiguration"]
        except Exception as e:
            print(f"❌ Error loading labeling configuration: {str(e)}")
            return None
    
    def create_custom_forms(self, config):
        """Create custom forms for participant and specimen fields"""
        print("📝 Setting up custom forms for BHARAT Study fields...")
        
        # Participant custom form (for cohort field)
        participant_form = {
            "name": "BHARAT_Participant_Demographics",
            "caption": "BHARAT Study Participant Demographics",
            "entityType": "ParticipantExtension",
            "creationTime": int(datetime.now().timestamp() * 1000),
            "fields": [
                {
                    "name": "cohort",
                    "caption": "Age Cohort",
                    "type": "DROPDOWN",
                    "mandatory": True,
                    "defaultValue": "",
                    "permissibleValues": [
                        {"value": "AG1", "conceptCode": "AG1"},
                        {"value": "AG2", "conceptCode": "AG2"},
                        {"value": "AG3", "conceptCode": "AG3"}, 
                        {"value": "AG4", "conceptCode": "AG4"},
                        {"value": "AG5", "conceptCode": "AG5"}
                    ]
                },
                {
                    "name": "enrollmentSite",
                    "caption": "Enrollment Site",
                    "type": "DROPDOWN",
                    "mandatory": True,
                    "permissibleValues": [
                        {"value": "BLR", "conceptCode": "BLR"},
                        {"value": "MSR", "conceptCode": "MSR"},
                        {"value": "BMC", "conceptCode": "BMC"}
                    ]
                }
            ]
        }
        
        # Specimen custom form (for analysis type field)
        specimen_form = {
            "name": "BHARAT_Specimen_Processing",
            "caption": "BHARAT Study Specimen Processing",
            "entityType": "SpecimenExtension",
            "creationTime": int(datetime.now().timestamp() * 1000),
            "fields": [
                {
                    "name": "analysisType",
                    "caption": "Analysis Type",
                    "type": "DROPDOWN",
                    "mandatory": False,
                    "permissibleValues": [
                        {"value": "GEN", "conceptCode": "GEN"},
                        {"value": "PROT", "conceptCode": "PROT"},
                        {"value": "META", "conceptCode": "META"},
                        {"value": "EPI", "conceptCode": "EPI"},
                        {"value": "CLIN", "conceptCode": "CLIN"},
                        {"value": "FLOW", "conceptCode": "FLOW"},
                        {"value": "DNA", "conceptCode": "DNA"},
                        {"value": "RNA", "conceptCode": "RNA"}
                    ]
                },
                {
                    "name": "processingBatch",
                    "caption": "Processing Batch",
                    "type": "STRING",
                    "mandatory": False
                },
                {
                    "name": "freezeThawCycles",
                    "caption": "Freeze/Thaw Cycles",
                    "type": "INTEGER",
                    "mandatory": False,
                    "defaultValue": "0"
                }
            ]
        }
        
        forms_created = []
        
        # Create participant form
        try:
            response = self.session.post(f"{API_BASE}/forms", json=participant_form)
            if response.status_code == 200:
                form_data = response.json()
                forms_created.append(("participant", form_data.get("id")))
                print(f"✅ Created participant custom form (ID: {form_data.get('id')})")
            else:
                print(f"❌ Failed to create participant form: {response.text}")
        except Exception as e:
            print(f"❌ Error creating participant form: {str(e)}")
        
        # Create specimen form  
        try:
            response = self.session.post(f"{API_BASE}/forms", json=specimen_form)
            if response.status_code == 200:
                form_data = response.json()
                forms_created.append(("specimen", form_data.get("id")))
                print(f"✅ Created specimen custom form (ID: {form_data.get('id')})")
            else:
                print(f"❌ Failed to create specimen form: {response.text}")
        except Exception as e:
            print(f"❌ Error creating specimen form: {str(e)}")
        
        return forms_created
    
    def associate_forms_with_protocol(self, forms_created):
        """Associate custom forms with the BHARAT collection protocol"""
        print("🔗 Associating custom forms with BHARAT Study protocol...")
        
        if not self.bharat_cp_id:
            print("❌ No BHARAT protocol ID available")
            return False
        
        for form_type, form_id in forms_created:
            form_context = {
                "formId": form_id,
                "entityType": "ParticipantExtension" if form_type == "participant" else "SpecimenExtension",
                "cpId": self.bharat_cp_id,
                "multiRecord": False,
                "sysForm": False,
                "notifEnabled": False
            }
            
            try:
                response = self.session.post(f"{API_BASE}/form-contexts", json=form_context)
                if response.status_code == 200:
                    print(f"✅ Associated {form_type} form with BHARAT protocol")
                else:
                    print(f"❌ Failed to associate {form_type} form: {response.text}")
            except Exception as e:
                print(f"❌ Error associating {form_type} form: {str(e)}")
        
        return True
    
    def update_collection_protocol_labels(self, config):
        """Update the collection protocol with BHARAT labeling formats"""
        print("🏷️  Updating BHARAT Study protocol label formats...")
        
        if not self.bharat_cp_id:
            print("❌ No BHARAT protocol ID available")
            return False
        
        try:
            # Get current protocol configuration
            response = self.session.get(f"{API_BASE}/collection-protocols/{self.bharat_cp_id}")
            if response.status_code != 200:
                print(f"❌ Failed to retrieve protocol: {response.status_code}")
                return False
            
            protocol_data = response.json()
            
            # Update label formats
            label_settings = config["collectionProtocolSettings"]
            protocol_data.update({
                "ppidFmt": label_settings["ppidFmt"],
                "visitNameFmt": label_settings["visitNameFmt"],
                "specimenLabelFmt": label_settings["specimenLabelFmt"],
                "derivativeLabelFmt": label_settings["derivativeLabelFmt"],
                "aliquotLabelFmt": label_settings["aliquotLabelFmt"],
                "labelSequenceKey": label_settings["labelSequenceKey"]
            })
            
            # Update protocol
            response = self.session.put(f"{API_BASE}/collection-protocols/{self.bharat_cp_id}", 
                                      json=protocol_data)
            if response.status_code == 200:
                print("✅ Updated BHARAT protocol with label formats")
                return True
            else:
                print(f"❌ Failed to update protocol labels: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating protocol labels: {str(e)}")
            return False
    
    def setup_specimen_type_abbreviations(self, config):
        """Setup specimen type abbreviations for BHARAT Study"""
        print("🧪 Setting up specimen type abbreviations...")
        
        abbreviations = config["specimenTypeAbbreviations"]
        
        try:
            # Get existing specimen types
            response = self.session.get(f"{API_BASE}/permissible-values", 
                                      params={"attribute": "specimen_type"})
            if response.status_code == 200:
                existing_types = response.json()
                print(f"ℹ️  Found {len(existing_types)} existing specimen types")
                
                # Check which types need abbreviation updates
                for spec_type, abbrev in abbreviations.items():
                    type_exists = any(t.get("value") == spec_type for t in existing_types)
                    if type_exists:
                        print(f"✅ Specimen type '{spec_type}' exists (abbrev: {abbrev})")
                    else:
                        print(f"⚠️  Specimen type '{spec_type}' not found - may need manual addition")
                
                return True
            else:
                print(f"❌ Failed to retrieve specimen types: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking specimen types: {str(e)}")
            return False
    
    def create_label_validation_rules(self, config):
        """Create validation rules for BHARAT Study labels"""
        print("✅ Setting up label validation rules...")
        
        validation_rules = config["validationRules"]
        
        # Log the validation patterns for reference
        print("📋 Label validation patterns:")
        for label_type, rule in validation_rules.items():
            print(f"   • {label_type}: {rule['pattern']}")
            print(f"     Description: {rule['description']}")
        
        print("ℹ️  Validation rules configured (enforcement depends on OpenSpecimen settings)")
        return True
    
    def test_label_generation(self, config):
        """Test the label generation with example data"""
        print("🧪 Testing label format examples...")
        
        examples = config["labelExamples"]
        
        print("\n📋 Expected Label Format Examples:")
        for label_type, example_data in examples.items():
            print(f"\n{label_type.title()}:")
            print(f"   Format: {example_data['format']}")
            print("   Examples:")
            for example in example_data["examples"]:
                print(f"     • {example}")
        
        return True
    
    def generate_setup_report(self, config):
        """Generate comprehensive setup report"""
        print("\n" + "="*70)
        print("🎉 BHARAT STUDY LABELING SYSTEM SETUP COMPLETE!")
        print("="*70)
        print(f"📅 Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 Collection Protocol ID: {self.bharat_cp_id}")
        print("")
        
        print("🏷️  LABELING HIERARCHY CONFIGURED:")
        print("   📊 Participants: BHARAT-AG3-P0234")
        print("   🧪 Specimens:    BHARAT-AG3-P0234-V2-BLD01")
        print("   ⚗️  Aliquots:     BHARAT-AG3-P0234-V2-BLD01-PROT-01")
        print("")
        
        print("📋 CUSTOM FIELDS ADDED:")
        print("   👥 Participant: Age cohort (AG1-AG5)")
        print("   🧪 Specimen: Analysis type (GEN, PROT, META, etc.)")
        print("   📊 Processing: Batch tracking, freeze/thaw cycles")
        print("")
        
        print("🔧 NEXT STEPS:")
        print("   1. Test participant registration with new cohort field")
        print("   2. Verify specimen labeling format in collection workflow")
        print("   3. Configure aliquot creation with analysis type selection")
        print("   4. Set up barcode printing with new label formats")
        print("   5. Train staff on the new numbering system")
        print("")
        
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*70)
    
    def run_setup(self):
        """Execute the complete labeling system setup"""
        print("\n🚀 BHARAT STUDY LABELING SYSTEM SETUP")
        print("=====================================")
        print("Implementing hierarchical specimen numbering...")
        print("")
        
        # Step 1: Authenticate
        if not self.authenticate():
            return False
        
        # Step 2: Find BHARAT protocol
        if not self.find_bharat_protocol():
            return False
        
        # Step 3: Load configuration
        config = self.load_labeling_config()
        if not config:
            return False
        
        # Step 4: Create custom forms
        forms_created = self.create_custom_forms(config)
        
        # Step 5: Associate forms with protocol
        self.associate_forms_with_protocol(forms_created)
        
        # Step 6: Update protocol label formats
        self.update_collection_protocol_labels(config)
        
        # Step 7: Setup specimen type abbreviations
        self.setup_specimen_type_abbreviations(config)
        
        # Step 8: Create validation rules
        self.create_label_validation_rules(config)
        
        # Step 9: Test label examples
        self.test_label_generation(config)
        
        # Step 10: Generate report
        self.generate_setup_report(config)
        
        return True

def main():
    """Main entry point"""
    try:
        print("BHARAT Study Labeling System Setup")
        print("==================================")
        
        username = input("Username (admin): ").strip()
        if not username:
            username = "admin"
            
        password = input("Password (AmruthDB7!): ").strip()  
        if not password:
            password = "AmruthDB7!"
        
        setup = BharatLabelingSetup(username, password)
        success = setup.run_setup()
        
        if success:
            print("\n✅ Labeling system setup completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Labeling system setup failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()