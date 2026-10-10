#!/usr/bin/env python3
"""Lane B15 identity verdict (descriptor offsets per IEEE 1722.1-2021 7.2.9 and 7.2.32) (offline, read-only): lane B10's identity_entity_b10.py (the four ATDECC
facts from the live ENTITY descriptor, unchanged offsets, IEEE 1722.1-2021 7.2.1) plus the console facts the
B15 assignment names, the live descriptors against the QSPI AEM bytes the console dumps, the clock sources
of #629, the UART grader and ADP.

usage: identity_b15.py <identity_dir>
Checks:
  atdecc-*        entity_id 020000fffe000001, entity_name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0",
                  serial_number "AX7101-0001" (ENTITY 0 over AECP)
  console-id      milan_status ID=4d494c4e and VERSION=00020060
  console-aem-crc CRC32 of the 7,512-byte AEM image in QSPI = 5ba355eb
  live-vs-qspi    ENTITY 0 and CONFIGURATION 0 over AECP equal the QSPI AEM bytes (312 and 106 bytes)
  clock-sources   CLOCK_SOURCE 0 INTERNAL, 1 INPUT_STREAM on STREAM_INPUT 1, 2 INPUT_STREAM on STREAM_INPUT 0,
                  3 NO_SUCH_DESCRIPTOR, CLOCK_DOMAIN 0 lists 0, 1, 2 (recorded with GET_CLOCK_SOURCE)
  grader          BAREMETAL UART SMOKE: PASS (10/10)
  adp             the DUT is discovered with entity model 001bc5c1935893e1
"""
import json
import re
import struct
import sys
from pathlib import Path

d = Path(sys.argv[1])
out = []


def check(name, good, detail):
    out.append(dict(check=name, result="PASS" if good else "FAIL", detail=detail))


aecp = {}
for line in (d / "identity-aecp.jsonl").read_text().splitlines():
    if line.startswith("{"):
        r = json.loads(line)
        if r.get("cmd"):
            aecp[(r["cmd"], r.get("req"))] = r


def s(b):
    return b.split(b"\0", 1)[0].decode("utf-8", "replace")


EXPECT = dict(entity_id="020000fffe000001", entity_name="Milan FPGA 1x1 TDM8", firmware_version="2.96.0",
              serial_number="AX7101-0001")
ent_r = aecp.get(("READ_DESCRIPTOR", "0000000000000000"))
ent = bytes.fromhex(ent_r["payload"])[4:] if ent_r and ent_r["status"] == "SUCCESS" else None
if ent is None:
    check("atdecc-entity", False, "no ENTITY 0 read")
else:
    got = dict(entity_id=ent[4:12].hex(), entity_name=s(ent[48:112]), firmware_version=s(ent[116:180]),
               serial_number=s(ent[244:308]))
    for k, v in EXPECT.items():
        check(f"atdecc-{k}", got[k] == v, dict(read=got[k], expected=v))

txt = (d / "console-identity.txt").read_text(encoding="ascii", errors="replace").replace("\r", "")
m = re.search(r"ID=([0-9a-fA-F]{8}) VERSION=([0-9a-fA-F]{8})", txt)
check("console-id", bool(m) and m.group(1).lower() == "4d494c4e" and m.group(2).lower() == "00020060",
      dict(read=m.groups() if m else None, expected=("4d494c4e", "00020060")))
m = re.search(r"cmd='crc 0x01400000 7512'.*?CRC32: ([0-9a-fA-F]{8})", txt, re.S)
check("console-aem-crc", bool(m) and m.group(1).lower() == "5ba355eb", dict(read=m.group(1) if m else None, expected="5ba355eb"))


def dump(addr, n):
    sec = txt.split(f"cmd='mem_read {addr} {n}'", 1)
    if len(sec) < 2:
        return None
    body = sec[1].split("###", 1)[0]
    b = bytearray()
    for ln in body.splitlines():
        mm = re.match(r"0x[0-9a-f]{8}\s+((?:[0-9a-f]{2} ){1,16})", ln)
        if mm:
            b += bytes.fromhex(mm.group(1).replace(" ", ""))
    return bytes(b[:n])


for name, req, addr, n in (("ENTITY 0", "0000000000000000", "0x01400110", 312),
                           ("CONFIGURATION 0", "0000000000010000", "0x01400248", 106)):
    q = dump(addr, n)
    r = aecp.get(("READ_DESCRIPTOR", req))
    live = bytes.fromhex(r["payload"])[4:] if r and r["status"] == "SUCCESS" else None
    diff = None if (q is None or live is None) else [i for i in range(min(len(q), len(live))) if q[i] != live[i]]
    check(f"live-vs-qspi-{name}", q is not None and live is not None and len(q) == len(live) == n and not diff,
          dict(qspi_bytes=None if q is None else len(q), live_bytes=None if live is None else len(live), differing_offsets=diff))

srcs = {}
for i in range(4):
    r = aecp.get(("READ_DESCRIPTOR", f"00000000000a{i:04x}"))
    if r and r["status"] == "SUCCESS":
        b = bytes.fromhex(r["payload"])[4:]
        typ, dt, di = struct.unpack(">H", b[72:74])[0], struct.unpack(">H", b[82:84])[0], struct.unpack(">H", b[84:86])[0]
        srcs[i] = dict(name=s(b[4:68]), type=typ, location_type=dt, location_index=di)
    else:
        srcs[i] = r["status"] if r else None
cd = aecp.get(("READ_DESCRIPTOR", "0000000000240000"))
cdl = None
if cd and cd["status"] == "SUCCESS":
    b = bytes.fromhex(cd["payload"])[4:]
    off, n = struct.unpack(">HH", b[72:76])
    cdl = [struct.unpack(">H", b[off + 2 * k:off + 2 * k + 2])[0] for k in range(n)]
gc = aecp.get(("GET_CLOCK_SOURCE", "00240000"))
cur = int(gc["payload"][8:12], 16) if gc and gc["status"] == "SUCCESS" else None
good = (isinstance(srcs.get(0), dict) and srcs[0]["type"] == 0 and isinstance(srcs.get(1), dict) and srcs[1]["type"] == 2
        and srcs[1]["location_type"] == 5 and srcs[1]["location_index"] == 1 and isinstance(srcs.get(2), dict)
        and srcs[2]["type"] == 2 and srcs[2]["location_type"] == 5 and srcs[2]["location_index"] == 0
        and srcs.get(3) == "NO_SUCH_DESCRIPTOR" and cdl == [0, 1, 2])
check("clock-sources", good, dict(sources=srcs, clock_domain_list=cdl, get_clock_source=cur))
g = (d / "grader-identity.txt").read_text(errors="replace")
check("grader", "BAREMETAL UART SMOKE: PASS (10/10)" in g, "BAREMETAL UART SMOKE line")
model = None
for line in (d / "adp-discover.jsonl").read_text().splitlines():
    if line.startswith("{"):
        r = json.loads(line)
        if r.get("type") == "adp" and r.get("entity_id") == "020000fffe000001":
            model = r.get("model_id")
check("adp", model == "001bc5c1935893e1", dict(model_id=model))
ok = all(o["result"] == "PASS" for o in out)
txt_out = "\n".join(json.dumps(o) for o in out) + f"\nIDENTITY GATE: {'PASS' if ok else 'FAIL'}\n"
(d / "identity-verdict.txt").write_text(txt_out)
print(txt_out, end="")
sys.exit(0 if ok else 1)
