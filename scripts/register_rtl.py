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

from register_sv import (WORD_BITS, Assign, Case, For, If, Node, Refusal, Scope, Statement, Vec, const_vec, evaluate,
                         parse_expression, parse_number, parse_statements, unparse)

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


class ConstScope(Scope):
    """Constants only: a signal in a constant expression is a refusal."""

    def __init__(self, sym: "Symbols") -> None:
        self.sym = sym

    def lookup(self, name: str) -> Vec | list[Vec]:
        """A constant's value, or an element list for a constant table."""
        if name in self.sym.arrays:
            return self.sym.arrays[name]
        return self.sym.resolve(name)


class Expr:
    """A constant expression: `value()` is its (value, declared width)."""

    def __init__(self, text: str, symbols: "Symbols") -> None:
        self.text = text
        self.sym = symbols

    def value(self) -> tuple[int, int | None]:
        """Evaluate to (value, width); the width is None when unsized."""
        v = evaluate(parse_expression(self.text), ConstScope(self.sym))
        if v.unknown:
            raise Refusal(f"{self.text!r} is not a constant")
        return v.value, (v.width if v.sized else None)


class Symbols:
    """Parameters, localparams and declared widths, resolved lazily."""

    def __init__(self) -> None:
        self.exprs: dict[str, str] = {}
        self.decl_width: dict[str, int | str] = {}
        self.cache: dict[str, Vec] = {}
        self.overrides: dict[str, int] = {}
        self.arrays: dict[str, list[Vec]] = {}

    def define(self, name: str, expr: str, width: int | str | None = None) -> None:
        """Record a constant's defining expression (first definition wins)."""
        self.exprs.setdefault(name, expr)
        if width is not None:
            self.decl_width.setdefault(name, width)

    def has(self, name: str) -> bool:
        """Whether a constant of that name is known."""
        return name in self.overrides or name in self.exprs

    def resolve(self, name: str) -> Vec:
        """A constant's value at its declared width."""
        if name in self.overrides:
            width = self.width(name)
            return const_vec(self.overrides[name], width or WORD_BITS, width is not None)
        if name not in self.cache:
            if name not in self.exprs:
                raise Refusal(f"unknown constant {name}")
            self.cache[name] = const_vec(0)       # guards a self-reference
            v = evaluate(parse_expression(self.exprs[name]), ConstScope(self))
            width = self.width(name)
            self.cache[name] = v.resized(width) if width is not None else v
        return self.cache[name]

    def value(self, name: str) -> int:
        """The constant's value."""
        return self.resolve(name).value

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


# ------------------------------------------------------------------ the model --
@dataclass
class RtlFacts:
    """Everything the generator reads out of milan_csr.sv and its includes."""
    sym: Symbols
    addresses: dict[str, int]                  # A_* label -> offset
    params: dict[str, int]
    write_arms: dict[str, list[tuple[str, list[Statement]]]]   # label -> [(block, statements)]
    read_blocks: dict[str, list[Statement]]    # read_mux, pp_read, strm_read_mux
    rom: list[Statement]                       # csr_default's body
    plain_rw: list[Statement]                  # is_plain_rw's body
    resets: dict[str, Node]                    # storage -> reset value
    array_resets: dict[str, Node]              # unpacked storage -> element reset value
    assigns: dict[str, Node]                   # assign target -> value
    signals: dict[str, int]                    # declared signal widths
    version: int
    arrays: set[str]
    read_loaded: set[str]                      # flops a read loads from an input before returning them
    usage: dict[str, set[int] | None]          # every read of a storage bit, a disabled build's excluded
    logic_usage: dict[str, set[int] | None]    # the same without the read decodes and the write merges
    text: str
    body: str
    wires: dict[str, Node]


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


#: Every top-level site of the RTL that reads the CSR bus. An `always` block is
#: `always:<name>`, a declaration or assign is `wire:<name>`. The two write
#: blocks and the three read blocks are parsed; each other site is either
#: consumed below or has no register-visible effect. A site not listed is
#: refused: it is a decode this generator does not read.
KNOWN_BUS_SITES = frozenset({
    "always:register_write", "always:pp_regs", "always:read_mux", "always:pp_read", "always:strm_read_mux",
    "always:axi_resp_fsm", "always:gptp_live_read_snapshot", "always:shadow_mem", "always:strm_slow_rd_S",
    "always:strm_srp_master_S",
    "wire:wr_fire", "wire:rd_fire", "wire:wr_addr", "wire:rd_addr", "wire:rd_win_w", "wire:rd_is_slow_w",
    "wire:s_axi_awready", "wire:s_axi_wready", "wire:s_axi_arready",
    "wire:is_cbs_en_wr", "wire:shadow_wval", "wire:win_alias_ctrl_w", "wire:win_alias_dmlo_w",
    "wire:win_alias_dmhi_w",
    "wire:shadow_axi_we", "wire:sh_waddr", "wire:sh_wdata", "wire:cmrd_go_w", "wire:snap_go_w", "wire:sel_wr_w",
    "wire:srp_prov_w", "wire:rd_in_window", "wire:pp_nvm_rd_w", "wire:o_pp_nvm_csr_addr",
})
BUS_SIGNAL_RE = re.compile(r"\b(wr_fire|wr_addr|rd_fire|rd_addr|rd_addr_q|s_axi_wdata)\b")
DECLARATION_RE = re.compile(r"\b(?:wire|assign)\s*(?:\[[^\]]*\])?\s*(\w+)\s*=[^;]*;", re.S)
ALWAYS_RE = re.compile(r"\balways_(?:ff|comb)\b[^;]*?\bbegin\b(?:\s*:\s*(\w+))?", re.S)


def bus_sites(body: str) -> dict[str, int]:
    """site -> first offset, for every place the module body reads the bus."""
    spans: list[tuple[int, int, str]] = []
    for m in ALWAYS_RE.finditer(body):
        begin = body.index("begin", m.start())
        spans.append((m.start(), begin + len(balanced(body, begin)),
                      f"always:{m.group(1) or 'anonymous@' + str(body.count(chr(10), 0, m.start()) + 1)}"))
    for m in DECLARATION_RE.finditer(body):
        if not any(a <= m.start() < b for a, b, _ in spans):
            spans.append((m.start(), m.end(), f"wire:{m.group(1)}"))
    for m in re.finditer(r"\blogic\b[^;=]*;", body):
        if not any(a <= m.start() < b for a, b, _ in spans):
            spans.append((m.start(), m.end(), "declaration"))
    found: dict[str, int] = {}
    for m in BUS_SIGNAL_RE.finditer(body):
        site = next((name for a, b, name in spans if a <= m.start() < b), None)
        if site is None:
            line = body.count("\n", 0, m.start()) + 1
            site = f"statement@{line}"
        found.setdefault(site, m.start())
    return found


def without_disabled_terms(body: str, params: dict[str, str], sym: Symbols) -> str:
    """The body with every `x & PARAM` term blanked where the parameter is 0:
    such a bit reaches nothing in this build."""
    def blank(m: re.Match) -> str:
        """Blank one term when its enabling parameter is 0."""
        return " " * len(m.group(0)) if sym.value(m.group(2)) == 0 else m.group(0)
    declarations = re.sub(r"\blogic\b[^;=]*;", lambda m: " " * len(m.group(0)), body)
    return re.sub(r"(\w+(?:\[[^\]]*\])?)\s*&\s*(" + "|".join(params) + r")\b(?!\s*\[)", blank, declarations)


def logic_text(body: str) -> str:
    """The body without the read decodes, the shadow mux and the write-merge
    images: what remains reads a stored bit because logic consumes it."""
    out = body
    for name in ("read_mux", "pp_read", "strm_read_mux"):
        m = re.search(r"always_comb\s+begin\s*:\s*" + name + r"\b", out)
        if m:
            start = out.index("begin", m.start())
            end = start + len(balanced(out, start))
            out = out[:m.start()] + " " * (end - m.start()) + out[end:]
    return re.sub(r"\{\s*\w+\[31:\d+\]\s*,\s*s_axi_wdata\[\d+(?::\d+)?\]\s*\}", " ", out)


def block_statements(text: str, keyword: str, name: str) -> list[Statement]:
    """The parsed statements of the named `always_*` block."""
    block = find_block(text, r"always_" + keyword + r"\b[^;]*?\bbegin\s*:\s*" + name + r"\b")
    return parse_statements(block)


def function_statements(text: str, name: str) -> list[Statement]:
    """The parsed body of a function, its header removed."""
    m = re.search(r"\bfunction\s+automatic\b[^;]*\b" + name + r"\s*\([^;]*;", text)
    if not m:
        raise Refusal(f"{RTL}: no function {name}")
    return parse_statements(text[m.end():text.index("endfunction", m.end())])


def find_case(statements: list[Statement], selector: str) -> Case | None:
    """The first `case (selector)` in a statement tree, depth first."""
    for st in statements:
        if isinstance(st, Case):
            if st.selector == ("id", selector):
                return st
            nested = find_case([s for _, body in st.items for s in body] + st.default, selector)
        elif isinstance(st, If):
            nested = find_case(st.then + st.other, selector)
        else:
            nested = None
        if nested:
            return nested
    return None


def reset_clauses(text: str) -> tuple[dict[str, Node], dict[str, Node]]:
    """storage -> reset value tree, and the same for unpacked arrays, from
    every `if (!aresetn)` clause. A reset statement outside this grammar is
    refused rather than read as no reset."""
    resets: dict[str, Node] = {}
    arrays: dict[str, Node] = {}
    for m in re.finditer(r"if\s*\(\s*!aresetn\s*\)\s*", text):
        end = statement_end(text, m.end())
        for st in parse_statements(text[m.end():end]):
            _reset_statement(st, resets, arrays)
    return resets, arrays


def _reset_statement(st: Statement, resets: dict[str, Node], arrays: dict[str, Node]) -> None:
    """One statement of a reset clause."""
    if isinstance(st, Assign) and not st.selects:
        resets.setdefault(st.target, st.value)
    elif isinstance(st, For) and len(st.body) == 1 and isinstance(st.body[0], Assign) and st.body[0].selects:
        arrays.setdefault(st.body[0].target, st.body[0].value)
    else:
        raise Refusal(f"{RTL}: a reset clause holds a statement this generator cannot read: {st}")


def read_loaded_flops(statements: list[Statement]) -> set[str]:
    """Flops a block loads directly from an input port. The read that fires
    the block returns the loaded value, so the reset value never shows."""
    found: set[str] = set()
    for st in statements:
        if isinstance(st, If):
            found |= read_loaded_flops(st.then) | read_loaded_flops(st.other)
        elif isinstance(st, Assign) and st.value[0] == "id" and st.value[1].startswith("i_"):
            found.add(st.target)
    return found


def named_labels(case: Case, block: str) -> list[tuple[str, list[Statement]]]:
    """(label, body) of every item of a decode. A label that is not an `A_*`
    name is a decoded word with no register name, and is refused."""
    out = []
    for labels, body in case.items:
        for label in labels:
            if label[0] != "id" or not label[1].startswith("A_"):
                raise Refusal(f"{RTL}: {block} decodes {unparse(label)}, which is not an A_* register")
            out.append((label[1], body))
    return out


def decode_write_arms(text: str) -> dict[str, list[tuple[str, list[Statement]]]]:
    """label -> [(block, statements)] of both write decodes."""
    arms: dict[str, list[tuple[str, list[Statement]]]] = {}
    for block_name in ("register_write", "pp_regs"):
        case = find_case(block_statements(text, "ff", block_name), "wr_addr")
        if case is None:
            raise Refusal(f"{RTL}: {block_name} has no case (wr_addr)")
        for label, body in named_labels(case, block_name):
            arms.setdefault(label, []).append((block_name, body))
    return arms


def decode_read_blocks(text: str) -> dict[str, list[Statement]]:
    """The three read decodes, each case label checked for a register name."""
    blocks = {name: block_statements(text, "comb", name) for name in ("read_mux", "pp_read", "strm_read_mux")}
    for name, statements in blocks.items():
        case = find_case(statements, "rd_addr_q")
        if case is None:
            raise Refusal(f"{RTL}: {name} has no case (rd_addr_q)")
        named_labels(case, name)
    return blocks


def constant_tables(text: str, sym: Symbols) -> None:
    """The unpacked constant tables (`'{...}`), which the shadow defaults index."""
    for m in re.finditer(r"localparam\s+int\s+(\w+)\s*\[0:\d+\]\s*=\s*'\{([^}]*)\}", text):
        sym.arrays[m.group(1)] = [const_vec(int(v.strip().replace("_", ""))) for v in m.group(2).split(",")]


def load_rtl(root: Path, shape: str, overrides: dict[str, int]) -> RtlFacts:
    """Read milan_csr.sv, its two generated includes and the parameters the
    shipping build passes, into one set of facts."""
    text = strip_comments(read_text(root, RTL))
    sym = Symbols()
    define_constants(strip_comments(read_text(root, ETH_PKG)), sym)
    for inc in re.findall(r'`include\s+"([^"]+)"', text):
        candidates = [f"{CSR_INCLUDE_DIR}/{inc}", f"{SHAPE_INCLUDE_DIR.format(shape=shape)}/{inc}"]
        path = next((c for c in candidates if (root / c).is_file()), None)
        if path is None:
            raise Refusal(f"{RTL} includes {inc}, found in neither {candidates}")
        define_constants(strip_comments(read_text(root, path)), sym)
    params = define_header_parameters(text, "milan_csr", sym)
    body_start = text.index(");", text.index("module milan_csr"))
    body = text[body_start:]
    define_constants(body, sym)
    constant_tables(text, sym)
    for name, value in overrides.items():
        if name not in params:
            raise Refusal(f"the SoC extract overrides {name}, which milan_csr.sv does not declare")
        sym.overrides[name] = value
    declared, arrays = declared_signals(text, sym)
    for name, rng in declared.items():
        sym.decl_width.setdefault(name, rng)
    addresses = {}
    for m in re.finditer(r"\b(A_\w+)\s*=\s*([^,;]+)", text):
        if m.group(1) not in addresses:
            addresses[m.group(1)] = Expr(m.group(2).strip(), sym).value()[0]
    signals = {}
    for name in list(sym.decl_width):
        try:
            w = sym.width(name)
        except Refusal:
            continue
        if w is not None:
            signals[name] = w
    storage = {n for n in signals if not n.startswith(("i_", "o_"))}
    effective = without_disabled_terms(body, params, sym)
    wires = {w.group(1): parse_expression(" ".join(w.group(2).split())) for w in
             re.finditer(r"\bwire\s*(?:\[[^\]]+\])?\s*(\w+)\s*=\s*([^;]+);", body)}
    assigns = {m.group(1): parse_expression(" ".join(m.group(2).split()))
               for m in re.finditer(r"\bassign\s+(\w+)\s*=\s*([^;]+);", body)}
    resets, array_resets = reset_clauses(body)
    loaded = read_loaded_flops(block_statements(text, "ff", "gptp_live_read_snapshot"))
    sites = bus_sites(body)
    unknown = sorted(set(sites) - KNOWN_BUS_SITES - {"declaration"})
    if unknown:
        raise Refusal(f"{RTL}: the CSR bus is read at {unknown}, which this generator does not read")
    return RtlFacts(sym, addresses, {name: sym.value(name) for name in params}, decode_write_arms(text),
                    decode_read_blocks(text), function_statements(text, "csr_default"),
                    function_statements(text, "is_plain_rw"), resets, array_resets, assigns, signals,
                    sym.value("VERSION"), arrays, loaded, bit_usage(effective, storage, sym),
                    bit_usage(logic_text(effective), storage, sym), text, body, wires)


# ------------------------------------------------------------- the SoC side --
def verilog_value(text: str) -> int | None:
    """An integer Verilog literal as LiteX writes it (`26'd50000000`), or
    None for a string or anything else."""
    text = text.strip()
    if text.startswith('"'):
        return None
    try:
        return parse_number(text).value
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
    for inc in re.findall(r'`include\s+"([^"]+)"', text):
        path = f"{SHAPE_INCLUDE_DIR.format(shape=soc['shape'])}/{inc}"
        if (root / path).is_file():
            define_constants(strip_comments(read_text(root, path)), sym)
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
