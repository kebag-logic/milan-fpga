"""Schedule only this campaign's native children on the assigned 32 CPUs.
Pausing changes wall time only: the native model advances explicit clock cycles.
All children are continued in finally; no paused process is left behind.
"""
from pathlib import Path
import os,signal,time,json
roots=('$VALIDATION_STORAGE/usbnet-a855/round7/census/','$VALIDATION_STORAGE/usbnet-a855/round7/census-supplemental/')
packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
log=(packet/'native-slots.jsonl').open('a',buffering=1)
paused=set();started=time.monotonic();ever=False
ours=Path('/proc/self/cgroup').read_text()
def children():
 out={}
 for f in Path('/proc').glob('[0-9]*/cmdline'):
  try:
   cmd=f.read_bytes().split(b'\0')[0].decode()
   if cmd.startswith(roots) and cmd.endswith('/native/Vsim') and (f.parent/'cgroup').read_text()==ours:
    stat=(f.parent/'stat').read_text().split();out[int(f.parent.name)]=(int(stat[21]),stat[2])
  except (OSError,ValueError):pass
 return out
def send(pid,sig):
 try:
  os.kill(pid,sig)
  log.write(json.dumps(dict(utc=time.time(),pid=pid,signal=sig.name))+'\n')
 except ProcessLookupError:pass
try:
 while True:
  live=children()
  if live:ever=True
  if not live and ever:break
  allowed=set(sorted(live,key=lambda pid:live[pid][0])[:32])
  paused.intersection_update(live)
  for pid in live:
   if pid not in allowed and pid not in paused:send(pid,signal.SIGSTOP);paused.add(pid)
   elif pid in allowed and pid in paused:send(pid,signal.SIGCONT);paused.remove(pid)
  time.sleep(1)
finally:
 for pid in paused:send(pid,signal.SIGCONT)
 log.close()
print('Native scheduling complete; every paused child resumed.')
