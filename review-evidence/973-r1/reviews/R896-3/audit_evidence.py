#!/usr/bin/env python3
"""Verify the published manifest and selected receipts without running broad banks."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = [Path(x).resolve() for x in sys.argv[1:3]]
ref = 'bf7e243062cfee72687b6b0374f70be88982171a'
prefix = 'review-evidence/973-r1/'
def blob(path):
    return subprocess.check_output(['git', '-C', str(root), 'show', ref + ':' + prefix + path])
manifest = json.loads(blob('MANIFEST.json'))
bad = []
for row in manifest:
    data = blob(row['file'])
    if hashlib.sha256(data).hexdigest() != row['published_sha256']:
        bad.append(row['file'])
    elif row['file'].startswith('author-r3/'):
        target = packet/'scratch/evidence'/row['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
assert not bad, bad
print(f'Published manifest: {len(manifest)}/{len(manifest)} SHA-256 values match')
ev = packet/'scratch/evidence/author-r3/receipts'
dest = packet/'published-receipts'
dest.mkdir(exist_ok=True)
def keep(rel):
    target = dest/rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ev/rel, target)
for rel in ['change/head.txt', 'checks/size-variants.txt', 'gates/r3-bnd.txt', 'gates/r3-bnd.rc',
            'gates/r3-twin.txt', 'gates/r3-cov.txt', 'gates/r3-boot.txt', 'gates/docs-steps.txt',
            'gates/builder-leg-0.json', 'gates/builder-leg-1.json', 'images/head-plat-ledger.txt',
            'images/compare-r2.txt', 'repro/tests-on-5759780f.txt', 'repro/tests-on-fix.txt']:
    keep(rel)
for k in range(4):
    rel=f'gates/firmware-shard-{k}.txt'; s=(ev/rel).read_text()
    assert 'test_ctrl_firmware: PASS' in s and 'HEAD 87b2fc0f' in s
    assert (ev/f'gates/firmware-shard-{k}.rc').read_text().strip()=='0'
    keep(rel)
    print(f'Firmware shard {k}: exact-head PASS; published summary '+s.splitlines()[0])
for stem in ['1x1','8x8-1if']:
    for tag in ['probes-', 'probes-r2-vs-r3-']:
        rel=f'cpu/compare/{tag}{stem}.md'; s=(ev/rel).read_text()
        rows=[line.split('|')[1:-1] for line in s.splitlines() if line.startswith('| `')]
        assert len(rows)==(88 if stem=='1x1' else 86)
        assert all(float(r[1])<=float(r[4]) and float(r[2])<=float(r[4]) and r[5].strip()=='fits / fits' for r in rows)
        print(f'{tag}{stem}: {len(rows)} paired probes, 0 misses/changed verdicts, max rounded difference {max(abs(float(r[3])) for r in rows):.3f} ms')
        keep(rel)
    rel=f'cpu/head-{stem}.txt'; s=(ev/rel).read_text()
    assert '10 groups graded, 0 refusals, 0 budget misses' in s and 'over the per-pass share' in s
    print(next(line for line in s.splitlines() if line.startswith('10 groups graded')))
    keep(rel)
for name in ['flip_grade.py_--check_--point_1x1_1if.txt','flip_grade.py_--check_--point_8x8_1if.txt','load_grade.py_--check.txt','shape_costs.py_--check.txt']:
    rel='cpu/graders/head-'+name
    assert (ev/rel).read_bytes()==blob('author-r1/receipts/cpu/graders/base-'+name)
    keep(rel); print('Grader unchanged against source base: '+name)
for point in ['1x1-if1','1x1-if2','8x8-if1','8x8-if2']:
    rel='images/head-'+point+'-size.json'; d=json.loads((ev/rel).read_text()); s=d['split']
    limit=s.get('ledgered_tiles') or s['budget_tiles']
    assert s['tiles']<=limit
    print(f"Image {point}: ROM {s['rom']['bytes']}, SRAM {s['sram']['bytes']}, tiles {s['tiles']} <= {limit}")
    keep(rel)
sys.dont_write_bytecode=True
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import srp_mutants
defs=[d for d in srp_mutants.DEFECTS if d.name.startswith('link-pass-')]
assert len(defs)==14
for campaign in ['srp-if1-mutants','srp-8x8-if1-mutants','srp-mutants']:
    for d in defs:
        rel=f'plants/{campaign}/{d.name}.log'; text=(ev/rel).read_text()
        test=d.test if '.' in d.test else 'Srp.'+d.test
        assert d.needle in text and '[  FAILED  ] '+test in text
        keep(rel)
    print(campaign+': 14 named assertion failures, including all three new plants')
for f in (ev/'plants').rglob('rv-*.log'):
    keep(str(f.relative_to(ev)))
for name in ['run_focused.py','run_controls.py','probe_stale_mark.cpp','probe_reattach_elided.cpp']:
    assert (packet/name).read_bytes()==blob('reviews/R896-2/'+name)
print('Prior reviewer runners and probes: byte-identical to published originals')
sig=subprocess.check_output(['git','-C',str(root),'log','-1','--format=%G?',ref],text=True).strip()
print('Evidence commit signature status: '+sig+' (N means unsigned; no signature verification claimed)')
print('PASS: published receipt audit; execution belongs to the author, no manager source bank inferred')
