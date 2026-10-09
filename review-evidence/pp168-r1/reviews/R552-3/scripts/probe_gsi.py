#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable notification-trigger probes for the 06 section 7 delta review.

Usage: probe_gsi.py <repo> <rev> <variant> <scratch_root> <verilator> <jobs>

Extracts <rev> of <repo> with `git archive` into <scratch_root>/<variant>,
applies the variant's text edits (each edit must match exactly once), builds
tb/pp_top with the given Verilator and runs `--gsi-internal-only`. Prints
the edits applied and returns the simulator's exit code. The source clone
is only read.

Variants
  C0     unmodified head (control)
  P1     test-only: after RETRY-RETAIN, assert no push for the discovered
         retry, let a repeated double timeout leave ACTIVE/7 unchanged and
         assert no push, then settle on the next discovered retry probe
  P1M1   P1 plus RTL mutant M1: the pbsta/acmpsta compare fires on every
         listener record write (the "only on a committed change" premise)
  P2     test-only: from PRB_W_RESP with retained ACTIVE/7, re-bind to
         another talker with STREAMING_WAIT; expect exactly one push,
         ACTIVE/0 with SW, then stop the phase
  P2Xc   P2 with the pbsta/acmpsta compare term removed from stri_events
  P2Xs   P2 with the started/stopped term removed from stri_events
  P2Xcs  P2 with both listener terms removed (must fail: no push)
  P2T    P2 plus non-functional $display instrumentation of both listener
         terms per cycle (no logic change)
"""
import os
import subprocess
import sys
import tarfile
import io

TB = "tb/pp_top/gsi_internal.hpp"
TOP = "hdl/top/protocol_processor_top.sv"
LSN = "hdl/acmp/KL_pp_acmp_listener.sv"

RETAIN_OLD = """    const auto next_probe = probe(0, 5000);
    check_frame(query(0), "RETRY-RETAIN", 0, 2, 7, 0, 0, false);
    settle(0, next_probe);
"""

P1_NEW = """    const auto next_probe = probe(0, 5000);
    check_frame(query(0), "RETRY-RETAIN", 0, 2, 7, 0, 0, false);
    CHECK(input_uns(0, 0).empty(),
          "R552P discovered retry (A12, A5): no push");
    const auto dup = probe(0, 500);
    CHECK(!dup.empty() && dup == next_probe,
          "R552P repeat: exact duplicate probe");
    CHECK(input_uns(0, 700).empty(),
          "R552P repeated double timeout, ACTIVE/7 unchanged: no push");
    check_frame(query(0), "R552P-REPEAT", 0, 2, 7, 0, 0, false);
    const auto third = probe(0, 5000);
    CHECK(input_uns(0, 0).empty(),
          "R552P second discovered retry: no push");
    check_frame(query(0), "R552P-RETAIN-2", 0, 2, 7, 0, 0, false);
    settle(0, third);
"""

P2_NEW = """    const auto next_probe = probe(0, 5000);
    check_frame(query(0), "RETRY-RETAIN", 0, 2, 7, 0, 0, false);
    (void)next_probe;
    {
      const bool was = (io.d->aecp_strm_started_o >> 0) & 1;
      binding(0, true, talker(0) + 0x55, 0x0008);
      const auto uns = input_uns(0, 150);
      CHECK(was && !((io.d->aecp_strm_started_o >> 0) & 1),
            "R552P REBIND-RETAINED: started/stopped changed");
      CHECK(uns.size() == 1,
            "R552P REBIND-RETAINED: exactly one push, got %zu", uns.size());
      if (!uns.empty())
        check_frame(uns[0], "R552P-REBIND-RETAINED", 0, 2, 0, 0, 0, true,
                    true, true);
      check_frame(query(0), "R552P-REBIND-RETAINED", 0, 2, 0, 0, 0, false,
                  true, true);
      return;
    }
"""

M1 = (TOP,
      """        lstn_gsi_changed_r[lstn_recwr_sink_w] <=
            (lstn_gsi_status_r[lstn_recwr_sink_w] != lstn_gsi_status_w);""",
      """        lstn_gsi_changed_r[lstn_recwr_sink_w] <= 1'b1;""")

NO_CMP = (TOP, "          || lstn_gsi_changed_r[k]\n", "          || 1'b0\n")
NO_STRT = (TOP, "           && lstn_act_strt_chg_w && !lstn_act_strt_cmd_chg_w)\n",
           "           && 1'b0)\n")

TRACE = (TOP, "  assign aecp_lock_held_o = ntfy_lock_held_w;\n",
         "  assign aecp_lock_held_o = ntfy_lock_held_w;\n"
         "  // R552 disposable instrumentation: print each cycle either listener\n"
         "  // Table 5.22 term is high, with a free-running cycle count.\n"
         "  logic [63:0] r552_cyc_r;\n"
         "  always_ff @(posedge clk_i) begin\n"
         "    if (!rst_n) r552_cyc_r <= '0; else r552_cyc_r <= r552_cyc_r + 64'd1;\n"
         "    if (rst_n && ((|lstn_gsi_changed_r) || lstn_act_strt_chg_w))\n"
         "      $display(\"R552T cyc=%0d cmp=%b strt=%b strt_cmd=%b act_sink=%0d stri_in=%b\",\n"
         "               r552_cyc_r, lstn_gsi_changed_r, lstn_act_strt_chg_w,\n"
         "               lstn_act_strt_cmd_chg_w, lstn_act_sink_w, ntfy_stri_in_w);\n"
         "  end\n")

VARIANTS = {
    "C0": [],
    "P1": [(TB, RETAIN_OLD, P1_NEW)],
    "P1M1": [(TB, RETAIN_OLD, P1_NEW), M1],
    "P2": [(TB, RETAIN_OLD, P2_NEW)],
    "P2Xc": [(TB, RETAIN_OLD, P2_NEW), NO_CMP],
    "P2Xs": [(TB, RETAIN_OLD, P2_NEW), NO_STRT],
    "P2Xcs": [(TB, RETAIN_OLD, P2_NEW), NO_CMP, NO_STRT],
    "P2T": [(TB, RETAIN_OLD, P2_NEW), TRACE],
}


def main():
    repo, rev, variant, root, verilator, jobs = sys.argv[1:7]
    dest = os.path.join(root, variant)
    if os.path.exists(dest):
        sys.exit(f"refusing to reuse {dest}")
    os.makedirs(dest)
    blob = subprocess.run(["git", "-C", repo, "archive", rev],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as t:
        t.extractall(dest, filter="data")
    for path, old, new in VARIANTS[variant]:
        p = os.path.join(dest, path)
        text = open(p).read()
        n = text.count(old)
        if n != 1:
            sys.exit(f"{variant}: edit for {path} matched {n} times")
        open(p, "w").write(text.replace(old, new))
        print(f"applied edit to {path}", flush=True)
    mk = os.path.join(dest, "tb/pp_top/Makefile")
    text = open(mk).read()
    open(mk, "w").write(text.replace("--build -j 0", f"--build -j {jobs}"))
    tbdir = os.path.join(dest, "tb/pp_top")
    b = subprocess.run(["make", f"VERILATOR={verilator}", "gsi-build"],
                       cwd=tbdir)
    print(f"build rc={b.returncode}", flush=True)
    if b.returncode:
        return b.returncode
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"],
                       cwd=tbdir)
    print(f"sim rc={r.returncode}", flush=True)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
