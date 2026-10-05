#!/usr/bin/env python3
"""Reviewer plant check: does every mutation arm still plant at a given tree?

Usage: plant_check.py TREE   (TREE = a git-archive extraction; nothing in it is written)

Group A (the 476 set): every tb/**/*.patch through `git apply --check` at TREE, and
every exact-text arm of the notify, d3 and acmp drivers through the driver's own
plant() on a private copy of the files the arm edits.
Group B (the 96 set): the other text-planting drivers under their own anchor rules:
tb/acmp_talker/retry_mutants.py (every MUTATIONS entry through its own
mutated_source(), plus the two bench-probe anchors it replaces), gsi_mutants.py
(each mutations() entry's exact count), name_wr_mutant.py (its one export anchor)
and tb/srp_admission/mutants.py (each MUTANTS edit's exact count, applied in order).
Prints one line per arm and a summary; exit 1 if any arm refuses.
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
results = []  # (group, arm, ok, detail)


def load(rel):
    path = TREE / rel
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(path.stem + "_rv", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- group A: patches
for patch in sorted(TREE.glob("tb/**/*.patch")):
    rel = patch.relative_to(TREE)
    p = subprocess.run(["git", "apply", "--check", str(patch)], cwd=TREE,
                       capture_output=True, text=True)
    results.append(("A", f"patch {rel}", p.returncode == 0, p.stderr.strip()[:200]))

# ---- group A: exact-text arms through each driver's own plant()
for rel in ("tb/pp_top/notify_mutants.py", "tb/pp_top/d3_mutants.py", "tb/pp_top/acmp_mutants.py"):
    mod = load(rel)
    for m in mod.MUTANTS:
        with tempfile.TemporaryDirectory(prefix="r494-plant-") as tmp:
            t = Path(tmp)
            for f in {e[0] for e in m.edits}:
                (t / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(TREE / f, t / f)
            before = {f: (t / f).read_text() for f in {e[0] for e in m.edits}}
            refusal = mod.plant(t, m.edits)
            changed = any((t / f).read_text() != before[f] for f in before)
            ok = refusal == "" and changed
            results.append(("A", f"{rel}:{m.name}", ok, refusal or ("" if changed else "no byte changed")))

# ---- group B
retry = load("tb/acmp_talker/retry_mutants.py")
src = (TREE / retry.RTL).read_text()
for name in retry.MUTATIONS:
    try:
        out = retry.mutated_source(src, name)
        results.append(("B", f"retry:{name}", out != src, "" if out != src else "no byte changed"))
    except RuntimeError as exc:
        results.append(("B", f"retry:{name}", False, str(exc)))
bfm = (TREE / "tb/acmp_talker/sim_main.cpp").read_text()
for anchor in ("  ++checks;", "if (!(cond)) { ++fails;"):
    n = bfm.count(anchor)
    results.append(("B", f"retry:bench-probe {anchor!r}", n >= 1, f"count {n}"))

gsi = load("tb/pp_top/gsi_mutants.py")
for name, filename, old, new, count, _exp in gsi.mutations():
    n = (TREE / filename).read_text().count(old)
    results.append(("B", f"gsi:{name}", n == count, f"count {n} want {count}"))

eng = (TREE / "hdl/aecp/KL_aecp_engine.sv").read_text()
n = eng.count("  assign name_wr_o = d3_nchg_w;")
results.append(("B", "name_wr:decode", n == 1, f"count {n} want 1"))

adm = load("tb/srp_admission/mutants.py")
original = (TREE / adm.ADMISSION).read_text()
for label, edits, _exp in adm.MUTANTS:
    source, ok, detail = original, True, ""
    for anchor, replacement, count in edits:
        if source.count(anchor) != count:
            ok, detail = False, f"{anchor!r} count {source.count(anchor)} want {count}"
            break
        source = source.replace(anchor, replacement)
    results.append(("B", f"srp_admission:{label}", ok, detail))

for g, arm, ok, detail in results:
    print(f"{g} {'PLANTS ' if ok else 'REFUSED'} {arm} {detail}".rstrip())
for g in ("A", "B"):
    sel = [r for r in results if r[0] == g]
    print(f"group {g}: {sum(r[2] for r in sel)} of {len(sel)} plant")
sys.exit(0 if all(r[2] for r in results) else 1)
