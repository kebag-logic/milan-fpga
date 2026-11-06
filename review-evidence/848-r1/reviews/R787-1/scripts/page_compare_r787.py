#!/usr/bin/env python3
"""Compare the base and head audit pages cell by cell, and every Findings row with --findings-dir output.

Usage: page_compare_r787.py BASE_PAGE HEAD_PAGE FINDINGS_DIR REPO RECEIPT
"""
import re, sys
from pathlib import Path

def cells(row):
    return [p.strip() for p in re.split(r"(?<!\\)\|", row)[1:-1]]

def sections(page):
    out, section = {}, ""
    for row in page.split("\n"):
        if row.startswith("## "):
            section = row[3:].strip()
        elif row.startswith("| ") and not set(row) <= set("|-: "):
            out.setdefault(section, []).append(cells(row))
    return out

base_text, head_text = Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text()
lanes, repo, receipt = Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
base, head = sections(base_text), sections(head_text)
log = [f"page lines base {base_text.count(chr(10))} head {head_text.count(chr(10))}"]

# Summary: pages by status kept, Lines column gone.
status_base = [r[:2] for r in base["Summary"] if r[0] in ("current", "stale", "superseded", "obsolete", "**total**")]
status_head = [r[:2] for r in head["Summary"] if r[0] in ("current", "stale", "superseded", "obsolete", "**total**")]
log.append(f"summary pages-by-status equal: {status_base == status_head} {status_head}")
lanes_base = [r for r in base["Summary"] if len(r) == 7]
lanes_head = [r for r in head["Summary"] if len(r) == 7]
log.append(f"lane table equal: {lanes_base == lanes_head} ({len(lanes_head)} rows incl header)")
log.append(f"head summary has a Lines header: {any('Lines' in c for r in head['Summary'] for c in r)}")

# Inventory: identical but for the removed count; banner evidence changes wording only.
ib = [r for r in base["Inventory"] if r[0] != "Page"]
ih = [r for r in head["Inventory"] if r[0] != "Page"]
log.append(f"inventory rows base {len(ib)} head {len(ih)}; head cell counts {sorted({len(r) for r in ih})}")
diffs = []
for b, h in zip(ib, ih):
    stripped = b[:1] + b[2:]
    if stripped != h:
        diffs.append((stripped[0], [(x, y) for x, y in zip(stripped, h) if x != y]))
log.append(f"inventory rows differing beyond the Lines cell: {len(diffs)}")
log += [f"  {page}: {change}" for page, change in diffs]

# Findings: identical but the third cell.
fb = [r for r in base["Findings"] if r[0] != "ID"]
fh = [r for r in head["Findings"] if r[0] != "ID"]
same = [b[:2] + b[3:] for b in fb] == [h[:2] + h[3:] for h in fh]
log.append(f"findings rows base {len(fb)} head {len(fh)}; equal but the third cell: {same}")
log.append(f"head Located values: {sorted({r[2] for r in fh})}")
log.append(f"base third cells that are not numbers: {sorted({r[2] for r in fb if not r[2].isdigit()})}")

# Any digit run on the head page that a page length moves? Evidence cells must carry none.
log.append(f"head evidence cells naming a line: {[r[5] for r in ih if re.search(r'line', r[5], re.I)]}")
log.append(f"head statement of `line N` in the Contradicted-by cells (recorded source citations): "
           f"{sum(bool(re.search(r'\bline[s]? \d', r[4])) for r in fh)} of {len(fh)} rows")

# Traceability: every Findings row maps to exactly one lane entry whose line really starts the statement.
entries = {}
for path in sorted(lanes.glob("*.md")):
    text = path.read_text()
    for m in re.finditer(r"^## (\S+): (.+):(\d+|\?)\n\n- Statement: (.*)\n- Contradicted by: (.*)\n- Correction: (.*)\n",
                         text, re.M):
        entries.setdefault((m.group(1), m.group(2)), []).append((path.name, m.group(3), m.group(4), m.group(6)))
log.append(f"lane files: {len(list(lanes.glob('*.md')))}; lane entries {sum(map(len, entries.values()))}")
missing, unknown, wrong, checked = [], [], [], 0
def plain(s):
    s = re.sub(r"!?\[([^\]]*)\](?:\([^)\n]*\)|\[[^\]\n]*\])", r"\1", s)
    s = re.sub(r"^\s*(?:>\s*)*(?:[-*+]\s+|\d+\.\s+)?", "", s)
    return " ".join(re.sub(r"[`*_]", "", s).split()).casefold()
for row in fh:
    page = re.match(r"\[(.+?)(?: \(historical\))?\]", row[1]).group(1)
    got = entries.get((row[0], page))
    if not got or len(got) != 1:
        missing.append((row[0], page, got)); continue
    lane, line, statement, _ = got[0]
    if line == "?":
        unknown.append((row[0], page)); continue
    lines = (repo / page).read_text(errors="replace").split("\n")
    window = plain(" ".join(plain(x) for x in lines[int(line) - 1:int(line) + 8]))
    probe = plain(statement).rstrip(".,;:")
    head_words = " ".join(probe.split()[:4])
    if head_words not in window:
        wrong.append((row[0], page, line, statement[:60]))
    checked += 1
log.append(f"traceability: rows {len(fh)}, resolved to a line {checked}, missing {len(missing)}, unknown {len(unknown)}, wrong line {len(wrong)}")
log += [f"  missing {m}" for m in missing] + [f"  wrong {w}" for w in wrong]
extra = set(entries) - {(r[0], re.match(r"\[(.+?)(?: \(historical\))?\]", r[1]).group(1)) for r in fh}
log.append(f"lane entries with no Findings row: {sorted(extra)}")
receipt.write_text("\n".join(log) + "\n")
print("\n".join(log))
