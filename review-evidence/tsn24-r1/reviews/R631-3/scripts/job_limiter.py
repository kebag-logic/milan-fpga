#!/usr/bin/env python3
import fcntl,json,os,pathlib,subprocess,sys,time
name=pathlib.Path(sys.argv[0]).name
cfg=json.loads(pathlib.Path(os.environ['REVIEW_LIMIT_CONFIG']).read_text())
cmd=cfg['commands'][name]+sys.argv[1:]
if name=='cppcheck': cmd=[a for a in cmd if not a.startswith('-j')]+['-j1']
locks=pathlib.Path(cfg['locks']);locks.mkdir(exist_ok=True)
while True:
    for i in range(cfg['jobs']):
        f=open(locks/str(i),'w')
        try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: f.close();continue
        try: sys.exit(subprocess.call(cmd))
        finally: f.close()
    time.sleep(0.1)
