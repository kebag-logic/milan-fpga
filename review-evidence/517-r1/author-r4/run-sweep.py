from pathlib import Path
import json
import subprocess
import sys

out = Path(__file__).resolve().parent
rows = []
for index in range(5):
    name = f'sweep-{index}'
    argv = ['scripts/run_all_suites.sh',str(out/name),'--shard',f'{index}/5']
    result = subprocess.run(['python3',str(out/'run-gate.py'),name,*argv],check=False)
    rows.append(dict(chunk=f'{index}/5',argv=argv,exit_code=result.returncode))
    (out/'sweep-exits.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Sweep chunk exits:',rows,flush=True)
sys.exit(any(row['exit_code'] for row in rows))
