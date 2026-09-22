#!/usr/bin/env python3
"""R226-2: positive renderer controls for the same session as r226_2_render.py.

Usage: python3 -B r226_2_render_positive.py <head-tree> <r226-1-probes-dir> <outdir>

Renders fixtures whose heading the head's arms say IS visible (valid and
cross-name closers), so an all-hidden result for the new fixtures cannot be
an artifact of the endpoint. Raw pages come from the head's own
`closer_arms()`; label pages are rebuilt as `em_dash_arms()` writes them.
"""
import json
import re
import sys
from pathlib import Path

head, r1, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(r1))
sys.path.insert(0, str(head / "scripts"))
sys.dont_write_bytecode = True
from r226_sweep import render_one  # noqa: E402
import gen_toc  # noqa: E402
sys.modules.setdefault("gen_toc", gen_toc)
import gen_toc_closer_cases as closers  # noqa: E402

want_raw = {"I440-T-valid pre/style '\\n'", "I440-T-valid pre/TEXTAREA 'x'",
            "I440-T-valid textarea/pre '\\n'", "I440-T-valid style/SCRIPT 'x'"}
rows = []
for name, page, holds in closers.closer_arms():
    if name in want_raw:
        rows.append({"id": "R226-2-pos-" + re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-"),
                     "arm": name, "source": page, "heading_text": "Probe",
                     "expects_visible": holds.__closure__[0].cell_contents == gen_toc.TEXT})
heading = "## Old — heading\n"
tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
for rid, prefix, findings, exempt in closers._label_rows():
    if rid in ("I440-E-cross", "I440-E-cross-inline"):
        rows.append({"id": "R226-2-pos-" + rid, "arm": rid, "heading_text": "Old — heading",
                     "source": "# Page\n\n" + prefix + heading + tail,
                     "expects_visible": (findings, exempt) == (0, 1)})
assert len(rows) == 6, [r["arm"] for r in rows]
report = []
for row in rows:
    rec = {"id": row["id"], "arm": row["arm"], "source": row["source"],
           "expects_visible": row["expects_visible"]}
    for mode in ("gfm", "markdown"):
        r = render_one(out, {"id": row["id"], "source": row["source"]}, mode)
        html = (out / "renderer" / mode / row["id"] / "response.html").read_text()
        rec[mode] = {"h2": r["h2"], "heading_rendered": bool(re.search(
            r"<h2[^>]*>.*?" + re.escape(row["heading_text"]) + r"\s*</h2>", html, re.S))}
    rec["agree"] = all(rec[m]["heading_rendered"] == row["expects_visible"] for m in ("gfm", "markdown"))
    report.append(rec)
    print(rec["id"], rec["gfm"], rec["markdown"], "agree" if rec["agree"] else "DISAGREE", flush=True)
(out / "render-positive-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=True) + "\n")
print("positive rows", len(report), "agree", sum(r["agree"] for r in report))
