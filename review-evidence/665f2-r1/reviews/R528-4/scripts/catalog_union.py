#!/usr/bin/env python3
"""Compare the controller mutant catalog and arm lists across three commits.

Usage: catalog_union.py <repo> <f2-parent> <dev-parent> <merge-or-head> <workdir>
Exports sw/firmware (and the generator inputs it imports) of each commit with
git archive, imports ctrl_mutants, and prints whether the merged catalog is
exactly the union of both parents' (name, path, old, new, kills) records.
"""
import importlib, json, subprocess, sys, tarfile, io
from pathlib import Path

repo, f2, dev, head, work = sys.argv[1:6]
work = Path(work)


def load(rev: str) -> dict:
    dest = work / rev
    if not dest.exists():
        dest.mkdir(parents=True)
        data = subprocess.run(["git", "-C", repo, "archive", rev, "sw", "tb/common", "configs", "scripts"],
                              check=True, capture_output=True).stdout
        tarfile.open(fileobj=io.BytesIO(data)).extractall(dest, filter="data")
    test = dest / "sw/firmware/ctrl/test"
    for m in [k for k in sys.modules if k.startswith(("ctrl_", "maap_", "fw_", "nvm_", "suite_"))]:
        del sys.modules[m]
    sys.path[:0] = [str(test), str(dest / "sw/firmware/gtest"), str(dest / "scripts")]
    try:
        mod = importlib.import_module("ctrl_mutants")
        out = {}
        for m in mod.MUTANTS:
            kills = tuple(tuple(k) for k in m.kills())
            out[m.name] = (m.path, m.old, m.new, kills)
        return out
    finally:
        del sys.path[:3]


cats = {name: load(rev) for name, rev in (("f2", f2), ("dev", dev), ("head", head))}
union = dict(cats["dev"])
conflict = [n for n in cats["f2"] if n in union and union[n] != cats["f2"][n]]
union.update(cats["f2"])
res = {
    "counts": {k: len(v) for k, v in cats.items()},
    "union_count": len(union),
    "same_name_different_record_between_parents": conflict,
    "head_equals_union": cats["head"] == union,
    "missing_from_head": sorted(set(union) - set(cats["head"])),
    "extra_in_head": sorted(set(cats["head"]) - set(union)),
    "changed_in_head": sorted(n for n in union if n in cats["head"] and cats["head"][n] != union[n]),
    "maap_count_head": sum(1 for n in cats["head"] if n.startswith(("maap-", "r2-"))),
    "dev_only": sorted(set(cats["dev"]) - set(cats["f2"])),
}
print(json.dumps(res, indent=1))
sys.exit(0 if res["head_equals_union"] and not conflict else 1)
