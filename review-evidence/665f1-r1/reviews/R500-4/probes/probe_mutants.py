#!/usr/bin/env python3
"""Reviewer probe (R500-4): plant reviewer-chosen defects into scratch copies
of sw/firmware/ctrl_nvm at the review head and grade named checks with the
head's own suite code, printing every finding (not only the first).

Usage: probe_mutants.py <clone> <workdir> [name ...]
Exit 0 when every probe's expectation holds (see EXPECT)."""
import shutil
import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(CLONE / "sw/firmware/ctrl_nvm/test"))

import nvm_mutants as nm                                   # noqa: E402
from nvm_bench import ROOT, shape_inputs                    # noqa: E402
import test_ctrl_nvm as t                                   # noqa: E402

STORE, LITESPI, FMODEL = nm.STORE, nm.LITESPI, "host/nvm_fmodel.c"
ARTY, ONE = "endstation_arty_current", "endstation_ax7101_1x1_tdm8"
DIGEST = "seen[j].digest == seen[n].digest &&\n\t\t    "
VARY = "dst[fm.fault_at - addr] ^= (uint8_t)(0x08u << (fm.varied++ % 5u));"

# name: (seams, shape, checks, expectation) with expectation "fail" (some
# named check must report a finding) or "pass" (all named checks green).
PROBES = {
    # the deadline alone truncated to whole clocks per us, the time base exact
    "deadline_only_truncated": (((LITESPI, nm.CALL_TICKS,
        "const uint32_t nvm_flash_litespi_call_ticks = "
        "LS_CALL_US * (CONFIG_CLOCK_FREQUENCY / 1000000u);"),), ARTY, ("port_clock",), "fail"),
    # the time base alone truncated, the deadline exact
    "timebase_only_truncated": (((LITESPI, nm.TO_US,
        "\treturn ls_ticks / (CONFIG_CLOCK_FREQUENCY / 1000000u);"),), ARTY,
        ("port_clock", "time_base"), "fail"),
    # the shipped round-4 mutant, every finding listed (data loss vs count)
    "refusal_by_verdict_all": (((STORE, nm.SAME_BYTES, "seen[j].vd == seen[n].vd"),), ONE,
        ("read_disagreement",), "fail"),
    # agreement on verdict and byte count, digest dropped
    "agree_without_digest": (((STORE, DIGEST, ""),), ONE, ("read_disagreement",), "fail"),
    # the fault model's third read repeats the first corruption (XOR 8, 16, 8):
    # the head must let read 3 agree with read 1, so the slot is REFUSED (not
    # UNREAD): the expected-held case is then expected to FAIL under the head.
    # This documents the any-pair agreement, a stated limit, not a defect.
    "model_repeats_first": (((FMODEL, VARY,
        "dst[fm.fault_at - addr] ^= (uint8_t)(0x08u << (fm.varied++ % 2u));"),), ONE,
        ("read_disagreement",), "fail"),
}


def main() -> int:
    names = sys.argv[3:] or list(PROBES)
    inputs = {}
    rc = 0
    for name in names:
        seams, stem, checks, want = PROBES[name]
        if stem not in inputs:
            inputs[stem] = shape_inputs(ROOT / "configs" / f"{stem}.yaml", WORK / "in" / stem)
        m = nm.Mutant(name, seams, checks)
        tree = WORK / name / "tree"
        if tree.exists():
            shutil.rmtree(tree)
        nm.plant(m, tree)
        b = t.bench_for(inputs[stem], WORK / name, tree)
        res = t.grade(b, list(checks))
        failed = any(res[c] for c in checks)
        ok = failed if want == "fail" else not failed
        rc |= 0 if ok else 1
        print(f"PROBE {name} at {stem} ({b.clock_hz} Hz): want {want}, "
              f"{'FAILED' if failed else 'PASSED'} -> {'as expected' if ok else 'UNEXPECTED'}")
        for c in checks:
            print(f"  {c}: {len(res[c])} finding(s)")
            for x in res[c]:
                print(f"    {x[:400]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
