#!/usr/bin/env python3
"""Focused processor suites in a disposable tree; CHECKOUT PACKET EXECUTABLE."""
import concurrent.futures,io,os,pathlib,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); exe=pathlib.Path(sys.argv[3]).resolve()
identity=subprocess.check_output([str(exe),'--version'],text=True)
assert '5.050' in identity
(packet/'simulator-identity.log').write_text(identity)
work=packet/'scratch/processor-focused'; work.mkdir(exist_ok=True)
raw=subprocess.check_output(['git','-C',str(root/'protocol-processor'),'archive','2cbed0a987c1e68402658d69459ab7e5aa571adc'])
with tarfile.open(fileobj=io.BytesIO(raw)) as archive: archive.extractall(work,filter='data')
# Bound each of four concurrent builds to four workers, including nested builds.
wrapper=packet/'scratch/bounded-simulator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j": a[i+1]="4"\nos.execv('+repr(str(exe))+',['+repr(str(exe))+']+a)\n')
wrapper.chmod(0o755)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
def run(name):
 cmd=['make','-j16','VERILATOR='+str(wrapper)]
 with (packet/(name+'.log')).open('w') as log:
  log.write('SUITE protocol-processor/tb/'+name+' at 2cbed0a987c1e68402658d69459ab7e5aa571adc; make -j16; four compile workers\n'); log.flush()
  rc=subprocess.run(cmd,cwd=work/'tb'/name,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (packet/(name+'.rc')).write_text(str(rc)+'\n'); print(name,rc,flush=True); return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: codes=list(pool.map(run,['acmp_listener','acmp_talker','tx_arbiter','aecp_notify']))
sys.exit(any(codes))
