#!/usr/bin/env python3
"""Disable or weaken each rule of check_ooc_clock.py and require its selftest to fail.

Usage: mutate_checker.py <path/to/check_ooc_clock.py> <scratch-dir>
Prints one line per mutant: name, selftest rc, how it was killed.
"""
import subprocess
import sys
from pathlib import Path

SRC = Path(sys.argv[1]).read_text(encoding="utf-8")
SCRATCH = Path(sys.argv[2])
SCRATCH.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    "R1 read_xdc-before-synth disabled":
        ('        findings.append(f"{name}: {XDC} is not read before synth_design")\n    for line',
         '        pass\n    for line'),
    "R1b any read_xdc basename accepted":
        ('words[0] == "read_xdc" and words[-1].split("/")[-1] == XDC',
         'words[0] == "read_xdc"'),
    "R2 constraint-after-synth disabled":
        ('            findings.append(f"{name}:{line}: {words[0]} after synth_design")',
         '            pass'),
    "R2b only read_xdc forbidden after synth":
        ('        if words[0] in CONSTRAINT_COMMANDS:\n            findings.append(f"{name}:{line}',
         '        if words[0] == "read_xdc":\n            findings.append(f"{name}:{line}'),
    "R3 synth count rule disabled":
        ('    if len(synth) != 1:\n', '    if len(synth) == 0:\n'),
    "R4 xdc clock count disabled":
        ('    if len(clocks) != 1 or clocks[0] is None:', '    if not clocks:'),
    "R5 period/port rule disabled":
        ('    if float(period) != PERIOD_NS or port != CLOCK_PORT:', '    if False:'),
    "R5b port not compared":
        ('    if float(period) != PERIOD_NS or port != CLOCK_PORT:', '    if float(period) != PERIOD_NS:'),
    "L1 never-started rule disabled":
        ('    if command is None or start is None:\n        return [f"{name}: synth_design never started"]',
         '    if command is None or start is None:\n        return []'),
    "L2 did-not-complete rule disabled":
        ('        return [f"{name}: synth_design did not complete"]', '        return []'),
    "L3 read echo rule disabled":
        ('        findings.append(f"{name}: {XDC} is not read before synth_design")\n    mapping',
         '        pass\n    mapping'),
    "L3b read echo searched whole log":
        ('    if first(lines, LOG_READ_RE, 0, command) is None:', '    if first(lines, LOG_READ_RE) is None:'),
    "L4 parse rule disabled":
        ('        findings.append(f"{name}: synth_design did not parse {XDC} before mapping")', '        pass'),
    "L4b parse searched whole log":
        ('    if first(lines, LOG_PARSE_RE, start, done if mapping is None else mapping) is None:',
         '    if first(lines, LOG_PARSE_RE) is None:'),
    "L5 echo-after-done rule disabled":
        ('            findings.append(f"{name}:{index + 1}: {echo.group(1)} after synth_design")', '            pass'),
}

print("control", end=": ")
ctl = SCRATCH / "control.py"
ctl.write_text(SRC, encoding="utf-8")
r = subprocess.run([sys.executable, "-I", str(ctl), "--selftest"], capture_output=True, text=True)
print(f"rc={r.returncode} {r.stdout.strip()}")
killed = 0
for i, (label, (old, new)) in enumerate(MUTANTS.items()):
    assert SRC.count(old) == 1, (label, SRC.count(old))
    path = SCRATCH / f"mutant_{i:02d}.py"
    path.write_text(SRC.replace(old, new), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(path), "--selftest"], capture_output=True, text=True)
    out = (r.stdout.strip().splitlines() or [""])[-1]
    err = (r.stderr.strip().splitlines() or [""])[-1]
    how = out if "escaped" in out else (f"crash: {err}" if r.returncode else f"SURVIVED: {out}")
    killed += r.returncode != 0
    print(f"{label}: rc={r.returncode} {how}")
print(f"killed {killed}/{len(MUTANTS)}")
