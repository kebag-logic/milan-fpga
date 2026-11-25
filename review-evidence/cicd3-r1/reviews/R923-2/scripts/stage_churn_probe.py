#!/usr/bin/env python3
"""Churn probe for scripts/mutant_stage.py: N independent processes repeatedly take and
release slots of one prefix (half through TMPDIR, half through a symbolic link to it, plus
in-tree holders through a linked parent) and each checks, while it holds, that its slot
holds only its own token. Any overlap of two holders on one physical slot fails the probe.

usage: python3 -I stage_churn_probe.py REPO SCRATCH [PROCS] [ROUNDS]
"""
import os, subprocess, sys, tempfile, json
from pathlib import Path

WORKER = r"""
import os, sys, time, json, tempfile
from pathlib import Path
spec_repo, token, parent, rounds = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
sys.path.insert(0, spec_repo + "/scripts")
import mutant_stage
bad = 0; slots = {}
for r in range(rounds):
    with mutant_stage.directory("churn-", parent or None) as held:
        mine = f"{token}-{r}"
        Path(held, "owner").write_text(mine)
        time.sleep(0.002)
        names = sorted(os.listdir(held))
        if names != ["owner"] or Path(held, "owner").read_text() != mine:
            bad += 1
        key = str(Path(held).resolve()); slots[key] = slots.get(key, 0) + 1
print(json.dumps({"token": token, "bad": bad, "stable_slots": sum(v for k, v in slots.items() if "churn-" in Path(k).name and Path(k).name[6:].isdigit()), "rounds": rounds}))
"""

def main():
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    procs_n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    rounds = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    scratch.mkdir(parents=True, exist_ok=False)
    real = scratch / "tmp"; real.mkdir(mode=0o700)
    alias = scratch / "tmp-alias"; alias.symlink_to(real)
    tree = scratch / "tree"; tree.mkdir()
    tree_alias = scratch / "tree-alias"; tree_alias.symlink_to(tree)
    procs = []
    for n in range(procs_n):
        kind = n % 4
        tmpdir = str(real if kind in (0, 2) else alias)
        parent = "" if kind < 2 else str(tree if kind == 2 else tree_alias)
        env = {k: v for k, v in os.environ.items() if not k.startswith("CCACHE_")}
        env["TMPDIR"] = tmpdir
        procs.append(subprocess.Popen([sys.executable, "-I", "-c", WORKER, str(repo), f"p{n}", parent, str(rounds)],
                                      env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    total_bad = 0
    for p in procs:
        out, err = p.communicate(timeout=600)
        print(out.strip(), ("stderr=" + err.strip()[:200]) if err.strip() else "")
        if p.returncode != 0:
            print("worker rc", p.returncode); total_bad += 1
        else:
            total_bad += json.loads(out)["bad"]
    left = sorted(os.listdir(real / f"milan-mutant-stage-{os.getuid()}")) if (real / f"milan-mutant-stage-{os.getuid()}").exists() else []
    print(f"processes={procs_n} rounds={rounds} overlaps={total_bad} root_leftovers={left} tree_leftovers={sorted(os.listdir(tree))}")
    return 1 if total_bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
