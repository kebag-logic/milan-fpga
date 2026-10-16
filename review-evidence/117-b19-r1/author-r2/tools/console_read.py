#!/usr/bin/env python3
"""Read-only readback over the AX7101 bare-metal console (issue 117; A196 reader,
A200 adds the BIOS mem_read command for the publication CSRs).

Sends only read commands (milan_status, milan_gettime, milan_nvm, mem_list,
crc, mem_read) and writes a timestamped transcript. The caller holds the
bench lock.

usage: console_read.py <port> <transcript> <command> [<command> ...]
"""
import os
import select
import sys
import termios
import time
import tty

READ_ONLY = ("milan_status", "milan_gettime", "milan_nvm", "mem_list", "crc ", "mem_read ")


def main() -> int:
    port, out_path, commands = sys.argv[1], sys.argv[2], sys.argv[3:]
    for cmd in commands:
        if cmd != "milan_nvm" and not cmd.startswith(READ_ONLY):
            raise SystemExit(f"refused: {cmd!r} is not a read-only command")
        if cmd.startswith("milan_nvm") and cmd != "milan_nvm":
            raise SystemExit(f"refused: {cmd!r} (only the bare status form)")
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        attrs = termios.tcgetattr(fd)
        attrs[4] = attrs[5] = termios.B115200
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        with open(out_path, "w") as out:
            for cmd in commands:
                termios.tcflush(fd, termios.TCIFLUSH)
                t0 = time.time()
                os.write(fd, (cmd + "\r").encode("ascii"))
                data = bytearray()
                deadline = time.monotonic() + (90.0 if cmd.startswith("crc") else 8.0)
                while time.monotonic() < deadline:
                    ready, _, _ = select.select([fd], [], [], 0.2)
                    if ready:
                        try:
                            data.extend(os.read(fd, 4096))
                        except BlockingIOError:
                            continue
                        text = data.decode("ascii", errors="replace")
                        # The prompt returning after the echoed command ends the reply.
                        if text.count("litex") >= 1 and text.rstrip().endswith(">"):
                            break
                t1 = time.time()
                text = data.decode("ascii", errors="replace")
                out.write(f"### {time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(t0))}"
                          f".{int((t0 % 1) * 1e6):06d}Z cmd={cmd!r} elapsed={t1 - t0:.3f}s\n")
                out.write(text.replace("\r", ""))
                out.write("\n")
                print(f"--- {cmd} ({t1 - t0:.2f}s)")
                print(text.replace("\r", ""))
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, saved)
        os.close(fd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
