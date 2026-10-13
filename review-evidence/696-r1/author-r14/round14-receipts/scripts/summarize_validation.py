import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
w=Path(__file__).resolve().parent;repo=w/'candidate';v=w/'validation';e=w/'excerpts';e.mkdir(exist_ok=True)
assert (w/'accepted-validation.rc').read_text().strip()=='0'
assert (w/'resource-bank.rc').read_text().strip()=='0'
assert (w/'record-measurements.rc').read_text().strip()=='0'
assert (w/'static-bank.rc').read_text().strip()=='0'
rows=json.loads((w/'accepted-validation.json').read_text())['commands'];assert len(rows)==22,(len(rows),rows)
assert all(r['rc']==0 for r in rows)
spec=importlib.util.spec_from_file_location('suite_tally',repo/'scripts/suite_tally.py');tally=importlib.util.module_from_spec(spec);spec.loader.exec_module(tally)
old=json.loads((w/'round13-totals.json').read_text())
suites=['maap','milan_dp','mbx','pp_shadow','capture_coherence','milan_dp_mclk','milan_dp_render']
results={};logdir=w/'suite-tally';logdir.mkdir(exist_ok=True)
for suite in suites:
 p=v/(suite+'.log');result=tally.scan(p.read_text(errors='replace'))
 results[suite]=dict(checks=result[0],failures=result[1],matched=result[2],unparsed=result[3],skipped=result[4])
 verdict=subprocess.run(['python3','scripts/suite_tally.py','--verdict',str(p)],cwd=repo,capture_output=True,text=True)
 (v/(suite+'-verdict.log')).write_text(verdict.stdout+verdict.stderr)
 (v/(suite+'-verdict.rc')).write_text(str(verdict.returncode)+'\n');assert verdict.returncode==0
 q=logdir/p.name
 if not q.exists():q.symlink_to(p)
with (v/'suite-tally.log').open('w') as f:rc=subprocess.run(['python3','scripts/suite_tally.py',str(logdir)],cwd=repo,stdout=f,stderr=subprocess.STDOUT).returncode
(v/'suite-tally.rc').write_text(str(rc)+'\n');assert rc==0
for row in rows:
 p=v/(row['name']+'.log');lines=p.read_text(errors='replace').splitlines()
 # Keep explicit results with line references; full raw-log identity remains in the manifest.
 found=[f'{i}: {line}' for i,line in enumerate(lines,1) if re.search(r'(?i)(\[ok\]|\[pass\]|caught|rejected|tests? passed|tests? from|checks|coverage:|ctrl_boundary:|test_ctrl_firmware:|test_ctrl_nvm:|ALL GATES|NOT RUN|mutants:|capture:|summary|scenarios? passed|steps? passed|REFUSED)',line)]
 part=1;chunk=[];size=0
 for line in found:
  if len(line.encode())>170000:line=line[:2000]+' [long line abbreviated; see raw log at this line number]'
  amount=len(line.encode())+1
  if chunk and size+amount>180000:
   (e/(row['name']+f'-{part:02}.txt')).write_text('\n'.join(chunk)+'\n');part+=1;chunk=[];size=0
  chunk.append(line);size+=amount
 (e/(row['name']+f'-{part:02}.txt')).write_text('\n'.join(chunk)+'\n')
summary=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),commands=rows,suites=results,suite_total=sum(r['checks'] for r in results.values()),prior=old)
(w/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(dict(commands=len(rows),suites=results,total=summary['suite_total']),indent=2))
