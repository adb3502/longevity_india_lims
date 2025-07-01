#!/usr/bin/env python3
"""
BHARAT Study Collection Protocol Setup Script
==================================================

This script sets up the BHARAT Study collection protocol in OpenSpecimen
using the REST API. It creates the complete longitudinal study framework
with 4 visits over 24 months and appropriate specimen collection requirements.

Usage:
    python setup-bharat-study-protocol.py

Requirements:
    - OpenSpecimen instance running and accessible
    - Valid admin credentials
    - Python 3.6+ with requests library
    
Author: Longevity India Initiative
Date: January 2025
"""

import requests
import json
import sys
import time
from datetime import datetime, timedelta

# Configuration
OPENSPECIMEN_URL = "http://localhost:8082/openspecimen"
API_BASE = f"{OPENSPECIMEN_URL}/rest/ng"

class BharatStudySetup:
    def __init__(self, username="admin", password="AmruthDB7!"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        
    def authenticate(self):
        """Authenticate with OpenSpecimen and get session token"""
        print("🔐 Authenticating with OpenSpecimen...")
        
        auth_data = {
            "loginName": self.username,
            "password": self.password,
            "domainName": "openspecimen"
        }
        
        try:
            response = self.session.post(
                f"{API_BASE}/sessions",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                session_data = response.json()
                self.auth_token = session_data.get("token")
                self.session.headers.update({
                    "X-OS-API-TOKEN": self.auth_token,
                    "Content-Type": "application/json"
                })
                print(f"✅ Authentication successful! Token: {self.auth_token[:20]}...")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def check_existing_protocol(self):
        """Check if BHARAT Study protocol already exists"""
        print("🔍 Checking for existing BHARAT Study protocol...")
        
        try:
            response = self.session.get(f"{API_BASE}/collection-protocols")
            
            if response.status_code == 200:
                protocols = response.json()
                for protocol in protocols:
                    if protocol.get("shortTitle") == "BHARAT-STUDY":
                        print(f"⚠️  BHARAT Study protocol already exists (ID: {protocol.get('id')})")
                        return protocol.get('id')
                
                print("✅ No existing BHARAT Study protocol found - safe to proceed")
                return None
            else:
                print(f"❌ Error checking protocols: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error checking existing protocols: {str(e)}")
            return None
    
    def create_sites_if_needed(self):
        """Create required sites if they don't exist"""
        print("🏥 Setting up required sites...")
        
        required_sites = [
            {
                "name": "IISc Bangalore",
                "code": "BLR",
                "instituteName": "Indian Institute of Science",
                "type": "Repository",
                "activityStatus": "Active",
                "address": {
                    "street": "CV Raman Avenue",
                    "city": "Bangalore",
                    "state": "Karnataka",
                    "country": "India",
                    "zipCode": "560012"
                }
            },
            {
                "name": "MS Ramaiah Hospital",
                "code": "MSR", 
                "instituteName": "MS Ramaiah Hospital",
                "type": "Collection Site",
                "activityStatus": "Active",
                "address": {
                    "street": "New BEL Road",
                    "city": "Bangalore", 
                    "state": "Karnataka",
                    "country": "India",
                    "zipCode": "560054"
                }
            },
            {
                "name": "Bangalore Medical College",
                "code": "BMC",
                "instituteName": "Bangalore Medical College & Research Institute", 
                "type": "Collection Site",
                "activityStatus": "Active",
                "address": {
                    "street": "Fort Road",
                    "city": "Bangalore",
                    "state": "Karnataka", 
                    "country": "India",
                    "zipCode": "560002"
                }
            }
        ]
        
        created_sites = []
        for site_data in required_sites:
            try:
                # Check if site exists
                response = self.session.get(f"{API_BASE}/sites")
                existing_sites = response.json() if response.status_code == 200 else []
                
                site_exists = any(site.get("name") == site_data["name"] for site in existing_sites)
                
                if not site_exists:
                    response = self.session.post(f"{API_BASE}/sites", json=site_data)
                    if response.status_code == 200:
                        created_site = response.json()
                        created_sites.append(created_site)
                        print(f"✅ Created site: {site_data['name']}")
                    else:
                        print(f"❌ Failed to create site {site_data['name']}: {response.text}")
                else:
                    print(f"ℹ️  Site already exists: {site_data['name']}")
                    
            except Exception as e:
                print(f"❌ Error creating site {site_data['name']}: {str(e)}")
        
        return created_sites
    
    def create_users_if_needed(self):
        """Create PI and coordinator users if they don't exist"""
        print("👥 Setting up study users...")
        
        users_to_create = [
            {
                "firstName": "Principal",
                "lastName": "Investigator", 
                "loginName": "pi@longevityindia.org",
                "emailAddress": "pi@longevityindia.org",
                "instituteName": "Indian Institute of Science",
                "primarySite": "IISc Bangalore",
                "type": "CONTACT",
                "activityStatus": "Active",
                "dnd": False,
                "manageForms": False
            },
            {
                "firstName": "Study",
                "lastName": "Coordinator",
                "loginName": "coordinator@longevityindia.org", 
                "emailAddress": "coordinator@longevityindia.org",
                "instituteName": "Indian Institute of Science",
                "primarySite": "IISc Bangalore",
                "type": "CONTACT", 
                "activityStatus": "Active",
                "dnd": False,
                "manageForms": False
            }
        ]
        
        for user_data in users_to_create:
            try:
                # Check if user exists
                response = self.session.get(f"{API_BASE}/users", params={"loginName": user_data["loginName"]})
                
                if response.status_code == 200:
                    users = response.json()
                    if not any(user.get("loginName") == user_data["loginName"] for user in users):
                        response = self.session.post(f"{API_BASE}/users", json=user_data)
                        if response.status_code == 200:
                            print(f"✅ Created user: {user_data['loginName']}")
                        else:
                            print(f"❌ Failed to create user {user_data['loginName']}: {response.text}")
                    else:
                        print(f"ℹ️  User already exists: {user_data['loginName']}")
                        
            except Exception as e:
                print(f"❌ Error creating user {user_data['loginName']}: {str(e)}")
    
    def load_protocol_configuration(self):
        """Load the BHARAT Study protocol configuration from JSON file"""
        print("📋 Loading BHARAT Study protocol configuration...")
        
        try:
            with open("bharat-study-collection-protocol.json", "r") as f:
                config = json.load(f)
            print("✅ Protocol configuration loaded successfully")
            return config
        except Exception as e:
            print(f"❌ Error loading protocol configuration: {str(e)}")
            return None
    
    def create_collection_protocol(self, config):
        """Create the BHARAT Study collection protocol"""
        print("🧬 Creating BHARAT Study collection protocol...")
        
        try:
            response = self.session.post(f"{API_BASE}/collection-protocols", json=config)
            
            if response.status_code == 200:
                protocol = response.json()
                protocol_id = protocol.get("id")
                print(f"✅ BHARAT Study protocol created successfully!")
                print(f"   Protocol ID: {protocol_id}")
                print(f"   Title: {protocol.get('title')}")
                print(f"   Short Title: {protocol.get('shortTitle')}")
                print(f"   Events: {len(protocol.get('events', []))} visits configured")
                return protocol_id
            else:
                print(f"❌ Failed to create protocol: {response.status_code}")
                print(f"   Error details: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating collection protocol: {str(e)}")
            return None
    
    def create_age_cohort_groups(self, protocol_id):
        """Create age cohort groups for the BHARAT Study"""
        print("👥 Setting up age cohort groups...")
        
        age_cohorts = [
            {"name": "AG1-Young-Adults", "description": "Age 20-30 years", "ageRange": "20-30"},
            {"name": "AG2-Early-Adults", "description": "Age 31-40 years", "ageRange": "31-40"}, 
            {"name": "AG3-Middle-Adults", "description": "Age 41-50 years", "ageRange": "41-50"},
            {"name": "AG4-Late-Adults", "description": "Age 51-60 years", "ageRange": "51-60"},
            {"name": "AG5-Senior-Adults", "description": "Age 61-70 years", "ageRange": "61-70"}
        ]
        
        created_groups = []
        for cohort in age_cohorts:
            group_data = {
                "name": cohort["name"],
                "description": cohort["description"],
                "activityStatus": "Active",
                "collectionProtocols": [{"id": protocol_id}]
            }
            
            try:
                response = self.session.post(f"{API_BASE}/cp-groups", json=group_data)
                if response.status_code == 200:
                    group = response.json()
                    created_groups.append(group)
                    print(f"✅ Created age cohort: {cohort['name']} ({cohort['ageRange']})")
                else:
                    print(f"❌ Failed to create cohort {cohort['name']}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error creating cohort {cohort['name']}: {str(e)}")
        
        return created_groups
    
    def setup_specimen_types(self):
        """Setup additional specimen types needed for BHARAT Study"""
        print("🧪 Setting up BHARAT Study specimen types...")
        
        # Check if custom specimen types need to be added
        try:
            response = self.session.get(f"{API_BASE}/permissible-values", params={"attribute": "specimen_type"})
            if response.status_code == 200:
                existing_types = response.json()
                print(f"ℹ️  Found {len(existing_types)} existing specimen types")
                
                # Add Hair and Buccal Cells if not present
                required_types = ["Hair", "Buccal Cells"] 
                existing_type_values = [t.get("value") for t in existing_types]
                
                for spec_type in required_types:
                    if spec_type not in existing_type_values:
                        print(f"⚠️  Specimen type '{spec_type}' may need to be added manually")
                    else:
                        print(f"✅ Specimen type '{spec_type}' already exists")
                        
        except Exception as e:
            print(f"❌ Error checking specimen types: {str(e)}")
    
    def generate_setup_report(self, protocol_id):
        """Generate a summary report of the setup"""
        print("\n" + "="*60)
        print("🎉 BHARAT STUDY SETUP COMPLETE!")
        print("="*60)
        print(f"📅 Setup completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🆔 Collection Protocol ID: {protocol_id}")
        print(f"🌐 OpenSpecimen URL: {OPENSPECIMEN_URL}")
        print("")
        print("📋 STUDY CONFIGURATION:")
        print("   • Longitudinal study with 4 visits (V0, V1, V2, V3)")
        print("   • Visit schedule: Baseline, 6mo, 12mo, 24mo")
        print("   • Age cohorts: 5 groups (20-30, 31-40, 41-50, 51-60, 61-70)")
        print("   • Sample types: Blood, Saliva, Hair, Buccal cells")
        print("   • Sites: IISc Bangalore, MS Ramaiah, BMC")
        print("")
        print("🔧 NEXT STEPS:")
        print("   1. Configure custom forms for multi-omics analysis")
        print("   2. Set up specimen labeling format (BHARAT-AGx-Pxxxx-Vx-TYPE)")
        print("   3. Configure dashboards and reports")
        print("   4. Set up inventory management")
        print("   5. Train study staff on the system")
        print("")
        print("📞 Support: bharat-study@longevityindia.org")
        print("="*60)
    
    def run_setup(self):
        """Execute the complete BHARAT Study setup"""
        print("\n🚀 BHARAT STUDY OPENSPECIMEN SETUP")
        print("=====================================")
        print("Setting up the longitudinal aging research protocol...")
        print("")
        
        # Step 1: Authenticate
        if not self.authenticate():
            print("❌ Setup failed - cannot authenticate")
            return False
        
        # Step 2: Check for existing protocol
        existing_id = self.check_existing_protocol()
        if existing_id:
            response = input(f"Protocol exists (ID: {existing_id}). Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("⏹️  Setup cancelled by user")
                return False
        
        # Step 3: Setup prerequisites
        self.create_sites_if_needed()
        self.create_users_if_needed()
        self.setup_specimen_types()
        
        # Step 4: Load protocol configuration
        config = self.load_protocol_configuration()
        if not config:
            print("❌ Setup failed - cannot load protocol configuration")
            return False
        
        # Step 5: Create collection protocol
        protocol_id = self.create_collection_protocol(config)
        if not protocol_id:
            print("❌ Setup failed - cannot create collection protocol")
            return False
        
        # Step 6: Create age cohort groups
        self.create_age_cohort_groups(protocol_id)
        
        # Step 7: Generate report
        self.generate_setup_report(protocol_id)
        
        return True

def main():
    """Main entry point"""
    try:
        # Get credentials from user
        print("BHARAT Study OpenSpecimen Setup")
        print("===============================")
        username = input(f"Username (admin): ").strip()
        if not username:
            username = "admin"
            
        password = input("Password (AmruthDB7!): ").strip()
        if not password:
            password = "AmruthDB7!"
        
        # Run setup
        setup = BharatStudySetup(username, password)
        success = setup.run_setup()
        
        if success:
            print("\n✅ Setup completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Setup failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()