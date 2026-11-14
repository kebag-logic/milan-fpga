#!/usr/bin/env python3
"""Read-only source, public-receipt and model audit. Run from the exact candidate clone."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import struct
import subprocess
import sys

HEAD = '5b264bf26416108add32d7fe5abca5252ffde2cb'
TREE = '2d2fa3312e4bf54ac42f71af967c83711a45bc36'
ARCHIVE = 'fa3f0a8cdcf3cb801cb2d97977b6df00585621ac'
PACKET = Path(__file__).resolve().parent
ROOT = Path.cwd()

def git(*args, cwd=ROOT, data=None):
    return subprocess.check_output(['git', *args], cwd=cwd, input=data)

def identity():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    for repo in [ROOT, *[ROOT/p for p in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
                                         'third_party/tsn-c-stack', 'third_party/lwSRP')]]:
        index = git('write-tree', cwd=repo).strip()
        tree = git('rev-parse', 'HEAD^{tree}', cwd=repo).strip()
        assert index == tree
        blobs = 0
        links = []
        for raw in git('ls-tree', '-rz', 'HEAD', cwd=repo).split(b'\0'):
            if not raw:
                continue
            meta, path = raw.split(b'\t', 1)
            mode, kind, oid = meta.split()
            file = repo/os.fsdecode(path)
            if kind == b'commit':
                links.append((os.fsdecode(path), oid.decode()))
                if (file/'.git').exists():
                    assert git('rev-parse', 'HEAD', cwd=file).strip() == oid
                continue
            content = os.fsencode(os.readlink(file)) if mode == b'120000' else file.read_bytes()
            actual = hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
            assert actual == oid.decode(), str(file)
            if mode in (b'100644', b'100755'):
                assert bool(file.stat().st_mode & 0o111) == (mode == b'100755'), str(file)
            blobs += 1
        print('IDENTITY', str(repo.relative_to(ROOT)) or '.', 'index and tracked blob bytes/modes PASS', blobs)
        for path, oid in links:
            print('GITLINK', path, oid)
    print('HEAD', HEAD, 'TREE', TREE)

def archive():
    prefix = 'review-evidence/894-r1/'
    manifest = json.loads(git('show', ARCHIVE+':'+prefix+'MANIFEST.json'))
    records = [r for r in manifest if r['file'].startswith('author-r9/')]
    base = PACKET/'scratch'/'archive'
    for r in records:
        data = git('show', ARCHIVE+':'+prefix+r['file'])
        assert hashlib.sha256(data).hexdigest() == r['published_sha256']
        dest = base/r['file']; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
    print('ARCHIVE', ARCHIVE, len(records), 'published SHA-256 values verified;',
          sum(r['path_redacted'] for r in records), 'redacted files')
    signed = b'gpgsig ' in git('cat-file', 'commit', ARCHIVE).split(b'\n\n')[0]
    print('Cryptographic signature present:', signed, '(manifest integrity is not signer authentication)')
    src = base/'author-r9'
    index = (src/'INDEX.md').read_text()
    absent, mismatched = [], []
    for name, digest in re.findall(r'\| `([^`]+)` \| [\d,]+ \| `([a-f0-9]{64})` \|', index):
        p = src/name
        if not p.exists(): absent.append(name)
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest: mismatched.append(name)
    print('INDEX absent:', absent, 'different from published bytes:', mismatched)
    wf = (src/'receipts/gates/workflows-verify.md').read_text()
    rows = [line.split('|')[1:-1] for line in wf.splitlines() if line.startswith('| ')][1:]
    counts = {}
    for row in rows:
        status = row[4].strip(); counts[status] = counts.get(status, 0)+1
    print('Local workflow receipt statuses:', counts)
    suites = checks = 0
    for k in range(4):
        text = (src/f'receipts/gates/sweep-shard{k}.txt').read_text()
        n,p,f,t = map(int, re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)',text).groups())
        c,fail = map(int, re.search(r'checks: (\d+)\s+in-suite failures: (\d+)', text).groups())
        assert n == p and f == t == fail == 0 and HEAD in text
        suites += n; checks += c
    print('SWEEP', suites, 'suites;', checks, 'checks; no failures')
    text = (src/'receipts/gates/harness-head-builds.txt').read_text()
    totals = [0,0,0]; lo,hi = math.inf,0; runs=0
    for block in re.split(r'^== ', text, flags=re.M)[1:]:
        label = block.splitlines()[0]
        m = re.search(r'JOINS .*?: (\d+) join interval\(s\), the shortest ([\d.]+) ms and the longest ([\d.]+) ms.*run-outs: (\d+) released, (\d+) empty',block)
        if not m: continue
        n,low,high,released,empty = m.groups()
        totals = [totals[0]+int(n), totals[1]+int(released), totals[2]+int(empty)]
        lo=min(lo,float(low)); hi=max(hi,float(high));runs+=1
        assert 181<=float(low)<=float(high)<=239 and HEAD in block
        print('JOINS', label, n, low, high, 'released', released, 'empty', empty)
    print('JOIN TOTAL',runs,'runs;', totals, 'intervals/released/empty; range',lo,hi,
          '; unplanted intervals',totals[0]-3)
    for cycles in (91625,98720,156716,2551):
        print('COST', cycles, 'cycles at 100 MHz =>',math.ceil(cycles/100*1.05/5)*5,'us with padding')
    text=(src/'receipts/images/rom-layout-f3.txt').read_text()
    images={}
    for tag,name,code,pad,ro,rom in re.findall(r'(r8-start|r8-head|r9-head) ([^:]+): .text (\d+), pad (\d+), .rodata (\d+), rom (\d+)',text):
        images[tag,name]=tuple(map(int,(code,pad,ro,rom)))
    for name in [n for t,n in images if t=='r8-start']:
        first,second,last = (images[t,name] for t in ('r8-start','r8-head','r9-head'))
        print('IMAGE',name,'round8 text/pad/rom deltas',second[0]-first[0],second[1]-first[1],second[3]-first[3],
              'round9 rom delta',last[3]-second[3])

def model():
    sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
    import rows_tiers as rt
    import paced_rows as pr
    import join_grade
    i=rt.point_inputs(ROOT,'1x1/1if')
    print('MODEL paced bound',pr.PACED_BOUNDS,'chosen pace',pr.choice(ROOT))
    for p in range(1,14):
        at=i._replace(pace_ms=p)
        print('PACE',p,'txL',rt.solve('txL',at,rt.BUILT)[0],'R4L',rt.solve('R4L',at,rt.BUILT)[0])
    print('Statements',pr.statements(ROOT))
    for p in (7,8,9):
        old=rt.LONG_RECORD_US['1x1/1if'];rt.LONG_RECORD_US['1x1/1if']=1040
        at=rt.point_inputs(ROOT,'1x1/1if')._replace(pace_ms=p)
        print('COUNTERFACTUAL current AMAP 30, record 1040, pace',p,'txL',rt.solve('txL',at,rt.BUILT)[0])
        rt.LONG_RECORD_US['1x1/1if']=old

def definition():
    path='sw/firmware/ctrl/test/test_aecp.cpp'
    values=[]
    for rev in ('dd01b0af','HEAD'):
        text=git('show',rev+':'+path).decode()
        start=text.index('TEST_F(Core, MapEditsAreTheirDefinitionRowForRow)')
        end=text.index('\n}\n',start)+3
        digest=hashlib.sha256(text[start:end].encode()).hexdigest();values.append(digest)
        print('DEFINITION body',rev,digest)
    assert values[0] == values[1]
    diff=git('diff','--no-ext-diff','--no-textconv','dd01b0af..HEAD').decode()
    path='';hits=[]
    for line in diff.splitlines():
        if line.startswith('+++ b/'):path=line[6:]
        elif line.startswith('+') and not line.startswith('+++') and not path.endswith('.md'):
            if re.search(r'issuecomment-\d+|\bR83[78](?:-\d+)?\b|\bround[ -]+\d+|\bB\d{2}\b',line,re.I):hits.append((path,line))
    print('NEW source comment prohibited-label scan:',hits)

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--identity-only',action='store_true');args=parser.parse_args()
    if args.identity_only: identity()
    else: archive();definition();model()
