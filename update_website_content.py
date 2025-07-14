#!/usr/bin/env python3
"""
Website Content Updater for California Probate Code Appellate Case Information Repository

This script reads the podcast pipeline databases and updates the website with actual episodes.
Simplified version that focuses on getting the real data into the website.

Author: Scholar Podcast System
Date: 2025-07-13
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

class WebsiteContentUpdater:
    def __init__(self):
        # Configuration paths
        self.base_dir = Path(__file__).parent.parent
        self.website_dir = Path(__file__).parent
        self.processed_cases_file = self.base_dir / "logs" / "processed_cases.json"
        self.special_editions_file = self.base_dir / "special_edition" / "processed_special_editions.json"
        self.index_html_file = self.website_dir / "index.html"
        
        print(f"📁 Base directory: {self.base_dir}")
        print(f"🌐 Website directory: {self.website_dir}")
        print(f"📊 Cases file: {self.processed_cases_file}")
        print(f"📄 HTML file: {self.index_html_file}")
        
    def load_processed_cases(self):
        """Load episodes from the processed cases database"""
        episodes = []
        
        if not self.processed_cases_file.exists():
            print(f"❌ Cases file not found: {self.processed_cases_file}")
            return episodes
        
        try:
            with open(self.processed_cases_file, 'r', encoding='utf-8') as f:
                cases_data = json.load(f)
                print(f"✅ Loaded {len(cases_data)} cases from database")
                
                episode_id = 1
                for case_key, case_info in cases_data.items():
                    episode = self.convert_case_to_episode(case_key, case_info, episode_id)
                    if episode:
                        episodes.append(episode)
                        episode_id += 1
                        
        except Exception as e:
            print(f"❌ Error loading cases: {e}")
            
        return episodes
    
    def convert_case_to_episode(self, case_key, case_info, episode_id):
        """Convert a single case to episode format"""
        try:
            # Extract case number (the key like S282314, B341750, etc.)
            case_number = case_key
            
            # Get enhanced case info if available
            enhanced_info = case_info.get('enhanced_case_info', {})
            file_info = case_info.get('file_info', {})
            
            # Extract title
            if enhanced_info:
                title = f"Case {enhanced_info.get('case_name', case_number)}"
                court = enhanced_info.get('court', 'California Appellate Court')
                date = enhanced_info.get('date', '2025-07-13')
            else:
                title = f"Case {case_number}"
                court = 'California Appellate Court'
                date = case_info.get('processed_date', '2025-07-13')[:10]  # Extract date part
            
            # Get audio URL - check for Podbean URL
            audio_url = '#'
            podbean_result = file_info.get('podbean_result', {})
            if podbean_result:
                episode_info = podbean_result.get('episode_info', {})
                if episode_info and 'episode' in episode_info:
                    audio_url = episode_info['episode'].get('permalink_url', '#')
                    if audio_url == '#':
                        audio_url = episode_info['episode'].get('player_url', '#')
            
            # Determine episode type based on file name or content
            episode_type = 'opinion'  # Default to opinion
            if 'brief' in case_key.lower() or 'brief' in str(file_info).lower():
                episode_type = 'brief'
            elif 'analysis' in case_key.lower() or 'special' in str(file_info).lower():
                episode_type = 'analysis'
            
            # Get duration
            duration = 'N/A'
            audio_result = file_info.get('audio_result', {})
            if audio_result and 'duration_estimate' in audio_result:
                duration_seconds = audio_result['duration_estimate']
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                duration = f"{minutes}:{seconds:02d}"
            
            # Generate description
            description = self.generate_description(case_info, episode_type, case_number)
            
            # Create episode object
            episode = {
                'id': episode_id,
                'type': episode_type,
                'title': title,
                'court': court,
                'date': date,
                'caseNumber': case_number,
                'description': description,
                'audioUrl': audio_url,
                'textUrl': '#',  # Could be populated with PDF links later
                'duration': duration,
                'keywords': self.extract_keywords(case_key, case_info)
            }
            
            return episode
            
        except Exception as e:
            print(f"❌ Error converting case {case_key}: {e}")
            return None
    
    def generate_description(self, case_info, episode_type, case_number):
        """Generate a professional description for the episode"""
        if episode_type == 'brief':
            return f"Professional case brief analysis of California case {case_number}, covering key legal principles, procedural requirements, and practical guidance for legal practitioners."
        elif episode_type == 'analysis':
            return f"Legal analysis and commentary on case {case_number}, providing in-depth examination of the decision's implications for California probate practice."
        else:
            return f"Appellate court decision in case {case_number}, addressing significant issues in California probate law with implications for legal practitioners and estate planning professionals."
    
    def extract_keywords(self, case_key, case_info):
        """Extract relevant keywords for search functionality"""
        keywords = ['probate', 'California', 'appellate']
        
        # Add case number variations
        if case_key:
            keywords.append(case_key.lower())
        
        # Add common probate terms
        probate_terms = ['estate', 'trust', 'guardianship', 'conservatorship', 
                        'will', 'inheritance', 'beneficiary', 'executor']
        
        # Simple keyword detection (could be enhanced with content analysis)
        content_str = str(case_info).lower()
        for term in probate_terms:
            if term in content_str:
                keywords.append(term)
        
        return keywords[:6]  # Limit to 6 keywords
    
    def update_website_html(self, episodes):
        """Update the index.html file with new episode data"""
        if not self.index_html_file.exists():
            print(f"❌ Website file not found: {self.index_html_file}")
            return False
        
        try:
            # Read current HTML
            with open(self.index_html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert episodes to JavaScript format
            episodes_js = json.dumps(episodes, indent=12)
            
            # Replace the episodes array in the JavaScript
            pattern = r'const episodes = \[.*?\];'
            replacement = f'const episodes = {episodes_js};'
            
            # Use DOTALL flag to match across newlines
            updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
            
            # Update statistics
            total_episodes = len(episodes)
            opinions = len([e for e in episodes if e['type'] == 'opinion'])
            briefs = len([e for e in episodes if e['type'] == 'brief'])
            analysis = len([e for e in episodes if e['type'] == 'analysis'])
            
            # Update stats in the HTML
            stats_updates = [
                (r'<div class="stat-number" id="totalEpisodes">\d+\+</div>',
                 f'<div class="stat-number" id="totalEpisodes">{total_episodes}</div>'),
                (r'<div class="stat-number" id="appealateOpinions">\d+\+</div>',
                 f'<div class="stat-number" id="appealateOpinions">{opinions}</div>'),
                (r'<div class="stat-number" id="caseBriefs">\d+\+</div>',
                 f'<div class="stat-number" id="caseBriefs">{briefs}</div>'),
                (r'<div class="stat-number" id="legalAnalysis">\d+\+</div>',
                 f'<div class="stat-number" id="legalAnalysis">{analysis}</div>')
            ]
            
            for pattern, replacement in stats_updates:
                updated_html = re.sub(pattern, replacement, updated_html)
            
            # Write updated content back
            with open(self.index_html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"✅ Website updated successfully!")
            print(f"📊 Statistics:")
            print(f"   - Total Episodes: {total_episodes}")
            print(f"   - Opinions: {opinions}")
            print(f"   - Briefs: {briefs}")
            print(f"   - Analysis: {analysis}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating website: {e}")
            return False
    
    def run_update(self):
        """Main function to run the website update"""
        print("🚀 Starting website content update...")
        
        # Load episodes from database
        print("\n📖 Loading episodes from database...")
        episodes = self.load_processed_cases()
        
        if not episodes:
            print("⚠️  No episodes found in database")
            return False
        
        print(f"✅ Converted {len(episodes)} episodes")
        
        # Show sample episode for verification
        if episodes:
            print(f"\n📋 Sample episode:")
            sample = episodes[0]
            print(f"   Title: {sample['title']}")
            print(f"   Court: {sample['court']}")
            print(f"   Type: {sample['type']}")
            print(f"   Audio URL: {sample['audioUrl']}")
            print(f"   Duration: {sample['duration']}")
        
        # Update website
        print("\n🔧 Updating website...")
        success = self.update_website_html(episodes)
        
        if success:
            print("\n🎉 Website update completed successfully!")
            print("🌐 Your website now contains actual podcast episodes from your database")
            return True
        else:
            print("\n❌ Website update failed")
            return False

def main():
    """Main function"""
    updater = WebsiteContentUpdater()
    success = updater.run_update()
    
    if success:
        print("\n✅ SUCCESS: Website has been updated with your podcast episodes!")
        print("🔄 You can now commit and push these changes to GitHub to update your live website.")
    else:
        print("\n❌ FAILED: Website update unsuccessful")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
