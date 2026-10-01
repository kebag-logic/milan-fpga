#!/usr/bin/env python3
"""Decode the AUDIO_UNIT and STREAM_PORT descriptors in a published survey record
(IEEE 1722.1-2021 7.2.3 and 7.2.13 layouts) and tally what READ_DESCRIPTOR sent.
Usage: audio_unit_check.py <peer-descs-2.jsonl>"""
import json, struct, sys, collections
AU = ["stream_in_ports", "stream_out_ports", "ext_in_ports", "ext_out_ports",
      "int_in_ports", "int_out_ports", "controls", "signal_selectors", "mixers",
      "matrices", "splitters", "combiners", "demultiplexers", "multiplexers",
      "transcoders", "control_blocks"]
tally = collections.Counter()
for line in open(sys.argv[1]):
    r = json.loads(line)
    if r.get("cmd") != "READ_DESCRIPTOR":
        if r.get("cmd"):
            tally[(r["cmd"], r.get("what", "")[:40], r.get("status"))] += 1
        continue
    what = r.get("what", "")
    t = what.split("-")[3] if what.count("-") >= 4 else "?"
    tally[("READ_DESCRIPTOR", t, r.get("status"))] += 1
    if r.get("status") != "SUCCESS" or not r.get("payload", "").strip("0123456789abcdef") == "":
        continue
    b = bytes.fromhex(r["payload"])[4:]
    dtype, didx = struct.unpack(">HH", b[:4])
    if dtype == 0x0002:
        v = struct.unpack(">32H", b[72:136])
        print(f"AUDIO_UNIT {didx}: " + ", ".join(f"{n}={v[2*k]}@{v[2*k+1]}" for k, n in enumerate(AU)))
    if dtype in (0x000E, 0x000F):
        ncl, bcl, nmp, bmp = struct.unpack(">4H", b[12:20])
        print(f"STREAM_PORT_{'INPUT' if dtype == 0x0E else 'OUTPUT'} {didx}: clusters {ncl}@{bcl}, static maps {nmp}@{bmp}")
for k, n in sorted(tally.items()):
    print(n, *k)
