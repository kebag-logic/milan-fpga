#!/usr/bin/env python3
"""Lane B7 identity verdict, offline: the DUT's console readback and live AECP descriptors
against the build of dev bbf704ec (its AEM image, BIOS and bitstream payload).

usage: identity_cmp.py <identity_dir> <aem_desc.bin> <expected.json>

expected.json holds the build's own values (VERSION, the CRC32 and size of the AEM image,
the BIOS ROM and the bitstream payload, the entity model ID) and the AEM image's descriptor
offsets (from the build's aem_desc.map). Checks:
  1. VERSION; the console CRCs of the AEM image, the BIOS ROM and the QSPI bitstream payload
     equal the build's;
  2. the QSPI AEM bytes the console dumps (ENTITY, CONFIGURATION, CLOCK_SOURCE 0-2,
     CLOCK_DOMAIN 0) equal the build's AEM image;
  3. every live descriptor read over AECP equals the build's AEM image byte for byte, or the
     differing bytes are listed by offset;
  4. the clock sources of #629: CLOCK_SOURCE 0 INTERNAL, 1 INPUT_STREAM on the CRF STREAM_INPUT,
     one INPUT_STREAM per AAF STREAM_INPUT, CLOCK_SOURCE 3 absent, and CLOCK_DOMAIN 0 listing
     exactly 0, 1, 2;
  5. the UART grader 10/10 and ADP showing the DUT with the build's entity model ID.
"""
import json
import re
import struct
import sys
from pathlib import Path

d = Path(sys.argv[1])
aem = Path(sys.argv[2]).read_bytes()
exp = json.loads(Path(sys.argv[3]).read_text())
txt = (d / "console-identity.txt").read_text(encoding="ascii", errors="replace").replace("\r", "")
out = []
ok = True


def check(name, good, detail):
    global ok
    ok = ok and bool(good)
    out.append(dict(check=name, result="PASS" if good else "FAIL", detail=detail))


def reply(cmd):
    m = re.search(r"cmd='%s'.*?\n(.*?)(?=\n###|\Z)" % re.escape(cmd), txt, re.S)
    return m.group(1) if m else ""


def dump(addr, n):
    body = reply(f"mem_read {addr} {n}")
    b = bytearray()
    for line in body.split("Memory dump:\n", 1)[-1].splitlines():
        parts = line.split()
        if not parts or not parts[0].startswith("0x"):
            continue
        for h in parts[1:17]:
            if re.fullmatch(r"[0-9a-f]{2}", h):
                b.append(int(h, 16))
            else:
                break
    return bytes(b[:n])


st = reply("milan_status")
m = re.search(r"VERSION=([0-9a-f]{8})", st)
check("version", m and m.group(1) == exp["version"], m.group(1) if m else None)
for key, cmd in (("aem", f"crc 0x01400000 {exp['aem_bytes']}"), ("rom", f"crc 0x00000000 {exp['rom_bytes']}"),
                 ("payload", f"crc 0x01000000 {exp['payload_bytes']}")):
    m = re.search(r"CRC32: ([0-9a-f]{8})", reply(cmd))
    check(f"crc-{key}", m and m.group(1) == exp[f"{key}_crc32"],
          dict(cmd=cmd, read=m.group(1) if m else None, build=exp[f"{key}_crc32"]))

offs = {k: tuple(v) for k, v in exp["offsets"].items()}  # name -> (offset, length)
for name, addr in (("ENTITY 0", "0x01400110"), ("CONFIGURATION 0", "0x01400248")):
    o, n = offs[name]
    check(f"qspi-{name}", dump(addr, n) == aem[o:o + n], dict(bytes=n))
o, n = offs["CLOCK_SOURCE 0"]
q = dump("0x01400620", 264)
check("qspi-CLOCK_SOURCE 0-2", q == aem[o:o + 264], dict(bytes=len(q)))
o, n = offs["CLOCK_DOMAIN 0"]
check("qspi-CLOCK_DOMAIN 0", dump("0x01401340", 82) == aem[o:o + n], dict(bytes=n))

DT = {0x0000: "ENTITY", 0x0001: "CONFIGURATION", 0x0005: "STREAM_INPUT", 0x0006: "STREAM_OUTPUT",
      0x000A: "CLOCK_SOURCE", 0x0024: "CLOCK_DOMAIN", 0x0009: "AVB_INTERFACE"}
live = {}
clk = None
for line in open(d / "identity-aecp.jsonl"):
    if not line.startswith("{"):
        continue
    r = json.loads(line)
    if r.get("type") != "aem":
        continue
    if r.get("cmd") == "GET_CLOCK_SOURCE":
        clk = int(r["payload"][8:12], 16) if r.get("status") == "SUCCESS" else r.get("status")
        continue
    t, i = int(r["req"][8:12], 16), int(r["req"][12:16], 16)
    name = f"{DT[t]} {i}"
    live[name] = (r.get("status"), bytes.fromhex(r["payload"])[4:] if r.get("status") == "SUCCESS" else b"")
for name, (status, body) in live.items():
    if name == "CLOCK_SOURCE 3":
        check("aecp-CLOCK_SOURCE 3 absent", status == "NO_SUCH_DESCRIPTOR", status)
        continue
    o, n = offs[name]
    ref = aem[o:o + n]
    diff = [k for k in range(max(len(ref), len(body))) if k >= len(ref) or k >= len(body) or ref[k] != body[k]]
    check(f"aecp-{name}", status == "SUCCESS" and not diff,
          dict(status=status, bytes=len(body), differing_offsets=diff[:32]))

CS_TYPE = {0: "INTERNAL", 1: "EXTERNAL", 2: "INPUT_STREAM"}
srcs = []
for k in range(3):
    b = live.get(f"CLOCK_SOURCE {k}", (None, b""))[1]
    if len(b) >= 86:
        flags, typ = struct.unpack(">HH", b[70:74])
        loc_t, loc_i = struct.unpack(">HH", b[82:86])
        srcs.append(dict(index=k, name=b[4:68].rstrip(b"\0").decode(errors="replace"), type=CS_TYPE.get(typ, typ),
                         flags=f"{flags:#06x}", location=f"{DT.get(loc_t, loc_t)} {loc_i}"))
fmt_kind = {}
for i in range(2):
    b = live.get(f"STREAM_INPUT {i}", (None, b""))[1]
    if len(b) >= 86:
        # STREAM_INPUT (IEEE 1722.1-2021 7.2.6): current_format at 74, formats_offset 82,
        # number_of_formats 84
        f_off, n_f = struct.unpack(">HH", b[82:86])
        fmts = [b[f_off + 8 * k:f_off + 8 * k + 8].hex() for k in range(n_f)]
        fmt_kind[i] = "CRF" if all(f.startswith("04") for f in fmts) else "AAF"
cd = live.get("CLOCK_DOMAIN 0", (None, b""))[1]
cd_list = []
if len(cd) >= 76:
    cur, c_off, c_n = struct.unpack(">HHH", cd[70:76])
    cd_list = [struct.unpack(">H", cd[c_off + 2 * k:c_off + 2 * k + 2])[0] for k in range(c_n)]
want = ([dict(type="INTERNAL")] + [dict(type="INPUT_STREAM", location=f"STREAM_INPUT {i}")
                                    for i, k in fmt_kind.items() if k == "CRF"]
        + [dict(type="INPUT_STREAM", location=f"STREAM_INPUT {i}") for i, k in fmt_kind.items() if k == "AAF"])
got = [dict(type=s["type"]) if s["type"] == "INTERNAL" else dict(type=s["type"], location=s["location"]) for s in srcs]
check("clock-sources-629", got == want and cd_list == [0, 1, 2],
      dict(stream_inputs=fmt_kind, clock_sources=srcs, clock_domain_list=cd_list, expected=want))
check("get-clock-source", clk == 0, clk)

g = (d / "grader-identity.txt").read_text(errors="replace")
check("uart-grader", "PASS (10/10)" in g, re.findall(r"SMOKE: .*", g))
adp = [json.loads(l) for l in open(d / "adp-discover.jsonl") if l.startswith("{")]
dut = [a for a in adp if a.get("type") == "adp" and a.get("entity_id") == "020000fffe000001"]
check("adp-dut-model", dut and all(a["model_id"] == exp["entity_model_id"] for a in dut),
      [a.get("model_id") for a in dut])
for r in out:
    print(json.dumps(r))
print("IDENTITY GATE:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
