"""Verify extracted public author entries against their published manifest hashes."""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
entries = json.loads((root / 'MANIFEST.json').read_text())
checked = 0
for entry in entries:
    if not entry['file'].startswith('author-r') or '/reviews/' in entry['file']:
        continue
    path = (root / entry['file']).resolve()
    assert root in path.parents, entry['file']
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == entry['published_sha256'], (entry['file'], actual)
    checked += 1
print('Author entries verified against published_sha256:', checked)
print('RESULT: PASS (content hashes only; no signer authentication asserted)')
