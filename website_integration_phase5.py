#!/usr/bin/env python3
"""
Phase 5: Website Integration & Deployment Pipeline
Complete automation from podcast content to live website

This script integrates with existing deployment tools:
- comprehensive_website_updater.py for content updates
- Git operations for GitHub Pages deployment
- Existing file synchronization utilities

Author: Scholar Podcast System - Phase 5 Integration
Date: July 17, 2025
"""

import os
import json
import shutil
import subprocess
import sys
import logging
from datetime import datetime
from pathlib import Path

class Phase5WebsiteIntegration:
    def __init__(self):
        self.website_dir = Path(__file__).parent
        self.podcast_dir = self.website_dir.parent
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for Phase 5"""
        log_dir = self.website_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - Phase5 - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"phase5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def execute_phase_5(self):
        """
        Main execution function for Phase 5
        Returns: int - Exit code (0=success, >0=failure)
        """
        try:
            print("🚀 === PHASE 5: WEBSITE INTEGRATION & DEPLOYMENT ===")
            self.logger.info("Starting Phase 5 execution")
            
            # Step 1: Content Synchronization
            print("\\n📁 Step 1: Synchronizing content files...")
            if not self.sync_content_files():
                return 1
                
            # Step 2: Website Content Update  
            print("\\n🔧 Step 2: Updating website content...")
            if not self.update_website_content():
                return 2
                
            # Step 3: Automated Deployment
            print("\\n🚀 Step 3: Deploying to GitHub Pages...")
            if not self.deploy_to_github():
                return 3
                
            # Step 4: Success Summary
            self.print_success_summary()
            
            self.logger.info("Phase 5 completed successfully!")
            return 0
            
        except Exception as e:
            self.logger.error(f"Phase 5 failed with exception: {e}")
            print(f"\\n❌ CRITICAL ERROR in Phase 5: {e}")
            return 99

    def sync_content_files(self):
        """Synchronize all content from pipeline to website directories"""
        try:
            print("  📋 Synchronizing files from podcast pipeline...")
            
            # Track success of each sync operation
            sync_results = {
                'covers': False,
                'pdfs': False, 
                'texts': False
            }
            
            # Sync covers (most likely to succeed)
            try:
                self._sync_covers()
                sync_results['covers'] = True
            except Exception as e:
                print(f"    ⚠️  Cover sync had issues: {e}")
                self.logger.warning(f"Cover sync failed: {e}")
            
            # Sync PDFs (improved error handling)
            try:
                self._sync_pdfs()
                sync_results['pdfs'] = True
            except Exception as e:
                print(f"    ⚠️  PDF sync had issues: {e}")
                self.logger.warning(f"PDF sync failed: {e}")
            
            # Sync text files
            try:
                self._sync_texts()
                sync_results['texts'] = True
            except Exception as e:
                print(f"    ⚠️  Text sync had issues: {e}")
                self.logger.warning(f"Text sync failed: {e}")
            
            # Report results
            successful_syncs = sum(sync_results.values())
            total_syncs = len(sync_results)
            
            print(f"  ✅ Content synchronization completed: {successful_syncs}/{total_syncs} operations successful")
            
            # Consider it successful if at least covers synced (most critical for website appearance)
            if sync_results['covers']:
                self.logger.info(f"Content synchronization completed: {successful_syncs}/{total_syncs} successful")
                return True
            else:
                print(f"  ⚠️  Critical content sync failures - covers not synced")
                self.logger.error("Critical content synchronization failures")
                return False
            
        except Exception as e:
            print(f"  ❌ Content synchronization failed: {e}")
            self.logger.error(f"Content synchronization failed: {e}")
            return False

    def _sync_covers(self):
        """Copy cover images from podcast directory"""
        covers_dir = self.website_dir / "covers"
        covers_dir.mkdir(exist_ok=True)
        
        cover_files = [
            "cover.png",
            "cover_briefing.png", 
            "cover_special_edition.png"
        ]
        
        synced_count = 0
        for cover_file in cover_files:
            src = self.podcast_dir / cover_file
            dst = covers_dir / cover_file
            if src.exists():
                shutil.copy2(src, dst)
                synced_count += 1
                self.logger.info(f"Synced cover: {cover_file}")
        
        print(f"    ✓ Synced {synced_count} cover images")

    def _sync_pdfs(self):
        """Copy PDF documents to website with improved error handling"""
        src_pdf_dir = self.podcast_dir / "probate_cases" / "pdfs"
        dst_pdf_dir = self.website_dir / "pdfs"
        
        if not src_pdf_dir.exists():
            print("    ⚠️  No PDF source directory found - skipping PDF sync")
            return
        
        try:
            # Create destination directory if it doesn't exist
            dst_pdf_dir.mkdir(exist_ok=True)
            
            # Sync published PDFs
            src_published = src_pdf_dir / "published"
            dst_published = dst_pdf_dir / "published"
            
            if src_published.exists():
                dst_published.mkdir(exist_ok=True)
                pdf_count = 0
                for pdf_file in src_published.glob("*.pdf"):
                    try:
                        dst_file = dst_published / pdf_file.name
                        if not dst_file.exists() or pdf_file.stat().st_mtime > dst_file.stat().st_mtime:
                            shutil.copy2(pdf_file, dst_file)
                            pdf_count += 1
                    except Exception as e:
                        print(f"    ⚠️  Could not copy {pdf_file.name}: {e}")
                        continue
                        
                print(f"    ✓ Synced {pdf_count} published PDFs")
            
            # Sync unpublished PDFs
            src_unpublished = src_pdf_dir / "unpublished"
            dst_unpublished = dst_pdf_dir / "unpublished"
            
            if src_unpublished.exists():
                dst_unpublished.mkdir(exist_ok=True)
                pdf_count = 0
                for pdf_file in src_unpublished.glob("*.pdf"):
                    try:
                        dst_file = dst_unpublished / pdf_file.name
                        if not dst_file.exists() or pdf_file.stat().st_mtime > dst_file.stat().st_mtime:
                            shutil.copy2(pdf_file, dst_file)
                            pdf_count += 1
                    except Exception as e:
                        print(f"    ⚠️  Could not copy {pdf_file.name}: {e}")
                        continue
                        
                print(f"    ✓ Synced {pdf_count} unpublished PDFs")
            
            self.logger.info("PDF synchronization completed with incremental updates")
            
        except Exception as e:
            print(f"    ⚠️  PDF sync had issues but continuing: {e}")
            self.logger.warning(f"PDF synchronization had issues: {e}")
            # Don't fail the entire process for PDF sync issues

    def _sync_texts(self):
        """Copy text files to website"""
        dst_text_dir = self.website_dir / "texts"
        dst_text_dir.mkdir(exist_ok=True)
        
        text_count = 0
        
        # Sync published text files
        src_text_dir = self.podcast_dir / "probate_cases" / "pdfs" / "published_text"
        if src_text_dir.exists():
            for txt_file in src_text_dir.glob("*.txt"):
                shutil.copy2(txt_file, dst_text_dir / txt_file.name)
                text_count += 1
        
        # Sync case briefs
        src_briefs_dir = self.podcast_dir / "podcast" / "case_briefs"
        if src_briefs_dir.exists():
            for brief_file in src_briefs_dir.glob("*.txt"):
                shutil.copy2(brief_file, dst_text_dir / f"brief_{brief_file.name}")
                text_count += 1
                
        print(f"    ✓ Synced {text_count} text files")
        self.logger.info(f"Synced {text_count} text files")

    def update_website_content(self):
        """Update website content using Phase 5 content updater wrapper"""
        try:
            print("  🔧 Running Phase 5 content updater...")
            
            # Check if our Phase 5 content updater exists
            updater_script = self.website_dir / "phase5_content_updater.py"
            if not updater_script.exists():
                print("  ❌ phase5_content_updater.py not found")
                print(f"  Expected location: {updater_script}")
                self.logger.error("Phase 5 content updater script not found")
                return False
            
            # Also check if comprehensive updater exists
            comprehensive_script = self.website_dir / "comprehensive_website_updater.py"
            if not comprehensive_script.exists():
                print("  ❌ comprehensive_website_updater.py not found")
                print(f"  Expected location: {comprehensive_script}")
                self.logger.error("Comprehensive website updater script not found")
                return False
            
            print(f"  📍 Found Phase 5 updater: {updater_script}")
            print(f"  📍 Found comprehensive updater: {comprehensive_script}")
            
            # Change to website directory for proper execution
            original_cwd = os.getcwd()
            os.chdir(self.website_dir)
            
            try:
                # Execute the Phase 5 content updater
                print("  ⚙️  Executing Phase 5 content updater...")
                result = subprocess.run([
                    sys.executable, 
                    "phase5_content_updater.py"
                ], capture_output=True, text=True)
                
                # Always restore original directory
                os.chdir(original_cwd)
                
                if result.returncode == 0:
                    print("  ✅ Website content updated successfully")
                    self.logger.info("Website content updated using Phase 5 updater")
                    
                    # Show key output information
                    if result.stdout:
                        # Extract useful info from stdout
                        output_lines = result.stdout.split('\n')
                        for line in output_lines:
                            if any(keyword in line for keyword in ['Found', 'episodes', 'Updated', 'SUCCESS', '✅', '📊']):
                                print(f"    📊 {line.strip()}")
                        self.logger.info(f"Phase 5 updater completed successfully")
                    
                    return True
                else:
                    print(f"  ❌ Phase 5 updater failed with exit code: {result.returncode}")
                    if result.stderr:
                        print(f"  📋 Error details: {result.stderr}")
                        self.logger.error(f"Phase 5 updater error: {result.stderr}")
                    if result.stdout:
                        print(f"  📋 Output: {result.stdout}")
                        self.logger.error(f"Phase 5 updater stdout: {result.stdout}")
                    return False
                    
            except Exception as inner_e:
                os.chdir(original_cwd)  # Ensure we restore directory
                raise inner_e
            
        except Exception as e:
            print(f"  ❌ Error running Phase 5 updater: {e}")
            self.logger.error(f"Website content update failed: {e}")
            return False

    def deploy_to_github(self):
        """Execute automated Git operations and deployment"""
        try:
            # Check if this is a git repository
            if not (self.website_dir / ".git").exists():
                print("  ❌ Not a git repository - cannot deploy")
                self.logger.error("Website directory is not a git repository")
                return False
            
            print("  📤 Executing git operations...")
            
            # Change to website directory
            os.chdir(self.website_dir)
            
            # Git operations with error handling
            commands = [
                {
                    'cmd': ["git", "add", "."],
                    'desc': "Adding changes to git",
                    'required': True
                },
                {
                    'cmd': ["git", "commit", "-m", f"Phase 5 automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                    'desc': "Committing changes",
                    'required': False  # Commit might fail if no changes
                },
                {
                    'cmd': ["git", "push", "origin", "main"],
                    'desc': "Pushing to GitHub Pages",
                    'required': True
                }
            ]
            
            for cmd_info in commands:
                cmd = cmd_info['cmd']
                desc = cmd_info['desc']
                required = cmd_info['required']
                
                print(f"    {desc}...")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    if required:
                        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                            print("    ℹ️  No changes to commit - website already up to date")
                            self.logger.info("No changes detected for commit")
                            continue
                        else:
                            print(f"    ❌ Failed: {' '.join(cmd)}")
                            print(f"    Error: {result.stderr}")
                            self.logger.error(f"Git command failed: {result.stderr}")
                            return False
                    else:
                        print(f"    ⚠️  Warning: {desc} failed (non-critical)")
                        self.logger.warning(f"Non-critical git operation failed: {result.stderr}")
                else:
                    print(f"    ✅ {desc} completed")
                    self.logger.info(f"Git operation successful: {' '.join(cmd)}")
            
            print("  ✅ GitHub deployment completed successfully")
            self.logger.info("GitHub deployment completed")
            return True
            
        except Exception as e:
            print(f"  ❌ GitHub deployment failed: {e}")
            self.logger.error(f"GitHub deployment failed: {e}")
            return False

    def print_success_summary(self):
        """Print comprehensive success summary"""
        print("\\n" + "="*60)
        print("🎉 PHASE 5 COMPLETED SUCCESSFULLY! 🎉")
        print("="*60)
        print()
        print("✅ Phase 5 Accomplishments:")
        print("   ✓ Content files synchronized from podcast pipeline")
        print("   ✓ Website updated with latest episodes and metadata")
        print("   ✓ Changes committed and pushed to GitHub")
        print("   ✓ Live website deployment initiated")
        print()
        print("🌐 Website Information:")
        print("   📍 Live URL: https://infosquawk.github.io/ca-probate-appellate-repository")
        print("   ⏱️  Update Time: 2-3 minutes for GitHub Pages build")
        print("   📊 Content: Latest episodes with professional case names")
        print()
        print("🔄 Integration Status:")
        print("   ✓ Pipeline content → Website content: SYNCHRONIZED")
        print("   ✓ Local changes → GitHub repository: DEPLOYED") 
        print("   ✓ GitHub repository → Live website: IN PROGRESS")
        print()
        print("📋 Next Steps:")
        print("   • Check live website in 2-3 minutes")
        print("   • Verify new episodes appear correctly")  
        print("   • Confirm search functionality works")
        print("   • Monitor logs for any deployment issues")

def main():
    """Main execution function for Phase 5"""
    print("🌟 SCHOLAR PODCAST SYSTEM - PHASE 5")
    print("    Website Integration & Deployment")
    print("    Complete End-to-End Automation")
    print()
    
    phase5 = Phase5WebsiteIntegration()
    exit_code = phase5.execute_phase_5()
    
    if exit_code == 0:
        print("\\n✅ Phase 5: Website Integration & Deployment - SUCCESS")
    else:
        print(f"\\n❌ Phase 5: Website Integration & Deployment - FAILED (Exit Code: {exit_code})")
        print("\\n🔧 Manual Recovery Options:")
        print("   • Check logs in website/logs/ for detailed error information")
        print("   • Run DEPLOY_FINAL_FIXES.bat for manual deployment")
        print("   • Use development/deploy_to_github_pages.bat as alternative")
        print("   • Verify git repository status and permissions")
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
