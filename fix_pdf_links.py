#!/usr/bin/env python3
"""
Fix PDF Links in Website
Updates the index.html file to include correct PDF links for all episodes
"""

import re
import os

def fix_pdf_links():
    """Update PDF links in the website episodes"""
    
    # Define the PDF mappings
    pdf_mappings = {
        # Case number: PDF path
        'B341350': 'pdfs/unpublished/B341350_a_Minor_ISMAEL_H_et_al_v_BERNARDINO_G_unpublished.pdf',
        'C102321': 'pdfs/unpublished/C102321_Conservatorship_of_the_Person_of_C_unpublished.pdf',
        'G063155': 'pdfs/published/G063155_Estate_of_LAYLA_BOYAJIAN_published.pdf',
        'B333052': 'pdfs/published/B333052_Conservatorship_of_ANNE_S_published.pdf',
        'S282314': 'pdfs/published/S282314_In_re_Discipline_published.pdf',
        'B330596': 'pdfs/unpublished/B330596_Nelson_v_Huhn_unpublished.pdf',
        'B341750': 'pdfs/unpublished/B341750_Conservatorship_of_Julie_C_unpublished.pdf'
    }
    
    # Read the current index.html
    html_file = 'index.html'
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = 0
    
    # For each case number, find and update the PDF links
    for case_number, pdf_path in pdf_mappings.items():
        
        # Pattern to find episodes with this case number and empty PDF URL
        # Look for opinion episodes (not briefs) with this case number
        pattern = (
            rf'({{[^}}]*?"type":\s*"opinion"[^}}]*?'
            rf'"caseNumber":\s*"{case_number}"[^}}]*?'
            rf'"pdfUrl":\s*"[^"]*")'
        )
        
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        for match in matches:
            episode_block = match.group(1)
            
            # Check if it already has a non-empty PDF URL
            if f'"pdfUrl": ""' in episode_block or '"pdfUrl":""' in episode_block:
                # Replace empty PDF URL with the correct one
                new_episode_block = re.sub(
                    r'"pdfUrl":\s*"[^"]*"',
                    f'"pdfUrl": "{pdf_path}"',
                    episode_block
                )
                
                content = content.replace(episode_block, new_episode_block)
                changes_made += 1
                print(f"Updated {case_number} with PDF: {pdf_path}")
    
    # Write the updated content back to the file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nTotal changes made: {changes_made}")
    return True

if __name__ == "__main__":
    print("Fixing PDF links in website...")
    if fix_pdf_links():
        print("PDF links updated successfully!")
        exit(0)
    else:
        print("Failed to update PDF links!")
        exit(1)
