#!/usr/bin/env python3
"""Passive serial listener (lane B21): opens the port, writes nothing, logs what arrives.

usage: console_listen.py <port> <transcript> <seconds>
The caller holds the bench lock.
"""
import os, select, sys, termios, time

port, out, secs = sys.argv[1], sys.argv[2], float(sys.argv[3])
fd = os.open(port, os.O_RDONLY | os.O_NOCTTY | os.O_NONBLOCK)
a = termios.tcgetattr(fd)
a[0] = 0; a[1] = 0; a[2] = termios.CS8 | termios.CREAD | termios.CLOCAL; a[3] = 0
a[4] = a[5] = termios.B115200
a[6][termios.VMIN] = 0; a[6][termios.VTIME] = 0
termios.tcsetattr(fd, termios.TCSANOW, a)
log = open(out, "ab")
log.write(("\n### %s passive listen %ss, nothing written\n" % (time.strftime("%Y-%m-%dT%H:%M:%S%z"), secs)).encode())
end = time.time() + secs
n = 0
while time.time() < end:
    r, _, _ = select.select([fd], [], [], 0.5)
    if r:
        d = os.read(fd, 65536)
        if d:
            n += len(d)
            log.write(("\n[+%.1fs] " % (secs - (end - time.time()))).encode() + d)
            log.flush()
log.write(("\n### end, %d bytes received\n" % n).encode())
os.close(fd)
