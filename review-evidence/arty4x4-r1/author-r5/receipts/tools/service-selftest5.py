import concurrent.futures,json,subprocess,sys
from pathlib import Path
R=Path('$VALIDATION_STORAGE/arty4x4-a863/gates5')
code="import sys; sys.path.insert(0,'tb/verilator/ctrl_service_budget'); import selftest; n=int(sys.argv[1]); selected=list(selftest.selftest_mutants.MUTANTS.items())[n::8]; print('PARTITION',n,'OF 8',len(selected),flush=True); selftest.selftest_mutants.MUTANTS=dict(selected); raise SystemExit(selftest.main([]))"
def one(n):
 with (R/f'service-selftest-{n}.log').open('w') as log: rc=subprocess.run([sys.executable,'-B','-c',code,str(n)],stdout=log,stderr=subprocess.STDOUT).returncode
 print('SELFTEST',n,rc,flush=True);return dict(partition=n,rc=rc)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(one,range(8)))
(R/'service-selftest.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(any(row['rc'] for row in rows))
