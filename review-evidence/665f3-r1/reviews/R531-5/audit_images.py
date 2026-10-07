#!/usr/bin/env python3
"""Independent final-ELF audit; imports no candidate checking code."""
import argparse, hashlib, json, re, struct, subprocess
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("images", type=Path); ap.add_argument("prefix"); a=ap.parse_args()
allowed=set("lui auipc jal jalr beq bne blt bge bltu bgeu lb lh lw lbu lhu sb sh sw addi slti sltiu xori ori andi slli srli srai add sub sll slt sltu xor srl sra or and fence ecall ebreak".split())
reports=[]
for f in sorted(a.images.glob("*/*/ctrl_app.elf")):
 b=f.read_bytes(); assert b[:7]==b"\x7fELF\x01\x01\x01", f
 h=struct.unpack_from("<HHIIIIIHHHHHH",b,16)
 assert h[0]==2 and h[1]==243 and h[2]==1 and h[6]==0, (f,h)
 sections=[struct.unpack_from("<IIIIIIIIII",b,h[5]+i*h[10]) for i in range(h[11])]
 strings=sections[h[12]]; names=b[strings[4]:strings[4]+strings[5]]
 def name(s): return names[s[0]:].split(b"\0",1)[0].decode()
 exec_bytes=sum(s[5] for s in sections if s[2]&4 and s[1]!=8)
 headers=subprocess.check_output([a.prefix+"readelf","-hA",str(f)],text=True)
 arch=re.findall(r'Tag_RISCV_arch: "([^"]+)"',headers); assert arch==["rv32i2p1"], arch
 syms=subprocess.check_output([a.prefix+"readelf","-Ws",str(f)],text=True)
 undefined=[line for line in syms.splitlines() if re.search(r"\bUND\s+\S",line)]
 assert not undefined, undefined
 dis=subprocess.check_output([a.prefix+"objdump","-d","-M","no-aliases",str(f)],text=True)
 words=re.findall(r"^\s*[0-9a-f]+:\s+([0-9a-f]+)\s+(\S+)",dis,re.M)
 assert len(words)*4==exec_bytes, (len(words),exec_bytes)
 assert all(len(w)==8 and int(w,16)&3==3 and m in allowed for w,m in words), [(w,m) for w,m in words if m not in allowed]
 sizes={name(s):s[5] for s in sections if s[2]&2}
 report={"image":str(f.relative_to(a.images)),"sha256":hashlib.sha256(b).hexdigest(),"flags":h[6],"architecture":arch[0],"instruction_words":len(words),"mnemonics":sorted({m for _,m in words}),"allocated_sections":sizes,"section_total":sum(sizes.values()),"undefined_symbols":undefined,"status":"PASS"}
 reports.append(report)
assert len(reports)==4
print(json.dumps(reports,indent=2))
