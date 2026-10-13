#!/usr/bin/env python3
"""Predict per-worker wall clock under the candidate's suite_shards.balance,
using the per-suite maximum of the candidate table and a --measure output.

Usage: python3 -I predict_workers.py <candidate-repo> <measure-output.txt>
"""
import ast
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import suite_shards as ss  # noqa: E402

text = Path(sys.argv[2]).read_text()
measured = ast.literal_eval(re.search(r"SUITE_SECONDS = (\{.*?\})", text, re.S).group(1))
merged = {k: max(v, measured.get(k, 0)) for k, v in ss.SUITE_SECONDS.items()}
suites = ss.sweep_suites(repo / "tb" / "verilator")
limit = 120 * 60 * ss.HEADROOM_PERCENT // 100
for label, table in (("candidate table", ss.SUITE_SECONDS),
                     ("max(table, source-head measured)", merged)):
    _, pred = ss.balance(suites, 5, table)
    print(f"{label}: predicted worker seconds {pred}; max {max(pred)}; "
          f"60% of 120 min = {limit}; ok={max(pred) <= limit}")
for s in ("avtp_rxmon", "crf_rx", "milan_dp", "tkdiag"):
    print(f"{s}: table {ss.SUITE_SECONDS[s]} measured-at-source-head {measured[s]}")
