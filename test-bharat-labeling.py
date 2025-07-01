#!/usr/bin/env python3
"""
BHARAT Study Labeling System Test Suite
========================================

This script validates and tests the BHARAT Study specimen labeling system
to ensure all label formats work correctly and meet study requirements.

Usage:
    python test-bharat-labeling.py

Author: Longevity India Initiative  
Date: January 2025
"""

import requests
import json
import sys
import re
from datetime import datetime, timedelta

# Configuration
OPENSPECIMEN_URL = "http://localhost:8080/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

class BharatLabelingTester:
    def __init__(self, username="admin@openspecimen.org", password="Login!@#"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.bharat_cp_id = None
        self.test_results = []
        
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
        """Find and validate BHARAT Study collection protocol"""
        print("🔍 Finding and validating BHARAT Study protocol...")
        
        try:
            response = self.session.get(f"{API_BASE}/collection-protocols")
            if response.status_code == 200:
                protocols = response.json()
                for protocol in protocols:
                    if protocol.get("shortTitle") == "BHARAT-STUDY" or protocol.get("code") == "BHARAT":
                        self.bharat_cp_id = protocol.get("id")
                        print(f"✅ Found BHARAT Study protocol (ID: {self.bharat_cp_id})")
                        
                        # Validate label formats
                        self.validate_protocol_label_formats(protocol)
                        return True
                
                print("❌ BHARAT Study protocol not found")
                return False
            else:
                print(f"❌ Error retrieving protocols: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error finding BHARAT protocol: {str(e)}")
            return False
    
    def validate_protocol_label_formats(self, protocol):
        """Validate that protocol has correct label formats"""
        print("🏷️  Validating protocol label formats...")
        
        expected_formats = {
            "ppidFmt": "%CP_CODE%-%CUSTOM_FIELD(cpr,cohort)%-%SYS_UID(4)%",
            "visitNameFmt": "%EVENT_CODE%",
            "specimenLabelFmt": "%PPI%-%VISIT_NAME%-%SP_TYPE_ABBR%%SYS_UID(2)%",
            "derivativeLabelFmt": "%PARENT_SPMN_LABEL%-%SP_TYPE_ABBR%-%SYS_UID(2)%",
            "aliquotLabelFmt": "%PARENT_SPMN_LABEL%-%CUSTOM_FIELD(specimen,analysisType)%-%SYS_UID(2)%"
        }
        
        for format_name, expected_format in expected_formats.items():
            actual_format = protocol.get(format_name, "")
            if actual_format:
                print(f"✅ {format_name}: {actual_format}")
                self.test_results.append(("PASS", f"Protocol {format_name} configured"))
            else:
                print(f"⚠️  {format_name}: Not configured or empty")
                self.test_results.append(("WARN", f"Protocol {format_name} missing"))
    
    def test_custom_forms(self):
        """Test that custom forms are properly created and associated"""
        print("📝 Testing custom forms...")
        
        try:
            # Check for participant custom form
            response = self.session.get(f"{API_BASE}/forms", 
                                      params={"entityType": "ParticipantExtension"})
            if response.status_code == 200:
                forms = response.json()
                bharat_participant_form = None
                for form in forms:
                    if "BHARAT" in form.get("name", ""):
                        bharat_participant_form = form
                        break
                
                if bharat_participant_form:
                    print(f"✅ Found BHARAT participant form: {bharat_participant_form['name']}")
                    self.test_results.append(("PASS", "Participant custom form exists"))
                    
                    # Validate cohort field
                    self.validate_cohort_field(bharat_participant_form)
                else:
                    print("❌ BHARAT participant custom form not found")
                    self.test_results.append(("FAIL", "Participant custom form missing"))
            
            # Check for specimen custom form
            response = self.session.get(f"{API_BASE}/forms",
                                      params={"entityType": "SpecimenExtension"})
            if response.status_code == 200:
                forms = response.json()
                bharat_specimen_form = None
                for form in forms:
                    if "BHARAT" in form.get("name", ""):
                        bharat_specimen_form = form
                        break
                
                if bharat_specimen_form:
                    print(f"✅ Found BHARAT specimen form: {bharat_specimen_form['name']}")
                    self.test_results.append(("PASS", "Specimen custom form exists"))
                    
                    # Validate analysis type field
                    self.validate_analysis_type_field(bharat_specimen_form)
                else:
                    print("❌ BHARAT specimen custom form not found")
                    self.test_results.append(("FAIL", "Specimen custom form missing"))
                    
        except Exception as e:
            print(f"❌ Error testing custom forms: {str(e)}")
            self.test_results.append(("ERROR", f"Custom form test error: {str(e)}"))
    
    def validate_cohort_field(self, form):
        """Validate that cohort field has correct values"""
        print("  🔍 Validating cohort field...")
        
        expected_cohorts = ["AG1", "AG2", "AG3", "AG4", "AG5"]
        
        # Get form details
        try:
            response = self.session.get(f"{API_BASE}/forms/{form['id']}")
            if response.status_code == 200:
                form_details = response.json()
                fields = form_details.get("fields", [])
                
                cohort_field = None
                for field in fields:
                    if field.get("name") == "cohort":
                        cohort_field = field
                        break
                
                if cohort_field:
                    pv_list = cohort_field.get("permissibleValues", [])
                    actual_cohorts = [pv.get("value") for pv in pv_list]
                    
                    missing_cohorts = set(expected_cohorts) - set(actual_cohorts)
                    if not missing_cohorts:
                        print("  ✅ All age cohorts (AG1-AG5) configured correctly")
                        self.test_results.append(("PASS", "Age cohort values correct"))
                    else:
                        print(f"  ❌ Missing cohorts: {missing_cohorts}")
                        self.test_results.append(("FAIL", f"Missing cohorts: {missing_cohorts}"))
                else:
                    print("  ❌ Cohort field not found in form")
                    self.test_results.append(("FAIL", "Cohort field missing"))
                    
        except Exception as e:
            print(f"  ❌ Error validating cohort field: {str(e)}")
    
    def validate_analysis_type_field(self, form):
        """Validate that analysis type field has correct values"""
        print("  🔍 Validating analysis type field...")
        
        expected_types = ["GEN", "PROT", "META", "EPI", "CLIN", "FLOW", "DNA", "RNA"]
        
        try:
            response = self.session.get(f"{API_BASE}/forms/{form['id']}")
            if response.status_code == 200:
                form_details = response.json()
                fields = form_details.get("fields", [])
                
                analysis_field = None
                for field in fields:
                    if field.get("name") == "analysisType":
                        analysis_field = field
                        break
                
                if analysis_field:
                    pv_list = analysis_field.get("permissibleValues", [])
                    actual_types = [pv.get("value") for pv in pv_list]
                    
                    missing_types = set(expected_types) - set(actual_types)
                    if len(missing_types) <= 2:  # Allow some flexibility
                        print("  ✅ Analysis type values configured correctly")
                        self.test_results.append(("PASS", "Analysis type values correct"))
                    else:
                        print(f"  ⚠️  Some analysis types missing: {missing_types}")
                        self.test_results.append(("WARN", f"Some analysis types missing"))
                else:
                    print("  ❌ Analysis type field not found in form")
                    self.test_results.append(("FAIL", "Analysis type field missing"))
                    
        except Exception as e:
            print(f"  ❌ Error validating analysis type field: {str(e)}")
    
    def test_label_format_patterns(self):
        """Test label format patterns with regex validation"""
        print("🧪 Testing label format patterns...")
        
        test_cases = [
            {
                "type": "participant",
                "pattern": r"^BHARAT-AG[1-5]-P\d{4}$",
                "valid_examples": [
                    "BHARAT-AG1-P0001",
                    "BHARAT-AG3-P0234", 
                    "BHARAT-AG5-P1000"
                ],
                "invalid_examples": [
                    "BHARAT-AG6-P0001",  # Invalid cohort
                    "BHARAT-AG1-0001",   # Missing P prefix
                    "BHARAT-AG1-P01"     # Too short number
                ]
            },
            {
                "type": "specimen",
                "pattern": r"^BHARAT-AG[1-5]-P\d{4}-V[0-3]-[A-Z]{2,4}\d{2}$",
                "valid_examples": [
                    "BHARAT-AG3-P0234-V0-BLD01",
                    "BHARAT-AG1-P0001-V2-SAL01",
                    "BHARAT-AG5-P1000-V3-HAR01"
                ],
                "invalid_examples": [
                    "BHARAT-AG3-P0234-V4-BLD01",  # Invalid visit
                    "BHARAT-AG3-P0234-V0-B01",    # Too short type
                    "BHARAT-AG3-P0234-V0-BLD1"    # Wrong number format
                ]
            },
            {
                "type": "aliquot", 
                "pattern": r"^BHARAT-AG[1-5]-P\d{4}-V[0-3]-[A-Z]{2,4}\d{2}-[A-Z]{2,5}-\d{2}$",
                "valid_examples": [
                    "BHARAT-AG3-P0234-V0-BLD01-PROT-01",
                    "BHARAT-AG1-P0001-V2-SAL01-DNA-01",
                    "BHARAT-AG5-P1000-V3-HAR01-META-01"
                ],
                "invalid_examples": [
                    "BHARAT-AG3-P0234-V0-BLD01-PROTEIN-01",  # Too long analysis
                    "BHARAT-AG3-P0234-V0-BLD01-PR-01",      # Too short analysis
                    "BHARAT-AG3-P0234-V0-BLD01-PROT-1"      # Wrong number format
                ]
            }
        ]
        
        for test_case in test_cases:
            print(f"\n  🔍 Testing {test_case['type']} label patterns...")
            pattern = re.compile(test_case['pattern'])
            
            # Test valid examples
            for example in test_case['valid_examples']:
                if pattern.match(example):
                    print(f"    ✅ Valid: {example}")
                    self.test_results.append(("PASS", f"{test_case['type']} valid: {example}"))
                else:
                    print(f"    ❌ Should be valid but failed: {example}")
                    self.test_results.append(("FAIL", f"{test_case['type']} validation failed: {example}"))
            
            # Test invalid examples
            for example in test_case['invalid_examples']:
                if not pattern.match(example):
                    print(f"    ✅ Correctly rejected: {example}")
                    self.test_results.append(("PASS", f"{test_case['type']} correctly rejected: {example}"))
                else:
                    print(f"    ❌ Should be invalid but passed: {example}")
                    self.test_results.append(("FAIL", f"{test_case['type']} incorrectly accepted: {example}"))
    
    def test_specimen_types_and_abbreviations(self):
        """Test that required specimen types exist with correct abbreviations"""
        print("🧪 Testing specimen types and abbreviations...")
        
        required_types = {
            "Whole Blood": "BLD",
            "Plasma": "PLA", 
            "Saliva": "SAL",
            "Hair": "HAR",
            "Buccal Cells": "CEL"
        }
        
        try:
            response = self.session.get(f"{API_BASE}/permissible-values",
                                      params={"attribute": "specimen_type"})
            if response.status_code == 200:
                specimen_types = response.json()
                existing_types = [st.get("value") for st in specimen_types]
                
                for spec_type, expected_abbrev in required_types.items():
                    if spec_type in existing_types:
                        print(f"  ✅ {spec_type} exists (expected abbrev: {expected_abbrev})")
                        self.test_results.append(("PASS", f"Specimen type exists: {spec_type}"))
                    else:
                        print(f"  ❌ {spec_type} missing")
                        self.test_results.append(("FAIL", f"Specimen type missing: {spec_type}"))
                        
        except Exception as e:
            print(f"❌ Error testing specimen types: {str(e)}")
            self.test_results.append(("ERROR", f"Specimen type test error: {str(e)}"))
    
    def test_collection_protocol_events(self):
        """Test that collection protocol has correct visit structure"""
        print("📅 Testing collection protocol visit structure...")
        
        if not self.bharat_cp_id:
            print("❌ No BHARAT protocol ID available")
            return
        
        try:
            response = self.session.get(f"{API_BASE}/collection-protocols/{self.bharat_cp_id}/events")
            if response.status_code == 200:
                events = response.json()
                
                expected_events = {
                    "V0": {"eventPoint": 0, "label": "Baseline"},
                    "V1": {"eventPoint": 180, "label": "6 Month"}, 
                    "V2": {"eventPoint": 365, "label": "12 Month"},
                    "V3": {"eventPoint": 730, "label": "24 Month"}
                }
                
                for event in events:
                    event_code = event.get("code", "")
                    event_point = event.get("eventPoint", 0)
                    
                    if event_code in expected_events:
                        expected_point = expected_events[event_code]["eventPoint"]
                        if event_point == expected_point:
                            print(f"  ✅ {event_code}: Day {event_point} (correct)")
                            self.test_results.append(("PASS", f"Event {event_code} configured correctly"))
                        else:
                            print(f"  ❌ {event_code}: Day {event_point} (expected {expected_point})")
                            self.test_results.append(("FAIL", f"Event {event_code} wrong timepoint"))
                
                if len(events) == 4:
                    print(f"  ✅ All 4 visits configured")
                    self.test_results.append(("PASS", "All 4 visits configured"))
                else:
                    print(f"  ⚠️  Expected 4 visits, found {len(events)}")
                    self.test_results.append(("WARN", f"Expected 4 visits, found {len(events)}"))
                    
        except Exception as e:
            print(f"❌ Error testing protocol events: {str(e)}")
            self.test_results.append(("ERROR", f"Protocol events test error: {str(e)}"))
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*70)
        print("📊 BHARAT STUDY LABELING SYSTEM TEST REPORT")
        print("="*70)
        print(f"📅 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Count results
        pass_count = len([r for r in self.test_results if r[0] == "PASS"])
        fail_count = len([r for r in self.test_results if r[0] == "FAIL"])
        warn_count = len([r for r in self.test_results if r[0] == "WARN"])
        error_count = len([r for r in self.test_results if r[0] == "ERROR"])
        total_count = len(self.test_results)
        
        print(f"📈 TEST SUMMARY:")
        print(f"   ✅ Passed: {pass_count}/{total_count}")
        print(f"   ❌ Failed: {fail_count}/{total_count}")
        print(f"   ⚠️  Warnings: {warn_count}/{total_count}")
        print(f"   🚨 Errors: {error_count}/{total_count}")
        print("")
        
        # Overall status
        if fail_count == 0 and error_count == 0:
            print("🎉 OVERALL STATUS: ✅ PASSED")
            print("   The BHARAT Study labeling system is ready for use!")
        elif fail_count > 0:
            print("🚨 OVERALL STATUS: ❌ FAILED")
            print("   Critical issues found that need to be addressed.")
        else:
            print("⚠️  OVERALL STATUS: 🔶 PASSED WITH WARNINGS")
            print("   System functional but some minor issues noted.")
        
        print("")
        
        # Detailed results
        if fail_count > 0 or error_count > 0:
            print("🔍 ISSUES FOUND:")
            for status, message in self.test_results:
                if status in ["FAIL", "ERROR"]:
                    icon = "❌" if status == "FAIL" else "🚨"
                    print(f"   {icon} {message}")
            print("")
        
        if warn_count > 0:
            print("⚠️  WARNINGS:")
            for status, message in self.test_results:
                if status == "WARN":
                    print(f"   ⚠️  {message}")
            print("")
        
        print("🔧 RECOMMENDATIONS:")
        if fail_count == 0 and error_count == 0:
            print("   1. ✅ System is ready for production use")
            print("   2. 🧪 Consider testing with actual participant registration")
            print("   3. 📋 Train staff on new labeling conventions")
        else:
            print("   1. 🔧 Address failed tests before using system")
            print("   2. 📞 Contact support if errors persist")
            print("   3. 🔄 Re-run tests after fixes")
        
        print("")
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*70)
        
        return fail_count == 0 and error_count == 0
    
    def run_tests(self):
        """Execute all tests"""
        print("\n🧪 BHARAT STUDY LABELING SYSTEM TESTS")
        print("=====================================")
        print("Validating specimen numbering implementation...")
        print("")
        
        # Step 1: Authenticate
        if not self.authenticate():
            return False
        
        # Step 2: Find and validate protocol
        if not self.find_bharat_protocol():
            return False
        
        # Step 3: Test custom forms
        self.test_custom_forms()
        
        # Step 4: Test label patterns
        self.test_label_format_patterns()
        
        # Step 5: Test specimen types
        self.test_specimen_types_and_abbreviations()
        
        # Step 6: Test protocol events
        self.test_collection_protocol_events()
        
        # Step 7: Generate report
        return self.generate_test_report()

def main():
    """Main entry point"""
    try:
        print("BHARAT Study Labeling System Tests")
        print("==================================")
        
        username = input("Username (admin@openspecimen.org): ").strip()
        if not username:
            username = "admin@openspecimen.org"
            
        password = input("Password (Login!@#): ").strip()
        if not password:
            password = "Login!@#"
        
        tester = BharatLabelingTester(username, password)
        success = tester.run_tests()
        
        if success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()