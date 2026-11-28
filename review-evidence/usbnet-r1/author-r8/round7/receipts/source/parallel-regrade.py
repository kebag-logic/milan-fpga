"""Call the unchanged per-group grader concurrently; require identical outputs."""
import concurrent.futures,hashlib,json,multiprocessing,sys
from pathlib import Path
root=Path.cwd();packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import run
original=run.graded
expected=json.loads((packet/'pre-parallel-grade-hashes.json').read_text())
def one(job):
 group,log,spec,out=job
 result=original([group],[log],spec,out)
 key=out.parent.name+'/'+group.name;path=out/(group.name+'.json')
 assert hashlib.sha256(path.read_bytes()).hexdigest()==expected[key],('grade changed',key)
 return result
def parallel(groups,logs,spec,out):
 assert len({g.name for g in groups})==len(groups)
 with concurrent.futures.ProcessPoolExecutor(max_workers=min(8,len(groups)),mp_context=multiprocessing.get_context('fork')) as pool:
  parts=list(pool.map(one,[(g,l,spec,out) for g,l in zip(groups,logs)]))
 # run.graded's only list-level missing-notice check is a per-group comprehension;
 # ordered concatenation is identical. All later cross-group checks remain in run.main.
 return tuple([item for part in parts for item in part[i]] for i in range(3))
if __name__=='__main__':
 run.graded=parallel
 raise SystemExit(run.main())
