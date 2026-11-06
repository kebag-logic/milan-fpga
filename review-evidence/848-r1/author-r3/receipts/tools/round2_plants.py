#!/usr/bin/env python3
"""The round-2 ruling's four plants, on one script: each must still be killed. Usage: round2_plants.py SCRIPT WORK"""
import subprocess, sys
from pathlib import Path
SRC = 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")'
PLANTS = {"R1": (SRC, 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
          "O1": ('for p in pages if p.area == area]', 'for p in pages if p.area == area and p.path != OUTPUT]'),
          "W7": ('grouped.setdefault(lanes[finding.page], []).append((finding, line))', 'grouped.setdefault(lanes[finding.page], [(finding, line)])'),
          "W8": ('f"- Statement: {finding.quote}", ', '')}
text = Path(sys.argv[1]).read_text(encoding="utf-8")
for name, (old, new) in PLANTS.items():
    assert text.count(old) == 1, name
    target = Path(sys.argv[2]) / name / "scripts" / "docs_inventory.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.replace(old, new), encoding="utf-8")
    done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True, timeout=200)
    print(name, "killed" if done.returncode else "SURVIVED")
