#!/usr/bin/env python3
"""Fetch named files from the published evidence tree and check them against its MANIFEST.json.
Usage: fetch_verify_evidence.py <manifest.json> <outdir> <relpath>...  (needs an authenticated gh)."""
import hashlib, json, subprocess, sys
from pathlib import Path
REF = '50e47e55a7cc8b0cb07d30628e493b6fcee6c8cf'
BASE = 'repos/kebag-logic/milan-fpga/contents/review-evidence/665s2c-r1/'
man = {e['file']: e for e in json.load(open(sys.argv[1]))}
out = Path(sys.argv[2])
bad = 0
for rel in sys.argv[3:]:
    data = subprocess.run(['gh', 'api', f'{BASE}{rel}?ref={REF}', '-H', 'Accept: application/vnd.github.raw'],
                          capture_output=True, check=True).stdout
    dst = out / rel; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data)
    got = hashlib.sha256(data).hexdigest(); want = man.get(rel, {}).get('published_sha256')
    ok = got == want; bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {got} {rel}")
sys.exit(1 if bad else 0)
