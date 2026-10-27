#!/usr/bin/env python3
"""Reviewer-owned probes for issue #206 on the processor's tb/pp_top GI section.

Reuses tb/pp_top/gsi_mutants.py's check_variant (each variant builds in its
own temporary source copy; the clone is never edited). Usage:

  TMPDIR=<scratch> python3 reviewer_probes.py <clone> <base_top.sv> <out> <verilator> <jobs> [name ...]

With names, only those variants run (results.json is then named
results-<first name>.json).

Variants:
  base-rtl            the head's tests over the base commit's top (must fail
                      with GI GATE lines)
  R-*                 extra reviewer mutants; each must fail at least one
                      named check prefix (any FAIL line counts; the run log
                      keeps every FAIL line for the report)
"""
import json
import sys
from pathlib import Path

clone, base_top, out, verilator, jobs = sys.argv[1:6]
only = sys.argv[6:]
sys.path.insert(0, str(Path(clone) / "tb/pp_top"))
sys.path.insert(0, str(Path(clone) / "tb/common"))
import gsi_mutants  # noqa: E402
from mutant_pool import in_order  # noqa: E402

top = "hdl/top/protocol_processor_top.sv"
head_text = (Path(clone) / top).read_text()
base_text = Path(base_top).read_text()
output = Path(out).resolve()
output.mkdir(parents=True, exist_ok=True)

GATE_BLOCK = ("      if (!gsi_settled_w) begin\n"
              "        case (gsi_sel_o)\n")
VARIANTS = [
    # the head's tests over the base RTL
    ("base-rtl", (top, head_text, base_text, 1), "GI GATE"),
    # only STREAM_ID_VALID cleared: the other two flags leak
    ("R-mask-sid-only", (top, "~64'h0000_0000_5200_0000", "~64'h0000_0000_4000_0000", 1),
     "GI GATE"),
    # an extra flag (BOUND 0x04000000) cleared too: other flags must be unchanged
    ("R-mask-overclears-bound", (top, "~64'h0000_0000_5200_0000", "~64'h0000_0000_5600_0000", 1),
     "GI"),
    # STREAM_FORMAT_VALID (0x80000000) cleared too: the one other flag the
    # harness integrator claims for an input
    ("R-mask-overclears-format", (top, "~64'h0000_0000_5200_0000", "~64'h0000_0000_D200_0000", 1),
     "GI"),
    # MSRP_ACC_LAT_VALID (0x20000000) cleared too
    ("R-mask-overclears-acclat", (top, "~64'h0000_0000_5200_0000", "~64'h0000_0000_7200_0000", 1),
     "GI"),
    # the flags placed in the upper half of the word (wrong lane)
    ("R-mask-wrong-lane", (top, "~64'h0000_0000_5200_0000", "~64'h5200_0000_0000_0000", 1),
     "GI GATE"),
    # selector 4 zeroed entirely while unsettled: the failure-code byte must survive
    ("R-sel4-fail-code-dropped", (top, "4'd4: aecp_gsi_data_w[63:16] = 48'd0;",
                                  "4'd4: aecp_gsi_data_w = 64'd0;", 1),
     "GI"),
    # settled decided from the acmpsta bits rather than pbsta
    ("R-status-wrong-field", (top, "(gsi_status_w[7:5] == pp_acmp_pkg::PB_COMPLETED_C);",
                              "(gsi_status_w[2:0] == pp_acmp_pkg::PB_COMPLETED_C);", 1),
     "GI GATE"),
    # settled read as PROBING_PASSIVE-or-better (>= 1)
    ("R-settled-ge-passive", (top, "(gsi_status_w[7:5] == pp_acmp_pkg::PB_COMPLETED_C);",
                              "(gsi_status_w[7:5] >= 3'd1);", 1),
     "GI GATE PASSIVE-STALE"),
    # the gate also applied to STREAM_OUTPUT words (stream_id zeroed for outputs)
    ("R-gate-leaks-to-output", (top, "    aecp_gsi_data_w = gsi_data_i;\n    if (gsi_input_w) begin\n",
                                "    aecp_gsi_data_w = gsi_data_i;\n"
                                "    if (!gsi_input_w && gsi_kind_o == 2'd0 && gsi_sel_o == 4'd2)\n"
                                "      aecp_gsi_data_w = 64'd0;\n"
                                "    if (gsi_input_w) begin\n", 1),
     ""),
    # the gate applied to selector 1 (stream_format) as well
    ("R-gate-hits-format", (top, GATE_BLOCK,
                            GATE_BLOCK + "          4'd1: aecp_gsi_data_w = 64'd0;\n", 1),
     ""),
]


def run(variant):
    name, edit, prefix, outdir, ver = variant
    # check_variant needs an expected line; run it with a never-matching name
    # and grade the transcript ourselves.
    try:
        rec = gsi_mutants.check_variant((name, edit, "\x00never", outdir, ver))
    except RuntimeError as exc:
        return {"variant": name, "error": str(exc)}
    log = (outdir / (name + "-run.log")).read_text()
    fails = [l for l in log.splitlines() if l.startswith("FAIL: ")]
    gate = [l for l in fails if prefix and l.startswith("FAIL: " + prefix)]
    complete = "[build default," in log
    return {"variant": name, "build_rc": rec["build_rc"], "run_rc": rec["run_rc"],
            "complete": complete, "fail_lines": len(fails),
            "fail_lines_matching_prefix": len(gate), "prefix": prefix,
            "first_fails": fails[:6],
            "tally": [l for l in log.splitlines() if "[build default," in l][-1:]}


units = [(n, e, p, output, verilator) for n, e, p in VARIANTS if not only or n in only]
assert not only or len(units) == len(only), "unknown variant name"
records = []
with in_order(run, units, int(jobs)) as results:
    for r in results:
        print(json.dumps(r), flush=True)
        records.append(r)
(output / ("results-%s.json" % only[0] if only else "results.json")).write_text(json.dumps(records, indent=2) + "\n")
