"""Summarise the writer-restart cases of the scratch nvm_cosim probe.

Reads the probe's per-case runs (outside the checkout), writes
`restart-cases.json`, and keeps each contract build's restart-case stdout
under `probe-evidence/` when it is 200 KB or smaller.
"""
from pathlib import Path
import hashlib
import json
import shutil

OUT = Path(__file__).parent
PROBE = Path('$VALIDATION_STORAGE/590-a430/probe/tb/verilator/nvm_cosim')
RUNS = PROBE / 'runs'
LOG = Path('$VALIDATION_STORAGE/590-a430/logs/probe-nvm_cosim.log')
KEYS = ('ms', 'backed', 'stale', 'dirty_pub', 'pend', 'hb')

cases = []
for run in sorted(RUNS.glob('*/W[1-4]_*')):
    stdout = run / 'stdout.log'
    raw = stdout.read_bytes()
    obs, console = [], []
    for line in raw.decode().splitlines():
        if line.startswith('OBS '):
            record = json.loads(line[4:])
            obs.append(dict(tag=record['tag'], **{key: record[key] for key in KEYS}))
        elif line.startswith('Milan NVM:'):
            console.append(line)
    kept = None
    if run.parent.name.startswith('contract-') and len(raw) <= 200000:
        target = OUT / 'probe-evidence' / run.parent.name / (run.name + '.stdout.log')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(stdout, target)
        kept = str(target.relative_to(OUT))
    cases.append(dict(build=run.parent.name, case=run.name, stdout_size=len(raw),
                      stdout_sha256=hashlib.sha256(raw).hexdigest(), kept=kept,
                      observations=obs, console=console))
log = LOG.read_bytes()
shutil.copyfile(LOG, OUT / 'logs' / LOG.name)
host = (PROBE / 'cosim_host.c').read_bytes()
summary = dict(probe_log=dict(size=len(log), sha256=hashlib.sha256(log).hexdigest(),
                              kept='logs/' + LOG.name),
               probe_cosim_host_sha256=hashlib.sha256(host).hexdigest(), cases=cases)
(OUT / 'restart-cases.json').write_text(json.dumps(summary, indent=2) + '\n')
print(len(cases), 'restart-case runs;', sum(1 for c in cases if c['kept']), 'contract logs kept')
