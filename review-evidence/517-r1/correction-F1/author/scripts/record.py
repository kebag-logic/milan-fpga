import json,os,subprocess,sys,time
from pathlib import Path
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);cmd=sys.argv[2:]; start=time.time()
with (out/'stdout').open('wb') as stdout,(out/'stderr').open('wb') as stderr:
 p=subprocess.run(cmd,stdout=stdout,stderr=stderr)
row={'argv':cmd,'cwd':os.getcwd(),'environment':{k:os.environ.get(k) for k in ('PATH','MAKEFLAGS','MFLAGS','VERILATOR_JOBS','SIM_JOBS','TMPDIR','MILAN_COUNTER_FRAME_OUT')},'start_utc':start,'elapsed_s':time.time()-start,'exit':p.returncode}
(out/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row));sys.exit(p.returncode)
