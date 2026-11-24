"""Run selected substantive workflow steps locally, in the foreground, retaining every exit."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import yaml

root = Path.cwd()
group = sys.argv[1]
out = Path('/data-2/milan/tmp/opt-a837/jobs') / group
out.mkdir(parents=True, exist_ok=True)
mdpython = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3'
env = dict(os.environ, RUNNER_TEMP=str(out), CI_CAMPAIGN_JOBS='4', CI_CENSUS_JOBS='2', GITHUB_PATH=str(out/'github-path'), VERILATOR_VERSION='v5.050')
rows = []

def run(name, script, directory=None):
    log = out / f'{len(rows):03d}.log'
    command = out / f'{len(rows):03d}.sh'
    command.write_text('set -euo pipefail\n' + script + '\n')
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(['bash', str(command)], cwd=directory or root, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=21600, check=False)
    row = dict(name=name, rc=result.returncode, seconds=round(time.monotonic()-start, 2),
               script=str(command), log=str(log))
    rows.append(row)
    (out/'results.json').write_text(json.dumps(rows, indent=2)+'\n')
    print(json.dumps(row), flush=True)
    if result.returncode:
        print('\n'.join(log.read_text(errors='replace').splitlines()[-12:]), flush=True)

if group == 'docs':
    doc = yaml.safe_load((root/'.github/workflows/docs.yml').read_text())
    for step in doc['jobs']['docs-gates-0']['steps']:
        if not step.get('id','').startswith('gate_') or 'run' not in step:
            continue
        script = step['run']
        if step['name'] == 'Build the validated HDL reference':
            script = 'python3 scripts/gen_hdl_reference.py --selftest\npython3 scripts/gen_hdl_reference.py --output "$RUNNER_TEMP/hdl-reference"'
        if step['name'] == 'Added-line em-dash gate':
            base = subprocess.check_output(['git','merge-base','HEAD','origin/dev-soft-core-optimisation'], text=True).strip()
            script = 'python3 scripts/check_em_dash.py --base ' + base
        for module in ('gen_hdl_reference','check_em_dash','gen_toc','docs_inventory'):
            script = script.replace('python3 scripts/'+module+'.py', mdpython+' scripts/'+module+'.py')
        run(step['name'], script)
    run('Advertised versus emitted', 'python3 scripts/check_wire_accountability.py --self-test')
    run('CI event and SHA contract', 'python3 scripts/ci_events.py --check\npython3 scripts/ci_events.py --selftest')
elif group in ('yosys-elaboration','verilator-lint','bdd-conformance','publication-census','split-cdc'):
    doc = yaml.safe_load((root/'.github/workflows/rtl-fast.yml').read_text())
    starts = ('Run the ratcheted', 'Prove ', 'Run the specification', 'Elaborate the integration',
              'Run the publication')
    for step in doc['jobs'][group]['steps']:
        if not step.get('name','').startswith(starts):
            continue
        run(step['name'], step['run'].replace('/opt/verilator/bin', '$VALIDATION_TOOLS/pinned-verilator-5.050'), root/step.get('working-directory','.'))
else:
    raise SystemExit('unknown group '+group)
raise SystemExit(1 if any(row['rc'] for row in rows) else 0)
