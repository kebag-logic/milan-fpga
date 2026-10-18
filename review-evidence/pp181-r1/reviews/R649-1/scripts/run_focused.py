#!/usr/bin/env python3
"""Run focused review checks in a disposable copy; no source checkout writes."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('phase', choices=['setup', 'router', 'notify', 'top', 'budget', 'docs'])
p.add_argument('--repo', required=True, type=Path)
p.add_argument('--packet', required=True, type=Path)
p.add_argument('--compiler', required=True, type=Path)
a = p.parse_args()
packet = a.packet.resolve()
tree = packet / 'scratch/head'
receipts = packet / 'receipts'
receipts.mkdir(exist_ok=True, parents=True)
def run(name, argv, cwd):
    with (receipts / (name + '.log')).open('w') as log:
        log.write('argv: ' + repr([str(x) for x in argv]) + '\n')
        log.flush()
        result = subprocess.run([str(x) for x in argv], cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, 'rc', result.returncode, flush=True)
    return result.returncode

if a.phase == 'setup':
    subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(a.repo), str(tree)], check=True)
    subprocess.run(['git', 'checkout', '--detach', '42eb9aef3642f6d98058fe634a70f6a9c749cd25'], cwd=tree, check=True)
    wrapper = packet / 'scratch/compiler'
    wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\n'
                       'for i in range(len(a)-1):\n'
                       ' if a[i] in ("-j", "--build-jobs"): a[i+1]="4"\n'
                       'os.execv(' + repr(str(a.compiler)) + ', [' + repr(str(a.compiler)) + '] + a)\n')
    wrapper.chmod(0o755)
    sys.exit(0)
compiler = 'VERILATOR=' + str(packet / 'scratch/compiler')
if a.phase in ('router', 'notify'):
    suite = {'router': 'event_router', 'notify': 'aecp_notify'}[a.phase]
    sys.exit(run(a.phase, ['make', '-j16', compiler], tree / 'tb' / suite))
if a.phase == 'docs':
    sys.exit(run('docs', ['make', '-j16', 'check'], tree))
if a.phase == 'budget':
    sys.exit(run('top-budget', ['make', '-j16', 'budget', compiler], tree / 'tb/pp_top'))
if a.phase == 'top':
    d = tree / 'tb/pp_top'
    rc = run('top-build', ['make', '-j16', 'gsi-build', compiler], d)
    if rc: sys.exit(rc)
    for option in ['notify', 'aecp-dispatch', 'spacing', 'hazards']:
        rc |= run('top-' + option, ['./obj_dir/Vpp_top_sim', '--' + option + '-only'], d)
    sys.exit(rc)
