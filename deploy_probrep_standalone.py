#!/usr/bin/env python3
"""
Standalone ProBrep.com Deployment Script
Independent deployment tool for website content to ProBrep.com via FTP
Includes connection testing, deployment, and verification capabilities
"""

import os
import sys
import json
import ftplib
import logging
import argparse
import traceback
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

class ProBrepDeployment:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.base_dir = self.script_dir.parent
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        """Configure logging for deployment operations"""
        log_dir = self.script_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_filename = f"probrep_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load FTP configuration from multiple possible locations"""
        config_files = [
            self.base_dir / "godaddy_config.json",
            self.script_dir / "godaddy_config.json",
            self.script_dir / "godaddy_config.ini"
        ]
        
        self.config = None
        for config_file in config_files:
            if config_file.exists():
                try:
                    if config_file.suffix == '.json':
                        with open(config_file, 'r', encoding='utf-8') as f:
                            self.config = json.load(f)
                    else:
                        # Handle .ini format if needed
                        import configparser
                        parser = configparser.ConfigParser()
                        parser.read(config_file)
                        self.config = dict(parser['DEFAULT'])
                    
                    self.logger.info(f"Configuration loaded from: {config_file}")
                    break
                except Exception as e:
                    self.logger.warning(f"Failed to load config from {config_file}: {e}")
        
        if not self.config:
            self.logger.error("No valid configuration file found")
            
    def test_connection(self):
        """Test FTP connection to ProBrep.com"""
        print(" Testing ProBrep.com FTP Connection...")
        print("=" * 50)
        
        if not self.config:
            print("[ERROR] Configuration not available")
            return False
            
        try:
            # Test FTP connection
            print(f"[CONNECT] Connecting to: {self.config.get('ftp_host', 'Unknown')}")
            
            ftp = ftplib.FTP()
            ftp.connect(self.config['ftp_host'])
            
            print(f" Authenticating as: {self.config.get('ftp_username', 'Unknown')}")
            ftp.login(self.config['ftp_username'], self.config['ftp_password'])
            
            print("[SUCCESS] FTP connection successful!")
            
            # Test directory access
            try:
                ftp.cwd('public_html')
                print("[FOLDER] Successfully accessed public_html directory")
                
                # List some contents
                files = ftp.nlst()
                print(f" Found {len(files)} items in public_html")
                
            except Exception as e:
                print(f"[WARNING]  Could not access public_html: {e}")
                print(" Will use root directory for deployment")
            
            ftp.quit()
            
            print(" Connection test completed successfully!")
            print("=" * 50)
            return True
            
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
            print("=" * 50)
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def deploy_website(self):
        """Deploy website content to ProBrep.com"""
        print(" Deploying Website to ProBrep.com...")
        print("=" * 50)
        
        if not self.config:
            print("[ERROR] Configuration not available")
            return False
            
        try:
            # Connect to FTP
            print("[CONNECT] Establishing FTP connection...")
            ftp = ftplib.FTP()
            ftp.connect(self.config['ftp_host'])
            ftp.login(self.config['ftp_username'], self.config['ftp_password'])
            
            print("[SUCCESS] FTP connection established")
            
            # Navigate to public_html if possible
            try:
                ftp.cwd('public_html')
                print("[FOLDER] Changed to public_html directory")
            except:
                print("[WARNING]  Using root directory")
            
            # Upload website content
            print(" Starting file upload...")
            uploaded_count = self._upload_directory_recursive(ftp, self.script_dir, "")
            
            ftp.quit()
            
            print(f"[SUCCESS] Deployment completed: {uploaded_count} files uploaded")
            print("=" * 50)
            
            self.logger.info(f"Deployment successful: {uploaded_count} files uploaded")
            return True
            
        except Exception as e:
            print(f"[ERROR] Deployment failed: {e}")
            print("=" * 50)
            self.logger.error(f"Deployment failed: {e}")
            return False
    
    def _upload_directory_recursive(self, ftp, local_dir, remote_dir):
        """Recursively upload directory contents with progress tracking"""
        uploaded_count = 0
        
        try:
            # Create remote directory if needed
            if remote_dir:
                try:
                    ftp.mkd(remote_dir)
                    print(f"[FOLDER] Created directory: {remote_dir}")
                except:
                    pass  # Directory might exist
                ftp.cwd(remote_dir)
            
            # Process all items in directory
            items = list(local_dir.iterdir())
            total_items = len(items)
            
            for i, item in enumerate(items, 1):
                progress = f"[{i}/{total_items}]"
                
                if item.is_file():
                    # Skip certain files
                    if self._should_skip_file(item):
                        print(f"[NEXT]  {progress} Skipping: {item.name}")
                        continue
                    
                    try:
                        print(f" {progress} Uploading: {item.name}")
                        
                        with open(item, 'rb') as f:
                            ftp.storbinary(f'STOR {item.name}', f)
                        
                        uploaded_count += 1
                        
                    except Exception as e:
                        print(f"[ERROR] {progress} Failed to upload {item.name}: {e}")
                        self.logger.warning(f"Upload failed for {item.name}: {e}")
                        
                elif item.is_dir() and not item.name.startswith('.'):
                    print(f"[FOLDER] {progress} Processing directory: {item.name}")
                    
                    try:
                        ftp.mkd(item.name)
                    except:
                        pass  # Directory might exist
                    
                    ftp.cwd(item.name)
                    sub_uploaded = self._upload_directory_recursive(ftp, item, "")
                    uploaded_count += sub_uploaded
                    ftp.cwd('..')
            
            if remote_dir:
                ftp.cwd('..')
                
        except Exception as e:
            print(f"[ERROR] Error processing directory {local_dir}: {e}")
            self.logger.error(f"Directory upload error: {e}")
            
        return uploaded_count
    
    def _should_skip_file(self, file_path):
        """Determine if a file should be skipped during upload"""
        skip_patterns = [
            # Hidden files
            lambda p: p.name.startswith('.'),
            # Log files
            lambda p: p.name.endswith('.log'),
            # Backup files
            lambda p: '.backup_' in p.name,
            # Python cache
            lambda p: p.name == '__pycache__',
            # Git files
            lambda p: p.name in ['.git', '.gitignore'],
            # Temporary files
            lambda p: p.name.endswith('.tmp') or p.name.endswith('.temp')
        ]
        
        return any(pattern(file_path) for pattern in skip_patterns)
    
    def verify_deployment(self):
        """Verify the deployment was successful"""
        print(" Verifying ProBrep.com Deployment...")
        print("=" * 50)
        
        if not self.config:
            print("[ERROR] Configuration not available")
            return False
            
        website_url = self.config.get('website_url', 'https://probrep.com')
        
        try:
            print(f"[WEB] Testing website accessibility: {website_url}")
            
            # Test main website
            response = urllib.request.urlopen(website_url, timeout=15)
            status_code = response.getcode()
            
            if status_code == 200:
                print(f"[SUCCESS] Website is accessible (Status: {status_code})")
                
                # Read some content to verify it's not just a placeholder
                content = response.read().decode('utf-8', errors='ignore')
                
                if len(content) > 1000:  # Basic content check
                    print(f"[SUCCESS] Website has substantial content ({len(content)} characters)")
                    
                    # Check for key elements
                    if 'episodes' in content.lower():
                        print("[SUCCESS] Episode content detected")
                    if 'california' in content.lower():
                        print("[SUCCESS] California probate content detected")
                        
                else:
                    print("[WARNING]  Website content seems limited")
                
                print(" Deployment verification successful!")
                print("=" * 50)
                return True
                
            else:
                print(f"[WARNING]  Website returned status code: {status_code}")
                print("=" * 50)
                return False
                
        except urllib.error.URLError as e:
            print(f"[ERROR] Website not accessible: {e}")
            print("=" * 50)
            return False
            
        except Exception as e:
            print(f"[ERROR] Verification failed: {e}")
            print("=" * 50)
            return False
    
    def show_status(self):
        """Display current configuration and status"""
        print(" ProBrep.com Deployment Status")
        print("=" * 50)
        
        if self.config:
            print("[SUCCESS] Configuration Status: LOADED")
            print(f"[CONNECT] FTP Host: {self.config.get('ftp_host', 'Not configured')}")
            print(f" FTP Username: {self.config.get('ftp_username', 'Not configured')}")
            print(f"[WEB] Website URL: {self.config.get('website_url', 'Not configured')}")
        else:
            print("[ERROR] Configuration Status: NOT LOADED")
            print(" Check godaddy_config.json file exists and is valid")
        
        # Check if website directory exists and has content
        if self.script_dir.exists():
            print(f"[SUCCESS] Website Directory: {self.script_dir}")
            
            # Count files
            html_files = list(self.script_dir.glob("*.html"))
            css_files = list(self.script_dir.glob("*.css"))
            js_files = list(self.script_dir.glob("*.js"))
            
            print(f"[FILE] HTML files: {len(html_files)}")
            print(f" CSS files: {len(css_files)}")
            print(f"[GEAR]  JS files: {len(js_files)}")
            
            # Check for key files
            if (self.script_dir / "index.html").exists():
                print("[SUCCESS] Main index.html found")
            else:
                print("[ERROR] index.html not found")
                
        else:
            print("[ERROR] Website directory not found")
        
        print("=" * 50)


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(
        description="Standalone ProBrep.com Deployment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy_probrep_standalone.py test      # Test FTP connection
  python deploy_probrep_standalone.py deploy    # Deploy website
  python deploy_probrep_standalone.py verify    # Verify deployment
  python deploy_probrep_standalone.py status    # Show status
        """
    )
    
    parser.add_argument(
        'action',
        choices=['test', 'deploy', 'verify', 'status'],
        help='Action to perform'
    )
    
    args = parser.parse_args()
    
    # Create deployment instance
    deployment = ProBrepDeployment()
    
    print(f"ProBrep.com Deployment Tool - {args.action.upper()}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Execute requested action
    success = False
    
    if args.action == 'test':
        success = deployment.test_connection()
    elif args.action == 'deploy':
        success = deployment.deploy_website()
    elif args.action == 'verify':
        success = deployment.verify_deployment()
    elif args.action == 'status':
        deployment.show_status()
        success = True
    
    print()
    print(f"[TIME] Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("[SUCCESS] Operation completed successfully!")
        sys.exit(0)
    else:
        print("[ERROR] Operation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
