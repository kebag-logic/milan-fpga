#!/usr/bin/env python3
import pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]);packet=pathlib.Path(sys.argv[2]);v=sys.argv[3]
out=packet/'focused';out.mkdir(exist_ok=True)
cmd=['make','-j16','VERILATOR='+v,'VERILATOR_JOBS=12','run']
with (out/'gptp-shadow.log').open('w') as f:
 f.write('$ '+' '.join(cmd)+'\n');f.flush()
 rc=subprocess.run(cmd,cwd=root/'tb/verilator/gptp_shadow',stdout=f,stderr=subprocess.STDOUT).returncode
(out/'gptp-shadow.rc').write_text(str(rc)+'\n');print('gptp-shadow',rc)
sys.exit(rc)
