#!/usr/bin/env python3
"""Read every read table as printed and compare it with a sweep log.
Usage: compare_sweep.py <page> <log> <reader|flag>
flag: `STRM_SEL[9]` selects the listener row at index 0 means the RTL flop only.
reader: that clause means what the STRM_LSN0 row says, bit 9 set with bit 8 at 0.
Exit 1 on any disagreement."""
import re, sys
page = open(sys.argv[1], encoding="utf-8").read().splitlines()
mode = sys.argv[3]
tables, name = {}, None
for at, line in enumerate(page):
    m = re.match(r"### (\S+) registers? \(offset 0x([0-9A-F]+)( to 0x([0-9A-F]+))?", line)
    if m:
        name = (m.group(1), int(m.group(2), 16), int(m.group(4), 16) if m.group(4) else int(m.group(2), 16))
    if line == "| When | A read returns |":
        rows = []
        for row in page[at + 2:]:
            if not row.startswith("|"):
                break
            when, value = row[2:-2].rsplit(" | ", 1)
            rows.append((when, value.strip("`")))
        for a in range(name[1], name[2] + 1, 4):
            tables[a] = (name[0], rows)
def listener_row(s):
    return s["ls0"] if mode == "flag" else (s["ls0"] and not s["dir"])
K = "the kind the last snapshot recorded for this counter is"
CLAUSE = {
    "the selected stream exists": lambda s: s["exists"], "the selected stream does not exist": lambda s: not s["exists"],
    "no snapshot is running": lambda s: not s["snap"], "a snapshot is running": lambda s: s["snap"],
    "`STRM_SEL[8]` selects a talker": lambda s: s["dir"], "`STRM_SEL[8]` selects a listener": lambda s: not s["dir"],
    "the stream index `STRM_SEL[3:0]` is 0": lambda s: s["idx"] == 0, "the stream index `STRM_SEL[3:0]` is not 0": lambda s: s["idx"] != 0,
    "the ACMP table answered since the last selection": lambda s: s["acmp"],
    "the ACMP table has not answered since the last selection": lambda s: not s["acmp"],
    "the SRP table answered since the last selection": lambda s: s["srp"],
    "the SRP table has not answered since the last selection": lambda s: not s["srp"],
    "`STRM_SEL[9]` selects the listener row at index 0": listener_row,
    "`STRM_SEL[9]` does not select the listener row at index 0": lambda s: not listener_row(s),
    "a channel-map readback has completed": lambda s: s["cm"], "no channel-map readback has completed": lambda s: not s["cm"],
    f"{K} `SK_RAW_C`": lambda s: s["kind"] == 1, f"{K} not `SK_RAW_C`": lambda s: s["kind"] != 1,
    f"{K} `SK_POISON_C`": lambda s: s["kind"] == 2, f"{K} not `SK_POISON_C`": lambda s: s["kind"] != 2,
    "every case": lambda s: True,
}
def holds(when, s):
    if when == "any other case":
        return None
    return any(all(CLAUSE[c](s) for c in part.split(" and ")) for part in when.split(" or "))
def expected(reg, addr, value, s, v):
    sid, dmac, ctlr, mac = s["sid"], s["dmac"], s["ctlr"], s["mac"]
    table = {"i_tctx_rd_data": 0x22222222, "i_lctx_rd_data": 0x11111111, "i_lwsrp_status": 0x33333333,
             "{31'd0, aaf_ctrl[0]}": 1, "aaf_dmlo": 0x12345678, "{16'd0, aaf_dmhi[15:0]}": 0xABCD,
             "{16'd0, i_srp_ctx_rd_stat}": 0x4444, "i_srp_ctx_rd_sid[31:0]": 0x66666666, "i_srp_ctx_rd_sid[63:32]": 0x55555555,
             "acmp_sid_q_r[31:0]": sid & 0xFFFFFFFF, "acmp_sid_q_r[63:32]": sid >> 32,
             "acmp_dmac_q_r[31:0]": dmac & 0xFFFFFFFF, "{16'd0, acmp_dmac_q_r[47:32]}": dmac >> 32,
             "{mac_wire_w[15:0], 16'd0}": (mac & 0xFFFF) << 16, "mac_wire_w[47:16]": mac >> 16}
    if value == "the fields above":
        if reg in ("STRMW_STATE", "STRMW_PDUS", "STRMW_CNTn"):
            return s["shadow"]
        if reg == "STRMW_CTLR_LO":
            return ctlr & 0xFFFFFFFF
        if reg == "STRMW_CTLR_HI":
            return ctlr >> 32
        if reg == "STRMW_BIND":
            return s["flags"] << 16 | s["tuid"]
        if reg == "RENDER_STAT":
            return 0x77000000 + s["idx"]
        if reg == "CHMAP_LOOP":
            return v if (v >> 26 & 1) and not v >> 28 else None
        raise SystemExit(f"no value for {reg}")
    return int(value, 16) if value.startswith("0x") else table[value]
lines = open(sys.argv[2], encoding="utf-8").read().splitlines()
keys = lines[0].split()
wrong = checked = moved = 0
hits, bad = {}, {}
for line in lines[1:]:
    if line.endswith("MOVED"):
        moved += 1
        continue
    f = dict(zip(keys, line.split()))
    s = {k: bool(int(f[k])) for k in ("exists", "snap", "dir", "ls0", "acmp", "srp", "cm")}
    s["idx"], s["kind"] = int(f["idx"]), int(f["kind"])
    for k in ("sid", "dmac", "ctlr", "flags", "tuid", "mac", "shadow"):
        s[k] = int(f[k], 16)
    addr, v = int(f["addr"], 16), int(f["value"], 16)
    if addr not in tables:
        continue
    reg, rows = tables[addr]
    matched = [r for r in rows if holds(r[0], s)] or [r for r in rows if r[0] == "any other case"]
    checked += 1
    for r in matched:
        hits[(reg, r[0], r[1])] = hits.get((reg, r[0], r[1]), 0) + 1
    said = {expected(reg, addr, r[1], s, v) for r in matched}
    note = ""
    if len(said) != 1:
        note = f"{len(matched)} rows hold with different values"
    elif v not in said:
        note = f"row `{matched[0][0]}` says {matched[0][1]}"
    if note:
        wrong += 1
        key = (reg, f"sel=0x{f['sel']}", int(s["exists"]), int(s["snap"]), int(s["acmp"]), int(s["srp"]))
        bad.setdefault(key, (f"read 0x{v:08X}: {note}", 0))
        bad[key] = (bad[key][0], bad[key][1] + 1)
for k, (msg, n) in sorted(bad.items()):
    print(f"DISAGREE {k[0]} {k[1]} exists={k[2]} snap={k[3]} acmp={k[4]} srp={k[5]} x{n} {msg}")
seen = []
for a in sorted(tables):
    reg, rows = tables[a]
    if reg in seen:
        continue
    seen.append(reg)
    for when, value in rows:
        print(f"{reg} hits={hits.get((reg, when, value), 0):6d} | {when} | {value}")
print(f"tables {len(seen)}, reads checked {checked}, reads dropped because state moved {moved}, disagreements {wrong}")
raise SystemExit(1 if wrong else 0)
