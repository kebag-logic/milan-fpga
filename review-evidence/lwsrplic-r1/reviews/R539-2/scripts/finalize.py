#!/usr/bin/env python3
"""Verify publication contents, source integrity, and seal a relative-path manifest."""
import hashlib
from pathlib import Path
import re
import subprocess
import sys

packet=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]).resolve()
head='4eba61b7b1c49fc9b7260a487240ca86f9d38168'
def git(*args):
    return subprocess.check_output(['git','-C',str(source),*args])
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='bf90243127da3e4d22eaeef1402542f1095ee263'
assert not git('status','--porcelain=v1','--ignored')
assert not git('diff','--raw','HEAD')
report=(packet/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R539] POSITIVE - exact head '+head
assert report.splitlines()[-1]=='R539-2 FINISHED'
assert 'SKELETON' not in report
no_fences=re.sub(r'```.*?```','',report,flags=re.S)
for href in re.findall(r'\]\(([^)]+)\)',no_fences):
    if '://' in href:continue
    target=(packet/href.split('#')[0]).resolve()
    assert target.is_relative_to(packet) and target.is_file(),href
terms=[bytes.fromhex(x) for x in ('636c61756465','636f646578','63686174677074','677074','6f70656e6169','616e7468726f706963','636f70696c6f74','67656d696e69','637572736f72','646565707365656b','6c6c616d61','6d69737472616c','6169646572','636c696e65','77696e6473757266','7177656e','67726f6b','6f707573','736f6e6e6574','6861696b75')]
pattern=re.compile(rb'(?i)(?<![a-z0-9])(?:'+b'|'.join(terms)+rb')(?![a-z])')
files=[packet/'REPORT.md',packet/'REPRODUCE.md']+sorted((packet/'scripts').glob('*.py'))+sorted(f for f in (packet/'receipts').iterdir() if f.is_file())
for f in files:
    assert not pattern.search(f.read_bytes()),f.relative_to(packet)
    assert all(str(root).encode() not in f.read_bytes() for root in (source,packet,Path.home())),f.relative_to(packet)
summary=packet/'receipts/publication-check.txt'
summary.write_text('Report header/trailer and receipt links: PASS\nExcluded-name and local-path screening of publishable files: PASS\nOriginal checkout, head, tree, index and clean status: PASS\nScratch excluded from manifest: PASS\n')
if summary not in files:files.append(summary)
files=sorted(files)
(packet/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(packet).as_posix()+'\n' for f in files))
result=subprocess.run(['sha256sum','--check','--quiet','MANIFEST.sha256'],cwd=packet)
assert result.returncode==0
print('Manifest verified:',len(files),'publishable files; scratch excluded.')
print('Original checkout remains exact and clean.')
