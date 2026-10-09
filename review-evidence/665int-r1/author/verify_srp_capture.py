#!/usr/bin/env python3
"""Distinguish a reproduced encoding mismatch from a raw equality pass."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys


def listener_records(frame):
    """Decode complete single/multi-vector Listener messages, not normalized bytes."""
    assert frame[:6] == bytes.fromhex("0180c200000e")
    assert frame[6:12] == bytes.fromhex("0a0b0c0d0e0f")
    assert frame[12:15] == bytes.fromhex("22ea00")
    off = 15
    records = []
    vectors = []
    while frame[off:off + 2] != b"\0\0":
        assert frame[off:off + 2] == b"\x03\x08"
        end = off + 4 + int.from_bytes(frame[off + 2:off + 4], "big")
        off += 4
        assert end <= len(frame) - 2
        while frame[off:off + 2] != b"\0\0":
            header = int.from_bytes(frame[off:off + 2], "big")
            assert header >> 13 == 0
            count = header & 8191
            assert 0 < count <= 2
            identity = int.from_bytes(frame[off + 2:off + 10], "big")
            three = frame[off + 10]
            four = frame[off + 11]
            vectors.append(count)
            for index in range(count):
                event = three // (6 ** (2 - index)) % 6
                subtype = (four >> (6 - 2 * index)) & 3
                records.append((identity + index, event, subtype))
            off += 12
        off += 2
        assert off == end
    assert off + 2 == len(frame)
    return sorted(records), vectors


def exact_witness(capture):
    a = bytes.fromhex(capture["frames"]["fabric"])
    b = bytes.fromhex(capture["frames"]["split"])
    expected = [(0x1122334455660001, 0, 2), (0x1122334455660002, 0, 2)]
    assert listener_records(a) == (expected, [2])
    assert listener_records(b) == (expected, [1, 1])
    header = bytes.fromhex("0180c200000e0a0b0c0d0e0f22ea00")
    message = bytes.fromhex("0308000e")
    sid1 = (0x1122334455660001).to_bytes(8, "big")
    sid2 = (0x1122334455660002).to_bytes(8, "big")
    assert a == header + message + b"\0\x02" + sid1 + bytes.fromhex("00a000000000")
    assert b == header + message + b"\0\x01" + sid2 + bytes.fromhex("00800000") + \
        message + b"\0\x01" + sid1 + bytes.fromhex("008000000000")
    assert len(a) == 35 and len(b) == 53 and a[20] == 2 and b[20] == 1
    assert a != b and a.ljust(60, b"\0") != b.ljust(60, b"\0")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    parser.add_argument("--require-equal", action="store_true")
    args = parser.parse_args()
    capture = json.loads(args.capture.read_text())
    frames = capture["frames"]
    if args.require_equal:
        equal = bytes.fromhex(frames["fabric"]) == bytes.fromhex(frames["split"])
        print("SRP RAW EQUALITY:", "PASS" if equal else "FAIL (outside processor#168)")
        return 0 if equal else 1
    exact_witness(capture)
    caught = []
    for name, placement, replacement, offset in (
        ("split-copies-fabric", "split", frames["fabric"], None),
        ("fabric-copies-split", "fabric", frames["split"], None),
        ("off-ledger-source-mac", "split", None, 6),
        ("wrong-listener-declaration", "split", None, 30),
        ("truncated-frame", "fabric", frames["fabric"][:-2], None),
    ):
        changed = deepcopy(capture)
        if offset is not None:
            raw = bytearray.fromhex(changed["frames"][placement])
            raw[offset] ^= 1 if offset != 30 else 0x40
            replacement = raw.hex()
        changed["frames"][placement] = replacement
        try:
            exact_witness(changed)
        except (AssertionError, IndexError):
            caught.append(name)
        else:
            raise AssertionError(f"escaped: {name}")
    child = subprocess.run([sys.executable, str(Path(__file__).resolve()), str(args.capture.resolve()),
                            "--require-equal"], text=True, capture_output=True, check=False, timeout=30)
    assert child.returncode == 1 and "SRP RAW EQUALITY: FAIL" in child.stdout
    print(child.stdout, end="")
    print("PASS: identical declaration set; exact unapproved encoding difference reproduced")
    print("PASS: 5/5 controls caught:", ", ".join(caught))
    print("Diagnostic rc 0 is not an equality verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
