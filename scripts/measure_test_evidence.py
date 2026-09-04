#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure how much a passing suite actually proves.

Why this exists. Rule 8 of the maintainability guide
(docs/development/CODE_QUALITY.md) says a test's oracle comes from the
specification, its assertions are mutation-proven, and a pass publishes a
non-zero tally. A suite can be green and prove nothing: assertions that have
never been observed to fail are indistinguishable from assertions that cannot.

Four things are counted or refused.

  1. MUTATION COVERAGE. A suite carries an executable arm that deliberately
     breaks something and requires the suite to notice. "Executable" is read
     from the suite's Makefile, not from its prose: the arm must sit in the
     recipe of a target that the suite's ENTRY runs (the sweep's bare `make`,
     the processor's own suite runner or CI), and must be one of three shapes -
     a mutation/negative driver script the recipe invokes, a compile-time
     mutation define the recipe passes, or a negative-case table the recipe
     consumes. A README sentence, a comment naming `mutants.py`, an empty
     `mutants:` target and an unrelated `-DUSE_MUTEX` all count for nothing,
     and so does an arm whose recipe's own error control keeps it from ever
     failing the suite: Make ignores the errors of a line whose prefix carries
     `-` and of a target `.IGNORE` names, and the shell reports the fallback's
     status after `||` (`|| true`, `|| :`, `|| echo`), the next command's
     after `;` and the consumer's after `|`. A plain driver, an `&&` chain, a
     driver run under `set -e` as the last element of its own list, and a
     `||` fallback that ends in `exit`/`false` carry the failure and count.
     The inventory includes the superproject's Verilator suites and the
     processor submodules' own RTL suites. This is a RATCHET: the number
     without an arm may only fall.

  2. REPLAYABLE RANDOMNESS. A test that draws random values without recording
     a seed cannot be replayed from its own failure. The scan knows the idioms
     of each language it reads (Python module and instance draws, `from random
     import`, numpy, `secrets`; C `rand()`, `std::rand`, `random_device`;
     SystemVerilog `$urandom`/`$random`/`randomize`) and the seed shapes that
     make each replayable, and it reads code, not comments or strings. This is
     a RATCHET; the guide records what it measures.

  3. DUT-SOURCE ORACLES. A high-signal inventory finds test programs that read
     production HDL text. The current readers are structural contract or
     mutation tools, each explicitly classified; an unexplained reader is
     refused because copying expected values out of the implementation would
     make a test agree with the same defect.

  4. WALL-CLOCK DEPENDENCE. Suite files that use host time or process/socket
     deadlines are ratcheted. Cycle-bounded protocol timeouts are deterministic
     and do not enter this population. The common runner must classify a suite
     killed by its wall-clock guard as UNKNOWN, never pass or fail, and must run
     the tally self-test before starting the sweep.

Not counted here, because another gate already owns it: a missing or malformed
tally is `NOCOUNT` in `scripts/suite_tally.py`, which refuses to let an unknown
look like agreement. This script imports that reader for its own arms instead
of re-implementing the judgement. The superproject sweep is the population of
that gate; the processor suites run under their own entries (see
SUITE_TREES), and the protocol processor's reader is recorded as upstream debt
in scripts/test_evidence.budget.

KNOWN LIMITS, by name, so nobody rediscovers them:
  - a package import in a testbench wrapper (`import x_pkg::*`) binds the
    DUT's types and constants and is not read as a DUT-source reader; the live
    wrappers carry no compare lines, and telling a structural import from an
    oracle import needs a reading of each wrapper, not a pattern;
  - `secrets.token_*` is a nonce (a container or file name), not a test draw;
    the draw-shaped `secrets.randbelow/randbits/choice` are counted, and can
    never be seeded;
  - a deadline passed positionally (`asyncio.wait_for(coro, 5)`) is not seen;
    the keyword form is;
  - a Makefile conditional is read with every branch live, so an arm inside an
    `ifeq` counts even when that branch would not be taken on the sweep host;
  - a default-constructed C++ engine (`std::mt19937 g;`) is deterministic by
    the standard and is not flagged; `srand(time(NULL))` is not a recorded
    seed and is;
  - recipe error control is read as Make and `sh -c` read it, no further: a
    status captured and re-raised later (`x || rc=1; ...; exit $$rc`), a
    driver used as an `if`/`while` condition, a driver inside `$(...)`,
    backticks or `$(shell ...)`, `set -o pipefail` (Make's shell is /bin/sh)
    and `make -i`/`MAKEFLAGS` at the entry are not followed, so a driver in
    those shapes is not credited; write the arm plain or `&&`-chained.

Usage:
    python3 scripts/measure_test_evidence.py            # the inventories
    python3 scripts/measure_test_evidence.py --check    # the ratchets
    python3 scripts/measure_test_evidence.py --selftest # fixture arms

Exit 0 = at or under the ratchets in scripts/test_evidence.budget; 1 = a
ratchet is exceeded; 2 = the population could not be established (a missing
entry file, no suites found), which no caller may read as a count of zero.
"""

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "test_evidence.budget"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from code_quality_scope import tracked  # noqa: E402
import suite_tally  # noqa: E402

#: Every suite tree, and the files whose `make` invocations are its entry. A
#: target is executed only if one of these runs it: the superproject sweep and
#: the protocol processor's runner run bare `make` in every suite directory,
#: the protocol processor's CI names one extra target by hand, and the gPTP
#: processor's top-level Makefile is its only runner (it has no CI of its own).
SUITE_TREES = (
    ("tb/verilator", "", ("scripts/run_all_suites.sh",)),
    ("protocol-processor/tb", "protocol-processor",
     ("protocol-processor/scripts/run_suites.sh",
      "protocol-processor/.github/workflows/hdl.yml")),
    ("gptp-processor/tb/verilator", "gptp-processor", ("gptp-processor/Makefile",)),
)

#: What `entry_targets()` answers with: the `make` goals each suite directory's
#: entries actually run, "" standing for the default goal. A key is the suite's
#: path, or the pair ("*", tree) for a runner that loops over a whole tree with
#: a shell variable in place of the directory, which reaches every suite in it.
EntryTable = dict[str | tuple[str, str], set[str]]

#: One executable arm found in a reachable recipe: (target, kind, detail),
#: where kind is "driver", "define" or "table".
Arm = tuple[str, str, str]

# --- source hygiene ----------------------------------------------------------

SLASH_FAMILY = {".c", ".cc", ".cpp", ".h", ".hpp", ".sv", ".svh", ".v"}
HASH_FAMILY = {".py", ".sh", ""}  # "" is a Makefile


def strip_source(text: str, suffix: str, strings: bool = False) -> str:
    """Drop comments and, if asked, string contents, so prose cannot arm or seed.

    A `#` preceded by `$`, `{` or `\\` is shell parameter syntax, not a comment.
    In the slash family only double quotes delimit strings; SystemVerilog's
    `1'b0` and C's char literals make the apostrophe useless as a delimiter.
    """
    slash = suffix in SLASH_FAMILY
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if slash and text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if slash and text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if not slash and c == "#" and (i == 0 or text[i - 1] not in "${\\"):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if c == '"' or (c == "'" and not slash):
            q = text[i:i + 3] if not slash and text[i:i + 3] in ('"""', "'''") else c
            j = i + len(q)
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text.startswith(q, j):
                    j += len(q)
                    break
                if len(q) == 1 and text[j] == "\n":
                    break
                j += 1
            out.append(q + q if strings else text[i:j])
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


# --- 1. mutation coverage: what the entry actually executes -----------------

MAKE_VAR = re.compile(r"^(?:override\s+|export\s+)?([.\w]+)\s*(::=|:=|\?=|\+=|=)\s*(.*)$")
MAKE_RULE = re.compile(r"^([^\s=][^=]*?)\s*::?(?!=)\s*(.*)$")
MAKE_REF = re.compile(r"\$\((\w[\w.]*)\)|\$\{(\w[\w.]*)\}")
MAKE_SKIP = re.compile(r"^(?:ifeq|ifneq|ifdef|ifndef|else|endif|include|-include|sinclude|"
                       r"vpath|unexport|\$\(eval)\b")
#: `make ... -C <dir> [targets]` inside an entry file, and the runner form
#: `cd "$d" && make [targets]`. The argument list stops at a shell operator.
MAKE_CALL = re.compile(r"(?:\$\(MAKE\)|(?<![\w/.-])make)\s+([^;&|)>\n]*)")
CD_MAKE_CALL = re.compile(r"cd\s+\"?(\$\{?\w+\}?)\"?/?\s*&&\s*make\b([^;&|)>\n]*)")
SHELL_WORDS = {"if", "then", "else", "elif", "fi", "do", "done", "for", "while",
               "until", "!", "{", "}", "(", ")", "in", "case", "esac", "exec", "time"}
#: A keyword whose command's status the shell consumes instead of reporting.
CONDITION = {"if", "elif", "while", "until", "!"}
#: A recipe line's prefix, read after expansion the way Make reads it (the
#: the build system's `$(Q)` idiom): `@` silences, `+` runs under -n,
#: `-` IGNORES ERRORS.
RECIPE_PREFIX = re.compile(r"^[\s@+-]*")
SHELL_OP = re.compile(r"\s*(;|&&|\|\||\|)\s*")
INTERPRETERS = re.compile(r"^(?:python[\d.]*|sh|bash|dash|env)$")
#: A define that means "mutate", as a whole `_`-delimited word: NVM_MUT_MAP_ALIAS
#: and X_MUTANT are; USE_MUTEX and COMMUTE are not.
MUT_DEFINE = re.compile(r"(?:\+define\+|-D)([A-Za-z_]\w*)")
MUT_NAME = re.compile(r"(?:^|_)MUT(?:ANTS?|ATIONS?|ATED?)?(?:_|$)")
#: A negative/mutation table a recipe consumes, or a driver script carries.
TABLE_VAR = re.compile(r"\$[({](MUTATIONS|MUTANTS|NEG_CASES|NEGATIVE_CASES)[)}]")
DRIVER_TABLE = re.compile(r"(?m)^\s*(?:MUTATIONS|MUTANTS|NEG_CASES|NEGATIVE_CASES)\s*=|"
                          r"\bmutation_checks\s*\(")
REWRITE = re.compile(r"\.replace\s*\(")
WRITES_BACK = re.compile(r"\.write_text\s*\(|\.write\s*\(|\bopen\s*\([^)]*[\"'][wa]")


def parse_makefile(
        text: str) -> tuple[dict[str, str], dict[str, list[list[str]]], str | None]:
    """(variables, rules, first_target). rules: target -> (prereqs, recipe lines)."""
    text = re.sub(r"\\\n[ \t]*", " ", strip_source(text, ""))
    variables, rules, first, current, in_define = {}, {}, None, [], False
    for line in text.splitlines():
        if in_define:
            in_define = not line.strip().startswith("endef")
            continue
        if line.startswith("\t"):
            for target in current:
                rules[target][1].append(line[1:].strip())
            continue
        s = line.strip()
        if not s or MAKE_SKIP.match(s):
            continue
        if s.startswith("define "):
            in_define = True
            continue
        m = MAKE_VAR.match(s)
        if m:
            name, op, value = m.groups()
            if op == "+=":
                variables[name] = (variables.get(name, "") + " " + value).strip()
            elif op != "?=" or name not in variables:
                variables[name] = value
            current = []
            continue
        m = MAKE_RULE.match(s)
        if m:
            targets = m.group(1).split()
            body = m.group(2)
            prereqs, _, inline = body.partition(";")
            current = targets
            for target in targets:
                rules.setdefault(target, [[], []])
                rules[target][0].extend(prereqs.split())
                if inline.strip():
                    rules[target][1].append(inline.strip())
                if first is None and not target.startswith("."):
                    first = target
            continue
        current = []
    return variables, rules, first


def expand(value: str, variables: dict[str, str], depth: int = 0) -> str:
    """Expand `$(NAME)` references; functions and automatic variables stay."""
    if depth > 8:
        return value

    def rep(m: re.Match[str]) -> str:
        """This reference's value, expanded in turn; an unset name stays
        written as it was, so an arm gated on it is not invented here."""
        name = m.group(1) or m.group(2)
        if name in variables:
            return expand(variables[name], variables, depth + 1)
        return m.group(0)
    return MAKE_REF.sub(rep, value)


def make_invocations(text: str) -> list[tuple[str, list[str]]]:
    """[(dir, [targets])] for every `make` an entry file runs; dir None = cwd."""
    calls = []
    for m in CD_MAKE_CALL.finditer(text):
        calls.append((m.group(1), [t for t in m.group(2).split() if not t.startswith("-")]))
    for m in MAKE_CALL.finditer(text):
        args, directory, targets, i = m.group(1).split(), None, [], 0
        while i < len(args):
            a = args[i]
            if a == "-C" and i + 1 < len(args):
                directory = args[i + 1].strip("\"'")
                i += 2
                continue
            if a.startswith("-C"):
                directory = a[2:].strip("\"'")
            elif a in ("-j", "-l", "-f", "-o") and i + 1 < len(args):
                i += 1
            elif not a.startswith("-") and "=" not in a:
                targets.append(a)
            i += 1
        if directory is not None:
            calls.append((directory, targets))
    return calls


def entry_targets() -> EntryTable:
    """suite -> set of targets its entries run ("" = the default goal)."""
    out = {}
    for tree, root, entries in SUITE_TREES:
        for entry in entries:
            path = REPO / entry
            if not path.is_file():
                print(f"REFUSED: suite entry {entry} is missing, so which targets "
                      f"the {tree} suites execute cannot be established", file=sys.stderr)
                sys.exit(2)
            for directory, targets in make_invocations(path.read_text(errors="replace")):
                goals = set(targets) or {""}
                if "$" in directory:
                    key = ("*", tree)
                else:
                    key = "/".join(p for p in (root, directory.strip("/")) if p)
                out.setdefault(key, set()).update(goals)
    return out


def suite_entries(suite: str, table: EntryTable) -> set[str]:
    """Every goal that reaches this suite: the ones named for it by path, plus
    the ones a whole-tree runner reaches it with."""
    goals = set(table.get(suite, ()))
    for tree, _root, _entries in SUITE_TREES:
        if suite.startswith(tree + "/"):
            goals |= table.get(("*", tree), set())
    return goals


def reachable_targets(variables: dict[str, str], rules: dict[str, list[list[str]]],
                      first: str | None, goals: set[str]) -> set[str]:
    """Every target the entry's goals actually run, through prerequisites and
    through recursive `make` calls in the recipes. An arm in a target nothing
    reaches is prose: it is why this walk exists rather than a scan of rules."""
    stack = [variables.get(".DEFAULT_GOAL", first) if g == "" else g for g in goals]
    seen = set()
    while stack:
        target = stack.pop()
        if target is None or target in seen or target not in rules:
            continue
        seen.add(target)
        prereqs, recipe = rules[target]
        stack.extend(expand(" ".join(prereqs), variables).split())
        for line in recipe:
            for m in MAKE_CALL.finditer(expand(line, variables)):
                stack.extend(t for t in m.group(1).split()
                             if not t.startswith("-") and "=" not in t)
    return seen


def shell_words(segment: str) -> tuple[list[str], list[str]]:
    """(leading keywords, command words) of one shell segment. Keywords,
    assignments and a group opener come off the front and a closer off the
    end, so `{ exit 1` and `(exit 1)` both read as `exit 1`."""
    words = segment.split()
    if words and len(words[0]) > 1 and words[0][0] in "{(":
        words[0:1] = [words[0][0], words[0][1:]]
    if words and len(words[-1]) > 1 and words[-1][-1] in "})" \
            and {"}": "{", ")": "("}[words[-1][-1]] not in words[-1]:
        words[-1:] = [words[-1][:-1], words[-1][-1]]
    lead = []
    while words and (words[0] in SHELL_WORDS or re.match(r"^\w+=", words[0])):
        lead.append(words.pop(0))
    while words and words[-1] in ("}", ")"):
        words.pop()
    return lead, words


def set_errexit(words: list[str], errexit: bool) -> bool:
    """errexit after this command: `set -e`/`set +e`, `set -o/+o errexit`."""
    if not words or words[0] != "set":
        return errexit
    for i, flag in enumerate(words[1:], 1):
        if flag in ("-o", "+o"):
            if i + 1 < len(words) and words[i + 1] == "errexit":
                errexit = flag == "-o"
        elif flag[:1] in "-+" and "e" in flag[1:]:
            errexit = flag[0] == "-"
    return errexit


def reraises(segments: list[str], k: int) -> bool:
    """Does the `||` fallback beginning at segment k end in `exit`/`false`,
    so the failure it caught still reaches Make? `|| true`, `|| :` and
    `|| echo ...` do not; `|| exit 1` and `|| { echo ...; exit 1; }` do."""
    if k >= len(segments):
        return False
    closer = {"{": "}", "(": ")"}.get(segments[k].lstrip()[:1])
    last = None
    for m in range(k, len(segments)):
        last = shell_words(segments[m])[1] or last
        if closer is None or segments[m].rstrip().endswith(closer):
            break
    if not last:
        return False
    return last[0] == "false" or (last[0] == "exit" and (len(last) < 2 or last[1] != "0"))


def reaches_make(segments: list[str], ops: list[str | None], leads: list[list[str]],
                 cmds: list[list[str]], i: int, errexit: bool) -> bool:
    """Does a non-zero exit of segment i become the recipe line's status?

    Make runs the line as one `sh -c` and reads that shell's exit status: an
    `&&` chain carries the first failure, `A || B` reports B's status, `A | B`
    reports B's, `A; B` reports B's unless errexit is on and A is the last
    element of its own and-or list, and a condition's status is consumed."""
    if CONDITION & set(leads[i]):
        return False
    j = i
    while ops[j] == "&&" or (ops[j] == "|" and j > i):
        j += 1
    if ops[j] is None:
        return True
    if ops[j] == "|":
        return False
    if ops[j] == "||":
        return reraises(segments, j + 1)
    if any(cmds[k] for k in range(j + 1, len(cmds))):
        return errexit and j == i
    return True


def commands(line: str, errexit: bool = False) -> list[tuple[str, str | None, bool]]:
    """The (command, argument, counts) triples a recipe line runs, per shell
    segment. `counts` is False where the recipe's own error control (the `-`
    prefix, `||`, `|`, `;`, a condition) keeps the command's failure from
    Make, so a failed campaign there would leave the suite green."""
    prefix = RECIPE_PREFIX.match(line).group(0)
    parts = SHELL_OP.split(line[len(prefix):])
    segments, ops = parts[0::2], parts[1::2] + [None]
    peeled = [shell_words(segment) for segment in segments]
    leads, cmds = [lead for lead, _ in peeled], [words for _, words in peeled]
    triples = []
    for i, words in enumerate(cmds):
        if not words:
            continue
        rest = [w for w in words[1:] if not w.startswith("-")]
        counts = "-" not in prefix and reaches_make(segments, ops, leads, cmds, i, errexit)
        triples.append((words[0], rest[0] if rest else None, counts))
        errexit = set_errexit(words, errexit)
    return triples


def is_driver(text: str, suffix: str) -> bool:
    """A script that carries a mutation/negative table, or rewrites the DUT
    text it reads and runs the harness on the result."""
    code = strip_source(text, suffix, strings=True)
    if DRIVER_TABLE.search(code):
        return True
    return bool(reads_dut_source(text, suffix) and REWRITE.search(code)
                and WRITES_BACK.search(strip_source(text, suffix)))


def arms(makefile: str, goals: set[str], scripts: dict[str, str]) -> list[Arm]:
    """Every executable arm: (target, kind, detail). `scripts` maps a script's
    basename to its text; only .py/.sh files are consulted, never prose. A
    recipe whose error control keeps the arm from failing the suite is not
    one: a `-` prefix or `.IGNORE` for a whole line or target, and per
    command whatever `commands()` marks as not counting."""
    variables, rules, first = parse_makefile(makefile)
    errexit = ".POSIX" in rules or any(
        flag.startswith("-") and "e" in flag[1:]
        for flag in expand(variables.get(".SHELLFLAGS", ""), variables).split())
    ignore = rules.get(".IGNORE")
    ignored = None if ignore is None else set(expand(" ".join(ignore[0]), variables).split())
    found = []
    for target in sorted(reachable_targets(variables, rules, first, goals)):
        if ignored is not None and (not ignored or target in ignored):
            continue
        for raw in rules[target][1]:
            line = expand(raw, variables)
            if "-" in RECIPE_PREFIX.match(line).group(0):
                continue
            for m in MUT_DEFINE.finditer(line):
                if MUT_NAME.search(m.group(1)):
                    found.append((target, "define", m.group(0)))
            for m in TABLE_VAR.finditer(raw):
                if expand(m.group(0), variables).strip() not in ("", m.group(0)):
                    found.append((target, "table", m.group(0)))
            for cmd, arg, counts in commands(line, errexit):
                if not counts:
                    continue
                candidate = arg if INTERPRETERS.match(cmd) and arg else cmd
                name = candidate.rsplit("/", 1)[-1].strip("\"'")
                suffix = Path(name).suffix
                if suffix in (".py", ".sh") and name in scripts \
                        and is_driver(scripts[name], suffix):
                    found.append((target, "driver", name))
    return found


def suites() -> list[str]:
    """The suite inventory: one directory per tracked testbench Makefile."""
    makefiles = tracked("tb/verilator/*/Makefile", "tb/*/Makefile")
    return sorted({str(Path(rel).parent) for rel in makefiles
                   if "/tb/" in rel or rel.startswith("tb/")})


def suite_files() -> dict[str, list[str]]:
    """suite -> every tracked file under it, from one listing of the trees."""
    files = tracked("tb/*")
    return {name: [rel for rel in files if rel.startswith(name + "/")] for name in suites()}


def suite_arms(name: str, files: list[str], table: EntryTable) -> list[Arm]:
    """One suite's executable arms, read from its Makefile with only the
    scripts it actually owns offered as candidate drivers."""
    scripts = {Path(rel).name: (REPO / rel).read_text(errors="replace")
               for rel in files if Path(rel).suffix in (".py", ".sh")}
    makefile = (REPO / name / "Makefile").read_text(errors="replace")
    return arms(makefile, suite_entries(name, table), scripts)


# --- 2. replayable randomness ---------------------------------------------

PY_DRAWS = ("random|randint|randrange|choice|choices|shuffle|sample|uniform|gauss|"
            "normalvariate|lognormvariate|expovariate|betavariate|gammavariate|"
            "triangular|vonmisesvariate|paretovariate|weibullvariate|getrandbits|randbytes")
PY_MODULE_DRAW = re.compile(rf"(?<![\w.])random\.(?:{PY_DRAWS})\s*\(")
PY_MODULE_SEED = re.compile(r"(?<![\w.])random\.seed\s*\(\s*[^\s)]")
PY_INSTANCE = re.compile(r"([\w.]+)\s*=\s*random\.(Random|SystemRandom)\s*\(\s*([^)]*)\)")
PY_FROM_IMPORT = re.compile(r"^\s*from\s+random\s+import\s+\(?([^)\n]+)", re.M)
PY_BARE_SEED = re.compile(r"(?<![\w.])seed\s*\(\s*[^\s)]")
NP_DRAW = re.compile(r"\b(?:np|numpy)\.random\.(?!seed\b|default_rng\b|RandomState\b)\w+\s*\("
                     r"|\b(?:np|numpy)\.random\.(?:default_rng|RandomState)\s*\(\s*\)")
NP_SEED = re.compile(r"\b(?:np|numpy)\.random\.(?:seed|default_rng|RandomState)\s*\(\s*[^\s)]")
SECRETS_DRAW = re.compile(r"\bsecrets\.(?:randbelow|randbits|choice)\s*\(")
C_DRAW = re.compile(r"(?<![\w:.>])(?:std::)?rand\s*\(\s*\)|(?<![\w:.>])(?:std::)?random\s*\(\s*\)"
                    r"|\b[ld]?rand48\s*\(|\brandom_device\b")
C_SEED = re.compile(r"\bsrand(?:om|48)?\s*\(\s*(?!(?:std::)?time\s*\(|(?:std::)?random_device)[^\s)]")
SEED_RECORDED = re.compile(r"\"[^\"\n]*\bseed\b[^\"\n]*\"", re.I)
SV_DRAW = re.compile(r"\$urandom(?:_range)?\b|\$random\b|\.randomize\s*\(")
SV_SEED = re.compile(r"\bsrandom\s*\(|\$urandom\s*\(\s*[^\s)]|\$random\s*\(\s*[^\s)]"
                     r"|\$value\$plusargs\s*\(\s*\"[^\"]*(?i:seed)")


def unseeded_draws(text: str, suffix: str) -> list[str]:
    """The random-draw shapes in `text` that no recorded seed makes replayable."""
    code = strip_source(text, suffix, strings=True)
    seedable = strip_source(text, suffix)
    found = []
    if suffix == ".py":
        if PY_MODULE_DRAW.search(code) and not PY_MODULE_SEED.search(code):
            found.append("random.<draw>() without random.seed(...)")
        for name, cls, arg in PY_INSTANCE.findall(code):
            if re.search(rf"(?<![\w.]){re.escape(name)}\.(?:{PY_DRAWS})\s*\(", code):
                if cls == "SystemRandom":
                    found.append(f"{name} = random.SystemRandom() cannot be seeded")
                elif not arg.strip():
                    found.append(f"{name} = random.Random() carries no seed")
        for m in PY_FROM_IMPORT.finditer(code):
            names = [n.strip().split(" as ")[-1].strip() for n in m.group(1).split(",")]
            for n in names:
                if n in PY_DRAWS.split("|") and re.search(rf"(?<![\w.]){n}\s*\(", code) \
                        and not (PY_MODULE_SEED.search(code) or PY_BARE_SEED.search(code)):
                    found.append(f"from random import {n} without seed(...)")
        if NP_DRAW.search(code) and not NP_SEED.search(code):
            found.append("numpy draw without np.random.seed/default_rng(seed)")
        if SECRETS_DRAW.search(code):
            found.append("secrets draw (never seedable)")
    elif suffix in SLASH_FAMILY and suffix not in (".sv", ".svh", ".v"):
        if C_DRAW.search(code) and not C_SEED.search(code):
            if not ("random_device" in code and SEED_RECORDED.search(seedable)):
                found.append("C draw without a recorded srand/seed")
    elif suffix in (".sv", ".svh", ".v"):
        if SV_DRAW.search(code) and not SV_SEED.search(seedable):
            found.append("$urandom/$random/randomize without srandom or a seed")
    return found


def draws_without_seed(text: str, suffix: str = ".py") -> bool:
    """Whether this text draws at all without a seed - the yes/no the arms use."""
    return bool(unseeded_draws(text, suffix))


def seed_population() -> list[str]:
    """The files judged for replayable randomness: test sources in every
    language the scan reads, plus the host scripts that generate stimulus."""
    return sorted(tracked("tb/*.py", "tb/*.cpp", "tb/*.cc", "tb/*.c", "tb/*.h",
                          "tb/*.sv", "tb/*.svh", "tb/*.v", "tb/*.sh",
                          "sw/*.py", "scripts/*.py", "tests/*.py"))


# --- 3. DUT-source oracles --------------------------------------------------

# Reading the DUT is not automatically wrong: mutation arms must rewrite the
# DUT and structural contract checks must inspect it. It is, however, the
# smallest useful static population for an implementation-derived-oracle
# review. Every present reader has a narrow recorded reason; a new one is debt
# until it is classified.
DUT_READ_PY = re.compile(r"\bread_text\s*\(|\bread_bytes\s*\(|\bopen\s*\(|\.read\s*\(|\.readlines\s*\(")
DUT_READ_C = re.compile(r"\bifstream\b|\bfopen\s*\(|\bstd::filesystem\b")
DUT_READ_SV = re.compile(r"`include\s+\"[^\"\n]*hdl/|\$fopen\s*\(|\$readmem[hb]\s*\(")
DUT_READ_SH = re.compile(r"(?m)^[^\n]*\b(?:cat|grep|sed|awk|head|tail|diff)\b[^\n]*"
                         r"(?:hdl/|\$[({](?:RTL|HDL)\w*[)}])")
DUT_PATH = re.compile(r"\b(?:RTL|FILTER)\s*=|[\"'][^\"'\n]*hdl/")
DUT_READER_DISPOSITIONS = {
    "gptp-processor/tb/check_phc_contract.py":
        "structural boundary check; it asserts required/forbidden tokens, not behavior",
    "gptp-processor/tb/tsngen/mutants.py":
        "mutation campaign; it stages three engine defects and requires failure",
    "protocol-processor/tb/nvm_port/measure_figures.py":
        "mutation campaign; it rewrites one RTL arm and requires the suite to fail",
    "tb/verilator/rx_filter/binding_mutant.py":
        "mutation campaign; it ties a real named binding low and requires failure",
    "tb/verilator/tcam/mutants.py":
        "mutation campaign; it injects three RTL defects and requires failure",
}


def reads_dut_source(text: str, suffix: str = ".py") -> bool:
    """Does this test program read production HDL text? A reader is not wrong
    by itself - a mutation arm has to rewrite the DUT - but it is where an
    implementation-derived oracle would hide, so each one is classified."""
    code = strip_source(text, suffix)
    if suffix in (".sh", ""):
        return bool(DUT_READ_SH.search(code))
    if suffix in (".sv", ".svh", ".v"):
        return bool(DUT_READ_SV.search(code) and DUT_PATH.search(code))
    reader = DUT_READ_C if suffix in SLASH_FAMILY else DUT_READ_PY
    return bool(reader.search(code) and DUT_PATH.search(code))


# --- 4. wall-clock dependence ----------------------------------------------

# Host time can vary with machine load. This deliberately ignores identifiers
# such as `timeout_cycles` and `int timeout = 100`: protocol time advanced by
# explicit DUT ticks is a deterministic oracle. It catches actual host clocks,
# sleeps, socket deadlines and subprocess deadlines, in each language's idiom.
PY_CLOCK = re.compile(r"\btime\.(?:time|monotonic|perf_counter|sleep|time_ns|monotonic_ns|"
                      r"perf_counter_ns)\s*\(|\bdatetime\.(?:now|utcnow|today)\s*\("
                      r"|\.settimeout\s*\(|\bselect\.select\s*\(|\bsignal\.alarm\s*\("
                      r"|\bSO_(?:RCV|SND)TIMEO\b")
PY_DEADLINE_CALL = re.compile(r"(?:\b(?:subprocess\.)?(?:run|call|check_call|check_output|Popen)"
                              r"|\.communicate|\.wait|\bwait_for|\.join|\.get|\.acquire"
                              r"|\.connect|\.recv)\s*\(")
C_CLOCK = re.compile(r"\bstd::chrono\b|\bchrono::|\bsteady_clock\b|\bsystem_clock\b"
                     r"|\bhigh_resolution_clock\b|(?<![\w:.>])clock\s*\(\s*\)"
                     r"|(?<![\w:.>])time\s*\(\s*(?:NULL|0|nullptr)?\s*\)|\bgettimeofday\s*\("
                     r"|\bclock_gettime\s*\(|(?<![\w:.>])(?:u|nano)?sleep\s*\(|\balarm\s*\("
                     r"|\bSO_(?:RCV|SND)TIMEO\b")
SH_CLOCK = re.compile(r"^\s*[-@+]*\s*timeout\s+\S|(?<![\w.$])sleep\s+[0-9.]|\$\(shell\s+date\b"
                      r"|^\s*[-@+]*\s*date\b|(?<![\w.$])date\s+\+", re.M)


def call_with_keyword(code: str, call: re.Pattern[str], keyword: str) -> bool:
    """Does any `call(` carry `keyword=` inside its own (balanced) parentheses?"""
    for m in call.finditer(code):
        depth, i = 1, m.end()
        while i < len(code) and depth:
            depth += {"(": 1, ")": -1}.get(code[i], 0)
            i += 1
        if re.search(rf"\b{keyword}\s*=", code[m.end():i]):
            return True
    return False


def uses_wall_clock(text: str, suffix: str = ".py") -> bool:
    """Does this suite file depend on host time rather than DUT cycles? A
    cycle-bounded protocol timeout is deterministic and stays out of the count;
    a clock read, a sleep, or a process/socket deadline does not."""
    code = strip_source(text, suffix)
    if suffix == ".py":
        return bool(PY_CLOCK.search(code) or call_with_keyword(code, PY_DEADLINE_CALL, "timeout"))
    if suffix in (".sh", ""):
        return bool(SH_CLOCK.search(code))
    if suffix in SLASH_FAMILY and suffix not in (".sv", ".svh", ".v"):
        return bool(C_CLOCK.search(code))
    return False


def runner_contract(text: str) -> list[str]:
    """Problems in the common sweep's timeout and tally evidence contract."""
    problems = []
    launch = text.find('timeout "$TMO" make')
    tally_selftest = text.find('suite_tally.py" --selftest')
    tally_run = text.find('suite_tally.py" "$OUT" --quiet')
    if launch < 0:
        problems.append("the per-suite wall-clock guard is missing")
    if tally_selftest < 0 or (launch >= 0 and tally_selftest > launch):
        problems.append("the tally self-test does not run before the first suite")
    if tally_run < 0 or (launch >= 0 and tally_run < launch):
        problems.append("the final log tally does not run after the suites")
    if "124|137)" not in text or "tmo=$((tmo + 1))" not in text:
        problems.append("timeout/OOM exits are not classified separately")
    if '[ "$tmo"  -gt 0 ] && exit 92' not in text:
        problems.append("an unknown timeout result does not return exit 92")
    if '[ "$tally_rc" -ne 0 ] && exit 90' not in text:
        problems.append("a malformed or missing tally does not return exit 90")
    return problems


# --- the audit ---------------------------------------------------------------

def test_sources() -> list[str]:
    """Every executable file under a tb/ tree, whether or not a suite owns it -
    the population the DUT-source-oracle inventory is drawn from."""
    suffixes = {".py", ".cpp", ".cc", ".c", ".h", ".sv", ".svh", ".v", ".sh"}
    return sorted(rel for rel in tracked("tb/*")
                  if Path(rel).suffix in suffixes or Path(rel).name == "Makefile")


def suite_sources(by_suite: dict[str, list[str]]) -> list[str]:
    """Executable files owned by a directory that the suite inventory names."""
    suffixes = {".py", ".cpp", ".cc", ".c", ".h", ".sv", ".svh", ".v", ".sh"}
    paths = {rel for files in by_suite.values() for rel in files}
    return sorted(rel for rel in paths
                  if Path(rel).suffix in suffixes or Path(rel).name == "Makefile")


def file_suffix(rel: str) -> str:
    """Which language's idioms to read this file with; "" selects the Makefile
    reader, so an extension-less recipe is not read as a shell script."""
    return "" if Path(rel).name == "Makefile" else Path(rel).suffix


def audit() -> tuple[dict[str, list[Arm]], list[str], dict[str, list[str]],
                     list[str], list[str], list[str], list[str]]:
    """All four inventories in one pass over the trees:
    (armed, unarmed, unseeded, readers, unexplained, stale, wallclock).
    `stale` names a recorded disposition whose reader has gone, which is how a
    classification stops standing for a file nobody reads any more."""
    table = entry_targets()
    by_suite = suite_files()
    armed, unarmed = {}, []
    for name, files in by_suite.items():
        found = suite_arms(name, files, table)
        if found:
            armed[name] = found
        else:
            unarmed.append(name)

    unseeded = {}
    for rel in seed_population():
        shapes = unseeded_draws((REPO / rel).read_text(errors="replace"), file_suffix(rel))
        if shapes:
            unseeded[rel] = shapes

    readers = [rel for rel in test_sources()
               if reads_dut_source((REPO / rel).read_text(errors="replace"), file_suffix(rel))]
    wallclock = [rel for rel in suite_sources(by_suite)
                 if uses_wall_clock((REPO / rel).read_text(errors="replace"), file_suffix(rel))]
    unexplained = sorted(set(readers) - set(DUT_READER_DISPOSITIONS))
    stale = sorted(set(DUT_READER_DISPOSITIONS) - set(readers))
    return armed, unarmed, unseeded, readers, unexplained, stale, wallclock


def read_budget() -> Sequence[int | None]:
    """The four ratchets, in the order the budget file writes them. A missing
    file, or a file short of four numbers, yields None in those places, and
    main() refuses to grade rather than treating an absence as a zero."""
    if not BUDGET.is_file():
        return None, None, None, None
    vals = [int(x) for x in re.findall(r"^\s*(\d+)\s*$", BUDGET.read_text(), re.M)]
    return (vals + [None, None, None, None])[:4]


# --- self-test ---------------------------------------------------------------

def selftest() -> int:
    """Run the fixture arms and return their exit code."""
    # The arms live in ``measure_test_evidence_selftest``: one long list of
    # independent fixtures with no reader in common with the rules above, and
    # importing them only when --selftest is asked for keeps this module's own
    # import free of them.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from measure_test_evidence_selftest import run_arms
    return run_arms()


def main() -> int:
    """Print the four inventories, grade them against the budget under
    --check, and return the process exit code. An empty suite population is
    exit 2, never a pass: zero suites without an arm is not the same claim."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet the four counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    armed, unarmed, unseeded, readers, unexplained, stale, wallclock = audit()
    population = len(armed) + len(unarmed)
    if population == 0:
        print("REFUSED: no RTL suite found under the suite trees; an empty population "
              "is not a pass", file=sys.stderr)
        return 2
    print(f"RTL suites with an executable mutation or negative arm: {len(armed)} of {population}")
    for tree, _root, entries in SUITE_TREES:
        n = sum(1 for s in list(armed) + unarmed if s.startswith(tree + "/"))
        print(f"   {n:3d} under {tree}  (entry: {', '.join(entries)})")
    print(f"\narmed suites, and the executed target that arms them ({len(armed)}):")
    for name, found in sorted(armed.items()):
        target, kind, detail = found[0]
        print(f"   {name}: `{target}` {kind} {detail}")
    print(f"\nsuites with none ({len(unarmed)}):")
    for name in unarmed:
        print(f"   {name}")
    print(f"\nfiles that draw random values without recording a seed ({len(unseeded)}):")
    for rel, shapes in sorted(unseeded.items()):
        print(f"   {rel}: {shapes[0]}")
    print(f"\ntest programs that read production HDL ({len(readers)}):")
    for rel in readers:
        print(f"   {rel}: {DUT_READER_DISPOSITIONS.get(rel, 'UNEXPLAINED')}")
    print(f"\nsuite files using host wall-clock/process deadlines ({len(wallclock)}):")
    for rel in wallclock:
        print(f"   {rel}")

    runner_problems = runner_contract((REPO / "scripts/run_all_suites.sh").read_text())
    print("\nrunner evidence contract: " + ("OK" if not runner_problems else "FAIL"))
    for problem in runner_problems:
        print(f"   {problem}")

    if not args.check:
        return 0

    b_unarmed, b_unseeded, b_unexplained, b_wallclock = read_budget()
    if any(value is None for value in
           (b_unarmed, b_unseeded, b_unexplained, b_wallclock)):
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} must hold four counts")
        return 1
    bad = False
    if len(unarmed) > b_unarmed:
        print(f"\nFAIL: {len(unarmed)} suite(s) with no mutation arm > ratchet "
              f"{b_unarmed}. A new suite proves its own assertions can fail.")
        bad = True
    if len(unseeded) > b_unseeded:
        print(f"\nFAIL: {len(unseeded)} unseeded random draw site(s) > ratchet "
              f"{b_unseeded}. A random test records the seed it can be replayed from.")
        bad = True
    if len(unexplained) > b_unexplained or stale:
        print(f"\nFAIL: {len(unexplained)} unexplained DUT-source reader(s) > "
              f"ratchet {b_unexplained}; stale dispositions: {stale}")
        bad = True
    if len(wallclock) > b_wallclock:
        print(f"\nFAIL: {len(wallclock)} wall-clock-dependent suite file(s) > "
              f"ratchet {b_wallclock}. New behavioral tests use DUT cycles, not host time.")
        bad = True
    if runner_problems:
        bad = True
    if bad:
        return 1
    print(f"\nTEST-EVIDENCE RATCHET: PASS ({len(unarmed)} <= {b_unarmed} suite(s) "
          f"without a mutation arm, {len(unseeded)} <= {b_unseeded} unseeded "
          f"draw site(s), {len(unexplained)} <= {b_unexplained} unexplained "
          f"DUT-source reader(s), {len(wallclock)} <= {b_wallclock} "
          "wall-clock-dependent suite file(s))")
    for label, have, budget in (("mutation", len(unarmed), b_unarmed),
                                ("unseeded-draw", len(unseeded), b_unseeded),
                                ("wall-clock", len(wallclock), b_wallclock)):
        if have < budget:
            print(f"  the {label} ratchet can be lowered to {have}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
