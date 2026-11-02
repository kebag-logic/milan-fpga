#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A reader of the SystemVerilog subset the CSR block uses (#797).

The register reference must never guess. So an expression or statement outside
this grammar is a `Refusal`, not a fallback. Three layers:

  * `Parser` turns text into a tree: expressions, then the statements of an
    `always` block or a function.
  * `evaluate` computes a tree in three-valued logic. A bit nothing fixes is
    unknown, so the reset value of a word is computed the way simulation would
    compute it, and an X on the page means an input or an unreset flop.
  * `Interpreter` runs a block with the read address known and every other
    signal left symbolic. What remains is the tree of everything that word can
    return, including under which condition.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Union

WORD_BITS = 32
MAX_LOOP = 1024


class Refusal(Exception):
    """An input the generator cannot honestly turn into a page."""


# -------------------------------------------------------------------- values --
@dataclass(frozen=True)
class Vec:
    """A three-valued bit vector: `unknown` marks the bits nothing fixes."""
    width: int
    value: int = 0
    unknown: int = 0
    sized: bool = True

    @property
    def mask(self) -> int:
        """All ones over the width."""
        return (1 << self.width) - 1

    @property
    def known(self) -> bool:
        """Whether every bit is fixed."""
        return self.unknown == 0

    def bit(self, n: int) -> int | None:
        """One bit: 0, 1 or None when unknown."""
        if n >= self.width:
            return 0
        if self.unknown >> n & 1:
            return None
        return self.value >> n & 1

    def resized(self, width: int) -> "Vec":
        """Zero-extended or truncated to `width`."""
        mask = (1 << width) - 1
        return Vec(width, self.value & mask, self.unknown & mask, True)

    def truth(self) -> bool | None:
        """As a condition: True, False, or None when undecided."""
        if self.value & ~self.unknown & self.mask:
            return True
        return None if self.unknown & self.mask else False


def unknown_vec(width: int) -> Vec:
    """A vector with no bit fixed."""
    return Vec(width, 0, (1 << width) - 1)


def const_vec(value: int, width: int = WORD_BITS, sized: bool = True) -> Vec:
    """A fully known vector."""
    return Vec(width, value & ((1 << width) - 1), 0, sized)


def merged(a: Vec, b: Vec) -> Vec:
    """The result of a choice nothing decides: bits that agree stay known."""
    width = max(a.width, b.width)
    x, y = a.resized(width), b.resized(width)
    differ = (x.value ^ y.value) | x.unknown | y.unknown
    mask = (1 << width) - 1
    return Vec(width, x.value & ~differ & mask, differ & mask)


# ------------------------------------------------------------------ the tree --
#: A tree node: a tuple whose first item names the construct.
Node = tuple


@dataclass
class Case:
    """A case statement: (labels, body) items and an optional default."""
    selector: Node
    items: list[tuple[list[Node], list]] = field(default_factory=list)
    default: list = field(default_factory=list)


@dataclass
class If:
    """if (cond) then else other."""
    cond: Node
    then: list
    other: list


@dataclass
class For:
    """for (var = start; cond; ...) body."""
    var: str
    start: Node
    cond: Node
    body: list


@dataclass
class Assign:
    """target[selects...] = value, blocking or non-blocking."""
    target: str
    selects: list[Node]
    value: Node
    blocking: bool


Statement = Union[Case, If, For, Assign]


# ----------------------------------------------------------------- tokenizer --
TOKEN_RE = re.compile(r"""
    (?P<cast>\d+'\(|[A-Za-z_]\w*'\()
  | (?P<num>(?:\d[\d_]*)?'[sS]?[hHdDbBoO][0-9a-fA-FxXzZ_]+|\d[\d_]*|'[01])
  | (?P<id>\$?[A-Za-z_]\w*)
  | (?P<op>\+:|<<|>>|==|!=|<=|>=|&&|\|\||\+\+|[-+*/%&|^~!?:(){}\[\],<>=;.@])
  | (?P<ws>\s+)
""", re.X)


def tokenize(text: str) -> list[tuple[str, str]]:
    """(kind, text) tokens of an expression or statement."""
    out, pos = [], 0
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            raise Refusal(f"cannot tokenize {text[pos:pos + 40]!r}")
        pos = m.end()
        kind = m.lastgroup
        if kind != "ws":
            out.append((kind, m.group(kind)))
    return out


def parse_number(tok: str) -> Vec:
    """A SystemVerilog integer literal; an x or z digit is an unknown bit."""
    if tok in ("'0", "'1"):
        if tok == "'1":
            raise Refusal("the fill literal '1 needs a width this reader does not track")
        return Vec(1, 0, 0, False)
    if "'" not in tok:
        return const_vec(int(tok.replace("_", "")), WORD_BITS, False)
    size, rest = tok.split("'", 1)
    rest = rest.lstrip("sS")
    base = {"h": 16, "d": 10, "b": 2, "o": 8}[rest[0].lower()]
    digits = rest[1:].replace("_", "")
    value = int(re.sub(r"[xXzZ]", "0", digits), base)
    bits_per = {16: 4, 8: 3, 2: 1}.get(base, 0)
    unknown = 0
    for digit in digits if bits_per else "":
        unknown = unknown << bits_per | ((1 << bits_per) - 1 if digit in "xXzZ" else 0)
    width = int(size.replace("_", "")) if size else WORD_BITS
    return Vec(width, value & ((1 << width) - 1), unknown & ((1 << width) - 1), bool(size))


# -------------------------------------------------------------------- parser --
class Parser:
    """A recursive-descent reader of the expressions and statements of the CSR
    block. Anything else is refused by name."""

    PREC = (("||",), ("&&",), ("|",), ("^",), ("&",), ("==", "!="), ("<", ">", "<=", ">="),
            ("<<", ">>"), ("+", "-"), ("*", "/", "%"))

    def __init__(self, text: str) -> None:
        self.toks = tokenize(text)
        self.pos = 0
        self.text = text

    def peek(self, k: int = 0) -> str:
        """The text of the token k ahead, or the empty string at the end."""
        i = self.pos + k
        return self.toks[i][1] if i < len(self.toks) else ""

    def take(self, want: str | None = None) -> str:
        """Consume one token, refusing when it is not the expected one."""
        if self.pos >= len(self.toks):
            raise Refusal(f"unexpected end of {self.text!r}")
        tok = self.toks[self.pos][1]
        if want is not None and tok != want:
            raise Refusal(f"expected {want!r} in {self.text[:200]!r}, found {tok!r}")
        self.pos += 1
        return tok

    def done(self) -> bool:
        """Whether every token was consumed."""
        return self.pos >= len(self.toks)

    # ---- expressions -----------------------------------------------------
    def expression(self) -> Node:
        """cond ? a : b, or a binary expression."""
        cond = self.binary(0)
        if self.peek() == "?":
            self.take("?")
            a = self.expression()
            self.take(":")
            return ("tern", cond, a, self.expression())
        return cond

    def binary(self, level: int) -> Node:
        """Left-associative binary operators by precedence level."""
        if level == len(self.PREC):
            return self.unary()
        left = self.binary(level + 1)
        while self.peek() in self.PREC[level]:
            op = self.take()
            left = ("bin", op, left, self.binary(level + 1))
        return left

    def unary(self) -> Node:
        """-x, ~x, !x, the reductions &x, |x, ^x, and primaries."""
        if self.peek() in ("-", "~", "!", "&", "|", "^"):
            op = self.take()
            return ("un", op, self.unary())
        return self.primary()

    def primary(self) -> Node:
        """Literals, casts, identifiers, $clog2, parentheses, concatenations."""
        kind, tok = self.toks[self.pos] if self.pos < len(self.toks) else ("", "")
        if kind == "num":
            self.take()
            return self.selects(("num", parse_number(tok), tok))
        if kind == "cast":
            self.take()
            width_text = tok[:-2]
            is_number = width_text.isdigit()
            width = ("num", parse_number(width_text), width_text) if is_number else ("id", width_text)
            inner = self.expression()
            self.take(")")
            return ("cast", width, inner)
        if tok == "(":
            self.take("(")
            inner = self.expression()
            self.take(")")
            return self.selects(inner)
        if tok == "{":
            return self.concat()
        if tok == "$clog2":
            self.take()
            self.take("(")
            inner = self.expression()
            self.take(")")
            return ("clog2", inner)
        if kind == "id" and not tok.startswith("$"):
            self.take()
            if self.peek() == "(":
                return self.call(tok)
            return self.selects(("id", tok))
        raise Refusal(f"unexpected {tok!r} in {self.text[:200]!r}")

    def call(self, name: str) -> Node:
        """name(a, b): a function call, which only a known decode may evaluate."""
        self.take("(")
        args = [self.expression()]
        while self.peek() == ",":
            self.take(",")
            args.append(self.expression())
        self.take(")")
        return ("call", name, args)

    def selects(self, base: Node) -> Node:
        """Zero or more [i], [h:l] or [s +: w] applied to `base`."""
        while self.peek() == "[":
            self.take("[")
            first = self.expression()
            if self.peek() == ":":
                self.take(":")
                base = ("range", base, first, self.expression())
            elif self.peek() == "+:":
                self.take("+:")
                base = ("ipart", base, first, self.expression())
            else:
                base = ("index", base, first)
            self.take("]")
        return base

    def concat(self) -> Node:
        """{a, b, c} or a replication {N{x}}."""
        self.take("{")
        first = self.expression()
        if self.peek() == "{":
            inner = self.concat()
            self.take("}")
            return ("repl", first, inner)
        parts = [first]
        while self.peek() == ",":
            self.take(",")
            parts.append(self.expression())
        self.take("}")
        return ("concat", parts)

    # ---- statements ------------------------------------------------------
    def statements(self) -> list[Statement]:
        """Every statement up to the end of the text."""
        out: list[Statement] = []
        while not self.done():
            out += self.statement()
        return out

    def body(self) -> list[Statement]:
        """One statement as a list, a begin-end block flattened."""
        return self.statement()

    def statement(self) -> list[Statement]:
        """One statement; a declaration or an empty statement yields nothing."""
        tok = self.peek()
        if tok == "begin":
            return self.block()
        if tok in ("unique", "priority"):
            self.take()
            tok = self.peek()
        if tok == "case":
            return [self.case_statement()]
        if tok == "if":
            return [self.if_statement()]
        if tok == "for":
            return [self.for_statement()]
        if tok in ("logic", "int", "integer", "bit"):
            while self.take() != ";":
                pass
            return []
        if tok == ";":
            self.take()
            return []
        return [self.assignment()]

    def block(self) -> list[Statement]:
        """begin [: name] ... end [: name]."""
        self.take("begin")
        if self.peek() == ":":
            self.take(":")
            self.take()
        out: list[Statement] = []
        while self.peek() != "end":
            if self.done():
                raise Refusal(f"unterminated begin in {self.text[:200]!r}")
            out += self.statement()
        self.take("end")
        if self.peek() == ":":
            self.take(":")
            self.take()
        return out

    def if_statement(self) -> If:
        """if (cond) stmt [else stmt]."""
        self.take("if")
        self.take("(")
        cond = self.expression()
        self.take(")")
        then = self.body()
        other: list[Statement] = []
        if self.peek() == "else":
            self.take("else")
            other = self.body()
        return If(cond, then, other)

    def for_statement(self) -> For:
        """for (type var = start; cond; step) stmt."""
        self.take("for")
        self.take("(")
        while self.peek() in ("int", "unsigned", "integer", "genvar"):
            self.take()
        var = self.take()
        self.take("=")
        start = self.expression()
        self.take(";")
        cond = self.expression()
        self.take(";")
        while self.take() != ")":
            pass
        return For(var, start, cond, self.body())

    def case_statement(self) -> Case:
        """case (sel) labels: stmt ... default: stmt endcase."""
        self.take("case")
        self.take("(")
        out = Case(self.expression())
        self.take(")")
        while self.peek() != "endcase":
            if self.done():
                raise Refusal(f"unterminated case in {self.text[:200]!r}")
            if self.peek() == "default":
                self.take()
                if self.peek() == ":":
                    self.take(":")
                out.default = self.body()
                continue
            labels = [self.expression()]
            while self.peek() == ",":
                self.take(",")
                labels.append(self.expression())
            self.take(":")
            out.items.append((labels, self.body()))
        self.take("endcase")
        return out

    def assignment(self) -> Assign:
        """target[...] = value; or target[...] <= value;."""
        kind, tok = self.toks[self.pos] if self.pos < len(self.toks) else ("", "")
        if kind != "id":
            raise Refusal(f"expected a statement in {self.text[:200]!r}, found {tok!r}")
        self.take()
        selects: list[Node] = []
        while self.peek() == "[":
            self.take("[")
            first = self.expression()
            if self.peek() == ":":
                self.take(":")
                selects.append(("range", first, self.expression()))
            elif self.peek() == "+:":
                self.take("+:")
                selects.append(("ipart", first, self.expression()))
            else:
                selects.append(("index", first))
            self.take("]")
        op = self.take()
        if op not in ("=", "<="):
            raise Refusal(f"expected an assignment to {tok} in {self.text[:200]!r}, found {op!r}")
        value = self.expression()
        self.take(";")
        return Assign(tok, selects, value, op == "=")


def parse_expression(text: str) -> Node:
    """One whole expression; trailing tokens are refused."""
    parser = Parser(text)
    node = parser.expression()
    if not parser.done():
        raise Refusal(f"trailing tokens in {text[:200]!r}")
    return node


def parse_statements(text: str) -> list[Statement]:
    """Every statement of a block's text."""
    return Parser(text).statements()


# ---------------------------------------------------------------- unparsing --
def unparse(node: Node) -> str:
    """A tree as RTL text, compact, for the page and for messages."""
    kind = node[0]
    if kind == "num":
        return node[2]
    if kind == "vec":
        return f"32'h{node[1].value:08X}" if node[1].width == WORD_BITS else f"{node[1].width}'h{node[1].value:X}"
    if kind == "id":
        return node[1]
    if kind == "index":
        return f"{unparse(node[1])}[{unparse(node[2])}]"
    if kind == "range":
        return f"{unparse(node[1])}[{unparse(node[2])}:{unparse(node[3])}]"
    if kind == "ipart":
        return f"{unparse(node[1])}[{unparse(node[2])} +: {unparse(node[3])}]"
    if kind == "concat":
        return "{" + ", ".join(unparse(p) for p in node[1]) + "}"
    if kind == "repl":
        return "{" + unparse(node[1]) + unparse(node[2]) + "}"
    if kind == "cast":
        return f"{unparse(node[1])}'({unparse(node[2])})"
    if kind == "clog2":
        return f"$clog2({unparse(node[1])})"
    if kind == "call":
        return f"{node[1]}({', '.join(unparse(a) for a in node[2])})"
    if kind == "un":
        return f"{node[1]}{_wrapped(node[2])}"
    if kind == "bin":
        return f"{_wrapped(node[2])} {node[1]} {_wrapped(node[3])}"
    if kind == "tern":
        return f"{_wrapped(node[1])} ? {unparse(node[2])} : {unparse(node[3])}"
    raise Refusal(f"cannot print {kind}")


def _wrapped(node: Node) -> str:
    """A sub-expression, parenthesized when it is not a primary."""
    text = unparse(node)
    return f"({text})" if node[0] in ("bin", "tern") else text


def mentions(node: object, name: str) -> bool:
    """Whether the tree names `name` anywhere."""
    if isinstance(node, tuple):
        if len(node) == 2 and node[0] == "id":
            return node[1] == name
        return any(mentions(child, name) for child in node[1:])
    if isinstance(node, list):
        return any(mentions(child, name) for child in node)
    return False


# ---------------------------------------------------------------- evaluation --
class Scope:
    """Name lookup for `evaluate`: a known constant, a signal's current value,
    or a refusal. Subclasses say which."""

    def lookup(self, name: str) -> Vec | list[Vec]:
        """The value of a name; an unpacked array is a list of elements."""
        raise Refusal(f"unknown name {name}")


def _bitwise(op: str, x: Vec, y: Vec) -> Vec:
    """&, | or ^ in three-valued logic: 0 & X is 0, and 1 | X is 1."""
    width = max(x.width, y.width)
    a, b = x.resized(width), y.resized(width)
    mask = (1 << width) - 1
    if op == "&":
        zero = (~a.value & ~a.unknown) | (~b.value & ~b.unknown)
        known = a.value & b.value & ~a.unknown & ~b.unknown & mask
        return Vec(width, known, (a.unknown | b.unknown) & ~zero & mask)
    if op == "|":
        one = (a.value & ~a.unknown) | (b.value & ~b.unknown)
        return Vec(width, one & mask, (a.unknown | b.unknown) & ~one & mask)
    return Vec(width, (a.value ^ b.value) & mask, (a.unknown | b.unknown) & mask)


def _compare(op: str, a: Vec, b: Vec) -> Vec:
    """==, !=, <, >, <=, >= as one bit."""
    width = max(a.width, b.width)
    x, y = a.resized(width), b.resized(width)
    if op in ("==", "!="):
        fixed = ~(x.unknown | y.unknown)
        if (x.value ^ y.value) & fixed & ((1 << width) - 1):
            return const_vec(int(op == "!="), 1)
        if x.unknown or y.unknown:
            return unknown_vec(1)
        return const_vec(int((x.value == y.value) == (op == "==")), 1)
    if x.unknown or y.unknown:
        return unknown_vec(1)
    result = {"<": x.value < y.value, ">": x.value > y.value,
              "<=": x.value <= y.value, ">=": x.value >= y.value}[op]
    return const_vec(int(result), 1)


def _arith(op: str, a: Vec, b: Vec) -> Vec:
    """+, -, *, /, %, << and >>; an unknown operand makes every bit unknown."""
    width = a.width if op in ("<<", ">>") else max(a.width, b.width)
    sized = a.sized or b.sized or op in ("<<", ">>")
    if a.unknown or b.unknown:
        return unknown_vec(width)
    x, y = a.value, b.value
    result = {"+": lambda: x + y, "-": lambda: x - y, "*": lambda: x * y,
              "/": lambda: x // y if y else 0, "%": lambda: x % y if y else 0,
              "<<": lambda: x << y, ">>": lambda: x >> y}[op]()
    return const_vec(result, width, sized)


def _binary(node: Node, scope: Scope) -> Vec:
    """A binary operator node."""
    op, left, right = node[1], node[2], node[3]
    a = evaluate(left, scope)
    if op in ("&&", "||"):
        first = a.truth()
        if first is (op == "||"):
            return const_vec(int(first), 1)
        second = evaluate(right, scope).truth()
        if second is (op == "||"):
            return const_vec(int(second), 1)
        if first is None or second is None:
            return unknown_vec(1)
        return const_vec(int(second), 1)
    b = evaluate(right, scope)
    if op in ("&", "|", "^"):
        return _bitwise(op, a, b)
    if op in ("==", "!=", "<", ">", "<=", ">="):
        return _compare(op, a, b)
    return _arith(op, a, b)


def _unary(node: Node, scope: Scope) -> Vec:
    """A unary operator node."""
    op = node[1]
    v = evaluate(node[2], scope)
    if op == "-":
        return unknown_vec(v.width) if v.unknown else const_vec(-v.value, v.width, v.sized)
    if op == "~":
        return Vec(v.width, ~v.value & v.mask & ~v.unknown, v.unknown)
    if op == "!":
        truth = v.truth()
        return unknown_vec(1) if truth is None else const_vec(int(not truth), 1)
    if op == "|":
        truth = v.truth()
        return unknown_vec(1) if truth is None else const_vec(int(truth), 1)
    if op == "&":
        if ~v.value & ~v.unknown & v.mask:
            return const_vec(0, 1)
        return unknown_vec(1) if v.unknown else const_vec(1, 1)
    if v.unknown:
        return unknown_vec(1)
    return const_vec(bin(v.value).count("1") & 1, 1)


def _base_value(node: Node, scope: Scope) -> Vec | list[Vec]:
    """The value a select applies to: a plain name may be an array."""
    return scope.lookup(node[1]) if node[0] == "id" else evaluate(node, scope)


def _select(node: Node, scope: Scope) -> Vec:
    """x[i] (an array element or one bit), x[h:l] or x[s +: w]."""
    kind = node[0]
    base = _base_value(node[1], scope)
    if kind == "index":
        index = evaluate(node[2], scope)
        if isinstance(base, list):
            if index.unknown:
                out = base[0]
                for element in base[1:]:
                    out = merged(out, element)
                return out
            if index.value >= len(base):
                raise Refusal(f"{unparse(node)} is outside its array")
            return base[index.value]
        if index.unknown:
            return unknown_vec(1)
        bit = base.bit(index.value)
        return unknown_vec(1) if bit is None else const_vec(bit, 1)
    if isinstance(base, list):
        raise Refusal(f"{unparse(node)} selects bits of a whole array")
    if kind == "range":
        hi, lo = evaluate(node[2], scope), evaluate(node[3], scope)
        if hi.unknown or lo.unknown:
            raise Refusal(f"{unparse(node)} has a part select that is not constant")
        hi_v, lo_v = max(hi.value, lo.value), min(hi.value, lo.value)
    else:
        start, width = evaluate(node[2], scope), evaluate(node[3], scope)
        if width.unknown:
            raise Refusal(f"{unparse(node)} has an indexed part select of unknown width")
        if start.unknown:
            return unknown_vec(width.value)
        hi_v, lo_v = start.value + width.value - 1, start.value
    width_v = hi_v - lo_v + 1
    mask = (1 << width_v) - 1
    return Vec(width_v, base.value >> lo_v & mask, base.unknown >> lo_v & mask)


def _concat(parts: list[Node], scope: Scope) -> Vec:
    """{a, b, c}: every part must have a declared width."""
    value, unknown, width = 0, 0, 0
    for part in parts:
        v = evaluate(part, scope)
        if not v.sized:
            raise Refusal(f"unsized part {unparse(part)} in a concatenation")
        value = value << v.width | v.value
        unknown = unknown << v.width | v.unknown
        width += v.width
    return Vec(width, value, unknown)


def evaluate(node: Node, scope: Scope) -> Vec:
    """The value of a tree in three-valued logic."""
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "vec":
        return node[1]
    if kind == "id":
        value = scope.lookup(node[1])
        if isinstance(value, list):
            raise Refusal(f"{node[1]} is an array used as a value")
        return value
    if kind == "bin":
        return _binary(node, scope)
    if kind == "un":
        return _unary(node, scope)
    if kind == "tern":
        cond = evaluate(node[1], scope).truth()
        if cond is None:
            return merged(evaluate(node[2], scope), evaluate(node[3], scope))
        return evaluate(node[2] if cond else node[3], scope)
    if kind in ("index", "range", "ipart"):
        return _select(node, scope)
    if kind == "concat":
        return _concat(node[1], scope)
    if kind == "repl":
        count = evaluate(node[1], scope)
        if count.unknown:
            raise Refusal(f"replication count of {unparse(node)} is not constant")
        return _concat([node[2]] * count.value, scope)
    if kind == "cast":
        width = evaluate(node[1], scope)
        if width.unknown:
            raise Refusal(f"cast width of {unparse(node)} is not constant")
        return evaluate(node[2], scope).resized(width.value)
    if kind == "clog2":
        v = evaluate(node[1], scope)
        if v.unknown:
            raise Refusal(f"{unparse(node)} is not constant")
        return const_vec(max(0, (v.value - 1).bit_length()), WORD_BITS, False)
    raise Refusal(f"cannot evaluate {kind}")


# --------------------------------------------------------------- interpreter --
class Interpreter:
    """Runs a block's statements with some names known and the rest symbolic.

    `state` maps a name to the tree it holds. A condition that evaluates to a
    known value picks its branch; any other condition keeps both as a `tern`
    node, so the final tree of a target names every value it can take."""

    def __init__(self, scope: Scope, state: dict[str, Node] | None = None) -> None:
        self.scope = scope
        self.state: dict[str, Node] = dict(state or {})

    def reduce(self, node: Node) -> Node:
        """`node` with state substituted and known choices resolved."""
        kind = node[0]
        if kind == "id":
            return self.state.get(node[1], node)
        if kind in ("num", "vec"):
            return node
        if kind == "tern":
            cond = self.reduce(node[1])
            truth = self.truth(cond)
            if truth is None:
                return ("tern", cond, self.reduce(node[2]), self.reduce(node[3]))
            return self.reduce(node[2] if truth else node[3])
        if kind == "concat":
            return ("concat", [self.reduce(p) for p in node[1]])
        if kind == "bin" and node[1] in ("&&", "||"):
            return self.reduce_logic(node)
        if kind in ("bin", "un"):
            out = (kind, node[1], *[self.reduce(p) for p in node[2:]])
            if kind == "bin" and node[1] in ("&", "|", "^"):
                return out
            value = evaluate(out, self.scope)
            return ("vec", value) if value.known else out
        if kind in ("index", "range", "ipart", "cast", "repl", "clog2"):
            return (kind, *[self.reduce(p) for p in node[1:]])
        raise Refusal(f"cannot interpret {kind}")

    def reduce_logic(self, node: Node) -> Node:
        """&& and ||, dropping an operand a known value decides."""
        op = node[1]
        left, right = self.reduce(node[2]), self.reduce(node[3])
        a, b = self.truth(left), self.truth(right)
        decisive = op == "||"
        if a is decisive or b is decisive:
            return ("vec", const_vec(int(decisive), 1))
        if a is not None:
            return right
        if b is not None:
            return left
        return ("bin", op, left, right)

    def truth(self, node: Node) -> bool | None:
        """A condition's truth under the scope, or None when undecided."""
        return evaluate(node, self.scope).truth()

    def run(self, statements: list[Statement]) -> None:
        """Execute statements in order."""
        for st in statements:
            if isinstance(st, Assign):
                self.assign(st)
            elif isinstance(st, If):
                self.branch(st.cond, st.then, st.other)
            elif isinstance(st, Case):
                self.case(st)
            else:
                self.loop(st)

    def assign(self, st: Assign) -> None:
        """A whole-signal assignment; a partial one is outside the grammar."""
        if st.selects:
            raise Refusal(f"the read path assigns part of {st.target}, which this reader does not model")
        self.state[st.target] = self.reduce(st.value)

    def branch(self, cond: Node, then: list, other: list) -> None:
        """if/else: a known condition runs one arm, an unknown one merges."""
        reduced = self.reduce(cond)
        truth = self.truth(reduced)
        if truth is True:
            self.run(then)
        elif truth is False:
            self.run(other)
        else:
            first = Interpreter(self.scope, self.state)
            first.run(then)
            second = Interpreter(self.scope, self.state)
            second.run(other)
            for name in set(first.state) | set(second.state):
                a, b = first.state.get(name), second.state.get(name)
                if a != b:
                    self.state[name] = ("tern", reduced, a if a is not None else ("id", name),
                                        b if b is not None else ("id", name))

    def case(self, st: Case) -> None:
        """A case as equality tests in label order: labels a known selector
        rules out are skipped, so a long decode needs no deep recursion."""
        selector = st.selector
        remaining: list = []
        for index, (labels, body) in enumerate(st.items):
            tests = [("bin", "==", selector, label) for label in labels]
            verdicts = [self.truth(self.reduce(test)) for test in tests]
            if True in verdicts:
                self.run(body)
                return
            if None in verdicts:
                remaining = st.items[index:]
                break
        if not remaining:
            self.run(st.default)
            return
        chain: list = list(st.default)
        for labels, body in reversed(remaining):
            cond = ("bin", "==", selector, labels[0])
            for label in labels[1:]:
                cond = ("bin", "||", cond, ("bin", "==", selector, label))
            chain = [If(cond, body, chain)]
        self.run(chain)

    def loop(self, st: For) -> None:
        """A for loop with constant bounds, unrolled."""
        self.state[st.var] = self.reduce(st.start)
        count = 0
        while self.truth(self.reduce(st.cond)):
            self.run(st.body)
            current = evaluate(self.state[st.var], self.scope)
            self.state[st.var] = ("vec", const_vec(current.value + 1, current.width))
            count += 1
            if count > MAX_LOOP:
                raise Refusal(f"a loop over {st.var} does not end")
        del self.state[st.var]


def flatten(node: Node, conds: tuple = ()) -> list[tuple[tuple, Node]]:
    """Every (conditions, value) a tree can yield: `conditions` is a tuple of
    (condition node, polarity); `value` holds no top-level choice."""
    if node[0] == "tern":
        return flatten(node[2], conds + ((node[1], True),)) + flatten(node[3], conds + ((node[1], False),))
    return [(conds, node)]
