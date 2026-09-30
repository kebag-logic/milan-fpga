"""Complete a separately built capture using its ordinary native driver and grader.

PR #609's `run_capture_native.py` with this lane's root; nothing else differs."""
from pathlib import Path
import json
import subprocess
import sys
root=Path('$LANES/70-lane2-pin')
sys.path.insert(0,str(root/'tb/verilator/nvm_capture_cpu'))
import run
build=Path(sys.argv[1])
spec=json.loads((build/'sources.json').read_text())
with (build/'capture.log').open('w') as log:
    result=subprocess.run(['$WORKSPACE_HOME/.local/bin/rtk', 'proxy','timeout','28800',str(build/'native/Vsim')],
                          cwd=build/'gateware',stdout=log,stderr=subprocess.STDOUT)
if len(sys.argv)>2:
    spec['baseline_measurement']=sys.argv[2]
run._grade(build,spec,result.returncode)
