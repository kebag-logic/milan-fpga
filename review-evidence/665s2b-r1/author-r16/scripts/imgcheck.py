#!/usr/bin/env python3
"""The harness's images rebuilt at a head through its own build.firmware(), and each ELF's sha256 against the leg
that measured it: the legs' figures speak for the head only where the image is the same.

usage: imgcheck.py CHECKOUT OUT BUILDS LEG:SHAPE:INTERFACES:MUTATION:VARIANT ...
"""
import hashlib
import sys
from pathlib import Path

checkout, out, builds, *items = sys.argv[1:]
sys.path.insert(0, str(Path(checkout) / 'tb/verilator/ctrl_service_budget'))
import build  # noqa: E402

bad = 0
for item in items:
    leg, shape, n_if, mutation, variant = item.split(':')
    (Path(out) / leg).mkdir(parents=True, exist_ok=True)
    elf = build.firmware(Path(out) / leg, shape, int(n_if), mutation, variant)
    now = hashlib.sha256(elf.read_bytes()).hexdigest()
    then = hashlib.sha256((Path(builds) / leg / 'image/ctrl_app.elf').read_bytes()).hexdigest()
    same = now == then
    bad += not same
    print(f'{leg}: {shape} {n_if}if mutation={mutation} variant={variant}: head {now[:16]} leg {then[:16]} '
          f'{"same" if same else "DIFFERENT"}')
print(f'{len(items) - bad} of {len(items)} images the same')
sys.exit(1 if bad else 0)
