#!/usr/bin/env python3
"""
Diagnostic script to check website issues
"""

import requests
import json
from pathlib import Path

# Test different URLs to see what's accessible
test_urls = [
    "https://probrep.com",
    "https://probrep.com/covers/cover_opinions.png",
    "https://probrep.com/pdfs/",
    "https://probrep.com/texts/",
    "https://probrep.com/index.html"
]

for url in test_urls:
    try:
        response = requests.get(url, timeout=10)
        print(f"✓ {url} -> Status: {response.status_code}")
        if url.endswith('.png'):
            print(f"  Image size: {len(response.content)} bytes")
        elif url.endswith('/'):
            print(f"  Content preview: {response.text[:100]}...")
    except Exception as e:
        print(f"✗ {url} -> Error: {e}")

print("\n" + "="*50)
print("Checking local HTML file for JavaScript issues...")

# Check the local HTML file for potential issues
html_path = Path("index.html")
if html_path.exists():
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for common JavaScript issues
    if "const episodes = [" in content:
        print("✓ Episodes array declaration found")
    else:
        print("✗ Episodes array declaration missing or malformed")
    
    if 'episodes.forEach' in content:
        print("✓ Episodes rendering code found")
    else:
        print("✗ Episodes rendering code not found")
    
    # Check for syntax issues
    if content.count('{') != content.count('}'):
        print("✗ Mismatched braces detected")
    else:
        print("✓ Braces are balanced")
        
    # Extract episode count
    import re
    episode_matches = re.findall(r'"id":\s*\d+', content)
    print(f"✓ Found {len(episode_matches)} episodes in HTML")
    
else:
    print("✗ Local index.html file not found")

print("Diagnostic complete!")
