#!/usr/bin/env python3
"""Independent composed-image link. Scaffolding measures sections, not board boot."""
import argparse,json,subprocess,sys,os,hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--cc',default='riscv64-elf-gcc');a=ap.parse_args()
r=a.root.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(r/'sw/firmware/ctrl/adp'));import adp_entity
import yaml,copy
cfg=yaml.safe_load((r/'configs/endstation_ax7101_8x8.yaml').read_text())
for kind,n in [('listeners',15),('talkers',16)]:
 sample=cfg['streams'][kind][0];cfg['streams'][kind]=[dict(sample,name=f'{kind} {i}') for i in range(n)]
cap=out/'capacity.yaml';cap.write_text(yaml.safe_dump(cfg,sort_keys=False))
configs=[r/'configs/endstation_ax7101_1x1_tdm8.yaml',r/'configs/endstation_ax7101_8x8.yaml',cap]
cc=a.cc;prefix=cc.removesuffix('gcc');flags=['-march=rv32i','-mabi=ilp32','-Os','-DNDEBUG','-std=c11','-ffreestanding','-fno-stack-protector','-ffunction-sections','-fdata-sections','-DCTRL_MBX_BASE=0x80000000u']
commands=[]
def run(cmd):
 commands.append(cmd);p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,p.stdout+p.stderr;return p.stdout
results=[]
for config in configs:
 fields=adp_entity.entity_fields(config)
 for interfaces in ([1,2] if config==cap else [1]):
  for label,root in [('dev',a.baseline.resolve()),('head',r)]:
   d=out/f'{config.stem}-if{interfaces}-{label}';d.mkdir(exist_ok=True)
   (d/'entity.h').write_text(adp_entity.emit_header(fields,config.name))
   extra=[]
   if interfaces==2:
    run(['python3',str(r/'sw/mailbox/gen_mailbox.py'),'--variant-interfaces','2','--out',str(d/'gen')]);extra=['-include',str(d/'gen/mbx_contract.h')]
   src=root/'sw/firmware/ctrl';includes=[f'-I{src/x}' for x in ['mbx','wire','port','loop','adp','maap','app']]+[f'-I{d}']
   maap=label=='head'
   text='#include "ctrl_app.h"\n#include "entity.h"\n#include <stdint.h>\n'
   if maap:text+='#include "maap_csr.h"\nstatic struct maap_csr csr;\nstatic uint32_t rd(void *p,unsigned i,uint32_t off){(void)p;return *(volatile uint32_t *)(uintptr_t)(0x90000000u+i*0x10000u+off);}\nstatic void wr(void *p,unsigned i,uint32_t off,uint32_t v){(void)p;*(volatile uint32_t *)(uintptr_t)(0x90000000u+i*0x10000u+off)=v;}\n'
   text+='static struct ctrl_app app;\nstatic _Alignas(max_align_t) unsigned char arena[32];\nstatic const struct ctrl_pool_class classes[]={{16,1}};\nstatic const struct adp_entity entity=ADP_ENTITY_GEN_INIT;\nstatic const struct ctrl_app_config cfg={&entity,0,arena,sizeof arena,classes,1,0,0};\nvoid _start(void){\n'
   if maap:text+=f'(void)maap_csr_init(&csr,(struct maap_csr_port){{0,rd,wr}},{fields["talker_stream_sources"]-1},true,1,1);\n(void)ctrl_app_start_maap(&app,&cfg,maap_csr_allocation,&csr,0);\n'
   else:text+='(void)ctrl_app_start(&app,&cfg);\n'
   text+='for(;;)ctrl_loop_step(&app.loop);}\n';(d/'entry.c').write_text(text)
   sources=['mbx/mbx.c','loop/ctrl_loop.c','port/ctrl_pool.c','port/ctrl_debug.c','port/shlan_port.c','adp/adp.c','adp/adp_mbx.c','app/ctrl_app.c','plat/mbx_plat_mmio.c']
   if maap:sources+=['maap/maap.c','maap/maap_mbx.c','maap/maap_csr.c']
   objs=[]
   for i,s in enumerate([src/x for x in sources]+[d/'entry.c']):
    obj=d/f'{i}.o';run([cc,*flags,*includes,*extra,'-c',str(s),'-o',str(obj)]);objs.append(str(obj))
   ld=d/'layout.ld';ld.write_text('ENTRY(_start)\nSECTIONS { . = 0x10000; .text : { *(.text .text.*) } .rodata : { *(.rodata .rodata.* .srodata .srodata.*) } .data : { *(.data .data.* .sdata .sdata.*) } .bss (NOLOAD) : { *(.bss .bss.* .sbss .sbss.*) *(COMMON) } .stack (NOLOAD) : { . = ALIGN(16); . += 4096; } }\n')
   elf=d/'app.elf';run([cc,*flags,'-nostartfiles','-nostdlib','-static','-Wl,--gc-sections,--no-undefined',f'-Wl,-Map={d / "app.map"}','-T',str(ld),*objs,'-Wl,--start-group','-lc','-lgcc','-Wl,--end-group','-o',str(elf)])
   undefined=run([prefix+'nm','-u',str(elf)]);assert not undefined.strip(),undefined
   symbols=run([prefix+'nm','-S','--size-sort',str(elf)]);(d/'symbols.txt').write_text(symbols)
   assert 'ctrl_app_start' in symbols and 'ctrl_loop_step' in symbols and 'mbx_hal_read32' in symbols
   if maap:assert all(x in symbols for x in ['maap_rx','maap_csr_allocation','maap_mbx_start'])
   assert not any(' '+n+'\n' in symbols for n in ['malloc','calloc','free','__assert_fail'])
   size=run([prefix+'size','-A',str(elf)]);sections={x.split()[0]:int(x.split()[1]) for x in size.splitlines() if x.startswith('.')}
   dims='#include "ctrl_app.h"\n'
   dims+='char sizeof_app[sizeof(struct ctrl_app)];char sizeof_pool[sizeof(struct ctrl_pool)];char sizeof_loop[sizeof(struct ctrl_loop)];char sizeof_adp[sizeof(struct adp_mbx)];\n'
   if maap:dims+='char sizeof_maap[sizeof(struct maap_mbx)];\n'
   (d/'dimensions.c').write_text(dims);run([cc,*flags,*includes,*extra,'-c',str(d/'dimensions.c'),'-o',str(d/'dimensions.o')])
   ds=run([prefix+'nm','-S',str(d/'dimensions.o')]);dimensions={line.split()[-1]:int(line.split()[1],16) for line in ds.splitlines() if ' sizeof_' in line}
   results.append(dict(shape=config.stem,interfaces=interfaces,image=label,fields=fields,sections=sections,dimensions=dimensions,undefined=undefined,elf_sha256=hashlib.sha256(elf.read_bytes()).hexdigest()))
   print(json.dumps(results[-1]),flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n');(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
