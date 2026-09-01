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
    r"AEM=(loaded|disabled)\s+"
    r"GPTP_GM=([0-9A-Fa-f]{16})\s+"
    r"GPTP_PARENT=([0-9A-Fa-f]{16})\s+"
    r"PDELAY_NS=([0-9]+)\s+AS_PATH_COUNT=([0-9]+)\s+"
    r"AS_PATH_GEN=([0-9]+)\s+CLKV_STAT=([0-9A-Fa-f]{8})\s+"
    r"SYNC=([01])\s+ASCAPABLE=([01])\s+TU=([01])"
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
    return {
        "id": int(match.group(1), 16),
        "version": int(match.group(2), 16),
        "ptp": int(match.group(3), 16),
        "adp": int(match.group(4), 16),
        "pp": int(match.group(5), 16),
        "pp_stat": int(match.group(6), 16),
        "aem": match.group(7),
        "gm": int(match.group(8), 16),
        "parent": int(match.group(9), 16),
        "pdelay_ns": int(match.group(10), 10),
        "path_count": int(match.group(11), 10),
        "path_gen": int(match.group(12), 10),
        "clkv_stat": int(match.group(13), 16),
        "sync": int(match.group(14), 10),
        "as_capable": int(match.group(15), 10),
        "tu": int(match.group(16), 10),
    }


def parse_tai(text):
    match = TAI_RE.search(text)
    if match is None:
        raise ValueError("milan_gettime response has no TAI_NS word")
    return int(match.group(1), 16)


def grade(status_text, first_time_text, second_time_text):
    status = parse_status(status_text)
    first = parse_tai(first_time_text)
    second = parse_tai(second_time_text)
    clkv_sync = (status["clkv_stat"] >> 1) & 1
    clkv_as_capable = (status["clkv_stat"] >> 16) & 1
    clkv_tu = status["clkv_stat"] & 1
    clkv_fields_match = (status["sync"] == clkv_sync and
                         status["as_capable"] == clkv_as_capable and
                         status["tu"] == clkv_tu)
    # Product fabric ownership leaves the compatibility fields at zero.
    fabric_reserved_fields_clear = not (status["clkv_stat"] & 0x0000FFF4)
    checks = [
        ("id-miln", status["id"] == 0x4D494C4E,
         f"ID=0x{status['id']:08X} VERSION=0x{status['version']:08X}"),
        ("version-gptp-publication",
         status["version"] >> 16 == 2 and
         (status["version"] & 0xFFFF) >= 0x0056,
         f"VERSION=0x{status['version']:08X} (need major 2, minor >= 0x0056)"),
        ("aem-image", status["aem"] == "loaded",
         f"AEM={status['aem']}"),
        ("fabric-enabled", bool(status["ptp"] & 1) and
         bool(status["adp"] & 1) and bool(status["pp"] & 1),
         f"PTP=0x{status['ptp']:08X} ADP=0x{status['adp']:08X} "
         f"PP=0x{status['pp']:08X}"),
        ("gptp-identities", status["gm"] != 0 and status["parent"] != 0,
         f"GM=0x{status['gm']:016X} PARENT=0x{status['parent']:016X}"),
        ("gptp-path", 1 <= status["path_count"] <= 8 and
         0 <= status["path_gen"] <= 15,
         f"count={status['path_count']} generation={status['path_gen']}"),
        ("gptp-pdelay", 0 < status["pdelay_ns"] < 800,
         f"pdelay={status['pdelay_ns']} ns (need a measured 0 < delay < 800 ns)"),
        ("clkv-fabric-owner", clkv_fields_match and
         fabric_reserved_fields_clear,
         f"CLKV_STAT=0x{status['clkv_stat']:08X} "
         f"SYNC={status['sync']} ASCAPABLE={status['as_capable']} "
         f"TU={status['tu']}"),
        ("gptp-locked", bool(status["sync"]) and
         bool(status["as_capable"]) and not bool(status["tu"]),
         f"SYNC={status['sync']} ASCAPABLE={status['as_capable']} "
         f"TU={status['tu']}"),
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
    status = ("ID=4d494c4e VERSION=00020056 PTP_CTRL=00000001 "
              "ADP_CTRL=00000001 PP_CTRL=00000001 PP_STAT=5b000010 "
              "AEM=loaded\n"
              "GPTP_GM=001bc5fffe001122 "
              "GPTP_PARENT=001bc5fffe334455 PDELAY_NS=600 "
              "AS_PATH_COUNT=3 AS_PATH_GEN=7 CLKV_STAT=00010002 "
              "SYNC=1 ASCAPABLE=1 TU=0\n"
              "TAI_NS=0x0000000100000000\n")
    parsed = parse_status(status)
    assert parsed["gm"] == 0x001BC5FFFE001122
    assert parsed["parent"] == 0x001BC5FFFE334455
    assert parsed["pdelay_ns"] == 600
    assert parsed["path_count"] == 3 and parsed["path_gen"] == 7
    checks = grade(status, "TAI_NS=0x0000000100001000\n",
                   "TAI_NS=0x0000000100002000\n")
    assert all(ok for _name, ok, _detail in checks)

    def verdict(candidate, name, first=0x1000, second=0x2000):
        results = grade(candidate, f"TAI_NS=0x{first:016X}\n",
                        f"TAI_NS=0x{second:016X}\n")
        return {check_name: ok for check_name, ok, _detail in results}[name]

    assert not verdict(status.replace("00020056", "00020055"),
                       "version-gptp-publication")
    assert not verdict(status.replace("AEM=loaded", "AEM=disabled"),
                       "aem-image")
    assert not verdict(status.replace("001bc5fffe001122",
                                      "0000000000000000"),
                       "gptp-identities")
    assert not verdict(status.replace("AS_PATH_COUNT=3", "AS_PATH_COUNT=0"),
                       "gptp-path")
    assert not verdict(status.replace("PDELAY_NS=600", "PDELAY_NS=800"),
                       "gptp-pdelay")
    assert not verdict(status.replace("PDELAY_NS=600", "PDELAY_NS=0"),
                       "gptp-pdelay")
    assert not verdict(status.replace("CLKV_STAT=00010002",
                                      "CLKV_STAT=00010003"),
                       "clkv-fabric-owner")
    unhealthy = status.replace(
        "CLKV_STAT=00010002 SYNC=1 ASCAPABLE=1 TU=0",
        "CLKV_STAT=00000001 SYNC=0 ASCAPABLE=0 TU=1")
    assert not verdict(unhealthy, "gptp-locked")
    assert not verdict(status, "phc-advances", first=0x2000, second=0x2000)

    malformed = [
        "ID=not-a-status",
        status.splitlines()[0],  # The pre-publication status is now refused.
        status.replace(" ASCAPABLE=1", ""),
    ]
    for candidate in malformed:
        try:
            parse_status(candidate)
        except ValueError:
            pass
        else:
            raise AssertionError(f"malformed status was accepted: {candidate!r}")
    print("BAREMETAL UART SMOKE SELF-TEST: PASS (12 negative arms)")


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
