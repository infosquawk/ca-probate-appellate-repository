import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import re
from datetime import datetime
import shutil

# === Settings ===
CHUNK_SIZE = 9000
MAX_WORKERS = 4

PROMPT_TEMPLATE = """You are a legal journalist analyzing a California court opinion for a probate law journal article. Focus on identifying and extracting information relevant to a comprehensive legal journal article for California probate practitioners.

IMPORTANT: Use only plain text with no special characters. Do not use asterisks, bullets, dashes, or any formatting symbols. Write in complete sentences and well-structured paragraphs. Use double line breaks between paragraphs for clear separation and readability.

From this portion of the court opinion, identify:
- Factual background and story elements about the parties and disputes
- Procedural history and legal proceedings
- California Probate Code sections mentioned or applied
- Legal issues and disputes presented
- Court's reasoning, analysis, and rulings
- How the court applied or interpreted probate code provisions
- Practical implications for probate practice

[Chunk {index}/{total}]

{text}
"""

FINAL_BRIEF_PROMPT = """You are a legal journalist writing an article for a probate legal journal about a California court opinion. Your article should be written for experienced California probate practitioners and should tell the complete story of this case in an engaging, narrative style.

IMPORTANT: You are provided with multiple chunk summaries below that collectively contain the complete court opinion. You MUST analyze and synthesize information from ALL the chunk summaries provided to create one comprehensive journal article. Use your discretion to include all information necessary to tell the complete story. Do NOT mention chunks, ask for additional information, or limit your analysis to only some of the summaries.

Structure your journal article as follows:

Begin with the story of the facts of the case. Tell the human story behind the legal dispute - who were the parties, what happened, what led to this litigation. Make this engaging and narrative, like the opening of a legal journal article that draws readers in.

Then explain the procedural posture of the case. Describe how this case made its way through the court system, what motions were filed, what the trial court ruled, and how it came before this appellate court.

Next, explain the legal issues in dispute in the case. What were the key legal questions the parties disagreed about? What interpretations of law were at stake?

Finally, explain how the Court ruled and the court's basis for the ruling. What did the court decide and why? What was the court's reasoning and legal analysis?

Throughout your article, focus on the application of the probate code to this case. Describe what probate code sections were involved, how they applied to the facts, and how the court interpreted them. This should be woven throughout your narrative, not treated as a separate section.

CRITICAL FORMATTING INSTRUCTIONS:
- Use NO special characters, asterisks, bullets, dashes, or formatting symbols
- Write in well-structured paragraphs with clear narrative flow
- Use double line breaks between paragraphs for proper separation and readability
- Write in an engaging, journalistic style appropriate for a legal publication
- Use professional legal terminology but maintain readability
- Tell a complete story that flows from facts through procedure to legal analysis to resolution
- Analyze ALL chunk summaries provided below and synthesize them into one complete article
- Do NOT mention chunks or ask for additional information
- Focus heavily on probate code application and interpretation throughout

Summaries:
{summaries}
"""

# === Helpers ===
def chunk_text(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def run_ollama(prompt):
    result = subprocess.run(
        ['ollama', 'run', 'llama3', '--', prompt],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return result.stdout.strip()

def summarize_chunk(index, total, chunk):
    prompt = PROMPT_TEMPLATE.format(index=index+1, total=total, text=chunk)
    return f"Summary of Chunk {index+1}: " + run_ollama(prompt)

def parse_case_filename(filename):
    stem = Path(filename).stem
    case_number = stem.split('_')[0]
    status = "Published" if "_published" in stem.lower() else "Unpublished"
    name_parts = stem.split('_')[1:]
    name_parts = [part for part in name_parts if part.lower() not in ("published", "unpublished")]
    case_name = " ".join(name_parts).strip()
    return case_number, case_name, status

def get_output_brief_filename(case_number, case_name, status):
    safe_name = re.sub(r'[^\w\s-]', '', case_name).strip().replace(' ', '_')
    return f"{case_number}_(Case_Brief)_{safe_name}_({status.lower()}).txt"

def get_output_folder(status, include_case_briefs=True):
    now = datetime.now()
    base = f"{now.year}-{now.month:02d}"
    suffix = f"_Case_Briefs_({status})" if include_case_briefs else f"_({status})"
    folder_name = base + suffix
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

def clean_special_characters(text):
    """Remove asterisks and other problematic special characters for TTS"""
    # Remove asterisks and other formatting characters
    text = re.sub(r'\*+', '', text)  # Remove asterisks
    text = re.sub(r'[•▪▫◦‣⁃]', '', text)  # Remove bullet points
    text = re.sub(r'[─━┄┅┈┉─]', '', text)  # Remove line characters
    text = re.sub(r'[▬▭▮▯▰▱]', '', text)  # Remove block characters
    text = re.sub(r'[\[\]{}]', '', text)  # Remove brackets
    text = re.sub(r'#+', '', text)  # Remove hash marks
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

def clean_brief_text(brief_text):
    """Clean special characters from brief text without adding headers or footers"""
    return clean_special_characters(brief_text)

# === Main Processor ===
def process_file(filepath):
    case_number, case_name, status = parse_case_filename(filepath.name)
    brief_filename = get_output_brief_filename(case_number, case_name, status)
    output_dir = get_output_folder(status, include_case_briefs=True)
    brief_path = output_dir / brief_filename

    if brief_path.exists():
        print(f"✅ Skipping {filepath.name} (brief already exists)")
        with open(brief_path, 'r', encoding='utf-8') as f:
            brief_text = f.read()
        return {
            "filename": filepath.name,
            "case_name": case_name,
            "brief": brief_text,
            "status": status
        }

    print(f"\n📄 Processing {filepath.name}...")

    text = filepath.read_text(encoding='utf-8', errors='ignore')
    chunks = chunk_text(text, CHUNK_SIZE)
    total_chunks = len(chunks)

    chunk_summaries = [""] * total_chunks
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(summarize_chunk, idx, total_chunks, chunk): idx
            for idx, chunk in enumerate(chunks)
        }

        completed = 0
        for future in as_completed(futures):
            idx = futures[future]
            chunk_summaries[idx] = future.result()
            completed += 1
            print(f"  → Completed chunk {completed}/{total_chunks}")

    summary_path = filepath.with_name(f"{filepath.stem}_chunksummary.txt")
    summary_path.write_text("\n\n".join(chunk_summaries), encoding='utf-8')
    print(f"  💾 Wrote chunk summaries to {summary_path.name}")

    print("  → Generating final brief...")
    final_prompt = FINAL_BRIEF_PROMPT.format(summaries="\n\n".join(chunk_summaries))
    raw_brief = run_ollama(final_prompt)
    clean_brief = clean_brief_text(raw_brief)

    brief_path.write_text(clean_brief, encoding='utf-8')
    print(f"  ✅ Wrote final brief to {brief_path}")

    try:
        summary_path.unlink()
        print(f"  🧹 Deleted {summary_path.name}")
    except Exception as e:
        print(f"  ⚠️ Could not delete {summary_path.name}: {e}")

    archive_dir = get_output_folder(status, include_case_briefs=False)
    archive_path = archive_dir / filepath.name
    try:
        shutil.move(str(filepath), str(archive_path))
        print(f"  📦 Moved original file to {archive_path}")
    except Exception as e:
        print(f"  ⚠️ Could not move original file: {e}")

    return {
        "filename": filepath.name,
        "case_name": case_name,
        "brief": clean_brief,
        "status": status
    }

# === Main Execution ===
if __name__ == "__main__":
    txt_files = list(Path('.').glob('*.txt'))
    if not txt_files:
        print("❌ No .txt files found in this directory.")
        exit()

    summaries_by_status = {"Published": [], "Unpublished": []}

    for file in txt_files:
        result = process_file(file)
        if result:
            summaries_by_status[result["status"]].append(result)

    for status, records in summaries_by_status.items():
        if not records:
            continue
        output_dir = get_output_folder(status, include_case_briefs=True)
        csv_path = output_dir / "0000-Brief_Summaries.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['filename', 'case_name', 'brief']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in records:
                writer.writerow({
                    'filename': row['filename'],
                    'case_name': row['case_name'],
                    'brief': row['brief']
                })
        print(f"\n📊 Saved 0000-Brief_Summaries.csv to {csv_path}")
