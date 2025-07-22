#!/usr/bin/env python3
"""
GoDaddy Deployment Pipeline
Replaces GitHub Pages deployment with FTP/SFTP upload to GoDaddy hosting
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
        self.base_dir = Path(__file__).parent.parent  # Go up to website directory
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
        Main deployment function - uploads website to GoDaddy via FTP
        Returns: bool - Success status
        """
        try:
            self.logger.info("=== Starting GoDaddy Deployment ===")
            
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
            "index.html",
            "covers/cover.png"
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
            # Read configuration
            ftp_host = self.config['godaddy']['ftp_host']
            ftp_user = self.config['godaddy']['ftp_username']
            ftp_pass = self.config['godaddy']['ftp_password']
            ftp_port = int(self.config['godaddy'].get('ftp_port', 21))
            
            # Connect to FTP server
            self.logger.info(f"Connecting to {ftp_host}:{ftp_port}")
            ftp = ftplib.FTP()
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_user, ftp_pass)
            
            # Navigate to public_html or web root
            web_root = self.config['godaddy'].get('web_root', 'public_html')
            try:
                ftp.cwd(web_root)
                self.logger.info(f"Changed to web root: {web_root}")
            except ftplib.error_perm:
                self.logger.warning(f"Could not change to {web_root}, using current directory")
            
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
        
        # Add main HTML file
        index_html = self.base_dir / "index.html"
        if index_html.exists():
            files_to_upload.append(index_html)
        
        # Add all files from subdirectories
        for subdir in ['covers', 'pdfs', 'texts']:
            subdir_path = self.base_dir / subdir
            if subdir_path.exists():
                for file_path in subdir_path.rglob('*'):
                    if file_path.is_file():
                        files_to_upload.append(file_path)
        
        # Add any additional static files
        for static_file in ['robots.txt', 'sitemap.xml']:
            static_path = self.base_dir / static_file
            if static_path.exists():
                files_to_upload.append(static_path)
        
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
                    except ftplib.error_perm as e:
                        self.logger.error(f"Cannot create directory {dir_name}: {e}")
        
        # Return to original directory
        ftp.cwd(current_dir)

    def upload_file(self, ftp, local_file, remote_path):
        """Upload a single file to the server"""
        try:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            
            self.logger.info(f"Uploaded: {remote_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to upload {remote_path}: {e}")
            return False

    def verify_deployment(self, ftp):
        """Verify that key files were uploaded successfully"""
        try:
            # Check if index.html exists
            try:
                ftp.size('index.html')
                self.logger.info("Deployment verification: index.html found")
            except:
                self.logger.error("Deployment verification: index.html not found")
                return False
            
            # Check if covers directory exists
            try:
                ftp.cwd('covers')
                ftp.cwd('..')
                self.logger.info("Deployment verification: covers directory found")
            except:
                self.logger.warning("Covers directory not found")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Deployment verification failed: {e}")
            return False

def main():
    """Main execution function for GoDaddy deployment"""
    try:
        deployer = GoDaddyDeploymentPipeline()
        success = deployer.deploy_to_godaddy()
        
        if success:
            print("GoDaddy Deployment - SUCCESS")
            exit(0)
        else:
            print("GoDaddy Deployment - FAILED")
            exit(1)
            
    except Exception as e:
        print(f"GoDaddy Deployment - CRITICAL ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main()
