#!/usr/bin/env python3
"""Run the unchanged harness checks and each mutation in exactly one process partition."""
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path
root,packet=(Path(v).resolve() for v in sys.argv[1:3])
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_mutants
names=list(selftest_mutants.MUTANTS)
count=8
if len(sys.argv)>3:
    index=int(sys.argv[3])
    selftest_mutants.MUTANTS={name:selftest_mutants.MUTANTS[name] for name in names[index::count]}
    raise SystemExit(selftest.main([]))
assert sorted(n for k in range(count) for n in names[k::count])==sorted(names)
def one(index):
    log=packet/f'harness-shard-{index}.log'
    with log.open('w') as sink:
        result=subprocess.run([sys.executable,'-B',__file__,str(root),str(packet),str(index)],
                              stdout=sink,stderr=subprocess.STDOUT)
    (packet/f'harness-shard-{index}.rc').write_text(str(result.returncode)+'\n')
    text=log.read_text()
    caught=sum(line.startswith('MUTANT caught:') for line in text.splitlines())
    assert caught==len(names[index::count]),(index,caught)
    assert result.returncode==0 and 'self-test: 0 failures' in text,index
    return dict(shard=index,rc=result.returncode,mutations=caught)
with concurrent.futures.ThreadPoolExecutor(max_workers=count) as pool:
    results=list(pool.map(one,range(count)))
summary=dict(mutations=len(names),disjoint_complete_partition=True,shards=results,
             baseline_checks='unchanged complete checks in every process')
(packet/'harness-parallel.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
