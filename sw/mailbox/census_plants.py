# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_plants.py - the defects publication_census.py --selftest elaborates, each refused by its own words.

Each plant edits a copy of one source the census elaborates: the datapath,
the processor wrapper, or the first copy of a file the datapath includes.
Every edit's old text must occur exactly once, so a plant whose fixture moved
fails the self-test instead of passing it unplanted. The reviewers' probes of
#665 are reproduced form for form: R582-2's census_probes.py and R583-2's
census_escape_probe.py (comment 6094461419), R582-3's and R583-3's
census_cone_probe.py (comment 6095903333), R582-4's census_block_probe.py and
R583-4's r583_4_census_probes.py (comment 6097292237), each escaping form
beside its plain-assign control.

A plant that instantiates a probe module defines it after the datapath's
``endmodule``, so the elaborator knows its ports: an input of any module is
the wire. A plant's words are one string, or several one finding must carry:
a cone plant is refused by its read's row and the port it reaches, a form the
front end or the elaborator refuses by that tool's words.

Each plant names the census rule (census_rules.RULES) whose removal must let
it through, and the self-test removes that rule and requires it to be: a plant
refused by sv2v or Yosys themselves names none. A plant elaborates at the
recipe's shape unless it names others: ``("N_STREAMS", 2)`` is the first
shape the builder builds that binds N_STREAMS to 2 or more, so a branch only
such shapes build is in the netlist it is judged on (#665, comment
6100024293: R583-5's S1 to S3, R582-5's arms B and E).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from census_rules import RULES

#: The class-D wire every first-hop probe reads, and the sites the plants anchor on.
WIRE = "pp_cd_srp_over_limit_w"
WIRE_DECL = "  wire                       pp_cd_srp_over_limit_w;"
CRF_STAT = "    crft_stat_c[4]     = 1'b0;"
CRF_DECL = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
VLAN_EN = "    .vlan_en_i  (crft_class_a_w),"
OVER_LIMIT = "      .srp_over_limit_o        (pp_cd_srp_over_limit_w),\n"
CLASS_A_PRIO = "      .srp_class_a_prio_o      (pp_cd_srp_class_a_prio_w),"
DOMAIN_CHANGE = ".srp_domain_change_o     (pp_cd_srp_domain_change_w),"
TLK_GATE = "    .i_tlk_gate_v         (8'(aaf_stream_en_w)),"
MAAP_INTERNAL = "      .cfg_maap_internal_i     (1'b0),"
STARTED_ACCEPT = ("  wire [ACMP_SINKS_C-1:0] acmpl_stopped_v_w = acmpl_bound_v_w\n"
                  "                                              & ~{};")
#: The datapath's last line: probe modules are defined after it.
TAIL = "\n`default_nettype wire\n"
#: Round 7's fixtures: a datapath output, the answer face's change strobe, the
#: wrapper and CSR instances, a CSR read-back input, the started port, and the
#: AAF stream gate of streams 1 and up, which no one-stream shape builds.
OUTPUT = "  output wire        o_desc_mem_req_valid,\n"
AVB_CHG = "  wire gsi_avb_chg_w = gsi_gm_chg_w"
SHADOW_CELL = "    ) pp_shadow ("
CSR_INST = "  ) csr ("
AVAIL_INDEX = "    .i_adp_available_index(adp_available_index),"
STARTED_DECL = "    output logic [N_STREAM_IN_P-1:0]   aecp_strm_started_o,"
STARTED_INNER = "      .aecp_strm_started_o (aecp_strm_started_o),"
STARTED_CONN = "      .aecp_strm_started_o (pp_aecp_strm_started_w),"
STREAM_GATE = "           (acmp_talker_active_aaf_w[gs] & lwsrp_stream_gate[gs]));"
#: The shapes a branch needs: more than one stream, the loopback lane.
STREAMS = ("N_STREAMS", 2)
LOOPBACK = ("LOOPBACK_P", 1)
#: The wrapper's port list: a class-D output, one moved out of the face, and the next section.
SHADOW_OVER_LIMIT = ("    output logic                         srp_over_limit_o,        "
                     "//! a source was refused against the port ceiling\n")
SHADOW_EID = ("    output logic [N_STREAM_IN_P*64-1:0]  acmp_bound_eid_o,        "
              "//! per-sink bound talker entity_id\n")
SHADOW_OBSERVABILITY = "    //! ---- observability ----\n"
#: The included files the include plants write into: one the module body
#: includes, one included before the module.
SHAPE_INCLUDE = "gen/adp_shape_defaults.svh"
#: The datapath's include of it; milan_csr includes the same file, so a plant guards its text to the datapath.
SHAPE_LINE = '  `include "gen/adp_shape_defaults.svh"'
EVENTS_INCLUDE = "ethernet_events.svh"

#: The status and answer-face consumers the cone plants route, and the row each read is keyed by.
TALKER_DECLARED = "lwsrp_talker_declared"
GSI_TKDCL = "gsi_tkdcl_w"
RES_ACTIVE = "lwsrp_res_active"
ROW = {TALKER_DECLARED: ("pp_cd_srp_tk_decl_state_w -> lwsrp_talker_declared:", "status"),
       GSI_TKDCL: ("pp_cd_srp_tk_decl_state_w -> gsi_tkdcl_w:", "processor"),
       RES_ACTIVE: ("pp_cd_srp_active_w -> lwsrp_res_active:", "status")}
#: R583-3's sink: another module's input port, which is the wire.
SINK = "  KL_probe_sink u_probe_sink (.a_i(probe_q));\n"
#: The probe modules, defined after the datapath.
SINK_MOD = "module KL_probe_sink (input logic [1:0] a_i, input logic [1:0] a_o);\nendmodule\n"
BUF_MOD = "module KL_probe_buf (input logic [1:0] a, output logic y_o);\n  assign y_o = |a;\nendmodule\n"
#: The words of a form the front end refuses, and of one the elaborator refuses.
SV2V = "the front end (sv2v) refused the datapath"
YOSYS = "the elaborator (Yosys) refused the datapath"
OPENER = "an escaped name holds a comment opener"


@dataclass(frozen=True)
class Plant:
    """One planted defect: the source it edits, its (old, new) edits, the words its finding must carry,
    the rule whose removal lets it through, and the shapes it is elaborated in."""

    what: str
    where: str                              # "datapath", "wrapper", "toolchain" or an included file's name
    edits: tuple[tuple[str, str], ...]
    word: str | tuple[str, ...]
    rule: str | None = None                 # None: refused by sv2v or Yosys, no census rule
    at: tuple[Any, ...] = ("recipe",)       # "recipe", or (parameter, least) for the first shape binding it so
    also: tuple[tuple[str, str], ...] = ()  # a wrapper plant's edits to the datapath

    def __post_init__(self) -> None:
        if self.rule is not None and self.rule not in RULES:
            raise KeyError(f"plant {self.what!r} names no census rule {self.rule}")


def unmapped(consumer: str, wire: str = WIRE) -> str:
    """The words refusing a read of wire into consumer that no row names."""
    return f"unmapped read: {wire} -> {consumer} reaches"


def reaches(sig: str, end: str) -> tuple[str, str, str]:
    """The words refusing a cone plant: sig's read row, counted in its class, reaching the wire at end."""
    row, kind = ROW[sig]
    return row, f"counted as {kind}, but it reaches the wire at", end


def modules(*text: str) -> tuple[str, str]:
    """The edit defining probe modules after the datapath."""
    return TAIL, TAIL + "".join(text)


def routed(decl: str, *mods: str) -> tuple[tuple[str, str], ...]:
    """R583-2's probe shape: decl placed before the CRF talker's C-TAG enable,
    and probe_w ANDed into that talker's vlan_en_i, which is on the wire."""
    return ((CRF_DECL, decl + CRF_DECL), (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),"),
            *((modules(*mods),) if mods else ()))


def anchored(decl: str, *mods: str) -> tuple[tuple[str, str], ...]:
    """R583-3's probe shape: decl placed before the CRF talker's C-TAG enable, a probe module's input its sink."""
    return ((CRF_DECL, decl + CRF_DECL), modules(SINK_MOD, *mods))


def on_crf(decl: str, term: str) -> tuple[tuple[str, str], ...]:
    """R582-2's probe shape: decl placed before the CRF talker's C-TAG enable, and term ANDed into it."""
    return ((CRF_DECL, decl + CRF_DECL.replace("=", f"= {term} &", 1)),)


def dot_mod(port: str) -> str:
    """A probe module with an input named port, for an implicit .name connection."""
    return f"module KL_probe_dot (input logic [1:0] {port}, output logic y_o);\nendmodule\n"


def cone_plants(sig: str) -> list[Plant]:
    """R582-3's part 1 forms, each routing sig onto the CRF talker's vlan_en_i,
    and R583-3's event control and _o-named input port, for one status or
    answer-face consumer."""
    return [
        Plant(f"R582-3: {sig} routed to the wire by a plain assign (its control)", "datapath",
              routed(f"  wire probe_w;\n  assign probe_w = |{sig};\n"), reaches(sig, "crf_tx.vlan_en_i"),
              rule="off-wire"),
        Plant(f"R582-3: {sig} routed to the wire by a positional port", "datapath",
              routed(f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({sig}, probe_w);\n", BUF_MOD),
              reaches(sig, "u_probe_pos.a"), rule="off-wire"),
        Plant(f"R582-3: {sig} routed to the wire by an implicit .name port", "datapath",
              routed(f"  wire probe_w;\n  KL_probe_dot u_probe_dot (.{sig}, .y_o(probe_w));\n", dot_mod(sig)),
              reaches(sig, f"u_probe_dot.{sig}"), rule="off-wire"),
        Plant(f"R582-3: {sig} routed to the wire by a case item label", "datapath",
              routed("  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    unique case (1'b1)\n"
                     f"      {sig}[0]: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n  end\n"),
              reaches(sig, "crf_tx.vlan_en_i"), rule="off-wire"),
        Plant(f"R582-3: {sig} routed to the wire by a function body's return", "datapath",
              routed(f"  function automatic logic probe_f();\n    return |{sig};\n  endfunction\n"
                     "  wire probe_w;\n  assign probe_w = probe_f();\n"),
              reaches(sig, "crf_tx.vlan_en_i"), rule="off-wire"),
        Plant(f"R583-3: {sig} as a register's event control", "datapath",
              anchored(f"  logic probe_q;\n  always_ff @(posedge {sig}[0]) probe_q <= 1'b1;\n" + SINK),
              reaches(sig, "u_probe_sink.a_i"), rule="off-wire"),
        Plant(f"R583-3: {sig} on an input port whose name ends in _o", "datapath",
              anchored(f"  KL_probe_sink u_probe_sink (.a_o({sig}));\n"), reaches(sig, "u_probe_sink.a_o"),
              rule="off-wire"),
    ]


def block_plants(sig: str) -> list[Plant]:
    """R582-4's procedural-block forms (E1 to E6) and their controls, each driving
    probe_q from sig into a probe module's input."""
    d = "  logic [1:0] probe_a, probe_q;\n"
    sink = reaches(sig, "u_probe_sink.a_i")
    return [
        Plant(f"R582-4: {sig}, always_ff begin, an if-begin block (its control)", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) begin if ({sig} != '0) begin probe_a <= '1; probe_q <= '1; end "
            "end\n" + SINK), sink, rule="off-wire"),
        Plant(f"R582-4 E1: {sig}, always_ff with no begin after the event control", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) if ({sig} != '0) begin probe_a <= '1; probe_q <= '1; end\n"
            + SINK), sink, rule="off-wire"),
        Plant(f"R582-4 E2: {sig}, always_ff with no begin, if/else", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) if ({sig} != '0) probe_a <= '1; else probe_q <= '1;\n" + SINK),
            sink, rule="off-wire"),
        Plant(f"R582-4 E3: {sig}, always_comb with no begin, case", "datapath", anchored(
            d + f"  always_comb case ({sig}) '0: probe_a = '1; default: probe_q = '1; endcase\n" + SINK), sink,
            rule="off-wire"),
        Plant(f"R582-4 E4: {sig}, an event control qualified by iff", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk iff (axis_resetn)) begin if ({sig} != '0) begin probe_a <= '1; "
            "probe_q <= '1; end end\n" + SINK), (SV2V, "iff")),
        Plant(f"R582-4: {sig}, a plain blocking assignment (its control)", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) begin probe_a <= '0; probe_q = {sig}; end\n" + SINK), sink,
            rule="off-wire"),
        Plant(f"R582-4 E5: {sig}, a compound assignment |=", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) begin probe_a <= '0; probe_q |= {sig}; end\n" + SINK), sink,
            rule="off-wire"),
        Plant(f"R582-4: {sig}, alias with the consumer on the right (its control)", "datapath", anchored(
            f"  wire [1:0] probe_q;\n  alias probe_q = {sig};\n" + SINK), (SV2V, "Parse error")),
        Plant(f"R582-4 E6: {sig}, alias with the consumer on the left", "datapath", anchored(
            f"  wire [1:0] probe_q;\n  alias {sig} = probe_q;\n" + SINK), (SV2V, "Parse error")),
    ]


def beginless_plants(sig: str) -> list[Plant]:
    """R583-4's F1 forms: a procedural block with no outer begin, or an event
    control nesting parentheses, its else branch's register on a probe input."""
    d = "  logic probe_a, probe_q;\n"
    sink = reaches(sig, "u_probe_sink.a_i")
    return [
        Plant(f"R583-4: {sig}, begin-less always_ff, if/else", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) if ({sig}[0]) probe_a <= 1'b0; else probe_q <= 1'b1;\n" + SINK),
            sink, rule="off-wire"),
        Plant(f"R583-4: {sig}, begin-less always_ff, if/else with begin/end branches", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) if ({sig}[0]) begin probe_a <= 1'b0; end\n"
            "  else begin probe_q <= 1'b1; end\n" + SINK), sink, rule="off-wire"),
        Plant(f"R583-4: {sig}, begin-less always_ff, a case's default item", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) case ({sig}[0]) 1'b1: probe_a <= 1'b0; "
            "default: probe_q <= 1'b1; endcase\n" + SINK), sink, rule="off-wire"),
        Plant(f"R583-4: {sig}, an event control nesting parentheses", "datapath", anchored(
            d + "  always_ff @(posedge axis_clk or negedge (axis_resetn)) begin\n"
            f"    if (!axis_resetn) probe_q <= 1'b0;\n    else if ({sig}[0]) probe_a <= 1'b0;\n"
            "    else probe_q <= 1'b1;\n  end\n" + SINK), sink, rule="off-wire"),
        Plant(f"R583-4: {sig}, the same if/else inside begin/end (its control)", "datapath", anchored(
            d + f"  always_ff @(posedge axis_clk) begin\n    if ({sig}[0]) probe_a <= 1'b0;\n"
            "    else probe_q <= 1'b1;\n  end\n" + SINK), sink, rule="off-wire"),
    ]


PLANTS = (
    # ---- the census's own defects ------------------------------------------
    Plant("an unmapped read on the wire", "datapath",
          (("(|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]);",
            f"(|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]) & ~{WIRE};"),),
          unmapped("crft_class_a_w"), rule="unmapped"),
    Plant("an unmapped read in a declaration's initialiser", "datapath",
          ((CRF_DECL, "  wire planted_w = |pp_cd_srp_granted_slope_bps_w;\n"
                      + CRF_DECL.replace("=", "= planted_w &", 1)),),
          unmapped("planted_w", "pp_cd_srp_granted_slope_bps_w"), rule="unmapped"),
    Plant("an unmapped read in an always block's condition", "datapath",
          ((CRF_STAT, CRF_STAT + "\n    if (pp_cd_srp_lstn_decl_state_w[0]) crft_stat_c[4] = 1'b1;"),),
          unmapped("crft_stat_c", "pp_cd_srp_lstn_decl_state_w"), rule="every-input"),
    Plant("a status read on the wire", "datapath",
          ((VLAN_EN, "    .vlan_en_i  (lwsrp_talker_declared),"),),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a GET_STREAM_INFO read on the wire", "datapath",
          ((VLAN_EN, "    .vlan_en_i  (gsi_tkdcl_w[0]),"),),
          reaches(GSI_TKDCL, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("the started level dropped from the accept", "datapath",
          ((STARTED_ACCEPT.format("pp_aecp_strm_started_w"), STARTED_ACCEPT.format("pp_cd_acmp_bound_w")),),
          unmapped("acmpl_stopped_v_w", "pp_cd_acmp_bound_w"), rule="unmapped"),
    # ---- R582-2's probes ----------------------------------------------------
    Plant("R582-2: a class-D output wired off the pp_cd_ prefix and read on the wire", "datapath",
          ((DOMAIN_CHANGE, ".srp_domain_change_o     (probe_dom_chg_w),"),
           *on_crf("  wire probe_dom_chg_w;\n", "~probe_dom_chg_w")),
          unmapped("crft_class_a_w", "probe_dom_chg_w"), rule="unmapped"),
    Plant("R582-2: an alias wire read on the wire", "datapath",
          on_crf(f"  wire probe_alias_w = {WIRE};\n", "~probe_alias_w"), unmapped("probe_alias_w"), rule="unmapped"),
    Plant("R582-2: a case selector in an always block", "datapath",
          ((CRF_STAT, CRF_STAT + f"\n    case ({WIRE}) 1'b1: crft_stat_c[4] = 1'b1; "
                                 "default: crft_stat_c[4] = 1'b0; endcase"),),
          unmapped("crft_stat_c"), rule="every-input"),
    Plant("R582-2: a case item label in an always block", "datapath",
          ((CRF_STAT, CRF_STAT + f"\n    case (1'b1) {WIRE}: crft_stat_c[4] = 1'b1; "
                                 "default: crft_stat_c[4] = 1'b0; endcase"),),
          unmapped("crft_stat_c"), rule="every-input"),
    Plant("R582-2: a function body called on the wire", "datapath",
          on_crf(f"  function automatic logic probe_f();\n    probe_f = {WIRE};\n  endfunction\n", "~probe_f()"),
          unmapped("crft_class_a_w"), rule="unmapped"),
    # ---- R583-2's probes ----------------------------------------------------
    Plant("R583-2: a plain assign on the wire (its control)", "datapath",
          routed(f"  wire probe_w;\n  assign probe_w = {WIRE};\n"), unmapped("probe_w"), rule="unmapped"),
    Plant("R583-2: a case item label in an always_comb", "datapath",
          routed("  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    unique case (1'b1)\n"
                 f"      {WIRE}: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n  end\n"),
          unmapped("probe_w"), rule="every-input"),
    Plant("R583-2: a positional port connection", "datapath",
          routed(f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({WIRE}, probe_w);\n", BUF_MOD),
          unmapped("u_probe_pos.a"), rule="unmapped"),
    Plant("R583-2: an implicit .name port connection", "datapath",
          routed(f"  wire probe_w;\n  KL_probe_dot u_probe_dot (.{WIRE}, .y_o(probe_w));\n", dot_mod(WIRE)),
          unmapped(f"u_probe_dot.{WIRE}"), rule="unmapped"),
    Plant("R583-2: a function body's return", "datapath",
          routed(f"  function automatic logic probe_f();\n    return {WIRE};\n  endfunction\n"
                 "  wire probe_w;\n  assign probe_w = probe_f();\n"),
          unmapped("probe_w"), rule="unmapped"),
    # ---- the cone: R582-3's and R583-3's probes ----------------------------
    *cone_plants(TALKER_DECLARED),
    *cone_plants(GSI_TKDCL),
    Plant("R582-3 part 2: a positional port naming a status consumer, its output unused", "datapath",
          anchored(f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({TALKER_DECLARED}, probe_w);\n", BUF_MOD),
          reaches(TALKER_DECLARED, "u_probe_pos.a"), rule="off-wire"),
    Plant("R583-3: a plain assign from the status consumer (its control)", "datapath",
          anchored(f"  wire probe_q;\n  assign probe_q = {RES_ACTIVE};\n" + SINK),
          reaches(RES_ACTIVE, "u_probe_sink.a_i"), rule="off-wire"),
    Plant("R583-3: a case item label naming the status consumer", "datapath",
          anchored("  logic probe_q;\n  always_comb begin\n    case (1'b1)\n"
                   f"      {RES_ACTIVE}: probe_q = 1'b1;\n      default: probe_q = 1'b0;\n    endcase\n  end\n" + SINK),
          reaches(RES_ACTIVE, "u_probe_sink.a_i"), rule="off-wire"),
    Plant("R583-3: a function body returning the status consumer", "datapath",
          anchored(f"  function automatic logic probe_f(input logic x);\n    return {RES_ACTIVE};\n  endfunction\n"
                   "  wire probe_q = probe_f(1'b0);\n" + SINK),
          reaches(RES_ACTIVE, "u_probe_sink.a_i"), rule="off-wire"),
    Plant("R583-3: the status consumer as a register's event control", "datapath",
          anchored(f"  logic probe_q;\n  always_ff @(posedge {RES_ACTIVE}) probe_q <= 1'b1;\n" + SINK),
          reaches(RES_ACTIVE, "u_probe_sink.a_i"), rule="off-wire"),
    Plant("R583-3: the status consumer on an input port whose name ends in _o", "datapath",
          anchored(f"  KL_probe_sink u_probe_sink (.a_o({RES_ACTIVE}));\n"), reaches(RES_ACTIVE, "u_probe_sink.a_o"),
          rule="off-wire"),
    # ---- the cone: further forms (round 5) ---------------------------------
    Plant("a relational <= in a case item label", "datapath",
          routed("  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    case (1'b1)\n"
                 f"      {TALKER_DECLARED} <= 1'b0: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n"
                 "  end\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a function's output argument", "datapath",
          routed("  function automatic logic probe_f(input logic a, output logic b);\n    b = a;\n    return 1'b0;\n"
                 "  endfunction\n  logic probe_w, probe_d;\n"
                 f"  always_comb probe_d = probe_f({TALKER_DECLARED}, probe_w);\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a task's output argument", "datapath",
          routed("  task automatic probe_t(input logic a, output logic b);\n    b = a;\n  endtask\n"
                 f"  logic probe_w;\n  always_comb probe_t({TALKER_DECLARED}, probe_w);\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a macro call's argument, the macro defined in an included file", SHAPE_INCLUDE,
          (("", "\n`define PROBE_M(x) (x)\n"),
           *anchored(f"  wire probe_q;\n  assign probe_q = `PROBE_M({TALKER_DECLARED});\n" + SINK)),
          reaches(TALKER_DECLARED, "u_probe_sink.a_i"), rule="off-wire"),
    Plant("the second assignment of a continuous assign list", "datapath",
          routed(f"  logic probe_a, probe_w;\n  assign probe_a = 1'b0, probe_w = {TALKER_DECLARED};\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a read carried to another target of its block", "datapath",
          routed(f"  logic probe_a, probe_w;\n  always_comb begin\n    probe_a = {TALKER_DECLARED};\n"
                 "    probe_w = probe_a;\n  end\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a struct member carrying the status consumer", "datapath",
          routed(f"  typedef struct packed {{ logic {TALKER_DECLARED}; }} probe_t;\n  probe_t probe_s;\n"
                 f"  assign probe_s.{TALKER_DECLARED} = {TALKER_DECLARED};\n"
                 f"  wire probe_w;\n  assign probe_w = probe_s.{TALKER_DECLARED};\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i"), rule="off-wire"),
    Plant("a status consumer written into a memory and read out of it", "datapath",
          anchored("  logic [1:0] probe_m [0:3];\n  logic [1:0] probe_i;\n  always_ff @(posedge axis_clk) begin\n"
                   f"    probe_i <= probe_i + 2'd1;\n    probe_m[probe_i] <= {{1'b0, {TALKER_DECLARED}}};\n  end\n"
                   "  wire [1:0] probe_q = probe_m[probe_i];\n" + SINK),
          reaches(TALKER_DECLARED, "u_probe_sink.a_i"), rule="memory"),
    Plant("a status consumer printed", "datapath",
          anchored(f"  always_ff @(posedge axis_clk) $display(\"%b\", {TALKER_DECLARED});\n"),
          reaches(TALKER_DECLARED, "which has no output"), rule="no-output-end"),
    Plant("a CSR block input outside the read-back face", "datapath",
          ((TLK_GATE, f"    .i_tlk_gate_v         (8'(aaf_stream_en_w) | 8'({TALKER_DECLARED})),"),),
          reaches(TALKER_DECLARED, "csr.i_tlk_gate_v"), rule="csr-readback"),
    Plant("a read-back port of another milan_csr cell", "datapath",
          anchored(f"  milan_csr u_probe_csr (.i_lwsrp_status({TALKER_DECLARED}));\n"),
          reaches(TALKER_DECLARED, "u_probe_csr.i_lwsrp_status"), rule="terminal-cell"),
    Plant("a wrapper input outside its answer face", "datapath",
          ((MAAP_INTERNAL, f"      .cfg_maap_internal_i     ({TALKER_DECLARED}),"),),
          reaches(TALKER_DECLARED, "pp_shadow.cfg_maap_internal_i"), rule="processor-face"),
    # ---- the procedural block: R582-4's and R583-4's probes ---------------
    *block_plants(TALKER_DECLARED),
    *block_plants(GSI_TKDCL),
    *beginless_plants(TALKER_DECLARED),
    *beginless_plants(GSI_TKDCL),
    # ---- the first hop: R583-4's probes -----------------------------------
    Plant("R583-4: a token-paste macro defined in an included file", EVENTS_INCLUDE,
          (("", "\n`define PROBE_CD(n) pp_cd_``n``_w\n"),
           *routed("  wire probe_w;\n  assign probe_w = `PROBE_CD(srp_over_limit);\n")),
          unmapped("probe_w"), rule="unmapped"),
    Plant("R583-4: the token-paste macro defined in the datapath (its control)", "datapath",
          routed("  `define PROBE_CD(n) pp_cd_``n``_w\n  wire probe_w;\n"
                 "  assign probe_w = `PROBE_CD(srp_over_limit);\n"),
          unmapped("probe_w"), rule="unmapped"),
    Plant("R583-4: a macro in an included file holding a hierarchical reference into the wrapper", EVENTS_INCLUDE,
          (("", "\n`define PROBE_H pp_shadow.srp_over_limit_o\n"),
           *routed("  wire probe_w;\n  assign probe_w = `PROBE_H;\n")),
          (YOSYS, "pp_shadow.srp_over_limit_o")),
    Plant("R583-4: a hierarchical reference into the wrapper (its control)", "datapath",
          routed("  wire probe_w;\n  assign probe_w = pp_shadow.srp_over_limit_o;\n"),
          (YOSYS, "pp_shadow.srp_over_limit_o")),
    Plant("R583-4: an escaped name holding // hides a read", "datapath",
          ((CRF_DECL, "  wire \\probe//w ;\n  assign \\probe//w = " + WIRE + ";\n" + CRF_DECL),
           (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~\\probe//w\n               ),")),
          (OPENER, "\\probe//"), rule="opener-guard"),
    Plant("an escaped name holding // drops a declaration's initialiser without an error", "datapath",
          ((CRF_DECL, "  wire \\probe//w = " + WIRE + "\n  ;\n" + CRF_DECL),),
          (OPENER, "\\probe//"), rule="opener-guard"),
    Plant("an escaped name holding /*", "datapath",
          ((CRF_DECL, "  wire \\probe/*w ;\n" + CRF_DECL),), (OPENER, "\\probe/*"), rule="opener-guard"),
    Plant("R583-4: escaped names holding a double quote around a read", "datapath",
          ((CRF_DECL, "  wire \\probe\"a ;\n  wire probe_w;\n  assign probe_w = " + WIRE + ";\n"
            "  wire \\probe\"b ;\n" + CRF_DECL),
           (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),")),
          unmapped("probe_w"), rule="unmapped"),
    Plant("R583-4: a second driver as the population net's declaration initialiser", "datapath",
          ((WIRE_DECL, f"  wire                       {WIRE} = 1'b0;"),),
          f"{WIRE} is driven by", rule="sole-driver"),
    Plant("R583-4: a second driver as a continuous assign (its control)", "datapath",
          ((CRF_DECL, f"  assign {WIRE} = 1'b0;\n" + CRF_DECL),),
          f"{WIRE} is driven by", rule="sole-driver"),
    # ---- the wrapper's class-D face -----------------------------------------
    Plant("a class-D port left unconnected", "datapath",
          ((OVER_LIMIT, "      .srp_over_limit_o        (),\n"),),
          "class-D port srp_over_limit_o is not connected", rule="port-connected"),
    Plant("a class-D port the instance omits", "datapath",
          ((OVER_LIMIT, ""),),
          "class-D port srp_over_limit_o is not connected", rule="port-connected"),
    Plant("a class-D port driving more than one net", "datapath",
          ((CLASS_A_PRIO, "      .srp_class_a_prio_o      ({probe_p_w, pp_cd_srp_class_a_prio_w[1:0]}),"),
           (CRF_DECL, "  wire probe_p_w;\n" + CRF_DECL)),
          "class-D port srp_class_a_prio_o drives pp_cd_srp_class_a_prio_w, probe_p_w, not one whole named net",
          rule="port-one-net"),
    Plant("a class-D port connected by an implicit .name, no net of its name", "datapath",
          ((OVER_LIMIT, "      .srp_over_limit_o,\n"),),
          (SV2V, 'implicit declaration of "srp_over_limit_o"')),
    Plant("a class-D output the census does not list", "wrapper",
          ((SHADOW_OVER_LIMIT, SHADOW_OVER_LIMIT + "    output logic                         srp_probe_level_o,\n"),),
          "the wrapper declares class-D output srp_probe_level_o, which CLASS_D_PORTS does not list",
          rule="face-listed"),
    Plant("a class-D output declared beside another, on one line", "wrapper",
          ((SHADOW_OVER_LIMIT, "    output logic                         srp_over_limit_o, srp_probe_level_o,\n"),),
          "the wrapper declares class-D output srp_probe_level_o, which CLASS_D_PORTS does not list",
          rule="face-listed"),
    Plant("a class-D output moved out of the face", "wrapper",
          ((SHADOW_EID, ""), (SHADOW_OBSERVABILITY, SHADOW_OBSERVABILITY + SHADOW_EID)),
          "CLASS_D_PORTS lists acmp_bound_eid_o, which the wrapper's class-D face does not declare",
          rule="face-declared"),
    # ---- forms the text census refused outright, now elaborated ------------
    Plant("a wildcard port connection", "datapath",
          routed("  wire probe_w;\n  KL_probe_all u_probe_all (.*);\n",
                 f"module KL_probe_all (input logic {WIRE}, output logic probe_w);\nendmodule\n"),
          unmapped(f"u_probe_all.{WIRE}"), rule="unmapped"),
    Plant("a hierarchical reference into the CSR block", "datapath",
          routed("  wire probe_w;\n  assign probe_w = csr.i_lwsrp_status[0];\n"), (YOSYS, "csr.i_lwsrp_status")),
    Plant("a hierarchical reference through a generate scope", "datapath",
          routed("  wire probe_w;\n  assign probe_w = g_probe[0].csr.i_lwsrp_status[0];\n"), YOSYS),
    Plant("a read written in an included file", SHAPE_INCLUDE,
          (("", f"\n`ifdef PROBE_IN_DATAPATH\n  wire probe_inc_w = {WIRE};\n`endif\n"),
           (SHAPE_LINE, f"`define PROBE_IN_DATAPATH\n{SHAPE_LINE}\n`undef PROBE_IN_DATAPATH"),
           *routed("  wire probe_w = probe_inc_w;\n")),
          unmapped("probe_inc_w"), rule="unmapped"),
    Plant("an include the front end cannot find", "datapath",
          ((CRF_DECL, '  `include "probe_missing.svh"\n' + CRF_DECL),),
          (SV2V, "probe_missing.svh")),
    # ---- the shapes: a branch the recipe's shape does not build ------------
    Plant("R583-5 S1: a read inside a generate branch only N_STREAMS > 1 builds", "datapath",
          routed(f"  wire probe_w;\n  if (N_STREAMS > 1) begin : g_probe_ns\n    assign probe_w = {WIRE};\n"
                 "  end else begin : g_probe_one\n    assign probe_w = 1'b0;\n  end\n"),
          unmapped("probe_w"), rule="shapes", at=(STREAMS,)),
    Plant("R583-5 S2: a read inside a generate loop with no iteration at one stream", "datapath",
          routed("  wire [7:0] probe_v;\n  assign probe_v[0] = 1'b0;\n"
                 "  for (genvar g = 1; g < 8; g++) begin : g_probe_l\n"
                 f"    if (g < N_STREAMS) begin : g_on\n      assign probe_v[g] = {WIRE};\n    end else begin : g_off\n"
                 "      assign probe_v[g] = 1'b0;\n    end\n  end\n  wire probe_w = |probe_v;\n"),
          unmapped("probe_v"), rule="shape-params", at=(STREAMS,)),
    Plant("R583-5 S3: a read inside a generate branch only LOOPBACK_P != 0 builds", "datapath",
          routed(f"  wire probe_w;\n  if (LOOPBACK_P != 0) begin : g_probe_lb\n    assign probe_w = {WIRE};\n"
                 "  end else begin : g_probe_nolb\n    assign probe_w = 1'b0;\n  end\n"),
          unmapped("probe_w"), rule="shape-params", at=(LOOPBACK,)),
    Plant("R582-5 arm B: a read inside if (N_STREAMS > 1) begin ... end", "datapath",
          routed(f"  wire probe_w;\n  if (N_STREAMS > 1) begin : g_probe_shape\n    assign probe_w = |{WIRE};\n"
                 "  end else begin : g_probe_shape_off\n    assign probe_w = 1'b0;\n  end\n"),
          unmapped("probe_w"), rule="shapes", at=(STREAMS,)),
    Plant("R582-5 arm E: a status consumer added to the g_aaf_stream_en loop's gate", "datapath",
          ((STREAM_GATE, STREAM_GATE.replace("lwsrp_stream_gate[gs]));",
                                             f"lwsrp_stream_gate[gs] & ~{TALKER_DECLARED}));")),),
          reaches(TALKER_DECLARED, "stream_en_i"), rule="shape-params", at=(STREAMS,)),
    Plant("a read inside a generate branch only a multi-stream shape's header builds", "datapath",
          routed(f"  wire probe_w;\n  if (ADP_TALKER_SRC_C > 1) begin : g_probe_hdr\n    assign probe_w = {WIRE};\n"
                 "  end else begin : g_probe_hdr_off\n    assign probe_w = 1'b0;\n  end\n"),
          unmapped("probe_w"), rule="shape-header", at=(STREAMS,)),
    Plant("a field read that reaches CSR read-back only in the multi-stream shapes", "datapath",
          ((CRF_DECL, "  wire probe_r;\n  if (N_STREAMS > 1) begin : g_probe_rb\n"
                      "    assign probe_r = |acmpl_stopped_v_w;\n  end else begin : g_probe_rb_off\n"
                      "    assign probe_r = 1'b0;\n  end\n" + CRF_DECL),
           (AVAIL_INDEX, "    .i_adp_available_index(adp_available_index ^ probe_r),")),
          ("the reads differ between the shapes",
           "pp_aecp_strm_started_w -> acmpl_stopped_v_w reaching csr, wire only in"),
          rule="same-across-shapes", at=("recipe", STREAMS)),
    # ---- one plant for each rule the probes above leave unplanted ----------
    Plant("R583-5 R1: a status consumer driven to a new datapath output", "datapath",
          ((OUTPUT, "  output wire        probe_o,\n" + OUTPUT),
           (CRF_DECL, f"  assign probe_o = |{TALKER_DECLARED};\n" + CRF_DECL)),
          reaches(TALKER_DECLARED, "the datapath output probe_o"), rule="output-is-wire"),
    Plant("R583-5 R2: a status consumer ORed into the answer face's change strobe", "datapath",
          ((AVB_CHG, f"  wire gsi_avb_chg_w = (|{TALKER_DECLARED}) | gsi_gm_chg_w"),),
          (ROW[TALKER_DECLARED][0], "counted as status, but it reaches the processor wrapper"),
          rule="status-not-processor"),
    Plant("a field read whose only wire is cut", "datapath",
          ((VLAN_EN, "    .vlan_en_i  (1'b0),"),),
          ("pp_cd_srp_tk_decl_state_w -> crft_class_a_w:", "as read on the wire, but it reaches no wire"),
          rule="field-on-wire"),
    Plant("a second driver of a net outside the population", "datapath",
          ((CRF_DECL, "  assign crft_class_a_w = 1'b0;\n" + CRF_DECL),),
          "crft_class_a_w has two drivers", rule="two-drivers"),
    Plant("two class-D ports driving one net", "datapath",
          ((DOMAIN_CHANGE, ".srp_domain_change_o     (pp_cd_srp_over_limit_w),"),),
          "class-D ports srp_domain_change_o and srp_over_limit_o drive one net, pp_cd_srp_over_limit_w",
          rule="ports-distinct"),
    Plant("the wrapper's cell renamed", "datapath",
          ((SHADOW_CELL, "    ) probe_shadow ("),),
          "the datapath holds KL_pp_shadow cell(s) ['probe_shadow']", rule="one-wrapper"),
    Plant("the CSR block's cell renamed", "datapath",
          ((CSR_INST, "  ) probe_csr ("),),
          "the datapath holds no milan_csr cell named csr", rule="csr-cell"),
    Plant("a class-D output named again in a block comment of the port list", "wrapper",
          ((SHADOW_OBSERVABILITY, SHADOW_OBSERVABILITY + "    /* srp_active_o */\n"),),
          "the wrapper's port list declares output srp_active_o 2 times", rule="face-placed"),
    Plant("the started level's port renamed", "wrapper",
          ((STARTED_DECL, STARTED_DECL.replace("aecp_strm_started_o", "aecp_strm_live_o")),
           (STARTED_INNER, "      .aecp_strm_started_o (aecp_strm_live_o),")),
          "the wrapper declares no output aecp_strm_started_o", rule="started-port",
          also=((STARTED_CONN, "      .aecp_strm_live_o (pp_aecp_strm_started_w),"),)),
    # ---- the tools ----------------------------------------------------------
    Plant("an sv2v other than the pinned release", "toolchain", (("sv2v", "sv2v v0.0.13"),),
          ("the census elaborates with the pinned sv2v", "`sv2v v0.0.13`"), rule="pins"),
    Plant("a Yosys other than the pinned version", "toolchain", (("yosys", "Yosys 0.67 (git sha1 0000000)"),),
          ("the census elaborates with the pinned sv2v", "`Yosys 0.67`"), rule="pins"),
)


def apply(src: Any, plant: Plant) -> Any:
    """A copy of the census's Sources with the plant's edits made, or a string
    saying why they cannot be. An edit whose old text is empty appends to an
    included file; the plant's other edits go to the datapath, a wrapper
    plant's to the wrapper and its ``also`` to the datapath. A toolchain
    plant edits no source."""
    if plant.where == "toolchain":
        return src
    if plant.where in ("datapath", "wrapper"):
        out, edits = src, plant.edits
    else:
        copies = src.included.get(plant.where, ())
        if not copies:
            return f"the datapath includes no {plant.where} to plant into"
        (path, text), *rest = copies
        out = replace(src, included={**src.included, plant.where: ((path, text + plant.edits[0][1]), *rest)})
        edits = plant.edits[1:]
    for where, pairs in (("wrapper" if plant.where == "wrapper" else "datapath", edits), ("datapath", plant.also)):
        text = getattr(out, where)
        for old, new in pairs:
            if text.count(old) != 1:
                return f"its fixture occurs {text.count(old)} times in the {where}"
            text = text.replace(old, new, 1)
        out = replace(out, **{where: text})
    return out
