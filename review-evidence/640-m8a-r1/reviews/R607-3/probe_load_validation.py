#!/usr/bin/env python3
"""Independent union-coverage and genuinely linked ELF refusal controls."""
import argparse, hashlib, importlib.util, json, pathlib, random, struct, subprocess, sys
ap=argparse.ArgumentParser();ap.add_argument('repo',type=pathlib.Path);ap.add_argument('out',type=pathlib.Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(a.repo/'sw/litex'));import ctrl_memory as cm;import test_ctrl_memory as t
rng=random.Random(640721)
for case in range(20000):
 segments=tuple((rng.randrange(30),bytes(rng.randrange(15))) for _ in range(rng.randrange(9)))
 start=rng.randrange(30);end=start+rng.randrange(1,25)
 covered={i for at,data in segments for i in range(at,at+len(data))}
 want=all(i in covered for i in range(start,end))
 assert cm._carried(segments,start,end)==want,(case,segments,start,end)
print('PASS: 20000 deterministic segment unions versus an independent byte-set oracle')
cc=t.fw_rv32.compiler();assert cc
linked=t.link(cc,a.out,(a.repo/'sw/firmware/ctrl/plat/ctrl_split.ld').read_text());raw=linked.read_bytes();img=cm.read_elf(linked)
words=struct.pack('<%dI'%len(cm.rom_words(img)),*cm.rom_words(img));cm.plan(img)
binary=a.out/'probe.bin';subprocess.run([cc.removesuffix('gcc')+'objcopy','-O','binary',str(linked),str(binary)],check=True)
assert words==binary.read_bytes()+bytes(-len(binary.read_bytes())%4)
oldfile=a.out/'old_ctrl_memory.py';oldfile.write_bytes(subprocess.check_output(['git','-C',str(a.repo),'show','76605880:sw/litex/ctrl_memory.py']))
spec=importlib.util.spec_from_file_location('old_ctrl_memory',oldfile);old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
oldimage=old.read_elf(linked);assert old.rom_words(oldimage)==cm.rom_words(img);assert old.plan(oldimage).summary()==cm.plan(img).summary()
print('PASS: valid linked ROM and plan match previous head; objcopy SHA256',hashlib.sha256(words).hexdigest())
phoff=struct.unpack_from('<I',raw,28)[0];ents,num=struct.unpack_from('<HH',raw,42)
count=0
for n in range(num):
 at=phoff+n*ents;kind,off,vaddr,paddr,filesz,memsz,flags,align=struct.unpack_from('<8I',raw,at)
 if kind!=1 or not filesz:continue
 for size in sorted({0,1,3,4,filesz-1}):
  if size>=filesz:continue
  data=bytearray(raw);struct.pack_into('<I',data,at+16,size);path=a.out/f'segment-{n}-filesz-{size}.elf';path.write_bytes(data)
  try:cm.plan(cm.read_elf(path))
  except cm.Refusal as e:
   expected='entry bytes' if paddr==0 and size<4 else 'load coverage'
   assert e.rule==expected,(n,size,e.rule,expected)
   print(f'PASS: linked segment {n} filesz {filesz}->{size}: {e.check} / {e.rule}');count+=1
  else:raise AssertionError((n,size,'accepted'))
print('PASS: linked truncation variants',count)
