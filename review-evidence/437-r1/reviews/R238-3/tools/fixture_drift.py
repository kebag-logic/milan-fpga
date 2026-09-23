#!/usr/bin/env python3
"""Re-send every committed #437 fixture request verbatim and compare today's
GitHub response with the recorded one; then score the head and base walks.

Usage: fixture_drift.py <head-scripts> <base-scripts> <out-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gfm  # noqa: E402

FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json",
            "gen_toc_container_walk.json")


def walk(scripts: str, rows: list, out: Path) -> list:
    src = out.with_suffix(".in.json")
    src.write_text(json.dumps(rows))
    subprocess.run([sys.executable, str(Path(__file__).with_name("walk.py")), scripts,
                    str(src), str(out)], check=True)
    src.unlink()
    return json.loads(out.read_text())


def main() -> int:
    head, base, outdir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for fixture in FIXTURES:
        for shape in json.loads((Path(head) / fixture).read_text())["shapes"]:
            rows.append({"fixture": fixture, "name": shape["name"], "page": shape["page"],
                         "recorded": shape["headings"], "limitation": shape.get("limitation"),
                         "rec_req": shape["request_bytes"], "rec_resp": shape["response_bytes"]})
    receipts = None
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=6) as pool:
        receipts = list(pool.map(lambda r: gfm.send(r["rec_req"].encode()), rows))
    h = walk(head, [{"name": r["name"], "page": r["page"]} for r in rows], outdir / "head_walk.json")
    b = walk(base, [{"name": r["name"], "page": r["page"]} for r in rows], outdir / "base_walk.json")
    report, counts = [], {}
    for r, rc, hw, bw in zip(rows, receipts, h, b):
        today = gfm.rendered_headings(rc["response_bytes"])
        row = {"fixture": r["fixture"], "name": r["name"],
               "encoder_matches_recorded_request": gfm.request_bytes(r["page"]).decode() == r["rec_req"],
               "response_bytes_identical_today": rc["response_bytes"] == r["rec_resp"],
               "headings_identical_today": today == r["recorded"],
               "today_request_sha256": rc["request_sha256"],
               "today_response_sha256": rc["response_sha256"],
               "github": today, "head": hw["walk"], "base": bw["walk"],
               "head_agrees": hw["walk"] == today, "base_agrees": bw["walk"] == today,
               "limitation": r["limitation"]}
        if r["limitation"]:
            lim = r["limitation"]
            row["limitation_walk_matches_head"] = lim["walk"] == hw["walk"]
            row["limitation_base_agreed_matches"] = lim["base_agreed"] == (bw["walk"] == today)
        report.append(row)
        key = (r["fixture"], "limitation" if r["limitation"] else "plain",
               "head=gh" if row["head_agrees"] else "head!=gh",
               "base=gh" if row["base_agrees"] else "base!=gh")
        counts[" ".join(key)] = counts.get(" ".join(key), 0) + 1
    (outdir / "fixture_drift.json").write_text(json.dumps(report, indent=1))
    lines = [f"shapes {len(report)}",
             f"encoder reproduces every recorded request: {all(r['encoder_matches_recorded_request'] for r in report)}",
             f"response bytes identical today: {sum(r['response_bytes_identical_today'] for r in report)}/{len(report)}",
             f"headings identical today: {sum(r['headings_identical_today'] for r in report)}/{len(report)}"]
    lines += [f"{k}: {v}" for k, v in sorted(counts.items())]
    bad = [r["name"] for r in report if r["limitation"] and not (
        r["limitation_walk_matches_head"] and r["limitation_base_agreed_matches"])]
    lines.append(f"limitation records inconsistent with measured walks: {bad}")
    regress = [f"{r['fixture']}: {r['name']}" for r in report if r["base_agrees"] and not r["head_agrees"]]
    lines.append(f"base agreed, head disagrees ({len(regress)}):")
    lines += ["  " + x for x in regress]
    fixed = [f"{r['fixture']}: {r['name']}" for r in report if not r["base_agrees"] and r["head_agrees"]]
    lines.append(f"base disagreed, head agrees ({len(fixed)})")
    both = [f"{r['fixture']}: {r['name']}" for r in report if not r["base_agrees"] and not r["head_agrees"]]
    lines.append(f"both disagree ({len(both)}):")
    lines += ["  " + x for x in both]
    (outdir / "SUMMARY.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
