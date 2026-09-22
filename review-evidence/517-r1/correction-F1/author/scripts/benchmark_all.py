import json,subprocess,sys
from pathlib import Path
out=Path(sys.argv[1]).resolve();lane=Path.cwd();head=json.loads((out/'candidate.json').read_text())['head']
assert all(row['exit']==0 for row in json.loads((out/'final-controls.json').read_text()))
assert not subprocess.check_output(['git','status','--porcelain'])
selector='$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator'
rows=[]
for jobs,name,temperature in [(1,'cold-sequential','cold'),(1,'warm-sequential','warm'),(2,'cold-pooled','cold'),(2,'warm-pooled','warm')]:
 cmd=['rtk','proxy',sys.executable,str(out/'bench/run_suite.py'),'--lane',str(lane),'--out',str(out/'runs'/name),'--verilator',selector,'--expect-head',head,'--jobs',str(jobs),'--temperature',temperature]
 rc=subprocess.run(['rtk','proxy',sys.executable,str(out/'scripts/record.py'),str(out/'benchmark-commands'/name),*cmd]).returncode
 rows.append({'name':name,'argv':cmd,'exit':rc});(out/'benchmark-progress.json').write_text(json.dumps(rows,indent=2)+'\n')
 if rc:sys.exit(rc)
 analysis=['rtk','proxy',sys.executable,str(out/'bench/analyze.py'),str(out/'runs'/name),str(lane),'--json',str(out/'runs'/name/'analysis.json')]
 rc=subprocess.run(['rtk','proxy',sys.executable,str(out/'scripts/record.py'),str(out/'analysis-commands'/name),*analysis]).returncode
 if rc:sys.exit(rc)
for temperature in ('cold','warm'):
 cmd=['rtk','proxy',sys.executable,str(out/'bench/compare.py'),str(lane),str(out/'runs'/(temperature+'-sequential')),str(out/'runs'/(temperature+'-pooled')),str(out/(temperature+'-comparison.json'))]
 rc=subprocess.run(['rtk','proxy',sys.executable,str(out/'scripts/record.py'),str(out/'comparison-commands'/temperature),*cmd]).returncode
 if rc:sys.exit(rc)
