#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Every boot path that enables the entity starts the restore walk.

Since processor pin d352bbaa the processor holds its ACMP listener and AECP
from reset until the restore walk reaches its terminal, and PP_CTRL[1] starts
that walk (parent issue #70, 5880276193 item 2). A boot that enables the
entity without starting it leaves the entity deaf and uncontrollable.
"""
from pathlib import Path

import test_nvm_firmware as nvm

#: planted startup states that reach a boot path of their own
SHAPE_OFF = ("return count == NVM_N_REC && bytes == NVM_AREA_RAW &&",
             "return 0 && count == NVM_N_REC && bytes == NVM_AREA_RAW &&")
#: the NVM_LOAD_TRIES refusals that leave the window unvalidated
REFUSE_ALL = ("--refuse-loads", "4")
TIMEOUT_LINE = "the restore walk did not sequence in time"


def cases(bench: nvm.Bench, disabled: nvm.Bench) -> list[tuple[str, nvm.Bench, tuple, dict]]:
    """(label, bench, harness arguments, expected summary fields) per boot path."""
    walked = dict(walks=1, enable_first=0)
    return [
        ("cold boot", bench, ("--boot",), dict(walked, done=1, closed=0)),
        ("refused window", bench, REFUSE_ALL + ("--boot",), dict(walked, done=1, fail=1)),
        ("persistence disabled", disabled, ("--boot",), dict(walked, done=1, fail=1)),
        ("cold boot, CLOSED restore", bench, ("--walk-closed", "--boot"),
         dict(walked, done=0, fail=1, closed=1)),
        ("persistence disabled, CLOSED restore", disabled, ("--walk-closed", "--boot"),
         dict(walked, done=0, fail=1, closed=1)),
    ]


def grade_benches(bench: nvm.Bench, disabled: nvm.Bench) -> list[str]:
    """Boot every path; each must start one walk before the enable and end at its terminal."""
    findings = []
    for label, target, args, expect in cases(bench, disabled):
        raw, summary, _ = nvm.run(target, *args)
        if target is disabled and "persistence disabled" not in raw:
            raise RuntimeError("boot-walk precondition was not reached: " + label)
        for key, want in expect.items():
            if summary.get(key) != want:
                findings.append(f"boot walk, {label}: {key}={summary.get(key)}, expected {want}")
        # a CLOSED restore never raises done; the wait must end at the
        # terminal rather than spend its whole timeout on it
        if TIMEOUT_LINE in raw:
            findings.append(f"boot walk, {label}: the restore wait ran out its timeout")
    return findings


def grade(cfg: Path, work: Path, source: str, bench: nvm.Bench) -> list[str]:
    """The shipping bench, plus one with the persistence-disabled path planted."""
    if source.count(SHAPE_OFF[0]) != 1:
        raise RuntimeError("boot-walk shape precondition anchor changed")
    disabled = nvm.make_bench(cfg, work / "shape-off", source.replace(*SHAPE_OFF))
    findings = grade_benches(bench, disabled)
    print(f"boot-walk {cfg.stem}: {len(cases(bench, disabled))} boot paths; "
          + (f"{len(findings)} finding(s)" if findings else "each starts one walk before the enable"))
    return findings


#: the defects the grade above must catch, each planted into a copy
MUTATIONS = {
    # the persistence-disabled path returning before the walk, as at dev
    "shape_path_skips_walk": (
        "\t\tif (!nvm_restore_ended())\n\t\t\tnvm_restore_walk();\n\t\treturn;\n",
        "\t\treturn;\n"),
    # the restore wait ending on done alone, which a CLOSED restore never raises
    "wait_on_done_only": (
        "\t\t(MILAN_PP_STAT_RESTORE_DONE | MILAN_PP_STAT_RESTORE_CLOSED)) != 0;",
        "\t\tMILAN_PP_STAT_RESTORE_DONE) != 0;"),
}


def self_test(cfg: Path, work: Path, source: str) -> list[str]:
    """Each planted boot-path defect must be caught by a named boot-walk finding."""
    findings = []
    for label, (old, new) in MUTATIONS.items():
        if source.count(old) != 1:
            findings.append(f"boot-walk self-test: the {label} plant no longer matches the firmware")
            continue
        planted = source.replace(old, new)
        bench = nvm.make_bench(cfg, work / label, planted)
        got = grade(cfg, work / label, planted, bench)
        if not any(item.startswith("boot walk, ") for item in got):
            findings.append(f"boot-walk self-test: the {label} defect was NOT caught")
        else:
            print(f"  boot-walk self-test OK: {label:<22} caught by {len(got)} finding(s); "
                  f"first: {got[0]}")
    return findings
