#!/usr/bin/env python3
"""Probe, at each given revision, whether every planted mutant that edits
hdl/aecp/KL_aecp_notify.sv can still be planted: `git apply --check` for the
explicit patch files, and the exactly-once anchor rule for the Python drivers'
text edits. Builds and runs nothing.
Usage: plant_probe.py <repo> <scratch> <rev> [<rev> ...]"""
import importlib.util, subprocess, sys, shutil
from pathlib import Path

NTFY = "hdl/aecp/KL_aecp_notify.sv"
repo, scratch, revs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
bad_total = 0
for rev in revs:
    tree = scratch / f"plant-{rev[:12]}"
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", str(repo), "archive", rev], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=tar, check=True)
    print(f"== rev {rev}  notify blob "
          + subprocess.run(["git", "-C", str(repo), "rev-parse", f"{rev}:{NTFY}"],
                           capture_output=True, text=True).stdout.strip())
    bad = 0
    patches = sorted(p for p in tree.glob("tb/**/*.patch") if f"+++ b/{NTFY}" in p.read_text())
    for p in patches:
        r = subprocess.run(["git", "apply", "--check", str(p)], cwd=tree, capture_output=True, text=True)
        ok = r.returncode == 0
        bad += not ok
        print(f"  patch {p.relative_to(tree)}: {'APPLIES' if ok else 'REFUSED'}"
              + ("" if ok else "  | " + r.stderr.strip().replace("\n", " | ")))
    text = (tree / NTFY).read_text()
    for drv in ("tb/pp_top/notify_mutants.py", "tb/pp_top/d3_mutants.py"):
        sys.path[:0] = [str(tree / "tb" / "common"), str(tree / "tb" / "pp_top")]
        spec = importlib.util.spec_from_file_location(f"m{abs(hash((rev, drv)))}", tree / drv)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        n = 0
        for m in mod.MUTANTS:
            for rel, old, _new in m.edits:
                if rel != NTFY:
                    continue
                n += 1
                c = text.count(old)
                bad += c != 1
                if c != 1:
                    print(f"  {drv} {m.name}: anchor occurs {c} times REFUSED")
        print(f"  {drv}: {n} notify edits checked")
    print(f"  rev {rev[:12]}: {len(patches)} notify patches, {bad} refused")
    bad_total += bad
sys.exit(1 if bad_total else 0)
