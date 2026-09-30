#!/usr/bin/env python3
"""Independent identity re-derivation from the published packet: the console
VERSION / CRC lines, and the AECP READ_DESCRIPTOR payloads (minus the 4-byte
configuration_index/reserved prefix) against the console's QSPI AEM dumps.
usage: check_identity.py <console-identity.txt> <identity-aecp.jsonl>"""
import json, re, sys
txt = re.sub(r"\x1b\[[0-9;]*m", "", open(sys.argv[1], errors="replace").read()).replace("\r", "")
print("VERSION", re.findall(r"VERSION=([0-9a-f]{8})", txt))
for m in re.finditer(r"cmd='crc (0x[0-9a-f]+) (\d+)'.*?CRC32: ([0-9a-f]{8})", txt, re.S):
    print("crc", m.group(1), m.group(2), m.group(3))
def dump(addr):
    blk = txt.split("cmd='mem_read %s " % addr, 1)[1].split("###", 1)[0]
    n = int(blk.split("'", 1)[0])
    out = bytearray()
    for line in blk.splitlines():
        m = re.match(r"^0x([0-9a-f]{8})\s+((?:[0-9a-f]{2} ){1,16})", line)
        if m:
            out += bytes.fromhex(m.group(2).replace(" ", ""))
    return bytes(out[:n])
q = {0: dump("0x01400110"), 1: dump("0x01400248")}
for l in open(sys.argv[2]):
    r = json.loads(l)
    if r.get("cmd") != "READ_DESCRIPTOR":
        continue
    d = int(r["req"][8:12], 16)
    body = bytes.fromhex(r["payload"])[4:]
    print({0: "ENTITY", 1: "CONFIGURATION"}[d], r["status"], len(body), "qspi", len(q[d]), "equal", body == q[d],
          "entity_id" if d == 0 else "", body[4:12].hex() if d == 0 else "",
          "fw" if d == 0 else "", body[0x74:0x84].split(b"\0")[0].decode() if d == 0 else "")
