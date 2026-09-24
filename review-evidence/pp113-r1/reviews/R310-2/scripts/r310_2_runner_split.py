#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer driver: the PR's own GSI mutation runner, split into groups.

Imports `mutations()` and `check_variant()` unchanged from
<repo>/tb/pp_top/gsi_mutants.py (read-only), copies the same source
directories into a private tree under --work, and runs only the variants
whose list position modulo --groups equals --group. Each group runs a golden
control first and a restored control last, with the same edit-site count and
named-failure rules as the runner. Used only so that every group fits a
bounded foreground step; the verdict rules are the runner's own.

Usage:
  r310_2_runner_split.py --repo <clone> --work <dir> --out <dir>
                         --verilator <path> --group N --groups M --cpus a,b
"""

import argparse
import importlib.util
import json
import os
import shutil
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--group", type=int, required=True)
    ap.add_argument("--groups", type=int, required=True)
    ap.add_argument("--cpus", required=True)
    a = ap.parse_args()
    os.sched_setaffinity(0, [int(c) for c in a.cpus.split(",")])
    spec = importlib.util.spec_from_file_location(
        "gsi_mutants", a.repo / "tb/pp_top/gsi_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = (a.out / f"group{a.group}").resolve()
    out.mkdir(parents=True, exist_ok=True)
    tree = (a.work / f"group{a.group}").resolve()
    if tree.exists():
        shutil.rmtree(tree)
    for directory in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(a.repo / directory, tree / directory,
                        ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    records = []
    errors = []

    def attempt(name, expected):
        try:
            records.append(mod.check_variant(tree, out, name, expected, a.verilator))
        except RuntimeError as exc:
            errors.append(str(exc))
            records.append({"variant": name, "passed": False, "error": str(exc)})

    attempt("golden", "")
    for i, (name, filename, old, new, count, expected) in enumerate(mod.mutations()):
        if i % a.groups != a.group:
            continue
        path = tree / filename
        original = path.read_text()
        if original.count(old) != count:
            errors.append(f"{name}: expected {count} exact edit sites")
            records.append({"variant": name, "passed": False, "error": errors[-1]})
            continue
        try:
            path.write_text(original.replace(old, new))
            attempt(name, expected)
        finally:
            path.write_text(original)
    attempt("restored", "")
    (out / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    shutil.rmtree(tree / "tb/pp_top/obj_dir", ignore_errors=True)
    print(f"group {a.group}: {len(records)} records, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
