#!/usr/bin/env python3
"""
Comprehensive Website Updater - ProBrep.com Edition
Advanced content processing with ProBrep.com deployment
Includes multi-source integration, AI descriptions, and JavaScript fixing
"""

import os
import sys
import json
import logging
import ftplib
import argparse
from pathlib import Path
from datetime import datetime
import re

class ComprehensiveWebsiteUpdaterProBrep:
    def __init__(self, no_deploy=False):
        self.base_dir = Path(__file__).parent
        self.podcast_dir = self.base_dir.parent
        self.no_deploy = no_deploy
        self.setup_logging()
        
    def setup_logging(self):
        """Configure comprehensive logging"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"comprehensive_updater_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_ftp_config(self):
        """Load ProBrep.com FTP configuration"""
        try:
            config_path = self.base_dir / "godaddy_config.json"
            if not config_path.exists():
                raise FileNotFoundError("FTP configuration file not found")
                
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load FTP configuration: {e}")
            return None

    def load_all_episodes(self):
        """Load episodes from all JSON databases"""
        all_episodes = []
        
        # Database sources with their processing methods
        databases = [
            {
                'path': self.podcast_dir / "logs" / "processed_cases.json",
                'type': 'podcast_episodes',
                'priority': 1
            },
            {
                'path': self.podcast_dir / "probate_cases" / "processed_cases.json", 
                'type': 'all_cases',
                'priority': 2
            },
            {
                'path': self.podcast_dir / "probate_cases" / "processed_briefs.json",
                'type': 'case_briefs',
                'priority': 3
            }
        ]
        
        for db_info in databases:
            if db_info['path'].exists():
                try:
                    with open(db_info['path'], 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        episodes = self._process_database(data, db_info)
                        all_episodes.extend(episodes)
                        self.logger.info(f"Loaded {len(episodes)} episodes from {db_info['path'].name}")
                except Exception as e:
                    self.logger.error(f"Failed to load {db_info['path']}: {e}")
        
        # Deduplicate and sort episodes
        unique_episodes = self._deduplicate_episodes(all_episodes)
        sorted_episodes = sorted(unique_episodes, key=lambda x: x.get('date', ''), reverse=True)
        
        self.logger.info(f"Total unique episodes processed: {len(sorted_episodes)}")
        return sorted_episodes
        
    def _process_database(self, data, db_info):
        """Process database into episode format"""
        episodes = []
        
        if db_info['type'] == 'podcast_episodes':
            # Process podcast episodes from logs/processed_cases.json
            for case_id, case_data in data.items():
                if isinstance(case_data, dict) and 'podbean_url' in case_data:
                    episode = self._create_episode_from_podcast(case_id, case_data)
                    if episode:
                        episodes.append(episode)
                        
        elif db_info['type'] == 'all_cases':
            # Process all cases from probate_cases/processed_cases.json
            for case_id, case_data in data.items():
                if isinstance(case_data, dict):
                    episode = self._create_episode_from_case(case_id, case_data)
                    if episode:
                        episodes.append(episode)
                        
        elif db_info['type'] == 'case_briefs':
            # Process case briefs from processed_briefs.json
            for case_id, brief_data in data.items():
                if isinstance(brief_data, dict):
                    episode = self._create_episode_from_brief(case_id, brief_data)
                    if episode:
                        episodes.append(episode)
        
        return episodes
        
    def _create_episode_from_podcast(self, case_id, case_data):
        """Create episode object from podcast data"""
        try:
            title = case_data.get('title', case_id)
            
            # Generate AI description
            description = self._generate_ai_description(case_data, 'podcast')
            
            episode = {
                'id': len(self.episodes) + 1 if hasattr(self, 'episodes') else 1,
                'type': 'opinion',
                'title': self._clean_title(title),
                'court': case_data.get('court', 'California Appellate Court'),
                'date': case_data.get('date', datetime.now().strftime('%Y-%m-%d')),
                'caseNumber': case_id,
                'description': description,
                'audioUrl': case_data.get('podbean_url', ''),
                'textUrl': f'texts/{case_id}.txt',
                'pdfUrl': f'pdfs/published/{case_id}.pdf',
                'duration': case_data.get('duration', 'Unknown'),
                'keywords': self._extract_keywords(title, description),
                'source': 'podcast'
            }
            
            return episode
            
        except Exception as e:
            self.logger.error(f"Failed to create episode from podcast data {case_id}: {e}")
            return None
            
    def _create_episode_from_case(self, case_id, case_data):
        """Create episode object from case data"""
        try:
            title = case_data.get('title', case_id)
            
            # Generate AI description
            description = self._generate_ai_description(case_data, 'case')
            
            episode = {
                'id': len(self.episodes) + 1 if hasattr(self, 'episodes') else 1,
                'type': 'opinion',
                'title': self._clean_title(title),
                'court': 'California Appellate Court',
                'date': case_data.get('processed_date', datetime.now().strftime('%Y-%m-%d')),
                'caseNumber': case_id,
                'description': description,
                'audioUrl': '',  # No audio for case-only entries
                'textUrl': f'texts/{case_id}.txt',
                'pdfUrl': f'pdfs/published/{case_id}.pdf',
                'duration': 'Document Only',
                'keywords': self._extract_keywords(title, description),
                'source': 'case'
            }
            
            return episode
            
        except Exception as e:
            self.logger.error(f"Failed to create episode from case data {case_id}: {e}")
            return None
            
    def _create_episode_from_brief(self, case_id, brief_data):
        """Create episode object from brief data"""
        try:
            title = f"Brief: {brief_data.get('title', case_id)}"
            
            # Generate AI description
            description = self._generate_ai_description(brief_data, 'brief')
            
            episode = {
                'id': len(self.episodes) + 1 if hasattr(self, 'episodes') else 1,
                'type': 'brief',
                'title': self._clean_title(title),
                'court': 'California Appellate Court',
                'date': brief_data.get('created_date', datetime.now().strftime('%Y-%m-%d')),
                'caseNumber': case_id,
                'description': description,
                'audioUrl': brief_data.get('audio_url', ''),
                'textUrl': f'texts/brief_{case_id}.txt',
                'pdfUrl': f'pdfs/published/{case_id}.pdf',
                'duration': brief_data.get('duration', 'Unknown'),
                'keywords': self._extract_keywords(title, description),
                'source': 'brief'
            }
            
            return episode
            
        except Exception as e:
            self.logger.error(f"Failed to create episode from brief data {case_id}: {e}")
            return None
            
    def _generate_ai_description(self, data, source_type):
        """Generate professional AI description for episode"""
        # This would integrate with Ollama LLaMA3 for actual AI generation
        # For now, create template-based descriptions
        
        templates = {
            'podcast': "This episode presents a comprehensive analysis of {title}, examining the legal precedents and judicial reasoning. The case addresses important questions in California probate law with implications for estate planning and inheritance disputes.",
            'case': "A detailed examination of {title}, providing insights into California appellate court reasoning and legal standards. This case contributes to the evolving landscape of probate and estate law in California.",
            'brief': "An AI-generated analysis of {title}, offering concise legal insights and key takeaways. This brief examines the essential legal principles and their practical applications in probate practice."
        }
        
        template = templates.get(source_type, templates['case'])
        title = data.get('title', 'this important case')
        
        description = template.format(title=title)
        
        # Add case-specific details if available
        if 'summary' in data:
            description += f" {data['summary'][:200]}..."
            
        return description
        
    def _clean_title(self, title):
        """Clean and standardize episode titles"""
        if not title:
            return "Untitled Case"
            
        # Remove common file extensions and artifacts
        title = re.sub(r'\.(pdf|txt|mp3)$', '', title, flags=re.IGNORECASE)
        
        # Clean up common patterns
        title = re.sub(r'_published|_unpublished', '', title)
        title = re.sub(r'_+', ' ', title)  # Replace underscores with spaces
        title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
        
        # Capitalize properly
        title = title.strip().title()
        
        return title
        
    def _extract_keywords(self, title, description):
        """Extract relevant keywords from title and description"""
        keywords = ['probate', 'California', 'appellate']
        
        # Common legal terms to look for
        legal_terms = [
            'estate', 'inheritance', 'will', 'trust', 'conservatorship',
            'guardianship', 'probate', 'appellate', 'court', 'appeal',
            'judgment', 'ruling', 'decision', 'opinion'
        ]
        
        text = f"{title} {description}".lower()
        
        for term in legal_terms:
            if term in text and term not in keywords:
                keywords.append(term)
                
        return keywords[:10]  # Limit to 10 keywords
        
    def _deduplicate_episodes(self, episodes):
        """Remove duplicate episodes based on case number"""
        seen_cases = set()
        unique_episodes = []
        
        for episode in episodes:
            case_number = episode.get('caseNumber', '')
            if case_number and case_number not in seen_cases:
                seen_cases.add(case_number)
                unique_episodes.append(episode)
                
        return unique_episodes
        
    def update_website_content(self):
        """Update website HTML with processed episodes"""
        try:
            # Load all episodes
            episodes = self.load_all_episodes()
            self.episodes = episodes  # Store for use in other methods
            
            # Generate statistics
            stats = self._calculate_statistics(episodes)
            
            # Update HTML file
            self._update_html_file(episodes, stats)
            
            self.logger.info(f"Website content updated with {len(episodes)} episodes")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update website content: {e}")
            return False
            
    def _calculate_statistics(self, episodes):
        """Calculate website statistics"""
        stats = {
            'total_episodes': len(episodes),
            'opinions': len([e for e in episodes if e.get('type') == 'opinion']),
            'briefs': len([e for e in episodes if e.get('type') == 'brief']),
            'analysis': len([e for e in episodes if e.get('type') == 'analysis']),
            'total_resources': len(episodes) * 3,  # PDF + Text + Audio
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return stats
        
    def _update_html_file(self, episodes, stats):
        """Update index.html with episode data and statistics"""
        html_file = self.base_dir / "index.html"
        
        if not html_file.exists():
            self.logger.error("index.html not found - creating new file")
            self._create_html_template()
            
        # Read current HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Generate JavaScript episodes array
        js_episodes = self._generate_javascript_episodes(episodes)
        
        # Fix JavaScript syntax
        js_episodes = self._fix_javascript_syntax(js_episodes)
        
        # Update episodes in HTML
        episode_pattern = r'const episodes = \[.*?\];'
        replacement = f'const episodes = {js_episodes};'
        
        html_content = re.sub(episode_pattern, replacement, html_content, flags=re.DOTALL)
        
        # Update statistics
        for stat_key, stat_value in stats.items():
            pattern = f'(?<=id="{stat_key}">)[^<]*'
            html_content = re.sub(pattern, str(stat_value), html_content)
            
        # Write updated HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        self.logger.info("HTML file updated successfully")
        
    def _generate_javascript_episodes(self, episodes):
        """Generate JavaScript episodes array"""
        js_episodes = []
        
        for episode in episodes:
            js_episode = {
                'id': episode.get('id', 0),
                'type': episode.get('type', 'opinion'),
                'title': episode.get('title', ''),
                'court': episode.get('court', ''),
                'date': episode.get('date', ''),
                'caseNumber': episode.get('caseNumber', ''),
                'description': episode.get('description', ''),
                'audioUrl': episode.get('audioUrl', ''),
                'textUrl': episode.get('textUrl', ''),
                'pdfUrl': episode.get('pdfUrl', ''),
                'duration': episode.get('duration', ''),
                'keywords': episode.get('keywords', []),
                'source': episode.get('source', '')
            }
            js_episodes.append(js_episode)
            
        return json.dumps(js_episodes, indent=2, ensure_ascii=False)
        
    def _fix_javascript_syntax(self, js_content):
        """Fix common JavaScript syntax issues"""
        # Remove trailing commas in objects and arrays
        js_content = re.sub(r',(\s*[}\]])', r'\1', js_content)
        
        # Ensure proper string escaping
        js_content = js_content.replace('\\"', '"')
        js_content = js_content.replace("'", "\\'")
        
        # Add missing semicolons where needed
        if not js_content.strip().endswith(';'):
            js_content = js_content.rstrip() + ';'
            
        return js_content
        
    def _create_html_template(self):
        """Create basic HTML template if file doesn't exist"""
        template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>California Probate Repository</title>
</head>
<body>
    <div id="total_episodes">0</div>
    <script>
        const episodes = [];
    </script>
</body>
</html>"""
        
        with open(self.base_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(template)
            
    def deploy_to_probrep(self):
        """Deploy website to ProBrep.com via FTP"""
        if self.no_deploy:
            self.logger.info("Deployment skipped (--no-deploy flag)")
            return True
            
        try:
            config = self.load_ftp_config()
            if not config:
                return False
                
            self.logger.info("Starting ProBrep.com deployment...")
            
            # Connect to FTP
            ftp = ftplib.FTP(config['ftp_host'])
            ftp.login(config['ftp_username'], config['ftp_password'])
            
            # Upload files
            self._upload_directory_ftp(ftp, self.base_dir, '/')
            
            ftp.quit()
            
            self.logger.info("ProBrep.com deployment completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"ProBrep.com deployment failed: {e}")
            return False
            
    def _upload_directory_ftp(self, ftp, local_dir, remote_dir):
        """Recursively upload directory to FTP"""
        for item in local_dir.iterdir():
            if item.is_file():
                remote_path = remote_dir + item.name
                try:
                    with open(item, 'rb') as f:
                        ftp.storbinary(f'STOR {remote_path}', f)
                    self.logger.info(f"Uploaded: {item.name}")
                except Exception as e:
                    self.logger.error(f"Failed to upload {item.name}: {e}")
            elif item.is_dir() and item.name not in ['.git', '__pycache__', 'logs']:
                remote_subdir = remote_dir + item.name + '/'
                try:
                    ftp.mkd(remote_subdir)
                except:
                    pass  # Directory might already exist
                self._upload_directory_ftp(ftp, item, remote_subdir)
                
    def run_comprehensive_update(self):
        """Run complete update process"""
        try:
            self.logger.info("=== Comprehensive Website Update - ProBrep.com Edition ===")
            
            # Update website content
            if not self.update_website_content():
                self.logger.error("Website content update failed")
                return False
                
            # Deploy to ProBrep.com
            if not self.deploy_to_probrep():
                self.logger.error("ProBrep.com deployment failed")
                return False
                
            self.logger.info("Comprehensive update completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Comprehensive update failed: {e}")
            return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Comprehensive Website Updater - ProBrep.com Edition')
    parser.add_argument('--no-deploy', action='store_true', 
                       help='Update content only, skip deployment')
    
    args = parser.parse_args()
    
    updater = ComprehensiveWebsiteUpdaterProBrep(no_deploy=args.no_deploy)
    
    success = updater.run_comprehensive_update()
    
    if success:
        print("Comprehensive Website Update - SUCCESS")
        exit(0)
    else:
        print("Comprehensive Website Update - FAILED") 
        exit(1)


if __name__ == "__main__":
    main()
