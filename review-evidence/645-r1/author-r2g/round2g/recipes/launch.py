import json, subprocess, sys
from pathlib import Path
w = Path(__file__).resolve().parent
name = sys.argv[1]
assert not (w / 'jobs' / (name + '.pid')).exists()
with (w / 'jobs' / (name + '.launcher.log')).open('w') as log:
    p = subprocess.Popen(['setsid', 'nohup', 'python3', '-B', str(w / 'run_job.py'), name], stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
(w / 'jobs' / (name + '.pid')).write_text(str(p.pid) + '\n')
print(name, p.pid)
