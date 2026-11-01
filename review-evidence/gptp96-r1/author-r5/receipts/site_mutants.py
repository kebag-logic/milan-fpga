"""Silence each finding site of check_docs.py in turn and report whether --selftest notices.

usage: python3 -I site_mutants.py <checkout-copy> <first-line> <last-line>
The copy's scripts/check_docs.py is mutated in place and restored after each run.
"""
import re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve(); first, last = int(sys.argv[2]), int(sys.argv[3])
script = root / "scripts" / "check_docs.py"
original = script.read_text(encoding="utf-8")
lines = original.splitlines(keepends=True)
survivors = 0
try:
    for index, line in enumerate(lines, start=1):
        if not (first <= index <= last) or not re.search(r"findings\.(append|extend)\(", line):
            continue
        mutant = lines[:]
        mutant[index - 1] = re.sub(r"findings\.(append|extend)\(", "(lambda *_: None)(", line, count=1)
        script.write_text("".join(mutant), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", str(script), "--selftest"],
                             capture_output=True, text=True, cwd=root)
        verdict = "killed" if run.returncode != 0 else "SURVIVED"
        survivors += run.returncode == 0
        tail = (run.stdout.strip().splitlines() or [""])[-1]
        print(f"line {index:4d} {verdict:8s} rc={run.returncode} {line.strip()[:60]!r} -> {tail} {run.stderr.strip()[-80:]}")
finally:
    script.write_text(original, encoding="utf-8")
print(f"survivors {survivors}")
