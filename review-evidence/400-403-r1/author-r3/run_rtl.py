from pathlib import Path
import subprocess, sys
out=Path(__file__).resolve().parent
steps=[('csr',['make','-C','tb/verilator/csr']),
       ('pp-shadow',['make','-C','tb/verilator/pp_shadow']),
       ('dp-prereq',['make','-C','tb/verilator/milan_dp','-f','Makefile','-f',str(out/'dp-chunks.mk'),'a316-prereq'])]
for n in range(1,36):
    steps.append((f'dp-{n:02d}', ['make','-C','tb/verilator/milan_dp','-f','Makefile','-f',str(out/'dp-chunks.mk'),f'a316-step-{n:02d}']))
for name,cmd in steps:
    rc=subprocess.run([sys.executable,str(out/'run_gate.py'),name,*cmd],timeout=43200).returncode
    if rc:
        sys.exit(rc)
