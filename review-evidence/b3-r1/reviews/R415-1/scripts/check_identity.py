#!/usr/bin/env python3
"""Re-derive the identity gate's descriptor equality from the public packet.

usage: check_identity.py <packet-author-dir>
Compares the AECP READ_DESCRIPTOR payloads (ENTITY 0, CONFIGURATION 0) with
the console hex dumps of the QSPI AEM bytes at 0x01400110 (312 B) and
0x01400248 (106 B), and prints VERSION, AEM CRC and entity id as read.
"""
import json, re, sys, os
d = sys.argv[1]
con = open(os.path.join(d, "identity/console-identity.txt")).read()
def dump(addr, n):
    blk = con.split(f"cmd='mem_read {addr} {n}'")[1].split("litex")[0]
    out = bytearray()
    for line in blk.splitlines():
        m = re.match(r"0x[0-9a-f]{8}\s+((?:[0-9a-f]{2} ?)+)", line.strip())
        if m:
            out += bytes.fromhex(m.group(1).replace(" ", ""))
    return bytes(out[:n])
ent, cfg = dump("0x01400110", 312), dump("0x01400248", 106)
pl = [json.loads(l) for l in open(os.path.join(d, "identity/identity-aecp.jsonl")) if '"READ_DESCRIPTOR"' in l]
res = {}
for rec in pl:
    p = bytes.fromhex(rec["payload"])
    desc = p[4:]  # configuration_index(2) + reserved(2), then the descriptor
    dtype = int.from_bytes(desc[0:2], "big")
    ref = ent if dtype == 0 else cfg if dtype == 1 else None
    res[dtype] = dict(status=rec["status"], bytes=len(desc), equal=(ref is not None and desc == ref))
print("ENTITY:", res.get(0))
print("CONFIGURATION:", res.get(1))
print("entity_id:", ent[4:12].hex(), "model_id:", ent[12:20].hex())
print("VERSION:", re.search(r"VERSION=(\w+)", con).group(1))
print("AEM CRC:", re.search(r"crc 0x01400000 7352\s+CRC32: (\w+)", con).group(1))
ok = res.get(0, {}).get("equal") and res.get(1, {}).get("equal") and ent[4:12].hex() == "020000fffe000001"
print("IDENTITY_DESCRIPTORS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
