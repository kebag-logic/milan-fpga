# SPDX-License-Identifier: Apache-2.0
"""Confirm the surviving two-tick plant against the earlier independent probe."""
import argparse, concurrent.futures as cf, os, shutil, subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,default=2)
a=p.parse_args()
src,packet=a.source.resolve(),a.packet.resolve()
def run(mode):
    work=packet/'scratch'/('deadline-'+mode)
    work.mkdir()
    shutil.copytree(src/'src',work/'src')
    f=work/'src/core/mrp_mad.c'
    old='ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);'
    original=f.read_text()
    assert original.count(old)==1
    f.write_text(original.replace(old,old.replace('1u','2u')))
    cmd=['cc','-std=c11','-O1','-g','-no-pie','-fsanitize=address,undefined','-fno-omit-frame-pointer',
        '-DLWSRP_MILAN='+('1' if mode=='ON' else '0'),'-Isrc/include','-Isrc',
        str(packet/'scripts/probe_r3.c'),str(packet/'scripts/probe_alloc.c'),
        'src/core/mrp_mad.c','src/core/mrp_pdu.c','src/ports/timer.c','src/modules/msrp.c','-o',str(work/'probe')]
    env=os.environ|{'ASAN_OPTIONS':'detect_leaks=1:abort_on_error=1'}
    for label,command in [('deadline-plant-build-'+mode,cmd),('deadline-plant-probe-'+mode,[str(work/'probe')])]:
        r=subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,timeout=180)
        out=(r.stdout+r.stderr).replace(str(packet),'$PACKET').replace(str(src),'$SOURCE')
        (packet/'receipts'/(label+'.log')).write_text(out)
        (packet/'receipts'/(label+'.rc')).write_text(str(r.returncode)+'\n')
        print(label,r.returncode, out[-100:],flush=True)
    f.write_text(original)
    assert f.read_bytes()==(src/'src/core/mrp_mad.c').read_bytes()
with cf.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as pool:
    list(pool.map(run,['OFF','ON']))
