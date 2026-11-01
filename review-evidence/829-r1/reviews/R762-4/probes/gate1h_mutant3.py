#!/usr/bin/env python3
"""Reader mutant: the planted text never reaches the list, and the once-only assert is removed with it.
A second run keeps the assert, which must then be what stops the gate. usage: gate1h_mutant3.py <clone> <scratch dir>
"""
import concurrent.futures, re, shutil, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); scratch = Path(sys.argv[2]).resolve()
OLD = 'str(planted) if Path(src).resolve() == datapath else src'
ASSERT = re.compile(r"^ +assert sources\.count\(str\(planted\)\) == 1, \\\n +f\"gate 1h: the build does not read .*\n", re.M)
def one(item):
    name, drop = item
    c = scratch / ("mut3" + ("a" if drop else "b")); shutil.rmtree(c, ignore_errors=True)
    shutil.copytree(root, c, symlinks=True)
    p = c / "sw/builder/test_builder.py"; s = p.read_text(); assert s.count(OLD) == 1; s = s.replace(OLD, "src")
    if drop:
        s, n = ASSERT.subn("", s); assert n == 1
    p.write_text(s)
    o = subprocess.run([sys.executable, "sw/builder/test_builder.py", "--gates", "test_gptp_datapath_carries_the_launch_shape"], cwd=c, capture_output=True, text=True)
    why = next((l for l in (o.stdout + o.stderr).splitlines() if l.startswith("AssertionError")), "(no assertion line)")
    shutil.rmtree(c, ignore_errors=True)
    return f"{'ok ' if o.returncode else 'BAD'} rc={o.returncode} {name}: {why[:170]}"
with concurrent.futures.ThreadPoolExecutor(2) as ex:
    for line in ex.map(one, [("the shipped file stays in the list, assert removed", True), ("the shipped file stays in the list, assert kept", False)]): print(line)
