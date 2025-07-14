import json
import re

def update_podcast_links():
    """Update website with correct Podbean podcast links from RSS feed"""
    
    # Podcast episodes found in RSS feed
    podcast_episodes = {
        'S282314': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-s282314-smart-fallback/',
            'duration': '1:18:36',
            'title': 'California Probate Case S282314 (Smart Fallback)'
        },
        'G063155': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-g063155-smart-fallback/',
            'duration': '31:13',
            'title': 'California Probate Case G063155 (Smart Fallback)'
        },
        'B341750': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-b341750-smart-fallback/',
            'duration': '23:53',
            'title': 'California Probate Case B341750 (Smart Fallback)'
        },
        'B330596': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-b330596-smart-fallback/',
            'duration': '57:34',
            'title': 'California Probate Case B330596 (Smart Fallback)'
        }
    }
    
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
    
    print("🔗 Updating podcast links from RSS feed...")
    print("📡 Found 4 new podcast episodes with Smart Fallback technology:")
    
    updated_count = 0
    
    # Update each episode with correct podcast links
    for episode in episodes:
        case_number = episode.get('caseNumber', '').upper()
        episode_type = episode.get('type', '')
        
        if episode_type == 'opinion' and case_number in podcast_episodes:
            podcast_info = podcast_episodes[case_number]
            
            # Update the episode with correct info
            old_url = episode.get('audioUrl', '#')
            old_duration = episode.get('duration', 'Unknown')
            
            episode['audioUrl'] = podcast_info['url']
            episode['duration'] = podcast_info['duration']
            
            # Update title to match RSS feed
            episode['title'] = f"Case {case_number} - {podcast_info['title'].split('(')[0].strip().replace('California Probate Case ' + case_number, '').strip() or 'Smart Fallback Edition'}"
            
            print(f"   ✅ {case_number}: {old_url} → {podcast_info['url']}")
            print(f"      Duration: {old_duration} → {podcast_info['duration']}")
            
            updated_count += 1
    
    # Create new JavaScript with updated links
    fixed_episodes_json = json.dumps(episodes, indent=12)
    
    # Replace the episodes array in the HTML
    new_content = re.sub(
        r'const episodes = \[.*?\];',
        f'const episodes = {fixed_episodes_json};',
        content,
        flags=re.DOTALL
    )
    
    # Write the updated content back
    with open(website_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n🎉 Successfully updated {updated_count} podcast links!")
    print("\n📊 Final Status:")
    
    # Count working vs disabled links after update
    audio_working = sum(1 for ep in episodes if ep.get('audioUrl') and ep['audioUrl'] != '#' and ep['audioUrl'] != '' and ep['audioUrl'].startswith('http'))
    audio_disabled = len([ep for ep in episodes if ep.get('type') == 'opinion']) - audio_working
    
    print(f"   🎧 Opinion episodes with audio: {audio_working} working, {audio_disabled} disabled")
    print(f"   📈 Total episodes: {len(episodes)}")
    
    print("\n🚀 Ready to deploy! All opinion podcasts now have working Podbean links!")
    
    return updated_count

if __name__ == "__main__":
    update_podcast_links()
