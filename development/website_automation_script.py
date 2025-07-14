#!/usr/bin/env python3
"""
Website Automation Script for California Probate Code Appellate Case Information Repository

This script reads the podcast pipeline databases and automatically updates the website
with new episodes. It integrates with the existing GitHub workflow.

Author: Scholar Podcast System
Date: 2025-07-13
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

class WebsiteAutomation:
    def __init__(self):
        # Configuration - adjust paths as needed
        self.scholar_podcast_dir = Path(__file__).parent.parent
        self.website_dir = Path(__file__).parent
        self.processed_cases_file = self.scholar_podcast_dir / "logs" / "processed_cases.json"
        self.special_editions_file = self.scholar_podcast_dir / "special_edition" / "processed_special_editions.json"
        self.index_html_file = self.website_dir / "index.html"
        
        # GitHub configuration
        self.github_repo_path = r"C:\Users\Ryan\GitHub\ca-probate-appellate-repository"
        self.github_username = "infosquawk"
        self.github_repository = "ca-probate-appellate-repository"
        
    def load_episode_databases(self):
        """Load episodes from both database files"""
        episodes = []
        
        # Load regular cases
        if self.processed_cases_file.exists():
            try:
                with open(self.processed_cases_file, 'r', encoding='utf-8') as f:
                    cases_data = json.load(f)
                    episodes.extend(self.convert_cases_to_episodes(cases_data))
            except Exception as e:
                print(f"Error loading processed cases: {e}")
        
        # Load special editions
        if self.special_editions_file.exists():
            try:
                with open(self.special_editions_file, 'r', encoding='utf-8') as f:
                    special_data = json.load(f)
                    episodes.extend(self.convert_special_to_episodes(special_data))
            except Exception as e:
                print(f"Error loading special editions: {e}")
        
        return episodes
    
    def convert_cases_to_episodes(self, cases_data):
        """Convert cases database to episode format"""
        episodes = []
        episode_id = 1
        
        for case_file, case_info in cases_data.items():
            # Determine episode type based on file naming or content
            episode_type = 'brief' if 'brief' in case_file.lower() else 'opinion'
            
            episode = {
                'id': episode_id,
                'type': episode_type,
                'title': self.extract_case_title(case_file),
                'court': self.extract_court_info(case_info),
                'date': case_info.get('date_processed', datetime.now().strftime('%Y-%m-%d')),
                'caseNumber': self.extract_case_number(case_file),
                'description': self.generate_description(case_info, episode_type),
                'audioUrl': case_info.get('podcast_url', '#'),
                'textUrl': '#',
                'duration': case_info.get('duration', 'N/A'),
                'keywords': self.extract_keywords(case_file, case_info)
            }
            episodes.append(episode)
            episode_id += 1
        
        return episodes
    
    def convert_special_to_episodes(self, special_data):
        """Convert special editions to episode format"""
        episodes = []
        episode_id = 1000  # Start at 1000 to avoid conflicts
        
        for special_file, special_info in special_data.items():
            episode = {
                'id': episode_id,
                'type': 'analysis',
                'title': self.extract_special_title(special_file),
                'court': 'Legal Analysis Special Edition',
                'date': special_info.get('date_processed', datetime.now().strftime('%Y-%m-%d')),
                'caseNumber': f"Analysis #{episode_id - 999}",
                'description': special_info.get('description', 'Legal analysis and commentary.'),
                'audioUrl': special_info.get('podcast_url', '#'),
                'textUrl': '#',
                'duration': special_info.get('duration', 'N/A'),
                'keywords': self.extract_special_keywords(special_file, special_info)
            }
            episodes.append(episode)
            episode_id += 1
        
        return episodes
    
    def extract_case_title(self, case_file):
        """Extract a readable case title from filename"""
        # Remove file extension and clean up
        title = Path(case_file).stem
        title = re.sub(r'_+', ' ', title)
        title = re.sub(r'-+', ' - ', title)
        title = title.title()
        return title
    
    def extract_court_info(self, case_info):
        """Extract court information"""
        # Look for court info in the case data
        content = case_info.get('content', '')
        if 'Court of Appeal' in content:
            return 'California Court of Appeal'
        elif 'Supreme Court' in content:
            return 'California Supreme Court'
        else:
            return 'California Appellate Court'
    
    def extract_case_number(self, case_file):
        """Extract case number from filename or content"""
        # Look for case number patterns
        case_number_match = re.search(r'(\d{4}[-_]CA[-_]\d+)', case_file)
        if case_number_match:
            return case_number_match.group(1).replace('_', '-')
        return f"Case #{hash(case_file) % 10000}"
    
    def generate_description(self, case_info, episode_type):
        """Generate a professional description"""
        if episode_type == 'brief':
            return "Professional case brief analysis covering key legal principles, procedural requirements, and practical guidance for practitioners."
        else:
            return "Appellate court decision addressing significant issues in California probate law with implications for legal practitioners and estate planning professionals."
    
    def extract_keywords(self, case_file, case_info):
        """Extract relevant keywords"""
        keywords = []
        content = case_info.get('content', '').lower()
        
        # Common probate keywords
        probate_terms = ['probate', 'estate', 'trust', 'guardianship', 'conservatorship', 
                        'will', 'inheritance', 'beneficiary', 'executor', 'administrator']
        
        for term in probate_terms:
            if term in content or term in case_file.lower():
                keywords.append(term)
        
        return keywords[:4]  # Limit to 4 keywords
    
    def extract_special_title(self, special_file):
        """Extract title for special editions"""
        title = Path(special_file).stem
        title = re.sub(r'_+', ' ', title)
        title = title.title()
        return title
    
    def extract_special_keywords(self, special_file, special_info):
        """Extract keywords for special editions"""
        return ['legal analysis', 'commentary', 'special edition', 'probate law']
    
    def update_website_content(self, episodes):
        """Update the website HTML with new episode data"""
        if not self.index_html_file.exists():
            print(f"Website file not found: {self.index_html_file}")
            return False
        
        try:
            with open(self.index_html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert episodes to JavaScript array
            episodes_js = json.dumps(episodes, indent=8)
            
            # Replace the episodes array in the JavaScript
            pattern = r'const episodes = \[.*?\];'
            replacement = f'const episodes = {episodes_js};'
            
            updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
            
            # Update statistics
            total_episodes = len(episodes)
            opinions = len([e for e in episodes if e['type'] == 'opinion'])
            briefs = len([e for e in episodes if e['type'] == 'brief'])
            analysis = len([e for e in episodes if e['type'] == 'analysis'])
            
            # Update stats in HTML
            updated_html = re.sub(r'<div class="stat-number" id="totalEpisodes">\d+\+</div>',
                                f'<div class="stat-number" id="totalEpisodes">{total_episodes}+</div>',
                                updated_html)
            updated_html = re.sub(r'<div class="stat-number" id="appealateOpinions">\d+\+</div>',
                                f'<div class="stat-number" id="appealateOpinions">{opinions}+</div>',
                                updated_html)
            updated_html = re.sub(r'<div class="stat-number" id="caseBriefs">\d+\+</div>',
                                f'<div class="stat-number" id="caseBriefs">{briefs}+</div>',
                                updated_html)
            updated_html = re.sub(r'<div class="stat-number" id="legalAnalysis">\d+\+</div>',
                                f'<div class="stat-number" id="legalAnalysis">{analysis}+</div>',
                                updated_html)
            
            # Write updated content
            with open(self.index_html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print(f"✅ Website updated with {total_episodes} episodes")
            print(f"   - Opinions: {opinions}")
            print(f"   - Briefs: {briefs}")
            print(f"   - Analysis: {analysis}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating website: {e}")
            return False
    
    def git_commit_and_push(self):
        """Commit and push changes to GitHub"""
        try:
            if not os.path.exists(self.github_repo_path):
                print(f"❌ GitHub repository path not found: {self.github_repo_path}")
                return False
            
            os.chdir(self.github_repo_path)
            
            # Git commands
            subprocess.run(['git', 'add', '.'], check=True)
            
            commit_message = f"Automated website update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            subprocess.run(['git', 'push'], check=True)
            
            print(f"✅ Changes pushed to GitHub")
            print(f"🌐 Website will update at: https://{self.github_username}.github.io/{self.github_repository}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Error with git operations: {e}")
            return False
    
    def run_automation(self):
        """Main automation workflow"""
        print("🚀 Starting website automation...")
        print(f"📁 Scholar podcast directory: {self.scholar_podcast_dir}")
        print(f"🌐 Website directory: {self.website_dir}")
        
        # Load episodes from databases
        print("\n📖 Loading episode databases...")
        episodes = self.load_episode_databases()
        
        if not episodes:
            print("⚠️  No episodes found in databases")
            return False
        
        print(f"✅ Loaded {len(episodes)} episodes")
        
        # Update website
        print("\n🔧 Updating website...")
        if not self.update_website_content(episodes):
            return False
        
        # Git operations (optional - uncomment if you want automatic git push)
        # print("\n📤 Pushing to GitHub...")
        # if not self.git_commit_and_push():
        #     return False
        
        print("\n🎉 Website automation completed successfully!")
        return True

def main():
    """Main function to run the automation"""
    automation = WebsiteAutomation()
    success = automation.run_automation()
    
    if success:
        print("\n✅ Automation completed successfully")
    else:
        print("\n❌ Automation failed")
        exit(1)

if __name__ == "__main__":
    main()
