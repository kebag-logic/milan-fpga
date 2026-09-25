import os, shlex, subprocess, sys
from pathlib import Path
out=Path('$MANAGEMENT/2026-09-23/545-a308')
commands=[line for line in (out/'milan-dp-run-dry.txt').read_text().replace('\\\n',' ').splitlines() if line and not line.startswith('echo ')]
assert len(commands)==33
os.environ['VERILATOR_JOBS']='4'
os.environ['PATH']='/tmp/545-a308-env/bin:'+os.environ['PATH']
os.chdir('$LANES/545-crf-servo-slew/tb/verilator/milan_dp')
start,end=map(int,sys.argv[1:])
for number in range(start,end+1):
    cmd=shlex.split(commands[number-1])
    subprocess.run(['python3','/tmp/545-a308-run.py',f'dp-run-{number:02d}','taskset','-c',os.environ.get('DP_CPUS','12-15'),*cmd],check=True)
print(f'Chunk {start}-{end}: all exits 0',flush=True)
