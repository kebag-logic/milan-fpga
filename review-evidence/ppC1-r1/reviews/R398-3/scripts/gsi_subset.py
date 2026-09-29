#!/usr/bin/env python3
"""Run named variants of tb/pp_top/gsi_mutants.py, each in its own isolated tree, in parallel.

usage: gsi_subset.py <repo> <outdir> <verilator> <variant|golden> [...]
Uses the driver's own mutations() table and check_variant() verdict unchanged;
only the scheduling differs (one private tree per variant instead of one shared
tree edited in turn). The checkout is never written.
"""
import concurrent.futures
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

repo, out, verilator = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
want = sys.argv[4:]
spec = importlib.util.spec_from_file_location("gsi", repo / "tb/pp_top/gsi_mutants.py")
gsi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsi)
table = {v[0]: v for v in gsi.mutations()}
out.mkdir(parents=True, exist_ok=True)


def one(name: str) -> tuple[str, str]:
    with tempfile.TemporaryDirectory(prefix="gsi-subset-", dir=out) as temp:
        tree = Path(temp)
        for directory in ("hdl", "tb/common", "tb/pp_top"):
            shutil.copytree(repo / directory, tree / directory,
                            ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
        expected = ""
        if name != "golden":
            _, filename, old, new, count, expected = table[name]
            path = tree / filename
            text = path.read_text()
            if text.count(old) != count:
                return name, "REFUSED"
            path.write_text(text.replace(old, new))
        try:
            gsi.check_variant(tree, out, name, expected, verilator)
            return name, "PASS" if name == "golden" else "DETECTED"
        except RuntimeError as err:
            return name, f"FAILED {err}"


with concurrent.futures.ThreadPoolExecutor(min(8, len(want))) as pool:
    results = list(pool.map(one, want))
for n, v in results:
    print(f"RESULT {n} {v}")
ok = all(v in ("PASS", "DETECTED") for _, v in results)
print("gsi subset:", "OK" if ok else "NOT OK")
sys.exit(0 if ok else 1)
