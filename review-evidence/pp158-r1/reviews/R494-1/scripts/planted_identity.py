#!/usr/bin/env python3
"""Planted-design identity for every arm that plants into KL_aecp_notify.sv.

Usage: planted_identity.py BASE_TREE HEAD_TREE LANE_RTL_DIFF
For each arm present at both trees (patches through git apply, exact-text arms of
the notify/d3/acmp drivers through the driver's own plant()), plant at base and at
head, apply the lane's KL_aecp_notify.sv diff to the planted base file, and require
it to equal the planted head file byte for byte. An arm whose planted base file
cannot take the lane diff is reported, not passed.
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE, HEAD, DIFF = (Path(a).resolve() for a in sys.argv[1:4])
NTFY = "hdl/aecp/KL_aecp_notify.sv"


def load(tree, rel):
    path = tree / rel
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(path.stem + "_" + tree.name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def planted_patch(tree, patch):
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        for f in subprocess.run(["git", "apply", "--numstat", str(patch)], cwd=tree,
                                capture_output=True, text=True).stdout.split("\n"):
            if f:
                rel = f.split("\t")[2]
                (t / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(tree / rel, t / rel)
        subprocess.run(["git", "apply", str(patch)], cwd=t, check=True)
        return (t / NTFY).read_text()


def planted_text(mod, tree, edits):
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        for f in {e[0] for e in edits}:
            (t / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(tree / f, t / f)
        assert mod.plant(t, edits) == ""
        return (t / NTFY).read_text()


def lane(base_text):
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / NTFY).parent.mkdir(parents=True)
        (t / NTFY).write_text(base_text)
        p = subprocess.run(["git", "apply", str(DIFF)], cwd=t, capture_output=True, text=True)
        return (t / NTFY).read_text() if p.returncode == 0 else None


arms = []
for patch in sorted(HEAD.glob("tb/**/*.patch")):
    rel = patch.relative_to(HEAD)
    if NTFY in patch.read_text() and (BASE / rel).exists():
        arms.append((str(rel), planted_patch(BASE, BASE / rel), planted_patch(HEAD, patch)))
for drv in ("tb/pp_top/notify_mutants.py", "tb/pp_top/d3_mutants.py", "tb/pp_top/acmp_mutants.py"):
    mb, mh = load(BASE, drv), load(HEAD, drv)
    base_arms = {m.name: m for m in mb.MUTANTS}
    for m in mh.MUTANTS:
        if any(e[0] == NTFY for e in m.edits) and m.name in base_arms:
            arms.append((f"{drv}:{m.name}", planted_text(mb, BASE, base_arms[m.name].edits),
                         planted_text(mh, HEAD, m.edits)))
ok = 0
for name, b, h in arms:
    moved = lane(b)
    same = moved is not None and moved == h
    ok += same
    print(f"{'IDENTICAL' if same else ('NO-APPLY ' if moved is None else 'DIFFERS  ')} {name}")
print(f"{ok} of {len(arms)} notify-planting arms: lane diff of planted base == planted head")
sys.exit(0 if ok == len(arms) else 1)
