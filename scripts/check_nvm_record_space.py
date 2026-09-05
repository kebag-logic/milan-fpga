#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the persisted record set must be COMPLETE, must fit the NVM record
namespace at EVERY shipped shape, and its commit must fit the commit deadline.

WHY THIS EXISTS. The first version of
`docs/design/SAVED_STATE_FASTCONNECT.md` sized the saved set in BYTES and
concluded that whole-image A/B promotion was affordable. That part was right.
What it never checked was the other capacity in the same design: the processor's
NVM port (`KL_pp_nvm_port` in the protocol-processor submodule) addresses a
record by `record_id[7:0]`, and the donor's F07.8 framing says "one record per
item group and index". One record per
writable name at the 8x8 shape of 2026-08 needed 235 ids on its own; the whole
persisted inventory needed 292. The namespace holds 256. The design could not
have been built as written, and no gate said so, because every check in the
tree was counting bytes. That arithmetic forced a BANKED name layout (eight
names per record) and a request that the donor amend F07.8 to allow it.

The SECOND review round found the mirror-image hole in the gate itself: every
check validated only the records `inventory()` chose to emit, so DELETING a
mandatory Milan item made the image smaller and the gate greener. An omission
oracle is therefore checked FIRST, against a ledger derived independently of
the inventory (section "THE LEDGER" below).

The THIRD round found the same class again, one level in: that oracle reduced
the inventory to `Counter(group)` and compared CARDINALITIES. Shifting every
`FMT_IN` tuple from index k to k+1 -- deleting real STREAM_INPUT 0 and
inventing a nonexistent index 9 -- left every count identical and the gate
silent. Three rounds of the same class is a statement about the SHAPE of the
instrument, not its spelling: this gate reasoned about the persisted set as
COUNTS and TABLES, and a count cannot see which items it counted.

So the shape changed. This gate now BUILDS THE IMAGE and READS IT BACK. Every
question that a table could only answer approximately is now answered on
bytes: the exact `(group, index)` key set (not its cardinality), the empty
name that is a legal value rather than an absence, and an image that is
CRC-clean but missing a mandatory record.
`--emit-record-table` publishes the byte offsets of that same image so
`tb/verilator/nvm_backend` can grade the region decoder of the shipping
backing store, `hdl/milan/KL_nvm_backend.sv`, against them.

THE BANKED LAYOUT IS RETIRED (#70, 2026-09-05). #259 retired the 8x8's
nonphysical clusters and the conformant floor fell to 164 of 256 at the worst
shipped shape, so nothing forces the divergence any more; and nothing ever
persisted or decoded a name bank -- no donor gateware decodes one, and no
producer writes a KLJ2 image to any board. The allocation is therefore the
donor's F07.8 rule unchanged, one record per item group and index, with each
user name its own 64-byte record, and the amendment request to the donor is
withdrawn (design page section 4.3).

WHAT IT CHECKS, per config, for the full persisted inventory of Milan v1.2
5.3.5.1 / 5.3.7.1 / 5.3.7.6 / 5.3.8.1 / 5.3.8.2 / 5.3.8.3 / 5.3.8.7 / 5.3.9.1 /
5.3.10.1 / 5.3.11.1 / 5.3.13 plus the three design-affirmative items (donor
`docs/architecture/07_memory_maps.md` 5.1: configuration index, system unique
id, media clock reference):

  0. every mandatory group is PRESENT with the cardinality the shape
     demands                                     -- an omission cannot pass
  1. every allocated record id is unique          -- no aliasing
  2. every id is inside the 8-bit namespace       -- < 256
  3. every group stays inside its allocated block -- shape growth is caught
     at the block boundary, not by a later collision
  4. every record payload fits `MAX_PAYLOAD_P`    -- the port refuses a stream
     it cannot delimit BEFORE any device traffic
  5. the whole image fits one 64 KiB erase block  -- the A/B slot geometry
  6. the allocation is the donor's own F07.8 rule and its conformant floor
     fits the namespace at EVERY shipped shape -- a shape whose record set
     the contract cannot hold is a finding that names it, never a silent
     divergence (that is the situation which once forced banking)
  7. the worst-case commit fits `T-NVM-COMMIT-TIMEOUT` with margin -- the
     deadline of design page section 9.4 is a measured bound, not a guess
  8. the KLJ2 image ROUND TRIPS: encode the inventory, decode it back, and
     every mandatory key returns byte for byte
  9. an EMPTY user name survives -- all 64 bytes zero is a legal AEM string
     and Milan 5.3.13 requires it to persist, so it must never be read as
     "no name stored"
 10. a CRC-CLEAN image that omits ANY mandatory record is REFUSED with zero
     records applied -- absence is not a way to restore a vendor default

THE LEDGER. Check 0 does not ask the inventory what it built. `LEDGER` below
declares, per persisted group, its clause and a cardinality rule evaluated from
`descriptor_counts` in the generated overlay. The writable-name count is
re-derived the same way, from the descriptor types that carry a settable name
slot, and cross-checked against the AEMI image header -- two independent
derivations of the same number, so a builder that changes one without the other
also reddens.

The BINDING block base is READ from the donor RTL (`REC_ID_BASE_P` in
`KL_acmp_nvm_shadow`), never mirrored here: that parameter is already fixed in
landed gateware, so the allocation contract has to bend around it rather than
restate it. The file it is read from is DERIVED through `scripts/pp_srcs.py`
rather than named, so a donor that moves or renames the module is followed
instead of silently missed.

USAGE
  scripts/check_nvm_record_space.py              # every configs/endstation_*.yaml
  scripts/check_nvm_record_space.py --config configs/endstation_ax7101_8x8.yaml
  scripts/check_nvm_record_space.py --mutate collide   # one negative control
  scripts/check_nvm_record_space.py --self-test        # run them all
  scripts/check_nvm_record_space.py --emit-record-table configs/e.yaml -o t.txt

Every `--mutate` arm is a negative control and is EXPECTED to exit 1.
`--self-test` runs all of them and fails if ANY of them passes, so no
assertion here can quietly become vacuous: each arm perturbs exactly one fixed
point and must be caught by the check that owns it.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import struct
import subprocess
import sys
import tempfile
import zlib
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# The contract, the codec and the shape derivation live beside this file; see
# their module docstrings for the split. `FIXED`, `SEAM` and `ALLOC` are the
# containers every `--mutate` control moves IN PLACE - never rebound - which
# is what keeps one shared value behind all four modules.
from nvm_contract import (                                    # noqa: E402
    ALIGN, ALIVE_HEARTBEATS, ALLOC, COMMIT_MARGIN, FIXED, FLASH_PAGE,
    KLJ2_HDR, KLJ2_TRAILER, LEDGER, MAP_ENTRY, MAX_PAYLOAD, NAME_BYTES, PAY,
    REC_HDR, ROOT, SEAM, T_NVM_HEARTBEAT_MS, T_NVM_WRITER_ALIVE_MS,
    T_PP_MAX_MS, T_SE_MAX_MS, VD_OK, VENDOR_DEFAULT_NAME, VERDICT_NAME,
    Donor, Ident, Key, Record, Shape)
from nvm_klj2 import (frame_record, klj2_assemble,            # noqa: E402
                      klj2_decode, name_table, names_from_image,
                      payload_bytes)
from nvm_shape import (binding_base, build, commit_worst_ms,  # noqa: E402
                       conformant_floor, expected_names, expected_records,
                       inventory, layout_version)



def _mut_collide():
    """Two groups share a base -- the uniqueness assertion must fire."""
    ALLOC["FMT_OUT"] = (ALLOC["FMT_IN"][0], ALLOC["FMT_IN"][1])


def _mut_block():
    """A group's block is too small for the shape -- capacity must fire."""
    b, _ = ALLOC["NAME"]
    ALLOC["NAME"] = (b, 8)


def _mut_payload():
    """A record grows past what the port can delimit -- payload must fire."""
    PAY["MCR"] = MAX_PAYLOAD + 1


def _mut_image():
    """The slot shrinks below the image -- the byte bound must fire."""
    FIXED.ERASE_BLOCK = 8 * 1024


def _mut_idspace():
    """The namespace shrinks below the F07.8 floor of the largest shipped
    shape -- the conformance check must fire and name that shape, the
    situation that once forced the banked layout."""
    FIXED.ID_SPACE = 128


def _mut_deadline():
    """The commit deadline drops below the worst-case flash transaction --
    the deadline assertion must fire."""
    FIXED.T_NVM_COMMIT_TIMEOUT_MS = 1000


def _mut_omit_singleton():
    """Delete a mandatory SINGLETON (system unique id) from the inventory."""
    def keep(r: Record) -> bool:
        """True for every row but the system-unique-id singleton."""
        return r[0] != "SUID"
    SEAM.OMIT = keep


def _mut_omit_indexed():
    """Delete a whole mandatory PER-DESCRIPTOR group (presentation offset)."""
    def keep(r: Record) -> bool:
        """True for every row outside the presentation-offset group."""
        return r[0] != "PT_OFS"
    SEAM.OMIT = keep


def _mut_omit_index():
    """Delete ONE index of a per-descriptor group (stream format in, index 0),
    which changes the cardinality without removing the group."""
    def keep(r: Record) -> bool:
        """True for every row but stream format in, index 0."""
        return not (r[0] == "FMT_IN" and r[1] == 0)
    SEAM.OMIT = keep


def _mut_omit_names():
    """Delete every name record -- the Milan 5.3.13 class in full."""
    def keep(r: Record) -> bool:
        """True for every row that carries no user name."""
        return r[0] != "NAME"
    SEAM.OMIT = keep


def _mut_shift_index():
    """Shift every FMT_IN record one index and one id up: real STREAM_INPUT 0
    disappears and a nonexistent index 9 replaces it. Ids stay unique and stay
    inside the block, and the COUNT does not move -- which is why round 3's
    Counter(group) oracle reported zero findings on exactly this."""
    def shift(recs: list[Record]) -> list[Record]:
        """Renumber every stream-format-in row one index and one id up."""
        return [(g, i + 1, None if r is None else r + 1, p, b)
                if g == "FMT_IN" else (g, i, r, p, b)
                for g, i, r, p, b in recs]
    SEAM.XFORM = shift


def _mut_shift_name():
    """The same defect on the NAME ordinals: ordinal 0 disappears and one
    past the last is invented, so the entity name is never persisted while
    the record count is unchanged."""
    def shift(recs: list[Record]) -> list[Record]:
        """Renumber every name row one ordinal and one id up."""
        return [(g, i + 1, None if r is None else r + 1, p, b)
                if g == "NAME" else (g, i, r, p, b)
                for g, i, r, p, b in recs]
    SEAM.XFORM = shift


def _mut_dup_index():
    """Two records claim the SAME (group, index) with DISTINCT ids. Id
    uniqueness is untouched and the key SET is untouched, so only an explicit
    duplicate check can see it -- the shape a partial regeneration leaves."""
    def dup(recs: list[Record]) -> list[Record]:
        """Append a second row claiming FMT_OUT[0] under a different id."""
        out = list(recs)
        for g, i, r, p, b in recs:
            if g == "FMT_OUT" and i == 0 and r is not None:
                out.append((g, i, r + 12, p, b))
                break
        return out
    SEAM.XFORM = dup


def _mut_name_absent_rule():
    """Restore round 3's content-based name presence rule, so an empty name is
    read back as 'no name stored' and the vendor default is restored over it."""
    SEAM.NAME_PRESENCE_FROM_CONTENT = True


def _mut_accept_absent():
    """Restore round 3's section 6.2 sentence -- an allocated id that is simply
    absent is not a failure -- so a CRC-clean image missing a mandatory record
    is accepted and the item silently reverts to its vendor default."""
    SEAM.DECODE_ALLOW_ABSENT = True


MUTATIONS = {
    "collide": _mut_collide,
    "shift_index": _mut_shift_index,
    "shift_name": _mut_shift_name,
    "dup_index": _mut_dup_index,
    "name_absent_rule": _mut_name_absent_rule,
    "accept_absent": _mut_accept_absent,
    "block": _mut_block,
    "payload": _mut_payload,
    "image": _mut_image,
    "idspace": _mut_idspace,
    "deadline": _mut_deadline,
    "omit_singleton": _mut_omit_singleton,
    "omit_indexed": _mut_omit_indexed,
    "omit_index": _mut_omit_index,
    "omit_names": _mut_omit_names,
}


# ---- the exact expectation, derived from the shape and never from the image -
def _class_of(group):
    if group in LEDGER:
        cls, clause, _rule = LEDGER[group]
        return cls, clause
    return "per-name", "Milan 5.3.13"


def record_keys(shape: Shape) -> set[Key]:
    """The exact (group, index) key set this shape requires.

    Round 3's oracle reduced the inventory to `Counter(group)` and compared
    CARDINALITIES, so shifting every FMT_IN tuple from index k to k+1 -- real
    STREAM_INPUT 0 gone, nonexistent index 9 invented -- left every count
    identical and the gate reported zero findings. A SET names both the key
    that went missing and the key that should not exist.
    """
    dc = shape.dc
    want = {(g, i) for g, card in expected_records(dc).items()
            for i in range(card)}
    want |= {("NAME", k) for k in range(expected_names(dc))}
    return want


def expected_payloads(shape: Shape) -> dict[Key, int]:
    """{(group, index): payload length} over exactly `record_keys()`."""
    spi_cl = {p["index"]: p["clusters"] * MAP_ENTRY for p in shape.spi}
    spo_cl = {p["index"]: p["clusters"] * MAP_ENTRY for p in shape.spo}
    out = {}
    for g, i in record_keys(shape):
        if g == "MAPS_IN":
            out[(g, i)] = spi_cl.get(i, 0)
        elif g == "MAPS_OUT":
            out[(g, i)] = spo_cl.get(i, 0)
        elif g == "NAME":
            out[(g, i)] = NAME_BYTES
        else:
            out[(g, i)] = PAY[g]
    return out


def completeness(shape: Shape, recs: list[Record]) -> list[str]:
    """Check 0: the inventory's (group, index) key set must EQUAL the set the
    shape requires -- not merely have the same cardinality per group.

    Graded against `record_keys()` and `expected_names()`, neither of which the
    inventory reads.
    """
    cfg, names = shape.cfg, shape.names
    findings = []

    want_names = expected_names(shape.dc)
    if want_names != names:
        findings.append(
            f"{cfg.stem}: the name ledger derives {want_names} writable names "
            f"from descriptor_counts but the AEMI image header carries "
            f"{names} -- the two derivations disagree")

    want = record_keys(shape)
    got = [(g, i) for g, i, _r, _p, _b in recs]
    have = set(got)

    def _fmt(keys):
        shown = ", ".join(f"{g}[{i}]" for g, i in sorted(keys)[:6])
        return shown + (f" and {len(keys) - 6} more" if len(keys) > 6 else "")

    if (want - have) and (have - want):
        findings.append(
            f"{cfg.stem}: the persisted inventory's record key set is not the "
            f"set this shape requires -- MISSING {_fmt(want - have)}; EXTRA "
            f"{_fmt(have - want)}. The cardinalities agree, which is exactly "
            f"why a count oracle cannot see this")

    for g, i in sorted(want - have)[:6]:
        cls, clause = _class_of(g)
        findings.append(
            f"{cfg.stem}: mandatory {cls} record {g}[{i}] ({clause}) is "
            f"MISSING from the persisted inventory")
    if len(want - have) > 6:
        findings.append(
            f"{cfg.stem}: and {len(want - have) - 6} further mandatory "
            f"record(s) are missing")

    for g, i in sorted(have - want)[:6]:
        findings.append(
            f"{cfg.stem}: the inventory allocates {g}[{i}], which this shape "
            f"does not have -- an EXTRA record for a descriptor that does not "
            f"exist")
    if len(have - want) > 6:
        findings.append(
            f"{cfg.stem}: and {len(have - want) - 6} further record(s) are "
            f"allocated for descriptors this shape does not have")

    for key, n in sorted(Counter(got).items()):
        if n > 1:
            ids = sorted(f"0x{r:02X}" if r is not None else "--"
                         for g, i, r, _p, _b in recs if (g, i) == key)
            findings.append(
                f"{cfg.stem}: {key[0]}[{key[1]}] is claimed by {n} records "
                f"({', '.join(ids)}) -- F07.8 is one record per item group and "
                f"index, so all but one of them is dead weight nothing reads")
    return findings


@dataclass(frozen=True)
class _Img:
    """One shape's KLJ2 image under test, and what it takes to rebuild it."""

    shape: Shape
    recs: list
    donor: Donor
    ident: Ident
    expect: dict


def _frames_for(img, nval, drop=None):
    """{record_id: framed record} for every record that has an id."""
    out = {}
    for g, i, r, p, _b in img.recs:
        if r is None or (g, i) == drop:
            continue
        out[r] = frame_record(r, payload_bytes(g, i, r, p, nval),
                              img.donor.layout)
    return out


def _assemble(img, frames):
    """The container blob for those frames, offsets discarded."""
    return klj2_assemble(frames, img.donor, img.ident)[0]


def _decode(img, blob):
    """(verdict, applied) for one blob, graded against this shape's set."""
    return klj2_decode(blob, img.donor, img.ident, img.expect)


def _round_trip(img):
    """Check 8, as (base frames, applied records or None, findings).

    `applied` is None when the image this gate encoded does not decode at all,
    which is the one failure that makes checks 9..11 unanswerable.
    """
    cfg, names = img.shape.cfg, img.shape.names
    findings = []
    nval = name_table()
    base_frames = _frames_for(img, nval)
    vd, applied = _decode(img, _assemble(img, base_frames))
    if vd != VD_OK:
        findings.append(
            f"{cfg.stem}: the KLJ2 image this gate encoded does not decode -- "
            f"verdict {VERDICT_NAME[vd]}, {len(applied)} record(s) applied")
        return base_frames, None, findings
    for g, i, r, p, _b in img.recs:
        if r is not None and applied.get((g, i)) != payload_bytes(
                g, i, r, p, nval):
            findings.append(
                f"{cfg.stem}: {g}[{i}] (record_id 0x{r:02X}) does not round "
                f"trip through the KLJ2 image")
            break
    return base_frames, applied, findings


def _empty_name_survives(img):
    """Check 9: an empty user name is a LEGAL AEM string, not an absence."""
    cfg, names = img.shape.cfg, img.shape.names
    findings = []
    empty = b"\x00" * NAME_BYTES
    b2 = _assemble(img, _frames_for(img, name_table({0: empty})))
    vd2, ap2 = _decode(img, b2)
    if vd2 != VD_OK:
        findings.append(
            f"{cfg.stem}: an image whose name ordinal 0 is the empty "
            f"string is refused with {VERDICT_NAME[vd2]}")
        return findings
    got = names_from_image(ap2, names)
    if 0 not in got:
        findings.append(
            f"{cfg.stem}: a user name SET to the empty string is not "
            f"restored at all -- the encoding reads 64 zero bytes as "
            f"'no name stored', so the Milan 5.3.13 name a controller "
            f"cleared comes back as the vendor default "
            f"{VENDOR_DEFAULT_NAME.decode()!r}")
    elif got[0] != empty:
        findings.append(
            f"{cfg.stem}: a user name SET to the empty string restores "
            f"as {got[0][:16]!r}..., not 64 zero bytes")
    if len(got) != names:
        findings.append(
            f"{cfg.stem}: {len(got)} of the shape's {names} writable "
            f"name ordinals restore from the image")
    return findings


def _incomplete_is_refused(img, base_frames):
    """Check 11: a CRC-CLEAN image that omits a mandatory record is REFUSED.

    Reported once: every mandatory key fails the same way, and one worked
    example names the rule that was withdrawn.
    """
    cfg = img.shape.cfg
    for key in sorted(img.expect):
        cut = dict(base_frames)
        drop_id = next((r for g, i, r, _p, _b in img.recs
                        if (g, i) == key and r is not None), None)
        if drop_id is None:
            continue
        del cut[drop_id]
        vd4, ap4 = _decode(img, _assemble(img, cut))
        if vd4 == VD_OK or ap4:
            return [
                f"{cfg.stem}: an image with mandatory record {key[0]}[{key[1]}]"
                f" (record_id 0x{drop_id:02X}) deleted and the CRC-32 "
                f"RECOMPUTED was accepted -- verdict {VERDICT_NAME[vd4]}, "
                f"{len(ap4)} record(s) applied. A logically incomplete image "
                f"must be refused with zero records applied, or the item it "
                f"omits silently reverts to its vendor default"]
    return []


def check_image(shape: Shape, recs: list[Record],
                donor: Donor) -> list[str]:
    """Checks 8..11: build the KLJ2 image and read it back.

    Everything here is a question a table cannot answer -- whether an empty
    name is a value or an absence, whether the tail of a bank is derived from
    the shape or from its own bytes, and whether an image that is CRC-clean but
    incomplete is refused.
    """
    #! An allocation whose ids do not fit `record_id[7:0]` cannot be framed at
    #! all. Check 2 owns that finding; re-reporting it here as a codec failure
    #! would bury the reason under a symptom.
    if any(r is None or r >= FIXED.ID_SPACE for _g, _i, r, _p, _b in recs):
        return []
    img = _Img(shape=shape, recs=recs, donor=donor,
               ident=Ident(seq=7, entity_id=0x0011223344556677,
                           model_id=0x8899AABBCCDDEEFF),
               expect=expected_payloads(shape))

    base_frames, applied, findings = _round_trip(img)
    if applied is None:
        return findings
    if shape.names:
        findings += _empty_name_survives(img)
    findings += _incomplete_is_refused(img, base_frames)
    return findings


TABLE_DIR = ROOT / "tb/verilator/nvm_backend"


def render_record_table(shape: Shape, recs: list[Record],
                        donor: Donor) -> str:
    """The byte-exact fixture tb/verilator/nvm_backend grades the RTL against.

    Offsets are relative to the start of the RECORD AREA (byte KLJ2_HDR of the
    image), which is what the backend's `img_base_r` points at.
    """
    layout = donor.layout
    ident = Ident(seq=7, entity_id=0x0011223344556677,
                  model_id=0x8899AABBCCDDEEFF)
    live = [(g, i, r, p) for g, i, r, p, _b in recs if r is not None]
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), layout)
              for g, i, r, p in live}
    blob, offs = klj2_assemble(frames, donor, ident)
    out = [
        "# GENERATED by scripts/check_nvm_record_space.py --emit-record-table",
        "# DO NOT EDIT: the gate rebuilds this file and reports a mismatch.",
        f"shape {shape.cfg.stem}",
        f"layout {layout}",
        f"hdrbytes {KLJ2_HDR}",
        f"imglen {len(blob)}",
        f"crc32 0x{zlib.crc32(blob[:-4]) & 0xFFFFFFFF:08X}",
        f"nrec {len(frames)}",
        "# rec <id> <area_offset> <framed_len> <payload_len> <group> <index>",
    ]
    for g, i, r, p in sorted(live, key=lambda t: t[2]):
        out.append(f"rec 0x{r:02X} {offs[r]} {REC_HDR + p} {p} {g} {i}")
    return "\n".join(out) + "\n"


def check_one(cfg: Path, out: Path, donor: Donor,
              verbose: bool) -> tuple[list[str], int]:
    """Every finding one config earns, with the F07.8 floor its shape
    implies. The floor comes back with the findings because the conformance
    check is a statement about the SET of shipped shapes, not about one."""
    names, dc, spi, spo = build(cfg, out)
    shape = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    recs = inventory(shape, donor.base)
    if SEAM.OMIT is not None:
        recs = [r for r in recs if SEAM.OMIT(r)]
    if SEAM.XFORM is not None:
        recs = SEAM.XFORM(recs)
    findings = completeness(shape, recs)

    seen = {}
    top = -1
    for group, index, rid, payload, block in recs:
        if rid is None:
            findings.append(
                f"{cfg.stem}: {group}[{index}] has no id -- the group's block "
                f"holds {block} and this shape needs {index + 1}")
            continue
        top = max(top, rid)
        if rid >= FIXED.ID_SPACE:
            findings.append(
                f"{cfg.stem}: {group}[{index}] wants record_id {rid} but the "
                f"port's namespace is record_id[7:0] -- {FIXED.ID_SPACE} ids")
        if rid in seen:
            findings.append(
                f"{cfg.stem}: record_id 0x{rid:02X} is claimed by both "
                f"{seen[rid]} and {group}[{index}] -- one of them is lost")
        seen[rid] = f"{group}[{index}]"
        if payload > MAX_PAYLOAD:
            findings.append(
                f"{cfg.stem}: {group}[{index}] payload is {payload} B, over "
                f"MAX_PAYLOAD_P = {MAX_PAYLOAD} -- the port refuses it")

    body = sum(REC_HDR + p for _, _, _, p, _ in recs)
    body += (-body) % ALIGN
    image = KLJ2_HDR + body + KLJ2_TRAILER
    if image > FIXED.ERASE_BLOCK:
        findings.append(
            f"{cfg.stem}: image is {image} B, over one "
            f"{FIXED.ERASE_BLOCK} B erase "
            f"block -- whole-image A/B promotion no longer fits a slot")

    worst = commit_worst_ms(image)
    if FIXED.T_NVM_COMMIT_TIMEOUT_MS < COMMIT_MARGIN * worst:
        findings.append(
            f"{cfg.stem}: T-NVM-COMMIT-TIMEOUT is "
            f"{FIXED.T_NVM_COMMIT_TIMEOUT_MS} ms "
            f"but the worst-case commit of an {image} B image is "
            f"{worst:.0f} ms (tSE {T_SE_MAX_MS} + "
            f"{math.ceil(image / FLASH_PAGE)} page(s) x {T_PP_MAX_MS} ms + "
            f"read-back), and the contract requires {COMMIT_MARGIN}x margin")

    findings += check_image(shape, recs, donor)

    # the committed fixture the Verilator suite reads must still be what this
    # gate would emit at this head, or the RTL is graded against stale bytes
    fixture = TABLE_DIR / f"records_{cfg.stem}.txt"
    if fixture.exists():
        if fixture.read_text() != render_record_table(shape, recs, donor):
            findings.append(
                f"{cfg.stem}: {fixture.relative_to(ROOT)} is STALE -- "
                f"tb/verilator/nvm_backend would grade the region decoder "
                f"against byte offsets this shape no longer has. Regenerate "
                f"it with --emit-record-table")

    floor = conformant_floor(names, dc)
    if verbose:
        print(f"{cfg.stem:<28} names={names:3d} records={len(recs):3d} "
              f"top_id={'--' if top < 0 else f'0x{top:02X}'} "
              f"image={image:6d} B "
              f"({image * 100 // FIXED.ERASE_BLOCK}% of a slot) "
              f"F07.8 floor={floor:3d}/{FIXED.ID_SPACE} "
              f"commit<={worst / 1000.0:.2f} s")
    return findings, floor


def check_deadline_shape() -> list:
    """The shape-independent half of the deadline contract."""
    findings = []
    if T_NVM_WRITER_ALIVE_MS < ALIVE_HEARTBEATS * T_NVM_HEARTBEAT_MS:
        findings.append(
            f"T-NVM-WRITER-ALIVE is {T_NVM_WRITER_ALIVE_MS} ms but the "
            f"contract requires {ALIVE_HEARTBEATS} heartbeats of "
            f"{T_NVM_HEARTBEAT_MS} ms inside it")
    return findings


def _arg_parser():
    """The command line, in one place, so `main` reads as the run it makes."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", action="append", type=Path,
                    help="config to check (default: every configs/endstation_*.yaml)")
    ap.add_argument("--mutate", choices=sorted(MUTATIONS),
                    help="perturb one fixed point so the matching assertion "
                         "must fire (negative control: MUST fail)")
    ap.add_argument("--self-test", action="store_true",
                    help="run every negative control and require each to "
                         "redden, then run the real check")
    ap.add_argument("--emit-record-table", type=Path, metavar="CONFIG",
                    help="write the byte-exact record table for one config "
                         "(the tb/verilator/nvm_backend fixture) and exit")
    ap.add_argument("-o", "--out", type=Path,
                    help="destination for --emit-record-table")
    ap.add_argument("--quiet", action="store_true")
    return ap


def _every_control_reddens():
    """Run each negative control in its OWN process; False if any of them
    passed, which means the assertion it targets has gone vacuous."""
    controls = [f"--mutate={m}" for m in sorted(MUTATIONS)]
    for c in controls:
        r = subprocess.run([sys.executable, __file__, c, "--quiet"],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"SELF-TEST FAILED: negative control {c} PASSED. The "
                  f"assertion it targets is vacuous and this gate is "
                  f"green because it stopped looking.")
            return False
        first = next((ln for ln in r.stdout.splitlines()
                      if ln.startswith("FINDING:")), "(no FINDING line)")
        print(f"self-test OK: {c:<24} exits {r.returncode} -- {first}")
    print()
    return True


def _emit_record_table(cfg, out, donor):
    """Write, or print, the byte-exact fixture for one config."""
    with tempfile.TemporaryDirectory(prefix="nvmrec.") as tmp:
        names, dc, spi, spo = build(cfg, Path(tmp))
    shape = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    recs = inventory(shape, donor.base)
    text = render_record_table(shape, recs, donor)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(f"wrote {out} ({len(text.splitlines())} lines)")
    else:
        sys.stdout.write(text)


def _conformance_findings(floors):
    """Check 6. The allocation is the donor's own F07.8 rule, one record per
    item group and index, so the only way it can stop fitting is a shape
    whose conformant floor overflows record_id[7:0]. That is a finding that
    names the shape and the arithmetic, never a silent divergence: the banked
    NAMES layout that once answered it (2026-08) is retired, because #259
    shrank the shape that forced it and nothing persisted or decoded it.
    """
    findings = []
    for cfg, floor in floors:
        if floor > FIXED.ID_SPACE:
            findings.append(
                f"no F07.8-conformant allocation exists at {cfg}: one record "
                f"per item group and index needs {floor} records and the "
                f"namespace holds {FIXED.ID_SPACE}, so the record contract "
                f"would have to change before that shape can ship")
    return findings


def _report(findings, cfgs, quiet):
    """Print the verdict and return the exit status it carries."""
    if findings:
        print()
        for f in findings[:12]:
            print(f"FINDING: {f}")
        if len(findings) > 12:
            print(f"... and {len(findings) - 12} more of the same shape")
        print(f"\n{len(findings)} finding(s) across {len(cfgs)} config(s)")
        return 1
    if not quiet:
        print(f"\n0 finding(s) across {len(cfgs)} config(s): the inventory's "
              f"(group, index) key set is exactly the set the shape requires "
              f"with no key claimed twice, every persisted "
              f"record has a unique id inside record_id[7:0], every group is "
              f"inside its block, every payload fits MAX_PAYLOAD_P, every "
              f"image fits one erase block, the allocation is the donor's own "
              f"F07.8 rule and its floor fits the namespace at every shipped "
              f"shape, the worst-case commit fits T-NVM-COMMIT-TIMEOUT with "
              f"{COMMIT_MARGIN}x margin, every record round trips through a "
              f"KLJ2 image, an empty user name survives it, and a CRC-clean "
              f"image missing any mandatory record is refused with zero "
              f"records applied")
    return 0


def main() -> int:
    """Exit status for the CLI: 1 when a finding stands or a negative
    control failed to redden, 0 when the shipped shapes all hold."""
    args = _arg_parser().parse_args()

    if args.mutate:
        MUTATIONS[args.mutate]()

    if args.self_test and not _every_control_reddens():
        return 1

    donor = Donor(base=binding_base(), layout=layout_version())

    if args.emit_record_table:
        _emit_record_table(args.emit_record_table, args.out, donor)
        return 0

    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    if not args.quiet:
        print(f"BINDING base read from the donor: "
              f"REC_ID_BASE_P = 0x{donor.base:02X}, "
              f"LAYOUT_VER_P = 0x{donor.layout:02X}")
        print(f"deadlines: "
              f"T-NVM-COMMIT-TIMEOUT = {FIXED.T_NVM_COMMIT_TIMEOUT_MS} ms, "
              f"T-NVM-WRITER-ALIVE = {T_NVM_WRITER_ALIVE_MS} ms, "
              f"heartbeat = {T_NVM_HEARTBEAT_MS} ms")

    findings = check_deadline_shape()
    floors = []
    with tempfile.TemporaryDirectory(prefix="nvmrec.") as tmp:
        for cfg in cfgs:
            f, floor = check_one(cfg, Path(tmp), donor, not args.quiet)
            findings += f
            floors.append((cfg.stem, floor))

    findings += _conformance_findings(floors)
    return _report(findings, cfgs, args.quiet)


if __name__ == "__main__":
    sys.exit(main())
