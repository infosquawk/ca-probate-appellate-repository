#!/usr/bin/env python3
"""
Direct Website Fix: Update Episode Titles in index.html
Directly fixes the remaining episode titles in the website JavaScript
"""

import os
import re
from pathlib import Path

def fix_website_episode_titles():
    """Fix the specific episode titles in index.html"""
    website_file = "index.html"
    
    if not os.path.exists(website_file):
        print(f"❌ Website file not found: {website_file}")
        return False
    
    print("🔧 Fixing episode titles in website...")
    
    # Read current content
    with open(website_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    backup_file = f"index_backup_{Path().cwd().name}.html"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📁 Backup created: {backup_file}")
    
    # Specific title fixes
    title_fixes = [
        # Fix episode titles
        ('"title": "Case B341350"', '"title": "In re Dominic H (B341350)"'),
        ('"title": "Case C102321"', '"title": "Conservatorship of the Person of C (C102321)"'),
        ('"title": "Case S282314"', '"title": "In re Discipline (S282314)"'),
        
        # Fix descriptions
        (
            'case B341350, addressing significant issues in California probate law',
            'In re Dominic H (B341350), guardianship proceeding for a minor'
        ),
        (
            'case C102321, addressing significant issues in California probate law',
            'Conservatorship of the Person of C (C102321), conservatorship proceeding'
        ),
        (
            'case S282314, addressing significant issues in California probate law',
            'In re Discipline (S282314), attorney discipline proceeding'
        )
    ]
    
    changes_made = 0
    for old_text, new_text in title_fixes:
        if old_text in content:
            content = content.replace(old_text, new_text)
            changes_made += 1
            print(f"✅ Fixed: {old_text} → {new_text}")
    
    # Write updated content
    if changes_made > 0:
        with open(website_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Updated website with {changes_made} fixes")
        return True
    else:
        print("\nℹ️ No fixes needed - titles already correct")
        return False

def main():
    """Main execution"""
    print("🎯 Direct Website Episode Title Fix")
    print("=" * 40)
    
    success = fix_website_episode_titles()
    
    if success:
        print("\n✅ Website fixed locally!")
        print("\n📊 Fixed Episodes:")
        print("   • B341350: 'Case B341350' → 'In re Dominic H (B341350)'")
        print("   • C102321: 'Case C102321' → 'Conservatorship of the Person of C (C102321)'")
        print("   • S282314: 'Case S282314' → 'In re Discipline (S282314)'")
        print("\n🚀 Ready to deploy to live website!")
        return True
    else:
        print("\n❌ No changes made")
        return False

if __name__ == "__main__":
    main()
