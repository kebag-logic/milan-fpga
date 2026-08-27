#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure where a failure could pass for success, and hold the count down.

Why this exists. Rule 6 of the maintainability guide
(docs/development/CODE_QUALITY.md) says an invalid parameter, state or tool
result must be rejected at the nearest responsible boundary and must propagate
a non-success verdict. Two populations in this tree can break that, and they
break it silently:

  1. A PARAMETERISED MODULE WITH NO ELABORATION CONTRACT. Forty-three
     first-party modules declare parameters; four reject an impossible
     combination at elaboration. The rest accept any value the caller passes.
     `rx_mac_filter` documented "true for TDATA_WIDTH>=48" in a banner for
     months - a comment does not stop a build, and at 32 bits the destination
     compare would have read past the end of the beat and filtered on
     undefined bits, which nothing downstream can detect.

  2. A PIPELINE THAT DISCARDS ITS PRODUCER'S EXIT CODE. In a shell without
     `pipefail`, `gate | tee log` exits with tee's status, so a failing gate
     reads as a pass. This is scored per-line and only for producers that ARE
     a verdict - a tool run, a make, a gate script.

Both are RATCHETS. Neither population can be emptied in one change without
exactly the churn the governing rule forbids, and the second has legitimate
members: `verilator --version | grep -F "$WANT"` deliberately wants grep's
status, because grep IS the assertion. Those are excluded by name, with the
reason recorded.

Usage:
    python3 scripts/measure_fail_fast.py            # both inventories
    python3 scripts/measure_fail_fast.py --check    # the ratchet
    python3 scripts/measure_fail_fast.py --selftest # fixture arms

Exit 0 = at or under the ratchet in scripts/fail_fast.budget.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "fail_fast.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE

COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
PARAM = re.compile(r"\bparameter\s+(?:int|logic|bit|integer|byte)?\s*"
                   r"(?:signed\s+)?(?:\[[^\]]*\]\s*)?(\w+)\s*=")
ELAB_CHECK = re.compile(r"\$fatal|\$error")

#: A pipeline whose producer is a verdict-bearing command. `\|\|` is excluded:
#: `a || b` is a fallback, not a pipe. Matched against shell_code(), never the
#: raw line.
PIPE = re.compile(
    r"^\s*(?P<lhs>.*?\b(?:python3?|make|verilator|yosys|sv2v|behave|pytest"
    r"|\./run\.sh|\./ooc\.sh|scripts/\S+\.(?:py|sh))\b[^|]*?)\|(?!\|)")

#: Pipelines where the CONSUMER is the assertion and its status is the point.
#: Each is matched on the whole line, so a new one has to be added deliberately.
INTENTIONAL = (
    ("--version | grep", "the grep IS the version assertion; its status is the verdict"),
)


def blank_comments(text):
    return COMMENT.sub(lambda m: "".join(c if c == "\n" else " " for c in m.group(0)),
                       text)


def tracked(*pats):
    out = subprocess.run(["git", "ls-files", *pats], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    return [p for p in out
            if not p.startswith(("third_party/", "external/", "protocol-processor/",
                                 "gptp-processor/", "gen/", "build/"))]


def scan_module(text):
    """(declares_parameters, has_elaboration_check) for one SystemVerilog source."""
    code = blank_comments(text)
    return bool(PARAM.search(code)), bool(ELAB_CHECK.search(code))


#: quoted spans and command substitutions, blanked before the producer search
_QUOTED = re.compile(r"\$\([^()]*\)|'[^']*'|\"[^\"]*\"")


def shell_code(line):
    """The part of a shell line that is COMMAND, with quotes and `$(...)`
    blanked out.

    Two false positives forced this. `printf "yosys FAIL: %s" ... | head`
    matched because the tool name was inside a FORMAT STRING, and a pipe inside
    `$(...)` is a substitution feeding an argument - its status is never the
    line's verdict, which is set by the command that consumes it.
    """
    return _QUOTED.sub(lambda m: " " * len(m.group(0)), line)


def scan_pipeline(line):
    """(is_masked, reason) for one shell/workflow line."""
    for needle, why in INTENTIONAL:
        if needle in line:
            return False, why
    if "pipefail" in line:
        return False, "the line sets pipefail"
    if line.lstrip().startswith("#"):
        return False, ""
    return bool(PIPE.match(shell_code(line))), ""


def audit():
    unguarded, guarded = [], []
    for rel in [p for p in tracked("hdl") if p.endswith(".sv") and p not in LINT_EXCLUDE]:
        has_params, has_check = scan_module((REPO / rel).read_text(errors="replace"))
        if not has_params:
            continue
        (guarded if has_check else unguarded).append(rel)

    masked, waived = [], []
    for rel in tracked("*.sh", ".github/workflows/*.yml", "syn/**/*.sh", "harness/**/*.sh"):
        text = (REPO / rel).read_text(errors="replace")
        pipefail_file = "pipefail" in text
        for n, line in enumerate(text.splitlines(), 1):
            is_masked, why = scan_pipeline(line)
            if why:
                waived.append((rel, n, why))
            elif is_masked and not pipefail_file:
                masked.append((rel, n, line.strip()[:96]))
    return unguarded, guarded, masked, waived


def read_budget():
    if not BUDGET.is_file():
        return None, None
    vals = [int(x) for x in re.findall(r"^\s*(\d+)\s*$", BUDGET.read_text(), re.M)]
    return (vals + [None, None])[:2]


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    ck("a module with parameters and no check is unguarded",
       scan_module("module m #(parameter int W = 8)(); endmodule") == (True, False))
    ck("a module with an elaboration $error is guarded",
       scan_module("module m #(parameter int W = 8)();\n if (W < 2) $error(\"no\");\n"
                   "endmodule") == (True, True))
    ck("a module with no parameters is not counted",
       scan_module("module m (); endmodule") == (False, False))
    ck("an $error inside a COMMENT does not count as a guard",
       scan_module("module m #(parameter int W = 8)();\n // $error(\"no\");\n"
                   "endmodule") == (True, False),
       "comments are blanked before the search")

    ck("a piped gate is masked", scan_pipeline("  python3 scripts/x.py | tee log")[0])
    ck("a piped make is masked", scan_pipeline("  make run | tail -5")[0])
    ck("a fallback is not a pipe", not scan_pipeline("  python3 scripts/x.py || exit 2")[0])
    ck("a comment is not a pipeline", not scan_pipeline("  # python3 x.py | tee log")[0])
    ck("a tool name inside a string is not a producer",
       not scan_pipeline('  printf "yosys FAIL: %s" "$x" | head -1')[0],
       "the match came from a format string, not a command")
    ck("a pipe inside a command substitution is not the line's verdict",
       not scan_pipeline('  msg=$(grep ERROR log | head -1); python3 x.py')[0])
    ck("a line that sets pipefail is not masked",
       not scan_pipeline("  set -o pipefail; python3 x.py | tee log")[0])
    ck("the version assertion is waived by name, with a reason",
       scan_pipeline('  verilator --version | grep -F "$WANT"') == (False,
       "the grep IS the version assertion; its status is the verdict"))
    ck("an ordinary command is not a pipeline",
       not scan_pipeline("  python3 scripts/x.py")[0])

    unguarded, guarded, masked, waived = audit()
    ck("the live scan reads the tree", len(unguarded) + len(guarded) > 20,
       f"{len(unguarded)} + {len(guarded)} modules with parameters")
    ck("the guarded set is not empty", len(guarded) >= 4,
       "an inert scan would report every module unguarded")
    ck("the waiver actually fires on the live tree", bool(waived),
       "no intentional pipeline was seen - the waiver is untested here")

    n = 16
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet both counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    unguarded, guarded, masked, waived = audit()

    print(f"parameterised modules with no elaboration contract "
          f"({len(unguarded)} of {len(unguarded) + len(guarded)}):")
    for rel in unguarded:
        print(f"   {rel}")
    print(f"\npipelines that discard their producer's exit code ({len(masked)}):")
    for rel, n, line in masked:
        print(f"   {rel}:{n}  {line}")
    print(f"\nwaived, with a reason ({len(waived)}):")
    for rel, n, why in waived:
        print(f"   {rel}:{n}  {why}")

    if not args.check:
        return 0

    b_unguarded, b_masked = read_budget()
    if b_unguarded is None or b_masked is None:
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} must hold two counts")
        return 1
    bad = False
    if len(unguarded) > b_unguarded:
        print(f"\nFAIL: {len(unguarded)} module(s) without an elaboration contract "
              f"> ratchet {b_unguarded}. A new parameter states what it refuses.")
        bad = True
    if len(masked) > b_masked:
        print(f"\nFAIL: {len(masked)} masked pipeline(s) > ratchet {b_masked}. "
              f"A verdict must not be piped away.")
        bad = True
    if bad:
        return 1
    print(f"\nFAIL-FAST RATCHET: PASS ({len(unguarded)} <= {b_unguarded} modules "
          f"without an elaboration contract, {len(masked)} <= {b_masked} masked "
          f"pipeline(s), {len(waived)} waived with a reason)")
    if len(unguarded) < b_unguarded or len(masked) < b_masked:
        print(f"  the ratchets can be lowered to {len(unguarded)} and {len(masked)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
