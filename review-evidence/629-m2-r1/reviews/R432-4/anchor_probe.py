#!/usr/bin/env python3
"""Reviewer probe: every control anchor of the five milan_dp campaigns.

For each (campaign, control, file, anchor) edit it reports how many times the
anchor occurs in its target source, the line span it covers, whether that span
touches the reshaped restart request in milan_datapath.sv, and whether it
touches a line the lane changed since its base. It imports the campaigns'
own tables, so it reads the same strings the campaigns plant.

Usage: python3 anchor_probe.py <repo> <lane-base-sha>
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
base = sys.argv[2]
dp = repo / "tb/verilator/milan_dp"
sys.path.insert(0, str(dp))
sys.path.insert(0, str(repo / "scripts"))

import gmstep_mutants as gm  # noqa: E402
import render_mutants as rm  # noqa: E402
import crflic_mutants as cm  # noqa: E402
import gsi_mutants as gs  # noqa: E402

DP = repo / "hdl/milan/milan_datapath.sv"
CSR = repo / "hdl/common/csr/milan_csr.sv"
PP = repo / "protocol-processor/hdl/top/protocol_processor_top.sv"


def changed_lines(path: Path) -> set[int]:
    """Post-image line numbers the lane added or changed since `base`."""
    rel = path.relative_to(repo)
    if str(rel).startswith("protocol-processor/"):
        return set()
    out = subprocess.run(["git", "-C", str(repo), "diff", "-U0", base, "HEAD", "--", str(rel)],
                         capture_output=True, text=True, check=True).stdout
    lines: set[int] = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, count = int(m.group(1)), int(m.group(2) or "1")
        lines.update(range(start, start + count))
    return lines


def span(text: str, anchor: str) -> tuple[int, int] | None:
    i = text.find(anchor)
    if i < 0:
        return None
    first = text.count("\n", 0, i) + 1
    last = first + anchor.rstrip("\n").count("\n")
    return first, last


dp_text = DP.read_text()
req = span(dp_text, gm.RESTART_DECL)
assert req is not None, "the restart request declaration is not where the campaign says"
req_lines = set(range(req[0], req[1] + 1))

edits = []  # (campaign, control, path, anchor)
for c in gm.CONTROLS:
    edits.append(("gmstep", c.name, gm.SOURCES[c.source].resolve(), c.anchor))
for name, src, pat, _rep, _mode, _chk in rm.MUTATIONS:
    edits.append(("render", name, rm.SOURCES[src][0].resolve(), pat))
for name, frag, _rep, _chk in cm.MUTATIONS:
    edits.append(("crflic", name, cm.DP_RTL.resolve(), frag))
for name, plants, _chk in gs.MUTATIONS:
    for f, frag, _rep in plants:
        edits.append(("gsi", name, PP if f == "pp" else DP, frag))
# render_csr_controls.py keeps its anchors inline; read them from its source
csr_src = (dp / "render_csr_controls.py").read_text()
tree = ast.parse(csr_src)
consts = {n.targets[0].id: n.value.value for n in ast.walk(tree)
          if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
          and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)}
edits.append(("render-csr", "wrong_fill", DP, consts["pattern"]))
edits.append(("render-csr", "bit9_window_selection", CSR, consts["selector"]))
edits.append(("render-csr", "absent_stage (start)", DP, "  KL_render_setpoint #(\n"))
edits.append(("render-csr", "absent_stage (end)", DP, "  //! the whole render map"))

cache: dict[Path, tuple[str, set[int]]] = {}
bad = 0
print(f"restart request mcr_restart_p_w: milan_datapath.sv:{req[0]}-{req[1]}")
print("campaign | control | file | occurrences | lines | in request | on lane-changed line")
for camp, name, path, anchor in edits:
    if path not in cache:
        cache[path] = (path.read_text(), changed_lines(path))
    text, lane = cache[path]
    n = text.count(anchor)
    s = span(text, anchor)
    lines = set(range(s[0], s[1] + 1)) if s else set()
    in_req = bool(path == DP and lines & req_lines)
    on_lane = bool(lines & lane)
    if n != 1 and not (camp == "render-csr" and "absent_stage" in name and n >= 1):
        bad += 1
    print(f"{camp} | {name} | {path.relative_to(repo)} | {n} | "
          f"{s[0]}-{s[1] if s else ''} | {'YES' if in_req else 'no'} | {'YES' if on_lane else 'no'}"
          if s else f"{camp} | {name} | {path.relative_to(repo)} | {n} | - | - | -")
print(f"{len(edits)} edits; {len({(c, n) for c, n, _, _ in edits})} controls; "
      f"{bad} anchor(s) not found exactly once")
sys.exit(1 if bad else 0)
