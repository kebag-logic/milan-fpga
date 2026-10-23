#!/usr/bin/env python3
"""Fetch selected public evidence; verify each file against its published hash."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
BASE = 'https://raw.githubusercontent.com/kebag-logic/milan-fpga/0ca01426bbafc52fce122363488d535e4a131b0c/review-evidence/632-r1/'

def fetch(entry):
    name = entry['file']
    dest = ROOT / 'scratch/public' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = dest.read_bytes() if dest.exists() else urllib.request.urlopen(BASE + name, timeout=90).read()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry['published_sha256'], name
    dest.write_bytes(data)
    return dict(file=name, sha256=digest, bytes=len(data), verified=True)

def main():
    manifest_path = ROOT / 'scratch/public-manifest.json'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    if not manifest_path.exists():
        manifest_path.write_bytes(urllib.request.urlopen(BASE + 'MANIFEST.json', timeout=90).read())
    manifest = json.loads(manifest_path.read_text())
    selected = []
    for e in manifest:
        p = e['file']
        if p in ('author-r7/receipts/INDEX.md', 'author-r7/PR-BODY.md', 'author-r7/HANDOFF.md'):
            selected.append(e)
        elif p.startswith('author-r7/receipts/round7/'):
            # Older stopped campaigns are retained in the publication, not positive evidence.
            if any(s in p for s in ['_dc9cda7d/', '_5282b8b6/', 'gmstep_mutants_d835ba12/', 'gmstep_stop_probe_d835ba12/']):
                if not any(s in p for s in ['notify_dc9cda7d/', 'gsi_mutants_dc9cda7d/', 'merge_dc9cda7d/']):
                    continue
            selected.append(e)
        elif p.startswith('author-r7/scripts/round7/'):
            selected.append(e)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(fetch, selected))
    (ROOT / 'public-evidence-verification.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Verified {len(results)} published files, {sum(r["bytes"] for r in results)} bytes; no hash mismatch.')

if __name__ == '__main__':
    main()
