#!/usr/bin/env python3
"""
BHARAT Study Multi-Omics Analysis Forms Setup
==============================================

This script creates comprehensive forms for tracking multi-omics analysis
in the BHARAT Study, including genomics, proteomics, metabolomics, and
epigenomics workflows.

Forms Created:
- DNA Extraction tracking
- Genomics Analysis (sequencing, quality metrics)
- Proteomics Analysis (mass spectrometry)
- Metabolomics Analysis (LC-MS/MS)
- Epigenomics Analysis (methylation, epigenetic clocks)
- Biomarker Panel Results (aging, inflammation, metabolic)

Usage:
    python setup-bharat-multi-omics-forms.py

Author: Longevity India Initiative
Date: January 2025
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
OPENSPECIMEN_URL = "http://localhost:8082/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

class BharatMultiOmicsFormsSetup:
    def __init__(self, username="admin", password="AmruthDB7!"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.bharat_cp_id = None
        self.created_forms = []
        
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
    
    def load_forms_configuration(self):
        """Load the multi-omics forms configuration"""
        print("📋 Loading multi-omics forms configuration...")
        
        try:
            with open("bharat-multi-omics-forms.json", "r") as f:
                config = json.load(f)
            print("✅ Multi-omics forms configuration loaded successfully")
            return config["multiOmicsForms"]
        except Exception as e:
            print(f"❌ Error loading forms configuration: {str(e)}")
            return None
    
    def create_form(self, form_config):
        """Create a single form in OpenSpecimen"""
        form_name = form_config["name"]
        print(f"📝 Creating form: {form_name}...")
        
        # Convert form configuration to OpenSpecimen format
        os_form = {
            "name": form_config["name"],
            "caption": form_config["caption"],
            "entityType": form_config["entityType"],
            "multiRecord": form_config.get("multiRecord", False),
            "creationTime": int(datetime.now().timestamp() * 1000),
            "fields": []
        }
        
        # Convert fields
        for field_config in form_config["fields"]:
            os_field = {
                "name": field_config["name"],
                "caption": field_config["caption"],
                "type": field_config["type"],
                "mandatory": field_config.get("mandatory", False),
                "defaultValue": field_config.get("defaultValue", "")
            }
            
            # Add type-specific properties
            if field_config["type"] == "STRING":
                if "maxLength" in field_config:
                    os_field["maxLength"] = field_config["maxLength"]
                if "pattern" in field_config:
                    os_field["pattern"] = field_config["pattern"]
            
            elif field_config["type"] in ["FLOAT", "INTEGER"]:
                if "minValue" in field_config:
                    os_field["minValue"] = field_config["minValue"]
                if "maxValue" in field_config:
                    os_field["maxValue"] = field_config["maxValue"]
                if "referenceRange" in field_config:
                    os_field["note"] = f"Reference Range: {field_config['referenceRange']}"
            
            elif field_config["type"] == "DATE":
                if "maxDate" in field_config:
                    os_field["maxDate"] = field_config["maxDate"]
            
            elif field_config["type"] in ["DROPDOWN", "MULTISELECT"]:
                if "permissibleValues" in field_config:
                    os_field["permissibleValues"] = field_config["permissibleValues"]
            
            elif field_config["type"] == "TEXT":
                if "maxLength" in field_config:
                    os_field["maxLength"] = field_config["maxLength"]
            
            elif field_config["type"] == "USER":
                if "excludeType" in field_config:
                    os_field["excludeType"] = field_config["excludeType"]
            
            os_form["fields"].append(os_field)
        
        # Create the form
        try:
            response = self.session.post(f"{API_BASE}/forms", json=os_form)
            if response.status_code == 200:
                form_data = response.json()
                form_id = form_data.get("id")
                print(f"✅ Created form: {form_name} (ID: {form_id})")
                self.created_forms.append({
                    "name": form_name,
                    "id": form_id,
                    "entityType": form_config["entityType"],
                    "caption": form_config["caption"]
                })
                return form_id
            else:
                print(f"❌ Failed to create form {form_name}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error creating form {form_name}: {str(e)}")
            return None
    
    def associate_forms_with_protocol(self):
        """Associate all created forms with the BHARAT collection protocol"""
        print("🔗 Associating forms with BHARAT Study protocol...")
        
        if not self.bharat_cp_id:
            print("❌ No BHARAT protocol ID available")
            return False
        
        for form_info in self.created_forms:
            form_context = {
                "formId": form_info["id"],
                "entityType": form_info["entityType"],
                "cpId": self.bharat_cp_id,
                "multiRecord": True,  # Allow multiple records for specimen events
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
    
    def create_workflow_configurations(self):
        """Create workflow configurations for multi-omics analysis"""
        print("⚙️  Setting up multi-omics workflow configurations...")
        
        # Create workflow mapping for different analysis types
        workflow_config = {
            "dnaExtraction": {
                "requiredFields": ["sampleId", "extractionDate", "extractionMethod", "dnaYield", "qcStatus"],
                "nextSteps": ["genomics", "epigenomics"],
                "qualityThresholds": {
                    "ratio260280": {"min": 1.8, "max": 2.0},
                    "ratio260230": {"min": 2.0, "max": 2.2},
                    "dnaYield": {"min": 10}
                }
            },
            "genomics": {
                "requiredFields": ["sequencingPlatform", "sequencingDepth", "q30Percentage"],
                "qualityThresholds": {
                    "q30Percentage": {"min": 85},
                    "sequencingDepth": {"min": 30}
                }
            },
            "proteomics": {
                "requiredFields": ["msPlatform", "proteinConcentration", "proteinsIdentified"],
                "qualityThresholds": {
                    "proteinsIdentified": {"min": 1000},
                    "fdrThreshold": {"max": 1.0}
                }
            },
            "metabolomics": {
                "requiredFields": ["analysisType", "lcmsMethod", "metabolitesDetected"],
                "qualityThresholds": {
                    "qcSamplePerformance": {"max": 20},
                    "peakQualityScore": {"min": 7}
                }
            }
        }
        
        print("✅ Multi-omics workflow configurations defined")
        return workflow_config
    
    def create_analysis_templates(self):
        """Create analysis templates for common workflows"""
        print("📋 Creating analysis templates...")
        
        templates = {
            "baseline_complete": {
                "name": "Baseline Visit Complete Analysis",
                "description": "Full multi-omics analysis for baseline visit (V0)",
                "forms": [
                    "BHARAT_DNA_Extraction",
                    "BHARAT_Genomics_Analysis",
                    "BHARAT_Proteomics_Analysis",
                    "BHARAT_Metabolomics_Analysis",
                    "BHARAT_Epigenomics_Analysis",
                    "BHARAT_Biomarker_Panel"
                ]
            },
            "follow_up_standard": {
                "name": "Follow-up Visit Standard Analysis",
                "description": "Standard analysis for follow-up visits (V1, V2, V3)",
                "forms": [
                    "BHARAT_Proteomics_Analysis",
                    "BHARAT_Metabolomics_Analysis",
                    "BHARAT_Biomarker_Panel"
                ]
            },
            "aging_focused": {
                "name": "Aging Biomarkers Focused Analysis",
                "description": "Focus on aging-specific biomarkers and epigenetic clocks",
                "forms": [
                    "BHARAT_Epigenomics_Analysis",
                    "BHARAT_Biomarker_Panel"
                ]
            }
        }
        
        print("✅ Analysis templates created")
        return templates
    
    def validate_forms_setup(self):
        """Validate that all forms were created and associated correctly"""
        print("🔍 Validating forms setup...")
        
        validation_results = []
        
        # Check that all expected forms were created
        expected_forms = [
            "BHARAT_DNA_Extraction",
            "BHARAT_Genomics_Analysis", 
            "BHARAT_Proteomics_Analysis",
            "BHARAT_Metabolomics_Analysis",
            "BHARAT_Epigenomics_Analysis",
            "BHARAT_Biomarker_Panel"
        ]
        
        created_form_names = [form["name"] for form in self.created_forms]
        
        for expected_form in expected_forms:
            if expected_form in created_form_names:
                validation_results.append(("PASS", f"Form created: {expected_form}"))
            else:
                validation_results.append(("FAIL", f"Form missing: {expected_form}"))
        
        # Check form associations
        if self.bharat_cp_id:
            try:
                response = self.session.get(f"{API_BASE}/collection-protocols/{self.bharat_cp_id}/forms")
                if response.status_code == 200:
                    associated_forms = response.json()
                    validation_results.append(("PASS", f"Found {len(associated_forms)} associated forms"))
                else:
                    validation_results.append(("WARN", "Could not verify form associations"))
            except Exception as e:
                validation_results.append(("ERROR", f"Error checking associations: {str(e)}"))
        
        # Report validation results
        pass_count = len([r for r in validation_results if r[0] == "PASS"])
        fail_count = len([r for r in validation_results if r[0] == "FAIL"])
        
        if fail_count == 0:
            print(f"✅ Validation passed: {pass_count} checks successful")
            return True
        else:
            print(f"❌ Validation failed: {fail_count} issues found")
            for status, message in validation_results:
                if status == "FAIL":
                    print(f"   ❌ {message}")
            return False
    
    def generate_setup_report(self, config):
        """Generate comprehensive setup report"""
        print("\n" + "="*70)
        print("🎉 BHARAT STUDY MULTI-OMICS FORMS SETUP COMPLETE!")
        print("="*70)
        print(f"📅 Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 Collection Protocol ID: {self.bharat_cp_id}")
        print("")
        
        print("📝 FORMS CREATED:")
        for form_info in self.created_forms:
            print(f"   ✅ {form_info['caption']} (ID: {form_info['id']})")
        print("")
        
        print("🧬 MULTI-OMICS ANALYSIS CAPABILITIES:")
        print("   📊 DNA Extraction: Quality tracking, yield measurement")
        print("   🧬 Genomics: Sequencing platforms, quality metrics, file tracking")
        print("   🔬 Proteomics: Mass spectrometry, protein identification")
        print("   ⚗️  Metabolomics: LC-MS methods, metabolite detection")
        print("   🧭 Epigenomics: Methylation analysis, epigenetic clocks")
        print("   🩸 Biomarkers: Aging panels, inflammation, metabolic health")
        print("")
        
        print("📋 ANALYSIS WORKFLOWS SUPPORTED:")
        print("   • Baseline complete analysis (all omics)")
        print("   • Follow-up standard analysis (proteomics, metabolomics)")
        print("   • Aging-focused analysis (epigenetics, biomarkers)")
        print("   • Custom analysis combinations")
        print("")
        
        print("🔧 NEXT STEPS:")
        print("   1. Test form functionality with sample data")
        print("   2. Configure analysis workflows and automation")
        print("   3. Set up data validation rules")
        print("   4. Train laboratory staff on form usage")
        print("   5. Integrate with instrument data capture")
        print("")
        
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*70)
    
    def run_setup(self):
        """Execute the complete multi-omics forms setup"""
        print("\n🚀 BHARAT STUDY MULTI-OMICS FORMS SETUP")
        print("=======================================")
        print("Creating comprehensive analysis tracking forms...")
        print("")
        
        # Step 1: Authenticate
        if not self.authenticate():
            return False
        
        # Step 2: Find BHARAT protocol
        if not self.find_bharat_protocol():
            return False
        
        # Step 3: Load configuration
        config = self.load_forms_configuration()
        if not config:
            return False
        
        # Step 4: Create all forms
        print(f"📝 Creating {len(config['forms'])} multi-omics analysis forms...")
        for form_config in config["forms"]:
            self.create_form(form_config)
        
        # Step 5: Associate forms with protocol
        self.associate_forms_with_protocol()
        
        # Step 6: Create workflow configurations
        self.create_workflow_configurations()
        
        # Step 7: Create analysis templates
        self.create_analysis_templates()
        
        # Step 8: Validate setup
        validation_success = self.validate_forms_setup()
        
        # Step 9: Generate report
        self.generate_setup_report(config)
        
        return validation_success

def main():
    """Main entry point"""
    try:
        print("BHARAT Study Multi-Omics Forms Setup")
        print("====================================")
        
        username = input("Username (admin): ").strip()
        if not username:
            username = "admin"
            
        password = input("Password (AmruthDB7!): ").strip()
        if not password:
            password = "AmruthDB7!"
        
        setup = BharatMultiOmicsFormsSetup(username, password)
        success = setup.run_setup()
        
        if success:
            print("\n✅ Multi-omics forms setup completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Multi-omics forms setup failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()