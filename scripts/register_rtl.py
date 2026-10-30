#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The RTL side of the register reference generator (#797).

Reads `hdl/common/csr/milan_csr.sv`, its generated includes and the
`milan_csr` instance in `hdl/milan/milan_datapath.sv`, and reads the SoC facts
from a builder export. `scripts/gen_register_reference.py` is the entry point;
this module only reads sources and evaluates their constant expressions.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTL = "hdl/common/csr/milan_csr.sv"
DATAPATH = "hdl/milan/milan_datapath.sv"
ETH_PKG = "hdl/common/ethernet_packet_pkg.sv"
CSR_INCLUDE_DIR = "hdl/common/csr"
SHAPE_INCLUDE_DIR = "configs/generated/{shape}"
DESCRIPTIONS = "scripts/register_descriptions.json"
SOC = "scripts/register_map_soc.json"
LEDGER = "docs/reference/milan_feature_status.json"
PAGE = "docs/reference/REGISTER_MAP.md"
DIAGRAM_DIR = "docs/diagrams/regmap"
WORD_BITS = 32


class Refusal(Exception):
    """An input the generator cannot honestly turn into a page."""


# ---------------------------------------------------------------- source text --
def strip_comments(text: str) -> str:
    """The text with comments and attributes blanked, line structure kept, so
    a line number found in the result is a line number in the file."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(c if c == "\n" else " " for c in text[i:j]))
            i = j
        elif text.startswith("(*", i) and not text.startswith("(*)", i):
            j = text.find("*)", i + 2)
            j = n if j < 0 else j + 2
            out.append(" " * (j - i))
            i = j
        elif text[i] == '"':
            j = text.find('"', i + 1)
            j = n if j < 0 else j + 1
            out.append(text[i:j])
            i = j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


TOKEN_RE = re.compile(r"""
    (?P<cast>\d+'\(|[A-Za-z_]\w*'\()
  | (?P<num>(?:\d[\d_]*)?'[sS]?[hHdDbBoO][0-9a-fA-FxXzZ_]+|\d[\d_]*)
  | (?P<id>\$?[A-Za-z_]\w*)
  | (?P<op><<|>>|==|!=|<=|>=|&&|\|\||[-+*/%&|^~!?:(){}\[\],<>=;.])
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


def parse_number(tok: str) -> tuple[int, int | None]:
    """(value, width) of a SystemVerilog integer literal."""
    if "'" not in tok:
        return int(tok.replace("_", "")), None
    size, rest = tok.split("'", 1)
    rest = rest.lstrip("sS")
    base = {"h": 16, "d": 10, "b": 2, "o": 8}[rest[0].lower()]
    digits = rest[1:].replace("_", "")
    value = int(re.sub(r"[xXzZ]", "0", digits), base)
    return value, (int(size.replace("_", "")) if size else None)


# ------------------------------------------------------- constant expressions --
@dataclass(frozen=True)
class Term:
    """One part of a read or assign expression, with its bit span."""
    kind: str          # "signal", "const", "complex"
    name: str          # signal name, or the expression text
    hi: int            # bit span inside the signal (signal), or width-1 (const)
    lo: int
    value: int | None = None


class Expr:
    """A recursive-descent reader of the constant and concatenation
    expressions the CSR block uses; widths come from `widths`."""

    def __init__(self, text: str, symbols: "Symbols"):
        self.toks = tokenize(text)
        self.pos = 0
        self.sym = symbols
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
            raise Refusal(f"expected {want!r} in {self.text!r}, found {tok!r}")
        self.pos += 1
        return tok

    def done(self) -> bool:
        """Whether every token was consumed."""
        return self.pos >= len(self.toks)

    # value evaluation ----------------------------------------------------
    def value(self) -> tuple[int, int | None]:
        """Evaluate the whole expression to (value, width)."""
        v = self.ternary()
        if not self.done():
            raise Refusal(f"trailing tokens in {self.text!r}")
        return v

    def ternary(self) -> tuple[int, int | None]:
        """cond ? a : b."""
        c = self.binary(0)
        if self.peek() == "?":
            self.take("?")
            a = self.ternary()
            self.take(":")
            b = self.ternary()
            return a if c[0] else b
        return c

    PREC = [("||",), ("&&",), ("|",), ("^",), ("&",), ("==", "!="), ("<", ">", "<=", ">="),
            ("<<", ">>"), ("+", "-"), ("*", "/", "%")]

    def binary(self, level: int) -> tuple[int, int | None]:
        """Left-associative binary operators by precedence level."""
        if level == len(self.PREC):
            return self.unary()
        left = self.binary(level + 1)
        while self.peek() in self.PREC[level]:
            op = self.take()
            right = self.binary(level + 1)
            a, b = left[0], right[0]
            width = max(w for w in (left[1], right[1], 0) if w is not None) or None
            left = ({"||": int(bool(a or b)), "&&": int(bool(a and b)), "|": a | b, "^": a ^ b,
                     "&": a & b, "==": int(a == b), "!=": int(a != b), "<": int(a < b),
                     ">": int(a > b), "<=": int(a <= b), ">=": int(a >= b), "<<": a << b,
                     ">>": a >> b, "+": a + b, "-": a - b, "*": a * b,
                     "/": a // b if b else 0, "%": a % b if b else 0}[op], width)
        return left

    def unary(self) -> tuple[int, int | None]:
        """-x, ~x, !x, and primaries."""
        if self.peek() in ("-", "~", "!"):
            op = self.take()
            v, w = self.unary()
            if op == "-":
                return -v, w
            if op == "!":
                return int(not v), 1
            return (~v) & ((1 << (w or WORD_BITS)) - 1), w
        return self.primary()

    def primary(self) -> tuple[int, int | None]:
        """Literals, casts, identifiers, $clog2, parentheses, concatenations."""
        kind, tok = self.toks[self.pos] if self.pos < len(self.toks) else ("", "")
        if kind == "num":
            self.take()
            return parse_number(tok)
        if kind == "cast":
            self.take()
            width_text = tok[:-2]
            width = int(width_text) if width_text.isdigit() else self.sym.value(width_text)
            v, _ = self.ternary()
            self.take(")")
            return v & ((1 << width) - 1) if v >= 0 else v, width
        if tok == "(":
            self.take("(")
            v = self.ternary()
            self.take(")")
            return v
        if tok == "{":
            parts = self.concat_parts()
            value, width = 0, 0
            for v, w in parts:
                if w is None:
                    raise Refusal(f"unsized part in concatenation {self.text!r}")
                value = (value << w) | (v & ((1 << w) - 1))
                width += w
            return value, width
        if tok == "$clog2":
            self.take()
            self.take("(")
            v, _ = self.ternary()
            self.take(")")
            return max(0, (v - 1).bit_length()), None
        if kind == "id":
            self.take()
            v, w = self.sym.value(tok), self.sym.width(tok)
            if self.peek() == "[":
                self.take("[")
                hi, _ = self.ternary()
                lo = hi
                if self.peek() == ":":
                    self.take(":")
                    lo, _ = self.ternary()
                self.take("]")
                return (v >> lo) & ((1 << (hi - lo + 1)) - 1), hi - lo + 1
            return v, w
        raise Refusal(f"unexpected {tok!r} in {self.text!r}")

    def concat_parts(self) -> list[tuple[int, int | None]]:
        """{a, b, c} or a replication {N{x}}."""
        self.take("{")
        parts = [self.ternary()]
        if self.peek() == "{":
            count = parts[0][0]
            inner = self.concat_parts()
            self.take("}")
            return inner * count
        while self.peek() == ",":
            self.take(",")
            parts.append(self.ternary())
        self.take("}")
        return parts


class Symbols:
    """Parameters, localparams and declared widths, resolved lazily."""

    def __init__(self) -> None:
        self.exprs: dict[str, str] = {}
        self.decl_width: dict[str, int | str] = {}
        self.cache: dict[str, tuple[int, int | None]] = {}
        self.overrides: dict[str, int] = {}

    def define(self, name: str, expr: str, width: int | str | None = None) -> None:
        """Record a constant's defining expression (first definition wins)."""
        self.exprs.setdefault(name, expr)
        if width is not None:
            self.decl_width.setdefault(name, width)

    def has(self, name: str) -> bool:
        """Whether a constant of that name is known."""
        return name in self.overrides or name in self.exprs

    def resolve(self, name: str) -> tuple[int, int | None]:
        """(value, width) of a constant."""
        if name in self.overrides:
            return self.overrides[name], self.width(name)
        if name not in self.cache:
            if name not in self.exprs:
                raise Refusal(f"unknown constant {name}")
            self.cache[name] = (0, None)       # guards a self-reference
            v, w = Expr(self.exprs[name], self).value()
            dw = self.width(name)
            self.cache[name] = (v, dw if dw is not None else w)
        return self.cache[name]

    def value(self, name: str) -> int:
        """The constant's value."""
        return self.resolve(name)[0]

    def width(self, name: str) -> int | None:
        """The declared width of a constant or signal, evaluated."""
        w = self.decl_width.get(name)
        if isinstance(w, str):
            w = range_width(w, self)
            self.decl_width[name] = w
        return w


def range_width(rng: str, sym: Symbols) -> int:
    """Width of a `[hi:lo]` packed range."""
    hi, lo = rng.strip()[1:-1].split(":", 1)
    return abs(Expr(hi, sym).value()[0] - Expr(lo, sym).value()[0]) + 1


def split_top(expr: str, sep: str) -> list[str]:
    """Split on a separator outside every bracket, `sep` being one character
    or the two-character `?:` handled by the caller."""
    parts, depth, cur, i = [], 0, "", 0
    while i < len(expr):
        c = expr[i]
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
        if depth == 0 and expr.startswith(sep, i) and not (
                sep == "|" and (expr.startswith("||", i) or (i and expr[i - 1] == "|"))) and not (
                sep == "&" and (expr.startswith("&&", i) or (i and expr[i - 1] == "&"))):
            parts.append(cur)
            cur = ""
            i += len(sep)
            continue
        cur += c
        i += 1
    parts.append(cur)
    return [p.strip() for p in parts]


def strip_parens(expr: str) -> str:
    """`(x)` -> `x` while the outer parentheses enclose everything."""
    expr = expr.strip()
    while expr.startswith("(") and matching(expr, 0, "(", ")") == len(expr) - 1:
        expr = expr[1:-1].strip()
    return expr


def is_concat(expr: str) -> bool:
    """Whether the whole expression is one `{...}` concatenation."""
    expr = expr.strip()
    return expr.startswith("{") and matching(expr, 0, "{", "}") == len(expr) - 1 \
        and not re.match(r"\{\s*\d+\s*\{", expr)


# ------------------------------------------------------------- block scanning --
def find_block(text: str, header_re: str) -> str:
    """The body of the first `begin ... end` block whose header matches."""
    m = re.search(header_re, text)
    if not m:
        raise Refusal(f"{RTL}: no block matching {header_re!r}")
    start = text.index("begin", m.start())
    return balanced(text, start)


WORD_RE = re.compile(r"\b(begin|end|case|endcase|fork|join)\b")


def balanced(text: str, start: int) -> str:
    """The text from a `begin` at `start` through its matching `end`."""
    depth = 0
    for m in WORD_RE.finditer(text, start):
        word = m.group(1)
        if word in ("begin", "case", "fork"):
            depth += 1
        elif word in ("end", "endcase", "join"):
            depth -= 1
            if depth == 0:
                return text[start:m.end()]
    raise Refusal(f"{RTL}: unbalanced block at offset {start}")


def statement_end(text: str, pos: int) -> int:
    """The index just past one statement starting at `pos`."""
    m = re.compile(r"\s*").match(text, pos)
    pos = m.end()
    if text.startswith("begin", pos):
        return pos + len(balanced(text, pos))
    for kw in ("unique case", "case"):
        if text.startswith(kw, pos):
            return pos + len(balanced(text, pos))
    if re.match(r"(if|for)\b", text[pos:]):
        paren = text.index("(", pos)
        close = matching(text, paren, "(", ")")
        end = statement_end(text, close + 1)
        if text.startswith("if", pos):
            m = re.compile(r"\s*else\b").match(text, end)
            if m:
                end = statement_end(text, m.end())
        return end
    depth = 0
    for i in range(pos, len(text)):
        c = text[i]
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
        elif c == ";" and depth == 0:
            return i + 1
    raise Refusal(f"{RTL}: unterminated statement at offset {pos}")


def matching(text: str, pos: int, open_c: str, close_c: str) -> int:
    """Index of the bracket closing the one at `pos`."""
    depth = 0
    for i in range(pos, len(text)):
        if text[i] == open_c:
            depth += 1
        elif text[i] == close_c:
            depth -= 1
            if depth == 0:
                return i
    raise Refusal(f"{RTL}: unbalanced {open_c} at offset {pos}")


def case_items(block: str, selector: str) -> list[tuple[list[str], str]]:
    """(labels, body) of every item of the first `case (selector)` in `block`."""
    m = re.search(r"\bcase\s*\(\s*" + re.escape(selector) + r"\s*\)", block)
    if not m:
        raise Refusal(f"{RTL}: no case ({selector})")
    whole = balanced(block, block.rfind("case", 0, m.end()))
    pos = whole.index(")", whole.index("(")) + 1
    end = whole.rindex("endcase")
    items = []
    while True:
        m = re.compile(r"\s*").match(whole, pos)
        pos = m.end()
        if pos >= end:
            break
        colon = item_colon(whole, pos)
        labels = [lab.strip() for lab in whole[pos:colon].split(",")]
        stop = statement_end(whole, colon + 1)
        items.append((labels, whole[colon + 1:stop].strip()))
        pos = stop
    return items


def item_colon(text: str, pos: int) -> int:
    """The `:` ending a case-item label list (brackets inside labels skipped)."""
    depth = 0
    for i in range(pos, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == ":" and depth == 0:
            return i
    raise Refusal(f"{RTL}: case item without a label at offset {pos}")


def label_name(label: str) -> str:
    """`A_MAC_CTRL[10:0]` -> `A_MAC_CTRL`."""
    return label.split("[", 1)[0].strip()


# ------------------------------------------------------------------ the model --
@dataclass
class RtlFacts:
    """Everything the generator reads out of milan_csr.sv and its includes."""
    sym: Symbols
    addresses: dict[str, int]                  # A_* label -> offset
    params: dict[str, int]
    write_arms: dict[str, list[tuple[str, str]]]   # label -> [(block, body)]
    read_arms: dict[str, tuple[str, str]]          # label -> (block, body)
    window_reads: dict[str, str]                   # label -> strm_mux body
    defaults: dict[str, str]                       # label -> csr_default expr
    plain_rw: set[str]
    resets: dict[str, str]                         # storage -> reset expr
    assigns: dict[str, str]                        # output port -> expr
    signals: dict[str, int]                        # declared signal widths
    cbs: dict[str, list[int]]
    cbs_en_reset: str
    version: int
    arrays: set[str]
    usage: dict[str, set[int] | None]
    text: str
    wires: dict[str, str]


def read_text(root: Path, rel: str) -> str:
    """A tracked input, refused by name when absent."""
    path = root / rel
    if not path.is_file():
        raise Refusal(f"missing input {rel}")
    return path.read_text(encoding="utf-8")


def define_header_parameters(text: str, module: str, sym: Symbols) -> dict[str, str]:
    """The `#( parameter ... )` list of `module`: name -> default expression."""
    start = re.search(r"\bmodule\s+" + module + r"\b(?:\s+import\s+[\w:*,\s]+;)?\s*#\s*\(", text)
    if not start:
        raise Refusal(f"no parameter list for module {module}")
    open_paren = text.index("(", start.end() - 1)
    body = text[open_paren + 1:matching(text, open_paren, "(", ")")]
    found = {}
    for decl in split_top(body, ","):
        m = re.match(r"\s*parameter\s+(?:(int\s+unsigned|int|bit|string|logic)\s*)?(\[[^\]]+\])?\s*(\w+)\s*=\s*(.+)$",
                     decl, re.S)
        if not m or m.group(1) == "string":
            continue
        width = m.group(2) or (1 if m.group(1) == "bit" else None)
        sym.define(m.group(3), " ".join(m.group(4).split()), width)
        found[m.group(3)] = " ".join(m.group(4).split())
    return found


def define_constants(text: str, sym: Symbols) -> None:
    """Every `localparam` (and package `parameter`) statement of a file,
    list form included."""
    for m in re.finditer(r"\b(parameter|localparam)\b([^;]*?);", text, re.S):
        decl = m.group(2)
        if m.group(1) == "parameter" and re.search(r",\s*$|\bparameter\b", decl):
            continue
        if "=" not in decl:
            continue
        width = None
        wm = re.match(r"\s*(?:(?:int|bit|logic|integer|string)\s+)?(?:unsigned\s+)?(\[[^\]]+\])?", decl)
        if wm and wm.group(1):
            width = wm.group(1)
        elif re.match(r"\s*(int|integer)\b", decl):
            width = None
        elif re.match(r"\s*bit\b", decl):
            width = 1
        body = decl[wm.end():] if wm else decl
        for name, expr in split_assignments(body):
            if "[" in name or "'{" in expr or expr.startswith('"'):
                continue
            sym.define(name, expr, width)


def split_assignments(body: str) -> list[tuple[str, str]]:
    """`A = 1, B = {2, 3}` -> [("A", "1"), ("B", "{2, 3}")], commas in
    brackets kept."""
    out, depth, cur = [], 0, ""
    for c in body + ",":
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
        if c == "," and depth == 0:
            if "=" in cur:
                name, expr = cur.split("=", 1)
                name = name.strip().split()[-1] if name.strip() else ""
                if re.fullmatch(r"\w+", name):
                    out.append((name, expr.strip()))
            cur = ""
        else:
            cur += c
    return out


def declared_signals(text: str, sym: Symbols) -> tuple[dict[str, str], set[str]]:
    """Width ranges of every port, logic and wire declaration, and the names
    declared as unpacked arrays (an index selects a whole element)."""
    found: dict[str, str] = {}
    arrays: set[str] = set()
    port_re = re.compile(r"\b(input|output)\s+(?:wire|logic)?\s*(\[[^\]]+\])?\s*(\w+)")
    for m in port_re.finditer(text):
        found.setdefault(m.group(3), m.group(2) or "[0:0]")
    decl_re = re.compile(r"\b(?:logic|wire|reg)\s*(\[[^\]]+\])?\s*([\w\s,]+?)\s*(\[[^\]]*\])?\s*(?:=[^;]*)?;")
    for m in decl_re.finditer(text):
        for name in m.group(2).split(","):
            name = name.strip()
            if re.fullmatch(r"[A-Za-z_]\w*", name):
                found.setdefault(name, m.group(1) or "[0:0]")
                if m.group(3):
                    arrays.add(name)
    return found, arrays


def bit_usage(text: str, names: set[str], sym: Symbols) -> dict[str, set[int] | None]:
    """For each storage name, the bits some expression reads; None means
    the whole value is read somewhere. Assignment targets are not reads."""
    used: dict[str, set[int] | None] = {}
    ref_re = re.compile(r"\b([A-Za-z_]\w*)\b(\s*\[[^\]]+\])?")
    for m in ref_re.finditer(text):
        name = m.group(1)
        if name not in names:
            continue
        after = text[m.end():m.end() + 40].lstrip()
        if after.startswith("<=") and not after.startswith("<=="):
            continue
        before = text[max(0, m.start() - 40):m.start()]
        if re.search(r"\b(logic|wire|reg)\b[^;]*$", before) and not re.search(r"=", before.split("\n")[-1]):
            continue
        if used.get(name, set()) is None:
            continue
        if not m.group(2):
            used[name] = None
            continue
        inner = m.group(2).strip()[1:-1]
        try:
            if ":" in inner and "+:" not in inner:
                hi, lo = (Expr(x, sym).value()[0] for x in inner.split(":", 1))
                used.setdefault(name, set()).update(range(min(hi, lo), max(hi, lo) + 1))
            else:
                used.setdefault(name, set()).add(Expr(inner, sym).value()[0])
        except (Refusal, ValueError):
            used[name] = None
    return used


def load_rtl(root: Path, shape: str, overrides: dict[str, int]) -> RtlFacts:
    """Read milan_csr.sv, its two generated includes and the parameters the
    shipping build passes, into one set of facts."""
    raw = read_text(root, RTL)
    text = strip_comments(raw)
    sym = Symbols()
    pkg = strip_comments(read_text(root, ETH_PKG))
    define_constants(pkg, sym)
    for inc in re.findall(r'`include\s+"([^"]+)"', text):
        candidates = [f"{CSR_INCLUDE_DIR}/{inc}", f"{SHAPE_INCLUDE_DIR.format(shape=shape)}/{inc}"]
        path = next((c for c in candidates if (root / c).is_file()), None)
        if path is None:
            raise Refusal(f"{RTL} includes {inc}, found in neither {candidates}")
        define_constants(strip_comments(read_text(root, path)), sym)
    params = define_header_parameters(text, "milan_csr", sym)
    body_start = text.index(");", text.index("module milan_csr"))
    define_constants(text[body_start:], sym)
    for name, value in overrides.items():
        if name not in params:
            raise Refusal(f"the SoC extract overrides {name}, which milan_csr.sv does not declare")
        sym.overrides[name] = value
    declared, arrays = declared_signals(text, sym)
    for name, rng in declared.items():
        sym.decl_width.setdefault(name, rng)

    addresses = {}
    for m in re.finditer(r"\b(A_\w+)\s*=\s*([^,;]+)", text):
        name, expr = m.group(1), m.group(2).strip()
        if name in addresses:
            continue
        addresses[name] = Expr(expr, sym).value()[0]

    write_arms: dict[str, list[tuple[str, str]]] = {}
    resets: dict[str, str] = {}
    for m in re.finditer(r"if\s*\(\s*!aresetn\s*\)\s*", text):
        rest = text[m.end():]
        stop = statement_end(rest, 0)
        for r in re.finditer(r"(\w+)\s*<=\s*([^;]+);", rest[:stop]):
            resets.setdefault(r.group(1), r.group(2).strip())
    for block_name in ("register_write", "pp_regs"):
        block = find_block(text, r"always_ff\s*@\(posedge aclk\)\s*begin\s*:\s*" + block_name + r"\b")
        for labels, body in case_items(block, "wr_addr"):
            for lab in labels:
                if lab != "default":
                    write_arms.setdefault(label_name(lab), []).append((block_name, body))

    read_arms: dict[str, tuple[str, str]] = {}
    for block_name, target in (("read_mux", "live_mux"), ("pp_read", "pp_rd_data_w")):
        block = find_block(text, r"always_comb\s*begin\s*:\s*" + block_name + r"\b")
        for labels, body in case_items(block, "rd_addr_q"):
            for lab in labels:
                if lab != "default":
                    read_arms[label_name(lab)] = (target, body)

    window_reads: dict[str, str] = {}
    strm = find_block(text, r"always_comb\s*begin\s*:\s*strm_read_mux\b")
    for m in re.finditer(r"rd_addr_q\s*==\s*(A_\w+)\)\s*\n?\s*strm_mux\s*=\s*([^;]+);", strm):
        window_reads[m.group(1)] = "strm_mux = " + m.group(2).strip() + ";"
    for labels, body in case_items(strm, "rd_addr_q"):
        for lab in labels:
            if lab != "default":
                window_reads[label_name(lab)] = body

    defaults: dict[str, str] = {}
    fn = text[text.index("function automatic [31:0] csr_default"):]
    fn = fn[:fn.index("endfunction")]
    for labels, body in case_items(fn, "a"):
        for lab in labels:
            if lab != "default":
                mm = re.match(r"csr_default\s*=\s*(.*);\s*$", body, re.S)
                if mm:
                    defaults[label_name(lab)] = mm.group(1).strip()

    fn = text[text.index("function automatic logic is_plain_rw"):]
    fn = fn[:fn.index("endfunction")]
    plain = set()
    for labels, _ in case_items(fn, "a"):
        plain.update(label_name(lab) for lab in labels if lab != "default")

    assigns = {}
    for m in re.finditer(r"\bassign\s+(o_\w+)\s*=\s*([^;]+);", text):
        assigns[m.group(1)] = " ".join(m.group(2).split())

    cbs = {}
    for name in ("CBS_IDLE_RST", "CBS_HI_RST", "CBS_LO_RST"):
        m = re.search(name + r"\s*\[0:\d+\]\s*=\s*'\{([^}]*)\}", text)
        if not m:
            raise Refusal(f"{RTL}: no {name} table")
        cbs[name] = [int(v.strip().replace("_", "")) for v in m.group(1).split(",")]
    m = re.search(r"CBS_EN_RST\s*=\s*([^;]+);", text)
    if not m:
        raise Refusal(f"{RTL}: no CBS_EN_RST")

    signals = {}
    for name in list(sym.decl_width):
        try:
            w = sym.width(name)
        except Refusal:
            continue
        if w is not None:
            signals[name] = w
    params_int = {}
    for name in params:
        params_int[name] = sym.value(name)
    storage = {n for n in signals if not n.startswith(("i_", "o_"))}
    usage = bit_usage(text[body_start:], storage, sym)
    wires = {w.group(1): " ".join(w.group(2).split()) for w in
             re.finditer(r"\bwire\s*(?:\[[^\]]+\])?\s*(\w+)\s*=\s*([^;]+);", text)}
    return RtlFacts(sym, addresses, params_int, write_arms, read_arms, window_reads, defaults,
                    plain, resets, assigns, signals, cbs, m.group(1).strip(), sym.value("VERSION"),
                    arrays, usage, text, wires)


# ------------------------------------------------------------- the SoC side --
def verilog_value(text: str) -> int | None:
    """An integer Verilog literal as LiteX writes it (`26'd50000000`), or
    None for a string or anything else."""
    text = text.strip()
    if text.startswith('"'):
        return None
    try:
        return parse_number(text)[0]
    except (KeyError, ValueError, IndexError):
        return None


def extract_soc(build: Path) -> dict:
    """The SoC facts the page states, read from a builder export: its
    `csr.csv`, its `aem_desc.json` and the datapath parameters in the
    generated top-level Verilog."""
    csv = build / "csr.csv"
    if not csv.is_file():
        raise Refusal(f"{build} has no csr.csv")
    lines = csv.read_text(encoding="utf-8").splitlines()
    litex = next((m.group(1) for ln in lines if (m := re.search(r"LiteX \(([0-9a-f]+)\)", ln))), "")
    body = [ln for ln in lines if ln and not ln.startswith("#")]
    out: dict = {
        "generated_by": "python3 scripts/gen_register_reference.py --soc-from <export>",
        "litex": litex,
        "csr_csv_sha256": hashlib.sha256("\n".join(body).encode()).hexdigest(),
        "memory_regions": [], "csr_banks": [], "csr_registers": [], "constants": {},
    }
    for ln in body:
        cells = ln.split(",")
        kind = cells[0]
        if kind == "memory_region":
            out["memory_regions"].append({"name": cells[1], "origin": int(cells[2], 16),
                                          "size": int(cells[3]), "type": cells[4]})
        elif kind == "csr_base":
            out["csr_banks"].append({"name": cells[1], "origin": int(cells[2], 16)})
        elif kind == "csr_register":
            out["csr_registers"].append({"name": cells[1], "address": int(cells[2], 16),
                                         "words": int(cells[3]), "mode": cells[4]})
        elif kind == "constant" and (cells[1].startswith(("milan_", "spiflash_"))
                                     or cells[1] in ("config_clock_frequency", "config_platform_name")):
            value = cells[2]
            out["constants"][cells[1]] = int(value) if re.fullmatch(r"-?\d+", value) else value
    aem = build / "aem_desc.json"
    if not aem.is_file():
        raise Refusal(f"{build} has no aem_desc.json")
    desc = json.loads(aem.read_text(encoding="utf-8"))
    out["pp_windows"] = {k: desc[k] for k in ("desc_base", "resp_base", "nvm_base", "nvm_stage_base",
                                              "window_bytes")}
    shape = re.search(r"out/([^/]+)/", desc.get("overlay", ""))
    if not shape:
        raise Refusal(f"{aem} names no builder shape in its overlay path")
    out["shape"] = shape.group(1)
    tops = sorted((build / "gateware").glob("*.v"))
    params: dict[str, int] = {}
    for top in tops:
        text = top.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"milan_datapath\s*#\(", text)
        if not m:
            continue
        block = text[m.end():matching(text, m.end() - 1, "(", ")")]
        for p in re.finditer(r"\.(\w+)\s*\(([^()]*)\)", block):
            v = verilog_value(p.group(2))
            if v is not None:
                params[p.group(1)] = v
        break
    if not params:
        raise Refusal(f"{build}/gateware has no milan_datapath instance")
    out["datapath_parameters"] = dict(sorted(params.items()))
    return out


def soc_text(soc: dict) -> str:
    """The extract as committed: sorted keys, two-space indent, newline."""
    return json.dumps(soc, indent=2, sort_keys=True) + "\n"


def csr_parameters(root: Path, soc: dict) -> tuple[dict[str, int], list[tuple[str, str, int]]]:
    """milan_csr's parameters as the shipping datapath instantiates them:
    the datapath's defaults, overridden by the export, mapped through the
    `milan_csr #( ... )` instance. Returns the overrides and a table of
    (parameter, expression, value)."""
    text = strip_comments(read_text(root, DATAPATH))
    sym = Symbols()
    define_constants(strip_comments(read_text(root, ETH_PKG)), sym)
    header = define_header_parameters(text, "milan_datapath", sym)
    for name, value in soc["datapath_parameters"].items():
        if name in header:
            sym.overrides[name] = value
    body = text[text.index(");", text.index("module milan_datapath")):]
    shape_inc = f"{SHAPE_INCLUDE_DIR.format(shape=soc['shape'])}/gen/adp_shape_defaults.svh"
    define_constants(strip_comments(read_text(root, shape_inc)), sym)
    define_constants(body, sym)
    m = re.search(r"\bmilan_csr\s*#\s*\(", body)
    if not m:
        raise Refusal(f"{DATAPATH} instantiates no milan_csr")
    block = body[m.end():matching(body, m.end() - 1, "(", ")")]
    overrides, table = {}, []
    for p in re.finditer(r"\.(\w+)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)", block):
        expr = " ".join(p.group(2).split())
        try:
            value = Expr(expr, sym).value()[0]
        except Refusal:
            continue
        overrides[p.group(1)] = value
        table.append((p.group(1), expr, value))
    return overrides, table


