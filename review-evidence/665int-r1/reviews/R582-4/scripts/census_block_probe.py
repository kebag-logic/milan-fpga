#!/usr/bin/env python3
"""Reviewer probe (R582-4) of sw/mailbox/publication_census.py's cone rule.

The census states (docstring "THE CONE"): a read leads to every signal its
statement can drive, "every target of the procedural block (always, initial,
final) it lies in". Each arm below routes a status consumer
(lwsrp_talker_declared) or an answer-face consumer (gsi_tkdcl_w) through a
procedural block into another module's input port, which the census defines
as the wire, and asks whether the census refuses it. Controls use the same
block written with an explicit begin right after the event control.

Usage: python3 -I -B census_block_probe.py <checkout>
In-memory copies only; writes nothing. Exit 0 always; the verdict is the
printed table (ESCAPES = the census accepted a cone that reaches the wire).
"""
import sys
from dataclasses import replace
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import publication_census as pc  # noqa: E402

ANCHOR = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
SINK = "  KL_probe_sink u_probe_sink (.a_i(probe_q));\n"
CONSUMERS = {"lwsrp_talker_declared": ("status", "logic"), "gsi_tkdcl_w": ("processor", "logic [1:0]")}


def arms(c: str, width: str):
    d = f"  {width} probe_a, probe_q;\n"
    return [
        ("control: always_ff begin, if-begin block", True,
         d + f"  always_ff @(posedge axis_clk) begin if ({c} != '0) begin probe_a <= '1; probe_q <= '1; end end\n" + SINK),
        ("E1 always_ff with no begin after the event control, if-begin block", False,
         d + f"  always_ff @(posedge axis_clk) if ({c} != '0) begin probe_a <= '1; probe_q <= '1; end\n" + SINK),
        ("E2 always_ff, no begin, if/else", False,
         d + f"  always_ff @(posedge axis_clk) if ({c} != '0) probe_a <= '1; else probe_q <= '1;\n" + SINK),
        ("E3 always_comb, no begin, case", False,
         d + f"  always_comb case ({c}) '0: probe_a = '1; default: probe_q = '1; endcase\n" + SINK),
        ("E4 always_ff begin, event control with a parenthesised iff", False,
         d + f"  always_ff @(posedge axis_clk iff (axis_resetn)) begin if ({c} != '0) begin probe_a <= '1; "
             f"probe_q <= '1; end end\n" + SINK),
        ("control: always_ff begin, plain blocking assignment", True,
         d + f"  always_ff @(posedge axis_clk) begin probe_a <= '0; probe_q = {c}; end\n" + SINK),
        ("E5 always_ff begin, compound assignment |=", False,
         d + f"  always_ff @(posedge axis_clk) begin probe_a <= '0; probe_q |= {c}; end\n" + SINK),
        ("control: alias with the consumer on the right", True,
         f"  wire {width.replace('logic', '').strip()} probe_q;\n  alias probe_q = {c};\n" + SINK),
        ("E6 alias with the consumer on the left", False,
         f"  wire {width.replace('logic', '').strip()} probe_q;\n  alias {c} = probe_q;\n" + SINK),
    ]


def main() -> int:
    known = pc.fields(pc.mailbox_model.load())
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    base, _ = pc.findings(src, pc.CENSUS, known)
    print(f"tracked sources: {len(base)} finding(s)")
    escapes = unexpected = 0
    for c, (kind, width) in CONSUMERS.items():
        for name, control, text in arms(c, width):
            assert src.datapath.count(ANCHOR) == 1
            planted = replace(src, datapath=src.datapath.replace(ANCHOR, text + ANCHOR, 1))
            try:
                got, _ = pc.findings(planted, pc.CENSUS, known)
            except pc.CensusError as exc:
                got = [f"census cannot read: {exc}"]
            refused = bool(got)
            tag = "REFUSED" if refused else "ESCAPES"
            ok = refused if control else True
            unexpected += control and not refused
            escapes += (not control) and (not refused)
            print(f"[{tag}] {kind:9} {c:22} {name}" + (f" :: {got[0][:160]}" if got else ""))
            if not ok:
                print("    ^ control not refused: the probe itself is broken")
    print(f"block probe: {escapes} escaping arm(s), {unexpected} control(s) not refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
