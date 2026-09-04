#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a first-party shell script fails when the thing it runs fails.

Why this exists. Rule 13 of the maintainability guide
(docs/development/CODE_QUALITY.md) is the shell half of the same argument
Rules 10, 11 and 12 make for SystemVerilog, C++ and Python. Shell is the
smallest population in the tree - 22 first-party scripts, 3 912 lines - and
the one where a defect is least visible, because a shell script that goes
wrong in the middle carries on and exits 0.

That is not a hypothetical here. Thirteen of the 22 scripts run with no
`set -e` at all, and several of them decide PASS or FAIL by grepping a tool's
combined output for an error pattern - which means an ABSENT tool produces no
error pattern, and the script reports PASS. A green CI run is then a
statement about a tool that never ran.

ShellCheck is not installed on every machine this repository is worked on and
is not pinned in any workflow, so the checks below are implemented here rather
than delegated. Each names the ShellCheck code it corresponds to, so a reader
who does have ShellCheck knows which finding is which.

REFUSED - small enough that one commit clears the population.

  1. BACKTICK COMMAND SUBSTITUTION (SC2006). `$( )` nests, quotes predictably
     and is the only form used in this tree today. Population: zero.

  2. A `cd` WITH NO FAILURE PATH (SC2164) in a script that does not `set -e`.
     `cd "$(dirname "$0")/.."` that fails leaves the script running every
     later command in the wrong directory - which for a script whose later
     commands are `rm -rf` is the difference between a failed build and a lost
     tree. Either `set -e`, or `|| exit`.

  3. BRANCHING ON `$?` IN A TEST (SC2181). `cmd; if [ $? -ne 0 ]` is one
     statement away from being wrong forever, because anything inserted
     between the two lines silently replaces the status being tested.
     `if ! cmd; then` cannot break that way.

  4. A SHEBANG WITHOUT THE EXECUTABLE BIT. A script that declares how to run
     itself and cannot be run is a file whose purpose a reader has to guess -
     and a `./script.sh` in a document or a workflow that does not work.

RATCHETED - the count is recorded in `scripts/sh_idiom.budget` and may only go
down.

  5. A SCRIPT WITHOUT `set -euo pipefail`. Six of 22 set the full trio;
     eleven set `set -u` alone, which is unset-variable protection with no
     failure propagation and no pipe status.

  6. AN UNQUOTED EXPANSION IN A WORD-SPLITTING CONTEXT (SC2086/SC2046), unless
     the line carries a `# shellcheck disable=` comment. About half of the 57
     are DELIBERATE word splitting of a source or flag list, which is exactly
     why the comment matters: without it a reader cannot tell the intentional
     ones from the accidental ones.

  7. A SCRIPT OF `LONG_SCRIPT_LINES` LINES OR MORE THAT KEEPS MOST OF ITS BODY
     OUTSIDE ANY FUNCTION. `syn/yosys/ooc.sh` is 688 lines with 86% of them at
     top level, so every variable in it is global and no part of it can be
     read alone.

WHAT IS NOT CHECKED, deliberately.

  * LINE LENGTH. Rule 9 measured a line-length check on this tree, REJECTED it
    with the reasons on the record, and named `syn/yosys/run.sh` and
    `syn/yosys/ooc.sh` specifically: their curated source lists are single
    lines BY DESIGN, because a line continuation is what let a shell comment
    silently shrink one of them. This gate does not reopen that.

  * `[` VERSUS `[[`. Both are correct in bash; the tree uses both; converting
    would be churn with no property gained.

  * SHELL IN A MAKEFILE OR A WORKFLOW `run:` BLOCK. Those are a different
    population with different quoting rules. `scripts/measure_fail_fast.py`
    already reads workflow `run:` blocks for Rule 6's masked-verdict check.

WHAT THE POPULATION IS. Every tracked first-party `*.sh` in this repository
and in the two pinned project-owned processors, through the shared scope
helper, minus `configs/generated/`, which `sw/builder/endstation_builder.py`
writes and which is therefore fixed in the generator.

Usage:

    python3 scripts/check_sh_idiom.py                 # the gate
    python3 scripts/check_sh_idiom.py --list          # per-file counts
    python3 scripts/check_sh_idiom.py --write-budget  # re-record the ratchets
    python3 scripts/check_sh_idiom.py --selftest      # the fixture arms

Exit 0 = no refused construct and every ratchet in `scripts/sh_idiom.budget`
holds; 1 = a finding, or a missing or malformed ratchet entry; 2 = the
population was refused, which no caller may read as a count of zero.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "sh_idiom.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import PROJECT_SUBMODULES, tracked  # noqa: E402

#: Written by sw/builder/endstation_builder.py: fixed in the generator.
EXCLUDED_PREFIXES = ("configs/generated/",)

POPULATION_ROOTS = ("scripts/", "syn/")

#: Above this, a straight-line script stops being readable as one thing.
LONG_SCRIPT_LINES = 100

#: The share of a long script's body that may sit outside any function before
#: it counts. 0.5 is deliberately generous: the finding is "this is one
#: program with global state", not "this is not decomposed enough".
TOP_LEVEL_SHARE = 0.5

CD_RE = re.compile(r"^\s*cd\s+[^\n]*$")
#: `$?` in a test that STARTS a statement. `cmd || [ $? -eq 1 ] || ...` is the
#: only way to tell `grep`'s "no match" (1) from its "error" (2) apart, and
#: nothing can be inserted between the command and that test, so it is not the
#: hazard SC2181 names. The hazard is `cmd` on one line and `if [ $? ]` on the
#: next, where any inserted statement silently replaces the status being read. Anchoring on `if` alone was wrong: an
#: `if ...; then f; exit $?; fi` passes a status ON, which is the correct
#: use, and the first version of this gate called it a finding.
STATUS_TEST_RE = re.compile(
    r"(?:^|;)\s*(?:if|while|until|elif)?\s*\[\[?[^\]]*\$\?[^\]]*\]")
FUNCTION_RE = re.compile(r"^\s*(?:function\s+)?([A-Za-z_][\w:.-]*)\s*\(\s*\)\s*\{")
SHELLCHECK_DISABLE_RE = re.compile(r"#\s*shellcheck\s+disable=")

#: An expansion with no quotes around it, in a context where the shell splits
#: on whitespace. Arithmetic contexts, assignments and `[[ ]]` do not split.
UNQUOTED_RE = re.compile(r"(?<![\"'\w])\$(?:\{[A-Za-z_][^}]*\}|[A-Za-z_]\w*|\()")

RATCHETED = (
    "no strict mode",
    "unquoted expansion",
    "top-heavy long script",
)

REFUSED = (
    "backtick substitution",
    "cd without a failure path",
    "branch on $?",
    "shebang without the executable bit",
)


def sources():
    """Every tracked first-party *.sh, across both project processors."""
    return sorted(p for p in tracked("*.sh")
                  if not p.startswith(EXCLUDED_PREFIXES))


def population_problem(paths):
    """Why this population may not be judged, or None when it is complete."""
    if not paths:
        return "the scan found no tracked shell at all"
    missing = [root for root in POPULATION_ROOTS
               if not any(p.startswith(root) for p in paths)]
    if missing:
        return "no tracked shell under " + ", ".join(missing)
    return None


def executable_bits():
    """{path: True} for every tracked path git records mode 100755."""
    run = subprocess.run(["git", "ls-files", "--stage", "--recurse-submodules"],
                         cwd=REPO, capture_output=True, text=True, check=True)
    out = {}
    for line in run.stdout.splitlines():
        mode, _, rest = line.partition(" ")
        if "\t" in rest:
            out[rest.split("\t", 1)[1]] = mode == "100755"
    return out


def strip_comments(text):
    """Blank comment bodies, keeping the `#` so a directive can still be seen.

    A `#` inside single or double quotes is not a comment, and a `$#` is a
    parameter. Both were wrong in the first version of this scanner.
    """
    out = []
    for line in text.splitlines():
        result = []
        quote = None
        index = 0
        while index < len(line):
            char = line[index]
            if quote:
                result.append(char)
                if char == quote:
                    quote = None
                elif char == "\\" and quote == '"' and index + 1 < len(line):
                    index += 1
                    result.append(line[index])
            elif char in "\"'":
                quote = char
                result.append(char)
            elif char == "#" and (not result or result[-1] not in "$\\"):
                result.append("#")
                result.append(" " * (len(line) - index - 1))
                break
            else:
                result.append(char)
            index += 1
        out.append("".join(result))
    return "\n".join(out)


def shell_flags(text):
    """Every `set` option this script turns on, letters and long names alike.

    `set -euo pipefail` is one statement in which the trailing `o` takes the
    NEXT WORD as its argument. A first version of this scanner read the flag
    letters and stopped, so it saw `e` and `u` and never saw `pipefail`, and
    reported that every script in the tree was missing strict mode - including
    the six that have it. The word after an `-...o` (or a standalone `-o`) is
    therefore consumed as an option name.
    """
    flags = set()
    for match in re.finditer(r"^[ \t]*set[ \t]+([^\n;&|)]*)", text, re.M):
        tokens = match.group(1).split()
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if not token.startswith("-") or token.startswith("--"):
                index += 1
                continue
            letters = token[1:]
            if letters.endswith("o") and index + 1 < len(tokens):
                flags.update(letters[:-1])
                flags.add(tokens[index + 1])
                index += 2
                continue
            flags.update(letters)
            index += 1
    return flags


def has_strict_mode(text):
    """True when the script sets errexit, nounset and pipefail."""
    flags = shell_flags(text)
    return {"e", "u"} <= flags and "pipefail" in flags


def _function_line_span(lines):
    """Number of lines inside a function definition, counted by brace depth."""
    inside = 0
    depth = 0
    for line in lines:
        if depth == 0 and FUNCTION_RE.match(line):
            depth = line.count("{") - line.count("}")
            inside += 1
            continue
        if depth > 0:
            inside += 1
            depth += line.count("{") - line.count("}")
    return inside


def _backticks(text):
    """(line, column) of every backtick that OPENS a command substitution.

    Quoting state is carried ACROSS LINES, which is the whole difficulty. A
    backtick inside SINGLE quotes is literal, and the single-quoted string in
    `protocol-processor/scripts/lint-diagrams.sh` is a five-line embedded awk
    program whose Markdown fence patterns are backticks; a per-line scanner
    loses that state on line two and reports three substitutions that are not
    there. Inside DOUBLE quotes a backtick still substitutes, so that case
    stays a finding, and a backslash disarms one in either place. Only the
    OPENING backtick of a pair is reported, so one substitution is one finding.
    """
    found = []
    quote = None
    in_backtick = False
    line = 1
    column = 0
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\n":
            line += 1
            column = 0
            index += 1
            continue
        if char == "\\" and quote != "'":
            index += 2
            column += 2
            continue
        if quote == "'":
            if char == "'":
                quote = None
        elif quote == '"':
            if char == '"':
                quote = None
            elif char == "`":
                if not in_backtick:
                    found.append((line, column))
                in_backtick = not in_backtick
        elif char in "\"'":
            quote = char
        elif char == "`":
            if not in_backtick:
                found.append((line, column))
            in_backtick = not in_backtick
        index += 1
        column += 1
    return found


def _splitting_context(line):
    """False for a line whose expansions the shell does not word-split."""
    stripped = line.strip()
    if stripped.startswith(("#", "local ", "export ", "declare ", "readonly ")):
        return False
    # An assignment does not word-split its right-hand side, and it is STILL an
    # assignment when a compound command introduces it: `if ! out=$(cmd)` is
    # the SC2181-free way to read a command's status, and a first version of
    # this check saw the leading `if !` and called the substitution a splitting
    # context - so repairing an SC2181 finding manufactured an SC2086 one.
    #
    # That exemption now lives in `_mask_assignments`, which applies it per
    # STATEMENT rather than per line. Testing it here as well would re-exempt
    # the whole of `a=1; rm -rf $target`, where the second statement splits and
    # is a real finding; the per-line test hid every one of those.
    if "[[" in stripped or "((" in stripped:
        return False          # neither construct word-splits
    return True


#: Statement separators, longest first so `;;` is not read as two `;`.
_SEPARATOR_RE = re.compile(r";;|;|\|\||&&|\||&")


def _mask_assignments(line):
    """Blank the right-hand side of every assignment STATEMENT on the line.

    `_splitting_context` already exempts a line that IS an assignment, because
    the shell does not word-split an assignment's right-hand side. It tested
    the whole line, so the exemption was lost the moment an assignment shared a
    line with anything else - and a `case` arm is exactly that shape:

        arty)   NS=4; CFG=${SWEEP_CFG:-configs/endstation_arty_4x4.yaml};;

    That reported one unquoted expansion for `${SWEEP_CFG:-...}`, which the
    shell cannot split, and the obvious repair - quoting it - broke two gates
    that parse this table out of sweep.sh by regex (`scripts/check_sweep_shape.py`
    and `sw/builder/test_builder.py`'s `sweep_inline`). A false positive whose
    repair breaks a real parser is worse than a missed finding, so the
    exemption is now applied per statement. Same length in, same length out, so
    the caller's column arithmetic is unchanged.
    """
    out, index, start, quote = list(line), 0, 0, None
    def blank(begin, end):
        segment = "".join(out[begin:end])
        if re.match(r"^\s*(?:(?:if|while|until|elif|then|do|else)\s+|!\s*)*"
                    r"[A-Za-z_]\w*\+?=", segment):
            for position in range(begin, end):
                if out[position] != "\n":
                    out[position] = " "
    while index < len(line):
        char = line[index]
        if quote:
            if char == quote:
                quote = None
            elif char == "\\" and index + 1 < len(line):
                index += 1
        elif char in "\"'":
            quote = char
        elif char == "\\" and index + 1 < len(line):
            index += 1
        else:
            match = _SEPARATOR_RE.match(line, index)
            if match:
                blank(start, index)
                index = match.end() - 1
                start = match.end()
        index += 1
    blank(start, len(line))
    return "".join(out)


def _unquoted_expansions(line, raw=None, carry=None):
    """Count expansions on this line that sit outside any quoting.

    `raw` is the line before comment blanking, because the
    `# shellcheck disable=` directive that marks a deliberate word split lives
    in the comment the blanking removed.

    `carry` is the quote character still open when the PREVIOUS line ended, or
    None. Returns `(count, quote_open_at_end)`. A quoted string in shell may
    span lines, and this scan is per line, so without the carry every
    continuation line of one looks unquoted:

        echo "--board ax7101 --cpu vexiiriscv \\
              --entity-gen-dir $SOC_DIR/../../configs/generated/..."

    `$SOC_DIR` there is inside double quotes and the shell does not split it,
    but line two on its own has no opening quote. Three such lines in
    sw/litex/build.sh were reported, and "repairing" them by breaking the
    string into several `echo` arguments is what hid --entity-gen-dir,
    --l2-bytes and --uart-baudrate from check_sweep_shape.py and from
    test_builder.py's sweep_inline, both of which read that flag list out of
    the source by regex.
    """
    if carry is None and SHELLCHECK_DISABLE_RE.search(raw if raw is not None else line):
        return 0, None
    if carry is None and not _splitting_context(line):
        # Still walk the line for the quote state the next one inherits.
        return 0, _quote_state_at_end(line, None)
    if carry is None:
        line = _mask_assignments(line)
    found = 0
    quote = carry
    index = 0
    while index < len(line):
        char = line[index]
        if quote:
            if char == quote:
                quote = None
            elif char == "\\" and index + 1 < len(line):
                index += 1
        elif char in "\"'":
            quote = char
        elif char == "\\":
            index += 1
        elif char == "$":
            match = UNQUOTED_RE.match(line, index)
            if match:
                found += 1
                index = match.end() - 1
        index += 1
    # Carry ONLY across an explicit backslash continuation. A line that ends
    # without one starts a new command, and an apostrophe left open by an awk
    # or sed program embedded in it must not leak into every line below: a
    # first version carried unconditionally and turned 7 findings into 74.
    return found, (quote if line.rstrip().endswith("\\") else None)


def _quote_state_at_end(line, carry):
    """The quote character still open after `line`, or None."""
    quote = carry
    index = 0
    while index < len(line):
        char = line[index]
        if quote:
            if char == quote:
                quote = None
            elif char == "\\" and index + 1 < len(line):
                index += 1
        elif char in "\"'":
            quote = char
        elif char == "\\":
            index += 1
        index += 1
    return quote if line.rstrip().endswith("\\") else None


def scan(text, rel="x.sh", is_executable=True):
    """(counts, sites) for one script's source text."""
    counts = dict.fromkeys(tuple(RATCHETED) + tuple(REFUSED), 0)
    sites = {key: [] for key in counts}

    def hit(key, lineno, detail):
        counts[key] += 1
        sites[key].append((lineno, detail))

    code = strip_comments(text)
    lines = code.splitlines()
    raw_lines = text.splitlines()
    flags = shell_flags(code)
    strict = {"e", "u"} <= flags and "pipefail" in flags
    #: The `cd` refusal asks only about ERREXIT, not the whole trio: with
    #: `set -e` a failed `cd` already ends the script, which is what the rule
    #: wants. A first version tested strict mode here and reported four scripts
    #: that set `-e` and are not at risk.
    errexit = "e" in flags

    if not strict:
        hit("no strict mode", 1, "no `set -euo pipefail`")

    if raw_lines and raw_lines[0].startswith("#!") and not is_executable:
        hit("shebang without the executable bit", 1, raw_lines[0][:60])

    for lineno, column in _backticks(code):
        source = lines[lineno - 1] if lineno <= len(lines) else ""
        hit("backtick substitution", lineno, source[column:column + 40].strip())

    open_quote = None      # a quoted string the previous line left open
    for lineno, line in enumerate(lines, 1):
        raw = raw_lines[lineno - 1] if lineno <= len(raw_lines) else line
        if not errexit and CD_RE.match(line):
            if "||" not in line and "&&" not in line:
                hit("cd without a failure path", lineno, line.strip()[:70])
        if STATUS_TEST_RE.search(line):
            hit("branch on $?", lineno, line.strip()[:70])
        count, open_quote = _unquoted_expansions(line, raw, open_quote)
        for _ in range(count):
            hit("unquoted expansion", lineno, line.strip()[:70])

    if len(lines) >= LONG_SCRIPT_LINES:
        inside = _function_line_span(lines)
        share = inside / len(lines)
        if share < TOP_LEVEL_SHARE:
            hit("top-heavy long script", 1,
                f"{len(lines)} lines, {100 * share:.0f}% inside a function")

    return counts, sites


def audit(paths):
    executable = executable_bits()
    totals = dict.fromkeys(tuple(RATCHETED) + tuple(REFUSED), 0)
    per_file = {}
    for rel in paths:
        counts, sites = scan((REPO / rel).read_text(errors="replace"), rel,
                             executable.get(rel, True))
        per_file[rel] = (counts, sites)
        for key, value in counts.items():
            totals[key] += value
    return totals, per_file


def parse_budget(text):
    """{key: int} from budget text; a malformed value simply has no entry."""
    out = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            key, value = line.split("=", 1)
            if value.strip().isdigit():
                out[key.strip()] = int(value.strip())
    return out


def read_budget():
    return parse_budget(BUDGET.read_text()) if BUDGET.is_file() else {}


def ratchet(totals, budget):
    """Missing entry = failure; over = failure; under = pass plus a note."""
    failures, notes = [], []
    for key in RATCHETED:
        limit = budget.get(key)
        if limit is None:
            failures.append(f"NO RATCHET for {key!r} in {BUDGET.relative_to(REPO)} "
                            f"(entry missing or not an integer)")
        elif totals[key] > limit:
            failures.append(
                f"FAIL: {key} {totals[key]} > ratchet {limit}. New shell complies "
                f"immediately; see Rule 13 in docs/development/CODE_QUALITY.md.")
        elif totals[key] < limit:
            notes.append(f"  the {key} ratchet can be lowered to {totals[key]}")
    return failures, notes


def write_budget(totals):
    previous = read_budget()
    raised = [key for key in RATCHETED
              if key in previous and totals[key] > previous[key]]
    if raised:
        print("REFUSED: --write-budget may only lower a ratchet; these rose: "
              + ", ".join(raised), file=sys.stderr)
        return 1
    width = max(len(key) for key in RATCHETED)
    lines = [
        "# Rule 13 ratchets - the shell idiom debt this tree still carries.",
        "# EVERY NUMBER MAY ONLY GO DOWN. Regenerate with",
        "#   python3 scripts/check_sh_idiom.py --write-budget",
        "# which refuses to raise one. What each entry counts is in the gate's",
        "# docstring and in docs/development/CODE_QUALITY.md's Rule 13.",
        "",
    ]
    for key in RATCHETED:
        lines.append(f"{key.ljust(width)} = {totals[key]}")
    BUDGET.write_text("\n".join(lines) + "\n")
    print(f"wrote {BUDGET.relative_to(REPO)}")
    return 0


def selftest():
    checks = failures = 0

    def ck(name, ok, detail=""):
        nonlocal checks, failures
        checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}" + (f": {detail}" if detail else ""))

    def count(src, key, **kwargs):
        return scan(src, **kwargs)[0][key]

    strict = "#!/usr/bin/env bash\nset -euo pipefail\n"

    # --- the refusals bite ---------------------------------------------------
    ck("a backtick substitution is a finding",
       count(strict + "x=`date`\n", "backtick substitution") == 1)
    ck("a $( ) substitution is not a finding",
       count(strict + "x=$(date)\n", "backtick substitution") == 0)
    ck("a backtick in a comment is not a finding",
       count(strict + "# see `date`\n", "backtick substitution") == 0,
       "comment bodies are blanked before matching")
    ck("a backtick inside single quotes is not a finding",
       count(strict + "awk '/^```sv/ { print }' f\n", "backtick substitution") == 0,
       "an embedded awk program is single-quoted, so its backticks are literal")
    ck("an escaped backtick is not a finding",
       count(strict + 'echo "a \\`literal\\` span"\n',
             "backtick substitution") == 0)
    ck("a backtick inside double quotes is still a finding",
       count(strict + 'echo "now is `date`"\n', "backtick substitution") == 1,
       "double quotes do not disarm command substitution")
    ck("a multi-line single-quoted program keeps its backticks literal",
       count(strict + "awk '\n/^```sv/ { a=1 }\n/^```$/ { a=0 }\n' f\n",
             "backtick substitution") == 0,
       "quoting state is carried across lines, or line two reads as code")
    ck("a bare cd without set -e is a finding",
       count("#!/bin/sh\ncd /tmp\n", "cd without a failure path") == 1)
    ck("a cd with || exit is not a finding",
       count("#!/bin/sh\ncd /tmp || exit 1\n", "cd without a failure path") == 0)
    ck("a bare cd under set -e is not a finding",
       count(strict + "cd /tmp\n", "cd without a failure path") == 0,
       "errexit already ends the script on a failed cd")
    ck("a bare cd under set -e alone is not a finding",
       count("#!/bin/sh\nset -e\ncd /tmp\n", "cd without a failure path") == 0,
       "the cd rule asks about errexit, not about the whole strict trio")
    ck("a bare cd under set -u alone is a finding",
       count("#!/bin/sh\nset -u\ncd /tmp\n", "cd without a failure path") == 1)
    ck("branching on $? is a finding",
       count(strict + "make\nif [ $? -ne 0 ]; then exit 1; fi\n",
             "branch on $?") == 1)
    ck("a chained $? test is not a finding",
       count(strict + "out=$(grep x f) || [ $? -eq 1 ] || exit 2\n",
             "branch on $?") == 0,
       "nothing can be inserted between the command and a || test")
    ck("passing $? on with exit is not a finding",
       count(strict + "if [ -n \"$x\" ]; then run; exit $?; fi\n",
             "branch on $?") == 0)
    ck("testing the command directly is not a finding",
       count(strict + "if ! make; then exit 1; fi\n", "branch on $?") == 0)
    ck("a shebang without the executable bit is a finding",
       count(strict, "shebang without the executable bit",
             is_executable=False) == 1)
    ck("a shebang with the executable bit is not a finding",
       count(strict, "shebang without the executable bit",
             is_executable=True) == 0)
    ck("a file with no shebang is not a finding",
       count("set -euo pipefail\n", "shebang without the executable bit",
             is_executable=False) == 0,
       "a sourced fragment is not run directly")

    # --- the ratchets count the right thing ----------------------------------
    ck("a script without strict mode is a finding",
       count("#!/bin/sh\necho hi\n", "no strict mode") == 1)
    ck("set -euo pipefail is strict mode",
       count(strict + "echo hi\n", "no strict mode") == 0)
    ck("set -u alone is not strict mode",
       count("#!/bin/sh\nset -u\n", "no strict mode") == 1,
       "eleven scripts set -u alone: no failure propagation, no pipe status")
    ck("the three flags set separately are strict mode",
       count("#!/bin/sh\nset -e\nset -u\nset -o pipefail\n", "no strict mode") == 0)
    ck("an unquoted expansion is a finding",
       count(strict + "rm -rf $target\n", "unquoted expansion") == 1)
    ck("a quoted expansion is not a finding",
       count(strict + 'rm -rf "$target"\n', "unquoted expansion") == 0)
    ck("an assignment does not word-split",
       count(strict + "x=$y\n", "unquoted expansion") == 0)
    ck("an assignment behind `if !` does not word-split",
       count(strict + "if ! out=$(make 2>&1); then exit 1; fi\n",
             "unquoted expansion") == 0,
       "this is the SC2181-free form; calling it SC2086 punishes the repair")
    # The per-statement exemption, as fixtures. The first arm is the one that
    # cost something: it was reported as a finding, and quoting it - the
    # obvious repair - broke check_sweep_shape.py and test_builder.py, both of
    # which parse this exact table out of sw/litex/sweep.sh by regex.
    ck("an assignment sharing a line with another statement does not word-split",
       count(strict + "arty)   NS=4; CFG=${SWEEP_CFG:-configs/a.yaml};;\n",
             "unquoted expansion") == 0,
       "a case arm is an assignment after a separator, and the shell still does"
       " not split it")
    ck("a real split after an assignment on the same line is still a finding",
       count(strict + "a=1; rm -rf $target\n", "unquoted expansion") == 1,
       "the per-line exemption hid every one of these")
    ck("both halves of a two-statement line are judged separately",
       count(strict + "foo=$bar; baz $qux\n", "unquoted expansion") == 1)
    ck("a separator inside quotes does not split the statement",
       count(strict + 'echo "a; b" $target\n', "unquoted expansion") == 1)
    ck("a command behind `if !` still word-splits its arguments",
       count(strict + "if ! grep -q x $files; then exit 1; fi\n",
             "unquoted expansion") == 1,
       "only the assignment is exempt, not everything after `if !`")
    ck("a [[ ]] test does not word-split",
       count(strict + 'if [[ $x == y ]]; then :; fi\n', "unquoted expansion") == 0)
    ck("a deliberate split carrying a shellcheck directive is not a finding",
       count(strict + "verilator $VFLAGS  # shellcheck disable=SC2086\n",
             "unquoted expansion") == 0,
       "the comment is what separates the intentional splits from the accidents")
    ck("an expansion inside a comment is not a finding",
       count(strict + "# uses $target\n", "unquoted expansion") == 0)
    top_heavy = strict + "echo x\n" * LONG_SCRIPT_LINES
    ck("a long top-level script is a finding",
       count(top_heavy, "top-heavy long script") == 1)
    decomposed = strict + "run() {\n" + "  echo x\n" * LONG_SCRIPT_LINES + "}\nrun\n"
    ck("a long decomposed script is not a finding",
       count(decomposed, "top-heavy long script") == 0)
    ck("a short top-level script is not a finding",
       count(strict + "echo x\n" * 5, "top-heavy long script") == 0)

    # --- budget logic --------------------------------------------------------
    measured = dict.fromkeys(RATCHETED, 0)
    measured["no strict mode"] = 2
    full = dict(measured)
    ck("a count above its budget fails the ratchet",
       ratchet(measured, dict(full, **{"no strict mode": 1}))[0] != [])
    ck("a count equal to its budget passes with no note",
       ratchet(measured, full) == ([], []))
    ck("a count below its budget names the lowerable value",
       "lowered to 2" in ratchet(measured, dict(full, **{"no strict mode": 3}))[1][0])
    ck("a missing budget entry fails the ratchet",
       ratchet(measured, {k: 0 for k in RATCHETED if k != "unquoted expansion"})[0] != [])

    # --- the live tree -------------------------------------------------------
    paths = sources()
    ck("the scan reaches the tracked shell", len(paths) >= 15, f"found {len(paths)}")
    ck("the live population is complete", population_problem(paths) is None,
       str(population_problem(paths)))
    ck("an empty population is refused", population_problem([]) is not None)
    ck("generated shell is out of scope",
       not any(p.startswith("configs/generated/") for p in paths))
    totals, _ = audit(paths)
    ck("the ratcheted populations are non-empty",
       any(totals[key] > 0 for key in RATCHETED),
       "an inert scan would report zero everywhere and ratchet to nothing")
    budget = read_budget()
    ck("the checked-in budget carries every ratcheted key",
       all(key in budget for key in RATCHETED),
       f"missing {[k for k in RATCHETED if k not in budget]}")

    print(f"\n{checks} checks: {checks - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="per-file counts")
    parser.add_argument("--write-budget", action="store_true",
                        help="re-record the ratchets at the measured counts")
    parser.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = parser.parse_args()
    if args.selftest:
        return selftest()

    paths = sources()
    problem = population_problem(paths)
    if problem is not None:
        print(f"POPULATION: REFUSED - {problem}. The gate reads every tracked "
              f"first-party *.sh in this repository and in "
              f"{' and '.join(PROJECT_SUBMODULES)}. Refusing beats counting: a scan "
              f"over a missing tree reports zero of everything, and zero of "
              f"everything is a clean ratchet.", file=sys.stderr)
        return 2

    totals, per_file = audit(paths)

    if args.write_budget:
        return write_budget(totals)

    if args.list:
        width = max(len(p) for p in paths)
        for rel in paths:
            counts = per_file[rel][0]
            if any(counts.values()):
                summary = "  ".join(f"{k}={v}" for k, v in counts.items() if v)
                print(f"{rel.ljust(width)}  {summary}")
        print()

    findings = []
    for key in REFUSED:
        for rel in paths:
            for lineno, detail in per_file[rel][1][key]:
                findings.append(
                    f"REFUSED {key.upper()}: {rel}:{lineno} — {detail}. "
                    f"Rule 13 in docs/development/CODE_QUALITY.md names what "
                    f"replaces it.")

    budget_failures, notes = ratchet(totals, read_budget())

    for line in findings + budget_failures:
        print(line, file=sys.stderr)
    if findings or budget_failures:
        return 1

    print(f"sh idiom: {len(paths)} first-party scripts")
    for key in REFUSED:
        print(f"  {key}: 0")
    budget = read_budget()
    for key in RATCHETED:
        print(f"  {key}: {totals[key]} <= {budget[key]}")
    for note in notes:
        print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
