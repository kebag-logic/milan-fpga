import importlib.util,json,subprocess,sys
from pathlib import Path
lane=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
suite=lane/'tb/verilator/milan_dp';sys.path.insert(0,str(suite))
import test_sim_pool_backpressure as test
old=subprocess.check_output(['git','-C',str(lane),'show','5874895eb817ed41c0f8be4eb427ad3315c29844:tb/verilator/milan_dp/sim_pool.py'])
(out/'restored-sim_pool.py').write_bytes(old)
original=test.prepare

def prepare(case,recipe,body):
 result=original(case,recipe,body);(case.dir/'sim_pool.py').write_bytes(old);return result
test.prepare=prepare
assert test.ctypes.CDLL(None).prctl(36,1,0,0,0)==0
rows=[]
for recipe in (False,True):
 for flush in (False,True):
  for sig in (test.signal.SIGINT,test.signal.SIGTERM):
   name=f"{recipe}-{flush}-{sig.name}";reason=None
   try:test.exercise(out/name,recipe,flush,sig,'active')
   except AssertionError as exc:reason=str(exc)
   row={'case':name,'rejected':reason=='runner did not shut down while stdout stayed blocked','reason':reason};rows.append(row);print(json.dumps(row),flush=True)
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
assert len(rows)==8 and all(row['rejected'] for row in rows)
