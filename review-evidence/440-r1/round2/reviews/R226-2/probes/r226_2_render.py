#!/usr/bin/env python3
"""R226-2: render the exact bytes of every fixture the correction adds.

Usage: python3 -B r226_2_render.py <head-tree> <r226-1-probes-dir> <outdir>

The 24 I440-T-other-name raw-walk pages come from the head's own
`closer_arms()`; the six I440-E-other-* BASE pages are rebuilt exactly as
`em_dash_arms()` writes them ("# Page\\n\\n" + prefix + heading + tail).
Each source is sent (synthetic text only) to GitHub's /markdown endpoint in
gfm and markdown modes through the public R226-1 `render_one` helper, which
keeps byte-exact request/response files and SHA-256 receipts. The oracle is
whether the probe/Old heading renders as an <h2>. Sources byte-identical to
an R226-1 fixture are also listed with that round's stored counts.
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

rows = []
for name, page, holds in closers.closer_arms():
    if name.startswith("I440-T-other-name"):
        rows.append({"id": "R226-2-" + re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-"),
                     "arm": name, "kind": "raw", "source": page,
                     "walk_expects": holds.__closure__[0].cell_contents,
                     "heading_text": "Probe"})
heading = "## Old — heading\n"
tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
for rid, prefix, findings, exempt in closers._label_rows():
    if rid.startswith("I440-E-other-"):
        rows.append({"id": "R226-2-" + rid, "arm": rid, "kind": "label-base-page",
                     "source": "# Page\n\n" + prefix + heading + tail,
                     "row_expects": [findings, exempt], "heading_text": "Old — heading"})
assert len(rows) == 30, len(rows)

r1_fixtures = {}
r1_index = {}
fx = r1.parent / "sweep" / "fixtures.json"
ix = r1.parent / "sweep" / "renderer-index.json"
if fx.exists():
    r1_fixtures = {r["source"]: r["id"] for r in json.loads(fx.read_text())}
    r1_index = json.loads(ix.read_text())

out.mkdir(parents=True, exist_ok=True)
report = []
for row in rows:
    rec = {k: row[k] for k in ("id", "arm", "kind")}
    rec["source"] = row["source"]
    for mode in ("gfm", "markdown"):
        r = render_one(out, {"id": row["id"], "source": row["source"]}, mode)
        html = (out / "renderer" / mode / row["id"] / "response.html").read_text()
        rendered = bool(re.search(r"<h2[^>]*>.*?" + re.escape(row["heading_text"]) + r"\s*</h2>",
                                  html, re.S))
        rec[mode] = {"h2": r["h2"], "heading_rendered": rendered}
    if row["kind"] == "raw":
        rec["walk_expects"] = row["walk_expects"]
        # arm expects the probe line inside the raw HTML block: renderer must hide it
        rec["agree"] = all(not rec[m]["heading_rendered"] for m in ("gfm", "markdown")) \
            == (row["walk_expects"] == gen_toc.HTML)
    else:
        rec["row_expects"] = row["row_expects"]
        # (1 finding, 0 exempt) is right exactly when the base page hides the heading
        hidden = all(not rec[m]["heading_rendered"] for m in ("gfm", "markdown"))
        rec["agree"] = hidden == (tuple(row["row_expects"]) == (1, 0))
    same = r1_fixtures.get(row["source"])
    rec["r226_1_identical_fixture"] = same
    rec["r226_1_counts"] = r1_index.get(same) if same else None
    report.append(rec)
    print(rec["id"], rec["gfm"], rec["markdown"], "agree" if rec["agree"] else "DISAGREE",
          "r226-1:", same, rec["r226_1_counts"], flush=True)
(out / "render-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=True) + "\n")
print("rows", len(report), "agree", sum(r["agree"] for r in report))
