#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Post-flash smoke test for the Milan bare-metal UART console."""

import argparse
import os
import re
import select
import sys
import termios
import time
import tty


STATUS_RE = re.compile(
    r"ID=([0-9A-Fa-f]{8})\s+VERSION=([0-9A-Fa-f]{8})\s+"
    r"PTP_CTRL=([0-9A-Fa-f]{8})\s+ADP_CTRL=([0-9A-Fa-f]{8})\s+"
    r"PP_CTRL=([0-9A-Fa-f]{8})\s+PP_STAT=([0-9A-Fa-f]{8})\s+"
    r"AEM=(loaded|disabled)"
)
TAI_RE = re.compile(r"TAI_NS=0x([0-9A-Fa-f]{16})")
BAUDS = {
    9600: termios.B9600,
    19200: termios.B19200,
    38400: termios.B38400,
    57600: termios.B57600,
    115200: termios.B115200,
}


def parse_status(text):
    match = STATUS_RE.search(text)
    if match is None:
        raise ValueError("milan_status response is missing or malformed")
    values = [int(word, 16) for word in match.groups()[:6]]
    return dict(zip(("id", "version", "ptp", "adp", "pp", "pp_stat"), values),
                aem=match.group(7))


def parse_tai(text):
    match = TAI_RE.search(text)
    if match is None:
        raise ValueError("milan_gettime response has no TAI_NS word")
    return int(match.group(1), 16)


def grade(status_text, first_time_text, second_time_text):
    status = parse_status(status_text)
    first = parse_tai(first_time_text)
    second = parse_tai(second_time_text)
    checks = [
        ("id-miln", status["id"] == 0x4D494C4E,
         f"ID=0x{status['id']:08X} VERSION=0x{status['version']:08X}"),
        ("aem-image", status["aem"] == "loaded",
         f"AEM={status['aem']}"),
        ("fabric-enabled", bool(status["ptp"] & 1) and
         bool(status["adp"] & 1) and bool(status["pp"] & 1),
         f"PTP=0x{status['ptp']:08X} ADP=0x{status['adp']:08X} "
         f"PP=0x{status['pp']:08X}"),
        ("phc-advances", second > first,
         f"0x{first:016X} -> 0x{second:016X}"),
    ]
    return checks


class Console:
    def __init__(self, path, baud):
        if baud not in BAUDS:
            raise ValueError(f"unsupported baud {baud}; choose {sorted(BAUDS)}")
        self.fd = os.open(path, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        self.saved = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        attrs = termios.tcgetattr(self.fd)
        attrs[4] = BAUDS[baud]
        attrs[5] = BAUDS[baud]
        termios.tcsetattr(self.fd, termios.TCSANOW, attrs)

    def close(self):
        if self.fd is not None:
            termios.tcsetattr(self.fd, termios.TCSANOW, self.saved)
            os.close(self.fd)
            self.fd = None

    def command(self, command, pattern, timeout):
        termios.tcflush(self.fd, termios.TCIFLUSH)
        os.write(self.fd, (command + "\r").encode("ascii"))
        deadline = time.monotonic() + timeout
        data = bytearray()
        while time.monotonic() < deadline:
            ready, _, _ = select.select([self.fd], [], [],
                                        min(0.2, deadline - time.monotonic()))
            if ready:
                try:
                    chunk = os.read(self.fd, 4096)
                except BlockingIOError:
                    continue
                data.extend(chunk)
                text = data.decode("ascii", errors="replace")
                if pattern.search(text):
                    return text
        text = data.decode("ascii", errors="replace")
        raise TimeoutError(f"timeout waiting for {pattern.pattern!r}; got {text!r}")

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()


def self_test():
    status = ("ID=4d494c4e VERSION=00000054 PTP_CTRL=00000001 "
              "ADP_CTRL=00000001 PP_CTRL=00000001 PP_STAT=5b000010 "
              "AEM=loaded\nTAI_NS=0x0000000100000000\n")
    checks = grade(status, "TAI_NS=0x0000000100001000\n",
                   "TAI_NS=0x0000000100002000\n")
    assert all(ok for _name, ok, _detail in checks)
    assert not grade(status.replace("AEM=loaded", "AEM=disabled"),
                     "TAI_NS=0x0000000000000002\n",
                     "TAI_NS=0x0000000000000002\n")[1][1]
    try:
        parse_status("ID=not-a-status")
    except ValueError:
        pass
    else:
        raise AssertionError("malformed status was accepted")
    print("BAREMETAL UART SMOKE SELF-TEST: PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="UART device, for example /dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.port:
        parser.error("--port is required unless --self-test is used")

    try:
        with Console(args.port, args.baud) as console:
            status = console.command("milan_status", STATUS_RE, args.timeout)
            first = console.command("milan_gettime", TAI_RE, args.timeout)
            time.sleep(0.2)
            second = console.command("milan_gettime", TAI_RE, args.timeout)
        checks = grade(status, first, second)
    except (OSError, ValueError, TimeoutError) as error:
        print(f"BAREMETAL UART SMOKE: FAIL ({error})", file=sys.stderr)
        return 1

    failures = 0
    for name, ok, detail in checks:
        print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} ({detail})")
        failures += not ok
    if failures:
        print(f"BAREMETAL UART SMOKE: FAIL ({failures} check(s) failed)")
        return 1
    print(f"BAREMETAL UART SMOKE: PASS ({len(checks)}/{len(checks)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
