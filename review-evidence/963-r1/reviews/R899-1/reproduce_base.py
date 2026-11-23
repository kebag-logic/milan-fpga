#!/usr/bin/env python3
"""Reuse a measured head model only after proving the base image differs inside map_command alone.
Usage: reproduce_base.py CHECKOUT PACKET HEAD_BUILD
Run with the same environment and interpreter as ctrl_service_budget/run.py.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
root, packet, head_build = (Path(v).resolve() for v in sys.argv[1:])
sys.path[:0] = [str(root/'tb/verilator/ctrl_service_budget'), str(root/'sw/litex')]
import build
import run
import ctrl_memory
import scenario
label=head_build.name.replace('head','base')
out = packet/'scratch'/label
out.mkdir(parents=True, exist_ok=True)
head_spec = json.loads((head_build/'build.json').read_text())
head_source = (root/'sw/firmware/ctrl/aecp/aecp_maps.c').read_text()
base_source = subprocess.check_output(['git','-C',str(root),'show',
 'dd163e41438acb86e0c4d4e76df90f3f91ace1c0:sw/firmware/ctrl/aecp/aecp_maps.c'],text=True)
plant=build.Plant('base-source','ctrl/aecp/aecp_maps.c',head_source,base_source)
elf=build.firmware(out,head_spec['shape'],head_spec['interfaces'],plant,
                   head_spec['variant'],Path(head_spec['flash_map']))
base_image=ctrl_memory.read_elf(elf)
head_image=ctrl_memory.read_elf(Path(head_spec['elf']))
base_words=ctrl_memory.rom_words(base_image)
head_words=ctrl_memory.rom_words(head_image)
base_bytes=b''.join(w.to_bytes(4,'little') for w in base_words)
head_bytes=b''.join(w.to_bytes(4,'little') for w in head_words)
build.symbols(elf)
base_functions=json.loads((elf.parent/'functions.json').read_text())
head_functions=json.loads((Path(head_spec['elf']).parent/'functions.json').read_text())
assert base_functions==head_functions, 'function addresses or extents changed'
name,addr,size=next(f for f in head_functions if f[0]=='aecp_map_command')
assert len(base_bytes)==len(head_bytes)
diff=[i for i,(a,b) in enumerate(zip(base_bytes,head_bytes)) if a!=b]
assert diff and all(addr<=i<addr+size for i in diff)
assert build.code_modules(elf.with_suffix('.map'))==build.code_modules(Path(head_spec['elf']).with_suffix('.map'))
proof=dict(base='dd163e41438acb86e0c4d4e76df90f3f91ace1c0',head='4cca956932073b3f704f12f81c53f2934cfa215c',
 same_functions=True,same_module_spans=True,map_address=addr,map_bytes=size,changed_bytes=len(diff),
 base_image_sha256=hashlib.sha256(base_bytes).hexdigest(),head_image_sha256=hashlib.sha256(head_bytes).hexdigest(),
 rom_bytes=len(base_bytes),source_only_substitution=True)
(packet/f'{label}-image-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
shutil.copytree(head_build/'gateware',out/'gateware',dirs_exist_ok=True)
inits=sorted((out/'gateware').glob('sim_rom_bank*.init'),key=lambda p:int(p.stem.split('bank')[1]))
banks=[[int(x,16) for x in init.read_text().split()] for init in inits]
original=[word for bank in banks for word in bank]
assert original[:len(head_words)]==head_words
assert len(base_words)<=len(original)
original[:len(base_words)]=base_words
offset=0
for init,bank in zip(inits,banks):
    init.write_text(''.join(f'{w:08x}\n' for w in original[offset:offset+len(bank)]))
    offset+=len(bank)
(out/'native').mkdir(exist_ok=True)
shutil.copy2(head_build/'native/Vsim',out/'native/Vsim')
point=scenario.point('1x1' if '1x1' in head_spec['shape'] else '8x8-1if',head_spec)
groups=[g for g in run.all_groups(point,head_spec) if g.name=='aecp-largest-notice']
assert len(groups)==1
results_dir=out/'results'
results_dir.mkdir(exist_ok=True)
log=run.run_group(out,results_dir,groups[0],'-')
results,refusals,misses=run.graded(groups,[log],head_spec,results_dir)
receipt=dict(results=results,refusals=refusals,misses=misses)
(packet/f'{label}-results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(proof,indent=2))
assert not refusals and not misses
print(json.dumps(results[0]['passes']['share'],indent=2))
