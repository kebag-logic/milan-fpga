#!/usr/bin/env python3
"""Run the exact-head check-ids.py over planted trees (its own self-test masters)
and print rc plus findings for each probe text. Usage: probe_ids_forms.py <clone>"""
import importlib.util, subprocess, sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
script = clone / "scripts/check-ids.py"
spec = importlib.util.spec_from_file_location("ci", script); ci = importlib.util.module_from_spec(spec); spec.loader.exec_module(ci)
PROBES = [
    # F3 composition and its valid counterpart
    ("f3-broken-STRT", "T-ADP-\n// DELAY(-STRT) x"),
    ("f3-broken-START", "T-ADP-\n// DELAY(-START) x"),
    ("f3-md-broken-STRT", "T-ADP-\nDELAY(-STRT) x"),
    ("break-opt-break-STRT", "T-ADP-\n// DELAY(-\n// STRT) x"),
    ("opt-break-STRT", "T-ADP-DELAY(-\n// STRT) x"),
    ("double-cont-STRT", "T-ADP-\n// DELAY-\n// STRT x"),
    ("double-cont-START", "T-ADP-\n// DELAY-\n// START x"),
    ("minus1-missing", "P-MISSING-1 x"),
    ("minus1-valid", "P-RX-SLOTS-1 x"),
    ("cont-minus1-valid", "P-RX-\n// SLOTS-1 x"),
    ("cont-family", "T-MRP-\n// * x"),
    ("cont-braces-valid", "T-NVM-\n// {RS-DEADLINE} x"),
    ("cont-then-braces-bad", "T-MRP-\n// {JOIN, NOPE} x"),
    ("cont-sibling-bad", "T-BUDGET-AECP-\n// TYP / -XX x"),
    # wrap at a space inside the sibling form (prose wrap)
    ("sibling-wrap-after-slash-bad", "T-BUDGET-AECP-TYP /\n-XX x"),
    ("sibling-wrap-after-slash-cmt-bad", "T-BUDGET-AECP-TYP /\n// -XX x"),
    ("sibling-wrap-before-slash-bad", "T-BUDGET-AECP-TYP\n/ -XX x"),
    ("sibling-broken-hyphen-bad", "T-BUDGET-AECP-TYP / -\n// XX x"),
    ("braces-wrap-bad", "T-MRP-{JOIN,\n NOPE} x"),
    ("opt-wrap-before-paren-bad", "T-ADP-DELAY\n(-STRT) x"),
    ("cr-lf-cont-STRT", "T-ADP-\r\n// DELAY(-STRT) x"),
    ("hash-cont-STRT", "T-ADP-\n# DELAY(-STRT) x"),
    ("star-cont-STRT", "T-ADP-\n * DELAY(-STRT) x"),
    ("quote-cont-STRT", "T-ADP-\n> DELAY(-STRT) x"),
]
for name, text in PROBES:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for rel, body in {str(ci.PARAMS): ci.SELFTEST_PARAMS, str(ci.TIMING): ci.SELFTEST_TIMING, ci.CASE: text}.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True); (root / rel).write_bytes(body.encode())
        p = subprocess.run([sys.executable, str(script), "--root", str(root)], capture_output=True, text=True)
        print(f"{name:34s} rc={p.returncode} findings={ci.findings(p.stdout)}")
