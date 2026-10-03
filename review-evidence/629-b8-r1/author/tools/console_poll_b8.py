#!/usr/bin/env python3
"""Lane B8: poll the DUT's media-clock and slip words over the bare-metal console, read-only.

usage: console_poll_b8.py <port> <out.jsonl> <max_s> <period_s> <stop>
  stop: none         poll for max_s
        locked       stop two polls after MCSRV_STAT[2:0] first reads 4 (LOCKED), or at max_s
        file:<path>  poll until <path> exists, or at max_s

Lane B7's console_poll.py with two lane B8 changes: each poll also reads `mem_read 0x900008d4
12` (SLIP_LB, SLIP_TDM, RENDER_STAT), `mem_read 0x90000738 4` (CRF_CTRL, [31] the CRF sink's
lock) and `mem_read 0x90000748 4` (CRF_RATE), the words lane B7's console_read.py reads every
30 s; and the `file:` stop, so one poll can run through a whole case while the run tool reads
the file. Each poll sends the same read-only BIOS command console_read.py sends and writes one
JSON line with this host's realtime and CLOCK_MONOTONIC_RAW before and after the reads and the
words. The caller holds the bench lock and must not use the console meanwhile.
"""
import json
import os
import select
import struct
import sys
import termios
import time
import tty

CMDS = (("0x900008e0", 8), ("0x900008f8", 4), ("0x900008d4", 12), ("0x90000738", 4), ("0x90000748", 4))


def main() -> int:
    port, out_path, max_s, period, stop = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    assert stop in ("none", "locked") or stop.startswith("file:")
    stop_file = stop[5:] if stop.startswith("file:") else None
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    out = open(out_path, "a", buffering=1)
    t_end = time.monotonic() + max_s
    after_lock = None
    n = 0
    try:
        tty.setraw(fd)
        attrs = termios.tcgetattr(fd)
        attrs[4] = attrs[5] = termios.B115200
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        while time.monotonic() < t_end:
            if stop_file and os.path.exists(stop_file):
                break
            t_next = time.monotonic() + period
            rt0, raw0 = time.time(), time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)
            words = {}
            for addr, nb in CMDS:
                termios.tcflush(fd, termios.TCIFLUSH)
                os.write(fd, f"mem_read {addr} {nb}\r".encode())
                data = bytearray()
                dl = time.monotonic() + 3.0
                while time.monotonic() < dl:
                    r, _, _ = select.select([fd], [], [], 0.05)
                    if r:
                        try:
                            data.extend(os.read(fd, 4096))
                        except BlockingIOError:
                            continue
                        tx = data.decode("ascii", errors="replace")
                        if "Memory dump:" in tx and tx.rstrip().endswith(">"):
                            break
                tx = data.decode("ascii", errors="replace").replace("\r", "")
                try:
                    line = tx.split("Memory dump:\n", 1)[1].splitlines()[0].split()
                    b = bytes(int(h, 16) for h in line[1:1 + nb])
                    base = int(addr, 16) - 0x90000000
                    for k in range(0, nb, 4):
                        words[f"{base + k:#05x}"] = f"{struct.unpack('<I', b[k:k + 4])[0]:08x}"
                except (IndexError, ValueError):
                    words[addr] = None
            rt1, raw1 = time.time(), time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)
            s = words.get("0x8f8")
            st = int(s, 16) & 7 if s else None
            out.write(json.dumps(dict(n=n, t0=round(rt0, 6), t1=round(rt1, 6), raw0=raw0, raw1=raw1,
                                      words=words, servo_state=st)) + "\n")
            n += 1
            if stop == "locked":
                if after_lock is None and st == 4:
                    after_lock = 0
                elif after_lock is not None:
                    after_lock += 1
                    if after_lock >= 2:
                        break
            while time.monotonic() < t_next:
                time.sleep(0.01)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, saved)
        os.close(fd)
        out.close()
    return 0 if (stop != "locked" or after_lock is not None) else 2


if __name__ == "__main__":
    sys.exit(main())
