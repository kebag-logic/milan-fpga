#!/usr/bin/env python3
"""Fact-survival check: every fragment of the old hand-written page must be on
the generated page, or be one of the deliberate, listed changes.
Fragments: each heading, each list item, each table cell, and each sentence
of each paragraph, normalised (whitespace, em dash written as --)."""
import re
import sys
from pathlib import Path

old_lines = Path(sys.argv[1]).read_text().splitlines()
new = Path(sys.argv[2]).read_text()


def norm(t):
    t = t.replace("—", "--").replace("\\|", "|")
    t = re.sub(r"<!--.*?-->", "", t)
    return " ".join(t.split()).strip(" *,;")


newn = norm(re.sub(r"(?m)^\s*(?:#{1,6}|[-*+]|\d+\.|>)\s+", "", new))
frags, para, skip, fence = [], [], False, False


def flush():
    if para:
        text = norm(" ".join(para))
        frags.extend(re.split(r"(?<=[.;:])\s+", text))
        para.clear()


for ln in old_lines:
    s = ln.strip()
    if s.startswith("```"):
        flush()
        fence = not fence
        continue
    if fence:
        frags.append(re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", s))
        continue
    if s.startswith("## "):
        skip = s == "## Contents"
    if skip or "milan-feature-status" in s:
        continue
    if not s:
        flush()
        continue
    if re.match(r"#{1,6}\s", s):
        flush()
        frags.append(re.sub(r"^#{1,6}\s+", "", s))
        continue
    if s.startswith("|"):
        flush()
        frags.extend(c for c in re.split(r"(?<!\\)\|", s.strip("|")))
        continue
    if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", ln):
        flush()
        para.append(re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", ln))
        continue
    para.append(re.sub(r"^>\s?", "", s))
flush()
frags = [piece for f in frags for piece in re.split(r"`\[", f)]
frags = [norm(re.sub(r"^\d+(?::\d+)?\]`\s*", "", f)) for f in frags]
frags = [f for f in frags if len(f) >= 25 and not re.fullmatch(r"[-:| ]+", f)]
missing = [f for f in frags if f not in newn]
print(f"fragments: {len(frags)}; present on the new page: {len(frags) - len(missing)}; missing: {len(missing)}")
for f in missing:
    print("MISSING:", f[:240])
