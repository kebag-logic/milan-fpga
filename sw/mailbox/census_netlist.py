# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_netlist.py - the datapath read the way publication_census.py reads it.

Comments and strings blanked, the text is cut into statements, a statement
into its assignments, and each assignment into its targets and its reads.
For every read the reader records what its statement can drive (every target
of a procedural block it lies in, the instance port of a named connection);
it records the place of every assignment target and every declared name, and
the place of every name. A place in none of these, or a read inside a
function, task, property or sequence declaration or inside a call's
arguments, is one the census cannot classify. publication_census.py's
docstring states the rule this serves.
"""

from __future__ import annotations

import bisect
import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field

KEYWORDS = frozenset("""
    assign wire logic reg begin end else if for case casez casex unique unique0 priority endcase default
    always always_comb always_ff always_latch posedge negedge or and generate endgenerate genvar localparam
    parameter input output inout signed unsigned int integer automatic function endfunction return initial
    typedef struct packed enum foreach while do module endmodule import export bit byte shortint longint
    string var const static""".split())
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*)*")
#: Every occurrence of a name, whatever stands before it: a '.' (an implicit
#: .name port, a member, a hierarchical path) or a '`' included.
TOKEN = re.compile(r"(?<![A-Za-z0-9_$])[A-Za-z_][A-Za-z0-9_$]*")
RETURN = re.compile(r"(?<![A-Za-z0-9_$])return(?![A-Za-z0-9_$])")
#: A based literal's digits, whose '?' and 'h' are no operator or name.
BASED = re.compile(r"'[sS]?[bBoOdDhH]\s*[0-9a-fA-FxXzZ?_]+")
#: A call: a function, task, system function or macro name, scoped or not, and its '('.
CALL = re.compile(r"(?<![A-Za-z0-9_$.'])[`$]?([A-Za-z_][\w$]*)(?:\s*(?:\.|::)\s*[A-Za-z_][\w$]*)*\s*\(")
#: Words before a '(' that call nothing.
NOT_CALLS = frozenset("""
    repeat wait iff assert assume cover expect property sequence posedge negedge edge or and not inside dist
    with type disable fork matches""".split())
#: The subroutines and assertion declarations whose bodies the census does not follow, each with its closing word.
SUBROUTINE = re.compile(r"\b(function|task|endfunction|endtask|endproperty|endsequence)\b"
                        r"|\b(property|sequence)(?=\s+[A-Za-z_])")
#: What may stand before a statement's own text: block keywords and labels, and preprocessor directive lines.
LEAD = re.compile(r"\s*(?:(?:begin|end|endcase|endfunction|endtask|endgenerate|else|generate)\b(?:\s*:\s*\w+)?"
                  r"|`\w+[^\n]*)")
LEAD_COND = re.compile(r"\s*(if|for)\s*\(")
INST_TYPE = re.compile(r"\s*([A-Za-z_]\w*)\s*(#\s*\()?")
INST_NAME = re.compile(r"\s*([A-Za-z_]\w*)\s*\(")
CONTROL = re.compile(r"\b(if|case|casez|casex|for|while)\s*\(")
OUTPUT_DECL = re.compile(r"\boutput\s+(?:wire\s+|logic\s+|reg\s+)?(?:signed\s+)?(?:\[[^\]]*\]\s*)*(\w+)")
DECL = re.compile(r"\s*(?:wire|logic|reg|var|tri|uwire)\b(?:\s+(?:logic|reg|wire)\b)?(?:\s+(?:signed|unsigned)\b)?")


class CensusError(ValueError):
    """The datapath could not be read the way the census reads it."""


@functools.lru_cache(maxsize=32)
def strip_comments(text: str) -> str:
    """The text with comments and string bodies blanked, its length and newlines kept."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(c if c == "\n" else " " for c in text[i:j]))
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            j = min(n, j + 1)
            out.append('"' + " " * max(0, j - i - 2) + ('"' if j - i >= 2 else ""))
        else:
            j = i + 1
            out.append(text[i])
        i = j
    return "".join(out)


def close_of(text: str, i: int) -> int:
    """The index just past the bracket group that opens at text[i]."""
    depth = 0
    for j in range(i, len(text)):
        if text[j] in "([{":
            depth += 1
        elif text[j] in ")]}":
            depth -= 1
            if depth == 0:
                return j + 1
    raise CensusError(f"an unbalanced bracket group opens at offset {i}")


def statements(code: str) -> list[tuple[int, int]]:
    """(start, end) of every statement: text up to a ';' outside brackets."""
    out, depth, start = [], 0, 0
    for i, c in enumerate(code):
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == ";" and depth == 0:
            out.append((start, i))
            start = i + 1
    if depth:
        raise CensusError("the datapath's brackets do not balance")
    return out


def top_level(text: str) -> list[tuple[int, int]]:
    """(start, end) of each comma-separated item of text, split outside brackets."""
    out, depth, start = [], 0, 0
    for i, c in enumerate(text + ","):
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == "," and depth == 0:
            out.append((start, i))
            start = i + 1
    return out


def lead_of(text: str) -> int:
    """Where a statement's own text starts: past block keywords, labels,
    directive lines and the conditions of a generate if or for."""
    at = 0
    while True:
        m = LEAD.match(text, at)
        if m:
            at = m.end()
            continue
        m = LEAD_COND.match(text, at)
        if m:
            at = close_of(text, m.end() - 1)
            continue
        return at


def label_end(text: str) -> int:
    """Where a statement's own text starts past its last label: a case item's
    expressions or default, a statement or block label, each ending in a ':'
    outside brackets that no '?' pairs with (a based literal's '?' digits and
    the '?' of ==? and !=? are no conditional operator)."""
    code = BASED.sub(lambda m: " " * len(m.group()), text)
    depth, pending, end = 0, 0, 0
    for i, c in enumerate(code):
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif depth or c not in "?:":
            continue
        elif c == "?":
            pending += code[i - 1:i] != "="
        elif ":" in (code[i - 1:i], code[i + 1:i + 2]) or code[i + 1:i + 2] in ("=", "/"):
            continue                      # '::', ':=', ':/'
        elif pending:
            pending -= 1
        else:
            end = i + 1
    return end


def assignment(text: str) -> tuple[int, int] | None:
    """(offset, length) of a statement's '=' or '<=' outside brackets, past
    its labels (a case item's `a <= b:` is no assignment). None when a
    `return` comes first: its '<=' compares."""
    depth = 0
    for i in range(label_end(text), len(text)):
        c = text[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif depth == 0 and c == "r" and RETURN.match(text, i):
            return None
        elif depth == 0 and c == "=":
            prev = text[i - 1] if i else " "
            if text[i + 1:i + 2] == "=" or prev in "=!>":
                continue
            if prev == "<":
                if text[i - 2:i - 1] == "<":
                    continue
                return i - 1, 2
            return i, 1
    return None


def opening(text: str, k: int) -> int:
    """The index of the bracket that the bracket at text[k - 1] closes."""
    depth = 0
    for m in range(k - 1, -1, -1):
        depth += {")": 1, "]": 1, "}": 1, "(": -1, "[": -1, "{": -1}.get(text[m], 0)
        if depth == 0:
            return m
    raise CensusError(f"an unbalanced bracket group closes at offset {k - 1}")


def lvalue_at(lhs: str) -> tuple[list[tuple[str, int]], int]:
    """Each signal a left-hand side drives with its offset in lhs (a
    concatenation's items each, never a name in an index), and where the
    left-hand side starts."""
    k = len(lhs.rstrip())
    while k and lhs[k - 1] == "]":
        k = len(lhs[:opening(lhs, k)].rstrip())
    if k and lhs[k - 1] == "}":
        m = opening(lhs, k)
        out = []
        for a, b in top_level(lhs[m + 1:k - 1]):
            out += [(n, m + 1 + a + at) for n, at in lvalue_at(lhs[m + 1 + a:m + 1 + b])[0]]
        return out, m
    m = k
    while m and (lhs[m - 1].isalnum() or lhs[m - 1] in "_$."):
        m -= 1
    name = lhs[m:k]
    return ([(name, m)] if name and name not in KEYWORDS else []), m


def lvalues(lhs: str) -> tuple[list[str], int]:
    """The signals a left-hand side drives, and where it starts in it."""
    found, start = lvalue_at(lhs)
    return [n for n, _ in found], start


def reads(text: str, base: int) -> list[tuple[int, str]]:
    """Every signal named in text, at its absolute offset; literals' base
    letters and system names are not signals, and a.b reads a."""
    out = []
    for m in IDENT.finditer(text):
        name = m.group()
        before = text[m.start() - 1] if m.start() else " "
        if name in KEYWORDS or before in "'$`":
            continue
        out.append((base + m.start(), name.split(".")[0]))
    return out


@dataclass
class Netlist:
    """The datapath as statements: who reads what, and where it ends.

    ``reads_at`` keys each read by the signal its own statement drives, which
    names a population read's row. ``drives`` maps the offset of each read to
    every signal its statement can drive, or inside a procedural block every
    signal the block drives; ``edges`` is the same by name. An offset in
    neither ``drives``, ``targets_at`` nor ``declared_at`` is an occurrence
    the census cannot classify.
    """

    code: str
    stmts: list[tuple[int, int]]
    edges: dict[str, set[str]]
    reads_at: list[tuple[int, str, str]]
    instances: dict[str, set[str]]
    bodies: dict[str, tuple[int, str]]
    outputs: set[str]
    newlines: list[int]
    drives: dict[int, frozenset[str]] = field(default_factory=dict)
    targets_at: set[int] = field(default_factory=set)
    declared_at: set[int] = field(default_factory=set)
    tokens: dict[str, list[int]] = field(default_factory=dict)
    subs: list[tuple[int, int]] = field(default_factory=list)

    def in_sub(self, pos: int) -> bool:
        """Whether an offset lies inside a function, task, property or sequence declaration."""
        return any(a <= pos < b for a, b in self.subs)

    def line(self, pos: int) -> int:
        """The 1-based source line of a character offset."""
        return bisect.bisect_right(self.newlines, pos)

    def text_at(self, pos: int) -> str:
        """The source line holding a character offset, its comments blanked."""
        n = self.line(pos)
        end = self.newlines[n] - 1 if n < len(self.newlines) else len(self.code)
        return " ".join(self.code[self.newlines[n - 1]:end].split())[:100]


def always_blocks(code: str, stmts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """The extent of every procedural block (always, initial, final): its
    begin to the matching end, or one statement."""
    toks = [(m.start(), m.group()) for m in re.finditer(
        r"\b(begin|end|always_comb|always_ff|always_latch|always|initial|final)\b", code)]
    out, i = [], 0
    while i < len(toks):
        pos, word = toks[i]
        if word not in ("begin", "end"):
            ev = re.match(r"\s*(@\s*(\([^)]*\)|\*))?\s*", code[pos + len(word):])
            body = pos + len(word) + ev.end()
            if code.startswith("begin", body):
                depth, j = 0, i + 1
                while j < len(toks):
                    depth += {"begin": 1, "end": -1}.get(toks[j][1], 0)
                    if depth == 0:
                        break
                    j += 1
                out.append((pos, toks[j][0] + 3))
                i = j
            else:
                out.append((pos, next(e for s, e in stmts if e > body)))
        i += 1
    return out


def subroutines(code: str) -> list[tuple[int, int]]:
    """The extent of every function, task, property and sequence
    declaration, from its keyword to the end of its closing keyword."""
    out, opened = [], None
    for m in SUBROUTINE.finditer(code):
        word = m.group()
        if not word.startswith("end"):
            if opened is not None:
                raise CensusError(f"a {word} opens at line {code.count(chr(10), 0, m.start()) + 1} inside "
                                  f"the {opened[1]} opened before it")
            opened = (m.start(), word)
        elif opened is None or word != "end" + opened[1]:
            raise CensusError(f"an {word} at line {code.count(chr(10), 0, m.start()) + 1} closes no "
                              f"{word[3:]}")
        else:
            out.append((opened[0], m.end()))
            opened = None
    if opened is not None:
        raise CensusError(f"the {opened[1]} opened at line {code.count(chr(10), 0, opened[0]) + 1} never closes")
    return out


def assignments(code: str, s: int, e: int) -> list[tuple[int, int, tuple[int, int]]]:
    """(start, end, (offset, length) of its '=' or '<=') of each assignment
    in the statement code[s:e]. An expression holds no comma outside
    brackets, so one after the first '=' starts another assignment of the
    same list (`assign a = x, b = y`, `wire a = x, b = y`)."""
    op = assignment(code[s:e])
    if op is None:
        return []
    rest = s + op[0] + op[1]
    cuts = [rest + b for _, b in top_level(code[rest:e])][:-1]
    out = []
    for a, b in zip([s] + [c + 1 for c in cuts], cuts + [e]):
        o = assignment(code[a:b])
        if o is not None:
            out.append((a, b, o))
    return out


def calls(text: str, base: int) -> list[tuple[int, int]]:
    """The extent of every call's parentheses in text, at absolute offsets:
    a function's, a task's, a system function's or a macro's."""
    out = []
    for c in CALL.finditer(text):
        if c.group().startswith(("`", "$")) or c.group(1) not in KEYWORDS | NOT_CALLS:
            out.append((base + c.end() - 1, base + close_of(text, c.end() - 1)))
    return out


def instance(code: str, s: int, e: int) -> tuple[str, str, tuple[int, str], list[tuple[int, str, str, list]]] | None:
    """The module instance the statement code[s:e] makes, if it makes one:
    (its name, its module, (offset, text) of its port list, and every read of
    a named port connection, whatever the port is called, as (offset, name,
    instance.port, the call extents of that connection))."""
    off = s + lead_of(code[s:e])
    lead = code[off:e]
    m = INST_TYPE.match(lead)
    if not m or m.group(1) in KEYWORDS:
        return None
    j = close_of(lead, m.end() - 1) if m.group(2) else m.end()
    n = INST_NAME.match(lead, j)
    if not n or n.group(1) in KEYWORDS:
        return None
    open_at = n.end() - 1
    body = lead[open_at + 1:close_of(lead, open_at) - 1]
    got = []
    for c in re.finditer(r"\.\s*(\w+)\s*\(", body):
        a = c.end() - 1
        expr, base = body[a + 1:close_of(body, a) - 1], off + open_at + 1 + a + 1
        spans = calls(expr, base)
        got += [(pos, name, f"{n.group(1)}.{c.group(1)}", spans) for pos, name in reads(expr, base)]
    return n.group(1), m.group(1), (off + open_at + 1, body), got


def netlist(text: str) -> Netlist:
    """Read the datapath into statements, instances, reads and what each read drives."""
    code = strip_comments(text)
    stmts = statements(code)
    blocks = always_blocks(code, stmts)
    subs = subroutines(code)
    edges: dict[str, set[str]] = defaultdict(set)
    reads_at: list[tuple[int, str, str]] = []
    instances: dict[str, set[str]] = defaultdict(set)
    bodies: dict[str, tuple[int, str]] = {}
    drives: dict[int, frozenset[str]] = {}
    targets_at: set[int] = set()
    block_targets: dict[tuple[int, int], set[str]] = defaultdict(set)
    block_ctrl: dict[tuple[int, int], list[tuple[int, str]]] = defaultdict(list)
    block_reads: dict[tuple[int, int], list[tuple[int, list[tuple[int, int]]]]] = defaultdict(list)

    def read(pos: int, name: str, consumer: str) -> None:
        """Record that `consumer` reads `name` at offset `pos`."""
        reads_at.append((pos, name, consumer))

    def drive(pos: int, consumers: set[str], spans: list[tuple[int, int]]) -> None:
        """What the read at `pos` can drive. A read inside a call's arguments
        or inside a subroutine drives nothing the census follows: the census
        does not see what a subroutine or macro does with it."""
        if consumers and not any(a <= pos < b for a, b in subs + spans):
            drives[pos] = drives.get(pos, frozenset()) | frozenset(consumers)

    for s0, e0 in stmts:
        assigns = assignments(code, s0, e0)
        if not assigns:
            made = instance(code, s0, e0)
            if made:
                inst, module, bodies[inst], got = made
                instances[inst].add(module)
                for pos, name, port, spans in got:
                    read(pos, name, port)
                    drive(pos, {port}, spans)
            continue
        for s, e, (at, width) in assigns:
            text_s = code[s:e]
            spans = calls(text_s, s)
            lhs = text_s[:at]
            found, start = lvalue_at(lhs)
            targets = [t for t, _ in found]
            targets_at.update(s + p for _, p in found)
            blk = next((b for b in blocks if b[0] <= s + at < b[1]), None)
            got = reads(text_s[at + width:], s + at + width)
            got += [(pos, name) for pos, name in reads(lhs[start:], s + start) if name not in targets]
            ctrl = []
            for c in CONTROL.finditer(lhs[:start]):
                a = c.end() - 1
                ctrl += reads(lhs[a + 1:close_of(lhs, a) - 1], s + a + 1)
            for t in targets:
                for pos, name in got:
                    read(pos, name, t)
            if blk:
                block_targets[blk].update(targets)
                block_ctrl[blk] += ctrl
                block_reads[blk] += [(pos, spans) for pos, _ in got + ctrl]
            else:
                for t in targets:
                    for pos, name in ctrl:
                        read(pos, name, t)
                for pos, _ in got + ctrl:
                    drive(pos, set(targets), spans)
    for blk, ctrl in block_ctrl.items():
        for t in block_targets[blk]:
            for pos, name in ctrl:
                read(pos, name, t)
    for blk, at in block_reads.items():
        for pos, spans in at:
            drive(pos, block_targets[blk], spans)
    tokens: dict[str, list[int]] = defaultdict(list)
    for m in TOKEN.finditer(code):
        tokens[m.group()].append(m.start())
    for pos, name in ((m.start(), m.group()) for m in TOKEN.finditer(code)):
        for consumer in drives.get(pos, ()):
            edges[name].add(consumer)
    newlines = [0] + [m.end() for m in re.finditer("\n", code)]
    net = Netlist(code, stmts, edges, reads_at, instances, bodies, set(OUTPUT_DECL.findall(code)), newlines,
                  drives, targets_at, set(), dict(tokens), subs)
    net.declared_at = {p for at in declarations(net, None).values() for p in at}
    return net


def declarations(net: Netlist, names: set[str] | None) -> dict[str, list[int]]:
    """Every offset at which a wire or variable declaration declares one of names (None: any name)."""
    out: dict[str, list[int]] = defaultdict(list)
    for s, e in net.stmts:
        text = net.code[s:e]
        m = DECL.match(text, lead_of(text))
        if not m:
            continue
        rest = text[m.end():]
        i = len(rest) - len(rest.lstrip())
        while rest.startswith("[", i):
            i = close_of(rest, i)
            i += len(rest[i:]) - len(rest[i:].lstrip())
        for a, b in top_level(rest[i:]):
            n = re.match(r"\s*([A-Za-z_]\w*)", rest[i + a:i + b])
            if n and (names is None or n.group(1) in names):
                out[n.group(1)].append(s + m.end() + i + a + n.start(1))
    return out
