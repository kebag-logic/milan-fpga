#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_contract.py - the fixed points `check_nvm_record_space.py` is asked about.

Split out of that gate so the three things it holds are separable: THIS file
is the contract - the measured constants, the id allocation, the ledger of
persisted items, the KLJ2/F07.8 wire numbers and the two mutable containers a
negative control is allowed to move. `nvm_klj2.py` is the codec that turns a
record set into an image and back; `nvm_shape.py` derives one config's shape
and its inventory; the gate itself holds the checks, the controls and the CLI.

THE ONE RULE THIS SPLIT DEPENDS ON, and the reason `Contract` and `Seams`
exist at all: a `--mutate` control must MUTATE the container every reader
already holds, never rebind a module name. `FIXED`, `SEAM` and `ALLOC` are
imported by name into three other modules, so a rebinding in one of them
would leave the others reading the pristine value and every negative control
would go green against an assertion that had stopped looking. Attribute and
item assignment on the shared object is what keeps them honest across the
split, exactly as it already kept them honest across `--self-test`'s
subprocesses.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- the fixed points, all of them measured or read, none invented ---------

MAX_PAYLOAD = 1024      # KL_pp_nvm_port MAX_PAYLOAD_P default
REC_HDR = 8             # F07.8: magic, layout_version, record_id, plen, crc16
NAME_BYTES = 64         # AEM name field

#: One inventory row, as `inventory()` emits it and every later check reads
#: it: (group, index, record_id -- None when the group's block cannot reach
#: this index -- payload bytes, block size).
Record = tuple[str, int, int | None, int, int]

#: (group, index): how a record is addressed once its id has been inverted,
#: and the key every expectation in this gate is expressed over.
Key = tuple[str, int]


class Contract:
    """The fixed points a `--mutate` negative control is allowed to move.

    Each of these used to be a module constant that its control rebound with a
    `global` statement. A rebinding leaves the module permanently changed, so
    the arms were order-dependent and only stayed honest because `--self-test`
    spends a fresh subprocess on each one. They are attributes of ONE container
    now: a control MUTATES the container that every reader already holds, so
    nothing is rebound and no arm can leave a value behind for the next.
    """

    def __init__(self):
        #: record_id[7:0], KL_pp_nvm_port manager face
        self.ID_SPACE = 256
        #: N25Q128 smallest erase unit = one A/B slot
        self.ERASE_BLOCK = 64 * 1024
        #: Design page section 9.4: the commit deadline, which must cover the
        #: worst-case flash transaction with margin at EVERY shape. The two
        #: liveness numbers it sits with are in the media section below; only
        #: this one has a control that moves it.
        self.T_NVM_COMMIT_TIMEOUT_MS = 8000


FIXED = Contract()


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
# loop it already runs during an erase. The commit deadline itself is
# `FIXED.T_NVM_COMMIT_TIMEOUT_MS`, because `--mutate=deadline` moves it.
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

# The allocation contract: the donor's F07.8 rule unchanged, one record per
# item group and index, with each user name persisted as one record per
# writable-name ordinal. Each entry is {base, block} and the group's index
# must satisfy 0 <= index < block.
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
    "NAME":       (0x80, 128),
}

# ---- THE LEDGER: what MUST be in the inventory, derived independently ------
#
# `LEDGER` is NOT read by `inventory()`. It is the expectation the inventory is
# graded against, so deleting a mandatory group from the inventory shrinks the
# image and reddens the gate instead of greening it. Each entry is
#   group -> (class, clause, cardinality(descriptor_counts))
# where class is one of "singleton" or "per-descriptor"; user names are one
# record per ordinal and are graded through NAME_SLOTS below.
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

# ---- the seams, so each new rule has a control that turns it off -----------
class Seams:
    """The behaviour a negative control replaces, held the way `Contract`
    holds the numbers: one container the arms MUTATE instead of five module
    names they used to rebind.
    """

    def __init__(self):
        #: post-`inventory()` filter, the seam an omission control perturbs.
        #: The default keeps everything; a `--mutate=omit_*` arm replaces it
        #: with a predicate that drops a mandatory class, exactly as an
        #: external wrapper around `inventory()` would.
        self.OMIT = None
        #: post-`inventory()` REWRITE, the seam an index-set control perturbs.
        #: `OMIT` can only delete; a shift, a replacement or a duplicate
        #: needs to rewrite tuples.
        self.XFORM = None
        #: round 3's rule: "an all-zero slot means no name stored". Milan
        #: 5.3.13 requires the empty name to survive, and the empty AEM string
        #: IS 64 zero bytes, so this rule cannot encode a legitimate value.
        self.NAME_PRESENCE_FROM_CONTENT = False
        #: round 3's section 6.2: "an allocated id that is simply absent is not
        #: a failure. That item was never saved and keeps its vendor default."
        self.DECODE_ALLOW_ABSENT = False


SEAM = Seams()


# ---- the three subjects every check below is asked about -------------------
#
# Almost every function here used to spell one of these out as four to six
# adjacent parameters of the same types, which is how `check_image` came to
# take nine and a caller had no way to check the order. They are one value
# each now, and a signature says WHICH of the three it needs.


@dataclass(frozen=True)
class Donor:
    """The two values read out of the donor RTL, never mirrored here."""

    base: int       # REC_ID_BASE_P, the BINDING block base
    layout: int     # LAYOUT_VER_P, the version every framed record carries


@dataclass(frozen=True)
class Ident:
    """The KLJ2 container's identity words, section 6.1 header."""

    seq: int
    entity_id: int
    model_id: int


@dataclass(frozen=True)
class Shape:
    """One config's persisted shape, as the builder and the overlay report it."""

    cfg: Path
    names: int      # writable name ordinals, from the AEMI image header
    dc: dict        # descriptor_counts, from the generated overlay
    spi: list       # stream_ports.input
    spo: list       # stream_ports.output
