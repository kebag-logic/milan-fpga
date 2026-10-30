"""Reviewer probe: the split platform's host arms at the head and a chosen set of planted defects.

Usage: python3 -B plat_probe.py <checkout> <work-dir> [--no-asan]

Imports the checkout's own campaign code (ctrl_mutants.plant / caught, plat_arms) read only, plants each
probe defect into a copy under <work-dir>, and runs the arm and named test the defect names. Prints one
line per arm and per defect; exit 0 when the head is green and every defect is graded as this script
requires (shipped and extra plants caught; with --no-asan, the console revert must ESCAPE, which shows the
sanitizer is what catches it).
"""
from __future__ import annotations

import dataclasses
import shutil
import sys
from pathlib import Path

checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
no_asan = "--no-asan" in sys.argv
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))

import ctrl_mutants as cm  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

if no_asan:
    original = plat_arms.arm_plat

    def arm_plat_without_sanitizer(tree):
        """arm_plat with the sanitizer withheld: the same sources and tests, address_sanitizer forced off."""
        real = dataclasses.replace

        def no_sanitizer(obj, **kw):
            if "address_sanitizer" in kw:
                kw["address_sanitizer"] = False
            return real(obj, **kw)
        plat_arms.dataclasses.replace = no_sanitizer
        try:
            return original(tree)
        finally:
            plat_arms.dataclasses.replace = real
    plat_arms.arm_plat = arm_plat_without_sanitizer

ARMS = {"plat": plat_arms.arm_plat, "platboot1": lambda t: plat_arms.arm_platboot(t, 1),
        "platboot2": lambda t: plat_arms.arm_platboot(t, 2)}
by_name = {m.name: m for m in cm.MUTANTS}
SHIPPED = ("plat-command-read-past-its-end", "plat-saved-state-after-mailbox-open", "plat-store-service-unbound")
PLAT = "plat/ctrl_plat.c"
CONSOLE = "plat/ctrl_plat_console.c"
EXTRA = (
    # the saved state never read at all: the boot must not reach READY (B1)
    Mutant("probe-saved-state-never-read", PLAT, "\tnvm_store_boot(env->flash, &p->binding.port);\n", "",
           "platboot1", "Boot.B1ReachesReadyInStepOrder", "B1 the boot reaches its ready state"),
    # the compare reads one byte past the command whenever the line is longer: ASan in K3
    Mutant("probe-compare-one-past", CONSOLE,
           "while (n < c->len && command[n] != '\\0' && command[n] == c->line[n]) {",
           "while (n < c->len && (command[n] != '\\0' || command[n + 1] == 'x') && command[n] == c->line[n]) {",
           "plat", "Plat.K3LinesEndOnceAndOthersAreRefused", "crashed on signal"),
)


def run(m: Mutant | None) -> tuple[bool, list[str]]:
    """Plant m (None: the head as it is) and run its arms; (graded as required, report lines)."""
    root = work / (m.name if m else "head")
    if m is None:
        copy = root / "work" / "ctrl"
        stack = root / "work" / "tsn-c-stack"
        shutil.rmtree(root / "work", ignore_errors=True)
        shutil.copytree(cm.CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
        for part in cm.STACK_PARTS:
            shutil.copytree(cm.STACK / part, stack / part)
        kills = [(a, "", "") for a in ARMS]
    else:
        copy, stack = cm.plant(m, root)
        kills = m.kills()
    tree = Tree(copy, root / "work" / "build", root / "reuse", fw_gtest.Build(jobs=4), stack)
    ok, lines = True, []
    for arm, test, needle in kills:
        try:
            outcome = ARMS[arm](tree)
        except Refusal as exc:
            outcome = Outcome(arm, 2, f"refused: {exc}")
        (root / f"{arm}.log").write_text(outcome.log)
        fails = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
        if m is None:
            good = outcome.rc == 0
            lines.append(f"HEAD arm {arm}: rc {outcome.rc} ({'PASS' if good else 'FAIL'}); "
                         f"{outcome.log.strip().splitlines()[-1] if outcome.log.strip() else ''}")
        else:
            got = cm.caught(test, needle, outcome)
            want_escape = no_asan and m.name in ("plat-command-read-past-its-end", "probe-compare-one-past")
            good = (not got) if want_escape else got
            lines.append(f"MUTANT {m.name} [{arm}] {'caught' if got else 'ESCAPED'} on {test} {needle!r} "
                         f"(required {'ESCAPED, sanitizer withheld' if want_escape else 'caught'}): "
                         f"{'as required' if good else 'WRONG'}; rc {outcome.rc}; {len(fails)} [FAIL] line(s)"
                         f"{'; first: ' + fails[0][:160] if fails else ''}")
        ok &= good
    shutil.rmtree(root / "work", ignore_errors=True)
    return ok, lines


def main() -> int:
    work.mkdir(parents=True, exist_ok=True)
    plan = ([None] if not no_asan else []) + [by_name[n] for n in SHIPPED if not no_asan or "command" in n]
    plan += [m for m in EXTRA if not no_asan or m.path == CONSOLE]
    wrong = 0
    for m in plan:
        ok, lines = run(m)
        wrong += not ok
        print("\n".join(lines), flush=True)
    print(f"plat_probe{' (sanitizer withheld)' if no_asan else ''}: {len(plan) - wrong} of {len(plan)} as required")
    return 1 if wrong else 0


if __name__ == "__main__":
    raise SystemExit(main())
