#!/usr/bin/env python3
"""Regenerate each capture shape's gPTP ROM with the builder and print its SHA-256.

Usage: gptp_ucode_hash.py <repo-root> <scratch-dir>
Configs are copied into the scratch dir first so the builder writes nothing in
the repository.
"""
import hashlib
import shutil
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/builder'))
import endstation_builder as eb  # noqa: E402

for name in ('endstation_ax7101_8x8', 'endstation_ax7101_1x1_tdm8'):
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    cfg = work / (name + '.yaml')
    shutil.copyfile(root / 'configs' / (name + '.yaml'), cfg)
    result = eb.build(str(cfg), outdir=str(work / 'out'))
    ucode = Path(result['paths']['gptp_ucode']).read_bytes()
    print(name, 'gptp_ucode_sha256', hashlib.sha256(ucode).hexdigest())
