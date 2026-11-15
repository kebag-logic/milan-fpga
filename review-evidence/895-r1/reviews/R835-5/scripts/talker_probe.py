#!/usr/bin/env python3
"""talker_probe.py TREE OUT PREFIX [INTERFACES...]

Reviewer probe. With PREFIX a defect-name prefix: run the tree's own SRP mutation campaign (srp_mutants.campaign)
restricted to the defects whose name starts with PREFIX, at each interface count given (2: the 8x8/2if entity;
1: 1x1/1if), each defect planted in the campaign's own disposable copy of sw/firmware/ctrl under OUT.
With PREFIX "arms": run the tree's unplanted Talker arms (srp_arms.talker_arms: srp_talker.cpp at 1x1/1if and
8x8/2if, and SrpGate.* at 8x8/2if) on a disposable copy under OUT and print each arm's gtest summary.
Read-only on TREE. Exit 1 when a defect escaped or an arm failed."""
import shutil
import sys
from pathlib import Path

tree, out, prefix = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
counts = [int(a) for a in sys.argv[4:]] or [2, 1]
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree / 'sw/firmware/gtest'))
import srp_mutants  # noqa: E402

lwsrp = (tree / 'third_party/lwSRP').resolve()
if prefix == 'arms':
    import fw_gtest
    import srp_arms
    src = out / 'ctrl'
    shutil.copytree(srp_mutants.CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    t = srp_mutants.Tree(src, out / 'build', out / 'reuse', fw_gtest.Build(jobs=4))
    failed = False
    for o in srp_arms.talker_arms(t, lwsrp):
        lines = [x for x in o.log.splitlines() if x.startswith(('[  PASSED', '[  FAILED', '[==========]'))]
        print(f"{o.arm}: rc {o.rc}; " + ' | '.join(lines), flush=True)
        failed |= o.rc != 0
    print(f"arms: {'FAIL' if failed else 'PASS'}")
    sys.exit(1 if failed else 0)
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(prefix))
print(f"{len(srp_mutants.DEFECTS)} defects: {', '.join(d.name for d in srp_mutants.DEFECTS)}", flush=True)
failed = False
for n in counts:
    print(f"== interfaces {n}", flush=True)
    failed = srp_mutants.campaign(out / f"if{n}", lwsrp, 4, n) or failed
print(f"probe {prefix} at {counts}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
