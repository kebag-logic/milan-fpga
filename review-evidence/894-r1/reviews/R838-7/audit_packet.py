#!/usr/bin/env python3
"""Verify the published archive's hashes and image-carry tables.
Usage: python3 audit_packet.py EXTRACTED_REVIEW_EVIDENCE_894_R1
"""
import hashlib
import json
import pathlib
import re
import sys

base = pathlib.Path(sys.argv[1])
errors = []
counts = {}
manifest = {row['file']: row for row in json.loads((base/'MANIFEST.json').read_text())}
for row in manifest.values():
    path = row['file']
    if not path.startswith(('author-r12/', 'author-r13/')):
        continue
    p = base/path
    actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'ABSENT'
    if actual != row['published_sha256']:
        errors.append(('manifest', path, actual, row['published_sha256']))
    part = path.split('/')[0]
    counts[part] = counts.get(part, 0)+1
print('Published manifest entries checked:', counts)
for part in counts:
    n = 0
    for path, size, sha in re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([a-f0-9]{64})` \|$', (base/part/'INDEX.md').read_text(), re.M):
        p = base/part/path
        data = p.read_bytes()
        n += 1
        if len(data) != int(size.replace(',', '')) or hashlib.sha256(data).hexdigest() != sha:
            entry = manifest.get(part+'/'+path, {})
            if entry.get('path_redacted') and entry.get('original_sha256') == sha:
                print('INDEX ORIGINAL HASH mapped by archive redaction manifest:', part+'/'+path)
            else:
                errors.append(('index', part, path, len(data), hashlib.sha256(data).hexdigest()))
    print(part, 'index rows checked:', n)
images = base/'author-r13/receipts/images'
def hashes(path):
    return {parts[1]: parts[0] for line in path.read_text().splitlines() if len(parts := line.split()) == 2}
old = hashes(images/'image-sha256-30a01422.txt')
new = hashes(images/'image-sha256-c274b9f5.txt')
two = [p for p in new if '2if/' in p]
same = [p for p in two if new[p] == old.get(p)]
print('Two-interface image inputs identical:', len(same), '/', len(two))
if len(same) != len(two):
    errors.append(('image mismatch', sorted(set(two)-set(same))))
one_diff = [p for p in new if '1if/' in p and new[p] != old.get(p)]
print('One-interface changed artifacts:', one_diff)
legs = [v for line in (images/'harness-elf-sha256.txt').read_text().splitlines()
        if (v := line.split()) and v[0] in {'H-B8F', 'H-L8L', 'H-L8A', 'H-L8N', 'H-L8O', 'H-J8'}]
print('Two-interface harness ELFs identical:', sum(v[1] == v[2] for v in legs), '/', len(legs))
assert len(legs) == 6 and all(v[1] == v[2] for v in legs)
for e in errors:
    print('MISMATCH', *e)
print('RESULT:', 'FAIL' if errors else 'PASS')
sys.exit(bool(errors))
