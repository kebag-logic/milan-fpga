#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure control-flow shape: nesting, decisions, and priority decided by source order.

Why this exists. Rule 2 of the maintainability guide
(docs/development/CODE_QUALITY.md) asks for the simplest control flow that
makes state, priority, timing and error paths obvious. "Simplest" cannot be
argued from taste and must not be imported as a generic complexity limit from
some other codebase, so this tool measures THIS tree first and the guide quotes
what it found.

Two languages, two different questions:

  * Host code (Python only - the C++, Tcl and shell in the tree are not
    measured) - how deep does control flow nest inside one function, and how
    many decision points does a reader hold at once? Depth is the number of
    enclosing branch/loop/with/try constructs; an `elif` continues its chain
    and adds no level. Decisions counts `if`, `for`, `async for`, `while`,
    `match` and each of its `case` arms, exception handlers, boolean
    operators, conditional expressions, `assert`, and each `for` clause of a
    comprehension. Neither is a defect on its own; together they say how much
    of a function a reader must simulate to know what it does with a failure.

  * SystemVerilog - is priority VISIBLE? Inside one procedural block a signal
    written at a point that is NOT mutually exclusive with an earlier write to
    the same signal takes its value from source order: the last write wins.
    `x = 1; if (q) x = 2;` is that shape, and so is a write in one `if` that a
    later, separate `if` repeats. `if (a) x = 1; else x = 2;`, an `else if`
    chain, and a full `case` with one write per arm are NOT: their arms are
    exclusive, no source order is involved, and they are not reported. That
    ordering is real, legal and frequently correct - and invisible at the
    point of use, because nothing in the block says "this is the default and
    that is the override". The rule does not forbid it; it asks that the
    priority be visible in structure or named explicitly, so this tool lists
    where the ordering is load-bearing. Targets are followed into struct
    members (`s.f` is its own target and `s = '0` covers it) and through
    concatenations (`{a, b} = ...` writes both); a loop variable is not a
    signal; writes to different constant bits or slices of one vector are
    disjoint, while any variable index is taken to overlap.

The population is the first-party scope the guide declares: Python under the
directories in PY_DIRS below, and every procedural block (`always_ff`,
`always_comb`, `always_latch`, `always @`) in the `.sv` files under `hdl/`, in
this repository and in both project-owned processor submodules. A file that
does not parse or a block that does not close is NAMED on stderr and makes the
run exit 2: a partial population must never read as a smaller baseline.

Nothing here is a gate. There is no threshold, nothing in CI fails on these
numbers, and a high count is a question for review, not a defect.

Usage:
    python3 scripts/measure_control_flow.py             # both, ranked
    python3 scripts/measure_control_flow.py --python    # host code only
    python3 scripts/measure_control_flow.py --sv        # RTL only
    python3 scripts/measure_control_flow.py --json      # machine-readable
    python3 scripts/measure_control_flow.py --selftest  # fixture arms

Exit 0 when the whole population was measured, 2 when any file or block could
not be (each one is named on stderr), 1 when --selftest fails.
"""

import argparse
import ast
import itertools
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import PROJECT_SUBMODULES, tracked

#: Directory pathspecs, applied by the scope helper to the superproject and to
#: both processor submodules alike (a name absent from a tree matches nothing
#: there), then filtered on `.py`. Directories are used because a git pathspec
#: `x/**/*.py` needs at least one directory level and does not match `x/a.py`.
PY_DIRS = ("scripts", "sw", "tb", "harness", "syn", "hdl", "bench")
#: The RTL population: `.sv` under hdl/ in each tree. Testbench and synthesis
#: SystemVerilog under tb/ and syn/, `.svh` headers and the generated `.v`
#: wrapper are outside it, and the guide says so.
SV_DIRS = ("hdl",)

#: constructs that add a level of nesting a reader must hold
_NESTING = (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.Match,
            ast.AsyncFor, ast.AsyncWith)
#: constructs that add a decision point - the guide's definition sentence
#: enumerates exactly this tuple
_DECISION = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Match,
             ast.match_case, ast.ExceptHandler, ast.BoolOp, ast.IfExp,
             ast.Assert, ast.comprehension)


def tree_of(path):
    """Which of the three first-party trees a tracked path belongs to."""
    head = path.split("/", 1)[0]
    return head if head in PROJECT_SUBMODULES else "superproject"


TREES = ("superproject", *PROJECT_SUBMODULES)


# ---------------------------------------------------------------------------
# host code
# ---------------------------------------------------------------------------
#: a nested definition is measured as its own unit, so the enclosing function
#: does not inherit its depth or its decisions. Without this an orchestrator
#: that defines one small helper reads as deeply nested when it is not.
_OWN_UNIT = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


def _own_body(node):
    """Walk `node`, yielding every descendant that still belongs to it."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _OWN_UNIT):
            continue
        yield child
        yield from _own_body(child)


def _is_elif(parent, child):
    """Python stores `elif` as an If that is the sole statement of its parent
    If's `orelse`. It continues a flat chain, so it adds no level."""
    return (isinstance(parent, ast.If) and isinstance(child, ast.If)
            and len(parent.orelse) == 1 and parent.orelse[0] is child)


def _depth(node, level=0):
    deepest = level
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _OWN_UNIT):
            continue
        nests = isinstance(child, _NESTING) and not _is_elif(node, child)
        deepest = max(deepest, _depth(child, level + 1 if nests else level))
    return deepest


def measure_python_source(src):
    """Return one row per function defined in `src`."""
    rows = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        end = getattr(node, "end_lineno", None) or max(
            (getattr(c, "lineno", node.lineno) for c in ast.walk(node)), default=node.lineno)
        rows.append({
            "name": node.name,
            "line": node.lineno,
            "loc": end - node.lineno + 1,
            "depth": _depth(node),
            "decisions": sum(1 for c in _own_body(node) if isinstance(c, _DECISION)),
        })
    return rows


def python_population():
    return [p for p in tracked(*PY_DIRS) if p.endswith(".py")]


def measure_python_texts(items):
    """Measure (path, text) pairs. Returns (rows, skipped): a text that does
    not parse is reported in `skipped`, never silently dropped."""
    rows, skipped = [], []
    for rel, text in items:
        try:
            found = measure_python_source(text)
        except (SyntaxError, ValueError) as e:
            skipped.append(f"{rel}: {e.__class__.__name__}: {e}")
            continue
        for row in found:
            row["path"] = rel
            rows.append(row)
    rows.sort(key=lambda r: (-r["depth"], -r["decisions"]))
    return rows, skipped


def measure_python():
    return measure_python_texts(
        (rel, (REPO / rel).read_text(errors="replace")) for rel in python_population())


# ---------------------------------------------------------------------------
# SystemVerilog - where is priority decided by source order?
# ---------------------------------------------------------------------------
_SV_COMMENT_RE = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
_SV_TOKEN_RE = re.compile(r'''
    "(?:[^"\\]|\\.)*"                                   # string literal, one token
  | \d[\d_]*\s*'\s*[sS]?[bBoOdDhH]\s*[0-9a-fA-FxXzZ?_]+  # sized literal 4'b??10
  | '[sS]?[bBoOdDhH][0-9a-fA-FxXzZ?_]+                  # unsized literal 'h1F
  | '[01xXzZ]\b                                        # fill literal '0
  | [A-Za-z_`$][A-Za-z0-9_$]*                          # identifier, keyword, $task, `macro
  | \d[\d_]*(?:\.\d[\d_]*)?                            # number
  | <<<=|>>>=|<<=|>>=|\+\+|--|\+=|-=|\*=|/=|%=|&=|\|=|\^=
  | <=|>=|===|!==|==|!=|&&|\|\||->|::|\+:|-:
  | \S
''', re.X)
_SV_IDENT_RE = re.compile(r"[A-Za-z_]\w*$")
_SV_HEADERS = ("always", "always_ff", "always_comb", "always_latch")
_SV_ASSIGN_OPS = {"=", "<=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
                  "<<=", ">>=", "<<<=", ">>>="}
_SV_INCDEC = {"++", "--"}
_SV_OPEN = {"(", "[", "{"}
_SV_CLOSE = {")", "]", "}"}
#: reaching one of these while inside a block means the block never closed
_SV_MODULE_SCOPE = {"module", "endmodule", "initial", "final", "assign", "generate",
                    "endgenerate", "function", "endfunction", "task", "endtask",
                    "genvar", "localparam", "parameter", "interface", "endinterface",
                    "package", "endpackage", *_SV_HEADERS}
_SV_NESTS = {"begin", "case", "casez", "casex", "fork"}


class _SvSyntax(Exception):
    """A block this parser cannot close; the caller reports it, never drops it."""


def _sv_strip(text):
    def blank(m):
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))
    return _SV_COMMENT_RE.sub(blank, text)


def _sv_tokens(text):
    """Tokenize comment-stripped SystemVerilog into (tokens, line numbers)."""
    toks, lines, line, last = [], [], 1, 0
    for m in _SV_TOKEN_RE.finditer(text):
        line += text.count("\n", last, m.start())
        last = m.start()
        toks.append(m.group(0))
        lines.append(line)
    return toks, lines


def _index_set(toks):
    """The bits a constant index selects, or None when it is not constant."""
    ints = []
    for t in toks:
        if not re.fullmatch(r"\d[\d_]*", t):
            if t not in (":", "+:", "-:"):
                return None
            ints.append(t)
        else:
            ints.append(int(t.replace("_", "")))
    if len(ints) == 1 and isinstance(ints[0], int):
        return {ints[0]}
    if len(ints) == 3 and isinstance(ints[0], int) and isinstance(ints[2], int):
        a, op, b = ints
        if op == ":":
            return set(range(min(a, b), max(a, b) + 1))
        if op == "+:":
            return set(range(a, a + b))
        if op == "-:":
            return set(range(a - b + 1, a + 1))
    return None


class _SvTarget:
    """An assignment target as a path of (identifier, [index token lists])."""

    def __init__(self, segments):
        self.segments = segments
        self.name = ".".join(ident for ident, _ in segments)

    def overlaps(self, other):
        for (ident_a, idx_a), (ident_b, idx_b) in zip(self.segments, other.segments):
            if ident_a != ident_b:
                return False
            for ia, ib in zip(idx_a, idx_b):
                sa, sb = _index_set(ia), _index_set(ib)
                if sa is not None and sb is not None and not (sa & sb):
                    return False
        return True     # equal, or one is a prefix (a whole struct covers a member)


def _sv_target(toks, i):
    """Parse one target at toks[i]; returns ([_SvTarget], next index) or (None, i)."""
    if i < len(toks) and toks[i] == "{":
        found, i = [], i + 1
        while i < len(toks) and toks[i] != "}":
            sub, i = _sv_target(toks, i)
            if sub is None:
                return None, i
            found.extend(sub)
            if i < len(toks) and toks[i] == ",":
                i += 1
        return found, i + 1
    if i < len(toks) and _SV_IDENT_RE.match(toks[i]):
        segments = [(toks[i], [])]
        i += 1
        while i < len(toks):
            if toks[i] == "[":
                depth, i, start = 1, i + 1, i + 1
                while i < len(toks) and depth:
                    depth += (toks[i] == "[") - (toks[i] == "]")
                    i += 1
                segments[-1][1].append(toks[start:i - 1])
            elif toks[i] == "." and i + 1 < len(toks) and _SV_IDENT_RE.match(toks[i + 1]):
                segments.append((toks[i + 1], []))
                i += 2
            else:
                break
        return [_SvTarget(segments)], i
    return None, i


def _sv_assignment_targets(toks):
    """Targets written by one simple statement, or [] when it is not a write."""
    if toks and toks[0] in _SV_INCDEC:
        found, _ = _sv_target(toks, 1)
        return found or []
    found, i = _sv_target(toks, 0)
    if found and i < len(toks) and (toks[i] in _SV_ASSIGN_OPS or toks[i] in _SV_INCDEC):
        return found
    return []


class _SvStatements:
    """A recursive-descent reader of ONE procedural statement and what it nests.

    It knows just enough SystemVerilog to tell a branch arm from a sequence:
    `begin`/`end`, `if`/`else`, `case` items, the loop forms, immediate
    assertions and compiler directives. Everything else is a simple statement
    running to `;`, classified as a write when it starts with a target and an
    assignment operator."""

    def __init__(self, toks, lines, pos):
        self.toks, self.lines, self.pos = toks, lines, pos
        self.nest = self.max_nest = 0

    def peek(self, k=0):
        i = self.pos + k
        return self.toks[i] if i < len(self.toks) else None

    def take(self):
        if self.pos >= len(self.toks):
            raise _SvSyntax("block is not closed before the end of the file")
        self.pos += 1
        return self.toks[self.pos - 1]

    def expect(self, want):
        t = self.take()
        if t != want:
            raise _SvSyntax(f"expected `{want}`, found `{t}` on line {self.lines[self.pos - 1]}")

    def balanced(self, opener):
        """Consume a bracketed group starting at the current token; return its inside."""
        self.expect(opener)
        depth, start = 1, self.pos
        while depth:
            t = self.take()
            depth += (t in _SV_OPEN) - (t in _SV_CLOSE)
        return self.toks[start:self.pos - 1]

    def label(self):
        if self.peek() == ":" and self.peek(1) is not None and _SV_IDENT_RE.match(self.peek(1)):
            self.pos += 2

    def directives(self):
        while (t := self.peek()) is not None and t.startswith("`"):
            if t in ("`ifdef", "`ifndef", "`elsif", "`undef"):
                self.pos += 2
            elif t in ("`else", "`endif", "`resetall"):
                self.pos += 1
            else:                                   # `define, `include, a statement macro
                line = self.lines[self.pos]
                while self.peek() is not None and self.lines[self.pos] == line:
                    self.pos += 1

    def enter(self):
        self.nest += 1
        self.max_nest = max(self.max_nest, self.nest)

    def sequence(self, closers):
        body = []
        while True:
            self.directives()               # an `endif may sit right before the closer
            if self.peek() in closers:
                break
            if self.peek() is None:
                raise _SvSyntax(f"`{'/'.join(closers)}` never comes")
            body.append(self.statement())
        self.pos += 1
        return body

    def case_label(self):
        if self.peek() == "default":
            self.pos += 1
            if self.peek() == ":":
                self.pos += 1
            return
        depth = 0
        while True:
            t = self.take()
            if t in _SV_OPEN:
                depth += 1
            elif t in _SV_CLOSE:
                depth -= 1
            elif t == ":" and depth == 0:
                return
            elif t == "endcase":
                raise _SvSyntax(f"case item without `:` before line {self.lines[self.pos - 1]}")

    def simple(self):
        start, depth = self.pos, 0
        while True:
            t = self.take()
            if t in _SV_OPEN:
                depth += 1
            elif t in _SV_CLOSE:
                depth -= 1
            elif t == ";" and depth == 0:
                break
            elif t in _SV_MODULE_SCOPE and depth == 0:
                raise _SvSyntax(f"reached `{t}` on line {self.lines[self.pos - 1]} "
                                "inside a block that never closed")
        targets = _sv_assignment_targets(self.toks[start:self.pos - 1])
        return ("assign", targets) if targets else ("other",)

    def statement(self):
        self.directives()
        t = self.peek()
        if t is None:
            raise _SvSyntax("block is not closed before the end of the file")
        if t in ("unique", "unique0", "priority"):
            self.pos += 1
            t = self.peek()
        if t == "begin":
            self.pos += 1
            self.label()
            self.enter()
            body = self.sequence(("end",))
            self.nest -= 1
            self.label()
            return ("seq", body)
        if t == "fork":
            self.pos += 1
            self.label()
            self.enter()
            body = self.sequence(("join", "join_any", "join_none"))
            self.nest -= 1
            self.label()
            return ("seq", body)
        if t == "if":
            self.pos += 1
            self.balanced("(")
            then = self.statement()
            other = None
            if self.peek() == "else":
                self.pos += 1
                other = self.statement()
            return ("if", then, other)
        if t in ("case", "casez", "casex"):
            self.pos += 1
            self.balanced("(")
            if self.peek() in ("inside", "matches"):
                self.pos += 1
            self.enter()
            arms = []
            while True:
                self.directives()
                if self.peek() == "endcase":
                    break
                if self.peek() is None:
                    raise _SvSyntax("`case` without `endcase`")
                self.case_label()
                arms.append(self.statement())
            self.pos += 1
            self.nest -= 1
            return ("case", arms)
        if t in ("for", "foreach", "while", "repeat"):
            # the header is one bracketed group, never a statement: `i = 0`
            # and `i++` in it are the loop variable, not a signal written twice
            self.pos += 1
            self.balanced("(")
            return ("loop", self.statement())
        if t == "forever":
            self.pos += 1
            return ("loop", self.statement())
        if t == "do":
            self.pos += 1
            body = self.statement()
            self.expect("while")
            self.balanced("(")
            self.expect(";")
            return ("loop", body)
        if t in ("assert", "assume", "cover"):
            self.pos += 1
            if self.peek() in ("property", "final"):
                self.pos += 1
            self.balanced("(")
            body = []
            if self.peek() == ";":
                self.pos += 1
            elif self.peek() != "else":
                body.append(self.statement())
            if self.peek() == "else":
                self.pos += 1
                body.append(self.statement())
            return ("seq", body)
        if t == ";":
            self.pos += 1
            return ("seq", [])
        if t in ("end", "endcase", "else", "join", "join_any", "join_none") or t in _SV_MODULE_SCOPE:
            raise _SvSyntax(f"unexpected `{t}` on line {self.lines[self.pos]}")
        return self.simple()


def _sv_exclusive(path_a, path_b):
    """Two writes are mutually exclusive when they sit in different arms of one branch."""
    for (branch_a, arm_a), (branch_b, arm_b) in zip(path_a, path_b):
        if branch_a != branch_b:
            return False        # diverged into sibling branches: both can run
        if arm_a != arm_b:
            return True
    return False                # one encloses the other, or both at one level


def _sv_order_dependent(stmt):
    """Names written at a point not exclusive with an earlier write they overlap."""
    seen, flagged, ids = [], set(), itertools.count()

    def walk(node, path):
        kind = node[0]
        if kind == "seq":
            for s in node[1]:
                walk(s, path)
        elif kind == "if":
            branch = next(ids)
            walk(node[1], path + ((branch, 0),))
            if node[2] is not None:
                walk(node[2], path + ((branch, 1),))
        elif kind == "case":
            branch = next(ids)
            for arm, body in enumerate(node[1]):
                walk(body, path + ((branch, arm),))
        elif kind == "loop":
            walk(node[1], path)
        elif kind == "assign":
            for target in node[1]:
                if any(target.overlaps(prev) and not _sv_exclusive(prev_path, path)
                       for prev, prev_path in seen):
                    flagged.add(target.name)
                seen.append((target, path))

    walk(stmt, ())
    return sorted(flagged)


def _sv_blocks(text):
    """Every procedural block in `text`: (kind, name, line, loc, depth, stmt),
    plus the blocks that could not be closed as (line, reason)."""
    toks, lines = _sv_tokens(_sv_strip(text))
    blocks, problems = [], []
    for i, kind in enumerate(toks):
        if kind not in _SV_HEADERS:
            continue
        reader = _SvStatements(toks, lines, i + 1)
        try:
            if reader.peek() == "@":
                reader.pos += 1
                if reader.peek() == "*":
                    reader.pos += 1
                else:
                    reader.balanced("(")
            name = None
            if reader.peek() == "begin" and reader.peek(1) == ":" and reader.peek(2):
                name = reader.peek(2)
            outer = reader.peek() in _SV_NESTS
            stmt = reader.statement()
        except _SvSyntax as e:
            problems.append((lines[i], str(e)))
            continue
        depth = reader.max_nest - (1 if outer else 0)
        blocks.append((kind, name or f"line{lines[i]}", lines[i],
                       lines[reader.pos - 1] - lines[i] + 1, depth, stmt))
    return blocks, problems


def measure_sv_source(text):
    """Return (one row per procedural block, [(line, reason)] for unclosed ones)."""
    rows = []
    blocks, problems = _sv_blocks(text)
    for kind, name, line, loc, depth, stmt in blocks:
        rows.append({
            "block": name,
            "kind": kind,
            "line": line,
            "loc": loc,
            "depth": depth,
            "order_dependent": _sv_order_dependent(stmt),
        })
    return rows, problems


def sv_population():
    return [p for p in tracked(*SV_DIRS) if p.endswith(".sv")]


def measure_sv_texts(items):
    """Measure (path, text) pairs. Returns (rows, skipped) - an unclosed block
    is reported in `skipped` with its line, never silently dropped."""
    rows, skipped = [], []
    for rel, text in items:
        found, problems = measure_sv_source(text)
        skipped.extend(f"{rel}:{line}: {why}" for line, why in problems)
        for row in found:
            row["path"] = rel
            rows.append(row)
    rows.sort(key=lambda r: (-len(r["order_dependent"]), -r["depth"], -r["loc"]))
    return rows, skipped


def measure_sv():
    return measure_sv_texts(
        (rel, (REPO / rel).read_text(errors="replace")) for rel in sv_population())


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------
PY_FIXTURES = [
    ("flat function is depth 0", "def f():\n    return 1\n", 0, 0),
    ("one if is depth 1", "def f(a):\n    if a:\n        return 1\n    return 0\n", 1, 1),
    ("sibling ifs do not stack", "def f(a):\n    if a:\n        pass\n    if a:\n        pass\n", 1, 2),
    ("nested if/for stacks", "def f(a):\n    if a:\n        for i in a:\n            if i:\n                pass\n", 3, 3),
    ("a flat elif chain is depth 1",
     "def f(r):\n    if r == 0:\n        pass\n    elif r == 1:\n        pass\n    elif r == 2:\n"
     "        pass\n    elif r == 3:\n        pass\n    elif r == 4:\n        pass\n", 1, 5),
    ("an elif arm's body still nests inside the chain",
     "def f(a):\n    if a:\n        pass\n    elif a:\n        for i in a:\n            pass\n", 2, 3),
    ("try/except counts the handler",
     "def f():\n    try:\n        pass\n    except ValueError:\n        pass\n", 1, 1),
    ("boolean operators are decisions", "def f(a, b):\n    return a and b\n", 0, 1),
    ("assert is a decision", "def f(a):\n    assert a\n", 0, 1),
    ("each for clause of a comprehension is a decision",
     "def f(a):\n    return [x for x in a for y in x]\n", 0, 2),
    ("async for nests and decides like for",
     "async def f(a):\n    async for x in a:\n        pass\n", 1, 1),
    ("a nested def is measured on its own",
     "def outer():\n    def inner(a):\n        if a:\n            pass\n    return inner\n", 0, 0),
    ("match cases are visible control flow",
     "def f(x):\n    match x:\n        case 0: return 0\n        case _: return 1\n", 1, 3),
]

SV_FIXTURES = [
    ("single assignment has no implicit priority",
     "always_comb begin : b  x_w = 1; end", []),
    ("a default then a narrower override is order dependent",
     "always_comb begin : b  x_w = 1; if (q) x_w = 2; end", ["x_w"]),
    ("default-then-override in a case is order dependent",
     "always_comb begin : b  y_w = 0; case (s) 2'd1: y_w = 1; endcase end", ["y_w"]),
    ("a write after a case that also wrote it is order dependent",
     "always_comb begin : b  case (s) 2'd0: y_w = 1; default: y_w = 0; endcase if (k) y_w = 2; end",
     ["y_w"]),
    ("two sibling ifs are not exclusive",
     "always_comb begin : b  if (a) x_w = 1; if (q) x_w = 2; end", ["x_w"]),
    ("an if/else pair is exclusive",
     "always_comb begin : b  if (a) x_w = 1; else x_w = 2; end", []),
    ("a full case with one write per arm is exclusive",
     "always_comb begin : b  case (s) 2'd0: y_w = 1; 2'd1: y_w = 2; default: y_w = 0; endcase end", []),
    ("an else-if chain is exclusive",
     "always_ff @(posedge c) begin : b  if (a) x_r <= 1; else if (b) x_r <= 2; else x_r <= 3; end", []),
    ("reset then else is exclusive",
     "always_ff @(posedge c) begin : b  if (!rst_n) x_r <= 0; else x_r <= y; end", []),
    ("two different signals are not order dependent",
     "always_comb begin : b  x_w = 1; y_w = 2; end", []),
    ("a comparison is not an assignment",
     "always_comb begin : b  x_w = (a == b); end", []),
    ("a comparison on a continuation line is not an assignment",
     "always_comb begin : b  if (a &&\n cnt <= 5) x_w = 1; end", []),
    ("a loop variable is not a signal, however many loops step it",
     "always_comb begin : b  for (int i = 0; i < 4; i = i + 1) y_w[i] = 0;"
     " for (int i = 0; i < 4; i = i + 1) z_w[i] = 0; end", []),
    ("a loop variable stepped with ++ is not a signal",
     "always_comb begin : b  for (int unsigned s = 0; s < 4; s++) begin y_w[s] = 0; end"
     " for (int unsigned s = 0; s < 4; s++) begin z_w[s] = 0; end end", []),
    ("a struct member is a target of its own",
     "always_comb begin : b  s.f = 1; s.f = 2; end", ["s.f"]),
    ("a whole-struct default then a member override is order dependent",
     "always_comb begin : b  s = '0; if (q) s.f = 1; end", ["s.f"]),
    ("two members of one struct are different targets",
     "always_comb begin : b  s.f = 1; s.g = 2; end", []),
    ("a concatenation writes each of its elements",
     "always_comb begin : b  {a_w, b_w} = 2'b00; {a_w, b_w} = 2'b11; end", ["a_w", "b_w"]),
    ("a concatenation element re-written alone is order dependent",
     "always_comb begin : b  {a_w, b_w} = 2'b00; if (q) b_w = 1; end", ["b_w"]),
    ("writes to different constant bits are disjoint",
     "always_comb begin : b  x_w[0] = 1; x_w[1] = 1; x_w[7:4] = 0; end", []),
    ("writes to overlapping slices are order dependent",
     "always_comb begin : b  x_w[7:0] = 1; x_w[3] = 1; end", ["x_w"]),
    ("a variable index may overlap anything",
     "always_comb begin : b  x_w[i] = 1; x_w[0] = 1; end", ["x_w"]),
    ("a block without begin is measured",
     "always_ff @(posedge c) if (rst) begin x_r <= 0; end else begin x_r <= 1; x_r <= 2; end", ["x_r"]),
    ("a begin inside a string does not unbalance the block",
     'always_comb begin : b  $display("begin"); x_w = 1; x_w = 2; end', ["x_w"]),
    ("a compiler directive right before the closing end does not unbalance the block",
     "always_ff @(posedge c) begin : b  x_r <= 1;\n`ifndef SYNTHESIS\n  y_r <= 1;\n`endif\nend", []),
]

#: one block per header form the tree uses; the census must find every one
SV_HEADER_FORMS = """
always_ff @(posedge c) begin : a  x_r <= 1; end
always_ff @(posedge c) if (r) x_r <= 0; else x_r <= 1;
always_comb for (int i = 0; i < 2; i++) y_w[i] = 0;
always_comb z_w = 1;
always @(posedge c) begin : e  w_r <= 1; end
always @* v_w = 2;
always_latch if (en) q_r = d;
"""


def _arm(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f": {detail}"))
    return 0 if ok else 1


def selftest():
    failures = 0
    for name, src, want_depth, want_dec in PY_FIXTURES:
        rows = measure_python_source(src)
        row = next(r for r in rows if r["name"] in ("f", "outer"))
        failures += _arm(f"python: {name}",
                         row["depth"] == want_depth and row["decisions"] == want_dec,
                         f"got depth {row['depth']} decisions {row['decisions']}, "
                         f"want {want_depth}/{want_dec}")

    # the nested-def arm also proves the inner function is reported separately
    src = next(s for n, s, _, _ in PY_FIXTURES if n.startswith("a nested def"))
    inner = [r for r in measure_python_source(src) if r["name"] == "inner"]
    failures += _arm("python: inner function reported with its own depth",
                     len(inner) == 1 and inner[0]["depth"] == 1, str(inner))

    rows, skipped = measure_python_texts([("bad.py", "def (:\n"), ("ok.py", "def f():\n    pass\n")])
    failures += _arm("python: an unparsable file is reported, not dropped",
                     len(skipped) == 1 and skipped[0].startswith("bad.py:") and len(rows) == 1,
                     f"rows {rows} skipped {skipped}")

    for name, src, want in SV_FIXTURES:
        rows, problems = measure_sv_source(src)
        got = rows[0]["order_dependent"] if rows else problems
        failures += _arm(f"sv: {name}", bool(rows) and not problems and got == want,
                         f"got {got}, want {want}")

    # nesting inside a procedural block, including case
    # depth is measured INSIDE the block: the block's own `begin` is the block,
    # so `if (q) begin case (...) ... endcase end` nests two levels, not three.
    rows, _ = measure_sv_source(
        "always_ff @(posedge c) begin : b if (q) begin case (s) 2'd0: x_r <= 1; endcase end end")
    failures += _arm("sv: begin/case nesting is counted inside the block",
                     rows[0]["depth"] == 2, f"got {rows[0]['depth']}, want 2")

    rows, problems = measure_sv_source(SV_HEADER_FORMS)
    names = [r["block"] for r in rows]
    failures += _arm("sv: every always header form opens a block, with or without begin",
                     len(rows) == 7 and not problems and names[0] == "a" and names[4] == "e"
                     and [r["kind"] for r in rows][4:6] == ["always", "always"],
                     f"blocks {names} problems {problems}")

    rows, problems = measure_sv_source(
        "always_ff @(posedge c) begin : a  begin x_r <= 1; end\n"
        "always_comb begin : b  y_w = 1; end\n")
    failures += _arm("sv: an unclosed block is reported by line, and the next block is still measured",
                     len(problems) == 1 and problems[0][0] == 1 and [r["block"] for r in rows] == ["b"],
                     f"rows {[r['block'] for r in rows]} problems {problems}")

    # the population arms need the pinned tree: the scan must reach both
    # processors' Python, or the guide's "first-party" number is a smaller one
    population = python_population()
    for sub in PROJECT_SUBMODULES:
        n = sum(1 for p in population if p.startswith(sub + "/"))
        failures += _arm(f"population: {sub} contributes Python files to the scan",
                         n > 0, f"{sub} contributes {n} .py files")

    total = (len(PY_FIXTURES) + 2 + len(SV_FIXTURES) + 3 + len(PROJECT_SUBMODULES))
    print(f"\n{total} checks: {total - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def _per_tree(rows, deep):
    for tree in TREES:
        mine = [r for r in rows if tree_of(r["path"]) == tree]
        print(f"  {tree}: {len(mine)} {deep(mine)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--python", action="store_true", help="host code only")
    ap.add_argument("--sv", action="store_true", help="RTL only")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    ap.add_argument("--top", type=int, default=15, help="rows per table (default 15)")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    want_py = args.python or not args.sv
    want_sv = args.sv or not args.python
    out, skipped = {}, []

    if want_py:
        rows, skip = measure_python()
        out["python"] = rows
        skipped += skip
        if not args.json:
            print(f"{'path:line':<58}{'function':<34}{'loc':>6}{'depth':>7}{'decisions':>11}")
            for r in rows[: args.top]:
                where = f"{r['path']}:{r['line']}"
                print(f"{where:<58}{r['name'][:33]:<34}{r['loc']:>6}{r['depth']:>7}{r['decisions']:>11}")
            deep = sum(1 for r in rows if r["depth"] >= 5)
            print(f"\n{len(rows)} first-party function(s); {deep} nest five levels or deeper"
                  + (f"; {len(skip)} file(s) NOT measured" if skip else ""))
            _per_tree(rows, lambda m: f"function(s), {sum(1 for r in m if r['depth'] >= 5)} "
                                      "at depth 5 or more")
            print()

    if want_sv:
        rows, skip = measure_sv()
        out["sv"] = rows
        skipped += skip
        if not args.json:
            print(f"{'path:line':<58}{'block':<28}{'depth':>7}{'order-dependent signals':>26}")
            for r in rows[: args.top]:
                where = f"{r['path']}:{r['line']}"
                print(f"{where:<58}{r['block'][:27]:<28}{r['depth']:>7}{len(r['order_dependent']):>26}")
            ordered = sum(1 for r in rows if r["order_dependent"])
            print(f"\n{len(rows)} procedural block(s); {ordered} resolve at least one signal "
                  f"by source order" + (f"; {len(skip)} block(s) NOT measured" if skip else ""))
            _per_tree(rows, lambda m: f"block(s), {sum(1 for r in m if r['order_dependent'])} "
                                      "resolve a signal by source order")

    if args.json:
        out["skipped"] = skipped
        print(json.dumps(out, indent=2))
    for s in skipped:
        print(f"[SKIP] {s}", file=sys.stderr)
    if skipped:
        print(f"[SKIP] {len(skipped)} file(s) or block(s) could not be measured: the "
              "population is incomplete and these numbers are not a baseline", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
