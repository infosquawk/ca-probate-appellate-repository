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

PROMPT_TEMPLATE = """You are a legal assistant. Please summarize the following part of a court opinion. Focus on any facts, procedural history, legal issues, and reasoning presented in this segment.

[Chunk {index}/{total}]

{text}
"""

FINAL_BRIEF_PROMPT = """Using the following chunk summaries of a court opinion, generate a legal case brief. Include:
1. Case name
2. Court and date
3. Procedural posture
4. Facts
5. Legal issue(s)
6. Holding
7. Reasoning

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
    return f"[Summary of Chunk {index+1}]\n" + run_ollama(prompt)

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

def add_header_footer(brief_text):
    # Try to extract case name and court from the brief text
    lines = brief_text.strip().splitlines()
    case = "Unknown Case"
    court = "Unknown Court"
    issued_by = "Unknown Judge(s)"

    for line in lines[:10]:  # search top 10 lines
        if "case name" in line.lower():
            case = line.split(":", 1)[-1].strip()
        elif "court" in line.lower():
            court = line.split(":", 1)[-1].strip()
        elif "issued by" in line.lower():
            issued_by = line.split(":", 1)[-1].strip()

    header = f"This case brief is an automatically generated brief of the Court's opinion in the case of {case}, issued by {issued_by} of the {court}.\n"
    footer = "\nEnd of Brief"
    return f"{header}\n{brief_text.strip()}{footer}"

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

    # Save chunk summaries temporarily
    summary_path = filepath.with_name(f"{filepath.stem}_chunksummary.txt")
    summary_path.write_text("\n\n".join(chunk_summaries), encoding='utf-8')
    print(f"  💾 Wrote chunk summaries to {summary_path.name}")

    # Final brief
    print("  → Generating final brief...")
    final_prompt = FINAL_BRIEF_PROMPT.format(summaries="\n\n".join(chunk_summaries))
    raw_brief = run_ollama(final_prompt)
    full_brief = add_header_footer(raw_brief)

    # Save final brief
    brief_path.write_text(full_brief, encoding='utf-8')
    print(f"  ✅ Wrote final brief to {brief_path}")

    # Delete chunk summary file
    try:
        summary_path.unlink()
        print(f"  🧹 Deleted {summary_path.name}")
    except Exception as e:
        print(f"  ⚠️ Could not delete {summary_path.name}: {e}")

    # Move original .txt file to archive
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
        "brief": full_brief,
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
        csv_path = output_dir / "brief_summaries.csv"
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
        print(f"\n📊 Saved brief_summaries.csv to {csv_path}")
