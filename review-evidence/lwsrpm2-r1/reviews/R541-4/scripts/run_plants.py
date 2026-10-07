# SPDX-License-Identifier: Apache-2.0
"""Replay the public round-three plants without changing their definitions."""
import argparse, concurrent.futures as cf, json, os, subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args()
src,packet=a.source.resolve(),a.packet.resolve()
def run(mode):
    work=packet/'scratch'/('plants-'+mode)
    r=subprocess.run(['python3',str(packet/'scripts/plants_r3.py'),str(src),str(work),str(packet/'scratch/deps'),mode,str(max(1,min(a.jobs//2,4)))],capture_output=True,text=True,timeout=540,env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(packet/'scratch')})
    dest=packet/'receipts'/('plants-'+mode)
    dest.mkdir(exist_ok=True)
    def clean(s): return s.replace(str(src),'$SOURCE').replace(str(packet),'$PACKET')
    (dest/'campaign.log').write_text(clean(r.stdout+r.stderr))
    (dest/'campaign.rc').write_text(str(r.returncode)+'\n')
    for f in work.glob('*/*.log'):
        (dest/(f.parent.name+'-'+f.name)).write_text(clean(f.read_text()))
    print(mode, 'rc',r.returncode, r.stdout, r.stderr,flush=True)
with cf.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(run,['OFF','ON']))
