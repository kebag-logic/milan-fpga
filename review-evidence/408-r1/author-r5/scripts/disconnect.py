#!/usr/bin/env python3
"""[A261] scratch: run gate 1b (absent mode) on an IN-MEMORY copy of the
lane's sw/builder/test_builder.py with exact, count-checked string patches.
No file in the lane is written. Prints the first assertion the gate stops on,
or GATE PASS.

usage: disconnect.py <lane> <patch.json> [--sdk <sdk-host-dir>]
patch.json: [[old, new], ...], each old occurring exactly once.
"""
import json
import sys
import tempfile
import types
from pathlib import Path

lane, patch_file = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sdk = Path(sys.argv[4]).resolve() if sys.argv[3:4] == ["--sdk"] else None
path = lane / "sw/builder/test_builder.py"
source = path.read_text(encoding="utf-8")
for old, new in json.loads(patch_file.read_text(encoding="utf-8")):
    assert source.count(old) == 1, f"patch anchor occurs {source.count(old)}x"
    source = source.replace(old, new, 1)
sys.path[:0] = [str(lane / "sw/builder"), str(lane / "scripts")]
module = types.ModuleType("test_builder")
module.__file__ = str(path)
sys.modules["test_builder"] = module
exec(compile(source, str(path), "exec"), module.__dict__)
import test_firmware_compiler as tfc  # noqa: E402  binds the module above

with tempfile.TemporaryDirectory(prefix="a261-dis-") as tmp:
    try:
        tfc.run_gate(sdk, Path(tmp) / "audit.jsonl", False)
    except AssertionError as exc:
        print("GATE STOPPED:", str(exc)[:1500])
        sys.exit(0)
print("GATE PASS with the patch applied")
