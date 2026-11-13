#!/usr/bin/env python3
"""Reproduce head/base analytical checks without checking out another branch.
Usage: python3 -B run_graders.py CHECKOUT PACKET
"""
import concurrent.futures
import io
from pathlib import Path
import subprocess
import sys
import tarfile

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
base = packet/'scratch/base'
base.mkdir(parents=True, exist_ok=True)
def export(root, rev, paths, target):
    data = subprocess.check_output(['git','-C',str(root),'archive',rev,*paths])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(target, filter='data')
export(repo,'b2d39235ab9bba85d7e560b5f5f78fb4be528960',
       ['tb/verilator/ctrl_service_budget','sw/mailbox','sw/firmware/ctrl'],base)
sub = base/'third_party/tsn-c-stack'
sub.mkdir(parents=True, exist_ok=True)
export(repo/'third_party/tsn-c-stack','715589c1db7cf67e2f3259fd7083ebc7f0923376',['include'],sub)
jobs = [(label,root,tool,'--check') for label,root in [('head',repo),('base',base)]
        for tool in ['load_grade','flip_grade']]
jobs += [('head',repo,tool,'--selftest') for tool in ['load_grade','flip_grade']]
def run(job):
    label,root,tool,flag=job
    result=subprocess.run([sys.executable,'-B',str(root/'tb/verilator/ctrl_service_budget'/(tool+'.py')),flag],
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    name=label+'-'+tool+flag.replace('--','-')
    log=result.stdout.replace(str(packet),'<packet>').replace(str(repo),'<clone>')
    (packet/'receipts'/(name+'.log')).write_text(log)
    (packet/'receipts'/(name+'.rc')).write_text(str(result.returncode)+'\n')
    expected=1 if tool=='flip_grade' and flag=='--check' else 0
    print(name,result.returncode,flush=True)
    return result.returncode==expected
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as workers:
    good=list(workers.map(run,jobs))
sys.exit(0 if all(good) else 1)
