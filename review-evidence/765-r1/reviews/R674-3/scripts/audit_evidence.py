#!/usr/bin/env python3
"""Check the included public execution receipts without rerunning their banks."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
HEAD='87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d'
BASE='d4a27e6334118c9eef1023aa27e9fd2b7de9f076'
P=ROOT/'published/author-r3/receipts'
for row in json.loads((ROOT/'receipts/public-selection.json').read_text()):
    assert hashlib.sha256((ROOT/'published'/row['file']).read_bytes()).hexdigest()==row['sha256'],row['file']
print('Selected receipt hashes: PASS (72 files)')
for group in ['r3-aaf','r3-rxmon','r3-probe','r3-tsnfuzz','r3-static']:
    assert HEAD in (P/group/'HEAD.txt').read_text(),group
    if group!='r3-static': assert (P/group/'rc').read_text().strip()=='rc=0',group
    print(group,'exact head',HEAD,'PASS')
gates=(P/'r3-static/gates.tsv').read_text().splitlines()
assert len(gates)==36
assert all(line.split('\t')[1]=='0' for line in gates)
print('Static/docs gates:',len(gates),'rc 0')
aaf=(P/'r3-aaf/aaf.log').read_text()
assert '164 pass, 0 fail, 0 known gaps' in aaf and 'freshness' in aaf and '1 PASS, 0 FAIL' in aaf
assert 'SUITE-SKIP' not in aaf
rx=(P/'r3-rxmon/make_run.log').read_text()
for count in [97,147]: assert f'{count} checks, 0 failures' in rx, count
for n,count in [(1,116),(8,119)]: assert f'lockstep N={n}: checks: {count}   failures: 0' in rx
for count in [14,6]: assert f'{count} checks: {count} PASS, 0 FAIL' in rx
print('Executed avtp_rxmon: flat 97/0; NX 147/0; lockstep 116/0,119/0; mutant controls 14/14,6/6')
tsn=(P/'r3-tsnfuzz/tsnfuzz.log').read_text()
for text in ['164 pass, 0 fail','677 pass, 0 fail','54 checks: 54 PASS, 0 FAIL','2 checks: 2 PASS, 0 FAIL']: assert text in tsn,text
assert 'deca300c9eb4863fa13383b45ba6cb6fd0828671' in (P/'r3-aaf/HEAD.txt').read_text()
print('Executed campaigns at pinned oracle: AAF 164/0; gPTP 677/0; grader 54/0; traceability 2/0')
regen=P/'r3-regen'
assert BASE in (regen/'HEAD.txt').read_text() and 'uncommitted' in (regen/'HEAD.txt').read_text()
assert (regen/'rc').read_text().strip()=='rc=2'
assert '164 pass, 0 fail, 0 known gaps' in (regen/'aaf.log').read_text()
artifact='hdl/ieee1722/avtp/doc/TEST_RESULTS.md'
assert artifact not in (regen/'status-before.txt').read_text()
assert artifact in (regen/'status-after.txt').read_text()
diff=subprocess.check_output(['git','-C',str(repo),'diff',BASE,HEAD,'--',artifact],text=True)
assert diff==(regen/'TEST_RESULTS.diff').read_text()
print('Regeneration: old-head-plus-edits 164/0; initial freshness refusal rc 2; emitted diff equals committed diff exactly')
probe=(P/'r3-probe/probe_flat_cpf256.log').read_text()
for line in ['PROBE cpf=256: frames_rx=3 unsupported=2','PROBE cpf=257: frames_rx=4 unsupported=2']: assert line in probe
assert (ROOT/'scripts/probe_flat_cpf256.sh').read_bytes()==(P/'r3-scripts/probe_flat_cpf256.sh').read_bytes()
print('Author and reviewer probe scripts byte-identical; published 256/257 observations match')
pr=(ROOT/'receipts/pr769-body.md').read_text()
assert pr.count('\u2014')==0
limitations=pr.split('## Known limitations / out of scope')[1].split('## Definition of Done')[0]
assert 'low eight bits' in limitations and '256, 512 or 768' in limitations
assert "rejects a count other than its current format's" in limitations
print('Current PR limitations: low-eight-bit read and current-format-relative rejection; prior em-dash residue resolved')
print('PASS: source-head published receipts and generation provenance; no manager bank inferred')
