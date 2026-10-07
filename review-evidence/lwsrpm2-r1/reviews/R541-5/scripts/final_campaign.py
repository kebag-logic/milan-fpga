# SPDX-License-Identifier: Apache-2.0
import argparse,concurrent.futures,importlib.util,os,sys
sys.dont_write_bytecode = True
from run_common import *
parser=argparse.ArgumentParser();parser.add_argument('--jobs',type=int,default=2);args=parser.parse_args()
assert 1<=args.jobs<=2
prefix=SCRATCH/'prefix';env=os.environ|{'LD_LIBRARY_PATH':str(prefix/'lib'),'PYTHONDONTWRITEBYTECODE':'1'}
spec=importlib.util.spec_from_file_location('r',ROOT/'tests/check_reversals.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def profile(mode):
    build=SCRATCH/('build-'+mode);source=SCRATCH/('source-'+mode);exe=SCRATCH/('probe-'+mode)
    def cmd(label,a,**kw):return run(mode+'-'+label,a,env=env,**kw)
    compilecmd=['cc','-std=c11','-I'+str(ROOT/'src/include'),'-I'+str(ROOT/'src'),'-I'+str(ROOT/'tests/unit'),PACKET/'scripts/probe.c',ROOT/'tests/unit/fault_alloc.c','-L'+str(build),'-Wl,-rpath,'+str(build),'-lshlan','-o',exe]
    assert cmd('final-probe-build',compilecmd)[0]==0
    assert cmd('final-probe',[exe])[0]==0
    rc,out=cmd('cross-port',[exe,'cross-port']);assert rc==1 and '36 value mismatches' in out
    for label,name,old,new,check in r.CASES:
        if label not in ['replacement-lv','replacement-leave-timer','receive-instance-stop']:continue
        path=source/name;original=path.read_text();assert old in original
        try:
            path.write_text(original.replace(old,new))
            assert cmd('own-edges-'+label+'-build',['cmake','--build',build,'--parallel','4'])[0]==0
            assert cmd('own-edges-'+label,[exe])[0]!=0
        finally:path.write_text(original)
    assert cmd('edges-restored-build',['cmake','--build',build,'--parallel','4'])[0]==0
    assert cmd('edges-restored-probe',[exe])[0]==0
    assert cmd('edges-restored-ctest',['ctest','--test-dir',build,'--output-on-failure'])[0]==0
    san=SCRATCH/('san-'+mode)
    flags='-fsanitize=address,undefined -fno-omit-frame-pointer'
    assert cmd('san-configure',['cmake','-S',source,'-B',san,'-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_PREFIX_PATH='+str(prefix),'-DLWSRP_MILAN='+mode,'-DCMAKE_C_FLAGS='+flags,'-DCMAKE_EXE_LINKER_FLAGS='+flags,'-DCMAKE_SHARED_LINKER_FLAGS='+flags])[0]==0
    assert cmd('san-build',['cmake','--build',san,'--parallel','4'])[0]==0
    assert cmd('san-units',[san/'unit_tests'])[0]==0
    sanexe=SCRATCH/('san-probe-'+mode)
    sancmd=['cc','-std=c11','-fsanitize=address,undefined','-fno-omit-frame-pointer','-I'+str(ROOT/'src/include'),'-I'+str(ROOT/'src'),'-I'+str(ROOT/'tests/unit'),PACKET/'scripts/probe.c',ROOT/'tests/unit/fault_alloc.c','-L'+str(san),'-Wl,-rpath,'+str(san),'-lshlan','-o',sanexe]
    assert cmd('san-probe-build',sancmd)[0]==0
    assert cmd('san-probe',[sanexe])[0]==0
    rc,out=cmd('san-cross-port',[sanexe,'cross-port']);assert rc==1 and '36 value mismatches' in out and 'runtime error:' not in out and 'ERROR: AddressSanitizer' not in out
with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    fs=[pool.submit(profile,m) for m in ['OFF','ON']]
    for f in fs:f.result()
