#!/usr/bin/env python3
"""Dump the source campaign's mutants as JSON.

Usage: source_mutants.py SOURCE_CHECKOUT OUT.json
Imports the source tables from SOURCE_CHECKOUT/sw/firmware/ctrl/test.
"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import ctrl_mutants
out = []
for m in ctrl_mutants.MUTANTS:
    out.append({'name': m.name, 'path': m.path, 'old': m.old, 'new': m.new,
                'kills': [list(k) for k in m.kills()]})
Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
print(len(out), 'source mutants')
