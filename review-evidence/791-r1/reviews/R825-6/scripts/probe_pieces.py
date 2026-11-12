"""Probe: ctrl_memory.cpu_regions tiles each split region exactly with aligned power-of-two pieces,
with no overlap or gap, and S9's journal_klj3 flash slot lies inside the flash window the CPU decodes.
usage: python3 probe_pieces.py <repo>"""
import sys, pathlib
repo = pathlib.Path(sys.argv[1]); sys.path[:0] = [str(repo / "sw/litex"), str(repo / "scripts")]
import ctrl_memory, milan_soc
contract = milan_soc.ctrl_mailbox_contract()
rows = [(ctrl_memory.ROM.origin, ctrl_memory.ROM.size, "rxc", "p"), (ctrl_memory.RAM.origin, ctrl_memory.RAM.size, "rwxc", "p"),
        (0x0100_0000, milan_soc.FLASH_SIZE, "rxc", "p"), (milan_soc.MILAN_CSR_BASE, milan_soc.MILAN_CSR_SIZE, "rw", "p"),
        (milan_soc.CTRL_MBX_BASE, contract.window_bytes, "rw", "p")]
pieces = ctrl_memory.cpu_regions(rows); bad = 0
for o, s, m, b in rows:
    mine = sorted((po, ps) for po, ps, pm, pb in pieces if o <= po < o + s and (pm, pb) == (m, b))
    ok = all(ps & (ps - 1) == 0 and po % ps == 0 for po, ps in mine) and mine[0][0] == o and \
        all(a[0] + a[1] == c[0] for a, c in zip(mine, mine[1:])) and mine[-1][0] + mine[-1][1] == o + s
    bad += not ok; print(f"{'ok ' if ok else 'BAD'} {o:#010x}+{s:#x}: {[(hex(a), hex(c)) for a, c in mine]}")
assert sum(ps for _, ps, *_ in pieces) == sum(s for _, s, *_ in rows), "pieces overlap or leave a gap"
j = milan_soc.FLASHBOOT_RESERVED["journal_klj3"]
inside = j["offset"] + j["size"] <= milan_soc.FLASH_SIZE
print(f"journal_klj3 flash [{j['offset']:#x}, {j['offset'] + j['size']:#x}) inside the {milan_soc.FLASH_SIZE:#x}-byte flash window: {inside}")
print("PROBE", "PASS" if not bad and inside else "FAIL"); sys.exit(1 if bad or not inside else 0)
