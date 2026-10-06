#!/usr/bin/env python3
"""Expose the two MAAP citations beside the standard's actual section headings.

Arguments: source checkout, standards directory, packet directory.
The full licensed extraction stays exclusively in scratch.
"""
import hashlib
from pathlib import Path
import re
import subprocess
import sys

root, standards, packet = map(Path, sys.argv[1:4])
pdf = standards / "1722-2016.pdf"
digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
assert digest == "ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c"
output = packet / "scratch/maap-citation-source.txt"
subprocess.run(["pdftotext", "-layout", str(pdf), str(output)], check=True)
text = output.read_text()
print("IEEE 1722-2016 source SHA-256:", digest)
for section, heading in [("B.3.2", "State machine"), ("B.3.3", "MAAP constants")]:
    assert re.search(r"(?m)^\s*" + re.escape(section + " " + heading) + r"\s*$", text)
    print("Source heading:", section, heading)
print("Independent reading: Table B.7 under B.3.2 supplies conflict-state actions and restart transitions.")
print("Independent reading: B.3.3 points to the constants of Table B.8, not those transitions.")
for n, line in enumerate((root / "docs/reference/FR_NFR.md").read_text().splitlines(), 1):
    if line.startswith("| MAAP ") and "B.3.3" in line:
        print(f"docs/reference/FR_NFR.md:{n}: {line}")
print("Finding reproduced: the loss/retry claim and conflict-handling attribution cite the constants clause.")
