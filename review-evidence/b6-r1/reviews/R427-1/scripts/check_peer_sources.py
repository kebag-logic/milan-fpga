#!/usr/bin/env python3
"""Is each clock source the runs set on the reference peer located on the input the case
claims? Reads the peer's descriptor survey (CLOCK_SOURCE location -> STREAM_INPUT ->
its current format) and each run's set-clock event. Prints no peer index.

usage: check_peer_sources.py <evidence author dir>
"""
import json, os, sys
root = sys.argv[1]
cs, si = {}, {}
for l in open(os.path.join(root, "restore/peer-descs.jsonl")):
    e = json.loads(l)
    if e.get("cmd") != "READ_DESCRIPTOR" or e.get("status") != "SUCCESS":
        continue
    p = e["payload"]
    if p.startswith("<"):
        continue  # a redacted descriptor
    dtype, didx = int(p[8:12], 16), int(p[12:16], 16)
    body = p[16 + 128:]  # after descriptor_type, descriptor_index and the 64-byte object_name
    if dtype == 0x000A:
        # localized_description(2) clock_source_flags(2) clock_source_type(2) identifier(8) location_type(2) location_index(2)
        ctype = int(body[8:12], 16)
        rest = body[12:]
        rest = rest[rest.index(">") + 1:] if rest.startswith("<") else rest[16:]
        cs[didx] = (ctype, int(rest[0:4], 16), int(rest[4:8], 16))
    elif dtype == 0x0005:
        # STREAM_INPUT: localized_description(2) clock_domain_index(2) stream_flags(2) current_format(8)
        si[didx] = body[12:28]
want = {"a1": "AAF (0205...)", "a2": "CRF (0410...)"}
ok = True
for case, label in want.items():
    for l in open(os.path.join(root, "runs", case, "events.jsonl")):
        e = json.loads(l)
        if e["kind"] == "set-clock" and e["tag"] == "case" and e["who"] == "peer":
            ctype, ltype, lidx = cs[e["src"]]
            fmt = si.get(lidx, "")
            kind = "AAF (0205...)" if fmt.startswith("0205") else "CRF (0410...)" if fmt.startswith("0410") else "?"
            good = ctype == 2 and ltype == 0x0005 and kind == label
            ok &= good
            print(f"{case}: peer source set is INPUT_STREAM: {ctype == 2}; located on a STREAM_INPUT: {ltype == 0x0005}; "
                  f"that input's format is {kind}; case claims {label}: {'OK' if good else 'MISMATCH'}")
src0 = cs.get(0)
print("peer as-found source is INTERNAL:", src0 is not None and src0[0] == 0)
print("RESULT", "PASS" if ok else "FAIL")
