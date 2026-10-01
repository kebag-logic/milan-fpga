#!/usr/bin/env python3
"""Check the published round 2 read record against the record the page cites.

usage: published_record_check.py <b5-r1 dir of the evidence branch>

<b5-r1> is review-evidence/b5-r1 as archived (it holds author/, author-r2/ and
MANIFEST.json). Prints: the published record's SHA-256 against the page's cited
value and the archive manifest's entry; the sum of its gaps against its own
metadata; every run of three or more 0x23 bytes; the author's figures step run
unmodified (expected to refuse) and run with its hash pin moved to the published
bytes, diffed against the published attribution receipt.
"""
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

CITED = "2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961"   # page :403-404
b5 = Path(sys.argv[1])
r2 = b5 / "author-r2"
rec = r2 / "receipts/a-long-reads.u16"
data = rec.read_bytes()
pub = hashlib.sha256(data).hexdigest()
meta = json.load(open(r2 / "receipts/a-long-reads.json"))
print(f"published record: {len(data)} B sha256 {pub}")
print(f"page cites:       {CITED}; equal: {pub == CITED}")
print(f"record json pins: {meta['record']['sha256']}; equal: {pub == meta['record']['sha256']}")
for e in json.load(open(b5 / "MANIFEST.json")):
    if e["file"] == "author-r2/receipts/a-long-reads.u16":
        print(f"archive manifest: {json.dumps(e)}")
gaps = np.frombuffer(data, dtype="<u2").astype(np.int64)
print(f"sum of gaps {gaps.sum()} us; json elapsed_us_record {meta['elapsed_us_record']}; "
      f"difference {gaps.sum() - meta['elapsed_us_record']} us")
i = 0
while i < len(data):
    if data[i] == 0x23:
        j = i
        while j < len(data) and data[j] == 0x23:
            j += 1
        if j - i >= 3:
            print(f"run of {j - i} bytes 0x23 at byte offsets {i}..{j - 1} (read intervals {i // 2}..{(j - 1) // 2})")
        i = j
    else:
        i += 1
tool = r2 / "tools/b5_attrib.py"
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    shutil.copy(rec, td / "a-long-reads.u16")
    shutil.copy(r2 / "receipts/a-long-reads.json", td / "a-long-reads.json")
    p = subprocess.run([sys.executable, str(tool), "figures", str(b5 / "author"), str(td)],
                       capture_output=True, text=True)
    print(f"author figures, unmodified inputs: rc={p.returncode}; "
          f"last stderr line: {(p.stderr.strip().splitlines() or [''])[-1]}")
    m = dict(meta)
    m["record"] = dict(meta["record"], sha256=pub)
    json.dump(m, open(td / "a-long-reads.json", "w"), indent=1)
    p = subprocess.run([sys.executable, str(tool), "figures", str(b5 / "author"), str(td)],
                       capture_output=True, text=True)
    print(f"author figures, hash pin moved to the published bytes: rc={p.returncode}")
    old = (r2 / "receipts/attribution.txt").read_text().splitlines()
    new = p.stdout.splitlines()
    d = list(difflib.unified_diff(old, new, "published attribution.txt", "figures on published record", n=0, lineterm=""))
    print(f"diff against the published receipt: {sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---'))} changed lines")
    print("\n".join(d))
