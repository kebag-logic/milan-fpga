# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The packet-mailbox contract, read from mailbox.yaml and validated.

One reading for every output. ``load()`` turns the YAML into a ``Contract``
and refuses a contract that could not be built (an overlapping field, a ring
that is not a power of two, a channel two EtherType rules both claim).
``constants()`` flattens it into the one named list every emitter writes, so
the SystemVerilog package, the C header and the reference page carry the same
names with the same values, and ``gen_mailbox.py --selftest`` can compare the
three outputs name by name.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

#: The contract this module reads unless told otherwise.
CONTRACT = Path(__file__).resolve().parent / "mailbox.yaml"

#: Every register, interface register and channel register lives below this
#: byte offset; the event ring and the channel rings live at or above it.
REGISTER_SPACE_BYTES = 0x400

#: A frame field a filter term reads is eight bytes long (an entity_id, or a
#: MAAP start address and count).
TERM_FIELD_BYTES = 8

ACCESS_KINDS = ("ro", "rw", "wo", "rw1c")


class ContractError(ValueError):
    """The YAML does not describe a buildable contract."""


@dataclass(frozen=True)
class Field:
    """A bit field of a 32-bit word."""

    name: str
    lsb: int
    width: int
    doc: str


@dataclass(frozen=True)
class Register:
    """A 32-bit register at a byte offset inside its block."""

    name: str
    offset: int
    access: str
    doc: str
    fields: tuple[Field, ...]


@dataclass(frozen=True)
class Word:
    """One header word of a record and its fields."""

    index: int
    fields: tuple[Field, ...]


@dataclass(frozen=True)
class Term:
    """One accept term of a channel's filter rule."""

    test: str
    offset: int
    msg_mask: int
    field: str
    doc: str


@dataclass(frozen=True)
class Channel:
    """One mailbox pair: an receive ring, a transmit ring and the filter rule feeding RX."""

    name: str
    ident: int
    rx_base: int
    rx_words: int
    tx_base: int
    tx_words: int
    max_frame_bytes: int
    ethertypes: tuple[int, ...]
    subtype: int | None
    burst: int
    refill_ms: int
    cite: str
    terms: tuple[Term, ...]


@dataclass(frozen=True)
class EventType:
    """One event the fabric posts, with the words after word 0."""

    name: str
    value: int
    doc: str
    words: tuple[Word, ...]


@dataclass(frozen=True)
class Contract:
    """The whole validated contract."""

    major: int
    minor: int
    magic: int
    window_bytes: int
    interfaces: int
    timers: int
    tick_ms: int
    index_bits: int
    registers: tuple[Register, ...]
    if_base: int
    if_stride: int
    if_registers: tuple[Register, ...]
    ch_base: int
    ch_stride: int
    ch_registers: tuple[Register, ...]
    evt_base: int
    evt_words: int
    rx_kind: int
    rx_header: tuple[Word, ...]
    rx_doc: str
    tx_kind: int
    tx_header: tuple[Word, ...]
    tx_doc: str
    ev_words: int
    ev_header: tuple[Word, ...]
    ev_doc: str
    event_types: tuple[EventType, ...]
    ethertype_byte: int
    subtype_byte: int
    msg_type_byte: int
    max_terms: int
    tests: tuple[tuple[str, int, str], ...]
    tmr_ops: tuple[tuple[str, int], ...]
    channels: tuple[Channel, ...]


@dataclass(frozen=True)
class Constant:
    """One named value every output carries: C ``MBX_<name>``, SV ``MBX_<name>_C``."""

    name: str
    value: int
    doc: str
    hexa: bool


def _need(node: dict[str, Any], key: str, where: str) -> Any:
    """A required key, or a named refusal."""
    if key not in node:
        raise ContractError(f"{where}: missing `{key}`")
    return node[key]


def _fields(raw: list[dict[str, Any]], where: str) -> tuple[Field, ...]:
    """Fields of one 32-bit word, refused when they overlap or overflow it."""
    out: list[Field] = []
    used = 0
    for item in raw:
        name = str(_need(item, "name", where))
        lsb = int(_need(item, "lsb", f"{where}.{name}"))
        width = int(_need(item, "width", f"{where}.{name}"))
        if width < 1 or lsb < 0 or lsb + width > 32:
            raise ContractError(f"{where}.{name}: bits [{lsb + width - 1}:{lsb}] leave the 32-bit word")
        mask = ((1 << width) - 1) << lsb
        if used & mask:
            raise ContractError(f"{where}.{name}: overlaps another field")
        used |= mask
        out.append(Field(name, lsb, width, str(item.get("doc", ""))))
    return tuple(out)


def _registers(raw: list[dict[str, Any]], where: str, limit: int) -> tuple[Register, ...]:
    """A register block, refused on a duplicate, unaligned or out-of-block offset."""
    out: list[Register] = []
    seen: dict[int, str] = {}
    for item in raw:
        name = str(_need(item, "name", where))
        offset = int(_need(item, "offset", f"{where}.{name}"))
        access = str(_need(item, "access", f"{where}.{name}"))
        if access not in ACCESS_KINDS:
            raise ContractError(f"{where}.{name}: access `{access}` is not one of {ACCESS_KINDS}")
        if offset % 4 or offset < 0 or offset >= limit:
            raise ContractError(f"{where}.{name}: offset {offset:#x} is unaligned or outside {limit:#x}")
        if offset in seen:
            raise ContractError(f"{where}.{name}: offset {offset:#x} already holds {seen[offset]}")
        seen[offset] = name
        fields = _fields(_need(item, "fields", f"{where}.{name}"), f"{where}.{name}")
        out.append(Register(name, offset, access, str(item.get("doc", "")), fields))
    return tuple(out)


def _words(raw: list[dict[str, Any]], where: str) -> tuple[Word, ...]:
    """Header words of a record, indexed and refused on a repeat."""
    out: list[Word] = []
    for item in raw:
        index = int(_need(item, "index", where))
        if any(w.index == index for w in out):
            raise ContractError(f"{where}: word {index} given twice")
        out.append(Word(index, _fields(_need(item, "fields", where), f"{where}.w{index}")))
    return tuple(sorted(out, key=lambda w: w.index))


def _power_of_two(value: int) -> bool:
    """True for 1, 2, 4, ..."""
    return value > 0 and value & (value - 1) == 0


def _terms(raw: list[dict[str, Any]], where: str, tests: dict[str, int], max_bytes: int) -> tuple[Term, ...]:
    """A channel's accept terms, refused on an unknown test or a field past the frame."""
    out: list[Term] = []
    for item in raw:
        test = str(_need(item, "test", where))
        if test not in tests or test == "none":
            raise ContractError(f"{where}: test `{test}` is not a usable filter test")
        offset = int(item.get("offset", 0))
        if test != "any" and offset + TERM_FIELD_BYTES > max_bytes:
            raise ContractError(f"{where}: a field at byte {offset} ends past max_frame_bytes {max_bytes}")
        msg_types = item.get("msg_types")
        mask = 0xFFFF if msg_types is None else sum(1 << int(m) for m in msg_types)
        if mask > 0xFFFF:
            raise ContractError(f"{where}: a message_type is wider than four bits")
        out.append(Term(test, offset, mask, str(item.get("field", "")), str(item.get("doc", ""))))
    return tuple(out)


def _channel(item: dict[str, Any], tests: dict[str, int], max_terms: int) -> Channel:
    """One channel, its rings and its rule."""
    name = str(_need(item, "name", "channels"))
    where = f"channels.{name}"
    rx = _need(item, "rx", where)
    tx = _need(item, "tx", where)
    match = _need(item, "match", where)
    rate = _need(item, "rate", where)
    max_bytes = int(_need(item, "max_frame_bytes", where))
    terms = _terms(_need(item, "accept", where), where, tests, max_bytes)
    if not 1 <= len(terms) <= max_terms:
        raise ContractError(f"{where}: {len(terms)} accept terms, the contract allows 1 to {max_terms}")
    ethertypes = tuple(int(e) for e in _need(match, "ethertypes", where))
    if not 1 <= len(ethertypes) <= 2:
        raise ContractError(f"{where}: one or two EtherTypes, got {len(ethertypes)}")
    subtype = match.get("subtype")
    channel = Channel(
        name=name, ident=int(_need(item, "id", where)),
        rx_base=int(_need(rx, "base", where)), rx_words=int(_need(rx, "words", where)),
        tx_base=int(_need(tx, "base", where)), tx_words=int(_need(tx, "words", where)),
        max_frame_bytes=max_bytes, ethertypes=ethertypes,
        subtype=None if subtype is None else int(subtype),
        burst=int(_need(rate, "burst", where)), refill_ms=int(_need(rate, "refill_ms", where)),
        cite=str(_need(item, "cite", where)), terms=terms)
    if not (14 < max_bytes <= 1514) or max_bytes % 2:
        raise ContractError(f"{where}: max_frame_bytes {max_bytes} is not an even 16..1514")
    if not 1 <= channel.burst <= 255 or not 1 <= channel.refill_ms <= 65535:
        raise ContractError(f"{where}: rate burst 1..255 and refill_ms 1..65535")
    return channel


def _check_rings(contract: Contract) -> None:
    """Every ring a power of two, aligned to its size, inside the window, disjoint."""
    spans: list[tuple[int, int, str]] = [(contract.evt_base, contract.evt_words, "event ring")]
    for ch in contract.channels:
        spans.append((ch.rx_base, ch.rx_words, f"{ch.name} rx"))
        spans.append((ch.tx_base, ch.tx_words, f"{ch.name} tx"))
        if (2 + (ch.max_frame_bytes + 3) // 4) > ch.rx_words:
            raise ContractError(f"{ch.name}: one max_frame_bytes record does not fit the receive ring")
    for base, words, label in spans:
        size = words * 4
        if not _power_of_two(words) or words > (1 << (contract.index_bits - 1)):
            raise ContractError(f"{label}: {words} words is not a power of two below 2^(index_bits-1)")
        if base % size or base < REGISTER_SPACE_BYTES or base + size > contract.window_bytes:
            raise ContractError(f"{label}: {base:#x}+{size:#x} is unaligned or outside the ring space")
    ordered = sorted(spans)
    for (b0, w0, l0), (b1, _w1, l1) in zip(ordered, ordered[1:]):
        if b0 + 4 * w0 > b1:
            raise ContractError(f"{l0} overlaps {l1}")


def _check_channels(contract: Contract) -> None:
    """Channel ids are 0..N-1, and no frame can classify into two channels."""
    idents = sorted(ch.ident for ch in contract.channels)
    if idents != list(range(len(idents))) or len(idents) > 8:
        raise ContractError(f"channel ids must be 0..N-1 with N <= 8, got {idents}")
    claims: dict[tuple[int, int | None], str] = {}
    for ch in contract.channels:
        for ethertype in ch.ethertypes:
            for key in ((ethertype, ch.subtype), (ethertype, None)):
                other = claims.get(key)
                if other is not None and (key[1] is None or ch.subtype is None):
                    raise ContractError(f"{ch.name} and {other} both claim EtherType {ethertype:#06x}")
            if (ethertype, ch.subtype) in claims:
                raise ContractError(f"{ch.name} repeats a classification of {claims[(ethertype, ch.subtype)]}")
            claims[(ethertype, ch.subtype)] = ch.name


def _check_blocks(contract: Contract) -> None:
    """The interface and channel register blocks fit and miss the global registers."""
    globals_at = {r.offset for r in contract.registers}
    for base, stride, regs, count, label in (
            (contract.if_base, contract.if_stride, contract.if_registers, contract.interfaces, "interface"),
            (contract.ch_base, contract.ch_stride, contract.ch_registers, len(contract.channels), "channel")):
        if any(r.offset >= stride for r in regs):
            raise ContractError(f"{label} registers spill out of their {stride:#x} stride")
        for k in range(count):
            for reg in regs:
                at = base + k * stride + reg.offset
                if at >= REGISTER_SPACE_BYTES or at in globals_at:
                    raise ContractError(f"{label} {k} {reg.name} at {at:#x} collides or leaves the register space")
                globals_at.add(at)


def _records(raw: dict[str, Any]) -> dict[str, Any]:
    """The three record layouts."""
    rx = _need(raw, "rx_frame", "records")
    tx = _need(raw, "tx_frame", "records")
    ev = _need(raw, "event", "records")
    return {
        "rx_kind": int(_need(rx, "kind", "rx_frame")), "rx_header": _words(_need(rx, "header", "rx_frame"), "rx"),
        "rx_doc": str(rx.get("doc", "")),
        "tx_kind": int(_need(tx, "kind", "tx_frame")), "tx_header": _words(_need(tx, "header", "tx_frame"), "tx"),
        "tx_doc": str(tx.get("doc", "")),
        "ev_words": int(_need(ev, "words", "event")), "ev_header": _words(_need(ev, "header", "event"), "event"),
        "ev_doc": str(ev.get("doc", "")),
    }


def load(path: Path = CONTRACT) -> Contract:
    """Read and validate the contract; a ContractError names what is wrong."""
    with path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    flt = _need(raw, "filter", "contract")
    tests = {str(t["name"]): int(t["value"]) for t in _need(flt, "tests", "filter")}
    max_terms = int(_need(flt, "max_terms", "filter"))
    ifr = _need(raw, "interface_registers", "contract")
    chr_ = _need(raw, "channel_registers", "contract")
    contract = Contract(
        major=int(raw["version"]["major"]), minor=int(raw["version"]["minor"]),
        magic=int(_need(raw, "magic", "contract")), window_bytes=int(_need(raw, "window_bytes", "contract")),
        interfaces=int(_need(raw, "interfaces", "contract")), timers=int(_need(raw, "timers", "contract")),
        tick_ms=int(_need(raw, "tick_ms", "contract")),
        index_bits=int(_need(raw, "index_bits", "contract")),
        registers=_registers(_need(raw, "registers", "contract"), "registers", REGISTER_SPACE_BYTES),
        if_base=int(ifr["base"]), if_stride=int(ifr["stride"]),
        if_registers=_registers(ifr["registers"], "interface_registers", REGISTER_SPACE_BYTES),
        ch_base=int(chr_["base"]), ch_stride=int(chr_["stride"]),
        ch_registers=_registers(chr_["registers"], "channel_registers", REGISTER_SPACE_BYTES),
        evt_base=int(raw["event_ring"]["base"]), evt_words=int(raw["event_ring"]["words"]),
        **_records(_need(raw, "records", "contract")),
        event_types=tuple(EventType(str(e["name"]), int(e["value"]), str(e.get("doc", "")),
                                    _words(e["words"], f"event_types.{e['name']}"))
                          for e in _need(raw, "event_types", "contract")),
        ethertype_byte=int(flt["ethertype_byte"]), subtype_byte=int(flt["subtype_byte"]),
        msg_type_byte=int(flt["msg_type_byte"]), max_terms=max_terms,
        tests=tuple((str(t["name"]), int(t["value"]), str(t.get("doc", ""))) for t in flt["tests"]),
        tmr_ops=tuple((str(o["name"]), int(o["value"])) for o in flt["tmr_ops"]),
        channels=tuple(sorted((_channel(c, tests, max_terms) for c in _need(raw, "channels", "contract")),
                              key=lambda c: c.ident)))
    _check_contract(contract)
    return contract


def _check_contract(contract: Contract) -> None:
    """The cross-item rules no single item can check."""
    if not 1 <= contract.interfaces <= 4 or not 1 <= contract.timers <= 64:
        raise ContractError("interfaces 1..4 and timers 1..64")
    if not 1 <= contract.tick_ms <= 255:
        raise ContractError(f"tick_ms {contract.tick_ms} is not 1..255")
    if contract.ev_words != 4 or [w.index for w in contract.rx_header] != [0, 1] \
            or [w.index for w in contract.tx_header] != [0, 1]:
        raise ContractError("records are two header words for frames and four words for an event")
    if contract.tests[0][:2] != ("none", 0):
        raise ContractError("filter test 0 must be `none`, the padding of an unused term")
    _check_rings(contract)
    _check_channels(contract)
    _check_blocks(contract)


def _field_constants(prefix: str, fields: tuple[Field, ...], doc: str) -> list[Constant]:
    """LSB and WIDTH of every field of one word."""
    out: list[Constant] = []
    for f in fields:
        out.append(Constant(f"{prefix}_{f.name}_LSB", f.lsb, f"{doc}: {f.doc}", False))
        out.append(Constant(f"{prefix}_{f.name}_WIDTH", f.width, f"{doc}: {f.doc}", False))
    return out


def _register_constants(contract: Contract) -> list[Constant]:
    """Offsets and fields of the three register blocks."""
    out: list[Constant] = []
    for reg in contract.registers:
        out.append(Constant(f"REG_{reg.name}", reg.offset, reg.doc, True))
        out += _field_constants(reg.name, reg.fields, reg.name)
    out.append(Constant("IF_BASE", contract.if_base, "first interface register block", True))
    out.append(Constant("IF_STRIDE", contract.if_stride, "bytes per interface block", True))
    for reg in contract.if_registers:
        out.append(Constant(f"IF_REG_{reg.name}", reg.offset, reg.doc, True))
        out += _field_constants(reg.name, reg.fields, reg.name)
    out.append(Constant("CH_BASE", contract.ch_base, "first channel register block", True))
    out.append(Constant("CH_STRIDE", contract.ch_stride, "bytes per channel block", True))
    for reg in contract.ch_registers:
        out.append(Constant(f"CH_REG_{reg.name}", reg.offset, reg.doc, True))
        out += _field_constants(reg.name, reg.fields, reg.name)
    return out


def _record_constants(contract: Contract) -> list[Constant]:
    """Record kinds, header words and event types."""
    out = [Constant("RX_KIND", contract.rx_kind, "KIND of an RX frame record", False),
           Constant("RX_HDR_WORDS", len(contract.rx_header), "header words of an RX record", False),
           Constant("TX_KIND", contract.tx_kind, "KIND of a TX frame record", False),
           Constant("TX_HDR_WORDS", len(contract.tx_header), "header words of a TX record", False),
           Constant("EV_WORDS", contract.ev_words, "words per event record", False),
           Constant("EVT_BASE", contract.evt_base, "event ring byte offset", True),
           Constant("EVT_WORDS", contract.evt_words, "event ring words", False)]
    for word in contract.rx_header:
        out += _field_constants(f"RXREC_W{word.index}", word.fields, f"RX record word {word.index}")
    for word in contract.tx_header:
        out += _field_constants(f"TXREC_W{word.index}", word.fields, f"TX record word {word.index}")
    for word in contract.ev_header:
        out += _field_constants(f"EVREC_W{word.index}", word.fields, f"event word {word.index}")
    for etype in contract.event_types:
        out.append(Constant(f"EV_TYPE_{etype.name}", etype.value, etype.doc, False))
        for word in etype.words:
            out += _field_constants(f"EV_{etype.name}_W{word.index}", word.fields,
                                    f"{etype.name} event word {word.index}")
    return out


def _channel_constants(contract: Contract) -> list[Constant]:
    """Every channel's rings, limits, classification and rule."""
    out: list[Constant] = []
    for ch in contract.channels:
        up = ch.name.upper()
        out += [Constant(f"CH_{up}", ch.ident, f"channel {ch.name}", False),
                Constant(f"CH_{up}_RX_BASE", ch.rx_base, f"{ch.name} receive ring byte offset", True),
                Constant(f"CH_{up}_RX_WORDS", ch.rx_words, f"{ch.name} receive ring words", False),
                Constant(f"CH_{up}_TX_BASE", ch.tx_base, f"{ch.name} transmit ring byte offset", True),
                Constant(f"CH_{up}_TX_WORDS", ch.tx_words, f"{ch.name} transmit ring words", False),
                Constant(f"CH_{up}_MAX_FRAME_BYTES", ch.max_frame_bytes, f"{ch.name} largest frame", False),
                Constant(f"CH_{up}_ETHERTYPE0", ch.ethertypes[0], f"{ch.name} EtherType", True),
                Constant(f"CH_{up}_ETHERTYPE1", ch.ethertypes[-1], f"{ch.name} second EtherType", True),
                Constant(f"CH_{up}_HAS_SUBTYPE", int(ch.subtype is not None), f"{ch.name} matches a subtype",
                         False),
                Constant(f"CH_{up}_SUBTYPE", ch.subtype or 0, f"{ch.name} AVTP subtype", True),
                Constant(f"CH_{up}_RATE_BURST", ch.burst, f"{ch.name} token bucket depth", False),
                Constant(f"CH_{up}_RATE_REFILL_MS", ch.refill_ms, f"{ch.name} ms per refilled token", False)]
        tests = {name: value for name, value, _doc in contract.tests}
        for k in range(contract.max_terms):
            term = ch.terms[k] if k < len(ch.terms) else Term("none", 0, 0, "", "unused")
            out += [Constant(f"CH_{up}_T{k}_TEST", tests[term.test], f"{ch.name} term {k}: {term.doc}", False),
                    Constant(f"CH_{up}_T{k}_OFFSET", term.offset, f"{ch.name} term {k} field byte", False),
                    Constant(f"CH_{up}_T{k}_MSG_MASK", term.msg_mask, f"{ch.name} term {k} message types", True)]
    return out


def constants(contract: Contract) -> list[Constant]:
    """The one flat list every output carries, in a stable order."""
    out = [Constant("VERSION_MAJOR", contract.major, "contract major version", False),
           Constant("VERSION_MINOR", contract.minor, "contract minor version", False),
           Constant("MAGIC", contract.magic, "ID.MAGIC", True),
           Constant("WINDOW_BYTES", contract.window_bytes, "host window size", True),
           Constant("REGISTER_SPACE_BYTES", REGISTER_SPACE_BYTES, "registers live below this offset", True),
           Constant("N_IF", contract.interfaces, "interfaces", False),
           Constant("N_TIMERS", contract.timers, "timer slots", False),
           Constant("TICK_MS", contract.tick_ms, "NOW_MS milliseconds per TICK (one centisecond)", False),
           Constant("N_CH", len(contract.channels), "channels", False),
           Constant("INDEX_BITS", contract.index_bits, "ring counter width", False),
           Constant("MAX_TERMS", contract.max_terms, "accept terms per channel", False),
           Constant("TERM_FIELD_BYTES", TERM_FIELD_BYTES, "bytes a filter term reads", False),
           Constant("ETHERTYPE_BYTE", contract.ethertype_byte, "wire byte of the EtherType", False),
           Constant("SUBTYPE_BYTE", contract.subtype_byte, "wire byte of the AVTP subtype", False),
           Constant("MSG_TYPE_BYTE", contract.msg_type_byte, "wire byte whose low nibble is message_type", False)]
    out += [Constant(f"TEST_{name.upper()}", value, doc, False) for name, value, doc in contract.tests]
    out += [Constant(f"TMR_OP_{name.upper()}", value, f"TMR_CMD.OP {name}", False)
            for name, value in contract.tmr_ops]
    out += _register_constants(contract)
    out += _record_constants(contract)
    out += _channel_constants(contract)
    seen: set[str] = set()
    for c in out:
        if c.name in seen:
            raise ContractError(f"constant {c.name} is generated twice")
        seen.add(c.name)
    return out
