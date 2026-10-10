#!/usr/bin/env python3
"""Lane B14: the SoC board console check, read-only (lane B7's soc_peek.py plus one command).

usage: soc_check.py <port> <transcript>

Reads 1 s, sends one carriage return and reads 3 s (soc_peek.py's peek). Only if the last line
is a root shell prompt does it send the one harmless read-only command `id -u` and read 3 s.
It never types a user name, a password or any other command. Prints PROMPT=root|login|unknown
and UID=<value> when the command ran. The caller holds the bench lock.
"""
import os
import re
import select
import sys
import termios
import time


def main():
    port, out = sys.argv[1], sys.argv[2]
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    a = termios.tcgetattr(fd)
    saved = termios.tcgetattr(fd)
    a[0] = 0; a[1] = 0
    a[2] = termios.CS8 | termios.CREAD | termios.CLOCAL
    a[3] = 0
    a[4] = a[5] = termios.B115200
    a[6][termios.VMIN] = 0; a[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, a)
    buf = bytearray()

    def read_for(s):
        end = time.monotonic() + s
        while time.monotonic() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if r:
                try:
                    buf.extend(os.read(fd, 4096))
                except BlockingIOError:
                    pass

    uid = None
    try:
        read_for(1.0)
        before = len(buf)
        os.write(fd, b"\r")
        read_for(3.0)
        tail = buf[before:].decode("utf-8", errors="replace").replace("\r", "")
        lines = [l for l in tail.split("\n") if l.strip()]
        last = lines[-1].strip() if lines else ""
        if re.search(r"login:\s*$", last) or re.search(r"[Pp]assword:\s*$", last):
            verdict = "login"
        elif re.search(r"#\s*$", last):
            verdict = "root"
        else:
            verdict = "unknown"
        mid = len(buf)
        if verdict == "root":
            os.write(fd, b"id -u\r")
            read_for(3.0)
            reply = buf[mid:].decode("utf-8", errors="replace").replace("\r", "")
            m = re.search(r"^(\d+)\s*$", reply, re.M)
            uid = int(m.group(1)) if m else None
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, saved)
        os.close(fd)
    text = buf.decode("utf-8", errors="replace").replace("\r", "")
    with open(out, "a") as f:
        f.write(f"### {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} one carriage return"
                f"{', then id -u' if verdict == 'root' else ''}\n{text}\n### PROMPT={verdict} UID={uid}\n")
    print(f"PROMPT={verdict} UID={uid}")
    return 0 if verdict == "root" and uid == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
