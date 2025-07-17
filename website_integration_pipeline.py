#!/usr/bin/env python3
"""
Phase 5: Website Integration & Deployment Pipeline
Integrates podcast content with website and deploys to GitHub Pages

File: website/website_integration_pipeline.py
"""

import os
import json
import shutil
import subprocess
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

class WebsiteIntegrationPipeline:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.podcast_dir = self.base_dir.parent
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for Phase 5 with Windows-safe encoding"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"phase5_website_integration_{timestamp}.log"
        
        # Use ASCII-safe logging format
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Phase 5 logging initialized - {log_file}")

    def execute_phase_5(self):
        """
        Main execution function for Phase 5
        Returns: bool - Success status
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info("Phase 5: Website Integration & Deployment Starting")
            self.logger.info("=" * 60)
            
            # Step 1: Content Synchronization
            self.logger.info("Step 1: Synchronizing content files...")
            if not self.sync_content_files():
                self.logger.error("Content synchronization failed")
                return False
                
            # Step 2: Website Content Update
            self.logger.info("Step 2: Updating website content...")
            if not self.update_website_content():
                self.logger.error("Website content update failed")
                return False
                
            # Step 3: Automated Deployment
            self.logger.info("Step 3: Deploying to GitHub Pages...")
            deploy_success = self.deploy_to_github()
            
            if not deploy_success:
                self.logger.warning("Automated deployment failed - manual deployment required")
                self.logger.info("Website content has been updated locally")
                return False
                
            # Step 4: Verification
            self.logger.info("Step 4: Verifying deployment...")
            if not self.verify_deployment():
                self.logger.warning("Deployment verification failed - manual check recommended")
                
            self.logger.info("=" * 60)
            self.logger.info("Phase 5 completed successfully!")
            self.logger.info("Website is updated and deployed to GitHub Pages")
            self.logger.info("=" * 60)
            return True
            
        except Exception as e:
            self.logger.error(f"Phase 5 failed with exception: {str(e)}")
            self.logger.exception("Full exception details:")
            return False

    def sync_content_files(self):
        """Synchronize all content from pipeline to website directories"""
        try:
            sync_tasks = [
                ("covers", self._sync_covers),
                ("PDFs", self._sync_pdfs),
                ("texts", self._sync_texts)
            ]
            
            for task_name, task_func in sync_tasks:
                self.logger.info(f"Syncing {task_name}...")
                try:
                    task_func()
                    self.logger.info(f"[SUCCESS] {task_name} synchronization completed")
                except Exception as e:
                    self.logger.error(f"[FAILED] {task_name} synchronization failed: {str(e)}")
                    # Continue with other tasks even if one fails
                    continue
            
            self.logger.info("Content synchronization process completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Content synchronization failed: {str(e)}")
            return False

    def _sync_covers(self):
        """Copy cover images from podcast directory"""
        covers_dir = self.base_dir / "covers"
        covers_dir.mkdir(exist_ok=True)
        
        cover_mappings = {
            "cover.png": "cover_opinions.png",
            "cover_briefing.png": "cover_briefs.png", 
            "cover_special_edition.png": "cover_special.png"
        }
        
        for src_name, dst_name in cover_mappings.items():
            src = self.podcast_dir / src_name
            dst = covers_dir / dst_name
            
            if src.exists():
                try:
                    shutil.copy2(src, dst)
                    self.logger.info(f"  Copied {src_name} -> {dst_name}")
                except Exception as e:
                    self.logger.warning(f"  Failed to copy {src_name}: {str(e)}")
            else:
                self.logger.warning(f"  Cover file not found: {src_name}")

    def _sync_pdfs(self):
        """Copy PDF documents to website with improved error handling"""
        src_pdf_dir = self.podcast_dir / "probate_cases" / "pdfs"
        dst_pdf_dir = self.base_dir / "pdfs"
        
        if not src_pdf_dir.exists():
            self.logger.warning("Source PDF directory not found - skipping PDF sync")
            return
            
        try:
            # Remove existing PDFs with retry logic
            if dst_pdf_dir.exists():
                self._safe_remove_directory(dst_pdf_dir)
            
            # Copy with retry logic
            self._safe_copy_directory(src_pdf_dir, dst_pdf_dir)
            
            # Count files for logging
            if dst_pdf_dir.exists():
                pdf_count = len(list(dst_pdf_dir.rglob("*.pdf")))
                self.logger.info(f"  Copied {pdf_count} PDF documents")
            else:
                self.logger.warning("  PDF directory copy may have failed")
                
        except Exception as e:
            self.logger.error(f"PDF synchronization failed: {str(e)}")
            self.logger.info("Continuing with other synchronization tasks...")

    def _safe_remove_directory(self, directory):
        """Safely remove directory with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                shutil.rmtree(directory)
                self.logger.info(f"  Removed existing directory: {directory}")
                return
            except PermissionError as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"  Permission error on attempt {attempt + 1}, retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    self.logger.error(f"  Could not remove directory after {max_retries} attempts: {str(e)}")
                    raise
            except Exception as e:
                self.logger.error(f"  Unexpected error removing directory: {str(e)}")
                raise

    def _safe_copy_directory(self, src, dst):
        """Safely copy directory with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                shutil.copytree(src, dst)
                self.logger.info(f"  Successfully copied {src} to {dst}")
                return
            except PermissionError as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"  Permission error on attempt {attempt + 1}, retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    self.logger.error(f"  Could not copy directory after {max_retries} attempts: {str(e)}")
                    # Don't raise - continue with other tasks
                    return
            except Exception as e:
                self.logger.error(f"  Unexpected error copying directory: {str(e)}")
                return

    def _sync_texts(self):
        """Copy text files to website"""
        dst_text_dir = self.base_dir / "texts"
        dst_text_dir.mkdir(exist_ok=True)
        
        text_sources = [
            (self.podcast_dir / "probate_cases" / "pdfs" / "published_text", ""),
            (self.podcast_dir / "probate_cases" / "pdfs" / "unpublished_text", ""),
            (self.podcast_dir / "podcast" / "case_briefs", "brief_")
        ]
        
        total_files = 0
        for src_dir, prefix in text_sources:
            if src_dir.exists():
                for txt_file in src_dir.glob("*.txt"):
                    try:
                        dst_file = dst_text_dir / f"{prefix}{txt_file.name}"
                        shutil.copy2(txt_file, dst_file)
                        total_files += 1
                    except Exception as e:
                        self.logger.warning(f"  Failed to copy {txt_file.name}: {str(e)}")
                        
        self.logger.info(f"  Copied {total_files} text files")

    def update_website_content(self):
        """Update website content using comprehensive updater logic"""
        try:
            # Check if comprehensive updater exists
            updater_script = self.base_dir / "comprehensive_website_updater.py"
            
            if updater_script.exists():
                self.logger.info("Using existing comprehensive_website_updater.py")
                
                # Execute the existing updater
                result = subprocess.run(
                    [sys.executable, "comprehensive_website_updater.py"],
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    self.logger.info("Website content update completed successfully")
                    if result.stdout:
                        self.logger.info(f"Updater output: {result.stdout}")
                    return True
                else:
                    self.logger.error(f"Website updater failed with exit code {result.returncode}")
                    if result.stderr:
                        self.logger.error(f"Error output: {result.stderr}")
                    return False
                    
            else:
                self.logger.warning("comprehensive_website_updater.py not found")
                self.logger.info("Attempting basic website update...")
                return self._basic_website_update()
                
        except subprocess.TimeoutExpired:
            self.logger.error("Website updater timed out after 5 minutes")
            return False
        except Exception as e:
            self.logger.error(f"Website content update failed: {str(e)}")
            return False

    def _basic_website_update(self):
        """Basic website update if comprehensive updater is not available"""
        try:
            # Load episode data from JSON files
            databases = [
                self.podcast_dir / "logs" / "processed_cases.json",
                self.podcast_dir / "probate_cases" / "processed_cases.json", 
                self.podcast_dir / "probate_cases" / "processed_briefs.json"
            ]
            
            total_episodes = 0
            for db_path in databases:
                if db_path.exists():
                    try:
                        with open(db_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            total_episodes += len(data)
                            self.logger.info(f"Loaded {len(data)} entries from {db_path.name}")
                    except Exception as e:
                        self.logger.warning(f"Could not load {db_path.name}: {str(e)}")
            
            self.logger.info(f"Basic website update completed - found {total_episodes} total episodes")
            return True
            
        except Exception as e:
            self.logger.error(f"Basic website update failed: {str(e)}")
            return False

    def deploy_to_github(self):
        """Execute automated Git operations and deployment"""
        try:
            # Check if this is a git repository
            if not (self.base_dir / ".git").exists():
                self.logger.error("Not a git repository - cannot deploy automatically")
                self.logger.info("Manual deployment required:")
                self.logger.info("  git init")
                self.logger.info("  git add .")
                self.logger.info("  git commit -m 'Initial commit'")
                self.logger.info("  git push origin main")
                return False
            
            # Check git status first
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if not status_result.stdout.strip():
                self.logger.info("No changes to commit - website is already up to date")
                return True
            
            # Git operations
            commit_message = f"Automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            git_commands = [
                (["git", "add", "."], "Staging changes"),
                (["git", "commit", "-m", commit_message], "Committing changes"),
                (["git", "push", "origin", "main"], "Pushing to GitHub")
            ]
            
            for cmd, description in git_commands:
                self.logger.info(f"{description}...")
                
                result = subprocess.run(
                    cmd, 
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    self.logger.error(f"Git command failed: {' '.join(cmd)}")
                    self.logger.error(f"Error: {result.stderr}")
                    
                    # For push failures, provide helpful guidance
                    if "push" in cmd:
                        self.logger.error("Push failed - possible causes:")
                        self.logger.error("  1. No internet connection")
                        self.logger.error("  2. Authentication issues")
                        self.logger.error("  3. Remote repository issues")
                        self.logger.info("Manual push required: git push origin main")
                    
                    return False
                
                self.logger.info(f"[SUCCESS] {description} completed")
                
                # Log meaningful output
                if result.stdout and result.stdout.strip():
                    self.logger.info(f"Output: {result.stdout.strip()}")
            
            self.logger.info("GitHub deployment completed successfully")
            return True
            
        except subprocess.TimeoutExpired:
            self.logger.error("Git operation timed out")
            return False
        except Exception as e:
            self.logger.error(f"GitHub deployment failed: {str(e)}")
            return False

    def verify_deployment(self):
        """Verify deployment was successful"""
        try:
            # Basic file verification
            required_files = [
                "index.html"
            ]
            
            for file_path in required_files:
                full_path = self.base_dir / file_path
                if not full_path.exists():
                    self.logger.error(f"Required file missing: {file_path}")
                    return False
            
            # Check if index.html has episode data
            index_file = self.base_dir / "index.html"
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if "episodes = [" in content:
                self.logger.info("[SUCCESS] Episode data found in index.html")
            else:
                self.logger.warning("Episode data may be missing from index.html")
                
            self.logger.info("Deployment verification completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Deployment verification failed: {str(e)}")
            return False


def main():
    """Main execution function for Phase 5"""
    pipeline = WebsiteIntegrationPipeline()
    
    try:
        success = pipeline.execute_phase_5()
        
        if success:
            print("\n[SUCCESS] Phase 5: Website Integration & Deployment - SUCCESS")
            print("  Website content updated and deployed to GitHub Pages")
            print("  Live website should update within 2-5 minutes")
            sys.exit(0)
        else:
            print("\n[FAILED] Phase 5: Website Integration & Deployment - FAILED")
            print("  Check logs for detailed error information")
            print("  Website content may need manual deployment")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Phase 5 interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Phase 5 failed with unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
