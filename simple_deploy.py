#!/usr/bin/env python3
"""
Simple ProBrep.com Deployment Script - No Unicode
Direct FTP deployment without emoji characters
"""

import os
import json
import ftplib
import logging
from pathlib import Path

def simple_probrep_deployment():
    """Simple ProBrep deployment without Unicode issues"""
    
    # Setup basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    print("Simple ProBrep.com Deployment")
    print("=" * 50)
    
    # Load FTP configuration
    try:
        with open('godaddy_config.ini', 'r') as f:
            content = f.read()
            
        # Parse basic config
        ftp_host = "probrep.com"
        ftp_username = "sysop2@probrep.com"
        ftp_password = "3YXdwJJXdVaZ6mf"
        
        print(f"FTP Host: {ftp_host}")
        print(f"FTP User: {ftp_username}")
        
    except Exception as e:
        print(f"Config error: {e}")
        return False
    
    # Connect to FTP
    try:
        print("Connecting to FTP server...")
        ftp = ftplib.FTP()
        ftp.connect(ftp_host)
        ftp.login(ftp_username, ftp_password)
        print("FTP connection successful!")
        
        # Upload main website file
        print("Uploading index.html...")
        if os.path.exists('index.html'):
            with open('index.html', 'rb') as f:
                ftp.storbinary('STOR index.html', f)
            print("index.html uploaded successfully")
        else:
            print("index.html not found")
            
        # Upload covers directory
        print("Creating covers directory...")
        try:
            ftp.mkd('covers')
        except:
            pass
            
        ftp.cwd('covers')
        covers_dir = Path('covers')
        if covers_dir.exists():
            for cover_file in covers_dir.glob('*.png'):
                print(f"Uploading {cover_file.name}...")
                with open(cover_file, 'rb') as f:
                    ftp.storbinary(f'STOR {cover_file.name}', f)
        ftp.cwd('..')
        
        # Upload PDFs directory
        print("Creating pdfs directory...")
        try:
            ftp.mkd('pdfs')
        except:
            pass
            
        ftp.cwd('pdfs')
        
        # Published PDFs
        try:
            ftp.mkd('published')
        except:
            pass
        ftp.cwd('published')
        
        published_dir = Path('pdfs/published')
        if published_dir.exists():
            for pdf_file in published_dir.glob('*.pdf'):
                print(f"Uploading {pdf_file.name}...")
                with open(pdf_file, 'rb') as f:
                    ftp.storbinary(f'STOR {pdf_file.name}', f)
        ftp.cwd('..')
        
        # Unpublished PDFs
        try:
            ftp.mkd('unpublished')
        except:
            pass
        ftp.cwd('unpublished')
        
        unpublished_dir = Path('pdfs/unpublished')
        if unpublished_dir.exists():
            for pdf_file in unpublished_dir.glob('*.pdf'):
                print(f"Uploading {pdf_file.name}...")
                with open(pdf_file, 'rb') as f:
                    ftp.storbinary(f'STOR {pdf_file.name}', f)
        ftp.cwd('..')
        ftp.cwd('..')  # Back to root
        
        # Upload texts directory
        print("Creating texts directory...")
        try:
            ftp.mkd('texts')
        except:
            pass
            
        ftp.cwd('texts')
        texts_dir = Path('texts')
        if texts_dir.exists():
            for txt_file in texts_dir.glob('*.txt'):
                print(f"Uploading {txt_file.name}...")
                with open(txt_file, 'rb') as f:
                    ftp.storbinary(f'STOR {txt_file.name}', f)
        ftp.cwd('..')
        
        ftp.quit()
        print("=" * 50)
        print("DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("Website available at: https://probrep.com")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

if __name__ == "__main__":
    success = simple_probrep_deployment()
    if success:
        print("SUCCESS: ProBrep.com deployment completed")
        exit(0)
    else:
        print("FAILED: ProBrep.com deployment failed")
        exit(1)
