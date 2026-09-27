#!/usr/bin/env python3
"""[R362] round-2: show each surviving mutant is not equivalent.

Usage: python3 -B r362_2_survivor_witness.py <repo-checkout> <scratch-dir>

For each survivor of r362_2_mutants.py, loads a mutated COPY of the planner as
a module and evaluates one distinguishing input on both the pristine and the
mutated copy. Also re-runs, against the self-test, the four text mutants whose
short anchors collided with test phrases, using unique full-literal anchors.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r362_2_mutants import MUTANTS  # noqa: E402

BY_ID = {m[0]: m for m in MUTANTS}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    text = (repo / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
    pristine = scratch / "pristine.py"
    pristine.write_text(text, encoding="utf-8")
    base = load(pristine, "pristine")

    def hist(m, intervals, events, gm, r):
        return m.check_release_tu_history(intervals, events, observation_resolution_s=r,
                                          capture_complete=True, gm_changes_s=gm)[0]

    def mr(m, pdus, causes, rd, r=0.001):
        return m.check_release_mr("s", pdus, causes, rd, observation_resolution_s=r,
                                  capture_complete=m.ReleaseCapture((-2.0, 2.0)))[0]

    trace = [{"stream_id": "s", "timestamp_s": i / 100, "pdu_index": i, "mr": int(i >= 1)} for i in range(40)]
    rd = [{"stream_id": "s", "timestamp_s": 0, "value": 0}, {"stream_id": "s", "timestamp_s": 0.39, "value": 1}]
    cz = {"stream_id": "s", "timestamp_s": 0.01, "kind": "media-clock-source change"}
    witnesses = {
        "C06": lambda m: hist(m, [(0, 0.01)], [0], [-0.0005], 0.001),
        "C07": lambda m: hist(m, [(0, 0.3), (0.3005, 0.6)], [], [0, 0.3], 0.001),
        "C09": lambda m: hist(m, [(0, 0.3), (0.3, 0.6)], [0], [0], 0.001),
        "C10": lambda m: hist(m, [], [], [], -1.0),
        "C19": lambda m: str(m.check_release_tu_history([], [], observation_resolution_s=0.001,
                                                        capture_complete=True, gm_changes_s=[])[1]
                             .get("resolution_limit_s")),
        "C34": lambda m: mr(m, trace, [cz, dict(cz, stream_id="")], rd),
        "C35": lambda m: mr(m, [dict(p, pdu_index=p["pdu_index"] - 5) for p in trace], [cz], rd),
        "C38": lambda m: m.check_release_mr("s", trace, [cz], rd, observation_resolution_s=0.001,
                                            capture_complete=m.ReleaseCapture((-2.0, 2.0)))[1]["cause_window"],
    }
    for mid, fn in witnesses.items():
        _, desc, old, new = BY_ID[mid]
        assert text.count(old) == 1, mid
        path = scratch / f"mut_{mid}.py"
        path.write_text(text.replace(old, new), encoding="utf-8")
        mutated = load(path, f"mut_{mid}")
        a, b = fn(base), fn(mutated)
        print(f"WITNESS {mid} {'DISTINGUISHED' if a != b else 'EQUIVALENT'} pristine={a!r} mutant={b!r} ({desc})")

    # Text mutants with unique full-literal anchors (the short anchors also occur in tests).
    fixes = [
        ("T20", '"hold each new value for at least 8 AVTPDUs of that stream; "',
         '"hold each new value for at least 7 AVTPDUs of that stream; "'),
        ("T22", '"GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "',
         '"GM change + 0.2 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "'),
        ("T23", '"observation_resolution_s must be less than min(0.25 s, 0.5 s); "',
         '"observation_resolution_s must be less than 0.5 s; "'),
        ("T24", '"mapped to that stream\'s clock source; GM change alone fails; "',
         '"mapped to that stream\'s clock source; GM change alone passes; "'),
        ("T25", '"(including PHC settime/adjtime and fabric discontinuity); "',
         '"(excluding PHC settime/adjtime and fabric discontinuity); "'),
    ]
    for mid, old, new in fixes:
        assert text.count(old) == 1, mid
        path = scratch / f"txt_{mid}.py"
        path.write_text(text.replace(old, new), encoding="utf-8")
        s = subprocess.run([sys.executable, "-B", str(path), "--self-test"], capture_output=True, text=True,
                           timeout=600)
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", s.stderr, re.M)))
        state = "KILLED" if s.returncode and failed else "SURVIVED(self-test)"
        print(f"TEXT {mid} {state} {','.join(failed)} :: {old} -> {new}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
