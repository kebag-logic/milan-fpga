#!/usr/bin/env python3
"""Run the PR's own srp_mutants.DEFECTS in parallel isolated roots (same plant, arm and caught())."""
import shutil, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
CLONE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("$REVIEWS/r532-1-665f4"); WORK = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("."); JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 1
sys.path[:0] = [str(CLONE / "sw/firmware/ctrl/test"), str(CLONE / "sw/firmware/gtest")]
import srp_mutants, fw_gtest
from ctrl_build import CTRL, Tree, Refusal
from srp_arms import arm_srp
LW = CLONE / "third_party/lwSRP"
def one(i):
    d = srp_mutants.DEFECTS[i]; out = WORK / f"{i:02d}"; src = out / "ctrl"
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / d.path; text = target.read_text()
    if text.count(d.old) != 1:
        return d.name, False, f"{text.count(d.old)} sites"
    target.write_text(text.replace(d.old, d.new))
    selected = d.test if "." in d.test else "Srp." + d.test
    try:
        r = arm_srp(Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=2)), LW, 2, debug=d.debug, test=(d.suite, selected))
        ok = srp_mutants.caught(selected, d.needle, r)
    except Refusal as e:
        return d.name, False, str(e)[:120]
    shutil.rmtree(out, ignore_errors=True)
    return d.name, ok, d.test
if __name__ == '__main__':
    with ProcessPoolExecutor(JOBS) as ex:
        res = list(ex.map(one, range(len(srp_mutants.DEFECTS))))
    for name, ok, why in res:
        print(f"[{'ok' if ok else 'ESCAPED'}] {name}: {why}")
    print(f"PR SRP campaign: {sum(ok for _, ok, _ in res)} of {len(res)} caught")
    sys.exit(0 if all(ok for _, ok, _ in res) else 1)
