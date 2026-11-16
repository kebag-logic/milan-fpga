#!/usr/bin/env python3
"""Read published receipt blobs at the immutable archive; verify their published hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
args=ap.parse_args()
archive='aedb770f03cab800b4623c0c13fde672ce26f670'
prefix='review-evidence/925-r1/'
def read(path):
    return subprocess.check_output(['git','-C',str(args.repo),'show',archive+':'+prefix+path])
manifest=json.loads(read('MANIFEST.json'))
receipts=[row for row in manifest if '/receipts/' in row['file']]
bad=[row['file'] for row in receipts if hashlib.sha256(read(row['file'])).hexdigest()!=row['published_sha256']]
print(json.dumps({'archive':archive,'receipt_files_checked':len(receipts),'mismatches':bad},indent=2))
raise SystemExit(bool(bad))
