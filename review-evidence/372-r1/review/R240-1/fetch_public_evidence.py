#!/usr/bin/env python3
"""Download only public manager receipts; do not consult reviewer reports."""
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent / 'public' / 'candidate1'
REF = 'eb06904188529a6004b8a557768b010fd1652101'
BASE = 'review-evidence/372-r1/candidate1'
PATHS = ['candidate.json', 'source-publication.json', 'full-native.json',
         'full-native/complete.json', 'full-native/results.json',
         'full-native/01.log', 'full-native/02.log', 'full-native/03.log',
         'full-native/04.log', 'full-native/05.log',
         'manager-builder-final/complete.json', 'manager-builder-final/results.json',
         'manager-builder/results.json', 'whitespace-correction-decision.json',
         'whitespace-correction/results.json', 'whitespace-correction/01.log',
         'builder-corrected-final-integrity.json', 'native-tree-integrity.json',
         'full-suite-logs/ptp_ts.log']
manifest = []
for name in PATHS:
    api = f'repos/kebag-logic/milan-fpga/contents/{BASE}/{name}?ref={REF}'
    raw = subprocess.check_output(['rtk','proxy','gh','api','-H','Accept: application/vnd.github.raw+json',api])
    path = OUT / name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(raw)
    manifest.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                         url=f'https://github.com/kebag-logic/milan-fpga/blob/{REF}/{BASE}/{name}'))
(OUT/'download-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
