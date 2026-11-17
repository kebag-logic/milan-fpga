#!/usr/bin/env python3
"""Reproduce cross-participant LeaveAll attribution using the public log format."""
import argparse
import json
import sys
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
a = p.parse_args()
sys.path.insert(0, str(a.repo.resolve() / "tb/verilator/ctrl_service_budget"))
import grade
import join_grade
import mrpdu_grade
import run
import scenario
import selftest
from selftest_leaveall import mrpdu, MSRP, MVRP
MS = 100_000

def check(name, sends, timers, expected):
    lines = ["MARK 1000 save.change"]
    for at in range(900, 1601, 10):
        lines += [f"EVW {at * MS} {n} {w:08x}" for n,w in enumerate((4,1,0,0))]
    word = 0
    for at, app, la in sends:
        frame = mrpdu(app, la)
        lines += selftest.tx_record(scenario.CH["srp"], 0, frame, word, at * MS)
        word += 2 + (len(frame) + 3) // 4
        lines += [f"ENTRY {at * MS - 2000} build_mrpdu"]
    for at in sorted(set([x[0] for x in sends] + [1600])):
        lines += [f"PASS {at} {at*MS-3000} {(at*MS-3000)//2} 2500 instr=10"]
    lines += [f"ENTRY {at*MS+100} {kind}" for at,kind in timers]
    log = grade.parse(selftest.synthetic(lines), 100_000_000, 50_000_000)
    j = join_grade.held(log)
    rows = mrpdu_grade.rows(grade.Grader(log), scenario.Group(name,save=dict(loaded=True,origin="save.change")))
    misses = run.stated_misses([dict(group=name, passes=dict(joins=j))])
    print(json.dumps(dict(case=name, expected=expected, leavealls=mrpdu_grade.leave_alls(log), joins=j,
                         rows=[dict(probe=r["probe"],ms=r["ms"]) for r in rows],misses=misses),indent=2))
    (Path(__file__).parent / (name+".log")).write_text(selftest.synthetic(lines))
    return j

la, join = "on_la_timer", "on_join_timer"
# Ground truth: MSRP expires at 1050, MVRP at 1190. MSRP omits LeaveAll
# at 1181 (its first opportunity) and sends it only at 1371. MVRP is correct.
j = check("participant_swap", [(1000,MSRP,False),(1040,MVRP,False),(1181,MSRP,False),
                              (1221,MVRP,True),(1371,MSRP,True)],
          [(1050,la),(1180,join),(1190,la),(1220,join),(1370,join)],
          "MSRP must fail: first opportunity 1180; first frame 1181 lacks LeaveAll; LeaveAll 1371")
assert j["leave_all"]["runs"]["sent"] == 2 and not j["leave_all"]["failing"], j
assert not j["failing"] and not j["over"], j
# Correct counterpart: MSRP includes LeaveAll at its first opportunity.
j = check("clean_overlap", [(1000,MSRP,False),(1040,MVRP,False),
                            (1181,MSRP,True),(1221,MVRP,True)],
          [(1050,la),(1180,join),(1190,la),(1220,join)],
          "Must pass: each participant sends LeaveAll at its own first opportunity")
assert j["leave_all"]["runs"]["sent"] == 2 and not j["leave_all"]["failing"], j
# A single-participant late control verifies that the ordinary late arm works.
j = check("late_control", [(1000,MSRP,False),(1240,MSRP,True)], [(1050,la),(1180,join)],
          "Must fail: LeaveAll 60 ms after opportunity 1180")
assert j["leave_all"]["runs"]["late"] == 1, j
print("REPRODUCED: cross-participant skipped LeaveAll escapes; single-participant late control fails")
