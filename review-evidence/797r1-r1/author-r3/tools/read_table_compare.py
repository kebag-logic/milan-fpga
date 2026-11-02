#!/usr/bin/env python3
"""Read each stream-window read table as printed and compare it with a sweep.
A clause joined by `and` binds tighter than `or`, the ordinary reading.
Usage: read_table_compare.py <page> <sweep log>   exit 1 on any disagreement."""
import re
import sys

page = open(sys.argv[1], encoding="utf-8").read().splitlines()
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
    "a snapshot is running": lambda s: s["snap"],
    "`STRM_SEL[8]` selects a talker": lambda s: s["dir"],
    "`STRM_SEL[8]` selects a listener": lambda s: not s["dir"],
    "the stream index `STRM_SEL[3:0]` is 0": lambda s: s["idx"] == 0,
    "the stream index `STRM_SEL[3:0]` is not 0": lambda s: s["idx"] != 0,
    "the ACMP table answered since the last selection": lambda s: s["acmp"],
    "the ACMP table has not answered since the last selection": lambda s: not s["acmp"],
    "the SRP table answered since the last selection": lambda s: s["srp"],
    "the SRP table has not answered since the last selection": lambda s: not s["srp"],
    "`STRM_SEL[9]` selects the listener row at index 0": lambda s: s["ls0"],
    "`STRM_SEL[9]` does not select the listener row at index 0": lambda s: not s["ls0"],
}


def holds(when, s):
    """The cell as a reader takes it: `and` binds tighter than `or`."""
    if when == "any other case":
        return None
    return any(all(CLAUSE[c](s) for c in part.split(" and ")) for part in when.split(" or "))


def expected(reg, value, s):
    """The number a read-value cell names, in this state."""
    table = {
        "i_tctx_rd_data": 0x22222222, "i_lctx_rd_data": 0x11111111, "i_lwsrp_status": 0x33333333,
        "{31'd0, aaf_ctrl[0]}": 1, "aaf_dmlo": 0x12345678, "{16'd0, aaf_dmhi[15:0]}": 0xABCD,
        "{16'd0, i_srp_ctx_rd_stat}": 0x4444, "i_srp_ctx_rd_sid[31:0]": 0x66666666, "i_srp_ctx_rd_sid[63:32]": 0x55555555,
        "acmp_sid_q_r[31:0]": s["sid"] & 0xFFFFFFFF, "acmp_sid_q_r[63:32]": s["sid"] >> 32,
        "acmp_dmac_q_r[31:0]": s["dmac"] & 0xFFFFFFFF, "{16'd0, acmp_dmac_q_r[47:32]}": s["dmac"] >> 32,
        "{mac_wire_w[15:0], 16'd0}": (s["mac"] & 0xFFFF) << 16, "mac_wire_w[47:16]": s["mac"] >> 16,
    }
    if value == "the fields above":
        return {"STRMW_CTLR_LO": s["ctlr"] & 0xFFFFFFFF, "STRMW_CTLR_HI": s["ctlr"] >> 32,
                "STRMW_BIND": s["flags"] << 16 | s["tuid"]}[reg]
    if value.startswith("0x"):
        return int(value, 16)
    return table[value]


lines = open(sys.argv[2], encoding="utf-8").read().splitlines()
keys = lines[0].split()
wrong = checked = 0
hits = {}
for line in lines[1:]:
    fields = dict(zip(keys, line.split()))
    s = {k: bool(int(fields[k])) for k in ("exists", "snap", "dir", "ls0", "acmp", "srp")}
    s["idx"] = int(fields["idx"])
    for k in ("sid", "dmac", "ctlr", "flags", "tuid", "mac"):
        s[k] = int(fields[k], 16)
    addr, value = int(fields["addr"], 16), int(fields["value"], 16)
    if addr not in tables:
        continue
    reg, rows = tables[addr]
    matched = [r for r in rows if holds(r[0], s)]
    if not matched:
        matched = [r for r in rows if r[0] == "any other case"]
    checked += 1
    for r in matched:
        hits[(addr, r[0])] = hits.get((addr, r[0]), 0) + 1
    note = ""
    said = {expected(reg, r[1], s) for r in matched}
    if len(said) != 1:
        note = f"{len(matched)} rows hold with different values"
    elif value not in said:
        note = f"row `{matched[0][0]}` says 0x{said.pop():08X}"
    if note:
        wrong += 1
        print(f"DISAGREE {reg} 0x{addr:03X} sel=0x{fields['sel']} snap={int(s['snap'])} acmp={int(s['acmp'])} "
              f"srp={int(s['srp'])} read 0x{value:08X}: {note}")
print(f"tables swept: {sorted(hex(a) for a in tables if any(k[0] == a for k in hits))}")
for addr in sorted(tables):
    reg, rows = tables[addr]
    if not any(k[0] == addr for k in hits):
        print(f"not swept: {reg} 0x{addr:03X} ({len(rows)} rows)")
        continue
    for when, value in rows:
        print(f"{reg} 0x{addr:03X} hits={hits.get((addr, when), 0):4d} | {when} | {value}")
print(f"reads checked {checked}, disagreements {wrong}")
raise SystemExit(1 if wrong else 0)
