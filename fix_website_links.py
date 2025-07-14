import json
import os
import re

def fix_website_links():
    """Fix the website links to make them functional"""
    
    # Read the current index.html
    website_path = r"C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\index.html"
    
    with open(website_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the episodes JavaScript array
    episodes_match = re.search(r'const episodes = (\[.*?\]);', content, re.DOTALL)
    if not episodes_match:
        print("❌ Could not find episodes array in HTML")
        return
    
    episodes_json = episodes_match.group(1)
    episodes = json.loads(episodes_json)
    
    print("🔧 Fixing episode links...")
    
    # Fix each episode
    for episode in episodes:
        episode_id = episode.get('id', 'unknown')
        title = episode.get('title', 'Unknown')
        
        # Fix audio URLs - disable buttons for placeholder links
        if episode.get('audioUrl') == '#':
            episode['audioUrl'] = ''  # Empty string will disable the button
            print(f"   📻 Disabled audio button for {title}")
        elif episode.get('audioUrl'):
            print(f"   ✅ Audio link OK for {title}")
        
        # Fix text URLs - remove local file paths
        if episode.get('textUrl', '').startswith('C:') or episode.get('textUrl', '').startswith('probate_cases'):
            episode['textUrl'] = ''  # Empty string will disable the button
            print(f"   📄 Disabled text button for {title} (local path)")
        elif episode.get('textUrl') and episode.get('textUrl') != '#':
            print(f"   ✅ Text link OK for {title}")
        elif episode.get('textUrl') == '#':
            episode['textUrl'] = ''
            print(f"   📄 Disabled text button for {title} (placeholder)")
    
    # Create new JavaScript with fixed links
    fixed_episodes_json = json.dumps(episodes, indent=12)
    
    # Replace the episodes array in the HTML
    new_content = re.sub(
        r'const episodes = \[.*?\];',
        f'const episodes = {fixed_episodes_json};',
        content,
        flags=re.DOTALL
    )
    
    # Also fix the button rendering to handle empty URLs
    button_fix = '''                        ${episode.audioUrl ? `<a href="${episode.audioUrl}" class="btn btn-primary" target="_blank">
                            🎧 Listen Now
                        </a>` : `<button class="btn btn-primary" disabled style="opacity: 0.5; cursor: not-allowed;">
                            🎧 Audio Coming Soon
                        </button>`}
                        ${episode.textUrl ? `<a href="${episode.textUrl}" class="btn btn-secondary">
                            📄 Read Text
                        </a>` : `<button class="btn btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed;">
                            📄 Text Coming Soon
                        </button>`}'''
    
    # Find the current button HTML and replace it
    new_content = re.sub(
        r'<a href="\$\{episode\.audioUrl\}".*?</a>\s*<a href="\$\{episode\.textUrl\}".*?</a>',
        button_fix,
        new_content,
        flags=re.DOTALL
    )
    
    # Write the fixed content back
    with open(website_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n✅ Website links fixed!")
    print("\n📊 Summary:")
    
    # Count working vs disabled links
    audio_working = sum(1 for ep in episodes if ep.get('audioUrl') and ep['audioUrl'] != '#' and ep['audioUrl'] != '')
    audio_disabled = len(episodes) - audio_working
    text_working = sum(1 for ep in episodes if ep.get('textUrl') and ep['textUrl'] != '#' and ep['textUrl'] != '')
    text_disabled = len(episodes) - text_working
    
    print(f"   🎧 Audio links: {audio_working} working, {audio_disabled} disabled")
    print(f"   📄 Text links: {text_working} working, {text_disabled} disabled")
    print(f"   📈 Total episodes: {len(episodes)}")
    
    print("\n🚀 Ready to deploy! Run deploy_website_to_github_FIXED.bat")

if __name__ == "__main__":
    fix_website_links()
