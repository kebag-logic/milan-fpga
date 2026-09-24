import json, os, subprocess, sys, time
from pathlib import Path
out = Path(__file__).resolve().parent
commands = json.loads((out/'sweep-commands.json').read_text())
start, end = map(int, sys.argv[1:])
env = os.environ.copy()
env['VERILATOR_JOBS'] = '8'
for index in range(start, end + 1):
    command = commands[index - 1]
    now = time.monotonic()
    name = f'sweep-{index:02d}'
    print(name, command[:120], flush=True)
    with (out/(name+'.log')).open('w') as log:
        result = subprocess.run(['bash', '-eu', '-c', command], cwd='$LANES/387-media-rebase/tb/verilator/milan_dp', env=env, stdout=log, stderr=subprocess.STDOUT, timeout=14400, check=False)
    receipt = dict(command=command, rc=result.returncode, elapsed_s=round(time.monotonic()-now,2))
    (out/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(name, 'rc',result.returncode,'seconds',receipt['elapsed_s'],flush=True)
    if result.returncode:
        print('\n'.join((out/(name+'.log')).read_text(errors='replace').splitlines()[-30:]),flush=True)
        sys.exit(result.returncode)
