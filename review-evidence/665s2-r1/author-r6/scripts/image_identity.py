#!/usr/bin/env python3
"""Rebuild the budget harness's linked images at a checkout's head and compare each ELF's sha256 with the digest a
round-2 build.json recorded for it (key build:image/ctrl_app.elf). Only build.firmware runs: the runtime archives
and the linked split image, through runtime_ssp.py and ctrl_srp_image.py (or fixture_variant.py), unchanged. No SoC
and no Verilator model are built.

Usage: image_identity.py CHECKOUT OUT RECEIPTS ARM...
RECEIPTS holds <arm>/build.json; each arm is rebuilt at its recorded shape, interfaces, mutation and variant.
Exit 0 only if every ELF matches.
"""
import hashlib
import json
import sys
from pathlib import Path

checkout, out, receipts = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import build  # noqa: E402

ok = True
for arm in sys.argv[4:]:
    spec = json.loads((receipts / arm / 'build.json').read_text())
    want = spec['inputs']['build:image/ctrl_app.elf']
    (out / arm).mkdir(parents=True, exist_ok=True)
    elf = build.firmware(out / arm, spec['shape'], spec['interfaces'], spec['mutation'], spec['variant'])
    got = hashlib.sha256(elf.read_bytes()).hexdigest()
    same = got == want
    ok &= same
    print(f"{'SAME' if same else 'DIFFERENT'} {arm} ({spec['shape']}, {spec['interfaces']} interface(s), mutation "
          f"{spec['mutation']}, variant {spec['variant']}): recorded {want}, rebuilt {got}", flush=True)
sys.exit(0 if ok else 1)
