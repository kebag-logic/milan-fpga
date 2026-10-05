#!/usr/bin/env python3
"""Link the focused suite's RV32I objects with libgcc and audit symbols."""
import pathlib, re, subprocess, sys
p=pathlib.Path(__file__).resolve().parents[1]; cc=pathlib.Path(sys.argv[1])
def run(argv):return subprocess.check_output([str(a) for a in argv],text=True)
objects=sorted((p/'scratch/firmware/checkout/rv32').glob('*.o'))
assert len(objects)==9, objects
libgcc=run([cc,'-march=rv32i','-mabi=ilp32','-print-libgcc-file-name']).strip()
out=p/'scratch/ctrl-linked.o'
subprocess.run([str(cc),'-march=rv32i','-mabi=ilp32','-nostdlib','-Wl,-r','-o',str(out),*[str(f) for f in objects],libgcc],check=True)
prefix=str(cc)[:-3]
undefined=run([prefix+'nm','-u',out]); print('Relocatable link: nine RV32I freestanding objects + libgcc; no C library.');print(undefined,end='')
assert {x.split()[-1] for x in undefined.splitlines()}=={'memcpy','memset','vsnprintf'}
all_symbols=run([prefix+'nm',out]); heap=re.findall(r'\b(?:malloc|calloc|realloc|free|sbrk|_sbrk)\s*$',all_symbols,re.M)
assert not heap,heap
print('PASS: no libc heap or OS dependency; shlan_* names are defined static-pool port functions.')
print(run([prefix+'readelf','-A',out]),end='')
dis=run([prefix+'objdump','-d',out]); (p/'receipts/rv32-disassembly.txt').write_text(dis)
instructions=[]
for line in dis.splitlines():
    match=re.match(r'\s*[0-9a-f]+:\s+[0-9a-f]+\s+(\S+)',line)
    if match:instructions.append(match[1])
extra=[x for x in instructions if re.match(r'^(?:mul|div|rem|amo|lr\.|sc\.|f[a-z]|c\.)',x)]
assert not extra,extra
print('PASS: linked instructions contain no M, A, floating-point or compressed instructions; library ELF attributes advertise a superset.')
print('Unique instruction mnemonics: '+', '.join(sorted(set(instructions))))
print(run([prefix+'size',out]).replace(str(out),'ctrl-linked.o'),end='')
