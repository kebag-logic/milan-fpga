#!/usr/bin/env python3
"""Plant generated-workflow defects in a disposable template/workflow copy."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
fixture = out/'scratch/workflow-drift'
fixture.mkdir(exist_ok=True)
for part in ['ci-templates','workflows']:
    shutil.copytree(root/'.github'/part,fixture/'.github'/part,dirs_exist_ok=True)
path = fixture/'.github/workflows/rtl-fast.yml'
original = path.read_text()
env = {**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(out/'scratch')}
def check(label, source, expected):
    path.write_text(source)
    run = subprocess.run([sys.executable,str(root/'scripts/ci_gate_workflows.py'),'--root',str(fixture),'--check'],
                         cwd=root,env=env,capture_output=True,text=True,timeout=60)
    assert run.returncode == expected, (label,run.stdout,run.stderr)
    if expected:
        assert '.github/workflows/rtl-fast.yml: regenerate the gate jobs' in run.stdout
    print(label, 'rc='+str(run.returncode), run.stdout.strip())
check('control',original,0)
check('consumer miss silently accepted',original.replace('fail-on-cache-miss: true','fail-on-cache-miss: false'),1)
check('tool/consumer agree on stale recipe key',original.replace('06e5a02fa8b585ca1b3cc3153245cd97f8b1009666d3b15728f325ed9bd22279','0'*64),1)
check('tool/consumer agree on stale version',original.replace('yosys-${{ env.YOSYS_VERSION }}-86f2ddeb','yosys-v0.65-86f2ddeb'),1)
check('new tool timeout raised',original.replace('name: Prepare pinned Yosys\n    runs-on: ubuntu-24.04\n    timeout-minutes: 30','name: Prepare pinned Yosys\n    runs-on: ubuntu-24.04\n    timeout-minutes: 45'),1)
check('restored control',original,0)
print('Generated-workflow drift probes: PASS')
