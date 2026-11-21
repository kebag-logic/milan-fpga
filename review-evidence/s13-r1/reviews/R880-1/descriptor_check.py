#!/usr/bin/env python3
"""Independently check generated descriptor bytes and reported ROM instruction deltas."""
import hashlib
from pathlib import Path
import struct
import sys
import zlib
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo/'sw/builder'))
import endstation_builder as eb
sys.path.insert(0, str(repo/'avdecc'))
import gen_aem_store as g
for shape, expected in [('1x1_tdm8',(0x38a80323,0xdb1deab5)), ('8x8',(0xd6dd74b9,0xb730ec91))]:
 cfg = eb.load_config(str(repo/f'configs/endstation_ax7101_{shape}.yaml'))
 images=[]
 for placement in ('all-fabric','split'):
  at=eb.with_placement(cfg,placement)
  model=g.build_model(g.spec_from_overlay(eb.emit_aem_overlay(at)))
  rom=eb._entity_model_image(at, eb.emit_aem_overlay(at))['aem_desc.bin']
  field=at['entity']['firmware_version'].encode()+bytes(64-len(at['entity']['firmware_version']))
  assert rom.count(field)==1
  entity=rom.index(field)-116
  print(shape, placement, 'ROM length',len(rom),'ENTITY base',entity,
        'version',rom[entity+116:entity+180].rstrip(b'\0'),
        'CRC32',hex(zlib.crc32(rom)), 'sha256',hashlib.sha256(rom).hexdigest())
  images.append((rom,entity))
 a,b=images
 assert a[1]==b[1] and len(a[0])==len(b[0])
 diff=[i for i,(x,y) in enumerate(zip(a[0],b[0])) if x!=y]
 assert diff==[a[1]+116] and (a[0][diff[0]], b[0][diff[0]])==(50,51)
 print('PASS independent descriptor delta: one byte at',hex(diff[0]))
 # The reported RISC-V instruction words: decode LUI plus signed ADDI.
 words = ((0x38a807b7,0x32378793),(0xdb1df7b7,0xab578793)) if shape=='1x1_tdm8' else ((0xd6dd77b7,0x4b978793),(0xb730f7b7,0xc9178793))
 values=[]
 for lui,addi in words:
  assert lui&127==0x37 and addi&0x707f==0x13
  assert ((lui>>7)&31)==((addi>>7)&31)==((addi>>15)&31)==15
  imm=addi>>20
  if imm&0x800: imm-=4096
  values.append(((lui&0xfffff000)+imm)&0xffffffff)
 assert values==[zlib.crc32(x[0]) for x in images], (values, [zlib.crc32(x[0]) for x in images])
 bits=sum((x^y).bit_count() for x,y in zip(words[0],words[1]))
 byte_count=sum(x!=y for x,y in zip(struct.pack('<II',*words[0]),struct.pack('<II',*words[1])))
 print('PASS reported instruction constants equal independently computed CRC32; changed bits',bits,'changed bytes',byte_count,'plus one descriptor byte')
