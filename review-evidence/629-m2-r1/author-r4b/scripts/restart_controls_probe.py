#!/usr/bin/env python3
"""Probe, outside the tree: every control of milan_dp's five mutation
campaigns (gmstep, render, crflic, gsi, render-csr) against the restart request this lane
reshaped in round 1. For each control it reports the anchor's count and line
span in its source at HEAD, whether the anchor lies inside the request
`mcr_restart_p_w`, and whether it overlaps a line this lane changed (git diff
-U0 <dev> HEAD). For every control that edits the request it renders the
planted declaration and compares its truth table with the clean request's
over every input, naming which terms the planted change actually gates.

Usage: python3 restart_controls_probe.py <tree> <dev-commit>"""
import ast
import importlib.util
import itertools
import re
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
DEV = sys.argv[2]
SUITE = TREE / "tb/verilator/milan_dp"
sys.path.insert(0, str(SUITE))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SUITE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


gm, rm, cm, gs = (load(n) for n in ("gmstep_mutants", "render_mutants",
                                    "crflic_mutants", "gsi_mutants"))
PP_TOP = (SUITE / gs.PP_HDL / gs.PP_TOP).resolve()


def changed_lines(path: Path) -> set[int]:
    """New-side line numbers this lane changed in `path` against DEV."""
    rel = path.resolve().relative_to(TREE)
    out = subprocess.run(["git", "-C", str(TREE), "diff", "-U0", DEV, "HEAD", "--", str(rel)],
                         capture_output=True, text=True, check=True).stdout
    lines: set[int] = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        lines.update(range(start, start + count))
    return lines


def span(text: str, anchor: str) -> tuple[int, int] | None:
    i = text.find(anchor)
    if i < 0:
        return None
    first = text.count("\n", 0, i) + 1
    return first, first + anchor.rstrip("\n").count("\n")


DP = (SUITE / gm.SOURCES["datapath"]).resolve()
DP_TEXT = DP.read_text()
REQ_START = DP_TEXT.index("  wire mcr_restart_p_w")
REQ_END = DP_TEXT.index(";", REQ_START) + 1
REQ_SPAN = (DP_TEXT.count("\n", 0, REQ_START) + 1, DP_TEXT.count("\n", 0, REQ_END) + 1)


def request_of(text: str) -> str:
    """The request's right-hand side in `text` (a planted datapath copy)."""
    start = text.index("  wire mcr_restart_p_w")
    rhs = text[text.index("=", start) + 1:text.index(";", start)]
    return " ".join(rhs.split())


def evaluate(expr: str, env: dict[str, int]) -> int:
    py = re.sub(r"~\s*(\w+)", r"(1 ^ \1)", expr)
    return eval(py, {}, dict(env)) & 1  # noqa: S307 - our own one-bit expression


def truth_diff(clean: str, planted: str) -> list[dict[str, int]]:
    names = sorted(set(re.findall(r"[A-Za-z_]\w*", clean + " " + planted)) | {"media_rebase_p_w"})
    rows = []
    for bits in itertools.product((0, 1), repeat=len(names)):
        env = dict(zip(names, bits))
        if evaluate(clean, env) != evaluate(planted, env):
            rows.append(env)
    return rows


rows = []
for c in gm.CONTROLS:
    rows.append(("gmstep", c.name, (SUITE / gm.SOURCES[c.source]).resolve(), c.anchor,
                 c.replacement, c.breaks))
# the same control as round 4 published it (c1288648), for the contrast
rows.append(("gmstep, as published at c1288648", "a PHC step suppresses a coincident CRF restart",
             DP, gm.RESTART_TRIGGER, gm.RESTART_TRIGGER[:-1] + " & ~media_rebase_p_w;",
             "coincident: a PHC step does not suppress the CRF restart"))
for name, source, pattern, replacement, _mode, breaks in rm.MUTATIONS:
    rows.append(("render", name, (SUITE / rm.SOURCES[source][0]).resolve(), pattern,
                 replacement, breaks))
for name, pattern, replacement, breaks in cm.MUTATIONS:
    rows.append(("crflic", name, DP, pattern, replacement, breaks))
for name, edits, breaks in gs.MUTATIONS:
    for where, pattern, replacement in edits:
        rows.append(("gsi", name, DP if where == "dp" else PP_TOP, pattern, replacement, breaks))

# render_csr_controls.py keeps its two anchors and the absent-stage cut inside
# main(): read them from its own text, not restated here
RCC = SUITE / "render_csr_controls.py"
rcc_names = {}
for node in ast.walk(ast.parse(RCC.read_text())):
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
            and isinstance(node.value.value, str) and len(node.targets) == 1 \
            and isinstance(node.targets[0], ast.Name):
        rcc_names[node.targets[0].id] = node.value.value
rcc_src = RCC.read_text()
CSR = (SUITE / "../../../hdl/common/csr/milan_csr.sv").resolve()
cut_start = re.search(r'source\.index\("(.*?)\\n"\)', rcc_src).group(1) + "\n"
cut_end = re.search(r'source\.index\("(.*?)", start\)', rcc_src).group(1)
cut = DP_TEXT[DP_TEXT.index(cut_start):DP_TEXT.index(cut_end, DP_TEXT.index(cut_start))]
rows.append(("render-csr", "wrong_fill", DP, rcc_names["pattern"], "8'd0};",
             "RENDER-CSR: filling mirrors taps"))
rows.append(("render-csr", "bit9_window_selection", CSR, rcc_names["selector"], "",
             "RENDER-CSR: bit 9 preserves talker rejection"))
rows.append(("render-csr", "absent_stage (the KL_render_setpoint instance, cut whole)", DP, cut, "",
             "(a pass with the CSR structurally zero)"))
print(f"tree {TREE} HEAD {subprocess.run(['git', '-C', str(TREE), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()}; lane delta against {DEV}")
print(f"request mcr_restart_p_w: {DP.name}:{REQ_SPAN[0]}-{REQ_SPAN[1]}: {request_of(DP_TEXT)}")
print()
cache: dict[Path, tuple[str, set[int]]] = {}
bad = 0
for campaign, name, path, anchor, replacement, breaks in rows:
    if path not in cache:
        cache[path] = (path.read_text(), changed_lines(path) if TREE in path.parents else set())
    text, lane = cache[path]
    count = text.count(anchor)
    sp = span(text, anchor)
    in_req = path == DP and sp is not None and not (sp[1] < REQ_SPAN[0] or sp[0] > REQ_SPAN[1])
    lane_hit = sp is not None and any(n in lane for n in range(sp[0], sp[1] + 1))
    where = f"{path.name}:{sp[0]}-{sp[1]}" if sp else f"{path.name}:-"
    print(f"[{campaign}] {name}")
    print(f"    anchor x{count} at {where}; inside the request: {'YES' if in_req else 'no'}; "
          f"on a line this lane changed: {'YES' if lane_hit else 'no'}; breaks {breaks!r}")
    if count != 1:
        bad += 1
    if in_req:
        planted = request_of(text.replace(anchor, replacement))
        print(f"    planted request: {planted}")
        try:
            diff = truth_diff(request_of(text), planted)
        except (SyntaxError, TypeError, NameError):
            print("    truth table: not evaluated (the planted term is a delayed register, "
                  "not a one-bit net of the request)")
            diff = None
        if diff is not None:
            def req_by(e: dict[str, int], crf: bool) -> bool:
                c = e["crf_clk_selected_r"] and (e["crf_mr_toggle_p_w"] or
                                                 (e["tkd_crflk_q_r"] and not e["crf_locked_w"]))
                a = e["aafm_disrupt_p_w"] or e["aafm_mr_toggle_p_w"]
                return bool(c and not a) if crf else bool(a and not c)
            names = sorted(set(re.findall(r"[A-Za-z_]\w*", request_of(text) + " " + planted))
                           | {"media_rebase_p_w"})
            envs = [dict(zip(names, b)) for b in itertools.product((0, 1), repeat=len(names))]
            for label, crf in (("selected-CRF-only", True), ("AAF-only", False)):
                req = [e for e in envs if req_by(e, crf)]
                for reb in (1, 0):
                    sub = [e for e in req if e["media_rebase_p_w"] == reb]
                    supp = sum(1 for e in sub if not evaluate(planted, e))
                    print(f"    {label} requests with media_rebase_p_w={reb}: "
                          f"{supp} of {len(sub)} suppressed by the planted form")
            print(f"    differs from the clean request on {len(diff)} of {len(envs)} input rows")
    print()
print(f"{len(rows)} anchors, {bad} not found exactly once")
sys.exit(1 if bad else 0)
