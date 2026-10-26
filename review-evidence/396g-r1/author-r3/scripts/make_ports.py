#!/usr/bin/env python3
"""Write the round-3 ports of the two reviewers' published delta probes.

Usage: python3 -I make_ports.py <R700-2 packet dir> <R699-2 scripts dir> <out dir>

Each port changes only the grader call: it passes `required_s`, the clean
capture's qualified length (stored frames less 63 guard samples at each end),
because the grader's default is now the 24-hour release requirement. The R700
port also records the verdict's `qualified` interval in each row and line.
Every other byte is the published script's. The unmodified scripts are run
separately; these ports only show the classification beneath the 24-hour rule.
"""
import pathlib
import sys

r700, r699, out = (pathlib.Path(arg) for arg in sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)


def port(source: pathlib.Path, target: pathlib.Path, edits: list) -> None:
    text = source.read_text()
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit(f"{source.name}: anchor occurs {text.count(old)} times: {old!r}")
        text = text.replace(old, new)
    target.write_text(text)
    print("wrote", target.name)


port(r700 / "delta_probes.py", out / "delta_probes.py", [
    ("t.CounterRunLog(arms,list(losses),0))",
     "t.CounterRunLog(arms,list(losses),0),required_s=(frames-126)/RATE)"),
    ("events=[e for e in detail.get('events',[]) if e['attribution']!='planted'])",
     "events=[e for e in detail.get('events',[]) if e['attribution']!='planted'],"
     "qualified=detail.get('qualified'))"),
    (" print(name,verdict,", " print(name,verdict,row['qualified'] and (row['qualified']['start'],row['qualified']['end']),"),
])
port(r699 / "grader_probe_r2.py", out / "grader_probe_r2.py", [
    ("    v, d = tc.grade_audio_counter_capture(cap, layout, rlog)\n",
     "    v, d = tc.grade_audio_counter_capture(cap, layout, rlog,\n"
     "                                          required_s=(len(cap) // (4 * channels) - 126) / RATE)\n"),
])
