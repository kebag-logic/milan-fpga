#!/usr/bin/env python3
"""Reviewer mutants R391-5 (disposable). Each entry is a list of exact edits
(path, old, new); every old text must occur exactly once in the tree.

R391-5 re-plants R391-4's six issue-cycle mutants against the arbiter's drain
at the round-5 head (9dce84e, no RTL change) and adds single-half variants:
each rule of the arbiter's banner mutated for ONE manager only, so that the
report can say which halves the in-tree benches grade (manager 1 is driven
freely by tb/acmp_nvm N10/N11; manager 0 is the real binding manager in both
tb/acmp_nvm and tb/pp_top).
"""

ARB = "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv"
ARM = ("  assign arm0_w = (iss0_w && !m0_we_i && m0_abort_i)\n"
       "                  || ((own_r == O_M0) && !we_r && m0_abort_i);\n"
       "  assign arm1_w = (iss1_w && !m1_we_i && m1_abort_i)\n"
       "                  || ((own_r == O_M1) && !we_r && m1_abort_i);\n")


def arm(a0, a1):
    return [(ARB, ARM, "  assign arm0_w = %s;\n  assign arm1_w = %s;\n" % (a0, a1))]


ISS0 = "(iss0_w && !m0_we_i && m0_abort_i)"
ISS1 = "(iss1_w && !m1_we_i && m1_abort_i)"
OWN0 = "((own_r == O_M0) && !we_r && m0_abort_i)"
OWN1 = "((own_r == O_M1) && !we_r && m1_abort_i)"

MUTANTS = {
    # ---- R391-4's six, re-run ----
    "issue_arm_m1_only": arm(OWN0, ISS1 + " || " + OWN1),
    "issue_arm_m0_only": arm(ISS0 + " || " + OWN0, OWN1),
    "issue_arm_stale_we": arm("(iss0_w && !we_r && m0_abort_i) || " + OWN0,
                              "(iss1_w && !we_r && m1_abort_i) || " + OWN1),
    "issue_arm_cross_intent": arm("(iss0_w && !m0_we_i && (m0_abort_i || m1_abort_i)) || " + OWN0,
                                  "(iss1_w && !m1_we_i && (m0_abort_i || m1_abort_i)) || " + OWN1),
    "issue_arm_write_too": arm("(iss0_w && m0_abort_i) || " + OWN0,
                               "(iss1_w && m1_abort_i) || " + OWN1),
    "issue_arm_one_clock_late": [(ARB, ARM,
        "  logic iss_ab_r;\n"
        "  always_ff @(posedge clk_i) iss_ab_r <= rst_n && ((iss0_w && !m0_we_i && m0_abort_i)\n"
        "                                                || (iss1_w && !m1_we_i && m1_abort_i));\n"
        "  assign arm0_w = (own_r == O_M0) && !we_r && (m0_abort_i || iss_ab_r);\n"
        "  assign arm1_w = (own_r == O_M1) && !we_r && (m1_abort_i || iss_ab_r);\n")],
    # ---- R391-5: one half at a time ----
    # cross intent, one direction each
    # manager 1's abort drains manager 0's READ in its issue cycle (N11b's input)
    "cross_iss_m1_drains_m0": arm("(iss0_w && !m0_we_i && (m0_abort_i || m1_abort_i)) || " + OWN0,
                                  ISS1 + " || " + OWN1),
    # manager 0's abort drains manager 1's READ in its issue cycle (the input the
    # author states is ungraded by construction)
    "cross_iss_m0_drains_m1": arm(ISS0 + " || " + OWN0,
                                  "(iss1_w && !m1_we_i && (m1_abort_i || m0_abort_i)) || " + OWN1),
    # manager 1's abort drains the READ manager 0 OWNS (after its issue cycle)
    "cross_own_m1_drains_m0": arm(ISS0 + " || ((own_r == O_M0) && !we_r && (m0_abort_i || m1_abort_i))",
                                  ISS1 + " || " + OWN1),
    # manager 0's abort drains the READ manager 1 OWNS
    "cross_own_m0_drains_m1": arm(ISS0 + " || " + OWN0,
                                  ISS1 + " || ((own_r == O_M1) && !we_r && (m1_abort_i || m0_abort_i))"),
    # a WRITE strobe with an abort arms the drain: one manager at a time
    "write_iss_m0_only": arm("(iss0_w && m0_abort_i) || " + OWN0, ISS1 + " || " + OWN1),
    "write_iss_m1_only": arm(ISS0 + " || " + OWN0, "(iss1_w && m1_abort_i) || " + OWN1),
    # an abort while a WRITE is owned cuts it: one manager at a time
    "write_own_m0_only": arm(ISS0 + " || ((own_r == O_M0) && m0_abort_i)", ISS1 + " || " + OWN1),
    "write_own_m1_only": arm(ISS0 + " || " + OWN0, ISS1 + " || ((own_r == O_M1) && m1_abort_i)"),
    # the issue cycle judged by the previous operation's we_r: one manager at a time
    "stale_we_m0_only": arm("(iss0_w && !we_r && m0_abort_i) || " + OWN0, ISS1 + " || " + OWN1),
    "stale_we_m1_only": arm(ISS0 + " || " + OWN0, "(iss1_w && !we_r && m1_abort_i) || " + OWN1),
}

# ---- R391-5 monitor (no behaviour change): prints a line for the first 20
# clocks of each kind in which either manager presents an input the in-tree
# benches leave ungraded for that manager (the harnesses never call final(),
# so no line of a kind means that kind never occurred in the run).
MON_ANCHOR = "  assign dbg_drain_o = drain_r;\n"
KINDS = (
    ("m0_abort_not_own_read", "m0_abort_i && !(iss0_w && !m0_we_i) && !((own_r == O_M0) && !we_r)"),
    ("m1_abort_not_own_read", "m1_abort_i && !(iss1_w && !m1_we_i) && !((own_r == O_M1) && !we_r)"),
    ("m0_abort_with_write", "m0_abort_i && ((iss0_w && m0_we_i) || ((own_r == O_M0) && we_r))"),
    ("m1_abort_with_write", "m1_abort_i && ((iss1_w && m1_we_i) || ((own_r == O_M1) && we_r))"),
    ("m0_issue_abort_after_write", "iss0_w && !m0_we_i && m0_abort_i && we_r"),
    ("m1_issue_abort_after_write", "iss1_w && !m1_we_i && m1_abort_i && we_r"),
    ("m0_abort_on_m1", "m0_abort_i && (iss1_w || (own_r == O_M1))"),
    ("m1_abort_on_m0", "m1_abort_i && (iss0_w || (own_r == O_M0))"),
)
MONITOR = MON_ANCHOR + "  // synthesis translate_off\n  int r391_n[0:%d];\n" % (len(KINDS) - 1)
MONITOR += "  initial for (int i = 0; i < %d; i++) r391_n[i] = 0;\n" % len(KINDS)
MONITOR += "  always @(posedge clk_i) if (rst_n) begin\n"
for k, (name, cond) in enumerate(KINDS):
    MONITOR += ("    if ((%s) && r391_n[%d] < 20) begin r391_n[%d] <= r391_n[%d] + 1; "
                "$display(\"R391MON %s at %%0t\", $time); end\n" % (cond, k, k, k, name))
MONITOR += "  end\n  // synthesis translate_on\n"
MUTANTS["mon_unreachable_inputs"] = [(ARB, MON_ANCHOR, MONITOR)]
