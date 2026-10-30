#!/usr/bin/env python3
"""Recheck exact source bytes, then hash every publishable packet artifact."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

P=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
record=json.loads((P/'integrity.json').read_text())
def git(*args):
    return subprocess.check_output(['git','-C',str(source),*args]).decode().strip()
assert git('rev-parse','HEAD')==record['head']
assert git('rev-parse','HEAD^{tree}')==record['tree']
assert not git('status','--porcelain=v1')
assert not git('diff','--cached','--name-only','HEAD')
for row in record['tracked']:
    path=source/row['path']
    data=os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==row['oid'],row['path']
    index=git('ls-files','--stage','--',row['path']).split()
    mode='120000' if path.is_symlink() else ('100755' if path.stat().st_mode&0o111 else '100644')
    assert index[0]==mode and index[1]==actual and index[2]=='0',row['path']
assert not [s for s in git('ls-files','--stage').splitlines() if s.startswith('160000 ')]
seal=json.loads((P/'independent-seal.json').read_text())
assert hashlib.sha256((P/'INDEPENDENT.md').read_bytes()).hexdigest()==seal['sha256']
report=(P/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R740] NEGATIVE - exact head '+record['head']
assert report.splitlines()[-1]=='R740-3 FINISHED'
assert 'SKELETON' not in report
assert all('| '+lens+' |' in report for lens in ['Conformance','RTL','Robustness','Tests','Docs'])
final={'head':record['head'],'tree':record['tree'],'tracked_blobs_and_modes':len(record['tracked']),'index_matches_head':True,'gitlinks':[],'source_status':'clean','independent_seal_matches':True,'report_final_line':report.splitlines()[-1]}
(P/'final-integrity.json').write_text(json.dumps(final,indent=2)+'\n')
files=sorted(p for p in P.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(P).parts and p.name!='MANIFEST.sha256')
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(P).as_posix()+'\n' for p in files)
(P/'MANIFEST.sha256').write_text(manifest)
for line in manifest.splitlines():
    digest,name=line.split('  ',1)
    assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest
print('Final source integrity:',len(record['tracked']),'tracked files, exact bytes/modes/index; no gitlinks; clean.')
print('Manifest:',len(files),'publishable files; scratch excluded; all hashes verified.')
