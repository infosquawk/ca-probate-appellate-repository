#!/usr/bin/env python3
"""
Updated Website Integration Pipeline for GoDaddy Hosting
Replaces GitHub Pages deployment with GoDaddy FTP deployment
"""

import os
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add the godaddy_initiation_scripts directory to the path
sys.path.append(str(Path(__file__).parent))

# Import the new GoDaddy deployment module
from godaddy_deployment_pipeline import GoDaddyDeploymentPipeline

class WebsiteIntegrationPipelineGoDaddy:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # Go up to website directory
        self.podcast_dir = self.base_dir.parent
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for Phase 5"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"phase5_godaddy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def execute_phase_5(self):
        """
        Main execution function for Phase 5 with GoDaddy deployment
        Returns: bool - Success status
        """
        try:
            self.logger.info("=== Phase 5: Website Integration & GoDaddy Deployment ===")
            
            # Step 1: Content Synchronization
            self.logger.info("Step 1: Synchronizing content files...")
            if not self.sync_content_files():
                return False
                
            # Step 2: Website Content Update
            self.logger.info("Step 2: Updating website content...")
            if not self.update_website_content():
                return False
                
            # Step 3: GoDaddy Deployment (replaces GitHub deployment)
            self.logger.info("Step 3: Deploying to GoDaddy hosting...")
            if not self.deploy_to_godaddy():
                return False
                
            # Step 4: Verification
            self.logger.info("Step 4: Verifying deployment...")
            if not self.verify_deployment():
                self.logger.warning("Deployment verification failed - manual check recommended")
                
            self.logger.info("Phase 5 completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Phase 5 failed with exception: {e}")
            return False

    def sync_content_files(self):
        """Synchronize all content from pipeline to website directories"""
        try:
            # Sync covers
            self._sync_covers()
            
            # Sync PDFs
            self._sync_pdfs()
            
            # Sync text files
            self._sync_texts()
            
            self.logger.info("Content synchronization completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Content synchronization failed: {e}")
            return False

    def _sync_covers(self):
        """Copy cover images from podcast directory"""
        covers_dir = self.base_dir / "covers"
        covers_dir.mkdir(exist_ok=True)
        
        cover_files = [
            "cover.png",
            "cover_briefing.png", 
            "cover_special_edition.png"
        ]
        
        for cover_file in cover_files:
            src = self.podcast_dir / cover_file
            dst = covers_dir / cover_file
            if src.exists():
                shutil.copy2(src, dst)
                self.logger.info(f"Copied {cover_file}")

    def _sync_pdfs(self):
        """Copy PDF documents to website"""
        src_pdf_dir = self.podcast_dir / "probate_cases" / "pdfs"
        dst_pdf_dir = self.base_dir / "pdfs"
        
        if src_pdf_dir.exists():
            if dst_pdf_dir.exists():
                shutil.rmtree(dst_pdf_dir)
            shutil.copytree(src_pdf_dir, dst_pdf_dir)
            self.logger.info("PDF documents synchronized")

    def _sync_texts(self):
        """Copy text files to website"""
        # Sync published text files
        src_text_dir = self.podcast_dir / "probate_cases" / "pdfs" / "published_text"
        dst_text_dir = self.base_dir / "texts"
        dst_text_dir.mkdir(exist_ok=True)
        
        if src_text_dir.exists():
            for txt_file in src_text_dir.glob("*.txt"):
                shutil.copy2(txt_file, dst_text_dir / txt_file.name)
        
        # Sync case briefs
        src_briefs_dir = self.podcast_dir / "podcast" / "case_briefs"
        if src_briefs_dir.exists():
            for brief_file in src_briefs_dir.glob("*.txt"):
                shutil.copy2(brief_file, dst_text_dir / f"brief_{brief_file.name}")
                
        self.logger.info("Text files synchronized")

    def update_website_content(self):
        """Update website content and URLs for GoDaddy hosting"""
        try:
            # Load data from all JSON sources
            databases = [
                self.podcast_dir / "logs" / "processed_cases.json",
                self.podcast_dir / "probate_cases" / "processed_cases.json", 
                self.podcast_dir / "probate_cases" / "processed_briefs.json"
            ]
            
            all_episodes = []
            for db_path in databases:
                if db_path.exists():
                    with open(db_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        episodes = self._convert_to_episodes(data, db_path.name)
                        all_episodes.extend(episodes)
            
            # Update website HTML with GoDaddy URLs
            self._update_html_with_episodes(all_episodes)
            
            # Update any hardcoded GitHub URLs to GoDaddy URLs
            self._update_urls_for_godaddy()
            
            self.logger.info(f"Website updated with {len(all_episodes)} episodes for GoDaddy hosting")
            return True
            
        except Exception as e:
            self.logger.error(f"Website content update failed: {e}")
            return False

    def _update_urls_for_godaddy(self):
        """Update any hardcoded URLs from GitHub to ProBRep.com"""
        try:
            # ProBRep.com domain configuration
            new_domain = "https://probrep.com"
            
            # Update index.html with new base URLs if needed
            index_file = self.base_dir / "index.html"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace any GitHub URLs with ProBRep.com URLs
                old_github_url = "https://infosquawk.github.io/ca-probate-appellate-repository"
                content = content.replace(old_github_url, new_domain)
                
                # Update any other GitHub references
                github_patterns = [
                    "infosquawk.github.io/ca-probate-appellate-repository",
                    "github.io/ca-probate-appellate-repository"
                ]
                
                for pattern in github_patterns:
                    content = content.replace(pattern, "probrep.com")
                
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"Updated URLs to use ProBRep.com domain: {new_domain}")
            
        except Exception as e:
            self.logger.warning(f"URL update failed: {e}")

    def _convert_to_episodes(self, data, source_db):
        """Convert JSON data to episode format"""
        episodes = []
        # Implementation depends on specific JSON structure
        # This would contain the logic from comprehensive_website_updater.py
        # but adapted for GoDaddy hosting
        
        # Basic implementation - you may need to adapt this based on your actual JSON structure
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'title' in value:
                    episode = {
                        'id': key,
                        'title': value.get('title', ''),
                        'description': value.get('description', ''),
                        'audioUrl': value.get('audioUrl', ''),
                        'source': source_db
                    }
                    episodes.append(episode)
        
        return episodes

    def _update_html_with_episodes(self, episodes):
        """Update index.html with episode data"""
        # Implementation would update the HTML file with new episode data
        # This is a placeholder - you would implement the actual HTML update logic here
        self.logger.info(f"HTML update placeholder - {len(episodes)} episodes ready for integration")

    def deploy_to_godaddy(self):
        """Execute GoDaddy deployment using the dedicated deployment pipeline"""
        try:
            # Use the GoDaddy deployment pipeline
            deployer = GoDaddyDeploymentPipeline()
            success = deployer.deploy_to_godaddy()
            
            if success:
                self.logger.info("GoDaddy deployment completed successfully")
                return True
            else:
                self.logger.error("GoDaddy deployment failed")
                return False
                
        except Exception as e:
            self.logger.error(f"GoDaddy deployment exception: {e}")
            return False

    def verify_deployment(self):
        """Verify deployment was successful"""
        try:
            # Basic verification - check if key files exist locally
            # (Remote verification would require additional HTTP checks)
            required_files = ["index.html", "covers/cover.png"]
            
            for file_path in required_files:
                if not (self.base_dir / file_path).exists():
                    self.logger.error(f"Required file missing: {file_path}")
                    return False
            
            # Could add HTTP verification to check if site is live
            self.logger.info("Local file verification passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Deployment verification failed: {e}")
            return False


def main():
    """Main execution function for Phase 5 with GoDaddy"""
    pipeline = WebsiteIntegrationPipelineGoDaddy()
    
    success = pipeline.execute_phase_5()
    
    if success:
        print("Phase 5: Website Integration & GoDaddy Deployment - SUCCESS")
        exit(0)
    else:
        print("Phase 5: Website Integration & GoDaddy Deployment - FAILED")
        exit(1)


if __name__ == "__main__":
    main()
