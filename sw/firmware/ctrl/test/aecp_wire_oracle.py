# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Wire comparison with clause-specific differences and independent framing checks."""
from __future__ import annotations
from collections import Counter
import copy
import json
from pathlib import Path
import re

COMMANDS = {0, 1, 2, 4, 6, 7, 8, 9, 14, 15, 16, 17, 20, 21, 22, 23,
            24, 25, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 75, 0x3fff}
NOTICES = {1, 6, 8, 14, 15, 16, 20, 22, 24, 34, 35, 37, 39, 40, 41, 44, 45}


def number(frame: bytes, start: int, size: int = 2) -> int:
    """Decode network order independently of the firmware's wire helpers."""
    return int.from_bytes(frame[start:start + size], "big")


def image_rows(header: Path) -> dict[tuple[int, int], bytes]:
    """Read the generated image directory without using the core image adapter."""
    text = header.read_text().split("aecp_entity_image[] = {", 1)[1]
    blob = bytes(int(n, 16) for n in re.findall(r"0x([0-9a-f]{2})", text))
    result = {}
    first = Counter()
    for n in range(number(blob, 8)):
        at = number(blob, 12, 4) + 16 * n
        kind = number(blob, at + 2)
        offset = number(blob, at + 8, 4)
        stride = number(blob, at + 14)
        for index in range(number(blob, at + 4)):
            value = bytearray(blob[offset + stride * index:offset + stride * index + number(blob, at + 6)])
            actual = first[kind] + index
            value[2:4] = actual.to_bytes(2, "big")
            result[kind, actual] = bytes(value)
        first[kind] += number(blob, at + 4)
    return result


def framing(frame: bytes) -> None:
    """IEEE 1722.1 9.2: the captured PDU includes exactly its declared bytes."""
    assert len(frame) >= 38 and frame[12:16] in (b"\x22\xf0\xfb\x00", b"\x22\xf0\xfb\x01",
                                              b"\x22\xf0\xfb\x07"), "wire header"
    assert len(frame) == 26 + (number(frame, 16) & 2047), "declared length"


def sequences(row: dict, side: str, registry: dict) -> list[bytes]:
    """Milan 5.4.5.1: grade each registry's own sequence before removing it for comparison."""
    request = bytes.fromhex(row["request"])
    port = row["interface"]
    if row["kind"] == "command" and request[15] == 0:
        key = (port, request[26:34])
        if number(request, 36) == 36:
            registry.setdefault(key, 0)
        elif number(request, 36) == 37:
            registry.pop(key, None)
    result = []
    for raw in row[side]:
        frame = bytearray.fromhex(raw)
        framing(frame)
        if frame[15] == 1 and frame[36] & 128:
            key = (port, bytes(frame[26:34]))
            assert key in registry, "unregistered recipient"
            assert number(frame, 34) == registry[key], "unsolicited sequence"
            registry[key] = (registry[key] + 1) & 65535
            if number(frame, 36) == 0x8025:
                del registry[key]
            frame[34:36] = b"\0\0"
        result.append(bytes(frame))
    return result


def response(row: dict, core: list[bytes], descriptors: dict) -> int:
    """Check command correlation, success/refusal and descriptor bytes against their image."""
    if row["kind"] != "command":
        return -1
    request = bytes.fromhex(row["request"])
    cmd = number(request, 36)
    assert core and core[0][:12] == request[6:12] + request[:6], "response MACs"
    reply = core[0]
    assert reply[18:38] == request[18:38], "command correlation"
    if request[15] == 6:
        assert number(reply, 16) >> 11 == 0, "MVU success"
        sub = number(request, 42)
        if sub in (1, 2):
            assert len(reply) == 54 and reply[44:46] == b"\0\0", "MVU UID length"
            assert number(reply, 46, 8) == (1 if sub == 1 else 0), "MVU UID value"
        else:
            assert len(reply) == 58 and number(reply, 46, 4) == 1, "MVU version"
        return -1
    status = {0: 11, 38: 7, 0x3fff: 1}.get(cmd, 0)
    assert number(reply, 16) >> 11 == status, "command status"
    if cmd == 4:
        key = (number(request, 42), number(request, 44))
        assert reply[38:42] == b"\0" * 4 and reply[42:] == descriptors[key], "descriptor bytes"
    return cmd


def difference(row: dict, fabric: list[bytes], core: list[bytes], counts: Counter) -> None:
    """Permit only documented differences, retaining every other response byte."""
    request = bytes.fromhex(row["request"])
    cmd = number(request, 36) if row["kind"] == "command" else -1
    if cmd == 4 and number(request, 38) != 0 and number(request, 42) in (0, 1):
        assert len(fabric) == len(core) == 1, "root response count"
        assert number(fabric[0], 16) >> 11 == 7 and fabric[0][38:] == request[38:46], "fabric root refusal"
        counts["IEEE 7.4.5.1/2: ignored root configuration"] += 1
        return
    if row["kind"] == "command" and request[15] == 6 and number(request, 42) in (1, 2):
        assert len(fabric) == len(core) == 1 and number(fabric[0], 16) >> 11 == 1, "fabric UID refusal"
        assert fabric[0][18:] == request[18:26 + (number(request, 16) & 2047)], "fabric UID echo"
        counts["Milan 5.4.4.2/3: system unique ID"] += 1
        return
    if len(core) == len(fabric) + 1 and cmd in (8, 20, 34, 35):
        extra = core.pop()
        opcode = number(extra, 36)
        if cmd in (8, 20):
            assert opcode == (cmd | 0x8000) and extra[38:] == core[0][38:], "default SET notice"
            counts["Milan 5.4.5.2: saved default override"] += 1
        else:
            assert opcode == 0x800f and len(extra) == 94, "started-state notice"
            expected = 0x80000008 if cmd == 35 else 0x80000000
            assert number(extra, 42, 4) == expected and extra[90] == 0x47, "started-state body"
            counts["Milan Table 5.22: started-state GET_STREAM_INFO"] += 1
    assert len(fabric) == len(core), "frame count"
    for left, right in zip(fabric, core):
        if left != right and number(right, 36) == 0x8001 and right[38:42] == b"\0\0\0\1":
            assert left[38:42] == b"\0" * 4 and left[:38] + left[42:] == right[:38] + right[42:], "unlock flags"
            counts["IEEE 7.4.2.1: unlock flag alternatives"] += 1
        else:
            assert left == right, "unclassified wire difference"


def grade(rows: list[dict], descriptors: dict) -> dict:
    """Require the complete command, descriptor, notification and timer census."""
    registry = {"fabric": {}, "core": {}}
    commands = set()
    notices = set()
    counts = Counter()
    read = set()
    kinds = Counter()
    for row in rows:
        kinds[row["kind"]] += 1
        core = sequences(row, "core", registry["core"])
        fabric = sequences(row, "fabric", registry["fabric"])
        cmd = response(row, core, descriptors)
        if cmd >= 0:
            commands.add(cmd)
        if cmd == 4:
            read.add((number(core[0], 42), number(core[0], 44)))
        notices.update(number(p, 36) & 0x7fff for p in core if p[15] == 1 and p[36] & 128)
        if row["kind"] in ("probe", "retry"):
            assert len(core) == 1 and core[0][15] == 0 and number(core[0], 36) == 3, "availability probe"
        difference(row, fabric, core.copy(), counts)
    assert commands == COMMANDS and read == descriptors.keys(), "command/descriptor census"
    assert notices == NOTICES, "notification census"
    assert all(kinds[k] == 1 for k in ("probe", "retry", "departure", "unlock")), "timer census"
    assert sorted(counts.values()) == [2, 2, 3, 3, 4], "difference census"
    return {"observations": len(rows), "commands": sorted(commands), "notifications": sorted(notices),
            "descriptors": len(read), "differences": dict(counts)}


def controls(rows: list[dict], descriptors: dict) -> int:
    """Plant missing records, byte/status/sequence corruption and forbidden extra notices."""
    changes = ("missing", "payload", "length", "status", "sequence", "extra")
    for change in changes:
        mutant = copy.deepcopy(rows)
        if change == "missing":
            mutant.pop(0)
        else:
            index = next(i for i, r in enumerate(mutant) if len(r["core"]) > 1) if change == "sequence" else 0
            frame = bytearray.fromhex(mutant[index]["core"][-1])
            offset = {"payload": 50, "length": 17, "status": 16, "sequence": 35, "extra": 36}[change]
            frame[offset] ^= 1
            if change == "extra":
                mutant[index]["core"].append(frame.hex())
            else:
                mutant[index]["core"][-1] = frame.hex()
        try:
            grade(mutant, descriptors)
        except AssertionError:
            continue
        raise AssertionError(f"wire control escaped: {change}")
    return len(changes)


def check(log: Path, header: Path) -> dict:
    """Read complete observations, then grade both the baseline and every negative control."""
    rows = [json.loads(line[5:]) for line in log.read_text().splitlines() if line.startswith("WIRE ")]
    descriptors = image_rows(header)
    report = grade(rows, descriptors)
    report["planted_controls"] = controls(rows, descriptors)
    return report
