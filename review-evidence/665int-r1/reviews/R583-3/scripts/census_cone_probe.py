#!/usr/bin/env python3
"""census_cone_probe.py - does the publication census follow a STATUS read's
consumer through every form, as its docstring claims ("the cone
over-approximates: a path it cannot rule out counts as reaching the wire")?

Usage: python3 -I census_cone_probe.py <tree>

<tree> is a checkout of the head under review. Nothing in it is modified: the
census module is imported from <tree>/sw/mailbox and each plant is applied to
an in-memory copy of milan_datapath.sv.

Every plant leaves the class-D wire's own occurrence untouched (it is still
the tracked `assign lwsrp_res_active = |pp_cd_srp_active_w;`, a status read
mapped to LWSRP_STATUS) and adds a path, one hop out, from that STATUS
consumer to another module's input port, i.e. to the wire. A sound census
must refuse each plant with "counted as status, but it reaches the wire".

A control plant uses a plain continuous assign for the same hop and must be
refused; it shows the probe's insertion point and terminal are valid.

Exit 0 when the probe ran; it prints REFUSED or ESCAPED per plant.
"""
import sys
from dataclasses import replace
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import publication_census as pc  # noqa: E402

ANCHOR = "  wire crft_class_a_w ="
SINK = "  KL_probe_sink u_probe_sink (.a_i(probe_q));\n"
PLANTS = {
    "control: plain assign from the status consumer": (
        "  wire probe_q;\n  assign probe_q = lwsrp_res_active;\n" + SINK),
    "case item label naming the status consumer": (
        "  logic probe_q;\n  always_comb begin\n    case (1'b1)\n"
        "      lwsrp_res_active: probe_q = 1'b1;\n      default: probe_q = 1'b0;\n    endcase\n  end\n" + SINK),
    "function body returning the status consumer": (
        "  function automatic logic probe_f(input logic x);\n    return lwsrp_res_active;\n  endfunction\n"
        "  wire probe_q = probe_f(1'b0);\n" + SINK),
    "event control (clock) of a register": (
        "  logic probe_q;\n  always_ff @(posedge lwsrp_res_active) probe_q <= 1'b1;\n" + SINK),
    "input port whose name ends in _o": (
        "  logic probe_q;\n  KL_probe_sink u_probe_sink (.a_o(lwsrp_res_active));\n"),
}


def main() -> int:
    known = pc.fields(pc.mailbox_model.load())
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    base, _ = pc.findings(src, pc.CENSUS, known)
    print(f"tracked sources: {len(base)} finding(s)")
    if ANCHOR not in src.datapath:
        print("anchor not found")
        return 2
    for what, text in PLANTS.items():
        planted = replace(src, datapath=src.datapath.replace(ANCHOR, text + ANCHOR, 1))
        try:
            got, _ = pc.findings(planted, pc.CENSUS, known)
        except pc.CensusError as exc:
            got = [f"census cannot read: {exc}"]
        hit = [f for f in got if "lwsrp_res_active" in f or "probe" in f]
        verdict = "REFUSED" if got else "ESCAPED"
        print(f"[{verdict}] {what}: {len(got)} finding(s)" + (f" - {hit[0] if hit else got[0]}" if got else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
