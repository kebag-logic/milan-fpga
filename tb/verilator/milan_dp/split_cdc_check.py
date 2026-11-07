#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""split_cdc_check.py - every crossing of KL_mbx_cdc goes through an approved primitive (#665 F-INT PR 2).

CONTRIBUTING.md section 1 allows a clock-domain crossing only through
cdc_pulse, cdc_handshake or toggle+sync. A simulation cannot see a crossing
that skips them: a raw wire crosses in Verilator as well as a handshake does.
This check reads the structure instead.

THE NETLIST. sv2v lowers KL_mbx_cdc and KL_mbx_cdc_window, and Yosys
elaborates them with cdc_handshake and cdc_pulse read as blackboxes, so each
primitive stays a cell with port directions. ``proc`` and ``flatten`` turn the
rest into flops and combinational cells.

THE DOMAINS. A flop is in the domain of the clock its CLK reads: sys_clk_i is
the mailbox's, dp_clk_i the datapath's. A port is in the domain its name
gives: m_* the mailbox's, d_* the datapath's. A primitive's outputs are in its
destination clock's domain (dest_out, dest_req, dest_pulse) or its source's
(src_rcv).

THE RULE. Every flop's inputs, every output port and every primitive's source
inputs (src_in, src_send, src_pulse) must read, through combinational cells
alone, only sources of their own domain. One reading is allowed by name: the
settings capture, whose flops ``fw_r`` take the m_fw_* bus KL_mbx holds from
its commit until its acknowledgement, enabled by u_fw_req's dest_pulse. Any
other reading across the two domains is a crossing without a primitive.

    python3 split_cdc_check.py              # the tracked sources
    python3 split_cdc_check.py --selftest   # and four plants, each refused

The tally line is ``checks: N   failures: M``.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PKG = ROOT / "hdl/milan/mailbox/KL_mbx_pkg.sv"
CDC = ROOT / "hdl/milan/mailbox/KL_mbx_cdc.sv"
WIN = ROOT / "hdl/milan/mailbox/KL_mbx_cdc_window.sv"
PRIMS = (ROOT / "hdl/common/cdc_handshake.sv", ROOT / "hdl/common/cdc_pulse.sv")
TOP = "KL_mbx_cdc"
CLOCKS = {"sys_clk_i": "sys", "dp_clk_i": "dp"}
#: a primitive's clock ports, and the domain each of its ports is in
PRIM_CLOCKS = {"cdc_handshake": ("src_clk", "dest_clk"), "cdc_pulse": ("src_clk", "dest_clk")}
SRC_SIDE = {"src_in", "src_send", "src_pulse", "src_rcv", "src_rst_n"}
#: the one reading across the domains this design is allowed: the held settings bus
HELD = ("fw_r", "m_fw_")


def netlist(cdc: Path, win: Path, work: Path) -> dict:
    """KL_mbx_cdc's flattened netlist, the primitives kept as cells."""
    top = subprocess.run(["sv2v", str(PKG), str(win), str(cdc)], capture_output=True, text=True, check=True).stdout
    lib = subprocess.run(["sv2v", *map(str, PRIMS)], capture_output=True, text=True, check=True).stdout
    (work / "top.v").write_text(top)
    (work / "lib.v").write_text(lib)
    subprocess.run(["yosys", "-q", "-p", f"read_verilog -lib {work / 'lib.v'}; read_verilog {work / 'top.v'}; "
                    f"hierarchy -check -top {TOP}; proc; flatten; opt_clean; write_json {work / 'net.json'}"],
                   check=True, capture_output=True, text=True)
    return json.loads((work / "net.json").read_text())["modules"][TOP]


def findings(mod: dict) -> tuple[int, list[str]]:
    """(sinks checked, every crossing without a primitive)."""
    names, aliases, driver = {}, defaultdict(set), {}
    for n, v in mod["netnames"].items():
        for b in v["bits"]:
            if isinstance(b, int):
                aliases[b].add(n)
                if b not in names or "$" in names[b]:
                    names[b] = n
    for p, v in mod["ports"].items():
        if v["direction"] == "input":
            for b in v["bits"]:
                driver[b] = ("in", p)
    clock_bit = {mod["ports"][c]["bits"][0]: d for c, d in CLOCKS.items()}
    flop_dom, prim_dom = {}, {}
    for n, c in mod["cells"].items():
        dirs = c.get("port_directions", {})
        if "CLK" in c["connections"]:
            flop_dom[n] = clock_bit.get(c["connections"]["CLK"][0], "?")
        elif c["type"] in PRIM_CLOCKS:
            s, d = (clock_bit.get(c["connections"][k][0], "?") for k in PRIM_CLOCKS[c["type"]])
            prim_dom[n] = (s, d)
        for p, bits in c["connections"].items():
            if dirs.get(p) == "output":
                for b in bits:
                    if isinstance(b, int):
                        driver[b] = (n, p)

    def domain_of(src: tuple[str, str]) -> str | None:
        n, p = src
        if n == "in":
            return CLOCKS.get(p, "sys" if p.startswith(("m_", "sys_")) else "dp" if p.startswith(("d_", "dp_")) else "?")
        if n in flop_dom:
            return flop_dom[n]
        if n in prim_dom:
            return prim_dom[n][0] if p in SRC_SIDE else prim_dom[n][1]
        return None

    memo: dict[int, frozenset] = {}

    def sources(bit) -> frozenset:
        """The (cell, port) sources a bit reads through combinational cells alone."""
        if not isinstance(bit, int):
            return frozenset()
        if bit in memo:
            return memo[bit]
        memo[bit] = frozenset()
        src = driver.get(bit)
        if src is None:
            out = frozenset()
        elif domain_of(src) is not None:
            out = frozenset({src})
        else:
            cell = mod["cells"][src[0]]
            dirs = cell.get("port_directions", {})
            out = frozenset().union(*(sources(b) for p, bits in cell["connections"].items()
                                      if dirs.get(p) != "output" for b in bits))
        memo[bit] = out
        return out

    sinks: list[tuple[str, str, list, bool]] = []
    for n, c in mod["cells"].items():
        if n in flop_dom:
            q = c["connections"]["Q"][0]
            held = HELD[0] in aliases.get(q, ())
            sinks.append((f"flop {HELD[0] if held else names.get(q, n)}", flop_dom[n],
                          [b for p, bits in c["connections"].items() if p not in ("CLK", "Q") for b in bits], held))
        elif n in prim_dom:
            for p, bits in c["connections"].items():
                if p in ("src_in", "src_send", "src_pulse"):
                    sinks.append((f"{n}.{p}", prim_dom[n][0], list(bits), False))
    for p, v in mod["ports"].items():
        if v["direction"] == "output":
            sinks.append((f"output {p}", "sys" if p.startswith("m_") else "dp", list(v["bits"]), False))
    out = []
    for label, dom, bits, held in sinks:
        bad = defaultdict(set)
        for b in bits:
            for s in sources(b):
                d = domain_of(s)
                if d not in (dom, None):
                    if held and s[0] == "in" and s[1].startswith(HELD[1]):
                        continue
                    bad[d].add(s[1] if s[0] == "in" else
                               names.get(mod["cells"][s[0]]["connections"].get("Q", [None])[0], s[0])
                               if s[0] in flop_dom else f"{s[0]}.{s[1]}")
        out += [f"a crossing without a primitive: {label} ({dom}) reads {', '.join(sorted(v))} ({d})"
                for d, v in sorted(bad.items())]
    return len(sinks), out


def run(cdc: Path = CDC, win: Path = WIN) -> tuple[int, list[str]]:
    with tempfile.TemporaryDirectory(prefix="split-cdc-") as tmp:
        return findings(netlist(cdc, win, Path(tmp)))


#: (name, the source, its tracked text, the planted text, the words its finding must hold)
PLANTS = (
    ("the publication block wired straight across", CDC,
     "          d_pub_bound_o, d_pub_sid_valid_o, d_pub_started_o, d_pub_sid_o} = pub_dst_w;",
     "          d_pub_bound_o, d_pub_sid_valid_o, d_pub_started_o, d_pub_sid_o} = pub_src_w;",
     "output d_pub_sid_o (dp) reads m_pub_sid_i (sys)"),
    ("the LINK level taken straight across", CDC,
     "        m_link_up_o     <= ev_dst_w[72 + NP_C + 4];",
     "        m_link_up_o     <= d_link_up_i;",
     "flop m_link_up_o (sys) reads d_link_up_i (dp)"),
    ("the settings read without their capture", CDC,
     "          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_r;",
     "          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_bus_w;",
     "output d_cur_config_o (dp) reads m_fw_cur_config_i (sys)"),
    ("a window's answer taken straight across", WIN,
     "  assign m_ans_data_o = out_w[ANS_W_P-1:0];",
     "  assign m_ans_data_o = ans_r;",
     "output m_ctr_ans_data_o (sys) reads"),
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    checks = failures = 0
    n, found = run()
    checks += 1
    failures += bool(found)
    print(f"{'[ok]  ' if not found else '[FAIL]'} the tracked sources: {n} sinks read their own domain"
          + "".join(f"\n       {f}" for f in found))
    if args.selftest:
        for name, src, old, new, words in PLANTS:
            checks += 1
            text = src.read_text()
            if text.count(old) != 1:
                print(f"[FAIL] {name}: its anchor is not in {src.name} once")
                failures += 1
                continue
            with tempfile.TemporaryDirectory(prefix="split-cdc-plant-") as tmp:
                copy = Path(tmp) / src.name
                copy.write_text(text.replace(old, new))
                _n, got = run(copy if src == CDC else CDC, copy if src == WIN else WIN)
            caught = any(words in f for f in got)
            failures += not caught
            print(f"{'[ok]  ' if caught else '[FAIL]'} planted {name}: "
                  + (next(f for f in got if words in f) if caught else f"not refused by '{words}': {got}"))
    print(f"checks: {checks}   failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
