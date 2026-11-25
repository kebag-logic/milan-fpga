#!/usr/bin/env python3
"""R924: verify the published packet and spot-check output/figure claims."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

CLONE = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
EVIDENCE = PACKET / "scratch" / "evidence"
REV = "726d9d2597c965868995948d16dac921bd5a1752"
PREFIX = "review-evidence/cicd3-r1/"


def blob(rev, path):
    return subprocess.check_output(["git", "show", rev + ":" + path], cwd=CLONE)


def constants(rev):
    result = {}
    for node in ast.parse(blob(rev, "scripts/suite_shards.py")).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") in ("SUITE_SECONDS", "PIECE_SECONDS") for t in node.targets):
            result[node.targets[0].id] = ast.literal_eval(node.value)
    return result


def main():
    manifest = json.loads(blob(REV, PREFIX + "MANIFEST.json"))
    verified = []
    for item in manifest:
        if not item["file"].startswith(tuple(f"author-r{i}/" for i in range(4, 8))):
            continue
        data = blob(REV, PREFIX + item["file"])
        sha = hashlib.sha256(data).hexdigest()
        assert sha == item["published_sha256"], item["file"]
        target = EVIDENCE / item["file"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        verified.append({"file": item["file"], "sha256": sha, "path_redacted": item["path_redacted"]})
    (PACKET / "evidence-integrity.json").write_text(json.dumps({"reviewer": "R924", "commit": REV,
          "verified_count": len(verified), "files": verified}, indent=2) + "\n")
    results = {"reviewer": "R924", "manifest_files_verified": len(verified)}
    before, after = constants("13e6d869"), constants("59f4f478")
    lowered = []
    for key in before:
        for name, previous in before[key].items():
            old = (previous,) if isinstance(previous, int) else previous
            new = (after[key][name],) if isinstance(previous, int) else after[key][name]
            for i, (a, b) in enumerate(zip(old, new)):
                if b < a:
                    lowered.append((name, i, a, b))
    assert all(row[0] == "milan_dp" for row in lowered), lowered
    results["figure_refresh_lowered_only_rekeyed_milan_dp"] = lowered
    # Recompute round-four maxima from the retained measurement table, without its conclusion.
    table = (EVIDENCE / "author-r4/receipts/hosted/deal-check-old-figures-on-old-runs.txt").read_text()
    maxima = {}
    for name, old, measured in re.findall(r"([a-zA-Z0-9_]+) (\d+)->(\d+)", table):
        if name != "ovh": maxima[name] = max(maxima.get(name, 0), int(measured))
    flattened = after["SUITE_SECONDS"].copy()
    for suite, legs in after["PIECE_SECONDS"].items():
        flattened.update({f"{suite}__{i}": n for i, n in enumerate(legs)})
    assert all(flattened[name] >= n for name, n in maxima.items())
    results["retained_table_window_maxima_covered"] = len(maxima)
    # Recompute the full byte digests, then compare raw per-case receipt objects.
    local = EVIDENCE / "author-r7/receipts/local"
    hashes = {}
    for pin in ("old", "new"):
        for case in ("gptp", "gptp-lat"):
            hashes[f"{pin}:{case}"] = hashlib.sha256((local / f"{case}.{pin}-pin.out").read_bytes()).hexdigest()
    seen, case_comparisons, gptp_runs = {}, 0, {"old": 0, "new": 0}
    for path in sorted((local / "pieces").glob("*.json")):
        pin = "old" if re.search(r"P\d[OHB]0-", path.name) else "new"
        receipt = json.loads(path.read_text())
        for row in receipt["results"]:
            case = row["case"]
            fingerprint = (row["outcome"], row["returncode"], row["output_sha256"])
            assert fingerprint[:2] == ("pass", 0)
            key = (pin, case)
            if key in seen:
                assert seen[key] == fingerprint
                case_comparisons += 1
            seen[key] = fingerprint
            if case in ("gptp", "gptp-lat"):
                assert row["output_sha256"] == hashes[f"{pin}:{case}"]
                gptp_runs[pin] += 1
    direct = (local / "direct-runs.txt").read_text().splitlines()[1:]
    for row in direct:
        cols = row.split()
        pin = "old" if cols[3] == "1616fc8f" else "new"
        assert cols[8] == "rc=0" and hashes[f"{pin}:{cols[5]}"].startswith(cols[9])
        gptp_runs[pin] += 1
    assert gptp_runs == {"old": 18, "new": 22}, gptp_runs
    for case in ("gptp", "gptp-lat"):
        old, new = [(local / f"{case}.{pin}-pin.out").read_text().splitlines() for pin in ("old", "new")]
        differences = [(a, b) for a, b in zip(old, new) if a != b]
        assert len(old) == len(new) and len(differences) == 1, differences
        assert "rp " in differences[0][0] and "wp " in differences[0][0], differences
    results["same_pin_case_comparisons"] = case_comparisons
    results["documented_gptp_executions"] = gptp_runs
    results["raw_output_sha256"] = hashes
    results["cross_pin_difference"] = "one response-pointer observation line per case; same-pin receipts identical"
    # One complete published A/B receipt pair per retained suite.
    comparisons = []
    for old_dir, new_dir in (("s1base-p1", "s1head-p1"), ("s18base-p1", "s18head-p1")):
        parent = EVIDENCE / "author-r4/receipts/ab"
        for path in (parent / old_dir).glob("*.json"):
            a, b = json.loads(path.read_text()), json.loads((parent / new_dir / path.name).read_text())
            assert a["inventory"] == b["inventory"] and a["results"] == b["results"]
            comparisons.append({"receipt": path.name, "cases": len(a["results"]), "identical": True})
    results["published_ab_receipts"] = comparisons
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
