"""Hold the run queue at about N runnable threads for S seconds: hashlib releases the GIL on large buffers.

Usage: python3 -I burner.py <threads> <seconds>
"""
import hashlib, sys, threading, time
n, secs = int(sys.argv[1]), float(sys.argv[2])
buf, end = b"\0" * (1 << 20), time.monotonic() + secs
def burn():
    while time.monotonic() < end:
        hashlib.sha256(buf).digest()
threads = [threading.Thread(target=burn) for _ in range(n)]
for t in threads: t.start()
for t in threads: t.join()
