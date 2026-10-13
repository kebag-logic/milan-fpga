#!/usr/bin/env python3
"""Re-run the F3b, ADP, and publication plants, without a full bank."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import sys

def worker(task):
    repo,packet,names = task
    repo,packet=Path(repo),Path(packet)
    sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
    import ctrl_mutants as m
    import ctrl_arms as a
    import ctrl_build as b
    import ctrl_reuse
    import fw_gtest
    root=packet/'scratch'/('controls-'+names[0])
    ctrl_reuse.cut_reuse(root/'reuse')
    b.stack_pin()
    build=fw_gtest.Build(jobs=4)
    receipts=packet/'controls'
    receipts.mkdir(exist_ok=True)
    results=[]
    for plant in [v for v in m.MUTANTS if v.name in names]:
        ctrl,stack=m.plant(plant,root)
        tree=b.Tree(ctrl,root/'work/build',root/'reuse',build,stack)
        passed=True
        for index,(arm,test,needle) in enumerate(plant.kills()):
            try:
                outcome=getattr(a,'arm_'+arm)(tree)
            except b.Refusal as exc:
                outcome=b.Outcome(arm,2,str(exc))
            caught=m.caught(test,needle,outcome)
            passed=passed and caught
            name=f'{plant.name}-{index}'
            (receipts/(name+'.log')).write_text(outcome.log)
            (receipts/(name+'.json')).write_text(json.dumps({'plant':plant.name,'arm':arm,'test':test,'needle':needle,'rc':outcome.rc,'caught':caught},indent=2)+'\n')
        row={'plant':plant.name,'caught':passed}
        print(json.dumps(row),flush=True)
        results.append(row)
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--packet',type=Path,required=True)
    p.add_argument('--jobs',type=int,default=2)
    args=p.parse_args()
    sys.path.insert(0,str(args.repo.resolve()/'sw/firmware/ctrl/test'))
    import ctrl_mutants
    names=[m.name for m in ctrl_mutants.MUTANTS if m.name.startswith(('f3b-','pin-adp-','pub-maap-','rv-maap-gate'))]
    print('Full table',len(ctrl_mutants.MUTANTS),'selected',len(names),flush=True)
    count=min(args.jobs,2)
    tasks=[(str(args.repo.resolve()),str(args.packet.resolve()),names[i::count]) for i in range(count)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=count) as pool:
        rows=[r for part in pool.map(worker,tasks) for r in part]
    (args.packet/'controls-results.json').write_text(json.dumps(rows,indent=2)+'\n')
    sys.exit(any(not r['caught'] for r in rows))
