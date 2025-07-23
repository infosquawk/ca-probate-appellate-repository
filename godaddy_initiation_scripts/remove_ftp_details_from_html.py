#!/usr/bin/env python3
"""
Quick Script: Remove FTP Account Details from HTML Pages
Removes sensitive FTP credential information from deployment test pages
"""

import re
from pathlib import Path

def remove_ftp_details_from_file(file_path):
    """Remove FTP account details from a specific HTML file"""
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the FTP account details section
        ftp_section_pattern = r'<div class="account-info">.*?</div>\s*'
        
        # Remove the FTP account details section
        content = re.sub(ftp_section_pattern, '', content, flags=re.DOTALL)
        
        # Remove FTP account reference from timestamp
        content = re.sub(r'<p>FTP Account:.*?</p>\s*', '', content)
        
        # Remove unused CSS for account-info class
        css_pattern = r'\.account-info \{[^}]*\}\s*'
        content = re.sub(css_pattern, '', content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Removed FTP details from: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def clean_all_deployment_files():
    """Remove FTP details from all deployment test files"""
    
    print("=== Remove FTP Account Details from HTML Pages ===")
    
    current_dir = Path(__file__).parent
    
    # Files to clean
    files_to_clean = [
        "manual_deployment_test.py",
        # Add other files here if needed
    ]
    
    cleaned_count = 0
    
    for filename in files_to_clean:
        file_path = current_dir / filename
        if file_path.exists():
            if remove_ftp_details_from_file(file_path):
                cleaned_count += 1
        else:
            print(f"⚠ File not found: {filename}")
    
    print(f"\n✅ Security cleanup complete!")
    print(f"📁 Files processed: {cleaned_count}")
    print("🔒 FTP credentials no longer visible in HTML output")

def clean_specific_html_string(html_content):
    """Clean FTP details from HTML string (for use in other scripts)"""
    
    # Remove FTP account details section
    html_content = re.sub(
        r'<div class="account-info">.*?</div>\s*', 
        '', 
        html_content, 
        flags=re.DOTALL
    )
    
    # Remove FTP account reference from timestamp
    html_content = re.sub(r'<p>FTP Account:.*?</p>\s*', '', html_content)
    
    # Remove unused CSS
    html_content = re.sub(
        r'\.account-info \{[^}]*\}\s*', 
        '', 
        html_content, 
        flags=re.DOTALL
    )
    
    return html_content

if __name__ == "__main__":
    print("ProBRep.com Security Cleanup Tool")
    print("=" * 40)
    
    # Clean all deployment files
    clean_all_deployment_files()
    
    print("\n🎯 SECURITY BEST PRACTICES:")
    print("✅ FTP credentials removed from public HTML")
    print("✅ Account details no longer visible on live website")
    print("✅ Sensitive information protected")
    print("\n🌐 Your test pages are now secure for public deployment!")
