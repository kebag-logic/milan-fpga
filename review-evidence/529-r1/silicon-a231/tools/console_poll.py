#!/usr/bin/env python3
"""Timed read-only console poller for the AX7101 bare-metal console (issue 117, A200).

Every <period> seconds for <duration> seconds, sends each command in turn and
appends a timestamped transcript. Only the read-only commands accepted by
console_read.py are allowed. The caller holds the bench lock.

usage: console_poll.py <port> <transcript> <duration_s> <period_s> <command> [<command> ...]
"""
import os
import select
import sys
import termios
import time
import tty

READ_ONLY = ("milan_status", "milan_gettime", "milan_nvm", "mem_list", "crc ", "mem_read ")


def check(cmd: str) -> None:
    if cmd != "milan_nvm" and not cmd.startswith(READ_ONLY):
        raise SystemExit(f"refused: {cmd!r} is not a read-only command")
    if cmd.startswith("milan_nvm") and cmd != "milan_nvm":
        raise SystemExit(f"refused: {cmd!r} (only the bare status form)")


def transact(fd: int, cmd: str) -> tuple[float, float, str]:
    termios.tcflush(fd, termios.TCIFLUSH)
    t0 = time.time()
    os.write(fd, (cmd + "\r").encode("ascii"))
    data = bytearray()
    deadline = time.monotonic() + 8.0
    while time.monotonic() < deadline:
        ready, _, _ = select.select([fd], [], [], 0.2)
        if ready:
            try:
                data.extend(os.read(fd, 4096))
            except BlockingIOError:
                continue
            text = data.decode("ascii", errors="replace")
            if text.count("litex") >= 1 and text.rstrip().endswith(">"):
                break
    return t0, time.time(), data.decode("ascii", errors="replace").replace("\r", "")


def main() -> int:
    port, out_path = sys.argv[1], sys.argv[2]
    duration, period = float(sys.argv[3]), float(sys.argv[4])
    commands = sys.argv[5:]
    for cmd in commands:
        check(cmd)
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        attrs = termios.tcgetattr(fd)
        attrs[4] = attrs[5] = termios.B115200
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        end = time.monotonic() + duration
        nxt = time.monotonic()
        rounds = 0
        with open(out_path, "w") as out:
            while time.monotonic() < end:
                for cmd in commands:
                    t0, t1, text = transact(fd, cmd)
                    out.write(f"### {time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(t0))}"
                              f".{int((t0 % 1) * 1e6):06d}Z cmd={cmd!r} elapsed={t1 - t0:.3f}s\n")
                    out.write(text)
                    out.write("\n")
                out.flush()
                rounds += 1
                nxt += period
                delay = nxt - time.monotonic()
                if delay > 0:
                    time.sleep(min(delay, max(0.0, end - time.monotonic())))
        print(f"rounds={rounds}")
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, saved)
        os.close(fd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
