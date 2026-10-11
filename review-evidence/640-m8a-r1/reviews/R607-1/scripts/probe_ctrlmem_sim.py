#!/usr/bin/env python3
"""R607-1 independent probe: the real milan_soc.CtrlMemory at a real image's banks.

Builds rom (initialised from the image) and sram exactly as add_ctrl_memory
does, from one linked split ELF, and checks in migen simulation:
  A. rom: every bank's first/last word plus a stride sample equal the image's
     load bytes (an independent pyelftools-free reader: the raw PT_LOAD bytes);
  B. both regions: addresses past the last bank, sampled across the whole
     decoded window (up to 2**16 words, beyond the 224 KiB region too), answer
     err, never ack;
  C. sram: a write at a sample of addresses past the last bank lands in no bank;
  D. back-to-back: a bank access issued on the cycle after an err completes
     with ack and the correct data (no stale err);
  E. sram writes and reads at every bank edge.

    probe_ctrlmem_sim.py <tree> <elf>
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

tree, elf = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/litex"))
import ctrl_memory  # noqa: E402
import milan_soc  # noqa: E402
from migen import ClockDomain, Module, run_simulation  # noqa: E402


def load_bytes(path: Path) -> bytes:
    """rom's initial bytes from the PT_LOAD headers, read independently."""
    data = path.read_bytes()
    phoff, = struct.unpack_from("<I", data, 28)
    phentsize, phnum = struct.unpack_from("<HH", data, 42)
    out = bytearray()
    for i in range(phnum):
        ptype, off, _vaddr, paddr, filesz, _m, _f, _a = struct.unpack_from("<8I", data, phoff + i * phentsize)
        if ptype == 1 and filesz:
            assert paddr < 0x38000, hex(paddr)
            if len(out) < paddr + filesz:
                out.extend(bytes(paddr + filesz - len(out)))
            out[paddr:paddr + filesz] = data[off:off + filesz]
    out.extend(bytes(-len(out) % 4))
    return bytes(out)


image = ctrl_memory.read_elf(elf)
plan = ctrl_memory.plan(image)
raw = load_bytes(elf)
words = list(struct.unpack(f"<{len(raw) // 4}I", raw))
assert words == ctrl_memory.rom_words(image)[:len(words)], "rom_words differs from the PT_LOAD bytes"


class Bench(Module):
    def __init__(self):
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.submodules.rom = milan_soc.CtrlMemory(ctrl_memory.ROM, plan.rom_banks, ctrl_memory.rom_words(image))
        self.submodules.ram = milan_soc.CtrlMemory(ctrl_memory.RAM, plan.ram_banks, None)


bench = Bench()
problems: list[str] = []


def access(bus, adr, we=0, dat=0, sel=0xF):
    yield bus.adr.eq(adr); yield bus.we.eq(we); yield bus.dat_w.eq(dat); yield bus.sel.eq(sel)
    yield bus.cyc.eq(1); yield bus.stb.eq(1)
    ans = ("none", None)
    for _ in range(8):
        yield
        a, e = (yield bus.ack), (yield bus.err)
        if a or e:
            ans = ("ack" if a else "err", (yield bus.dat_r))
            break
    yield bus.cyc.eq(0); yield bus.stb.eq(0)
    return ans


def back_to_back(bus, hole_adr, good_adr):
    """err on the hole, then the next cycle a bank read: it must ack with its data."""
    yield bus.adr.eq(hole_adr); yield bus.we.eq(0); yield bus.sel.eq(0xF)
    yield bus.cyc.eq(1); yield bus.stb.eq(1)
    first = None
    for _ in range(8):
        yield
        if (yield bus.err) or (yield bus.ack):
            first = "err" if (yield bus.err) else "ack"
            break
    yield bus.adr.eq(good_adr)          # next request presented immediately
    second = ("none", None)
    for _ in range(8):
        yield
        a, e = (yield bus.ack), (yield bus.err)
        if a or e:
            second = ("ack" if a else "err", (yield bus.dat_r))
            break
    yield bus.cyc.eq(0); yield bus.stb.eq(0)
    yield
    return first, second


def edges(banks):
    out, first = [], 0
    for size in banks:
        d = size // 4
        out += [first, first + d - 1]
        first += d
    return out, first


rom_edges, rom_words_n = edges(plan.rom_banks)
ram_edges, ram_words_n = edges(plan.ram_banks)
ram_base = ctrl_memory.RAM.origin // 4
window = 1 << 16
results: dict[str, object] = {}


def run():
    rom_addrs = sorted(set([a for a in rom_edges if a < len(words)] + list(range(0, len(words), 97))))
    got = []
    for a in rom_addrs:
        got.append((a, (yield from access(bench.rom.bus, a))))
    results["rom"] = got
    holes = sorted(set([rom_words_n, rom_words_n + 1, 0xDFFF, 0xE000, 0xFFFF] + list(range(rom_words_n, window, 1531))))
    results["rom_hole"] = []
    for a in holes:
        results["rom_hole"].append((a, (yield from access(bench.rom.bus, a))))
    rholes = sorted(set([ram_words_n, ram_words_n + 1, 0xDFFF, 0xE000, 0xFFFF] + list(range(ram_words_n, window, 1531))))
    for a in rholes:
        yield from access(bench.ram.bus, ram_base + a, we=1, dat=0x5A5A_5A5A)
    results["ram_hole"] = []
    for a in rholes:
        results["ram_hole"].append((a, (yield from access(bench.ram.bus, ram_base + a))))
    # every sram bank edge: write a tag, read it back; then the alias cells of each hole write
    for a in ram_edges:
        yield from access(bench.ram.bus, ram_base + a, we=1, dat=(a * 2654435761) & 0xFFFFFFFF)
    results["ram_edges"] = []
    for a in ram_edges:
        results["ram_edges"].append((a, (yield from access(bench.ram.bus, ram_base + a))))
    alias = sorted({a % size for a in rholes for size in (s // 4 for s in plan.ram_banks)} - set(ram_edges))
    results["ram_alias"] = []
    for a in alias[:400]:
        results["ram_alias"].append((a, (yield from access(bench.ram.bus, ram_base + a))))
    results["b2b_rom"] = yield from back_to_back(bench.rom.bus, rom_words_n + 5, 3)
    results["b2b_ram"] = yield from back_to_back(bench.ram.bus, ram_base + ram_words_n + 5, ram_base + ram_edges[0])


run_simulation(bench, run())

bad = [(a, r) for a, r in results["rom"] if r != ("ack", words[a])]
print(f"A rom reads: {len(results['rom'])} words checked, {len(bad)} wrong {bad[:3]}")
problems += ["A"] if bad else []
for key in ("rom_hole", "ram_hole"):
    bad = [(hex(a), r) for a, r in results[key] if r[0] != "err"]
    print(f"B {key}: {len(results[key])} addresses past the last bank up to 0xFFFF, {len(bad)} not err {bad[:3]}")
    problems += ["B " + key] if bad else []
bad = [(a, r) for a, r in results["ram_alias"] if r[0] != "ack" or r[1] == 0x5A5A_5A5A]
print(f"C sram alias cells: {len(results['ram_alias'])} checked, {len(bad)} written by a hole write {bad[:3]}")
problems += ["C"] if bad else []
want_rom = ("err", ("ack", words[3]))
print(f"D back-to-back rom: {results['b2b_rom']} want {want_rom}")
problems += ["D rom"] if (results["b2b_rom"][0], results["b2b_rom"][1]) != want_rom else []
want_ram = ("err", ("ack", (ram_edges[0] * 2654435761) & 0xFFFFFFFF))
print(f"D back-to-back sram: {results['b2b_ram']} want {want_ram}")
problems += ["D ram"] if (results["b2b_ram"][0], results["b2b_ram"][1]) != want_ram else []
bad = [(a, r) for a, r in results["ram_edges"] if r != ("ack", (a * 2654435761) & 0xFFFFFFFF)]
print(f"E sram bank edges: {len(results['ram_edges'])} checked, {len(bad)} wrong")
problems += ["E"] if bad else []
print(f"banks rom {plan.rom_banks} sram {plan.ram_banks}")
print("PROBE RESULT:", "PASS" if not problems else f"FAIL {problems}")
sys.exit(1 if problems else 0)
