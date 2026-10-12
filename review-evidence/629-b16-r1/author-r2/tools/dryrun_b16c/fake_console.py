#!/usr/bin/env python3
"""B16c dry run (offline): a pty standing in for the DUT's console. It answers mem_read with a Memory dump line and
any other command with a line, each ending with the prompt. MCSRV_STAT (0x900008f8) reads LOCKED (4) from 2 s after
the model's DUT clock-source set while the model's DUT source is not 0 (FAKE_NO_LOCK=1: never), IDLE otherwise.
usage: fake_console.py <fake_dir>   (prints the pty path, then serves until killed)"""
import json
import os
import pty
import sys
import time
import tty

D = sys.argv[1]
m, s = pty.openpty()
tty.setraw(s)
print(os.ttyname(s), flush=True)
buf = b""
while True:
    buf += os.read(m, 4096)
    while b"\r" in buf:
        cmd, buf = buf.split(b"\r", 1)
        c = cmd.decode(errors="replace").strip()
        out = c + "\r\n"
        if c.startswith("mem_read"):
            _, a, n = c.split()
            n = int(n)
            vals = bytearray(n)
            if a == "0x900008f8":
                try:
                    M = json.load(open(os.path.join(D, "model.json")))
                except Exception:
                    M = {}
                locked = (M.get("clk", {}).get("dut", 0) != 0 and M.get("set_t") and time.time() - M["set_t"] > 2.0
                          and os.environ.get("FAKE_NO_LOCK") != "1")
                vals[0] = 0x24 if locked else 0x20
            out += "Memory dump:\r\n" + a + " " + " ".join("%02x" % v for v in vals) + "\r\n"
        else:
            out += "fake reply\r\n"
        os.write(m, (out + "litex> ").encode())
