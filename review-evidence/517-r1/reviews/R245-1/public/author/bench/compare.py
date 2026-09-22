#!/usr/bin/env python3
"""Compare complete per-leg bytes/results and controlled full-suite timings.

Usage: python3 compare.py LANE SEQUENTIAL_RUN POOLED_RUN OUTPUT_JSON
Run once for cold and once for warm. Both inputs must come from run_suite.py.
The reported resource/concurrency samples are telemetry, not test evidence.
"""
import hashlib
import json
import sys
from pathlib import Path

from analyze import ORDINARY, GPTP, split_log


def load(path):
    return json.loads(path.read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def render_semantics(text):
    records, lines = [], []
    for line in text.splitlines():
        if line.startswith("RENDER-PHASE "):
            rec = json.loads(line.removeprefix("RENDER-PHASE "))
            records.append({k: v for k, v in rec.items() if k not in ("t_s", "elapsed_s", "idle_s")})
        else:
            lines.append(line)
    return records, lines


def main():
    lane, seq, pool, output = map(Path, sys.argv[1:])
    sys.path.insert(0, str(lane / "scripts"))
    from suite_tally import scan, log_reports_failure
    ids = [load(r / "identity.json") for r in (seq, pool)]
    for field in ("head", "tree", "tool", "tool_sha256", "tool_files", "version", "command", "mode",
                  "affinity", "limits", "cgroup", "submodules"):
        assert ids[0][field] == ids[1][field], f"different {field}"
    assert [i["environment"]["SIM_JOBS"] for i in ids] == ["1", "2"]
    assert ({k: v for k, v in ids[0]["environment"].items() if k != "SIM_JOBS"}
            == {k: v for k, v in ids[1]["environment"].items() if k != "SIM_JOBS"})
    for r in (seq, pool):
        ending = load(r / "exit.json")
        assert ending == dict(make=0, verdict=0, tally=0, clean=True, same_head=True), ending
    for r in (seq, pool):
        before, after = load(r / "inputs-before.json"), load(r / "inputs-after.json")
        assert all(after.get(k) == v for k, v in before.items()), "existing input changed during run"
        assert {p.name: p.read_bytes() for p in (r / "headers-before").iterdir()} == {
            p.name: p.read_bytes() for p in (r / "headers-after").iterdir()}, "tracked header bytes changed"
    assert load(seq / "inputs-after.json") == load(pool / "inputs-after.json"), "input bytes differ"
    assert load(seq / "executables.json") == load(pool / "executables.json"), "executable bytes differ"
    legs = []
    for pos, name in enumerate(ORDINARY, 1):
        filename = f"{pos:02d}-{Path(name).name}.log"
        a, b = [(r / "legs" / filename).read_bytes() for r in (seq, pool)]
        assert a == b, f"different complete output for {name}"
        tally = scan(a.decode())
        assert tally[0] > 0 and tally[1] == 0 and not tally[3], (name, tally)
        assert not log_reports_failure(a.decode())[1], name
        legs.append(dict(command=[name], bytes=len(a), sha256=sha(a), checks=tally[0],
                         failures=tally[1], tally_lines=[m[3] for m in tally[2]]))
    whole = [(r / "milan_dp.log").read_text() for r in (seq, pool)]
    sections = [split_log(t) for t in whole]
    for name in GPTP:
        assert sections[0][name] == sections[1][name], f"gPTP output changed: {name}"
    render = [render_semantics(s["python3 render_mutants.py"]) for s in sections]
    assert render[0] == render[1], "render verdicts, inventory or phase semantics changed"
    counts = [scan(t) for t in whole]
    assert counts[0][:2] == counts[1][:2] and not counts[0][3] and not counts[1][3]
    times = [load(r / "summary.json") for r in (seq, pool)]
    a, b = [t["wall_s"] for t in times]
    report = dict(head=ids[0]["head"], tree=ids[0]["tree"], temperature=ids[0]["mode"],
                  complete_leg_bytes_equal=True, executable_bytes_equal=True, input_bytes_equal=True,
                  legs=legs, whole_checks=counts[0][0], whole_failures=counts[0][1],
                  render_phase_records=len(render[0][0]), render_semantics_equal=True,
                  sequential_seconds=a, pooled_seconds=b, seconds_saved=round(a-b, 3),
                  percent_saved=round((a-b)/a*100, 3), measurably_faster=b < a,
                  timing_attribution="Whole suite includes unchanged builds, gPTP and render; no build-speed claim.")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
