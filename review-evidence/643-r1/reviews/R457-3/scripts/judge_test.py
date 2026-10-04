#!/usr/bin/env python3
"""R457-2 offline test of tdm8_render_mutants.py's --law-boundary judge and
argument parsing, on synthetic leg output. No build, no simulation.

usage: judge_test.py <suite dir>
"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import tdm8_render_mutants as m  # noqa: E402

ok = True


def expect(what, cond):
    global ok
    print(("[ok]   " if cond else "[BAD]  ") + what)
    ok &= bool(cond)


FILL = m.LAW_CHECK_STEMS[0]
BAND = m.LAW_CHECK_STEMS[1]


def leg(rows, extra_fails=()):
    """rows: (phase, outcome, [failed stems])"""
    out = []
    for p, o, fails in rows:
        for s in fails:
            out.append(f"  [FAIL] T30 INTERNAL LAW +{p}: {s}")
        out.append(f"  [BOUNDARY] +{p}: {o}, {len(fails)} check(s) failed")
    out += [f"  [FAIL] {f}" for f in extra_fails]
    out.append("RESULT: x")
    return "\n".join(out)


# the sound design
p, _ = m.boundary_problems(leg([(1, "graded PASS", []), (2, "NOT GRADABLE", [])]), True, [1, 2])
expect("sound: graded PASS + NOT GRADABLE is clean", p == [])
p, _ = m.boundary_problems(leg([(1, "graded FAIL", [FILL])]), True, [1])
expect("sound: a graded FAIL is refused", p)
p, _ = m.boundary_problems(leg([(1, "NOT GRADABLE", ["the aligner held"])]), True, [1])
expect("sound: NOT GRADABLE with a failed check is refused", p)
p, _ = m.boundary_problems(leg([(1, "graded PASS", [])]), True, [1, 2])
expect("sound: a requested phase with no verdict is refused", p)
p, _ = m.boundary_problems(leg([(1, "graded PASS", [])]).replace("RESULT: x", ""), True, [1])
expect("sound: no RESULT line (a crash) is refused", p)
p, _ = m.boundary_problems(leg([(1, "graded PASS", [])], ["something else"]), True, [1])
expect("sound: a stray failing check is refused", p)
# a setpoint defect
p, _ = m.boundary_problems(leg([(1, "graded FAIL", [FILL, BAND]), (2, "NOT GRADABLE", [])]), False, [1, 2])
expect("defect: graded FAIL on both stems + NOT GRADABLE is clean", p == [])
p, _ = m.boundary_problems(leg([(1, "graded PASS", [])]), False, [1])
expect("defect: a graded PASS is refused", p)
p, _ = m.boundary_problems(leg([(1, "graded FAIL", [FILL])]), False, [1])
expect("defect: a graded FAIL on the fill alone is refused", p)
p, _ = m.boundary_problems(leg([(1, "graded FAIL", [BAND])]), False, [1])
expect("defect: a graded FAIL on the band alone is refused", p)
p, _ = m.boundary_problems(leg([(1, "graded FAIL", [FILL, BAND, "T30 INTERNAL LAW +1: the aligner held its settled report through the phase"])]), False, [1])
expect("defect: a graded FAIL that also fails the settled hold is refused", p)
# a scan must hold both kinds
runs = [("d", "scan", True, [1, 2], True)]
pa, fa = m.judge_boundary_rounds(runs, [(0, leg([(1, "graded PASS", []), (2, "graded PASS", [])]))])
expect("scan with no NOT GRADABLE phase is refused", fa == 1)
pa, fa = m.judge_boundary_rounds(runs, [(0, leg([(1, "NOT GRADABLE", []), (2, "NOT GRADABLE", [])]))])
expect("scan with only NOT GRADABLE phases is refused", fa == 1)
pa, fa = m.judge_boundary_rounds(runs, [(0, leg([(1, "graded PASS", []), (2, "NOT GRADABLE", [])]))])
expect("scan with both kinds passes", pa == 1 and fa == 0)
# argument parsing
for argv, want in ([[], ("full", 1)], [["--leg-defects"], ("--leg-defects", 1)],
                   [["--law-boundary"], ("--law-boundary", 1)],
                   [["--law-boundary", "--jobs", "6"], ("--law-boundary", 6)]):
    expect(f"parse_args({argv}) == {want}", m.parse_args(argv) == want)
for argv in (["--jobs", "4"], ["--law-boundary", "--jobs", "0"], ["--law-boundary", "--jobs"],
             ["--leg-defects", "--law-boundary"], ["--leg-defects", "--jobs", "2"], ["--bogus"]):
    try:
        m.parse_args(argv)
        expect(f"parse_args({argv}) refused", False)
    except SystemExit as e:
        expect(f"parse_args({argv}) refused (exit {e.code})", e.code == 2)
print("ALL OK" if ok else "SOME BAD")
sys.exit(0 if ok else 1)
