#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Every boot path that enables the entity starts the restore walk.

Since processor pin d352bbaa the processor holds its ACMP listener and AECP
from reset until the restore walk reaches its terminal, and PP_CTRL[1] starts
that walk (parent issue #70, 5880276193 item 2). A boot that enables the
entity without starting it leaves the entity deaf and uncontrollable.

The console reports what the firmware knows and no more (D3 section 5.3,
change 3): the enable is a REQUEST the fabric holds until the restore releases
it, so no boot path may claim an enabled entity, and a wait that runs out
reports that the restore has not reached its terminal and that the fabric
holds the enable.
"""
from pathlib import Path
import re

import test_nvm_firmware as nvm

#: planted startup states that reach a boot path of their own
SHAPE_OFF = ("return count == NVM_N_REC && bytes == NVM_AREA_RAW &&",
             "return 0 && count == NVM_N_REC && bytes == NVM_AREA_RAW &&")
#: the NVM_LOAD_TRIES refusals that leave the window unvalidated
REFUSE_ALL = ("--refuse-loads", "4")
#: the bounded wait's report at its timeout
TIMEOUT_LINE = ("Milan NVM: the restore walk has not reached its terminal; "
                "the fabric holds the entity enable until it does.")
#: entity_advertise()'s report after its two writes, once per verified boot
REQUEST_LINE = ("Milan baremetal: fabric entity enable requested; the fabric holds "
                "it until the restore releases it; UART diagnostics ready.")
#: any wording that claims the entity IS enabled, which the firmware cannot
#: know when it prints and which a CLOSED restore makes false until reset
ENABLED_CLAIM = re.compile(r"entity (?:is )?enabled\b")


def cases(bench: nvm.Bench, disabled: nvm.Bench) -> list[tuple[str, nvm.Bench, tuple, dict]]:
    """(label, bench, harness arguments, expected summary fields) per boot path.

    A label carrying "stalled" is a walk that never reaches a terminal, the
    one path whose wait must run out and say so."""
    walked = dict(walks=1, enable_first=0)
    return [
        ("cold boot", bench, ("--boot",), dict(walked, done=1, closed=0)),
        ("refused window", bench, REFUSE_ALL + ("--boot",), dict(walked, done=1, fail=1)),
        ("persistence disabled", disabled, ("--boot",), dict(walked, done=1, fail=1)),
        ("cold boot, CLOSED restore", bench, ("--walk-closed", "--boot"),
         dict(walked, done=0, fail=1, closed=1)),
        ("persistence disabled, CLOSED restore", disabled, ("--walk-closed", "--boot"),
         dict(walked, done=0, fail=1, closed=1)),
        ("cold boot, stalled restore", bench, ("--walk-stall", "--boot"),
         dict(walked, done=0, closed=0)),
        ("persistence disabled, stalled restore", disabled, ("--walk-stall", "--boot"),
         dict(walked, done=0, closed=0)),
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
        if "stalled" not in label and TIMEOUT_LINE in raw:
            findings.append(f"boot walk, {label}: the restore wait ran out its timeout")
        if "stalled" in label and TIMEOUT_LINE not in raw:
            findings.append(f"boot walk, {label}: the timeout did not report that the "
                            "restore has not reached its terminal and the fabric holds the enable")
        if raw.count(REQUEST_LINE) != 1:
            findings.append(f"boot walk, {label}: the enable request was reported "
                            f"{raw.count(REQUEST_LINE)} time(s), expected once")
        claim = ENABLED_CLAIM.search(raw)
        if claim:
            findings.append(f"boot walk, {label}: the console claims the entity enabled "
                            f"({claim.group(0)!r}) with done={summary.get('done')} "
                            f"closed={summary.get('closed')}")
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


#: the defects the grade above must catch, each planted into a copy, and
#: the words of the finding that must name it
MUTATIONS = {
    # the persistence-disabled path returning before the walk, as at dev
    "shape_path_skips_walk": (
        "\t\tif (!nvm_restore_ended())\n\t\t\tnvm_restore_walk();\n\t\treturn;\n",
        "\t\treturn;\n",
        "boot walk, persistence disabled: walks=0, expected 1"),
    # the restore wait ending on done alone, which a CLOSED restore never raises
    "wait_on_done_only": (
        "\t\t(MILAN_PP_STAT_RESTORE_DONE | MILAN_PP_STAT_RESTORE_CLOSED)) != 0;",
        "\t\tMILAN_PP_STAT_RESTORE_DONE) != 0;",
        "boot walk, cold boot, CLOSED restore: the restore wait ran out its timeout"),
    # the enable line as at dev 1e80128f: it claims an enabled entity after
    # a CLOSED restore, which holds the enable until reset
    "enable_line_claims_enabled": (
        'printf("' + REQUEST_LINE + '\\n");',
        'printf("Milan baremetal: fabric entity enabled; UART diagnostics ready.\\n");',
        "boot walk, cold boot, CLOSED restore: the console claims the entity enabled"),
    # the timeout line as at dev 1e80128f: it neither names the terminal
    # nor says that the fabric holds the enable
    "timeout_line_holds_unsaid": (
        'printf("' + TIMEOUT_LINE + '\\n");',
        'printf("Milan NVM: the restore walk did not sequence in time.\\n");',
        "boot walk, cold boot, stalled restore: the timeout did not report"),
}


def self_test(cfg: Path, work: Path, source: str) -> list[str]:
    """Each planted boot-path defect must be caught by a named boot-walk finding."""
    findings = []
    for label, (old, new, words) in MUTATIONS.items():
        if source.count(old) != 1:
            findings.append(f"boot-walk self-test: the {label} plant no longer matches the firmware")
            continue
        planted = source.replace(old, new)
        bench = nvm.make_bench(cfg, work / label, planted)
        got = grade(cfg, work / label, planted, bench)
        named = [item for item in got if item.startswith(words)]
        if not named:
            findings.append(f"boot-walk self-test: the {label} defect was NOT caught by "
                            f"{words!r}; findings: {got}")
        else:
            print(f"  boot-walk self-test OK: {label:<36} caught by {len(got)} finding(s); "
                  f"named: {named[0]}")
    return findings
