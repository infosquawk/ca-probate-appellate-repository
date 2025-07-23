# Save this as fix_js_errors.py in your website directory
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all the problematic descriptions by removing line breaks
fixes = [
    ('Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn this California Appellate Court case, the Estate of Eden Ahbez presents', 'In this California Appellate Court case, the Estate of Eden Ahbez presents'),
    ('Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn this California Appellate Court case, In re Dominic H.,', 'In this California Appellate Court case, In re Dominic H.,'),
    ('Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn this California Appellate Court case, the court grappled', 'In this California Appellate Court case, the court grappled'),
    ('Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn the California Court of Appeal case', 'In the California Court of Appeal case'),
    ('Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn the Conservatorship of Anne S.,', 'In the Conservatorship of Anne S.,'),
    ('Here is a professional 2-3 sentence description suitable for podcast and website listings:\n\nIn the California Appellate Court case of Huhn v. Nelson', 'In the California Appellate Court case of Huhn v. Nelson')
]

for old, new in fixes:
    content = content.replace(old, new)

with open('index_FIXED.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed file created: index_FIXED.html")