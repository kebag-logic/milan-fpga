# SPDX-License-Identifier: Apache-2.0
"""Run from a fresh packet containing scripts; products stay in packet/scratch."""
import argparse, concurrent.futures as cf, hashlib, os, subprocess, tarfile, urllib.request
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1])
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args()
src,packet=a.source.resolve(),a.packet.resolve()
scratch=packet/'scratch'
scratch.mkdir(exist_ok=True)
(packet/'receipts').mkdir(exist_ok=True)
archive=scratch/'cgreen.tar.gz'
if not archive.exists():
    urllib.request.urlretrieve('https://api.github.com/repos/cgreen-devs/cgreen/tarball/1.6.3',archive)
with tarfile.open(archive) as t:
    names=t.getnames()
    t.extractall(scratch,filter='data')
dep=scratch/names[0].split('/')[0]
for label,cmd in [
    ('configure',['cmake','-S',dep,'-B',scratch/'cgreen-build','-DCMAKE_POLICY_VERSION_MINIMUM=3.5','-DCMAKE_INSTALL_PREFIX='+str(scratch/'deps')]),
    ('build',['make','-C',scratch/'cgreen-build','-j16']),
    ('install',['make','-C',scratch/'cgreen-build','-j16','install'])]:
    r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,timeout=540)
    (packet/'receipts'/('dependency-'+label+'.log')).write_text((r.stdout+r.stderr).replace(str(packet),'$PACKET'))
    (packet/'receipts'/('dependency-'+label+'.rc')).write_text(str(r.returncode)+'\n')
    if r.returncode: raise SystemExit(r.returncode)
def run(name,jobs):
    cmd=['python3',str(packet/'scripts'/name),'--source',str(src),'--packet',str(packet)]
    if jobs:cmd+=['--jobs',str(jobs)]
    return subprocess.run(cmd,timeout=540).returncode
run('run_review.py',min(a.jobs,4))
with cf.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(run,'run_reversals.py',2),pool.submit(run,'run_plants.py',4)]
    campaign_results=[f.result() for f in futures]
run('run_extra.py',min(a.jobs,4))
run('check_deadline_mutation.py',2)
run('audit.py',None)
print('Expected at the reviewed head: both interleaving probes fail; the two-tick plant survives unit tests and fails probe_r3.')
raise SystemExit(any(campaign_results))
