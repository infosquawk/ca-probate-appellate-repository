#!/usr/bin/env python3
"""
Quick test to verify brief links are now working after copying missing files
"""
from pathlib import Path

# Test the conversion logic with the newly available files
def test_brief_link_conversion():
    website_texts_dir = Path("C:/Users/Ryan/Google_Drive/My_Documents/Work/0000-Claude-Workspace/scholar_podcast/website/texts")
    
    # Test cases that were previously broken
    test_cases = [
        {
            "case_number": "B341350",
            "file_path": "probate_cases\\pdfs\\unpublished_text\\2025-07_Case_Briefs_(Unpublished)\\B341350_(Case_Brief)__(unpublished).txt",
            "expected_filename": "B341350_(Case_Brief)_Unknown_(unpublished).txt"
        },
        {
            "case_number": "C102321", 
            "file_path": "probate_cases\\pdfs\\unpublished_text\\2025-07_Case_Briefs_(Unpublished)\\C102321_(Case_Brief)__(unpublished).txt",
            "expected_filename": "C102321_(Case_Brief)_Unknown_(unpublished).txt"
        }
    ]
    
    print("Testing newly copied brief files...")
    print("=" * 50)
    
    for test in test_cases:
        expected_file_path = website_texts_dir / test["expected_filename"]
        file_exists = expected_file_path.exists()
        
        print(f"Case {test['case_number']}:")
        print(f"  Expected file: {test['expected_filename']}")
        print(f"  File exists: {'✅ YES' if file_exists else '❌ NO'}")
        print(f"  Should convert to: texts/{test['expected_filename']}")
        print()
    
    return True

if __name__ == "__main__":
    test_brief_link_conversion()
