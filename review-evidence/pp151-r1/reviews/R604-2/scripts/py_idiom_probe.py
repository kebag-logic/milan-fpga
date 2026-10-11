#!/usr/bin/env python3
"""Run the parent's Rule 12 per-module scan on chosen processor files.

usage: py_idiom_probe.py CHECKER_PY FILE...
CHECKER_PY is the parent's scripts/check_py_idiom.py at the dev commit under review;
its tree-scope helper module is stubbed because only `scan` is used here.
Exit 0 when every refused and ratcheted count is zero for every file.
"""
import importlib.util
import sys
import types
from pathlib import Path


def main() -> int:
    """Print every non-zero finding per file and return 1 if any exists."""
    checker, files = Path(sys.argv[1]), sys.argv[2:]
    stub = types.ModuleType("code_quality_scope")
    stub.PROJECT_SUBMODULES = ("protocol-processor",)
    stub.tracked = lambda pattern: []
    sys.modules["code_quality_scope"] = stub
    spec = importlib.util.spec_from_file_location("check_py_idiom", checker)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    bad = 0
    for name in files:
        counts, sites = mod.scan(Path(name).read_text(), name)
        nonzero = {k: v for k, v in counts.items() if v}
        print(f"{name}: {nonzero or 'all zero'}")
        for key, where in sites.items():
            for line, detail in where:
                print(f"    {key} at {line}: {detail}")
        bad += bool(nonzero)
    return int(bad != 0)


if __name__ == "__main__":
    raise SystemExit(main())
