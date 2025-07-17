#!/usr/bin/env python3
"""
Comprehensive Website Automation Script - IMPROVED LINKS VERSION
California Probate Code Appellate Case Information Repository

This script automatically reviews ALL available files from the Scholar Podcast System
and updates the website with complete episode data from multiple sources.
NOW WITH IMPROVED LINK MAPPING LOGIC!

Data Sources:
- logs/processed_cases.json (podcast episodes with audio)
- probate_cases/processed_cases.json (all processed PDF cases)
- probate_cases/processed_briefs.json (case briefs with Podbean URLs)
- special_edition/* (special editions and analysis)

Author: Scholar Podcast System
Version: 2.2 - IMPROVED LINKS
Date: 2025-07-17
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class ComprehensiveWebsiteUpdater:
    def __init__(self):
        # Configuration paths
        self.base_dir = Path(__file__).parent.parent
        self.website_dir = Path(__file__).parent
        
        # Data source files
        self.logs_cases_file = self.base_dir / "logs" / "processed_cases.json"
        self.probate_cases_file = self.base_dir / "probate_cases" / "processed_cases.json"
        self.briefs_file = self.base_dir / "probate_cases" / "processed_briefs.json"
        self.special_edition_dir = self.base_dir / "special_edition"
        
        # Website file
        self.index_html_file = self.website_dir / "index.html"
        
        # Website content directories
        self.website_texts_dir = self.website_dir / "texts"
        self.website_pdfs_dir = self.website_dir / "pdfs"
        
        # Episode collection
        self.all_episodes = []
        self.stats = {
            'total': 0,
            'opinions': 0,
            'briefs': 0,
            'analysis': 0,
            'with_audio': 0,
            'pdf_only': 0
        }
        
        print(f"🔧 Comprehensive Website Updater Initialized (IMPROVED LINKS VERSION)")
        print(f"📁 Base directory: {self.base_dir}")
        print(f"🌐 Website directory: {self.website_dir}")
        
    def find_text_file(self, case_number: str, is_brief: bool = False) -> str:
        """Find text file for a case with IMPROVED logic"""
        if not self.website_texts_dir.exists():
            return ''
        
        case_upper = case_number.upper()
        
        # For case briefs
        if is_brief:
            # Look for files with (Case_Brief) pattern first
            for txt_file in self.website_texts_dir.glob("*.txt"):
                if (case_upper in txt_file.name.upper() and 
                    "(Case_Brief)" in txt_file.name):
                    return f"texts/{txt_file.name}"
            
            # Fallback to *_brief.txt pattern
            for txt_file in self.website_texts_dir.glob("*.txt"):
                if (case_upper in txt_file.name.upper() and 
                    "_brief.txt" in txt_file.name.lower()):
                    return f"texts/{txt_file.name}"
        
        # For original court opinions
        else:
            # Look for original text files (not briefs)
            for txt_file in self.website_texts_dir.glob("*.txt"):
                if (case_upper in txt_file.name.upper() and 
                    "(Case_Brief)" not in txt_file.name and
                    "_brief.txt" not in txt_file.name.lower()):
                    return f"texts/{txt_file.name}"
        
        return ''

    def find_pdf_file(self, case_number: str) -> str:
        """Find PDF file for a case with IMPROVED logic"""
        if not self.website_pdfs_dir.exists():
            return ''
        
        case_upper = case_number.upper()
        
        # Search in both published and unpublished directories
        for subdir in ['published', 'unpublished']:
            pdf_dir = self.website_pdfs_dir / subdir
            if pdf_dir.exists():
                for pdf_file in pdf_dir.glob("*.pdf"):
                    if case_upper in pdf_file.name.upper():
                        return f"pdfs/{subdir}/{pdf_file.name}"
        
        return ''
    
    def load_all_content(self):
        """Load content from all available sources"""
        print("\n📖 Loading content from all sources...")
        
        # Load podcast episodes (logs/processed_cases.json)
        self.load_podcast_episodes()
        
        # Load processed cases (probate_cases/processed_cases.json)
        self.load_processed_cases()
        
        # Load case briefs (probate_cases/processed_briefs.json)
        self.load_case_briefs()
        
        # Load special editions (if available)
        self.load_special_editions()
        
        # Remove duplicates and sort
        self.deduplicate_and_sort()
        
        # Calculate statistics
        self.calculate_statistics()
        
    def load_podcast_episodes(self):
        """Load episodes from logs/processed_cases.json"""
        if not self.logs_cases_file.exists():
            print(f"⚠️  Logs cases file not found: {self.logs_cases_file}")
            return
            
        try:
            with open(self.logs_cases_file, 'r', encoding='utf-8') as f:
                logs_data = json.load(f)
                
            print(f"📊 Found {len(logs_data)} podcast episodes in logs")
            
            for case_key, case_info in logs_data.items():
                episode = self.convert_podcast_episode(case_key, case_info)
                if episode:
                    self.all_episodes.append(episode)
                    
        except Exception as e:
            print(f"❌ Error loading podcast episodes: {e}")
    
    def load_processed_cases(self):
        """Load cases from probate_cases/processed_cases.json"""
        if not self.probate_cases_file.exists():
            print(f"⚠️  Probate cases file not found: {self.probate_cases_file}")
            return
            
        try:
            with open(self.probate_cases_file, 'r', encoding='utf-8') as f:
                probate_data = json.load(f)
                
            # The file has a nested structure
            processed_cases = probate_data.get('processed_cases', {})
            print(f"📊 Found {len(processed_cases)} processed cases")
            
            # Only include cases with probate content that aren't already in podcast episodes
            existing_case_numbers = {ep['caseNumber'] for ep in self.all_episodes}
            
            for case_key, case_info in processed_cases.items():
                if case_info.get('found_probate_code', False) and case_key not in existing_case_numbers:
                    episode = self.convert_processed_case(case_key, case_info)
                    if episode:
                        self.all_episodes.append(episode)
                        
        except Exception as e:
            print(f"❌ Error loading processed cases: {e}")
    
    def load_case_briefs(self):
        """Load case briefs from probate_cases/processed_briefs.json"""
        if not self.briefs_file.exists():
            print(f"⚠️  Briefs file not found: {self.briefs_file}")
            return
            
        try:
            with open(self.briefs_file, 'r', encoding='utf-8') as f:
                briefs_data = json.load(f)
                
            print(f"📊 Found {len(briefs_data)} case briefs")
            
            for brief_key, brief_info in briefs_data.items():
                episode = self.convert_case_brief(brief_key, brief_info)
                if episode:
                    self.all_episodes.append(episode)
                    
        except Exception as e:
            print(f"❌ Error loading case briefs: {e}")
    
    def load_special_editions(self):
        """Load special editions from special_edition directory"""
        # Look for the California's Heritage file in website/texts
        heritage_file = self.website_texts_dir / "2025-07-13_Californias_Heritage_of_Estates_analysis.txt"
        if heritage_file.exists():
            episode = {
                'id': len(self.all_episodes) + 1,
                'type': 'analysis',
                'title': "Analysis: California's Heritage Of Estates",
                'court': 'Legal Analysis Special Edition',
                'date': '2025-07-13',
                'caseNumber': 'Analysis-14',
                'description': 'Special legal analysis and commentary on California probate law matters. In-depth examination with practical implications for legal practitioners.',
                'audioUrl': 'https://www.podbean.com/ew/pb-thdza-1904721',
                'textUrl': 'texts/2025-07-13_Californias_Heritage_of_Estates_analysis.txt',
                'pdfUrl': '',
                'duration': 'Audio',
                'keywords': ['legal analysis', 'commentary', 'special edition', 'probate law'],
                'source': 'special_edition'
            }
            self.all_episodes.append(episode)
            print(f"📊 Found 1 special edition analysis with audio")
    
    def convert_podcast_episode(self, case_key: str, case_info: Dict) -> Optional[Dict]:
        """Convert podcast episode from logs to website format with IMPROVED linking"""
        try:
            file_info = case_info.get('file_info', {})
            enhanced_info = case_info.get('enhanced_case_info', {})
            
            # Determine case name
            case_name = enhanced_info.get('case_name', '')
            if not case_name or case_name == 'Unknown':
                # Map specific cases to their known names
                case_mapping = {
                    'B333052': 'Conservatorship of ANNE S',
                    'G063155': 'Estate of LAYLA BOYAJIAN',
                    'B341750': 'Conservatorship of Julie C',
                    'B330596': 'Nelson v Huhn',
                    'D085918': 'Estate of EDEN AHBEZ'
                }
                case_name = case_mapping.get(case_key, 'Unknown')
            
            # Basic episode info
            episode = {
                'id': len(self.all_episodes) + 1,
                'type': 'opinion',
                'title': f"Case {case_key} - {case_name}" if case_name != 'Unknown' else f"Case {case_key}",
                'court': enhanced_info.get('court', 'California Appellate Court'),
                'date': enhanced_info.get('date', case_info.get('processed_date', '2025-07-13')[:10]),
                'caseNumber': case_key,
                'description': f"Appellate court decision in case {case_key}, addressing significant issues in California probate law. Generated using Enhanced StyleTTS2 neural voice synthesis with complete legal opinion content.",
                'audioUrl': '#',
                'textUrl': '',  # Will be set below
                'pdfUrl': '',   # Will be set below
                'duration': 'N/A',
                'keywords': ['probate', 'California', 'appellate', case_key.lower()],
                'source': 'podcast'
            }
            
            # IMPROVED: Find actual text and PDF files
            episode['textUrl'] = self.find_text_file(case_key, is_brief=False)
            episode['pdfUrl'] = self.find_pdf_file(case_key)
            
            # Get Podbean URL if available
            podbean_result = file_info.get('podbean_result', {})
            if podbean_result and podbean_result.get('episode_info', {}).get('episode'):
                episode_info = podbean_result['episode_info']['episode']
                episode['audioUrl'] = episode_info.get('permalink_url', '#')
            
            # Get duration if available
            audio_result = file_info.get('audio_result', {})
            if audio_result.get('duration_estimate'):
                duration_seconds = audio_result['duration_estimate']
                hours = int(duration_seconds // 3600)
                minutes = int((duration_seconds % 3600) // 60)
                seconds = int(duration_seconds % 60)
                
                if hours > 0:
                    episode['duration'] = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    episode['duration'] = f"{minutes}:{seconds:02d}"
                    
            return episode
            
        except Exception as e:
            print(f"⚠️  Error converting podcast episode {case_key}: {e}")
            return None
    
    def convert_processed_case(self, case_key: str, case_info: Dict) -> Optional[Dict]:
        """Convert processed case to website format"""
        try:
            file_paths = case_info.get('file_paths', {})
            case_name = file_paths.get('case_name', case_key)
            
            episode = {
                'id': len(self.all_episodes) + 1,
                'type': 'opinion',
                'title': case_name.replace('_', ' ').title() if case_name != case_key else f"Case {case_key}",
                'court': 'California Appellate Court',
                'date': case_info.get('processed_date', '2025-07-13')[:10],
                'caseNumber': case_key,
                'description': f"California appellate court case {case_key} addressing probate law matters. PDF document processed and available for review.",
                'audioUrl': '#',  # No audio for these cases yet
                'textUrl': self.find_text_file(case_key, is_brief=False),
                'pdfUrl': self.find_pdf_file(case_key),
                'duration': 'PDF',
                'keywords': ['probate', 'California', 'appellate', case_key.lower(), 'pdf'],
                'source': 'processed_case'
            }
            
            return episode
            
        except Exception as e:
            print(f"⚠️  Error converting processed case {case_key}: {e}")
            return None
    
    def convert_case_brief(self, brief_key: str, brief_info: Dict) -> Optional[Dict]:
        """Convert case brief to website format with IMPROVED linking"""
        try:
            case_number = brief_info.get('case_number', 'Unknown')
            case_name = brief_info.get('case_name', f"Case {case_number}")
            
            # Skip specific test briefs that should be excluded
            excluded_cases = ['B007052', 'B007596']
            excluded_names = ['Conservatorship of TEST S', 'Nelson v Testman', 'Trust v Huhn']
            
            if case_number in excluded_cases or case_name in excluded_names:
                print(f"⚠️  Skipping excluded brief: {case_name} ({case_number})")
                return None
            
            episode = {
                'id': len(self.all_episodes) + 1,
                'type': 'brief',
                'title': f"Brief: {case_name}",
                'court': 'California Appellate Court',
                'date': brief_info.get('processed_date', '2025-07-13')[:10],
                'caseNumber': case_number,
                'description': f"AI-generated case brief for {case_name} ({case_number}). Professional analysis covering key legal principles, procedural requirements, and practical guidance for practitioners.",
                'audioUrl': '#',
                'textUrl': '',  # Will be set below
                'pdfUrl': '',   # Will be set below
                'duration': 'N/A',
                'keywords': ['case brief', 'probate', 'California', 'analysis', case_number.lower()],
                'source': 'case_brief'
            }
            
            # IMPROVED: Find actual case brief text file and related PDF
            episode['textUrl'] = self.find_text_file(case_number, is_brief=True)
            episode['pdfUrl'] = self.find_pdf_file(case_number)
            episode['originalTextUrl'] = self.find_text_file(case_number, is_brief=False)
            
            # Get Podbean URL and duration
            podbean_result = brief_info.get('podbean_result', {})
            if podbean_result and podbean_result.get('episode_info', {}).get('episode'):
                episode_info = podbean_result['episode_info']['episode']
                episode['audioUrl'] = episode_info.get('permalink_url', '#')
                
            if brief_info.get('duration'):
                duration_seconds = brief_info['duration']
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                episode['duration'] = f"{minutes}:{seconds:02d}"
                
            return episode
            
        except Exception as e:
            print(f"⚠️  Error converting case brief {brief_key}: {e}")
            return None
    
    def deduplicate_and_sort(self):
        """Remove duplicates and sort episodes"""
        # Remove duplicates based on case number and type
        seen = set()
        unique_episodes = []
        
        for episode in self.all_episodes:
            key = (episode['caseNumber'], episode['type'])
            if key not in seen:
                seen.add(key)
                unique_episodes.append(episode)
        
        # Sort by date (newest first) and then by case number
        unique_episodes.sort(key=lambda x: (x['date'], x['caseNumber']), reverse=True)
        
        # Reassign IDs
        for i, episode in enumerate(unique_episodes, 1):
            episode['id'] = i
        
        self.all_episodes = unique_episodes
        print(f"📊 After deduplication: {len(self.all_episodes)} unique episodes")
    
    def calculate_statistics(self):
        """Calculate episode statistics"""
        self.stats['total'] = len(self.all_episodes)
        self.stats['opinions'] = len([ep for ep in self.all_episodes if ep['type'] == 'opinion'])
        self.stats['briefs'] = len([ep for ep in self.all_episodes if ep['type'] == 'brief'])
        self.stats['analysis'] = len([ep for ep in self.all_episodes if ep['type'] == 'analysis'])
        self.stats['with_audio'] = len([ep for ep in self.all_episodes if ep['audioUrl'] != '#'])
        self.stats['pdf_only'] = len([ep for ep in self.all_episodes if ep['audioUrl'] == '#'])
        
        print(f"\n📊 Final Statistics:")
        print(f"   Total Episodes: {self.stats['total']}")
        print(f"   Opinions: {self.stats['opinions']}")
        print(f"   Briefs: {self.stats['briefs']}")
        print(f"   Analysis: {self.stats['analysis']}")
        print(f"   With Audio: {self.stats['with_audio']}")
        print(f"   PDF/Text Only: {self.stats['pdf_only']}")
    
    def update_website_html(self):
        """Update the website HTML with all episode data"""
        if not self.index_html_file.exists():
            print(f"❌ Website file not found: {self.index_html_file}")
            return False
            
        try:
            # Read current HTML
            with open(self.index_html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert episodes to JavaScript format
            episodes_js = json.dumps(self.all_episodes, indent=12)
            
            # Replace the episodes array
            updated_html = re.sub(
                r'const episodes = \[[\s\S]*?\];',
                f'const episodes = {episodes_js};',
                html_content,
                flags=re.DOTALL
            )
            
            # Update statistics in HTML
            stats_updates = [
                (r'<div class="stat-number" id="totalEpisodes">\d+\+?</div>',
                 f'<div class="stat-number" id="totalEpisodes">{self.stats["total"]}</div>'),
                (r'<div class="stat-number" id="appealateOpinions">\d+\+?</div>',
                 f'<div class="stat-number" id="appealateOpinions">{self.stats["opinions"]}</div>'),
                (r'<div class="stat-number" id="caseBriefs">\d+\+?</div>',
                 f'<div class="stat-number" id="caseBriefs">{self.stats["briefs"]}</div>'),
                (r'<div class="stat-number" id="legalAnalysis">\d+\+?</div>',
                 f'<div class="stat-number" id="legalAnalysis">{self.stats["analysis"]}</div>')
            ]
            
            for pattern, replacement in stats_updates:
                updated_html = re.sub(pattern, replacement, updated_html)
            
            # Write updated content
            with open(self.index_html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"✅ Website updated successfully with IMPROVED LINKS!")
            print(f"🌐 Ready for deployment with {self.stats['total']} total episodes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating website: {e}")
            return False
    
    def generate_summary_report(self):
        """Generate a summary report of the update"""
        print(f"\n📋 COMPREHENSIVE UPDATE SUMMARY (IMPROVED LINKS)")
        print(f"============================================")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"")
        print(f"📊 Content Statistics:")
        print(f"   Total Episodes: {self.stats['total']}")
        print(f"   ├── Appellate Opinions: {self.stats['opinions']}")
        print(f"   ├── Case Briefs: {self.stats['briefs']}")
        print(f"   └── Legal Analysis: {self.stats['analysis']}")
        print(f"")
        print(f"🎧 Audio Availability:")
        print(f"   With Live Audio: {self.stats['with_audio']}")
        print(f"   PDF/Text Only: {self.stats['pdf_only']}")
        print(f"")
        
        # Check link status for each type
        opinion_with_text = 0
        opinion_with_pdf = 0
        brief_with_text = 0
        brief_with_pdf = 0
        
        for episode in self.all_episodes:
            if episode['type'] == 'opinion':
                if episode.get('textUrl') and episode['textUrl'] != '' and episode['textUrl'] != '#':
                    opinion_with_text += 1
                if episode.get('pdfUrl') and episode['pdfUrl'] != '' and episode['pdfUrl'] != '#':
                    opinion_with_pdf += 1
            elif episode['type'] == 'brief':
                if episode.get('textUrl') and episode['textUrl'] != '' and episode['textUrl'] != '#':
                    brief_with_text += 1
                if episode.get('pdfUrl') and episode['pdfUrl'] != '' and episode['pdfUrl'] != '#':
                    brief_with_pdf += 1
        
        print(f"🔗 Link Status Analysis:")
        print(f"   Opinion Posts:")
        print(f"      With Text Links: {opinion_with_text}/{self.stats['opinions']}")
        print(f"      With PDF Links: {opinion_with_pdf}/{self.stats['opinions']}")
        print(f"   Brief Posts:")
        print(f"      With Text Links: {brief_with_text}/{self.stats['briefs']}")
        print(f"      With PDF Links: {brief_with_pdf}/{self.stats['briefs']}")
        print(f"")
        
        # Show sample episodes by type with link status
        print(f"🔍 Sample Episodes by Type (with link status):")
        for episode_type in ['opinion', 'brief', 'analysis']:
            episodes_of_type = [ep for ep in self.all_episodes if ep['type'] == episode_type]
            if episodes_of_type:
                sample = episodes_of_type[0]
                audio_status = "🎧 Audio" if sample['audioUrl'] != '#' else "📄 Text"
                text_status = "📄 Text" if sample.get('textUrl') and sample['textUrl'] not in ['', '#'] else "No Text"
                pdf_status = "📋 PDF" if sample.get('pdfUrl', '') != '' else "No PDF"
                print(f"   {episode_type.title()}: {sample['title']}")
                print(f"      Links: {audio_status} | {text_status} | {pdf_status}")
        
        print(f"")
        print(f"✅ Website is now populated with IMPROVED LINKS!")
        print(f"🔗 All file paths use proper web-accessible relative paths")
    
    def run_comprehensive_update(self):
        """Main function to run the comprehensive update"""
        print("🚀 Starting comprehensive website update with IMPROVED LINKS...")
        
        try:
            # Load all content from all sources
            self.load_all_content()
            
            if not self.all_episodes:
                print("⚠️  No episodes found in any data sources")
                return False
            
            # Update website
            print("\n🔧 Updating website...")
            if not self.update_website_html():
                return False
            
            # Generate summary report
            self.generate_summary_report()
            
            print("\n🎉 Comprehensive update completed successfully with IMPROVED LINKS!")
            return True
            
        except Exception as e:
            print(f"\n❌ Comprehensive update failed: {e}")
            return False

def main():
    """Main function"""
    updater = ComprehensiveWebsiteUpdater()
    success = updater.run_comprehensive_update()
    
    if success:
        print("\n✅ SUCCESS: Website has been updated with IMPROVED LINKS!")
        print("🔄 You can now commit and push these changes to GitHub to update your live website.")
        print("🌐 All file paths have been converted to web-accessible relative paths.")
        print("🔗 Links should now work properly on the live website!")
    else:
        print("\n❌ FAILED: Comprehensive update unsuccessful")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
