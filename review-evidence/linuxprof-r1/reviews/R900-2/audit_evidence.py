#!/usr/bin/env python3
"""Read-only audit of the published source and evidence. Usage: REPO PACKET."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo, packet = map(Path, sys.argv[1:3])
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
evidence = '7095fc64b8b27f841e7dffaab2be953430487b5e'
head = '66b4def34dcbc0d371ce4eb339d3d0226875befa'
prior = '677d605f37c3a80654df1dd2cde053b57242845b'
base = '854bd7236792ce1adbd10c43b13a6a5002ad3bb6'
prefix = 'review-evidence/linuxprof-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def blob(path):
    return git('show', evidence + ':' + prefix + path)
manifest = json.loads(blob('MANIFEST.json'))
rows = []
for item in manifest:
    if not item['file'].startswith(('author/', 'author-r2/')):
        continue
    data = blob(item['file'])
    actual = hashlib.sha256(data).hexdigest()
    assert actual == item['published_sha256'], item['file']
    rows.append({'file': item['file'], 'sha256': actual, 'path_redacted': item['path_redacted']})
    if item['file'].startswith('author-r2/receipts/'):
        dest = packet / 'scratch' / 'published' / item['file']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
captures = [json.loads(blob('author-r2/receipts/identity-' + rev[:8] + '.json')) for rev in (base, prior, head)]
assert all(len(c) == 245 for c in captures)
assert captures[0] == captures[1] == captures[2]
assert all(blob('author-r2/receipts/identity-' + rev[:8] + '.rc').strip() == b'0' for rev in (base, prior, head))
docs = blob('author-r2/receipts/docs-gates.log').decode()
commands = [line for line in docs.splitlines() if line.startswith('== rc=')]
assert len(commands) == 24 and all(line.startswith('== rc=0 ') for line in commands)
for name in ('gates-32-41-42', 'gate-bad-configs', 'discriminate', 'host-image'):
    assert blob('author-r2/receipts/' + name + '.rc').strip() == b'0'
delta = git('diff', '--no-ext-diff', '--no-textconv', base + '..' + head)
packet.joinpath('source.diff').write_bytes(delta)
delta2 = git('diff', '--no-ext-diff', '--no-textconv', prior + '..' + head)
packet.joinpath('delta.diff').write_bytes(delta2)
raw_commit = git('cat-file', 'commit', evidence)
verify = subprocess.run(['git', '-C', str(repo), 'verify-commit', evidence], capture_output=True)
result = dict(evidence_commit=evidence, source_head=head, source_tree=git('rev-parse', head+'^{tree}').decode().strip(),
              verified_files=rows, identity_count=245, identity_equal_across=[base, prior, head],
              docs_commands=commands, diff_sha256=hashlib.sha256(delta).hexdigest(),
              delta_sha256=hashlib.sha256(delta2).hexdigest(),
              evidence_signature=dict(gpgsig_present=b'\ngpgsig ' in raw_commit,
                                      verify_commit_rc=verify.returncode,
                                      verification_output=(verify.stdout + verify.stderr).decode()),
              signature_limit='The published evidence commit is unsigned; hashes verify integrity, not a signer identity.')
packet.joinpath('evidence-audit.json').write_text(json.dumps(result, indent=2)+'\n')
print('Published author files verified:', len(rows))
print('Identity: 245/245 equal at base, prior and head; recorded rc=0 for each capture')
print('Docs: 24/24 recorded rc=0; four focused receipt statuses rc=0')
print('Signature: evidence commit has no gpgsig; verify-commit rc=' + str(verify.returncode))
