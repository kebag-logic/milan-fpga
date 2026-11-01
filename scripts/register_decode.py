#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""What a read of each CSR address returns, computed from the RTL (#797).

`ReadModel` runs the block's own read decodes with the address known. The
result is the tree of everything that word can return. Evaluating that tree in
the reset state gives the reset value the page prints, with an unknown bit only
where an input or an unreset flop sets it.

The model also holds the checks that stop a register being lost: the address
census, the range terms of the decodes, and the comparison of a shadow-served
word's flop reset with the value the defaults ROM serves.
"""

from __future__ import annotations

from dataclasses import dataclass

from register_rtl import RTL, RtlFacts, find_case
from register_sv import (WORD_BITS, Assign, Case, For, If, Interpreter, Node, Refusal, Scope, Statement, Vec, const_vec,
                         evaluate, flatten, mentions, parse_expression, unknown_vec, unparse)

#: Read-decode ranges this generator documents as register arrays:
#: base label -> (register name, end label). A range term in the read decodes
#: with a live value and a base not listed here is refused.
RANGE_ARRAYS = {
    "A_STATS_BASE": ("STATS", "A_STATS_END"),
    "A_LTAP_BASE": ("LTAP", "A_LTAP_END"),
    "A_APRB_BASE": ("APRB", "A_APRB_END"),
    "A_RSVD_GAP_BASE": ("RSVD_GAP", "A_RSVD_GAP_END"),
    "A_STRMW_CNT0": ("STRMW_CNT", "A_STRMW_CNT_END"),
}
#: Range bounds that name no register of their own and are not arrays above.
WINDOW_BOUNDS = ("A_STRMW_END", "A_CBS_BASE", "A_CBS_END")
#: Locals a read decode computes from the address before using it.
ADDRESS_LOCALS = ("soff", "loff", "aoff", "coff", "strm_hit")
UNPACKED_ELEMENTS = 4096
SCAN_END = 0x1000
LIVE_EXPR = parse_expression("(strm_hit || rd_in_window) ? live_mux : 32'h0")
SHADOW_EXPR = parse_expression("(rd_in_window && !live_hit) ? shadow_q : 32'h0")
SLOW_DATA = parse_expression("strm_dir_r ? i_tctx_rd_data : i_lctx_rd_data")


def zero_node(node: Node) -> bool:
    """Whether a tree is the constant zero."""
    return node[0] in ("num", "vec") and node[1].known and node[1].value == 0


def is_constant(node: Node, scope: Scope) -> bool:
    """Whether a value tree is fully known under `scope`."""
    return evaluate(node, scope).known


class SymbolicScope(Scope):
    """Constants and the given names are known; every other signal is not."""

    def __init__(self, facts: RtlFacts, known: dict[str, Vec]) -> None:
        self.f = facts
        self.known = known

    def constant(self, name: str) -> Vec | list[Vec] | None:
        """A given name, a constant table or a constant, or None."""
        if name in self.known:
            return self.known[name]
        if name in self.f.sym.arrays:
            return self.f.sym.arrays[name]
        return self.f.sym.resolve(name) if self.f.sym.has(name) else None

    def lookup(self, name: str) -> Vec | list[Vec]:
        """Known names, then wires through their definition, else unknown."""
        value = self.constant(name)
        if value is not None:
            return value
        definition = self.f.wires.get(name) or self.f.assigns.get(name)
        if definition is not None:
            return evaluate(definition, self)
        return self.unset(name)

    def unset(self, name: str) -> Vec | list[Vec]:
        """A signal nothing in this scope fixes."""
        width = self.f.signals.get(name)
        if width is None:
            raise Refusal(f"{RTL}: {name} has no declaration this generator can read")
        if name in self.f.arrays:
            return [unknown_vec(width)] * UNPACKED_ELEMENTS
        return unknown_vec(width)


class ResetScope(SymbolicScope):
    """The state after reset: flops hold their reset clause's value. An input,
    a flop with no reset clause, or a flop the read itself loads from an input,
    stays unknown."""

    def lookup(self, name: str) -> Vec | list[Vec]:
        """Known names, then reset clauses, then wires, else unknown."""
        value = self.constant(name)
        if value is not None:
            return value
        if name in self.f.read_loaded:
            return self.unset(name)
        if name in self.f.resets:
            return evaluate(self.f.resets[name], self).resized(self.f.signals.get(name, WORD_BITS))
        if name in self.f.array_resets:
            element = evaluate(self.f.array_resets[name], self).resized(self.f.signals.get(name, WORD_BITS))
            return [element] * UNPACKED_ELEMENTS
        definition = self.f.wires.get(name) or self.f.assigns.get(name)
        if definition is not None:
            return evaluate(definition, self)
        return self.unset(name)


def joined(op: str, a: Node, b: Node, ip: Interpreter) -> Node:
    """a && b or a || b, a known operand dropped or deciding the result."""
    decisive = op == "||"
    first, second = ip.truth(a), ip.truth(b)
    if first is decisive or second is decisive:
        return ("vec", const_vec(int(decisive), 1))
    if first is not None:
        return b
    if second is not None:
        return a
    return ("bin", op, a, b)


def as_condition(node: Node, ip: Interpreter) -> Node:
    """A one-bit choice as plain logic: c ? 1 : x is c || x, and c ? 0 : x is
    !c && x, so a condition prints without a nested choice."""
    if node[0] == "bin" and node[1] in ("&&", "||"):
        return joined(node[1], as_condition(node[2], ip), as_condition(node[3], ip), ip)
    if node[0] != "tern":
        return node
    cond = node[1]
    a, b = as_condition(node[2], ip), as_condition(node[3], ip)
    first, second = ip.truth(a), ip.truth(b)
    if first is True:
        return joined("||", cond, b, ip)
    if first is False:
        return joined("&&", ("un", "!", cond), b, ip)
    if second is True:
        return joined("||", ("un", "!", cond), a, ip)
    if second is False:
        return joined("&&", cond, a, ip)
    return node


@dataclass
class RangeTerm:
    """`signal >= lo && signal < hi` in a decode, with the value it selects."""
    lo: str
    hi: str
    value: Node | None


class ReadModel:
    """The read path of the CSR block, by address."""

    def __init__(self, facts: RtlFacts) -> None:
        self.f = facts
        self.addr_bits = facts.sym.value("ADDR_WIDTH")
        self.trees: dict[int, Node] = {}
        self.rom_trees: dict[int, Node] = {}

    def vec(self, addr: int) -> Vec:
        """An address as the decode compares it."""
        return const_vec(addr, self.addr_bits)

    # ---- the defaults ROM and the shadow set --------------------------------
    def rom_tree(self, addr: int) -> Node:
        """The value `csr_default` holds for a word."""
        if addr not in self.rom_trees:
            known = const_vec(addr, 11)
            ip = Interpreter(SymbolicScope(self.f, {"a": known}), {"a": ("vec", known)})
            ip.run(self.f.rom)
            self.rom_trees[addr] = ip.state.get("csr_default", ("vec", const_vec(0)))
        return self.rom_trees[addr]

    def rom_value(self, addr: int) -> Vec:
        """The word the shadow sweep loads at reset."""
        return evaluate(self.rom_tree(addr), SymbolicScope(self.f, {})).resized(WORD_BITS)

    def plain(self, addr: int) -> bool:
        """Whether `is_plain_rw` says the shadow RAM stores writes to a word."""
        known = self.vec(addr)
        ip = Interpreter(SymbolicScope(self.f, {"a": known}), {"a": ("vec", known)})
        ip.run(self.f.plain_rw)
        result = ip.state.get("is_plain_rw")
        return bool(result is not None and evaluate(result, ip.scope).truth())

    # ---- the read path --------------------------------------------------------
    def tree(self, addr: int) -> Node:
        """Everything a read of `addr` can return, as one tree."""
        if addr in self.trees:
            return self.trees[addr]
        known = self.vec(addr)
        ip = Interpreter(SymbolicScope(self.f, {"rd_addr_q": known, "rd_addr": known}),
                         {"rd_addr_q": ("vec", known), "rd_addr": ("vec", known)})
        for block in ("pp_read", "strm_read_mux", "read_mux"):
            ip.run(self.f.read_blocks[block])
        live, shadow = ip.reduce(LIVE_EXPR), ip.reduce(SHADOW_EXPR)
        if zero_node(live) and not zero_node(ip.state["live_mux"]):
            raise Refusal(f"{RTL}: word 0x{addr:03X} has a read arm, and rd_in_window makes it read 0")
        if zero_node(shadow):
            normal = live
        elif zero_node(live):
            normal = shadow
        else:
            normal = ("bin", "|", live, shadow)
        slow = as_condition(ip.reduce(self.f.wires["rd_is_slow_w"]), ip)
        truth = ip.truth(slow)
        if truth is False:
            out = normal
        elif truth is True:
            out = ip.reduce(SLOW_DATA)
        else:
            out = ("tern", slow, ip.reduce(SLOW_DATA), normal)
        self.trees[addr] = self.expanded(out, ip)
        return self.trees[addr]

    def expanded(self, node: Node, ip: Interpreter) -> Node:
        """A value that is a wire defined by a choice or a concatenation is
        read through its definition, so the choice shows and fields name bits."""
        if node[0] == "tern":
            return ("tern", node[1], self.expanded(node[2], ip), self.expanded(node[3], ip))
        if node[0] == "id" and self.f.wires.get(node[1], ("",))[0] in ("tern", "concat"):
            return self.expanded(ip.reduce(self.f.wires[node[1]]), ip)
        return node

    def views(self, addr: int) -> list[tuple[tuple, Node]]:
        """Every (conditions, value) a read of `addr` can yield."""
        return flatten(self.tree(addr))

    def reset(self, addr: int) -> Vec:
        """What a read returns in the reset state; X only on unset bits."""
        scope = ResetScope(self.f, {"rd_addr_q": self.vec(addr), "rd_addr": self.vec(addr),
                                    "shadow_q": self.rom_value(addr)})
        return evaluate(self.tree(addr), scope).resized(WORD_BITS)

    def flop_reset(self, name: str) -> Vec | None:
        """A flop's reset value, or None when it has no reset clause."""
        node = self.f.resets.get(name)
        if node is None:
            return None
        return evaluate(node, ResetScope(self.f, {})).resized(self.f.signals.get(name, WORD_BITS))

    def decoded(self, addr: int) -> bool:
        """Whether a word holds anything: a read other than zero, or a store."""
        tree = self.tree(addr)
        if tree == ("id", "shadow_q"):
            return self.plain(addr) or self.rom_value(addr).value != 0
        return not zero_node(tree)

    # ---- structure of the decodes ----------------------------------------------
    def range_terms(self) -> list[RangeTerm]:
        """Every address range the read decodes test; any other comparison of
        the address outside a known form is refused."""
        terms: list[RangeTerm] = []
        self.literals: dict[int, Node] = {}
        for block in ("pp_read", "read_mux", "strm_read_mux"):
            self._walk_terms(self.f.read_blocks[block], terms)
        return terms

    def _walk_terms(self, statements: list[Statement], terms: list[RangeTerm]) -> None:
        """Depth-first over one decode's conditions and assignments."""
        for st in statements:
            if isinstance(st, If):
                self._condition_term(st, terms)
                self._walk_terms(st.then, terms)
                self._walk_terms(st.other, terms)
            elif isinstance(st, Case):
                for _, body in st.items:
                    self._walk_terms(body, terms)
                self._walk_terms(st.default, terms)
            elif isinstance(st, For):
                self._walk_terms(st.body, terms)
            elif mentions(st.value, "rd_addr_q"):
                self._assignment_term(st, terms)

    def _assignment_term(self, st: Assign, terms: list[RangeTerm]) -> None:
        """An assignment from the address: only the decode's own locals."""
        if st.target not in ADDRESS_LOCALS:
            raise Refusal(f"{RTL}: {st.target} reads the address in a form this generator cannot read: "
                          f"{unparse(st.value)}")
        if st.target == "strm_hit":
            bounds = self._range_bounds(st.value)
            if bounds:
                terms.append(RangeTerm(bounds[0], bounds[1], None))

    @staticmethod
    def _range_bounds(cond: Node) -> tuple[str, str] | None:
        """(lo label, hi text) of `rd_addr_q >= lo && rd_addr_q < hi`."""
        if cond[0] != "bin" or cond[1] != "&&":
            return None
        low, high = cond[2], cond[3]
        address = ("id", "rd_addr_q")
        if low[0] == "bin" and low[1] == ">=" and low[2] == address and low[3][0] == "id" \
                and high[0] == "bin" and high[1] == "<" and high[2] == address:
            return low[3][1], unparse(high[3])
        return None

    def _condition_term(self, st: If, terms: list[RangeTerm]) -> None:
        """One `if` that tests the address."""
        cond = st.cond
        if not mentions(cond, "rd_addr_q"):
            return
        value = st.then[0].value if st.then and isinstance(st.then[0], Assign) else None
        bounds = self._range_bounds(cond)
        if bounds:
            terms.append(RangeTerm(bounds[0], bounds[1], value))
            return
        if cond[0] == "bin" and cond[1] == "==" and cond[2] == ("id", "rd_addr_q"):
            target = cond[3]
            if target[0] == "id" and target[1].startswith("A_"):
                return
            self.literals[evaluate(target, SymbolicScope(self.f, {})).value] = value
            return
        raise Refusal(f"{RTL}: a read decode tests the address in a form this generator cannot read: {unparse(cond)}")

    def check_ranges(self) -> None:
        """Every live range term is a documented array, and every documented
        array still has its term."""
        found = {t.lo: t for t in self.range_terms()}
        scope = SymbolicScope(self.f, {})
        for lo, term in found.items():
            if lo in RANGE_ARRAYS or lo == "A_STRM_SEL" or lo == "A_CHMAP_CTRL":
                continue
            if term.value is None or not is_constant(term.value, scope) \
                    or not zero_node(("vec", evaluate(term.value, scope))):
                raise Refusal(f"{RTL}: the read decode serves the range {lo} to {term.hi}, "
                              "which this generator does not document")
        for lo, (name, hi) in RANGE_ARRAYS.items():
            if lo not in found or found[lo].hi != hi:
                raise Refusal(f"{RTL}: the {name} range decode ({lo} to {hi}) this generator documents is gone")

    def check_shadow_flops(self, rom_labels: set[str]) -> None:
        """A word served from the shadow RAM or named in the defaults ROM must
        reset its flop to the value the ROM serves: the RTL says the ROM must
        mirror the reset block, and the page states only one number."""
        for label, arms in self.f.write_arms.items():
            addr = self.f.addresses[label]
            if not (self.plain(addr) or label in rom_labels):
                continue
            for _, body in arms:
                for st in body:
                    if isinstance(st, Assign) and not st.selects and st.value == ("id", "s_axi_wdata"):
                        self._check_flop(label, addr, st.target)

    def _check_flop(self, label: str, addr: int, flop: str) -> None:
        """One flop against the defaults ROM."""
        reset = self.flop_reset(flop)
        rom = self.rom_value(addr)
        if reset is None:
            raise Refusal(f"{RTL}: {flop} backs {label} and has no reset clause")
        if reset.value != rom.value or reset.unknown:
            raise Refusal(f"{RTL}: {flop} resets to 0x{reset.value:08X} but the defaults ROM serves "
                          f"0x{rom.value:08X} for {label}")

    def rom_labels(self) -> set[str]:
        """The registers `csr_default` names in its own arms."""
        case = find_case(self.f.rom, "a")
        if case is None:
            raise Refusal(f"{RTL}: csr_default has no case (a)")
        labels = set()
        for items, _ in case.items:
            for label in items:
                base = label[1] if label[0] == "range" else label
                if base[0] != "id" or not base[1].startswith("A_"):
                    raise Refusal(f"{RTL}: csr_default names {unparse(label)}, which is not an A_* register")
                labels.add(base[1])
        return labels

    def read_labels(self) -> set[str]:
        """The registers the read decodes name, as case labels or tests."""
        labels: set[str] = set()
        for block in self.f.read_blocks.values():
            self._collect_labels(block, labels)
        return labels

    def _collect_labels(self, statements: list[Statement], labels: set[str]) -> None:
        """Depth-first collection for `read_labels`."""
        for st in statements:
            if isinstance(st, Case):
                if st.selector == ("id", "rd_addr_q"):
                    labels.update(label[1] for items, _ in st.items for label in items if label[0] == "id")
                for _, body in st.items:
                    self._collect_labels(body, labels)
                self._collect_labels(st.default, labels)
            elif isinstance(st, If):
                if st.cond[0] == "bin" and st.cond[1] == "==" and st.cond[2] == ("id", "rd_addr_q") \
                        and st.cond[3][0] == "id":
                    labels.add(st.cond[3][1])
                self._collect_labels(st.then, labels)
                self._collect_labels(st.other, labels)
            elif isinstance(st, For):
                self._collect_labels(st.body, labels)

    def census(self, covered: set[int]) -> None:
        """Every word the decodes serve is on the page, or the page is refused."""
        for addr in range(0, SCAN_END, 4):
            if addr not in covered and self.decoded(addr):
                raise Refusal(f"{RTL}: word 0x{addr:03X} is decoded and has no register on the page")
