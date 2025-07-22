# ProBRep.com GoDaddy Migration Setup Instructions

## Overview
This directory contains all the scripts needed to migrate your Scholar Podcast pipeline from GitHub Pages to ProBRep.com GoDaddy hosting.

## Files in This Directory

### 1. `test_ftp_connection.py`
- **Purpose**: Test FTP connection to ProBRep.com
- **Usage**: `python test_ftp_connection.py`
- **What it does**: 
  - Tests FTP credentials
  - Verifies upload permissions
  - Creates the configuration file automatically

### 2. `godaddy_config.ini`
- **Purpose**: Configuration template for ProBRep.com hosting
- **Contains**: FTP credentials, domain settings, deployment options
- **Note**: Will be created automatically by the test script

### 3. `godaddy_deployment_pipeline.py`
- **Purpose**: Main deployment script for uploading to GoDaddy
- **Usage**: `python godaddy_deployment_pipeline.py`
- **What it does**:
  - Uploads all website files to ProBRep.com
  - Creates directories as needed
  - Verifies successful deployment

### 4. `website_integration_pipeline_godaddy.py`
- **Purpose**: Updated Phase 5 integration for GoDaddy hosting
- **Usage**: Called automatically by the main pipeline
- **What it does**:
  - Syncs content from podcast pipeline
  - Updates website URLs for ProBRep.com
  - Deploys to GoDaddy hosting

### 5. `run_enhanced_pipeline_fixed2_GODADDY.bat`
- **Purpose**: Updated main pipeline batch file
- **Usage**: Replace your existing `run_enhanced_pipeline_fixed2.bat`
- **What it does**:
  - Runs all 4 existing phases
  - Adds Phase 5 with GoDaddy deployment

## Quick Setup Process

### Step 1: Test FTP Connection (5 minutes)
```bash
cd C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\godaddy_initiation_scripts
python test_ftp_connection.py
```

**Expected Output:**
```
✓ FTP connection established
✓ FTP login successful
✓ Successfully navigated to public_html
✓ READY FOR DEPLOYMENT
```

### Step 2: Copy Configuration File (1 minute)
The test script will create `godaddy_config.ini`. Copy it to the parent directory:
```bash
copy godaddy_config.ini ..\godaddy_config.ini
```

### Step 3: Copy Deployment Scripts (2 minutes)
Copy the deployment scripts to the website directory:
```bash
copy godaddy_deployment_pipeline.py ..\godaddy_deployment_pipeline.py
copy website_integration_pipeline_godaddy.py ..\website_integration_pipeline_godaddy.py
```

### Step 4: Update Main Pipeline (2 minutes)
Replace your main pipeline batch file:
```bash
copy run_enhanced_pipeline_fixed2_GODADDY.bat ..\..\run_enhanced_pipeline_fixed2.bat
```

**WARNING**: This will overwrite your existing batch file. Make a backup first if needed.

### Step 5: Test Manual Deployment (5 minutes)
Test the deployment manually:
```bash
cd ..\
python godaddy_deployment_pipeline.py
```

### Step 6: Test Full Pipeline (10 minutes)
Run your complete pipeline with GoDaddy deployment:
```bash
cd ..\..\
C:\Windows\System32\cmd.exe /K ""C:\ProgramData\Anaconda3\Scripts\activate.bat" && CALL "C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\run_enhanced_pipeline_fixed2.bat""
```

## What Changes After Migration

### ✅ New Website URL:
- **Old**: `https://infosquawk.github.io/ca-probate-appellate-repository`
- **New**: `https://probrep.com`

### ✅ Same Functionality:
- All 4 phases of content creation work exactly the same
- Website interface remains identical
- Search, navigation, and podcast links all work
- Same command to run the pipeline

### ✅ Better Control:
- Full control over hosting environment
- Custom domain (probrep.com)
- No GitHub Pages limitations
- Professional domain structure

## Troubleshooting

### If FTP Test Fails:
1. **Check credentials**: Verify in GoDaddy control panel
2. **Check FTP enabled**: Ensure FTP is active in hosting settings
3. **Try FileZilla**: Test with manual FTP client
4. **Contact GoDaddy**: Verify hosting plan includes FTP

### If Deployment Fails:
1. **Check permissions**: Ensure write access to public_html
2. **Check space**: Verify sufficient storage
3. **Check logs**: Review `website/logs/` for details
4. **Manual upload**: Try uploading one file manually via FTP

### If Website Doesn't Load:
1. **Check DNS**: Ensure probrep.com points to GoDaddy
2. **Check SSL**: Verify SSL certificate is active
3. **Check files**: Confirm index.html in public_html
4. **Wait**: DNS changes can take 24 hours

## File Structure After Setup

```
scholar_podcast/
├── run_enhanced_pipeline_fixed2.bat          # UPDATED: Now deploys to ProBRep.com
└── website/
    ├── godaddy_config.ini                     # NEW: Your FTP credentials
    ├── godaddy_deployment_pipeline.py         # NEW: Main deployment
    ├── website_integration_pipeline_godaddy.py  # NEW: Integration script
    ├── index.html                             # EXISTING: Will upload to ProBRep.com
    └── godaddy_initiation_scripts/            # NEW: This directory with all scripts
        ├── test_ftp_connection.py
        ├── godaddy_config.ini
        ├── godaddy_deployment_pipeline.py
        ├── website_integration_pipeline_godaddy.py
        ├── run_enhanced_pipeline_fixed2_GODADDY.bat
        └── SETUP_INSTRUCTIONS.md
```

## Support

### For FTP Issues:
- **GoDaddy Support**: Available via chat/phone
- **Manual Testing**: Use FileZilla or WinSCP

### For Pipeline Issues:
- **Check logs**: `website/logs/` directory
- **Test individually**: Run each script separately
- **Rollback**: Keep GitHub Pages active during testing

## Success Verification

### ✅ Migration Complete When:
- [ ] FTP test passes
- [ ] Manual deployment succeeds  
- [ ] Full pipeline runs without errors
- [ ] Website loads at `https://probrep.com`
- [ ] All functionality works (search, links, downloads)

## Need Help?

If you encounter any issues:

1. **Check this file** for troubleshooting steps
2. **Review logs** in `website/logs/` directory
3. **Test components individually** before running full pipeline
4. **Keep GitHub Pages active** as backup during migration

---

**Ready to Start?**

Run this command to begin:
```bash
python test_ftp_connection.py
```

If successful, follow the 6-step setup process above!
