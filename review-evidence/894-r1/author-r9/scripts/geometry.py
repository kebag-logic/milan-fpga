#!/usr/bin/env python3
"""Print each configuration's map-key geometry from its generated descriptors."""
import struct, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root/'sw/builder'))
import endstation_builder as builder
def descs(path):
    cfg = builder.load_config(str(path))
    blob = builder._entity_model_image(cfg, builder.emit_aem_overlay(cfg))['aem_desc.bin']
    count = struct.unpack_from('>H', blob, 8)[0]; directory = struct.unpack_from('>I', blob, 12)[0]
    d = {}
    for n in range(count):
        config, typ, number, length, offset, _, stride = struct.unpack_from('>HHHHIHH', blob, directory+16*n)
        for k in range(number):
            value = blob[offset+stride*k:offset+stride*k+length]
            d[config, typ, struct.unpack_from('>H', value, 2)[0]] = value
    return d
for path in [Path(p) for p in sys.argv[2:]] or sorted((root/'configs').glob('endstation_*.yaml')):
    d = descs(path)
    out = []
    for typ in (5, 6):
        for (c, t, i), v in sorted(d.items()):
            if t != typ: continue
            fmt = struct.unpack_from('>Q', v, 74)[0]
            start, n = struct.unpack_from('>HH', v, 82)
            lst = [struct.unpack_from('>Q', v, start + 8*k)[0] for k in range(n)]
            ch = lambda f: (f >> 22) & 1023 if f >> 56 == 2 else 0
            out.append(f"{'SI' if typ==5 else 'SO'}{i}:cur{ch(fmt)}/max{max(map(ch, lst), default=0)}")
    for typ in (14, 15):
        for (c, t, i), v in sorted(d.items()):
            if t != typ: continue
            nc, base, nmaps = struct.unpack_from('>HHH', v, 12)
            cc = [struct.unpack_from('>H', d[c, 20, base+k], 84)[0] for k in range(nc)]
            out.append(f"{'PI' if typ==14 else 'PO'}{i}:{'dyn' if nmaps==0 else 'static'} clusters {nc} ch {sorted(set(cc))}")
    print(path.name, ' '.join(out))
