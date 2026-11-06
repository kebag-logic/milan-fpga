#!/usr/bin/env python3
"""Show the required outcomes fit the module limit: apply a minimal disposable edit, then re-grade the survivors.

Usage: fix_feasibility_r787.py HEAD_SCRIPT WORKDIR RECEIPT
Illustration only; the design stays the executor's.
"""
import subprocess, sys
from pathlib import Path
head, work, receipt = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
text = head.read_text(encoding="utf-8")
EDITS = [
 ("            if text not in rendered + listed:\n", '            if text not in (listed if text.startswith("## ") else rendered):\n'),
 ('("archive index stays current", lambda root: None, 0, "archive index"),',
  '("archive index stays current", lambda root: None, 0, ("archive index", "| Documentation audit |")),'),
 ('"Copy of the D0-002 statement on `README.md`.", "## D0-002: README.md:5\\n",',
  '"Copy of the D0-002 statement on `README.md`.", "## D0-002: README.md:5\\n",\n          "## D0-001: docs/guides/A.md:3\\n\\n- Statement: resets to 0x1\\n",'),
]
for old, new in EDITS:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
MUT = {
 "R1": ('f"| {cell(source_of(finding))} | {cell(finding.correction)} |")', 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
 "O1": ('for p in pages if p.area == area]', 'for p in pages if p.area == area and p.path != OUTPUT]'),
 "W7": ('grouped.setdefault(lanes[finding.page], []).append((finding, line))', 'grouped.setdefault(lanes[finding.page], [(finding, line)])'),
 "W8": ('f"- Statement: {finding.quote}", ', ''),
}
def grade(name, source):
    d = work / name / "scripts"; d.mkdir(parents=True, exist_ok=True)
    (d / "docs_inventory.py").write_text(source, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(d / "docs_inventory.py"), "--selftest"], capture_output=True, text=True)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:120]
log = [f"edited script lines: {text.count(chr(10))}", f"edited script selftest: {grade('fixed', text)}"]
for name, (old, new) in MUT.items():
    assert text.count(old) == 1, name
    rc, note = grade(name, text.replace(old, new))
    log.append(f"{name}: {'killed' if rc else 'SURVIVED'} :: {note}")
receipt.write_text("\n".join(log) + "\n"); print("\n".join(log))
