"""Bounded foreground capture, stopped through standard input."""
import subprocess,sys,select,time,signal
interface,seconds=sys.argv[1:];seconds=int(seconds)
p=subprocess.Popen(["timeout","-s","INT","-k","2s",str(seconds)+"s","tcpdump","-U","-n","-i",interface,"-w","-"],stdin=subprocess.DEVNULL)
try:
 end=time.monotonic()+seconds+3
 while p.poll() is None and time.monotonic()<end:
  ready,_,_=select.select([sys.stdin],[],[],.1)
  if ready:
   sys.stdin.readline();p.send_signal(signal.SIGINT);break
 p.wait(timeout=4)
finally:
 if p.poll() is None:
  p.send_signal(signal.SIGINT)
  p.wait(timeout=4)
if p.returncode not in (0,124,130,-2):raise SystemExit(p.returncode)
