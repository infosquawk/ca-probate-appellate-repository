#!/usr/bin/env python3
"""
Fix JavaScript syntax errors in index.html - Remove problematic line breaks from episode descriptions
"""

import re
import os

def fix_javascript_syntax():
    """Fix JavaScript syntax errors caused by unescaped line breaks in descriptions"""
    
    # Read the current HTML file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ index.html not found in current directory")
        return False
    
    print("🔧 Fixing JavaScript syntax errors...")
    
    # Find and fix all problematic descriptions with line breaks
    # Pattern: "description": "Here is a professional...:\n\nActual content..."
    pattern = r'"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\s*\n\s*([^"]*)"'
    
    def fix_description(match):
        description_content = match.group(1)
        # Clean up the description - remove extra whitespace and newlines
        cleaned_desc = re.sub(r'\s+', ' ', description_content.strip())
        # Return the fixed description without the "Here is a professional..." prefix
        return f'"description": "{cleaned_desc}"'
    
    # Apply the fix
    content_fixed = re.sub(pattern, fix_description, content, flags=re.MULTILINE | re.DOTALL)
    
    # Count how many fixes were applied
    fixes_count = len(re.findall(pattern, content, flags=re.MULTILINE | re.DOTALL))
    
    if fixes_count > 0:
        # Create backup of original
        with open('index.html.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write the fixed content
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content_fixed)
        
        print(f"✅ Fixed {fixes_count} JavaScript syntax errors")
        print("✅ Created backup: index.html.backup")
        print("✅ Updated index.html with fixes")
        
        # Also create a clean fixed version for deployment
        with open('index_FIXED.html', 'w', encoding='utf-8') as f:
            f.write(content_fixed)
        print("✅ Created index_FIXED.html for deployment")
        
        return True
    else:
        print("ℹ️ No JavaScript syntax errors found to fix")
        return False

def deploy_fixed_version():
    """Deploy the fixed version to GoDaddy"""
    try:
        import ftplib
        import json
        
        # Load GoDaddy config
        config_path = 'godaddy_config.json'
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            return False
            
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("🚀 Deploying fixed version to probrep.com...")
        
        # Connect to FTP
        ftp = ftplib.FTP()
        ftp.connect(config['host'], 21)
        ftp.login(config['username'], config['password'])
        
        # Upload the fixed index.html
        with open('index.html', 'rb') as f:
            ftp.storbinary('STOR index.html', f)
        
        ftp.quit()
        
        print("✅ Successfully deployed fixed version!")
        print("✅ Website should now display episodes correctly")
        print("🌐 Test at: https://probrep.com")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    """Main execution function"""
    print("🔧 JavaScript Syntax Error Fixer")
    print("=" * 50)
    
    # Fix the JavaScript syntax errors
    if fix_javascript_syntax():
        print("\n🚀 Deploy the fix? (y/n): ", end="")
        response = input().lower().strip()
        
        if response in ['y', 'yes']:
            deploy_fixed_version()
        else:
            print("ℹ️ Fixed files created. Deploy manually when ready:")
            print("   python deploy_probrep_standalone.py deploy")
    else:
        print("❌ No fixes applied. Check the file manually.")

if __name__ == "__main__":
    main()
