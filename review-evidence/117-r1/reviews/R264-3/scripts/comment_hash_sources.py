#!/usr/bin/env python3
"""Which public issue/PR comments carry each page hash in full (or a prefix).

Usage: comment_hash_sources.py COMMENTS.json [...]
"""
import json, re, sys

full = {
    ".bit": "f0725eef7a361bd7dc6d692c369868f25e5d4f49f6b7267562a0b5f949ada33d",
    "payload": "aaece32fc6c84f790273878350f674c142407a6b9ff2097862870784921da5fb",
    "aem_desc.bin": "9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404",
    "bios.bin": "69322600bc9dc40a698ed30d125d29d2723f51cc1b26c0f1c3abc96acb39deab",
    "flashboot_layout.json": "71e798fc401ed3fbaac4cd43a299f23498beafa466aaa17d6773590a62fa93e2",
    "csr.csv": "4db0e6da9c9c910a5ee00e56c25908c190c380799e44c846bcfb4ffc7dc045a7",
    "firmware field digest": "33f0e7f9e86fe4829a2de6f6d04d1edf1463b7d6653c2865ad985f183b0ddfbc",
}
prefixes = {"la_avdecc_cxx": "95d64fd5", "la_avdecc_controller_cxx": "8ef4b008",
            "counters probe": "ad579e18", "probe source": "0e9faf30"}
cs = [c for f in sys.argv[1:] for c in json.load(open(f))]
for name, h in full.items():
    ids = [str(c["id"]) for c in cs if h in c["body"]]
    pre = sorted({f"{c['id']}:{len(m)}hex" for c in cs for m in re.findall(h[:8] + r"[0-9a-f]*", c["body"]) if m != h})
    print(f"FULL {name} {h[:16]}... full_in={','.join(ids) or 'none'} shorter_forms={','.join(pre) or 'none'}")
for name, p in prefixes.items():
    ids = sorted({str(c["id"]) for c in cs if re.search(p + r"[0-9a-f]{56}", c["body"])})
    print(f"PREFIX {name} {p} full_value_in={','.join(ids) or 'none'}")
