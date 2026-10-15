#!/usr/bin/env python3
"""Lane B17 (new): the SoC board's serial console, one harmless read-only check.

usage: soc_check_b17.py <port> <transcript>
The caller holds the bench lock. Sends one empty line and reads what the console shows. Only if
the last line is a root shell prompt (ends with "# ") does it send the board script's read-only
`status` verb (never `up` or `down`) and read until the prompt returns. On a login prompt, or
anything else, it sends nothing more and exits 3 (the assignment's STOP: the manager logs in;
no credential is ever typed or stored). Writes a timestamped transcript.
"""
import os
import select
import sys
import termios
import time
import tty


def read_for(fd, seconds, until=None):
    data = bytearray()
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        r, _, _ = select.select([fd], [], [], 0.1)
        if r:
            try:
                data.extend(os.read(fd, 4096))
            except BlockingIOError:
                continue
            if until and until(data.decode("utf-8", "replace")):
                break
    return data.decode("utf-8", "replace").replace("\r", "")


def main() -> int:
    port, out_path = sys.argv[1], sys.argv[2]
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    rc = 0
    with open(out_path, "w") as out:
        try:
            tty.setraw(fd)
            attrs = termios.tcgetattr(fd)
            attrs[4] = attrs[5] = termios.B115200
            termios.tcsetattr(fd, termios.TCSANOW, attrs)
            termios.tcflush(fd, termios.TCIFLUSH)
            out.write(f"### {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} send: empty line\n")
            os.write(fd, b"\r")
            text = read_for(fd, 2.0)
            out.write(text + "\n")
            last = text.rstrip("\n").splitlines()[-1] if text.strip() else ""
            if last.endswith("# ") or last.rstrip().endswith("#"):
                out.write(f"### {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} root prompt; send: status verb\n")
                os.write(fd, b"tdm8-uac2.sh status\r")
                text = read_for(fd, 8.0, until=lambda t: t.count("\n") >= 2 and t.rstrip().endswith("#"))
                out.write(text + "\n")
                print("ROOT_PROMPT")
            elif "login" in last.lower():
                print("LOGIN_PROMPT: STOP")
                rc = 3
            else:
                print(f"UNKNOWN_CONSOLE_STATE: nothing sent beyond the empty line ({len(text)} chars)")
                rc = 3
        finally:
            termios.tcsetattr(fd, termios.TCSANOW, saved)
            os.close(fd)
    return rc


if __name__ == "__main__":
    sys.exit(main())
