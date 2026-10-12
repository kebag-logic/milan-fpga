#!/usr/bin/env python3
"""Run focused review checks synchronously, retaining individual receipts.

Usage: python3 run_checks.py ROOT PACKET PINNED_VERILATOR GROUP
All temporary and build output belongs below PACKET/scratch.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet, pinned = map(Path, sys.argv[1:4])
group = sys.argv[4]
env = dict(os.environ, TMPDIR=str(packet / 'scratch/tmp'), PYTHONDONTWRITEBYTECODE='1')
env['VERILATOR'] = str(pinned)
receipts = packet / 'receipts'
receipts.mkdir(exist_ok=True)
failures = []

def run(name, args, cwd=None, extra=None):
    """Wait for one command and retain its complete output and status."""
    started = time.monotonic()
    with (receipts / (name + '.log')).open('w') as log:
        result = subprocess.run(args, cwd=cwd or root, env=env | (extra or {}),
                                stdout=log, stderr=subprocess.STDOUT, check=False)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    info = dict(command=args, cwd=str(cwd or root), rc=result.returncode,
                seconds=round(time.monotonic() - started, 2))
    (receipts / (name + '.json')).write_text(json.dumps(info, indent=2) + '\n')
    print(name, result.returncode, info['seconds'], flush=True)
    if result.returncode:
        failures.append(name)
    return result.returncode

if group == 'counters':
    run('make-counters', ['make', '-j16', '-C', 'tb/verilator/milan_dp', 'counters'])
elif group == 'units':
    # The pinned executable's -j0 requests all CPUs. Limit each build to four.
    wrapper = packet / 'scratch/verilator-limited'
    wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\n'
                       'for i in range(len(a)-1):\n'
                       ' if a[i]=="-j" and (a[i+1]=="0" or int(a[i+1])>4): a[i+1]="4"\n'
                       'os.execv(' + repr(str(pinned)) + ',[' + repr(str(pinned)) + ']+a)\n')
    wrapper.chmod(0o755)
    for name, target in [('avtp_rxmon', 'run'), ('tkdiag', 'run'), ('crf_rx', 'unit')]:
        run(name, ['make', '-j16', '-C', 'tb/verilator/' + name, target],
            extra={'VERILATOR': str(wrapper)})
elif group == 'light':
    tasks = [('counter-helper', ['python3', 'tb/tools/torture_campaign.py', '--self-test'], None),
             ('behave', ['python3', '-m', 'behave', '--no-capture', '-f', 'plain'], root / 'tests')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda task: run(*task), tasks))
elif group == 'mutants':
    variants = ['tx-interval', 'rx-interval', 'tx-reset', 'aaf-reset', 'crf-reset',
                'rx-saturation', 'late', 'rate', 'tx-nodirty', 'fixed-grid']
    def campaign(variant):
        return run('plant-' + variant, ['python3', 'tb/verilator/milan_dp/stream_counters.py',
                   '--variant', variant, '--work', str(packet / 'scratch' / ('plant-' + variant))])
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(campaign, variants))
elif group == 'f5':
    for shape, variant in [(1, 'clean'), (8, 'clean'), (1, 'late'), (1, 'rate'), (1, 'fixed-grid')]:
        name = f'f5-{shape}-{variant}'
        run(name, ['python3', 'tb/verilator/milan_dp/stream_counter_f5.py', '--shape', str(shape),
                  '--variant', variant, '--work', str(packet / 'scratch' / name)])
elif group == 'docs':
    import shlex
    import yaml
    workflow = yaml.safe_load((root / '.github/workflows/docs.yml').read_text())
    excluded = ('builder/', 'act_ci.py', 'ci_rv32_sdk.py', 'nvm_hosttest/')
    tasks = []
    for step in workflow['jobs']['docs-check']['steps']:
        for line in step.get('run', '').splitlines():
            if not line.startswith('python3 ') or 'pip install' in line or any(x in line for x in excluded):
                continue
            if line.endswith('\\') or '$' in line:
                continue
            args = shlex.split(line)
            tasks.append(args)
    tasks += [['python3', 'scripts/check_em_dash.py', '--base', 'c6bd08c6'],
              ['python3', 'scripts/check_wire_accountability.py', '--self-test'],
              ['python3', 'scripts/pp_srcs.py', '--check', '--selftest']]
    (receipts / 'docs-commands.json').write_text(json.dumps(tasks, indent=2) + '\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda pair: run('docs-%02d-%s' % (pair[0], Path(pair[1][1]).stem), pair[1]), enumerate(tasks)))
elif group == 'probes':
    for name in ['reproduce_contract', 'probe_xside_law', 'probe_snapshot']:
        args = ['python3', str(packet / 'scripts' / (name + '.py')), str(root)]
        if name == 'probe_snapshot':
            args.append(str(packet))
        run(name, args)
elif group == 'direct':
    def direct(shape):
        name = 'direct-' + str(shape)
        return run(name, ['python3', 'tb/verilator/milan_dp/stream_counters.py', '--shape', str(shape),
                         '--work', str(packet / 'scratch' / name)], extra={'MAKEFLAGS': ' -w'})
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(direct, [1, 8]))
else:
    raise SystemExit('Unknown group: ' + group)
raise SystemExit(int(bool(failures)))
