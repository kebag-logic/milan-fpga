#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Link a reachable ctrl_app composition and report separate RAM sections.

Runtime archives must be bare-metal ILP32 libraries, never the SDK's glibc.
Their sizes and hashes are recorded alongside the section and symbol reports.
The firmware objects are rebuilt with the shared CI-pinned RV32 compiler.
The ELF is a size fixture; it has no board reset entry or fabric licence port.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from ctrl_build import CTRL, HERE, ROOT, PORTABLE, RV32_FLAGS, NVM_DIR, Tree, Refusal, run
from srp_arms import prepared, LWSRP_SOURCES
from ctrl_arms import lwsrp_pin
import fw_gtest
import fw_rv32


def checked(argv: list[str]) -> str:
    """Every compiler and binary inspection must succeed."""
    result=run(argv)
    if result.returncode:
        raise Refusal(result.stdout+result.stderr)
    return result.stdout


def main() -> int:
    """Measure one selected shape and composition."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--ctrl-source",type=Path,default=CTRL)
    parser.add_argument("--without-srp",action="store_true")
    parser.add_argument("--interfaces",type=int,choices=(1,2),default=1)
    parser.add_argument("--libc",type=Path,required=True)
    parser.add_argument("--compiler-runtime",type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    try:
        cc=fw_rv32.compiler()
        if cc is None:
            raise Refusal("the pinned RV32 compiler is required")
        tree=Tree(args.ctrl_source.resolve(),out,out/"reuse",fw_gtest.Build(jobs=4))
        variant,inc=prepared(tree,args.interfaces,out,args.config.resolve())
        checked([sys.executable,"-B",str(CTRL/"adp/adp_entity.py"),str(args.config),
                 "-o",str(out/"adp_entity_gen.h")])
        flags=[*RV32_FLAGS,"-DNDEBUG","-fno-pie","-ffunction-sections","-fdata-sections"]
        inc += [f"-I{out}",f"-I{NVM_DIR}",*fw_rv32.includes(cc)]
        sources=[(variant if name.startswith("mbx/") else tree.src)/name for name in PORTABLE]
        sources += [tree.src/"plat/mbx_plat_mmio.c",HERE/"ctrl_image.c"]
        libraries=[args.libc.resolve(),args.compiler_runtime.resolve()]
        if not args.without_srp:
            lw=ROOT/"third_party/lwSRP"; lwsrp_pin(lw)
            inc += [f"-I{tree.src/'srp'}",f"-I{lw/'src/include'}",f"-I{lw/'src'}"]
            flags += ["-DCTRL_IMAGE_SRP","-DLWSRP_MILAN=1"]
            sources += [tree.src/"app/ctrl_app_srp.c",tree.src/"srp/srp_mbx.c",
                        *[lw/"src"/name for name in LWSRP_SOURCES]]
        objects=[]
        for index,src in enumerate(sources):
            obj=out/f"{index}-{src.stem}.o"
            checked([cc,*flags,*inc,"-c",str(src),"-o",str(obj)])
            objects.append(obj)
        findings=fw_rv32.object_findings(cc,objects)
        if findings:
            raise Refusal(str(findings))
        elf=out/"ctrl_app.elf"; mapfile=out/"ctrl_app.map"
        ldflags=[]
        checked([cc,"-march=rv32i","-mabi=ilp32","-nostdlib","-static","-no-pie",
                 "-Wl,--gc-sections,--build-id=none",f"-Wl,-Map,{mapfile}",
                 "-T",str(HERE/"ctrl_image.ld"),*ldflags,*map(str,objects),
                 "-Wl,--start-group",*map(str,libraries),"-Wl,--end-group","-o",str(elf)])
        nm=cc.removesuffix("gcc")+"nm"
        data=elf.read_bytes()
        attributes=checked([cc.removesuffix("gcc")+"readelf","-A",str(elf)])
        arches=re.findall(r'Tag_RISCV_arch: "([^"]+)"',attributes)
        if (data[:7] != b"\x7fELF\x01\x01\x01" or
                struct.unpack_from("<HH",data,16) != (2,243) or
                struct.unpack_from("<I",data,36)[0] != 0 or
                len(arches) != 1 or not re.fullmatch(r"rv32i\d+p\d+",arches[0])):
            raise Refusal("linked image must be RV32I ILP32, including runtime code")
        symbols=checked([nm,"-S",str(elf)])
        if checked([nm,"-u",str(elf)]).strip():
            raise Refusal("linked runtime has unresolved symbols")
        forbidden={"malloc","calloc","realloc","free","sbrk","_sbrk"}
        names={line.split()[-1] for line in symbols.splitlines() if line.split()}
        if names & forbidden:
            raise Refusal("heap dependency in composed image")
        required={"ctrl_app_start","ctrl_loop_run","image_app","image_arena"}
        if not args.without_srp:
            required |= {"ctrl_app_start_maap","ctrl_app_attach_srp","maap_rx","maap_poll",
                         "acmp_rx","acmp_poll","image_acmp","srp_mbx_init","srp_mbx_attach","srp_mbx_bind","mrp_rx",
                         "mrp_transmit","image_srp","image_sources"}
        if required-names:
            raise Refusal(f"composition discarded required code/storage: {sorted(required-names)}")
        size=checked([cc.removesuffix("gcc")+"size","-A",str(elf)])
        sections={name:int(count) for name,count in re.findall(r"^(\.\S+)\s+(\d+)\s+",size,re.M)}
        if any(name not in sections for name in (".text",".rodata",".bss",".stack")):
            raise Refusal("missing measured sections")
        storage={}
        addresses={}
        for line in symbols.splitlines():
            fields=line.split()
            if len(fields)>=3:
                addresses[fields[-1]]=int(fields[0],16)
            if len(fields)==4 and fields[3].startswith("image_"):
                storage[fields[3]]=int(fields[1],16)
        records=[]
        for path in [*libraries,elf,mapfile]:
            records.append({"name":path.name,"size":path.stat().st_size,
                            "sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
        report={"shape":args.config.stem,"interfaces":args.interfaces,"srp":not args.without_srp,
                "sections":sections,"static_storage":storage,"artifacts":records,
                "ram_sections":sum(sections.get(n,0) for n in (".text",".rodata",".data",".bss",".stack")),
                "ram_span":addresses["__image_end"]-addresses["__image_start"]}
        (out/"symbols.txt").write_text(symbols)
        (out/"size.txt").write_text(size)
        (out/"size.json").write_text(json.dumps(report,indent=2)+"\n")
        print(json.dumps(report,indent=2))
        return 0
    except (Refusal,OSError,ValueError) as error:
        print(f"REFUSED: {error}",file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
