#!/usr/bin/env python3
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
