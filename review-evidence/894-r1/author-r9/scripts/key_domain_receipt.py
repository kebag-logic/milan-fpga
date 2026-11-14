#!/usr/bin/env python3
"""Every accepted map key of every dynamic port, per configuration, at its slot in the build's key domain: the
generated constants (aecp_entity.py, AECP_ENTITY_KEY_*), the table aecp_maps.c sizes from them (MAP_FIRSTS x
MAP_CHANNELS, at least 256 slots), each port's accepted keys (an output port: every STREAM_OUTPUT's channels of its
advertised formats; an input port: each of its clusters' channels), and whether every key's slot is in the table and
its own. usage: python3 -I key_domain_receipt.py TREE CONFIG..."""
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/aecp'))
sys.path.insert(0, str(root / 'sw/builder'))
import aecp_shape  # noqa: E402
import endstation_builder as builder  # noqa: E402

for path in map(Path, sys.argv[2:]):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, '-B', str(root / 'sw/firmware/ctrl/aecp/aecp_entity.py'), str(path), '-o',
                        f'{tmp}/h'], check=True)
        k = {m[0]: int(m[1]) for m in re.findall(r'#define AECP_ENTITY_KEY_(\w+) (\d+)u', Path(f'{tmp}/h').read_text())}
    firsts, channels = max(k['STREAMS'], k['CLUSTERS']), max(k['STREAM_CHANNELS'], k['CLUSTER_CHANNELS'])
    slots = max(firsts * channels, 256)
    cfg = builder.load_config(str(path))
    found = aecp_shape.descriptors(builder._entity_model_image(cfg, builder.emit_aem_overlay(cfg))['aem_desc.bin'])
    width = lambda v, at: (struct.unpack_from('>Q', v, at)[0] >> 22) & 1023 if struct.unpack_from('>Q', v, at)[0] >> 56 == 2 else 0
    print(f'{path.stem}: constants {k}; domain {firsts} x {channels} = {firsts * channels}, table {slots} slots')
    for (c, typ, index), port in sorted(found.items()):
        if typ not in (14, 15) or struct.unpack_from('>H', port, 16)[0]:
            continue
        number, base = struct.unpack_from('>HH', port, 12)
        keys = []
        if typ == 15 and number:
            for (cc, t, s), v in found.items():
                if cc == c and t == 6:
                    start, n = struct.unpack_from('>HH', v, 82)
                    keys += [(s, ch) for ch in range(max([width(v, 74)] + [width(v, start + 8 * j) for j in range(n)]))]
        if typ == 14:
            for cl in range(number):
                keys += [(cl, ch) for ch in range(struct.unpack_from('>H', found[c, 20, base + cl], 84)[0])]
        at = [f * channels + ch for f, ch in keys if f < firsts and ch < channels]
        own = len(at) == len(keys) and len(set(at)) == len(at) and all(s < slots for s in at)
        print(f'  {"input" if typ == 14 else "output"} port {index}: {len(keys)} accepted keys, '
              f'slots {min(at, default=0)}..{max(at, default=0)}, each in the table and its own: {own}')
