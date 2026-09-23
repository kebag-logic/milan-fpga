#!/usr/bin/env python3
"""Reconcile the original readiness bundle's nested SHA256SUMS refusals
against the outer immutable manifest and the published reconciliation file.
Usage: reconcile_readiness.py <517-r1 dir at b9a05dc9> <523-r1 reconciliation json>"""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); rec = json.load(open(sys.argv[2]))
outer = [e for e in json.load(open(root / 'MANIFEST.json')) if '523-readiness/' in e['file']]
outer = {e['file'].split('523-readiness/', 1)[1]: e for e in outer}
base = root / 'followups/523-readiness'
nested = {}
for line in open(base / 'SHA256SUMS'):
    h, name = line.rstrip('\n').split(None, 1); nested[name.lstrip('*')] = h
ok = True; refused = []
for r in rec['files']:
    f = r['file']; pub = hashlib.sha256((base / f).read_bytes()).hexdigest(); o = outer.get(f)
    checks = dict(published_bytes_match_record=pub == r['published_sha256'],
                  outer_original=o is not None and o['original_sha256'] == r['original_sha256'],
                  outer_published=o is not None and o['published_sha256'] == pub,
                  outer_redacted_flag=o is not None and o['path_redacted'] == r['path_redacted'])
    if f == 'SHA256SUMS':
        checks['not_self_listed'] = f not in nested
    else:
        checks['nested_is_original'] = nested.get(f) == r['original_sha256']
        checks['nested_refuses_iff_redacted'] = (nested.get(f) != pub) == r['path_redacted']
        if nested.get(f) != pub: refused.append(f)
    good = all(checks.values()); ok &= good
    print(f"{f:45s} {'OK ' if good else 'BAD'} {checks}")
print('outer entries:', len(outer), 'reconciled rows:', len(rec['files']))
print('nested refusals (%d):' % len(refused), refused)
verdict = ok and len(refused) == 6 and len(outer) == 22 == len(rec['files'])
print('RECONCILIATION', 'PASS' if verdict else 'FAIL')
sys.exit(0 if verdict else 1)
