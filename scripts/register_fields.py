#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Per-bit field derivation for the register reference generator (#797).

Turns the facts `register_rtl.py` reads into registers with fields: what a
read returns at each bit, what a write does there, which RTL name the bit
carries and its reset value. Nothing here is hand-kept register data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from register_rtl import (RTL, WORD_BITS, Expr, Refusal, RtlFacts, is_concat,
                          matching, split_top, statement_end, strip_parens)

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
    ("X", "Set by the block that drives this input, not by the register file."),
)


@dataclass
class Bit:
    """What one bit of one register does on a read and on a write."""
    read: str = "zero"          # zero, stored, signal, const, complex
    read_name: str = ""
    read_value: int | None = 0
    write: str = "none"         # none, stored, w1c, strobe, magic, complex
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
class Register:
    """One addressable word, or one array of identical words."""
    label: str                  # RTL label without the A_ prefix
    offset: int
    fields: list[Field] = field(default_factory=list)
    reset: str = ""
    count: int = 1
    stride: int = 4
    array_resets: list[int] | None = None
    sources: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    rtl_range: str = ""

    @property
    def rtl_label(self) -> str:
        """The label as the RTL spells it."""
        return "A_" + self.label

    @property
    def rtl_name(self) -> str:
        """What the page cites as the RTL source: the label, or for an
        array the range labels the read decode uses."""
        return self.rtl_range or self.rtl_label


SIMPLE_TERM_RE = re.compile(r"^(?P<id>[A-Za-z_]\w*)(?:\[(?P<hi>[^\]:]+)(?::(?P<lo>[^\]]+))?\])?$")


def field_name(signal: str) -> str:
    """An RTL signal or constant name as a field name: the port direction
    prefix and the register/wire/constant suffix dropped, upper case."""
    name = re.sub(r"^(i|o)_", "", signal)
    name = re.sub(r"_(r|w|q|p|c|C|qq)$", "", name)
    return name.upper()


#: Address labels that bound a range rather than name a register.
MARKER_RE = re.compile(r"_(END|BASE)$|^A_STRMW_CNT0$")


class Deriver:
    """Turns the RTL facts into registers with fields."""

    def __init__(self, facts: RtlFacts):
        self.f = facts
        self.sym = facts.sym
        self.consumers = self._consumers()
        self.extra_strobes = self._extra_strobes()
        self.setters = self._setters()

    # ---- naming helpers --------------------------------------------------
    def _consumers(self) -> dict[str, list[tuple[int, int, str, str]]]:
        """storage -> [(hi, lo, output field, span note)] from the assigns."""
        out: dict[str, list[tuple[int, int, str, str]]] = {}
        for port, rhs in self.f.assigns.items():
            name = field_name(port)
            rhs = strip_parens(rhs)
            tern = re.fullmatch(r"(\w+)\[(\d+)\]\s*\?\s*(\w+)\[(\d+)\]\s*:\s*(.+)", rhs)
            if tern:
                out.setdefault(tern.group(1), []).append(
                    (int(tern.group(2)), int(tern.group(2)), name + "_SELECT", ""))
                out.setdefault(tern.group(3), []).append(
                    (int(tern.group(4)), int(tern.group(4)), name, ""))
                continue
            rhs = re.sub(r"\s*&\s*[A-Z]\w*_P$", "", rhs)
            parts = split_top(rhs[1:-1], ",") if is_concat(rhs) else [rhs]
            widths = [self.term_width(p) for p in parts]
            if None in widths:
                continue
            top = sum(widths) - 1
            for part, width in zip(parts, widths):
                m = SIMPLE_TERM_RE.match(part.strip())
                lo_out = top - width + 1
                span = f"[{top}:{lo_out}]" if len(parts) > 1 else ""
                top -= width
                if not m or m.group("id") in self.f.assigns:
                    continue
                sig = m.group("id")
                if sig not in self.f.signals or sig.startswith(("i_", "o_")):
                    continue
                hi, lo = self.slice_of(m, sig)
                out.setdefault(sig, []).append((hi, lo, name, span))
        return out

    def _extra_strobes(self) -> dict[str, list[tuple[int, str]]]:
        """label -> [(bit, name)] for `wire x = wr_fire && (wr_addr == A_Y)
        && s_axi_wdata[n]` decodes outside the write case."""
        out: dict[str, list[tuple[int, str]]] = {}
        text = self.f.text
        for m in re.finditer(r"wire\s+(\w+)\s*=\s*wr_fire\s*&&\s*\(wr_addr\s*==\s*(A_\w+)\)\s*&&\s*"
                             r"s_axi_wdata\[(\d+)\]", text):
            out.setdefault(m.group(2), []).append((int(m.group(3)), field_name(m.group(1))))
        return out

    def _setters(self) -> dict[str, dict[int, str]]:
        """storage -> {bit: name} for `if (i_x) storage[n] <= 1'b1;`, the
        hardware event that latches a status bit."""
        out: dict[str, dict[int, str]] = {}
        text = self.f.text
        for m in re.finditer(r"if\s*\((i_\w+)\)\s*(\w+)\[(\d+)\]\s*<=\s*1'b1\s*;", text):
            out.setdefault(m.group(2), {})[int(m.group(3))] = field_name(m.group(1))
        return out

    def slice_of(self, m: re.Match, sig: str) -> tuple[int, int]:
        """(hi, lo) a simple term selects from its signal."""
        width = self.f.signals.get(sig, WORD_BITS)
        if m.group("hi") is None:
            return width - 1, 0
        hi = Expr(m.group("hi"), self.sym).value()[0]
        lo = Expr(m.group("lo"), self.sym).value()[0] if m.group("lo") else hi
        return hi, lo

    def term_width(self, term: str) -> int | None:
        """Bit width of one concatenation part."""
        term = strip_parens(term)
        and_param = re.fullmatch(r"(.+?)\s*&\s*([A-Z]\w*_P)", term)
        if and_param:
            term = and_param.group(1).strip()
        m = SIMPLE_TERM_RE.match(term)
        if m:
            sig = m.group("id")
            if sig in self.f.arrays and m.group("hi") is not None and m.group("lo") is None:
                return self.f.signals.get(sig, WORD_BITS)
            if m.group("hi") is not None:
                hi, lo = self.slice_of(m, sig)
                return hi - lo + 1
            if sig in self.f.signals:
                return self.f.signals[sig]
            if self.sym.has(sig):
                return self.sym.width(sig)
            return None
        try:
            return Expr(term, self.sym).value()[1]
        except Refusal:
            return None

    def name_term(self, sig: str, hi: int, lo: int, bit: int) -> tuple[str, str]:
        """(field name, span note) for one bit of a term `sig[hi:lo]`.

        A port or constant names the whole term. A storage register names
        each bit by the output port that bit drives; a stored bit that
        drives nothing is RESERVED when other bits of the same register do
        drive something, and takes the register's own name otherwise."""
        if sig.startswith(("i_", "o_")) or self.sym.has(sig):
            width = self.f.signals.get(sig) or self.sym.width(sig) or WORD_BITS
            span = "" if (hi, lo) == (width - 1, 0) else (f"[{hi}:{lo}]" if hi != lo else f"[{hi}]")
            return field_name(sig), span
        return self.storage_name(sig, bit)

    def storage_name(self, sig: str, bit: int) -> tuple[str, str]:
        """(field name, span note) of bit `bit` of a storage register."""
        name, span, _ = self.storage_naming(sig, bit)
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

    def used(self, sig: str, bit: int) -> bool:
        """Whether some expression of the RTL reads bit `bit` of `sig`."""
        if sig not in self.f.usage:
            return False
        bits = self.f.usage[sig]
        return bits is None or bit in bits

    # ---- read side -------------------------------------------------------
    def read_expr(self, label: str) -> tuple[str, str]:
        """(kind, expression) of what a read of `label` returns."""
        if label in self.f.read_arms:
            target, body = self.f.read_arms[label]
            return "arm", self.choose(body, target)
        if label in self.f.window_reads:
            return "window", self.choose(self.f.window_reads[label], "strm_mux")
        if label in self.f.plain_rw:
            return "shadow", ""
        if label in self.f.defaults:
            return "const", self.f.defaults[label]
        return "zero", ""

    def choose(self, body: str, target: str) -> str:
        """The expression a read arm assigns, parameter-guarded arms resolved."""
        body = body.strip()
        if body.startswith("begin"):
            body = body[len("begin"):body.rindex("end")].strip()
        m = re.fullmatch(r"if\s*\((\w+)\)\s*" + target + r"\s*=\s*(.+?);\s*else\s*" + target +
                         r"\s*=\s*(.+?);", body, re.S)
        if m and self.sym.has(m.group(1)):
            return m.group(2) if self.sym.value(m.group(1)) else m.group(3)
        m = re.fullmatch(target + r"\s*=\s*(.+?);", body, re.S)
        if m:
            return " ".join(m.group(1).split())
        return "COMPLEX:" + " ".join(body.split())

    def read_bits(self, label: str, bits: list[Bit], reg: Register) -> None:
        """Fill the read half of every bit of `label`."""
        kind, expr = self.read_expr(label)
        reg.sources.append(f"read: {kind}")
        if kind == "zero":
            return
        if kind == "shadow":
            for b in bits:
                b.read = "stored"
            return
        if kind == "const":
            self.attribute(expr, bits, const=True)
            return
        if expr.startswith("COMPLEX:") or "?" in expr:
            for b in bits:
                b.read, b.read_name, b.read_value = "complex", label, None
            return
        self.attribute(expr, bits)

    def attribute(self, expr: str, bits: list[Bit], const: bool = False) -> None:
        """Bit-by-bit sources of a read expression, MSB first. A wire whose
        definition is a concatenation is read through its definition."""
        expr = strip_parens(expr)
        if expr in self.f.wires and is_concat(self.f.wires[expr]):
            expr = self.f.wires[expr]
        ors = split_top(expr, "|")
        if len(ors) > 1:
            for part in ors:
                sub = [Bit() for _ in range(WORD_BITS)]
                self.attribute(part, sub, const)
                for b, s in zip(bits, sub):
                    if s.read != "zero" and not (s.read == "const" and s.read_value == 0):
                        if b.read in ("zero",) or (b.read == "const" and b.read_value == 0):
                            b.read, b.read_name, b.read_value = s.read, s.read_name, s.read_value
                            b.notes = [x for x in b.notes if not x.startswith(("src:", "span:"))] + s.notes
                        elif b.read == "signal" and s.read == "signal":
                            b.notes.append(f"or:{b.read_name}")
                            b.read_name = s.read_name
                            b.notes = [x for x in b.notes if not x.startswith(("src:", "span:"))] + s.notes
            return
        concat = is_concat(expr)
        parts = split_top(expr[1:-1], ",") if concat else [expr]
        widths = [self.term_width(p) for p in parts]
        if not concat and widths[0] is None:
            widths = [WORD_BITS]
        if None in widths:
            for b in bits:
                b.read, b.read_name, b.read_value = "complex", "", None
            return
        pos = sum(widths) - 1
        for part, width in zip(parts, widths):
            part = strip_parens(part)
            lo_bit = pos - width + 1
            m = SIMPLE_TERM_RE.match(part)
            and_param = re.fullmatch(r"(.+?)\s*&\s*([A-Z]\w*_P)", part)
            if and_param:
                m = SIMPLE_TERM_RE.match(and_param.group(1).strip())
                if not self.sym.value(and_param.group(2)):
                    m = None
                    part = "0"
            if m and m.group("id") in self.f.arrays and m.group("hi") is not None \
                    and m.group("lo") is None:
                for k in range(width):
                    if 0 <= lo_bit + k < WORD_BITS:
                        b = bits[lo_bit + k]
                        b.read, b.read_name, b.read_value = "signal", "@WORD", None
                        b.notes.append(f"src:{part}[{k}]")
            elif m and not self.sym.has(m.group("id")):
                sig = m.group("id")
                hi, lo = self.slice_of(m, sig)
                for k in range(width):
                    if 0 <= lo_bit + k < WORD_BITS:
                        b = bits[lo_bit + k]
                        name, span = self.name_term(sig, hi, lo, lo + k)
                        b.read = "signal"
                        b.read_name = name
                        b.read_value = None
                        b.notes.append(f"src:{sig}[{lo + k}]")
                        if span:
                            b.notes.append(f"span:{span}")
            else:
                try:
                    value, _ = Expr(part, self.sym).value()
                except Refusal:
                    value = None
                cname = ""
                cast = re.fullmatch(r"\w+'\((\w+)\)", part)
                if m and self.sym.has(m.group("id")):
                    cname = field_name(m.group("id"))
                elif cast and self.sym.has(cast.group(1)):
                    cname = field_name(cast.group(1))
                elif not concat:
                    cname = "@WORD"
                elif const and not (value == 0 and width >= 4):
                    cname = f"BIT{lo_bit}" if width == 1 else f"BITS{pos}_{lo_bit}"
                for k in range(width):
                    if 0 <= lo_bit + k < WORD_BITS:
                        b = bits[lo_bit + k]
                        b.read = "const"
                        b.read_value = None if value is None else (value >> k) & 1
                        b.read_name = cname
            pos -= width

    # ---- write side ------------------------------------------------------
    def write_bits(self, label: str, bits: list[Bit], reg: Register) -> None:
        """Fill the write half of every bit of `label` from its write arms."""
        arms = self.f.write_arms.get(label, [])
        for bit, name in self.extra_strobes.get(label, []):
            bits[bit].write, bits[bit].write_name = "strobe", name
        if label in self.f.plain_rw and not arms:
            for b in bits:
                b.write = "stored"
            return
        for _, body in arms:
            self.write_body(body, bits, reg, cond="")
        if label in self.f.plain_rw:
            for b in bits:
                if b.write == "none":
                    b.write = "stored"

    def write_body(self, body: str, bits: list[Bit], reg: Register, cond: str) -> None:
        """Apply one arm's statements to the bits."""
        body = body.strip()
        if body.startswith("begin"):
            body = body[len("begin"):body.rindex("end")]
        pos = 0
        while True:
            m = re.compile(r"\s*").match(body, pos)
            pos = m.end()
            if pos >= len(body):
                return
            end = statement_end(body, pos)
            self.write_stmt(body[pos:end].strip(), bits, reg, cond)
            pos = end

    def strobe_name(self, pulse: str) -> str:
        """A one-cycle strobe named by the output port it drives."""
        for port, rhs in self.f.assigns.items():
            if rhs == pulse:
                return field_name(port)
        return field_name(pulse)

    def write_stmt(self, st: str, bits: list[Bit], reg: Register, cond: str) -> None:
        """One statement of a write arm."""
        if st.startswith("begin"):
            self.write_body(st, bits, reg, cond)
            return
        m = re.fullmatch(r"if\s*\((.+?)\)\s*(.+)", st, re.S)
        if m and st.startswith("if"):
            paren = st.index("(")
            close = matching(st, paren, "(", ")")
            c = " ".join(st[paren + 1:close].split())
            rest = st[close + 1:].strip()
            els = None
            then_end = statement_end(rest, 0)
            then, tail = rest[:then_end], rest[then_end:].strip()
            if tail.startswith("else"):
                els = tail[4:].strip()
            bm = re.fullmatch(r"s_axi_wdata\[(\d+)\](?:\s*&&\s*(.+))?", c)
            any_m = re.fullmatch(r"\|\s*s_axi_wdata\[(\d+):(\d+)\]", c)
            if bm:
                n = int(bm.group(1))
                guard = bm.group(2)
                tm = re.fullmatch(r"(\w+)(?:\[(\d+)\])?\s*<=\s*1'b([01])\s*;", then.strip())
                if tm and tm.group(3) == "1" and not guard:
                    bits[n].write, bits[n].write_name = "strobe", self.strobe_name(tm.group(1))
                    return
                if tm and tm.group(3) == "0" and not guard:
                    bits[n].write, bits[n].write_name = "w1c", tm.group(1)
                    return
                pulse = re.search(r"(\w+_p|\w+_pend_r)\s*<=\s*1'b1", then)
                bits[n].write = "strobe"
                bits[n].write_name = self.strobe_name(pulse.group(1)) if pulse else "COMMIT"
                if guard:
                    bits[n].notes.append(f"cond:{guard}")
                self.write_body("begin " + then + " end", bits, reg,
                                (cond + " " + (guard or "")).strip())
                return
            if any_m:
                hi, lo = int(any_m.group(1)), int(any_m.group(2))
                tm = re.fullmatch(r"(\w+)\s*<=\s*1'b1\s*;", then.strip())
                for n in range(lo, hi + 1):
                    bits[n].write = "w1c_any"
                    bits[n].write_name = self.strobe_name(tm.group(1)) if tm else ""
                return
            self.write_body("begin " + then + " end", bits, reg, (cond + " " + c).strip())
            if els:
                self.write_body("begin " + els + " end", bits, reg, (cond + " not " + c).strip())
            return
        m = re.fullmatch(r"(\w+)(\[[^\]]+\])?\s*<=\s*(.+?);", st, re.S)
        if not m:
            return
        target, rhs = m.group(1), " ".join(m.group(3).split())
        if m.group(2):
            return
        if rhs == "s_axi_wdata":
            for b in bits:
                self.store(b, target, cond)
            return
        sl = re.fullmatch(r"s_axi_wdata\[(\d+)(?::(\d+))?\]", rhs)
        if sl:
            hi = int(sl.group(1))
            lo = int(sl.group(2)) if sl.group(2) else hi
            for n in range(lo, hi + 1):
                if target.endswith("_p"):
                    bits[n].write, bits[n].write_name = "strobe", self.strobe_name(target)
                else:
                    self.store(bits[n], target, cond, n - lo)
            return
        mk = re.fullmatch(r"\(s_axi_wdata\s*!=\s*(\S+)\)", rhs)
        if mk:
            key = Expr(mk.group(1), self.sym).value()[0]
            for b in bits:
                b.write, b.write_name = "magic", target
            reg.side_effects.append(f"magic:{key:#010x}:{target}")
            return
        tern = re.fullmatch(r"(\w+)\s*\?\s*(\{.+\})\s*:\s*s_axi_wdata", rhs)
        if tern:
            forced = self.forced_bits(tern.group(2))
            for n, b in enumerate(bits):
                self.store(b, target, cond)
                if n in forced:
                    b.notes.append(f"masked:{tern.group(1)}")
            return
        if is_concat(rhs):
            forced = self.forced_bits(rhs)
            for n, b in enumerate(bits):
                if n not in forced:
                    self.store(b, target, cond)
            return
        if target.endswith("_p") and rhs == "1'b1":
            reg.side_effects.append(f"pulse:{self.strobe_name(target)}{(' ' + cond) if cond else ''}")
            return
        merge = re.fullmatch(r"\{" + target + r"\[31:(\d+)\],\s*s_axi_wdata\[(\d+)(?::(\d+))?\]\}", rhs)
        if merge:
            hi = int(merge.group(2))
            lo = int(merge.group(3)) if merge.group(3) else hi
            for n in range(lo, hi + 1):
                self.store(bits[n], target, cond)

    def forced_bits(self, concat: str) -> set[int]:
        """Bits of a `{s_axi_wdata[..], 1'b0, s_axi_wdata[..]}` image that a
        literal replaces; bits taken from the bus are not in the set."""
        parts = split_top(concat.strip()[1:-1], ",")
        widths = [self.term_width(p) for p in parts]
        out, pos = set(), sum(w or 0 for w in widths) - 1
        for part, width in zip(parts, widths):
            width = width or 0
            if not part.strip().startswith("s_axi_wdata"):
                out.update(range(pos - width + 1, pos + 1))
            pos -= width
        return out

    def store(self, b: Bit, target: str, cond: str, target_bit: int | None = None) -> None:
        """Record that a write stores this bit into `target` (at
        `target_bit` when the arm stores a slice at an offset)."""
        if b.write in ("strobe", "w1c", "w1c_any", "magic"):
            return
        b.write, b.write_name = "stored", target
        if target_bit is not None:
            b.notes.append(f"tbit:{target_bit}")
        if cond:
            b.notes.append(f"cond:{cond}")

    def write_effective(self, b: Bit, n: int, label: str) -> bool:
        """Whether a stored bit can be observed: kept by the shadow RAM, or
        read by some expression of the RTL."""
        if label in self.f.plain_rw or b.read == "stored":
            return True
        tbit = next((int(x[5:]) for x in b.notes if x.startswith("tbit:")), n)
        return self.used(b.write_name, tbit)

    # ---- reset -----------------------------------------------------------
    def reset_word(self, label: str, bits: list[Bit]) -> list[int | None]:
        """Per-bit reset values: the defaults ROM for shadow words, the
        reset block for flops, X for live inputs."""
        kind, _ = self.read_expr(label)
        out: list[int | None] = [0] * WORD_BITS
        dflt = 0
        if label in self.f.defaults:
            dflt = Expr(self.f.defaults[label], self.sym).value()[0]
        for n, b in enumerate(bits):
            if kind == "shadow" or (kind == "const"):
                out[n] = (dflt >> n) & 1
            elif b.read == "const":
                out[n] = b.read_value
            elif b.read == "zero":
                out[n] = 0
            elif b.read == "signal":
                src = next((x[4:] for x in b.notes if x.startswith("src:")), "")
                sig, idx = src.rsplit("[", 1)
                idx = int(idx[:-1])
                if sig in self.f.resets:
                    try:
                        v = Expr(self.f.resets[sig], self.sym).value()[0]
                        out[n] = (v >> idx) & 1
                    except Refusal:
                        out[n] = None
                else:
                    out[n] = None
            else:
                out[n] = None
        return out

    # ---- assembly --------------------------------------------------------
    def register(self, label: str) -> Register:
        """One register with its fields, derived bit by bit."""
        reg = Register(label[2:], self.f.addresses[label])
        bits = [Bit() for _ in range(WORD_BITS)]
        self.read_bits(label, bits, reg)
        self.write_bits(label[2:] if False else label, bits, reg)
        resets = self.reset_word(label, bits)
        reg.fields = self.group(reg, bits, resets)
        reg.reset = reset_text(resets)
        return reg

    def group(self, reg: Register, bits: list[Bit], resets: list[int | None]) -> list[Field]:
        """Consecutive bits with one name and one access become one field."""
        rows = []
        for n in range(WORD_BITS - 1, -1, -1):
            b = bits[n]
            name, access = self.classify(reg, b, n)
            if name == "@WORD":
                name = reg.label
            if (name, access) == ("RESERVED", "R/W"):
                b.notes = [x for x in b.notes if not x.startswith("span:")]
            span = next((x[5:] for x in b.notes if x.startswith("span:")), "")
            notes = sorted({x for x in b.notes
                            if x.startswith(("masked:", "cond:", "or:", "writes:", "reads:", "key"))})
            rows.append((n, name, access, span, tuple(notes)))
        fields: list[Field] = []
        for n, name, access, span, notes in rows:
            if fields and fields[-1].name == name and fields[-1].access == access and \
                    fields[-1].span == span and tuple(fields[-1].notes) == notes and fields[-1].lo == n + 1:
                fields[-1].lo = n
            else:
                fields.append(Field(n, n, name, access, "", list(notes), span))
        for fl in fields:
            fl.reset = reset_text(resets[fl.lo:fl.hi + 1], short=True)
        return self.unique(fields)

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

    def classify(self, reg: Register, b: Bit, n: int) -> tuple[str, str]:
        """(field name, access code) of bit `n`."""
        r, w = b.read, b.write
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
            if w == "w1c_any" and b.write_name:
                return b.write_name, ("R/W1C" if not reads_zero else "W1C")
            return (b.read_name or field_name(b.write_name)), ("R/W1C" if not reads_zero else "W1C")
        if w == "stored" and not self.write_effective(b, n, reg.rtl_label):
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

    # ---- arrays ----------------------------------------------------------
    def array_registers(self) -> list[Register]:
        """The address ranges the read decode serves by offset rather than
        by label: the RMON snapshot, the CBS queue window, the latency-tap
        and parser-probe words, the reserved gap and the window counters.
        Each is refused when its range term has left the decode."""
        a, t = self.f.addresses, self.f.text
        need = {
            "STAT": r"A_STATS_BASE\s*&&\s*rd_addr_q\s*<\s*A_STATS_END\)\s*live_mux\s*=\s*stat_snap",
            "LTAP": r"A_LTAP_BASE\s*&&\s*rd_addr_q\s*<\s*A_LTAP_END\)\s*live_mux\s*=\s*i_ltap_regs",
            "APRB": r"A_APRB_BASE\s*&&\s*rd_addr_q\s*<\s*A_APRB_END\)\s*live_mux\s*=\s*i_aprb_regs",
            "GAP": r"A_RSVD_GAP_BASE\s*&&\s*rd_addr_q\s*<\s*A_RSVD_GAP_END\)\s*live_mux\s*=\s*32'd0",
            "CNT": r"A_STRMW_CNT0\s*&&\s*rd_addr_q\s*<\s*A_STRMW_CNT_END\)",
            "CBS": r"a\s*>=\s*A_CBS_BASE\s*&&\s*a\s*<\s*A_CBS_END\)\s*\n?\s*is_plain_rw",
            "CBS_EN": r"is_cbs_en_wr\s*\?\s*\{31'h0,\s*s_axi_wdata\[0\]\}\s*:\s*s_axi_wdata",
        }
        for name, pattern in need.items():
            if not re.search(pattern, t):
                raise Refusal(f"{RTL}: the {name} range decode this generator documents is gone")
        out = []
        ns = self.sym.value("NS")
        out.append(array_register("STATS", a["A_STATS_BASE"], (ns, 4), [Field(31, 0, "STAT_SNAP", "R", "0")],
                              [0] * ns, "read: A_STATS_BASE to A_STATS_END (stat_snap)"))
        nq = self.sym.value("NUM_QUEUES")
        mask = (1 << WORD_BITS) - 1
        for off, key, table in ((0x0, "CBS_IDLE", "CBS_IDLE_RST"), (0x4, "CBS_HI", "CBS_HI_RST"),
                                (0x8, "CBS_LO", "CBS_LO_RST")):
            resets = [v & mask for v in self.f.cbs[table][:nq]]
            out.append(array_register(key, a["A_CBS_BASE"] + off, (nq, 0x20), [Field(31, 0, key, "R/W", "see table")],
                                  resets, f"reset: A_CBS_BASE + 0x{off:X} + 0x20 * q ({table})"))
        en = Expr(self.f.cbs_en_reset, self.sym).value()[0]
        out.append(array_register("CBS_EN", a["A_CBS_BASE"] + 0xC, (nq, 0x20),
                              [Field(31, 1, "RESERVED", "R", "0"), Field(0, 0, "CBS_EN", "R/W", "see table")],
                              [(en >> q) & 1 for q in range(nq)], "reset: A_CBS_BASE + 0xC + 0x20 * q (CBS_EN_RST)"))
        n_ltap = (a["A_LTAP_END"] - a["A_LTAP_BASE"]) // 4
        out.append(array_register("LTAP", a["A_LTAP_BASE"], (n_ltap, 4), [Field(31, 0, "LTAP_REGS", "R", "X")],
                              None, "read: A_LTAP_BASE to A_LTAP_END (i_ltap_regs)"))
        n_aprb = (a["A_APRB_END"] - a["A_APRB_BASE"]) // 4
        out.append(array_register("APRB", a["A_APRB_BASE"], (n_aprb, 4), [Field(31, 0, "APRB_REGS", "R", "X")],
                              None, "read: A_APRB_BASE to A_APRB_END (i_aprb_regs)"))
        n_gap = (a["A_RSVD_GAP_END"] - a["A_RSVD_GAP_BASE"]) // 4
        out.append(array_register("RSVD_GAP", a["A_RSVD_GAP_BASE"], (n_gap, 4), [Field(31, 0, "RESERVED", "R", "0")],
                              [0] * n_gap, "read: A_RSVD_GAP_BASE to A_RSVD_GAP_END"))
        n_cnt = (a["A_STRMW_CNT_END"] - a["A_STRMW_CNT0"]) // 4
        out.append(array_register("STRMW_CNT", a["A_STRMW_CNT0"], (n_cnt, 4), [Field(31, 0, "SNAP_SHADOW", "R", "X")],
                              None, f"read: A_STRMW_CNT0..{n_cnt - 1} (A_STRMW_CNT0 to A_STRMW_CNT_END)"))
        return out

    def all_registers(self) -> list[Register]:
        """Every register and array, in offset order; range markers skipped."""
        regs = [self.register(n) for n in self.f.addresses if not MARKER_RE.search(n)]
        regs += self.array_registers()
        return sorted(regs, key=lambda r: (r.offset, r.label))

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


def array_register(label: str, offset: int, geometry: tuple[int, int], fields: list[Field],
          resets: list[int] | None, source: str) -> Register:
    """One array of identical words, `geometry` = (count, stride); `source`
    names the RTL range."""
    count, stride = geometry
    reg = Register(label, offset, fields, count=count, stride=stride, array_resets=resets)
    reg.rtl_range = source.split(": ", 1)[1] if ": " in source else source
    reg.sources.append(source)
    if resets is None:
        reg.reset = "0xXXXXXXXX"
    elif len(set(resets)) == 1:
        reg.reset = f"0x{resets[0]:08X}"
    else:
        reg.reset = "see table"
    for fl in fields:
        if fl.reset == "see table" and resets is not None and len(set(resets)) == 1:
            fl.reset = reset_text([(resets[0] >> k) & 1 for k in range(fl.lo, fl.hi + 1)], short=True)
    return reg


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


