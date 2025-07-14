# 🔧 DEPLOYMENT SCRIPT TROUBLESHOOTING

## Common Issues and Solutions

### 1. **Authentication Error**
If you see authentication errors when pushing to GitHub:

**Solution A - Use GitHub Token:**
```bash
git remote set-url origin https://YOUR_GITHUB_TOKEN@github.com/infosquawk/ca-probate-appellate-repository.git
```

**Solution B - GitHub CLI (if installed):**
```bash
gh auth login
```

**Solution C - Manual Authentication:**
- Git will prompt for username: `infosquawk`
- Git will prompt for password: Use your GitHub personal access token

### 2. **Repository Not Found Error**
**Check:** 
- Repository exists: https://github.com/infosquawk/ca-probate-appellate-repository
- Repository is public
- Repository name is spelled correctly

### 3. **Permission Denied**
**Solutions:**
- Use your GitHub token as password
- Check repository permissions
- Ensure you're logged in as `infosquawk`

### 4. **Git Not Found**
**Install Git:**
- Download from: https://git-scm.com/
- Add to Windows PATH
- Restart Command Prompt

### 5. **Directory Access Issues**
**Solutions:**
- Run Command Prompt as Administrator
- Check file permissions
- Ensure directories exist

## Manual Backup Method

If the script fails, you can manually upload via GitHub web interface:

1. Go to your repository: https://github.com/infosquawk/ca-probate-appellate-repository
2. Click "uploading an existing file"
3. Drag and drop all files from: `C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\`
4. Commit changes

## Verify Deployment

After successful deployment:
1. Wait 2-5 minutes for GitHub Pages to build
2. Visit: https://infosquawk.github.io/ca-probate-appellate-repository
3. Check that your website loads correctly

## Enable GitHub Pages (if not done)

1. Go to repository Settings
2. Click "Pages" in sidebar
3. Source: "Deploy from a branch"
4. Branch: "main"
5. Folder: "/ (root)"
6. Save

Your website will be live at: https://infosquawk.github.io/ca-probate-appellate-repository
