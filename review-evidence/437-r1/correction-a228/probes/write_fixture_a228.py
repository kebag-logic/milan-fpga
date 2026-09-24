"""Add A228's recorded pages to scripts/gen_toc_shapes.json: the gfm pages
join `shapes`, the file-view pages form `file_view`.
Usage: write_fixture_a228.py <repo> <rendered-a228.json>"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc_renderer as r
path = repo / "scripts" / "gen_toc_shapes.json"
doc = json.loads(path.read_text(encoding="utf-8"))
rows = json.loads(Path(sys.argv[2]).read_text())
keys = ("set", "name", "source", "page", "request_bytes", "request_sha256",
        "response_bytes", "response_sha256", "recorded_utc")
names = {s["name"] for s in doc["shapes"]}
view = []
for row in rows:
    out = {k: row[k] for k in keys}
    if row["mode"] == "gfm":
        assert out["name"] not in names, out["name"]
        out["headings"] = [list(h) for h in r.headings_of(row["response_bytes"])]
        doc["shapes"].append(out)
    else:
        out["headings"] = [list(h) for h in r.anchored_headings_of(row["response_bytes"])]
        view.append(out)
doc["about"] += (" file_view (the first correction round of PR #538, for the"
                 " R237-5 and R238-4 reviews): pages recorded in the API's"
                 " `markdown` mode, GitHub's file view, whose headings carry"
                 " their anchors, so `headings` there is (level, text, anchor);"
                 " gen_toc_shape_cases.py requires every heading the walk lists,"
                 " label and anchor, to be one of them, in order.")
doc["method"] = doc["method"].replace(
    "Recorded 2026-09-23 (UTC times per shape).",
    "Recorded 2026-09-23, and on 2026-09-24 for the pages the first correction"
    " round of PR #538 added (UTC times per shape). The `file_view` pages were"
    " sent the same way with mode markdown.")
assert "2026-09-24" in doc["method"]
doc["file_view"] = view
path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(doc["shapes"]), "shapes,", len(view), "file-view pages")
for v in view:
    print("  ", v["name"], v["headings"])
