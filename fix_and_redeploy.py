#!/usr/bin/env python3
"""
Fix and Redeploy ProBRep.com Website
This script fixes the episode data issues by updating the website content 
with current data from all JSON databases and then redeploys to ProBRep.com
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import re

def main():
    print("🔧 FIXING AND REDEPLOYING PROBREP.COM WEBSITE")
    print("=" * 60)
    
    # Set working directory
    base_dir = Path("C:/Users/Ryan/Google_Drive/My_Documents/Work/0000-Claude-Workspace/scholar_podcast")
    website_dir = base_dir / "website"
    
    print(f"📁 Working directory: {website_dir}")
    
    # Step 1: Update website content with latest episode data
    print("\n🔄 Step 1: Updating website content with latest episode data...")
    
    try:
        # Run the comprehensive website updater
        result = subprocess.run([
            sys.executable, "comprehensive_website_updater.py"
        ], 
        cwd=website_dir,
        capture_output=True, 
        text=True,
        timeout=300  # 5 minute timeout
        )
        
        print("WEBSITE UPDATER OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("WEBSITE UPDATER WARNINGS/ERRORS:")
            print(result.stderr)
            
        if result.returncode != 0:
            print(f"❌ Website updater failed with return code {result.returncode}")
            return False
            
        print("✅ Website content updated successfully!")
        
    except subprocess.TimeoutExpired:
        print("❌ Website updater timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running website updater: {e}")
        return False
    
    # Step 2: Deploy updated content to ProBRep.com
    print("\n🚀 Step 2: Deploying updated content to ProBRep.com...")
    
    try:
        # Run the GoDaddy deployment script
        result = subprocess.run([
            sys.executable, "deploy_full_website_to_godaddy.py"
        ], 
        cwd=website_dir,
        capture_output=True, 
        text=True,
        timeout=600  # 10 minute timeout for deployment
        )
        
        print("DEPLOYMENT OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("DEPLOYMENT WARNINGS/ERRORS:")
            print(result.stderr)
            
        if result.returncode != 0:
            print(f"❌ Deployment failed with return code {result.returncode}")
            return False
            
        print("✅ Deployment to ProBRep.com completed successfully!")
        
    except subprocess.TimeoutExpired:
        print("❌ Deployment timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False
    
    # Step 3: Verify deployment
    print("\n🔍 Step 3: Verification and next steps...")
    print("✅ Website content has been updated with latest episode data")
    print("✅ Updated content deployed to ProBRep.com")
    print("\n📝 Please verify the following:")
    print("   1. Visit https://probrep.com - website should load with episodes")
    print("   2. Check that episode search and filtering work")
    print("   3. Verify audio links work (go to Podbean)")
    print("   4. Test PDF and text file downloads")
    print("   5. Confirm mobile responsiveness")
    
    print("\n🎉 FIX AND REDEPLOY COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All operations completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some operations failed - check output above")
        sys.exit(1)
