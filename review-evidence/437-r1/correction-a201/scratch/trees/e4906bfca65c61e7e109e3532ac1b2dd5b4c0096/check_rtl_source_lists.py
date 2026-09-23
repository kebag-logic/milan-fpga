#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: every list that compiles `milan_datapath` carries every module it needs.

Why this exists, with the receipts. There are FOUR independent lists of the
same RTL - the Vivado sources in `sw/litex/milan_soc.py`, the `milan_datapath`
row in `syn/yosys/run.sh`, `DP_SRCS` in `syn/yosys/ooc.sh`, and the source
list in `tb/verilator/milan_dp/Makefile`.
`scripts/check_soc_sources.py` has guarded exactly one of them since a missing
`KL_i2s_feed_mux` entry killed three Vivado runs forty minutes in. The other
three were unguarded, and extracting one module into
`hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv` broke three Verilator suites at
once, each with the same "Cannot find file containing module" - one per list
that nobody had told.

THE AUTHORITY IS THE RTL, NOT ANOTHER LIST. This gate walks the module closure
of `milan_datapath` through the sources themselves: what the datapath
instantiates, what those modules instantiate, transitively, plus every package
and interface they reference and every unit file they `include`. Checking one
list against another would let all five agree and all five be wrong, which is
the same defect wearing a different hat. `scripts/check_soc_sources.py` owns
the first hop - the instantiation shapes, the comment blanking, the include
splicing - and this gate imports it rather than writing a second copy: a gate
about single sources of truth that forked its own instantiation parser would
be self-refuting. The hop has to see every shape a front end accepts, because
a shape it does not see is a file no consumer is told about: the first
version needed two leading spaces and walked past the one column-0
instantiation the tree already had (`traffic_class_map` in
`traffic_classifier.sv`), reported 108 files and "4 of 4 complete", and let
that file be dropped from both Yosys rows with the gate green while Yosys
failed on it. The independent oracle for the walk is a real front end over
exactly the closure: `verilator --lint-only` with an include directory that
holds only headers (so no module can be found by filename) must report zero
MODMISSING.

AND THE CONSUMERS ARE ASKED, NOT PARSED. A recogniser accepts what it has
modelled, and `make` and `bash` accept something else - the lesson
`syn/ooc/dp_srcs.py` records after four escapes. So each consumer prints its
own expansion (`make -s print-srcs`, `syn/yosys/run.sh --emit`,
`syn/yosys/ooc.sh --emit-dp`) and this gate reads that. The Vivado list has no
expansion step; it is read the way Python reads it - the list literal and the
registrations beside it through `ast`, in which a comment does not exist - and
its starred `_pp_sources()` entry is expanded through the same `pp_srcs.py`
that `milan_soc.py` itself calls. A regex over the file's text counted a
commented-out row as carried.

A CONSUMER THAT CANNOT ANSWER FAILS THE GATE. An emit path that exits
non-zero, a Makefile that is absent, a `make` the host lacks: each is a
consumer this run did not check, and by default that is exit 2, never a green
with a note in the log. `--allow-skip` is the explicit opt-out for a host
without the tooling; it prints a loud SKIPPED marker per consumer and the
verdict says how many were not covered. CI runs the strict default. A
diagnosed defect - `print-srcs` having become a makefile's default goal, so a
bare `make` prints a list instead of running the suite - is a finding (exit 1)
and is never skippable.

THE SELF-TEST MUTATES A COPY OF EACH CONSUMER AND ASKS THE COPY. Set
arithmetic on an already-fetched list cannot fail on a passing gate, and would
pass with every fetcher stubbed to return the closure. So `--selftest` copies
each consumer file, removes one closure file from the copy, and runs the copy's
own emit path: `make -f <copy>` from the suite directory, the copied script
beside the original under a temporary name (it resolves the repository from
its own location), the copied Python list through the same reader. The removal
must be reported by that path and by nothing else, the tree must be
byte-identical afterwards, and a stubbed fetcher fails the arm.

THE PROCESSOR'S OWN LIST IS A SIXTH CONSUMER, OF A DIFFERENT AUTHORITY. The
protocol processor's portability gate (`protocol-processor/syn/yosys/run.sh`)
keeps a hand-written `tops` array that its `hdl/README.md` rule 2 says must
name every module, so each is elaborated as a Yosys top. It is not one of the
five milan_datapath lists and `pp_srcs.py` does not feed it, so the closure
walk above cannot see it drift - and at pin 3770ae02 it had: six declared
modules were absent and both repositories reported the processor as covered.
This list is read, not asked, because its only expansion path runs Yosys; so
it is read the way bash reads it - `#` at the start of a word is a comment to
the end of the line, quotes are unquoted - since splitting the raw text
credited a commented-out top as elaborated.
Here the authority is the set of modules DECLARED under `protocol-processor/hdl`;
every one must be a top, or be named in `scripts/processor_yosys_tops.budget`
with the reason it is not. An omission that is not recorded is refused; a
recorded name that has become a top is refused as stale, so the record cannot
outlive the debt it describes. The gPTP processor keeps no native list: its
portability coverage is the closure walk itself, and the inventory prints how
many of its files that walk reaches.

Usage:
    python3 scripts/check_rtl_source_lists.py               # gate, strict
    python3 scripts/check_rtl_source_lists.py --list        # closure, per list, extras
    python3 scripts/check_rtl_source_lists.py --files       # closure paths, packages first
    python3 scripts/check_rtl_source_lists.py --allow-skip  # tool-less host opt-out
    python3 scripts/check_rtl_source_lists.py --selftest    # mutation arms

Exit 0 = every consumer answered and carries the whole closure, and the
         processor tops array names every declared module that the budget
         does not.
Exit 1 = a consumer is missing a file, a makefile's default goal prints the
         list, or the processor tops array has an unrecorded omission or a
         stale record.
Exit 2 = the closure could not be built, or a consumer could not be asked
         (without --allow-skip), or every consumer was skipped.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: the first hop is OWNED by check_soc_sources.py: the instantiation regex,
#: the comment blanking, the include splicing, the search roots and the Vivado
#: list reader. Importing them is the point of this gate: two instantiation
#: parsers would be two truths.
from check_soc_sources import (INST_RE, PREFIXES, SEARCH_ROOTS, SOC, spliced,
                               strip_comments, vivado_sources)
from pp_srcs import pp_sources


def absent_roots() -> list[str]:
    """Declaration roots that are not checked out: with one gone, an unresolved
    module cannot be told apart from a missing tree."""
    return [r for r in SEARCH_ROOTS if not (REPO / r).is_dir()]


def _rel(path):
    try:
        return Path(path).resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


DECL_RE = re.compile(r"^\s*(module|package|interface)\s+([A-Za-z_]\w*)\b", re.M)


@lru_cache(maxsize=1)
def declaration_index() -> dict[str, tuple[str, Path]]:
    """Every module/package/interface declaration, indexed by unit name.
    Comments are blanked first, so a declaration quoted in one is not one."""
    found = {}
    for root in SEARCH_ROOTS:
        base = REPO / root
        if not base.is_dir():
            continue
        for path in sorted(list(base.rglob("*.sv")) + list(base.rglob("*.v"))):
            text = strip_comments(path.read_text(errors="replace"))
            for kind, name in DECL_RE.findall(text):
                found.setdefault(name, (kind, path))
    return found


@lru_cache(maxsize=1)
def units_by_file() -> dict[Path, list[str]]:
    """{resolved path: [unit names it declares]} - the index turned round."""
    out = {}
    for name, (_kind, path) in declaration_index().items():
        out.setdefault(path.resolve(), []).append(name)
    return out


def module_file(name: str) -> Path | None:
    """The source file declaring `name`, or None.

    Declaration membership, not a naming prefix, decides whether a child is
    first-party/project RTL. Prefixes are retained only to turn a misspelled
    project-looking child into an unresolved error.
    """
    item = declaration_index().get(name)
    return item[1] if item else None


PACKAGE_REF_RE = re.compile(r"\b([A-Za-z_]\w*)::")


class Closure(NamedTuple):
    units: dict          # unit name -> repo-relative file declaring it
    unresolved: set      # project-looking module names no source declares
    bad_includes: list   # (unit, include name) pairs no file answers to


@lru_cache(maxsize=None)
def closure(top: str = "milan_datapath") -> Closure:
    """Every project compilation unit reachable from `top`.

    A module instantiation (any shape the first hop accepts, inside included
    bodies too), a package-qualified reference, any use of a declared
    interface's name (through any modport, as a port type, as an instance) and
    an `include of a file that declares a unit all add that unit's file.
    """
    start = module_file(top)
    if start is None:
        return Closure({}, {top}, [])
    index = declaration_index()
    interfaces = [n for n, (kind, _p) in index.items() if kind == "interface"]
    seen, unresolved, bad_includes, queue = {}, set(), [], [(top, start)]
    while queue:
        name, path = queue.pop()
        if name in seen:
            continue
        seen[name] = path.relative_to(REPO).as_posix()
        text, included, missing_inc = spliced(path)
        bad_includes.extend((name, inc) for inc in missing_inc)
        children = set(INST_RE.findall(text))
        children |= {n for n in PACKAGE_REF_RE.findall(text)
                     if index.get(n, (None,))[0] == "package"}
        children |= {n for n in interfaces
                     if re.search(r"\b" + re.escape(n) + r"\b", text)}
        for inc in included:
            children |= set(units_by_file().get(inc.resolve(), ()))
        for child in children:
            if child in seen:
                continue
            child_path = module_file(child)
            if child_path is None:
                if child.startswith(PREFIXES):
                    unresolved.add(child)
            else:
                queue.append((child, child_path))
    return Closure(seen, unresolved, bad_includes)


# ---------------------------------------------------------------------------
# consumers - each ASKS its own tooling for the expansion it will really use
# ---------------------------------------------------------------------------
class Answer(NamedTuple):
    files: object   # the repo-relative files the consumer will compile, or None
    kind: str       # "ok" | "unanswered" (could not ask) | "defect" (diagnosed)
    why: object     # the reason, when kind is not "ok"


def _repo_rel(tokens, cwd):
    """Resolve a consumer's own path tokens to repo-relative posix paths.

    A source list is a list of FILES, and one file may declare several modules
    (`KL_aaf_latency_chain` lives inside `KL_aaf_latency_taps.sv`,
    `event_counter` beside `ethernet_events`). Comparing module names to file
    stems would demand entries that must not exist, so the comparison is made
    where the lists actually live: on files."""
    out = set()
    for tok in tokens:
        if not tok.endswith((".sv", ".v")):
            continue
        try:
            out.add((cwd / tok).resolve().relative_to(REPO).as_posix())
        except ValueError:
            continue          # outside the repo: not something a gate can own
    return out


def _run(cmd, cwd):
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                             timeout=300)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"{cmd[0]}: {exc}"
    if out.returncode != 0:
        return None, f"{' '.join(str(c) for c in cmd)} exited {out.returncode}"
    return out.stdout, None


def default_goal_is_print_srcs(directory: Path,
                               makefile: str | Path = "Makefile") -> bool | None:
    """True when a bare `make` in `directory` would print the source list,
    False when it would not, None when make could not say.

    Adding a `print-srcs` target ABOVE a makefile's first real target makes it
    the default goal, so the suite stops running and prints a file list. The
    tally gate then reports NOCOUNT rather than a failure, which is a suite
    that measured nothing wearing the costume of a suite that passed. This
    happened here when print-srcs was first added to a Verilator suite.

    MAKE ASKS ITSELF. A second makefile adds one target that echoes
    `.DEFAULT_GOAL`, which make has already resolved from the FIRST target of
    the first makefile - so this reads make's own answer rather than a model of
    makefile syntax. Comparing a dry run to the printed list does not work: an
    `@`-prefixed recipe makes `-n` print the command, not run it.
    """
    with tempfile.TemporaryDirectory() as td:
        probe = Path(td) / "probe.mk"
        probe.write_text("__kl_show_default_goal:\n\t@echo $(.DEFAULT_GOAL)\n")
        out, _err = _run(["make", "-s", "-f", str(makefile), "-f", str(probe),
                          "__kl_show_default_goal"], directory)
    if out is None or not out.strip():
        return None
    return out.strip().splitlines()[-1].strip() == "print-srcs"


def _from_make(suite, makefile=None):
    """`make -s print-srcs` in the suite directory. A copy of the Makefile is
    fed with `-f` and still runs from the suite directory, so its relative
    paths and `$(CURDIR)` resolve exactly as the original's do."""
    d = REPO / "tb/verilator" / suite
    mk = Path(makefile) if makefile else d / "Makefile"
    if not mk.is_file():
        return Answer(None, "unanswered", f"{_rel(mk)} is absent")
    text, err = _run(["make", "-s", "-f", str(mk), "print-srcs"], d)
    if text is None:
        return Answer(None, "unanswered", err)
    goal = default_goal_is_print_srcs(d, mk)
    if goal is None:
        return Answer(None, "unanswered",
                      f"tb/verilator/{suite}: make could not report its default goal")
    if goal:
        return Answer(None, "defect",
                      f"tb/verilator/{suite}: a bare `make` prints the source list "
                      f"instead of running the suite - print-srcs has become the "
                      f"default goal")
    return Answer(_repo_rel(text.split(), d), "ok", None)


def _from_yosys_run(script=None):
    """`run.sh --emit milan_datapath`, the record bash prints from its own
    expansion of the `tops` row. A copy must sit beside the original: the
    script resolves the repository from `$0`."""
    s = Path(script) if script else REPO / "syn/yosys/run.sh"
    if not s.is_file():
        return Answer(None, "unanswered", f"{_rel(s)} is absent")
    text, err = _run([str(s), "--emit", "milan_datapath"], s.parent)
    if text is None:
        return Answer(None, "unanswered", err)
    names = set()
    for line in text.splitlines():
        if line.startswith("src="):
            names |= _repo_rel(line[4:].split(), s.parent)
    return Answer(names, "ok", None)


def _from_yosys_ooc(script=None):
    """`ooc.sh --emit-dp`, bash's own expansion of `DP_SRCS`."""
    s = Path(script) if script else REPO / "syn/yosys/ooc.sh"
    if not s.is_file():
        return Answer(None, "unanswered", f"{_rel(s)} is absent")
    text, err = _run([str(s), "--emit-dp"], s.parent)
    if text is None:
        return Answer(None, "unanswered", err)
    return Answer(_repo_rel(text.split(), s.parent), "ok", None)


def _from_vivado_list(soc=None):
    """The source paths `milan_soc.py` registers, read as Python reads them
    (check_soc_sources.vivado_sources), with the starred `_pp_sources()` entry
    expanded through the same `pp_srcs.py` the SoC calls - and only when that
    entry is still there."""
    s = Path(soc) if soc else SOC
    if not s.is_file():
        return Answer(None, "unanswered", f"{_rel(s)} is absent")
    paths, derived, why = vivado_sources(s)
    if paths is None:
        return Answer(None, "unanswered", why)
    tokens = list(paths)
    if "_pp_sources" in derived:
        tokens += pp_sources()
    return Answer(_repo_rel(tokens, REPO), "ok", None)


class Consumer(NamedTuple):
    label: str
    fetch: object        # fetch() -> Answer for the real consumer;
                         # fetch(copy) -> the same emit path over a copy
    source: str          # the consumer file, repo-relative
    copy_beside: bool    # a copy must live in the consumer's own directory
                         # because the script resolves the repository from $0


CONSUMERS = (
    Consumer("Vivado sources (sw/litex/milan_soc.py)", _from_vivado_list,
             "sw/litex/milan_soc.py", False),
    Consumer("Yosys milan_datapath row (syn/yosys/run.sh)", _from_yosys_run,
             "syn/yosys/run.sh", True),
    Consumer("Yosys DP_SRCS (syn/yosys/ooc.sh)", _from_yosys_ooc,
             "syn/yosys/ooc.sh", True),
    Consumer("Verilator milan_dp (tb/verilator/milan_dp)",
             lambda copy=None: _from_make("milan_dp", copy),
             "tb/verilator/milan_dp/Makefile", False),
)


# ---------------------------------------------------------------------------
# the processor-native Yosys tops list - declared modules are the authority
# ---------------------------------------------------------------------------
#: (submodule, its portability script, the RTL root whose declarations it must
#: name). One entry today; a second processor that grows a native tops list is
#: added here and nowhere else.
PROCESSOR_TOPS = (("protocol-processor", "syn/yosys/run.sh", "hdl"),)

#: one `processor_tops_audit()` row: the submodule and its script, the tops the
#: script elaborates, every module its RTL root declares, the recorded
#: omissions still absent, the unrecorded ones, the stale records, and the
#: reason the row could not be read at all.
TopsRow = tuple[str, str, set[str], set[str], list[str], list[str], list[str],
                str | None]
TOPS_BUDGET = REPO / "scripts/processor_yosys_tops.budget"
_TOPS_ARRAY_RE = re.compile(r"\btops=\(")


def bash_array_words(text: str, pos: int) -> tuple[list[str], int] | None:
    """The words of a bash `( ... )` array literal whose body starts at `pos`,
    read the way bash reads it: `#` at the start of a word opens a comment to
    the end of the line; `'...'` is literal; `"..."` is literal except that a
    backslash quotes a following `"`, `\\`, `$`, backquote or newline; an
    unquoted backslash quotes the next character; and the literal ends at the
    first `)` that is none of those. Nothing is expanded - the entries are
    plain module names, and a `$var` here stays the word `$var`, which names
    no declared module and so is refused rather than credited. Returns
    (words, index after the `)`), or None when the literal is never closed.

    The array cannot be ASKED like the other consumers: the script's only
    expansion path elaborates every top through Yosys. Reading its raw text
    with split() credited a commented-out top as elaborated, since `# KL_b`
    became the words `#` and `KL_b` (PR #277 review)."""
    words, word, in_word = [], [], False
    n = len(text)
    while pos < n:
        c = text[pos]
        if c in " \t\n":
            if in_word:
                words.append("".join(word))
                word, in_word = [], False
            pos += 1
        elif c == "#" and not in_word:
            nl = text.find("\n", pos)
            pos = n if nl < 0 else nl + 1
        elif c == ")":
            if in_word:
                words.append("".join(word))
            return words, pos + 1
        elif c == "'":
            end = text.find("'", pos + 1)
            if end < 0:
                return None
            word.append(text[pos + 1:end])
            in_word, pos = True, end + 1
        elif c == '"':
            in_word, pos = True, pos + 1
            while pos < n and text[pos] != '"':
                if text[pos] == "\\" and pos + 1 < n and text[pos + 1] in '"\\$`\n':
                    if text[pos + 1] != "\n":
                        word.append(text[pos + 1])
                    pos += 2
                else:
                    word.append(text[pos])
                    pos += 1
            if pos >= n:
                return None
            pos += 1
        elif c == "\\":
            if pos + 1 >= n:
                return None
            if text[pos + 1] != "\n":
                word.append(text[pos + 1])
                in_word = True
            pos += 2
        else:
            word.append(c)
            in_word, pos = True, pos + 1
    return None


def parse_tops_array(text: str) -> set[str] | None:
    """The names in a bash `tops=( ... )` array as bash would run them, or
    None when there is no such array or it is never closed."""
    m = _TOPS_ARRAY_RE.search(text)
    if m is None:
        return None
    parsed = bash_array_words(text, m.end())
    return None if parsed is None else set(parsed[0])


def declared_modules(text: str) -> set[str]:
    """Module names declared in one SystemVerilog source (packages and
    interfaces are not tops and are not counted)."""
    return set(re.findall(r"^\s*module\s+([A-Za-z_]\w*)\b", text, re.M))


def read_tops_budget(text: str) -> dict[str, str]:
    """`name  reason` per line; `#` starts a comment. Returns {name: reason}."""
    out = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        name, _, reason = line.partition(" ")
        out[name] = reason.strip()
    return out


def compare_tops(tops: set[str], declared: set[str],
                 recorded: dict[str, str]) -> tuple[list[str], list[str]]:
    """(unrecorded, stale) - the two refusals.

    `unrecorded`: declared modules that are neither tops nor in the budget.
    `stale`: budget names that are tops now (the debt was paid upstream and the
    record must go) or that no source declares any more."""
    missing = declared - tops
    unrecorded = sorted(missing - set(recorded))
    stale = sorted(n for n in recorded if n not in missing)
    return unrecorded, stale


def processor_tops_audit() -> list[TopsRow]:
    """[(submodule, script, tops, declared, recorded_missing, unrecorded,
    stale, skip_reason)] - one row per PROCESSOR_TOPS entry."""
    recorded = read_tops_budget(TOPS_BUDGET.read_text()) if TOPS_BUDGET.is_file() else {}
    rows = []
    for sub, script, hdl in PROCESSOR_TOPS:
        path = REPO / sub / script
        root = REPO / sub / hdl
        if not root.is_dir():
            rows.append((sub, script, set(), set(), [], [], [],
                         f"{sub}/{hdl} is not checked out"))
            continue
        if not path.is_file():
            rows.append((sub, script, set(), set(), [], [], [],
                         f"{sub}/{script} is absent at this pin"))
            continue
        tops = parse_tops_array(path.read_text(errors="replace"))
        if tops is None:
            rows.append((sub, script, set(), set(), [], [], [],
                         f"{sub}/{script} carries no closed tops=( ... ) array"))
            continue
        declared = set()
        for src in sorted(root.rglob("*.sv")):
            declared |= declared_modules(src.read_text(errors="replace"))
        unrecorded, stale = compare_tops(tops, declared, recorded)
        recorded_missing = sorted((declared - tops) & set(recorded))
        rows.append((sub, script, tops, declared, recorded_missing, unrecorded,
                     stale, None))
    return rows


# ---------------------------------------------------------------------------
# the comparison and the verdict
# ---------------------------------------------------------------------------
class Row(NamedTuple):
    label: str
    kind: str        # "ok" | "unanswered" | "defect"
    missing: list    # closure files the consumer does not carry
    extra: list      # files the consumer carries that the closure does not need
    why: object


def audit(consumers: Sequence[Consumer] = CONSUMERS,
          top: str = "milan_datapath") -> tuple[Closure, set[str], list[Row]]:
    """(closure, need, rows) - one Row per consumer."""
    cl = closure(top)
    need = set(cl.units.values())
    rows = []
    for c in consumers:
        answer = c.fetch()
        if answer.kind != "ok":
            rows.append(Row(c.label, answer.kind, [], [], answer.why))
        else:
            rows.append(Row(c.label, "ok", sorted(need - answer.files),
                            sorted(answer.files - need), None))
    return cl, need, rows


def verdict(cl: Closure, need: set[str], rows: list[Row],
            tops_rows: list[TopsRow], allow_skip: bool = False,
            list_mode: bool = False) -> tuple[int, list[str]]:
    """(rc, lines). The exit code is decided here and nowhere else.

    0: every consumer answered and is complete, the tops audit is clean.
    1: a finding - a missing file, a default-goal defect, tops drift or a stale
       record. Never skippable.
    2: a consumer could not be asked and --allow-skip was not given, or every
       consumer was skipped (a run that checked nothing proves nothing).
    """
    lines = []
    findings = skipped = unanswered = answered = 0
    for row in rows:
        if row.kind == "unanswered":
            if allow_skip:
                skipped += 1
                lines.append(f"!! SKIPPED (--allow-skip)  {row.label}: {row.why}  "
                             f"-- NOT COVERED by this verdict")
            else:
                unanswered += 1
                lines.append(f"CANNOT ASK  {row.label}: {row.why} -> this consumer "
                             f"was not checked; pass --allow-skip to accept that "
                             f"on a host without the tooling")
            continue
        if row.kind == "defect":
            findings += 1
            lines.append(f"DEFAULT GOAL: {row.why} -> fix the makefile "
                         f"(.DEFAULT_GOAL := all, or the real target first)")
            continue
        answered += 1
        for path in row.missing:
            findings += 1
            names = sorted(m for m, p in cl.units.items() if p == path)
            lines.append(f"MISSING SOURCE: {row.label} does not carry '{path}' "
                         f"(declares {', '.join(names)}), which milan_datapath "
                         f"needs -> that consumer cannot build")
        if list_mode:
            if not row.missing:
                lines.append(f"ok       {row.label}")
            if row.extra:
                lines.append(f"extra    {row.label}: {len(row.extra)} file(s) the "
                             f"closure does not need: {', '.join(row.extra)}")

    tops_note = []
    for sub, script, tops, declared, recorded, unrecorded, stale, why in tops_rows:
        if why is not None:
            if allow_skip:
                skipped += 1
                lines.append(f"!! SKIPPED (--allow-skip)  {sub} native tops list: "
                             f"{why}  -- NOT COVERED by this verdict")
            else:
                unanswered += 1
                lines.append(f"CANNOT ASK  {sub} native tops list: {why}")
            continue
        for name in unrecorded:
            findings += 1
            lines.append(f"TOPS DRIFT: {sub}/{script} does not elaborate declared "
                         f"module '{name}' as a top and "
                         f"scripts/processor_yosys_tops.budget does not record why "
                         f"-> its portability is unproven")
        for name in stale:
            findings += 1
            lines.append(f"STALE RECORD: scripts/processor_yosys_tops.budget names "
                         f"'{name}' but {sub}/{script} elaborates it (or nothing "
                         f"declares it) -> remove the line")
        if list_mode or recorded:
            lines.append(f"{sub} native tops list ({script}): {len(tops)} top(s) for "
                         f"{len(declared)} declared module(s); {len(recorded)} "
                         f"recorded omission(s) at this pin: {', '.join(recorded) or '-'}")
        tops_note.append(f"{sub} {len(tops)}/{len(declared)} tops, {len(recorded)} recorded")

    if list_mode:
        gptp = {p for p in cl.units.values() if p.startswith("gptp-processor/")}
        lines.append(f"gptp-processor keeps no native tops list; the closure walk "
                     f"reaches {len(gptp)} of its file(s)")

    if unanswered:
        lines.append(f"RTL source-list gate: NOT CHECKED - {unanswered} consumer(s) "
                     f"could not be asked ({findings} finding(s) among the rest)")
        return 2, lines
    if findings:
        return 1, lines
    if not answered:
        lines.append("RTL source-list gate: NOT CHECKED - every consumer was skipped, "
                     "so this run proved nothing")
        return 2, lines
    text = (f"RTL source-list gate: OK ({len(need)} files in the milan_datapath "
            f"closure, {answered} of {len(rows)} consumer list(s) carry all of them; "
            f"{'; '.join(tops_note) or 'no processor tops list reachable'}")
    lines.append(text + (f"; {skipped} SKIPPED by --allow-skip and NOT covered by "
                         f"this verdict)" if skipped else ")"))
    return 0, lines


# ---------------------------------------------------------------------------
# self-test support: a mutated COPY of a consumer, asked through its own path
# ---------------------------------------------------------------------------
def drop_source_token(text: str, basename: str) -> str:
    """The consumer text with every path token ending in `/basename` removed:
    a quoted Python row (with its comma) or a bare shell/make word."""
    b = re.escape(basename)
    return re.sub(r'"[^"\s]*/' + b + r'"\s*,?'
                  r'|(?<=[\s|="])\S*/' + b + r'(?=\s|$|")', "", text)


@contextmanager
def mutated_copy(consumer: Consumer, basename: str) -> Iterator[Path | None]:
    """A copy of the consumer file with one source removed, placed where its
    emit path can run: beside the original under a temporary name when the
    script resolves the repository from `$0`, in a temporary directory
    otherwise. Deleted on the way out, whatever happened."""
    src = REPO / consumer.source
    text = src.read_text()
    mutated = drop_source_token(text, basename)
    if mutated == text:
        yield None
        return
    td = None
    if consumer.copy_beside:
        copy = src.parent / f".selftest-{os.getpid()}-{src.name}"
    else:
        td = tempfile.mkdtemp()
        copy = Path(td) / src.name
    try:
        copy.write_text(mutated)
        shutil.copymode(src, copy)
        yield copy
    finally:
        copy.unlink(missing_ok=True)
        if td is not None:
            shutil.rmtree(td, ignore_errors=True)


def selftest() -> int:
    """Mutation arms. Every one removes or breaks something and demands the
    right complaint; each fails when the defect it guards is put back.

    They live in ``check_rtl_source_lists_selftest``: one long list of
    independent fixtures with no reader in common with the rules above, and
    importing them only when --selftest is asked for keeps this module's own
    import free of them.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_rtl_source_lists_selftest import run_arms
    return run_arms()


def main() -> int:
    """Build the closure, ask every consumer, and print the verdict it exits on."""
    args = sys.argv[1:]
    unknown = [a for a in args
               if a not in ("--list", "--files", "--selftest", "--allow-skip")]
    if unknown:
        print(f"unknown option(s): {' '.join(unknown)}", file=sys.stderr)
        print(__doc__.split("Usage:")[1].split("Exit 0")[0], file=sys.stderr)
        return 2
    if "--selftest" in args:
        return selftest()

    gone = absent_roots()
    if gone:
        print(f"CANNOT BUILD THE CLOSURE: source root(s) {', '.join(gone)} are "
              f"not checked out, so an unresolved module cannot be told apart "
              f"from a missing tree. Run `git submodule update --init`.")
        return 2
    cl, need, rows = audit()
    if not need or cl.unresolved or cl.bad_includes:
        for name in sorted(cl.unresolved):
            print(f"UNRESOLVED MODULE: '{name}' is instantiated but no source in "
                  f"{', '.join(SEARCH_ROOTS)} declares it")
        for unit, inc in cl.bad_includes:
            print(f"UNRESOLVED INCLUDE: {unit} `include's '{inc}' but no file under "
                  f"{', '.join(SEARCH_ROOTS)} answers to it, so its body could not "
                  f"be walked")
        if not need:
            print("CLOSURE EMPTY: milan_datapath could not be read")
        return 2

    if "--files" in args:
        # the closure as a front end wants it: packages first, one path per line
        packages = {p for u, p in cl.units.items()
                    if declaration_index()[u][0] == "package"}
        for path in sorted(packages) + sorted(need - packages):
            print(path)
        return 0

    list_mode = "--list" in args
    if list_mode:
        print(f"file closure of milan_datapath ({len(need)} file(s), "
              f"{len(cl.units)} module/package/interface unit(s)):")
        for path in sorted(need):
            names = sorted(m for m, p in cl.units.items() if p == path)
            print(f"   {path}  [{', '.join(names)}]")
        print()

    rc, lines = verdict(cl, need, rows, processor_tops_audit(),
                        allow_skip="--allow-skip" in args, list_mode=list_mode)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
