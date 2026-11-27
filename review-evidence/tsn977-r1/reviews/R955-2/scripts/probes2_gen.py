#!/usr/bin/env python3
"""Second probe set: compilable forms of four first-set probes and whole-field drops. Usage: probes2_gen.py ACMP_C OUT"""
import json, sys
src = open(sys.argv[1]).read()
P = []
def add(n, o, w): P.append({"name": n, "old": o, "new": w})
add("r-rec-drop-p0", "(uint32_t)(p[0] ^ flags) | p[1]", "(uint32_t)(flags & 0u) | p[1]")
add("r-view-drop-stream", "(stream_id ^ y->stream.stream_id) | (dest_mac", "(stream_id & 0u) | (dest_mac")
add("r-view-drop-dest", "| (dest_mac ^ y->stream.dest_mac) |", "| (dest_mac & 0u) |")
add("r-view-drop-vlan", "(uint64_t)(vlan_id ^ y->stream.vlan_id) |", "(uint64_t)(vlan_id & 0u) |")
add("r-rec-drop-unique", "uint16_t unique = b ? s->binding.talker_unique_id : 0u;",
    "uint16_t unique = b ? s->binding.talker_unique_id : 0u;\n\tunique = (uint16_t)((p[2] << 8) | p[3]);")
add("r-rec-drop-talker", "\tuint32_t th = (uint32_t)(talker >> 32);\n\tuint32_t tl = (uint32_t)talker;",
    "\t(void)talker;\n\tuint32_t th = ((uint32_t)p[4] << 24) | ((uint32_t)p[5] << 16) | ((uint32_t)p[6] << 8) | p[7];\n"
    "\tuint32_t tl = ((uint32_t)p[8] << 24) | ((uint32_t)p[9] << 16) | ((uint32_t)p[10] << 8) | p[11];")
add("r-rec-drop-controller", "\tuint32_t ch = (uint32_t)(controller >> 32);\n\tuint32_t cl = (uint32_t)controller;",
    "\t(void)controller;\n\tuint32_t ch = ((uint32_t)p[12] << 24) | ((uint32_t)p[13] << 16) | ((uint32_t)p[14] << 8) | p[15];\n"
    "\tuint32_t cl = ((uint32_t)p[16] << 24) | ((uint32_t)p[17] << 16) | ((uint32_t)p[18] << 8) | p[19];")
add("r-rec-unique-low-byte-only", "(uint32_t)(p[2] ^ (unique >> 8)) |", "(uint32_t)(p[2] & 0u) |")
bad = [p["name"] for p in P if src.count(p["old"]) != 1]
if bad: sys.exit("bad anchors: " + ", ".join(bad))
json.dump(P, open(sys.argv[2], "w"), indent=1); print(len(P), "probes")
