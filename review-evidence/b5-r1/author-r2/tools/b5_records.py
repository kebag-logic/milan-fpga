#!/usr/bin/env python3
"""Round-2 record checks for lane B5 from the round-1 packet alone (no bench access).

usage: b5_records.py <a472_packet_dir> <repo_dir>

1. Controller tool revision: the b5_ctl.py hashes the packet recorded, every controller
   output stream's start time (the controller's clock), and whether each descriptor
   survey carries the audio-unit walk.
2. Direction B: the reference peer's configuration counts, AUDIO_UNIT 0's port and
   routing-element counts, its stream ports' clusters and maps, and the walk's reads,
   decoded from restore/peer-descs-2.jsonl.
3. The survey walk's descriptor type codes (b5_ctl.py, as published) against the
   numbering the repository encodes (avdecc/aem_descriptors.py, IEEE 1722.1 Table 7.1).
"""
import datetime as dt
import json
import re
import struct
import sys
from pathlib import Path

P, REPO = Path(sys.argv[1]), Path(sys.argv[2])
out = []
p = out.append


def utc(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%H:%M:%S.%f")[:-3] + "Z"


def jl(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if line.startswith("{"):
            r = json.loads(line)
            rows.append(r.get("line", r))
    return rows


p("== 1. controller tool revision")
for tag in ("start", "end"):
    txt = (P / f"restore/controller-{tag}.txt").read_text()
    h = re.search(r"^([0-9a-f]{64})  b5_ctl\.py$", txt, re.M).group(1)
    ls = re.search(r"\s(\d+) (\w{3} +\d+ \d\d:\d\d) b5_ctl\.py$", txt, re.M)
    lock = (P / f"restore/lock-{tag}.txt").read_text().split()[1]
    p(f"{tag} snapshot (lock {lock}): staged by scp, then hashed: b5_ctl.py {h} {ls.group(1)} B, file time {ls.group(2)}")
p("the run tool starts the staged agent and records no hash of it (tools/run_a.py, class Agent)")
streams = [("start census", "restore/census-start.jsonl"), ("start survey", "restore/peer-descs.jsonl"),
           ("survey with the audio unit's children", "restore/peer-descs-2.jsonl"),
           ("agent dry run", "runs/agent-dryrun.txt"), ("run abort-agent-start", "runs/abort-agent-start/ctl.jsonl"),
           ("run a-try1", "runs/a-try1/ctl.jsonl"), ("run diag1", "runs/diag1/ctl.jsonl"),
           ("run a-long", "runs/a-long/ctl.jsonl"), ("run cap-test1", "runs/cap-test1/ctl.jsonl"),
           ("end census", "restore/census-end.jsonl")]
for name, f in streams:
    rows = jl(P / f)
    st = [r for r in rows if r.get("type") == "start"][0]
    au = sum(1 for r in rows if r.get("type") == "audio-unit")
    stamped = sum(1 for r in rows if "t_tx" in r)
    p(f"{name:40s} mode {st['mode']:6s} start {utc(st['t'])} (controller clock); audio-unit records {au}; "
      f"stamped exchanges {stamped}")
s1 = jl(P / "restore/peer-descs.jsonl")
au1 = [r for r in s1 if r.get("what") == "desc-peer-1-0x0002-0"]
p(f"start survey: AUDIO_UNIT 0 read {au1[0]['status'] if au1 else 'absent'}, and no audio-unit walk followed it")
p("so the controller copy changed between the start snapshot and the second survey; that staging has no recorded hash")

p("")
p("== 2. Direction B: the reference peer's AEM (restore/peer-descs-2.jsonl)")
rows = jl(P / "restore/peer-descs-2.jsonl")
names = {0x0002: "AUDIO_UNIT", 0x0005: "STREAM_INPUT", 0x0006: "STREAM_OUTPUT", 0x0009: "AVB_INTERFACE",
         0x000A: "CLOCK_SOURCE", 0x000B: "MEMORY_OBJECT", 0x000C: "LOCALE", 0x001A: "CONTROL", 0x0024: "CLOCK_DOMAIN"}
cnt = [r for r in rows if r.get("type") == "counts"][0]
p(f"configuration {cnt['configuration']} descriptor counts: "
  + ", ".join(f"{names.get(int(k, 16), k)} {v}" for k, v in sorted(cnt["counts"].items())))
au = [r for r in rows if r.get("what") == "desc-peer-1-0x0002-0" and r["status"] == "SUCCESS"][-1]
b = bytes.fromhex(au["payload"])[4:]
fields = ["stream input ports", "stream output ports", "external input ports", "external output ports",
          "internal input ports", "internal output ports", "controls", "signal selectors", "mixers", "matrices",
          "splitters", "combiners", "demultiplexers", "multiplexers", "transcoders", "control blocks"]
v = struct.unpack(">32H", b[72:136])
p("AUDIO_UNIT 0: " + ", ".join(f"{f} {v[2 * i]} (base {v[2 * i + 1]})" for i, f in enumerate(fields)))
ctl = [r for r in rows if r.get("what") == "desc-peer-1-0x001a-0" and r["status"] == "SUCCESS"]
if ctl:
    cb = bytes.fromhex(ctl[0]["payload"])[4:]
    p(f"CONTROL 0 (configuration level): control_type {cb[82:90].hex()} (90e0f00000000001 is IDENTIFY)")
for t, name in ((0x000E, "STREAM_PORT_INPUT"), (0x000F, "STREAM_PORT_OUTPUT")):
    d = [r for r in rows if r.get("what") == f"desc-peer-1-{t:#06x}-0" and r["status"] == "SUCCESS"][0]
    pb = bytes.fromhex(d["payload"])[4:]
    ncl, bcl, nmp, bmp = struct.unpack(">4H", pb[12:20])
    m = [r for r in rows if r.get("what") == f"map-peer-{t:#06x}-0-0"][0]
    mb = bytes.fromhex(m["payload"])
    nmap = struct.unpack(">H", mb[8:10])[0]
    maps = [struct.unpack(">4H", mb[12 + 8 * i:20 + 8 * i]) for i in range(nmap)]
    offs = sorted(set(o for _, _, o, _ in maps))
    p(f"{name} 0: clusters {ncl} from index {bcl}; static maps {nmp}; dynamic map {m['status']}, {nmap} mappings, "
      f"cluster offsets {offs[0]} .. {offs[-1]} (all within the port's own {ncl} clusters: {offs[-1] < ncl})")
walk = [r for r in rows if re.match(r"desc-peer-1-0x00(1[0-4])-", r.get("what", ""))]
by = {}
for r in walk:
    k = r["what"].rsplit("-", 1)[0].split("-")[-1]
    by.setdefault(k, []).append((int(r["what"].rsplit("-", 1)[1]), r["status"]))
for k, xs in sorted(by.items()):
    idx = [i for i, _ in xs]
    p(f"walk reads of type {k}: indices {min(idx)} .. {max(idx)} ({len(xs)}), statuses {sorted(set(s for _, s in xs))}")

p("")
p("== 3. the walk's descriptor type codes")
src = (P / "tools/b5_ctl.py").read_text().splitlines()
repo = (REPO / "avdecc/aem_descriptors.py").read_text()
m = re.search(r"^AUDIO_CLUSTER, AUDIO_MAP, CONTROL, CLOCK_DOMAIN = (0x\w+), (0x\w+), (0x\w+), (0x\w+)$", repo, re.M)
line = repo[:m.start()].count("\n") + 1
AC, AM = int(m.group(1), 16), int(m.group(2), 16)
p(f"repository (avdecc/aem_descriptors.py:{line}): AUDIO_CLUSTER {AC:#06x}, AUDIO_MAP {AM:#06x}; "
  "IEEE 1722.1 Table 7.1 (the table that file cites): EXTERNAL_PORT_INPUT 0x0010, EXTERNAL_PORT_OUTPUT 0x0011, "
  "INTERNAL_PORT_INPUT 0x0012")
want = {"clusters": AC, "maps": AM, "external input ports": 0x0010, "external output ports": 0x0011}
for i, s in enumerate(src, 1):
    if "for t, n, base in ((0x000E" in s:
        codes = re.findall(r"\((0x\w+), (\w+), (\w+)\)", s)
        for c, n, _ in codes:
            role = {"nein": "external input ports", "neout": "external output ports"}.get(n)
            if role:
                c = int(c, 16)
                p(f"b5_ctl.py:{i} reads {role} as {c:#06x}; expected {want[role]:#06x}: {'OK' if c == want[role] else 'WRONG'}")
    mm = re.search(r'read_desc\(c, "peer", cur, (0x\w+), k\)', s)
    if mm:
        role = "clusters" if "bcl" in src[i - 2] else "maps"
        c = int(mm.group(1), 16)
        p(f"b5_ctl.py:{i} reads {role} as {c:#06x}; expected {want[role]:#06x}: {'OK' if c == want[role] else 'WRONG'}")
print("\n".join(out))
