#!/usr/bin/env python3
"""Reviewer probes (R583-5) against the netlist publication census of PR #704.

usage: census_probes_r583_5.py REPO [JOBS]

Each probe plants text into an in-memory copy of milan_datapath.sv and runs
the census's own findings() (the census's files are never edited). Expected
outcomes are stated per probe: REFUSED means the census must report a
finding carrying the words; ACCEPTED means the census reports no finding
although a class-D value is read (a gap), printed so a reader can judge it.
"""
import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
sys.path.insert(0, str(repo / "sw/mailbox"))
import census_elab as ce  # noqa: E402
import publication_census as pc  # noqa: E402
import census_plants as cp  # noqa: E402

W = cp.WIRE                                   # pp_cd_srp_over_limit_w, a status-only class-D net
TD = cp.TALKER_DECLARED                       # lwsrp_talker_declared, a status consumer
ROUTE = cp.routed                             # decl before crft_class_a_w, probe_w ANDed into crf_tx.vlan_en_i
OUT_ANCHOR = "  output wire        o_desc_mem_req_valid,\n"
CHG = "  wire gsi_avb_chg_w = gsi_gm_chg_w"

PROBES = [
    # ---- shape: a read the elaborated shape prunes ------------------------------------------------
    ("S1 a read inside a generate branch taken only when N_STREAMS > 1 (the 4x4, 8ch and 8x8 shapes)",
     ROUTE(f"  wire probe_w;\n  if (N_STREAMS > 1) begin : g_probe_ns\n    assign probe_w = {W};\n"
           "  end else begin : g_probe_one\n    assign probe_w = 1'b0;\n  end\n"),
     "expect ACCEPTED (gap)", f"unmapped read: {W} -> probe_w"),
    ("S1c control: the same branch taken when N_STREAMS >= 1",
     ROUTE(f"  wire probe_w;\n  if (N_STREAMS >= 1) begin : g_probe_ns\n    assign probe_w = {W};\n"
           "  end else begin : g_probe_one\n    assign probe_w = 1'b0;\n  end\n"),
     "expect REFUSED", f"unmapped read: {W} -> probe_w"),
    ("S2 a read inside a generate loop with no iteration at N_STREAMS = 1",
     ROUTE(f"  wire [7:0] probe_v;\n  assign probe_v[0] = 1'b0;\n  for (genvar g = 1; g < 8; g++) begin : g_probe_l\n"
           f"    if (g < N_STREAMS) begin : g_on\n      assign probe_v[g] = {W};\n    end else begin : g_off\n"
           "      assign probe_v[g] = 1'b0;\n    end\n  end\n  wire probe_w = |probe_v;\n"),
     "expect ACCEPTED (gap)", f"unmapped read: {W}"),
    ("S3 a read gated by LOOPBACK_P (the loopback-lane shapes)",
     ROUTE(f"  wire probe_w;\n  if (LOOPBACK_P != 0) begin : g_probe_lb\n    assign probe_w = {W};\n"
           "  end else begin : g_probe_nolb\n    assign probe_w = 1'b0;\n  end\n"),
     "expect ACCEPTED (gap)", f"unmapped read: {W} -> probe_w"),
    ("S4 control: the same read masked by a constant expression of the shape, not a generate branch",
     ROUTE(f"  wire probe_w;\n  assign probe_w = {W} & (N_STREAMS > 1);\n"),
     "expect REFUSED", f"unmapped read: {W} -> probe_w"),
    # ---- rules the self-test may not plant --------------------------------------------------------
    ("R1 a status consumer driven to a new datapath output port",
     ((OUT_ANCHOR, "  output wire        probe_o,\n" + OUT_ANCHOR),
      (cp.CRF_DECL, f"  assign probe_o = {TD};\n" + cp.CRF_DECL)),
     "expect REFUSED", ("counted as status, but it reaches the wire at", "the datapath output probe_o")),
    ("R2 a status consumer into the wrapper's answer face (gsi_avb_chg_i)",
     ((CHG, f"  wire gsi_avb_chg_w = {TD} | gsi_gm_chg_w"),),
     "expect REFUSED", "counted as status, but it reaches the processor wrapper"),
]


def run(probe):
    what, edits, expect, words = probe
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    text = src.datapath
    for old, new in edits:
        if text.count(old) != 1:
            return what, expect, f"fixture occurs {text.count(old)} times: {old[:40]!r}", []
        text = text.replace(old, new, 1)
    known = pc.fields(pc.mailbox_model.load())
    try:
        got, _ = pc.findings(replace(src, datapath=text), pc.CENSUS, known)
    except ce.CensusError as exc:
        got = [f"the census cannot read it: {exc}"]
    ws = (words,) if isinstance(words, str) else words
    hit = [f for f in got if all(w in f for w in ws)]
    verdict = "REFUSED" if hit else ("REFUSED (other words)" if got else "ACCEPTED")
    return what, expect, verdict, got


if __name__ == "__main__":
    ce.recipe(); ce.tracked_openers()
    with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
        for what, expect, verdict, got in pool.map(run, PROBES):
            print(f"[{verdict}] {what} ({expect})")
            for f in got[:3]:
                print(f"    {f[:300]}")
