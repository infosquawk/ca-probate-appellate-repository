#!/usr/bin/env python3
"""
Enhanced Website Updater with AI-Generated Descriptions
Prioritizes AI-generated descriptions from case brief pipeline
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class EnhancedWebsiteUpdater:
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
            'with_descriptions': 0,
            'with_ai_descriptions': 0
        }
        
        # Setup logging
        self.setup_logging()
        
        print(f"🤖 Enhanced Website Updater with AI Descriptions Initialized")
        print(f"📁 Base directory: {self.base_dir}")
        print(f"🌐 Website directory: {self.website_dir}")
        
    def setup_logging(self):
        """Setup logging"""
        log_dir = self.website_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"enhanced_website_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def convert_to_web_path(self, file_path: str, case_number: str = "") -> str:
        """Convert file system paths to web-accessible relative paths"""
        if not file_path or file_path == '#':
            return '#'
            
        # Handle different types of file paths
        file_path_lower = file_path.lower()
        
        # Special edition files
        if 'special_edition' in file_path_lower or 'californias_heritage' in file_path_lower:
            if 'californias_heritage' in file_path_lower:
                web_file = "texts/2025-07-13_Californias_Heritage_of_Estates_analysis.txt"
                web_path = self.website_dir / web_file.replace('texts/', '')
                if web_path.exists():
                    return web_file
            return '#'
        
        # Case brief files
        if 'case_brief' in file_path_lower or '_brief' in file_path_lower:
            filename = Path(file_path).name
            
            # First try: exact filename match
            exact_match_path = self.website_texts_dir / filename
            if exact_match_path.exists():
                return f"texts/{filename}"
            
            # Second try: find by case number
            if case_number and self.website_texts_dir.exists():
                for txt_file in self.website_texts_dir.glob("*.txt"):
                    if (txt_file.name.upper().startswith(case_number.upper()) and 
                        'case_brief' in txt_file.name.lower()):
                        return f"texts/{txt_file.name}"
            
            return '#'
        
        # PDF files
        if file_path_lower.endswith('.pdf'):
            filename = Path(file_path).name
            
            # Check both published and unpublished directories
            pdf_locations = ['pdfs/published/', 'pdfs/unpublished/']
            for location in pdf_locations:
                web_file = f"{location}{filename}"
                if (self.website_dir / web_file).exists():
                    return web_file
            
            return ''
        
        # Text files from probate_cases
        if 'probate_cases' in file_path_lower and file_path_lower.endswith('.txt'):
            filename = Path(file_path).name
            
            if self.website_texts_dir.exists():
                for txt_file in self.website_texts_dir.glob("*.txt"):
                    if case_number and case_number.upper() in txt_file.name.upper():
                        return f"texts/{txt_file.name}"
                    elif filename.lower() == txt_file.name.lower():
                        return f"texts/{txt_file.name}"
            
            return '#'
        
        return '#'
    
    def find_original_text_url(self, case_number: str, case_name: str = "") -> str:
        """Find the original court opinion text file for a case"""
        if not self.website_texts_dir.exists():
            return ''
            
        for txt_file in self.website_texts_dir.glob("*.txt"):
            filename = txt_file.name
            
            # Skip case brief files
            if 'case_brief' in filename.lower() or '_brief' in filename.lower():
                continue
                
            # Match by case number
            if case_number and case_number.upper() in filename.upper():
                if any(keyword in filename.lower() for keyword in ['published', 'unpublished', 'estate', 'conservatorship']):
                    return f"texts/{filename}"
        
        return ''
    
    def find_pdf_url(self, case_number: str, case_name: str = "") -> str:
        """Find the PDF file for a case"""
        if not self.website_pdfs_dir.exists():
            return ''
            
        for subdir in ['published', 'unpublished']:
            pdf_dir = self.website_pdfs_dir / subdir
            if pdf_dir.exists():
                for pdf_file in pdf_dir.glob("*.pdf"):
                    if case_number and case_number.upper() in pdf_file.name.upper():
                        return f"pdfs/{subdir}/{pdf_file.name}"
        
        return ''
    
    def get_enhanced_description(self, case_id: str, case_data: Dict, source_type: str) -> str:
        """Get enhanced description with AI-generated content prioritized"""
        
        # Priority 1: Check for AI-generated description from briefs
        if hasattr(self, 'briefs_data') and case_id in self.briefs_data:
            brief_data = self.briefs_data[case_id]
            ai_description = brief_data.get('description')
            if ai_description and len(ai_description.strip()) > 50:
                self.logger.info(f"Using AI-generated description for {case_id}")
                return ai_description.strip()
        
        # Priority 2: Check for description in case data
        description = case_data.get('description', '')
        if description and len(description.strip()) > 50:
            return description.strip()
        
        # Priority 3: Generate description based on case type and available data
        return self.generate_fallback_description(case_id, case_data, source_type)

    def generate_fallback_description(self, case_id: str, case_data: Dict, source_type: str) -> str:
        """Generate fallback description when AI description unavailable"""
        case_name = case_data.get('case_name', case_data.get('title', case_id))
        
        if source_type == 'podcast':
            if 'Conservatorship' in case_name:
                return f"Professional analysis of {case_name}, examining the legal standards and procedural requirements for establishing conservatorship under California law. This appellate court decision addresses key issues in conservatorship proceedings and their impact on individual rights."
            elif 'Estate' in case_name:
                return f"Comprehensive review of {case_name}, analyzing probate law principles and estate administration procedures. This California appellate court opinion addresses important questions in estate litigation and probate administration."
            elif 'Guardianship' in case_name:
                return f"Legal analysis of {case_name}, focusing on guardianship establishment and the court's role in protecting minor interests. This decision examines procedural safeguards and substantive requirements in guardianship proceedings."
            else:
                return f"Professional legal analysis of {case_name}, a California appellate court decision examining key principles of probate and family law. This case addresses important legal issues with practical implications for legal practitioners."
        
        elif source_type == 'brief':
            return f"AI-generated case brief analyzing {case_name}. This comprehensive analysis examines the legal issues, court reasoning, and practical implications of this California appellate court decision, presented in accessible language for legal professionals."
        
        elif source_type == 'special':
            return f"Special legal analysis examining {case_name}. This in-depth commentary provides expert insights into California probate law, appellate procedure, and legal practice considerations relevant to contemporary legal issues."
        
        return f"Professional legal analysis of {case_name}, providing expert examination of California appellate court decisions and their impact on legal practice."
    
    def load_all_content(self):
        """Load content from all available sources with AI description priority"""
        print("\n📖 Loading content from all sources with AI description priority...")
        
        # Load case briefs first (for AI descriptions)
        self.load_case_briefs()
        
        # Load podcast episodes
        self.load_podcast_episodes()
        
        # Load processed cases
        self.load_processed_cases()
        
        # Load special editions
        self.load_special_editions()
        
        # Remove duplicates and sort
        self.deduplicate_and_sort()
        
        # Calculate enhanced statistics
        self.calculate_enhanced_statistics()
        
    def load_case_briefs(self):
        """Load case briefs from processed_briefs.json"""
        if not self.briefs_file.exists():
            print(f"⚠️  Briefs file not found: {self.briefs_file}")
            self.briefs_data = {}
            return
            
        try:
            with open(self.briefs_file, 'r', encoding='utf-8') as f:
                self.briefs_data = json.load(f)
                
            print(f"📊 Found {len(self.briefs_data)} case briefs")
            print(f"🤖 AI descriptions available: {len([b for b in self.briefs_data.values() if b.get('description_generated')])}")
            
            for brief_key, brief_info in self.briefs_data.items():
                episode = self.convert_case_brief(brief_key, brief_info)
                if episode:
                    self.all_episodes.append(episode)
                    
        except Exception as e:
            print(f"❌ Error loading case briefs: {e}")
            self.briefs_data = {}
    
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
    
    def load_special_editions(self):
        """Load special editions from special_edition directory"""
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
        """Convert podcast episode from logs to website format with AI descriptions"""
        try:
            file_info = case_info.get('file_info', {})
            enhanced_info = case_info.get('enhanced_case_info', {})
            
            # Determine case name
            case_name = enhanced_info.get('case_name', '')
            if not case_name or case_name == 'Unknown':
                case_mapping = {
                    'B333052': 'Conservatorship of ANNE S',
                    'G063155': 'Estate of LAYLA BOYAJIAN',
                    'B341750': 'Conservatorship of Julie C',
                    'B330596': 'Nelson v Huhn',
                    'D085918': 'Estate of EDEN AHBEZ',
                    'B341350': 'In re Dominic H',
                    'C102321': 'Conservatorship of the Person of C',
                    'S282314': 'In re Discipline'
                }
                
                if case_key in case_mapping:
                    case_name = case_mapping[case_key]
                else:
                    case_name = 'Unknown'
            
            # Basic episode info
            episode = {
                'id': len(self.all_episodes) + 1,
                'type': 'opinion',
                'title': f"Case {case_key} - {case_name}" if case_name != 'Unknown' else f"Case {case_key}",
                'court': enhanced_info.get('court', 'California Appellate Court'),
                'date': enhanced_info.get('date', case_info.get('processed_date', '2025-07-13')[:10]),
                'caseNumber': case_key,
                'description': self.get_enhanced_description(case_key, {'case_name': case_name, **enhanced_info}, 'podcast'),
                'audioUrl': '#',
                'textUrl': '#',
                'pdfUrl': '',
                'duration': 'N/A',
                'keywords': ['probate', 'California', 'appellate', case_key.lower()],
                'source': 'podcast'
            }
            
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
            
            # Find PDF URL for this case
            episode['pdfUrl'] = self.find_pdf_url(case_key, case_name)
                    
            return episode
            
        except Exception as e:
            print(f"⚠️  Error converting podcast episode {case_key}: {e}")
            return None
    
    def convert_processed_case(self, case_key: str, case_info: Dict) -> Optional[Dict]:
        """Convert processed case to website format with AI descriptions"""
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
                'description': self.get_enhanced_description(case_key, {'case_name': case_name, **case_info}, 'processed_case'),
                'audioUrl': '#',
                'textUrl': '#',
                'pdfUrl': self.find_pdf_url(case_key, case_name),
                'duration': 'PDF',
                'keywords': ['probate', 'California', 'appellate', case_key.lower(), 'pdf'],
                'source': 'processed_case'
            }
            
            return episode
            
        except Exception as e:
            print(f"⚠️  Error converting processed case {case_key}: {e}")
            return None
    
    def convert_case_brief(self, brief_key: str, brief_info: Dict) -> Optional[Dict]:
        """Convert case brief to website format with AI descriptions"""
        try:
            case_number = brief_info.get('case_number', 'Unknown')
            case_name = brief_info.get('case_name', f"Case {case_number}")
            
            # Skip excluded cases
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
                'description': self.get_enhanced_description(case_number, brief_info, 'brief'),
                'audioUrl': '#',
                'textUrl': '#',
                'pdfUrl': '',
                'duration': 'N/A',
                'keywords': ['case brief', 'probate', 'California', 'analysis', case_number.lower()],
                'source': 'case_brief'
            }
            
            # Convert file path to web path
            original_file_path = brief_info.get('file_path', '')
            episode['textUrl'] = self.convert_to_web_path(original_file_path, case_number)
            
            # Find related PDF and original text files
            episode['pdfUrl'] = self.find_pdf_url(case_number, case_name)
            episode['originalTextUrl'] = self.find_original_text_url(case_number, case_name)
            
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
    
    def calculate_enhanced_statistics(self):
        """Calculate enhanced episode statistics including AI descriptions"""
        self.stats['total'] = len(self.all_episodes)
        self.stats['opinions'] = len([ep for ep in self.all_episodes if ep['type'] == 'opinion'])
        self.stats['briefs'] = len([ep for ep in self.all_episodes if ep['type'] == 'brief'])
        self.stats['analysis'] = len([ep for ep in self.all_episodes if ep['type'] == 'analysis'])
        self.stats['with_audio'] = len([ep for ep in self.all_episodes if ep['audioUrl'] != '#'])
        self.stats['with_descriptions'] = len([ep for ep in self.all_episodes if ep.get('description') and len(ep['description']) > 50])
        
        # Count AI-generated descriptions
        ai_description_count = 0
        for episode in self.all_episodes:
            case_id = episode.get('caseNumber', '')
            if case_id in getattr(self, 'briefs_data', {}):
                if self.briefs_data[case_id].get('description_generated'):
                    ai_description_count += 1
        
        self.stats['with_ai_descriptions'] = ai_description_count
        
        print(f"📊 Enhanced Statistics:")
        print(f"    Total Episodes: {self.stats['total']}")
        print(f"    Opinions: {self.stats['opinions']}")
        print(f"    Briefs: {self.stats['briefs']}")
        print(f"    Analysis: {self.stats['analysis']}")
        print(f"    With Audio: {self.stats['with_audio']}")
        print(f"    With Descriptions: {self.stats['with_descriptions']}")
        print(f"    🤖 With AI Descriptions: {self.stats['with_ai_descriptions']}")
    
    def update_website(self):
        """Update the website HTML with enhanced episode data and descriptions"""
        try:
            print(f"\n🔧 Updating website HTML with AI descriptions...")
            
            if not self.index_html_file.exists():
                print(f"❌ HTML file not found: {self.index_html_file}")
                return False
                
            with open(self.index_html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Create backup
            backup_file = self.index_html_file.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
            import shutil
            shutil.copy2(self.index_html_file, backup_file)
            
            # Convert episodes to JavaScript format
            episodes_js = json.dumps(self.all_episodes, indent=8)
            
            # Replace episodes array in HTML
            pattern = r'const episodes = \[.*?\];'
            replacement = f'const episodes = {episodes_js};'
            
            updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
            
            # Update statistics in HTML
            updated_html = re.sub(
                r'<div class="stat-number" id="totalEpisodes">\d+\+?</div>',
                f'<div class="stat-number" id="totalEpisodes">{self.stats["total"]}+</div>',
                updated_html
            )
            
            updated_html = re.sub(
                r'<div class="stat-number" id="appealateOpinions">\d+\+?</div>',
                f'<div class="stat-number" id="appealateOpinions">{self.stats["opinions"]}+</div>',
                updated_html
            )
            
            updated_html = re.sub(
                r'<div class="stat-number" id="caseBriefs">\d+\+?</div>',
                f'<div class="stat-number" id="caseBriefs">{self.stats["briefs"]}+</div>',
                updated_html
            )
            
            updated_html = re.sub(
                r'<div class="stat-number" id="legalAnalysis">\d+\+?</div>',
                f'<div class="stat-number" id="legalAnalysis">{self.stats["analysis"]}+</div>',
                updated_html
            )
            
            # Write updated HTML
            with open(self.index_html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"✅ Website HTML updated successfully with AI descriptions!")
            print(f"    Episodes: {self.stats['total']}")
            print(f"    With descriptions: {self.stats['with_descriptions']}")
            print(f"    🤖 With AI descriptions: {self.stats['with_ai_descriptions']}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating website HTML: {e}")
            return False

def main():
    """Main function to run the enhanced website updater"""
    print("🚀 ENHANCED WEBSITE UPDATER WITH AI DESCRIPTIONS")
    print("   AI-generated descriptions prioritized for professional content")
    print("="*60)
    
    try:
        # Create updater instance
        updater = EnhancedWebsiteUpdater()
        
        # Load all content with AI description priority
        updater.load_all_content()
        
        # Check if we have episodes to update
        if not updater.all_episodes:
            print("⚠️  No episodes found - website will not be updated")
            return False
        
        # Update the website
        success = updater.update_website()
        
        if success:
            print("\n🎉 ENHANCED WEBSITE UPDATE WITH AI DESCRIPTIONS COMPLETED!")
            print("="*60)
            return True
        else:
            print("\n❌ Website update failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Critical error in enhanced website updater: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)