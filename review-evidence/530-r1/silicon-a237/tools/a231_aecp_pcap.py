#!/usr/bin/env python3
"""Offline AECP decoder for a controller-host capture (issue 529, A231).

Reads a classic pcap (tcpdump -w, micro- or nanosecond), keeps every AECP AEM
PDU (AVTP subtype 0xFB, message type 0 or 1) in which the given entity is the
target or the controller, and prints:

  - one JSON line per such PDU (--lines), with the unsolicited flag (the u bit,
    command_type bit 15), status, sequence id, the controller id it is addressed
    to, and for GET_COUNTERS the decoded counters_valid mask and valid quadlets;
  - a summary: PDU counts keyed by message, command, u bit and whether the
    entity is the PDU's target or its controller; per command and descriptor, how many unsolicited responses the
    entity sent to each controller, the smallest gap between two pushes of the
    same descriptor to the same controller (the Milan 5.4.2.25 / Table 5.22
    one-second limit), and whether every pushed counter was non-decreasing.

usage: a231_aecp_pcap.py <pcap> <entity_eid_hex> [--lines]
"""
import json
import struct
import sys
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a231_counters_poll import decode_counters  # noqa: E402

AEM_CMDS = {0x0000: "ACQUIRE_ENTITY", 0x0001: "LOCK_ENTITY", 0x0002: "ENTITY_AVAILABLE",
            0x0003: "CONTROLLER_AVAILABLE", 0x0004: "READ_DESCRIPTOR", 0x0007: "GET_CONFIGURATION",
            0x0009: "GET_STREAM_FORMAT", 0x000F: "GET_STREAM_INFO", 0x0011: "GET_NAME",
            0x0015: "GET_SAMPLING_RATE", 0x0017: "GET_CLOCK_SOURCE", 0x0019: "GET_CONTROL",
            0x0024: "REGISTER_UNSOLICITED_NOTIFICATION", 0x0025: "DEREGISTER_UNSOLICITED_NOTIFICATION",
            0x0027: "GET_AVB_INFO", 0x0028: "GET_AS_PATH", 0x0029: "GET_COUNTERS",
            0x002B: "GET_AUDIO_MAP", 0x004B: "GET_DYNAMIC_INFO"}
DTYPES = {0: "ENTITY", 5: "STREAM_INPUT", 6: "STREAM_OUTPUT", 9: "AVB_INTERFACE", 0x24: "CLOCK_DOMAIN"}


def pcap_records(path):
    with open(path, "rb") as f:
        hdr = f.read(24)
        magic = struct.unpack("<I", hdr[:4])[0]
        if magic in (0xA1B2C3D4, 0xA1B23C4D):
            endian = "<"
        else:
            magic = struct.unpack(">I", hdr[:4])[0]
            endian = ">"
        if magic not in (0xA1B2C3D4, 0xA1B23C4D):
            raise SystemExit("not a classic pcap file")
        scale = 1e-9 if magic == 0xA1B23C4D else 1e-6
        while True:
            rh = f.read(16)
            if len(rh) < 16:
                return
            ts_s, ts_f, incl, _orig = struct.unpack(endian + "IIII", rh)
            data = f.read(incl)
            yield ts_s + ts_f * scale, data


def main():
    path, eid = sys.argv[1], bytes.fromhex(sys.argv[2])
    lines = "--lines" in sys.argv[3:]
    pushes = defaultdict(list)  # (cmd, dtype, dindex, controller) -> [(t, decoded)]
    counts = defaultdict(int)
    first_t = None
    for t, fr in pcap_records(path):
        if len(fr) < 14 + 24:
            continue
        et = struct.unpack(">H", fr[12:14])[0]
        off = 14
        if et == 0x8100:
            et = struct.unpack(">H", fr[16:18])[0]
            off = 18
        if et != 0x22F0:
            continue
        p = fr[off:]
        if p[0] != 0xFB or (p[1] & 0x0F) not in (0, 1):
            continue
        target, ctl = p[4:12], p[12:20]
        if eid not in (target, ctl):
            continue
        first_t = first_t if first_t is not None else t
        mt = p[1] & 0x0F
        status = p[2] >> 3
        cdl = struct.unpack(">H", p[2:4])[0] & 0x7FF
        seq = struct.unpack(">H", p[20:22])[0]
        ct = struct.unpack(">H", p[22:24])[0]
        u = ct >> 15
        cmd = ct & 0x7FFF
        payload = p[24:12 + cdl]
        rec = dict(t=round(t, 6), dst=fr[0:6].hex(":"), src=fr[6:12].hex(":"),
                   msg="RESPONSE" if mt else "COMMAND", u=u, cmd=AEM_CMDS.get(cmd, f"{cmd:#06x}"),
                   status=status, cdl=cdl, seq=seq, target=target.hex(), controller=ctl.hex())
        if cmd == 0x0029 and mt == 1 and len(payload) >= 8:
            rec["decoded"] = decode_counters(payload.hex())
        elif len(payload) >= 4 and cmd in (0x0027, 0x0028, 0x0004, 0x0009, 0x000F, 0x0011, 0x0017):
            rec["descriptor"] = dict(type=struct.unpack(">H", payload[0:2])[0],
                                     index=struct.unpack(">H", payload[2:4])[0])
        key = (rec["msg"], rec["cmd"], "unsolicited" if u else "solicited",
               "entity-is-target" if target == eid else "entity-is-controller")
        counts[key] += 1
        if u and mt == 1 and target == eid:
            d = rec.get("decoded") or {}
            dk = (rec["cmd"], d.get("descriptor_type", rec.get("descriptor", {}).get("type")),
                  d.get("descriptor_index", rec.get("descriptor", {}).get("index")), ctl.hex())
            pushes[dk].append((t, d))
        if lines:
            print(json.dumps(rec, separators=(",", ":")))
    print("== PDU counts (message, command, solicited/unsolicited, direction)")
    for k in sorted(counts):
        print(f"   {counts[k]:6d}  {' '.join(k)}")
    print("== unsolicited responses from the entity, per command/descriptor/controller")
    for (cmd, dtype, dindex, ctl), evs in sorted(pushes.items(), key=lambda kv: str(kv[0])):
        ts = [e[0] for e in evs]
        gaps = [b - a for a, b in zip(ts, ts[1:])]
        mono = "n/a"
        if cmd == "GET_COUNTERS":
            mono = "yes"
            for (_, a), (_, b) in zip(evs, evs[1:]):
                for name, v in b.get("counters", {}).items():
                    if v < a.get("counters", {}).get(name, 0):
                        mono = f"NO ({name} {a['counters'][name]} -> {v})"
        dname = DTYPES.get(dtype, dtype)
        gap = f"{min(gaps):.3f}s" if gaps else "n/a"
        print(f"   {cmd} {dname} {dindex} -> {ctl}: n={len(evs)} "
              f"first=+{ts[0] - first_t:.3f}s last=+{ts[-1] - first_t:.3f}s "
              f"min_gap={gap} non_decreasing={mono}")
        if cmd == "GET_COUNTERS":
            print(f"      valid={evs[0][1].get('counters_valid')} first={evs[0][1].get('counters')}")
            print(f"      valid={evs[-1][1].get('counters_valid')} last={evs[-1][1].get('counters')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
