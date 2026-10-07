#!/usr/bin/env python3
"""Cross-check the published round-3 OOC receipts against the PR body's claims and
the reviewed head's blobs (no synthesis is run). usage: timing_receipt_audit.py REPO EVIDENCE_DIR"""
import json, subprocess, sys
from pathlib import Path
repo, ev = sys.argv[1], Path(sys.argv[2])
fin = json.load(open(ev / "measurement-m3final.json")); base = json.load(open(ev / "measurement-m3base.json"))
scope = json.load(open(ev / "rtl-scope-m3final.json")); ref = json.load(open(ev / "resource-reference-m3.json"))
blob = lambda rev, p: subprocess.run(["git", "-C", repo, "rev-parse", f"{rev}:{p}"], capture_output=True, text=True).stdout.strip()
claims = {"WNS_ns": 3.337, "TNS_ns": 0.0, "failing_setup": 0, "WHS_ns": 0.159, "max_levels": 16, "above_20": 0,
          "startpoints": 328, "u_pp_lut": 22478, "u_pp_ff": 18951, "own_lut_delta": -110, "own_ff_delta": 6,
          "base_WNS_ns": -3.562, "base_above_20": 146535, "base_max_levels": 51, "worst_arbiter_slack": 11.912}
obs = {"WNS_ns": fin["timing"]["setup"]["worst_slack_ns"], "TNS_ns": fin["timing"]["setup"]["total_violation_ns"],
       "failing_setup": fin["timing"]["setup"]["failing_endpoints"], "WHS_ns": fin["timing"]["hold"]["worst_slack_ns"],
       "max_levels": fin["cone"]["max_levels"], "above_20": fin["cone"]["above_20"],
       "startpoints": fin["cone"]["queried_startpoints"], "u_pp_lut": fin["area"]["u_pp"]["lut"], "u_pp_ff": fin["area"]["u_pp"]["ff"],
       "own_lut_delta": (fin["area"]["(u_pp)"]["lut"] - base["area"]["(u_pp)"]["lut"]) + (fin["area"]["u_tx_arbiter"]["lut"] - base["area"]["u_tx_arbiter"]["lut"]),
       "own_ff_delta": (fin["area"]["(u_pp)"]["ff"] - base["area"]["(u_pp)"]["ff"]) + (fin["area"]["u_tx_arbiter"]["ff"] - base["area"]["u_tx_arbiter"]["ff"]),
       "base_WNS_ns": base["timing"]["setup"]["worst_slack_ns"], "base_above_20": base["cone"]["above_20"],
       "base_max_levels": base["cone"]["max_levels"], "worst_arbiter_slack": fin["cone"]["min_slack_ns"]}
hist = sum(int(v) for v in fin["cone"]["histogram"].values())
out = {"claims_vs_receipt": {k: {"claimed": claims[k], "receipt": obs[k], "match": claims[k] == obs[k]} for k in claims},
       "final_histogram_sum": hist, "final_pairs": fin["cone"]["pairs"],
       "histogram_levels_above_20": [k for k in fin["cone"]["histogram"] if int(k) > 20],
       "blobs": {"arbiter_receipt": scope["arbiter_blob"], "arbiter_head": blob("HEAD", "hdl/packet_engine/KL_pp_tx_arbiter.sv"),
                 "notify_receipt": scope["notify_blob"], "notify_head": blob("HEAD", "hdl/aecp/KL_aecp_notify.sv"),
                 "notify_new_main": blob("c9f74b6866a63dd3c0e4534724bfc07a86ad142b", "hdl/aecp/KL_aecp_notify.sv"),
                 "top_head": blob("HEAD", "hdl/top/protocol_processor_top.sv"), "top_in_receipt": None},
       "input_digests": {"stored_parent_reference_ooc_1x1": ref["original_record"]["inputs_sha256"],
                         "fresh_new_main_reference": ref["fresh_record"]["inputs_sha256"],
                         "final_measurement": None,
                         "fresh_flow": ref["fresh_record"]["identity"]["flow"], "stored_flow": ref["original_record"]["identity"]["flow"]}}
out["all_claims_match"] = all(v["match"] for v in out["claims_vs_receipt"].values())
out["blobs_match"] = out["blobs"]["arbiter_receipt"] == out["blobs"]["arbiter_head"] and out["blobs"]["notify_receipt"] == out["blobs"]["notify_head"]
print(json.dumps(out, indent=1))
