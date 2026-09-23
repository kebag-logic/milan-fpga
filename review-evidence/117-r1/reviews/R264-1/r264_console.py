#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer parser for the issue 117 console transcripts.

A transcript is a sequence of blocks headed
  ### <ISO-8601 UTC send time> cmd='<command>' elapsed=<s>s
followed by the echoed command and the BIOS/firmware output. This parser
returns one record per block: the send time (epoch seconds, build-box clock),
the command, and the decoded fields (milan_status key=value pairs, or the
little-endian 32-bit word of a 4-byte mem_read).

Usage: r264_console.py summary <transcript> ...
"""
import datetime
import re
import sys

HDR = re.compile(r"^### (\S+) cmd='([^']*)' elapsed=([0-9.]+)s")
KV = re.compile(r"([A-Z_0-9]+)=([0-9A-Za-z_]+)")
MEM = re.compile(r"^0x([0-9a-f]{8})\s+((?:[0-9a-f]{2} ){4})")


def parse(path):
    blocks = []
    cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        m = HDR.match(line)
        if m:
            t = datetime.datetime.fromisoformat(m.group(1).replace("Z", "+00:00")).timestamp()
            cur = dict(t=t, cmd=m.group(2), elapsed=float(m.group(3)), kv={}, word=None, addr=None, text=[])
            blocks.append(cur)
            continue
        if cur is None:
            continue
        cur["text"].append(line.rstrip("\n"))
        if cur["cmd"] == "milan_status":
            for k, v in KV.findall(line):
                cur["kv"][k] = v
        mm = MEM.match(line)
        if mm and cur["cmd"].startswith("mem_read"):
            b = bytes.fromhex(mm.group(2).replace(" ", ""))
            cur["addr"] = int(mm.group(1), 16)
            cur["word"] = int.from_bytes(b, "little")
    return blocks


def summary(path):
    b = parse(path)
    st = [x for x in b if x["cmd"] == "milan_status" and "CLKV_STAT" in x["kv"]]
    words = {}
    for x in b:
        if x["addr"] is not None:
            words.setdefault(x["addr"], []).append(x["word"])
    out = [f"{path}: blocks {len(b)}, milan_status with CLKV {len(st)}"]
    for k in ("GPTP_GM", "GPTP_PARENT", "CLKV_STAT", "SYNC", "ASCAPABLE", "TU", "AS_PATH_COUNT", "AS_PATH_GEN", "GPTP_LAT"):
        vals = {}
        for x in st:
            vals[x["kv"].get(k)] = vals.get(x["kv"].get(k), 0) + 1
        out.append(f"  {k}: {vals}")
    pd = sorted(int(x["kv"]["PDELAY_NS"]) for x in st if "PDELAY_NS" in x["kv"])
    if pd:
        out.append(f"  PDELAY_NS min {pd[0]} max {pd[-1]} median {pd[len(pd)//2]}")
    for a in sorted(words):
        v = words[a]
        out.append(f"  0x{a:08x}: n={len(v)} distinct={sorted({f'{w:#x}' for w in v})[:8]} first={v[0]:#x} last={v[-1]:#x}")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "summary":
        raise SystemExit(__doc__)
    for p in sys.argv[2:]:
        print(summary(p))
