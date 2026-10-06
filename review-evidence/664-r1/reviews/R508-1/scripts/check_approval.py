#!/usr/bin/env python3
"""Compare public approval text with both Git revisions; formatting normalization only."""
import html
from pathlib import Path
import re
import subprocess
import sys

root, body_path = map(Path, sys.argv[1:3])
base = "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"
head = "a27808375427859dc357f6bfd0a88842062b20ed"
body = body_path.read_text()


def normalize(s):
    s = s.replace("<br>", "\n")
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return " ".join(html.unescape(s).split())


def source(rev, name):
    return subprocess.check_output(["git", "-C", str(root), "show", f"{rev}:{name}"], text=True)


count = 0
for row in body.splitlines():
    if not re.match(r"\| (?:FR-CTRL-04|NFR-(?:LAT-02|SCUP-0[24]|SCOUT-0[123]|REL-02)) \|", row):
        continue
    key, old, new = row.strip("|").split("|")
    key = key.strip()
    for rev, given in ((base, old), (head, new)):
        actual = next(line for line in source(rev, "docs/reference/FR_NFR.md").splitlines() if line.startswith(f"| {key} |"))
        assert normalize(given) == normalize(actual.strip("|")), (key, rev, "different approval text")
    print("PASS old/new requirement row", key)
    count += 1
assert count == 8, count

row = next(line for line in body.splitlines() if line.startswith("| REQUIREMENTS.md Section 1 |"))
_, old, new = row.strip("|").split("|")
for rev, given in ((base, old), (head, new)):
    section = source(rev, "REQUIREMENTS.md").split("## 1. Product ownership\n", 1)[1].split("## 2. Reference standards", 1)[0]
    assert normalize(given) == normalize(section), (rev, "product ownership approval mismatch")
print("PASS old/new REQUIREMENTS.md section 1 (line wrapping, HTML table escaping and link markup normalized)")

actual = source(head, "docs/reference/FR_NFR.md").split("### 3.4.1 Control service budget and normative timing", 1)[1].split("### 3.5", 1)[0]
given = body.split("### 3.4.1 Control service budget and normative timing", 1)[1].split("The corresponding changed architecture", 1)[0]
assert normalize(actual) == normalize(given), "budget and hook approval mismatch"
print("PASS complete new timing budget and hook sections (same formatting normalization)")
