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


MUTATIONS = {
    "collide": _mut_collide,
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


def completeness(cfg, recs, names, dc, flat):
    """Check 0: every mandatory group present, at the ledger's cardinality.

    Graded against `LEDGER` and `expected_names()`, neither of which the
    inventory reads, so an inventory that drops a mandatory item cannot make
    this quiet.
    """
    findings = []
    got = Counter(g for g, _i, _r, _p, _b in recs)

    want_names = expected_names(dc)
    if want_names != names:
        findings.append(
            f"{cfg.stem}: the name ledger derives {want_names} writable names "
            f"from descriptor_counts but the AEMI image header carries "
            f"{names} -- the two derivations disagree")

    for group, want in sorted(expected_records(dc).items()):
        cls, clause, _rule = LEDGER[group]
        have = got.get(group, 0)
        if have == 0 and want > 0:
            findings.append(
                f"{cfg.stem}: mandatory {cls} group {group} ({clause}) is "
                f"MISSING from the persisted inventory -- the shape needs "
                f"{want} record(s) and none were generated")
        elif have != want:
            findings.append(
                f"{cfg.stem}: mandatory {cls} group {group} ({clause}) has "
                f"{have} record(s) but the shape needs {want}")

    name_group = "NAME" if flat else "NAMES_BANK"
    have = got.get(name_group, 0)
    want = (want_names if flat
            else (want_names + NAMES_PER_BANK - 1) // NAMES_PER_BANK)
    if have == 0 and want > 0:
        findings.append(
            f"{cfg.stem}: mandatory bank group {name_group} (Milan 5.3.13) is "
            f"MISSING from the persisted inventory -- the shape needs {want} "
            f"record(s) for {want_names} user-settable name(s) and none were "
            f"generated")
    elif have != want:
        findings.append(
            f"{cfg.stem}: mandatory bank group {name_group} (Milan 5.3.13) has "
            f"{have} record(s) but {want_names} name(s) need {want}")
    elif not flat and have * NAMES_PER_BANK < want_names:
        findings.append(
            f"{cfg.stem}: {have} name bank(s) of {NAMES_PER_BANK} cover "
            f"{have * NAMES_PER_BANK} name slot(s), short of {want_names}")
    return findings


def check_one(cfg, out, base, flat, verbose):
    names, dc, spi, spo = build(cfg, out)
    recs = inventory(names, dc, spi, spo, base, flat)
    if OMIT is not None:
        recs = [r for r in recs if OMIT(r)]
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

    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    base = binding_base()
    if not args.quiet:
        print(f"BINDING base read from the donor: REC_ID_BASE_P = 0x{base:02X}")
        print(f"deadlines: T-NVM-COMMIT-TIMEOUT = {T_NVM_COMMIT_TIMEOUT_MS} ms, "
              f"T-NVM-WRITER-ALIVE = {T_NVM_WRITER_ALIVE_MS} ms, "
              f"heartbeat = {T_NVM_HEARTBEAT_MS} ms")

    findings = check_deadline_shape()
    floors = []
    with tempfile.TemporaryDirectory(prefix="nvmrec.") as tmp:
        for cfg in cfgs:
            f, floor = check_one(cfg, Path(tmp), base, args.flat,
                                 not args.quiet)
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
        print(f"\n0 finding(s) across {len(cfgs)} config(s): every mandatory "
              f"group is present at the shape's cardinality, every persisted "
              f"record has a unique id inside record_id[7:0], every group is "
              f"inside its block, every payload fits MAX_PAYLOAD_P, every "
              f"image fits one erase block, banking is forced by a shipped "
              f"shape, and the worst-case commit fits T-NVM-COMMIT-TIMEOUT "
              f"with {COMMIT_MARGIN}x margin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
