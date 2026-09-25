import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = Path.cwd()
SUITE = ROOT / 'tb/verilator/milan_dp'
name, jobs, temperature = sys.argv[1:]
DEST = OUT / name
DEST.mkdir()
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no']).strip()
head = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def headers():
    paths = subprocess.check_output(['git','ls-files','-z','*.svh']).decode().split('\0')
    return {p:digest(ROOT/p) for p in paths if p}

def binaries():
    return {str(p.relative_to(SUITE)):digest(p) for p in SUITE.glob('obj_*/Vmilan_dp*')
            if p.is_file() and os.access(p,os.X_OK)}

def inputs():
    paths = list(SUITE.glob('*.hex'))
    paths += list((SUITE/'gen_divergent').rglob('*.svh'))
    paths += [SUITE/'obj_gmstep/aemi.bin']
    paths += list((ROOT/'configs').glob('*.yaml'))
    return {str(p.relative_to(ROOT)):digest(p) for p in paths if p.is_file()}

def descendants(pid):
    pending = [pid]
    found = []
    while pending:
        current = pending.pop()
        p = Path('/proc')/str(current)
        try:
            children = (p/'task'/str(current)/'children').read_text().split()
            pending.extend(int(child) for child in children)
            status = (p/'status').read_text().splitlines()
            rss = next((int(line.split()[1]) for line in status if line.startswith('VmRSS:')),0)
            executable = os.path.basename(os.readlink(p/'exe'))
            found.append(dict(pid=current, executable=executable, rss_kib=rss))
        except (FileNotFoundError,ProcessLookupError,PermissionError):
            pass
    return found

before = headers()
if temperature == 'cold':
    with (DEST/'clean.log').open('wb') as log:
        clean = subprocess.run(['make','-C',str(SUITE),'clean'],stdout=log,stderr=subprocess.STDOUT)
    assert clean.returncode == 0
argv = ['make','-C','tb/verilator/milan_dp',f'SIM_JOBS={jobs}','VERILATOR_JOBS=8']
logpath = DEST/'milan_dp.log'
started = time.monotonic()
peak_rss = peak_ordinary = peak_group = 0
ordinary_names = {'Vmilan_dp_sim','Vmilan_dp_notify','Vmilan_dp_crflic','Vmilan_dp_nxn',
                  'Vmilan_dp_nxndv','Vmilan_dp_nxn8','Vmilan_dp_nxn4c',
                  'Vmilan_dp_nolpf','Vmilan_dp_prune','Vmilan_dp_ax1x1','Vmilan_dp_aclk'}
group_names = {'Vmilan_dp_notify','Vmilan_dp_nxn','Vmilan_dp_nxndv','Vmilan_dp_nxn8','Vmilan_dp_nxn4c'}
seen = {}
with logpath.open('wb') as log, (DEST/'resources.jsonl').open('w') as samples:
    process = subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT)
    while process.poll() is None:
        rows = descendants(process.pid)
        pooled = [row for row in rows if row['executable'] in ordinary_names]
        # Count ordinary simulations only while the pool owner is active.
        pool_active = False
        for row in rows:
            try:
                cmd = (Path('/proc')/str(row['pid'])/'cmdline').read_bytes().split(b'\0')
                if b'sim_pool.py' in cmd: pool_active = True
            except (FileNotFoundError,ProcessLookupError): pass
        if pool_active:
            peak_ordinary = max(peak_ordinary,len(pooled))
            peak_group = max(peak_group,sum(row['executable'] in group_names for row in pooled))
            for row in pooled: seen[row['pid']] = row['executable']
        peak_rss = max(peak_rss,sum(row['rss_kib'] for row in rows))
        samples.write(json.dumps(dict(seconds=time.monotonic()-started, load_average=os.getloadavg(), pool=pool_active, processes=rows))+'\n')
        time.sleep(0.5)
    status = process.wait()
elapsed = time.monotonic()-started
after = headers()
for path in (SUITE/'obj_legs').glob('*.log'):
    shutil.copyfile(path,DEST/path.name)
result = dict(head=head,argv=argv,temperature=temperature,jobs=int(jobs),seconds=elapsed,
              exit_code=status,cpus=sorted(os.sched_getaffinity(0)),peak_rss_kib=peak_rss,
              peak_ordinary=peak_ordinary,peak_exclusive=peak_group,observed_ordinary=seen,
              headers_before=before,headers_after=after,binaries=binaries(),
              headers_unchanged=before==after,runtime_inputs=inputs())
(DEST/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('headers_before','headers_after','binaries','observed_ordinary','runtime_inputs')},indent=2),flush=True)
if status:sys.exit(status)
assert before == after, 'tracked generated header changed'
assert peak_ordinary <= int(jobs) and peak_group <= 1
captures = sorted(DEST.glob('[0-9][0-9]-*.log'))
assert len(captures)==11, captures
assert {p.name.split('-',1)[1].removesuffix('.log') for p in captures}==ordinary_names
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no']).strip()
verdict = subprocess.run(['python3','scripts/suite_tally.py','--verdict',str(logpath)])
sys.exit(verdict.returncode)
