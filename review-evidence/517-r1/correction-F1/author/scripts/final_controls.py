from pathlib import Path
import json,subprocess,sys
out=Path(sys.argv[1]).resolve();lane=Path.cwd();head=json.loads((out/'candidate.json').read_text())['head']
commands=[
 ('focused',[sys.executable,str(out/'public/public/author/bench/checks.py'),str(lane),str(out/'final-focused')]),
 ('additional',[sys.executable,str(out/'scripts/additional_gates.py'),str(out/'final-additional')]),
 ('backpressure',['timeout','90s',sys.executable,'tb/verilator/milan_dp/test_sim_pool_backpressure.py','--output',str(out/'final-backpressure')]),
 ('negative',['timeout','60s',sys.executable,str(out/'scripts/restored_defect.py'),str(lane),str(out/'final-restored-defect')]),
 ('integrity',[sys.executable,str(out/'scripts/integrity.py'),str(lane),str(out/'pre-benchmark-integrity.json'),head]),
 ('diff-check',['git','diff','--check',head+'^',head]),
]
rows=[]
for name,cmd in commands:
 rc=subprocess.run(['rtk','proxy',sys.executable,str(out/'scripts/record.py'),str(out/('final-'+name+'-command')),'rtk','proxy',*cmd]).returncode
 rows.append({'name':name,'argv':cmd,'exit':rc})
(out/'final-controls.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(int(any(row['exit'] for row in rows)))
