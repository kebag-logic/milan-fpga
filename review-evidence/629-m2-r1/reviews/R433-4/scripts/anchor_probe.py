#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R433-4): every control anchor of the five milan_dp campaigns.

Usage: anchor_probe.py <checkout root> <lane base commit>

For each control it imports the campaign's own table, applies its edits in
order exactly as the campaign does (count == 1 before each replace), and
reports the 1-based line span of each anchor in the unmutated source, whether
that span overlaps the restart request `mcr_restart_p_w`, and whether it
overlaps a line this lane changed (git diff <base>..HEAD, new-side lines).
It also reports the planted request text for every control whose anchor lies
in the request. Read-only: nothing is written to the checkout.
"""
import importlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
DP = ROOT / "tb/verilator/milan_dp"
sys.path.insert(0, str(DP))
sys.path.insert(0, str(ROOT / "scripts"))


def changed_lines(path: Path) -> set[int]:
    rel = path.resolve().relative_to(ROOT)
    out = subprocess.run(["git", "-C", str(ROOT), "diff", "-U0", f"{BASE}..HEAD", "--", str(rel)],
                         capture_output=True, text=True, check=True).stdout
    lines: set[int] = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, n = int(m.group(1)), int(m.group(2) or "1")
        lines.update(range(start, start + n))
    return lines


def span(text: str, anchor: str) -> tuple[int, int]:
    i = text.index(anchor)
    a = text.count("\n", 0, i) + 1
    return a, a + anchor.count("\n") - (1 if anchor.endswith("\n") else 0)


DP_RTL = (ROOT / "hdl/milan/milan_datapath.sv").resolve()
dp_text = DP_RTL.read_text()
req_start = dp_text.index("  wire mcr_restart_p_w")
req_end = dp_text.index(";", req_start)
REQ = (dp_text.count("\n", 0, req_start) + 1, dp_text.count("\n", 0, req_end) + 1)
print(f"request mcr_restart_p_w at milan_datapath.sv:{REQ[0]}-{REQ[1]}")

rows = []  # (campaign, control, file, anchor, replacement)
rm = importlib.import_module("render_mutants")
for name, src, pat, rep, _mode, _brk in rm.MUTATIONS:
    rows.append(("render", name, [(rm.SOURCES[src][0], pat, rep)]))
rc = importlib.import_module("render_csr_controls")
rows.append(("render-csr", "wrong_fill", [(rc.DP_RTL, "rsp_fill_w[s*8 +: 8]};", "8'd0};")]))
rows.append(("render-csr", "bit9_window_selection",
             [(rc.CSR_RTL, "if (!strm_dir_r && (32'(strm_idx_r) == s))", None)]))
rows.append(("render-csr", "absent_stage (start)", [(rc.DP_RTL, "  KL_render_setpoint #(\n", None)]))
cm = importlib.import_module("crflic_mutants")
for name, pat, rep, _brk in cm.MUTATIONS:
    rows.append(("crflic", name, [(cm.DP_RTL, pat, rep)]))
gm = importlib.import_module("gsi_mutants")
for name, edits, _brk in gm.MUTATIONS:
    rows.append(("gsi", name, [((gm.DP_RTL if w == "dp" else gm.PP_HDL / gm.PP_TOP), p, r)
                               for w, p, r in edits]))
gs = importlib.import_module("gmstep_mutants")
for c in gs.CONTROLS:
    rows.append(("gmstep", c.name, [(gs.SOURCES[c.source], c.anchor, c.replacement)]))

cache: dict[Path, set[int]] = {}
n_anchor = bad = 0
for camp, name, edits in rows:
    texts: dict[Path, str] = {}
    for path, pat, rep in edits:
        path = path.resolve()
        orig = path.read_text()
        cur = texts.setdefault(path, orig)
        n = cur.count(pat)
        n_anchor += 1
        a, b = span(orig, pat) if orig.count(pat) == 1 else (0, 0)
        if path not in cache:
            cache[path] = changed_lines(path)
        lane = bool(cache[path] & set(range(a, b + 1)))
        in_req = path == DP_RTL and not (b < REQ[0] or a > REQ[1])
        if n != 1:
            bad += 1
        print(f"{camp:10s} | {name[:70]:70s} | {path.name}:{a}-{b} | count={n} "
              f"| in_request={'YES' if in_req else 'no'} | lane_changed={'YES' if lane else 'no'}")
        if rep is not None and n == 1:
            texts[path] = cur.replace(pat, rep)
        if in_req and rep is not None:
            t = texts[path]
            s = t.index("  wire mcr_restart_p_w")
            print("    planted request: " + " ".join(t[s:t.index(";", s) + 1].split()))
print(f"anchors: {n_anchor}; anchors not found exactly once: {bad}")
sys.exit(1 if bad else 0)
