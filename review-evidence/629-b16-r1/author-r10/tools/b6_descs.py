#!/usr/bin/env python3
"""Decode a descriptor survey (b6_ctl.py descs / dutdescs output) into the fields this lane
uses: per STREAM_INPUT/OUTPUT the clock domain, flags, current format, format list and AVB
interface index; per CLOCK_SOURCE its type, flags and location; per CLOCK_DOMAIN its
current source and list. Object names are left out (they can carry private product names)
unless --names is given, for the operator's terminal only.

usage: b6_descs.py <survey.jsonl> [--names]
"""
import json
import struct
import sys

NAMES = "--names" in sys.argv
CS_TYPE = {0: "INTERNAL", 1: "EXTERNAL", 2: "INPUT_STREAM", 0xFFFF: "EXPANSION"}
DT = {0x0005: "STREAM_INPUT", 0x0006: "STREAM_OUTPUT", 0x000A: "CLOCK_SOURCE", 0x0024: "CLOCK_DOMAIN",
      0x0009: "AVB_INTERFACE", 0x0002: "AUDIO_UNIT", 0x000E: "STREAM_PORT_INPUT", 0x000F: "STREAM_PORT_OUTPUT",
      0x001A: "CONTROL", 0x0010: "EXTERNAL_PORT_INPUT", 0x0011: "EXTERNAL_PORT_OUTPUT",
      0x0012: "INTERNAL_PORT_INPUT", 0x0013: "INTERNAL_PORT_OUTPUT", 0x0014: "AUDIO_CLUSTER", 0x0017: "AUDIO_MAP",
      0x0001: "CONFIGURATION", 0x0000: "ENTITY"}
# IEEE 1722.1 Table 7.1 codes. The audio-unit walk of the survey this lane inherited (b6_ctl.py descs,
# from lane B5) reads clusters as 0x0010 and maps as 0x0014; PR #628 records that defect. This lane
# uses the survey only for STREAM_INPUT/OUTPUT, CLOCK_SOURCE, CLOCK_DOMAIN, AVB_INTERFACE and CONTROL.


def name(b):
    return b[4:68].split(b"\0")[0].decode("utf-8", "replace")


for line in open(sys.argv[1]):
    try:
        r = json.loads(line)
    except ValueError:
        continue
    w = r.get("what", "")
    if r.get("cmd") == "GET_CLOCK_SOURCE":
        print(f"{r.get('role')} GET_CLOCK_SOURCE {r.get('status')} source={r.get('clock_source', r.get('payload', '')[8:12])}")
        continue
    if not w.startswith("desc-") or r.get("status") != "SUCCESS":
        if w.startswith("desc-"):
            print(w, r.get("status"))
        continue
    b = bytes.fromhex(r["payload"])[4:]
    t, i = struct.unpack(">HH", b[:4])
    nm = f" name={name(b)!r}" if NAMES else ""
    who = r.get("role")
    if t in (0x0005, 0x0006):
        cd, fl = struct.unpack(">HH", b[70:74])
        cur = b[74:82].hex()
        fo, nf = struct.unpack(">HH", b[82:86])
        fmts = [b[fo + 8 * k: fo + 8 * k + 8].hex() for k in range(nf)]
        avbi = struct.unpack(">H", b[126:128])[0] if len(b) >= 128 else None
        bl = struct.unpack(">I", b[128:132])[0] if len(b) >= 132 else None
        ro_, nr = struct.unpack(">HH", b[132:136]) if len(b) >= 136 else (None, None)
        red = [struct.unpack(">H", b[ro_ + 2 * k: ro_ + 2 * k + 2])[0] for k in range(nr)] if nr else []
        print(f"{who} {DT[t]} {i}: clock_domain={cd} flags={fl:#06x} current={cur} formats={fmts} "
              f"avb_if={avbi} buffer_ns={bl} redundant={red}{nm}")
    elif t == 0x000A:
        fl, ty = struct.unpack(">HH", b[70:74])
        ident = b[74:82].hex()
        lt, li = struct.unpack(">HH", b[82:86])
        print(f"{who} CLOCK_SOURCE {i}: type={CS_TYPE.get(ty, ty)} flags={fl:#06x} id={ident} "
              f"location={DT.get(lt, hex(lt))} {li}{nm}")
    elif t == 0x0024:
        cs, off, n = struct.unpack(">HHH", b[70:76])
        lst = [struct.unpack(">H", b[off + 2 * k: off + 2 * k + 2])[0] for k in range(n)]
        print(f"{who} CLOCK_DOMAIN {i}: current_source={cs} sources={lst}{nm}")
    elif t == 0x0009:
        mac = b[70:76].hex()
        fl = struct.unpack(">H", b[76:78])[0]
        print(f"{who} AVB_INTERFACE {i}: flags={fl:#06x}{nm}")
    elif t == 0x001A:
        bl = b[70:]
        print(f"{who} CONTROL {i}: len={len(b)} raw70={bl[:40].hex()}{nm}")
    else:
        print(f"{who} {DT.get(t, hex(t))} {i}: len={len(b)}{nm}")
