#!/usr/bin/env python3
"""Run format_mutants.run_pair for one two-copy arm with a kept work dir, log
every make command it issues, and report which planted files each build
compiled (from Verilator's dependency files). usage:
probe_pair_inputs.py <tree> <work-dir> <arm-prefix>"""
import subprocess, sys
from pathlib import Path
tree, work, arm = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(tree / "tb/verilator/avtp_rxmon"))
import format_mutants as fm  # noqa: E402
real = subprocess.run
def logged(cmd, *a, **k):
    if cmd and cmd[0] == "make":
        print("MAKE:", " ".join(str(c) for c in cmd[1:]))
    return real(cmd, *a, **k)
subprocess.run = logged
work.mkdir(parents=True, exist_ok=True)
pair = next(p for p in fm.BOTH_COPIES if p[0].startswith(arm))
caught = fm.run_pair(fm.RTL.read_text(), fm.REF.read_text(), pair, work)
print("caught:", caught)
orig = {"ctx": fm.RTL.read_text(), "ctx_ref": fm.REF.read_text()}
for f in sorted(work.glob("KL_avtp_rx_monitor_*.sv")):
    stem = "ctx_ref" if "_ctx_ref_" in f.name else "ctx"
    a, b = orig[stem].splitlines(), f.read_text().splitlines()
    d = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    print(f"{f.name}: {len(d)} line(s) differ from the {stem} source; same length: {len(a) == len(b)}")
    for i, x, y in d:
        print(f"   :{i}\n     - {x.strip()}\n     + {y.strip()}")
for dep in sorted(work.rglob("*__ver.d")):
    srcs = [s for s in dep.read_text().split() if s.endswith(".sv") and "KL_avtp_rx_monitor_ctx" in s]
    print(f"{dep.relative_to(work)}: {[Path(s).name for s in srcs]}")
