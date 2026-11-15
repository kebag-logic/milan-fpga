#!/usr/bin/env python3
"""Hash every entry of an evidence MANIFEST.json under a prefix against the extracted files.
usage: python3 -I verify_manifest.py EVIDENCE_ROOT PREFIX"""
import hashlib, json, os, sys
root, prefix = sys.argv[1], sys.argv[2]
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
entries = [e for e in m if e['file'].startswith(prefix)]
missing = [e['file'] for e in entries if not os.path.exists(os.path.join(root, e['file']))]
bad = [e['file'] for e in entries if e['file'] not in missing and
       hashlib.sha256(open(os.path.join(root, e['file']), 'rb').read()).hexdigest() != e['published_sha256']]
disk = [os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(os.path.join(root, prefix)) for f in fs]
unlisted = sorted(set(disk) - {e['file'] for e in entries})
print(f'{prefix}: {len(entries)} entries, {len(entries) - len(missing)} present, {len(bad)} mismatched, '
      f'{len(missing)} missing, {len(unlisted)} unlisted')
for f in bad + missing + unlisted:
    print(' ', f)
sys.exit(1 if bad or missing or unlisted else 0)
