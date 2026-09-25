#!/usr/bin/env python3
"""Reviewer probes on the #508 [GSI] G8 withdrawal grading (R306-2).

Reuses the lane's own gsi_mutants.py plant/build/run machinery (imported from
the clone under review, unmodified) so every probe is built by the suite's own
`make notify-build` recipe against a COPY of the processor hdl/ tree.

  P1  drop srp_evt_tk_unreg_w from stri_events      -> expect G8 exact count to fail
  P2  trace-only: print every sink-0 stri trigger    -> expect PASS; shows order
  P3  ungate the SRP bridge from registered FAILED  -> expect a G8 per-push
                                                       bridge-id check to fail
  P4  drop lstn_gsi_changed_r for sink 0 while a    -> expect G8 exact count to fail
      withdrawal happened in the last 64 cycles        (the second push is the
      (only the post-withdrawal teardown strobe)       settlement teardown's)

usage: g8_probes.py <clone>/tb/verilator/milan_dp [P1 P2 P3 P4]
Needs the pinned Verilator first on PATH; TMPDIR selects the work area.
"""
import sys, tempfile
from pathlib import Path

HERE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(HERE))
import gsi_mutants as gm  # noqa: E402

UNREG = "          || srp_evt_tk_reg_w[k] || srp_evt_tk_unreg_w[k]"
STRI = "  always_comb begin : stri_events"
LSTN = "          || lstn_gsi_changed_r[k]\n"
GATE = ("      if (srp_tk_reg_state_w[gsi_sink_w] == 2'd2) begin\n"
        "        gsi_fail_bridge_w = srp_snk_fail_bridge_w[gsi_sink_w];\n"
        "      end\n")
TRACE = """  logic [63:0] r306_cyc_r;
  always_ff @(posedge clk_i) begin : r306_trace
    if (!rst_n) r306_cyc_r <= '0;
    else begin
      r306_cyc_r <= r306_cyc_r + 64'd1;
      if (srp_evt_tk_unreg_w[0])   $display("R306TRACE cyc=%0d sink0 srp_evt_tk_unreg", r306_cyc_r);
      if (srp_evt_tk_reg_w[0])     $display("R306TRACE cyc=%0d sink0 srp_evt_tk_reg", r306_cyc_r);
      if (srp_evt_tk_fail_chg_w[0]) $display("R306TRACE cyc=%0d sink0 srp_evt_tk_fail_chg", r306_cyc_r);
      if (lstn_gsi_changed_r[0])   $display("R306TRACE cyc=%0d sink0 lstn_gsi_changed status=%02x", r306_cyc_r, lstn_gsi_status_r[0]);
      if (ntfy_stri_in_w[0])       $display("R306TRACE cyc=%0d sink0 ntfy_stri_in", r306_cyc_r);
    end
  end

"""
RECENT = """  logic [6:0] r306_recent_unreg_r;
  always_ff @(posedge clk_i) begin : r306_recent
    if (!rst_n) r306_recent_unreg_r <= '0;
    else if (srp_evt_tk_unreg_w[0]) r306_recent_unreg_r <= 7'd127;
    else if (r306_recent_unreg_r != 0) r306_recent_unreg_r <= r306_recent_unreg_r - 7'd1;
  end

"""
PROBES = {
    "P1": ("r306 P1 withdrawal trigger removed from stri_events",
           [("pp", UNREG, "          || srp_evt_tk_reg_w[k]")],
           "[GSI] G8 sink 0 withdrawn: unsolicited GET_STREAM_INFO(sink 0) to A"),
    "P2": ("r306 P2 trace only", [("pp", STRI, TRACE + STRI)], None),
    "P3": ("r306 P3 bridge id not gated on registered FAILED",
           [("pp", GATE, "      gsi_fail_bridge_w = srp_snk_fail_bridge_w[gsi_sink_w];\n")],
           "[GSI] G8 sink 0 registrar withdrawal to A: msrp_failure_bridge_id"),
    "P4": ("r306 P4 teardown strobe after a withdrawal suppressed on sink 0",
           [("pp", STRI, RECENT + STRI),
            ("pp", LSTN, "          || (lstn_gsi_changed_r[k] && !(k == 0 && r306_recent_unreg_r != 0))\n")],
           "[GSI] G8 sink 0 withdrawn: unsolicited GET_STREAM_INFO(sink 0) to A"),
}

rc = 0
with tempfile.TemporaryDirectory(prefix="r306-g8-") as td:
    work = Path(td)
    for key in (sys.argv[2:] or list(PROBES)):
        name, edits, must = PROBES[key]
        tag = key
        planted = gm.plant(name, edits, work, tag)
        if planted is None:
            print(f"[{key}] PATTERN MISMATCH"); rc = 1; continue
        exe = gm.build(planted[0], planted[1], work / f"obj_{tag}")
        if exe is None:
            print(f"[{key}] BUILD FAILED"); rc = 1; continue
        r, out = gm.run_leg(exe)
        (Path(__file__).resolve().parent / "receipts" / f"probe_{key}.log").write_text(out)
        v = gm.verdict(r, out, must)
        fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
        tally = [l for l in out.splitlines() if l.startswith("checks:")]
        print(f"[{key}] {name}: verdict={v} rc={r} {tally[-1] if tally else ''}")
        for l in fails[:12]:
            print(f"    {l.strip()[:160]}")
        want = "pass" if must is None else "caught"
        if v != want:
            rc = 1
print("probe driver rc", rc)
sys.exit(rc)
