#!/usr/bin/env python3
"""Enumerate map-key hash slots from generated dynamic-port descriptors."""
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root/'sw/builder'))
import endstation_builder as builder

def audit(path):
    cfg = builder.load_config(str(path))
    blob = builder._entity_model_image(cfg, builder.emit_aem_overlay(cfg))['aem_desc.bin']
    count = struct.unpack_from('>H', blob, 8)[0]
    directory = struct.unpack_from('>I', blob, 12)[0]
    descriptors = {}
    for n in range(count):
        config, typ, number, length, offset, _, stride = struct.unpack_from('>HHHHIHH', blob, directory+16*n)
        for k in range(number):
            value = blob[offset+stride*k:offset+stride*k+length]
            index = struct.unpack_from('>H', value, 2)[0]
            descriptors[config,typ,index] = value
    ports, aliases, first_alias = 0, 0, None
    for (config, typ, index), port in descriptors.items():
        if typ not in (14,15) or struct.unpack_from('>H', port, 16)[0]:
            continue
        keys = []
        if typ == 14:
            nc, base = struct.unpack_from('>HH', port, 12)
            for cluster in range(nc):
                channels = struct.unpack_from('>H', descriptors[config,20,base+cluster], 84)[0]
                keys += [(cluster,c) for c in range(channels)]
        else:
            for (conf, stream_type, stream), value in descriptors.items():
                if conf != config or stream_type != 6:
                    continue
                fmt = struct.unpack_from('>Q', value, 74)[0]
                if fmt >> 56 == 2:
                    keys += [(stream,c) for c in range((fmt >> 22)&1023)]
        slots = {}
        for key in keys:
            slot = (key[0]+9*key[1])&255
            if slot in slots:
                aliases += 1
                first_alias = first_alias or (typ,index,slots[slot],key,slot)
            slots[slot] = key
        ports += 1
    print(f'{path.name}: accepted, {ports} dynamic ports, {aliases} aliased keys, first={first_alias}')

for path in sorted((root/'configs').glob('endstation_*.yaml')):
    audit(path)
audit(Path(__file__).resolve().parent/'scratch/maps/sixteen-outputs.yaml')
