#!/usr/bin/env python3
"""Judge each named file with the bare-metal scope gate's own per-file scanner (#259), every
policy class on every line, so each file the lane touches reports its own finding count.
Usage: baremetal_scan_files.py CHECKOUT ROOT PATH... (PATH relative to ROOT)."""
import importlib.util
import pathlib
import sys

checkout, root = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location('check_baremetal_only', checkout / 'scripts/check_baremetal_only.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
total = 0
for path in sys.argv[3:]:
    findings = gate.scan_path(path) + gate.scan_file(root, path)
    lines = len((root / path).read_text(encoding='utf-8', errors='replace').splitlines())
    total += len(findings)
    print(f'{path}: {lines} lines, {len(findings)} findings')
    for f in findings:
        print('  ', f)
print(f'baremetal per-file scan: {total} findings across {len(sys.argv) - 3} files')
raise SystemExit(1 if total else 0)
