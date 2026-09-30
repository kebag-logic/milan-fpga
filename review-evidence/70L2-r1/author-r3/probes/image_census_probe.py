#!/usr/bin/env python3
"""Probe (not in the tree): the ruled linked-image census of aem_loaded, by address.

usage: image_census_probe.py <builder-tree> <census-stub-dir> <firmware.c> <pic|nopie>

Compiles <firmware.c> against the census stub headers with the pinned SDK compiler
at the census flags (-std=gnu99 -O0 -fno-inline), either at the SDK's default code
model (PIC, what gate 1b's census reads) or with the product's -no-pie (LiteX
common.mak BASEFLAGS). Links the unit alone with the pinned SDK linker, keeping
relocations (-q), without relaxation, under a script that defines no symbol, with
unresolved externals at 0. Reads the image's ELF symbol and relocation tables in
Python (no disassembler: the only instruction bits read are the 7-bit opcode at a
relocation site and at each AUIPC). Then:

  one name   exactly one symbol, `aem_loaded`, local, on the verdict's 4 bytes;
  references every relocation whose target lands on those bytes, under any symbol:
             an in-place load or store (%lo on a load/store) is a use in place;
             %lo on an addi, a GOT entry, a data word or any other kind forms the
             full address somewhere it can escape to;
  stores     exactly one in-place store on the verdict, inside milan_init();
  value      the resolver (rv32_unit, forget-on-call) on the same compile's
             assembly: the stores on the verdict's address, by address, are
             milan_init()'s one store of load_aem_image()'s return;
  pc-rel     every AUIPC in the image carries a relocation.
Also reports, for the PIC model, the registers holding the full address at
milan_init()'s call to nvm_boot() (from the relocations and the resolver).
Prints one VERDICT line: KEPT, or FORGOTTEN with the broken pins named.
"""
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

tree, stubs, source, model = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
assert model in ("pic", "nopie")
SDK = Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"
FLAGS = ["-std=gnu99", "-O0", "-fno-inline"] + (["-no-pie"] if model == "nopie" else [])
SCRIPT = """SECTIONS {
  . = 0x10000;
  .text : { *(.text .text.*) }
  .rodata : { *(.rodata .rodata.* .srodata .srodata.*) }
  .data : { *(.data .data.* .data.rel.ro .data.rel.ro.* .sdata .sdata.*) }
  .bss : { *(.sbss .sbss.* .bss .bss.* COMMON) }
}
"""
R = {1: "R_RISCV_32", 16: "BRANCH", 17: "JAL", 18: "CALL", 19: "CALL_PLT", 20: "GOT_HI20",
     23: "PCREL_HI20", 24: "PCREL_LO12_I", 25: "PCREL_LO12_S", 26: "HI20", 27: "LO12_I",
     28: "LO12_S", 51: "RELAX", 43: "ALIGN"}
OPC = {0x03: "load", 0x07: "load-fp", 0x23: "store", 0x27: "store-fp", 0x13: "op-imm",
       0x37: "lui", 0x17: "auipc", 0x67: "jalr", 0x6f: "jal", 0x2f: "amo"}


def run(argv):
    got = subprocess.run(argv, capture_output=True, text=True)
    assert got.returncode == 0, (argv, got.stderr[-2000:])
    return got


with tempfile.TemporaryDirectory(prefix="a457-image-") as tmp:
    tmp = Path(tmp)
    (tmp / "unit.ld").write_text(SCRIPT)
    run([str(SDK), *FLAGS, f"-I{stubs}", "-S", "-o", str(tmp / "unit.s"), str(source)])
    run([str(SDK), *FLAGS, "-c", "-o", str(tmp / "unit.o"), str(tmp / "unit.s")])
    run([str(SDK), *(["-no-pie"] if model == "nopie" else []), "-nostdlib", "-nostartfiles", "-static",
         "-Wl,-q", "-Wl,--no-relax", "-Wl,--unresolved-symbols=ignore-all", "-Wl,-e,0",
         "-Wl,-T," + str(tmp / "unit.ld"), "-o", str(tmp / "unit.elf"), str(tmp / "unit.o")])
    assembly = (tmp / "unit.s").read_text()
    elf = (tmp / "unit.elf").read_bytes()

# ---- ELF32 little-endian, read by hand -------------------------------------
assert elf[:4] == b"\x7fELF" and elf[4] == 1 and elf[5] == 1
e_flags, = struct.unpack_from("<I", elf, 0x24)
assert not e_flags & 1, "RVC image: 16-bit instructions, so words are not instructions"
e_shoff, = struct.unpack_from("<I", elf, 0x20)
e_shentsize, e_shnum, e_shstrndx = struct.unpack_from("<HHH", elf, 0x2E)
sections = [struct.unpack_from("<IIIIIIIIII", elf, e_shoff + i * e_shentsize) for i in range(e_shnum)]
shstr = sections[e_shstrndx]


def cstr(table, offset):
    start = table[4] + offset
    return elf[start:elf.index(b"\0", start)].decode()


names = [cstr(shstr, s[0]) for s in sections]
symtab_index = next(i for i, s in enumerate(sections) if s[1] == 2)
symtab = sections[symtab_index]
strtab = sections[symtab[6]]
symbols = []
for i in range(symtab[5] // 16):
    st_name, value, size, info, _other, shndx = struct.unpack_from("<IIIBBH", elf, symtab[4] + 16 * i)
    symbols.append(dict(name=cstr(strtab, st_name), value=value, size=size, bind=info >> 4,
                        type=info & 15, shndx=shndx))
verdicts = [s for s in symbols if s["name"] == "aem_loaded"]
broken = []
if len(verdicts) != 1 or verdicts[0]["type"] != 1 or verdicts[0]["size"] != 4:
    print("VERDICT FORGOTTEN: the image has no single 4-byte object named aem_loaded", verdicts)
    sys.exit(0)
verdict = verdicts[0]
lo, hi = verdict["value"], verdict["value"] + 4
if verdict["bind"] != 0:
    broken.append("aem_loaded is not a local symbol of the image")
others = sorted({s["name"] for s in symbols if s is not verdict and s["type"] not in (3, 4)
                 and s["value"] < hi and s["value"] + max(s["size"], 1) > lo})
if others:
    broken.append(f"another symbol names the verdict's storage: {others}")
functions = sorted((s["value"], s["value"] + s["size"], s["name"]) for s in symbols if s["type"] == 2)


def owner(address):
    return next((name for start, end, name in functions if start <= address < end), "<no function>")


def word_at(address):
    for s in sections:
        if s[2] & 2 and s[1] != 8 and s[3] <= address < s[3] + s[5]:
            return struct.unpack_from("<I", elf, s[4] + address - s[3])[0]
    return None


relocs = []  # (site, type, target, target-section-index)
for s in sections:
    if s[1] != 4 or not sections[s[7]][2] & 2:
        continue
    for k in range(s[5] // 12):
        offset, info, addend = struct.unpack_from("<IIi", elf, s[4] + 12 * k)
        sym = symbols[info >> 8] if info >> 8 else dict(value=0)
        relocs.append((offset, info & 255, (sym["value"] + addend) & 0xFFFFFFFF))
hi_at = {site: target for site, kind, target in relocs if kind in (20, 23)}
references, stores = [], []
for site, kind, target in relocs:
    if kind in (24, 25):  # %pcrel_lo names its %pcrel_hi's label: the address is that HI20's target
        target = hi_at.get(target)
    if target is None or not lo <= target < hi:
        continue
    opcode = OPC.get((word_at(site) or 0) & 0x7F, "data")
    where = owner(site)
    if kind in (26, 23) and opcode in ("lui", "auipc"):
        role = "upper part"
    elif kind in (27, 24) and opcode in ("load", "load-fp"):
        role = "in-place load"
    elif kind in (28, 25) and opcode in ("store", "store-fp"):
        role = "in-place store"
        stores.append(where)
    elif kind in (27, 24) and opcode == "op-imm":
        role = "FULL ADDRESS formed in a register"
    elif kind == 20:
        role = "FULL ADDRESS held in a GOT data word"
    elif kind == 1:
        role = "FULL ADDRESS held in a data word"
    else:
        role = f"UNRECOGNISED reference {R.get(kind, kind)}/{opcode}"
    references.append((where, hex(site), R.get(kind, kind), role))
escapes = [r for r in references if r[3].startswith(("FULL", "UNRECOGNISED"))]
if escapes:
    broken.append(f"the verdict's address escapes: {escapes}")
if stores != ["milan_init"]:
    broken.append(f"in-place stores on the verdict: {stores or 'none'} (exactly milan_init's one)")
auipc_sites = {site for site, kind, _t in relocs if kind in (18, 19, 20, 23)}
for s in sections:
    if s[1] == 1 and s[2] & 4:
        for off in range(0, s[5], 4):
            address = s[3] + off
            if struct.unpack_from("<I", elf, s[4] + off)[0] & 0x7F == 0x17 and address not in auipc_sites:
                broken.append(f"an AUIPC without a relocation at {hex(address)} in {owner(address)}")

# ---- the stored value, by the resolver on the same compile's assembly -------
sys.argv = ["x"]
sys.path.insert(0, str(tree / "sw/builder"))
import test_builder as tb  # noqa: E402
addresses = {s["name"]: s["value"] for s in symbols if s["type"] not in (3, 4)}


def resolved(name):
    found = re.fullmatch(r"([A-Za-z_.$][\w.$]*)(?:([+-])(\d+))?", name)
    if not found or found.group(1) not in addresses:
        return None
    delta = int(found.group(3) or 0) * (-1 if found.group(2) == "-" else 1)
    return addresses[found.group(1)] + delta


unit = tb.rv32_unit(assembly)
valued = sorted((fn, repr(value)) for fn, run_ in unit["runs"].items()
                for _at, (address, value) in run_["stores"]
                if isinstance(address, tb.Rv32Where) and address.kind == "sym"
                and (resolved(address.detail) is None or lo <= resolved(address.detail) < hi))
if valued != [("milan_init", repr(tb.Rv32Tag("call:load_aem_image")))]:
    broken.append(f"resolved stores on the verdict's address: {valued}")

# ---- PIC only: what holds the full address at milan_init()'s call to nvm_boot()
if model == "pic":
    boot = tb.rv32_run(unit["functions"]["milan_init"], unit["data"])
    for _at, (callee, handed) in boot["calls"]:
        if callee == "nvm_boot":
            holding = sorted(reg for reg, value in handed.items() if isinstance(value, tb.Rv32Sym)
                             and resolved(value.name) is not None
                             and lo <= resolved(value.name) + value.offset < hi)
            print(f"  at milan_init()'s call to nvm_boot(), the verdict's address is held in {holding}")

print(f"  model={model} verdict=0x{lo:08x} references:")
for ref in references:
    print("   ", ref)
print("VERDICT", "KEPT" if not broken else "FORGOTTEN: " + " | ".join(broken))
