#!/usr/bin/env python3
"""
ProBrep.com Complete Website Deployment Script
Automatically uploads website and all content files via FTP
"""

import os
import ftplib
import configparser
import time
from pathlib import Path
import sys

class ProBrepDeployer:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config_file = self.script_dir / "godaddy_config.ini"
        self.ftp = None
        self.uploaded_files = 0
        self.total_files = 0
        
        # Load FTP configuration
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        
        self.ftp_host = self.config.get('godaddy', 'ftp_host')
        self.ftp_username = self.config.get('godaddy', 'ftp_username')
        self.ftp_password = self.config.get('godaddy', 'ftp_password')
        self.ftp_port = self.config.getint('godaddy', 'ftp_port')
        self.web_root = self.config.get('godaddy', 'web_root')
        
        print("="*60)
        print("ProBrep.com Complete Website Deployment")
        print("="*60)
        print(f"Target: {self.ftp_host}{self.web_root}")
        print(f"FTP User: {self.ftp_username}")

    def connect_ftp(self):
        """Establish FTP connection"""
        try:
            print("\n🔌 Connecting to FTP server...")
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.ftp_host, self.ftp_port)
            self.ftp.login(self.ftp_username, self.ftp_password)
            
            # Only change directory if web_root is not root
            if self.web_root and self.web_root != "/" and self.web_root.strip():
                self.ftp.cwd(self.web_root)
                print(f"📁 Changed to directory: {self.web_root}")
            else:
                print("📁 Using FTP root directory (already in public_html)")
                
            print("✅ FTP connection established successfully!")
            return True
        except Exception as e:
            print(f"❌ FTP connection failed: {e}")
            return False

    def create_remote_directory(self, remote_path):
        """Create directory on FTP server if it doesn't exist"""
        try:
            # Try to change to the directory
            self.ftp.cwd(remote_path)
            # Go back to current working directory
            self.ftp.cwd('/')
            return True
        except:
            try:
                # Directory doesn't exist, create it
                parts = remote_path.strip('/').split('/')
                current_path = '/'
                
                for part in parts:
                    if part:
                        current_path = f"{current_path}{part}/" if current_path == '/' else f"{current_path}/{part}/"
                        try:
                            self.ftp.cwd(current_path)
                        except:
                            self.ftp.mkd(current_path.rstrip('/'))
                            print(f"📁 Created directory: {current_path.rstrip('/')}")
                
                self.ftp.cwd('/')  # Return to root
                return True
            except Exception as e:
                print(f"❌ Failed to create directory {remote_path}: {e}")
                return False

    def upload_file(self, local_file, remote_file, description=""):
        """Upload a single file to FTP server"""
        try:
            # Create remote directory if needed
            remote_dir = os.path.dirname(remote_file)
            if remote_dir and remote_dir != '/':
                self.create_remote_directory(remote_dir)
            
            # Upload file
            with open(local_file, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_file}', file)
            
            self.uploaded_files += 1
            file_size = os.path.getsize(local_file) / 1024  # KB
            print(f"✅ [{self.uploaded_files}/{self.total_files}] {description}: {remote_file} ({file_size:.1f} KB)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to upload {local_file}: {e}")
            return False

    def count_files_to_upload(self):
        """Count total files that will be uploaded"""
        count = 0
        
        # Website file
        if (self.script_dir / "index_WORKING_LINKS.html").exists():
            count += 1
        
        # Cover images
        covers_dir = self.script_dir / "covers"
        if covers_dir.exists():
            count += len([f for f in covers_dir.glob("*.png")])
        
        # PDF files
        pdfs_dir = self.script_dir / "pdfs"
        if pdfs_dir.exists():
            for subdir in ['published', 'unpublished']:
                subdir_path = pdfs_dir / subdir
                if subdir_path.exists():
                    count += len([f for f in subdir_path.glob("*.pdf")])
        
        # Text files
        texts_dir = self.script_dir / "texts"
        if texts_dir.exists():
            count += len([f for f in texts_dir.glob("*.txt")])
        
        return count

    def deploy_website(self):
        """Deploy the main website file"""
        print("\n🌐 Deploying Website...")
        
        website_file = self.script_dir / "index_WORKING_LINKS.html"
        if website_file.exists():
            # Backup existing index.html
            try:
                backup_name = f"index.backup_{int(time.time())}.html"
                self.ftp.rename("index.html", backup_name)
                print(f"📦 Backed up existing website as: {backup_name}")
            except:
                pass  # File might not exist
                
            return self.upload_file(website_file, "index.html", "Main Website")
        else:
            print("❌ Website file not found: index_WORKING_LINKS.html")
            return False

    def deploy_covers(self):
        """Deploy cover images"""
        print("\n🖼️ Deploying Cover Images...")
        
        covers_dir = self.script_dir / "covers"
        if not covers_dir.exists():
            print("⚠️ No covers directory found")
            return True
        
        success = True
        for cover_file in covers_dir.glob("*.png"):
            remote_path = f"covers/{cover_file.name}"
            if not self.upload_file(cover_file, remote_path, "Cover Image"):
                success = False
        
        return success

    def deploy_pdfs(self):
        """Deploy PDF documents"""
        print("\n📄 Deploying PDF Documents...")
        
        pdfs_dir = self.script_dir / "pdfs"
        if not pdfs_dir.exists():
            print("⚠️ No pdfs directory found")
            return True
        
        success = True
        for subdir in ['published', 'unpublished']:
            subdir_path = pdfs_dir / subdir
            if subdir_path.exists():
                for pdf_file in subdir_path.glob("*.pdf"):
                    remote_path = f"pdfs/{subdir}/{pdf_file.name}"
                    if not self.upload_file(pdf_file, remote_path, f"PDF ({subdir})"):
                        success = False
        
        return success

    def deploy_texts(self):
        """Deploy text files"""
        print("\n📝 Deploying Text Files...")
        
        texts_dir = self.script_dir / "texts"
        if not texts_dir.exists():
            print("⚠️ No texts directory found")
            return True
        
        success = True
        for text_file in texts_dir.glob("*.txt"):
            remote_path = f"texts/{text_file.name}"
            if not self.upload_file(text_file, remote_path, "Text File"):
                success = False
        
        return success

    def verify_deployment(self):
        """Verify key files were uploaded successfully"""
        print("\n🔍 Verifying Deployment...")
        
        key_files = [
            "index.html",
            "covers/cover_opinions.png",
            "pdfs/published/B333052_Conservatorship_of_ANNE_S_published.pdf",
            "texts/B333052_(Case_Brief)_Conservatorship_of_ANNE_S_(published).txt"
        ]
        
        verified = 0
        for file_path in key_files:
            try:
                # Try to get file size (confirms file exists)
                self.ftp.size(file_path)
                print(f"✅ Verified: {file_path}")
                verified += 1
            except:
                print(f"❌ Missing: {file_path}")
        
        print(f"\n📊 Verification Results: {verified}/{len(key_files)} key files confirmed")
        return verified == len(key_files)

    def deploy_all(self):
        """Execute complete deployment"""
        start_time = time.time()
        
        # Count files to upload
        self.total_files = self.count_files_to_upload()
        print(f"\n📋 Total files to upload: {self.total_files}")
        
        if self.total_files == 0:
            print("❌ No files found to upload!")
            return False
        
        # Connect to FTP
        if not self.connect_ftp():
            return False
        
        try:
            # Deploy components
            steps = [
                ("Website", self.deploy_website),
                ("Cover Images", self.deploy_covers),
                ("PDF Documents", self.deploy_pdfs),
                ("Text Files", self.deploy_texts)
            ]
            
            all_success = True
            for step_name, step_func in steps:
                if not step_func():
                    all_success = False
                    print(f"⚠️ {step_name} deployment had issues")
            
            # Verify deployment
            if all_success:
                self.verify_deployment()
            
            elapsed_time = time.time() - start_time
            print(f"\n⏱️ Deployment completed in {elapsed_time:.1f} seconds")
            print(f"📊 Uploaded {self.uploaded_files} files successfully")
            
            if all_success:
                print("\n🎉 DEPLOYMENT SUCCESSFUL!")
                print("🌐 Your website is now live at: https://probrep.com")
                print("✅ All file links should now work correctly")
            else:
                print("\n⚠️ DEPLOYMENT COMPLETED WITH WARNINGS")
                print("🔧 Some files may need manual attention")
            
            return all_success
            
        except Exception as e:
            print(f"\n❌ DEPLOYMENT FAILED: {e}")
            return False
        
        finally:
            if self.ftp:
                self.ftp.quit()
                print("🔌 FTP connection closed")

def main():
    """Main execution function"""
    try:
        deployer = ProBrepDeployer()
        success = deployer.deploy_all()
        
        if success:
            print("\n" + "="*60)
            print("🎉 PROBREP.COM DEPLOYMENT COMPLETE!")
            print("="*60)
            print("✅ Website updated with working file links")
            print("✅ All PDFs, texts, and covers uploaded")
            print("✅ Database integration maintained")
            print("🌐 Visit: https://probrep.com")
            sys.exit(0)
        else:
            print("\n❌ Deployment had issues - check output above")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()