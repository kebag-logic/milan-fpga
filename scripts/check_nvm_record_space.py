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
writable name at the 8x8 shape needs 235 ids on its own; the whole persisted
inventory needs 292. The namespace holds 256. The design could not have been
built as written, and no gate said so, because every check in the tree was
counting bytes.

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
name that is a legal value rather than an absence, the unused tail of the last
name bank, and an image that is CRC-clean but missing a mandatory record.
`--emit-record-table` publishes the byte offsets of that same image so
`tb/verilator/nvm_backend` can grade the region decoder of
`syn/ooc/sizing/KL_nvm_backend_sizer.sv` against them.

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
  6. banking is NECESSARY at some shipped shape   -- the divergence from the
     donor's F07.8 contract has to be forced, never a preference
  7. the worst-case commit fits `T-NVM-COMMIT-TIMEOUT` with margin -- the
     deadline of design page section 9.4 is a measured bound, not a guess
  8. the KLJ2 image ROUND TRIPS: encode the inventory, decode it back, and
     every mandatory key returns byte for byte
  9. an EMPTY user name survives -- all 64 bytes zero is a legal AEM string
     and Milan 5.3.13 requires it to persist, so it must never be read as
     "no name stored"
 10. the unused tail of the last name bank is derived from the SHAPE, never
     from slot content: writing rubbish into the tail changes nothing
 11. a CRC-CLEAN image that omits ANY mandatory record is REFUSED with zero
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
  scripts/check_nvm_record_space.py --flat       # the pre-review allocation:
                                                 # one record per item, no banking
  scripts/check_nvm_record_space.py --mutate collide   # one negative control
  scripts/check_nvm_record_space.py --self-test        # run them all
  scripts/check_nvm_record_space.py --emit-record-table configs/e.yaml -o t.txt

`--flat` and every `--mutate` arm are negative controls and are EXPECTED to
exit 1. `--self-test` runs all of them and fails if ANY of them passes, so no
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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- the fixed points, all of them measured or read, none invented ---------

ID_SPACE = 256          # record_id[7:0], KL_pp_nvm_port manager face
MAX_PAYLOAD = 1024      # KL_pp_nvm_port MAX_PAYLOAD_P default
ERASE_BLOCK = 64 * 1024  # N25Q128 smallest erase unit = one A/B slot
REC_HDR = 8             # F07.8: magic, layout_version, record_id, plen, crc16
NAME_BYTES = 64         # AEM name field
NAMES_PER_BANK = 8      # the banking factor the design page fixes

# ---- KLJ2 container and F07.8 record framing, section 6.1 ------------------
KLJ2_MAGIC   = 0x324A4C4B    # 'KLJ2' when hexdumped
KLJ2_FMT_VER = 0x0002_0000   # {major, minor}
REC_MAGIC    = 0x1722        # F07.8 record magic, big-endian
# layout_version: READ from the donor RTL below, never mirrored here.

#: section 6.2 verdicts. VD_INCOMPLETE is added by review round 4: an image
#: that is CRC-clean but missing a mandatory record used to be ACCEPTED,
#: because "an allocated id that is simply absent is not a failure".
(VD_OK, VD_MAGIC, VD_VER, VD_LEN, VD_CRC, VD_ENT, VD_SHAPE, VD_REC,
 VD_STALE, VD_BLANK, VD_INCOMPLETE) = range(11)
VERDICT_NAME = {
    VD_OK: "VD_OK", VD_MAGIC: "VD_MAGIC", VD_VER: "VD_VER", VD_LEN: "VD_LEN",
    VD_CRC: "VD_CRC", VD_ENT: "VD_ENT", VD_SHAPE: "VD_SHAPE",
    VD_REC: "VD_REC", VD_STALE: "VD_STALE", VD_BLANK: "VD_BLANK",
    VD_INCOMPLETE: "VD_INCOMPLETE",
}

#: A vendor default name, so "restored the default instead of the empty string
#: the controller set" is a DISTINGUISHABLE outcome rather than a silent one.
VENDOR_DEFAULT_NAME = b"Kebag Milan Endstation"
KLJ2_HDR = 40           # KLJ2 container header, 10 words
KLJ2_TRAILER = 4        # CRC-32 word, last
ALIGN = 4               # the record area is zero-padded to a word boundary

# ---- the media, from the datasheet, and the deadlines derived from it ------
# Micron N25Q128 Table 32 "AC Characteristics", MAXIMUM column: tSE = 3 s for
# one 64 KiB sector, tPP = 5 ms for a page program of n <= 256 bytes. The
# read-back runs at the instantiated LiteSPI clock,
# `add_spi_flash(mode="1x", clk_freq=12.5e6)` in sw/litex/milan_soc.py, so one
# byte costs 8 clocks.
T_SE_MAX_MS = 3000      # tSE max, one 64 KiB erase block = one A/B slot
T_PP_MAX_MS = 5         # tPP max, one page program
FLASH_PAGE = 256        # program page size
SPI_HZ = 12_500_000     # milan_soc.py add_spi_flash(clk_freq=12.5e6), 1x mode

# Design page section 9.4. The commit deadline must cover the worst-case flash
# transaction with margin at EVERY shape; the liveness deadline is independent
# of it because the writer services the heartbeat from the same status-poll
# loop it already runs during an erase.
T_NVM_COMMIT_TIMEOUT_MS = 8000
T_NVM_WRITER_ALIVE_MS = 2000
T_NVM_HEARTBEAT_MS = 500
COMMIT_MARGIN = 2       # required ratio of deadline to worst-case transaction
ALIVE_HEARTBEATS = 4    # required heartbeats inside the liveness deadline

# Payload widths in bytes. BINDING is the one the donor already fixed
# (KL_acmp_nvm_shadow: payload_length = 20); the rest are the AEM field widths.
PAY = {
    "CFG_IDX": 2,       # configuration_index u16
    "SUID": 8,          # system_unique_id u64
    "RATE": 4,          # current_sampling_rate u32
    "CLKSRC": 2,        # clock_source_index u16
    "MCR": 66,          # user_mcr_prio u8 + MC domain name 64 B + pad
    "BINDING": 20,      # measured: KL_acmp_nvm_shadow payload_length
    "FMT_IN": 8,        # stream_format u64
    "FMT_OUT": 8,
    "PT_OFS": 4,        # presentation time offset u32 ns
}
MAP_ENTRY = 8           # {stream_index, stream_channel, cluster_offset,
                        #  cluster_channel} x u16

# The banked allocation contract. Each entry is {base, block} and the group's
# index must satisfy 0 <= index < block.
ALLOC = {
    "CFG_IDX":    (0x00, 1),
    "SUID":       (0x01, 1),
    "RATE":       (0x02, 8),
    "CLKSRC":     (0x0A, 8),
    "MCR":        (0x12, 8),
    "BINDING":    (None, 16),   # base READ from the donor RTL
    "FMT_IN":     (0x30, 16),
    "FMT_OUT":    (0x40, 16),
    "PT_OFS":     (0x50, 16),
    "MAPS_IN":    (0x60, 16),
    "MAPS_OUT":   (0x70, 16),
    "NAMES_BANK": (0x80, 128),
}

# ---- THE LEDGER: what MUST be in the inventory, derived independently ------
#
# `LEDGER` is NOT read by `inventory()`. It is the expectation the inventory is
# graded against, so deleting a mandatory group from the inventory shrinks the
# image and reddens the gate instead of greening it. Each entry is
#   group -> (class, clause, cardinality(descriptor_counts))
# where class is one of "singleton", "per-descriptor" or "bank".
LEDGER = {
    "CFG_IDX":  ("singleton", "donor 07 5.1 design decision", lambda d: 1),
    "SUID":     ("singleton", "donor 07 5.1 design decision", lambda d: 1),
    "RATE":     ("per-descriptor", "Milan 5.3.5.1", lambda d: d["AUDIO_UNIT"]),
    "CLKSRC":   ("per-descriptor", "Milan 5.3.11.1", lambda d: d["CLOCK_DOMAIN"]),
    "MCR":      ("per-descriptor", "donor 07 5.1 design decision",
                 lambda d: d["CLOCK_DOMAIN"]),
    "BINDING":  ("per-descriptor", "Milan 5.3.8.2/.3/.7",
                 lambda d: d["STREAM_INPUT"]),
    "FMT_IN":   ("per-descriptor", "Milan 5.3.8.1", lambda d: d["STREAM_INPUT"]),
    "FMT_OUT":  ("per-descriptor", "Milan 5.3.7.1", lambda d: d["STREAM_OUTPUT"]),
    "PT_OFS":   ("per-descriptor", "Milan 5.3.7.6", lambda d: d["STREAM_OUTPUT"]),
    "MAPS_IN":  ("per-descriptor", "Milan 5.3.10.1",
                 lambda d: d["STREAM_PORT_INPUT"]),
    "MAPS_OUT": ("per-descriptor", "Milan 5.3.9.1",
                 lambda d: d["STREAM_PORT_OUTPUT"]),
}

#: settable name slots per descriptor of each type. ENTITY carries two,
#: entity_name and group_name; a type absent from this table has no
#: user-settable name and contributes nothing to Milan 5.3.13.
NAME_SLOTS = {
    "ENTITY": 2, "CONFIGURATION": 1, "AUDIO_UNIT": 1, "STREAM_INPUT": 1,
    "STREAM_OUTPUT": 1, "AVB_INTERFACE": 1, "CLOCK_SOURCE": 1,
    "CLOCK_DOMAIN": 1, "CONTROL": 1, "AUDIO_CLUSTER": 1,
}

#: post-`inventory()` filter, the seam an omission control perturbs. The
#: default keeps everything; a `--mutate=omit_*` arm replaces it with a
#: predicate that drops a mandatory class, exactly as an external wrapper
#: around `inventory()` would.
OMIT = None

#: post-`inventory()` REWRITE, the seam an index-set control perturbs. OMIT can
#: only delete; a shift, a replacement or a duplicate needs to rewrite tuples.
XFORM = None

# ---- decoder behaviour, so each new rule has a control that turns it off ---
#: round 3's rule: "an all-zero slot means no name stored". Milan 5.3.13
#: requires the empty name to survive, and the empty AEM string IS 64 zero
#: bytes, so this rule cannot encode a legitimate value.
NAME_PRESENCE_FROM_CONTENT = False
#: derive the writable-name count from the last non-zero slot instead of from
#: the shape. Identical on every entity whose last name is non-empty.
NAMES_TAIL_FROM_CONTENT = False
#: round 3's section 6.2: "an allocated id that is simply absent is not a
#: failure. That item was never saved and keeps its vendor default."
DECODE_ALLOW_ABSENT = False


def _mut_collide():
    """Two groups share a base -- the uniqueness assertion must fire."""
    ALLOC["FMT_OUT"] = (ALLOC["FMT_IN"][0], ALLOC["FMT_IN"][1])


def _mut_block():
    """A group's block is too small for the shape -- capacity must fire."""
    b, _ = ALLOC["NAMES_BANK"]
    ALLOC["NAMES_BANK"] = (b, 8)


def _mut_payload():
    """A bank grows past what the port can delimit -- payload must fire."""
    global NAMES_PER_BANK
    NAMES_PER_BANK = 32


def _mut_image():
    """The slot shrinks below the image -- the byte bound must fire."""
    global ERASE_BLOCK
    ERASE_BLOCK = 8 * 1024


def _mut_idspace():
    """The namespace grows past the donor-conformant floor -- the necessity
    assertion must fire, because banking would then be a divergence from
    F07.8 that nothing forces."""
    global ID_SPACE
    ID_SPACE = 512


def _mut_deadline():
    """The commit deadline drops below the worst-case flash transaction --
    the deadline assertion must fire."""
    global T_NVM_COMMIT_TIMEOUT_MS
    T_NVM_COMMIT_TIMEOUT_MS = 1000


def _mut_omit_singleton():
    """Delete a mandatory SINGLETON (system unique id) from the inventory."""
    global OMIT

    def keep(r):
        return r[0] != "SUID"
    OMIT = keep


def _mut_omit_indexed():
    """Delete a whole mandatory PER-DESCRIPTOR group (presentation offset)."""
    global OMIT

    def keep(r):
        return r[0] != "PT_OFS"
    OMIT = keep


def _mut_omit_index():
    """Delete ONE index of a per-descriptor group (stream format in, index 0),
    which changes the cardinality without removing the group."""
    global OMIT

    def keep(r):
        return not (r[0] == "FMT_IN" and r[1] == 0)
    OMIT = keep


def _mut_omit_names():
    """Delete every name record -- the Milan 5.3.13 class in full."""
    global OMIT

    def keep(r):
        return r[0] not in ("NAMES_BANK", "NAME")
    OMIT = keep


def _mut_shift_index():
    """Shift every FMT_IN record one index and one id up: real STREAM_INPUT 0
    disappears and a nonexistent index 9 replaces it. Ids stay unique and stay
    inside the block, and the COUNT does not move -- which is why round 3's
    Counter(group) oracle reported zero findings on exactly this."""
    global XFORM

    def shift(recs):
        return [(g, i + 1, None if r is None else r + 1, p, b)
                if g == "FMT_IN" else (g, i, r, p, b)
                for g, i, r, p, b in recs]
    XFORM = shift


def _mut_shift_bank():
    """The same defect on the NAME BANK ordinals: bank 0 disappears and a bank
    one past the last is invented, so the first eight user names are never
    persisted while the bank count is unchanged."""
    global XFORM

    def shift(recs):
        return [(g, i + 1, None if r is None else r + 1, p, b)
                if g == "NAMES_BANK" else (g, i, r, p, b)
                for g, i, r, p, b in recs]
    XFORM = shift


def _mut_dup_index():
    """Two records claim the SAME (group, index) with DISTINCT ids. Id
    uniqueness is untouched and the key SET is untouched, so only an explicit
    duplicate check can see it -- the shape a partial regeneration leaves."""
    global XFORM

    def dup(recs):
        out = list(recs)
        for g, i, r, p, b in recs:
            if g == "FMT_OUT" and i == 0 and r is not None:
                out.append((g, i, r + 12, p, b))
                break
        return out
    XFORM = dup


def _mut_name_absent_rule():
    """Restore round 3's content-based name presence rule, so an empty name is
    read back as 'no name stored' and the vendor default is restored over it."""
    global NAME_PRESENCE_FROM_CONTENT
    NAME_PRESENCE_FROM_CONTENT = True


def _mut_tail_from_content():
    """Derive the used part of the last bank from slot content instead of from
    the shape, which loses any trailing name the controller set to empty."""
    global NAMES_TAIL_FROM_CONTENT
    NAMES_TAIL_FROM_CONTENT = True


def _mut_accept_absent():
    """Restore round 3's section 6.2 sentence -- an allocated id that is simply
    absent is not a failure -- so a CRC-clean image missing a mandatory record
    is accepted and the item silently reverts to its vendor default."""
    global DECODE_ALLOW_ABSENT
    DECODE_ALLOW_ABSENT = True


MUTATIONS = {
    "collide": _mut_collide,
    "shift_index": _mut_shift_index,
    "shift_bank": _mut_shift_bank,
    "dup_index": _mut_dup_index,
    "name_absent_rule": _mut_name_absent_rule,
    "tail_from_content": _mut_tail_from_content,
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

SHADOW_STEM = "KL_acmp_nvm_shadow"
BASE_RE = re.compile(r"parameter\s+logic\s*\[7:0\]\s+REC_ID_BASE_P\s*=\s*8'h([0-9A-Fa-f]{2})")
LAYOUT_RE = re.compile(r"parameter\s+logic\s*\[7:0\]\s+LAYOUT_VER_P\s*=\s*8'h([0-9A-Fa-f]{2})")


def shadow_path() -> Path:
    """Locate the ACMP NVM shadow through the derived submodule source list."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import pp_srcs
    hits = [s for s in pp_srcs.pp_sources()
            if Path(s).stem == SHADOW_STEM]
    if len(hits) != 1:
        sys.exit(f"FATAL: expected exactly one {SHADOW_STEM} source in the "
                 f"derived submodule list, found {len(hits)}. The donor "
                 f"renamed or duplicated it and this gate must be re-pointed, "
                 f"not relaxed.")
    return ROOT / hits[0]


def binding_base() -> int:
    """Read REC_ID_BASE_P out of the donor RTL rather than mirroring it."""
    shadow = shadow_path()
    m = BASE_RE.search(shadow.read_text())
    if not m:
        sys.exit(f"FATAL: REC_ID_BASE_P not found in {shadow.name}; the donor "
                 f"moved the parameter and this gate must be re-pointed, not "
                 f"relaxed.")
    return int(m.group(1), 16)


def layout_version() -> int:
    """Read LAYOUT_VER_P out of the donor RTL, for the same reason as the
    binding base: it is already fixed in landed gateware, and every record this
    gate frames has to carry the value the port will check."""
    shadow = shadow_path()
    m = LAYOUT_RE.search(shadow.read_text())
    if not m:
        sys.exit(f"FATAL: LAYOUT_VER_P not found in {shadow.name}; the donor "
                 f"moved the parameter and this gate must be re-pointed, not "
                 f"relaxed.")
    return int(m.group(1), 16)


def build(cfg: Path, out: Path) -> tuple[int, dict, list, list]:
    """Build one config and return (writable names, descriptor counts, ports)."""
    subprocess.run([sys.executable, str(ROOT / "sw/builder/endstation_builder.py"),
                    str(cfg), "-o", str(out)],
                   check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    stem = cfg.stem
    overlay = out / stem / "aem_overlay.json"
    img = out / f"{stem}.img.bin"
    subprocess.run([sys.executable, str(ROOT / "avdecc/gen_aemi_image.py"),
                    "--overlay", str(overlay), "-o", str(img),
                    "--line-bytes", "576"],
                   check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    blob = img.read_bytes()
    _, names = struct.unpack_from(">HH", blob, 8)
    o = json.loads(overlay.read_text())
    ports = o["stream_ports"]
    return names, o["descriptor_counts"], ports["input"], ports["output"]


def expected_names(dc: dict) -> int:
    """Re-derive the writable-name count from the descriptor shape alone.

    This is the SECOND derivation of a number the AEMI image header also
    carries. Grading the inventory against it catches an inventory that drops
    the name class, and grading it against the header catches a builder that
    changes one without the other.
    """
    return sum(dc.get(t, 0) * slots for t, slots in NAME_SLOTS.items())


def expected_records(dc: dict) -> dict:
    """The mandatory group -> cardinality ledger for one shape."""
    return {g: rule(dc) for g, (_cls, _clause, rule) in LEDGER.items()}


def conformant_floor(names: int, dc: dict) -> int:
    """The record count ANY allocation obeying the donor's F07.8 rule needs.

    F07.8 is "one record per item group and index", so the count is fixed by
    the shape and no allocation can do better. A perfectly packed allocation
    would place them at ids 0 .. floor-1, so `floor > ID_SPACE` is an
    impossibility proof rather than a property of the layout in ALLOC.
    """
    return sum(expected_records(dc).values()) + names


def commit_worst_ms(image: int) -> float:
    """Worst-case flash transaction time for one whole-image A/B commit."""
    pages = math.ceil(image / FLASH_PAGE)
    readback_ms = image * 8 * 1000.0 / SPI_HZ
    return T_SE_MAX_MS + pages * T_PP_MAX_MS + readback_ms


def inventory(names, dc, spi, spo, base, flat):
    """Return the record list: (group, index, id, payload_bytes)."""
    recs = []

    def add(group, index, payload):
        b, block = ALLOC[group]
        if group == "BINDING":
            b = base
        if index >= block:
            recs.append((group, index, None, payload, block))
        else:
            recs.append((group, index, b + index, payload, block))

    add("CFG_IDX", 0, PAY["CFG_IDX"])
    add("SUID", 0, PAY["SUID"])
    for u in range(dc["AUDIO_UNIT"]):
        add("RATE", u, PAY["RATE"])
    for d in range(dc["CLOCK_DOMAIN"]):
        add("CLKSRC", d, PAY["CLKSRC"])
        add("MCR", d, PAY["MCR"])
    for k in range(dc["STREAM_INPUT"]):
        add("BINDING", k, PAY["BINDING"])
        add("FMT_IN", k, PAY["FMT_IN"])
    for i in range(dc["STREAM_OUTPUT"]):
        add("FMT_OUT", i, PAY["FMT_OUT"])
        add("PT_OFS", i, PAY["PT_OFS"])
    for p in spi:
        add("MAPS_IN", p["index"], p["clusters"] * MAP_ENTRY)
    for p in spo:
        add("MAPS_OUT", p["index"], p["clusters"] * MAP_ENTRY)

    if flat:
        # The pre-review allocation: one record per writable name, laid out
        # straight after the last per-index group. This is what the first
        # version of the design page adopted from F07.8 unchanged.
        first = ALLOC["NAMES_BANK"][0]
        for n in range(names):
            recs.append(("NAME", n, first + n, NAME_BYTES, names))
    else:
        banks = (names + NAMES_PER_BANK - 1) // NAMES_PER_BANK
        b, block = ALLOC["NAMES_BANK"]
        for k in range(banks):
            recs.append(("NAMES_BANK", k, b + k if k < block else None,
                         NAMES_PER_BANK * NAME_BYTES, block))
    return recs


# ---- the KLJ2 codec: this gate now builds the image and reads it back -----
#
# Rounds 1, 2 and 3 all found the same class of hole -- a check that reasons
# about the persisted set as counts or tables and therefore cannot see WHICH
# items it counted. Bytes settle every one of those questions, so the codec
# below is the instrument, and the checks are asked of an image rather than of
# a list.

_CRC16_TAB = []
for _b in range(256):
    _c = _b << 8
    for _ in range(8):
        _c = ((_c << 1) ^ 0x1021) & 0xFFFF if _c & 0x8000 else (_c << 1) & 0xFFFF
    _CRC16_TAB.append(_c)


def crc16_ccitt(data, crc=0xFFFF):
    """CCITT-FALSE (poly 0x1021, init 0xFFFF), the donor's `crc16_f()` in
    `KL_acmp_nvm_shadow.sv`, table-driven so the omission sweep is affordable."""
    for b in data:
        crc = ((crc << 8) & 0xFFFF) ^ _CRC16_TAB[((crc >> 8) ^ b) & 0xFF]
    return crc


def id_blocks(base):
    """(group, base, block) for every allocated group, BINDING resolved."""
    return [(g, base if g == "BINDING" else b, blk)
            for g, (b, blk) in ALLOC.items()]


def key_of_id(rid, base, flat):
    """Invert the section 4.2 allocation: record_id -> (group, index)."""
    for g, b, blk in id_blocks(base):
        if b is not None and b <= rid < b + blk:
            return ("NAME", rid - b) if (flat and g == "NAMES_BANK") \
                else (g, rid - b)
    return None


def frame_record(rid, payload, layout):
    """One F07.8 frame: {magic 0x1722, layout_version, record_id,
    payload_length, crc16} big-endian, then the payload. The crc16 covers the
    header without its own two bytes and then the payload -- the donor's
    "header-sans-crc + payload" accumulate."""
    hdr = struct.pack(">HBBH", REC_MAGIC, layout, rid, len(payload))
    return hdr + struct.pack(">H", crc16_ccitt(hdr + payload)) + payload


def klj2_assemble(frames, layout, seq, entity_id, model_id):
    """Concatenate framed records in ASCENDING record_id (section 6.1) and wrap
    them in the container. Returns (blob, {record_id: offset inside the record
    area}) -- the offsets tb/verilator/nvm_backend grades the RTL against."""
    body, offs = b"", {}
    for rid in sorted(frames):
        offs[rid] = len(body)
        body += frames[rid]
    body += b"\x00" * ((-len(body)) % ALIGN)
    img_len = KLJ2_HDR + len(body) + KLJ2_TRAILER
    hdr = struct.pack("<10I", KLJ2_MAGIC, KLJ2_FMT_VER, seq, len(frames),
                      img_len,
                      entity_id & 0xFFFFFFFF, (entity_id >> 32) & 0xFFFFFFFF,
                      model_id & 0xFFFFFFFF, (model_id >> 32) & 0xFFFFFFFF,
                      layout)
    blob = hdr + body
    return blob + struct.pack("<I", zlib.crc32(blob) & 0xFFFFFFFF), offs


def klj2_decode(blob, layout, entity_id, model_id, expect, base, flat):
    """Apply ZERO records unless every section 6.2 test passes.

    `expect` is the exact per-shape mandatory set, {(group, index): payload
    length}, derived from the LEDGER and the descriptor shape rather than from
    the image. Round 3's acceptance order validated only the records that were
    PRESENT and said in as many words that an allocated id which is simply
    absent is not a failure, so a CRC-clean image could omit any mandatory
    item, publish an accepted sequence and silently restore a changed value to
    its vendor default. That sentence is withdrawn; absence is now VD_INCOMPLETE.
    """
    if len(blob) < KLJ2_HDR + KLJ2_TRAILER:
        return VD_LEN, {}
    if all(b == 0xFF for b in blob):
        return VD_BLANK, {}
    magic, ver, _seq, nrec, img_len, elo, ehi, mlo, mhi, rlay = \
        struct.unpack_from("<10I", blob, 0)
    if magic != KLJ2_MAGIC:
        return VD_MAGIC, {}
    if (ver >> 16) != (KLJ2_FMT_VER >> 16):
        return VD_VER, {}
    if not (44 <= img_len <= 65536) or len(blob) != img_len:
        return VD_LEN, {}
    if (zlib.crc32(blob[:-4]) & 0xFFFFFFFF) != \
            struct.unpack_from("<I", blob, img_len - 4)[0]:
        return VD_CRC, {}
    if (elo | (ehi << 32)) != entity_id:
        return VD_ENT, {}
    if (mlo | (mhi << 32)) != model_id:
        return VD_SHAPE, {}
    if rlay != layout:
        return VD_REC, {}

    applied, pos, end, last = {}, KLJ2_HDR, img_len - KLJ2_TRAILER, -1
    for _ in range(nrec):
        if pos + REC_HDR > end:
            return VD_LEN, {}
        rmagic, rver, rid, plen = struct.unpack_from(">HBBH", blob, pos)
        rcrc = struct.unpack_from(">H", blob, pos + 6)[0]
        if rmagic != REC_MAGIC or rver != layout:
            return VD_REC, {}
        if pos + REC_HDR + plen > end:
            return VD_LEN, {}
        pay = blob[pos + REC_HDR:pos + REC_HDR + plen]
        if crc16_ccitt(blob[pos:pos + 6] + pay) != rcrc:
            return VD_REC, {}
        if rid <= last:                     # section 6.1: ascending, normative
            return VD_REC, {}
        last = rid
        key = key_of_id(rid, base, flat)
        if key is None or key not in expect or expect[key] != plen:
            return VD_REC, {}
        applied[key] = pay
        pos += REC_HDR + plen
    if pos + ((-(pos - KLJ2_HDR)) % ALIGN) != end:
        return VD_LEN, {}
    if set(expect) - set(applied) and not DECODE_ALLOW_ABSENT:
        return VD_INCOMPLETE, {}
    return VD_OK, applied


def name_table(n_names, overrides=None):
    """ordinal -> the 64-byte AEM string the entity currently holds.

    A name is a fixed 64-byte NUL-padded AEM string and `SET_NAME` writes all
    eight 64-bit lanes with no non-zero requirement, so EVERY 64-byte value is
    legal -- including all zeros, which is the empty string.
    """
    over = overrides or {}

    def val(ordinal):
        if ordinal in over:
            return over[ordinal]
        if ordinal >= n_names:
            return b"\x00" * NAME_BYTES       # unused tail of the last bank
        return (VENDOR_DEFAULT_NAME + b" %d" % ordinal)[:NAME_BYTES] \
            .ljust(NAME_BYTES, b"\x00")
    return val


def payload_bytes(group, index, rid, plen, nval=None):
    """Deterministic record content.

    With `nval`, a name bank is the eight 64-byte slots of ordinals
    8*index .. 8*index+7. Without it every record follows one arithmetic rule,
    which is the form `--emit-record-table` publishes: the C++ in
    tb/verilator/nvm_backend regenerates the same bytes independently, so a
    disagreement about WHERE a record starts shows up as a byte mismatch
    instead of as agreement about nothing.
    """
    if group == "NAMES_BANK" and nval is not None:
        return b"".join(nval(index * NAMES_PER_BANK + slot)
                        for slot in range(NAMES_PER_BANK))
    return bytes(((rid * 131 + j * 17) & 0xFF) for j in range(plen))


def names_from_image(applied, n_names):
    """ordinal -> 64 bytes, for the ordinals THIS SHAPE has.

    Presence is a property of the SHAPE, never of the content. Ordinal
    >= n_names maps to no descriptor, so the tail of the last bank is never
    read, and an all-zero slot INSIDE the shape is therefore the empty name --
    a legal value Milan 5.3.13 requires to survive -- rather than an absence.
    """
    if NAMES_TAIL_FROM_CONTENT:
        n_names = 0
        for (g, i), pay in applied.items():
            if g != "NAMES_BANK":
                continue
            for slot in range(NAMES_PER_BANK):
                if any(pay[slot * NAME_BYTES:(slot + 1) * NAME_BYTES]):
                    n_names = max(n_names, i * NAMES_PER_BANK + slot + 1)
    out = {}
    for k in range(n_names):
        bank, slot = divmod(k, NAMES_PER_BANK)
        pay = applied.get(("NAMES_BANK", bank))
        if pay is None:
            continue
        v = pay[slot * NAME_BYTES:(slot + 1) * NAME_BYTES]
        if NAME_PRESENCE_FROM_CONTENT and not any(v):
            continue                        # round 3: "no name stored"
        out[k] = v
    return out


# ---- the exact expectation, derived from the shape and never from the image -
def _class_of(group):
    if group in LEDGER:
        cls, clause, _rule = LEDGER[group]
        return cls, clause
    return ("bank" if group == "NAMES_BANK" else "per-name"), "Milan 5.3.13"


def record_keys(names, dc, flat):
    """The exact (group, index) key set this shape requires.

    Round 3's oracle reduced the inventory to `Counter(group)` and compared
    CARDINALITIES, so shifting every FMT_IN tuple from index k to k+1 -- real
    STREAM_INPUT 0 gone, nonexistent index 9 invented -- left every count
    identical and the gate reported zero findings. A SET names both the key
    that went missing and the key that should not exist.
    """
    want = {(g, i) for g, card in expected_records(dc).items()
            for i in range(card)}
    n = expected_names(dc)
    if flat:
        want |= {("NAME", k) for k in range(n)}
    else:
        want |= {("NAMES_BANK", k)
                 for k in range((n + NAMES_PER_BANK - 1) // NAMES_PER_BANK)}
    return want


def expected_payloads(names, dc, spi, spo, flat):
    """{(group, index): payload length} over exactly `record_keys()`."""
    spi_cl = {p["index"]: p["clusters"] * MAP_ENTRY for p in spi}
    spo_cl = {p["index"]: p["clusters"] * MAP_ENTRY for p in spo}
    out = {}
    for g, i in record_keys(names, dc, flat):
        if g == "MAPS_IN":
            out[(g, i)] = spi_cl.get(i, 0)
        elif g == "MAPS_OUT":
            out[(g, i)] = spo_cl.get(i, 0)
        elif g == "NAMES_BANK":
            out[(g, i)] = NAMES_PER_BANK * NAME_BYTES
        elif g == "NAME":
            out[(g, i)] = NAME_BYTES
        else:
            out[(g, i)] = PAY[g]
    return out


def completeness(cfg, recs, names, dc, flat):
    """Check 0: the inventory's (group, index) key set must EQUAL the set the
    shape requires -- not merely have the same cardinality per group.

    Graded against `record_keys()` and `expected_names()`, neither of which the
    inventory reads.
    """
    findings = []

    want_names = expected_names(dc)
    if want_names != names:
        findings.append(
            f"{cfg.stem}: the name ledger derives {want_names} writable names "
            f"from descriptor_counts but the AEMI image header carries "
            f"{names} -- the two derivations disagree")

    want = record_keys(names, dc, flat)
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


def check_image(cfg, recs, names, dc, spi, spo, base, flat, layout):
    """Checks 8..11: build the KLJ2 image and read it back.

    Everything here is a question a table cannot answer -- whether an empty
    name is a value or an absence, whether the tail of a bank is derived from
    the shape or from its own bytes, and whether an image that is CRC-clean but
    incomplete is refused.
    """
    ENT, MODEL, SEQ = 0x0011223344556677, 0x8899AABBCCDDEEFF, 7
    findings = []
    #! An allocation whose ids do not fit `record_id[7:0]` cannot be framed at
    #! all. Check 2 owns that finding; re-reporting it here as a codec failure
    #! would bury the reason under a symptom.
    if any(r is None or r >= ID_SPACE for _g, _i, r, _p, _b in recs):
        return findings
    expect = expected_payloads(names, dc, spi, spo, flat)
    banks = (names + NAMES_PER_BANK - 1) // NAMES_PER_BANK

    def frames_for(nval, drop=None):
        out = {}
        for g, i, r, p, _b in recs:
            if r is None or (g, i) == drop:
                continue
            out[r] = frame_record(r, payload_bytes(g, i, r, p, nval), layout)
        return out

    def decode(blob):
        return klj2_decode(blob, layout, ENT, MODEL, expect, base, flat)

    # 8. round trip
    nval = name_table(names)
    base_frames = frames_for(nval)
    blob, _offs = klj2_assemble(base_frames, layout, SEQ, ENT, MODEL)
    vd, applied = decode(blob)
    if vd != VD_OK:
        findings.append(
            f"{cfg.stem}: the KLJ2 image this gate encoded does not decode -- "
            f"verdict {VERDICT_NAME[vd]}, {len(applied)} record(s) applied")
        return findings
    for g, i, r, p, _b in recs:
        if r is not None and applied.get((g, i)) != payload_bytes(
                g, i, r, p, nval):
            findings.append(
                f"{cfg.stem}: {g}[{i}] (record_id 0x{r:02X}) does not round "
                f"trip through the KLJ2 image")
            break

    if not flat and names:
        # 9. an EMPTY user name is a legal AEM string and must survive
        empty = b"\x00" * NAME_BYTES
        b2, _ = klj2_assemble(frames_for(name_table(names, {0: empty})),
                              layout, SEQ, ENT, MODEL)
        vd2, ap2 = decode(b2)
        if vd2 != VD_OK:
            findings.append(
                f"{cfg.stem}: an image whose name ordinal 0 is the empty "
                f"string is refused with {VERDICT_NAME[vd2]}")
        else:
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

        # 10. the unused tail of the last bank is derived from the SHAPE
        if banks * NAMES_PER_BANK > names:
            junk = {o: b"\xFF" * NAME_BYTES
                    for o in range(names, banks * NAMES_PER_BANK)}
            b3, _ = klj2_assemble(frames_for(name_table(names, junk)),
                                  layout, SEQ, ENT, MODEL)
            vd3, ap3 = decode(b3)
            if vd3 != VD_OK or names_from_image(ap3, names) != \
                    names_from_image(applied, names):
                findings.append(
                    f"{cfg.stem}: rubbish written into the "
                    f"{banks * NAMES_PER_BANK - names} unused slot(s) of the "
                    f"last name bank changed what restores -- the tail must "
                    f"follow from the shape's {names} writable names, never "
                    f"from slot content")

    # 11. a CRC-clean image that omits a mandatory record must be REFUSED
    for key in sorted(expect):
        cut = {r: f for r, f in base_frames.items()}
        drop_id = next((r for g, i, r, _p, _b in recs
                        if (g, i) == key and r is not None), None)
        if drop_id is None:
            continue
        del cut[drop_id]
        b4, _ = klj2_assemble(cut, layout, SEQ, ENT, MODEL)
        vd4, ap4 = decode(b4)
        if vd4 == VD_OK or ap4:
            findings.append(
                f"{cfg.stem}: an image with mandatory record {key[0]}[{key[1]}]"
                f" (record_id 0x{drop_id:02X}) deleted and the CRC-32 "
                f"RECOMPUTED was accepted -- verdict {VERDICT_NAME[vd4]}, "
                f"{len(ap4)} record(s) applied. A logically incomplete image "
                f"must be refused with zero records applied, or the item it "
                f"omits silently reverts to its vendor default")
            break
    return findings


TABLE_DIR = ROOT / "tb/verilator/nvm_backend"


def render_record_table(cfg, recs, layout):
    """The byte-exact fixture tb/verilator/nvm_backend grades the RTL against.

    Offsets are relative to the start of the RECORD AREA (byte KLJ2_HDR of the
    image), which is what the backend's `img_base_r` points at.
    """
    ENT, MODEL, SEQ = 0x0011223344556677, 0x8899AABBCCDDEEFF, 7
    live = [(g, i, r, p) for g, i, r, p, _b in recs if r is not None]
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), layout)
              for g, i, r, p in live}
    blob, offs = klj2_assemble(frames, layout, SEQ, ENT, MODEL)
    out = [
        "# GENERATED by scripts/check_nvm_record_space.py --emit-record-table",
        "# DO NOT EDIT: the gate rebuilds this file and reports a mismatch.",
        f"shape {cfg.stem}",
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


def check_one(cfg, out, base, flat, verbose, layout):
    names, dc, spi, spo = build(cfg, out)
    recs = inventory(names, dc, spi, spo, base, flat)
    if OMIT is not None:
        recs = [r for r in recs if OMIT(r)]
    if XFORM is not None:
        recs = XFORM(recs)
    findings = completeness(cfg, recs, names, dc, flat)

    seen = {}
    top = -1
    for group, index, rid, payload, block in recs:
        if rid is None:
            findings.append(
                f"{cfg.stem}: {group}[{index}] has no id -- the group's block "
                f"holds {block} and this shape needs {index + 1}")
            continue
        top = max(top, rid)
        if rid >= ID_SPACE:
            findings.append(
                f"{cfg.stem}: {group}[{index}] wants record_id {rid} but the "
                f"port's namespace is record_id[7:0] -- {ID_SPACE} ids")
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
    if image > ERASE_BLOCK:
        findings.append(
            f"{cfg.stem}: image is {image} B, over one {ERASE_BLOCK} B erase "
            f"block -- whole-image A/B promotion no longer fits a slot")

    worst = commit_worst_ms(image)
    if T_NVM_COMMIT_TIMEOUT_MS < COMMIT_MARGIN * worst:
        findings.append(
            f"{cfg.stem}: T-NVM-COMMIT-TIMEOUT is {T_NVM_COMMIT_TIMEOUT_MS} ms "
            f"but the worst-case commit of an {image} B image is "
            f"{worst:.0f} ms (tSE {T_SE_MAX_MS} + "
            f"{math.ceil(image / FLASH_PAGE)} page(s) x {T_PP_MAX_MS} ms + "
            f"read-back), and the contract requires {COMMIT_MARGIN}x margin")

    findings += check_image(cfg, recs, names, dc, spi, spo, base, flat, layout)

    # the committed fixture the Verilator suite reads must still be what this
    # gate would emit at this head, or the RTL is graded against stale bytes
    fixture = TABLE_DIR / f"records_{cfg.stem}.txt"
    if fixture.exists() and not flat:
        if fixture.read_text() != render_record_table(cfg, recs, layout):
            findings.append(
                f"{cfg.stem}: {fixture.relative_to(ROOT)} is STALE -- "
                f"tb/verilator/nvm_backend would grade the region decoder "
                f"against byte offsets this shape no longer has. Regenerate "
                f"it with --emit-record-table")

    floor = conformant_floor(names, dc)
    if verbose:
        print(f"{cfg.stem:<28} names={names:3d} records={len(recs):3d} "
              f"top_id={'--' if top < 0 else f'0x{top:02X}'} "
              f"image={image:6d} B ({image * 100 // ERASE_BLOCK}% of a slot) "
              f"F07.8 floor={floor:3d}/{ID_SPACE} "
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", action="append", type=Path,
                    help="config to check (default: every configs/endstation_*.yaml)")
    ap.add_argument("--flat", action="store_true",
                    help="the pre-review allocation, one record per item "
                         "(negative control: MUST fail at 8x8)")
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
    args = ap.parse_args()

    if args.mutate:
        MUTATIONS[args.mutate]()

    if args.self_test:
        controls = ["--flat"] + [f"--mutate={m}" for m in sorted(MUTATIONS)]
        for c in controls:
            r = subprocess.run([sys.executable, __file__, c, "--quiet"],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 0:
                print(f"SELF-TEST FAILED: negative control {c} PASSED. The "
                      f"assertion it targets is vacuous and this gate is "
                      f"green because it stopped looking.")
                return 1
            first = next((ln for ln in r.stdout.splitlines()
                          if ln.startswith("FINDING:")), "(no FINDING line)")
            print(f"self-test OK: {c:<24} exits {r.returncode} -- {first}")
        print()

    base = binding_base()
    layout = layout_version()

    if args.emit_record_table:
        cfg = args.emit_record_table
        with tempfile.TemporaryDirectory(prefix="nvmrec.") as tmp:
            names, dc, spi, spo = build(cfg, Path(tmp))
        recs = inventory(names, dc, spi, spo, base, False)
        text = render_record_table(cfg, recs, layout)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text)
            print(f"wrote {args.out} ({len(text.splitlines())} lines)")
        else:
            sys.stdout.write(text)
        return 0

    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    if not args.quiet:
        print(f"BINDING base read from the donor: REC_ID_BASE_P = 0x{base:02X}, "
              f"LAYOUT_VER_P = 0x{layout:02X}")
        print(f"deadlines: T-NVM-COMMIT-TIMEOUT = {T_NVM_COMMIT_TIMEOUT_MS} ms, "
              f"T-NVM-WRITER-ALIVE = {T_NVM_WRITER_ALIVE_MS} ms, "
              f"heartbeat = {T_NVM_HEARTBEAT_MS} ms")

    findings = check_deadline_shape()
    floors = []
    with tempfile.TemporaryDirectory(prefix="nvmrec.") as tmp:
        for cfg in cfgs:
            f, floor = check_one(cfg, Path(tmp), base, args.flat,
                                 not args.quiet, layout)
            findings += f
            floors.append((cfg.stem, floor))

    # Check 6. Banking is a DIVERGENCE from the donor's F07.8 contract, so it
    # has to be forced by a shipped shape. If the conformant allocation fits
    # everywhere, the divergence is unjustified and this gate says so rather
    # than blessing it.
    if not args.flat and floors:
        worst_cfg, worst_floor = max(floors, key=lambda t: t[1])
        if worst_floor <= ID_SPACE:
            findings.append(
                f"banking is NOT necessary: the donor-conformant F07.8 "
                f"allocation needs at most {worst_floor} records "
                f"({worst_cfg}) and the namespace holds {ID_SPACE} -- one "
                f"record per item group and index fits every shipped shape, "
                f"so the divergence from F07.8 has nothing forcing it")

    if findings:
        print()
        for f in findings[:12]:
            print(f"FINDING: {f}")
        if len(findings) > 12:
            print(f"... and {len(findings) - 12} more of the same shape")
        print(f"\n{len(findings)} finding(s) across {len(cfgs)} config(s)")
        return 1
    if not args.quiet:
        print(f"\n0 finding(s) across {len(cfgs)} config(s): the inventory's "
              f"(group, index) key set is exactly the set the shape requires "
              f"with no key claimed twice, every persisted "
              f"record has a unique id inside record_id[7:0], every group is "
              f"inside its block, every payload fits MAX_PAYLOAD_P, every "
              f"image fits one erase block, banking is forced by a shipped "
              f"shape, the worst-case commit fits T-NVM-COMMIT-TIMEOUT with "
              f"{COMMIT_MARGIN}x margin, every record round trips through a "
              f"KLJ2 image, an empty user name survives it, the unused tail of "
              f"the last name bank follows from the shape, and a CRC-clean "
              f"image missing any mandatory record is refused with zero "
              f"records applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
