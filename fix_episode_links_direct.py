#!/usr/bin/env python3
"""
DIRECT FIX: Update specific episodes with correct links
Addresses the immediate brief link issues
"""

import json
import re
from pathlib import Path

def fix_episode_links_directly():
    """Fix the episode links directly in index.html"""
    
    website_dir = Path(__file__).parent
    index_file = website_dir / "index.html"
    
    print(f"🔧 Fixing episode links directly in {index_file}")
    
    # Read the current HTML content
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the episodes JavaScript array
    episodes_match = re.search(r'const episodes = (\[.*?\]);', content, re.DOTALL)
    if not episodes_match:
        print("❌ Could not find episodes array in HTML")
        return False
    
    episodes_json = episodes_match.group(1)
    episodes = json.loads(episodes_json)
    
    print(f"📊 Found {len(episodes)} episodes to review")
    
    # Fix specific episodes with known issues
    fixes_applied = 0
    
    for episode in episodes:
        episode_id = episode.get('id', 'unknown')
        case_number = episode.get('caseNumber', '')
        episode_type = episode.get('type', '')
        
        # Fix Episode 10: B333052 opinion should link to original court text
        if (case_number == 'B333052' and episode_type == 'opinion' and 
            episode.get('textUrl') == '#'):
            episode['textUrl'] = 'texts/B333052_Conservatorship_of_ANNE_S_published.txt'
            print(f"✅ Fixed Episode {episode_id}: B333052 opinion text link")
            fixes_applied += 1
        
        # Fix Episode 1: B341350 opinion - check if court opinion exists
        elif (case_number == 'B341350' and episode_type == 'opinion' and 
              episode.get('textUrl') == '#'):
            # B341350 doesn't have an original court opinion in website/texts/
            # This is expected - some cases only have briefs
            print(f"ℹ️  Episode {episode_id}: B341350 opinion - no original court text available")
        
        # Fix Episode 3: C102321 opinion - check if court opinion exists  
        elif (case_number == 'C102321' and episode_type == 'opinion' and 
              episode.get('textUrl') == '#'):
            # C102321 doesn't have an original court opinion in website/texts/
            # This is expected - some cases only have briefs
            print(f"ℹ️  Episode {episode_id}: C102321 opinion - no original court text available")
        
        # Episode 7: B341750 brief is missing the brief file - can't fix without regenerating
        elif (case_number == 'B341750' and episode_type == 'brief' and 
              episode.get('textUrl') == '#'):
            print(f"⚠️  Episode {episode_id}: B341750 brief file is missing - requires regeneration")
    
    if fixes_applied > 0:
        # Convert back to JavaScript and update HTML
        updated_episodes_js = json.dumps(episodes, indent=12)
        updated_content = re.sub(
            r'const episodes = \[.*?\];',
            f'const episodes = {updated_episodes_js};',
            content,
            flags=re.DOTALL
        )
        
        # Write updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Applied {fixes_applied} fixes to index.html")
        return True
    else:
        print("ℹ️  No fixes needed - all detectable issues are due to missing source files")
        return False

def main():
    """Main function"""
    print("🚀 Applying direct fixes to episode links...")
    
    success = fix_episode_links_directly()
    
    if success:
        print("\n✅ SUCCESS: Episode links updated!")
        print("🔄 Next step: Deploy to GitHub Pages")
        print("\nCommands to deploy:")
        print("cd website")  
        print("git add .")
        print("git commit -m 'Fix: Direct episode link corrections'")
        print("git push origin main")
    else:
        print("\n❓ INFO: Direct fixes not needed")
        print("💡 Main issue is missing B341750 brief file")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
