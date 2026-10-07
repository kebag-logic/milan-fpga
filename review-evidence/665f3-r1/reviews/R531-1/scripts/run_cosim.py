#!/usr/bin/env python3
import io,os,shutil,subprocess,sys,tarfile
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve();verilator=Path(sys.argv[3]).resolve()
work=packet/'scratch/cosim'
if work.exists(): shutil.rmtree(work)
work.mkdir(parents=True)
version=subprocess.check_output([str(verilator),'--version'],text=True)
assert 'Verilator 5.050 ' in version,version
(packet/'receipts/cosim-tool-identity.txt').write_text(version)
data=subprocess.check_output(['git','archive','HEAD','hdl/milan/mailbox','sw/firmware/ctrl','sw/firmware/ctrl_nvm','tb/common','tb/verilator/mbx'],cwd=root)
with tarfile.open(fileobj=io.BytesIO(data)) as archive: archive.extractall(work,filter='data')
wrapper=work/'verilator-capped'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\na=["8" if x=="0" and i>0 and a[i-1]=="-j" else x for i,x in enumerate(a)]\nos.execv('+repr(str(verilator))+',['+repr(str(verilator))+']+a)\n')
wrapper.chmod(0o755)
cmd=['make','--silent','-j16','run-cosim','VERILATOR='+str(wrapper)]
with (packet/'receipts/cosim.log').open('w') as f:
 f.write('Fresh git archive of reviewed HEAD. make -j16 run-cosim; compiler build jobs capped at 8.\n'+version);f.flush()
 rc=subprocess.run(cmd,cwd=work/'tb/verilator/mbx',stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'MAKEFLAGS':'--silent'}).returncode
(packet/'receipts/cosim.rc').write_text(str(rc)+'\n')
print('cosim rc',rc);sys.exit(rc)
