#!/usr/bin/env python3
"""Reviewer probe: derive fixture media from TREE's generators and compare with its oracle.json.
usage: derive_media.py TREE"""
import json, sys, tempfile
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/fw_service_budget'))
import run
for receipt in json.loads((tree / 'tb/verilator/fw_service_budget/oracle.json').read_text()):
    with tempfile.TemporaryDirectory(prefix='r566-media-') as d:
        m = run.oracle_media(Path(d), receipt['shape'], receipt['media'])
    print(json.dumps(dict(shape=m['shape'], plan=m['plan'], image_bytes=m['image_bytes'], records=m['records'],
                          aem_bytes=m['aem_bytes'], slots_match=m['slots_sha256'] == receipt['media']['slots_sha256'])))
