#!/usr/bin/env python3
"""R456-3: offline unit checks of the round-3 runner changes in
tdm8_render_mutants.py (#643, head 36207e91). Usage: r3_runner_checks.py SUITE_DIR

1. OFFSETS_LINE parses a window line in the leg's exact printf format
   (sim_tdm8_render.cpp the_window_is_gradable), with and without the
   walk_wraps() suffix, for negative, zero and positive offsets.
2. window_walks() returns (phase, low, high, walk, clearance) in order and
   ignores the T30 CRF LAW line and the histogram line.
3. print_the_largest_walk() names the largest walk, where, and the stated walk.
4. run_mutations()'s verdict lines quote a string target once and a tuple
   target as "<first>" and N more, with no stray quote (R456-2 S4), with the
   build and the leg stubbed out.
Nothing is built or run; the module is imported with bytecode writing off."""
import contextlib
import io
import sys
from pathlib import Path

sys.dont_write_bytecode = True
suite = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(suite))
import tdm8_render_mutants as m  # noqa: E402

ok = True


def chk(name: str, cond: bool) -> None:
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name)


FMT = ("  [i]    %s: over %d steady PDU ends the first pop after the end is taken "
       "%+d..%+d cycles from it and the pop nearest the boundary %+d..%+d (walk %d); "
       "the least clearance is %d cycles, at PDU %d (offset %+d), against the %d-cycle "
       "ambiguity window: margin %d%s\n")
WRAP = ("; the nearest pop changes side half a tick from the grid, so the walk is "
        "the first pop after's range")


def line(tag, ends, nmin, nmax, dmin, dmax, walk, clear, cid, cdel, w, suffix=""):
    return FMT % (tag, ends, nmin, nmax, dmin, dmax, walk, clear, cid, cdel, w,
                  clear - w, suffix)


out = "".join([
    "[LAW-BOUNDARY] T30's INTERNAL law at the feed phases where a PDU end meets a pop "
    "(the ambiguity window is 9 cycles: a walk of 5 plus a guard of 4)\n",
    line("T30 INTERNAL LAW +0", 124, 2025, 2027, -58, -56, 2, 56, 7, -56, 9),
    "  [i]    T30 INTERNAL LAW +0: PDU ends per nearest-pop offset (offset:ends): -58:3 -57:90\n",
    line("T30 INTERNAL LAW +2026", 124, 1, 2083, -1, 0, 1, 0, 9, 0, 9),
    line("T30 INTERNAL LAW +984", 124, 1040, 1043, -1043, 1042, 3, 1040, 11, 1041, 9, WRAP),
    line("T30 CRF LAW", 292, 1495, 1500, -592, -587, 5, 587, 900, -587, 9),
])
ww = m.window_walks(out)
chk(f"window_walks parses the three [LAW] lines, not CRF or the histogram: {ww}",
    ww == [(0, -58, -56, 2, 56), (2026, -1, 0, 1, 0), (984, -1043, 1042, 3, 1040)])
chk("a zero offset printed '+0' parses", ww[1][2] == 0)
chk("the wrap suffix does not stop the line parsing", len(ww) == 3 and ww[2][3] == 3)
st = [x[1] for x in m.STATED_WALK_LINE.finditer(out)]
chk(f"STATED_WALK_LINE reads the stated walk: {st}", st == ["5"])

runs = [("the unmutated gateware", "ascending", True, [0], True)]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    m.print_the_largest_walk(runs, [(0, out)])
txt = buf.getvalue().strip()
print("    " + txt)
chk("print_the_largest_walk names walk 3 at +984 over 3 windows and stated 5",
    txt == "[i] law boundary: the largest walk over 3 windows is 3 cycles "
           "(the unmutated gateware, ascending, +984); the leg states a walk of 5")

# 4. verdict lines, the build and leg stubbed
tup = ("check A", "check B", "check C")
m.MUTATIONS = (("mut one", "dp", [], "ship", "--law-only", "check S"),
               ("mut two", "dp", [], "ship", "--law-only", tup),
               ("mut three", "dp", [], "ship", "--law-only", tup))
m.plant = lambda *a, **k: ("value", None)
m.build = lambda *a, **k: Path("/nonexistent")
m.SOURCES = {"dp": (None, "DP_SRC")}
m.run_leg = lambda exe, mode: (1, "")
answers = iter(["caught", "caught", "pass"])
m.verdict = lambda *a: next(answers)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    tally = m.run_mutations(Path("/nonexistent"))
lines = buf.getvalue().splitlines()
for ln in lines:
    print("    " + ln)
chk("string target quoted once",
    lines[0] == '[PASS] mutant caught (ship --law-only): mut one - breaks "check S"')
chk("tuple target: first name quoted, then 'and 2 more', no stray quote",
    lines[1] == '[PASS] mutant caught (ship --law-only): mut two - breaks "check A" and 2 more')
chk("survivor line uses the same naming",
    lines[2] == '[FAIL] mutant SURVIVED: mut three. The leg does not prove "check A" and 2 more.')
chk(f"tally {tally}", tally == (2, 1))
sys.exit(0 if ok else 1)
