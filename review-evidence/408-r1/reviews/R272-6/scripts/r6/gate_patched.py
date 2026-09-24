#!/usr/bin/env python3
"""R272-6: run the WHOLE gate 1b (test_firmware_compiler.run_gate) on an
in-memory copy of <tree>/sw/builder/test_builder.py with count-checked
--patch replacements (JSON list of [old, new]). No file in <tree> is written.
Usage: gate_patched.py --tree <repo> (--sdk <dir> | --absent) --audit <jsonl>
       [--patch <json> ...]"""
import argparse
import json
import sys
import types
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sdk", type=Path)
    mode.add_argument("--absent", action="store_true")
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--patch", type=Path, action="append", default=[])
    args = parser.parse_args()
    tree = args.tree.resolve()
    builder_path = tree / "sw/builder/test_builder.py"
    source = builder_path.read_text(encoding="utf-8")
    for patch_file in args.patch:
        for old, new in json.loads(patch_file.read_text(encoding="utf-8")):
            assert source.count(old) == 1, f"{patch_file}: {old!r}"
            source = source.replace(old, new, 1)
        print(f"PATCHED: {patch_file.name}", flush=True)
    sys.path.insert(0, str(tree / "scripts"))
    sys.path.insert(0, str(tree / "sw/builder"))
    module = types.ModuleType("test_builder")
    module.__file__ = str(builder_path)
    sys.modules["test_builder"] = module
    exec(compile(source, str(builder_path), "exec"), module.__dict__)
    import test_firmware_compiler as tfc
    tfc.run_gate(None if args.absent else args.sdk.resolve(), args.audit,
                 False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
