#!/usr/bin/env python3
"""Retrieve selected public receipts and check the publication manifest."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
REV='71b87fde5932bca3b1cde4a7c98ae564bcfe316e'
PREFIX='review-evidence/765-r1/'
def blob(name):
    return subprocess.check_output(['git','-C',str(REPO),'show',REV+':'+PREFIX+name])
manifest=blob('MANIFEST.json')
(ROOT/'published').mkdir(exist_ok=True)
(ROOT/'published/MANIFEST.json').write_bytes(manifest)
groups=['aaf','rxmon','probe','regen','static','tsnfuzz']
selected=[]
for entry in json.loads(manifest):
    name=entry['file']
    if any(name.startswith('author-r3/receipts/r3-'+g+'/') for g in groups) or name in [
        'author-r3/receipts/r3-scripts/probe_flat_cpf256.sh',
        'author-r3/receipts/r3-scripts/regen_aaf.sh',
        'reviews/R673-2/scripts/probe_flat_cpf256.sh']:
        data=blob(name)
        actual=hashlib.sha256(data).hexdigest()
        assert actual==entry['published_sha256'], name
        out=ROOT/'published'/name
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_bytes(data)
        selected.append({'file':name,'sha256':actual,'path_redacted':entry['path_redacted']})
(ROOT/'receipts/public-selection.json').write_text(json.dumps(selected,indent=2)+'\n')
print('Publication:',REV)
print('Selected receipts verified against published_sha256:',len(selected))
print('Declared redacted receipts:',sum(x['path_redacted'] for x in selected))
v=json.loads(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/git/commits/'+REV]))['verification']
(ROOT/'receipts/publication-verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('Public commit signature status:',v['verified'],v['reason'])
print('Manifest signature files:',[x['file'] for x in json.loads(manifest) if x['file'].endswith(('.sig','.asc','.pub'))])
