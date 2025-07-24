#!/usr/bin/env python3
"""
Simple diagnostic script to check HTML file
"""

import re
from pathlib import Path

print("Checking local HTML file for JavaScript issues...")

# Check the local HTML file for potential issues
html_path = Path("index.html")
if html_path.exists():
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("HTML file found and loaded successfully")
    
    # Check for common JavaScript issues
    if "const episodes = [" in content:
        print("Episodes array declaration found")
    else:
        print("ERROR: Episodes array declaration missing or malformed")
    
    if 'episodes.forEach' in content:
        print("Episodes rendering code found")
    else:
        print("ERROR: Episodes rendering code not found")
    
    # Check for syntax issues
    brace_balance = content.count('{') - content.count('}')
    if brace_balance == 0:
        print("Braces are balanced")
    else:
        print(f"ERROR: Mismatched braces (difference: {brace_balance})")
        
    # Extract episode count
    episode_matches = re.findall(r'"id":\s*\d+', content)
    print(f"Found {len(episode_matches)} episodes in HTML")
    
    # Check for trailing commas in last episode
    episodes_section = content[content.find("const episodes = ["):content.find("];")]
    if episodes_section.count("},\n]") > 0 or episodes_section.count("},]") > 0:
        print("ERROR: Trailing comma found in episodes array")
    else:
        print("No trailing comma issues detected")
    
    # Check for specific error patterns
    if '"},\n        ];' in content:
        print("ERROR: Trailing comma before array close found!")
    
    print(f"Total content length: {len(content)} characters")
    
else:
    print("ERROR: Local index.html file not found")

print("Diagnostic complete!")
