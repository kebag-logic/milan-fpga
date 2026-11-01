#!/usr/bin/env python3
"""Read or write the Arty's two runtime latency corrections over its console; caller holds the bench lock.
usage: lat.py <transcript> read | lat.py <transcript> write <ingress_ns> <egress_ns>
Writes only 0x540 and 0x544 and reads back 0x540, 0x544 and GPTP_LAT. Prints the applied pair and exits 1 if GPTP_LAT does not read what was written."""
import os, re, select, sys, termios, time, tty
PORT = "/dev/serial/by-id/<adapter>"
BASE = 0x90000000
out = sys.argv[1]; mode = sys.argv[2]
fd = os.open(PORT, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
saved = termios.tcgetattr(fd)
def tx(cmd):
    termios.tcflush(fd, termios.TCIFLUSH); t0 = time.time(); os.write(fd, (cmd + "\r").encode()); data = bytearray(); dl = time.monotonic() + 5
    while time.monotonic() < dl:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try: data.extend(os.read(fd, 4096))
            except BlockingIOError: continue
            s = data.decode('ascii', 'replace')
            if s.count('litex') >= 1 and s.rstrip().endswith('>'): break
    return t0, data.decode('ascii', 'replace').replace('\r', '')
def word(s, addr):
    m = re.search(r"^0x%08x\s+((?:[0-9a-f]{2} ){4})" % addr, s, re.M)
    return int("".join(reversed(m.group(1).split())), 16) if m else None
rc = 0
try:
    tty.setraw(fd); a = termios.tcgetattr(fd); a[4] = a[5] = termios.B115200; termios.tcsetattr(fd, termios.TCSANOW, a)
    with open(out, "a") as o:
        if mode == "write":
            ing, egr = int(sys.argv[3]), int(sys.argv[4])
            assert 0 <= ing <= 65535 and 0 <= egr <= 65535
            for addr, v in ((BASE + 0x540, ing), (BASE + 0x544, egr)):
                t0, s = tx(f"mem_write 0x{addr:08x} 0x{v:x}"); o.write(f"### {t0:.3f}\n{s}\n")
        vals = {}
        for off in (0x540, 0x544, 0x7f0):
            t0, s = tx(f"mem_read 0x{BASE + off:08x} 4"); o.write(f"### {t0:.3f}\n{s}\n"); vals[off] = word(s, BASE + off)
        lat = vals[0x7f0]
        print(f"0x540={vals[0x540]} 0x544={vals[0x544]} GPTP_LAT=0x{lat:08x} ingress={lat >> 16} egress={lat & 0xffff}")
        if mode == "write" and lat != ((ing << 16) | egr):
            print("READBACK MISMATCH"); rc = 1
finally:
    termios.tcsetattr(fd, termios.TCSANOW, saved); os.close(fd)
sys.exit(rc)
