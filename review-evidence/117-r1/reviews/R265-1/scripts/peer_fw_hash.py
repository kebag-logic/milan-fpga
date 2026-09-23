#!/usr/bin/env python3
"""SHA-256 of the reference peer's 64-octet ENTITY firmware_version field.

Usage: peer_fw_hash.py <jsonl> [...]
READ_DESCRIPTOR(ENTITY) response payload = configuration_index(2) +
reserved(2) + ENTITY descriptor (IEEE 1722.1 Clause 7.2.1); firmware_version
is descriptor octets 116..179. Prints the hash and the non-NUL length only.
"""
import hashlib, json, sys
for path in sys.argv[1:]:
    for line in open(path):
        j = json.loads(line)
        p = j.get("payload")
        if j.get("cmd") != "READ_DESCRIPTOR" or not p or j.get("req", "")[:8] not in ("00000000",):
            continue
        b = bytes.fromhex(p)
        if b[4:6] != b"\x00\x00" or len(b) < 4 + 312:
            continue
        fw = b[4 + 116:4 + 180]
        print(path, j.get("target"), "fw_field_len", len(fw), "nonNUL", len(fw.rstrip(b"\0")),
              "sha256", hashlib.sha256(fw).hexdigest(), "reserved", b[2:4].hex())
