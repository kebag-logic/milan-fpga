# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_plants.py - the defects publication_census.py --selftest plants, each refused by its own words.

Each plant edits a copy of one source the census reads: the datapath, the
processor wrapper, or the first copy of a file the datapath includes. Every
edit's old text must occur exactly once, so a plant whose fixture moved fails
the self-test instead of passing it unplanted. The reviewers' probes are
R582-2's census_probes.py and R583-2's census_escape_probe.py (#665,
comment 6094461419), and R582-3's and R583-3's census_cone_probe.py (#665,
comment 6095903333), reproduced here form for form.

A plant's words are one string, or several that one finding must all carry:
a cone plant is refused by its read's row and by the occurrence that reaches
the wire.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

#: The class-D wire every probe reads, and the sites the plants anchor on.
WIRE = "pp_cd_srp_over_limit_w"
CRF_STAT = "    crft_stat_c[4]     = 1'b0;"
CRF_DECL = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
VLAN_EN = "    .vlan_en_i  (crft_class_a_w),"
OVER_LIMIT = "      .srp_over_limit_o        (pp_cd_srp_over_limit_w),\n"
DOMAIN_CHANGE = ".srp_domain_change_o     (pp_cd_srp_domain_change_w),"
STARTED_ACCEPT = ("  wire [ACMP_SINKS_C-1:0] acmpl_stopped_v_w = acmpl_bound_v_w\n"
                  "                                              & ~{};")
#: The wrapper's port list: a class-D output, one moved out of the face, and the next section.
SHADOW_OVER_LIMIT = ("    output logic                         srp_over_limit_o,        "
                     "//! a source was refused against the port ceiling\n")
SHADOW_EID = ("    output logic [N_STREAM_IN_P*64-1:0]  acmp_bound_eid_o,        "
              "//! per-sink bound talker entity_id\n")
SHADOW_OBSERVABILITY = "    //! ---- observability ----\n"
#: The included file the include plant writes into.
SHAPE_INCLUDE = "gen/adp_shape_defaults.svh"


def unaccounted(line: str) -> str:
    """The words refusing an occurrence of WIRE on the planted line that starts with `line`."""
    return f"unaccounted occurrence of {WIRE} at `{line}"


@dataclass(frozen=True)
class Plant:
    """One planted defect: the source it edits, its (old, new) edits, the words its finding must carry."""

    what: str
    where: str                              # "datapath", "wrapper" or "include"
    edits: tuple[tuple[str, str], ...]
    word: str | tuple[str, ...]


def routed(decl: str) -> tuple[tuple[str, str], ...]:
    """R583-2's probe shape: decl placed before the CRF talker's C-TAG enable,
    and probe_w ANDed into that talker's vlan_en_i, which is on the wire."""
    return ((CRF_DECL, decl + CRF_DECL), (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),"))


def anchored(decl: str) -> tuple[tuple[str, str], ...]:
    """R583-3's probe shape: decl placed before the CRF talker's C-TAG enable, routed nowhere else."""
    return ((CRF_DECL, decl + CRF_DECL),)


#: The status and answer-face consumers the cone plants route, and the row each read is keyed by.
TALKER_DECLARED = "lwsrp_talker_declared"
GSI_TKDCL = "gsi_tkdcl_w"
RES_ACTIVE = "lwsrp_res_active"
ROW = {TALKER_DECLARED: ("pp_cd_srp_tk_decl_state_w -> lwsrp_talker_declared (line", "status"),
       GSI_TKDCL: ("pp_cd_srp_tk_decl_state_w -> gsi_tkdcl_w (line", "processor"),
       RES_ACTIVE: ("pp_cd_srp_active_w -> lwsrp_res_active (line", "status")}
#: R583-3's sink: another module's input port, which is the wire.
SINK = "  KL_probe_sink u_probe_sink (.a_i(probe_q));\n"


def reaches(sig: str, end: str) -> tuple[str, str, str]:
    """The words refusing a cone plant: sig's read row, counted in its class, reaching the wire at end."""
    row, kind = ROW[sig]
    return row, f"counted as {kind}, but it reaches the wire at", end


def unclassified(line: str) -> str:
    """The end an occurrence the census cannot classify reaches, on the planted line starting with `line`."""
    return f"`{line}"


def cone_plants(sig: str) -> list[Plant]:
    """R582-3's part 1 forms, each routing sig onto the CRF talker's
    vlan_en_i, and R583-3's event control and _o-named input port, for one
    status or answer-face consumer."""
    return [
        Plant(f"R582-3: {sig} routed to the wire by a plain assign (its control)", "datapath",
              routed(f"  wire probe_w;\n  assign probe_w = {sig}[0];\n"), reaches(sig, "crf_tx.vlan_en_i")),
        Plant(f"R582-3: {sig} routed to the wire by a positional port", "datapath",
              routed(f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({sig}, probe_w);\n"),
              reaches(sig, unclassified(f"KL_probe_buf u_probe_pos ({sig}, probe_w);"))),
        Plant(f"R582-3: {sig} routed to the wire by an implicit .name port", "datapath",
              routed(f"  wire probe_w;\n  KL_probe_buf u_probe_dot (.{sig}, .y_o(probe_w));\n"),
              reaches(sig, unclassified(f"KL_probe_buf u_probe_dot (.{sig}, .y_o(probe_w));"))),
        Plant(f"R582-3: {sig} routed to the wire by a case item label", "datapath",
              routed("  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    unique case (1'b1)\n"
                     f"      {sig}[0]: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n  end\n"),
              reaches(sig, unclassified(f"{sig}[0]: probe_w = 1'b1;"))),
        Plant(f"R582-3: {sig} routed to the wire by a function body's return", "datapath",
              routed(f"  function automatic logic probe_f();\n    return {sig}[0];\n  endfunction\n"
                     "  wire probe_w;\n  assign probe_w = probe_f();\n"),
              reaches(sig, unclassified(f"return {sig}[0];"))),
        Plant(f"R583-3: {sig} as a register's event control", "datapath",
              anchored(f"  logic probe_q;\n  always_ff @(posedge {sig}) probe_q <= 1'b1;\n" + SINK),
              reaches(sig, unclassified(f"always_ff @(posedge {sig}) probe_q <= 1'b1;"))),
        Plant(f"R583-3: {sig} on an input port whose name ends in _o", "datapath",
              anchored(f"  KL_probe_sink u_probe_sink (.a_o({sig}));\n"), reaches(sig, "u_probe_sink.a_o")),
    ]


def on_crf(decl: str, term: str) -> tuple[tuple[str, str], ...]:
    """R582-2's probe shape: decl placed before the CRF talker's C-TAG enable, and term ANDed into it."""
    return ((CRF_DECL, decl + CRF_DECL.replace("=", f"= {term} &", 1)),)


PLANTS = (
    # ---- the census's own defects (round 3) ---------------------------------
    Plant("an unmapped read on the wire", "datapath",
          (("(|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]);",
            f"(|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]) & ~{WIRE};"),),
          f"unmapped read: {WIRE} -> crft_class_a_w"),
    Plant("an unmapped read in a declaration's initialiser", "datapath",
          ((CRF_DECL, "  wire planted_w = |pp_cd_srp_granted_slope_bps_w;\n"
                      + CRF_DECL.replace("=", "= planted_w &", 1)),),
          "unmapped read: pp_cd_srp_granted_slope_bps_w -> planted_w"),
    Plant("an unmapped read in an always block's condition", "datapath",
          ((CRF_STAT, CRF_STAT + "\n    if (pp_cd_srp_lstn_decl_state_w[0]) crft_stat_c[4] = 1'b1;"),),
          "unmapped read: pp_cd_srp_lstn_decl_state_w -> crft_stat_c"),
    Plant("a status read on the wire", "datapath",
          ((VLAN_EN, "    .vlan_en_i  (lwsrp_talker_declared),"),),
          "counted as status, but it reaches the wire"),
    Plant("a GET_STREAM_INFO read on the wire", "datapath",
          ((VLAN_EN, "    .vlan_en_i  (gsi_tkdcl_w[0]),"),),
          "counted as processor, but it reaches the wire"),
    Plant("the started level dropped from the accept", "datapath",
          ((STARTED_ACCEPT.format("pp_aecp_strm_started_w"), STARTED_ACCEPT.format("pp_cd_acmp_bound_w")),),
          "unmapped read: pp_cd_acmp_bound_w -> acmpl_stopped_v_w"),
    # ---- R582-2's probes ----------------------------------------------------
    Plant("R582-2: a class-D output wired off the pp_cd_ prefix and read on the wire", "datapath",
          ((DOMAIN_CHANGE, ".srp_domain_change_o     (probe_dom_chg_w),"),
           *on_crf("  wire probe_dom_chg_w;\n", "~probe_dom_chg_w")),
          "unmapped read: probe_dom_chg_w -> crft_class_a_w"),
    Plant("R582-2: an alias wire read on the wire", "datapath",
          on_crf(f"  wire probe_alias_w = {WIRE};\n", "~probe_alias_w"),
          f"unmapped read: {WIRE} -> probe_alias_w"),
    Plant("R582-2: a case selector in an always block", "datapath",
          ((CRF_STAT, CRF_STAT + f"\n    case ({WIRE}) 1'b1: crft_stat_c[4] = 1'b1; "
                                 "default: crft_stat_c[4] = 1'b0; endcase"),),
          f"unmapped read: {WIRE} -> crft_stat_c"),
    Plant("R582-2: a case item label in an always block", "datapath",
          ((CRF_STAT, CRF_STAT + f"\n    case (1'b1) {WIRE}: crft_stat_c[4] = 1'b1; "
                                 "default: crft_stat_c[4] = 1'b0; endcase"),),
          unaccounted(f"case (1'b1) {WIRE}: crft_stat_c[4] = 1'b1;")),
    Plant("R582-2: a function body called on the wire", "datapath",
          on_crf(f"  function automatic logic probe_f();\n    probe_f = {WIRE};\n  endfunction\n", "~probe_f()"),
          f"unmapped read: {WIRE} -> probe_f"),
    # ---- R583-2's probes ----------------------------------------------------
    Plant("R583-2: a plain assign on the wire (its control)", "datapath",
          routed(f"  wire probe_w;\n  assign probe_w = {WIRE};\n"),
          f"unmapped read: {WIRE} -> probe_w"),
    Plant("R583-2: a case item label in an always_comb", "datapath",
          routed("  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    unique case (1'b1)\n"
                 f"      {WIRE}: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n  end\n"),
          unaccounted(f"{WIRE}: probe_w = 1'b1;")),
    Plant("R583-2: a positional port connection", "datapath",
          routed(f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({WIRE}, probe_w);\n"),
          unaccounted(f"KL_probe_buf u_probe_pos ({WIRE}, probe_w);")),
    Plant("R583-2: an implicit .name port connection", "datapath",
          routed(f"  wire probe_w;\n  KL_probe_buf u_probe_dot (.{WIRE}, .y_o(probe_w));\n"),
          unaccounted(f"KL_probe_buf u_probe_dot (.{WIRE}, .y_o(probe_w));")),
    Plant("R583-2: a function body's return", "datapath",
          routed(f"  function automatic logic probe_f();\n    return {WIRE};\n  endfunction\n"
                 "  wire probe_w;\n  assign probe_w = probe_f();\n"),
          unaccounted(f"return {WIRE};")),
    # ---- the cone, fail closed: R582-3's and R583-3's probes (round 5) ------
    *cone_plants(TALKER_DECLARED),
    *cone_plants(GSI_TKDCL),
    Plant("R582-3 part 2: a positional port naming a status consumer, its output unused", "datapath",
          anchored(f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({TALKER_DECLARED}, probe_w);\n"),
          reaches(TALKER_DECLARED, unclassified(f"KL_probe_buf u_probe_pos ({TALKER_DECLARED}, probe_w);"))),
    Plant("R583-3: a plain assign from the status consumer (its control)", "datapath",
          anchored(f"  wire probe_q;\n  assign probe_q = {RES_ACTIVE};\n" + SINK),
          reaches(RES_ACTIVE, "u_probe_sink.a_i")),
    Plant("R583-3: a case item label naming the status consumer", "datapath",
          anchored("  logic probe_q;\n  always_comb begin\n    case (1'b1)\n"
                   f"      {RES_ACTIVE}: probe_q = 1'b1;\n      default: probe_q = 1'b0;\n    endcase\n  end\n" + SINK),
          reaches(RES_ACTIVE, unclassified(f"{RES_ACTIVE}: probe_q = 1'b1;"))),
    Plant("R583-3: a function body returning the status consumer", "datapath",
          anchored(f"  function automatic logic probe_f(input logic x);\n    return {RES_ACTIVE};\n  endfunction\n"
                   "  wire probe_q = probe_f(1'b0);\n" + SINK),
          reaches(RES_ACTIVE, unclassified(f"return {RES_ACTIVE};"))),
    Plant("R583-3: the status consumer as a register's event control", "datapath",
          anchored(f"  logic probe_q;\n  always_ff @(posedge {RES_ACTIVE}) probe_q <= 1'b1;\n" + SINK),
          reaches(RES_ACTIVE, unclassified(f"always_ff @(posedge {RES_ACTIVE}) probe_q <= 1'b1;"))),
    Plant("R583-3: the status consumer on an input port whose name ends in _o", "datapath",
          anchored(f"  logic probe_q;\n  KL_probe_sink u_probe_sink (.a_o({RES_ACTIVE}));\n"),
          reaches(RES_ACTIVE, "u_probe_sink.a_o")),
    # ---- the cone, fail closed: further forms ------------------------------
    Plant("a relational <= in a case item label", "datapath",
          routed("  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    case (1'b1)\n"
                 f"      {TALKER_DECLARED} <= 1'b0: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n"
                 "  end\n"),
          reaches(TALKER_DECLARED, unclassified(f"{TALKER_DECLARED} <= 1'b0: probe_w = 1'b1;"))),
    Plant("a function's output argument", "datapath",
          routed("  function automatic logic probe_f(input logic a, output logic b);\n    b = a;\n    return 1'b0;\n"
                 "  endfunction\n  logic probe_w, probe_d;\n"
                 f"  always_comb probe_d = probe_f({TALKER_DECLARED}, probe_w);\n"),
          reaches(TALKER_DECLARED, unclassified(f"always_comb probe_d = probe_f({TALKER_DECLARED}, probe_w);"))),
    Plant("a task's output argument", "datapath",
          routed("  task automatic probe_t(input logic a, output logic b);\n    b = a;\n  endtask\n"
                 f"  logic probe_w;\n  always_comb probe_t({TALKER_DECLARED}, probe_w);\n"),
          reaches(TALKER_DECLARED, unclassified(f"always_comb probe_t({TALKER_DECLARED}, probe_w);"))),
    Plant("a macro call's argument, the macro defined outside the datapath", "datapath",
          anchored(f"  wire probe_d;\n  assign probe_d = `PROBE_M({TALKER_DECLARED});\n"),
          reaches(TALKER_DECLARED, unclassified(f"assign probe_d = `PROBE_M({TALKER_DECLARED});"))),
    Plant("the second assignment of a continuous assign list", "datapath",
          routed(f"  logic probe_a, probe_w;\n  assign probe_a = 1'b0, probe_w = {TALKER_DECLARED}[0];\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i")),
    Plant("a read in a block that also drives another target", "datapath",
          routed(f"  logic probe_a, probe_w;\n  always_comb begin\n    probe_a = {TALKER_DECLARED}[0];\n"
                 "    probe_w = 1'b0;\n  end\n"),
          reaches(TALKER_DECLARED, "crf_tx.vlan_en_i")),
    Plant("a member named like the status consumer", "datapath",
          routed(f"  wire probe_w;\n  assign probe_w = probe_s.{TALKER_DECLARED};\n"),
          reaches(TALKER_DECLARED, unclassified(f"assign probe_w = probe_s.{TALKER_DECLARED};"))),
    Plant("a CSR block input outside the read-back face", "datapath",
          anchored(f"  milan_csr u_probe_csr (.i_probe({TALKER_DECLARED}));\n"),
          reaches(TALKER_DECLARED, "u_probe_csr.i_probe")),
    Plant("a wrapper input outside its answer face", "datapath",
          ((OVER_LIMIT, OVER_LIMIT + f"      .cfg_probe_i             ({TALKER_DECLARED}),\n"),),
          reaches(TALKER_DECLARED, "pp_shadow.cfg_probe_i")),
    # ---- the wrapper's class-D face -----------------------------------------
    Plant("a class-D port left unconnected", "datapath",
          ((OVER_LIMIT, "      .srp_over_limit_o        (),\n"),),
          "class-D port srp_over_limit_o is left unconnected"),
    Plant("a class-D port the instance omits", "datapath",
          ((OVER_LIMIT, ""),),
          "class-D port srp_over_limit_o is not connected"),
    Plant("a class-D port connected to an expression", "datapath",
          ((OVER_LIMIT, f"      .srp_over_limit_o        ({WIRE}[0]),\n"),),
          "class-D port srp_over_limit_o is connected to an expression"),
    Plant("a class-D port connected by an implicit .name", "datapath",
          ((OVER_LIMIT, "      .srp_over_limit_o,\n"),),
          "the wrapper instance connects `.srp_over_limit_o`, which is not a named port connection"),
    Plant("a class-D output the census does not list", "wrapper",
          ((SHADOW_OVER_LIMIT, SHADOW_OVER_LIMIT + "    output logic                         srp_probe_level_o,\n"),),
          "the wrapper declares class-D output srp_probe_level_o, which CLASS_D_PORTS does not list"),
    Plant("a class-D output declared beside another, on one line", "wrapper",
          ((SHADOW_OVER_LIMIT, "    output logic                         srp_over_limit_o, srp_probe_level_o,\n"),),
          "the wrapper declares class-D output srp_probe_level_o, which CLASS_D_PORTS does not list"),
    Plant("a class-D output moved out of the face", "wrapper",
          ((SHADOW_EID, ""), (SHADOW_OBSERVABILITY, SHADOW_OBSERVABILITY + SHADOW_EID)),
          "CLASS_D_PORTS lists acmp_bound_eid_o, which the wrapper's class-D face does not declare"),
    # ---- the forms refused outright -----------------------------------------
    Plant("a wildcard port connection", "datapath",
          routed("  wire probe_w;\n  KL_probe_buf u_probe_all (.*);\n"),
          "a wildcard port connection (.*)"),
    Plant("a hierarchical reference into the wrapper", "datapath",
          routed("  wire probe_w;\n  assign probe_w = pp_shadow.srp_over_limit_o;\n"),
          "a hierarchical reference into pp_shadow"),
    Plant("a hierarchical reference into the CSR block", "datapath",
          routed("  wire probe_w;\n  assign probe_w = csr.i_lwsrp_status[0];\n"),
          "a hierarchical reference into csr"),
    Plant("a hierarchical reference through a generate scope", "datapath",
          routed("  wire probe_w;\n  assign probe_w = g_probe[0].csr.i_lwsrp_status[0];\n"),
          "a hierarchical reference into csr"),
    Plant("a macro token paste", "datapath",
          routed("  `define PROBE_CD(n) pp_cd_``n``_w\n"
                 "  wire probe_w;\n  assign probe_w = `PROBE_CD(srp_over_limit);\n"),
          "a macro token paste"),
    Plant("a second driver", "datapath",
          ((CRF_DECL, f"  assign {WIRE} = 1'b0;\n" + CRF_DECL),),
          unaccounted(f"assign {WIRE} = 1'b0;")),
    Plant("an included file naming a class-D wire", "include",
          ((SHAPE_INCLUDE, f"\n  wire probe_inc_w = {WIRE};\n"),),
          f"an included file names class-D wire {WIRE}"),
    Plant("an include the census cannot find", "datapath",
          ((CRF_DECL, '  `include "probe_missing.svh"\n' + CRF_DECL),),
          "the datapath includes probe_missing.svh, which the census cannot find"),
)


def apply(src: Any, plant: Plant) -> Any:
    """A copy of the census's Sources with the plant's edits made, or a string saying why they cannot be."""
    if plant.where == "include":
        rel, line = plant.edits[0]
        copies = src.included.get(rel, ())
        if not copies:
            return f"the datapath includes no {rel} to plant into"
        (path, text), *rest = copies
        return replace(src, included={**src.included, rel: ((path, text + line), *rest)})
    text = getattr(src, plant.where)
    for old, new in plant.edits:
        if text.count(old) != 1:
            return f"its fixture occurs {text.count(old)} times in the {plant.where}"
        text = text.replace(old, new, 1)
    return replace(src, **{plant.where: text})
