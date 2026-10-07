import concurrent.futures,json,pathlib,shutil,sys
root=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build as b, ctrl_arms, acmp_review_mutants as defs, fw_gtest
names=['acmp-slot-sum-wraps','acmp-one-slot-for-all-interfaces','acmp-record-flag-defines-swapped','acmp-longer-record-applied','acmp-nvm-d3-rollback-drops-bindings','acmp-due-unsigned','acmp-earliest-unsigned','acmp-owed-probe-timer-runs','acmp-version-unchecked']
def run(name):
    m=next(m for m in defs.MUTANTS if m.name==name); out=p/'scratch/native-mutations'/name
    src=out/'ctrl'; shutil.copytree(b.CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
    f=src/m.path;s=f.read_text(); assert s.count(m.old)==1,(name,s.count(m.old));f.write_text(s.replace(m.old,m.new))
    t=b.Tree(src,out/'build',p/'scratch/native/reuse',fw_gtest.Build(jobs=4))
    result=getattr(ctrl_arms,'arm_'+m.arm)(t)
    (p/'receipts'/('regression-'+name+'.log')).write_text(result.log)
    (p/'receipts'/('regression-'+name+'.rc')).write_text(str(result.rc)+'\n')
    caught=result.rc!=0 and '[FAIL] '+m.test in result.log and m.needle in result.log
    print(name,caught,flush=True)
    return dict(name=name,rc=result.rc,caught=caught,expected_test=m.test,expected_text=m.needle)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,names))
(p/'receipts/native-regression-mutations.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(int(not all(x['caught'] for x in results)))
