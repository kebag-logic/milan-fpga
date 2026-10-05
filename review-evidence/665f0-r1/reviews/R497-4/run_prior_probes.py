#!/usr/bin/env python3
"""Rerun immutable public probes, applying only the obsolete mutation-site relocation.
Usage: python3 run_prior_probes.py REPO PACKET
The capacity probe changes its oracle to round-4's publicly authorized rule.
"""
import concurrent.futures, pathlib, runpy, shutil, subprocess, sys
repo,packet=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3])
out=packet/'scratch/prior-rerun';out.mkdir(parents=True,exist_ok=True)
sys.argv=[str(packet/'prior-probes/adp_reviewer_mutants.py'),str(repo),str(out)]
m=runpy.run_path(sys.argv[0])
mutants=m['M'].copy()
rel,old,new=mutants['second-shutdown-overwrites-index']
assert old.count('a->departing_owed != UINT32_MAX')==1
mutants['second-shutdown-overwrites-index']=(rel,old.replace('a->departing_owed != UINT32_MAX','a->departing_owed < ADP_DEPARTING_OWED_MAX'),new.replace('a->departing_owed != UINT32_MAX','a->departing_owed < ADP_DEPARTING_OWED_MAX'))
def build_run(name,ctrl,main,args=()):
    exe=out/name
    argv=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-pedantic',*[f'-I{ctrl/d}' for d in m['INC']],*[str(ctrl/s) for s in m['SRC']],str(main),'-o',str(exe)]
    b=subprocess.run(argv,capture_output=True,text=True)
    assert b.returncode==0,b.stderr
    r=subprocess.run([str(exe),*args],capture_output=True,text=True,timeout=540)
    log=(r.stdout+r.stderr).replace(str(repo),'$REPO').replace(str(packet/'scratch'),'$SCRATCH')
    (packet/(name+'.log')).write_text(log);(packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
    return r.returncode,log
ctrl=repo/'sw/firmware/ctrl'
def job(name):
    if name=='prior-bound':
        rc,log=build_run(name,ctrl,packet/'prior-probes/probe_owed_bound.c')
        import re
        rows=re.findall(r'PROBE k=(\d+) room_first=(\d+) owed_departing=(\d+) available_committed_in_pass=(\d+).*?accesses_from_room=(\d+)',log)
        assert rc==0 and len(rows)==12,log
        for k,room,n,p,a in rows:
            assert int(n)==min(int(k),2) and int(p)==min(int(k),2)+1 and int(a)<=1628,(k,room,n,p,a)
        return name,'PASS: 12 rows match capped k+1 bound'
    if name=='prior-rules':
        rc,log=build_run(name,ctrl,packet/'prior-probes/probe_owed_rules.c')
        assert rc==0 and 'DEPARTING(1) delivered' in log and 'L2 state=3 timer=2' in log and 'L3 sends_before_TMR_DELAY=0' in log,log
        return name,'PASS: L1-L3 outcomes'
    if name=='capacity-rule':
        rc,log=build_run(name,ctrl,packet/'capacity_rule_probe.c',['4294967296'])
        assert rc==0,log
        return name,'PASS: 2 owed + 4294967294 coalesced'
    rel,old,new=mutants[name]
    copy=out/name/'ctrl';shutil.copytree(ctrl,copy,ignore=shutil.ignore_patterns('__pycache__'))
    f=copy/rel;s=f.read_text();assert s.count(old)==1,(name,s.count(old));f.write_text(s.replace(old,new))
    rc,log=build_run('mutant-'+name,copy,copy/'test/test_adp.c')
    fails=[ln for ln in log.splitlines() if '[FAIL]' in ln]
    assert rc==1 and fails,(name,rc,log)
    return name,'CAUGHT: '+fails[0].strip()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(job,['prior-bound','prior-rules','capacity-rule',*mutants]))
lines=['Public probe origin: 9c149b82fd15cdcd5502382a8390a9e9c7f2aca9; source blobs in prior-probes/origin.json.', 'The second-SHUTDOWN mutation is relocated from the old UINT32_MAX guard to ADP_DEPARTING_OWED_MAX; its assignment is unchanged.']
lines += [name+': '+verdict for name,verdict in results]
lines += ['RESULT: PASS; 8/8 prior reviewer mutants compile, execute, and fail checks.']
(packet/'prior-probes-summary.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
