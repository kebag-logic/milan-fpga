from pathlib import Path
import re
r=Path('$VALIDATION_STORAGE/pp73-a595/r4');lines=[]
for side in ['base','head']:
 bank=r/'parent-e8454e27'/side
 codes={p.stem:p.read_text().strip() for p in bank.glob('*.rc')}
 assert len(codes)==5 and all(x=='0' for x in codes.values()),(side,codes)
 lines.append(f'{side}: all five original-parent commands rc 0')
for name in ['bdd','feature_status','pp_srcs','rom_verify_tcam']:
 b=(r/'parent-e8454e27/base'/(name+'.log')).read_text()
 h=(r/'parent-e8454e27/head'/(name+'.log')).read_text()
 def norm(s):return re.sub(r'Took .*','Took <elapsed>',re.sub(r'\d+\.\d+s','<seconds>',s))
 assert norm(b)==norm(h),name
 lines.append(f'{name}: byte-identical {b==h}; identical without elapsed times')
rows=[]
for side in ['base','head']:
 rows.append(['\t'.join(x.split('\t')[1:]) for x in (r/'parent-e8454e27'/side/'rom_rows_at_pin.tsv').read_text().splitlines()])
assert rows[0]==rows[1]
lines.append('ROM ledger rows identical apart from commit key')
for name in ['head-python','head-python-list','head-python-self']:
 assert (r/'logs'/(name+'.rc')).read_text().strip()=='0',name
old=(r.parent/'r2/pgates/head/bank/py_idiom.log').read_text().splitlines()[1:]
new=(r/'logs/head-python.log').read_text().splitlines()[1:]
assert new==old,'Python ratchet counts changed'
lines.append('Consumer Python gate, listing and 54-check self-test rc 0; all ratchet counts and budgets unchanged from 99757648')
(r/'comparisons/parent.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
