#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure where a failure could pass for success, and hold the count down.

Why this exists. Rule 6 of the maintainability guide
(docs/development/CODE_QUALITY.md) says an invalid parameter, state or tool
result must be rejected at the nearest responsible boundary and must propagate
a non-success verdict. Two populations in this tree can break that, and they
break it silently:

  1. A PARAMETERISED MODULE WITH NO ELABORATION CONTRACT. Fifty-three
     first-party modules across the superproject and its project-owned
     processor submodules declare parameters; ten reject an impossible
     combination at elaboration. The rest accept any value the caller passes.
     `rx_mac_filter` documented "true for TDATA_WIDTH>=48" in a banner for
     months - a comment does not stop a build, and at 32 bits the destination
     compare would have read past the end of the beat and filtered on
     undefined bits, which nothing downstream can detect.

  2. A PIPELINE THAT DISCARDS ITS PRODUCER'S EXIT CODE. In a shell without
     `pipefail`, `gate | tee log` exits with tee's status, so a failing gate
     reads as a pass. This is scored per-line and only for producers that ARE
     a verdict - a tool run, a make, a gate script - and, since review, a
     leftmost `grep`/`cat` that READS A FILE: `grep -A2 "LUTs" util.rpt |
     head` under `set -e` without pipefail exits 0 when the report does not
     exist, which is how a synthesis flow whose tools produced nothing was
     published as measured (gptp-processor/syn/ooc/run.sh, at the pin).

  3. A CAPTURED VERDICT WHOSE STATUS IS DISCARDED. `out=$(verilator ...)`
     followed by a grep of the TEXT decides the verdict from what the tool
     printed, never from what it returned. Without errexit the assignment's
     status goes nowhere; with `local`/`export` in front it is the builtin's
     status even under errexit. A verilator that crashes silently, or is not
     installed and shadowed by a stub, prints nothing, matches no `%Error`,
     and reads as LINT OK for every top (protocol-processor/scripts/
     lint_hdl.sh, at the pin). Only the assignment forms are modelled: an
     argument-form `echo "k=$(tool)"` is a verdict the CONSUMER decides, and
     the one such site here (elaborate.yml's scope publication) is fail-closed
     by the CI contract, which treats an empty publication as RTL-relevant.

All three are RATCHETS. None can be emptied in one change without exactly the
churn the governing rule forbids, and the pipeline population has legitimate
members: `verilator --version | grep -F "$WANT"` deliberately wants grep's
status, because grep IS the assertion. Those are excluded by name, with the
reason recorded. Debt that lives in a pinned processor submodule is counted
here and fixed upstream; the pin bump lowers the ratchet.

GITHUB'S DEFAULT `run` SHELL IS `bash -e {0}`: errexit, NO pipefail. Only a
step that declares `shell: bash` gets `-eo pipefail`. The first version of
this scan assumed every workflow step had pipefail and let one step's
`set -o pipefail` protect the next; both are modelled per step now, and every
piped step in this tree sets `set -euo pipefail` itself.

Usage:
    python3 scripts/measure_fail_fast.py            # both inventories
    python3 scripts/measure_fail_fast.py --check    # the ratchet
    python3 scripts/measure_fail_fast.py --selftest # fixture arms

Exit 0 = at or under all three ratchets in scripts/fail_fast.budget.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "fail_fast.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE
from code_quality_scope import tracked

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

#: A leftmost grep/cat that reads a FILE and feeds a consumer. The file is the
#: flow's product, so its absence is the failure; grep reading stdin is a
#: consumer (an assertion) and is not matched here. Matched against
#: shell_code(), where quoted patterns are already blanked.
FILE_PIPE = re.compile(r"^\s*(?:grep|egrep|fgrep|cat)\b(?P<args>[^|]*)\|(?!\|)")

#: A captured verdict: `$(tool ...)` for the same producers as PIPE. Matched
#: on the RAW logical line (shell_code() blanks substitutions on purpose).
SUBST = re.compile(
    r"\$\(\s*(?:python3?|make|verilator|yosys|sv2v|vivado|iverilog|behave|pytest"
    r"|\./run\.sh|\./ooc\.sh|scripts/\S+\.(?:py|sh))\b")

#: Pipelines where the CONSUMER is the assertion and its status is the point.
#: Each is matched on the whole line, so a new one has to be added deliberately.
INTENTIONAL = (
    ("--version | grep", "the grep IS the version assertion; its status is the verdict"),
)


def blank_comments(text):
    return COMMENT.sub(lambda m: "".join(c if c == "\n" else " " for c in m.group(0)),
                       text)


def scan_module(text):
    """(declares_parameters, has_elaboration_check) for one SystemVerilog source."""
    code = blank_comments(text)
    return bool(PARAM.search(code)), bool(ELAB_CHECK.search(code))


MODULE = re.compile(r"^\s*module\s+([A-Za-z_]\w*)\b", re.M)
ENDMODULE = re.compile(r"\bendmodule\b")


def scan_modules(text):
    """Return `(name, has_parameters, has_check)` per module, never per file."""
    code = blank_comments(text)
    rows = []
    for match in MODULE.finditer(code):
        end = ENDMODULE.search(code, match.end())
        if end is None:
            continue
        has_params, has_check = scan_module(code[match.start():end.end()])
        rows.append((match.group(1), has_params, has_check))
    return rows


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


def _reads_a_file(args):
    """True when a grep/cat argument list names at least one file operand.

    Options are skipped; for grep the first bare token is the pattern (blank
    when it was quoted), so a file is the second bare token; for cat any bare
    token is a file."""
    bare = [t for t in args.split() if not t.startswith("-")]
    return len(bare) >= 1


def scan_pipeline(line):
    """(is_masked, reason) for one shell/workflow line."""
    for needle, why in INTENTIONAL:
        if needle in line:
            return False, why
    if line.lstrip().startswith("#"):
        return False, ""
    code = shell_code(line)
    if PIPE.match(code):
        return True, ""
    m = FILE_PIPE.match(code)
    if m:
        args = m.group("args")
        bare = [t for t in args.split() if not t.startswith("-")]
        # grep: pattern then file(s) - a quoted pattern was blanked, so a bare
        # file token alone means the pattern was quoted; cat: any bare token
        is_cat = code.lstrip().startswith("cat")
        quoted_pattern = bool(re.match(r"^\s*(?:grep|egrep|fgrep)\b[^|]*?[\"']", line))
        needs = 1 if (is_cat or quoted_pattern) else 2
        return len(bare) >= needs, ""
    return False, ""


_STEP_START = re.compile(r"^\s*-\s+\w+:")
_SHELL_BASH = re.compile(r"^\s*shell:\s*bash\b")


def workflow_steps(text):
    """[(first_line_no, lines, bash_shell)] - one entry per workflow step.

    Text before the first `- key:` is the preamble (one entry, no shell). A
    step declares `shell: bash` before or after its `run:` block, so the whole
    step is read before its lines are scanned."""
    steps, cur, start = [], [], 1
    for n, line in enumerate(text.splitlines(), 1):
        if _STEP_START.match(line) and cur:
            steps.append((start, cur))
            cur, start = [], n
        cur.append(line)
    if cur:
        steps.append((start, cur))
    return [(start, lines, any(_SHELL_BASH.match(l) for l in lines))
            for start, lines in steps]


def _units(text, workflow):
    """[(first_line_no, lines, pipefail0, errexit0)] - the scan units.

    A `.sh` file is one unit that starts with neither option. A workflow is one
    unit per step: GitHub's default shell is `bash -e {0}` (errexit, no
    pipefail), and `shell: bash` is `bash --noprofile --norc -eo pipefail {0}`.
    Options set inside one step never reach the next - each step is a fresh
    shell."""
    if not workflow:
        return [(1, text.splitlines(), False, False)]
    return [(start, lines, bash, True) for start, lines, bash in workflow_steps(text)]


def scan_pipelines(text, workflow=False):
    """Return masked and waived pipeline rows, respecting activation order.

    Ordinary `.sh` files must enable pipefail before the pipeline; a later
    mention cannot retroactively protect an earlier line. A workflow step
    starts without pipefail unless it declares `shell: bash`.
    """
    masked, waived = [], []
    for start, lines, active, _ in _units(text, workflow):
        for n, line in enumerate(lines, start):
            code = shell_code(line)
            if re.search(r"\bset\s+\+o\s+pipefail\b", code):
                active = False
            elif re.search(r"\bset\b[^#\n]*\bpipefail\b", code):
                active = True
            is_masked, why = scan_pipeline(line)
            if why:
                waived.append((n, why))
            elif is_masked and not active:
                masked.append((n, line.strip()[:96]))
    return masked, waived


_ERREXIT_ON = re.compile(r"\bset\s+(?:-[a-df-zA-Z]*e[a-zA-Z]*\b|-o\s+errexit\b|-[a-zA-Z]*\s+-o\s+errexit\b)")
_ERREXIT_OFF = re.compile(r"\bset\s+(?:\+[a-zA-Z]*e[a-zA-Z]*\b|\+o\s+errexit\b)")
_GUARD_PREFIX = re.compile(r"^\s*(?:if|elif|while|until)\b|^\s*!\s|^\s*\[|^\s*test\b")
_BUILTIN_PREFIX = re.compile(r"^\s*(?:local|export|declare|readonly|typeset)\b")
_ASSIGN_PREFIX = re.compile(r"^\s*[A-Za-z_]\w*\+?=")


def logical_lines(lines, start):
    """Join backslash-continued lines; yields (first_line_no, joined)."""
    buf, first = [], None
    for n, line in enumerate(lines, start):
        if first is None:
            first = n
        if line.rstrip().endswith("\\"):
            buf.append(line.rstrip()[:-1])
            continue
        buf.append(line)
        yield first, " ".join(buf)
        buf, first = [], None
    if buf:
        yield first, " ".join(buf)


def scan_substitution(line, errexit):
    """(is_masked, form) for one logical line holding `$(producer ...)`.

    Forms: `local/export x=$(...)` is masked whatever errexit says - the status
    is the builtin's. A bare assignment is masked when errexit is off and no
    `||`/`&&` consults the status. A test (`if`, `!`, `[`) consults it. Any
    other form is the consumer's verdict and is not modelled here."""
    if line.lstrip().startswith("#"):
        return False, "comment"
    m = SUBST.search(line)
    if not m:
        return False, ""
    if _BUILTIN_PREFIX.match(line):
        return True, "builtin"
    if _GUARD_PREFIX.match(line):
        return False, "test"
    if _ASSIGN_PREFIX.match(line):
        tail = line[m.end():]
        consulted = ("||" in tail) or ("&&" in tail)
        return (not errexit) and not consulted, "assignment"
    return False, "argument"


def scan_substitutions(text, workflow=False):
    """Masked captured-verdict rows [(line_no, text)], errexit in line order."""
    masked = []
    for start, lines, _, errexit in _units(text, workflow):
        for n, line in logical_lines(lines, start):
            code = shell_code(line.replace("$(", "  "))   # keep the $( visible below
            if _ERREXIT_OFF.search(code):
                errexit = False
            elif _ERREXIT_ON.search(code):
                errexit = True
            is_masked, _form = scan_substitution(line, errexit)
            if is_masked:
                masked.append((n, line.strip()[:96]))
    return masked


def audit():
    unguarded, guarded = [], []
    for rel in [p for p in tracked("hdl") if p.endswith(".sv") and p not in LINT_EXCLUDE]:
        for name, has_params, has_check in scan_modules(
                (REPO / rel).read_text(errors="replace")):
            if not has_params:
                continue
            unit = f"{rel}:{name}"
            (guarded if has_check else unguarded).append(unit)

    masked, waived, captured = [], [], []
    for rel in tracked("*.sh", ".github/workflows/*.yml", "syn/**/*.sh", "harness/**/*.sh"):
        text = (REPO / rel).read_text(errors="replace")
        workflow = rel.startswith(".github/workflows/") or "/.github/workflows/" in rel
        found, exceptions = scan_pipelines(text, workflow=workflow)
        masked.extend((rel, n, line) for n, line in found)
        waived.extend((rel, n, why) for n, why in exceptions)
        captured.extend((rel, n, line) for n, line in scan_substitutions(text, workflow=workflow))
    return unguarded, guarded, masked, waived, captured


def read_budget():
    if not BUDGET.is_file():
        return None, None
    vals = [int(x) for x in re.findall(r"^\s*(\d+)\s*$", BUDGET.read_text(), re.M)]
    return (vals + [None, None, None])[:3]


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
    rows = scan_modules(
        "module guarded #(parameter int A=1)(); if (!A) $error(\"A\"); endmodule\n"
        "module bare #(parameter int B=1)(); endmodule")
    ck("two modules in one file are measured independently",
       rows == [("guarded", True, True), ("bare", True, False)], f"{rows}")

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
       not scan_pipelines("set -o pipefail\npython3 x.py | tee log")[0])
    ck("a later pipefail cannot protect an earlier pipeline",
       scan_pipelines("python3 x.py | tee log\nset -o pipefail")[0] ==
       [(1, "python3 x.py | tee log")])
    ck("the GitHub Actions default run shell has NO pipefail",
       scan_pipelines("    - name: s\n      run: |\n        python3 x.py | tee log\n",
                      workflow=True)[0] == [(3, "python3 x.py | tee log")],
       "GitHub's default is `bash -e {0}`; only `shell: bash` adds pipefail")
    ck("a step that declares shell: bash is protected, before or after its run block",
       not scan_pipelines("    - name: s\n      run: |\n        python3 x.py | tee log\n"
                          "      shell: bash\n", workflow=True)[0])
    ck("pipefail set in one step does not protect the next step",
       scan_pipelines("    - run: |\n        set -euo pipefail\n        python3 a.py | tee a\n"
                      "    - run: |\n        python3 b.py | tee b\n", workflow=True)[0]
       == [(5, "python3 b.py | tee b")])
    ck("a file-reading grep piped to head is a producer whose status is lost",
       scan_pipelines('set -e\ngrep -A2 "Slice LUTs\\|DSPs" ucpu_util.rpt | head -20\n')[0]
       == [(2, 'grep -A2 "Slice LUTs\\|DSPs" ucpu_util.rpt | head -20')],
       "a missing report makes grep fail and head succeed: the flow exits 0")
    ck("a file-reading cat piped to a consumer is the same shape",
       scan_pipeline("cat engine_util.rpt | tail -3")[0])
    ck("grep reading stdin is a consumer, not a producer",
       not scan_pipeline('echo "$out" | grep -q FAIL')[0])
    ck("a bare grep pattern with no file reads stdin and is not a producer",
       not scan_pipeline("grep foo | head -1")[0])
    ck("the file-reading grep is protected once pipefail is on",
       not scan_pipelines("set -eo pipefail\ngrep x rpt | head\n")[0])
    ck("a captured verdict with no errexit and no guard is discarded",
       scan_substitutions("set -u\nout=$(verilator --lint-only -Wall \\\n  $pkgs $all 2>&1)\n"
                          "if echo \"$out\" | grep -q Error; then rc=1; fi\n")
       == [(2, "out=$(verilator --lint-only -Wall    $pkgs $all 2>&1)")],
       "a silent non-zero verilator prints nothing, matches nothing, reads as OK")
    ck("the same capture under errexit is not discarded",
       not scan_substitutions("set -eu\nout=$(verilator --lint-only x.sv 2>&1)\n"))
    ck("errexit switched off later un-protects a later capture",
       scan_substitutions("set -e\nset +e\nout=$(make lint)\n") == [(3, "out=$(make lint)")])
    ck("a local/export assignment discards the status even under errexit",
       scan_substitutions("set -e\nf() {\n  local out=$(make lint)\n}\n") == [(3, "local out=$(make lint)")]
       and scan_substitutions("set -e\nexport OUT=$(python3 x.py)\n") == [(2, "export OUT=$(python3 x.py)")],
       "the builtin's status is what the shell sees")
    ck("a capture whose status is consulted is not discarded",
       not scan_substitutions("x=$(python3 y.py) || exit 2\n")
       and not scan_substitutions("if ! x=$(python3 y.py); then exit 2; fi\n"))
    ck("an argument-form substitution is the consumer's verdict and is not modelled",
       not scan_substitutions('echo "rtl=$(python3 scripts/ci_scope.py)" >> "$OUT"\n'))
    ck("a workflow step starts with errexit, so a bare capture there is not discarded",
       not scan_substitutions("    - run: |\n        rtl=\"$(python3 scripts/ci_scope.py)\"\n",
                              workflow=True))
    ck("a capture inside a comment is not a finding",
       not scan_substitutions("set -u\n# out=$(verilator x)\n"))
    ck("the version assertion is waived by name, with a reason",
       scan_pipeline('  verilator --version | grep -F "$WANT"') == (False,
       "the grep IS the version assertion; its status is the verdict"))
    ck("an ordinary command is not a pipeline",
       not scan_pipeline("  python3 scripts/x.py")[0])

    unguarded, guarded, masked, waived, captured = audit()
    ck("the live scan reads the tree", len(unguarded) + len(guarded) > 20,
       f"{len(unguarded)} + {len(guarded)} modules with parameters")
    ck("the guarded set is not empty", len(guarded) >= 4,
       "an inert scan would report every module unguarded")
    ck("the waiver actually fires on the live tree", bool(waived),
       "no intentional pipeline was seen - the waiver is untested here")
    ck("the live scan reaches both processor submodules' shell wrappers",
       any(rel.startswith("gptp-processor/") for rel, _, _ in masked + captured) and
       any(rel.startswith("protocol-processor/") for rel, _, _ in masked + captured),
       f"masked {[r for r, _, _ in masked]}, captured {[r for r, _, _ in captured]}")

    n = 36
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet both counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    unguarded, guarded, masked, waived, captured = audit()

    print(f"parameterised modules with no elaboration contract "
          f"({len(unguarded)} of {len(unguarded) + len(guarded)}):")
    for rel in unguarded:
        print(f"   {rel}")
    print(f"\npipelines that discard their producer's exit code ({len(masked)}):")
    for rel, n, line in masked:
        print(f"   {rel}:{n}  {line}")
    print(f"\ncaptured verdicts whose exit status is discarded ({len(captured)}):")
    for rel, n, line in captured:
        print(f"   {rel}:{n}  {line}")
    print(f"\nwaived, with a reason ({len(waived)}):")
    for rel, n, why in waived:
        print(f"   {rel}:{n}  {why}")

    if not args.check:
        return 0

    b_unguarded, b_masked, b_captured = read_budget()
    if b_unguarded is None or b_masked is None or b_captured is None:
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} must hold three counts")
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
    if len(captured) > b_captured:
        print(f"\nFAIL: {len(captured)} captured verdict(s) discarded > ratchet "
              f"{b_captured}. A tool's exit status is the verdict; its text is not.")
        bad = True
    if bad:
        return 1
    print(f"\nFAIL-FAST RATCHET: PASS ({len(unguarded)} <= {b_unguarded} modules "
          f"without an elaboration contract, {len(masked)} <= {b_masked} masked "
          f"pipeline(s), {len(captured)} <= {b_captured} discarded captured "
          f"verdict(s), {len(waived)} waived with a reason)")
    if len(unguarded) < b_unguarded or len(masked) < b_masked or len(captured) < b_captured:
        print(f"  the ratchets can be lowered to {len(unguarded)}, {len(masked)} "
              f"and {len(captured)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
