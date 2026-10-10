#!/usr/bin/env python3
"""Parse the published peer survey (restore/peer-descs.jsonl): CONFIGURATION counts, AUDIO_UNIT 0 port and
control counts, STREAM_PORT_OUTPUT 0 base cluster, and the stream-port audio maps (IEEE 1722.1-2021 7.2).
usage: parse_peer_survey.py <peer-descs.jsonl>"""
import json, struct, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
def body(r):
    p = r.get('payload', '')
    if not p or p.startswith('<'):
        return None
    try:
        return bytes.fromhex(p)
    except ValueError:
        return None
seen = set()
for r in rows:
    w = r.get('what', ''); b = body(r)
    if b is None or w in seen:
        continue
    seen.add(w)
    if r.get('cmd') == 'READ_DESCRIPTOR' and r.get('status') == 'SUCCESS':
        cfg, _, dt, di = struct.unpack('>HHHH', b[:8]); d = b[4:]
        if dt == 0x0001:
            cnt, off = struct.unpack('>HH', d[70:74])
            pairs = [struct.unpack('>HH', d[off + 4 * i:off + 4 * i + 4]) for i in range(cnt)]
            print(w, 'CONFIGURATION counts', {hex(t): n for t, n in pairs})
        elif dt == 0x0002:
            f = struct.unpack('>' + 'H' * 32, d[68:68 + 64])
            names = ['localized', 'clock_domain', 'n_si_ports', 'base_si', 'n_so_ports', 'base_so', 'n_ext_in', 'base_ext_in',
                     'n_ext_out', 'base_ext_out', 'n_int_in', 'base_int_in', 'n_int_out', 'base_int_out', 'n_controls', 'base_control',
                     'n_sig_sel', 'base_sig_sel', 'n_mixers', 'base_mixer', 'n_matrices', 'base_matrix', 'n_splitters', 'base_split',
                     'n_combiners', 'base_comb', 'n_demux', 'base_demux', 'n_mux', 'base_mux', 'n_transcoders', 'base_trans']
            print(w, 'AUDIO_UNIT', dict(zip(names, f)))
        elif dt in (0x000E, 0x000F):
            f = struct.unpack('>HHHHHHHH', d[4:20])
            print(w, 'STREAM_PORT', hex(dt), di, dict(zip(['clock_domain', 'port_flags', 'n_controls', 'base_control', 'n_clusters', 'base_cluster', 'n_maps', 'base_map'], f)))
    elif r.get('cmd') == 'GET_AUDIO_MAP' and r.get('status') == 'SUCCESS':
        dt, di, mi, nm, n, _ = struct.unpack('>HHHHHH', b[:12])
        maps = [struct.unpack('>HHHH', b[12 + 8 * i:20 + 8 * i]) for i in range(n)]
        print(w, 'AUDIO_MAP', hex(dt), di, 'mappings (stream_index, stream_channel, cluster_offset, cluster_channel):', maps)
ns = [r['what'] for r in rows if r.get('status') == 'NO_SUCH_DESCRIPTOR']
print('NO_SUCH_DESCRIPTOR', len(ns), 'types', sorted(set(x.split('-')[3] for x in ns)), 'cfg', sorted(set(x.split('-')[2] for x in ns)))
