#!/usr/bin/env python3
"""R583-4 census probes: forms the fail-closed census rule claims to refuse.

Usage: python3 -I r583_4_census_probes.py <tree>   (an export of the head; nothing is written)

Each probe edits an in-memory copy of the datapath (and, where stated, of the
first copy of an included file), then calls the census's own findings() with
its tracked CENSUS table. A probe whose read reaches the wire while the census
reports zero findings is an ESCAPE. Controls are the same edit in a form the
census already refuses; they must be REFUSED.
"""
import sys
from dataclasses import replace
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import mailbox_model  # noqa: E402
import publication_census as pc  # noqa: E402

src = pc.load(tree / "hdl/milan/milan_datapath.sv", tree / "hdl/milan/KL_pp_shadow.sv")
known = pc.fields(mailbox_model.load())

CRF_DECL = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
VLAN_EN = "    .vlan_en_i  (crft_class_a_w),"
SINK = "  KL_probe_sink u_probe_sink (.a_i(probe_q));\n"
WIRE = "pp_cd_srp_over_limit_w"
DECL = "  wire                       pp_cd_srp_over_limit_w;"
INC = "ethernet_events.svh"


def edit(text, old, new):
    assert text.count(old) == 1, f"fixture occurs {text.count(old)} times: {old!r}"
    return text.replace(old, new, 1)


def dp(*edits):
    t = src.datapath
    for o, n in edits:
        t = edit(t, o, n)
    return replace(src, datapath=t)


def with_include(s, line):
    (path, text), *rest = s.included[INC]
    return replace(s, included={**s.included, INC: ((path, text + line), *rest)})


def anchored(decl):
    return dp((CRF_DECL, decl + CRF_DECL))


def routed(decl):
    return dp((CRF_DECL, decl + CRF_DECL), (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),"))


PROBES = []


def probe(name, kind, s):
    PROBES.append((name, kind, s))


for sig in ("lwsrp_talker_declared", "gsi_tkdcl_w"):
    # cone: a procedural block without begin/end holding an if/else or case
    probe(f"{sig}: begin-less always_ff, if/else, else-branch register to a sink", "probe",
          anchored("  logic probe_a, probe_q;\n"
                   f"  always_ff @(posedge axis_clk) if ({sig}[0]) probe_a <= 1'b0; else probe_q <= 1'b1;\n" + SINK))
    probe(f"{sig}: begin-less always_ff, if/else with begin/end branches", "probe",
          anchored("  logic probe_a, probe_q;\n"
                   f"  always_ff @(posedge axis_clk) if ({sig}[0]) begin probe_a <= 1'b0; end\n"
                   "  else begin probe_q <= 1'b1; end\n" + SINK))
    probe(f"{sig}: begin-less always_ff, case selector, default-item register to a sink", "probe",
          anchored("  logic probe_a, probe_q;\n"
                   f"  always_ff @(posedge axis_clk) case ({sig}[0]) 1'b1: probe_a <= 1'b0; "
                   "default: probe_q <= 1'b1; endcase\n" + SINK))
    probe(f"{sig}: begin/end always_ff whose event control nests parentheses, if/else", "probe",
          anchored("  logic probe_a, probe_q;\n"
                   f"  always_ff @(posedge axis_clk or posedge (axis_rst)) begin\n"
                   f"    if ({sig}[0]) probe_a <= 1'b0;\n    else probe_q <= 1'b1;\n  end\n" + SINK))
    probe(f"{sig}: CONTROL, the same if/else inside begin/end", "control",
          anchored("  logic probe_a, probe_q;\n"
                   f"  always_ff @(posedge axis_clk) begin\n    if ({sig}[0]) probe_a <= 1'b0;\n"
                   "    else probe_q <= 1'b1;\n  end\n" + SINK))

# first hop: a macro defined in an included file
probe("included file defines a token-paste macro; datapath reads pp_cd_srp_over_limit_w through it", "probe",
      with_include(routed("  wire probe_w;\n  assign probe_w = `PROBE_CD(srp_over_limit);\n"),
                   "\n`define PROBE_CD(n) pp_cd_``n``_w\n"))
probe("included file defines a macro holding a hierarchical reference into the wrapper", "probe",
      with_include(routed("  wire probe_w;\n  assign probe_w = `PROBE_H;\n"),
                   "\n`define PROBE_H pp_shadow.srp_over_limit_o\n"))
probe("CONTROL: the token-paste macro defined in the datapath", "control",
      routed("  `define PROBE_CD(n) pp_cd_``n``_w\n  wire probe_w;\n  assign probe_w = `PROBE_CD(srp_over_limit);\n"))
probe("CONTROL: the hierarchical reference written in the datapath", "control",
      routed("  wire probe_w;\n  assign probe_w = pp_shadow.srp_over_limit_o;\n"))

# first hop: escaped identifiers holding a comment or string opener (IEEE 1800-2017 5.6.1)
probe("escaped identifier containing // hides a read of the class-D wire", "probe",
      dp((CRF_DECL, "  wire \\probe//w ;\n  assign \\probe//w = " + WIRE + ";\n" + CRF_DECL),
         (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~\\probe//w\n               ),")))
probe("escaped identifier containing a double quote hides the statements up to the next quote", "probe",
      dp((CRF_DECL, "  wire \\probe\"a ;\n  wire probe_w;\n  assign probe_w = " + WIRE + ";\n"
          "  wire \\probe\"b ;\n" + CRF_DECL),
         (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),")))
probe("CONTROL: the same read through a plain wire", "control",
      routed("  wire probe_w;\n  assign probe_w = " + WIRE + ";\n"))

# a second driver: the docstring says a second driver fails
probe("second driver as the population wire's declaration initialiser", "probe",
      dp((DECL, "  wire                       pp_cd_srp_over_limit_w = 1'b0;")))
probe("CONTROL: second driver as a continuous assign", "control",
      dp((CRF_DECL, f"  assign {WIRE} = 1'b0;\n" + CRF_DECL)))

escapes = bad_controls = 0
for name, kind, s in PROBES:
    try:
        got, _ = pc.findings(s, pc.CENSUS, known)
    except pc.CensusError as exc:
        got = [f"census cannot read it: {exc}"]
    verdict = "REFUSED" if got else "ACCEPTED"
    if kind == "control":
        bad_controls += not got
        tag = "ok" if got else "BAD"
    else:
        escapes += not got
        tag = "refused" if got else "ESCAPE"
    print(f"[{tag}] {kind:7} {name}: {verdict}" + (f" :: {got[0][:170]}" if got else ""))
print(f"r583-4 probes: {sum(k == 'probe' for _, k, _ in PROBES)} probes, {escapes} escape(s); "
      f"{sum(k == 'control' for _, k, _ in PROBES)} controls, {bad_controls} not refused")
sys.exit(1 if bad_controls else 0)
