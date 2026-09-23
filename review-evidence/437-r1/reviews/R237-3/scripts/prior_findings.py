#!/usr/bin/env python3
"""Replay every prior public finding's recorded pages at this head.

Usage: prior_findings.py <prior-dir> <head-scripts> <base-scripts> <out.json>
<prior-dir> holds the public R237-r1, R238-r1 and R237-2 receipts fetched
from the evidence commit (fetched names keep their public paths with `/`
replaced by `_`). For every page with a recorded GitHub rendering, the head
and base walks' headings are compared with it. The pages are also written
to <out>.pages.json so they can be freshly rendered.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(prior: Path) -> dict:
    rows = {}
    for name, cls in (("reviews_R237-2_receipts_combinatorial-render.json", "R237-2 F1 corpus"),
                      ("reviews_R237-2_receipts_comment-rule-render.json", "R237-2 F2 probes"),
                      ("reviews_R237-2_receipts_regression-seed-render.json", "R237-2 F1 seeds")):
        for r in json.loads((prior / name).read_text())["rows"]:
            rows[f"{cls} | {r['name']}"] = {"page": r["page"], "github": [h[1] for h in r["rendered"]],
                                           "prior_class": r["class"]}
    for line in (prior / "reviews_R238-1_receipts_probes.jsonl").read_text().splitlines():
        r = json.loads(line)
        rows[f"R238-r1 | {r['id']}"] = {"page": r["page"], "github": r["github"], "prior_class": None}
    for r in json.loads((prior / "reviews_R237-1_renderer-responses.json").read_text()):
        rows[f"R237-r1 | {r['id']}"] = {"page": r["page"], "github": r["headings"], "prior_class": None}
    return rows


def main() -> None:
    prior, head, base, out_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
    rows = load(prior)
    pages = {k: v["page"] for k, v in rows.items()}
    Path(out_path + ".pages.json").write_text(json.dumps(pages, indent=0))
    with tempfile.TemporaryDirectory() as tmp:
        walks = {}
        for tag, tree in (("head", head), ("base", base)):
            out = Path(tmp) / f"{tag}.json"
            subprocess.run([sys.executable, "-B", str(HERE / "walk_headings.py"), tree,
                            out_path + ".pages.json", str(out)], check=True)
            walks[tag] = json.loads(out.read_text())
    summary = {}
    for key, row in rows.items():
        # GitHub's lists count only the probe words the prior rounds scored
        want = [h for h in row["github"] if h in ("Old", "Real")]
        head_h = [h[1] for h in walks["head"][key]["headings"] if h[1] in ("Old", "Real")]
        base_h = [h[1] for h in walks["base"][key]["headings"] if h[1] in ("Old", "Real")]
        row.update(head=head_h, base=base_h, head_agrees=head_h == want, base_agrees=base_h == want)
        group = key.split(" | ")[0]
        s = summary.setdefault(group, {"rows": 0, "head_agrees": 0, "regress_vs_base": []})
        s["rows"] += 1
        s["head_agrees"] += row["head_agrees"]
        if row["base_agrees"] and not row["head_agrees"]:
            s["regress_vs_base"].append(key)
        if row["prior_class"] == "REGRESSION":
            s.setdefault("prior_regression_rows", 0)
            s["prior_regression_rows"] += 1
            s.setdefault("prior_regression_rows_agreeing_now", 0)
            s["prior_regression_rows_agreeing_now"] += row["head_agrees"]
    json.dump({"summary": summary, "rows": rows}, open(out_path, "w"), indent=1)
    for group, s in summary.items():
        print(group, {k: (v if not isinstance(v, list) else len(v)) for k, v in s.items()})
    disagree = [k for k, r in rows.items() if not r["head_agrees"]]
    print("head disagreements:", len(disagree))
    for k in disagree:
        print("  ", k, "github", rows[k]["github"], "head", rows[k]["head"], "base", rows[k]["base"])


if __name__ == "__main__":
    main()
