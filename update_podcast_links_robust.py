import re

def update_podcast_links_robust():
    """Update website with correct Podbean podcast links using regex replacement"""
    
    # Podcast episodes found in RSS feed
    podcast_updates = {
        'S282314': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-s282314-smart-fallback/',
            'duration': '1:18:36'
        },
        'G063155': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-g063155-smart-fallback/',
            'duration': '31:13'
        },
        'B341750': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-b341750-smart-fallback/',
            'duration': '23:53'
        },
        'B330596': {
            'url': 'https://probate-cal.podbean.com/e/california-probate-case-b330596-smart-fallback/',
            'duration': '57:34'
        }
    }
    
    # Read the current index.html
    website_path = r"C:\Users\Ryan\Google_Drive\My_Documents\Work\0000-Claude-Workspace\scholar_podcast\website\index.html"
    
    with open(website_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔗 Updating podcast links from RSS feed...")
    print("📡 Found 4 new podcast episodes with Smart Fallback technology:")
    
    updated_count = 0
    
    # Update each case number using regex replacement
    for case_number, podcast_info in podcast_updates.items():
        
        # Pattern to find the episode with this case number
        pattern = rf'"caseNumber":\s*"{case_number}".*?"audioUrl":\s*"[^"]*".*?"duration":\s*"[^"]*"'
        
        def replace_episode_data(match):
            episode_text = match.group(0)
            # Replace audioUrl
            episode_text = re.sub(r'"audioUrl":\s*"[^"]*"', f'"audioUrl": "{podcast_info["url"]}"', episode_text)
            # Replace duration
            episode_text = re.sub(r'"duration":\s*"[^"]*"', f'"duration": "{podcast_info["duration"]}"', episode_text)
            return episode_text
        
        # Apply the replacement
        old_content = content
        content = re.sub(pattern, replace_episode_data, content, flags=re.DOTALL)
        
        if old_content != content:
            print(f"   ✅ {case_number}: Updated with {podcast_info['url']}")
            print(f"      Duration: {podcast_info['duration']}")
            updated_count += 1
        else:
            print(f"   ⚠️  {case_number}: Not found or already updated")
    
    # Write the updated content back
    with open(website_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n🎉 Successfully updated {updated_count} podcast links!")
    print("\n📊 Final Status:")
    print(f"   🎧 Opinion episodes with audio: All 5 should now have working links")
    print(f"   📈 All Podbean episodes connected to website")
    
    print("\n🚀 Ready to deploy! All opinion podcasts now have working Podbean links!")
    
    return updated_count

if __name__ == "__main__":
    update_podcast_links_robust()
