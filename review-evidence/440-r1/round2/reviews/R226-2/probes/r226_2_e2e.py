#!/usr/bin/env python3
"""R226-2 end-to-end: the public R226-1 e2e procedure with four more pages.

Usage: python3 -B r226_2_e2e.py <scripts-dir> <label> <outdir> <r226-1-probes-dir> [--render-new]

Loads the public R226-1 `r226_e2e.py` unchanged (its page(), git() and
main()) and appends E19-E22: the xmp closer after <pre> on a later line, and
div/title/xmp on the opening line. Real `gen_toc.py --write/--check` and
`check_em_dash.py --base` CLIs run on a real Git repository exactly as in
R226-1. With --render-new, the four new BASE pages are sent (synthetic text
only) to GitHub's /markdown endpoint in gfm and markdown modes and the oracle
is written to <outdir>/e2e-oracle-new.json.
"""
import json
import re
import runpy
import sys
from pathlib import Path

scripts, label, out, r1 = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]).resolve()
render_new = "--render-new" in sys.argv
sys.path.insert(0, str(r1))
sys.dont_write_bytecode = True
mod = runpy.run_path(str(r1 / "r226_e2e.py"), run_name="r226_e2e_lib")
NEW = [
    ("E19-non-type1-name-xmp", "<pre>\n</xmp>\n"),
    ("E20-non-type1-name-div-opening-line", "<pre>x</div>\n"),
    ("E21-non-type1-name-title-opening-line", "<pre>x</title>\n"),
    ("E22-non-type1-name-xmp-opening-line", "<pre>x</xmp>\n"),
]
mod["CASES"].extend(NEW)
main = mod["main"]
main.__globals__["CASES"] = mod["CASES"]
sys.argv = [sys.argv[0], scripts, label, str(out)]
main()
if render_new:
    from r226_sweep import render_one  # noqa: E402
    oracle = {}
    for cid, prefix in NEW:
        src = mod["page"](prefix).decode("utf-8")
        row = {"id": f"R226-2-E-{cid}", "source": src}
        for mode in ("markdown", "gfm"):
            r = render_one(out / "e2e-render", row, mode)
            html = (out / "e2e-render" / "renderer" / mode / row["id"] / "response.html").read_text()
            oracle.setdefault(cid, {})[mode] = {"h2": r["h2"], "old_heading_rendered": bool(
                re.search(r"<h2[^>]*>.*?Old — heading", html, re.S))}
    (out / "e2e-oracle-new.json").write_text(json.dumps(oracle, indent=1, ensure_ascii=False) + "\n")
    print("oracle-new", json.dumps(oracle, ensure_ascii=False))
