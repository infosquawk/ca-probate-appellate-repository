#!/usr/bin/env python3
"""
Manual Deployment Test for ProBRep.com - UPDATED CREDENTIALS  
Upload a simple test page to verify live website functionality
"""

import ftplib
from io import BytesIO
from datetime import datetime

def deploy_test_page():
    """Deploy a simple test page to ProBRep.com"""
    
    print("=== ProBRep.com Manual Deployment Test ===")
    
    # Updated FTP settings (sysop2 account)
    ftp_host = "probrep.com"
    ftp_user = "sysop2@probrep.com"  # UPDATED
    ftp_pass = "nq6FRcSQk8i5chh"     # UPDATED
    
    # Create test HTML page
    test_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProBRep.com - Migration Test</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        .status {{
            background: rgba(46, 204, 113, 0.8);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
        }}
        .info {{
            background: rgba(52, 152, 219, 0.8);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .timestamp {{
            text-align: center;
            opacity: 0.8;
            margin-top: 20px;
        }}
        .next-steps {{
            background: rgba(230, 126, 34, 0.8);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        ul {{
            margin: 10px 0;
        }}
        li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ProBRep.com</h1>
        
        <div class="status">
            ✅ MIGRATION TEST SUCCESSFUL!
        </div>
        
        <div class="info">
            <h3>📋 System Status</h3>
            <ul>
                <li><strong>Domain:</strong> probrep.com</li>
                <li><strong>Hosting:</strong> GoDaddy (Active)</li>
                <li><strong>FTP Deployment:</strong> Working</li>
                <li><strong>SSL Certificate:</strong> <span id="ssl-status">Checking...</span></li>
                <li><strong>DNS Resolution:</strong> 208.109.58.241</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>📈 California Probate Repository</h3>
            <p>Professional legal resource for California appellate court probate decisions.</p>
            <ul>
                <li>Automated content pipeline integration</li>
                <li>AI-powered case brief generation</li>
                <li>Podcast episode hosting and distribution</li>
                <li>Professional legal document access</li>
            </ul>
        </div>
        
        <div class="next-steps">
            <h3>🎯 Next Steps</h3>
            <ol>
                <li>Complete pipeline script deployment</li>
                <li>Test full integration with existing content</li>
                <li>Deploy production website</li>
                <li>Update podcast RSS feeds</li>
                <li>Monitor performance and analytics</li>
            </ol>
        </div>
        
        <div class="timestamp">
            <p>Deployment Test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Scholar Podcast Pipeline → ProBRep.com Migration</p>
        </div>
    </div>
    
    <script>
        // Check if page loaded over HTTPS
        if (location.protocol === 'https:') {{
            document.getElementById('ssl-status').innerHTML = '✅ Active (HTTPS)';
            document.getElementById('ssl-status').style.color = '#2ecc71';
        }} else {{
            document.getElementById('ssl-status').innerHTML = '⚠️ HTTP Only';
            document.getElementById('ssl-status').style.color = '#f39c12';
        }}
    </script>
</body>
</html>"""
    
    try:
        print("Connecting to ProBRep.com...")
        print(f"Using account: {ftp_user}")
        
        # Connect and login
        ftp = ftplib.FTP()
        ftp.connect(ftp_host, 21, timeout=10)
        ftp.login(ftp_user, ftp_pass)
        print("✓ Connected and authenticated")
        
        # Change to public_html directory
        try:
            ftp.cwd('public_html')
            print("✓ Changed to /public_html directory")
        except ftplib.error_perm:
            print("⚠ Warning: Could not access public_html directory, using root")
            print("  This may indicate a different hosting setup")
        
        # Upload test page as index.html
        print("Uploading test page...")
        html_file = BytesIO(test_html.encode('utf-8'))
        ftp.storbinary('STOR index.html', html_file)
        print("✓ Test page uploaded as index.html")
        
        # Verify upload
        files = ftp.nlst()
        if 'index.html' in files:
            size = ftp.size('index.html')
            print(f"✓ Upload verified - Size: {size} bytes")
        
        ftp.quit()
        print("✓ FTP connection closed")
        
        print("\n" + "="*50)
        print("🌐 MANUAL DEPLOYMENT SUCCESSFUL!")
        print(f"📧 FTP Account: {ftp_user}")
        print("\n🔗 Test your live website:")
        print("   HTTP:  http://probrep.com")
        print("   HTTPS: https://probrep.com")
        print("\n✅ What to verify:")
        print("   1. Page loads correctly")
        print("   2. SSL certificate works (green lock)")
        print("   3. Content displays properly")
        print("   4. No browser errors")
        print("   5. Migration test status shows successful")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Manual deployment failed: {e}")
        return False

if __name__ == "__main__":
    print("ProBRep.com Manual Deployment Test - UPDATED CREDENTIALS")
    print("="*55)
    
    success = deploy_test_page()
    
    if success:
        print("\n🎯 READY FOR FULL MIGRATION!")
        print("Your website is live and ready for pipeline integration.")
    else:
        print("\n❌ Manual deployment issues need resolution.")
