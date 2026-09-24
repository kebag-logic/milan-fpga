"""Audit completed gate receipts, original counts and named mutation failures."""
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((OUT / name).read_text())


def suite_counts(name):
    return {m[0]: int(m[1]) for m in re.findall(
        r"^PASS (\w+) \((\d+) checks: \d+ PASS, 0 FAIL\)$",
        (OUT / name).read_text(), re.MULTILINE)}


gates = ["focused-live-peers", "docs-final", "lint", "yosys", "suites",
         "nvm-figures", "mutants", "reviewer-r310", "reviewer-r311"]
gates += ["parent-" + name for name in
          ("cpp", "python", "xvlog", "source-lists", "pp-srcs", "builder", "consumer")]
for name in gates:
    assert read(name + ".json")["rc"] == 0, name

baseline = suite_counts("baseline-suites.log")
candidate = suite_counts("suites.log")
assert len(baseline) == len(candidate) == 33
assert baseline.keys() == candidate.keys()
for name, count in baseline.items():
    assert candidate[name] == count + (5568 if name == "pp_top" else 0), name
assert sum(baseline.values()) == 1009045
assert sum(candidate.values()) == 1014613
assert "GI latency walks added: 5568 checks, 0 failures" in (
    OUT / "focused-live-peers.log").read_text()

mutants = read("mutants/results.json")
assert len(mutants) == 22
assert mutants[0]["variant"] == "golden"
assert mutants[-1]["variant"] == "restored"
for item in mutants:
    assert item["build_rc"] == 0 and item["passed"], item
    if item["variant"] in ("golden", "restored"):
        assert item["run_rc"] == 0
    else:
        assert item["run_rc"] == 1 and item["named_failures"]

probes = []
for role, names in (
    ("r310", ("cmp-low3", "cmp-high2", "cmp-no-bit31", "cmp-low16")),
    ("r311", ("r-cmp-low8", "r-cmp-low16", "r-cmp-high16", "r-cmp-no-bit31")),
):
    directory = OUT / ("reviewer-" + role)
    if role == "r310":
        rows = [json.loads(line) for line in
                (directory / "probes.jsonl").read_text().splitlines()]
    else:
        rows = json.loads((directory / "results.json").read_text())
    by_name = {row["variant"]: row for row in rows}
    assert set(by_name) == {"golden", *names}
    assert by_name["golden"]["build_rc"] == 0
    assert by_name["golden"]["run_rc"] == 0
    assert "6182 checks, 0 failures" in (directory / "golden-run.log").read_text()
    for name in names:
        row = by_name[name]
        assert row["build_rc"] == 0 and row["run_rc"] == 1, row
        text = (directory / (name + "-run.log")).read_text()
        assert "[build default," in text
        named = [line for line in text.splitlines() if
                 line.startswith("FAIL: GI LATENCY-WALK-") and
                 "exactly one unsolicited response" in line]
        assert named, row
        # Both directions, both baseline polarities must detect omitted bits.
        for walk in ("ONE", "ZERO"):
            for direction in ("step", "return"):
                assert any("WALK-" + walk in line and
                           " " + direction + ":" in line for line in named)
        probes.append(dict(role=role, variant=name, build_rc=0, run_rc=1,
                           named_check=named[0], named_failure_count=len(named)))

summary = dict(gates={name: 0 for name in gates},
               original_suites=33, original_checks=1009045, added_checks=5568,
               candidate_checks=1014613, suite_counts=candidate,
               retained_mutants=20, reviewer_truncations=probes)
(OUT / "verification-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
