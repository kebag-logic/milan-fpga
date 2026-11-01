#!/usr/bin/env python3
"""Search current pages for the recorded forms without using the checker's own matcher.

usage: python3 -I ten_forms_grep.py <check_docs.py> <repo>
Reads the unit-bearing rows of the constants table with the checker's row patterns only.
"""
import importlib.util, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("check_docs", sys.argv[1])
m = importlib.util.module_from_spec(spec)
root = Path(sys.argv[2])
sys.path.insert(0, str(root))
spec.loader.exec_module(m)
gen = m.load_generator() if hasattr(m, "load_generator") else None
constants = (root / m.CONSTANTS_PAGE).read_text()
rows = []
for line in m.section_lines(constants, m.CONSTANTS_HEADING):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    match = m.CONSTANT_ROW_RE.match(line.strip())
    unit = m.UNIT_CELL_RE.search(cells[2]) if match and len(cells) > 2 else None
    if unit:
        rows.append((match.group(1), int(cells[1].replace(",", "")), unit.group(1)))
print("unit rows", rows)
pages = [p for p in sorted(root.rglob("*.md")) if ".git" not in p.parts and "history" not in p.parts]
print("current pages scanned", len(pages))
words = {"ms": "milli?seconds?|msecs?", "ns": "nano?seconds?|nsecs?", "us": "micro?seconds?|usecs?", "s": "seconds?|secs?", "ppm": "parts per million", "min": "minutes?"}
hits = 0
for name, value, unit in rows:
    v = re.escape(str(value)); vc = re.escape(f"{value:,}")
    num = f"(?:{v}|{vc})"
    forms = {
      "spelled unit": rf"(?<![\d.,]){num}[\s-]*(?:{words.get(unit, unit)})\b",
      "link on value": rf"\[{num}\]\([^)]*\)[\s-]*{unit}\b",
      "HTML tag on value": rf"<[^>]+>{num}</[^>]+>[\s-]*{unit}\b",
      "entity space": rf"(?<![\d.,]){num}&(?:nbsp|#160|#xA0|ensp|thinsp);{unit}\b",
      "strikethrough": rf"~~{num}~~[\s-]*{unit}\b",
    }
    if unit == "ms":
        dec = f"{value/1000:g}"
        if "." in dec:
            forms["decimal seconds"] = rf"(?<![\d.,]){re.escape(dec)}[\s-]*s(?:ec(?:ond)?s?)?\b"
    if unit == "ns":
        dec = f"{value/1000:g}"
        if "." in dec:
            forms["decimal us"] = rf"(?<![\d.,]){re.escape(dec)}[\s-]*(?:us|µs|μs)\b"
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for label, pat in forms.items():
            for found in re.finditer(pat, text, re.I):
                hits += 1
                print(f"HIT {label} {name} {page.relative_to(root)}: {found.group(0)!r}")
        lines = text.split("\n")
        for i in range(len(lines) - 1):
            if re.search(rf"(?<![\d.,]){num}\s*$", lines[i]) and re.match(rf"\s*{unit}\b", lines[i + 1]):
                hits += 1
                print(f"HIT wrapped {name} {page.relative_to(root)}:{i+1}")
home = constants.split("\n")
indented = [i + 1 for i, l in enumerate(home) if re.match(r" {1,3}#{1,6} ", l)]
print("indented headings on the constants page", indented)
all_hits = [p for p in pages if re.search(r"^ {1,3}#{1,6} ", p.read_text(encoding="utf-8"), re.M)]
print("pages with an indented heading", [str(p.relative_to(root)) for p in all_hits])
print("total hits", hits)
