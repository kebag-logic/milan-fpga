#!/usr/bin/env python3
"""Compare pre-fix and post-fix resolver observations over census assembly.

Usage: resolver_equivalence.py <checkout> <pre-rev> <asm> [<asm> ...]
Loads sw/builder/test_builder.py at <pre-rev> (git show) and from the
working tree, runs rv32_unit() of each over every assembly file, and
prints any difference in per-function stores, calls, returns, branches,
symstores, seeds, data and the defined/exported/addressed sets. Exit 1 on
any difference. Read-only for the checkout.
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

checkout, pre_rev, *asms = sys.argv[1:]
checkout = Path(checkout)
sys.path.insert(0, str(checkout / "sw/builder"))
for sub in ("scripts", "avdecc", "sw/litex"):
    sys.path.insert(0, str(checkout / sub))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


with tempfile.TemporaryDirectory() as tmp:
    pre_path = Path(tmp) / "test_builder_pre.py"
    pre_path.write_text(subprocess.run(
        ["git", "-C", str(checkout), "show", f"{pre_rev}:sw/builder/test_builder.py"],
        check=True, capture_output=True, text=True).stdout)
    pre = load("test_builder_pre", pre_path)
post = load("test_builder_post", checkout / "sw/builder/test_builder.py")


def view(module, asm):
    unit = module.rv32_unit(asm)
    out = {"data": unit["data"], "seeds": {k: {r: repr(v) for r, v in s.items()}
                                          for k, s in unit["seeds"].items()},
           "defined": sorted(unit["defined"]), "exported": sorted(unit["exported"]),
           "addressed": sorted(unit["addressed"]), "private": sorted(unit["private"])}
    for name, run in sorted(unit["runs"].items()):
        out[name] = {key: repr(run[key]) for key in
                     ("stores", "calls", "rets", "branches")}
        out[name]["symstores"] = sorted(run["symstores"])
        out[name]["reachable"] = sorted(run["reachable"])
    return out


different = 0
for path in asms:
    asm = Path(path).read_text()
    a, b = view(pre, asm), view(post, asm)
    keys = sorted(set(a) | set(b))
    diffs = [k for k in keys if a.get(k) != b.get(k)]
    stores = sum(len(run["stores"]) for run in post.rv32_unit(asm)["runs"].values())
    print(f"{path}: functions={len(post.rv32_unit(asm)['runs'])} "
          f"stores={stores} differing_keys={diffs}")
    for k in diffs:
        print(f"  PRE  {k}: {a.get(k)}")
        print(f"  POST {k}: {b.get(k)}")
    different += bool(diffs)
print("EQUIVALENT" if not different else f"DIFFERENT in {different} file(s)")
sys.exit(1 if different else 0)
