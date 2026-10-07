#!/usr/bin/env python3
"""Run the PR's ctrl_mutants.MUTANTS in parallel isolated roots (same plant, arms and caught())."""
import shutil, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
CLONE = Path(sys.argv[1]).resolve(); WORK = Path(sys.argv[2]).resolve(); JOBS = int(sys.argv[3])
sys.path[:0] = [str(CLONE / "sw/firmware/ctrl/test"), str(CLONE / "sw/firmware/gtest")]
import ctrl_mutants, ctrl_arms, fw_gtest
from ctrl_build import Tree, Refusal, Outcome
from ctrl_reuse import cut_reuse
REUSE = WORK / "reuse"
def one(i):
    m = ctrl_mutants.MUTANTS[i]; root = WORK / f"m{i:03d}"
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "unit": ctrl_arms.arm_unit, "walk": ctrl_arms.arm_walk, "entity": ctrl_arms.arm_entity,
            "rv32": lambda tree: ctrl_arms.arm_rv32(tree, True)}
    tree = Tree(ctrl_mutants.plant(m, root), root / "work" / "build", REUSE, fw_gtest.Build(jobs=2))
    missed = []
    for arm, test, needle in m.kills():
        try:
            outcome = arms[arm](tree)
        except Refusal as exc:
            outcome = Outcome(arm, 2, f"refused: {exc}")
        if not ctrl_mutants.caught(test, needle, outcome):
            missed.append(f"{arm}:{test}")
    shutil.rmtree(root, ignore_errors=True)
    return m.name, missed
if __name__ == "__main__":
    shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir(parents=True)
    cut_reuse(REUSE)
    with ProcessPoolExecutor(JOBS) as ex:
        res = list(ex.map(one, range(len(ctrl_mutants.MUTANTS))))
    for name, missed in res:
        print(f"[{'ok' if not missed else 'ESCAPED'}] {name} {' '.join(missed)}")
    print(f"PR ctrl campaign: {sum(not m for _, m in res)} of {len(res)} caught")
    sys.exit(0 if all(not m for _, m in res) else 1)
