#!/usr/bin/env python3
"""Verify the public packet hashes and unchanged dependencies without executing its banks."""
from pathlib import Path
import hashlib, json, subprocess, sys, re, io, tarfile
P=Path(__file__).resolve().parent
R=Path(sys.argv[1]).resolve()
E=P/'scratch/review-evidence/gptpsw-r1'
REF='86911b961e2f83f3dbe29a5dfc7dd628a5474365'
def git(*args): return subprocess.check_output(['git','-C',str(R),*args]).decode()
if not (E/'MANIFEST.json').exists():
    # The evidence object must be available locally (git fetch origin <REF>).
    data=subprocess.check_output(['git','-C',str(R),'archive',REF,
        'review-evidence/gptpsw-r1/MANIFEST.json','review-evidence/gptpsw-r1/author-r3'])
    (P/'scratch').mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(P/'scratch',filter='data')
rows=json.loads((E/'MANIFEST.json').read_text())
checked=[]
for row in rows:
    if not row['file'].startswith('author-r3/'): continue
    f=E/row['file']; digest=hashlib.sha256(f.read_bytes()).hexdigest()
    assert digest==row['published_sha256'],row['file']
    checked.append({'file':row['file'],'sha256':digest,'redacted':row['path_redacted']})
(P/'verified-evidence.json').write_text(json.dumps(checked,indent=2)+'\n')
print('PUBLIC EVIDENCE COMMIT',REF)
print('PASS published hashes',len(checked),'files')
print('Commit signature status:',git('log','-1','--format=%G?',REF).strip(),'(N means no commit signature; hashes are integrity, not signer authentication)')
import yaml
def nodoc(v):
    if isinstance(v,dict):return {k:nodoc(x) for k,x in v.items() if k!='doc'}
    if isinstance(v,list):return [nodoc(x) for x in v]
    return v
old=yaml.safe_load(git('show','f15b3a7d:sw/mailbox/mailbox.yaml'))
new=yaml.safe_load((R/'sw/mailbox/mailbox.yaml').read_text())
assert nodoc(old)==nodoc(new)
print('PASS contract YAML identical after excluding doc fields')
for rev in ['8121e098','9d753fa0','64a473be','333dc7c5','09c5934a']:
    print('DELTA',rev,'to HEAD:')
    print(git('diff','--name-only',rev+'..HEAD').strip())
selected={
 'gates-8167b70d/xvlog-8167b70d.log':None,
 'gates-8167b70d/SUMMARY.txt':r'xvlog|rc=[^0]',
 'gptp/gptp_mutants-final.log':r'baseline|rate-envelope|RESULT|killed',
 'harness/egress-ledger-8x8-1if.txt':None,
 'harness/cost-8x8-1if.txt':None,
 'harness/cost-8x8.txt':None,
 'publication/tb_cdc_pub-on-f15b3a7d-crossing.log':r'FAIL|failures',
 'publication/tb_cdc_pub-8121e098-crossing.log':r'failures',
 'publication/split-sw-new.checks':None,
 'publication/split-sw-oldcdc.checks':None,
 'closedloop/make-gptp_sw-64a473be.log':r'PASS|RESULT|flood|stamped|offset|checks:',
 'closedloop/gptp_sw_mutants-64a473be.log':r'caught|RESULT|killed',
 'tsu/tsu_mutants-64a473be.log':r'caught|RESULT|killed',
}
for name,pat in selected.items():
    print('\nRECEIPT',name)
    text=(E/'author-r3/receipts'/name).read_text()
    print('\n'.join(l for l in text.splitlines() if pat is None or re.search(pat,l)))
for f in sorted((E/'author-r3/receipts/route').glob('route-*.txt')):
    print('\nROUTE',f.name)
    print('\n'.join(l for l in f.read_text().splitlines() if re.search(r'^# route|WNS|WHS|Block RAM Tile|Slice LUTs|Slice Registers',l)))
for f in sorted((E/'author-r3/receipts/fwgate').glob('shard-*')):
    print('\nFIRMWARE',f.name)
    print('\n'.join(l for l in f.read_text().splitlines() if re.search(r'52 tests|gptp_ubsan|MbxModelGptp|test_ctrl_firmware:|826 of 826',l)))
