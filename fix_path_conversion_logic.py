#!/usr/bin/env python3
"""
URGENT FIX: Path Conversion Logic for Brief Links
Fixes the convert_to_web_path function to properly find existing files
"""

import os
import re
from pathlib import Path

def fix_comprehensive_website_updater():
    """Fix the path conversion logic in comprehensive_website_updater.py"""
    
    website_dir = Path(__file__).parent
    updater_file = website_dir / "comprehensive_website_updater.py"
    
    print(f"🔧 Fixing path conversion logic in {updater_file}")
    
    # Read the current file
    with open(updater_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Enhanced convert_to_web_path function
    new_convert_function = '''    def convert_to_web_path(self, file_path: str, case_number: str = "") -> str:
        """
        Convert file system paths to web-accessible relative paths
        ENHANCED VERSION - Better file matching
        """
        if not file_path or file_path == '#':
            return '#'
            
        # Handle different types of file paths
        file_path_lower = file_path.lower()
        
        # Special edition files - look for matching files in texts/
        if 'special_edition' in file_path_lower or 'californias_heritage' in file_path_lower:
            # Check if the corresponding file exists in website/texts/
            if 'californias_heritage' in file_path_lower:
                web_file = "texts/2025-07-13_Californias_Heritage_of_Estates_analysis.txt"
                web_path = self.website_dir / web_file.replace('texts/', '')
                if web_path.exists():
                    return web_file
            return '#'
        
        # Case brief files - convert to texts/ directory
        if 'case_brief' in file_path_lower or '_brief' in file_path_lower:
            filename = Path(file_path).name
            
            # First try: exact filename match in website/texts/
            exact_match_path = self.website_texts_dir / filename
            if exact_match_path.exists():
                return f"texts/{filename}"
            
            # Second try: find by case number in filename
            if case_number and self.website_texts_dir.exists():
                for txt_file in self.website_texts_dir.glob("*.txt"):
                    # Match files that start with the case number and contain "Case_Brief"
                    if (txt_file.name.upper().startswith(case_number.upper()) and 
                        'case_brief' in txt_file.name.lower()):
                        return f"texts/{txt_file.name}"
            
            # Third try: broader filename matching
            if self.website_texts_dir.exists():
                for txt_file in self.website_texts_dir.glob("*.txt"):
                    if filename.lower() == txt_file.name.lower():
                        return f"texts/{txt_file.name}"
            
            return '#'
        
        # PDF files - convert to pdfs/ directory  
        if file_path_lower.endswith('.pdf'):
            filename = Path(file_path).name
            
            # Check both published and unpublished directories
            pdf_locations = ['pdfs/published/', 'pdfs/unpublished/']
            for location in pdf_locations:
                web_file = f"{location}{filename}"
                if (self.website_dir / web_file).exists():
                    return web_file
            
            return ''  # Empty string for missing PDFs (don't show button)
        
        # Text files from probate_cases - convert to texts/ directory
        if 'probate_cases' in file_path_lower and file_path_lower.endswith('.txt'):
            filename = Path(file_path).name
            
            # Try to find the matching file in website/texts/
            if self.website_texts_dir.exists():
                for txt_file in self.website_texts_dir.glob("*.txt"):
                    # Match by case number or filename
                    if case_number and case_number.upper() in txt_file.name.upper():
                        return f"texts/{txt_file.name}"
                    elif filename.lower() == txt_file.name.lower():
                        return f"texts/{txt_file.name}"
            
            return '#'
        
        # Default fallback
        return '#'
    
    def find_original_text_url(self, case_number: str, case_name: str = "") -> str:
        """
        Find the original court opinion text file for a case
        ENHANCED VERSION - Better pattern matching
        """
        if not self.website_texts_dir.exists():
            return ''
            
        # Look for original court opinion text files (not briefs)
        for txt_file in self.website_texts_dir.glob("*.txt"):
            filename = txt_file.name
            
            # Skip case brief files
            if 'case_brief' in filename.lower() or '_brief' in filename.lower():
                continue
                
            # Match by case number and look for published/unpublished indicators
            if case_number and case_number.upper() in filename.upper():
                # Further filter for original court texts
                if any(keyword in filename.lower() for keyword in ['published', 'unpublished']):
                    # Make sure it's not a brief file
                    if 'brief' not in filename.lower():
                        return f"texts/{filename}"
        
        return \'\'\'
    
    # Replace the existing functions
    function_pattern = r'def convert_to_web_path\(self, file_path: str, case_number: str = ""\) -> str:.*?(?=\n    def |\nclass |\n\ndef |\Z)'
    content = re.sub(function_pattern, new_convert_function.strip(), content, flags=re.DOTALL)
    
    # Write the updated content
    with open(updater_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Path conversion logic updated!")
    print("🔧 Enhanced file matching for existing brief and court opinion files")

def main():
    """Run the fix"""
    print("🚀 Fixing comprehensive website updater path conversion logic...")
    fix_comprehensive_website_updater()
    print("\n✅ Fix completed! Now run the website updater to apply changes.")

if __name__ == "__main__":
    main()
