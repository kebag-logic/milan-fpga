#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Per-bit field derivation for the register reference generator (#797).

Turns the facts `register_rtl.py` reads into registers with fields: what a
read returns at each bit, what a write does there, which RTL name the bit
carries and its reset value. Nothing here is hand-kept register data. A write
or read form outside the grammar is refused, so a field is never published as
read-only because its write arm could not be read.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from register_decode import RANGE_ARRAYS, WINDOW_BOUNDS, ReadModel, ResetScope, SymbolicScope, zero_node
from register_rtl import RTL, RtlFacts, find_case
from register_sv import (WORD_BITS, Assign, Case, For, If, Interpreter, Node, Refusal, Statement, Vec, evaluate,
                         mentions, parse_expression, unparse)

# -------------------------------------------------------------- derivation --
#: Access codes, in the order the legend lists them.
ACCESS_LEGEND = (
    ("R", "Read-only. Writes are ignored."),
    ("W", "Write-only. The written value is used; a read returns 0."),
    ("R/W", "Read and write. A read returns the stored value."),
    ("W1C", "Write 1 to clear. Writing 0 has no effect."),
    ("R/W1C", "A read returns the latched bit; writing 1 clears it."),
    ("W1S", "Write 1 to trigger a one-cycle action. The bit self-clears and reads 0."),
    ("R/W1S", "A read returns the bit's status; writing 1 triggers the action."),
    ("RC", "Read clears. No register of this block clears on read."),
    ("WO", "Write-only word whose write is the action. This block shows such words as W."),
)
#: Reset column codes beyond a hex value.
RESET_LEGEND = (
    ("X", "This block's reset does not fix the bit: an input or an unreset flop sets it."),
)
WDATA = "s_axi_wdata"
FORM_REFUSAL = "a write form this generator cannot read"


@dataclass
class Bit:
    """What one bit of one register does on a read and on a write."""
    read: str = "zero"          # zero, stored, signal, const, complex
    read_name: str = ""
    read_value: int | None = 0
    write: str = "none"         # none, stored, w1c, w1c_any, strobe, magic
    write_name: str = ""
    notes: list[str] = field(default_factory=list)


@dataclass
class Field:
    """A run of bits that share one name and one behaviour."""
    hi: int
    lo: int
    name: str
    access: str
    reset: str                  # hex digits, "X", or "0"
    notes: list[str] = field(default_factory=list)
    span: str = ""              # the slice of a wider RTL value, e.g. [47:32]

    @property
    def bits(self) -> str:
        """`[h:l]` or `[b]` as the field table prints it."""
        return f"{self.hi}" if self.hi == self.lo else f"{self.hi}:{self.lo}"


@dataclass
class Effect:
    """A statement of a write arm beyond storing the written value."""
    target: str
    action: str                 # sets, clears, counts, loads
    conds: tuple = ()           # (condition node, polarity) pairs
    trigger: int | None = None  # the written bit that fires it, if one does


@dataclass
class Register:
    """One addressable word, or one array of identical words."""
    label: str                  # RTL label without the A_ prefix
    offset: int
    fields: list[Field] = field(default_factory=list)
    reset: str = ""
    count: int = 1
    stride: int = 4
    array_resets: list[int | None] | None = None
    side_effects: list[str] = field(default_factory=list)
    effects: list[Effect] = field(default_factory=list)
    views: list[tuple[tuple, Node]] = field(default_factory=list)
    rtl_range: str = ""
    sources: dict[int, str] = field(default_factory=dict)  # word bit -> RTL signal bit it holds
    reset_bits: list[int | None] = field(default_factory=list)  # per-bit reset, LSB first

    @property
    def rtl_label(self) -> str:
        """The label as the RTL spells it."""
        return "A_" + self.label

    @property
    def rtl_name(self) -> str:
        """What the page cites as the RTL source: the label, or for an
        array the range labels the read decode uses."""
        return self.rtl_range or self.rtl_label


@dataclass
class Term:
    """What one bit of a value is: a constant, one signal bit, or logic."""
    kind: str                   # const, sig, word, expr
    name: str = ""              # signal or array name; a constant's field name
    idx: int = 0
    hi: int = 0
    lo: int = 0
    value: int = 0
    text: str = ""
    ors: tuple = ()

    def rtl(self) -> str:
        """The bit as RTL text."""
        if self.kind == "const":
            return f"1'b{self.value}"
        if self.kind == "sig":
            return f"{self.name}[{self.idx}]"
        return self.text


def field_name(signal: str) -> str:
    """An RTL signal or constant name as a field name: the port direction
    prefix and the register/wire/constant suffix dropped, upper case."""
    name = re.sub(r"^(i|o)_", "", signal)
    name = re.sub(r"_(r|w|q|p|c|C|qq)$", "", name)
    return name.upper()


def conj(conds: tuple) -> str:
    """Conditions as one RTL expression, a false polarity spelled with `!`."""
    parts = []
    for node, polarity in conds:
        if polarity:
            parts.append(unparse(node))
        elif node[0] == "un" and node[1] == "!":
            parts.append(unparse(node[2]))
        elif node[0] == "id" or node[0] == "index":
            parts.append("!" + unparse(node))
        else:
            parts.append(f"!({unparse(node)})")
    return " && ".join(parts)


def _const_terms(v: Vec, label: str = "") -> list[Term]:
    """The bits of a known or partly known constant, LSB first."""
    width = v.width if v.sized else WORD_BITS
    return [Term("const", label, value=v.bit(k) or 0) for k in range(width)]


class Deriver:
    """Turns the RTL facts into registers with fields."""

    def __init__(self, facts: RtlFacts, literal_words: dict[int, str] | None = None) -> None:
        self.f = facts
        self.sym = facts.sym
        self.model = ReadModel(facts)
        self.scope = SymbolicScope(facts, {})
        self.literal_words = dict(literal_words or {})
        self.consumers = self._consumers()
        self.extra_strobes = self._extra_strobes()
        self.setters = self._setters()

    def is_constant_name(self, name: str) -> bool:
        """Whether a name is a parameter, a localparam or a constant table."""
        return self.sym.has(name) or name in self.sym.arrays

    # ---- bit terms ----------------------------------------------------------
    def bit_terms(self, node: Node) -> list[Term]:
        """What each bit of a value is, LSB first, with constants folded."""
        kind = node[0]
        if kind in ("num", "vec"):
            return _const_terms(node[1])
        if kind == "id":
            return self._id_terms(node[1])
        if kind in ("index", "range", "ipart"):
            return self._select_terms(node)
        if kind == "concat":
            return [t for part in reversed(node[1]) for t in self.bit_terms(part)]
        if kind == "cast":
            width = evaluate(node[1], self.scope).value
            inner = self.bit_terms(node[2])
            pad = [Term("const")] * max(0, width - len(inner))
            return (inner + pad)[:width]
        if kind == "bin" and node[1] in ("&", "|"):
            return self._bitwise_terms(node)
        return self._expr_terms(node)

    def _expr_terms(self, node: Node) -> list[Term]:
        """A value that is logic over several signals, bit by bit."""
        value = evaluate(node, self.scope)
        if value.known:
            return _const_terms(value)
        text = unparse(node)
        width = value.width
        return [Term("expr", text=f"({text})[{k}]" if width > 1 else text, idx=k) for k in range(width)]

    def _id_terms(self, name: str) -> list[Term]:
        """A whole name: a constant, a wire built by concatenation, a signal."""
        if self.is_constant_name(name):
            return _const_terms(self.sym.resolve(name), field_name(name))
        definition = self.f.wires.get(name)
        if definition is not None and definition[0] == "concat":
            return self.bit_terms(definition)
        width = self.f.signals.get(name)
        if width is None:
            raise Refusal(f"{RTL}: {name} has no declaration this generator can read")
        return [Term("sig", name, k, width - 1, 0) for k in range(width)]

    def _select_terms(self, node: Node) -> list[Term]:
        """x[i], x[h:l] or x[s +: w] of a signal, a table or an array element."""
        base = node[1]
        if base[0] != "id":
            return self._expr_terms(node)
        name = base[1]
        if self.is_constant_name(name):
            return _const_terms(evaluate(node, self.scope), field_name(name))
        if name in self.f.arrays and node[0] == "index":
            width = self.f.signals.get(name, WORD_BITS)
            return [Term("word", name, k, width - 1, 0, text=f"{unparse(node)}[{k}]") for k in range(width)]
        if node[0] == "index":
            index = evaluate(node[2], self.scope)
            if index.unknown:
                return self._expr_terms(node)
            hi = lo = index.value
        elif node[0] == "range":
            a, b = evaluate(node[2], self.scope).value, evaluate(node[3], self.scope).value
            hi, lo = max(a, b), min(a, b)
        else:
            start, width_v = evaluate(node[2], self.scope), evaluate(node[3], self.scope).value
            if start.unknown:
                return self._expr_terms(node)
            lo, hi = start.value, start.value + width_v - 1
        return [Term("sig", name, k, hi, lo) for k in range(lo, hi + 1)]

    def _bitwise_terms(self, node: Node) -> list[Term]:
        """x & y or x | y, a constant operand folding each bit it decides."""
        op = node[1]
        left, right = self.bit_terms(node[2]), self.bit_terms(node[3])
        width = max(len(left), len(right))
        left += [Term("const")] * (width - len(left))
        right += [Term("const")] * (width - len(right))
        out = []
        for a, b in zip(left, right):
            out.append(self._and_bit(a, b) if op == "&" else self._or_bit(a, b))
        return out

    @staticmethod
    def _and_bit(a: Term, b: Term) -> Term:
        """One bit of an AND."""
        for x, y in ((a, b), (b, a)):
            if x.kind == "const":
                return y if x.value else Term("const")
        return Term("expr", text=f"{a.rtl()} & {b.rtl()}")

    @staticmethod
    def _or_bit(a: Term, b: Term) -> Term:
        """One bit of an OR; two signals keep the later one's name."""
        for x, y in ((a, b), (b, a)):
            if x.kind == "const":
                return Term("const", value=1) if x.value else y
        if a.kind == "sig" and b.kind == "sig":
            return Term("sig", b.name, b.idx, b.hi, b.lo, ors=a.ors + (field_name(a.name),))
        return Term("expr", text=f"{a.rtl()} | {b.rtl()}")

    # ---- naming helpers --------------------------------------------------
    def _consumers(self) -> dict[str, list[tuple[int, int, str, str]]]:
        """storage -> [(hi, lo, output field, span note)] from the assigns."""
        out: dict[str, list[tuple[int, int, str, str]]] = {}
        ip = Interpreter(self.scope)
        for port, value in self.f.assigns.items():
            if not port.startswith("o_"):
                continue
            name = field_name(port)
            rhs = ip.reduce(value)
            if rhs[0] == "tern":
                self._consume_choice(rhs, name, out)
                continue
            parts = rhs[1] if rhs[0] == "concat" else [rhs]
            terms = [self.bit_terms(p) for p in parts]
            top = sum(len(t) for t in terms) - 1
            for part_terms in terms:
                lo_out = top - len(part_terms) + 1
                span = f"[{top}:{lo_out}]" if len(parts) > 1 else ""
                top = lo_out - 1
                self._consume_part(part_terms, name, span, out)
        return out

    def _consume_choice(self, rhs: Node, name: str, out: dict) -> None:
        """o = s[n] ? t[m] : other: the select and the chosen bit are named."""
        for node, suffix in ((rhs[1], "_SELECT"), (rhs[2], "")):
            if node[0] == "index" and node[1][0] == "id":
                bit = evaluate(node[2], self.scope).value
                out.setdefault(node[1][1], []).append((bit, bit, name + suffix, ""))

    def _consume_part(self, terms: list[Term], name: str, span: str, out: dict) -> None:
        """One slice of a signal that drives an output port."""
        sigs = [t for t in terms if t.kind == "sig"]
        if not sigs or len(sigs) != len(terms) or len({t.name for t in sigs}) != 1:
            return
        sig = sigs[0].name
        if sig in self.f.assigns or sig not in self.f.signals or sig.startswith(("i_", "o_")):
            return
        out.setdefault(sig, []).append((sigs[-1].idx, sigs[0].idx, name, span))

    def _extra_strobes(self) -> dict[str, list[tuple[int, str]]]:
        """label -> [(bit, name)] for `wire x = wr_fire && (wr_addr == A_Y)
        && s_axi_wdata[n]` decodes outside the write case."""
        out: dict[str, list[tuple[int, str]]] = {}
        for m in re.finditer(r"wire\s+(\w+)\s*=\s*wr_fire\s*&&\s*\(wr_addr\s*==\s*(A_\w+)\)\s*&&\s*"
                             r"s_axi_wdata\[(\d+)\]", self.f.text):
            out.setdefault(m.group(2), []).append((int(m.group(3)), field_name(m.group(1))))
        return out

    def _setters(self) -> dict[str, dict[int, str]]:
        """storage -> {bit: name} for `if (i_x) storage[n] <= 1'b1;`, the
        hardware event that latches a status bit."""
        out: dict[str, dict[int, str]] = {}
        for m in re.finditer(r"if\s*\((i_\w+)\)\s*(\w+)\[(\d+)\]\s*<=\s*1'b1\s*;", self.f.text):
            out.setdefault(m.group(2), {})[int(m.group(3))] = field_name(m.group(1))
        return out

    def name_term(self, term: Term) -> tuple[str, str]:
        """(field name, span note) for one signal bit of a read value. A port
        or constant names the whole term. A storage register names each bit
        by the output port that bit drives; a stored bit that drives nothing
        is RESERVED when other bits of the same register do drive something,
        and takes the register's own name otherwise."""
        sig = term.name
        if sig.startswith(("i_", "o_")) or self.sym.has(sig):
            width = self.f.signals.get(sig) or self.sym.width(sig) or WORD_BITS
            hi, lo = term.hi, term.lo
            span = "" if (hi, lo) == (width - 1, 0) else (f"[{hi}:{lo}]" if hi != lo else f"[{hi}]")
            return field_name(sig), span
        name, span, _ = self.storage_naming(sig, term.idx)
        return name, span

    def storage_naming(self, sig: str, bit: int) -> tuple[str, str, str]:
        """(name, span, kind): kind is `setter` (a hardware event latches
        the bit), `consumer` (the bit drives an output port), `own` (the
        storage's own name) or `reserved` (stored, read by nothing)."""
        setters = self.setters.get(sig, {})
        if bit in setters:
            return setters[bit], "", "setter"
        width = self.f.signals.get(sig, WORD_BITS)
        if width < WORD_BITS and sig.endswith("_r") and self.used(sig, bit):
            return field_name(sig), "", "own"
        consumers = self.consumers.get(sig, [])
        for c_hi, c_lo, name, span in consumers:
            if c_lo <= bit <= c_hi:
                if span:
                    top = int(span[1:-1].split(":")[0])
                    off = top - c_hi
                    span = f"[{c_hi + off}:{c_lo + off}]" if c_hi != c_lo else f"[{c_hi + off}]"
                return name, span, "consumer"
        if setters or consumers:
            return "RESERVED", "", "reserved"
        return field_name(sig), "", "own"

    def check_reserved(self, sig: str, bit: int) -> None:
        """A bit the page calls reserved must drive nothing: a reader the
        generator cannot name is refused, never printed as `drives nothing`."""
        bits = self.f.logic_usage.get(sig, set())
        if bits is None or bit in bits:
            raise Refusal(f"{RTL}: {sig}[{bit}] is read by logic this generator cannot name, "
                          "so it cannot be called reserved")

    def used(self, sig: str, bit: int) -> bool:
        """Whether some expression of the RTL reads bit `bit` of `sig`."""
        if sig not in self.f.usage:
            return False
        bits = self.f.usage[sig]
        return bits is None or bit in bits

    # ---- read side -------------------------------------------------------
    def read_bits(self, addr: int, bits: list[Bit], reg: Register) -> None:
        """Fill the read half of every bit of a word from what a read can
        return. One value names the bits; several live values leave one word."""
        views = self.model.views(addr)
        reg.views = views if len(views) > 1 else []
        live = [leaf for _, leaf in views if not self._is_const(leaf)]
        if not live:
            if len(views) == 1:
                self.attribute(views[0][1], bits)
            else:
                for b in bits:
                    b.read, b.read_name, b.read_value = "complex", "", None
            return
        if len(live) > 1:
            for b in bits:
                b.read, b.read_name, b.read_value = "complex", "", None
            return
        if live[0] == ("id", "shadow_q"):
            if self.model.plain(addr):
                for b in bits:
                    b.read = "stored"
            elif self.model.rom_value(addr).value:
                self.attribute(self.model.rom_tree(addr), bits, const=True)
            return
        self.attribute(live[0], bits)

    def _is_const(self, leaf: Node) -> bool:
        """Whether a read value is fixed whatever the state."""
        return evaluate(leaf, SymbolicScope(self.f, {"shadow_q": Vec(WORD_BITS, 0, (1 << WORD_BITS) - 1)})).known

    def attribute(self, node: Node, bits: list[Bit], const: bool = False) -> None:
        """Bit-by-bit sources of a read value, parts named one at a time."""
        parts = node[1] if node[0] == "concat" else [node]
        pos = 0
        for part in reversed(parts):
            terms = self.bit_terms(part)
            label = self._const_label(part, node[0] == "concat", const, (pos + len(terms) - 1, pos))
            for k, term in enumerate(terms):
                if pos + k < WORD_BITS:
                    self._set_read(bits[pos + k], term, label, pos + k)
            pos += len(terms)
        if pos > WORD_BITS:
            raise Refusal(f"{RTL}: a read of {pos} bits does not fit one word: {unparse(node)}")

    def _const_label(self, part: Node, in_concat: bool, const: bool, span: tuple[int, int]) -> str:
        """The field name of a constant part of a read value."""
        inner = part[2] if part[0] == "cast" else part
        if inner[0] == "id" and self.is_constant_name(inner[1]):
            return field_name(inner[1])
        if not in_concat:
            return "@WORD"
        value = evaluate(part, self.scope)
        hi, lo = span
        if const and value.known and not (value.value == 0 and hi - lo + 1 >= 4):
            return f"BIT{lo}" if hi == lo else f"BITS{hi}_{lo}"
        return ""

    def _set_read(self, b: Bit, term: Term, label: str, n: int) -> None:
        """One bit of a read value."""
        if term.kind == "const":
            b.read, b.read_value, b.read_name = "const", term.value, term.name or label
            return
        b.read, b.read_value = "signal", None
        if term.kind == "word":
            b.read_name = "@WORD"
            b.notes.append(f"src:{term.text}")
        elif term.kind == "expr":
            b.read_name = f"BIT{n}"
            b.notes.append(f"expr:{term.text}")
        else:
            name, span = self.name_term(term)
            b.read_name = name
            b.notes.append(f"src:{term.name}[{term.idx}]")
            if span:
                b.notes.append(f"span:{span}")
            b.notes += [f"or:{other}" for other in term.ors]

    # ---- write side ------------------------------------------------------
    def write_bits(self, label: str, bits: list[Bit], reg: Register) -> None:
        """Fill the write half of every bit of `label` from its write arms."""
        arms = self.f.write_arms.get(label, [])
        addr = self.f.addresses.get(label, reg.offset)
        for bit, name in self.extra_strobes.get(label, []):
            bits[bit].write, bits[bit].write_name = "strobe", name
        for _, body in arms:
            self.walk_arm(body, bits, reg, ())
        if self.model.plain(addr):
            for b in bits:
                if b.write == "none":
                    b.write = "stored"

    def walk_arm(self, statements: list[Statement], bits: list[Bit], reg: Register, conds: tuple) -> None:
        """Every statement of one write arm; any other form is refused."""
        for st in statements:
            if isinstance(st, If):
                self.write_if(st, bits, reg, conds)
            elif isinstance(st, Assign):
                self.write_assign(st, bits, reg, conds)
            elif isinstance(st, For):
                self.write_loop(st, reg, conds)
            else:
                raise Refusal(f"{RTL}: a case statement inside the {reg.rtl_label} write arm is {FORM_REFUSAL}")

    def write_loop(self, st: For, reg: Register, conds: tuple) -> None:
        """A loop in a write arm: a snapshot of several words."""
        for inner in st.body:
            if not isinstance(inner, Assign) or mentions(inner.value, WDATA):
                raise Refusal(f"{RTL}: a loop in the {reg.rtl_label} write arm is {FORM_REFUSAL}")
            reg.effects.append(Effect(inner.target, "loads", conds))

    def write_if(self, st: If, bits: list[Bit], reg: Register, conds: tuple) -> None:
        """A condition in a write arm: a written bit triggers, a selected bit
        range triggers on any set bit, and anything else is a plain condition."""
        cond = st.cond
        guard = None
        trigger = cond
        if cond[0] == "bin" and cond[1] == "&&" and self._wdata_bit(cond[2]) is not None:
            trigger, guard = cond[2], cond[3]
        bit = self._wdata_bit(trigger)
        if bit is not None:
            if st.other:
                raise Refusal(f"{RTL}: an else on a written bit in {reg.rtl_label} is {FORM_REFUSAL}")
            self.write_trigger((bit, guard), st.then, bits, reg, conds)
            return
        if cond[0] == "un" and cond[1] == "|" and cond[2][0] == "range" and cond[2][1] == ("id", WDATA):
            self.write_any(cond[2], st, bits)
            return
        if mentions(cond, WDATA):
            raise Refusal(f"{RTL}: the condition {unparse(cond)} in {reg.rtl_label} is {FORM_REFUSAL}")
        self.walk_arm(st.then, bits, reg, conds + ((cond, True),))
        self.walk_arm(st.other, bits, reg, conds + ((cond, False),))

    @staticmethod
    def _wdata_bit(node: Node) -> int | None:
        """n for `s_axi_wdata[n]`, else None."""
        if node[0] == "index" and node[1] == ("id", WDATA) and node[2][0] == "num":
            return node[2][1].value
        return None

    def write_trigger(self, trigger: tuple[int, Node | None], body: list, bits: list[Bit], reg: Register,
                      conds: tuple) -> None:
        """`if (s_axi_wdata[n] [&& guard]) ...`: a W1C, a strobe or a commit."""
        bit, guard = trigger
        b = bits[bit]
        single = body[0] if len(body) == 1 and isinstance(body[0], Assign) else None
        if single is not None and guard is None and single.value[0] == "num" and not mentions(single.value, WDATA):
            one = single.value[1].value == 1
            if one and not single.selects:
                b.write, b.write_name = "strobe", self.strobe_name(single.target)
                return
            if not one and len(single.selects) == 1:
                b.write, b.write_name = "w1c", single.target
                return
            raise Refusal(f"{RTL}: the {reg.rtl_label} statement on written bit {bit} is {FORM_REFUSAL}")
        pulses = [s.target for s in body if isinstance(s, Assign) and s.value == ("num", s.value[1], "1'b1")
                  and s.target.endswith(("_p", "_pend_r"))] if body else []
        b.write = "strobe"
        b.write_name = self.strobe_name(pulses[0]) if pulses else "COMMIT"
        inner = conds + (((guard, True),) if guard is not None else ())
        before = len(reg.effects)
        self.walk_arm(body, bits, reg, inner)
        b.write = "strobe"
        fired = reg.effects[before:]
        del reg.effects[before:]
        for effect in fired:
            effect.trigger = bit
            if effect.target not in pulses[:1]:
                reg.effects.append(effect)
        if guard is not None:
            b.notes.append("cond:" + unparse(guard))

    def write_any(self, select: Node, st: If, bits: list[Bit]) -> None:
        """`if (|s_axi_wdata[h:l]) strobe <= 1'b1;`: any set bit fires it."""
        hi, lo = evaluate(select[2], self.scope).value, evaluate(select[3], self.scope).value
        single = st.then[0] if len(st.then) == 1 and isinstance(st.then[0], Assign) else None
        if single is None or st.other:
            raise Refusal(f"{RTL}: the statement on {unparse(select)} is {FORM_REFUSAL}")
        for n in range(lo, hi + 1):
            bits[n].write = "w1c_any"
            bits[n].write_name = self.strobe_name(single.target)
            bits[n].notes.append(f"any:{hi}:{lo} {bits[n].write_name}")

    def strobe_name(self, pulse: str) -> str:
        """A one-cycle strobe named by the output port it drives."""
        for port, value in self.f.assigns.items():
            if value == ("id", pulse) and port.startswith("o_"):
                return field_name(port)
        return field_name(pulse)

    def write_assign(self, st: Assign, bits: list[Bit], reg: Register, conds: tuple) -> None:
        """One non-blocking assignment in a write arm."""
        value = st.value
        if not mentions(value, WDATA):
            reg.effects.append(Effect(st.target, self._action(st), conds))
            return
        if st.selects:
            raise Refusal(f"{RTL}: the {reg.rtl_label} store to part of {st.target} is {FORM_REFUSAL}")
        if value == ("id", WDATA):
            for b in bits:
                self.store(b, st.target, conds)
            return
        if value[0] in ("index", "range") and value[1] == ("id", WDATA):
            self._store_slice(st.target, value, bits, reg, conds)
            return
        if value[0] == "bin" and value[1] == "!=" and value[2] == ("id", WDATA):
            key = evaluate(value[3], self.scope).value
            for b in bits:
                b.write, b.write_name = "magic", st.target
            reg.side_effects.append(f"magic:{key:#010x}:{st.target}")
            return
        if value[0] == "tern" and value[3] == ("id", WDATA) and value[2][0] == "concat":
            forced = self.forced_bits(value[2])
            for n, b in enumerate(bits):
                self.store(b, st.target, conds)
                if n in forced:
                    b.notes.append(f"masked:{unparse(value[1])}")
            return
        if value[0] == "concat":
            forced = self.forced_bits(value)
            for n, b in enumerate(bits):
                if n not in forced:
                    self.store(b, st.target, conds)
            return
        raise Refusal(f"{RTL}: {st.target} <= {unparse(value)} in {reg.rtl_label} is {FORM_REFUSAL}")

    def _store_slice(self, target: str, value: Node, bits: list[Bit], reg: Register, conds: tuple) -> None:
        """target <= s_axi_wdata[h:l] or [n]."""
        hi = evaluate(value[2], self.scope).value
        lo = evaluate(value[3], self.scope).value if value[0] == "range" else hi
        for n in range(lo, hi + 1):
            if target.endswith("_p"):
                bits[n].write, bits[n].write_name = "strobe", self.strobe_name(target)
            else:
                self.store(bits[n], target, conds, n - lo)

    @staticmethod
    def _action(st: Assign) -> str:
        """What a statement without the written value does to its target."""
        value = st.value
        if value[0] == "num" and value[1].known:
            return "sets" if value[1].value == 1 else "clears" if value[1].value == 0 else "loads"
        if mentions(value, st.target):
            return "counts"
        return "loads"

    def forced_bits(self, concat: Node) -> set[int]:
        """Bits of a `{s_axi_wdata[..], 1'b0, s_axi_wdata[..]}` image that a
        literal or the old value replaces; bits from the bus are not in the set."""
        parts = concat[1]
        widths = [evaluate(p, self.scope).width for p in parts]
        out, pos = set(), sum(widths) - 1
        for part, width in zip(parts, widths):
            if not mentions(part, WDATA):
                out.update(range(pos - width + 1, pos + 1))
            pos -= width
        return out

    def store(self, b: Bit, target: str, conds: tuple, target_bit: int | None = None) -> None:
        """Record that a write stores this bit into `target` (at
        `target_bit` when the arm stores a slice at an offset)."""
        if b.write in ("strobe", "w1c", "w1c_any", "magic"):
            return
        b.write, b.write_name = "stored", target
        if target_bit is not None:
            b.notes.append(f"tbit:{target_bit}")
        if conds:
            b.notes.append("cond:" + conj(conds))

    def write_effective(self, b: Bit, n: int, addr: int) -> bool:
        """Whether a stored bit can be observed: kept by the shadow RAM, or
        read by some expression of the RTL."""
        if self.model.plain(addr) or b.read == "stored":
            return True
        tbit = next((int(x[5:]) for x in b.notes if x.startswith("tbit:")), n)
        return self.used(b.write_name, tbit)

    # ---- reset -----------------------------------------------------------
    def reset_word(self, addr: int, bits: list[Bit]) -> list[int | None]:
        """Per-bit reset values: what a read returns in the reset state. A
        write-only bit shows the reset of the flop it stores into."""
        value = self.model.reset(addr)
        out: list[int | None] = [value.bit(n) for n in range(WORD_BITS)]
        for n, b in enumerate(bits):
            if b.read == "zero" and b.write == "stored" and b.write_name:
                flop = self.model.flop_reset(b.write_name)
                tbit = next((int(x[5:]) for x in b.notes if x.startswith("tbit:")), n)
                if flop is not None:
                    out[n] = flop.bit(tbit)
        return out

    # ---- assembly --------------------------------------------------------
    def register(self, label: str, addr: int) -> Register:
        """One register with its fields, derived bit by bit."""
        reg = Register(label[2:], addr)
        bits = [Bit() for _ in range(WORD_BITS)]
        self.read_bits(addr, bits, reg)
        self.write_bits(label, bits, reg)
        resets = self.reset_word(addr, bits)
        reg.fields = self.group(reg, bits, resets, addr)
        reg.reset = reset_text(resets)
        reg.reset_bits = resets
        reg.sources = self.bit_sources(bits)
        return reg

    def bit_sources(self, bits: list[Bit]) -> dict[int, str]:
        """word bit -> the signal bit it reads or stores, for naming the word
        in a condition another register's write depends on."""
        out: dict[int, str] = {}
        for n, b in enumerate(bits):
            src = next((x[4:] for x in b.notes if x.startswith("src:")), "")
            if src:
                out[n] = src
            elif b.write == "stored" and b.write_name:
                tbit = next((int(x[5:]) for x in b.notes if x.startswith("tbit:")), n)
                out[n] = f"{b.write_name}[{tbit}]"
        return out

    def group(self, reg: Register, bits: list[Bit], resets: list[int | None], addr: int) -> list[Field]:
        """Consecutive bits with one name and one access become one field."""
        rows = []
        for n in range(WORD_BITS - 1, -1, -1):
            b = bits[n]
            name, access = self.classify(reg, b, n, addr)
            if name == "@WORD":
                name = reg.label
            if (name, access) == ("RESERVED", "R/W"):
                b.notes = [x for x in b.notes if not x.startswith("span:")]
                self.check_reserved(b.write_name, next((int(x[5:]) for x in b.notes if x.startswith("tbit:")), n))
            span = next((x[5:] for x in b.notes if x.startswith("span:")), "")
            notes = sorted({x for x in b.notes
                            if x.startswith(("masked:", "cond:", "or:", "writes:", "reads:", "key", "expr:",
                                             "strobe:", "w1c:", "any:"))})
            rows.append((n, name, access, span, tuple(notes), self.source_index(b)))
        fields: list[Field] = []
        previous = None
        for n, name, access, span, notes, source in rows:
            contiguous = previous is None or source is None or source == (previous[0], previous[1] - 1)
            if fields and fields[-1].name == name and fields[-1].access == access and contiguous and \
                    fields[-1].span == span and tuple(fields[-1].notes) == notes and fields[-1].lo == n + 1:
                fields[-1].lo = n
            else:
                fields.append(Field(n, n, name, access, "", list(notes), span))
            previous = source
        for fl in fields:
            fl.reset = reset_text(resets[fl.lo:fl.hi + 1], short=True)
        return self.unique(fields)

    @staticmethod
    def source_index(b: Bit) -> tuple[str, int] | None:
        """(signal, bit) a read bit comes from, so a field never joins bits
        whose sources are not contiguous."""
        src = next((x[4:] for x in b.notes if x.startswith("src:")), "")
        m = re.fullmatch(r"(\w+)\[(\d+)\]", src)
        return (m.group(1), int(m.group(2))) if m else None

    def unique(self, fields: list[Field]) -> list[Field]:
        """Two runs with one name get their bit range appended, so every
        field name in a register is unique (the descriptions key)."""
        seen: dict[str, int] = {}
        for fl in fields:
            seen[fl.name] = seen.get(fl.name, 0) + 1
        for fl in fields:
            if seen[fl.name] > 1 and fl.name != "RESERVED":
                fl.name = f"{fl.name}_{fl.hi}" if fl.hi == fl.lo else f"{fl.name}_{fl.hi}_{fl.lo}"
        return fields

    def classify(self, reg: Register, b: Bit, n: int, addr: int) -> tuple[str, str]:
        """(field name, access code) of bit `n`."""
        r, w = b.read, b.write
        self.note_write_kind(b)
        if r == "complex":
            return reg.label, ("R" if w == "none" else "R/W")
        reads_zero = r == "zero" or (r == "const" and b.read_value == 0 and not b.read_name)
        if w == "magic":
            if reads_zero:
                b.notes.append("key")
                return "RESERVED", "R"
            return b.read_name or field_name(b.write_name), "R/W"
        if w == "strobe":
            if reads_zero:
                return b.write_name, "W1S"
            if r == "signal" and b.read_name != b.write_name and self.wide_input(b):
                b.notes.append(f"reads:{b.read_name}")
                return b.write_name, "R/W1S"
            return (b.read_name or b.write_name), "R/W1S"
        if w in ("w1c", "w1c_any"):
            return (b.read_name or field_name(b.write_name)), ("R/W1C" if not reads_zero else "W1C")
        if w == "stored" and not self.write_effective(b, n, addr):
            w = "none"
        if w == "stored":
            if r == "signal":
                src = next((x[4:] for x in b.notes if x.startswith("src:")), "")
                if src and not src.startswith(b.write_name + "["):
                    wname = self.stored_name(reg, b, n)
                    b.notes = [x for x in b.notes if not x.startswith("span:")]
                    b.notes.append(f"writes:{wname}")
                return b.read_name, "R/W"
            return self.stored_name(reg, b, n), ("R/W" if r == "stored" else "W")
        if reads_zero:
            return "RESERVED", "R"
        if r == "stored":
            return self.stored_name(reg, b, n), "R"
        return (b.read_name or reg.label), "R"

    @staticmethod
    def note_write_kind(b: Bit) -> None:
        """Record the write's action on the bit, for the field's row."""
        if b.write == "strobe":
            b.notes.append(f"strobe:{b.write_name}")
        elif b.write == "w1c":
            b.notes.append("w1c:")

    # ---- arrays ----------------------------------------------------------
    def range_register(self, base: str, name: str, end: str) -> Register:
        """An array the read decode serves by range, its fields derived from
        the first word and its resets from every word."""
        lo, hi = self.f.addresses[base], self.f.addresses[end]
        reg = self.array_shell(name, lo, ((hi - lo) // 4, 4), f"{base} to {end}")
        for fl in reg.fields:
            if fl.name == reg.label:
                fl.name = self.array_field_name(lo, reg)
        return reg

    def array_field_name(self, addr: int, reg: Register) -> str:
        """An array word's field takes the name of the array it reads."""
        for _, leaf in self.model.views(addr):
            if leaf[0] in ("index", "ipart") and leaf[1][0] == "id":
                return field_name(leaf[1][1])
        return reg.label

    def array_shell(self, name: str, lo: int, geometry: tuple[int, int], source: str) -> Register:
        """Derive one word and record the resets of all its elements."""
        count, stride = geometry
        reg = self.register("A_" + name, lo)
        reg.count, reg.stride = count, stride
        reg.rtl_range = source
        values = [self.model.reset(lo + k * stride) for k in range(count)]
        reg.array_resets = [None if v.unknown else v.value for v in values]
        unique_values = set(reg.array_resets)
        if unique_values == {None}:
            reg.reset = "0xXXXXXXXX"
        elif len(unique_values) == 1:
            reg.reset = f"0x{reg.array_resets[0]:08X}"
        else:
            reg.reset = "see table"
            for fl in reg.fields:
                if fl.name != "RESERVED":
                    fl.reset = "see table"
        return reg

    def cbs_registers(self) -> list[Register]:
        """The queue window: which words exist comes from `is_plain_rw`, what
        each word is from the table `csr_default` serves it from."""
        lo, hi = self.f.addresses["A_CBS_BASE"], self.f.addresses["A_CBS_END"]
        words: dict[str, list[int]] = {}
        for addr in range(lo, hi, 4):
            tree = self.model.rom_tree(addr)
            table = self._rom_table(tree)
            plain = self.model.plain(addr)
            if plain != (table is not None):
                raise Refusal(f"{RTL}: word 0x{addr:03X} of the CBS window: is_plain_rw says {plain}, "
                              f"and csr_default serves it from {table}")
            if table:
                words.setdefault(table, []).append(addr)
        out = []
        for table, addrs in words.items():
            stride = addrs[1] - addrs[0] if len(addrs) > 1 else 0x20
            if any(b - a != stride for a, b in zip(addrs, addrs[1:])):
                raise Refusal(f"{RTL}: the {table} words of the CBS window are not evenly spaced")
            name = re.sub(r"_RST$", "", table)
            source = f"A_CBS_BASE + 0x{addrs[0] - lo:X} + 0x{stride:X} * q ({table})"
            reg = self.array_shell(name, addrs[0], (len(addrs), stride), source)
            self.fold_shadow_mask(reg, addrs[0], name)
            out.append(reg)
        return out

    def fold_shadow_mask(self, reg: Register, addr: int, name: str) -> None:
        """The shadow write image: `shadow_wval` stores bits for one word."""
        known = const_vec_addr(addr, self.model.addr_bits)
        ip = Interpreter(SymbolicScope(self.f, {"wr_addr": known}), {"wr_addr": ("vec", known)})
        image = ip.reduce(self.f.wires["shadow_wval"])
        forced = self.forced_bits(image) if image[0] == "concat" else set()
        kept = [n for n in range(WORD_BITS) if n not in forced]
        hi, lo = max(kept), min(kept)
        resets = reg.array_resets or []
        word = Field(hi, lo, name, "R/W", "see table" if reg.reset == "see table" else reset_text(
            [(resets[0] or 0) >> k & 1 for k in range(lo, hi + 1)], short=True))
        reg.fields = ([Field(WORD_BITS - 1, hi + 1, "RESERVED", "R", "0")] if hi < WORD_BITS - 1 else []) + [word] + (
            [Field(lo - 1, 0, "RESERVED", "R", "0")] if lo else [])

    @staticmethod
    def _rom_table(tree: Node) -> str | None:
        """The constant table a defaults value indexes, if any."""
        node = tree
        while node[0] in ("range", "index", "concat", "cast"):
            node = node[1][-1] if node[0] == "concat" else node[2] if node[0] == "cast" else node[1]
        return node[1] if node[0] == "id" and node[1].endswith("_RST") else None

    def markers(self) -> set[str]:
        """Labels that bound a range rather than name a register."""
        out = set(WINDOW_BOUNDS) | set(RANGE_ARRAYS)
        out.update(hi for _, hi in RANGE_ARRAYS.values())
        return out

    def all_registers(self) -> list[Register]:
        """Every register and array, in offset order, after every check that
        stops a word being lost."""
        self.model.check_ranges()
        rom_labels = self.model.rom_labels()
        self.model.check_shadow_flops(rom_labels)
        markers = self.markers()
        read_labels = self.model.read_labels()
        regs = []
        for label, addr in self.f.addresses.items():
            if label in markers:
                continue
            decoded = (label in read_labels or label in self.f.write_arms or label in self.extra_strobes
                       or self.model.plain(addr) or label in rom_labels)
            if not decoded:
                raise Refusal(f"{RTL}: {label} is declared and nothing decodes it")
            regs.append(self.register(label, addr))
        for base, (name, end) in RANGE_ARRAYS.items():
            regs.append(self.range_register(base, name, end))
        regs += self.cbs_registers()
        regs += self.literal_registers()
        covered = {r.offset + k * r.stride for r in regs for k in range(r.count)}
        self.model.census(covered)
        return sorted(regs, key=lambda r: (r.offset, r.label))

    def literal_registers(self) -> list[Register]:
        """Words a read decode tests by a literal address. Each must be named
        in the descriptions, and each name must match a literal test."""
        literals = self.model.literals
        extra = sorted(set(literals) - set(self.literal_words))
        if extra:
            raise Refusal(f"{RTL}: a read decode tests the literal address 0x{extra[0]:03X}, "
                          "which no register names")
        out = []
        for addr, name in self.literal_words.items():
            if addr not in literals:
                raise Refusal(f"the descriptions name literal word 0x{addr:03X}, which {RTL} does not test")
            reg = self.register("A_" + name, addr)
            reg.rtl_range = f"literal 0x{addr:03X}"
            out.append(reg)
        return out

    def wide_input(self, b: Bit) -> bool:
        """Whether the bit reads part of a wider input word."""
        src = next((x[4:] for x in b.notes if x.startswith("src:")), "")
        sig = src.rsplit("[", 1)[0]
        return sig.startswith("i_") and self.f.signals.get(sig, 1) > 1

    def stored_name(self, reg: Register, b: Bit, n: int) -> str:
        """The name of a stored bit: the output port it drives, the storage's
        own name, or the register's name when nothing names the bit."""
        if b.write_name:
            tbit = next((int(x[5:]) for x in b.notes if x.startswith("tbit:")), n)
            name, span, kind = self.storage_naming(b.write_name, tbit)
            if span:
                b.notes.append(f"span:{span}")
            if kind in ("consumer", "setter", "reserved"):
                return name
            if b.write_name.endswith("_r") or self.f.signals.get(b.write_name, WORD_BITS) < WORD_BITS:
                return name
        return reg.label


def const_vec_addr(addr: int, bits: int) -> Vec:
    """An address as a decode compares it."""
    return Vec(bits, addr & ((1 << bits) - 1))


def reset_text(values: list[int | None], short: bool = False) -> str:
    """Hex digits for a reset value; X marks a nibble that holds an unknown
    bit. `values` is LSB first."""
    width = len(values)
    if all(v == 0 for v in values):
        return "0" if short else "0x" + "0" * 8
    if short and all(v is None for v in values):
        return "X"
    digits = []
    for nib in range((width + 3) // 4):
        chunk = values[nib * 4:nib * 4 + 4]
        if any(v is None for v in chunk):
            digits.append("X")
        else:
            digits.append(f"{sum((v or 0) << k for k, v in enumerate(chunk)):X}")
    text = "".join(reversed(digits))
    if short:
        return text.lstrip("0") + "h" if text.strip("0") else "0"
    return "0x" + text.rjust(8, "0")
