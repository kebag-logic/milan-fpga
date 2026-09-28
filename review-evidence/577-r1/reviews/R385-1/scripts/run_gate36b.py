#!/usr/bin/env python3
"""Run only the gate 36b tests (plus gate 36a for context) from a tree root."""
import sys, importlib, io, contextlib
from pathlib import Path

root = Path(sys.argv[1]).resolve()
names = sys.argv[2:] or ["test_shipping_image_contract",
                         "test_shipping_image_contract_index_walk"]
sys.path.insert(0, str(root / "sw/builder"))
tb = importlib.import_module("test_builder")
assert Path(tb.__file__).resolve().is_relative_to(root), tb.__file__
rc = 0
for n in names:
    print(f"{n}:", flush=True)
    try:
        getattr(tb, n)()
        print(f"RESULT {n} PASS")
    except BaseException as exc:  # noqa: BLE001 - record every failure mode
        rc = 1
        print(f"RESULT {n} FAIL {type(exc).__name__}: {str(exc)[:300]}")
sys.exit(rc)
