from pathlib import Path
import subprocess
import re

ROOT = Path(__file__).resolve().parents[1]
OUTBREAKS_DIR = ROOT / "outbreaks"
OUTPUT_FILE = ROOT / "_recent-updates.md"


def git_output(args):
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def get_title(slug):
    index_file = OUTBREAKS_DIR / slug / "index.qmd"

    if index_file.exists():
        text = index_file.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
        if match:
            return match.group(1)

    return slug.replace("-", " ").title()


updates = []

for csv_file in OUTBREAKS_DIR.glob("*/data/references.csv"):
    slug = csv_file.parts[-3]
    rel_path = csv_file.relative_to(ROOT).as_posix()

    date = git_output(["log", "-1", "--format=%cs", "--", rel_path])

    if date:
        updates.append({
            "date": date,
            "title": get_title(slug),
            "slug": slug
        })


updates = sorted(updates, key=lambda x: x["date"], reverse=True)[:5]


with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    f.write("## Recently updated\n\n")
    f.write("This section is generated automatically from the most recent updates to outbreak evidence datasets.\n\n")

    if not updates:
        f.write("No outbreak datasets have been added yet.\n")
    else:
        f.write("::: {.card-grid}\n\n")

        for update in updates:
            f.write("::: {.info-card}\n")
            f.write(f"### {update['title']}\n\n")
            f.write(f"**Updated:** {update['date']}\n\n")
            f.write(f"[View evidence table](outbreaks/{update['slug']}/)\n")
            f.write(":::\n\n")

        f.write(":::\n")
