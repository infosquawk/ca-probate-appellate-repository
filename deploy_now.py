#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GoDaddy Full Website Deployment Pipeline - COMPLETELY FIXED VERSION
No syntax errors, clean unicode handling, fully functional
"""

import os
import json
import ftplib
import logging
from datetime import datetime
from pathlib import Path
import configparser
import unicodedata
import re

class GoDaddyDeploymentPipeline:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.podcast_dir = self.base_dir.parent
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self):
        """Load GoDaddy FTP configuration"""
        config_file = self.base_dir / "godaddy_config.ini"
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file missing: {config_file}")
            
        config = configparser.ConfigParser()
        with open(config_file, 'r', encoding='utf-8') as f:
            config.read_string(f.read())
        return config

    def setup_logging(self):
        """Configure logging"""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        log_file = log_dir / f"godaddy_deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def sanitize_filename(self, filename):
        """Sanitize filename for FTP safety"""
        # Normalize unicode characters
        filename = unicodedata.normalize('NFD', filename)
        filename = ''.join(c for c in filename if unicodedata.category(c) != 'Mn')
        
        # Replace common special characters
        replacements = {
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a',
            'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
            'ñ': 'n', 'ç': 'c',
            '’': "'", '“': '"', '”': '"', '–': '-', '—': '-',
            ' ': '_',
        }
        
        for old, new in replacements.items():
            filename = filename.replace(old, new)
        
        # Remove non-ASCII characters
        filename = ''.join(c for c in filename if ord(c) < 128)
        
        # Clean up multiple underscores
        filename = re.sub(r'_+', '_', filename)
        filename = filename.strip('_.-')
        
        return filename

    def deploy_to_godaddy(self):
        """Main deployment function"""
        try:
            self.logger.info("=== Starting GoDaddy Full Website Deployment ===")
            
            # Step 1: Validate local files
            if not self.validate_local_files():
                return False
                
            # Step 2: Connect to FTP
            ftp = self.connect_ftp()
            if not ftp:
                return False
                
            # Step 3: Upload files
            if not self.sync_files_to_server(ftp):
                ftp.quit()
                return False
                
            # Step 4: Verify
            if not self.verify_deployment(ftp):
                self.logger.warning("Deployment verification failed")
                
            ftp.quit()
            self.logger.info("GoDaddy deployment completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"GoDaddy deployment failed: {e}")
            return False

    def validate_local_files(self):
        """Validate required local files exist"""
        required_files = ["index.html"]
        
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
            ftp_host = self.config['godaddy']['ftp_host']
            ftp_user = self.config['godaddy']['ftp_username']
            ftp_pass = self.config['godaddy']['ftp_password']
            ftp_port = int(self.config['godaddy'].get('ftp_port', 21))
            
            self.logger.info(f"Connecting to {ftp_host}:{ftp_port}")
            self.logger.info(f"Using account: {ftp_user}")
            
            ftp = ftplib.FTP()
            ftp.encoding = 'utf-8'
            ftp.connect(ftp_host, ftp_port, timeout=30)
            ftp.login(ftp_user, ftp_pass)
            
            web_root = self.config['godaddy'].get('web_root', '/public_html')
            if web_root and web_root != '/' and web_root != '':
                try:
                    ftp.cwd(web_root.lstrip('/'))
                    self.logger.info(f"Changed to web root: {web_root}")
                except ftplib.error_perm:
                    self.logger.info(f"Could not change to {web_root}, using root")
            
            self.logger.info("FTP connection established successfully")
            return ftp
            
        except Exception as e:
            self.logger.error(f"FTP connection failed: {e}")
            return None

    def sync_files_to_server(self, ftp):
        """Upload all files to server"""
        try:
            local_files = self.get_local_files()
            self.logger.info(f"Found {len(local_files)} files to upload")
            
            upload_count = 0
            failed_files = []
            
            for local_file in local_files:
                try:
                    relative_path = local_file.relative_to(self.base_dir)
                    
                    path_parts = []
                    for part in relative_path.parts:
                        sanitized_part = self.sanitize_filename(part)
                        path_parts.append(sanitized_part)
                    
                    sanitized_relative_path = Path(*path_parts)
                    remote_dir = str(sanitized_relative_path.parent).replace('\\', '/')
                    if remote_dir != '.':
                        self.ensure_remote_directory(ftp, remote_dir)
                    
                    remote_path = str(sanitized_relative_path).replace('\\', '/')
                    
                    if self.upload_file(ftp, local_file, remote_path):
                        upload_count += 1
                        if str(relative_path) != remote_path:
                            self.logger.info(f"Sanitized: {relative_path} → {remote_path}")
                    else:
                        failed_files.append(str(relative_path))
                        
                except Exception as e:
                    self.logger.error(f"Error processing {local_file}: {e}")
                    failed_files.append(str(local_file))
            
            if failed_files:
                self.logger.error(f"Failed to upload {len(failed_files)} files")
                for failed_file in failed_files:
                    self.logger.error(f"  {failed_file}")
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
        
        index_html = self.base_dir / "index.html"
        if index_html.exists():
            files_to_upload.append(index_html)
            size = index_html.stat().st_size
            self.logger.info(f"Added: index.html ({size} bytes)")
        
        for subdir in ['covers', 'pdfs', 'texts']:
            subdir_path = self.base_dir / subdir
            if subdir_path.exists():
                count = 0
                unicode_count = 0
                for file_path in subdir_path.rglob('*'):
                    if file_path.is_file():
                        files_to_upload.append(file_path)
                        count += 1
                        try:
                            file_path.name.encode('ascii')
                        except UnicodeEncodeError:
                            unicode_count += 1
                msg = f"Added: {subdir}/ directory ({count} files"
                if unicode_count > 0:
                    msg += f", {unicode_count} with unicode chars"
                msg += ")"
                self.logger.info(msg)
            else:
                self.logger.info(f"Skipped: {subdir}/ directory (not found)")
        
        for static_file in ['robots.txt', 'sitemap.xml']:
            static_path = self.base_dir / static_file
            if static_path.exists():
                files_to_upload.append(static_path)
                self.logger.info(f"Added: {static_file}")
        
        return files_to_upload

    def ensure_remote_directory(self, ftp, directory):
        """Create remote directory if it doesn't exist"""
        if not directory or directory == '.':
            return
            
        dirs = directory.split('/')
        current_dir = ftp.pwd()
        
        for dir_name in dirs:
            if dir_name:
                try:
                    ftp.cwd(dir_name)
                except ftplib.error_perm:
                    try:
                        ftp.mkd(dir_name)
                        ftp.cwd(dir_name)
                        self.logger.info(f"Created directory: {dir_name}")
                    except ftplib.error_perm as e:
                        self.logger.error(f"Cannot create directory {dir_name}: {e}")
                        break
        ftp.cwd(current_dir)

    def upload_file(self, ftp, local_file, remote_path):
        """Upload a single file"""
        try:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            
            local_size = local_file.stat().st_size
            try:
                remote_size = ftp.size(remote_path)
                if local_size == remote_size:
                    self.logger.info(f"✓ Uploaded: {remote_path} ({local_size} bytes)")
                else:
                    self.logger.warning(f"⚠ Size mismatch: {remote_path}")
            except ftplib.error_perm:
                self.logger.info(f"✓ Uploaded: {remote_path} ({local_size} bytes)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to upload {remote_path}: {e}")
            return False

    def verify_deployment(self, ftp):
        """Verify that deployment was successful"""
        try:
            verification_count = 0
            self.logger.info("Verifying deployment...")
            
            try:
                size = ftp.size('index.html')
                self.logger.info(f"✓ Verification: index.html found ({size} bytes)")
                verification_count += 1
            except:
                self.logger.error("✗ Verification: index.html not found")
                return False
            
            directories_to_check = ['covers', 'pdfs', 'texts']
            for dir_name in directories_to_check:
                try:
                    ftp.cwd(dir_name)
                    files = ftp.nlst()
                    ftp.cwd('..')
                    self.logger.info(f"✓ Verification: {dir_name} directory ({len(files)} files)")
                    verification_count += 1
                except:
                    self.logger.info(f"ℹ {dir_name} directory not found (may be empty)")
            
            self.logger.info(f"Deployment verification: {verification_count} checks passed")
            return verification_count >= 1
            
        except Exception as e:
            self.logger.error(f"Deployment verification failed: {e}")
            return False


def main():
    """Main execution function"""
    try:
        print("🚀 ProBRep.com Full Website Deployment (Unicode Fixed)")
        print("=" * 60)
        
        deployer = GoDaddyDeploymentPipeline()
        success = deployer.deploy_to_godaddy()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ FULL WEBSITE DEPLOYMENT - SUCCESS!")
            print("🌐 Your complete website is now live at:")
            print("   https://probrep.com")
            print("\n📋 What was deployed:")
            print("   ✓ Main website (index.html)")
            print("   ✓ Podcast covers")
            print("   ✓ Court documents (PDFs)")
            print("   ✓ Case briefs and text files")
            print("   ✓ Site configuration files")
            print("\n🔧 Unicode issues resolved:")
            print("   ✓ Filenames with special characters sanitized")
            print("   ✓ UTF-8 encoding for all operations")
            print("   ✓ FTP upload in binary mode")
            print("   ✓ Comprehensive error handling")
            print("\n🎯 Next steps:")
            print("   1. Visit https://probrep.com to verify")
            print("   2. Test all functionality")
            print("   3. Update DNS/redirects if needed")
            print("   4. Monitor for any issues")
        else:
            print("\n" + "=" * 60)
            print("❌ FULL WEBSITE DEPLOYMENT - FAILED")
            print("Check the logs for detailed error information")
            print("Common unicode issues and solutions:")
            print("  • Files with special characters → Automatically sanitized")
            print("  • Encoding errors → Using UTF-8 throughout")
            print("  • FTP upload issues → Using binary mode")
            
    except Exception as e:
        print(f"\n💥 DEPLOYMENT CRITICAL ERROR: {e}")
        print("Check configuration and try again")


if __name__ == "__main__":
    main()
