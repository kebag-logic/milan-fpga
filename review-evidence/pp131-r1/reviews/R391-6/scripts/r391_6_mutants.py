#!/usr/bin/env python3
"""Reviewer mutants R391-6 (disposable). Each entry is a list of exact edits
(path, old, new); every old text must occur exactly once in the tree.

Carries every R391-5 edit unchanged (r391_5_mutants.py, same directory) and adds:
- an arbiter variant of the owned cross term that arms only in the first owned
  clock of manager 0's READ (a narrower form of cross_own_m1_drains_m0);
- four harness/tap edits of tb/acmp_nvm that weaken N11d's stimulus or its
  bookkeeping, each of which N11d's own non-vacuity terms must catch;
- a print-only arbiter monitor that reports, per READ manager 0 OWNS in the
  arbiter's own state (own_r == O_M0, !we_r), how many owned clocks it had,
  how many of them carried manager 1's abort, and whether its issue clock did.
"""
import importlib.util
import os

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("r391_5_mutants", os.path.join(_here, "r391_5_mutants.py"))
_m5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m5)

MUTANTS = dict(_m5.MUTANTS)
ARB, ARM, arm = _m5.ARB, _m5.ARM, _m5.arm
ISS0, ISS1, OWN1 = _m5.ISS0, _m5.ISS1, _m5.OWN1
SIM = "tb/acmp_nvm/sim_main.cpp"
WRAP = "tb/acmp_nvm/acmp_nvm_wrap.sv"

# ---- arbiter: manager 1's abort drains the READ manager 0 owns, first owned clock only
MUTANTS["cross_own_m1_drains_m0_first_clk"] = [(ARB, ARM,
    "  logic r391_prev_own0_r;\n"
    "  always_ff @(posedge clk_i) r391_prev_own0_r <= rst_n && (own_r == O_M0);\n"
    "  assign arm0_w = " + ISS0 + "\n"
    "                  || ((own_r == O_M0) && !we_r && (m0_abort_i || (m1_abort_i && !r391_prev_own0_r)));\n"
    "  assign arm1_w = " + ISS1 + " || " + OWN1 + ";\n")]

# ---- harness: N11d's stimulus never presented (the drive term removed)
MUTANTS["h_n11d_no_drive"] = [(SIM,
    "                    || (m1_abort_over_m0 && m0_rd_own)\n", "")]
# ---- harness: the abort presented in every other owned clock only
MUTANTS["h_n11d_half_drive"] = [(SIM,
    "                    || (m1_abort_over_m0 && m0_rd_own)\n",
    "                    || (m1_abort_over_m0 && m0_rd_own && (cycles % 2 == 0))\n")]
# ---- harness: the abort also presented in manager 0's issue clock (N11b's term)
MUTANTS["h_n11d_also_issue"] = [(SIM,
    "                    || (m1_abort_over_m0 && m0_rd_own)\n",
    "                    || (m1_abort_over_m0 && (m0_rd_own || (d->mgr_req_o && !d->mgr_we_o)))\n")]
# ---- tap: the owned span never ends (arb_end_o stuck low)
MUTANTS["t_arb_end_stuck0"] = [(WRAP,
    "  assign arb_end_o        = np_done_w || np_err_w;\n",
    "  assign arb_end_o        = 1'b0;\n")]

# ---- print-only monitor of manager 0's owned READs in the arbiter's own state
MON_ANCHOR = "  assign dbg_drain_o = drain_r;\n"
MON = MON_ANCHOR + (
    "  // synthesis translate_off\n"
    "  int r391_span, r391_ab, r391_iss_ab, r391_early_ab;\n"
    "  initial begin r391_span = 0; r391_ab = 0; r391_iss_ab = 0; r391_early_ab = 0; end\n"
    "  always @(posedge clk_i) if (rst_n) begin\n"
    "    if (iss0_w && !m0_we_i) begin\n"
    "      r391_span <= 0; r391_ab <= 0; r391_early_ab <= 0; r391_iss_ab <= int'(m1_abort_i);\n"
    "    end else if ((own_r == O_M0) && !we_r) begin\n"
    "      if (end_w) $display(\"R391OWN0 t=%0t owned=%0d m1ab=%0d m1ab_before_end=%0d iss_m1ab=%0d drain=%0d\",\n"
    "                          $time, r391_span + 1, r391_ab + int'(m1_abort_i), r391_early_ab, r391_iss_ab, drain_r);\n"
    "      else begin r391_span <= r391_span + 1; r391_ab <= r391_ab + int'(m1_abort_i);\n"
    "                 r391_early_ab <= r391_early_ab + int'(m1_abort_i); end\n"
    "    end\n"
    "  end\n"
    "  // synthesis translate_on\n")
MUTANTS["mon_own0_reads"] = [(ARB, MON_ANCHOR, MON)]

# ---- diagnostic twin of h_n11d_also_issue: the same stimulus edit, and N11d's
# message prints the issue-cycle count it checks (m0_rd_issues_m1_abort) where
# the head's text reads "none"
MUTANTS["h_n11d_also_issue_diag"] = MUTANTS["h_n11d_also_issue"] + [(SIM,
    "and in none of their %d issue cycles, none drained \"\n"
    "          \"(from %ld), and the walk completes as saved: %s %s\", tag, m0_own_cyc_m1_abort,\n"
    "          m0_own_cyc, m0_own_rds, m0_own_span_min, m0_rd_issues, drain_on, why.c_str(),\n",
    "and in %d of their %d issue cycles, none drained \"\n"
    "          \"(from %ld), and the walk completes as saved: %s %s\", tag, m0_own_cyc_m1_abort,\n"
    "          m0_own_cyc, m0_own_rds, m0_own_span_min, m0_rd_issues_m1_abort, m0_rd_issues, drain_on, why.c_str(),\n")]
