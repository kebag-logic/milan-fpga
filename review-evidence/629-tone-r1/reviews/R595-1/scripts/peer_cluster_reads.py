#!/usr/bin/env python3
"""R595-1: list the reference peer's AUDIO_CLUSTER / STREAM_PORT / AUDIO_UNIT reads in the published
start survey (restore/peer-descs.jsonl) with their status, configuration index and port fields.

usage: peer_cluster_reads.py <packet_author_dir>
"""
import json
import os
import struct
import sys

rows = [json.loads(line) for line in open(os.path.join(sys.argv[1], "restore", "peer-descs.jsonl"))]
for d in rows:
    if d.get("type") == "counts":
        print("CONFIGURATION", d["configuration"], "top-level descriptor counts", d["counts"])
    if d.get("type") == "audio-unit":
        print("AUDIO_UNIT 0 ports (count, base):", {k: v for k, v in d.items() if k.endswith("ports")})
    w = d.get("what", "")
    if d.get("cmd") == "GET_CONFIGURATION" and d.get("role") == "peer":
        print("GET_CONFIGURATION current", int(d["payload"][4:8], 16))
    if not w.startswith("desc-peer-1-0x00"):
        continue
    t = int(w.split("-")[3], 16)
    if t not in (0x0002, 0x000E, 0x000F, 0x0010):
        continue
    p = bytes.fromhex(d["payload"]) if "<" not in d["payload"] else b""
    cfg = struct.unpack(">H", p[0:2])[0] if p else None
    extra = ""
    if d["status"] == "SUCCESS" and t in (0x000E, 0x000F):
        ncl, bcl, nmp, bmp = struct.unpack(">4H", p[4 + 12:4 + 20])
        extra = f"clusters {ncl} from {bcl}, maps {nmp} from {bmp}"
    if d["status"] == "SUCCESS" and t == 0x0002:
        ports = struct.unpack(">12H", p[4 + 72:4 + 96])
        extra = f"stream in/out, external in/out, internal in/out (count, base): {ports}"
    print(f"{w:28s} {d['status']:20s} cfg={cfg} {extra}")
n_fail = sum(1 for d in rows if d.get("what", "").startswith("desc-peer-1-0x0010") and d["status"] != "SUCCESS")
n_all = sum(1 for d in rows if d.get("what", "").startswith("desc-peer-1-0x0010"))
print(f"AUDIO_CLUSTER reads: {n_all}, answered other than SUCCESS: {n_fail}")
