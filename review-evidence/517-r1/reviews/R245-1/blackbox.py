#!/usr/bin/env python3
"""Independent real-Makefile probes. Models/compiler are inert fixtures.

Run with repository and a fresh output directory. No source checkout writes.
Compiler and prerequisite receipts are evidence of wiring, not HDL execution.
"""
import ctypes
import hashlib
import json
import os
import select
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=False)
HERE = ROOT / 'tb/verilator/milan_dp'
BASE = '483a133ed08867ea0d300d2b4a027b5b48a4282f'
LEGACY = subprocess.check_output(['git', '-C', str(ROOT), 'show', BASE + ':tb/verilator/milan_dp/Makefile']).decode()
tail = LEGACY[LEGACY.index('\t./obj_dir/Vmilan_dp_sim', LEGACY.index('\nrun:')):]
LEGS = [line.strip() for line in tail.splitlines() if line.startswith('\t./obj_')][:10]
assert len(LEGS) == 10
GROUP = LEGS[1:6]
PREREQS = ['./obj_gptp/Vmilan_dp_gptp', './obj_gptplat/Vmilan_dp_gptplat']
FAKE = r'''#!/usr/bin/env python3
import fcntl,hashlib,json,os,resource,signal,subprocess,sys,time
from pathlib import Path
cfg=json.loads(Path('config.json').read_text())
def event(kind,**kw):
    with open('ledger.jsonl','a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        f.write(json.dumps(dict(kind=kind,**kw))+'\n');f.flush()
def body(name):return (name+' stdout\n').encode()+b'X'*70000+b'\x00\xff\n'+(name+' stderr\n').encode()
name='./'+str(Path(sys.argv[0]))
if Path(sys.argv[0]).name=='compiler':
    event('build',argv=sys.argv[1:]);sys.exit(0)
if Path(sys.argv[0]).name=='render_mutants.py':
    event('render');sys.exit(0)
if name in cfg['prereqs']:
    event('prereq',name=name);sys.exit(0)
assert name in cfg['legs'],name
index=cfg['legs'].index(name); group=name in cfg['group']
with open('state.json','r+') as f:
    fcntl.flock(f,fcntl.LOCK_EX);state=json.load(f)
    state['alive'].append(name)
    event('start',name=name,pid=os.getpid(),argv=sys.argv,cwd=os.getcwd(),alive=list(state['alive']),group=[x for x in state['alive'] if x in cfg['group']],input_hash=hashlib.sha256(Path('input.hex').read_bytes()).hexdigest())
    f.seek(0);json.dump(state,f);f.truncate()
data=body(name);os.write(1,data[:-len((name+' stderr\n').encode())]);os.write(2,(name+' stderr\n').encode())
if cfg['case'].startswith('interrupt'):
    # Each leg owns a child that creates a new session and a further child.
    childcode="import os,subprocess,sys,time; from pathlib import Path; p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(120)']); Path(sys.argv[1]).write_text(str(os.getpid())+' '+str(p.pid)); time.sleep(120)"
    child=subprocess.Popen([sys.executable,'-c',childcode,'desc-'+str(index)],start_new_session=True)
    while not Path('desc-'+str(index)).exists():time.sleep(.002)
    Path('ready-'+str(index)).write_text(str(os.getpid()))
    time.sleep(120)
else:
    time.sleep(.16 if index==1 else .055)
    if 'MILAN_COUNTER_FRAME_OUT' in os.environ and index in (2,3,4,5):
        try:Path(os.environ['MILAN_COUNTER_FRAME_OUT']).write_bytes(name.encode())
        except OSError:event('empty-failure',name=name);sys.exit(1)
    with open('state.json','r+') as f:
        fcntl.flock(f,fcntl.LOCK_EX);state=json.load(f);state['alive'].remove(name)
        f.seek(0);json.dump(state,f);f.truncate()
    event('end',name=name)
    if cfg['case']=='fail' and index==0:sys.exit(7)
    if cfg['case']=='crash' and index==0:
        resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.kill(os.getpid(),signal.SIGSEGV)
'''
assert ctypes.CDLL(None).prctl(36, 1, 0, 0, 0) == 0

def cleanup():
    while True:
        pids = Path(f'/proc/self/task/{os.getpid()}/children').read_text().split()
        if not pids: break
        for pid in pids: os.kill(int(pid), signal.SIGKILL)
        for pid in pids: os.waitpid(int(pid), 0)

def run(case, jobs=None, mutation=None):
    name = case + ('-' + jobs if jobs is not None else '') + ('-' + mutation if mutation else '')
    dst = OUT/name; dst.mkdir()
    runner = (HERE/'sim_pool.py').read_text()
    makefile = (HERE/'Makefile').read_text()
    if mutation == 'ungroup': makefile = makefile.replace('--exclusive ', '')
    if mutation == 'third': runner = runner.replace('self.jobs = jobs', 'self.jobs = 3')
    if mutation == 'empty-truthiness': runner = runner.replace('frame_dump = FRAME_DUMP_VAR in os.environ', 'frame_dump = bool(os.environ.get(FRAME_DUMP_VAR))')
    if mutation == 'lost-output': runner = runner.replace('shutil.copyfileobj(capture, self.out)', 'capture.read()')
    if mutation == 'masked-exit': runner = runner.replace('return 0 if passed else 1', 'return 0')
    if mutation == 'leak-adopted': runner = runner.replace('reap_adopted(running)', 'None # planted missing adoption cleanup')
    (dst/'sim_pool.py').write_text(runner); (dst/'Makefile').write_text(makefile)
    (dst/'fixture.py').write_text(FAKE)
    for path in [*LEGS,*PREREQS,'compiler','render_mutants.py']:
        exe=dst/path;exe.parent.mkdir(parents=True,exist_ok=True);exe.write_text(FAKE);exe.chmod(0o755)
    if case=='missing':(dst/LEGS[0]).unlink()
    (dst/'config.json').write_text(json.dumps(dict(case=case,legs=LEGS,group=GROUP,prereqs=PREREQS)))
    (dst/'state.json').write_text(json.dumps(dict(alive=[])))
    (dst/'input.hex').write_bytes(b'0123456789abcdef\n')
    env={k:v for k,v in os.environ.items() if k not in ('MILAN_COUNTER_FRAME_OUT','MAKEFLAGS','MFLAGS','MAKELEVEL')}
    env.update(MAKEFLAGS='-j8',PYTHONDONTWRITEBYTECODE='1')
    if case=='frame':env['MILAN_COUNTER_FRAME_OUT']=str(dst/'frame.bin')
    if case=='empty':env['MILAN_COUNTER_FRAME_OUT']=''
    argv=['make','--no-print-directory','-f',str(dst/'Makefile'),'run',f'CURDIR={HERE}',f'VERILATOR={dst}/compiler','VERILATOR_JOBS=8']
    if jobs is not None:argv.append('SIM_JOBS='+jobs)
    # These generated inputs are intentionally inert, never rebuilt by a probe.
    for p in ('ltn_rom.hex','ucode.hex','gptp_ucode.hex','../../../hdl/common/csr/gen/lwsrp_csr_defaults.svh','../../../hdl/common/gen/adp_shape_defaults.svh','../../../configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh','../../../configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh','../../../configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh','gen_divergent/gen/adp_shape_defaults.svh'):
        argv += ['-o',p]
    pidfds={}; timed_out=False
    try:
        with (dst/'stdout').open('wb') as stdout,(dst/'stderr').open('wb') as stderr:
            proc=subprocess.Popen(argv,cwd=dst,env=env,stdout=stdout,stderr=stderr,start_new_session=True)
            if case.startswith('interrupt'):
                deadline=time.monotonic()+10
                while len(list(dst.glob('ready-*')))<2:
                    if proc.poll() is not None:raise AssertionError('make exited before interrupt handshake')
                    assert time.monotonic()<deadline,'interrupt fixture not ready'
                    time.sleep(.005)
                pids=[]
                for f in dst.glob('ready-*'):pids+=list(map(int,f.read_text().split()))
                for f in dst.glob('desc-*'):pids+=list(map(int,f.read_text().split()))
                pidfds={pid:os.pidfd_open(pid) for pid in pids}
                sig=signal.SIGINT if case.endswith('int') else signal.SIGTERM
                os.killpg(proc.pid,sig)
            try:code=proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                timed_out=True;os.killpg(proc.pid,signal.SIGKILL);code=proc.wait()
        rows=[json.loads(x) for x in (dst/'ledger.jsonl').read_text().splitlines()]
        starts=[x for x in rows if x['kind']=='start'];ends=[x for x in rows if x['kind']=='end']
        checks={};checks['no-timeout']=not timed_out
        checks['builds-and-prereqs']=len([x for x in rows if x['kind']=='build'])==12 and sorted(x['name'] for x in rows if x['kind']=='prereq')==sorted(PREREQS)
        checks['bounds']=all(len(x['alive'])<=2 and len(x['group'])<=1 for x in starts)
        checks['group-order']=[x['name'] for x in starts if x['name'] in GROUP]==GROUP[:sum(x['name'] in GROUP for x in starts)]
        checks['argv-inputs']=all(x['argv']==[x['name']] and x['cwd']==str(dst) and x['input_hash']==hashlib.sha256(b'0123456789abcdef\n').hexdigest() for x in starts)
        render=[x for x in rows if x['kind']=='render']
        if case in ('normal','frame') and jobs not in ('0','3','8','02','-1',''):
            checks['all-once']=sorted(x['name'] for x in starts)==sorted(LEGS)
            checks['success-render']=code==0 and len(render)==1 and rows[-1]['kind']=='render'
        else:checks['failure-no-render']=code!=0 and not render
        if case=='normal' and jobs in (None,'2'):
            checks['independent-overlap']=any(len(x['alive'])==2 and len(x['group'])==1 for x in starts)
        if case in ('frame','empty') or jobs=='1':
            checks['whole-set-sequential']=all(len(x['alive'])==1 for x in starts) and [x['name'] for x in starts]==LEGS[:len(starts)]
        if case=='frame':checks['last-writer']=(dst/'frame.bin').read_bytes()==LEGS[5].encode()
        if case=='empty':checks['empty-outcome']=[x['name'] for x in starts]==LEGS[:3]
        if jobs in ('0','3','8','02','-1',''):checks['no-starts']=not starts
        text=(dst/'stdout').read_bytes(); log_positions=[]
        for i,exe in enumerate(LEGS):
            cap=dst/'obj_legs'/f'{i+1:02d}-{Path(exe).name}.log'
            if any(x['name']==exe for x in starts):
                wanted=(exe+' stdout\n').encode()+b'X'*70000+b'\x00\xff\n'+(exe+' stderr\n').encode()
                checks['capture-'+str(i)]=cap.read_bytes()==wanted
                checks['replay-'+str(i)]=text.count(wanted)==1
                log_positions.append(text.find(wanted))
        checks['ordered-output']=log_positions==sorted(log_positions)
        if case.startswith('interrupt'):
            states={}
            for pid,fd in pidfds.items():
                poll=select.poll();poll.register(fd,select.POLLIN|select.POLLHUP);states[str(pid)]=poll.poll(0)
            checks['descendants-reaped']=all(events and events[0][1]&select.POLLHUP for events in states.values())
            checks['attributable-interrupt']=all((x['name']+' was killed by this runner on SIG').encode() in text for x in starts)
            (dst/'pidfd-states.json').write_text(json.dumps(states,indent=2))
        row=dict(case=name,argv=argv,makeflags=env['MAKEFLAGS'],exit=code,checks=checks,accepted=all(checks.values()),mutation=mutation)
        (dst/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
        print(name,code,'ACCEPTED' if row['accepted'] else 'REJECTED',','.join(k for k,v in checks.items() if not v),flush=True)
        return row
    finally:
        cleanup()
        for fd in pidfds.values():os.close(fd)

rows=[]
for case,jobs in [('normal',None),('normal','1'),('frame',None),('empty',None),('fail',None),('crash',None),('missing',None),('interrupt-int',None),('interrupt-term',None)]+[('normal',j) for j in ('0','3','8','02','-1','')]:
    rows.append(run(case,jobs))
for case,mutation in [('normal','ungroup'),('normal','third'),('empty','empty-truthiness'),('normal','lost-output'),('fail','masked-exit'),('interrupt-term','leak-adopted')]:
    rows.append(run(case,mutation=mutation))
(OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
assert all(r['accepted'] != bool(r['mutation']) for r in rows)
