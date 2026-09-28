"""Publish the authorized final issue comment only after the candidate audit."""
from pathlib import Path
import hashlib
import json
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/602-phc-step-mr')
HEAD = '6b2ebd1c435136966f84ffc16d28a80c7d6b9387'
assert not (OUT/'publication.json').exists(), 'Final comment already published'
audit = json.loads((OUT/'final-audit.json').read_text())
assert audit['head'] == HEAD and audit['clean'] and audit['pr_body_format_valid']
assert audit['read_only_inputs_verified'] == 15
assert json.loads((OUT/'candidate-audit.json').read_text())['rc'] == 0
head = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert head == HEAD
assert not subprocess.check_output(['rtk', 'proxy', 'git', 'status', '--porcelain'], cwd=ROOT)
body = (OUT/'REVIEW-READY.md').read_bytes()
assert body.startswith(b'[A397] REVIEW READY\n') and HEAD.encode() in body
assert all(p.stat().st_size <= 200000 for p in OUT.rglob('*') if p.is_file())
result = subprocess.run(['rtk', 'proxy', 'gh', 'issue', 'comment', '602', '--repo',
                         'kebag-logic/milan-fpga', '--body-file', str(OUT/'REVIEW-READY.md')],
                        cwd=ROOT, text=True, capture_output=True, check=True, timeout=120)
url = result.stdout.strip()
assert url.startswith('https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-'), url
record = {'head':HEAD, 'url':url, 'body_sha256':hashlib.sha256(body).hexdigest(),
          'kind':'new REVIEW READY comment', 'rc':result.returncode}
(OUT/'publication.json').write_text(json.dumps(record,indent=2)+'\n')
with (OUT/'HANDOFF.md').open('a') as f:
    f.write('\nThe final [A397] REVIEW READY comment was published: '+url+'\n')
manifest = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name != 'MANIFEST.sha256':
        manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name)
(OUT/'MANIFEST.sha256').write_text('\n'.join(manifest)+'\n')
print(json.dumps(record,indent=2))
