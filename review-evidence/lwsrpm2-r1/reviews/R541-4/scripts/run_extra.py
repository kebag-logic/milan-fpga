# SPDX-License-Identifier: Apache-2.0
"""Supplementary source-list, freestanding, and native-policy checks."""
import argparse, concurrent.futures as cf, json, os, subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args()
src,packet=a.source.resolve(),a.packet.resolve()
scratch=packet/'scratch'
prefix=scratch/'deps'
env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(scratch),'LD_LIBRARY_PATH':str(prefix/'lib'),'ASAN_OPTIONS':'detect_leaks=1:abort_on_error=1'}
def run(label,cmd,extra=None,stdin=None):
    r=subprocess.run(list(map(str,cmd)),cwd=src,env=env|(extra or {}),input=stdin,capture_output=True,text=True,timeout=540)
    out=(r.stdout+r.stderr).replace(str(src),'$SOURCE').replace(str(packet),'$PACKET')
    (packet/'receipts'/(label+'.log')).write_text(out)
    (packet/'receipts'/(label+'.rc')).write_text(str(r.returncode)+'\n')
    print(label,r.returncode,out[-180:],flush=True)
def native(mode):
    b=scratch/('native-'+mode)
    run('native-build-'+mode,['cc','-std=c11','-g','-O1','-no-pie','-fsanitize=address,undefined','-fno-omit-frame-pointer','-DLWSRP_MILAN='+('1' if mode=='ON' else '0'),'-Isrc/include','-Isrc',packet/'scripts/probe_r4_native.c',packet/'scripts/probe_alloc.c','src/core/mrp_mad.c','src/core/mrp_pdu.c','src/ports/timer.c','src/modules/msrp.c','-o',b])
    run('native-'+mode,[b])
def codec():
    b=scratch/'codec'
    run('codec-build',['cc','-std=c11','-Isrc/include','-I'+str(prefix/'include'),'tests/unit/mrp_pdu_test.c','src/core/mrp_pdu.c','-xc','-','-L'+str(prefix/'lib'),'-lcgreen','-o',b],stdin='#include <cgreen/cgreen.h>\nTestSuite *mrp_pdu_suite(void);\nint main(void) { return run_test_suite(mrp_pdu_suite(), create_text_reporter()); }\n')
    run('codec',[b])
with cf.ThreadPoolExecutor(max_workers=min(a.jobs,4)) as pool:
    fs=[pool.submit(native,m) for m in ['OFF','ON']]
    fs += [pool.submit(codec),pool.submit(run,'freestanding-OFF',['python3','tests/check_freestanding.py']),pool.submit(run,'freestanding-ON',['python3','tests/check_freestanding.py'],{'CC':'cc -DLWSRP_MILAN=1'}),pool.submit(run,'embedded',['python3','tests/check_embedded.py','--work-dir',scratch/'embedded']),pool.submit(run,'scenario-dry',['behave','--dry-run'])]
    for f in fs: f.result()
