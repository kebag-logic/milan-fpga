#!/usr/bin/env python3
"""[R383] Drive probe_elab.py over the base tree and hook-wiring mutants, then
check whether the committed #607 test file notices each mutant.
Usage: elab_mutants.py <extracted head tree> <empty out dir> <litex python>"""
import json, os, shutil, subprocess, sys
from pathlib import Path
tree, out, py = Path(sys.argv[1]).resolve(), str(Path(sys.argv[2]).resolve()), sys.argv[3]
here = Path(__file__).resolve().parent
A = '                if board == "ax7101":\n                    add_eth_constraints('
CASES = [("BASE", None, None),
         ("M7 gate to arty", A, A.replace('"ax7101"', '"arty"')),
         ("M8 wrong port", 'lookup_request("eth_clocks", eth_phy_index).rx)',
          'lookup_request("eth_clocks", 1 - eth_phy_index).rx)'),
         ("M16 call unreachable when a MAC exists", A,
          A.replace('"ax7101":', '"ax7101" and not with_mac:'))]
for label, old, new in CASES:
    cmd = [py, "-B", str(here / "probe_elab.py"), str(tree), out] + ([old, new] if old else [])
    r = subprocess.run(cmd, cwd=tree / "sw/litex", capture_output=True, text=True, timeout=600,
                       env={**os.environ, "PYTHONHASHSEED": "0"})
    marked = [l for l in r.stdout.splitlines() if l.startswith("RESULT: ")]
    if not marked:
        sys.exit(f"{label}: probe produced no result\n{r.stderr[-3000:]}")
    d = json.loads(marked[-1][len("RESULT: "):])
    unit = "n/a"
    if old:
        mut = tree.parent / "elab-mut"
        shutil.rmtree(mut, ignore_errors=True); shutil.copytree(tree, mut, symlinks=True)
        f = mut / "sw/litex/milan_soc.py"; f.write_text(f.read_text().replace(old, new))
        u = subprocess.run([py, "-B", "sw/builder/test_clock_constraints.py"], cwd=mut,
                           capture_output=True, text=True, timeout=600)
        unit = "KILLED" if u.returncode else "SURVIVED"
        shutil.rmtree(mut)
    print(f"{label}: elaboration={d['result'][:120]!r} hook_calls={len(d['add_eth_constraints_calls'])} "
          f"bounded_eth={[c['bounded_eth'] for c in d['add_eth_constraints_calls']]} "
          f"outdir_left={d['outdir_left']} committed_test={unit}")
