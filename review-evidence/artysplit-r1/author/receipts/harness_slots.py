"""One process-owned flock slot per final harness leg; four total in this lane."""
import contextlib,datetime,fcntl,json,os,time
from pathlib import Path
ROOT=Path('$VALIDATION_STORAGE/artysplit-a829/r4/final-slots')
@contextlib.contextmanager
def slot(label):
 ROOT.mkdir(exist_ok=True)
 while True:
  held=None
  for number in range(4):
   handle=(ROOT/f'{number}.lock').open('a+')
   try:fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:handle.close();continue
   held=(number,handle);break
  if held:break
  time.sleep(0.2)
 number,handle=held
 record=dict(slot=number,pid=os.getpid(),label=label,started=datetime.datetime.now(datetime.timezone.utc).isoformat())
 handle.seek(0);handle.truncate();handle.write(json.dumps(record)+'\n');handle.flush()
 try:yield number
 finally:
  record['finished']=datetime.datetime.now(datetime.timezone.utc).isoformat()
  with (ROOT/f'{os.getpid()}-{time.time_ns()}.json').open('w') as log:json.dump(record,log,indent=2)
  fcntl.flock(handle,fcntl.LOCK_UN);handle.close()
