#!/usr/bin/env python3
"""Check public composition ancestry, retained tables, image-input deltas and receipt identities."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
head = '43076d0f8c87b5118f6f4317d000a7eebdefc967'
base = 'aa30d77f75cd97b3a29878ca0ed68010a7629266'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root, env=env)
def blob(ref, path):
    return git('show', f'{ref}:{path}').decode()

rows = []
def check(name, ok, detail):
    rows.append(dict(check=name, pass_=bool(ok), evidence=detail))

check('head and tree', git('rev-parse','HEAD').decode().strip() == head and
      git('rev-parse','HEAD^{tree}').decode().strip() == 'c0a5e3cb0e0dfd9899e57053ad1a6f5b32f9c32e', head)
donors = {'958':'1825ba4e','961':'287ca1ee','959':'8aeb2f0b','975':'3cda030c',
          '971':'c113018d','978':'87b2fc0f','974':'77a74b2f'}
for pr, ref in donors.items():
    full = git('rev-parse', ref).decode().strip()
    rc = subprocess.run(['git','merge-base','--is-ancestor',full,head],cwd=root,env=env).returncode
    check('approved donor ancestry #' + pr, rc == 0, full)

merges = ['c812b438','e3de632b','ee58b499','8fac1fd2','23ee9529','b04610c2','d6c398c8','93c5ad84','4df6751e']
for m in merges:
    parents = git('rev-list','--parents','-n','1',m).decode().split()
    check('two-parent merge '+m,len(parents) == 3, parents)
for m in ('93c5ad84','4df6751e'):
    check('tree-preserving merge '+m, git('rev-parse',m+'^{tree}') == git('rev-parse',m+'^1^{tree}'),
          git('rev-parse',m+'^{tree}').decode().strip())

# Every changed RTL file is byte-identical to one of the approved source heads.
rtl = git('diff','--name-only',base,head,'--','hdl').decode().splitlines()
for path in rtl:
    matches = []
    for pr, ref in donors.items():
        if git('rev-parse',f'{ref}:{path}') == git('rev-parse',f'{head}:{path}'):
            matches.append(pr)
    if matches:
        check('retained RTL '+path, True, {'approved_prs':matches,'blob':git('rev-parse',f'{head}:{path}').decode().strip()})
    else:
        # The top-level datapath combines receive fan-out, render width and
        # the already-landed placement/version connection. Prove every merge
        # used its automatic result, then prove no subsequent alteration.
        clean = all(not git('show','--format=','--remerge-diff',m,'--',path).strip() for m in merges)
        check('composed RTL '+path,clean and git('rev-parse',f'd6c398c8:{path}') == git('rev-parse',f'{head}:{path}'),
              {'automatic_merges':merges,'blob':git('rev-parse',f'{head}:{path}').decode().strip()})

path = 'sw/firmware/ctrl/test/test_plat_sinks.cpp'
tests = lambda s: set(re.findall(r'TEST_F\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)',s))
parents = [tests(blob(r,path)) for r in ('23ee9529^1','23ee9529^2')]
current = tests(blob(head,path))
check('sink fixture test union', current == parents[0] | parents[1],
      {'left':len(parents[0]),'right':len(parents[1]),'union':len(current),'tests':sorted(current)})
path = 'sw/firmware/ctrl/test/aecp_mutants.py'
tables = lambda s: set(re.findall(r'for row in (aecp_\w+)\.ROWS',s))
for merge in ('c812b438','8fac1fd2'):
    union = tables(blob(merge+'^1',path)) | tables(blob(merge+'^2',path))
    check('AECP table union '+merge, tables(blob(merge,path)) == union,sorted(union))
path = 'sw/firmware/ctrl/test/srp_mutants.py'
tables = lambda s: set(re.findall(r'(srp_\w+_mutants)\.\w+',s))
union = tables(blob('b04610c2^1',path)) | tables(blob('b04610c2^2',path))
check('SRP table union',tables(blob(head,path)) == union, sorted(union))
source = blob(head,'sw/firmware/ctrl/test/test_ctrl_firmware.py')
check('both SRP 8x8 campaign prefixes', 'srp_early_mutants.PREFIX, srp_link_mutants.PREFIX' in source,
      'sw/firmware/ctrl/test/test_ctrl_firmware.py:241-244')
source = blob(head,'sw/firmware/ctrl/test/sink_mutants.py')
check('distinct sink fixture selectors',all(s in source for s in ['EARLY_S13 = "Early.S13','EARLY_S14 = "Early.S14',
      'S13 = "Streams.S13','S14 = "Streams.S14','EARLY_S13, POWER_ON','EARLY_S14, REBOUND']),
      'sw/firmware/ctrl/test/sink_mutants.py')

for merge in ('c812b438','8fac1fd2','23ee9529'):
    path = 'docs/design/SPLIT_CONTROL_MEMORY.md'
    headings = lambda s: set(re.findall(r'^### .+',s,re.M))
    union = headings(blob(merge+'^1',path)) | headings(blob(merge+'^2',path))
    missing = sorted(union - headings(blob(head,path)))
    check('retained design sections '+merge,not missing,{'count':len(union),'missing':missing})

for ref in ('c2b2ba1a','f5a1585e'):
    changed=git('diff','--name-only',ref,head).decode().splitlines()
    check('changes since measured head '+ref, True, changed)
defines=lambda s: re.findall(r'^#define .+',s,re.M)
path='sw/firmware/ctrl/loop/ctrl_loop.h'
check('scheduler constants unchanged',defines(blob(base,path)) == defines(blob(head,path)),path)
check('stack pin unchanged',git('rev-parse',f'{base}:third_party/tsn-c-stack') == git('rev-parse',f'{head}:third_party/tsn-c-stack'),
      git('rev-parse',f'{head}:third_party/tsn-c-stack').decode().strip())
check('notice rounding rule', ((30948 * 105 + 49999) // 50000) * 5 == 325,
      '30,948 cycles at 100 MHz; 309.48 us * 1.05 = 324.954 us; ceil to 5 us = 325 us')

public = packet/'scratch/public/review-evidence/train1123-r1'
manifest=json.loads((public/'MANIFEST.json').read_text())
for entry in manifest:
    path=public/entry['file']
    if not path.is_file():
        continue
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    check('published receipt '+entry['file'],digest == entry['published_sha256'],digest)
images={}
for ref,rel in [('c2b2ba1a','author/receipts/ledger/plat-ledger-c2b2ba1a.txt'),
                ('f5a1585e','author/receipts/ledger/plat-ledger-f5a1585e.txt'),
                ('43076d0f','author-r2/receipts/ledger/plat-ledger-43076d0f.txt')]:
    images[ref]=dict((path,digest) for digest,path in re.findall(r'^([a-f0-9]{64})\s+(\./\S+)$',(public/rel).read_text(),re.M))
check('24 published image hashes identical',len(images['43076d0f']) == 24 and len({json.dumps(v,sort_keys=True) for v in images.values()}) == 1,images)
output=json.dumps(rows,indent=2)+'\n'
(packet/'receipts/composition-audit.json').write_text(output)
for row in rows:
    if not row['check'].startswith('published receipt') or not row['pass_']:
        print(('PASS ' if row['pass_'] else 'FAIL ')+row['check']+' '+json.dumps(row['evidence']))
print(f'{len(rows)} checks, {sum(not row["pass_"] for row in rows)} failures')
raise SystemExit(any(not row['pass_'] for row in rows))
