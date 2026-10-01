#!/usr/bin/env python3
"""Independent decode of the peer's second descriptor survey (restore/peer-descs-2.jsonl).

usage: peer_walk.py <a472_packet_dir> <repo>
Tallies every exchange, decodes AUDIO_UNIT and STREAM_PORT descriptors per
IEEE 1722.1 7.2.3 / 7.2.13 field order, and checks the type codes the page cites
against the repository's avdecc/aem_descriptors.py.
"""
import collections, json, re, struct, sys, pathlib

pk, repo = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
recs = [json.loads(l) for l in open(pk / "restore/peer-descs-2.jsonl")]
ex = [r for r in recs if "cmd" in r]
print("exchanges", len(ex))
tally = collections.Counter()
reads = collections.defaultdict(list)
for r in ex:
    m = re.match(r"desc-peer-\d+-(0x[0-9a-f]{4})-(\d+)", r.get("what", ""))
    typ = m.group(1) if m else r.get("what")
    tally[(r["cmd"], typ, r["status"])] += 1
    if m:
        reads[typ].append((int(m.group(2)), r["status"], r.get("payload", "")))
for k in sorted(tally):
    print("  ", *k, tally[k])

def u16(b, o):
    return struct.unpack_from(">H", b, o)[0]

for typ in ("0x0002",):
    for idx, st, p in reads[typ]:
        if st != "SUCCESS" or p.startswith("<"):
            continue
        b = bytes.fromhex(p)[4:]
        assert u16(b, 0) == 2
        f = [u16(b, o) for o in range(70, 70 + 2 * 38, 2)]
        names = ["clock_domain_index", "n_stream_in_ports", "base_stream_in_port", "n_stream_out_ports",
                 "base_stream_out_port", "n_ext_in_ports", "base_ext_in", "n_ext_out_ports", "base_ext_out",
                 "n_int_in_ports", "base_int_in", "n_int_out_ports", "base_int_out", "n_controls", "base_control",
                 "n_signal_selectors", "base_ss", "n_mixers", "base_mixer", "n_matrices", "base_matrix",
                 "n_splitters", "base_splitter", "n_combiners", "base_combiner", "n_demux", "base_demux",
                 "n_mux", "base_mux", "n_transcoders", "base_transcoder", "n_control_blocks", "base_cb"]
        print(f"AUDIO_UNIT index {idx}:", {n: v for n, v in zip(names, f)})
for typ, name in (("0x000e", "STREAM_PORT_INPUT"), ("0x000f", "STREAM_PORT_OUTPUT")):
    for idx, st, p in reads[typ]:
        b = bytes.fromhex(p)[4:]
        # 7.2.13: type, index, clock_domain_index, port_flags, number_of_controls, base_control,
        # number_of_clusters, base_cluster, number_of_maps, base_map
        t, i, cd, fl, nc, bc, ncl, bcl, nm, bm = struct.unpack_from(">10H", b, 0)
        print(f"{name} {i}: clusters {ncl} from {bcl}; static maps {nm} from {bm}; controls {nc}")
idx10 = sorted(i for i, s, _ in reads["0x0010"])
print("type 0x0010 reads:", len(idx10), "indices", idx10[0], "..", idx10[-1],
      "statuses", collections.Counter(s for _, s, _ in reads["0x0010"]))
src = (repo / "avdecc/aem_descriptors.py").read_text()
for n in ("EXTERNAL_PORT_INPUT", "EXTERNAL_PORT_OUTPUT", "INTERNAL_PORT_INPUT", "AUDIO_CLUSTER", "AUDIO_MAP"):
    m = re.search(rf"\b{n}\b\s*[:=]\s*(0x[0-9A-Fa-f]+|\d+)", src)
    print("repo", n, m.group(1) if m else "NOT FOUND")
