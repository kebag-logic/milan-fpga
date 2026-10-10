#!/usr/bin/env python3
"""Lane B7: look at the SoC board's serial console without typing a command.

usage: soc_peek.py <port> <transcript>

Opens the console, reads for 1 s, sends one carriage return (an empty line, which a shell
answers with its prompt and a login prompt with itself), reads for 3 s more, and writes the
received bytes to the transcript. Prints PROMPT=root, PROMPT=login or PROMPT=unknown. It never
types a user name, a password or a command. The caller holds the bench lock.
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

    try:
        read_for(1.0)
        before = len(buf)
        os.write(fd, b"\r")
        read_for(3.0)
    finally:
        os.close(fd)
    text = buf.decode("utf-8", errors="replace")
    tail = text[before:].replace("\r", "")
    lines = [l for l in tail.split("\n") if l.strip()]
    last = lines[-1].strip() if lines else ""
    if re.search(r"login:\s*$", last) or re.search(r"[Pp]assword:\s*$", last):
        verdict = "login"
    elif re.search(r"#\s*$", last):
        verdict = "root"
    else:
        verdict = "unknown"
    with open(out, "a") as f:
        f.write(f"### {time.strftime('%Y-%m-%dT%H:%M:%S%z')} sent one carriage return\n")
        f.write(f"### before it ({before} bytes):\n{text[:before]}\n### after it:\n{tail}\n### PROMPT={verdict}\n")
    print(f"PROMPT={verdict}")
    return 0 if verdict == "root" else 3


if __name__ == "__main__":
    sys.exit(main())
