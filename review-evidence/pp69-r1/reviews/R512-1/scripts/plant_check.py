#!/usr/bin/env python3
"""Reviewer probe: does every mutation arm still plant in a source tree?

Usage: plant_check.py TREE

Checks, without building or simulating:
  * every tb/**/*.patch through `git apply --check` from TREE's root;
  * every patch label named by a patch-driven driver exists as a file;
  * every exact-text arm of the plant() drivers (acmp, notify, d3) through the
    driver's own plant() on a private copy of the files it edits;
  * every other exact-text arm (gsi, name_wr, retry, srp_admission) through
    the driver's own counting rule (each anchor must occur exactly `count`
    times, applied in order).
Prints one line per refusal and a summary; exit 0 when nothing refuses.
"""
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def load(tree: Path, rel: str):
    path = tree / rel
    sys.path[:0] = [str(path.parent), str(tree / "tb/common")]
    spec = importlib.util.spec_from_file_location("drv_" + rel.replace("/", "_")[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    refused = []
    # 1. every patch file
    patches = sorted(tree.glob("tb/**/*.patch"))
    p_ok = 0
    for p in patches:
        r = subprocess.run(["git", "apply", "--check", str(p)], cwd=tree,
                           capture_output=True, text=True)
        if r.returncode == 0:
            p_ok += 1
        else:
            refused.append(f"patch {p.relative_to(tree)}: {r.stderr.strip().splitlines()[:1]}")
    # 2. patch labels named by the patch drivers exist
    missing = []
    for rel in ("tb/adp_engine/mutants.py", "tb/maap/mutants.py", "tb/srp_top/mutants.py",
                "tb/pp_top/aecp_mutants.py", "tb/pp_top/aecp_dispatch_mutants.py",
                "tb/pp_top/ctr_mutants.py"):
        text = (tree / rel).read_text()
        for name in set(re.findall(r'"([A-Za-z0-9_.-]+\.patch)"', text)):
            if not list(tree.glob(f"tb/**/{name}")):
                missing.append(f"{rel}: {name}")
    refused += [f"missing patch file named by {m}" for m in missing]
    # 3. plant() drivers
    plant_arms = 0
    plant_ok = 0
    for rel in ("tb/pp_top/acmp_mutants.py", "tb/pp_top/notify_mutants.py",
                "tb/pp_top/d3_mutants.py"):
        mod = load(tree, rel)
        for m in mod.MUTANTS:
            if not m.edits:
                continue
            plant_arms += 1
            with tempfile.TemporaryDirectory() as tmp:
                t = Path(tmp)
                for f in {e[0] for e in m.edits}:
                    (t / f).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(tree / f, t / f)
                why = mod.plant(t, m.edits)
            if why:
                refused.append(f"{rel} {m.name}: {why}")
            else:
                plant_ok += 1
    # 4. other exact-text arms
    other = 0
    other_ok = 0
    gsi = load(tree, "tb/pp_top/gsi_mutants.py")
    for name, f, old, new, count, _ in gsi.mutations():
        other += 1
        n = (tree / f).read_text().count(old)
        if n == count:
            other_ok += 1
        else:
            refused.append(f"gsi {name}: {n} sites, want {count}")
    other += 1
    eng = (tree / "hdl/aecp/KL_aecp_engine.sv").read_text()
    if eng.count("  assign name_wr_o = d3_nchg_w;") == 1:
        other_ok += 1
    else:
        refused.append("name_wr decode: export anchor not unique")
    retry = load(tree, "tb/acmp_talker/retry_mutants.py")
    src = (tree / retry.RTL).read_text()
    for name in retry.MUTATIONS:
        other += 1
        try:
            retry.mutated_source(src, name)
            other_ok += 1
        except RuntimeError as e:
            refused.append(f"retry {name}: {e}")
    adm = load(tree, "tb/srp_admission/mutants.py")
    asrc = (tree / adm.ADMISSION).read_text()
    for label, edits, _ in adm.MUTANTS:
        other += 1
        s = asrc
        ok = True
        for anchor, repl, count in edits:
            if s.count(anchor) != count:
                ok = False
                refused.append(f"srp_admission {label}: {s.count(anchor)} copies, want {count}")
                break
            s = s.replace(anchor, repl)
        other_ok += ok
    for r in refused:
        print("REFUSED", r)
    print(f"patch files: {p_ok} of {len(patches)} apply")
    print(f"plant() arms: {plant_ok} of {plant_arms} plant")
    print(f"patches + plant() arms: {p_ok + plant_ok} of {len(patches) + plant_arms}")
    print(f"other exact-text arms: {other_ok} of {other} plant")
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
