from pathlib import Path
import json
out=Path(__file__).resolve().parents[1]
for run in sorted((out/'runs').glob('*')) if (out/'runs').exists() else []:
 if not run.is_dir():continue
 summary=run/'summary.json'
 if summary.exists():
  result=json.loads(summary.read_text());print(run.name,{'wall_s':result['wall_s'],'exit':result['exit']});continue
 p=run/'samples.jsonl'
 if p.exists() and p.stat().st_size:
  with p.open('rb') as f:
   f.seek(max(0,p.stat().st_size-200000));lines=f.read().splitlines()
  sample=json.loads(lines[-1]);procs=sample['procs']
  ordinary=[r['argv'][0] for r in procs if r['argv'] and r['argv'][0].startswith('./obj_')]
  other=[r['argv'][:2] for r in procs if r['argv'] and (any('render_mutants.py' in a for a in r['argv']) or 'verilator_bin' in r['argv'][0])]
  print(run.name,{'elapsed_s':sample['t'],'ordinary':ordinary,'other':other,'sample_rss_kb':sum(r['rss_kb'] for r in procs)})
  text=(run/'milan_dp.log').read_text(errors='replace');print('recent verdicts', [x for x in text.splitlines() if 'checks:' in x or 'RENDER-PHASE ' in x][-2:])
