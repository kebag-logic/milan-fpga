#!/usr/bin/env python3
"""Audit published receipt hashes and compare their machine-readable summaries."""
import hashlib,json,pathlib,re,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
ev=pathlib.Path(sys.argv[1]).resolve()
out=[]
manifest=json.loads((ev/'MANIFEST.json').read_text())
bad=[]
for row in manifest:
    f=ev/row['file']
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=row['published_sha256']:bad.append(row['file'])
out.append(f'Published manifest: {len(manifest)} files checked, mismatches {bad}')
r=ev/'author-r1/receipts'
g=json.loads((r/'stack/gates-5d14a6d8/gates.json').read_text())
out.append(f'Stack author gates: {len(g)}, nonzero {[x for x in g if x["rc"]]}')
fw=r/'gates/27495a06'
for f in sorted(fw.glob('firmware-gate-shard*.txt')):
    s=f.read_text()
    out.append(f'{f.name}: PASS={"test_ctrl_firmware: PASS" in s}, rc0={"END rc=0" in s}, suite verdicts={len(re.findall(r"verdict: PASS",s))}')
for f in sorted((r/'cpu/compare').glob('*.txt')):
    lines=f.read_text().splitlines()
    out.extend([f.name+': '+x for x in lines if x.startswith(('probes:','verdicts changed:','misses each side:','largest differences:'))])
for stem in ['flip_grade.py_--check','flip_grade.py_--check_--point_1x1_1if','load_grade.py_--check','shape_costs.py_--check']:
    out.append(stem+': base/head bytes equal='+str((r/'cpu/graders'/('base-'+stem+'.log')).read_bytes()==(r/'cpu/graders'/('head-'+stem+'.log')).read_bytes()))
out.append('Platform and size-fixture image pairs: '+str(sum('relinks equal to built: 2/2' in x and 'rc 0' in x for x in (r/'images/SUMMARY.txt').read_text().splitlines())))
out.append('Budget canonical image comparisons refused: '+str(sum(x.startswith('budget-') and 'rc 1' in x for x in (r/'images/SUMMARY.txt').read_text().splitlines())))
out.append('Budget hash rows: base='+str(len((r/'images/budget-hashes-base.txt').read_text().splitlines()))+' head='+str(len((r/'images/budget-hashes-head.txt').read_text().splitlines())))
text='\n'.join(out)+'\n'
(p/'receipts/evidence-audit.txt').write_text(text)
print(text)
assert not bad
