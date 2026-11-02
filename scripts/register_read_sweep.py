#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Sweep every read table of the register reference against milan_csr (#797).

Why this exists. A read table row on `docs/reference/REGISTER_MAP.md` says
what a read returns when its clauses hold. The generator words each clause
from a flop or a wire, so a check that reads the clause as that flop proves
the generator agrees with itself, not that the printed words are true. This
sweep reads each clause as the page prints it.

What it does:

  * elaborates `hdl/common/csr/milan_csr.sv` alone with Verilator, at the
    parameters the page's "Build parameters" table prints, and at the same
    parameters with two listeners and two talkers;
  * drives the selection, the ACMP and SRP table answers (to a poll and to a
    provisioning write), a running snapshot, the counter kinds and the
    channel-map readback through the block's own ports and registers, and
    reads every word that has a read table;
  * evaluates each row's clauses through CLAUSE, which maps the printed words
    to what the harness did or read back through a register, never to the
    flop the generator worded. A read must equal the value of every row that
    holds, or the "any other case" row when none does.

A clause, value cell or read table this sweep cannot read is a refusal, so a
new wording or a new table cannot pass unswept. The counter kinds and the
latched snapshot words are deposited, the one state the harness sets inside
the block; the clause that reads them names the recorded kind.

Not a gate: it needs Verilator and a C++ compiler.

Usage:
    python3 scripts/register_read_sweep.py
    python3 scripts/register_read_sweep.py --page FILE --work DIR

Exit status: 0 every read agrees, 1 a read disagrees, 2 a refusal or a failed
build.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RTL = "hdl/common/csr/milan_csr.sv"
PAGE = "docs/reference/REGISTER_MAP.md"
CSR_INCLUDE = "hdl/common/csr"
#: The shape headers each build includes; the window decode reads none of them.
SHAPE_INCLUDE = {"ship": "configs/generated/endstation_ax7101_1x1_tdm8",
                 "2x2": "configs/generated/endstation_arty_4x4"}
#: The 2x2 build: two streams each way. SRP_LSN0_ROW_C at N_STREAMS 2 with
#: the CRF source is 2 + 3 - 1 (hdl/milan/milan_datapath.sv, SRP_LSN0_ROW_C).
WIDE = {"N_LISTENERS_P": 2, "N_TALKERS_P": 2, "SRP_LSN0_ROW_P": 4}
#: Selections swept: both directions, indices in and out of range on either build.
INDICES = (0, 1, 2, 3, 15)
#: Distinct constants driven on the read-data inputs, by the name a value cell prints.
DRIVEN = {"i_lctx_rd_data": 0x11111111, "i_tctx_rd_data": 0x22222222, "i_lwsrp_status": 0x33333333,
          "i_srp_ctx_rd_stat": 0x4444, "i_srp_ctx_rd_sid": 0x5555555566666666,
          "aaf_ctrl": 0x00000001, "aaf_dmlo": 0x12345678, "aaf_dmhi": 0x0000ABCD,
          "i_chmap_rd_data": 0x2ABC, "render": 0x70000000, "shadow": 0x5A000000}

State = dict[str, int]
#: The state columns of a harness log line, as numbers.
LOGGED = ("sel9", "dir", "idx", "acmp", "srp", "srpw", "srppoll", "snap", "word", "cmdone", "cmvalid",
          "cmside", "cmaddr", "cmdata")

#: Each printed clause, read as the page states it, over what the harness did
#: or read back. `sel9` is the last bit 9 written: STRM_SEL[9] is a write-only
#: field that reads 0. `snap` is STRM_SNAP[0] as read before the reads.
CLAUSE: dict[str, Callable[[State], bool]] = {
    "the selected stream exists": lambda s: s["exists"] == 1,
    "the selected stream does not exist": lambda s: s["exists"] == 0,
    "a snapshot is running": lambda s: s["snap"] == 1,
    "no snapshot is running": lambda s: s["snap"] == 0,
    "`STRM_SEL[8]` selects a talker": lambda s: s["dir"] == 1,
    "`STRM_SEL[8]` selects a listener": lambda s: s["dir"] == 0,
    "the stream index `STRM_SEL[3:0]` is 0": lambda s: s["idx"] == 0,
    "the stream index `STRM_SEL[3:0]` is not 0": lambda s: s["idx"] != 0,
    "the ACMP table answered since the last selection": lambda s: s["acmp"] == 1,
    "the ACMP table has not answered since the last selection": lambda s: s["acmp"] == 0,
    "the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write":
        lambda s: s["srppoll"] == 1,
    "the SRP table has not answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write":
        lambda s: s["srppoll"] == 0,
    "`STRM_SEL[9]` is 1": lambda s: s["sel9"] == 1,
    "`STRM_SEL[9]` is 0": lambda s: s["sel9"] == 0,
    "the kind the last snapshot recorded for this counter is `SK_RAW_C`": lambda s: s["kind"] == s["SK_RAW_C"],
    "the kind the last snapshot recorded for this counter is `SK_POISON_C`": lambda s: s["kind"] == s["SK_POISON_C"],
    "the kind the last snapshot recorded for this counter is `SK_ZERO_C`": lambda s: s["kind"] == s["SK_ZERO_C"],
    # CHMAP_SNAP[1] as the harness read it just before CHMAP_LOOP.
    "`CHMAP_SNAP[1]` is 1": lambda s: s["cmvalid"] == 1,
    "`CHMAP_SNAP[1]` is 0": lambda s: s["cmvalid"] == 0,
}


class Refusal(Exception):
    """The sweep cannot read something the page prints."""


# ------------------------------------------------------------------ the page --
def read_tables(page: list[str]) -> dict[int, tuple[str, list[tuple[str, str]]]]:
    """Every `| When | A read returns |` table, by each word address it covers."""
    tables: dict[int, tuple[str, list[tuple[str, str]]]] = {}
    head = None
    for at, line in enumerate(page):
        m = re.match(r"### (\S+) registers? \(offset 0x([0-9A-F]+)(?: to 0x([0-9A-F]+), stride 0x([0-9A-F]+))?", line)
        if m:
            head = m.groups()
        if line != "| When | A read returns |":
            continue
        if head is None:
            raise Refusal(f"{PAGE}:{at + 1}: a read table under no register heading")
        rows = []
        for row in page[at + 2:]:
            if not row.startswith("|"):
                break
            when, value = row[2:-2].rsplit(" | ", 1)
            rows.append((when, value))
        first = int(head[1], 16)
        last = int(head[2], 16) if head[2] else first
        step = int(head[3], 16) if head[3] else 4
        for addr in range(first, last + 1, step):
            tables[addr] = (head[0], rows)
    return tables


def build_parameters(page: list[str]) -> dict[str, int]:
    """The `Build parameters` table: the values the shipping build elaborates."""
    out: dict[str, int] = {}
    start = page.index("## Build parameters")
    for line in page[start:]:
        m = re.match(r"\| `(\w+)` \| [^|]+ \| ([\d,]+) \|$", line)
        if m:
            out[m.group(1)] = int(m.group(2).replace(",", ""))
        elif out and not line.startswith("|"):
            break
    if "N_LISTENERS_P" not in out:
        raise Refusal(f"{PAGE}: no Build parameters table")
    return out


def holds(when: str, s: State) -> bool | None:
    """A When cell as printed: one conjunction; None for the fallback row."""
    if when == "any other case":
        return None
    if when == "every case":
        return True
    for clause in when.split(" and "):
        if clause not in CLAUSE:
            raise Refusal(f"{PAGE}: the clause '{clause}' has no reading in CLAUSE")
    return all(CLAUSE[c](s) for c in when.split(" and "))


def field(word: int, lo: int, width: int) -> int:
    """`width` bits of `word` from bit `lo`."""
    return word >> lo & ((1 << width) - 1)


def fields_above(reg: str, s: State, k: dict[str, int]) -> int:
    """What a register's field table names, from what the harness drove."""
    ctx = s["ctx"]
    if reg == "STRMW_CTLR_LO":
        return field(ctx, k["ACMP_CTX_CTLR_LO_C"], 32)
    if reg == "STRMW_CTLR_HI":
        return field(ctx, k["ACMP_CTX_CTLR_LO_C"] + 32, 32)
    if reg == "STRMW_BIND":
        return field(ctx, k["ACMP_CTX_FLAGS_LO_C"], 16) << 16 | field(ctx, k["ACMP_CTX_TUID_LO_C"], 16)
    if reg in ("STRMW_STATE", "STRMW_PDUS", "STRMW_CNTn"):
        return DRIVEN["shadow"] + s["word"]
    if reg == "RENDER_STAT":
        return DRIVEN["render"] + s["idx"]
    if reg == "CHMAP_LOOP":
        side, addr, data = s["cmside"], s["cmaddr"], s["cmdata"]
        fed, mapped = data >> 14 & 1, data >> 13 & 1
        return (side << 27 | 1 << 26 | addr << 20 | side << 19 | (mapped & ~fed & 1) << 18
                | fed << 17 | mapped << 16 | data)
    raise Refusal(f"{PAGE}: {reg} prints 'the fields above' and the sweep has no reading of its fields")


def value_of(reg: str, cell: str, s: State, k: dict[str, int]) -> int:
    """The number a value cell names, in this state."""
    if cell == "the fields above":
        return fields_above(reg, s, k)
    text = cell.strip("`")
    if text.startswith("0x"):
        return int(text, 16)
    ctx, mac = s["ctx"], s["mac"]
    sid, dmac = field(ctx, k["ACMP_CTX_SID_LO_C"], 64), field(ctx, k["ACMP_CTX_DMAC_LO_C"], 48)
    known = {
        "i_lctx_rd_data": DRIVEN["i_lctx_rd_data"], "i_tctx_rd_data": DRIVEN["i_tctx_rd_data"],
        "i_lwsrp_status": DRIVEN["i_lwsrp_status"], "{16'd0, i_srp_ctx_rd_stat}": DRIVEN["i_srp_ctx_rd_stat"],
        "i_srp_ctx_rd_sid[31:0]": field(DRIVEN["i_srp_ctx_rd_sid"], 0, 32),
        "i_srp_ctx_rd_sid[63:32]": field(DRIVEN["i_srp_ctx_rd_sid"], 32, 32),
        "{31'd0, aaf_ctrl[0]}": DRIVEN["aaf_ctrl"] & 1, "aaf_dmlo": DRIVEN["aaf_dmlo"],
        "{16'd0, aaf_dmhi[15:0]}": DRIVEN["aaf_dmhi"] & 0xFFFF,
        "acmp_sid_q_r[31:0]": field(sid, 0, 32), "acmp_sid_q_r[63:32]": field(sid, 32, 32),
        "acmp_dmac_q_r[31:0]": field(dmac, 0, 32), "{16'd0, acmp_dmac_q_r[47:32]}": field(dmac, 32, 16),
        "{mac_wire_w[15:0], 16'd0}": field(mac, 0, 16) << 16, "mac_wire_w[47:16]": field(mac, 16, 32),
    }
    if text not in known:
        raise Refusal(f"{PAGE}: {reg} prints the value {cell}, which the sweep cannot evaluate")
    return known[text]


# --------------------------------------------------------------- the harness --
HARNESS = r'''#include "Vmilan_csr.h"
#include "Vmilan_csr___024root.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
static Vmilan_csr* t;
template <class T> static void setv(T& v, int on) { v = on; }
template <std::size_t N> static void setv(VlWide<N>& v, int on) { for (std::size_t i = 0; i < N; i++) v[i] = on; }
static void put32(CData& v, int, uint32_t x) { v = x; }
static void put32(SData& v, int, uint32_t x) { v = x; }
static void put32(IData& v, int, uint32_t x) { v = x; }
static void put32(QData& v, int s, uint32_t x) { v &= ~(0xFFFFFFFFULL << (32 * s)); v |= (uint64_t)x << (32 * s); }
template <std::size_t N> static void put32(VlWide<N>& v, int s, uint32_t x) { v[s] = x; }
static void tick() { t->aclk = 0; t->eval(); t->aclk = 1; t->eval(); t->aclk = 0; t->eval(); }
static void ticks(int n) { for (int i = 0; i < n; i++) tick(); }
static uint32_t rd(uint32_t a) {
  t->s_axi_araddr = a; t->s_axi_arvalid = 1; t->s_axi_rready = 0; int g = 0; t->eval();
  while (!t->s_axi_arready) { tick(); if (++g > 4000) { printf("FAIL ar %x\n", a); exit(2); } }
  tick(); t->s_axi_arvalid = 0; t->eval(); g = 0;
  while (!t->s_axi_rvalid) { tick(); if (++g > 4000) { printf("FAIL r %x\n", a); exit(2); } }
  uint32_t v = t->s_axi_rdata; t->s_axi_rready = 1; t->eval(); tick(); t->s_axi_rready = 0; t->eval(); tick();
  return v;
}
static void wr(uint32_t a, uint32_t d) {
  t->s_axi_awaddr = a; t->s_axi_wdata = d; t->s_axi_wstrb = 0xF; t->s_axi_awvalid = 1; t->s_axi_wvalid = 1;
  t->s_axi_bready = 1; int g = 0; t->eval();
  while (!t->s_axi_awready) { tick(); if (++g > 4000) { printf("FAIL aw %x\n", a); exit(2); } }
  tick(); t->s_axi_awvalid = 0; t->s_axi_wvalid = 0; t->eval(); ticks(4);
}
// One answer from a table, only while the block asks: the engines' contract.
static int answer_acmp() {
  ticks(2); if (!t->o_acmp_tbl_req) return 0;
  t->i_acmp_tbl_gnt = 1; tick(); t->i_acmp_tbl_gnt = 0; ticks(2); return 1;
}
static int answer_srp() {
  ticks(2); if (!t->o_srp_ctx_req) return 0;
  t->i_srp_ctx_gnt = 1; tick(); t->i_srp_ctx_gnt = 0; ticks(2); return 1;
}
static const uint32_t WORDS[] = {@WORDS@};
static const int KINDS[3] = {@SK_ZERO_C@, @SK_RAW_C@, @SK_POISON_C@};
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv); t = new Vmilan_csr; auto* r = t->rootp;
  t->s_axi_awvalid = 0; t->s_axi_wvalid = 0; t->s_axi_arvalid = 0; t->s_axi_bready = 1; t->s_axi_rready = 0;
@INIT@
  for (int i = 0; i < (int)(sizeof(t->i_acmp_tbl_ctx) / 4); i++) t->i_acmp_tbl_ctx[i] = 0xA5000000u + 0x01010101u * i;
  printf("ctxwords %d\n", (int)(sizeof(t->i_acmp_tbl_ctx) / 4));
  t->i_lctx_rd_data = @i_lctx_rd_data@u; t->i_tctx_rd_data = @i_tctx_rd_data@u; t->i_lwsrp_status = @i_lwsrp_status@u;
  t->i_srp_ctx_rd_stat = @i_srp_ctx_rd_stat@u; t->i_srp_ctx_rd_sid = @i_srp_ctx_rd_sid@ULL;
  for (int s = 0; s < @N_LISTENERS_P@; s++) put32(t->i_render_status, s, @render@u + s);
  t->i_chmap_rd_data = @i_chmap_rd_data@u;
  t->aresetn = 0; ticks(8); t->aresetn = 1; ticks(530);
  wr(0x654, @aaf_ctrl@u); wr(0x658, @aaf_dmlo@u); wr(0x65C, @aaf_dmhi@u);
  printf("addr value sel9 dir idx acmp srp srpw srppoll snap kinds word mac cmdone cmvalid cmside cmaddr cmdata\n");
  // Channel-map readback: never, answered, re-armed in flight, timed out, answered.
  int cmdone = 0, cmside = 0, cmaddr = 0;
  auto loop_read = [&]() {
    uint32_t st = rd(0x910), v = rd(0x914);
    printf("914 %08x 0 0 0 0 0 0 0 0 0000000000 0 %012llx %d %u %d %d %d\n", v,
           (unsigned long long)r->milan_csr__DOT__mac_wire_w, cmdone, st >> 1 & 1, cmside, cmaddr,
           @i_chmap_rd_data@);
  };
  auto arm = [&](int side, int addr, int answer) {
    wr(0x904, (side << 8) | addr); wr(0x910, 1);
    if (!answer) return;
    int g = 0; while (!t->o_chmap_rd_en && ++g < 100) tick();
    tick(); t->i_chmap_rd_valid = 1; tick(); t->i_chmap_rd_valid = 0; ticks(4);
    cmdone = 1; cmside = side; cmaddr = addr;
  };
  loop_read();
  arm(1, 0x2A, 1); loop_read();
  wr(0x904, 0x005); wr(0x910, 1); loop_read();
  ticks(64); loop_read();
  arm(0, 0x11, 1); loop_read();
  arm(1, 0x03, 0); loop_read();
  ticks(64); loop_read();
  // Stream window: selection, table answers, snapshot, counter kinds.
  for (int sel9 = 0; sel9 < 2; sel9++) for (int dir = 0; dir < 2; dir++)
  for (int ii = 0; ii < @N_INDICES@; ii++) for (int acmp = 0; acmp < 2; acmp++)
  for (int srpmode = 0; srpmode < 4; srpmode++) for (int snap = 0; snap < 2; snap++)
  for (int ks = 0; ks < 3; ks++) {
    static const int IDX[] = {@INDICES@};
    int idx = IDX[ii];
    t->i_lctx_snap_ok = 1; t->i_tctx_snap_ok = 1; ticks(2);
    uint32_t sel = (sel9 << 9) | (dir << 8) | idx;
    wr(0x800, sel); ticks(4);
    int acmp_ans = acmp ? answer_acmp() : 0;
    // srp: the table answered since the selection; srpw: it answered a
    // provisioning write; srppoll: a poll answer is the latest answer, after
    // the selection and after any STRMW_CTRL write.
    int srp_ans = 0, srpw = 0, srppoll = 0;
    if (srpmode == 1) srppoll = srp_ans = answer_srp();
    if (srpmode >= 2) {
      wr(0x810, @aaf_ctrl@u); srpw = t->o_srp_ctx_we;
      if (srpw) srp_ans = answer_srp();
      if (srpmode == 3) { srppoll = answer_srp(); srp_ans |= srppoll; }
    }
    if (snap) { t->i_lctx_snap_ok = 0; t->i_tctx_snap_ok = 0; wr(0x804, 1); ticks(8); }
    char kinds[11];
    for (int n = 0; n < 10; n++) {
      int k = KINDS[(n + ks) % 3];
      r->milan_csr__DOT__snap_kind_r[1 + n] = k; kinds[n] = '0' + k;
    }
    kinds[10] = 0;
    for (int w = 0; w < 12; w++) r->milan_csr__DOT__snap_shadow_r[w] = @shadow@u + w;
    t->eval();
    uint32_t busy = rd(0x804) & 1;
    for (uint32_t a : WORDS) {
      uint32_t v = rd(a);
      int word = a == 0x82C ? 0 : a == 0x858 ? 11 : (a >= 0x830 && a < 0x858) ? 1 + (int)((a - 0x830) / 4) : 0;
      printf("%x %08x %d %d %d %d %d %d %d %u %s %d %012llx 0 0 0 0 0\n", a, v, sel9, dir, idx, acmp_ans,
             srp_ans, srpw, srppoll, busy, kinds, word, (unsigned long long)r->milan_csr__DOT__mac_wire_w);
    }
    uint32_t after = rd(0x804) & 1, back = rd(0x800);
    if (after != busy) { printf("FAIL snapshot state moved during the reads at sel %03x\n", sel); return 2; }
    if (back != (sel & 0x10F)) { printf("FAIL STRM_SEL reads %08x after writing %03x\n", back, sel); return 2; }
    t->i_lctx_snap_ok = 1; t->i_tctx_snap_ok = 1; int g = 0;
    while ((rd(0x804) & 1) && ++g < 400) ticks(8);
    ticks(4);
  }
  delete t; return 0;
}
'''

#: Inputs held high: the engines' ready and valid answers.
HIGH = {"i_lctx_rd_valid", "i_tctx_rd_valid", "i_lctx_wr_rdy", "i_tctx_wr_rdy", "i_lctx_snap_ok", "i_tctx_snap_ok"}
#: Inputs the harness drives itself.
OWN = {"aclk", "aresetn", "s_axi_awaddr", "s_axi_awvalid", "s_axi_wdata", "s_axi_wstrb", "s_axi_wvalid",
       "s_axi_bready", "s_axi_araddr", "s_axi_arvalid", "s_axi_rready", "i_acmp_tbl_ctx", "i_render_status"}


def rtl_constants(text: str) -> dict[str, int]:
    """The localparams the expected values and the kinds need."""
    out = {}
    for name in ("ACMP_CTX_CTLR_LO_C", "ACMP_CTX_SID_LO_C", "ACMP_CTX_DMAC_LO_C", "ACMP_CTX_FLAGS_LO_C",
                 "ACMP_CTX_TUID_LO_C", "SK_ZERO_C", "SK_RAW_C", "SK_POISON_C"):
        m = re.search(rf"\b{name}\s*=\s*(?:\d+'d)?(\d+)", text)
        if not m:
            raise Refusal(f"{RTL}: no constant {name}")
        out[name] = int(m.group(1))
    return out


def harness(text: str, words: list[int], params: dict[str, int], k: dict[str, int]) -> str:
    """The C++ harness for one build, its inputs read from the module header."""
    bare = re.sub(r"/\*.*?\*/", "", re.sub(r"//.*", "", text), flags=re.S)
    header = bare[bare.index("module milan_csr"):]
    header = header[:header.index(");\n")]
    ports = re.findall(r"\binput\s+wire\s*(?:\[[^\]]+\])?\s*(\w+)", header)
    init = "\n".join(f"  setv(t->{p}, {int(p in HIGH)});" for p in ports if p not in OWN)
    code = HARNESS.replace("@INIT@", init).replace("@WORDS@", ", ".join(f"0x{a:03X}" for a in words))
    code = code.replace("@INDICES@", ", ".join(map(str, INDICES))).replace("@N_INDICES@", str(len(INDICES)))
    code = code.replace("@N_LISTENERS_P@", str(params["N_LISTENERS_P"]))
    for name, value in DRIVEN.items():
        code = code.replace(f"@{name}@", f"0x{value:X}")
    for name in ("SK_ZERO_C", "SK_RAW_C", "SK_POISON_C"):
        code = code.replace(f"@{name}@", str(k[name]))
    return code


def build_and_run(shape: str, params: dict[str, int], code: str, work: Path) -> list[str]:
    """Build one shape with Verilator and return its log lines."""
    obj = work / shape
    obj.mkdir(parents=True, exist_ok=True)
    (obj / "sweep.cpp").write_text(code, encoding="utf-8")
    cmd = ["verilator", "--cc", "--exe", "--build", "-j", "8", "-O2", "-Wno-fatal", "-Wno-lint", "-Wno-style",
           "--public-flat-rw", "--top-module", "milan_csr", f"+incdir+{ROOT / CSR_INCLUDE}",
           f"+incdir+{ROOT / SHAPE_INCLUDE[shape]}", "--Mdir", str(obj / "obj"), "-o", "Vsweep",
           *[f"-G{name}={value}" for name, value in params.items()],
           str(ROOT / RTL), str(obj / "sweep.cpp")]
    built = subprocess.run(cmd, capture_output=True, text=True, check=False)
    (obj / "build.log").write_text(built.stdout + built.stderr, encoding="utf-8")
    if built.returncode:
        raise Refusal(f"{shape}: the Verilator build failed, see {obj / 'build.log'}")
    ran = subprocess.run([str(obj / "obj" / "Vsweep")], capture_output=True, text=True, check=False)
    (obj / "sweep.log").write_text(ran.stdout, encoding="utf-8")
    if ran.returncode:
        raise Refusal(f"{shape}: the harness stopped: {ran.stdout.splitlines()[-1:]}")
    return ran.stdout.splitlines()


# --------------------------------------------------------------- the compare --
def compare(shape: str, lines: list[str], tables: dict, params: dict[str, int], k: dict[str, int]) -> int:
    """Check every read in one log against the page; print per-table counts."""
    ctxwords = int(lines[0].split()[1])
    ctx = sum((0xA5000000 + 0x01010101 * i) % (1 << 32) << (32 * i) for i in range(ctxwords))
    keys = lines[1].split()
    reads: dict[str, int] = {}
    wrong: dict[str, int] = {}
    hits: dict[tuple[str, str], int] = {}
    for line in lines[2:]:
        got = dict(zip(keys, line.split()))
        addr, value = int(got["addr"], 16), int(got["value"], 16)
        reg, rows = tables[addr]
        s: State = {name: int(got[name]) for name in LOGGED}
        count = params["N_TALKERS_P"] if s["dir"] else params["N_LISTENERS_P"]
        s["exists"] = int(s["idx"] < count)
        s["kind"] = int(got["kinds"][s["word"] - 1]) if reg == "STRMW_CNTn" else -1
        s["ctx"], s["mac"] = ctx, int(got["mac"], 16)
        s.update(k)
        matched = [row for row in rows if holds(row[0], s)]
        if not matched:
            matched = [row for row in rows if row[0] == "any other case"]
        reads[reg] = reads.get(reg, 0) + 1
        for row in matched:
            hits[(reg, row[0])] = hits.get((reg, row[0]), 0) + 1
        said = {value_of(reg, row[1], s, k) for row in matched}
        note = ""
        if not matched:
            note = "no row holds"
        elif len(said) != 1:
            note = f"{len(matched)} rows hold with different values"
        elif value not in said:
            note = f"row '{matched[0][0]}' says 0x{said.pop():08X}"
        if note:
            wrong[reg] = wrong.get(reg, 0) + 1
            state = " ".join(f"{name}={got[name]}" for name in LOGGED[:-3])
            print(f"DISAGREE {shape} {reg} 0x{addr:03X} {state} read 0x{value:08X}: {note}")
    seen = {reg for reg, _ in tables.values()}
    for reg in sorted(seen - set(reads)):
        raise Refusal(f"{shape}: the read table of {reg} was not swept")
    print(f"{shape}: table, reads, disagreements")
    for reg in sorted(seen, key=lambda r: min(a for a, t in tables.items() if t[0] == r)):
        print(f"  {reg} {reads[reg]} {wrong.get(reg, 0)}")
        rows = next(t[1] for t in tables.values() if t[0] == reg)
        for when, cell in rows:
            print(f"    hits={hits.get((reg, when), 0):5d} | {when} | {cell}")
    total = sum(wrong.values())
    print(f"{shape}: {len(seen)} tables, {sum(reads.values())} reads, {total} disagreements")
    return total


def main() -> int:
    """Sweep both builds against the page; the exit status is the verdict."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--page", default=str(ROOT / PAGE), help="the page whose read tables are swept")
    parser.add_argument("--work", help="build directory; a temporary one by default")
    args = parser.parse_args()
    try:
        page = Path(args.page).read_text(encoding="utf-8").splitlines()
        tables = read_tables(page)
        text = (ROOT / RTL).read_text(encoding="utf-8")
        k = rtl_constants(text)
        ship = build_parameters(page)
        words = sorted(a for a in tables if a != 0x914)
        with tempfile.TemporaryDirectory() as scratch:
            work = Path(args.work or scratch)
            total = 0
            for shape, params in (("ship", ship), ("2x2", {**ship, **WIDE})):
                lines = build_and_run(shape, params, harness(text, words, params, k), work)
                total += compare(shape, lines, tables, params, k)
    except Refusal as refusal:
        print(f"register_read_sweep: REFUSED: {refusal}")
        return 2
    print(f"register_read_sweep: {total} disagreement(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
