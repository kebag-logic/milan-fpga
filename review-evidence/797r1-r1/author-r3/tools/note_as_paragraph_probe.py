#!/usr/bin/env python3
"""Render the page's one-column Note rows as paragraphs and run the repository's own
doc-style analyzer on the result. Usage: note_as_paragraph_probe.py <repo-root>"""
import re, sys
from pathlib import Path
sys.dont_write_bytecode = True
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import check_doc_style as c
page = (root / "docs/reference/REGISTER_MAP.md").read_text(encoding="utf-8")
print("analyzer findings on the page as committed:", len(c.analyze(page)))
out, lines, i = [], page.splitlines(), 0
while i < len(lines):
    if lines[i].strip() == "| Note |":
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            out += [lines[i].strip().strip("|").strip(), ""]
            i += 1
        continue
    out.append(lines[i]); i += 1
f = c.analyze("\n".join(out) + "\n")
para = [x for x in f if x.reason.startswith("paragraph has")]
sent = [x for x in f if x.reason.startswith("sentence has")]
print("analyzer findings with Note rows as paragraphs:", len(f), "paragraph-limit", len(para), "sentence-limit", len(sent))
print("max paragraph:", max([int(m.group(1)) for m in (re.search(r"has (\d+) words", x.reason) for x in para) if m], default=0))
others = 0
for d in c.DOCUMENTS:
    if d.is_file() and d.name != "REGISTER_MAP.md":
        others += sum(1 for l in d.read_text(encoding="utf-8").splitlines() if l.strip() == "| Note |")
print("'| Note |' tables in the other gated documents:", others)
print("'| Note |' tables on this page:", sum(1 for l in lines if l.strip() == "| Note |"))
