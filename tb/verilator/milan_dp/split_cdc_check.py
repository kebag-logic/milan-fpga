#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""split_cdc_check.py - every crossing of KL_mbx_cdc goes through an approved primitive (#665).

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
gives: m_* and sys_* the mailbox's, d_* and dp_* the datapath's. A
primitive's src_* ports are in the domain of the clock its src_clk reads, its
dest_* ports in the domain of the clock its dest_clk reads.

THE RULE. Each of these sinks must read, through combinational cells alone,
only sources of its own domain:

  - every flop's inputs other than its clock;
  - every output port;
  - every primitive's src_in, src_send, src_pulse and src_rst_n, in its
    source domain, and its dest_rst_n, in its destination domain.

Every flop's CLK and every primitive's src_clk and dest_clk must read one of
the two clock inputs, straight.

THE ONE ALLOWANCE is the settings capture. The flop ``fw_r`` may read the
data bits of the bus KL_mbx holds, every m_fw_* input but m_fw_send_i (the
commit level itself), only through a ``$mux`` whose select is u_fw_req's
dest_pulse, straight, on the input that select takes. Any other reading of
those bits is a crossing without a primitive: on every datapath cycle, on
another select, on the select's other input, or by another flop.

NOT READ HERE. That KL_mbx holds the bus from its commit until the
acknowledgement, and refuses a face write or GO while busy, is KL_mbx's
behaviour, outside this netlist. The milan_dp split leg's [FACE] checks and
their mutants hold it.

    python3 split_cdc_check.py              # the tracked sources
    python3 split_cdc_check.py --selftest   # and every plant in PLANTS, each refused by its words

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
#: a primitive's inputs judged in its source domain, and in its destination domain
SRC_SINKS = ("src_in", "src_send", "src_pulse", "src_rst_n")
DEST_SINKS = ("dest_rst_n",)
#: the one reading across the domains this design is allowed: the held settings bus,
#: taken by the flop HELD_FLOP through a $mux whose select is GATE
HELD_FLOP = "fw_r"
GATE = ("u_fw_req", "dest_pulse")


def held_bus(port: str) -> bool:
    """A data bit of the settings bus KL_mbx holds: every m_fw_* input but the commit level."""
    return port.startswith("m_fw_") and port != "m_fw_send_i"


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

    def gated(cell: dict) -> bool:
        """A $mux whose select is u_fw_req's dest_pulse, straight."""
        return (cell["type"] == "$mux" and mod["cells"].get(GATE[0], {}).get("type") == "cdc_pulse"
                and driver.get(cell["connections"]["S"][0]) == GATE)

    memo: dict[tuple[int, bool], frozenset] = {}

    def sources(bit, taken: bool = False) -> frozenset:
        """The ((cell, port), taken) sources a bit reads through combinational cells alone.

        ``taken`` is true on a path that passed the B input of a gated $mux:
        the input it selects while u_fw_req's dest_pulse is high.
        """
        if not isinstance(bit, int):
            return frozenset()
        key = (bit, taken)
        if key in memo:
            return memo[key]
        memo[key] = frozenset()
        src = driver.get(bit)
        if src is None:
            out = frozenset()
        elif domain_of(src) is not None:
            out = frozenset({(src, taken)})
        else:
            cell = mod["cells"][src[0]]
            dirs = cell.get("port_directions", {})
            gate = gated(cell)
            out = frozenset().union(*(sources(b, taken or (gate and p == "B"))
                                      for p, bits in cell["connections"].items()
                                      if dirs.get(p) != "output" for b in bits))
        memo[key] = out
        return out

    def label_of(s: tuple[str, str]) -> str:
        if s[0] == "in":
            return s[1]
        if s[0] in flop_dom:
            return names.get(mod["cells"][s[0]]["connections"].get("Q", [None])[0], s[0])
        return f"{s[0]}.{s[1]}"

    clock_src = {("in", c) for c in CLOCKS}
    sinks: list[tuple[str, str, list, bool]] = []
    clock_sinks: list[tuple[str, int]] = []
    for n, c in mod["cells"].items():
        if n in flop_dom:
            q = c["connections"]["Q"][0]
            held = HELD_FLOP in aliases.get(q, ())
            label = f"flop {HELD_FLOP if held else names.get(q, n)}"
            sinks.append((label, flop_dom[n],
                          [b for p, bits in c["connections"].items() if p not in ("CLK", "Q") for b in bits], held))
            clock_sinks.append((f"{label}'s CLK", c["connections"]["CLK"][0]))
        elif n in prim_dom:
            for p, bits in c["connections"].items():
                if p in SRC_SINKS:
                    sinks.append((f"{n}.{p}", prim_dom[n][0], list(bits), False))
                elif p in DEST_SINKS:
                    sinks.append((f"{n}.{p}", prim_dom[n][1], list(bits), False))
            for p in PRIM_CLOCKS[c["type"]]:
                clock_sinks.append((f"{n}.{p}", c["connections"][p][0]))
    for p, v in mod["ports"].items():
        if v["direction"] == "output":
            sinks.append((f"output {p}", "sys" if p.startswith("m_") else "dp", list(v["bits"]), False))
    out = []
    for label, dom, bits, held in sinks:
        bad, untaken = defaultdict(set), set()
        for b in bits:
            for s, taken in sources(b):
                d = domain_of(s)
                if d in (dom, None):
                    continue
                if held and s[0] == "in" and held_bus(s[1]):
                    if not taken:
                        untaken.add(s[1])
                    continue
                bad[d].add(label_of(s))
        out += [f"a crossing without a primitive: {label} ({dom}) reads {', '.join(sorted(v))} ({d})"
                for d, v in sorted(bad.items())]
        if untaken:
            out.append(f"a crossing without a primitive: {label} ({dom}) takes the held bus "
                       f"{', '.join(sorted(untaken))} (sys) other than through a $mux selected by "
                       f"{GATE[0]}.{GATE[1]}")
    for label, bit in clock_sinks:
        if driver.get(bit) not in clock_src:
            src = driver.get(bit)
            out.append(f"a clock that is not a clock input: {label} reads "
                       f"{label_of(src) if src else 'a constant'}")
    return len(sinks) + len(clock_sinks), out


def run(cdc: Path = CDC, win: Path = WIN) -> tuple[int, list[str]]:
    with tempfile.TemporaryDirectory(prefix="split-cdc-") as tmp:
        return findings(netlist(cdc, win, Path(tmp)))


#: (name, the source, its tracked text, the planted text, the words its findings must hold, each)
TAKE = "    else if (fw_take_p_w) fw_r <= fw_bus_w;"
PLANTS = (
    ("the publication block wired straight across", CDC,
     "          d_pub_bound_o, d_pub_sid_valid_o, d_pub_started_o, d_pub_sid_o} = pub_dst_w;",
     "          d_pub_bound_o, d_pub_sid_valid_o, d_pub_started_o, d_pub_sid_o} = pub_src_w;",
     ("output d_pub_sid_o (dp) reads m_pub_sid_i (sys)",)),
    ("the LINK level taken straight across", CDC,
     "        m_link_up_o     <= ev_dst_w[72 + NP_C + 4];",
     "        m_link_up_o     <= d_link_up_i;",
     ("flop m_link_up_o (sys) reads d_link_up_i (dp)",)),
    ("the settings read without their capture", CDC,
     "          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_r;",
     "          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_bus_w;",
     ("output d_cur_config_o (dp) reads m_fw_cur_config_i (sys)",)),
    ("a window's answer taken straight across", WIN,
     "  assign m_ans_data_o = out_w[ANS_W_P-1:0];",
     "  assign m_ans_data_o = ans_r;",
     ("output m_ctr_ans_data_o (sys) reads",)),
    ("the held bus taken on every datapath cycle", CDC, TAKE,
     "    else                  fw_r <= fw_bus_w;",
     ("flop fw_r (dp) takes the held bus",)),
    ("the held bus taken on the commit level, in the mailbox's clock", CDC, TAKE,
     "    else if (m_fw_send_i) fw_r <= fw_bus_w;",
     ("flop fw_r (dp) reads m_fw_send_i (sys)", "flop fw_r (dp) takes the held bus")),
    ("the held bus taken on the request pulse, in the mailbox's clock", CDC, TAKE,
     "    else if (fw_req_p_w) fw_r <= fw_bus_w;",
     ("flop fw_r (dp) reads fw_send_q_r, m_fw_send_i (sys)", "flop fw_r (dp) takes the held bus")),
    ("the held bus taken while the pulse is low", CDC, TAKE,
     "    else if (!fw_take_p_w) fw_r <= fw_bus_w;",
     ("flop fw_r (dp) takes the held bus",)),
    ("a datapath flop other than fw_r sampling the held bus", CDC,
     "      ev_dom_r  <= d_gptp_domain_i;",
     "      ev_dom_r  <= m_fw_identify_i;",
     ("flop ev_dom_r (dp) reads m_fw_identify_i (sys)",)),
    ("a destination reset from the other domain", CDC,
     "    .dest_clk(dp_clk_i), .dest_rst_n(dp_rst_n), .dest_out(pub_dst_w), .dest_req());",
     "    .dest_clk(dp_clk_i), .dest_rst_n(sys_rst_n), .dest_out(pub_dst_w), .dest_req());",
     ("u_pub.dest_rst_n (dp) reads sys_rst_n (sys)",)),
    ("a source reset from the other domain", CDC,
     "  cdc_pulse u_fw_ack (.src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_pulse(fw_take_p_w),",
     "  cdc_pulse u_fw_ack (.src_clk(dp_clk_i), .src_rst_n(sys_rst_n), .src_pulse(fw_take_p_w),",
     ("u_fw_ack.src_rst_n (dp) reads sys_rst_n (sys)",)),
    ("a primitive clocked by a level", CDC,
     "                      .dest_clk(sys_clk_i), .dest_rst_n(sys_rst_n), .dest_pulse(m_fw_ack_p_o));",
     "                      .dest_clk(m_fw_send_i), .dest_rst_n(sys_rst_n), .dest_pulse(m_fw_ack_p_o));",
     ("a clock that is not a clock input: u_fw_ack.dest_clk reads m_fw_send_i",)),
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
            hits = [next((f for f in got if w in f), None) for w in words]
            caught = all(hits)
            failures += not caught
            print(f"{'[ok]  ' if caught else '[FAIL]'} planted {name}: "
                  + ("".join(f"\n       {h}" for h in hits) if caught
                     else f"not refused by {[w for w, h in zip(words, hits) if not h]}: {got}"))
    print(f"checks: {checks}   failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
