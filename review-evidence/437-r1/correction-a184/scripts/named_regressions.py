#!/usr/bin/env python3
"""The named regression items, re-rendered fresh and judged per walk.

Items: R238-r1's 62 probes (A, B, C, D, F, P rows), R237-r1's 42 renderer
controls and 3 block-marker controls, and #516's twelve unclosed-comment
variants (exact bytes from the A172 packet). Each page is rendered fresh
(render.py receipts) and compared with the publicly recorded response; each
walk (base 88e9276b, a172 b5e6c23e, head = lane working tree) is judged
AGREE or not against the fresh rendering.

Usage: named_regressions.py OUT_RENDER.json OUT_TABLE.json
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_way import PUB, REVS, load, rendered, walk_headings  # noqa: E402

HERE = Path(__file__).resolve().parent


def items() -> list[dict]:
    rows = []
    for x in map(json.loads, open(PUB / "reviews/R238-1/receipts/probes.jsonl")):
        rows.append({"id": f"R238 {x['id']}", "page": x["page"], "recorded": x["github"]})
    resp = {x["id"]: x for x in json.load(open(PUB / "reviews/R237-1/renderer-responses.json"))}
    for rid, x in resp.items():
        rows.append({"id": f"R237 {rid}", "page": x["request"]["text"],
                     "recorded": [h[1] for h in rendered(x["html"])]})
    for x in json.load(open(PUB / "reviews/R237-1/block-marker-inputs.json")):
        rows.append({"id": f"R237 {x['id']}", "page": x["page"], "recorded": None})
    for i, x in enumerate(json.load(open(PUB / "correction-a172/exploratory-unclosed-comments.json"))):
        rows.append({"id": f"#516 variant {i + 1}", "page": x["page"], "recorded": x["github"]})
    return rows


def main() -> int:
    render_out, table_out = sys.argv[1], sys.argv[2]
    rows = items()
    Path(render_out + ".in").write_text(json.dumps([{"id": r["id"], "page": r["page"]} for r in rows]))
    subprocess.run([sys.executable, "-B", str(HERE / "render.py"), render_out + ".in", render_out], check=True)
    fresh = {r["id"]: r for r in json.load(open(render_out))}
    table, counts = [], {}
    with tempfile.TemporaryDirectory(prefix="a184.named.") as tmp:
        walks = {n: load(n, rev, Path(tmp))[0] for n, rev in REVS.items()}
        for r in rows:
            gh = fresh[r["id"]]["github"]
            names = [t for _, t in gh]
            row = {"id": r["id"], "page": r["page"], "github": names,
                   "recorded_matches_fresh": r["recorded"] is None or r["recorded"] == names}
            for n, mod in walks.items():
                w = walk_headings(mod, r["page"])
                row[n] = w if w == "REFUSED" else [t for _, t in w]
                row[f"{n}_agrees"] = w == gh
            row["verdict"] = ("REGRESSION" if row["base_agrees"] and not row["head_agrees"] else
                              "agree" if row["head_agrees"] else
                              "pre-existing identical" if row["base"] == row["head"] else "pre-existing changed")
            counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1
            table.append(row)
    Path(table_out).write_text(json.dumps({"counts": counts, "rows": table}, indent=1) + "\n")
    print(json.dumps(counts))
    for row in table:
        if row["verdict"] != "agree" or not row["recorded_matches_fresh"]:
            print(f"{row['verdict']:24s} {row['id']:40s} gh={row['github']} base={row['base']} "
                  f"head={row['head']} recorded_matches_fresh={row['recorded_matches_fresh']}")
    return 1 if counts.get("REGRESSION") else 0


if __name__ == "__main__":
    sys.exit(main())
