#!/usr/bin/env python3

import json
import ftplib
from pathlib import Path

def deploy_fixed():
    website_dir = Path(__file__).parent
    
    # Load config
    config_files = [
        website_dir.parent / "godaddy_config.json",
        website_dir / "godaddy_config.json"
    ]
    
    config = None
    for config_file in config_files:
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✓ Loaded config from {config_file}")
            break
    
    if not config:
        print("ERROR: No godaddy_config.json found!")
        return False
    
    index_file = website_dir / "index.html"
    if not index_file.exists():
        print("ERROR: index.html not found!")
        return False
    
    print(f"✓ Found index.html ({index_file.stat().st_size} bytes)")
    
    try:
        ftp = ftplib.FTP()
        ftp.connect(config['ftp_host'], 21)
        ftp.login(config['ftp_username'], config['ftp_password'])
        print("✓ Connected to FTP server")
        
        # Try public_html first (most likely correct location)
        try:
            ftp.cwd('/public_html')
            print("✓ Changed to /public_html directory")
            
            # Upload index.html
            with open(index_file, 'rb') as f:
                ftp.storbinary('STOR index.html', f)
            print("✓ index.html uploaded to /public_html")
            
            # Upload covers
            covers_dir = website_dir / "covers"
            if covers_dir.exists():
                print("Uploading covers...")
                try:
                    ftp.mkd('covers')
                except:
                    pass  # Directory might already exist
                    
                for cover_file in covers_dir.glob("*.png"):
                    with open(cover_file, 'rb') as f:
                        ftp.storbinary(f'STOR covers/{cover_file.name}', f)
                    print(f"  ✓ Uploaded {cover_file.name}")
            
            # Upload PDFs
            pdfs_dir = website_dir / "pdfs"
            if pdfs_dir.exists():
                print("Uploading PDFs...")
                try:
                    ftp.mkd('pdfs')
                except:
                    pass
                    
                for subdir in ['published', 'unpublished']:
                    subdir_path = pdfs_dir / subdir
                    if subdir_path.exists():
                        try:
                            ftp.mkd(f'pdfs/{subdir}')
                        except:
                            pass
                        for pdf_file in subdir_path.glob("*.pdf"):
                            with open(pdf_file, 'rb') as f:
                                ftp.storbinary(f'STOR pdfs/{subdir}/{pdf_file.name}', f)
                            print(f"  ✓ Uploaded {pdf_file.name}")
            
            print("\n" + "="*50)
            print("✓ DEPLOYMENT SUCCESSFUL to /public_html")
            print("✓ All files uploaded successfully")
            print("✓ Website should be live at: https://probrep.com")
            print("✓ Allow 5-15 minutes for changes to appear")
            print("="*50)
            
        except Exception as e:
            print(f"❌ Failed to upload to /public_html: {e}")
            print("Trying root directory as fallback...")
            
            ftp.cwd('/')
            with open(index_file, 'rb') as f:
                ftp.storbinary('STOR index.html', f)
            print("✓ Uploaded to root directory")
            print("⚠ Files may not be visible - contact GoDaddy support")
        
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"❌ DEPLOYMENT FAILED: {e}")
        return False

if __name__ == "__main__":
    deploy_fixed()
