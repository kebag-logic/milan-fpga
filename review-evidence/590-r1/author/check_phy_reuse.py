"""Prove that a changed PHY peer source refuses reuse before native execution."""
from pathlib import Path
import subprocess
root=Path.cwd()
base=Path('/tmp/a385-final3-service-1x1')
command=['rtk','proxy','timeout','60','$WORKSPACE_HOME/litex-milan/venv/bin/python','-B',
         'tb/verilator/fw_service_budget/run.py','--shape','endstation_ax7101_1x1_tdm8',
         '--build-dir',str(base),'--reuse-build','--build-only']
subprocess.run(command,check=True)
for name,comment in (('phy.py',b'\n# Reuse binding control.\n'),('phy.hpp',b'\n// Reuse binding control.\n')):
    path=root/'tb/verilator/fw_service_budget'/name
    original=path.read_bytes()
    try:
        path.write_bytes(original+comment)
        result=subprocess.run(command,capture_output=True,text=True)
        assert result.returncode != 0 and 'stale or unbound build; rebuild' in result.stderr,(name,result)
        print(name,'changed-source refusal PASS',flush=True)
    finally:
        path.write_bytes(original)
    subprocess.run(command,check=True)
print('PHY reuse inventory: two negative and three positive checks PASS')
