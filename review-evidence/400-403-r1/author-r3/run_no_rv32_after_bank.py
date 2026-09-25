from pathlib import Path
import json, subprocess, sys, time
out=Path(__file__).resolve().parent
print('Waiting for bank-48 to finish before the complete no-RV32 run.',flush=True)
while True:
    rows=[json.loads(s) for s in (out/'gates.jsonl').read_text().splitlines()]
    complete=next((r for r in rows if r['label']=='bank-48'), None)
    if complete:
        if complete['exit']:
            sys.exit(complete['exit'])
        break
    time.sleep(10)
sys.exit(subprocess.run([sys.executable,str(out/'run_gate.py'),'builder-no-rv32',
                         'python3','-u',str(out/'no-rv32-builder.py')],timeout=43200).returncode)
