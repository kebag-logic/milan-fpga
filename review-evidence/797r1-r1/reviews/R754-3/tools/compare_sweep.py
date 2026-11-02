#!/usr/bin/env python3
"""Read every printed read-table row of the page as one conjunction and compare
it with a sweep. A read must match exactly one value, and that value is what it
returned. Usage: compare_sweep.py <page> <sweep log> <N_LISTENERS> ; exit 1 on a disagreement."""
import re
import sys

page = open(sys.argv[1], encoding="utf-8").read().splitlines()
n_l = int(sys.argv[3])
tables, name = {}, None
for at, line in enumerate(page):
    m = re.match(r"### (\S+) registers? \(offset 0x([0-9A-F]+)", line)
    if m:
        name = (m.group(1), int(m.group(2), 16))
    if line == "| When | A read returns |":
        rows = []
        for row in page[at + 2:]:
            if not row.startswith("|"):
                break
            when, value = row[2:-2].rsplit(" | ", 1)
            rows.append((when, value.strip("`")))
        tables[name[1]] = (name[0], rows)

CLAUSE = {
    "the selected stream exists": lambda s: s["exists"],
    "the selected stream does not exist": lambda s: not s["exists"],
    "no snapshot is running": lambda s: not s["snap"],
    "`STRM_SEL[8]` selects a talker": lambda s: s["dir"],
    "`STRM_SEL[8]` selects a listener": lambda s: not s["dir"],
    "the stream index `STRM_SEL[3:0]` is 0": lambda s: s["idx"] == 0,
    "the stream index `STRM_SEL[3:0]` is not 0": lambda s: s["idx"] != 0,
    "the ACMP table answered since the last selection": lambda s: s["acmp"],
    "the SRP table answered since the last selection": lambda s: s["srp"],
    "`STRM_SEL[9]` selects the listener row at index 0": lambda s: s["ls0"],
    "`STRM_SEL[9]` does not select the listener row at index 0": lambda s: not s["ls0"],
    "the kind the last snapshot recorded for this counter is `SK_RAW_C`": lambda s: s["kind"] == 1,
    "the kind the last snapshot recorded for this counter is `SK_POISON_C`": lambda s: s["kind"] == 2,
    "a channel-map readback has completed": lambda s: s["cmrd"],
    "no channel-map readback has completed": lambda s: not s["cmrd"],
}


def fields(reg, addr, s):
    """What the RTL's own arm returns for a row that prints `the fields above`."""
    if reg == "STRMW_STATE":
        return 0xC0000000
    if reg == "STRMW_PDUS":
        return 0xC000000B
    if reg.startswith("STRMW_CNT"):
        return 0xC0000001 + (addr - 0x830) // 4
    if reg == "STRMW_CTLR_LO":
        return s["ctlr"] & 0xFFFFFFFF
    if reg == "STRMW_CTLR_HI":
        return s["ctlr"] >> 32
    if reg == "STRMW_BIND":
        return s["flags"] << 16 | s["tuid"]
    if reg == "RENDER_STAT":
        return 0x70000000 + s["idx"]
    if reg == "CHMAP_LOOP":
        data = 0x2C5A
        return 1 << 27 | 1 << 26 | 0x2A << 20 | 1 << 19 | ((data >> 13 & 1) & ~(data >> 14 & 1) & 1) << 18 \
            | (data >> 14 & 1) << 17 | (data >> 13 & 1) << 16 | data
    raise KeyError(reg)


def number(reg, addr, value, s):
    """The number a read-value cell names in this state."""
    m = re.fullmatch(r"0x([0-9A-F]+)", value)
    if m:
        return int(m.group(1), 16)
    if value == "the fields above":
        return fields(reg, addr, s)
    return {
        "i_tctx_rd_data": 0x22222222, "i_lctx_rd_data": 0x11111111, "i_lwsrp_status": 0x33333333,
        "{31'd0, aaf_ctrl[0]}": s["aafc"] & 1, "aaf_dmlo": s["dmlo"], "{16'd0, aaf_dmhi[15:0]}": s["dmhi"] & 0xFFFF,
        "{16'd0, i_srp_ctx_rd_stat}": 0x4444, "i_srp_ctx_rd_sid[31:0]": 0x66666666, "i_srp_ctx_rd_sid[63:32]": 0x55555555,
        "acmp_sid_q_r[31:0]": s["sid"] & 0xFFFFFFFF, "acmp_sid_q_r[63:32]": s["sid"] >> 32,
        "acmp_dmac_q_r[31:0]": s["dmac"] & 0xFFFFFFFF, "{16'd0, acmp_dmac_q_r[47:32]}": s["dmac"] >> 32,
        "{mac_wire_w[15:0], 16'd0}": (s["mac"] & 0xFFFF) << 16, "mac_wire_w[47:16]": s["mac"] >> 16,
    }[value]


logf = open(sys.argv[2], encoding="utf-8")
head = logf.readline().split()
hexes = {"addr", "value", "sel", "mac", "sid", "dmac", "ctlr", "flags", "tuid", "aafc", "dmlo", "dmhi"}
reads = bad = 0
hits, bad_by, examples = {}, {}, {}
overlaps = 0
for line in logf:
    s = {k: int(v, 16 if k in hexes else 10) for k, v in zip(head, line.split())}
    addr = s["addr"]
    table = next(((reg, rows) for base, (reg, rows) in tables.items()
                  if base == addr or (reg.startswith("STRMW_CNT") and 0x830 <= addr < 0x858)), None)
    if table is None:
        raise SystemExit(f"no table for {addr:x}")
    reg, rows = table
    true = [r for r in rows if r[0] != "any other case" and all(CLAUSE[c](s) for c in r[0].split(" and "))]
    if not true:
        true = [r for r in rows if r[0] == "any other case"]
    reads += 1
    values = {number(reg, addr, r[1], s) for r in true}
    if len(true) > 1:
        overlaps += 1
    for r in true:
        hits[(reg, r[0])] = hits.get((reg, r[0]), 0) + 1
    if len(true) != 1 and len(values) != 1 or s["value"] not in values:
        bad += 1
        bad_by[reg] = bad_by.get(reg, 0) + 1
        examples.setdefault(reg, (f"sel=0x{s['sel']:03X} snap={s['snap']} acmp={s['acmp']} srp={s['srp']} kind={s['kind']} "
                                  f"cmrd={s['cmrd']} read=0x{s['value']:08X} rows={[(r[0], r[1]) for r in true]}"))
print(f"reads={reads} disagreements={bad} reads_matching_two_rows_same_value={overlaps} listeners={n_l}")
for reg, count in sorted(bad_by.items()):
    print(f"DISAGREE {reg}: {count}; first: {examples[reg]}")
for base, (reg, rows) in sorted(tables.items()):
    for when, value in rows:
        print(f"{reg} 0x{base:03X} hits={hits.get((reg, when), 0):6d} | {when} | {value}")
sys.exit(1 if bad else 0)
