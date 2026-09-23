#!/usr/bin/env python3
"""Apply one textual mutation to an RTL file, run a suite, restore the file.

usage: a218-mutate.py NAME SUITE FILE OLD NEW [OLD NEW ...]
The log goes to $OUT/logs/93-<suite>-mutant-<NAME>.log; the tally and the
first failing check names are printed. The file is always restored.
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = "$LANES/pp92-93-boot-restore"
OUT = "$MANAGEMENT/2026-09-23/pp92-a218/logs"
PIN = "$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin"

name, suite, rel = sys.argv[1], sys.argv[2], sys.argv[3]
pairs = list(zip(sys.argv[4::2], sys.argv[5::2]))
path = os.path.join(ROOT, rel)
orig = open(path).read()
text = orig
for old, new in pairs:
    n = text.count(old)
    if n != 1:
        sys.exit(f"{name}: pattern occurs {n} times: {old!r}")
    text = text.replace(old, new)
bak = path + ".a218bak"
shutil.copy2(path, bak)
try:
    open(path, "w").write(text)
    env = dict(os.environ, PATH=PIN + ":" + os.environ["PATH"])
    tdir = os.path.join(ROOT, "tb", suite)
    target = os.environ.get("TARGET", "")
    cmd = ["make"] + ([target] if target else [])
    p = subprocess.run(cmd, cwd=tdir, env=env, capture_output=True, text=True,
                       timeout=int(os.environ.get("TMO", "1500")))
    log = os.path.join(OUT, f"93-{suite}-mutant-{name}.log")
    with open(log, "w") as f:
        f.write(f"# mutant {name} on {rel}\n")
        for old, new in pairs:
            f.write(f"# - {old}\n# + {new}\n")
        f.write(f"# make {target} in tb/{suite}: exit {p.returncode}\n")
        f.write(p.stdout)
        f.write(p.stderr)
    tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", p.stdout)
    fails = [l for l in p.stdout.splitlines() if l.startswith("FAIL")]
    print(f"{name}: exit {p.returncode} {tally[-1] if tally else 'NO TALLY'}")
    for l in fails[:12]:
        print("   ", l[:170])
    if len(fails) > 12:
        print(f"    ... {len(fails) - 12} more")
finally:
    shutil.move(bak, path)
