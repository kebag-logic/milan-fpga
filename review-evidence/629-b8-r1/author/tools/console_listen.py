#!/usr/bin/env python3
"""Lane B8: record the DUT's bare-metal console for a fixed time without typing anything.

usage: console_listen.py <port> <transcript> <seconds>

Opens the console at 115200 8N1, never writes to it, and records every received chunk with
this host's realtime and CLOCK_MONOTONIC_RAW, as one JSON line per chunk ({"t", "raw", "hex"}).
Used across the one authorised power cycle to record the boot. The caller holds the bench lock.
"""
import json
import os
import select
import sys
import termios
import time
import tty


def main() -> int:
    port, out_path, secs = sys.argv[1], sys.argv[2], float(sys.argv[3])
    fd = os.open(port, os.O_RDONLY | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    n = 0
    try:
        tty.setraw(fd)
        attrs = termios.tcgetattr(fd)
        attrs[4] = attrs[5] = termios.B115200
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        end = time.monotonic() + secs
        with open(out_path, "w", buffering=1) as out:
            out.write(json.dumps(dict(start=round(time.time(), 6), raw=time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW),
                                      seconds=secs)) + "\n")
            while time.monotonic() < end:
                r, _, _ = select.select([fd], [], [], 0.1)
                if not r:
                    continue
                try:
                    d = os.read(fd, 4096)
                except BlockingIOError:
                    continue
                if d:
                    n += len(d)
                    out.write(json.dumps(dict(t=round(time.time(), 6), raw=time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW),
                                              hex=d.hex())) + "\n")
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, saved)
        os.close(fd)
    print(f"BYTES={n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
