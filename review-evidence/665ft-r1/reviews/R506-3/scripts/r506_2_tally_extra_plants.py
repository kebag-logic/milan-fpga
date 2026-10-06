#!/usr/bin/env python3
"""R506-2 probe: the listener's stated behaviours that tally_selftest.py does not plant.

Usage: python3 tally_extra_plants.py <review clone>
Builds r506_2_extra_cases.cpp (beside this script) against the clone's listener and
against copies with one defect planted each. Prints, per defect, whether the
clone's own planted cases (tally_selftest.CASES) catch it and whether the
extra cases do.
"""
import os, sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import fw_gtest, tally_selftest as ts  # noqa: E402
HERE = Path(__file__).resolve().parent
EXTRA = (
    ts.Case("SIGFPE inside a test", "Sig.Fpe", False, (1, 1), "Sig.Fpe"),
    ts.Case("SIGBUS inside a test", "Sig.Bus", False, (1, 1), "Sig.Bus"),
    ts.Case("SIGILL inside a test", "Sig.Ill", False, (1, 1), "Sig.Ill"),
    ts.Case("a failure in a suite's tear-down", "TearDownFails.*", False, (1, 1), "TearDownFails"),
    ts.Case("a failure in a global environment", "Pass.*", False, (1, 1), "(program)", env=(("R506_ENV_FAIL", "1"),)),
    ts.Case("a disabled suite", "DISABLED_WholeSuite.*", False, (0, 1), "DISABLED_WholeSuite.NeverRuns"),
)
DEFECTS = (
    ts.Defect("sigfpe-unhandled", "for (const int sig : {SIGSEGV, SIGBUS, SIGFPE, SIGILL, SIGABRT})",
              "for (const int sig : {SIGSEGV, SIGBUS, SIGILL, SIGABRT})", ()),
    ts.Defect("sigbus-unhandled", "for (const int sig : {SIGSEGV, SIGBUS, SIGFPE, SIGILL, SIGABRT})",
              "for (const int sig : {SIGSEGV, SIGFPE, SIGILL, SIGABRT})", ()),
    ts.Defect("program-failure-not-counted",
              '"  [FAIL] (program): a failure outside every test\\n");\n            failures++;',
              '"  [FAIL] (program): a failure outside every test\\n");', ()),
    ts.Defect("disabled-suite-not-counted",
              'std::strncmp(suite->name(), "DISABLED_", 9) == 0 || std::strncmp(info->name(), "DISABLED_", 9) == 0',
              'std::strncmp(info->name(), "DISABLED_", 9) == 0', ()),
)
def build_extra(out, b, main_source):
    objs = fw_gtest.compile_tests(b, [f"-I{clone / 'sw/firmware/gtest'}"], [HERE / "r506_2_extra_cases.cpp", main_source], out)
    return fw_gtest.link(b, objs, out / "extra_cases")
def red(cases, exe, work):
    out = {}
    for c in cases:
        old = dict(os.environ)
        os.environ.update(dict(c.env))
        try:
            out[c.what] = ts.grade_case(ts.Case(c.what, c.gtest_filter, c.passes, c.tally, c.names, c.nocount), exe, work, quiet=True)
        finally:
            os.environ.clear(); os.environ.update(old)
    return out
def main():
    print(f"toolchain: {fw_gtest.toolchain()}")
    b = fw_gtest.Build()
    rc = 0
    with tempfile.TemporaryDirectory(prefix="r506-tally.") as tmp:
        w = Path(tmp)
        (w / "base").mkdir()
        base_extra = build_extra(w / "base", b, fw_gtest.MAIN_SOURCE)
        for what, wrong in red(EXTRA, base_extra, w / "base").items():
            print(f"[{'ok' if not wrong else 'FAIL'}] unmutated listener, extra case {what}: {wrong[:1] or 'reads as planted'}")
            rc |= bool(wrong)
        for d in DEFECTS:
            o = w / d.name; o.mkdir()
            src = ts.plant(d, o)
            own = ts.build(o / "own", b, src) if (o / "own").mkdir() is None else None
            own_red = {c.what: ts.grade_case(c, own, o / "own", quiet=True) for c in ts.CASES if not c.env}
            own_caught = sorted(k for k, v in own_red.items() if v)
            (o / "x").mkdir()
            ex = build_extra(o / "x", b, src)
            ex_red = {k: v for k, v in red(EXTRA, ex, o / "x").items() if v}
            print(f"[defect] {d.name}: clone's planted cases reddened: {own_caught or 'NONE (escape)'}; "
                  f"extra cases reddened: {sorted(ex_red) or 'none'}"
                  + (f" ({next(iter(ex_red.values()))[0]})" if ex_red else ""))
    return rc
sys.exit(main())
