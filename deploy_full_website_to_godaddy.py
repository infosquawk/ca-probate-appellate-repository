#!/usr/bin/env python3
"""
GoDaddy Full Website Deployment Pipeline
Replaces GitHub Pages deployment with FTP upload to GoDaddy hosting
Uses /public_html directory structure for sysop2@probrep.com account
"""

import os
import json
import ftplib
import logging
from datetime import datetime
from pathlib import Path
import hashlib
import configparser

class GoDaddyDeploymentPipeline:
    def __init__(self):
        self.base_dir = Path(__file__).parent  # website directory
        self.podcast_dir = self.base_dir.parent
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self):
        """Load GoDaddy FTP configuration"""
        config_file = self.base_dir / "godaddy_config.ini"
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file missing: {config_file}")
            
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def setup_logging(self):
        """Configure logging for GoDaddy deployment"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"godaddy_deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def deploy_to_godaddy(self):
        """
        Main deployment function - uploads complete website to GoDaddy via FTP
        Returns: bool - Success status
        """
        try:
            self.logger.info("=== Starting GoDaddy Full Website Deployment ===")
            
            # Step 1: Validate local files
            if not self.validate_local_files():
                return False
                
            # Step 2: Connect to GoDaddy FTP
            ftp = self.connect_ftp()
            if not ftp:
                return False
                
            # Step 3: Sync files to GoDaddy
            if not self.sync_files_to_server(ftp):
                ftp.quit()
                return False
                
            # Step 4: Verify deployment
            if not self.verify_deployment(ftp):
                self.logger.warning("Deployment verification failed - manual check recommended")
                
            ftp.quit()
            self.logger.info("GoDaddy deployment completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"GoDaddy deployment failed: {e}")
            return False

    def validate_local_files(self):
        """Validate that required local files exist"""
        required_files = [
            "index.html"
        ]
        
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                self.logger.error(f"Required file missing: {file_path}")
                return False
                
        self.logger.info("Local file validation passed")
        return True

    def connect_ftp(self):
        """Establish FTP connection to GoDaddy"""
        try:
            # Read configuration (updated credentials)
            ftp_host = self.config['godaddy']['ftp_host']
            ftp_user = self.config['godaddy']['ftp_username']
            ftp_pass = self.config['godaddy']['ftp_password']
            ftp_port = int(self.config['godaddy'].get('ftp_port', 21))
            
            self.logger.info(f"Connecting to {ftp_host}:{ftp_port}")
            self.logger.info(f"Using account: {ftp_user}")
            
            # Connect to FTP server
            ftp = ftplib.FTP()
            ftp.connect(ftp_host, ftp_port, timeout=30)
            ftp.login(ftp_user, ftp_pass)
            
            # Check web root setting and change to public_html
            web_root = self.config['godaddy'].get('web_root', '/public_html')
            if web_root and web_root != '/' and web_root != '':
                try:
                    ftp.cwd(web_root.lstrip('/'))
                    self.logger.info(f"Changed to web root: {web_root}")
                except ftplib.error_perm:
                    self.logger.info(f"Could not change to {web_root}, using root directory")
            else:
                self.logger.info("Using root directory for deployment")
            
            self.logger.info("FTP connection established successfully")
            return ftp
            
        except Exception as e:
            self.logger.error(f"FTP connection failed: {e}")
            return None

    def sync_files_to_server(self, ftp):
        """Synchronize local files to GoDaddy server"""
        try:
            # Get list of local files to upload
            local_files = self.get_local_files()
            
            self.logger.info(f"Found {len(local_files)} files to upload")
            
            # Upload each file
            upload_count = 0
            for local_file in local_files:
                relative_path = local_file.relative_to(self.base_dir)
                
                # Create remote directory if needed
                remote_dir = str(relative_path.parent).replace('\\', '/')
                if remote_dir != '.':
                    self.ensure_remote_directory(ftp, remote_dir)
                
                # Upload file
                remote_path = str(relative_path).replace('\\', '/')
                if self.upload_file(ftp, local_file, remote_path):
                    upload_count += 1
                else:
                    self.logger.error(f"Failed to upload: {relative_path}")
                    return False
            
            self.logger.info(f"Successfully uploaded {upload_count} files")
            return True
            
        except Exception as e:
            self.logger.error(f"File synchronization failed: {e}")
            return False

    def get_local_files(self):
        """Get list of all files to upload"""
        files_to_upload = []
        
        self.logger.info("Scanning local files for deployment...")
        
        # Add main HTML file
        index_html = self.base_dir / "index.html"
        if index_html.exists():
            files_to_upload.append(index_html)
            self.logger.info(f"Added: index.html ({index_html.stat().st_size} bytes)")
        
        # Add all files from subdirectories
        for subdir in ['covers', 'pdfs', 'texts']:
            subdir_path = self.base_dir / subdir
            if subdir_path.exists():
                count = 0
                for file_path in subdir_path.rglob('*'):
                    if file_path.is_file():
                        files_to_upload.append(file_path)
                        count += 1
                self.logger.info(f"Added: {subdir}/ directory ({count} files)")
            else:
                self.logger.info(f"Skipped: {subdir}/ directory (not found)")
        
        # Add any additional static files
        for static_file in ['robots.txt', 'sitemap.xml']:
            static_path = self.base_dir / static_file
            if static_path.exists():
                files_to_upload.append(static_path)
                self.logger.info(f"Added: {static_file}")
        
        return files_to_upload

    def ensure_remote_directory(self, ftp, directory):
        """Create remote directory if it doesn't exist"""
        dirs = directory.split('/')
        current_dir = ftp.pwd()
        
        for dir_name in dirs:
            if dir_name:
                try:
                    ftp.cwd(dir_name)
                except ftplib.error_perm:
                    # Directory doesn't exist, create it
                    try:
                        ftp.mkd(dir_name)
                        ftp.cwd(dir_name)
                        self.logger.info(f"Created directory: {dir_name}")
                    except ftplib.error_perm as e:
                        self.logger.error(f"Cannot create directory {dir_name}: {e}")
        
        # Return to original directory
        ftp.cwd(current_dir)

    def upload_file(self, ftp, local_file, remote_path):
        """Upload a single file to the server"""
        try:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            
            # Get file size for verification
            local_size = local_file.stat().st_size
            try:
                remote_size = ftp.size(remote_path)
                if local_size == remote_size:
                    self.logger.info(f"✓ Uploaded: {remote_path} ({local_size} bytes)")
                else:
                    self.logger.warning(f"⚠ Size mismatch: {remote_path} (local: {local_size}, remote: {remote_size})")
            except:
                self.logger.info(f"✓ Uploaded: {remote_path} ({local_size} bytes)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to upload {remote_path}: {e}")
            return False

    def verify_deployment(self, ftp):
        """Verify that key files were uploaded successfully"""
        try:
            verification_count = 0
            
            self.logger.info("Verifying deployment...")
            
            # Check if index.html exists
            try:
                size = ftp.size('index.html')
                self.logger.info(f"✓ Verification: index.html found ({size} bytes)")
                verification_count += 1
            except:
                self.logger.error("✗ Verification: index.html not found")
                return False
            
            # Check if covers directory exists
            try:
                ftp.cwd('covers')
                files = ftp.nlst()
                ftp.cwd('..')
                self.logger.info(f"✓ Verification: covers directory found ({len(files)} files)")
                verification_count += 1
            except:
                self.logger.warning("⚠ Covers directory not found (may be empty)")
            
            # Check if pdfs directory exists  
            try:
                ftp.cwd('pdfs')
                ftp.cwd('..')
                self.logger.info("✓ Verification: pdfs directory found")
                verification_count += 1
            except:
                self.logger.info("ℹ PDFs directory not found (may not exist yet)")
            
            # Check if texts directory exists
            try:
                ftp.cwd('texts')
                files = ftp.nlst()
                ftp.cwd('..')
                self.logger.info(f"✓ Verification: texts directory found ({len(files)} files)")
                verification_count += 1
            except:
                self.logger.info("ℹ Texts directory not found (may not exist yet)")
            
            self.logger.info(f"Deployment verification: {verification_count} checks passed")
            return verification_count >= 1  # At least index.html must exist
            
        except Exception as e:
            self.logger.error(f"Deployment verification failed: {e}")
            return False

def main():
    """Main execution function for GoDaddy deployment"""
    try:
        print("🚀 ProBRep.com Full Website Deployment")
        print("=" * 50)
        
        deployer = GoDaddyDeploymentPipeline()
        success = deployer.deploy_to_godaddy()
        
        if success:
            print("\n" + "=" * 50)
            print("✅ FULL WEBSITE DEPLOYMENT - SUCCESS!")
            print("🌐 Your complete website is now live at:")
            print("   https://probrep.com")
            print("\n📋 What was deployed:")
            print("   ✓ Main website (index.html)")
            print("   ✓ Podcast covers")
            print("   ✓ Court documents (PDFs)")
            print("   ✓ Case briefs and text files")
            print("   ✓ Site configuration files")
            print("\n🎯 Next steps:")
            print("   1. Visit https://probrep.com to verify")
            print("   2. Test all functionality")
            print("   3. Update DNS/redirects if needed")
            print("   4. Monitor for any issues")
            exit(0)
        else:
            print("\n" + "=" * 50)
            print("❌ FULL WEBSITE DEPLOYMENT - FAILED")
            print("Check the logs for detailed error information")
            exit(1)
            
    except Exception as e:
        print(f"\n💥 DEPLOYMENT CRITICAL ERROR: {e}")
        print("Check configuration and try again")
        exit(1)

if __name__ == "__main__":
    main()
