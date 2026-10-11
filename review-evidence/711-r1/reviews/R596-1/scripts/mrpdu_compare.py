#!/usr/bin/env python3
"""mrpdu_compare.py BASE_DIR HEAD_DIR [--control NAME] [--json OUT]

Reviewer-written MRPDU decoder and base/head comparison. It is written from
IEEE 802.1Q-2018 10.8.1.2 (MRPDU and Message structure), 10.8.2.4 to 10.8.2.10
(AttributeType, AttributeLength, VectorHeader, LeaveAllEvent, NumberOfValues,
FirstValue, ThreePackedEvents, EndMark), 35.2.2.4 to 35.2.2.7 (MSRP
AttributeListLength, attribute types and lengths, FourPackedEvents for the
Listener) and 11.2.3.1 (MVRP VID attribute). It shares no code with lwSRP, the
firmware fixtures or the lane's own decoder.

Inputs are dump directories: one text file per test executable with lines
"R" (host model reset) or "F <interface> <now_ms> <len> <hex>" (one SRP-channel
TX frame). Files are paired by name, segments by reset order, frames by order.

For every pair it compares interface, model time, Ethernet header, ProtocolVersion,
the set of LeaveAll AttributeTypes, and the multiset of decoded
(AttributeType, value, AttributeEvent, FourPackedEvent) tuples. It grades every
head MRPDU for the grouped form: one Message per AttributeType, types ascending,
a LeaveAll vector (NumberOfValues 0) only first, every other vector
NumberOfValues 1 without LeaveAll, FirstValue strictly ascending. On both sides
it checks that a type's LeaveAll precedes that type's values in the PDU.

Controls (--control): drop-event, change-event, change-byte (one ThreePacked
octet of one head frame altered before decoding), swap (head graded as base).
Exit 0 only with no problem and no decoded difference.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

MSRP, MVRP = 0x22EA, 0x88F5
# 35.2.2.4 Table 35-? (MSRP attribute types) and 11.2.3.1.6 (MVRP VID).
ATTR_LEN = {MSRP: {1: 25, 2: 34, 3: 8, 4: 4}, MVRP: {1: 2}}
LISTENER = 3


class Malformed(Exception):
    pass


def u16(b: bytes, o: int) -> int:
    if o + 2 > len(b):
        raise Malformed(f"read past end at {o}")
    return (b[o] << 8) | b[o + 1]


def add_int(value: bytes, k: int) -> bytes:
    n = int.from_bytes(value, "big") + k
    return (n % (1 << (8 * len(value)))).to_bytes(len(value), "big")


def decode(frame: bytes) -> dict:
    """Decode one Ethernet frame carrying an MRPDU (no VLAN tag)."""
    if len(frame) < 17:
        raise Malformed("short frame")
    et = u16(frame, 12)
    if et not in (MSRP, MVRP):
        return {"ethertype": et, "raw": frame.hex()}
    msrp = et == MSRP
    o = 14
    pv = frame[o]; o += 1
    messages = []          # (type, [vectors]) where vector = (la, n, firstvalue, events, four)
    while True:
        if o + 2 > len(frame):
            raise Malformed("no MRPDU EndMark")
        if frame[o] == 0 and frame[o + 1] == 0:
            o += 2
            break
        atype, alen = frame[o], frame[o + 1]; o += 2
        want = ATTR_LEN[et].get(atype)
        if want is None or alen != want:
            raise Malformed(f"type {atype} length {alen}")
        list_end = None
        if msrp:
            list_end = o + 2 + u16(frame, o); o += 2
            if list_end > len(frame):
                raise Malformed("AttributeListLength past frame")
        vectors = []
        while True:
            if o + 2 > len(frame):
                raise Malformed("no AttributeList EndMark")
            if frame[o] == 0 and frame[o + 1] == 0:
                o += 2
                break
            hdr = u16(frame, o); o += 2
            la_ev, n = hdr >> 13, hdr & 0x1FFF
            if la_ev not in (0, 1):
                raise Malformed(f"LeaveAllEvent {la_ev}")
            fv = frame[o:o + alen]; o += alen
            if len(fv) != alen:
                raise Malformed("short FirstValue")
            three = frame[o:o + (n + 2) // 3]; o += (n + 2) // 3
            four = b""
            if msrp and atype == LISTENER:
                four = frame[o:o + (n + 3) // 4]; o += (n + 3) // 4
            if o > len(frame):
                raise Malformed("vector past frame")
            events, fours = [], []
            for i in range(n):
                byte = three[i // 3]
                if byte > 215:
                    raise Malformed(f"ThreePackedEvents {byte}")
                ev = (byte // 36, (byte // 6) % 6, byte % 6)[i % 3]
                events.append(ev)
                if four:
                    fours.append((four[i // 4] >> (6 - 2 * (i % 4))) & 3)
            vectors.append((la_ev == 1, n, bytes(fv), events, fours))
        if list_end is not None and o != list_end:
            raise Malformed(f"AttributeListLength mismatch {o} != {list_end}")
        messages.append((atype, vectors))
    tail = frame[o:]
    return {"ethertype": et, "pv": pv, "messages": messages, "tail_nonzero": any(tail)}


def semantics(d: dict) -> dict:
    """Layout-free meaning of one decoded MRPDU."""
    if "raw" in d:
        return {"raw": d["raw"]}
    la_types, tuples, order_ok = set(), collections.Counter(), True
    seen_values = set()
    for atype, vectors in d["messages"]:
        for la, n, fv, events, fours in vectors:
            if la:
                la_types.add(atype)
                if atype in seen_values:
                    order_ok = False      # this type's values preceded its LeaveAll
            if n > 1 and d["ethertype"] == MSRP:
                raise Malformed("MSRP NumberOfValues > 1 (increment rule not modelled)")
            for i, ev in enumerate(events):
                value = add_int(fv, i)
                tuples[(atype, value.hex(), ev, fours[i] if fours else None)] += 1
                seen_values.add(atype)
    return {"et": d["ethertype"], "pv": d["pv"], "la": sorted(la_types),
            "tuples": tuples, "la_order_ok": order_ok}


def grouped_problems(d: dict) -> list[str]:
    if "raw" in d:
        return []
    out, types = [], [m[0] for m in d["messages"]]
    if len(set(types)) != len(types):
        out.append(f"type repeated across Messages {types}")
    if types != sorted(types):
        out.append(f"types not ascending {types}")
    for atype, vectors in d["messages"]:
        values = []
        for k, (la, n, fv, events, fours) in enumerate(vectors):
            if la and (k != 0 or n != 0):
                out.append(f"type {atype}: LeaveAll vector at {k} with {n} values")
            if not la:
                if n != 1:
                    out.append(f"type {atype}: NumberOfValues {n}")
                values.append(fv)
        if values != sorted(values) or len(set(values)) != len(values):
            out.append(f"type {atype}: FirstValue not strictly ascending")
    if d["tail_nonzero"]:
        out.append("non-zero octets after the MRPDU EndMark")
    return out


def load(directory: Path) -> dict[str, list[list[tuple]]]:
    runs = {}
    for path in sorted(directory.glob("*.txt")):
        segments = [[]]
        for line in path.read_text().splitlines():
            if line == "R":
                segments.append([])
            elif line.startswith("F "):
                _, iface, ms, n, hx = line.split(" ")
                frame = bytes.fromhex(hx)
                if len(frame) != int(n):
                    raise SystemExit(f"{path}: length field mismatch")
                segments[-1].append((int(iface), int(ms), frame))
        runs[normalise(path.name)] = segments
    return runs


def normalise(name: str) -> str:
    # the executable path embeds a random build root ("..._ctrl-fw-XXXXXXXX_"); drop it
    return re.sub(r"^.*?_ctrl-fw-[^_]+_", "", name.removesuffix(".txt"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base", type=Path)
    ap.add_argument("head", type=Path)
    ap.add_argument("--control", choices=["drop-event", "change-event", "change-byte", "swap"])
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    base, head = load(a.base), load(a.head)
    if a.control == "swap":
        base, head = head, base
    problems, stats = [], collections.Counter()
    per_exe = {}
    if set(base) != set(head):
        problems.append(f"executables differ: only base {sorted(set(base)-set(head))}, only head {sorted(set(head)-set(base))}")
    planted = False
    for exe in sorted(set(base) & set(head)):
        b_segs, h_segs = base[exe], head[exe]
        es = collections.Counter()
        if len(b_segs) != len(h_segs):
            problems.append(f"{exe}: {len(b_segs)} base segments, {len(h_segs)} head")
            continue
        for si, (bs, hs) in enumerate(zip(b_segs, h_segs)):
            if len(bs) != len(hs):
                problems.append(f"{exe} segment {si}: {len(bs)} base frames, {len(hs)} head")
                continue
            for fi, ((bi, bm, bf), (hi, hm, hf)) in enumerate(zip(bs, hs)):
                where = f"{exe} seg {si} frame {fi}"
                if a.control == "change-byte" and not planted and len(hf) > 14 and u16(hf, 12) == MVRP:
                    hf = bytearray(hf)
                    # the last ThreePacked octet of the PDU's last vector: before the two EndMarks
                    end = len(hf) - 1
                    while end > 14 and hf[end] == 0:
                        end -= 1
                    hf[end] = (hf[end] + 36) % 216
                    hf = bytes(hf); planted = True
                try:
                    bd, hd = decode(bf), decode(hf)
                    bsem, hsem = semantics(bd), semantics(hd)
                except Malformed as exc:
                    problems.append(f"{where}: malformed: {exc}")
                    continue
                if "raw" in bsem or "raw" in hsem:
                    stats["non-MRP frames"] += 1
                    if bf != hf:
                        problems.append(f"{where}: non-MRP frame differs")
                    continue
                stats["MRPDUs"] += 1; es["MRPDUs"] += 1
                stats["octets base"] += len(bf); stats["octets head"] += len(hf)
                if a.control in ("drop-event", "change-event") and not planted and hsem["tuples"]:
                    key = next(iter(hsem["tuples"]))
                    hsem["tuples"][key] -= 1
                    if a.control == "change-event":
                        hsem["tuples"][(key[0], key[1], (key[2] + 1) % 6, key[3])] += 1
                    hsem["tuples"] += collections.Counter()
                    planted = True
                same = (bi, bm, bf[:14]) == (hi, hm, hf[:14]) and \
                       all(bsem[k] == hsem[k] for k in ("et", "pv", "la", "tuples"))
                for side, sem in (("base", bsem), ("head", hsem)):
                    if not sem["la_order_ok"]:
                        problems.append(f"{where}: {side} LeaveAll after a value of its type")
                for p in grouped_problems(hd):
                    problems.append(f"{where}: head not grouped: {p}")
                stats["values"] += sum(bsem["tuples"].values())
                stats["LeaveAll types"] += len(bsem["la"])
                if not same:
                    stats["decoded differently"] += 1; es["decoded differently"] += 1
                    problems.append(f"{where}: DECODED DIFFERENTLY")
                elif bf == hf:
                    stats["byte-identical"] += 1; es["byte-identical"] += 1
                else:
                    stats["layout-only"] += 1; es["layout-only"] += 1
                types = [m[0] for m in bd["messages"]]
                if len(set(types)) != len(types):
                    stats["base MRPDUs with a type in two Messages"] += 1
        per_exe[exe] = dict(es)
    stats["executables"] = len(set(base) & set(head))
    stats["segments"] = sum(len(s) for s in head.values())
    report = {"control": a.control, "stats": dict(stats), "problems": problems[:200],
              "problem_count": len(problems), "per_executable": per_exe}
    print(json.dumps({k: report[k] for k in ("control", "stats", "problem_count")}, indent=1))
    for p in problems[:20]:
        print("PROBLEM", p)
    if a.json:
        a.json.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
