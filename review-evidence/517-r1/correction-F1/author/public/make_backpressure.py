#!/usr/bin/env python3
"""Cancellation control at a saturated stdout pipe, with an owned descendant."""
import ctypes
import json
import os
import select
import signal
import shutil
import subprocess
import sys
import time
from pathlib import Path

root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
rows=[]
for sig in (signal.SIGTERM,signal.SIGINT):
    dst=out/sig.name
    seed=Path(sys.argv[3]).resolve()
    shutil.copytree(seed,dst)
    for stale in ['ledger.jsonl','stdout','stderr','receipt.json']:
        (dst/stale).unlink(missing_ok=True)
    (dst/'state.json').write_text(json.dumps(dict(alive=[])))
    fast=dst/'obj_dir/Vmilan_dp_sim';hold=dst/'obj_notify/Vmilan_dp_notify'
    fast.write_text('#!/usr/bin/env python3\nimport os,time\nfrom pathlib import Path\nwhile not Path("ready").exists():time.sleep(.005)\nos.write(1,b"fast complete\\n"+b"x"*262144+b"\\n")\n')
    hold.write_text('#!/usr/bin/env python3\nimport os,subprocess,sys,time\nfrom pathlib import Path\np=subprocess.Popen([sys.executable,"-c","import time;time.sleep(120)"],start_new_session=True)\nos.write(1,b"hold partial\\n")\nPath("ready").write_text(str(os.getpid())+" "+str(p.pid)+" "+str(os.getppid()))\ntime.sleep(120)\n')
    fast.chmod(0o755);hold.chmod(0o755)
    argv=[x.replace(str(seed),str(dst)) for x in json.loads((seed/'receipt.json').read_text())['argv']]
    argv.insert(1,'-s')
    env={k:v for k,v in os.environ.items() if k!='MILAN_COUNTER_FRAME_OUT'}
    proc=subprocess.Popen(argv,cwd=dst,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:
        deadline=time.monotonic()+10
        while not (dst/'ready').exists():
            assert proc.poll() is None,'runner exited before saturated pipe'
            assert time.monotonic()<deadline,'did not reach saturated output handshake'
            time.sleep(.005)
        pids=list(map(int,(dst/'ready').read_text().split()));runner=pids.pop()
        while 'pipe_write' not in Path(f'/proc/{runner}/wchan').read_text().strip():
            assert time.monotonic()<deadline,'runner did not reach saturated pipe'
            time.sleep(.005)
        fds={pid:os.pidfd_open(pid) for pid in pids}
        os.killpg(proc.pid,sig)
        # A deliberately stalled consumer remains stalled through this observation.
        time.sleep(.2)
        blocked=Path(f'/proc/{runner}/wchan').read_text().strip()
        status=Path(f'/proc/{runner}/status').read_text();(dst/'status-after-signal').write_text(status)
        pending=int(next(x.split()[1] for x in status.splitlines() if x.startswith('ShdPnd:')),16)
        states={}
        for pid,fd in fds.items():
            poll=select.poll();poll.register(fd,select.POLLIN|select.POLLHUP);states[pid]=poll.poll(0)
        # Positive control: drain exactly the same pipe, then cleanup must finish.
        stdout,stderr=proc.communicate(timeout=10)
        (dst/'stdout-after-drain').write_bytes(stdout);(dst/'stderr').write_bytes(stderr)
        after={}
        for pid,fd in fds.items():
            poll=select.poll();poll.register(fd,select.POLLIN|select.POLLHUP);after[pid]=poll.poll(0);os.close(fd)
        row=dict(signal=sig.name,argv=argv,make_pid=proc.pid,runner_pid=runner,blocked_after_signal=blocked,pending_signal=bool(pending & (1 << (sig-1))),owned_pidfd_events_while_blocked=states,exit_after_drain=proc.returncode,owned_pidfd_events_after_drain=after)
        rows.append(row);(dst/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row),flush=True)
    finally:
        if proc.poll() is None:proc.kill();proc.wait()
        while True:
            children=Path(f'/proc/self/task/{os.getpid()}/children').read_text().split()
            if not children:break
            for child in children:os.kill(int(child),signal.SIGKILL)
            for child in children:os.waitpid(int(child),0)
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
