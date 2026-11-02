#!/usr/bin/env python3
"""Explain SHA256SUMS mismatches of a published evidence directory.

Usage: sums_redaction_check.py MANIFEST.json EVIDENCE_DIR MANIFEST_PREFIX
A SUMS line whose published bytes differ is explained only when MANIFEST
marks that file path_redacted and its original_sha256 equals the SUMS hash.
"""
import hashlib, json, os, sys
man_path, base, prefix = sys.argv[1:4]
man = {e['file']: e for e in json.load(open(man_path))}
bad = unexpl = 0
missing = []
for line in open(os.path.join(base, 'SHA256SUMS')):
    h, p = line.rstrip('\n').split(None, 1)
    p = os.path.normpath(p.lstrip('*'))
    fp = os.path.join(base, p)
    if not os.path.exists(fp):
        missing.append(p)
        continue
    if hashlib.sha256(open(fp, 'rb').read()).hexdigest() != h:
        bad += 1
        e = man.get(prefix + p)
        if not (e and e.get('path_redacted') and e.get('original_sha256') == h):
            unexpl += 1
            print('UNEXPLAINED', p)
print('SUMS lines mismatching published bytes:', bad, 'unexplained:', unexpl,
      'missing files:', missing)
sys.exit(1 if unexpl or missing else 0)
