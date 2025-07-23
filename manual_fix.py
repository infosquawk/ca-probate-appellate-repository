#!/usr/bin/env python3
"""
Manual Website Content Fix
This script manually extracts episode data from JSON files and fixes the website HTML
"""

import json
import re
from pathlib import Path

def load_episode_data():
    """Load and process episode data from JSON files"""
    base_dir = Path("C:/Users/Ryan/Google_Drive/My_Documents/Work/0000-Claude-Workspace/scholar_podcast")
    
    episodes = []
    
    # Load from logs/processed_cases.json
    logs_file = base_dir / "logs" / "processed_cases.json"
    if logs_file.exists():
        with open(logs_file, 'r', encoding='utf-8') as f:
            logs_data = json.load(f)
        
        print(f"Found {len(logs_data)} episodes in logs")
        
        for case_key, case_info in logs_data.items():
            file_info = case_info.get('file_info', {})
            enhanced_info = case_info.get('enhanced_case_info', {})
            
            # Get case name
            case_name_mapping = {
                'S282314': 'In re Discipline',
                'B341750': 'Conservatorship of Julie C',
                'B330596': 'Nelson v Huhn',
                'G063155': 'Estate of LAYLA BOYAJIAN',
                'B333052': 'Conservatorship of ANNE S',
                'C102321': 'Conservatorship of the Person of C',
                'B341350': 'In re Dominic H',
                'D085918': 'Estate of EDEN AHBEZ'
            }
            
            case_name = enhanced_info.get('case_name', case_name_mapping.get(case_key, case_key))
            
            episode = {
                'id': len(episodes) + 1,
                'type': 'opinion',
                'title': f"Case {case_key} - {case_name}",
                'court': 'California Appellate Court',
                'date': enhanced_info.get('date', case_info.get('processed_date', '2025-07-13')[:10]),
                'caseNumber': case_key,
                'description': f"Professional analysis of {case_name}, examining key principles of California probate law. This appellate court decision addresses important legal issues with practical implications for legal practitioners.",
                'audioUrl': '#',
                'textUrl': '#',
                'pdfUrl': '',
                'duration': 'N/A',
                'keywords': ['probate', 'California', 'appellate', case_key.lower()],
                'source': 'podcast'
            }
            
            # Get Podbean URL
            podbean_result = file_info.get('podbean_result', {})
            if podbean_result and podbean_result.get('episode_info', {}).get('episode'):
                episode_info = podbean_result['episode_info']['episode']
                episode['audioUrl'] = episode_info.get('permalink_url', '#')
            
            # Get duration
            audio_result = file_info.get('audio_result', {})
            if audio_result.get('duration_estimate'):
                duration_seconds = audio_result['duration_estimate']
                hours = int(duration_seconds // 3600)
                minutes = int((duration_seconds % 3600) // 60)
                seconds = int(duration_seconds % 60)
                
                if hours > 0:
                    episode['duration'] = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    episode['duration'] = f"{minutes}:{seconds:02d}"
            
            episodes.append(episode)
    
    # Load from probate_cases/processed_briefs.json
    briefs_file = base_dir / "probate_cases" / "processed_briefs.json"
    if briefs_file.exists():
        with open(briefs_file, 'r', encoding='utf-8') as f:
            briefs_data = json.load(f)
        
        print(f"Found {len(briefs_data)} case briefs")
        
        for brief_key, brief_info in briefs_data.items():
            case_number = brief_info.get('case_number', 'Unknown')
            case_name = brief_info.get('case_name', f"Case {case_number}")
            
            # Skip test cases
            if case_number in ['B007052', 'B007596'] or 'TEST' in case_name:
                continue
            
            episode = {
                'id': len(episodes) + 1,
                'type': 'brief',
                'title': f"Brief: {case_name}",
                'court': 'California Appellate Court',
                'date': brief_info.get('processed_date', '2025-07-13')[:10],
                'caseNumber': case_number,
                'description': brief_info.get('description', f"AI-generated case brief analyzing {case_name}. Professional analysis covering key legal principles, procedural requirements, and practical guidance for practitioners."),
                'audioUrl': '#',
                'textUrl': '#',
                'pdfUrl': '',
                'duration': 'N/A',
                'keywords': ['case brief', 'probate', 'California', 'analysis', case_number.lower()],
                'source': 'case_brief'
            }
            
            # Get Podbean URL and duration
            podbean_result = brief_info.get('podbean_result', {})
            if podbean_result and podbean_result.get('episode_info', {}).get('episode'):
                episode_info = podbean_result['episode_info']['episode']
                episode['audioUrl'] = episode_info.get('permalink_url', '#')
                
            if brief_info.get('duration'):
                duration_seconds = brief_info['duration']
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                episode['duration'] = f"{minutes}:{seconds:02d}"
            
            episodes.append(episode)
    
    # Add special edition
    episodes.append({
        'id': len(episodes) + 1,
        'type': 'analysis',
        'title': "Analysis: California's Heritage Of Estates",
        'court': 'Legal Analysis Special Edition',
        'date': '2025-07-13',
        'caseNumber': 'Analysis-14',
        'description': 'Special legal analysis and commentary on California probate law matters. In-depth examination with practical implications for legal practitioners.',
        'audioUrl': 'https://www.podbean.com/ew/pb-thdza-1904721',
        'textUrl': 'texts/2025-07-13_Californias_Heritage_of_Estates_analysis.txt',
        'pdfUrl': '',
        'duration': 'Audio',
        'keywords': ['legal analysis', 'commentary', 'special edition', 'probate law'],
        'source': 'special_edition'
    })
    
    # Sort by date (newest first)
    episodes.sort(key=lambda x: x['date'], reverse=True)
    
    # Reassign IDs
    for i, episode in enumerate(episodes, 1):
        episode['id'] = i
    
    return episodes

def update_html_file(episodes):
    """Update the HTML file with new episode data"""
    html_file = Path("C:/Users/Ryan/Google_Drive/My_Documents/Work/0000-Claude-Workspace/scholar_podcast/website/index.html")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert episodes to JavaScript
    episodes_js = json.dumps(episodes, indent=8)
    
    # Replace the episodes array
    pattern = r'const episodes = \[.*?\];'
    replacement = f'const episodes = {episodes_js};'
    
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Update statistics
    stats = {
        'total': len(episodes),
        'opinions': len([ep for ep in episodes if ep['type'] == 'opinion']),
        'briefs': len([ep for ep in episodes if ep['type'] == 'brief']),
        'analysis': len([ep for ep in episodes if ep['type'] == 'analysis'])
    }
    
    updated_html = re.sub(
        r'<div class="stat-number" id="totalEpisodes">\d+\+?</div>',
        f'<div class="stat-number" id="totalEpisodes">{stats["total"]}+</div>',
        updated_html
    )
    
    # Write updated file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    return stats

def main():
    print("🔧 MANUAL WEBSITE CONTENT FIX")
    print("=" * 50)
    
    # Load episode data
    print("📖 Loading episode data from JSON files...")
    episodes = load_episode_data()
    
    print(f"✅ Loaded {len(episodes)} episodes")
    
    # Show episode summary
    print("\n📊 Episode Summary:")
    opinions = len([ep for ep in episodes if ep['type'] == 'opinion'])
    briefs = len([ep for ep in episodes if ep['type'] == 'brief'])
    analysis = len([ep for ep in episodes if ep['type'] == 'analysis'])
    with_audio = len([ep for ep in episodes if ep['audioUrl'] != '#'])
    
    print(f"   Opinions: {opinions}")
    print(f"   Briefs: {briefs}")
    print(f"   Analysis: {analysis}")
    print(f"   With Audio: {with_audio}")
    
    # Update HTML
    print("\n🔧 Updating HTML file...")
    stats = update_html_file(episodes)
    
    print("✅ HTML file updated successfully!")
    print(f"   Total Episodes: {stats['total']}")
    print(f"   Statistics updated")
    
    print("\n🎉 MANUAL FIX COMPLETED!")
    print("=" * 50)
    print("Now run: python deploy_full_website_to_godaddy.py")
    
    return episodes

if __name__ == "__main__":
    episodes = main()
