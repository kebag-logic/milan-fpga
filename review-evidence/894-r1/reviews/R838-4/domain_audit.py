#!/usr/bin/env python3
"""Check generated key bounds against every advertised format and dynamic port."""
from pathlib import Path
import re
import struct
import sys

root=Path.cwd()
packet=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'sw/firmware/ctrl/aecp'))
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import aecp_entity
import aecp_arms

configs=sorted((root/'configs').glob('endstation_*.yaml'))
configs += [aecp_arms.key_geometry(packet/'scratch/domain-configs',name,widths)
            for name,widths in aecp_arms.KEY_GEOMETRIES]
total=nonempty=0
for path in configs:
    h=aecp_entity.emit(path)
    constants={k:int(v) for k,v in re.findall(r'#define AECP_ENTITY_KEY_(\w+) (\d+)u',h)}
    cfg=aecp_entity.builder.load_config(str(path))
    blob=aecp_entity.builder._entity_model_image(cfg,aecp_entity.builder.emit_aem_overlay(cfg))['aem_desc.bin']
    count=struct.unpack_from('>H',blob,8)[0]
    offset=struct.unpack_from('>I',blob,12)[0]
    descriptors={}
    for row in range(count):
        c,t,n,length,start,_,stride=struct.unpack_from('>HHHHIHH',blob,offset+16*row)
        for k in range(n):
            d=blob[start+k*stride:start+k*stride+length]
            index=struct.unpack_from('>H',d,2)[0]
            descriptors[c,t,index]=d
    first=max(constants['STREAMS'],constants['CLUSTERS'])
    width=max(constants['STREAM_CHANNELS'],constants['CLUSTER_CHANNELS'])
    slots=max(first*width,256)
    print(path.stem,constants,'domain',first*width,'slots',slots)
    for (c,t,index),d in sorted(descriptors.items()):
        if t not in (14,15) or struct.unpack_from('>H',d,16)[0]:continue
        ncluster,base=struct.unpack_from('>HH',d,12)
        keys=set()
        if t==14:
            for k in range(ncluster):
                channels=struct.unpack_from('>H',descriptors[c,20,base+k],84)[0]
                keys.update((k,ch) for ch in range(channels))
        elif ncluster:
            for (cc,tt,s),stream in descriptors.items():
                if cc!=c or tt!=6:continue
                start,n=struct.unpack_from('>HH',stream,82)
                for at in [74,*range(start,start+8*n,8)]:
                    f=struct.unpack_from('>Q',stream,at)[0]
                    if f>>56==2:keys.update((s,ch) for ch in range((f>>22)&1023))
        assert all(k<first and ch<width for k,ch in keys)
        positions={k*width+ch for k,ch in keys}
        assert len(positions)==len(keys) and all(p<slots for p in positions)
        print(' port',t,index,'accepted keys',len(keys),'PASS')
        total+=1;nonempty+=bool(keys)
print('TOTAL',total,'dynamic ports including',total-nonempty,'empty domains;',nonempty,'nonempty')
