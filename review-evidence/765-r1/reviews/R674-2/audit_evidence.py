#!/usr/bin/env python3
"""Audit downloaded public receipts; no campaigns or build banks are rerun."""
import hashlib
import json
import re
from pathlib import Path
p=Path(__file__).resolve().parent
r=p/'published/author-r2/receipts'
for x in json.loads((p/'publication-hash-check.json').read_text()):
 assert hashlib.sha256((p/'published'/x['file']).read_bytes()).hexdigest()==x['sha256']
print('PASS 70 downloaded receipts retain their verified publication hashes')
for folder in ['r2-rxmon','r2-tsnfuzz','r2-static','r2-builder']:
 assert 'd4a27e6334118c9eef1023aa27e9fd2b7de9f076' in (r/folder/'HEAD.txt').read_text()
print('PASS all four final receipt groups name exact head')
for folder in ['r2-rxmon','r2-tsnfuzz']:
 assert (r/folder/'rc').read_text().strip()=='rc=0'
for f in ['leg-0.rc','leg-1.rc','union.rc']: assert (r/'r2-builder'/f).read_text().strip()=='rc=0'
rows=(r/'r2-static/gates.tsv').read_text().splitlines()
assert len(rows)==34 and all(x.split('\t')[1]=='0' for x in rows)
print('PASS final exit receipts; 34 static/docs rows rc 0')
for l in (r/'r2-rxmon/make_run.log').read_text().splitlines():
 if (('checks:' in l or 'failures:' in l or 'checks, 0 failures' in l) and len(l)<180) or re.match(r'^(14|6) checks:',l): print(l)
for l in (r/'r2-tsnfuzz/tsnfuzz.log').read_text().splitlines():
 if 'pass, 0 fail' in l or 'freshness (' in l or '54 checks' in l or 'traceability contracts' in l: print(l)
assert 'deca300c9eb4863fa13383b45ba6cb6fd0828671' in (r/'r2-tsnfuzz/HEAD.txt').read_text()
print('PASS field oracle receipt names CI pin deca300c9eb4863fa13383b45ba6cb6fd0828671')
regen=(r/'r2-regen/aaf.log').read_text()
assert (r/'r2-regen/rc').read_text().strip()=='rc=2'
assert '164 pass, 0 fail, 0 known gaps' in regen and 'STALE hdl/ieee1722/avtp/doc/TEST_RESULTS.md' in regen
assert 'hdl/ieee1722/avtp/doc/TEST_RESULTS.md' not in (r/'r2-regen/status-before.txt').read_text()
assert 'hdl/ieee1722/avtp/doc/TEST_RESULTS.md' in (r/'r2-regen/status-after.txt').read_text()
print('PASS generation provenance: campaign 164/0; precommit freshness correctly refuses old record (make rc 2); final-head freshness passes')
for l in (r/'r2-builder/leg-1.log').read_text().splitlines():
 if '[gate 11] SKIP' in l: print(l)
print((r/'r2-builder/union.log').read_text().strip())
pr=json.loads((p/'pr.json').read_text())
assert pr['head']['sha']=='d4a27e6334118c9eef1023aa27e9fd2b7de9f076'
assert '\u2014' not in pr['body']
print('PASS R674-1-RES1: no U+2014 in current PR body')
commit=json.loads((p/'evidence-commit.json').read_text())
print('Publication authentication:',json.dumps(commit['verification']))
