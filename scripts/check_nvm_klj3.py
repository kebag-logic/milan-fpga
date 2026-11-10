#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""check_nvm_klj3.py - the gate of the split placement's saved-state reference (#823).

scripts/nvm_klj3.py is the oracle the split placement's saved-state store
(sw/firmware/ctrl_nvm) is graded against byte for byte, so a defect in it
would let the store and the reference agree on wrong bytes. This gate holds the reference to the rules
themselves, never to the store:

  space      the layout 3 declaration (nvm_layout3.h) reads as one block per
             group, each directly after the one before, inside a 16-bit id;
  ledger     at every shipped shape the inventory holds exactly the records
             scripts/nvm_contract.py's LEDGER and NAME_SLOTS require, each id
             inside its group's block;
  split      the builder's split output (nvm_split.json) counts the same
             records and the constants the store is built against follow it;
  round trip every record of the shape assembled and decoded back, and an
             all-erased container decoded with nothing applied;
  refusals   a KLJ2 container (the all-fabric writer's own, for this shape) is
             VD_VER, a foreign magic VD_MAGIC, another major VD_VER, the
             reserved header byte set VD_REC, an id one past the layout 3
             space VD_REC, a record with its crc16 broken VD_REC;
  capacity   the shape with its names at the NAME block's capacity places its
             last name at the block's last id and round trips; one name more
             has no id;
  journal    a slot's log (#823 decision 3): two deltas behind a base give
             the later value and the last sequence, the log ending on the page
             after them; a delta only its CRC-32 refuses, a stale one and one
             past the segment cap each leave the log torn before it.

--self-test plants one defect per rule into the reference (a seam the
reference exposes, replaced for one run) and requires the rule's check to
fail.

usage:
    python3 scripts/check_nvm_klj3.py
    python3 scripts/check_nvm_klj3.py --self-test

Exit 0 = every check passed (and every planted defect was caught); 1 = a
finding; 2 = refused (a shape could not be built).
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import json
import struct
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import nvm_klj3 as k3                                         # noqa: E402
import nvm_layout3                                            # noqa: E402
from nvm_contract import (LEDGER, NAME_SLOTS, VD_MAGIC, VD_OK,  # noqa: E402
                          VD_REC, VD_VER, Donor, Ident, Shape)
from nvm_klj2 import crc16_ccitt, frame_record, klj2_assemble, payload_bytes  # noqa: E402
from nvm_shape import binding_base, build, inventory, layout_version  # noqa: E402

IDENT = Ident(seq=5, entity_id=0x0011223344556677, model_id=0x8899AABBCCDDEEFF)


@dataclasses.dataclass(frozen=True)
class Built:
    """One shipped config: its shape and the builder's split output."""

    shape: Shape
    space: dict


def built(cfg: Path, out: Path) -> Built:
    """Run the builder for `cfg` and read the shape and the split output back."""
    names, dc, spi, spo = build(cfg, out)
    space = json.loads((out / cfg.stem / "nvm_split.json").read_text())
    return Built(Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo), space)


def frames(shape: Shape) -> dict[int, bytes]:
    """Every record of the shape framed under layout 3, deterministic payloads."""
    return {r: k3.frame_record3(r, payload_bytes(g, i, r, p))
            for g, i, r, p, _b in k3.inventory3(shape) if r is not None}


def reseal(blob: bytes) -> bytes:
    """The container with its CRC-32 trailer recomputed."""
    import zlib
    return blob[:-4] + struct.pack("<I", zlib.crc32(blob[:-4]) & 0xFFFF_FFFF)


# ---------------------------------------------------------------- the rules ----

def check_space() -> list[str]:
    """One block per group, each after the one before, inside a 16-bit id."""
    lay, found, at = k3.LAYOUT, [], 0
    for b in lay.blocks:
        if b.base != at or b.cap < 1:
            found.append(f"space: {b.group} starts at {b.base} with {b.cap} ids, not at {at}")
        at = b.base + b.cap
    if [b.group for b in lay.blocks] != [g for g, _ in nvm_layout3.BLOCKS]:
        found.append("space: the blocks are not in the declared order")
    if lay.id_space > 1 << 16 or lay.rec_hdr != 10 or lay.layout != 3:
        found.append(f"space: {lay.id_space} ids, a {lay.rec_hdr}-byte header, layout {lay.layout}")
    return found


def check_ledger(b: Built) -> list[str]:
    """The inventory is the LEDGER's records and the names, each id in its block."""
    found = []
    rows = k3.inventory3(b.shape)
    want = {g: rule(b.shape.dc) for g, (_c, _cl, rule) in LEDGER.items()}
    want["NAME"] = sum(b.shape.dc.get(t, 0) * n for t, n in NAME_SLOTS.items())
    got = {g: sum(1 for r in rows if r[0] == g) for g in want}
    if got != want or len(rows) != sum(want.values()):
        found.append(f"ledger: {b.shape.cfg.stem} inventory {got}, the ledger {want}")
    for g, i, rid, _p, _blk in rows:
        block = k3.LAYOUT.block(g)
        if rid is None or not block.base <= rid <= block.last or rid != block.base + i:
            found.append(f"ledger: {b.shape.cfg.stem} {g}[{i}] has id {rid}, block {block.base}..{block.last}")
    return found


def check_split(b: Built) -> list[str]:
    """The builder's split output and the store's constants follow the shape."""
    try:
        constants = k3.split_constants(b.space, b.shape)
    except ValueError as exc:
        return [f"split: {b.shape.cfg.stem}: {exc}"]
    found = []
    counts = {blk["group"]: blk["count"] for blk in b.space["blocks"]}
    rows = k3.inventory3(b.shape)
    if any(counts[g] != sum(1 for r in rows if r[0] == g) for g in counts):
        found.append(f"split: {b.shape.cfg.stem} counts {counts} are not the inventory's")
    ports = sum(1 for n, v in constants.items() if n.startswith("MILAN_NVM3_MAPOUT_ENTRIES_") and v)
    if ports != b.shape.dc["STREAM_PORT_OUTPUT"] or constants["MILAN_NVM3_N_NAME"] != b.shape.names:
        found.append(f"split: {b.shape.cfg.stem} publishes {ports} output ports and "
                     f"{constants['MILAN_NVM3_N_NAME']} names")
    return found


def check_round_trip(b: Built) -> list[str]:
    """Every payload decodes back; the all-erased container applies nothing."""
    fr = frames(b.shape)
    expect = k3.expected3(b.shape)
    blob, _ = k3.klj3_assemble(fr, IDENT)
    vd, applied = k3.klj3_decode(blob, IDENT, expect)
    found = []
    if vd != VD_OK or {k3.rid_of_key3(k): v for k, v in applied.items()} != {r: f[10:] for r, f in fr.items()}:
        found.append(f"round trip: {b.shape.cfg.stem} verdict {vd}, {len(applied)} of {len(fr)} records")
    erased = {r: k3.erased_record3(len(f) - k3.REC_HDR3) for r, f in fr.items()}
    vd, applied = k3.klj3_decode(k3.klj3_assemble(erased, IDENT)[0], IDENT, expect)
    if vd != VD_OK or applied:
        found.append(f"round trip: {b.shape.cfg.stem} all erased: verdict {vd}, {len(applied)} applied")
    return found


def klj2_container(shape: Shape) -> bytes:
    """The all-fabric writer's KLJ2 container of the shape (scripts/nvm_klj2.py)."""
    donor = Donor(base=binding_base(), layout=layout_version())
    fr = {r: frame_record(r, payload_bytes(g, i, r, p), donor.layout)
          for g, i, r, p, _b in inventory(shape, donor.base) if r is not None}
    return klj2_assemble(fr, donor, IDENT)[0]


def check_refusals(b: Built) -> list[str]:
    """Each refusal of #823 and the framing, with its verdict."""
    fr = frames(b.shape)
    expect = k3.expected3(b.shape)
    full, offs = k3.klj3_assemble(fr, IDENT)
    last = max(fr)
    at = k3.HDR + offs[min(fr)]

    def rewrite(rid: int, header: Callable[[bytes], bytes]) -> bytes:
        """The container with record `rid`'s header rewritten by `header`, its crc16 closing."""
        f = fr[rid]
        hdr = header(f[:8])
        return k3.klj3_assemble({**fr, rid: hdr + struct.pack(">H", crc16_ccitt(hdr + f[10:])) + f[10:]}, IDENT)[0]

    cases = (
        ("the all-fabric writer's KLJ2 container", klj2_container(b.shape), VD_VER),
        ("a foreign magic", reseal(b"KLJ1" + full[4:]), VD_MAGIC),
        ("major version 2", reseal(full[:4] + struct.pack("<I", 0x0002_0000) + full[8:]), VD_VER),
        ("the reserved header byte set", rewrite(min(fr), lambda h: h[:3] + b"\x01" + h[4:]), VD_REC),
        (f"id {k3.LAYOUT.id_space}, one past the space",
         rewrite(last, lambda h: h[:4] + struct.pack(">H", k3.LAYOUT.id_space) + h[6:]), VD_REC),
        ("a record whose crc16 does not close", reseal(full[:at + 10] + bytes([full[at + 10] ^ 1]) + full[at + 11:]),
         VD_REC),
    )
    return [f"refusals: {b.shape.cfg.stem}: {label}: verdict {vd}, want {want}"
            for label, blob, want in cases
            for vd in [k3.klj3_decode(blob, IDENT, expect)[0]] if vd != want]


def check_capacity(b: Built) -> list[str]:
    """At the NAME capacity the last name is the block's last id and the
    container round trips; one more name has no id."""
    name = k3.LAYOUT.block("NAME")
    full = dataclasses.replace(b.shape, names=name.cap)
    names = [r for r in k3.inventory3(full) if r[0] == "NAME"]
    found = []
    if (names[0][2], names[-1][2]) != (name.base, name.last):
        found.append(f"capacity: names at ids {names[0][2]} to {names[-1][2]}, the block {name.base}..{name.last}")
    found += [x.replace("round trip", "capacity") for x in check_round_trip(Built(full, b.space))]
    over = [r for r in k3.inventory3(dataclasses.replace(b.shape, names=name.cap + 1)) if r[0] == "NAME"]
    if over[-1][2] is not None:
        found.append(f"capacity: name {name.cap} of {name.cap + 1} has id {over[-1][2]}")
    return found


def check_journal(b: Built) -> list[str]:
    """Two deltas replayed in order; a torn, a stale and an oversized delta each stop the walk."""
    fr = frames(b.shape)
    expect = k3.expected3(b.shape)
    first, last = min(fr), max(fr)

    def frame(rid: int, seed: int) -> bytes:
        """Record rid with a payload no golden frame carries."""
        return k3.frame_record3(rid, bytes((rid * 7 + j * 3 + seed) & 0xFF for j in range(len(fr[rid]) - 10)))

    def ident(seq: int) -> Ident:
        """The gate's identity at sequence seq."""
        return Ident(seq=seq, entity_id=IDENT.entity_id, model_id=IDENT.model_id)

    base = k3.klj3_assemble(fr, ident(5))[0]
    one = k3.klj3_delta({last: frame(last, 1)}, ident(6))
    two = k3.klj3_delta({first: frame(first, 2), last: frame(last, 3)}, ident(7))

    def decode(deltas: list[bytes]) -> tuple:
        """The reference's walk of base and deltas as a slot."""
        slot = k3.klj3_slot(base, deltas)
        return k3.klj3_slot_decode(slot + bytes([0xFF]) * (k3.SLOT - len(slot)), IDENT, expect)

    found = []
    start = k3.log_start(len(base))
    vd, seq, applied, end, torn = decode([one, two])
    got = {k3.rid_of_key3(k): v for k, v in applied.items()}
    if (vd, seq, end, torn) != (VD_OK, 7, start + 2 * k3.PAGE, False) or \
            (got.get(first), got.get(last)) != (frame(first, 2)[10:], frame(last, 3)[10:]):
        found.append(f"journal: {b.shape.cfg.stem} two deltas: verdict {vd}, sequence {seq}, end {end}, torn {torn}")
    pad = k3.HDR + 2 * 10 + len(fr[first]) - 10 + len(fr[last]) - 10
    at = pad if pad < len(two) - 4 else len(two) - 1
    bad_pad = two[:at] + bytes([two[at] ^ 0x80]) + two[at + 1:]
    stale = k3.klj3_delta({last: frame(last, 3)}, ident(6))
    big = two[:16] + struct.pack("<I", k3.SEG_MAX + 4) + two[20:]
    for label, seg in (("a delta only its CRC-32 refuses", bad_pad), ("a stale delta", stale),
                       ("a delta past the segment cap", big)):
        vd, seq, applied, end, torn = decode([one, seg])
        if (vd, seq, end, torn) != (VD_OK, 6, start + k3.PAGE, True):
            found.append(f"journal: {b.shape.cfg.stem} {label}: sequence {seq}, end {end}, torn {torn}")
    return found


RULES: dict[str, Callable[[Built], list[str]]] = {
    "ledger": check_ledger, "split": check_split, "round trip": check_round_trip,
    "refusals": check_refusals, "capacity": check_capacity, "journal": check_journal,
}


def findings(shapes: list[Built]) -> list[str]:
    """Every finding of every rule at every shape."""
    return check_space() + [x for rule in RULES.values() for b in shapes for x in rule(b)]


# ------------------------------------------------------------- the self-test ----

def _frame_crc_short(rid: int, payload: bytes) -> bytes:
    """A frame whose crc16 skips the record_id."""
    hdr = struct.pack(">HBBHH", 0x1722, 3, 0, rid, len(payload))
    return hdr + struct.pack(">H", crc16_ccitt(hdr[:4] + payload)) + payload


def _decode_klj2_as_magic(blob, ident, expect):
    """KLJ2 not recognised: the foreign-magic verdict."""
    return (VD_MAGIC, {}) if blob[:4] == b"KLJ2" else REAL["klj3_decode"](blob, ident, expect)


def _decode_reserved_ignored(blob, ident, expect):
    """The reserved byte ignored: every record's byte 3 cleared and the crc16 re-closed first."""
    out = bytearray(blob)
    vd, applied = REAL["klj3_decode"](blob, ident, expect)
    if vd != VD_REC:
        return vd, applied
    pos, end = k3.HDR, len(out) - 4
    while pos + 10 <= end and out[pos:pos + 2] == b"\x17\x22":
        plen = struct.unpack_from(">H", out, pos + 6)[0]
        if out[pos + 3]:
            out[pos + 3] = 0
            body = bytes(out[pos:pos + 8] + out[pos + 10:pos + 10 + plen])
            out[pos + 8:pos + 10] = struct.pack(">H", crc16_ccitt(body))
        pos += 10 + plen
    return REAL["klj3_decode"](reseal(bytes(out)), ident, expect)


def _key_exclusive_end(rid):
    """A block's last id taken as outside it."""
    key = REAL["key_of_id3"](rid)
    return None if key and rid == k3.LAYOUT.block(key[0]).last else key


def _inventory_last_name_dropped(shape):
    """The shape's last name left out."""
    rows = REAL["inventory3"](shape)
    names = [r for r in rows if r[0] == "NAME"]
    return [r for r in rows if r is not names[-1]] if names else rows


def _split_counts_unchecked(space):
    """The split output's counts taken without the cross-check."""
    return {b["group"]: int(b["count"]) + (1 if b["group"] == "NAME" else 0) for b in space["blocks"]}


def _delta_crc_unchecked(seg, prev, ident, expect):
    """A delta taken without its CRC-32: its trailer resealed first."""
    length = struct.unpack_from("<I", seg, 16)[0]
    if 44 <= length <= len(seg):
        seg = reseal(bytes(seg[:length])) + seg[length:]
    return REAL["_delta_records"](seg, prev, ident, expect)


def _delta_stale_accepted(seg, prev, ident, expect):
    """A delta's sequence never compared with the one before it."""
    return REAL["_delta_records"](seg, struct.unpack_from("<I", seg, 8)[0] - 1, ident, expect)


def _slot_first_wins(slot, ident, expect):
    """Each record's first value kept, not its last: the deltas replayed in reverse."""
    vd, seq, applied, end, torn = REAL["klj3_slot_decode"](slot, ident, expect)
    if vd != VD_OK:
        return vd, seq, applied, end, torn
    first = REAL["_delta_records"](slot[k3.log_start(struct.unpack_from("<I", slot, 16)[0]):], 0, ident, expect)
    if first:
        applied.update(first[1])
    return vd, seq, applied, end, torn


REAL = {name: getattr(k3, name) for name in ("klj3_decode", "key_of_id3", "inventory3", "_delta_records",
                                               "klj3_slot_decode")}
PLANTS = (
    ("a frame's crc16 skipping the record_id", "frame_record3", _frame_crc_short, "round trip"),
    ("KLJ2 refused as a foreign magic", "klj3_decode", _decode_klj2_as_magic, "refusals"),
    ("the reserved header byte ignored", "klj3_decode", _decode_reserved_ignored, "refusals"),
    ("a block's last id outside it", "key_of_id3", _key_exclusive_end, "capacity"),
    ("the last name left out of the inventory", "inventory3", _inventory_last_name_dropped, "ledger"),
    ("the split output's NAME count off by one", "split_counts", _split_counts_unchecked, "split"),
    ("a delta accepted without its CRC-32", "_delta_records", _delta_crc_unchecked, "journal"),
    ("a stale delta accepted", "_delta_records", _delta_stale_accepted, "journal"),
    ("the deltas replayed in reverse", "klj3_slot_decode", _slot_first_wins, "journal"),
)


@contextlib.contextmanager
def planted(name: str, stand_in: Callable) -> Iterator[None]:
    """nvm_klj3's `name` replaced by `stand_in` for one run."""
    real = getattr(k3, name)
    setattr(k3, name, stand_in)
    try:
        yield
    finally:
        setattr(k3, name, real)


def self_test(shapes: list[Built]) -> list[str]:
    """Each plant must turn its rule's check red."""
    out = []
    for label, name, stand_in, rule in PLANTS:
        with planted(name, stand_in):
            try:
                red = [x for b in shapes for x in RULES[rule](b)]
            except Exception as exc:  # noqa: BLE001 - a plant that breaks the check is also red
                red = [f"{type(exc).__name__}: {exc}"]
        if red:
            print(f"  self-test OK: {label}: caught by {rule} ({red[0][:90]})")
        else:
            out.append(f"self-test: {label} was NOT caught by {rule}")
    return out


def main() -> int:
    """Every shipped shape through every rule; with --self-test, the plants too."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--self-test", action="store_true", help="plant one defect per rule; each must be caught")
    ap.add_argument("--config", action="append", type=Path, help="configs (default: every configs/endstation_*.yaml)")
    args = ap.parse_args()
    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    with tempfile.TemporaryDirectory(prefix="klj3.") as tmp:
        try:
            shapes = [built(c, Path(tmp) / c.stem) for c in cfgs]
        except (subprocess.CalledProcessError, OSError, ValueError) as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 2
    found = findings(shapes)
    if not found and args.self_test:
        found = self_test(shapes)
    for x in found:
        print(f"FINDING: {x}")
    if found:
        return 1
    print(f"split saved-state reference (#823): OK across {len(shapes)} shape(s), layout {k3.LAYOUT.layout}, "
          f"{k3.LAYOUT.id_space} ids, NAME {k3.LAYOUT.block('NAME').base} to {k3.LAYOUT.block('NAME').last}"
          + (f", and all {len(PLANTS)} planted defects caught" if args.self_test else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
