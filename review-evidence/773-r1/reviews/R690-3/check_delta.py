#!/usr/bin/env python3
"""Check the immutable documentation delta and falsify the prior bad sentence.
Usage: python3 check_delta.py REPO PACKET PR_JSON
"""
from pathlib import Path
from collections import Counter
import json, re, subprocess, sys
repo, packet, prfile = [Path(a).resolve() for a in sys.argv[1:]]
head='e658682ed451ba46885225e5b3fc16841f61a5ca'
prior='1b47a3dcff0cb65cb5cebe1f86327429a76f775d'
page='docs/design/MEDIA_CLOCK_FOLLOWING.md'
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],text=True)
assert git('rev-parse','HEAD').strip()==head
assert git('rev-parse','HEAD^').strip()==prior
assert git('diff','--name-only',prior,head).splitlines()==[page]
assert git('diff','--name-status',prior,head).strip()=='M\t'+page
print('PASS: one documentation commit; only '+page+' changed; every other tree entry unchanged')
text=' '.join((repo/page).read_text().split())
pr=json.loads(prfile.read_text())
assert pr['head']['sha']==head
body=' '.join(pr['body'].split())
excerpt=packet/'public/author-r2/receipts/round2/sweep/excerpts/capture_coherence.txt'
rows=re.findall(r'\[WIRE\] offset (\d+) ns:.*?\[HOLD\].*?max (\d+) ns',excerpt.read_text())
counts=Counter(int(v) for ofs,v in rows if ofs=='2000000')
assert counts==Counter({2059807:9,2059787:14})
assert 'largest 2 ms `[HOLD]` maximum is 2,059,807 ns, in 9 of its 23 runs; the other 14 reach 2,059,787 ns' in text
assert 'largest 2 ms `[HOLD]` maximum 2,059,807 ns in 9 of 23 runs, 2,059,787 ns in the other 14' in body
assert 'its timestamp less the applied offset. That is after the hand-over, which is Equation (1)\'s TT, so it is transit' in text
assert 'Internal cleared-context reviewer: [R689]' in body
assert 'External reviewer: [R690]' in body
print('PASS: both measurement sentences agree with all 23 runs; 20 ns difference is one 50 MHz cycle')
print('PASS: CRF corner names timestamp-minus-applied-offset and post-TT transit; roles name both reviewers')
control=packet/'scratch/prior-sentence'
for name in [page,'docs/reference/MILAN_COMPLIANCE_MATRIX.md']:
 dest=control/name;dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(git('show',prior+':'+name))
result=subprocess.run([sys.executable,str(packet/'check_bounds.py'),str(control),str(excerpt)],capture_output=True,text=True)
(packet/'prior-sentence-control.log').write_text(result.stdout+result.stderr)
(packet/'prior-sentence-control.rc').write_text(str(result.returncode)+'\n')
assert result.returncode==1
assert 'FAIL: doc claims every 2 ms run attains 2059807; only 9 of 23 do' in result.stdout
assert 'PASS: both bound derivations' in result.stdout
print('PASS: unchanged prior check_bounds.py rejects the prior sentence after all numeric checks pass; rc 1 expected')
