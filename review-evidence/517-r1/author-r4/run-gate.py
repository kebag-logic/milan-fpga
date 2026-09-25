import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/517-bounded-simulation-pool')
ENV = os.environ.copy()
ENV['PATH'] = '$VALIDATION_STORAGE/517-a321-env/bin:$VALIDATION_STORAGE/408-manager-r7/pinned-tool-bin:' + ENV['PATH']
ENV['VERILATOR_JOBS'] = '8'
ENV['PYTHONDONTWRITEBYTECODE'] = '1'
ENV['PYTHONUNBUFFERED'] = '1'
for key in ('SIM_JOBS', 'MILAN_COUNTER_FRAME_OUT', 'SUITE_TIMEOUT', 'MAKEFLAGS', 'MFLAGS'):
    ENV.pop(key, None)
os.sched_setaffinity(0, set(range(16, 24)))
name, *argv = sys.argv[1:]
assert name and argv
log = OUT / (name + '.log')
assert not log.exists(), log
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
record = dict(name=name, argv=argv, head=head, cwd=str(ROOT),
              start=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              cpus=sorted(os.sched_getaffinity(0)), verilator_jobs=8)
print('START', name, flush=True)
start = time.monotonic()
with log.open('wb') as output:
    result = subprocess.run(argv, cwd=ROOT, env=ENV, stdout=output,
                            stderr=subprocess.STDOUT, check=False)
record.update(exit_code=result.returncode, seconds=time.monotonic()-start)
(OUT / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n')
with (OUT / 'gates.jsonl').open('a') as ledger:
    ledger.write(json.dumps(record) + '\n')
with (OUT / 'HANDOFF.md').open('a') as handoff:
    command = ' '.join(argv).replace(str(OUT), '$EVIDENCE')
    handoff.write(f"\nGate `{name}`: `{command}`; exit {result.returncode}; {record['seconds']:.3f} s; `{log.name}`.\n")
subprocess.run(['python3', str(OUT / 'refresh-handoff.py')], check=True)
print('END', name, 'exit', result.returncode, 'seconds', round(record['seconds'], 3), flush=True)
print(log.read_text(errors='replace')[-3500:], flush=True)
sys.exit(result.returncode)
