import json,subprocess,time
from pathlib import Path
p=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
rows=[]
for script,args in [('check_py_idiom.py',[]),('check_cpp_idiom.py',[]),('measure_fail_fast.py',['--check']),('check_hygiene.py',['--check']),('check_port_contracts.py',[]),('measure_naming.py',['--check']),('check_todo_ownership.py',[]),('measure_test_evidence.py',['--check'])]:
 command=['python3','scripts/'+script,*args]
 with (p/('gate-'+script+'.log')).open('w') as f:
  result=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT)
 rows.append(dict(command=command,rc=result.returncode))
 print(script,result.returncode,flush=True)
 (p/'gates.json').write_text(json.dumps(rows,indent=2)+'\n')
