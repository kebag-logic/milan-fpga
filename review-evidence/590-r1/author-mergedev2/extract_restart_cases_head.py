"""Summarise the writer-restart cases of the nvm_cosim suite run at the stub-commit head.

Reads the checkout's git-ignored `tb/verilator/nvm_cosim/runs/` left by the
`nvm_cosim-4c2a30de` gate run, writes `restart-cases-4c2a30de.json`, keeps each
contract build's restart-case stdout under `head-evidence/`, and compares every
case run's stdout (all builds, all cases) with the scratch probe's.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

OUT = Path(__file__).parent
ROOT = Path('$LANES/590-592-599-firmware')
RUNS = ROOT / 'tb/verilator/nvm_cosim/runs'
PROBE_RUNS = Path('$VALIDATION_STORAGE/590-a430/probe/tb/verilator/nvm_cosim/runs')
KEYS = ('ms', 'backed', 'stale', 'dirty_pub', 'pend', 'hb')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert head == '4c2a30debb031595b81c5c4bfc53b601a0fec528', head
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()


#: the host prints the address of its DDR buffer ("at 0x…", "-> 0x…"), which moves
#: with address-space randomisation from one process to the next
HOST_ADDRESS = re.compile(rb'(at|->) 0x[0-9a-f]+')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalised(path):
    return hashlib.sha256(HOST_ADDRESS.sub(rb'\1 <host-address>', path.read_bytes())).hexdigest()


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
        target = OUT / 'head-evidence' / run.parent.name / (run.name + '.stdout.log')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(stdout, target)
        kept = str(target.relative_to(OUT))
    cases.append(dict(build=run.parent.name, case=run.name, stdout_size=len(raw),
                      stdout_sha256=hashlib.sha256(raw).hexdigest(), kept=kept,
                      observations=obs, console=console))
here = {str(p.relative_to(RUNS)): digest(p) for p in RUNS.glob('*/*/stdout.log')}
probe = {str(p.relative_to(PROBE_RUNS)): digest(p) for p in PROBE_RUNS.glob('*/*/stdout.log')}
here_n = {str(p.relative_to(RUNS)): normalised(p) for p in RUNS.glob('*/*/stdout.log')}
probe_n = {str(p.relative_to(PROBE_RUNS)): normalised(p) for p in PROBE_RUNS.glob('*/*/stdout.log')}
comparison = dict(case_runs_here=len(here), case_runs_probe=len(probe),
                  only_here=sorted(set(here) - set(probe)), only_probe=sorted(set(probe) - set(here)),
                  byte_identical=sum(1 for k in set(here) & set(probe) if here[k] == probe[k]),
                  differing_raw=len([k for k in set(here) & set(probe) if here[k] != probe[k]]),
                  differing_after_host_address_normalisation=sorted(
                      k for k in set(here_n) & set(probe_n) if here_n[k] != probe_n[k]))
summary = dict(head=head, runs=str(RUNS), all_case_stdout_vs_probe=comparison,
               case_runs={key: dict(stdout_sha256=here[key], normalised_sha256=here_n[key]) for key in sorted(here)},
               cases=cases)
(OUT / 'restart-cases-4c2a30de.json').write_text(json.dumps(summary, indent=2) + '\n')
print(len(cases), 'restart-case runs;', sum(1 for c in cases if c['kept']), 'contract logs kept')
print(json.dumps(comparison))
