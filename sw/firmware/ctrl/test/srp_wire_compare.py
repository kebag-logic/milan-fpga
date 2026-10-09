#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent Clause 10.8 decoder and transmit-opportunity comparison.

The parser follows IEEE 802.1Q-2018 10.8.1 and 10.8.2, without importing either
implementation's decoder. Application-specific lengths, FourPacked presence
and increment fields are supplied separately, as 10.8.2.2/.7 require.
Explicit EndMarks and the 1500-byte frame ceiling follow ruling 6087462816.
Decoding retains encounter order. Only canonical_opportunity sorts declarations;
it preserves duplicates, and equal_opportunities preserves opportunity order.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Any
from collections.abc import Sequence


class Malformed(ValueError):
    """A captured transmitter output violates the checked wire structure."""


@dataclass(frozen=True)
class Attribute:
    """Application-defined attribute width, packing and increment fields."""
    length: int
    four_packed: bool
    increment_fields: tuple


# Application parameters, not parser behavior. Clause 10.8 deliberately leaves
# these to the application; MSRP defines them in Tables 35-1..3 and 35.2.2.8/.9.
MSRP = {
    1: Attribute(25, False, ((6, 2), (8, 6))),
    2: Attribute(34, False, ((6, 2), (8, 6))),
    3: Attribute(8, True, ((6, 2),)),
    4: Attribute(4, False, ((0, 1), (1, 1))),
}


def require(condition: bool, reason: str) -> None:
    """Reject malformed wire bytes with a precise reason."""
    if not condition:
        raise Malformed(reason)


def increment(first: bytes, delta: int, fields: Sequence[tuple[int, int]]) -> bytes:
    """Expand FirstValue + k within each application-defined field."""
    value = bytearray(first)
    for offset, width in fields:
        total = int.from_bytes(first[offset:offset + width], "big") + delta
        require(total < 1 << (8 * width), "FirstValue + k overflows its field")
        value[offset:offset + width] = total.to_bytes(width, "big")
    return bytes(value)


def decode_mrpdu(pdu: bytes, attributes: dict[int, Attribute]) -> dict[str, Any]:
    """Return events in encounter order and LeaveAll presence per type.

    No sorting, deduplication, missing-frame tolerance or cross-opportunity
    matching occurs. A zero-value LeaveAll survives in the per-type flags.
    """
    require(len(pdu) >= 3 and pdu[0] == 0, "ProtocolVersion or truncated PDU")
    offset = 1
    messages = 0
    events = []
    leave_all = set()
    while True:
        require(offset + 2 <= len(pdu), "missing PDU EndMark")
        if pdu[offset:offset + 2] == b"\0\0":
            offset += 2
            break
        require(offset + 4 <= len(pdu), "truncated Message header")
        kind, length = pdu[offset:offset + 2]
        require(kind in attributes, "unknown AttributeType")
        attr = attributes[kind]
        require(length == attr.length, "inconsistent AttributeLength")
        list_length = int.from_bytes(pdu[offset + 2:offset + 4], "big")
        offset += 4
        end = offset + list_length
        require(list_length >= 2 and end <= len(pdu) - 2,
                "inconsistent AttributeListLength")
        vectors = 0
        while True:
            require(offset + 2 <= end, "missing AttributeList EndMark")
            header = int.from_bytes(pdu[offset:offset + 2], "big")
            offset += 2
            if header == 0:
                require(offset == end, "early AttributeList EndMark")
                break
            flag, count = divmod(header, 8192)
            require(flag in (0, 1), "reserved LeaveAllEvent")
            require(flag == 1 or count > 0, "empty non-LeaveAll vector")
            if flag:
                leave_all.add(kind)
            three_count = (count + 2) // 3
            four_count = (count + 3) // 4 if attr.four_packed else 0
            stop = offset + length + three_count + four_count
            require(stop <= end - 2, "truncated vector or AttributeList EndMark")
            first = pdu[offset:offset + length]
            three = pdu[offset + length:offset + length + three_count]
            four = pdu[offset + length + three_count:stop]
            require(all(v < 216 for v in three), "reserved ThreePackedEvents")
            unpacked = []
            for packed in three:
                unpacked.extend((packed // 36, (packed // 6) % 6, packed % 6))
            subtypes = []
            for packed in four:
                subtypes.extend((packed >> 6, (packed >> 4) & 3,
                                 (packed >> 2) & 3, packed & 3))
            # Transmitters encode unused packed-event positions as zero.
            require(not any(unpacked[count:]), "nonzero ThreePacked padding")
            require(not any(subtypes[count:]), "nonzero FourPacked padding")
            for k in range(count):
                value = increment(first, k, attr.increment_fields)
                events.append((kind, value.hex(), unpacked[k],
                               subtypes[k] if attr.four_packed else None))
            offset = stop
            vectors += 1
        require(vectors > 0, "empty AttributeList")
        messages += 1
    require(messages > 0, "empty MRPDU")
    require(not any(pdu[offset:]), "nonzero bytes after PDU EndMark")
    return {
        "events": [(*event, event[0] in leave_all) for event in events],
        "leave_all_types": sorted(leave_all),
    }


def decode_frame(frame: bytes) -> dict[str, Any]:
    """Decode an untagged MSRP frame including its Ethernet identity."""
    require(17 <= len(frame) <= 1500, "frame length outside 17..1500")
    require(frame[:6] == bytes.fromhex("0180c200000e"), "MSRP destination")
    require(frame[12:14] == bytes.fromhex("22ea"), "MSRP EtherType")
    return {"ethernet_header": frame[:14].hex(), **decode_mrpdu(frame[14:], MSRP)}


def canonical_opportunity(frames: Sequence[bytes]) -> dict[str, Any]:
    """Canonical multiset within ONE opportunity, retaining every declaration.

    IEEE 802.1Q 10.8.1/.2 permits arbitrary message/vector order. Multiple
    frames from one opportunity are combined, without crossing its boundary.
    Empty LeaveAll vectors remain observable through their per-type flags.
    """
    decoded = [decode_frame(frame) for frame in frames]
    headers = {item["ethernet_header"] for item in decoded}
    require(len(headers) <= 1, "mixed Ethernet headers within an opportunity")
    events = [event for item in decoded for event in item["events"]]
    leave_all = {kind for item in decoded for kind in item["leave_all_types"]}
    return {
        "ethernet_header": next(iter(headers), None),
        "events": sorted(events, key=lambda event: (event[0], event[1], event[2],
                                                   -1 if event[3] is None else event[3], event[4])),
        "leave_all_types": sorted(leave_all),
    }


def equal_opportunities(fabric: Sequence[Sequence[bytes]], split: Sequence[Sequence[bytes]]) -> bool:
    """Compare paired opportunities in order, never searching ahead."""
    return ([canonical_opportunity(frames) for frames in fabric] ==
            [canonical_opportunity(frames) for frames in split])


def equal_frame_opportunity(fabric: bytes, split: bytes) -> bool:
    """One paired opportunity, containing one frame on each side."""
    return equal_opportunities([[fabric]], [[split]])


def message(kind: int, first: bytes, count: int, three: bytes = b"",
            four: bytes = b"", leave_all: bool = False) -> bytes:
    """Fixture builder: vectors can also be constructed directly as literals."""
    header = (count + (8192 if leave_all else 0)).to_bytes(2, "big")
    vector = header + first + three + four + b"\0\0"
    return bytes((kind, len(first))) + len(vector).to_bytes(2, "big") + vector


def fixture(messages: Sequence[bytes]) -> bytes:
    """Construct a complete frame around independent literal Messages."""
    return bytes.fromhex("0180c200000e0a0b0c0d0e0f22ea00") + b"".join(messages) + b"\0\0"


def controls() -> dict[str, Any]:
    """Prove packing/order tolerance and rejection of named planted defects."""
    sid1 = bytes.fromhex("1122334455660001")
    sid2 = bytes.fromhex("1122334455660002")
    one = message(3, sid1, 1, b"\0", b"\x80")
    two = message(3, sid2, 1, b"\0", b"\x80")
    packed = fixture([message(3, sid1, 2, b"\0", b"\xa0")])
    unpacked = fixture([one, two])
    expected = [(3, sid1.hex(), 0, 2, False), (3, sid2.hex(), 0, 2, False)]
    assert decode_frame(packed)["events"] == expected
    assert decode_frame(unpacked)["events"] == expected
    assert packed != unpacked and equal_frame_opportunity(packed, unpacked)
    assert equal_frame_opportunity(packed, unpacked.ljust(60, b"\0"))
    mutations = {
        "plus-k-off-by-one": fixture([one, message(3, bytes.fromhex("1122334455660003"), 1,
                                                   b"\0", b"\x80")]),
        "wrong-AttributeEvent": fixture([one, message(3, sid2, 1, b"\x24", b"\x80")]),
        "wrong-FourPackedEvent": fixture([one, message(3, sid2, 1, b"\0", b"\x40")]),
        "dropped-declaration": fixture([one]),
        "extra-declaration": fixture([one, two, two]),
    }
    assert equal_frame_opportunity(packed, fixture([two, one]))
    assert equal_opportunities([[packed]], [[fixture([one]), fixture([two])]])
    later = fixture([message(3, sid1, 1, b"\x24", b"\x80")])
    assert not equal_opportunities([[packed], [later]], [[later], [packed]])
    assert not equal_opportunities([[packed], [later]], [[packed, later]])
    results = [{"plant": "swapped-opportunities", "caught_by": "ordered opportunity comparison"},
               {"plant": "collapsed-opportunities", "caught_by": "ordered opportunity comparison"}]
    for name, mutated in mutations.items():
        assert not equal_frame_opportunity(packed, mutated), name
        results.append({"plant": name, "caught_by": "canonical multiset comparison"})
    good_la = fixture([message(3, sid1, 0, leave_all=True),
                       message(4, bytes.fromhex("06030002"), 1, b"\0")])
    bad_la = fixture([message(4, bytes(4), 0, leave_all=True),
                      message(4, bytes.fromhex("06030002"), 1, b"\0")])
    assert decode_frame(good_la)["leave_all_types"] == [3]
    assert decode_frame(bad_la)["leave_all_types"] == [4]
    assert not equal_frame_opportunity(good_la, bad_la)
    results.append({"plant": "LeaveAll-wrong-attribute-type", "caught_by": "per-type LeaveAll comparison"})
    malformed = {}
    for name, offset, value in (
        ("malformed-PDU-EndMark", len(packed) - 1, 1),
        ("malformed-list-EndMark", len(packed) - 3, 1),
        ("wrong-ProtocolVersion", 14, 1),
        ("wrong-AttributeLength", 16, 9),
        ("wrong-AttributeListLength", 18, 13),
        ("reserved-ThreePackedEvents", 29, 216),
        ("reserved-LeaveAllEvent", 19, 64),
    ):
        data = bytearray(packed)
        data[offset] = value
        malformed[name] = bytes(data)
    malformed["truncated-PDU-EndMark"] = packed[:-1]
    malformed["oversized-frame"] = packed.ljust(1501, b"\0")
    for name, data in malformed.items():
        try:
            decode_frame(data)
        except Malformed as error:
            results.append({"plant": name, "caught_by": str(error)})
        else:
            raise AssertionError(f"escaped: {name}")
    # Independent literals exercise event packing across byte boundaries.
    five = fixture([message(3, sid1, 5, bytes((8, 138)), bytes((108, 64)))])
    assert [row[2] for row in decode_frame(five)["events"]] == [0, 1, 2, 3, 5]
    assert [row[3] for row in decode_frame(five)["events"]] == [1, 2, 3, 0, 1]
    assert [row[1] for row in decode_frame(five)["events"]] == [
        f"112233445566{k:04x}" for k in range(1, 6)]
    return {"packing_only": "PASS", "within_opportunity_order": "PASS",
            "frame_grouping": "PASS", "zero_padding": "PASS",
            "five_value_vector": "PASS", "plants": results}


def main() -> int:
    """Check controls and optionally compare a capture; unequal exits one."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = {"controls": controls()} if args.self_test else {}
    if args.capture:
        capture = json.loads(args.capture.read_text())
        opportunities = {}
        for name in ("fabric", "split"):
            frames = capture["frames"][name]
            if isinstance(frames, str):
                frames = [frames]
            opportunities[name] = [[bytes.fromhex(frame)] for frame in frames]
        equal = equal_opportunities(opportunities["fabric"], opportunities["split"])
        report.update(equal=equal,
                      decoded={name: [[decode_frame(frame) for frame in opportunity]
                                      for opportunity in sequence]
                               for name, sequence in opportunities.items()},
                      canonical={name: [canonical_opportunity(opportunity) for opportunity in sequence]
                                 for name, sequence in opportunities.items()})
    else:
        equal = True
        if not args.self_test:
            parser.error("supply a capture or --self-test")
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
