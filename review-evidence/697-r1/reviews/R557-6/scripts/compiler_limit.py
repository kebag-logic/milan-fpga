#!/usr/bin/env python3
"""Bound aggregate compiler memory while independent foreground suites overlap."""
import fcntl,os,pathlib,shutil,subprocess,sys,time
name=pathlib.Path(sys.argv[0]).name
binary=shutil.which(name,path=os.environ["REVIEW_ORIGINAL_PATH"])
locks=pathlib.Path(os.environ["REVIEW_COMPILER_LOCKS"]); locks.mkdir(exist_ok=True)
while True:
 for n in range(8):
  file=(locks/str(n)).open("w")
  try: fcntl.flock(file,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError: file.close(); continue
  try: sys.exit(subprocess.run([binary,*sys.argv[1:]]).returncode)
  finally: file.close()
 time.sleep(.05)
