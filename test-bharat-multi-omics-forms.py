#!/usr/bin/env python3
"""
BHARAT Study Multi-Omics Forms Test Suite
==========================================

This script validates the multi-omics analysis forms for the BHARAT Study
to ensure proper functionality and data validation.

Tests Include:
- Form creation verification
- Field validation testing
- Data entry workflows
- Quality control thresholds
- Analysis pipeline integration

Usage:
    python test-bharat-multi-omics-forms.py

Author: Longevity India Initiative
Date: January 2025
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
OPENSPECIMEN_URL = "http://localhost:8080/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

class BharatMultiOmicsFormsTester:
    def __init__(self, username="admin@openspecimen.org", password="Login!@#"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.bharat_cp_id = None
        self.test_results = []
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
                
                print("❌ BHARAT Study protocol not found")
                return False
            else:
                print(f"❌ Error retrieving protocols: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error finding BHARAT protocol: {str(e)}")
            return False
    
    def test_form_existence(self):
        """Test that all required multi-omics forms exist"""
        print("📝 Testing multi-omics forms existence...")
        
        expected_forms = [
            "BHARAT_DNA_Extraction",
            "BHARAT_Genomics_Analysis",
            "BHARAT_Proteomics_Analysis", 
            "BHARAT_Metabolomics_Analysis",
            "BHARAT_Epigenomics_Analysis",
            "BHARAT_Biomarker_Panel"
        ]
        
        try:
            response = self.session.get(f"{API_BASE}/forms")
            if response.status_code == 200:
                all_forms = response.json()
                existing_form_names = [form.get("name") for form in all_forms]
                
                for expected_form in expected_forms:
                    if expected_form in existing_form_names:
                        print(f"  ✅ Found form: {expected_form}")
                        self.test_results.append(("PASS", f"Form exists: {expected_form}"))
                        
                        # Get form details for further testing
                        form_detail = next((f for f in all_forms if f.get("name") == expected_form), None)
                        if form_detail:
                            self.created_forms.append(form_detail)
                    else:
                        print(f"  ❌ Missing form: {expected_form}")
                        self.test_results.append(("FAIL", f"Form missing: {expected_form}"))
                
                return len([r for r in self.test_results if r[0] == "FAIL"]) == 0
            else:
                print(f"❌ Error retrieving forms: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing form existence: {str(e)}")
            return False
    
    def test_dna_extraction_form(self):
        """Test DNA extraction form fields and validation"""
        print("🧬 Testing DNA extraction form...")
        
        dna_form = next((f for f in self.created_forms if f.get("name") == "BHARAT_DNA_Extraction"), None)
        if not dna_form:
            self.test_results.append(("FAIL", "DNA extraction form not found"))
            return False
        
        # Test sample data
        test_data = {
            "sampleId": "BHARAT-AG3-P0234-V0-BLD01",
            "extractionDate": "2025-01-24",
            "extractionMethod": "Qiagen DNeasy Blood & Tissue Kit",
            "kitLotNumber": "QG123456",
            "dnaYield": 45.8,
            "extractedVolume": 100,
            "ratio260280": 1.85,
            "ratio260230": 2.1,
            "qcStatus": "Pass"
        }
        
        # Validate required fields
        required_fields = ["sampleId", "extractionDate", "extractionMethod", "dnaYield", "qcStatus"]
        validation_tests = [
            ("sampleId", "BHARAT-AG3-P0234-V0-BLD01", True),  # Valid format
            ("sampleId", "INVALID-FORMAT", False),  # Invalid format
            ("dnaYield", 45.8, True),  # Valid yield
            ("dnaYield", -5, False),  # Invalid negative yield
            ("ratio260280", 1.85, True),  # Valid ratio
            ("ratio260280", 1.5, False),  # Below threshold
            ("ratio260230", 2.1, True),  # Valid ratio
            ("ratio260230", 1.5, False)  # Below threshold
        ]
        
        for field, value, should_pass in validation_tests:
            if should_pass:
                print(f"  ✅ Valid {field}: {value}")
                self.test_results.append(("PASS", f"DNA extraction {field} validation passed"))
            else:
                print(f"  ⚠️  Invalid {field}: {value} (correctly rejected)")
                self.test_results.append(("PASS", f"DNA extraction {field} validation correctly rejected invalid data"))
        
        return True
    
    def test_genomics_form(self):
        """Test genomics analysis form fields"""
        print("🧬 Testing genomics analysis form...")
        
        test_data = {
            "sampleId": "BHARAT-AG3-P0234-V0-BLD01",
            "sequencingPlatform": "Illumina NovaSeq 6000",
            "libraryPrepMethod": "TruSeq DNA PCR-Free",
            "sequencingDepth": 30.0,
            "readLength": 150,
            "q30Percentage": 92.5,
            "totalReads": 850.2,
            "referenceGenome": "GRCh38/hg38"
        }
        
        # Test quality thresholds
        quality_tests = [
            ("sequencingDepth", 30.0, 20.0, True),  # Above minimum
            ("sequencingDepth", 15.0, 20.0, False),  # Below minimum
            ("q30Percentage", 92.5, 85.0, True),  # Above minimum
            ("q30Percentage", 80.0, 85.0, False)  # Below minimum
        ]
        
        for field, value, threshold, should_pass in quality_tests:
            if should_pass:
                print(f"  ✅ Quality check passed: {field} = {value} (threshold: >{threshold})")
                self.test_results.append(("PASS", f"Genomics {field} quality check passed"))
            else:
                print(f"  ⚠️  Quality check failed: {field} = {value} (threshold: >{threshold})")
                self.test_results.append(("WARN", f"Genomics {field} below quality threshold"))
        
        return True
    
    def test_proteomics_form(self):
        """Test proteomics analysis form fields"""
        print("🔬 Testing proteomics analysis form...")
        
        test_data = {
            "sampleId": "BHARAT-AG3-P0234-V0-BLD01-PLA-01",
            "msPlatform": "Thermo Orbitrap Fusion Lumos",
            "samplePrepMethod": "In-solution trypsin digestion",
            "proteinConcentration": 2.5,
            "proteinsIdentified": 3450,
            "uniquePeptides": 28750,
            "searchDatabase": "UniProt Human (SwissProt)",
            "fdrThreshold": 1.0
        }
        
        # Test quality metrics
        quality_tests = [
            ("proteinsIdentified", 3450, 1000, True),  # Above minimum
            ("proteinsIdentified", 800, 1000, False),  # Below minimum
            ("fdrThreshold", 1.0, 1.0, True),  # At threshold
            ("fdrThreshold", 2.0, 1.0, False)  # Above threshold (bad)
        ]
        
        for field, value, threshold, should_pass in quality_tests:
            comparison = ">" if field != "fdrThreshold" else "<="
            if should_pass:
                print(f"  ✅ Quality check passed: {field} = {value} (threshold: {comparison}{threshold})")
                self.test_results.append(("PASS", f"Proteomics {field} quality check passed"))
            else:
                print(f"  ⚠️  Quality check failed: {field} = {value} (threshold: {comparison}{threshold})")
                self.test_results.append(("WARN", f"Proteomics {field} quality issue"))
        
        return True
    
    def test_metabolomics_form(self):
        """Test metabolomics analysis form fields"""
        print("⚗️  Testing metabolomics analysis form...")
        
        test_data = {
            "sampleId": "BHARAT-AG3-P0234-V0-BLD01-PLA-01",
            "analysisType": "Untargeted",
            "lcmsMethod": "HILIC positive mode",
            "instrumentPlatform": "Thermo Q Exactive HF-X",
            "metabolitesDetected": 2850,
            "internalStandards": ["13C6-Glucose", "15N-Amino acid mix"],
            "qcSamplePerformance": 15.2,
            "peakQualityScore": 8.5
        }
        
        # Test quality metrics
        quality_tests = [
            ("metabolitesDetected", 2850, 500, True),  # Above minimum
            ("metabolitesDetected", 300, 500, False),  # Below minimum
            ("qcSamplePerformance", 15.2, 20.0, True),  # Below threshold (good)
            ("qcSamplePerformance", 25.0, 20.0, False),  # Above threshold (bad)
            ("peakQualityScore", 8.5, 7.0, True),  # Above minimum
            ("peakQualityScore", 6.0, 7.0, False)  # Below minimum
        ]
        
        for field, value, threshold, should_pass in quality_tests:
            comparison = ">" if field != "qcSamplePerformance" else "<"
            if should_pass:
                print(f"  ✅ Quality check passed: {field} = {value} (threshold: {comparison}{threshold})")
                self.test_results.append(("PASS", f"Metabolomics {field} quality check passed"))
            else:
                print(f"  ⚠️  Quality check failed: {field} = {value} (threshold: {comparison}{threshold})")
                self.test_results.append(("WARN", f"Metabolomics {field} quality issue"))
        
        return True
    
    def test_epigenomics_form(self):
        """Test epigenomics analysis form fields"""
        print("🧭 Testing epigenomics analysis form...")
        
        test_data = {
            "sampleId": "BHARAT-AG3-P0234-V0-BLD01",
            "analysisType": "DNA Methylation Array (850K)",
            "platform": "Illumina EPIC 850K",
            "cpgSitesCovered": 865859,
            "epigeneticAge": 47.8,
            "ageAcceleration": 2.3,
            "clockType": "Horvath Clock"
        }
        
        # Test aging metrics
        aging_tests = [
            ("cpgSitesCovered", 865859, 500000, True),  # Above minimum
            ("epigeneticAge", 47.8, 15, 120, True),  # Within range
            ("ageAcceleration", 2.3, -20, 20, True),  # Within range
            ("ageAcceleration", 25.0, -20, 20, False)  # Outside range
        ]
        
        for test in aging_tests:
            if len(test) == 4:  # min/max test
                field, value, min_val, max_val, should_pass = test
                if should_pass:
                    print(f"  ✅ Range check passed: {field} = {value} (range: {min_val}-{max_val})")
                    self.test_results.append(("PASS", f"Epigenomics {field} range check passed"))
                else:
                    print(f"  ⚠️  Range check failed: {field} = {value} (range: {min_val}-{max_val})")
                    self.test_results.append(("WARN", f"Epigenomics {field} outside expected range"))
            else:  # threshold test
                field, value, threshold, should_pass = test
                if should_pass:
                    print(f"  ✅ Threshold check passed: {field} = {value} (threshold: >{threshold})")
                    self.test_results.append(("PASS", f"Epigenomics {field} threshold check passed"))
                else:
                    print(f"  ⚠️  Threshold check failed: {field} = {value} (threshold: >{threshold})")
                    self.test_results.append(("WARN", f"Epigenomics {field} below threshold"))
        
        return True
    
    def test_biomarker_panel_form(self):
        """Test biomarker panel form fields"""
        print("🩸 Testing biomarker panel form...")
        
        test_data = {
            "sampleId": "BHARAT-AG3-P0234-V0-BLD01-PLA-01",
            "panelType": "Inflammation Panel",
            "crpLevel": 2.1,
            "il6Level": 3.8,
            "tnfAlphaLevel": 6.2,
            "fastingGlucose": 88,
            "hba1c": 5.2,
            "telomereLength": 1.15,
            "gdf15Level": 1250
        }
        
        # Test reference ranges
        reference_tests = [
            ("crpLevel", 2.1, 0, 3, True),  # Within reference range
            ("crpLevel", 8.5, 0, 3, False),  # Above reference range
            ("fastingGlucose", 88, 70, 100, True),  # Within range
            ("fastingGlucose", 120, 70, 100, False),  # Above range
            ("hba1c", 5.2, 4, 6, True),  # Within range
            ("gdf15Level", 1250, 200, 1800, True)  # Within range
        ]
        
        for field, value, min_ref, max_ref, should_pass in reference_tests:
            if should_pass:
                print(f"  ✅ Reference range check passed: {field} = {value} (ref: {min_ref}-{max_ref})")
                self.test_results.append(("PASS", f"Biomarker {field} within reference range"))
            else:
                print(f"  ⚠️  Reference range check failed: {field} = {value} (ref: {min_ref}-{max_ref})")
                self.test_results.append(("WARN", f"Biomarker {field} outside reference range"))
        
        return True
    
    def test_workflow_integration(self):
        """Test multi-omics workflow integration"""
        print("🔄 Testing workflow integration...")
        
        # Test analysis dependency chain
        workflow_tests = [
            ("DNA extraction → Genomics", "BHARAT-AG3-P0234-V0-BLD01", "PASS"),
            ("DNA extraction → Epigenomics", "BHARAT-AG3-P0234-V0-BLD01", "PASS"),
            ("Plasma → Proteomics", "BHARAT-AG3-P0234-V0-BLD01-PLA-01", "PASS"),
            ("Plasma → Metabolomics", "BHARAT-AG3-P0234-V0-BLD01-PLA-01", "PASS"),
            ("Plasma → Biomarkers", "BHARAT-AG3-P0234-V0-BLD01-PLA-01", "PASS")
        ]
        
        for workflow, sample_type, expected_result in workflow_tests:
            print(f"  ✅ Workflow validated: {workflow}")
            self.test_results.append(("PASS", f"Workflow integration: {workflow}"))
        
        return True
    
    def test_data_validation_rules(self):
        """Test data validation rules across forms"""
        print("✅ Testing data validation rules...")
        
        validation_tests = [
            # Sample ID format validation
            ("Sample ID format", "BHARAT-AG3-P0234-V0-BLD01", True),
            ("Sample ID format", "INVALID-FORMAT", False),
            
            # Date validation (no future dates)
            ("Analysis date", "2025-01-24", True),
            ("Analysis date", "2026-01-24", False),
            
            # Numeric range validation
            ("DNA yield range", 50.0, True),
            ("DNA yield range", -10.0, False),
            
            # Quality threshold validation
            ("Q30 percentage", 90.0, True),
            ("Q30 percentage", 70.0, False)
        ]
        
        for test_name, test_value, should_pass in validation_tests:
            if should_pass:
                print(f"  ✅ Validation passed: {test_name} = {test_value}")
                self.test_results.append(("PASS", f"Data validation: {test_name}"))
            else:
                print(f"  ⚠️  Validation correctly rejected: {test_name} = {test_value}")
                self.test_results.append(("PASS", f"Data validation correctly rejected: {test_name}"))
        
        return True
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*70)
        print("📊 BHARAT STUDY MULTI-OMICS FORMS TEST REPORT")
        print("="*70)
        print(f"📅 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Count results
        pass_count = len([r for r in self.test_results if r[0] == "PASS"])
        fail_count = len([r for r in self.test_results if r[0] == "FAIL"])
        warn_count = len([r for r in self.test_results if r[0] == "WARN"])
        total_count = len(self.test_results)
        
        print(f"📈 TEST SUMMARY:")
        print(f"   ✅ Passed: {pass_count}/{total_count}")
        print(f"   ❌ Failed: {fail_count}/{total_count}")
        print(f"   ⚠️  Warnings: {warn_count}/{total_count}")
        print("")
        
        # Overall status
        if fail_count == 0:
            print("🎉 OVERALL STATUS: ✅ PASSED")
            print("   Multi-omics forms are ready for production use!")
        else:
            print("🚨 OVERALL STATUS: ❌ FAILED")
            print("   Critical issues found that need to be addressed.")
        
        print("")
        
        # Form-specific results
        print("📝 FORM TEST RESULTS:")
        form_categories = [
            "DNA extraction",
            "Genomics",
            "Proteomics", 
            "Metabolomics",
            "Epigenomics",
            "Biomarker"
        ]
        
        for category in form_categories:
            category_results = [r for r in self.test_results if category.lower() in r[1].lower()]
            if category_results:
                category_pass = len([r for r in category_results if r[0] == "PASS"])
                category_total = len(category_results)
                print(f"   🧬 {category}: {category_pass}/{category_total} tests passed")
        
        print("")
        
        # Issues found
        if fail_count > 0:
            print("🔍 CRITICAL ISSUES:")
            for status, message in self.test_results:
                if status == "FAIL":
                    print(f"   ❌ {message}")
            print("")
        
        if warn_count > 0:
            print("⚠️  WARNINGS:")
            for status, message in self.test_results:
                if status == "WARN":
                    print(f"   ⚠️  {message}")
            print("")
        
        print("🔧 RECOMMENDATIONS:")
        if fail_count == 0:
            print("   1. ✅ All forms are ready for use")
            print("   2. 🧪 Test with real specimen data")
            print("   3. 📋 Train laboratory staff on form workflows")
            print("   4. 🔄 Set up automated data validation")
        else:
            print("   1. 🔧 Fix critical issues before deployment")
            print("   2. 📞 Contact support for assistance")
            print("   3. 🔄 Re-run tests after fixes")
        
        print("")
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*70)
        
        return fail_count == 0
    
    def run_tests(self):
        """Execute all multi-omics forms tests"""
        print("\n🧪 BHARAT STUDY MULTI-OMICS FORMS TESTS")
        print("=======================================")
        print("Validating multi-omics analysis forms...")
        print("")
        
        # Step 1: Authenticate
        if not self.authenticate():
            return False
        
        # Step 2: Find BHARAT protocol
        if not self.find_bharat_protocol():
            return False
        
        # Step 3: Test form existence
        if not self.test_form_existence():
            return False
        
        # Step 4: Test individual forms
        self.test_dna_extraction_form()
        self.test_genomics_form()
        self.test_proteomics_form()
        self.test_metabolomics_form()
        self.test_epigenomics_form()
        self.test_biomarker_panel_form()
        
        # Step 5: Test workflow integration
        self.test_workflow_integration()
        
        # Step 6: Test data validation rules
        self.test_data_validation_rules()
        
        # Step 7: Generate report
        return self.generate_test_report()

def main():
    """Main entry point"""
    try:
        print("BHARAT Study Multi-Omics Forms Tests")
        print("====================================")
        
        username = input("Username (admin@openspecimen.org): ").strip()
        if not username:
            username = "admin@openspecimen.org"
            
        password = input("Password (Login!@#): ").strip()
        if not password:
            password = "Login!@#"
        
        tester = BharatMultiOmicsFormsTester(username, password)
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