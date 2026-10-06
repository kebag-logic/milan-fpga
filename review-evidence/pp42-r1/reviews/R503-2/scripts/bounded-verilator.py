#!/usr/bin/env python3
"""Use the pinned compiler with at most three builds and two compile jobs each."""
import fcntl,os,pathlib,subprocess,sys,time
real=os.environ.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
a=sys.argv[1:]
for i in range(len(a)-1):
 if a[i] in ("-j","--build-jobs"): a[i+1]="2"
lockdir=pathlib.Path(os.environ["REVIEW_LOCKDIR"]);lockdir.mkdir(parents=True,exist_ok=True)
while True:
 for i in range(3):
  f=(lockdir/str(i)).open("w")
  try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError: f.close();continue
  sys.exit(subprocess.run([real,*a]).returncode)
 time.sleep(.2)
