#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: first-party Python says what it means, and a stranger can fix it.

Why this exists. Rule 12 of the maintainability guide
(docs/development/CODE_QUALITY.md) is the Python half of the same argument
Rule 10 makes for SystemVerilog and Rule 11 makes for C++: the language's own
idiom is not a style preference, it is the difference between a reader who can
change one thing and a reader who has to understand everything first.

This tree has 129 tracked first-party Python files and 104 847 lines - more
Python than SystemVerilog - and until this gate there was no Python linter,
formatter or type-checker configuration anywhere in it. Twenty-six hand-written
gates police the RTL and the documentation; nothing policed the gates.

The checks are AST-based, never textual, so a construct inside a string or a
docstring is not a finding and cannot be one.

REFUSED - the population is zero, or small enough that one commit clears it.

  1. A BARE `except:`. It swallows `KeyboardInterrupt` and `SystemExit`, so a
     gate that uses one cannot be interrupted and can report a pass after being
     killed. Measured population: zero. Every handler in the tree names a type.

  2. A MUTABLE DEFAULT ARGUMENT - `def f(x=[])`, `{}`, `set()`, `list()`,
     `dict()`. The default object is created once, at def time, and every call
     that mutates it changes the default for every later call. Measured
     population: zero, across 3 192 function definitions.

  3. `shell=True` OR `os.system()`. Every subprocess call in this tree already
     passes an argument list, which is both injection-proof and readable
     without knowing a shell's quoting rules. Measured population: zero.

  4. SHADOWING A BUILT-IN by binding one of `BUILTIN_NAMES` as a variable,
     parameter, function or class. `type = ...` costs the rest of the scope
     the ability to call `type()`, and the reader never sees why.

  5. A WILDCARD IMPORT (`from X import *`), unless the module is in
     `WILDCARD_EXCEPTIONS`. The three in this tree are `from migen import *` in
     the LiteX sources, which is that framework's documented usage; they are
     recorded there with the reason rather than tolerated silently.

  6. `eval()` OR `exec()` on anything but a literal, unless the call site is in
     `DYNAMIC_EXEC_INVENTORY` with its guard and its reason. Two of the four
     sites already carried a `# noqa: S307` marker, which is a hazard noticed
     and then left unenforced.

RATCHETED - too large to repair in one behaviour-preserving change, so the
count is recorded in `scripts/py_idiom.budget` and may only go down.

  7. A FUNCTION OVER `LONG_FUNCTION_LINES` LINES. 133 functions hold 40 584
     lines - 39% of all the Python in the tree lives inside 4% of its
     functions. The largest is 7 059 lines and contains 103 nested `def`s,
     239 asserts and 557 statements of its own; a traceback out of any of its
     239 failure modes names one function, and `git blame` on any line in it
     reports the whole suite.

  8. A MODULE OVER `LONG_MODULE_LINES` LINES. 27 of 129 files hold 66% of the
     population. The largest is 15 594 lines with 274 statements that run on
     import.

  9. A PUBLIC FUNCTION WITHOUT A COMPLETE PEP 484 SIGNATURE - every
     non-`self` parameter annotated and a return annotation. 386 of 2 698
     public functions have one. `scripts/act_ci.py` annotates 167 of its 171,
     so this is a house skill that simply was not asked for anywhere else.

 10. A PUBLIC FUNCTION WITHOUT A DOCSTRING.

 11. AN `os.path` USE. `pathlib` is what the canonical helpers
     (`code_quality_scope.py`, `check_sv_idiom.py`) use, and files that mix
     both leave a reader unable to tell whether a variable holding "a path" is
     a `str` or a `Path`.

 12. AN `open()` OUTSIDE A `with` STATEMENT. 227 of the 250 are
     `open(p).read()` one-liners that lean on refcount collection to close the
     handle; `Path(p).read_text()` says the same thing in fewer characters and
     closes deterministically.

 13. A FUNCTION TAKING MORE THAN `MAX_PARAMETERS` PARAMETERS. The largest
     takes 33, all positional-or-keyword, all untyped, several adjacent pairs
     of the same type and default.

 14. A `global` STATEMENT. All 41 are a self-test reaching up to overwrite its
     own module's contract constants so an arm will fire; the arms are then
     order-dependent and leave the module permanently mutated.

 15. A SOURCE LINE OVER `MAX_COLUMNS` COLUMNS. Deliberately 120 and not the
     100 Rule 9 rejected repository-wide: 100 fights the `$error` and
     source-list rules that Rule 9 records, and 120 does not.

WHAT IS NOT CHECKED, deliberately.

  * FORMATTING IS NOT CHECKED, and no formatter is run. Rule 9 records why: a
    flag-day `black` or `ruff format` rollout would rewrite every file in the
    tree and bury real findings under a new baseline nobody reads. Line length
    is the one lay-out property here, and only at 120.

  * NESTING DEPTH IS RULE 2's. `scripts/measure_control_flow.py` already
    measures it and deliberately proposes no threshold.

  * NAMING IS RULE 4's, except for the built-in shadowing above, which is a
    correctness hazard rather than a naming preference.

  * A PRIVATE FUNCTION (leading underscore) OWES NO SIGNATURE OR DOCSTRING.
    The rule is about what crosses a module boundary.

WHAT THE POPULATION IS. Every tracked first-party `*.py` in this repository and
in the two pinned project-owned processors, through the shared scope helper
(`code_quality_scope.py`, which refuses an absent or off-pin processor). A file
that does not parse is a finding in itself and is reported, not skipped.

Usage:

    python3 scripts/check_py_idiom.py                 # the gate
    python3 scripts/check_py_idiom.py --list          # per-file counts
    python3 scripts/check_py_idiom.py --write-budget  # re-record the ratchets
    python3 scripts/check_py_idiom.py --selftest      # the fixture arms

Exit 0 = no refused construct and every ratchet in `scripts/py_idiom.budget`
holds; 1 = a finding, or a missing or malformed ratchet entry; 2 = the
population was refused, which no caller may read as a count of zero.
"""

import argparse
import ast
import builtins
import sys
from collections.abc import Sequence
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "py_idiom.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import PROJECT_SUBMODULES, tracked  # noqa: E402

#: The population must reach each of these, or the scan is measuring a tree
#: that is not there.
POPULATION_ROOTS = ("scripts/", "sw/", "tb/") + tuple(
    f"{sub}/" for sub in PROJECT_SUBMODULES)

#: F.3's Python sibling. The same 100 `check_cpp_idiom.py` uses, so a reader
#: does not have to remember two numbers.
LONG_FUNCTION_LINES = 100

#: A module a reviewer can open. 1000 is generous and still excludes 27 files.
LONG_MODULE_LINES = 1000

#: I.24/F.15's Python sibling. Above six, a caller cannot check the order.
MAX_PARAMETERS = 6

#: Rule 9 measured and REJECTED a 100-column check for this tree, with the
#: reasons on the record. 120 does not fight either of them.
MAX_COLUMNS = 120

#: Shadowing one of these costs the rest of the scope the ability to call it.
#: Restricted to the names whose loss actually bites; `id` and `input` are
#: shadowed harmlessly and often enough that including them would be a fight.
BUILTIN_NAMES = frozenset({
    "type", "set", "list", "dict", "tuple", "str", "int", "float", "bool",
    "bytes", "len", "map", "filter", "range", "sum", "min", "max", "next",
    "open", "print", "hash", "format", "object", "vars", "dir", "compile",
}) & frozenset(dir(builtins))

#: `from X import *` is refused except for a framework that documents it as the
#: usage. Each entry names the module and why, because an unexplained exception
#: is how the next one gets added.
WILDCARD_EXCEPTIONS = {
    "migen": "the migen/LiteX DSL is documented as `from migen import *`; the "
             "names it exports are the language of a migen module",
}

#: `eval`/`exec` on a non-literal, with the guard that makes each safe. An entry
#: is a (path, reason) pair; a site not listed here is refused. All three read a
#: number out of a source file that is the contract, rather than restating it
#: where the two could drift, and all three prove the text is arithmetic before
#: evaluating it. That proof is the entry fee: an unguarded `eval` on file text
#: is refused however good the reason.
DYNAMIC_EXEC_INVENTORY = {
    "sw/builder/test_builder.py":
        "reads a C `#define` bit expression out of the firmware source. Guarded "
        "by `re.fullmatch(r'[0-9A-Fa-fxX()~|&^<>+\\-\\s]*')` and a second pass "
        "refusing any residual identifier, with `__builtins__` emptied.",
    "sw/trace/test_trace_roundtrip.py":
        "reads MILAN_TRACE_BUDGET_BYTES_PER_HOUR and MILAN_TRACE_MIN_FLUSH_BYTES "
        "out of milan_trace.h, which is the ABI. `_c_define_int` parses the "
        "expression and walks every node against an integer-arithmetic "
        "whitelist before compiling it, with `__builtins__` emptied.",
    "tests/steps/crf_class_a_steps.py":
        "resolves a SystemVerilog localparam expression after substituting its "
        "identifiers. Guarded by `re.fullmatch(r'[\\s0-9+\\-*/()]+')`, so only "
        "digits and the four operators reach it.",
}

RATCHETED = (
    "long function",
    "long module",
    "unannotated public function",
    "undocumented public function",
    "os.path use",
    "unmanaged open",
    "too many parameters",
    "global statement",
    "over-long line",
)

REFUSED = (
    "bare except",
    "mutable default argument",
    "shell invocation",
    "shadowed builtin",
    "wildcard import",
    "dynamic eval/exec",
    "unparseable source",
)

#: How many of each finding one module carries, keyed by finding name. Every
#: key in `RATCHETED` and `REFUSED` is present, at zero when nothing was found,
#: so a caller never has to distinguish "clean" from "not measured".
Counts = dict[str, int]

#: Where each of those findings is: `{key: [(line, detail)]}`, detail being the
#: text the report prints after the location.
Sites = dict[str, list[tuple[int, str]]]

#: A function definition in either of its two AST spellings.
FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef


def sources() -> list[str]:
    """Every tracked first-party *.py, across both project processors."""
    return sorted(tracked("*.py"))


def population_problem(paths: Sequence[str]) -> str | None:
    """Why this population may not be judged, or None when it is complete."""
    if not paths:
        return "the scan found no tracked Python at all"
    missing = [root for root in POPULATION_ROOTS
               if not any(p.startswith(root) for p in paths)]
    if missing:
        return "no tracked Python under " + ", ".join(missing)
    return None


def _is_public(node: FunctionNode) -> bool:
    return not node.name.startswith("_")


def _parameters(node: FunctionNode) -> list[ast.arg]:
    args = node.args
    return args.posonlyargs + args.args + args.kwonlyargs


def _fully_annotated(node: FunctionNode) -> bool:
    named = [a for a in _parameters(node) if a.arg not in ("self", "cls")]
    return all(a.annotation is not None for a in named) and node.returns is not None


def _bound_names(tree: ast.AST) -> list[tuple[int, str]]:
    """Names bound in a scope where they would shadow a built-in.

    A CLASS BODY IS NOT SUCH A SCOPE, and this is not a technicality. A
    dataclass field `type: int` and a method `def set(self, ...)` live in the
    class namespace: nothing inside the class can reach them unqualified, so
    neither costs any scope the ability to call `type()` or `set()`. They are
    also exactly where a protocol field has to keep the name the specification
    gives it - `tb/tools/avtp_wire_truth.py` names an IEEE 1722 header field
    `type` because that is what the standard calls it. A first version of this
    gate counted all four and would have demanded a rename that made the
    structures disagree with the document they encode. Class bodies are
    therefore descended into only for their functions.
    """
    names: list[tuple[int, str]] = []

    def visit(node: ast.AST, in_class_body: bool) -> None:
        """Collect into `names` every binding this subtree makes.

        `in_class_body` is what carries the rule above down the walk: a name
        bound directly in a class body is recorded nowhere, while a function
        nested anywhere below one is descended into as ordinary code.
        """
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                visit(child, in_class_body=True)
                continue
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not in_class_body:
                    names.append((child.lineno, child.name))
                names.extend((child.lineno, a.arg) for a in _parameters(child))
                visit(child, in_class_body=False)
                continue
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
                if not in_class_body:
                    names.append((child.lineno, child.id))
            visit(child, in_class_body)

    visit(tree, in_class_body=False)
    return names


def _is_mutable_default(node: ast.expr) -> bool:
    if isinstance(node, (ast.List, ast.Dict, ast.Set)):
        return True
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in ("list", "dict", "set", "bytearray"))


def _managed_opens(tree: ast.AST) -> set[tuple[int, int]]:
    """Positions of every `open(...)` that IS a `with` item's context."""
    managed: set[tuple[int, int]] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                for sub in ast.walk(item.context_expr):
                    if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
                            and sub.func.id == "open"):
                        managed.add((sub.lineno, sub.col_offset))
    return managed


def scan(text: str, rel: str = "x.py") -> tuple[Counts, Sites]:
    """(counts, sites) for one module's source text."""
    counts: Counts = dict.fromkeys(tuple(RATCHETED) + tuple(REFUSED), 0)
    sites: Sites = {key: [] for key in counts}

    def hit(key: str, lineno: int, detail: str) -> None:
        """Record one more `key` finding, at `lineno`, with the text to print."""
        counts[key] += 1
        sites[key].append((lineno, detail))

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        hit("unparseable source", exc.lineno or 1, f"{exc.msg}")
        return counts, sites

    lines = text.splitlines()
    if len(lines) > LONG_MODULE_LINES:
        hit("long module", 1, f"{len(lines)} lines")
    for lineno, line in enumerate(lines, 1):
        if len(line) > MAX_COLUMNS:
            hit("over-long line", lineno, f"{len(line)} columns")

    managed = _managed_opens(tree)

    for lineno, name in _bound_names(tree):
        if name in BUILTIN_NAMES:
            hit("shadowed builtin", lineno, name)

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            hit("bare except", node.lineno, "except:")

        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                if node.module not in WILDCARD_EXCEPTIONS:
                    hit("wildcard import", node.lineno,
                        f"from {node.module} import *")

        elif isinstance(node, ast.Global):
            for name in node.names:
                hit("global statement", node.lineno, name)

        elif isinstance(node, ast.Attribute):
            if (isinstance(node.value, ast.Name) and node.value.id == "os"
                    and node.attr == "path"):
                hit("os.path use", node.lineno, "os.path")

        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                if func.id == "open" and (node.lineno, node.col_offset) not in managed:
                    hit("unmanaged open", node.lineno, "open(...) outside a with")
                if func.id in ("eval", "exec"):
                    literal = node.args and isinstance(node.args[0], ast.Constant)
                    if not literal and rel not in DYNAMIC_EXEC_INVENTORY:
                        hit("dynamic eval/exec", node.lineno, f"{func.id}(...)")
            if isinstance(func, ast.Attribute) and func.attr == "system":
                if isinstance(func.value, ast.Name) and func.value.id == "os":
                    hit("shell invocation", node.lineno, "os.system(...)")
            for kw in node.keywords:
                if (kw.arg == "shell" and isinstance(kw.value, ast.Constant)
                        and kw.value.value is True):
                    hit("shell invocation", node.lineno, "shell=True")

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            length = end - node.lineno + 1
            if length > LONG_FUNCTION_LINES:
                hit("long function", node.lineno, f"{node.name} is {length} lines")
            if len(_parameters(node)) + bool(node.args.vararg) + bool(node.args.kwarg) \
                    > MAX_PARAMETERS:
                hit("too many parameters", node.lineno,
                    f"{node.name} takes {len(_parameters(node))}")
            for default in list(node.args.defaults) + list(node.args.kw_defaults):
                if default is not None and _is_mutable_default(default):
                    hit("mutable default argument", node.lineno, node.name)
            if _is_public(node):
                if not _fully_annotated(node):
                    hit("unannotated public function", node.lineno, node.name)
                if ast.get_docstring(node) is None:
                    hit("undocumented public function", node.lineno, node.name)

    return counts, sites


def audit(paths: Sequence[str]) -> tuple[Counts, dict[str, tuple[Counts, Sites]]]:
    """The population's summed counts, and each module's own counts and sites.

    Every path is read and scanned exactly once, so the caller may report a
    finding's location without re-parsing the module it came from.
    """
    totals: Counts = dict.fromkeys(tuple(RATCHETED) + tuple(REFUSED), 0)
    per_file: dict[str, tuple[Counts, Sites]] = {}
    for rel in paths:
        counts, sites = scan((REPO / rel).read_text(errors="replace"), rel)
        per_file[rel] = (counts, sites)
        for key, value in counts.items():
            totals[key] += value
    return totals, per_file


def parse_budget(text: str) -> Counts:
    """{key: int} from budget text; a malformed value simply has no entry."""
    out: Counts = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            key, value = line.split("=", 1)
            if value.strip().isdigit():
                out[key.strip()] = int(value.strip())
    return out


def read_budget() -> Counts:
    """The recorded ratchets; an absent budget file reads as no entries at all.

    That empty result is deliberately not a pass: `ratchet` treats a missing
    key as a failure, so a deleted budget file fails the gate rather than
    silently granting every count an unbounded allowance.
    """
    return parse_budget(BUDGET.read_text()) if BUDGET.is_file() else {}


def ratchet(totals: Counts, budget: Counts) -> tuple[list[str], list[str]]:
    """Missing entry = failure; over = failure; under = pass plus a note."""
    failures: list[str] = []
    notes: list[str] = []
    for key in RATCHETED:
        limit = budget.get(key)
        if limit is None:
            failures.append(f"NO RATCHET for {key!r} in {BUDGET.relative_to(REPO)} "
                            f"(entry missing or not an integer)")
        elif totals[key] > limit:
            failures.append(
                f"FAIL: {key} {totals[key]} > ratchet {limit}. New Python complies "
                f"immediately; see Rule 12 in docs/development/CODE_QUALITY.md.")
        elif totals[key] < limit:
            notes.append(f"  the {key} ratchet can be lowered to {totals[key]}")
    return failures, notes


def write_budget(totals: Counts) -> int:
    """Re-record the ratchets at the measured counts, refusing to raise one.

    Returns the exit status: 1 when some count has grown since the checked-in
    budget was written, in which case nothing is written at all.
    """
    previous = read_budget()
    raised = [key for key in RATCHETED
              if key in previous and totals[key] > previous[key]]
    if raised:
        print("REFUSED: --write-budget may only lower a ratchet; these rose: "
              + ", ".join(raised), file=sys.stderr)
        return 1
    width = max(len(key) for key in RATCHETED)
    lines = [
        "# Rule 12 ratchets - the Python idiom debt this tree still carries.",
        "# EVERY NUMBER MAY ONLY GO DOWN. Regenerate with",
        "#   python3 scripts/check_py_idiom.py --write-budget",
        "# which refuses to raise one. What each entry counts is in the gate's",
        "# docstring and in docs/development/CODE_QUALITY.md's Rule 12.",
        "",
    ]
    for key in RATCHETED:
        lines.append(f"{key.ljust(width)} = {totals[key]}")
    BUDGET.write_text("\n".join(lines) + "\n")
    print(f"wrote {BUDGET.relative_to(REPO)}")
    return 0


class _Tally:
    """A self-test's running PASS/FAIL count, printed one arm at a time.

    Calling it decides one arm: the name is printed with its verdict, and the
    detail is shown only on a failure, where it is the reason a reader needs.
    """

    def __init__(self) -> None:
        self.checks = 0
        self.failures = 0

    def __call__(self, name: str, ok: bool, detail: str = "") -> None:
        self.checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            self.failures += 1
            print(f"[FAIL] {name}" + (f": {detail}" if detail else ""))


def _count(src: str, key: str, rel: str = "x.py") -> int:
    """How many `key` findings one fixture source produces, judged as `rel`."""
    return scan(src, rel)[0][key]


def _selftest_refusals(ck: _Tally) -> None:
    """Arms for checks 1-6: each refused construct fires, its safe form does not."""
    ck("a bare except is a finding",
       _count("try:\n    f()\nexcept:\n    pass\n", "bare except") == 1)
    ck("a typed except is not a finding",
       _count("try:\n    f()\nexcept OSError:\n    pass\n", "bare except") == 0)
    ck("a mutable default list is a finding",
       _count("def f(x=[]):\n    return x\n", "mutable default argument") == 1)
    ck("a mutable default from a call is a finding",
       _count("def f(x=dict()):\n    return x\n", "mutable default argument") == 1,
       "dict() builds the same shared object [] does")
    ck("an immutable default is not a finding",
       _count("def f(x=()):\n    return x\n", "mutable default argument") == 0)
    ck("a None default is not a finding",
       _count("def f(x=None):\n    return x\n", "mutable default argument") == 0)
    ck("shell=True is a finding",
       _count("import subprocess\nsubprocess.run(c, shell=True)\n",
              "shell invocation") == 1)
    ck("os.system is a finding",
       _count("import os\nos.system('ls')\n", "shell invocation") == 1)
    ck("an argument-list subprocess call is not a finding",
       _count("import subprocess\nsubprocess.run(['ls', '-l'])\n",
              "shell invocation") == 0)
    ck("shadowing type is a finding",
       _count("type = 3\n", "shadowed builtin") == 1)
    ck("a parameter shadowing a builtin is a finding",
       _count("def f(list):\n    return list\n", "shadowed builtin") == 1)
    ck("an ordinary name is not a finding",
       _count("kind = 3\n", "shadowed builtin") == 0)
    ck("a dataclass field named for a protocol field is not a finding",
       _count("class Pdu:\n    type: int\n", "shadowed builtin") == 0,
       "a class body is not a scope any unqualified call resolves in")
    ck("a method named set is not a finding",
       _count("class Regs:\n    def set(self, k):\n        pass\n",
              "shadowed builtin") == 0)
    ck("a local inside a method still shadows",
       _count("class C:\n    def f(self):\n        type = 1\n        return type\n",
              "shadowed builtin") == 1,
       "the class body is skipped, its function bodies are not")
    ck("a wildcard import is a finding",
       _count("from something import *\n", "wildcard import") == 1)
    ck("a recorded wildcard exception is not a finding",
       _count("from migen import *\n", "wildcard import") == 0,
       "migen documents `from migen import *` as its usage")
    ck("eval on a non-literal is a finding",
       _count("eval(user_text)\n", "dynamic eval/exec") == 1)
    ck("eval on a literal is not a finding",
       _count("eval('1 + 1')\n", "dynamic eval/exec") == 0)
    ck("a file that does not parse is a finding, not a skip",
       _count("def (:\n", "unparseable source") == 1,
       "a skipped file reads as a clean one")


def _selftest_ratchets(ck: _Tally) -> None:
    """Arms for checks 7-15: each ratcheted construct is counted, and only it.

    Every arm here is a pair - the shape that must count, and the neighbouring
    shape that must not - because a check that only ever fires is as useless as
    one that never does.
    """
    long_body = "def f():\n" + "    x = 1\n" * (LONG_FUNCTION_LINES + 5)
    ck("a function over the line limit is a finding",
       _count(long_body, "long function") == 1)
    ck("a short function is not a finding",
       _count("def f():\n    return 1\n", "long function") == 0)
    ck("a module over the line limit is a finding",
       _count("x = 1\n" * (LONG_MODULE_LINES + 1), "long module") == 1)
    ck("an unannotated public function is a finding",
       _count("def f(a):\n    return a\n", "unannotated public function") == 1)
    ck("a fully annotated public function is not a finding",
       _count("def f(a: int) -> int:\n    return a\n",
              "unannotated public function") == 0)
    ck("a missing return annotation alone is a finding",
       _count("def f(a: int):\n    return a\n", "unannotated public function") == 1)
    ck("a private function owes no signature",
       _count("def _f(a):\n    return a\n", "unannotated public function") == 0,
       "the rule is about what crosses a module boundary")
    ck("self does not need an annotation",
       _count("class C:\n    def f(self) -> int:\n        return 1\n",
              "unannotated public function") == 0)
    ck("an undocumented public function is a finding",
       _count("def f() -> int:\n    return 1\n",
              "undocumented public function") == 1)
    ck("a documented public function is not a finding",
       _count('def f() -> int:\n    """Say what."""\n    return 1\n',
              "undocumented public function") == 0)
    ck("os.path is a finding",
       _count("import os\np = os.path.join(a, b)\n", "os.path use") == 1)
    ck("pathlib is not a finding",
       _count("from pathlib import Path\np = Path(a) / b\n", "os.path use") == 0)
    ck("an unmanaged open is a finding",
       _count("t = open(p).read()\n", "unmanaged open") == 1)
    ck("an open inside a with is not a finding",
       _count("with open(p) as fh:\n    t = fh.read()\n", "unmanaged open") == 0)
    ck("a nested open inside a with item is not a finding",
       _count("import contextlib\nwith contextlib.closing(open(p)) as fh:\n    pass\n",
              "unmanaged open") == 0,
       "the open is the with item's context expression, however it is wrapped")
    wide = "def f(" + ", ".join(f"a{i}" for i in range(MAX_PARAMETERS + 1)) + "):\n    pass\n"
    ck("a function over the parameter limit is a finding",
       _count(wide, "too many parameters") == 1)
    ck("a function at the parameter limit is not a finding",
       _count("def f(" + ", ".join(f"a{i}" for i in range(MAX_PARAMETERS)) + "):\n    pass\n",
              "too many parameters") == 0)
    ck("a global statement is a finding",
       _count("def f():\n    global X\n    X = 1\n", "global statement") == 1)
    ck("an over-long line is a finding",
       _count("x = '" + "a" * MAX_COLUMNS + "'\n", "over-long line") == 1)
    ck("a line at the limit is not a finding",
       _count("x = 1" + " " * (MAX_COLUMNS - 5) + "\n", "over-long line") == 0)


def _selftest_string_immunity(ck: _Tally) -> None:
    """The arm proving the scan reads the AST, so quoted text can never count."""
    ck("a construct quoted in a docstring is not a finding",
       _count('"""example: except: pass, and shell=True"""\n', "bare except") == 0,
       "the scan is AST-based, so a string cannot be a finding")


def _selftest_budget(ck: _Tally) -> None:
    """Arms for the ratchet verdict: over fails, equal passes, under is a note.

    The missing-entry arm is the one that matters most - an absent budget key
    must fail, never read as an unbounded allowance.
    """
    measured = dict.fromkeys(RATCHETED, 0)
    measured["long function"] = 2
    full = dict(measured)
    below = dict(full, **{"long function": 1})
    slack = dict(full, **{"long function": 3})
    ck("a count above its budget fails the ratchet", ratchet(measured, below)[0] != [])
    ck("a count equal to its budget passes with no note",
       ratchet(measured, full) == ([], []))
    ck("a count below its budget passes and names the lowerable value",
       ratchet(measured, slack)[0] == []
       and "lowered to 2" in ratchet(measured, slack)[1][0])
    ck("a missing budget entry fails the ratchet",
       ratchet(measured, {k: 0 for k in RATCHETED if k != "long module"})[0] != [],
       "an absent entry must never read as an unbounded allowance")
    ck("a malformed budget value is no entry", parse_budget("long function = many") == {})


def _selftest_live_tree(ck: _Tally) -> None:
    """Arms proving the scan really reaches this tree, and refuses a partial one.

    A gate that measures a smaller population than it claims reports fewer
    findings and ratchets to them, so the population is checked before any
    count taken from it is trusted.
    """
    paths = sources()
    ck("the scan reaches over 100 first-party modules", len(paths) > 100,
       f"found {len(paths)}")
    for sub in PROJECT_SUBMODULES:
        ck(f"the scan reaches {sub}", any(p.startswith(f"{sub}/") for p in paths))
    ck("the live population is complete", population_problem(paths) is None,
       str(population_problem(paths)))
    ck("an empty population is refused", population_problem([]) is not None)
    ck("a population missing a tree is refused",
       population_problem(["scripts/check_py_idiom.py"]) is not None,
       "a partial scan must never establish a smaller baseline")
    totals, _ = audit(paths)
    ck("the ratcheted populations are non-empty",
       any(totals[key] > 0 for key in RATCHETED),
       "an inert scan would report zero everywhere and ratchet to nothing")
    budget = read_budget()
    ck("the checked-in budget carries every ratcheted key",
       all(key in budget for key in RATCHETED),
       f"missing {[k for k in RATCHETED if k not in budget]}")


def selftest() -> int:
    """Run every fixture arm in order, print the tally, and return 1 on any FAIL.

    Each group below is one construct family the gate implements; the order is
    the order the report reads in, and no group depends on another having run.
    """
    ck = _Tally()
    _selftest_refusals(ck)
    _selftest_ratchets(ck)
    _selftest_string_immunity(ck)
    _selftest_budget(ck)
    _selftest_live_tree(ck)
    print(f"\n{ck.checks} checks: {ck.checks - ck.failures} PASS, {ck.failures} FAIL")
    return 1 if ck.failures else 0


def main() -> int:
    """The process exit status: 0 clean, 1 a finding, 2 a refused population."""
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
              f"first-party *.py in this repository and in "
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
                    f"Rule 12 in docs/development/CODE_QUALITY.md names what "
                    f"replaces it.")

    budget_failures, notes = ratchet(totals, read_budget())

    for line in findings + budget_failures:
        print(line, file=sys.stderr)
    if findings or budget_failures:
        return 1

    total_lines = sum(len((REPO / p).read_text(errors="replace").splitlines())
                      for p in paths)
    print(f"py idiom: {len(paths)} first-party modules, {total_lines} lines")
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
