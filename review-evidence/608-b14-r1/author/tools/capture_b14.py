"""Bounded foreground capture, stopped through standard input.

Lane B2's capture.py with two changes:
  * an optional capture filter (argv[3]) and a 256-byte snap length, the bench brief's, so the
    8000 PDU/s AAF streams can be left out;
  * the stop signals tcpdump itself. On this tap host a SIGINT sent to `timeout` is not forwarded
    to its child (tested 2026-10-10 05:50 UTC: the child was SIGKILLed after the kill-after delay,
    rc 137, with no statistics), while tcpdump exits cleanly on its own SIGINT. The deadline is
    kept here (and by the caller's outer timeout).
"""
import subprocess,sys,select,time,signal
interface,seconds=sys.argv[1:3];seconds=int(seconds);filt=sys.argv[3:4]
p=subprocess.Popen(["tcpdump","-U","-n","-s","256","-i",interface,"-w","-",*filt],stdin=subprocess.DEVNULL)
try:
 end=time.monotonic()+seconds
 while p.poll() is None and time.monotonic()<end:
  ready,_,_=select.select([sys.stdin],[],[],.1)
  if ready:
   sys.stdin.readline();break
finally:
 if p.poll() is None:
  p.send_signal(signal.SIGINT)
  try:
   p.wait(timeout=4)
  except subprocess.TimeoutExpired:
   p.kill();p.wait(timeout=4)
if p.returncode not in (0,124,130,-2):raise SystemExit(p.returncode)
