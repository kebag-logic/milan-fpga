from pathlib import Path
import json,subprocess,sys
p=Path(__file__).resolve().parent
cmds=json.loads((p/'milan-dp-commands.json').read_text())
first,last=map(int,sys.argv[1:3])
for i in range(first,last+1):
 rc=subprocess.run(['python3',str(p/'run_gate.py'),f'dp-{i:02d}','--cwd','tb/verilator/milan_dp',*cmds[i-1]]).returncode
 if rc:sys.exit(rc)
print(f'CHUNK {first}-{last} all rc 0',flush=True)
