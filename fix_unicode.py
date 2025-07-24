#!/usr/bin/env python3
"""
Fix Unicode characters in deployment script
"""

import re

# Read the current deployment script
script_path = "deploy_probrep_standalone.py"

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Unicode emojis with text equivalents
replacements = {
    '🌐': '[WEB]',
    '⏰': '[TIME]',
    '✅': '[SUCCESS]',
    '❌': '[ERROR]',
    '⚠️': '[WARNING]',
    '📁': '[FOLDER]',
    '📄': '[FILE]', 
    '⏭️': '[NEXT]',
    '⚙️': '[GEAR]',
    '📡': '[CONNECT]'
}

# Apply replacements
for emoji, replacement in replacements.items():
    content = content.replace(emoji, replacement)

# Remove any remaining Unicode characters above ASCII range
content = re.sub(r'[^\x00-\x7F]+', '', content)

# Write back the fixed content
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Unicode characters fixed in deployment script!")
