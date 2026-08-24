# Saved state and fast connect — the backing store decision

> **Corrected after review round 1, and the correction changed the design.**
> The first version of this page sized the saved record set in BYTES, found it
> fitted one erase block, and stopped. It never checked the OTHER capacity in
> the same design: the processor addresses a record by `record_id[7:0]`, so the
> namespace holds 256 records, and one record per persisted item needs **292**
> at the 8x8 shape. The set did not fit, and the page said it did.
>
> What changed, and what did not:
>
> | | before | after |
> |---|---|---|
> | whole-image A/B promotion into the reserved `journal` slots | decided | **unchanged** |
> | media owned by firmware through the existing LiteSPI master | decided | **unchanged** |
> | record namespace inside the image | one record per item group and index | **changed**: names are banked, section 4 |
> | the on-flash container | KLJ1 v1 "carried forward unchanged" | **changed**: a new version, KLJ2, section 6 |
> | the backend's memory and the transfer mechanism | left open | **decided**: section 8 |
> | `nvm_backed_o` | asserts once a writer has answered | **changed**: live, with a deadline and a revocation list, section 9 |
> | the area claim | borrowed issue #69's unrelated LUT delta | **corrected**: section 8.3 says what is settled and what is not measured |
> | "three source files cite this page" | three | **corrected**: two, section 5 and the note below |
>
> A decision record whose arithmetic was corrected is a better artifact than one
> that quietly does not add up. The correction is recorded here rather than
> silently applied, and on issue #70.

Milan v1.2 names eight things a PAAD-AE shall keep across a power cycle, plus
the bound state, the binding parameters and the started/stopped state. This
device keeps none of them. `KL_pp_shadow` answers the processor's NVM port with
a blank-flash responder: reads return `0xFF`, writes are accepted and discarded,
erase completes. A restore walk therefore always finds blank flash, restores
zero records, and -- until the wrapper started publishing `nvm_backed_o` --
reported success for it.

This page is the **decision record** issue #70's first work item asks for:
which media backs those records, who owns the write path, how the records are
named inside the image, and what the fabric is allowed to claim about a restore.
It does not describe a built system. Every row below is marked with what proves
it.

> **A page of this name existed before and was deleted** in `eff99a9c`, the
> commit that substituted the legacy 1722.1/SRP plane for the protocol
> processor. It described an architecture that no longer exists -- a CSR ingest
> group the fabric consumed at boot -- and deleting it with the plane was right.
> What was NOT right is that source files still cite it by section, and nothing
> caught that: `scripts/check_doc_paths.py` reads `git ls-files '*.md'`, so a
> citation inside a `.py` or `.sv` comment is invisible to it. The exact
> inventory, re-derived at this head rather than restated from round 1, is in
> section 5.1. The gate gap is filed separately.

## Contents

- **[1. Status](#1-status)** -- A row per piece with the evidence that proves it. The honest bottom line: the media is reserved and one record class is framed, but there is no device behind the port, no manager for the other eleven item groups, and the shipping firmware profile cannot write flash at all.
- **[2. What the two ends actually look like](#2-what-the-two-ends-actually-look-like)** -- The port offers a per-record region with `ERASE_REGION` and an eight-bit record id; the media offers 64 KiB erase blocks, two of them. Three ways they fail to compose, including the one round 1 missed: the record id is a capacity, not just an address width.
- **[3. The decision](#3-the-decision)** -- One image, promoted A/B, media owned by firmware through the LiteSPI master that already exists. Three measured reasons rather than a preference, with reason 1 re-measured after the namespace correction.
- **[4. The record allocation contract](#4-the-record-allocation-contract)** -- The BLOCKER the review found and the fix. 292 records at 8x8 against 256 ids, the banked allocation that brings it to 87, exactly what banking costs and what it saves, and the gate that fails on the old allocation and passes on this one.
- **[5. Where it lives in the 16 MB QSPI](#5-where-it-lives-in-the-16-mb-qspi)** -- The two reserved slots and why `journal` is raw rather than a filesystem, plus the rule a reflash must obey. Cited by `milan_soc.py` as the map's single source of truth, and 5.1 re-derives every citation of this page at this head, including the two that round 1 miscounted.
- **[6. The record image format: KLJ2](#6-the-record-image-format-klj2)** -- A new versioned container, not KLJ1 carried forward: byte-level field widths, the endianness seam between the little-endian container and the big-endian records, the exact CRC coverage, the identity and shape binding, and an eleven-row acceptance order with a verdict code per failure.
- **[7. Durability: the A/B contract](#7-durability-the-ab-contract)** -- The write and read rules in full, and the property they buy: at every instant of a commit at least one slot holds a complete image whose CRC closes.
- **[8. Where the image lives in fabric, and what it costs](#8-where-the-image-lives-in-fabric-and-what-it-costs)** -- The second BLOCKER. The backend's memory is settled (the reserved DRAM window, not BRAM) and so is the transfer (ordinary loads and stores, no DMA and no CSR data window), with the measured slack behind both. Then the area answer, split honestly into what is structural and what this lane cannot measure.
- **[9. What the fabric may claim: the durability and liveness contract](#9-what-the-fabric-may-claim-the-durability-and-liveness-contract)** -- Why an answered-once bit cannot report a writer that wedges later, and the replacement: a live `nvm_backed` with a deadline and a revocation list, plus `nvm_dirty` and `nvm_stale` so the five honest states are distinguishable.
- **[10. Kernel and boot-side work](#10-kernel-and-boot-side-work)** -- Five items, and the reason `/proc/mtd` staying empty is permanent rather than a misconfiguration. Cited by `gen_mtd_partitions.py`, whose section 10 reference had nothing to resolve to until now.
- **[11. Bench recipe](#11-bench-recipe)** -- G0, G0b and G1, which run today, and what G1 means on a baremetal profile where no MTD device ever probes. Cited by `gen_mtd_partitions.py` and `milan_soc.py`.
- **[12. The commit marks that already exist](#12-the-commit-marks-that-already-exist)** -- Eight marks across seven programs, derived from the pinned donor rather than from a comment, plus the exemplar that is not one and the deliberate absence at IDENTIFY that is a requirement. Round 1 said three.
- **[13. Risks, stated rather than discovered later](#13-risks-stated-rather-than-discovered-later)** -- The proven writer no longer exists in the tree, persistence depends on firmware liveness, the debounce window is a data-loss window a PR must quantify, four donor defects are open against the port, and five RTL citations of this page stay stale.
- **[14. What this page does NOT decide](#14-what-this-page-does-not-decide)** -- Two things, down from four: the debounce window's value, and where the proposed CSR bits actually land.
- **[15. Sequencing](#15-sequencing)** -- Why this page is deliberately ahead of the submodule pin it will be implemented on, and why nothing in it moves when that pin lands.
- **[16. Acceptance for the implementation](#16-acceptance-for-the-implementation)** -- Sixteen checks in five groups, including the vacuity trap a naive save/restore test falls into, one refused case per container verdict code, and the requirement that deleting any of the eight `NVM_MARK` sites must redden something.

## 1. Status

| Piece | State | Evidence |
|---|---|---|
| The flash map reserves the media | **Landed** | `FLASHBOOT_RESERVED` in `sw/litex/milan_soc.py`: `journal` at `0xEE_0000`, 128 KiB, and `user` at `0xF0_0000`, 1 MiB |
| The processor frames and streams one record class | **Landed** (submodule) | `KL_pp_nvm_port` + `KL_acmp_nvm_shadow`. The shadow is the ONLY manager wired to the port today (`protocol_processor_top.sv` lines 2261 and 2278); it owns BINDING records and nothing else |
| A manager for every other persisted item | **ABSENT** | `KL_pp_nvm_port`'s own header says the manager "lands in P4". Nothing serializes names, formats, offsets, maps, rates, clock source, configuration index or SUID |
| The processor emits commit marks | **Landed, unobserved** | **eight** `NVM_MARK` sites across seven programs, section 12.1; every one terminates at `aecp_eff_nvm_stb_nc_w` / `aecp_eff_nvm_mark_nc_w` in `protocol_processor_top.sv` lines 2777, 2778, 3051 and 3052 |
| A device behind the port | **ABSENT** | `NVM_BACKED_C = 1'b0` in `hdl/milan/KL_pp_shadow.sv`, a localparam and deliberately not a parameter |
| A write path on the shipping profile | **ABSENT** | the baremetal firmware reads flash through the XIP window and has no erase or program path |
| The record set fits the namespace | **DECIDED HERE**, gated | section 4, `scripts/check_nvm_record_space.py` |
| The backing store | **DECIDED HERE**, not built | sections 3 and 8 |

**Which donor commit.** `dev` pins the processor at `a25b5cc9`, which carries
`protocol-processor/tb/nvm_port`. That suite's power-cut arm lands at `44489453`, ten commits later,
and arrives with issue #69's pin bump (PR #227). The mark inventory in section
12.1 is identical at both commits, so nothing on this page waits on that pin.

## 2. What the two ends actually look like

**The port's face** (`KL_pp_nvm_port`, measured from its ports): a
region-addressed byte stream. `{op READ / WRITE / ERASE_REGION, region =
record_id (8 bits), offset (16 bits), len (16 bits)}`, one byte per handshake,
`done` and `err` as one-cycle pulses. One region per record: "a partial update
never rewrites unrelated records". Records carry `{magic 0x1722,
layout_version, record_id, payload_length, crc16 CCITT-FALSE}` and the port
refuses a stream whose `payload_length` exceeds `MAX_PAYLOAD_P` (default 1024)
before any device traffic. A BINDING payload is 20 bytes at
`record_id = REC_ID_BASE_P + sink`, and `REC_ID_BASE_P` is `0x20`.

**The media's face**: a 16 MB N25Q128 whose smallest erase unit is a 64 KiB
block, of which exactly two are reserved for this purpose, as slot A and slot B.

These do not compose directly, in **three** independent ways, and all three are
the design problem:

- `ERASE_REGION` per record has no meaning on NOR flash unless a region is at
  least an erase block. 256 possible record ids at 64 KiB each is the entire
  device.
- The port's durability guarantee is weaker than the media's. The donor's own
  review states it: a torn commit leaves every OTHER record untouched, but the
  record being rewritten is unprotected, and because the erase precedes the
  write, `err` never means "the saved set is unchanged". Closing that needs the
  specified-but-unimplemented crc16 check or A/B promotion; the port has no slot
  notion at all.
- **The namespace is a capacity, not just an address width.** `record_id` is
  eight bits. Section 4 counts what the persisted set actually needs, which is
  the check the first version of this page never ran.

So something between them has to turn a per-record region port into a
whole-image A/B promotion, and it has to name more items than the port can
address one at a time. Section 3 decides where that something lives; section 4
decides how it names records.

## 3. The decision

**The record set is stored as one image, promoted A/B into the reserved raw
`journal` slots, and the media is owned by the firmware through the LiteSPI
master that already exists. The fabric owns the verdict, never the media.**

Three things make that the answer rather than a fabric-side flash master:

1. **The whole set fits in one erase block, measured at both shapes.** With the
   allocation of section 4, `scripts/check_nvm_record_space.py` measures
   **2,544 bytes** at the shipping `endstation_ax7101_1x1_tdm8` shape and
   **18,144 bytes** at `endstation_ax7101_8x8`, which is 27 percent of one
   64 KiB slot. Both fit one block with margin, so whole-image promotion is not
   a compromise forced by geometry; it is comfortably affordable, and it
   upgrades the durability guarantee from the port's per-record one to "at every
   instant at least one slot holds a complete CRC-closing image".
2. **The controller already exists and the fabric does not need pads.**
   `sw/litex/milan_soc.py` instantiates `add_spi_flash(mode="1x",
   clk_freq=12.5e6, with_master=True)`. `with_master=True` is a CSR-driven
   command master: write enable, page program and sector erase are reachable
   today from the CPU. A second master in fabric would duplicate that logic AND
   contend for the same physical device with the boot path. The standing
   instruction to keep usage low and re-use existing resources points the same
   way.
3. **The recipe is silicon-proven, in history.** The deleted page records that a
   userspace writer, `acmp-persist`, drove RDID / WREN / SE-D8 / PP / RDSR over
   those CSRs against this board, with a JEDEC guard and an address clamp. It is
   no longer in the tree -- see the risk in section 13 -- but the sequence is not
   speculative.

Reason 1 is the one that was wrong in round 1, and it was wrong by omission
rather than by arithmetic: bytes were counted, ids were not. Section 4 is the
repair.

## 4. The record allocation contract

### 4.1 What the persisted set actually needs

Milan v1.2 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7,
5.3.9.1, 5.3.10.1, 5.3.11.1 and 5.3.13, plus the three design-affirmative items
the donor's `07_memory_maps.md` section 5.1 adds (configuration index, system
unique id, media clock reference). One record per item group and index, which is
what F07.8 specifies and what the first version of this page adopted:

| Group | per | 1x1 | 8x8 |
|---|---|---|---|
| configuration index | entity | 1 | 1 |
| system unique id | entity | 1 | 1 |
| sampling rate | AUDIO_UNIT | 1 | 1 |
| clock source | CLOCK_DOMAIN | 1 | 1 |
| media clock reference | CLOCK_DOMAIN | 1 | 1 |
| binding, parameters and started state | STREAM_INPUT | 2 | 9 |
| stream format in | STREAM_INPUT | 2 | 9 |
| stream format out | STREAM_OUTPUT | 2 | 9 |
| presentation time offset | STREAM_OUTPUT | 2 | 9 |
| channel map in | STREAM_PORT_INPUT | 1 | 8 |
| channel map out | STREAM_PORT_OUTPUT | 1 | 8 |
| user-settable name | writable name | 31 | **235** |
| **total records** | | **46** | **292** |

Every number is generated, not asserted: the shape comes from
`aem_overlay.json`'s `descriptor_counts`, and the name count is the writable
name count in the AEMI image header, which
[`avdecc/gen_aemi_image.py`](../../avdecc/gen_aemi_image.py) builds from the
descriptors that carry a settable name slot (ENTITY contributes two, entity_name
and group_name).

**292 records do not fit 256 ids.** The highest id a flat allocation reaches at
8x8 is 362. The 1x1 shape fits with 46, which is why the hole survived a sizing
round that only ever looked at the shipping default. The review's floor of 262
(names plus per-stream formats plus bindings) is a subset of this count.

### 4.2 The allocation

Records are allocated in fixed blocks by group, and the names group is
**banked**: one record carries eight name slots of 64 bytes, indexed by the same
ordinal the AEMI name table uses, with the tail of the last bank zero-filled.

| ids | group | block | index | 1x1 | 8x8 |
|---|---|---|---|---|---|
| `0x00` | configuration index | 1 | -- | 1 | 1 |
| `0x01` | system unique id | 1 | -- | 1 | 1 |
| `0x02` .. `0x09` | sampling rate | 8 | AUDIO_UNIT | 1 | 1 |
| `0x0A` .. `0x11` | clock source | 8 | CLOCK_DOMAIN | 1 | 1 |
| `0x12` .. `0x19` | media clock reference | 8 | CLOCK_DOMAIN | 1 | 1 |
| `0x1A` .. `0x1F` | reserved | 6 | -- | -- | -- |
| `0x20` .. `0x2F` | binding | 16 | sink | 2 | 9 |
| `0x30` .. `0x3F` | stream format in | 16 | STREAM_INPUT | 2 | 9 |
| `0x40` .. `0x4F` | stream format out | 16 | STREAM_OUTPUT | 2 | 9 |
| `0x50` .. `0x5F` | presentation time offset | 16 | STREAM_OUTPUT | 2 | 9 |
| `0x60` .. `0x6F` | channel map in | 16 | STREAM_PORT_INPUT | 1 | 8 |
| `0x70` .. `0x7F` | channel map out | 16 | STREAM_PORT_OUTPUT | 1 | 8 |
| `0x80` .. `0xFF` | name bank | 128 | ordinal / 8 | 4 | **30** |
| **records** | | | | **19** | **87** |
| **highest id** | | | | `0x83` | `0x9D` |

The binding block base is not chosen here. It is `REC_ID_BASE_P` in
`KL_acmp_nvm_shadow`, already fixed in landed gateware, and the gate READS it
out of the donor RTL rather than restating it, so a donor that moves the
parameter reddens the parent rather than silently aliasing. The file it reads is
located through [`scripts/pp_srcs.py`](../../scripts/pp_srcs.py)'s derived
source list rather than by a hardcoded path, so a donor that renames or moves
the module is followed rather than missed.

The blocks are what makes this contract shape-independent. A record is placed at
`base + index`, and a shape whose index leaves the block is a finding at the
block boundary rather than a collision discovered later. The name banks give
128 banks of 8, which is 1,024 name slots against the 235 the largest shipped
shape uses.

### 4.3 What the fix costs

| | flat, one record per item | banked |
|---|---|---|
| records at 8x8 | 292 | 87 |
| highest id at 8x8 | 362, over the namespace | `0x9D` |
| image bytes at 8x8 | 19,464 | **18,144** |
| image bytes at 1x1 | 2,696 | **2,544** |

**Banking is cheaper in bytes as well as in ids**, by 1,320 bytes at 8x8: 30
eight-byte record headers replace 235 of them, which more than pays for the 320
bytes of zero-fill in the last bank.

The cost is granularity, and it is already paid:

- **The media cost is zero.** Whole-image A/B promotion erases and reprograms
  the entire 64 KiB slot on every commit regardless of which record changed, so
  a name bank and a name record cost the same number of erase cycles.
- **The port cost is one stream of 520 bytes instead of 72**, at one byte per
  handshake, once per debounced commit. The flash erase that follows it is the
  cost of a commit; the byte pump is not.
- **The dirty-tracking granularity is a bank**, so two names changed in the same
  bank coalesce into one bank rewrite. Under the debounce of section 13 that is
  the behaviour wanted, not a penalty.
- **The donor's F07.8 text owes an amendment.** "One record per item group and
  index" stops being true for the names group. **No landed RTL changes**: the
  only manager wired to the port is `KL_acmp_nvm_shadow`, which owns the
  BINDING block and is untouched, and the manager that would emit name records
  does not exist yet. The amendment is a donor documentation change, and it is
  named here as an obligation rather than assumed away.

### 4.4 The gate

[`scripts/check_nvm_record_space.py`](../../scripts/check_nvm_record_space.py)
builds every `configs/endstation_*.yaml`, generates the full persisted inventory
for each, and asserts five things: every record id is unique, every id is inside
`record_id[7:0]`, every group stays inside its block, every payload fits
`MAX_PAYLOAD_P`, and the whole image fits one erase block. `--flat` restores the
pre-review allocation and is a negative control that must exit 1 at 8x8;
`--mutate` perturbs one fixed point at a time so each assertion is shown to
fire; `--self-test` runs all five controls and fails if any of them passes.

## 5. Where it lives in the 16 MB QSPI

The map is generated from `FLASHBOOT_LAYOUT` and `FLASHBOOT_RESERVED` in
[`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) -- **the single source of
truth; slots are added there, never by hand** -- and
[`sw/dts/gen_mtd_partitions.py`](../../sw/dts/gen_mtd_partitions.py) derives the
kernel's `fixed-partitions` node from the same reader.

| Offset | Size | Slot | Written by |
|---|---|---|---|
| `0xEE_0000` | 128 KiB | **`journal`** -- 2 x 64 KiB erase blocks, slot A and slot B, raw | the persistence writer only |
| `0xF0_0000` | 1 MiB | `user` -- jffs2, mounted at `/user` | Linux profiles only |

`journal` is raw and filesystem-free on purpose. Each slot is exactly one erase
block, so "a torn write cannot damage the other slot" is a property of the flash
geometry rather than a promise from a filesystem, and the slot is readable
before any mount -- which is where a fast connect wants to happen. A reflash
must not erase either slot: a gateware update that silently wipes saved bindings
is worse than having none, because the entity then comes back unbound
*sometimes*.

**Board applicability.** The AX7101 has the reservation. A board without it gets
no journal, and the degradation is part of the design: no journal, no replay,
the entity boots unbound and waits for a controller -- exactly what it does
today.

### 5.1 The citations this page exists to keep meaningful

Re-derived at this head with
`grep -rn SAVED_STATE_FASTCONNECT --include=*.py --include=*.sv .`:

| file | line | cites | resolves |
|---|---|---|---|
| `sw/litex/milan_soc.py` | 137 | section 11 gate G0 | yes, section 11 |
| `sw/litex/milan_soc.py` | 159 | section 5, the flash map's one source of truth | yes, this section |
| `sw/dts/gen_mtd_partitions.py` | 24 | section 10 kernel-side work, section 11 gate G1 | yes, sections 10 and 11 |
| `sw/dts/gen_mtd_partitions.py` | 122 | section 11 gate G1 | yes, section 11 |
| `hdl/common/csr/milan_csr.sv` | 447, 689, 701, 712, 851 | the deleted page's E1 to E4 register groups | **no** |

**Two corrections to round 1.** It said three Python files cite the page; there
are **two** (`sw/builder/test_builder.py` does not cite it at all, and the round-1
evidence comment claiming it does was wrong). And it repaired sections 5 and 11
while `gen_mtd_partitions.py` also asks for **section 10**, which is why section
10 below is the kernel and boot-side work rather than something else.

The five `milan_csr.sv` citations point at the legacy plane's `0x7A0` / `0x7B8`
/ `0x7C8` register groups. This page does not restore those groups, because they
do not exist any more. Those citations stay stale, and they are named here
rather than counted as repaired.

## 6. The record image format: KLJ2

The deleted page's `KLJ1` v1 is **not** carried forward, and the round-1 claim
that it was is withdrawn. It cannot be carried forward: its records were six
fixed little-endian words that were literally the six register writes of a plane
that no longer exists, its `SHAPE` word carried `n_rec` in eight bits (the same
limit as section 4, in the container this time), and it had no notion of a
variable-length record. What IS carried forward is everything that was
independent of the plane: the slot geometry, the A/B rule, the wrap-safe
sequence compare, the digest algorithm and the verdict taxonomy.

### 6.1 The container

A slot image is a **little-endian** 32-bit word header, a byte-oriented record
area, and a little-endian 32-bit trailer. The header and trailer are
little-endian because the firmware that writes them is the only thing that
parses them. The records inside are **big-endian**, because a record is the
processor's F07.8 frame verbatim and 1722.1 is network order throughout. That
seam is deliberate, and it is stated here so an encoder does not have to guess.

Header, 10 words, 40 bytes:

| w | Name | Content |
|---|---|---|
| 0 | `MAGIC` | `0x324A4C4B`, which hexdumps as the ASCII `KLJ2` |
| 1 | `FMT_VER` | `{major[31:16], minor[15:0]}`; this version is `0x0002_0000` |
| 2 | `SEQ` | free-running u32 generation counter |
| 3 | `N_REC` | record count in `[15:0]`, `[31:16]` reserved zero |
| 4 | `IMG_LEN` | total bytes, word 0 through the trailer inclusive |
| 5 | `ENT_LO` | owning `entity_id[31:0]` |
| 6 | `ENT_HI` | owning `entity_id[63:32]` |
| 7 | `MODEL_LO` | owning `entity_model_id[31:0]` |
| 8 | `MODEL_HI` | owning `entity_model_id[63:32]` |
| 9 | `REC_LAYOUT` | the F07.8 `layout_version` every record in this image carries, in `[7:0]`; `[31:8]` reserved zero |

`entity_model_id` is the shape binding. It is hash-derived from the descriptor
shape, so any change of configuration moves it, and an image from a different
shape is refused by identity rather than being partially parsed.

Record area: `N_REC` F07.8 frames concatenated, each
`{magic 0x1722, layout_version, record_id, payload_length, crc16}` big-endian
followed by `payload_length` payload bytes, with no padding between records. A
record is self-delimiting from its own `payload_length`; nothing else indexes
it. The area is zero-padded to a 4-byte boundary; the pad is counted in
`IMG_LEN` and covered by the digest.

Trailer, 1 word: `CRC-32/ISO-HDLC` (reflected polynomial `0xEDB88320`, init
`0xFFFFFFFF`, final XOR `0xFFFFFFFF`) over **every preceding byte of the
image**, that is bit-for-bit `zlib.crc32(blob[:-4])`. It is the same algorithm
KLJ1 v1 used, so a writer that already had one keeps it. Placing it **last** is
what makes the replay atomic: the reader physically cannot have acted on
anything before it has seen and checked the digest.

### 6.2 Acceptance order, and the rejection behind "if the fabric rejects it"

A reader applies **zero** records until every one of these passes, in this
order. Each failure has a verdict code, and the fabric publishes the verdict and
the accepted `SEQ`:

| # | Test | Verdict on failure |
|---|---|---|
| 1 | `MAGIC` is `KLJ2` | `VD_MAGIC` |
| 2 | `FMT_VER` major is 2 | `VD_VER`, never reinterpreted |
| 3 | `IMG_LEN` is at least 44 and at most 65,536 | `VD_LEN` |
| 4 | the slot actually holds `IMG_LEN` bytes | `VD_LEN` |
| 5 | CRC-32 over bytes 0 to `IMG_LEN` minus 4 matches the trailer | `VD_CRC` |
| 6 | `ENT_LO` and `ENT_HI` equal this entity's `entity_id` | `VD_ENT` |
| 7 | `MODEL_LO` and `MODEL_HI` equal this build's `entity_model_id` | `VD_SHAPE` |
| 8 | every record: magic `0x1722`, `layout_version` equal to `REC_LAYOUT` and to the port's `LAYOUT_VER_P`, `record_id` inside a block allocated for this shape, `payload_length` the length section 4 fixes for that group, crc16 closes | `VD_REC` |
| 9 | no `record_id` appears twice | `VD_REC` |
| 10 | the record area ends exactly at the trailer | `VD_LEN` |
| 11 | `SEQ` advances past the already-accepted one | `VD_STALE`, ignored |

A blank slot, all `0xFF`, fails test 1 and is reported as `VD_BLANK` rather than
an error: Milan permits an entity that has never been bound.

An allocated id that is simply **absent** from the image is not a failure. That
item was never saved and keeps its vendor default. This is what lets the image
shrink and grow with the shape without a migration.

**Migration.** There is none from KLJ1: major 1 is refused with `VD_VER` and
never reinterpreted, and a board carrying one boots unbound, which is the same
degradation as a blank slot. Within major 2 a reader accepts any minor: a minor
may only add records with new ids, which rule 8 already refuses if the reader
does not know them, and rule 10's exact-fit test keeps an unknown trailing
record from being read as payload.

### 6.3 Encoder and decoder goldens

The implementation owes a pinned golden image per shape, with its CRC, produced
by the firmware encoder and reproduced byte for byte by the fabric decoder, plus
one refused case per verdict code in the table above. That is the only way two
independent implementations, the firmware writer and the fabric reader, can be
shown to agree; the deleted page's 52-byte worked example is the shape of the
artifact wanted.

## 7. Durability: the A/B contract

```
write:  new_seq = accepted_seq + 1
        target  = the slot that is NOT currently authoritative
        erase(target) ; program(target, image(new_seq)) ; read back ; verify crc
        the authoritative slot is never erased

read:   read both slots; newer = (int32_t)(A.seq - B.seq) > 0
        offer the newer; if it fails section 6.2, offer the other
        if both fail, do nothing -- boot unbound
```

At every instant of the write sequence at least one slot holds a complete image
whose CRC closes. Power can be removed at any point. This is the guarantee the
port alone cannot give, and it is why the promotion lives above the port rather
than inside it. A rollback to the older slot after a torn newest one is
**intentional**: that slot was also controller-authorised, so restoring it is
within Milan 5.5.1.2, and the accepted `SEQ` is published so it is visible.

## 8. Where the image lives in fabric, and what it costs

### 8.1 The memory: the reserved DRAM window, not BRAM

**Decided.** The fabric-side record image lives in the processor's existing
reserved main-memory window, not in block RAM.

- The standing instruction is that memory-shaped control state goes to DDR3
  because BRAM is the binding constraint, and the processor is already built
  that way: the donor's `07_memory_maps.md` section 3.3.1 puts the descriptor
  image in main memory rather than on chip for exactly this reason.
- The window exists and is reserved.
  [`sw/builder/endstation_builder.py`](../../sw/builder/endstation_builder.py)
  derives `pp_mem_phys = pcm_ring_phys - PP_MEM_BYTES` and emits a `no-map`
  `ppmem` reservation of `PP_MEM_BYTES` = 1,048,576 bytes at `0x7F700000`;
  `sw/litex/milan_soc.py` reads it and only checks it. It holds the descriptor
  image, measured at 40,000 bytes at 8x8, plus the 4,096-byte response buffer.
  Adding the measured 18,144-byte record image brings the window to 62,240 of
  1,048,576 bytes, under 6 percent. **No new reservation and no device-tree
  change.**
- The BRAM alternative is what is being declined, and its cost is the number
  that decides it: 18,144 bytes byte-wide is 5 BRAM36 at the 8x8 shape, on a
  device whose area campaign is fought in single-digit percentages.

### 8.2 The transfer: ordinary loads and stores, no DMA, no CSR data window

**Decided.** Because the image is in DRAM, the firmware reaches it the way it
reaches anything else in DRAM. Nothing streams it through a CSR window and
nothing needs a DMA engine, because the data never has to move: the fabric
writes it where the CPU can already read it.

What crosses the CSR boundary is a control tuple only: the image base and
length, the sequence number, the dirty and verdict state of section 9, and the
firmware's acknowledgement. That is the smallest contract that can carry the
decision, and it is why "DMA versus a CSR window" stopped being a question
rather than being answered as one.

### 8.3 The area, honestly

Issue #70 work item 1 asks for the flash path's area to be measured before
committing. Here is exactly what this lane can and cannot answer.

**Settled, and structural rather than estimated:**

- **Zero new flash controller and zero new pads.** The LiteSPI master is already
  instantiated with `with_master=True` in `sw/litex/milan_soc.py`; the decision
  adds no second master and no second consumer of the device.
- **Zero new BRAM.** The image is DRAM-resident by section 8.1, and the DRAM it
  needs is inside an existing reservation with the slack measured above.
- **Zero new DRAM reservation and no DTB change**, from the same measurement.

**Not measured, and not measurable from this lane:** the LUT and FF cost of the
backend itself, which is the region-to-offset decoder that replaces
`KL_pp_shadow`'s blank-flash responder, its main-memory access path, and the
control CSRs. There is no RTL for it, and this lane is a decision record with
none. A number here would be an estimate wearing a measurement's clothes, and
the first version of this page already made that mistake once by quoting issue
#69's `+4,396 LUT` datapath delta, which is a different change on a different
plane and says nothing about this one. That figure is removed rather than
reinterpreted.

**What the implementation PR owes**, with a recipe that runs today:

```sh
# before: the shipping build at the shape under test
scripts/area_baseline.py --build <before>
# after: the same shape with the backend
scripts/area_baseline.py --build <after> --compare <before>
```

Post-place, at both `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`,
per that script's own recorded traps that post-synth numbers move by thousands
of LUT and that out-of-context numbers do not preserve rank order.

**This narrows work item 1's acceptance, and the narrowing is public.** The
memory and transfer choices it asked to settle are settled here, with measured
inputs; the backend's own LUT delta moves to the implementation PR with a named
recipe. Issue #70 records the change.

## 9. What the fabric may claim: the durability and liveness contract

`nvm_backed_o` stops being a constant `0`. The round-1 version of this page made
it assert "once a writer has answered at least once since reset", and the review
is right that this cannot report a writer that answers once and then wedges: the
volatile image would keep accepting changes while `PP_STAT` still advertised
durable backing, which recreates the false-success condition issue #70 exists to
remove. It is the same lie in slower motion.

### 9.1 The bits

[`docs/reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) today defines
`PP_STAT[6] nvm_backed`, `[7] nvm_blank`, `[4] nvm_alarm` and
`[3] restore_fail`. The contract needs two more bits and a field, and `[23:8]`
is free:

| bit | name | meaning |
|---|---|---|
| `[6]` | `nvm_backed` | **live**: a writer answered within `T-NVM-WRITER-ALIVE` and no unrevoked failure is outstanding |
| `[8]` | `nvm_dirty` | the fabric image holds committed changes that no slot yet holds |
| `[9]` | `nvm_stale` | `nvm_backed` was true since reset and is now false |
| `[15:12]` | `nvm_verdict` | the section 6.2 verdict code of the last image offered |

`nvm_backed` remains **fabric-derived evidence and never a knob**: no CSR write
can set it, which is the property that made it a localparam rather than a
parameter in the first place, and it survives being made dynamic.

### 9.2 When it sets, and when it is revoked

**Sets** on the first firmware answer after reset that completes a whole
transaction: a commit whose read-back verified, a boot restore whose slot passed
section 6.2, or an explicit liveness poll answered. The reset value is 0.

**Re-arms** the deadline on every completed transaction.

**Clears** on any of: the deadline expiring; a commit not acknowledged within
`T-NVM-COMMIT-TIMEOUT`; a reported erase, program or read-back-verify failure; a
reported JEDEC identity mismatch; the port's `nvm_alarm` raised by
bounded-retry exhaustion. Every one of these raises `nvm_stale` at the same
time.

### 9.3 Reading the three bits together

| `nvm_backed` | `nvm_dirty` | `nvm_stale` | Meaning |
|---|---|---|---|
| `1` | `0` | `0` | **Durable.** Everything committed is in a slot |
| `1` | `1` | `0` | **In flight.** A commit is inside the debounce window or in progress; a power cut here loses the marked changes and nothing else |
| `0` | any | `0` | **Never backed.** No writer has answered since reset; nothing is backed and nothing claims to be |
| `0` | `1` | `1` | **Writer lost with data outstanding.** The image accepted changes that are NOT durable. This is the wedged-writer case, and it reads as not backed |
| `0` | `0` | `1` | **Writer lost, nothing outstanding.** Still not backed |

The split between `dirty` and `backed` is the part that matters. When the writer
wedges, the entity must keep answering AECP and keep accepting SETs: refusing a
controller because flash is unreachable would be a worse defect than not saving.
What it must not do is claim durability. `nvm_dirty` is what makes the debounce
window visible instead of implicit, and it is what a power-cut test reads to
know whether the loss it observed was permitted.

## 10. Kernel and boot-side work

Cited by [`sw/dts/gen_mtd_partitions.py`](../../sw/dts/gen_mtd_partitions.py) as
where the kernel-side story lives.

1. **The partition node is generated, not hand-written.**
   `gen_mtd_partitions.py` derives `journal@ee0000` and `user@f00000` from the
   same `FLASHBOOT_RESERVED` reader `milan_soc.py` uses, so there is no second
   copy to drift.
2. **No mtd driver binds.** No upstream Linux driver claims `litex,spiflash`, so
   the partitions are declared and never parsed, `/proc/mtd` stays empty, and
   this is a permanent property of the kernel rather than a configuration
   mistake. It is recorded in that script and repeated here because it is the
   reason G1 in section 11 is a falsifier rather than a pass criterion.
3. **The write path is the LiteSPI CSR master either way**, on Linux and on
   baremetal. Nothing in this design needs mtd.
4. **On the shipping `--flashboot baremetal` profile** there is no kernel at
   all. The equivalent obligation is that the firmware resolves the slot offsets
   from the generated map rather than from literals, which is what keeps
   `milan_soc.py` the single source of truth for the firmware as well.
5. **A reflash must not erase either reserved slot.** A gateware update that
   silently wipes saved bindings is worse than having none.

## 11. Bench recipe

**G0 -- build with the layout (host only, no board).** `sw/builder/test_builder.py`
checks the map's internal consistency, including that the rootfs still fits under
the reserved slots. It passes today.

**G0b -- the record set fits the namespace (host only, no board).**
`scripts/check_nvm_record_space.py`, and `--self-test` for its negative
controls. Both pass today.

**G1 -- the partition appears.** On a Linux profile, `journal@ee0000` and
`user@f00000` are in the DTS and the built DTB.
[`sw/dts/gen_mtd_partitions.py`](../../sw/dts/gen_mtd_partitions.py) derives them
from the same map. Note the standing limitation in section 10 item 2: no
upstream Linux driver claims `litex,spiflash`, so no device ever probes and the
partitions are declared but never parsed. **On the shipping baremetal profile G1
does not apply**; section 10 item 4 is the equivalent.

**G2 to G5** -- restore from a host-written image, fast connect with no
controller, the write path, and the reboot drill -- are the implementation
ticket's and need a board. The bench is down at the time of writing.

## 12. The commit marks that already exist

### 12.1 The inventory, derived from the donor

Eight `NVM_MARK` sites across seven programs in
`protocol-processor/hdl/aecp/ucode/gen_ucode.py`, identical at the pinned
`a25b5cc9` and at `44489453`. The line numbers below are at `44489453`, the
commit this page cites:

| Program | line | mark class | persists |
|---|---|---|---|
| `SET_SAMPLING_RATE` | 1284 | 1 | sampling rate, 5.3.5.1 |
| `SET_CLOCK_SOURCE` | 1322 | 1 | clock source, 5.3.11.1 |
| `SET_CONFIGURATION` | 1557 | 1 | configuration index |
| `ADD` / `REMOVE_AUDIO_MAPPINGS` | 1673 | 6 | channel maps, 5.3.9.1 and 5.3.10.1 |
| `SET_STREAM_INPUT_FORMAT` | 1807 via `_sfmt(SEL_FMTIN)` | 1 | stream format in, 5.3.8.1 |
| `SET_STREAM_OUTPUT_FORMAT` | 1807 via `_sfmt(SEL_FMTOUT)` | 1 | stream format out, 5.3.7.1 |
| `SET_STREAM_INFO` | 1884 | 1 | presentation time offset, 5.3.7.6 |
| `SET_NAME` | 1973 | 7 | user names, 5.3.13 |

The two stream-format entries are one source program placed twice
(`place(E_SFMTI, _sfmt(SEL_FMTIN))` and `place(E_SFMTO, _sfmt(SEL_FMTOUT))`), so
deleting the mark deletes both. A test that grades only one of them cannot tell
the difference, which is why the acceptance in section 16 names them separately.

Two more sites exist and are deliberately not in that table: a
`SET_SAMPLING_RATE` **exemplar** at line 438 with mark class `0x21`, which is
documentation for the donor's `06_aecp_engine.md` section 8 and not an
operational program, and the **absence** at line 1464, where `SET_CONTROL`
carries a comment saying no mark is emitted because 5.3.12 keeps IDENTIFY
volatile. That absence is a requirement, and section 16 grades it.

The round-1 version of this page said there were three marks. There are eight,
and the five it omitted (maps, both stream formats, presentation offset, names)
are exactly the items with the most records in section 4.

### 12.2 Where they go today

Nowhere. `KL_aecp_ucpu` drives `eff_nvm_stb_o` and `eff_nvm_mark_o[7:0]`, and
`protocol_processor_top.sv` binds both to `_nc_w` wires at lines 2777, 2778,
3051 and 3052. The mark carries a class, not a record id; mapping a class plus
the program's descriptor index onto section 4's allocation is the missing
manager's job.

## 13. Risks, stated rather than discovered later

- **The proven writer is gone.** `acmp-persist` was a Linux userspace program in
  a rootfs overlay; the shipping profile is `--flashboot baremetal` and the
  baremetal firmware is one C file that only reads. The write path must be
  written again, in `sw/firmware/milan_baremetal/`, against the same CSRs. The
  historical program is recoverable from git if its exact command sequence is
  wanted.
- **Persistence depends on firmware liveness.** A fabric-owned master would not.
  This is the price of re-using the controller, and section 9 is what keeps that
  price honest rather than hidden.
- **The debounce window is a data-loss window.** The processor already debounces
  commits (`T-NVM-DEBOUNCE`, coalescing) and the mapping compliance sequence
  issues a dozen SETs in a row, so a commit per command would burn erase cycles
  for nothing. Whatever window is chosen, the PR that lands it must say what a
  power cut inside it loses, and `nvm_dirty` is the bit that makes it visible.
- **Four donor defects are open against the port** and matter to any consumer:
  an unowned `done_seen_r`, no timeout so a silent device wedges the port,
  restore failures collapsing three situations into one signal, and `record_id`
  never checked against its region. The last one is now load-bearing: section
  4's blocks are enforced by the manager and by
  `scripts/check_nvm_record_space.py`, not by the port.
- **The donor's F07.8 text and this page disagree** until the amendment of
  section 4.3 lands. The gate is the tie-breaker in the meantime.
- **Five `milan_csr.sv` citations of this page stay stale**, section 5.1. They
  name register groups the substituted plane deleted.

## 14. What this page does NOT decide

Two things, down from four.

- **The debounce window's value.** It is a wear-versus-loss trade that needs a
  bench, and section 13 says what the PR that picks it owes.
- **The exact CSR addresses** of the control tuple in section 8.2, and the bit
  positions proposed in section 9.1. The shapes are decided; where they land in
  `milan_csr` is the implementation's, and
  [`docs/reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) owes the
  rows -- including a correction, because it currently describes `nvm_backed` as
  a **constant**, which section 9 makes wrong.

## 15. Sequencing

The parent-side work starts when issue #69's submodule pin is on `dev`: that pin
is the one carrying the donor's nvm_port power-cut coverage, and there is no
donor commit with one without the other. This page is deliberately ahead of it,
because the decision it records is what the implementation needs first and it
depends on none of that. Section 12.1's inventory is identical at both commits,
so nothing here moves when the pin does.

## 16. Acceptance for the implementation

**The record namespace**

- [ ] `scripts/check_nvm_record_space.py` passes for every shipped config, and
      its `--self-test` still reddens on all five negative controls.
- [ ] The manager emits records at the section 4.2 ids, and a record whose id is
      outside its group's block is refused rather than written.

**The container**

- [ ] A pinned golden image per shape, byte for byte, with its CRC, produced by
      the firmware encoder and reproduced by the fabric decoder.
- [ ] One refused case per verdict code in section 6.2, each proving **zero**
      records were applied: foreign entity, foreign model, bad magic, wrong
      major, truncated, overrun, bad digest, unknown record id, duplicate record
      id, mixed layout_version, torn slot, stale sequence.

**The status bits**

- [ ] `nvm_backed` reports the truth on a build with and without a writer,
      proven both ways.
- [ ] A writer that answers once and then stops drives `nvm_backed` to 0 and
      `nvm_stale` to 1 within `T-NVM-WRITER-ALIVE`, with `nvm_dirty` reporting
      whether anything was outstanding.
- [ ] A failed erase, a failed program and a failed read-back-verify each revoke
      `nvm_backed` independently.
- [ ] A power cut inside the debounce window loses exactly the marked changes,
      and `nvm_dirty` said so beforehand.
- [ ] A restore walk over blank flash reports "nothing restored", never success.

**The saved set**

- [ ] All eight Milan items plus the bound state, the binding parameters and
      started/stopped survive a reset that is proven to have cleared the rows
      first (the vacuity trap: a restore that writes nothing and a store that was
      never reset both pass a naive read-back).
- [ ] The volatile set does NOT survive: after restore the lock is clear, the
      controller registry is empty, IDENTIFY is 0.
- [ ] A commit interrupted at every stage leaves a complete image in one slot.

**The marks**

- [ ] Each of the **eight** marks in section 12.1 is graded end to end: deleting
      it alone must redden a save/restore test. Both stream-format placements
      count separately, and the mapping, presentation-offset and name marks are
      included.
- [ ] Deleting the mark's **absence** at `SET_CONTROL`, that is adding one, must
      also redden something: 5.3.12 requires IDENTIFY to stay volatile.
