#!/usr/bin/env python3
"""
Phase 5 Website Content Updater Wrapper
Uses the existing comprehensive_website_updater.py properly

Author: Scholar Podcast System - Phase 5 Integration  
Date: July 17, 2025
"""

import sys
import os
from pathlib import Path

def run_comprehensive_updater():
    """Execute the comprehensive website updater as a module"""
    try:
        print("🔧 Phase 5: Running comprehensive website updater...")
        
        # Add the website directory to Python path
        website_dir = Path(__file__).parent
        sys.path.insert(0, str(website_dir))
        
        # Import and run the comprehensive updater
        from comprehensive_website_updater import ComprehensiveWebsiteUpdater
        
        # Create and run the updater
        updater = ComprehensiveWebsiteUpdater()
        
        # Load all content from databases
        updater.load_all_content()
        
        # Check if we have episodes to update
        if not updater.all_episodes:
            print("⚠️  No episodes found - website will not be updated")
            return False
        
        print(f"📊 Found {len(updater.all_episodes)} total episodes")
        print(f"    - Opinions: {updater.stats.get('opinions', 0)}")
        print(f"    - Briefs: {updater.stats.get('briefs', 0)}")
        print(f"    - Analysis: {updater.stats.get('analysis', 0)}")
        
        # Update the website (this method should exist in the class)
        if hasattr(updater, 'update_website'):
            success = updater.update_website()
            if success:
                print("✅ Website updated successfully with comprehensive updater")
                return True
            else:
                print("❌ Website update failed")
                return False
        else:
            print("⚠️  ComprehensiveWebsiteUpdater missing update_website method")
            print("    Will attempt manual HTML update...")
            
            # Manual fallback - update HTML directly
            success = manual_html_update(updater)
            return success
            
    except ImportError as e:
        print(f"❌ Could not import comprehensive_website_updater: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running comprehensive updater: {e}")
        return False

def manual_html_update(updater):
    """Manual HTML update as fallback"""
    try:
        import json
        import re
        
        print("🔧 Performing manual HTML update...")
        
        # Read current HTML
        html_file = updater.index_html_file
        if not html_file.exists():
            print(f"❌ HTML file not found: {html_file}")
            return False
            
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert episodes to JavaScript format
        episodes_js = json.dumps(updater.all_episodes, indent=8)
        
        # Update episodes array in HTML
        pattern = r'const episodes = \[.*?\];'
        replacement = f'const episodes = {episodes_js};'
        
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # Update statistics
        stats = updater.stats
        updated_html = re.sub(
            r'<div class="stat-number" id="totalEpisodes">\d+\+?</div>',
            f'<div class="stat-number" id="totalEpisodes">{stats["total"]}+</div>',
            updated_html
        )
        
        # Write updated HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ Manual HTML update completed - {stats['total']} episodes")
        return True
        
    except Exception as e:
        print(f"❌ Manual HTML update failed: {e}")
        return False

if __name__ == "__main__":
    success = run_comprehensive_updater()
    if success:
        print("✅ Phase 5 website content update completed successfully")
        sys.exit(0)
    else:
        print("❌ Phase 5 website content update failed")
        sys.exit(1)
