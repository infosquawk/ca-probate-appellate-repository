#!/usr/bin/env python3
"""
Quick deployment script for website link fix
Deploys the corrected link labels to GitHub Pages
"""

import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def deploy_website_fix():
    """Deploy the website link fix to GitHub Pages"""
    
    # Configuration
    GITHUB_USERNAME = "infosquawk"
    REPOSITORY_NAME = "ca-probate-appellate-repository"
    WEBSITE_SOURCE_DIR = Path(__file__).parent
    GIT_CLONE_DIR = Path("C:/Users/Ryan/GitHub")
    REPO_LOCAL_PATH = GIT_CLONE_DIR / REPOSITORY_NAME
    
    print("🚀 Deploying Website Link Fix")
    print("="*50)
    print(f"Repository: {GITHUB_USERNAME}/{REPOSITORY_NAME}")
    print(f"Source: {WEBSITE_SOURCE_DIR}")
    print(f"Target: {REPO_LOCAL_PATH}")
    print()
    
    # Create GitHub directory if needed
    GIT_CLONE_DIR.mkdir(exist_ok=True)
    
    # Change to GitHub directory
    os.chdir(GIT_CLONE_DIR)
    
    # Check if repo exists, clone or pull
    if REPO_LOCAL_PATH.exists():
        print("📂 Repository exists locally, pulling latest changes...")
        os.chdir(REPO_LOCAL_PATH)
        success, output = run_command("git pull origin main")
        if not success:
            print(f"⚠️  Warning: Could not pull latest changes: {output}")
    else:
        print("📥 Cloning repository...")
        success, output = run_command(f"git clone https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}.git")
        if not success:
            print(f"❌ Failed to clone repository: {output}")
            return False
        os.chdir(REPO_LOCAL_PATH)
    
    # Configure git
    print("🔧 Configuring Git...")
    run_command(f"git config user.name '{GITHUB_USERNAME}'")
    run_command(f"git config user.email '{GITHUB_USERNAME}@users.noreply.github.com'")
    
    # Copy the updated index.html
    print("📋 Copying updated index.html...")
    source_file = WEBSITE_SOURCE_DIR / "index.html"
    target_file = REPO_LOCAL_PATH / "index.html"
    
    if source_file.exists():
        shutil.copy2(source_file, target_file)
        print("✅ Updated index.html copied")
    else:
        print(f"❌ Source file not found: {source_file}")
        return False
    
    # Check for changes
    success, output = run_command("git diff --name-only")
    if not output.strip():
        print("ℹ️  No changes detected - already up to date")
        return True
    
    print(f"📋 Changes detected in: {output.strip()}")
    
    # Add, commit, and push
    print("📤 Adding changes to Git...")
    success, output = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {output}")
        return False
    
    print("💾 Committing changes...")
    commit_message = f"Fix link labels in Opinion posts - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    success, output = run_command(f"git commit -m \"{commit_message}\"")
    if not success:
        print(f"❌ Failed to commit: {output}")
        return False
    
    print("🚀 Pushing to GitHub...")
    success, output = run_command("git push origin main")
    if not success:
        print(f"❌ Failed to push: {output}")
        return False
    
    print()
    print("="*50)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("="*50)
    print(f"🌐 Website will be updated at: https://{GITHUB_USERNAME}.github.io/{REPOSITORY_NAME}")
    print("📋 Changes made:")
    print("   • Opinion posts now show 'Case Text' instead of 'Case Brief'")
    print("   • Brief posts still show 'Case Brief' (unchanged)")
    print("   • Analysis posts still show 'Text' (unchanged)")
    print()
    print("⏱️  GitHub Pages deployment typically takes 2-5 minutes")
    print()
    
    return True

if __name__ == "__main__":
    success = deploy_website_fix()
    if success:
        print("🎉 Link fix deployment completed successfully!")
    else:
        print("❌ Deployment failed - check error messages above")
