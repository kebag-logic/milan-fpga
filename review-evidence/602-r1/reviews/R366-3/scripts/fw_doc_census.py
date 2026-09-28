#!/usr/bin/env python3
"""R366-3: check docs/integration/BAREMETAL_FIRMWARE.md's PHC re-base/restart
census rows against the committed RTL and the builder's pinned census.

Read-only. Usage: fw_doc_census.py <clone>
Counts code references (comments stripped) of each net in milan_datapath.sv,
extracts each named initializer, and prints the doc rows and builder pins
beside them. Exit 1 on any disagreement.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
dp = (root / "hdl/milan/milan_datapath.sv").read_text()
doc = (root / "docs/integration/BAREMETAL_FIRMWARE.md").read_text().splitlines()
tb = (root / "sw/builder/test_builder.py").read_text()

code = re.sub(r"/\*.*?\*/", " ", dp, flags=re.S)
code = re.sub(r"//[^\n]*", "", code)


def refs(net: str) -> int:
    return len(re.findall(rf"\b{re.escape(net)}\b", code))


def initializer(net: str) -> str:
    m = re.search(rf"wire\s+{net}\s*=\s*(.*?);", code, flags=re.S)
    return " ".join(m.group(1).split()) if m else "<none>"


bad = 0
expect_doc = {"media_rebase_p_w": 2, "mcr_restart_p_w": 2,
              "eff_ptp_adjust_w": 3, "cfg_ptp_cmd_load": 5}
for net, n in expect_doc.items():
    got = refs(net)
    pin = re.search(rf'"{net}": (\d+),', tb)
    pin_n = int(pin.group(1)) if pin else None
    ok = got == n == pin_n
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {net}: RTL code refs={got} doc={n} builder_pin={pin_n}")

for net, want in (("media_rebase_p_w", "eff_ptp_adjust_w | cfg_ptp_cmd_load"),
                  ("mcr_restart_p_w",
                   "crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)")):
    got = initializer(net)
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {net} initializer: {got!r}")

rr = [m.start() for m in re.finditer(r"\brender_recentre_p_w\b", code)]
print(f"render_recentre_p_w initializer: {initializer('render_recentre_p_w')!r}")
print("media_rebase_p_w reference contexts:")
for m in re.finditer(r"\bmedia_rebase_p_w\b", code):
    line = code.count("\n", 0, m.start()) + 1
    print(f"  milan_datapath.sv:{line}: {dp.splitlines()[line - 1].strip()}")
print("mcr_restart_p_w reference contexts:")
for m in re.finditer(r"\bmcr_restart_p_w\b", code):
    line = code.count("\n", 0, m.start()) + 1
    print(f"  milan_datapath.sv:{line}: {dp.splitlines()[line - 1].strip()}")

print("doc rows:")
for i, ln in enumerate(doc, 1):
    if re.match(r"\| `(media_rebase_p_w|mcr_restart_p_w|render_recentre_p_w|cfg_ptp_cmd_load)`", ln):
        print(f"  BAREMETAL_FIRMWARE.md:{i}: {ln}")
row = [ln for ln in doc if ln.startswith("| `mcr_restart_p_w` is exactly")]
doc_expr = re.search(r"is exactly `(.*?)` \|", row[0]).group(1).replace("\\|", "|") if row else ""
ok = doc_expr == initializer("mcr_restart_p_w")
bad += not ok
print(f"{'OK ' if ok else 'BAD'} doc mcr_restart_p_w expression equals the RTL initializer")
ok = bool(row) and "media_rebase_p_w" not in row[0] and "#602" in row[0]
bad += not ok
print(f"{'OK ' if ok else 'BAD'} doc mcr_restart_p_w row has no PHC-step term and cites #602")
mrow = [ln for ln in doc if ln.startswith("| `media_rebase_p_w` has exactly")]
ok = bool(mrow) and "two references" in mrow[0] and "#602" in mrow[0] and "mcr_restart_p_w" not in mrow[0]
bad += not ok
print(f"{'OK ' if ok else 'BAD'} doc media_rebase_p_w row says two references, names only the render reader, cites #602")
print(f"disagreements: {bad}")
sys.exit(1 if bad else 0)
