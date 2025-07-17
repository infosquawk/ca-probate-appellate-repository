#!/usr/bin/env python3
"""
Quick test to verify brief link conversion is working
"""

import json
from pathlib import Path

# Test the conversion logic
def convert_to_web_path(file_path: str, case_number: str = "") -> str:
    """Convert file system paths to web-accessible relative paths"""
    if not file_path or file_path == '#':
        return '#'
        
    file_path_lower = file_path.lower()
    website_texts_dir = Path("texts")
    
    # Case brief files - convert to texts/ directory
    if 'case_brief' in file_path_lower or '_brief' in file_path_lower:
        filename = Path(file_path).name
        
        # First try: exact filename match in website/texts/
        exact_match_path = website_texts_dir / filename
        if exact_match_path.exists():
            return f"texts/{filename}"
        
        # Second try: find by case number in filename
        if case_number and website_texts_dir.exists():
            for txt_file in website_texts_dir.glob("*.txt"):
                # Match files that start with the case number and contain "Case_Brief"
                if (txt_file.name.upper().startswith(case_number.upper()) and 
                    'case_brief' in txt_file.name.lower()):
                    return f"texts/{txt_file.name}"
        
        # Third try: broader filename matching
        if website_texts_dir.exists():
            for txt_file in website_texts_dir.glob("*.txt"):
                if filename.lower() == txt_file.name.lower():
                    return f"texts/{txt_file.name}"
        
        return '#'
    
    return '#'

# Test with sample paths from processed_briefs.json
test_cases = [
    {
        "case_number": "B333052",
        "file_path": "probate_cases\\pdfs\\published_text\\2025-07_Case_Briefs_(Published)\\B333052_(Case_Brief)_Conservatorship_of_ANNE_S_(published).txt",
        "expected": "texts/B333052_(Case_Brief)_Conservatorship_of_ANNE_S_(published).txt"
    },
    {
        "case_number": "G063155", 
        "file_path": "probate_cases\\pdfs\\published_text\\2025-07_Case_Briefs_(Published)\\G063155_(Case_Brief)_Estate_of_LAYLA_BOYAJIAN_(published).txt",
        "expected": "texts/G063155_(Case_Brief)_Estate_of_LAYLA_BOYAJIAN_(published).txt"
    },
    {
        "case_number": "B330596",
        "file_path": "probate_cases\\pdfs\\unpublished_text\\2025-07_Case_Briefs_(Unpublished)\\B330596_(Case_Brief)_Nelson_v_Huhn_(unpublished).txt",
        "expected": "texts/B330596_(Case_Brief)_Nelson_v_Huhn_(unpublished).txt"
    }
]

print("Testing brief link conversion...")
print("=" * 50)

for i, test in enumerate(test_cases, 1):
    case_number = test["case_number"]
    file_path = test["file_path"]
    expected = test["expected"]
    
    result = convert_to_web_path(file_path, case_number)
    
    print(f"Test {i}: Case {case_number}")
    print(f"  Input path: {file_path}")
    print(f"  Expected:   {expected}")
    print(f"  Result:     {result}")
    print(f"  Status:     {'✅ PASS' if result == expected else '❌ FAIL'}")
    print()

print("Test completed!")
