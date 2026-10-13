#!/usr/bin/env python3
"""Compare the DUT's live ENTITY 0 and CONFIGURATION 0 descriptors (AECP
READ_DESCRIPTOR, avdecc_ro.py output) with the AEM bytes the DUT console dumps
from its QSPI AEM region (mem_read 0x01400110 312 and 0x01400248 106).

usage: aecp_vs_qspi.py <identity-aecp.jsonl> <console-identity.txt>
"""
import json
import re
import sys


def dump(txt, addr):
    m = re.search(r"cmd='mem_read %s (\d+)'.*?Memory dump:\n(.*?)\n(?:\x1b|litex|###|$)" % addr, txt, re.S)
    n = int(m.group(1))
    b = bytearray()
    for line in m.group(2).splitlines():
        parts = line.split()
        if not parts or not parts[0].startswith("0x"):
            continue
        for h in parts[1:17]:
            if re.fullmatch(r"[0-9a-f]{2}", h):
                b.append(int(h, 16))
            else:
                break
    return bytes(b[:n])


txt = open(sys.argv[2], encoding="ascii", errors="replace").read().replace("\r", "")
qspi = {"ENTITY": dump(txt, "0x01400110"), "CONFIGURATION": dump(txt, "0x01400248")}
rows = [json.loads(l) for l in open(sys.argv[1]) if l.startswith("{")]
ok = True
n = 0
for r in rows:
    if r.get("type") != "aem":
        continue
    name = {0: "ENTITY", 1: "CONFIGURATION"}[int(r["req"][8:12], 16)]
    body = bytes.fromhex(r["payload"])[4:] if r.get("status") == "SUCCESS" else b""
    same = body == qspi[name] and len(body) > 0
    extra = f" entity_id={body[4:12].hex()} model_id={body[12:20].hex()}" if name == "ENTITY" and body else ""
    print(f"{name} 0: status={r.get('status')} bytes={len(body)} equal_to_qspi_aem_bytes={same}{extra}")
    ok = ok and same
    n += 1
print("AECP identity:", "PASS" if ok and n == 2 else "FAIL")
sys.exit(0 if ok and n == 2 else 1)
