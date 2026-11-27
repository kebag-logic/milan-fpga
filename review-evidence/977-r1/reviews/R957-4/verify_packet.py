#!/usr/bin/env python3
"""Verify a downloaded author packet against the published MANIFEST.json, and the ELF identity receipt's pairing.

Usage: python3 -I verify_packet.py MANIFEST.json PACKET_DIR PREFIX
PREFIX is the packet's directory name inside the manifest (e.g. author-r12/). Nothing is written.
"""
import hashlib
import json
import os
import re
import sys

manifest, root, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
entries = [e for e in json.load(open(manifest)) if e['file'].startswith(prefix)]
seen, ok, bad = set(), 0, 0
for e in entries:
    rel = e['file'][len(prefix):]
    seen.add(rel)
    path = os.path.join(root, rel)
    got = hashlib.sha256(open(path, 'rb').read()).hexdigest() if os.path.exists(path) else None
    status = 'OK' if got == e['published_sha256'] else 'MISMATCH'
    ok += status == 'OK'
    bad += status != 'OK'
    redacted = '' if e['original_sha256'] == e['published_sha256'] else ' (published bytes differ from original)'
    print(f'{status} {e["published_sha256"][:16]} {rel}{redacted}')
for d, _, files in os.walk(root):
    for f in files:
        rel = os.path.relpath(os.path.join(d, f), root)
        if rel not in seen:
            print(f'UNLISTED {rel}')
print(f'manifest: {ok} OK, {bad} mismatched, of {len(entries)} entries under {prefix}')

elf = os.path.join(root, 'receipts/elf-identity-3256d1d2.txt')
if os.path.exists(elf):
    secs = re.split(r'^## ', open(elf).read(), flags=re.M)[1:]
    tables = {s.split('\n', 1)[0].strip(): dict((m.group(2), m.group(1)) for m in
              re.finditer(r'^([0-9a-f]{64})\s+(\S+)', s, flags=re.M)) for s in secs}
    hashed = {k: v for k, v in tables.items() if v}
    (a_name, a), (b_name, b) = list(hashed.items())[:2]
    same = set(a) == set(b) and all(a[k] == b[k] for k in a)
    print(f'ELF receipt: {a_name} {len(a)} paths, {b_name} {len(b)} paths, same paths and every sha256 equal: {same}')
