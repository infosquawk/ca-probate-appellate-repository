import re

# Read the HTML file
with open('C:/Users/Ryan/Google_Drive/My_Documents/Work/0000-Claude-Workspace/scholar_podcast/website/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original content length:", len(content))

# Fix the specific problematic descriptions
fixes = [
    # Fix 1: Estate of Eden Ahbez
    ('"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn this California Appellate Court case, the Estate of Eden Ahbez presents a key issue in trust administration and estate planning: whether an individual without a direct familial or pecuniary interest can bring a petition under Section 850 of the California Probate Code. The court ultimately ruled in favor of Debra Guess, finding that she satisfied the requirements of Section 850 and had standing to b...",',
     '"description": "In this California Appellate Court case, the Estate of Eden Ahbez presents a key issue in trust administration and estate planning: whether an individual without a direct familial or pecuniary interest can bring a petition under Section 850 of the California Probate Code. The court ultimately ruled in favor of Debra Guess, finding that she satisfied the requirements of Section 850 and had standing to bring the petition.",'),
    
    # Fix 2: In re Dominic H
    ('"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn this California Appellate Court case, In re Dominic H., the court grapples with the complex issues surrounding parental rights and guardianship. The case centers on whether the trial court erred in denying Bernardino\'s petition for presumed father status under Adoption of Kelsey S., and whether the parties seeking termination of parental rights complied with the Indian Child Welfare Act (ICWA) and r...",',
     '"description": "In this California Appellate Court case, In re Dominic H., the court grapples with the complex issues surrounding parental rights and guardianship. The case centers on whether the trial court erred in denying Bernardino\'s petition for presumed father status under Adoption of Kelsey S., and whether the parties seeking termination of parental rights complied with the Indian Child Welfare Act (ICWA).",'),
    
    # Fix 3: Conservatorship of the Person of C
    ('"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn this California Appellate Court case, the court grappled with the issue of ensuring knowing and voluntary waivers of jury trials in Lanterman-Petris-Short (LPS) Act conservatorship proceedings. The case centered around C.S., a proposed conservatee alleged to be gravely disabled due to mental illness, whose right to a jury trial was at stake. The court ultimately held that the trial court\'s failure t...",',
     '"description": "In this California Appellate Court case, the court grappled with the issue of ensuring knowing and voluntary waivers of jury trials in Lanterman-Petris-Short (LPS) Act conservatorship proceedings. The case centered around C.S., a proposed conservatee alleged to be gravely disabled due to mental illness, whose right to a jury trial was at stake.",'),
    
    # Fix 4: Layla Boyajian
    ('"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn the California Court of Appeal case, Boyajian v. [Unknown], the court addressed two key legal issues: whether a stand-alone revocation document constitutes a subsequent will, and whether undue influence was exercised in the creation of a prior will. The court ultimately held that physical alteration is required to effect a revocation by cancellation, and that the proponent failed to present sufficie...",',
     '"description": "In the California Court of Appeal case, Boyajian v. [Unknown], the court addressed two key legal issues: whether a stand-alone revocation document constitutes a subsequent will, and whether undue influence was exercised in the creation of a prior will. The court ultimately held that physical alteration is required to effect a revocation by cancellation.",'),
    
    # Fix 5: Conservatorship of ANNE S
    ('"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn the Conservatorship of Anne S., the California Court of Appeal addresses the standing requirements for petitioning for conservatorship under Probate Code section 1820. The court holds that Marc B. Hankin, a neighbor of Anne S., lacks standing to bring a petition for conservatorship due to his lack of interest or connection to Anne\'s well-being. This case serves as a reminder to practitioners of the ...",',
     '"description": "In the Conservatorship of Anne S., the California Court of Appeal addresses the standing requirements for petitioning for conservatorship under Probate Code section 1820. The court holds that Marc B. Hankin, a neighbor of Anne S., lacks standing to bring a petition for conservatorship due to his lack of interest or connection to Anne\'s well-being.",'),
    
    # Fix 6: Nelson v. Huhn
    ('"description": "Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn the California Appellate Court case of Huhn v. Nelson, the court addressed whether a settlement term sheet constitutes an agreement to arbitrate and whether an appraisal report can be confirmed as an arbitration award. The court held that the settlement term sheet does not qualify as an arbitration agreement, but rather only provides for a binding valuation. This decision highlights the importance o...",',
     '"description": "In the California Appellate Court case of Huhn v. Nelson, the court addressed whether a settlement term sheet constitutes an agreement to arbitrate and whether an appraisal report can be confirmed as an arbitration award. The court held that the settlement term sheet does not qualify as an arbitration agreement, but rather only provides for a binding valuation.",')
]

# Apply each fix
fixed_count = 0
for old_text, new_text in fixes:
    if old_text in content:
        content = content.replace(old_text, new_text)
        fixed_count += 1
        print(f"✅ Fixed description {fixed_count}")

print(f"\nTotal fixes applied: {fixed_count}")
print("Fixed content length:", len(content))

# Write the fixed content
with open('C:/Users/Ryan/Google_Drive/My_Documents/Work/0000-Claude-Workspace/scholar_podcast/website/index_FIXED.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Created index_FIXED.html")
print("✅ Ready for deployment!")
