# SPDX-License-Identifier: Apache-2.0
"""Compile literal-wire and allocation probes against the frozen source."""
import argparse
from pathlib import Path
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,default=2)
a=p.parse_args();source=a.source.resolve();packet=a.packet.resolve()
def run(label,command):
    r=subprocess.run(list(map(str,command)),cwd=source,capture_output=True,text=True,timeout=120)
    output=r.stdout+r.stderr
    output=output.replace(str(source),'$SOURCE').replace(str(packet),'$PACKET')
    (packet/'receipts'/f'{label}.log').write_text(output)
    (packet/'receipts'/f'{label}.rc').write_text(str(r.returncode)+'\n')
    (packet/'receipts'/f'{label}.command.json').write_text(json.dumps([str(x).replace(str(source),'$SOURCE').replace(str(packet),'$PACKET') for x in command],indent=2)+'\n')
    print(label,'rc',r.returncode,output.strip(),flush=True)
    return r.returncode
def profile(mode):
    exe=packet/'scratch'/f'probe-{mode}'
    cmd=['cc','-std=c11','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer',
        '-DLWSRP_MILAN='+str(int(mode=='ON')),'-Isrc/include','-Isrc',packet/'scripts/probe.c',
        'src/core/mrp_mad.c','src/core/mrp_pdu.c','src/modules/mvrp.c','src/modules/mmrp.c',
        'src/modules/msrp.c','src/ports/timer.c','-o',exe]
    assert run('probe-build-'+mode,cmd)==0
    for name in ['atomic','extensions','overflow','retention','recovery','order','allocation','allocation-control']:
        run(f'probe-{name}-{mode}',[exe,name])
with ThreadPoolExecutor(max_workers=min(a.jobs,2)) as pool:
    list(pool.map(profile,['OFF','ON']))
