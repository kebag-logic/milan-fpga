#!/usr/bin/env python3
"""Check generated pin records and regenerate owned outputs in a disposable clone."""
import pathlib, subprocess, sys, os
root=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
os.environ['TMPDIR']=str(out.parent/'scratch')
commands=[
 ('rom-record',['bash','syn/yosys/ooc.sh','--record-rom-digests']),
 ('port-record',['python3','scripts/check_port_contracts.py','--write-budget']),
 ('boundaries-regenerate',['python3','docs/diagrams/submodule_boundaries.gen.py']),
 ('timesync-regenerate',['python3','docs/diagrams/timesync_chain.gen.py']),
 ('boundaries-check',['python3','docs/diagrams/submodule_boundaries.gen.py','--check']),
 ('timesync-check',['python3','docs/diagrams/timesync_chain.gen.py','--check']),
 ('submodule-docs',['python3','scripts/check_submodule_docs.py']),
 ('gptp-docs',['python3','scripts/check_gptp_docs.py','--with-submodule']),
 ('port-contracts',['python3','scripts/check_port_contracts.py']),
 ('tracked-diff',['git','diff','--exit-code','HEAD']),
]
failed=[]
for name,cmd in commands:
 with (out/(name+'.log')).open('w') as f:
  f.write('$ '+' '.join(cmd)+'\n');f.flush()
  rc=subprocess.run(cmd,cwd=root,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/(name+'.rc')).write_text(str(rc)+'\n')
 print(name,rc,flush=True)
 if rc: failed.append(name)
print('failed:',failed)
sys.exit(bool(failed))
