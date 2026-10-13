#!/usr/bin/env python3
"""Repeat the retained-reset sensitivity checks in a disposable checkout."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("disposable_checkout", type=Path)
a = p.parse_args()
packet = Path(__file__).resolve().parent
root = a.disposable_checkout.resolve()
assert root.is_relative_to(packet / "scratch"), "Use only a disposable scratch checkout"
path = root / "hdl/ieee1722/crf/KL_crf_rx.sv"
original = path.read_bytes()
text = original.decode()
start = text.index("      if (w_bind_rise_w) begin")
names = ["pdu_count_o", "fmt_err_o", "seq_err_o", "mr_cnt_o", "tu_cnt_o",
         "late_cnt_o", "early_cnt_o", "cnt_locked_o", "cnt_unlocked_o", "cnt_intr_o",
         "iv_uf_r", "iv_sm_r", "iv_mr_r", "iv_tu_r", "iv_lt_r", "iv_et_r"]
results = []
try:
    for name in names:
        tail, count = re.subn(r"(?m)^\s*" + re.escape(name) + r"\s*<=\s*(?:'0|1'b0);\n",
                              "\n", text[start:], count=1)
        assert count == 1, name
        path.write_text(text[:start] + tail)
        with (packet / ("contract-remove-" + name + ".log")).open("w") as log:
            result = subprocess.run([sys.executable, "-B", str(packet / "prior-probes/reproduce_contract.py"),
                                     str(root)], stdout=log, stderr=subprocess.STDOUT)
        results.append({"removed": name, "rc": result.returncode})
        assert result.returncode == 1, results[-1]
finally:
    path.write_bytes(original)
(packet / "contract-mutations.json").write_text(json.dumps(results, indent=2) + "\n")
