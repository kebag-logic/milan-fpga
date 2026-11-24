from pathlib import Path
import argparse,json,sys
ROOT=Path('/data-2/milan/lanes/opt-hart2');sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import run, scenario
b=Path(sys.argv[1]); point=sys.argv[2]
spec=json.loads((b/'build.json').read_text())
groups={g.name:g for g in run.all_groups(scenario.point(point,spec),spec)}
args=argparse.Namespace(cpu_regions='cover',mutation='none',record_budget_findings=False,record_share_findings=False)
rows=[]
for p in sorted((b/'group-grades').glob('*-verdict.json')):
 r=json.loads(p.read_text());rc=run.verdict(args,[groups[r['group']]],r['refusals'],r['budget_misses'],r['share_misses'],r['other_findings'])
 rows.append(dict(group=r['group'],record_mode_rc=r['grader_rc'],strict_rc=rc,refusals=len(r['refusals']),budget_misses=len(r['budget_misses']),share_findings=len(r['share_misses']),other_findings=len(r['other_findings'])))
result=dict(point=point,geometry=spec['hart1_geometry'],groups=rows,complete=len(rows)==9,strict_rc=int(len(rows)!=9 or any(r['strict_rc'] for r in rows)))
(b/'strict-grades.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(result['strict_rc'])
