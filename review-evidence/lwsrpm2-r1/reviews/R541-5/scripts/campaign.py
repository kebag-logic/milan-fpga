# SPDX-License-Identifier: Apache-2.0
"""Foreground bounded campaigns. Builds and suites have separate logs and codes."""
import argparse, concurrent.futures, importlib.util, os, pathlib, shutil, sys
sys.dont_write_bytecode = True
from run_common import ROOT, PACKET, SCRATCH, run
parser=argparse.ArgumentParser()
parser.add_argument('--jobs',type=int,default=2)
args=parser.parse_args()
assert 1 <= args.jobs <= 2
prefix=SCRATCH/'prefix'
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib');env['PYTHONDONTWRITEBYTECODE']='1'
spec=importlib.util.spec_from_file_location('reversals',ROOT/'tests/check_reversals.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
labels=['pending-flush','flush-before-refresh','flush-deadline','flush-observer',
        'replacement-lv','replacement-leave-timer','receive-instance-stop','flush-completion',
        'flush-retry','replacement-order','receive-stop','registrar-recovery-indication',
        'callback-order','propagation-retention','milan-delayed-in-leave','milan-restarted-lv-deadline']
selected=[c for c in module.CASES if c[0] in labels]
assert len(selected)==len(labels)
def profile(mode):
    source=SCRATCH/('source-'+mode);source.mkdir()
    for name in ['CMakeLists.txt','src','tests']:
        p=ROOT/name
        if p.is_dir():shutil.copytree(p,source/name,ignore=shutil.ignore_patterns('__pycache__'))
        else:shutil.copy2(p,source/name)
    build=SCRATCH/('build-'+mode)
    def command(label,args,**kw):return run(mode+'-'+label,args,env=env,**kw)
    assert command('configure',['cmake','-S',source,'-B',build,'-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_PREFIX_PATH='+str(prefix),'-DLWSRP_MILAN='+mode])[0]==0
    buildcmd=['cmake','--build',build,'--parallel','4']
    assert command('build',buildcmd)[0]==0
    assert command('ctest',['ctest','--test-dir',build,'--output-on-failure'])[0]==0
    assert command('units',[build/'unit_tests'])[0]==0
    scenario_env=env|{'SHLAN_LIBRARY':str(build/'libshlan.so')}
    assert run(mode+'-scenarios',['behave'],env=scenario_env)[0]==0
    exe=SCRATCH/('probe-'+mode)
    compilecmd=['cc','-std=c11','-Wall','-Wextra','-I'+str(ROOT/'src/include'),'-I'+str(ROOT/'src'),'-I'+str(ROOT/'tests/unit'),PACKET/'scripts/probe.c',ROOT/'tests/unit/fault_alloc.c','-L'+str(build),'-Wl,-rpath,'+str(build),'-lshlan','-o',exe]
    assert command('probe-build',compilecmd)[0]==0
    assert command('probe',[exe])[0]==0
    for label,name,old,new,check in selected:
        path=source/name;original=path.read_text();assert old in original
        try:
            path.write_text(original.replace(old,new))
            assert command(label+'-build',buildcmd)[0]==0
            rc,out=command(label,[build/'unit_tests'])
            required=module.REQUIRED_FAILURES.get(label,[])
            assert rc!=0 and 'Failure:' in out and all(test in out for test in required),(label,rc,required)
            if label in ['pending-flush','flush-before-refresh','flush-observer','flush-deadline']:
                assert command(label+'-probe',[exe])[0]!=0
        finally:path.write_text(original)
    # Reviewer mutation: only JoinMt bypasses pending withdrawal; JoinIn still works.
    path=source/'src/core/mrp_mad.c';original=path.read_text()
    old='if (previous && previous->flush_pending) {'
    new='if (previous && previous->flush_pending && attr_event != MRP_ATTR_EVENT_JOINMT) {'
    assert old in original
    try:
        path.write_text(original.replace(old,new))
        assert command('own-joinmt-build',buildcmd)[0]==0
        rc,out=command('own-joinmt',[build/'unit_tests']);assert rc!=0 and 'pending_flush_precedes_received_registration' in out
        assert command('own-joinmt-probe',[exe])[0]!=0
    finally:path.write_text(original)
    assert command('restored-build',buildcmd)[0]==0
    assert command('restored-ctest',['ctest','--test-dir',build,'--output-on-failure'])[0]==0
    assert command('restored-probe',[exe])[0]==0
    print(mode,'PASS',len(selected),'sampled reversals + own selective JoinMt mutation',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    futures=[pool.submit(profile,m) for m in ['OFF','ON']]
    for f in futures:f.result()
