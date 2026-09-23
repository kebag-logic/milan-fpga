#!/usr/bin/env python3
"""Reviewer-owned parser for the #117 console transcripts.

A transcript is a sequence of blocks headed
  ### <ISO-8601 UTC> cmd='<command>' elapsed=<s>s
Each block is one command. milan_status blocks carry KEY=VALUE tokens;
mem_read blocks carry one "Memory dump" line whose four octets are read
little-endian (the dump prints memory order; the CSR is a 32-bit LE word).
Yields dicts with t (epoch seconds, command send time), cmd, and either
fields (milan_status), addr/word (mem_read) or crc (crc).
"""
import datetime as dt
import re

HDR = re.compile(r"^### (\S+) cmd='([^']*)' elapsed=([0-9.]+)s")
KV = re.compile(r"([A-Z_0-9]+)=([0-9A-Za-z_]+)")
DUMP = re.compile(r"^0x([0-9a-f]{8})\s+((?:[0-9a-f]{2} ){4})")


def _t(iso):
    return dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def blocks(path):
    cur = None
    for line in open(path, errors="replace"):
        m = HDR.match(line)
        if m:
            if cur:
                yield cur
            cur = dict(t=_t(m.group(1)), iso=m.group(1), cmd=m.group(2), el=float(m.group(3)), body=[])
            continue
        if cur is not None:
            cur["body"].append(line.rstrip("\n"))
    if cur:
        yield cur


def parse(path):
    out = []
    for b in blocks(path):
        r = dict(t=b["t"], iso=b["iso"], cmd=b["cmd"], el=b["el"])
        if b["cmd"] == "milan_status":
            f = {}
            for ln in b["body"]:
                for k, v in KV.findall(ln):
                    f[k] = v
            r["fields"] = f
            r["ok"] = "CLKV_STAT" in f and "GPTP_GM" in f
        elif b["cmd"].startswith("mem_read"):
            r["addr"] = int(b["cmd"].split()[1], 16)
            r["word"] = None
            for ln in b["body"]:
                m = DUMP.match(ln)
                if m:
                    octs = bytes.fromhex(m.group(2).replace(" ", ""))
                    r["word"] = int.from_bytes(octs, "little")
        elif b["cmd"].startswith("crc"):
            r["crc"] = None
            for ln in b["body"]:
                if ln.startswith("CRC32:"):
                    r["crc"] = ln.split()[1]
        out.append(r)
    return out
