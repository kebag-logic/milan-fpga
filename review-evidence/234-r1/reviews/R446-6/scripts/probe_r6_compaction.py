#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 6): is the compaction commit c7cde331 behaviour-preserving for the self-test?

Loads pp_resource_gate_selftest.py as of <before> and <after> (each beside its own commit's gate and parser, in its
own scratch folder) and compares every module-level name: data by value, with any function inside it compared by
its bytecode and constants (line numbers excluded); functions by bytecode and constants; a bare object() sentinel compares equal to another. Prints every name that
differs, so the remainder can be read by hand.

Usage: probe_r6_compaction.py <checkout> <before> <after> <scratch-dir>
"""

import importlib.util
from pathlib import Path
import subprocess
import sys
import types

REPO, BEFORE, AFTER, SCRATCH = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
FILES = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py")


def load(commit: str) -> types.ModuleType:
    folder = SCRATCH / commit
    folder.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        (folder / name).write_bytes(subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:syn/ooc/{name}"],
                                                   check=True, capture_output=True).stdout)
    for name in ("pp_resource_gate", "pp_baseline_rank", "pp_resource_gate_selftest"):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(folder))
    try:
        spec = importlib.util.spec_from_file_location("pp_resource_gate_selftest", folder / FILES[2])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(folder))
    return module


def shape(value: object, depth: int = 0) -> object:
    """A comparable form: functions by code, containers element-wise."""
    if depth > 50:
        return "<deep>"
    if isinstance(value, types.FunctionType):
        return ("fn", code(value.__code__), tuple(shape(cell.cell_contents, depth + 1) for cell in value.__closure__ or ()))
    if isinstance(value, (tuple, list)):
        return (type(value).__name__, tuple(shape(item, depth + 1) for item in value))
    if isinstance(value, dict):
        return ("dict", tuple((key, shape(item, depth + 1)) for key, item in value.items()))
    if type(value) is object:
        return ("sentinel",)
    if isinstance(value, types.ModuleType):
        return ("module", value.__name__)
    if isinstance(value, type):
        return ("type", value.__qualname__)
    return ("value", repr(value))


def code(obj: types.CodeType) -> object:
    consts = tuple(code(c) if isinstance(c, types.CodeType) else repr(c) for c in obj.co_consts)
    return obj.co_code, consts, obj.co_names, obj.co_varnames


def main() -> None:
    before, after = load(BEFORE), load(AFTER)
    names_before = {n for n in vars(before) if not n.startswith("__")}
    names_after = {n for n in vars(after) if not n.startswith("__")}
    print(f"only before: {sorted(names_before - names_after)}")
    print(f"only after: {sorted(names_after - names_before)}")
    differ = [n for n in sorted(names_before & names_after) if shape(getattr(before, n)) != shape(getattr(after, n))]
    print(f"common names: {len(names_before & names_after)}; differing: {differ}")
    for kind in ("ROUTE_ARMS", "OOC_ARMS", "CHECK_ARMS", "MALFORMED"):
        if hasattr(before, kind):
            a, b = getattr(before, kind), getattr(after, kind)
            same = [shape(x) == shape(y) for x, y in zip(a, b)]
            print(f"{kind}: {len(a)} -> {len(b)} arms; labels equal: {[x[0] for x in a] == [y[0] for y in b]}; "
                  f"arms differing: {[a[i][0] for i, s in enumerate(same) if not s]}")


if __name__ == "__main__":
    main()
