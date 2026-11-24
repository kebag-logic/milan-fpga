#!/usr/bin/env python3
"""Verify published receipt hashes without reading other reviewers' reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root, out = map(lambda x: Path(x).resolve(), sys.argv[1:3])
base = out/'scratch/review-evidence/loopbram-r1'
entries = json.loads((out/'scratch/public-manifest.json').read_text())
checked = []
for entry in entries:
    if not entry['file'].startswith(('author-r4/', 'author-r5/')):
        continue
    file = base/entry['file']
    actual = hashlib.sha256(file.read_bytes()).hexdigest()
    assert actual == entry['published_sha256'], entry['file']
    checked.append(dict(file=entry['file'], sha256=actual))
inner = []
published = {e['file']: e for e in entries}
normalized = []
for manifest in sorted((base/'author-r5/receipts').glob('manifest-*.jsonl')):
    for line in manifest.read_text().splitlines():
        entry = json.loads(line)
        data = (manifest.parent/entry['file']).read_bytes()
        outer = published['author-r5/receipts/'+entry['file']]
        assert outer['original_sha256'] == entry['sha256'], entry['file']
        if outer['path_redacted']:
            normalized.append(entry['file'])
        else:
            assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['file']
            assert len(data) == entry['bytes'], entry['file']
        inner.append(entry['file'])
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
prior = 'dc78aedae34c25a97125ecd6816a1f645db5575f'
head = '9acb9b828b29aba71bd51303a4836f86c2278267'
assert git('rev-parse','HEAD') == head
changed = git('diff','--name-only',prior,head).splitlines()
protected = [f for f in changed if f.startswith(('sw/', 'configs/', '.github/')) or (f.startswith('hdl/') and not f.endswith('.md'))]
assert not protected, protected
pins = [line for line in git('ls-tree','-r',head).splitlines() if line.startswith('160000')]
assert pins == [line for line in git('ls-tree','-r',prior).splitlines() if line.startswith('160000')]
result = dict(head=head, tree=git('rev-parse','HEAD^{tree}'), prior=prior, commits=git('rev-list','--count',prior+'..'+head), changed=changed, protected_changes=protected, submodule_gitlinks=pins, verified_published_files=len(checked), verified_inner_receipts=len(inner), public_evidence_commit='0f09f6eeb886aa832b4401026be0d2c91dcdcb29', cryptographic_signature='The published commit has no gpgsig header; verified Git object identity and SHA-256 manifests, not signer authentication.')
(out/'packet-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'publication-normalization.json').write_text(json.dumps(normalized,indent=2)+'\n')
(out/'published-hashes.json').write_text(json.dumps(checked,indent=2)+'\n')
print(json.dumps(result,indent=2))
