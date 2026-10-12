#!/usr/bin/env python3
"""Recompute window and mutation summaries from retained review receipts."""
import argparse, pathlib, json, re
p=argparse.ArgumentParser();p.add_argument('packet',type=pathlib.Path);a=p.parse_args();r=a.packet/'receipts';out={'windows':[],'mutants':[],'native':[]}
for shape in (1,8):
 name=f'frames-only-{shape}';text=(r/f'{name}.run.log').read_text(); assert (r/f'{name}.rc').read_text().strip()=='0'
 rows=[line.split(',') for line in text.splitlines() if re.match(r'^\d+,[56],\d+,[01],[0-4],',line)]
 graded=[x for x in rows if int(x[4])>=2];assert len(graded)==(24 if shape==1 else 108);assert all(x[5]=='1' for x in graded)
 cond=[line.split(',') for line in text.splitlines() if line.startswith('OUTPUT_CONDITION,')]
 assert len(cond)==shape+1
 assert all(x[2:] == ['frames-only','0','0','1','0','0','0'] for x in cond)
 service=[int(line.split(',')[2])/1000 for line in text.splitlines() if line.startswith('SERVICE,')]
 out['windows'].append(dict(shape=shape,recorded=len(rows),graded=len(graded),output_graded=sum(x[1]=='6' for x in graded),min_gap_ms=min(float(x[6]) for x in rows),max_gap_ms=max(float(x[7]) for x in rows),service_max_ms=max(service)))
for n,group in [('tx-nodirty','OUTPUT_CADENCE'),('tx-interval','TX'),('rx-interval','RX'),('tx-reset','TX_RESET'),('aaf-reset','RX_RESET'),('crf-reset','RX_RESET'),('rx-saturation','RX'),('late','CADENCE'),('rate','RATE')]:
 text=(r/f'{n}.run.log').read_text();fail=[line for line in text.splitlines() if '[FAIL]' in line]
 assert fail and all(f'[726 {group}]' in line for line in fail)
 escape=(r/f'{n}.escape.log').read_text();assert 'RESULT: PASS' in escape and '[FAIL]' not in escape
 assert (r/f'{n}.rc').read_text().strip()=='0'
 out['mutants'].append(dict(name=n,group=group,failures=len(fail),escape='PASS'))
for n,group in [('f5-late','CADENCE'),('f5-rate','RATE')]:
 text=(r/f'{n}.run.log').read_text();fail=[line for line in text.splitlines() if '[FAIL] Mailbox.' in line]
 assert fail and all(f'[F5 {group}]' in line for line in fail)
 escape=(r/f'{n}.escape.log').read_text();assert '[FAIL]' not in escape and (r/f'{n}.rc').read_text().strip()=='0'
 out['mutants'].append(dict(name=n,group=group,failures=len(fail),escape='PASS'))
for shape in (1,8):
 text=(r/f'before-{shape}.run.log').read_text();fail=[line for line in text.splitlines() if '[FAIL]' in line];groups=set(re.search(r'\[726 ([A-Z_]+)\]',line)[1] for line in fail);assert groups=={'TX','RX','CADENCE'}
 assert (r/f'before-{shape}.rc').read_text().strip()=='0'
for n in ('tkdiag','crf-rx','rxmon-nx','lockstep-1','lockstep-8'):
 text=(r/f'{n}.run.log').read_text();assert (r/f'{n}.rc').read_text().strip()=='0'
 out['native'].append(dict(name=n,result='PASS',summary=[line for line in text.splitlines() if 'checks' in line and ('failures' in line or '0 failures' in line)]))
print(json.dumps(out,indent=2))
