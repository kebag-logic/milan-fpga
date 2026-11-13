#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split CPU's generated region decode, read off its netlist and compared with the SoC's regions (#791).

A VexiiRiscv netlist decides whether a fetch or a load may reach the bus in
one combinational fault term per port, its PMA:

  - fetch: FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault, of the fetch address;
  - load: LsuCachelessPlugin_logic_onPma_port_rsp_fault, of the data address
    and the access ({size, store}: a word load is 3'b100).

Stores are not graded: at the pinned generator the data port's term admits a
store wherever it admits a load, whatever the region's mode, so it decides
nothing a load does not (#791 is the fetch and load decode).

This reads each term's assign and every assign it uses from the netlist,
inlined, and evaluates it. The address may appear only masked by a constant,
(address & C), so the term reads only the bits of those masks. A region
[origin, origin + size) reads only the bits from the lowest set bit of
origin | size upward. Evaluating every combination of the union of those
bits, the other bits zero, therefore decides the term at every one of the
2^32 addresses. The term is exact when the addresses it admits are exactly
the regions of that access's mode: x for a fetch, r for a load. Any other
use of the address, or a construct this reader does not know, is refused by
name rather than guessed.

    python3 decode.py <VexiiRiscvLitex_*.v> <regions.json>

regions.json is [[origin, size, mode, bus], ...]: the SoC's own regions
(soc.json's memory_regions), then the CPU's own devices, which LiteX keeps
as linker regions and the CPU decodes too (soc.json's cpu_devices). Exit 0
when every port is exact, 1 when one is not, 2 when the netlist cannot be
read.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

#: Each port: its fault term, its address, its access argument (name, value) or None, and the mode it needs.
PORTS = {
    'fetch': ('FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault', 'FetchL1Plugin_pmaBuilder_addressBits', None, 'x'),
    'load': ('LsuCachelessPlugin_logic_onPma_port_rsp_fault', 'LsuCachelessPlugin_pmaBuilder_addressBits',
             ('LsuCachelessPlugin_pmaBuilder_argsBits', 0b100), 'r'),
}
#: More bits than this would make the enumeration slow; no shipping netlist comes near it.
MAX_BITS = 24
_TOKEN = re.compile(r"\s*(?:(\d+)'([bhd])([0-9a-fA-F_]+)|(\d+)|([A-Za-z_]\w*)|(==|!=|&&|\|\||[!~&|^(){},\[\]]))")


class Unreadable(RuntimeError):
    """The netlist holds something this reader does not decide."""


def tokens(text: str) -> list[tuple]:
    """The expression's tokens; a character no token starts with is refused, never skipped."""
    out, at = [], 0
    while text[at:].strip():
        match = _TOKEN.match(text, at)
        if not match or match.end() == at:
            raise Unreadable(f'unknown text {text[at:at + 20].strip()!r}')
        out.append(match.groups(''))
        at = match.end()
    return out


def assigns(text: str) -> tuple[dict[str, str], dict[str, int]]:
    """Every one-line continuous assign to a whole signal, and every declared width."""
    rhs = dict(re.findall(r'^\s*assign (\w+) = (.*);\s*$', text, re.M))
    widths = {name: int(hi) - int(lo) + 1 if hi else 1 for hi, lo, name in
              re.findall(r'^\s*(?:wire|reg)\s+(?:\[(\d+):(\d+)\]\s+)?(\w+)\s*;', text, re.M)}
    return rhs, widths


class Term:
    """One fault term, inlined to its free inputs: the address and the access argument."""

    def __init__(self, text: str, signal: str, address: str, argument: str | None) -> None:
        self.rhs, self.widths = assigns(text)
        self.free = {address, *([argument] if argument else [])}
        self.address = address
        self.tree = self.inline(signal, set())
        self.masks: set[int] = set()
        self.collect(self.tree)

    def inline(self, name: str, seen: set[str]) -> tuple:
        """The signal's assign, parsed, with every signal it reads inlined."""
        if name in self.free:
            return ('id', name, self.widths.get(name))
        if name in seen:
            raise Unreadable(f'{name} reads itself')
        if name not in self.rhs:
            raise Unreadable(f'{name} has no one-line assign to read')
        self.tokens, self.at = tokens(self.rhs[name]), 0
        tree = self.expression()
        if self.at != len(self.tokens):
            raise Unreadable(f'{name}: unread text after its expression')
        return self.resolve(tree, seen | {name})

    def resolve(self, node: tuple, seen: set[str]) -> tuple:
        """Replace each signal of a parsed tree by its own inlined assign."""
        if node[0] == 'ref':
            width = self.widths.get(node[1])
            inner = self.inline(node[1], seen)
            return inner if inner[0] == 'id' else ('wire', width, inner)
        if node[0] in ('const', 'id'):
            return node
        return (node[0], *[self.resolve(n, seen) if isinstance(n, tuple) else n for n in node[1:]])

    def take(self, want: str | None = None) -> tuple:
        """The next token, refused when it is not `want`."""
        if self.at >= len(self.tokens):
            raise Unreadable('the expression ends early')
        token = self.tokens[self.at]
        if want is not None and token[5] != want:
            raise Unreadable(f'expected {want!r}, read {"".join(token)!r}')
        self.at += 1
        return token

    def peek(self) -> str:
        """The next operator token, or ''."""
        return self.tokens[self.at][5] if self.at < len(self.tokens) else ''

    def expression(self) -> tuple:
        """Verilog precedence, lowest first: || && | ^ & == !=, then the unary operators."""
        return self.binary(0)

    LEVELS = (('||',), ('&&',), ('|',), ('^',), ('&',), ('==', '!='))

    def binary(self, level: int) -> tuple:
        """One precedence level, left associative."""
        if level == len(self.LEVELS):
            return self.unary()
        node = self.binary(level + 1)
        while self.peek() in self.LEVELS[level]:
            op = self.take()[5]
            node = ('bin', op, node, self.binary(level + 1))
        return node

    def unary(self) -> tuple:
        """! ~ and the reduction | and &, then a primary and its bit select."""
        if self.peek() in ('!', '~', '|', '&'):
            op = self.take()[5]
            return ('un', op, self.unary())
        node = self.primary()
        if self.peek() == '[':
            self.take('[')
            index = self.take()
            if not index[3]:
                raise Unreadable('a bit select that is not one constant index')
            self.take(']')
            node = ('bit', int(index[3]), node)
        return node

    def primary(self) -> tuple:
        """A sized constant, a signal, a parenthesised expression or a concatenation."""
        token = self.take()
        if token[0]:
            base = {'b': 2, 'h': 16, 'd': 10}[token[1]]
            return ('const', int(token[2].replace('_', ''), base), int(token[0]))
        if token[4]:
            return ('ref', token[4])
        if token[5] == '(':
            node = self.expression()
            self.take(')')
            return node
        if token[5] == '{':
            parts = [self.expression()]
            while self.peek() == ',':
                self.take(',')
                parts.append(self.expression())
            self.take('}')
            return ('cat', *parts)
        raise Unreadable(f'unexpected {"".join(token)!r}')

    def collect(self, node: tuple) -> None:
        """Every mask the address is read through; any other read of the address is refused."""
        if node[0] == 'id' and node[1] == self.address:
            raise Unreadable(f'{self.address} is read other than through a constant mask')
        if node[0] == 'bin' and node[1] == '&' and self.address in (self.name(node[2]), self.name(node[3])):
            other = node[3] if self.name(node[2]) == self.address else node[2]
            self.masks.add(self.constant(other))
            return
        for child in node[1:]:
            if isinstance(child, tuple):
                self.collect(child)

    @staticmethod
    def name(node: tuple) -> str | None:
        """The free input a node is, if it is one."""
        return node[1] if node[0] == 'id' else None

    def constant(self, node: tuple) -> int:
        """A subtree that reads no free input, as its value."""
        value, _ = self.evaluate(node, {})
        if not isinstance(value, int):
            raise Unreadable('a mask that is not a constant')
        return value

    def evaluate(self, node: tuple, env: dict) -> tuple[object, int]:
        """The node's value and width; the free inputs come from env, ints or arrays of them."""
        kind = node[0]
        if kind == 'const':
            return node[1], node[2]
        if kind == 'id':
            if node[1] not in env:
                raise Unreadable(f'{node[1]} has no value here')
            return env[node[1]], node[2] or 32
        if kind == 'wire':
            value, width = self.evaluate(node[2], env)
            return value, node[1] or width
        if kind == 'bit':
            value, _ = self.evaluate(node[2], env)
            return (value >> node[1]) & 1, 1
        if kind == 'un':
            value, width = self.evaluate(node[2], env)
            full = (1 << width) - 1
            if node[1] == '~':
                return ~value & full, width
            return truth({'!': value == 0, '|': value != 0, '&': value == full}[node[1]]), 1
        if kind == 'cat':
            value, width = 0, 0
            for part in node[1:]:
                v, w = self.evaluate(part, env)
                value, width = (value << w) | v, width + w
            if width > 64:
                raise Unreadable('a concatenation wider than 64 bits')
            return value, width
        a, wa = self.evaluate(node[2], env)
        b, wb = self.evaluate(node[3], env)
        op = node[1]
        if op in ('&', '|', '^'):
            return {'&': lambda: a & b, '|': lambda: a | b, '^': lambda: a ^ b}[op](), max(wa, wb)
        if op in ('==', '!='):
            return truth(a == b) if op == '==' else truth(a != b), 1
        return (truth((a != 0) & (b != 0)) if op == '&&' else truth((a != 0) | (b != 0))), 1


def truth(value: object) -> object:
    """A comparison's result as 0 or 1, for an int or an array."""
    return int(value) if isinstance(value, bool) else value.astype('uint64')


def region_bits(regions: list) -> int:
    """The address bits membership of every region reads: from the lowest set bit of origin | size up."""
    bits = 0
    for origin, size, *_ in regions:
        low = (origin | size) & -(origin | size)
        bits |= 0xFFFF_FFFF & ~(low - 1)
    return bits


def representatives(bits: int) -> object:
    """Every address whose bits outside `bits` are zero, as an array."""
    import numpy as np
    positions = [b for b in range(32) if bits >> b & 1]
    if len(positions) > MAX_BITS:
        raise Unreadable(f'{len(positions)} address bits to enumerate, more than {MAX_BITS}')
    index = np.arange(1 << len(positions), dtype='uint64')
    address = np.zeros_like(index)
    for j, b in enumerate(positions):
        address |= ((index >> np.uint64(j)) & np.uint64(1)) << np.uint64(b)
    return address


def spans(addresses: object, flags: object) -> list[tuple[int, int]]:
    """The admitted addresses among the sorted representatives, as [start, end) spans of them."""
    out, start = [], None
    order = addresses.argsort()
    addrs, marks = addresses[order], flags[order]
    for a, m in zip(addrs.tolist(), marks.tolist()):
        if m and start is None:
            start = a
        elif not m and start is not None:
            out.append((start, a))
            start = None
    if start is not None:
        out.append((start, 1 << 32))
    return out


def check(netlist: Path, regions: list) -> list[tuple[str, bool, str]]:
    """For each port, whether it admits exactly the SoC's regions of its mode, with the evidence."""
    import numpy as np
    text = netlist.read_text()
    results = []
    for port, (signal, address, argument, mode) in PORTS.items():
        term = Term(text, signal, address, argument[0] if argument else None)
        want_regions = [r for r in regions if mode in r[2]]
        bits = region_bits(regions)
        for mask in term.masks:
            bits |= mask
        addrs = representatives(bits)
        env = {address: addrs, **({argument[0]: argument[1]} if argument else {})}
        fault, _ = term.evaluate(term.tree, env)
        admitted = np.asarray(fault) == 0
        want = np.zeros(addrs.shape, dtype=bool)
        for origin, size, *_ in want_regions:
            want |= (addrs >= np.uint64(origin)) & (addrs < np.uint64(origin + size))
        wrong = addrs[admitted != want]
        got = spans(addrs, admitted)
        detail = (f'{len(addrs)} representatives of {bin(bits).count("1")} bits; admits '
                  + ', '.join(f'[0x{a:08x}, 0x{b:08x})' for a, b in got)
                  + f'; wants the {mode} regions '
                  + ', '.join(f'[0x{o:08x}, 0x{o + s:08x})' for o, s, *_ in want_regions))
        if len(wrong):
            first = int(wrong.min())
            detail += (f'; first difference 0x{first:08x}, '
                       f'{"admitted outside" if admitted[addrs == first][0] else "refused inside"} the regions')
        results.append((f'the {port} decode admits exactly the SoC regions it may {port}', not len(wrong), detail))
    return results


def main(argv: list[str]) -> int:
    """Check one netlist against one region list; print each port's verdict."""
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[-4], file=sys.stderr)
        return 2
    try:
        results = check(Path(argv[0]), json.loads(Path(argv[1]).read_text()))
    except Unreadable as error:
        print(f'DECODE refused: {error}')
        return 2
    for name, ok, detail in results:
        print(f'DECODE {"PASS" if ok else "FAIL"} {name}: {detail}')
    return 0 if all(ok for _, ok, _ in results) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
