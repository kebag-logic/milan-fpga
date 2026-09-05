# Saved state and fast connect — the backing store decision

> **Corrected three times, and every correction changed the design.**
> Round 1 sized the saved record set in BYTES, found it fitted one erase block,
> and stopped. It never checked the OTHER capacity in the same design: the
> processor addresses a record by `record_id[7:0]`, so the namespace holds 256
> records, and one record per persisted item needs **292** at the 8x8 shape.
> Round 2 fixed the arithmetic and then over-claimed on the result: it settled
> the record allocation on the parent's own gate although the pinned donor's
> F07.8 says otherwise, declared the backend's area unmeasurable, left the two
> liveness deadlines unvalued, and deliberately left five RTL citations stale.
>
> What changed, and what did not:
>
> | | round 1 | round 2 | now |
> |---|---|---|---|
> | whole-image A/B promotion into the reserved `journal` slots | decided | unchanged | **unchanged** |
> | media owned by firmware through the existing LiteSPI master | decided | unchanged | **unchanged** |
> | record namespace inside the image | one record per item group and index | banked, decided | **one record per item group and index, DECIDED (2026-09-05)**: the banked proposal is withdrawn, section 4.3 |
> | the on-flash container | KLJ1 v1 "carried forward unchanged" | a new version, KLJ2 | unchanged, section 6 |
> | the backend's memory and the transfer mechanism | left open | decided | unchanged, section 8 |
> | `nvm_backed_o` | asserts once a writer has answered | live, with a revocation list | **plus recovery semantics, an exhaustive state table and two derived deadline values**, section 9 |
> | the area claim | borrowed issue #69's unrelated LUT delta | withdrawn as unmeasurable | **measured**: a synthesizable before/after pair, section 8.3 |
> | the record-space gate | did not exist | five negative controls, no omission oracle | **fifteen controls**, and the gate now encodes and decodes the image instead of counting it, section 4.4 |
> | the five `milan_csr.sv` citations | dangling | named as deliberately stale | **repaired**, section 5.1 |
>
> **Round 3 changed four more things, and one of them is about this page's own
> method.** Three rounds running, a finding landed in the same class: a check
> that reasoned about the persisted set as COUNTS or TABLES and therefore could
> not see WHICH items it counted. Round 1 counted bytes and not ids. Round 2
> counted records and not presence. Round 3's oracle counted groups and not
> indices, and an off-by-one that deleted STREAM_INPUT 0 and invented a
> nonexistent index 9 passed it in silence. That is a statement about the shape
> of the instrument, not its spelling, so the shape changed: the gate now BUILDS
> the KLJ2 image and READS IT BACK, and the sizing candidate is DRIVEN against
> that image rather than only synthesised.
>
> | | round 3 | now |
> |---|---|---|
> | the empty-name case | an all-zero slot meant "no name stored", so a legal empty name could not be encoded at all | presence follows from the SHAPE; a record is the value, and 64 zero bytes is the empty name, section 4.3 |
> | the completeness oracle | `Counter(group)`, cardinalities only | the exact `(group, index)` key set, with the missing and the extra keys named, section 4.4 |
> | an incomplete but CRC-clean image | accepted; the absent item reverted to its vendor default | refused with `VD_INCOMPLETE` and zero records applied, section 6.2 |
> | the two channel-map groups in the sizing candidate | one `{prefix,length}` table for both directions, and a nominal stride after each group | direction-distinct state and group bases derived from the actual preceding lengths, section 8.3 |
> | the recovery machine | a latch cleared only by reset, with the published bit masked | the latch itself is cleared by the recovery condition, section 9.2 |
> | the area measurement | 539 LUT, with 128 LUT6 of distributed RAM in no column at all | **781 LUT-equivalents** at 8x8 worst case, with a LUTRAM column added to `ooc.sh`, section 8.3 |
>
> A decision record whose arithmetic was corrected is a better artifact than one
> that quietly does not add up. The corrections are recorded here rather than
> silently applied, and on issue #70.
>
> **The fabric half landed (2026-09-05).** `hdl/milan/KL_nvm_backend.sv` is the
> device behind the processor's NVM port in `KL_pp_shadow`, with the third
> main-memory master in the SoC, the control face at `0x934`-`0x93C` and the
> section 9 bits in `PP_STAT`. Its area is measured on the shipping module in
> section 8.3, and it is above the candidate's bound: 992 LUT-equivalents and
> 377 FF worst case against 781 and 280. The firmware writer that configures,
> validates and commits the image does not exist yet, so nothing persists yet
> and the status still says so.

Milan v1.2 names eight things a PAAD-AE shall keep across a power cycle, plus
the bound state, the binding parameters and the started/stopped state. This
device keeps none of them yet. `KL_pp_shadow` answers the processor's NVM port
with `KL_nvm_backend`, the backing store this page decided (sections 4, 8 and
9); until firmware configures and validates a record image through it, the
backend answers exactly what the blank-flash responder it replaced did: reads
return `0xFF`, writes are accepted and discarded, erase completes. A restore
walk therefore still finds blank flash, restores zero records, and -- since the
wrapper started publishing `nvm_backed_o` -- says so rather than reporting
success for it.

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
- **[4. The record allocation contract](#4-the-record-allocation-contract)** -- The BLOCKER round 1 missed: 292 records at the 2026-08 8x8 shape against 256 ids, and the banked allocation proposed to bring it to 87. Then the reversal: #259 shrank that shape to a conformant 164, and nothing had persisted or decoded a bank, so the allocation is the donor's own F07.8 rule, one record per item group and index, DECIDED, and the amendment request is withdrawn. Plus the gate that builds the image and reads it back.
- **[5. Where it lives in the 16 MB QSPI](#5-where-it-lives-in-the-16-mb-qspi)** -- The two reserved slots and why `journal` is raw rather than a filesystem, plus the rule a reflash must obey. Cited by `milan_soc.py` as the map's single source of truth, and 5.1 re-derives every citation of this page at this head: zero unresolved, because the five RTL comments round 2 left stale are repaired against the register map.
- **[6. The record image format: KLJ2](#6-the-record-image-format-klj2)** -- A new versioned container, not KLJ1 carried forward: byte-level field widths, the endianness seam between the little-endian container and the big-endian records, the exact CRC coverage, the identity and shape binding, and a twelve-row acceptance order with a verdict code per failure, including the rule that refuses a CRC-clean image which omits a mandatory record.
- **[7. Durability: the A/B contract](#7-durability-the-ab-contract)** -- The write and read rules in full, and the property they buy: at every instant of a commit at least one slot holds a complete image whose CRC closes.
- **[8. Where the image lives in fabric, and what it costs](#8-where-the-image-lives-in-fabric-and-what-it-costs)** -- The memory is settled (the reserved DRAM window, not BRAM) and so is the transfer (ordinary loads and stores, with no CSR data window), with the measured slack behind both. Then the area, MEASURED: a before/after pair OOC-mapped at both shapes and DRIVEN against a byte-exact image, bounded at 781 LUT-equivalents and 280 FF, and calibrated against three blocks already in the tree.
- **[9. What the fabric may claim: the durability and liveness contract](#9-what-the-fabric-may-claim-the-durability-and-liveness-contract)** -- Why an answered-once bit cannot report a writer that wedges later, and the replacement: a live `nvm_backed` with a revocation list, `nvm_dirty` and `nvm_stale`, the rule that says when the loss is forgiven, all eight bit combinations with the one that cannot occur named (unreachable in the STATE now, not merely masked at the face), and the two deadlines derived from the flash datasheet rather than chosen.
- **[10. Boot-side work](#10-boot-side-work)** -- Five items, and why the block-layer route a previous profile assumed was never available on this controller.
- **[11. Bench recipe](#11-bench-recipe)** -- G0 and G0b, which run today, and why G1 belonged to a superseded target profile. Cited by `milan_soc.py`.
- **[12. The commit marks that already exist](#12-the-commit-marks-that-already-exist)** -- Eight marks across seven programs, derived from the pinned donor rather than from a comment, plus the exemplar that is not one and the deliberate absence at IDENTIFY that is a requirement. Round 1 said three.
- **[13. Risks, stated rather than discovered later](#13-risks-stated-rather-than-discovered-later)** -- The proven writer no longer exists in the tree, persistence depends on firmware liveness, the debounce window is a data-loss window a PR must quantify, four donor defects are open against the port, and the record contract's one external dependency is now the donor pin itself.
- **[14. What this page does NOT decide](#14-what-this-page-does-not-decide)** -- Two things: the debounce window's value, and where the proposed CSR bits actually land.
- **[15. Sequencing](#15-sequencing)** -- Why this page is deliberately ahead of the submodule pin it will be implemented on, and why nothing in it moves when that pin lands.
- **[16. Acceptance for the implementation](#16-acceptance-for-the-implementation)** -- Twenty-seven checks in six groups, including the vacuity trap a naive save/restore test falls into, one refused case per container verdict code, the six liveness and recovery cases the state table makes determinate, and the requirement that deleting any of the eight `NVM_MARK` sites must redden something.

## 1. Status

| Piece | State | Evidence |
|---|---|---|
| The flash map reserves the media | **Landed** | `FLASHBOOT_RESERVED` in `sw/litex/milan_soc.py`: `journal` at `0xEE_0000`, 128 KiB, and `user` at `0xF0_0000`, 1 MiB |
| The processor frames and streams one record class | **Landed** (submodule) | `KL_pp_nvm_port` + `KL_acmp_nvm_shadow`. The shadow is the ONLY manager wired to the port today (`protocol_processor_top.sv` lines 2261 and 2278); it owns BINDING records and nothing else |
| A manager for every other persisted item | **ABSENT** | `KL_pp_nvm_port`'s own header says the manager "lands in P4". Nothing serializes names, formats, offsets, maps, rates, clock source, configuration index or SUID |
| The processor emits commit marks | **Landed, unobserved** | **eight** `NVM_MARK` sites across seven programs, section 12.1; every one terminates at `aecp_eff_nvm_stb_nc_w` / `aecp_eff_nvm_mark_nc_w` in `protocol_processor_top.sv` lines 2777, 2778, 3051 and 3052 |
| A device behind the port | **Landed** (2026-09-05) | `hdl/milan/KL_nvm_backend.sv`, instantiated by `KL_pp_shadow` behind the processor's device face; the third main-memory master in `sw/litex/milan_soc.py`; the control face `PP_NVM_SEL`/`PP_NVM_DATA`/`PP_NVM_STAT` at `0x934`-`0x93C` and the section 9 bits in `PP_STAT`. `nvm_backed` is live fabric evidence now, and still never a knob |
| A write path on the shipping profile | **ABSENT** | the baremetal firmware reads flash through the XIP window and has no erase or program path |
| The record set fits the namespace | **DECIDED HERE** (2026-09-05), gated: the donor's F07.8 rule unchanged, one record per item group and index, 164 of 256 ids at the largest shipped shape | sections 4.2 and 4.3, `scripts/check_nvm_record_space.py` |
| The backing store | **DECIDED HERE, fabric half built** | sections 3 and 8; the firmware half (validate a slot into the window, heartbeat, commit the image into the journal slots, acknowledge) is the remaining work item |
| The backend's area | **MEASURED**, on the shipping module | section 8.3: 992 LUT-equivalents / 377 FF OOC worst case for `KL_nvm_backend`, against 35 LUT / 21 FF for the responder it replaced, by the recipe in 8.3; the post-place delta is still owed by the bitstream build |
| The backend does what it is priced for | **DRIVEN**, the shipping source | `tb/verilator/nvm_backend`: 433 checks at 8x8 and 148 at 1x1 against a byte-exact KLJ2 image, plus four negative controls that must each go RED; `tb/verilator/pp_shadow` grades the integration through the CSR window |
| The liveness and commit deadlines | **DECIDED HERE**, gated | section 9.4, and check 7 of `scripts/check_nvm_record_space.py` |

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
   allocation of section 4, the donor's own F07.8 rule unchanged,
   `scripts/check_nvm_record_space.py` measures **2,696 bytes** at the shipping
   `endstation_ax7101_1x1_tdm8` shape and **9,224 bytes** at
   `endstation_ax7101_8x8`, which is 14 percent of one 64 KiB slot. Both fit
   one block with margin, so whole-image promotion is not
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
3. **The controller is directly usable from bare-metal firmware.** The required
   RDID / WREN / SE-D8 / PP / RDSR sequence is issued through those CSRs, with a
   JEDEC guard and an address clamp. Section 13 keeps the missing firmware writer
   explicit rather than treating controller reachability as completed persistence.

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

### 4.2 The allocation -- DECIDED, the donor's F07.8 rule unchanged

> **Status: decided on 2026-09-05 (#70).** The pinned donor's F07.8 is the
> normative record contract and says "one record per item group and index".
> This allocation obeys it in every group, user names included, so no donor
> change gates it. The banked names layout that sections 4.2 and 4.3 carried as
> a PROPOSAL from 2026-08 is withdrawn; section 4.3 keeps the arithmetic that
> forced it, the correction it went through, and why it stopped being needed.

Records are allocated in fixed blocks by group. A user name is one record per
writable-name ordinal, indexed by the same ordinal the AEMI name table uses,
and its 64-byte payload is the AEM string verbatim: 64 zero bytes is the empty
name, a legal value a controller may set, never an absence. Which ordinals
exist follows from the shape, never from what the bytes happen to be.

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
| `0x80` .. `0xFF` | user name | 128 | name ordinal | 31 | **107** |
| **records** | | | | **46** | **164** |
| **highest id** | | | | `0x9E` | `0xEA` |

The binding block base is not chosen here. It is `REC_ID_BASE_P` in
`KL_acmp_nvm_shadow`, already fixed in landed gateware, and the gate READS it
out of the donor RTL rather than restating it, so a donor that moves the
parameter reddens the parent rather than silently aliasing. The file it reads is
located through [`scripts/pp_srcs.py`](../../scripts/pp_srcs.py)'s derived
source list rather than by a hardcoded path, so a donor that renames or moves
the module is followed rather than missed.

The blocks are what makes this contract shape-independent. A record is placed at
`base + index`, and a shape whose index leaves the block is a finding at the
block boundary rather than a collision discovered later. The name block holds
128 ordinals against the 107 the largest shipped shape has; a shape with more
writable names than that is check 3's finding, and a shape whose whole record
set outgrows the 256-id namespace is check 6's, named as such rather than
absorbed by a layout nobody decided.

### 4.3 Why the donor contract was going to change, and why it no longer does

**In 2026-08 no conformant allocation existed at the 8x8 shape.** This was
arithmetic, not a preference, and the gate computed it rather than asserting it.
F07.8 fixes one record per item group and index, so the record COUNT is a
property of the shape and no allocation can improve on it. A perfectly packed
conformant allocation would place those records at ids `0 .. count-1`, so
`count > 256` refuted every possible conformant allocation, not just one:

```
python3 scripts/check_nvm_record_space.py     # the "F07.8 floor" column, 2026-08
  endstation_arty_4x4          ... F07.8 floor= 88/256
  endstation_arty_8ch          ... F07.8 floor=120/256
  endstation_arty_current      ... F07.8 floor= 42/256
  endstation_ax7101_1x1_tdm8   ... F07.8 floor= 46/256
  endstation_ax7101_8x8        ... F07.8 floor=292/256
```

235 of those 292 were Milan 5.3.13 names, and 5.3.13 has no escape clause:
every descriptor with a user-settable name has its name persisted. At that
shape the record contract had to change or the 8x8 could not be made
compliant, so this page proposed a BANKED names group -- one record carrying
eight 64-byte name slots, 87 records and `0x9D` as the highest id at 8x8 --
and asked the donor to amend F07.8 accordingly, filed as donor issue #24.

**The proposal went through one correction worth keeping.** Its first wording
said an all-zero slot meant "no name stored". A name slot is a fixed 64-byte
NUL-padded AEM string and `SET_NAME` writes all eight 64-bit lanes with no
non-zero requirement
(`protocol-processor/hdl/aecp/ucode/gen_ucode.py` lines 1897-1924), so the
value space is every 64-byte string, and the empty string is the one that is
64 zero bytes. Under that wording a name a controller cleared came back as the
vendor default: the encoding was not injective on the value space, and Milan
5.3.13 grants no exemption for it. The repair was to take content out of the
presence decision entirely -- presence follows from the SHAPE, a slot is the
value and nothing else. That rule survives the reversal below unchanged: a
NAME record's 64 bytes are the value, and the gate's check 9 still encodes the
empty name and reads it back, with the content-based rule kept as the negative
control `--mutate=name_absent_rule`.

**Then the forcing shape went away.** #259 retired the 8x8's nonphysical
clusters, its floor fell from 292 to 164 of 256, and no shipped shape forced
banking any more. On 2026-08-25 the banked layout was nevertheless RETAINED
as a persisted-format decision, on the premise that it was already persisted
in flashed boards' KLJ2 images and decoded by landed donor gateware, which
would have made a flat re-allocation a migration.

**That premise did not hold, and on 2026-09-05 (#70) the decision was
reversed.** Checked at `dev` with the donor pinned at `e743dcdc`: no donor
gateware decodes a name bank (a search of the donor's RTL, documentation and
tests for the bank vocabulary finds nothing, and its F07.8 still reads "one
record per item group and index"); the only manager wired to `KL_pp_nvm_port`
is `KL_acmp_nvm_shadow`, which owns BINDING records; and no producer writes a
KLJ2 image to any board, because the device behind the port and the write
path on the shipping profile are both absent (section 1). The KLJ2 encoder and
decoder exist only in this repository's gate, its sizing candidate and that
candidate's bench. There was nothing to migrate.

PERSISTED-FORMAT DECISION (#70, 2026-09-05): the allocation is the donor's
F07.8 rule unchanged, one record per item group and index, with each user name
one 64-byte record at `0x80 + ordinal` (section 4.2). The amendment request to
the donor is withdrawn and donor issue #24 is to be closed as no longer needed.
Nothing in this repository asks the donor to change its record contract.

**What the reversal costs, at the shapes that ship today**, measured by the
gate at both allocations before the banked code was removed:

| | banked (withdrawn) | flat, F07.8 (decided) |
|---|---|---|
| records at 8x8 | 87 | 164 |
| highest id at 8x8 | `0x9D` | `0xEA` |
| image bytes at 8x8 | 8,800 | **9,224** |
| image bytes at 1x1 | 2,544 | **2,696** |
| worst commit at 8x8 (section 9.4 deadline 8,000 ms) | 3.18 s | 3.19 s |

The flat images are 424 and 152 bytes larger, 14 and 4 percent of one 64 KiB
slot, and every one still fits one erase block with margin. What the
reversal buys is the removal of the only cross-repository dependency the
record contract had, and with it the largest open risk this page carried.

### 4.4 The gate

[`scripts/check_nvm_record_space.py`](../../scripts/check_nvm_record_space.py)
builds every `configs/endstation_*.yaml`, generates the full persisted inventory
for each, **encodes it as a KLJ2 image and decodes it back**, and asserts eleven
things:

0. **the inventory's exact `(group, index)` key set is the set the shape
   requires, with no key claimed twice.** This is graded against a ledger the
   inventory does not read -- one entry per persisted group with its clause and
   a rule over `descriptor_counts` -- plus a second, independent derivation of
   the writable-name count from the descriptor types that carry a settable name
   slot, cross-checked against the AEMI image header. Round 2's gate had no
   oracle at all here; round 3's had one, but it reduced the inventory to
   `Counter(group)` and compared CARDINALITIES, so shifting every `FMT_IN` tuple
   from index k to k+1 -- deleting real STREAM_INPUT 0 and allocating a record
   for a nonexistent index 9 -- left every count identical and the gate silent.
   A set names both the key that went missing and the key that should not
   exist, and a separate duplicate check catches two records claiming one key
   with distinct ids.
1. every record id is unique;
2. every id is inside `record_id[7:0]`;
3. every group stays inside its block;
4. every payload fits `MAX_PAYLOAD_P`;
5. the whole image fits one erase block;
6. **the allocation is the donor's own F07.8 rule and fits** -- the conformant
   floor of every shipped shape is inside the namespace, and a shape whose
   record set the contract cannot hold is a finding that names it, never a
   silent divergence;
7. **the worst-case commit fits `T-NVM-COMMIT-TIMEOUT`** with the 2x margin
   section 9.4 requires, at every shape;
8. **every record round trips** through an encoded and decoded KLJ2 image, byte
   for byte;
9. **an empty user name survives.** The image is re-encoded with name ordinal 0
   set to 64 zero bytes and read back, and the restored value has to be exactly
   64 zero bytes rather than the vendor default -- the case section 4.3's
   round-3 text could not represent;
10. **a CRC-clean image that omits ANY mandatory record is refused** with zero
    records applied. Each mandatory key in turn is deleted, the CRC-32 is
    RECOMPUTED so the image is clean, and the decoder has to answer
    `VD_INCOMPLETE` (section 6.2).

`--mutate` perturbs one fixed point at a time so each assertion is shown to
fire: four omission arms, two index-set arms (a shift that keeps the
cardinality, and a duplicate key with distinct ids), a namespace shrunk below
the conformant floor, and two arms that restore a round-3 DECODER rule -- the
content-based name presence rule and "an absent allocated id is not a
failure". `--self-test` runs all fifteen controls and fails if any of them
passes.

`--emit-record-table` writes the byte offsets of that same image for
`tb/verilator/nvm_backend`, and the gate rebuilds and compares the committed
fixture on every run, so the RTL cannot be graded against stale bytes.

## 5. Where it lives in the 16 MB QSPI

The map is generated from `FLASHBOOT_LAYOUT` and `FLASHBOOT_RESERVED` in
[`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) -- **the single source of
truth; slots are added there, never by hand** -- and
the retired flash-partition emitter derived the same
`fixed-partitions` node from that reader.

| Offset | Size | Slot | Written by |
|---|---|---|---|
| `0xEE_0000` | 128 KiB | **`journal`** -- 2 x 64 KiB erase blocks, slot A and slot B, raw | the persistence writer only |
| `0xF0_0000` | 1 MiB | `user` -- writable region, unclaimed today | no current product owner |

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
`grep -rn SAVED_STATE_FASTCONNECT --include=*.py --include=*.sv --include=*.sh .`:

| file | line | cites | resolves |
|---|---|---|---|
| `sw/litex/milan_soc.py` | 137 | section 11 gate G0 | yes, section 11 |
| `sw/litex/milan_soc.py` | 159 | section 5, the flash map's one source of truth | yes, this section |
| `scripts/check_nvm_record_space.py` | 8 | the page, as the design the gate defends | yes, sections 4 and 9.4 |
| `syn/yosys/ooc.sh` | 81 | section 8.3 | yes, section 8.3 |
| `syn/ooc/sizing/KL_nvm_blankflash_sizer.sv` | 8 | section 8.3 | yes, section 8.3 |
| `hdl/milan/KL_nvm_backend.sv` | 8 | sections 4, 8 and 9 | yes |

**Zero unresolved citations, and that is a change.** Round 2 left five
`hdl/common/csr/milan_csr.sv` comments citing this page by section and called
them stale on purpose. The review was right that this was the worse of the two
outcomes: restoring the page turned an obviously broken reference into a
plausible but false one, and the registers those comments annotate DO exist as
live CSR shells. They are repaired in this PR rather than named. Each of the
five now states the shell's actual status -- dead port or unwired, at VERSION
major 2 -- and points at the group section of
[`docs/reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) that documents
exactly that artifact, which is where the ABI and the preserved verdict tables
already live. None of them cites this page any more, because this page does not
describe those registers: it describes the plane that replaces them.

| line | cited this page as | now says |
|---|---|---|
| `447` | E1, Section 5 | DEAD PORT at VERSION major 2, register-map group `0x7A0` |
| `689` | E1, Section 5 | DEAD PORT, writes accepted, ack never asserts, group `0x7A0` |
| `701` | E3, Section 8, plus a deleted testbench | UNWIRED, writes discarded, `0x7C0` / `0x7C4` structural zeros, group `0x7B8` |
| `712` | E4, Section 10c, plus a deleted testbench | UNWIRED, writes discarded, `0x7D4` a structural zero, group `0x7C8` |
| `851` | E2, Section 5 | DEAD, no ACMP context table, `0x860` / `0x864` / `0x868` structural zeros, group `0x800` |

The two references to testbenches that were deleted with their engines
(`persist_wrap.sv` and `aempatch_wrap.sv`) went with them: a comment naming a
file that is not in the tree is the same defect one level down.

**Two corrections to round 1**, kept because they are still the record. It said
three Python files cite the page; there are **two**
(`sw/builder/test_builder.py` does not cite it at all, and the round-1 evidence
comment claiming it does was wrong). And it repaired sections 5 and 11 while a
third citation asked for **section 10**, which is why section 10 below is the
boot-side work rather than something else.

**The gate gap that let this happen is still open.**
`scripts/check_doc_paths.py` reads `git ls-files '*.md'`, so a citation inside a
`.py`, `.sv` or `.sh` comment is invisible to it and nothing in CI would catch
the next one. Widening it is a gate change with its own escape-hunt obligation
and belongs with #236 and #224; the table above is a hand-run substitute, and
the next person to move a section in this page has to re-run that grep by hand.

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

Record area: `N_REC` F07.8 frames concatenated **in ascending `record_id`**,
each `{magic 0x1722, layout_version, record_id, payload_length, crc16}`
big-endian followed by `payload_length` payload bytes, with no padding between
records. A record is self-delimiting from its own `payload_length`; nothing
else indexes it. The ascending order is normative rather than incidental: it
is what lets a decoder compute a record's byte offset from the shape and the
section 4.2 blocks alone, which is what the region decoder measured in
section 8.3 does, instead of carrying a 256-entry offset table. The area is zero-padded to a 4-byte boundary; the pad is counted in
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
| 12 | **every record this shape requires is present**: the exact `(group, index)` set derived from `descriptor_counts` and the writable-name count, section 4 | `VD_INCOMPLETE` |

A blank slot, all `0xFF`, fails test 1 and is reported as `VD_BLANK` rather than
an error: Milan permits an entity that has never been bound.

**Rule 12 is new, and it withdraws a sentence.** Round 3 of this page said that
an allocated id which is simply absent from the image is not a failure, because
that item was never saved and keeps its vendor default. The review was right
that this makes the whole acceptance order decorative: a CRC-clean image could
omit ANY mandatory saved item, publish an accepted `SEQ` and a durable-looking
status, and silently restore a controller-set value to the vendor default. It
also left a reader with no rule at all for telling an intentionally-defaulted
item from a writer that dropped a changed one, because absence carried both
meanings at once.

An image is now either COMPLETE for the shape it names or it is refused whole.
That costs nothing this page wanted: the shape is already pinned by
`entity_model_id` in rule 7, so "the image grows and shrinks with the shape"
was never a within-model property -- a shape change moves the model id and the
image is refused by identity anyway. What it buys is that absence stops being
an encoding. The set is derived, per shape, by
`scripts/check_nvm_record_space.py`, which deletes each mandatory record in
turn from a CRC-RECOMPUTED image and requires the refusal, with zero records
applied.

**Migration.** There is none from KLJ1: major 1 is refused with `VD_VER` and
never reinterpreted, and a board carrying one boots unbound, which is the same
degradation as a blank slot. Within major 2 a reader accepts any minor: a minor
may only add records with new ids, which rule 8 already refuses if the reader
does not know them, and rule 10's exact-fit test keeps an unknown trailing
record from being read as payload. Rule 12 constrains the OTHER direction --
a minor may not remove a record the shape requires -- and both are decided by
the shape, which rule 7 has already bound.

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
  reads the config's explicit `platform.pp_mem_phys`, validates its alignment,
  and emits a `no-map` `ppmem` reservation of `PP_MEM_BYTES` = 1,048,576 bytes
  (the AX7101 shapes place it at `0x7F700000`);
  `sw/litex/milan_soc.py` reads it and only checks it. It holds the descriptor
  image, measured at 40,000 bytes at 8x8, plus the 4,096-byte response buffer.
  Adding the measured 9,224-byte record image brings the window to 53,320 of
  1,048,576 bytes, about 5 percent. **No new reservation and no change to the
  published memory map.**
- The BRAM alternative is what is being declined, and its cost is the number
  that decides it: 9,224 bytes byte-wide is 3 BRAM36 at the 8x8 shape, on a
  device whose area campaign is fought in single-digit percentages.

### 8.2 The transfer: ordinary loads and stores, no CSR data window

**Decided.** Because the image is in DRAM, the firmware reaches it the way it
reaches anything else in DRAM. Nothing streams it through a CSR window and
nothing needs a separate transfer engine, because the data never has to move: the fabric
writes it where the CPU can already read it.

What crosses the CSR boundary is a control tuple only: the image base and
length, the sequence number, the dirty and verdict state of section 9, and the
firmware's acknowledgement. That is the smallest contract that can carry the
decision; bulk data does not cross the CSR window.

Landed as an indexed window of three registers, `PP_NVM_SEL`, `PP_NVM_DATA` and
`PP_NVM_STAT` at `0x934`-`0x93C`
([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md)): the word index, the word
it names, and the status and strobe word. Beside the tuple above the window
carries the two per-port channel-map length tables the section 4.2 decoder
needs, which firmware derives from the same overlay the descriptor image came
from. Writing the image base or length clears the image's validity, so a moved
image has to be validated again before a READ serves a byte out of it.

### 8.3 The area, measured

Issue #70 work item 1 asks for the flash path's area to be measured before
committing. Round 1 substituted issue #69's unrelated `+4,396 LUT` datapath
delta; round 2 removed it and declared the backend unmeasurable from a
documentation lane. The review refused that narrowing, and it was right to:
a bound does not need the shipping module, only a synthesizable candidate.

Round 3 supplied a candidate and the review found that it could not do the job
it was priced for, which is a different objection and a fair one: **a
synthesizable but functionally impossible sketch does not discharge an area
acceptance.** Two defects, both in the part that was supposed to be the
expensive part:

- the two channel-map groups shared ONE `{prefix,length}` table indexed by
  `dev_region_i[3:0]`, so `0x60+k` and `0x70+k` read the same entry. The
  generated 8x8 overlay is asymmetric -- an input port has 8 clusters (64-byte
  payload, 72-byte framed record), an output port has 17 (136 and 144) -- so at
  least one direction addressed the wrong span. The 1x1 shape is worse, not
  better: its single input port has ZERO clusters, an 8-byte framed record with
  no payload at all, against the same 136-byte output payload;
- the group base after each channel-map group advanced by a NOMINAL stride,
  although KLJ2 section 6.1 concatenates records with no inter-record padding.

Both are repaired, the nominal-size parameter is gone rather than corrected, and
the module under test is now the SHIPPING one, DRIVEN rather than only
synthesised.
[`tb/verilator/nvm_backend`](../../tb/verilator/nvm_backend/README.md) reads
every `0x60..0x67` and `0x70..0x77` mapping -- and every other allocated record
-- out of a byte-exact KLJ2 image at both shapes, and carries four negative
controls, each a copy of the shipping source with one defect planted (the three
above plus a READ that ignores the validity gate), every one of which must go
RED. The image's offsets come from
`scripts/check_nvm_record_space.py --emit-record-table` and its bytes are
rebuilt independently in the harness, which checks its own CRC-32 against the
encoder's before a clock is driven.

**Settled, and structural rather than estimated:**

- **Zero new flash controller and zero new pads.** The LiteSPI master is already
  instantiated with `with_master=True` in `sw/litex/milan_soc.py`; the decision
  adds no second master and no second consumer of the device.
- **Zero new BRAM.** The image is DRAM-resident by section 8.1, and the DRAM it
  needs is inside an existing reservation with the slack measured above.
- **Zero new DRAM reservation and no published-map change**, from the same measurement.

**Measured, before and after, on the same face.**
[`syn/ooc/sizing/KL_nvm_blankflash_sizer.sv`](../../syn/ooc/sizing/KL_nvm_blankflash_sizer.sv)
is the BEFORE: the blank-flash responder `hdl/milan/KL_pp_shadow.sv` carried
until the backend landed, lifted verbatim. The AFTER is the shipping module
itself, [`hdl/milan/KL_nvm_backend.sv`](../../hdl/milan/KL_nvm_backend.sv):
the region-to-offset decoder, the main-memory access path with its one-lane
word cache, the validity gate with its blank and discard paths, the span checks
a record operation must pass before a byte moves, the control CSRs and the
section 9 machine with its two deadline counters. Both are registered as tops in
[`syn/yosys/ooc.sh`](../../syn/yosys/ooc.sh) and measured with the recipe that
file already carries, `synth_xilinx -family xc7 -flatten`, which is the only
mapping this repository judges an area lever on.

| top | shape | LUT | LUTRAM | **LUT_TOT** | FF | RAMB36 | DSP | CARRY4 |
|---|---|---|---|---|---|---|---|---|
| `KL_nvm_blankflash_sizer` (before) | -- | 35 | 0 | **35** | 21 | 0 | 0 | 5 |
| `KL_nvm_backend` (shipping) | 1x1 | 756 | 0 | **756** | 377 | 0 | 6 | 108 |
| `KL_nvm_backend` (shipping) | 8x8 | 773 | 128 | **901** | 313 | 0 | 6 | 107 |
| `KL_nvm_backend`, `-nodsp` | 1x1 | 855 | 0 | **855** | 377 | 0 | 0 | 134 |
| `KL_nvm_backend`, `-nodsp` | 8x8 | 864 | 128 | **992** | 313 | 0 | 0 | 133 |

**The shipping module is above the candidate's bound, and the record says so.**
The sizing candidate this section priced the decision on measured 553, 676, 636
and 781 LUT-equivalents in the same four columns, with 280 and 216 FF; it is
retired with the module that replaced it. The shipping module is 211
LUT-equivalents and 97 FF above the candidate's worst case. The difference is
what the candidate did not carry and a device on a real port cannot do without:
the one-lane word cache (a 64-bit lane and its tag, so consecutive byte reads
inside a lane cost one memory transaction instead of eight), the validity gate
with the blank-read and write-discard paths that keep today's behaviour until
firmware has validated an image, the two span checks (inside the record, inside
the image) that refuse an operation before it touches memory, and the error and
status paths a bus error or a refused operation has to reach the processor
through. A bound that held while the shipping module is a fifth larger is still
the decision's bound; the number the bitstream carries is the one below.

**The `LUTRAM` column is new, and its absence was an under-count of 128 LUT.**
At the 8x8 shape yosys maps the two eight-entry channel-map tables to 32
`RAM32M` cells, and `syn/yosys/ooc.sh` counted only `LUT1..LUT6`, so 128 LUT6 of
SLICEM sat in no column at all and the block read 128 LUT cheaper than it is. A
distributed-RAM mapping is legal and is usually the cheap one; what is not legal
is pricing a block as though those LUTs were free. `ooc.sh` now converts every
distributed-RAM primitive to its LUT6 count (UG474: `RAM32M` and `RAM64M` and
`RAM128X1D` occupy 4, `RAM32X1D` and `RAM64X1D` occupy 2) and prints `LUT_TOT`.
The three calibration blocks below carry no distributed RAM, so their figures
are unchanged by it -- the column is additive, not a re-scaling.

The six `DSP48E1` are the constant-stride multiplies in the region decoder,
which the default `synth_xilinx` mapping happily hands to a DSP. Both mappings
are published because either is a legal implementation, and the `-nodsp` column
is the LUT-only worst case: **the backend costs at most 992 LUT-equivalents and
377 FF**, which is **1.56 percent of the XC7A100T's 63,400 LUT** and 0.30
percent of its 126,800 FF. The delta over the responder it replaced is **+957
LUT and +356 FF** in the LUT-only mapping, taking the worst column of each: 8x8
for LUT, 1x1 for FF, because the shapes trade one against the other (at 8x8 the
tables become distributed RAM and stop costing flops).

Calibration, measured in the same run so the figure is anchored rather than
free-floating: `KL_maap` is 637 LUT / 268 FF, `tcam` is 678 LUT / 1,680 FF and
`KL_chan_map_render` is 5,468 LUT / 2,101 FF (re-measured with the shipping
module on 2026-09-05; the render map grew with the cluster work since round 3,
the other two are unchanged). **Round 3's claim that the backend is smaller
than the MAAP engine is withdrawn**: at 992 LUT-equivalents it is larger than
either `KL_maap` or `tcam`, and under a fifth of `KL_chan_map_render`. What the
calibration still supports is the conclusion the
decision needs -- a block of this size cannot invalidate the selected
architecture on a device whose area campaign is fought in single-digit
percentages -- and it no longer supports the softer claim that was made
alongside it.

**What the number is, and is not.** `ooc.sh`'s own header states the rule this
repository uses: a standalone OOC figure is the UPPER bound for a block,
because in context it shares decode and constants with its neighbours, so the
in-context delta is always the smaller and truer number. It is also
pre-placement, and `scripts/area_baseline.py` records that post-synth numbers
move by thousands of LUT and that out-of-context numbers do not preserve rank
order. So this bounds the decision -- 992 LUT-equivalents cannot invalidate the
selected architecture on a device where the area campaign is fought in
single-digit percentages -- and it does not replace the post-place delta.

**What the implementation PR still owes**, with a recipe that runs today:

```sh
# before: the shipping build at the shape under test
scripts/area_baseline.py --build <before>
# after: the same shape with the backend
scripts/area_baseline.py --build <after> --compare <before>
```

Post-place, at both `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.
That is a build-time obligation on the module that actually lands, not a
precondition for the decision this page records: work item 1 asked for the area
to be measured before committing, and it is measured above.

**Reproduce it:**

```sh
# the before, and the three calibration blocks in the same run
syn/yosys/ooc.sh KL_nvm_blankflash_sizer KL_maap tcam KL_chan_map_render

# the after, at the 1x1 shape; prefix OOC_NODSP=1 for the LUT-only column
OOC_CHPARAM="N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_SPORT_IN_P=1 N_SPORT_OUT_P=1 \
             N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1 N_NAME_P=31" \
  syn/yosys/ooc.sh KL_nvm_backend

# the after, at the 8x8 shape
OOC_CHPARAM="N_STREAM_IN_P=9 N_STREAM_OUT_P=9 N_SPORT_IN_P=8 N_SPORT_OUT_P=8 \
             N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1 N_NAME_P=107" \
  syn/yosys/ooc.sh KL_nvm_backend

# and what the module actually DOES, at both shapes, with the four
# negative controls that must each fail
make -C tb/verilator/nvm_backend
```

There is no `MAP_BYTES_P` any more. Round 3's recipe passed a nominal
channel-map size, and no single value is right: at 8x8 the two directions are 72
and 144 framed bytes, and at 1x1 they are 8 and 144. The lengths are
firmware-loaded per port and per direction now, and the group bases after them
are derived from those lengths.

`OOC_NODSP=1` is added to `ooc.sh` by this PR for the same reason both columns
are published: a block whose only DSPs come from constant strides is priced
honestly only if the LUT-only mapping is shown as well, because the DSP column
hides LUTs.

`KL_nvm_blankflash_sizer` takes no `OOC_CHPARAM`: it has no parameters, and
passing any makes yosys refuse with `Can't find object for defparam`. That is
also the negative control for the two `OOC_CHPARAM` runs above -- the 1x1 and
8x8 columns differ, so the parameters are reaching the design rather than being
silently ignored.

**Why the BEFORE sketch is not under `hdl/`, and the AFTER is.** The
blank-flash sizer is not shipping RTL any more: nothing instantiates it,
`milan_soc.py` does not register it, and `scripts/lint_rtl.py` sweeps `hdl/`
and would treat it as a module the SoC forgot to wire, so it stays in
`syn/ooc/sizing/` and states its status structurally. The backend IS shipping
RTL: it lives in `hdl/milan/`, `lint_rtl.py` sweeps it, all five RTL source
lists carry it (`scripts/check_rtl_source_lists.py`), `syn/yosys/run.sh`
synthesises it as a top of its own and inside `KL_pp_shadow` and
`milan_datapath`, and `tb/verilator/nvm_backend` lints both files with `-Wall`
and no `-Wno-*` as its `lint` prerequisite. Round 3's PR published a lint
command that did not reproduce, because one file declared two top-level modules
and tripped `DECLFILENAME` under this repository's Verilator 5.050; the tops
have lived in one file each since, and the check is a suite step the
`verilator-suites` aggregate carries, not a sentence.

One simplification remains from the candidate's header. The channel-map one is
gone: it was the largest under-count risk, it turned out to be an outright
defect rather than a risk, and it is direction-distinct state that the suite
grades against a byte-exact image. The datapath still moves one byte per
device-face handshake, as the processor's port does; on the memory side the
word cache already coalesces the reads of one lane into one transaction, and a
write is one strobe-masked lane per byte. A variant that gathered a record's
write bytes into whole lanes would trade a lane buffer for fewer bus cycles,
which is tens of LUT either way on a 992-LUT block, and the bus is not what the
port's byte pace waits on.

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
| `[9]` | `nvm_stale` | `nvm_backed` was true since reset and is now false, and the loss has not been made good; cleared by the recovery rule of section 9.2, never by a writer merely answering again |
| `[15:12]` | `nvm_verdict` | the section 6.2 verdict code of the last image offered |

`nvm_backed` remains **fabric-derived evidence and never a knob**: no CSR write
can set it, which is the property that made it a localparam rather than a
parameter in the first place, and it survives being made dynamic.

**Landed (2026-09-05)**: `PP_STAT[8]`, `[9]`, `[10]` `nvm_img_valid` (firmware
validated the image in the window) and `[15:12]` are published as above, driven
by `KL_nvm_backend` through `KL_pp_shadow`, and the same word is readable on the
backend's own face as `PP_NVM_STAT`. One verdict moved with them: `restore_fail`
on a completed walk now means a torn read-back OR a **blind walk**, one during
which no validated image stood behind the device face for every cycle. The
shadow latches that per walk rather than reading the live level, because a
firmware that validates the image after the walk has restored nothing, and a
verdict that flipped to success on it would be this page's false success moved
up one level. `tb/verilator/pp_shadow` drives exactly that sequence: a walk, then
a heartbeat that makes the writer live, and `restore_fail` stays raised.

### 9.2 When it sets, when it is revoked, and when the loss is forgiven

**`nvm_backed` sets** on the first firmware answer after reset that completes a
whole transaction: a commit whose read-back verified, a boot restore whose slot
passed section 6.2, or a heartbeat. The reset value is 0.

**Re-arms** the `T-NVM-WRITER-ALIVE` deadline on every heartbeat and on every
completed transaction.

**Clears** on any of: `T-NVM-WRITER-ALIVE` expiring; a commit not acknowledged
within `T-NVM-COMMIT-TIMEOUT`; a reported erase, program or read-back-verify
failure; a reported JEDEC identity mismatch; the port's `nvm_alarm` raised by
bounded-retry exhaustion.

**`nvm_stale` sets** whenever `nvm_backed` falls after having been 1 at any
point since reset. It is not set by a build that never had a writer: that is
the `(0,\*,0)` "never backed" state, which is a different and honest thing.

**`nvm_stale` clears** when `nvm_backed` is true again AND `nvm_dirty` is 0 --
that is, when the writer is live and nothing the outage left outstanding is
still un-durable. Two cases fall out of that one rule:

- Nothing was outstanding when the writer was lost. The loss cost nothing, so
  the bit clears as soon as liveness returns.
- Something was outstanding. The bit stays set through the recovery until the
  commit that makes `nvm_dirty` 0 completes.

**The rule clears the STATE, not just the view.** Round 3 wrote this section
both ways at once: it said the bit clears after a clean recovery, and then said
the latch is cleared only by reset with the published bit masked by
`NOT (backed AND NOT dirty)`. The candidate implemented the second, and the
review was right that the two are not the same contract. A mask makes a healed
outage LOOK repaired while the latch still remembers it, so the next ordinary
controller change -- which sets `nvm_dirty` and therefore lifts the mask --
republishes `nvm_stale` = 1 with no new loss anywhere. One historical outage
would contaminate every commit for the rest of the power cycle, and the
`(backed=1, dirty=1, stale=0)` in-flight row of section 9.3 would be
unreachable in practice.

So the recovery condition clears the latch itself, and there is no mask. Stated
as a next-state function with its priorities written out rather than left to
statement order:

```
loss     = (T-NVM-WRITER-ALIVE expired OR T-NVM-COMMIT-TIMEOUT expired)
           AND a writer had been live at some point since reset
backed'  = loss ? 0 : heartbeat ? 1 : backed
dirty'   = change_accepted ? 1 : commit_acknowledged ? 0 : dirty
stale'   = loss ? 1 : (backed' AND NOT dirty') ? 0 : stale
```

Two priorities are deliberate. A loss in the same cycle as a heartbeat WINS,
because a heartbeat proves the writer answered at some point, not that the
deadline had not already lapsed. A change accepted in the same cycle as a commit
acknowledgement WINS, so a controller SET landing on the commit boundary is
never lost.

The recovery arm is evaluated on the NEXT values of the other two bits, which is
what makes the clear atomic with the event that earns it rather than one cycle
late. It also makes `(backed=1, dirty=0, stale=1)` unreachable in the STATE
rather than masked at the face: `stale` can only still be 1 if the previous
cycle took the loss arm, which drove `backed'` to 0, or held the latch, which
requires `backed'` = 0 or `dirty'` = 1. No read can observe the pair because no
cycle holds it.

The rule is deliberately NOT "clears when a writer answers again". A writer
that comes back has proved liveness, not durability; the changes accepted while
it was gone are still only in the volatile image. Clearing on the answer would
re-create exactly the false-success condition issue #70 exists to remove, one
level up. That is why the `AND NOT dirty` half of the condition is load-bearing,
and `tb/verilator/nvm_backend` drives all four sequences -- a never-backed
build, a loss with nothing outstanding followed by a recovery and a later
ordinary change, a loss with data outstanding that stays stale through the
recovery until the commit completes, and a second loss that sets it again --
with the round-3 keep-the-latch machine compiled in as a negative control that
must fail.

### 9.3 Reading the three bits together

All eight combinations, with the one that cannot occur named as such rather
than left off the table. Round 2's version of this table had five rows and used
"any" in one of them, which hid the recovery state entirely.

| `nvm_backed` | `nvm_dirty` | `nvm_stale` | Reachable | Meaning |
|---|---|---|---|---|
| `1` | `0` | `0` | yes | **Durable.** Everything committed is in a slot |
| `1` | `1` | `0` | yes | **In flight.** A commit is inside the debounce window or in progress; a power cut here loses the marked changes and nothing else |
| `1` | `0` | `1` | **no** | Unreachable by construction: the recovery arm of section 9.2 clears the latch on exactly this condition, and a loss forces `backed` to 0 in the same cycle, so no cycle holds the pair and no read can observe it |
| `1` | `1` | `1` | yes | **Recovering.** The writer is answering again, but changes accepted during the outage are still not durable. Reads as backed, because a commit will now complete, and as stale, because one has not yet |
| `0` | `0` | `0` | yes | **Never backed, nothing outstanding.** Reset state, and the state of a build with no writer |
| `0` | `1` | `0` | yes | **Never backed, changes accepted.** A controller SET landed before any writer answered. Nothing is backed and nothing claims to be |
| `0` | `0` | `1` | yes | **Writer lost, nothing outstanding.** Everything that was committed is durable; new changes will not be |
| `0` | `1` | `1` | yes | **Writer lost with data outstanding.** The image accepted changes that are NOT durable. This is the wedged-writer case, and it reads as not backed |

The split between `dirty` and `backed` is the part that matters. When the writer
wedges, the entity must keep answering AECP and keep accepting SETs: refusing a
controller because flash is unreachable would be a worse defect than not saving.
What it must not do is claim durability. `nvm_dirty` is what makes the debounce
window visible instead of implicit, and it is what a power-cut test reads to
know whether the loss it observed was permitted.

### 9.4 The deadlines

Round 2 made `T-NVM-WRITER-ALIVE` and `T-NVM-COMMIT-TIMEOUT` load-bearing and
gave neither a value, which left two conforming implementations free to
disagree about when a legal flash operation becomes a stale one. Both are fixed
here, and both are derived rather than chosen.

**The media's worst case.** Micron N25Q128 Table 32 "AC Characteristics",
MAXIMUM column: `tSE` = **3 s** for one 64 KiB sector, `tPP` = **5 ms** for one
page program of up to 256 bytes. The read-back runs at the instantiated LiteSPI
clock, `add_spi_flash(mode="1x", clk_freq=12.5e6)`, so a byte costs 8 clocks.
One whole-image A/B commit is one erase, `ceil(image / 256)` page programs and
one read-back:

```
T_commit_worst = tSE(max) + ceil(IMG_LEN/256) x tPP(max) + IMG_LEN x 8 / 12.5e6
```

| shape | image | pages | erase | program | read-back | **worst case** |
|---|---|---|---|---|---|---|
| `endstation_ax7101_1x1_tdm8` | 2,696 B | 11 | 3,000 ms | 55 ms | 1.7 ms | **3.06 s** |
| `endstation_ax7101_8x8` | 9,224 B | 37 | 3,000 ms | 185 ms | 5.9 ms | **3.19 s** |

The erase dominates: 94 percent of the worst case at 8x8 is one `tSE`.

**`T-NVM-COMMIT-TIMEOUT` = 8,000 ms**, required to be at least **2x** the
worst-case transaction at EVERY shipped shape. That is 2.51x at 8x8 and 2.62x
at 1x1. The margin covers the byte pump, the CPU's polling loop and a second
erase if the first slot verify fails. Below 2x the deadline starts declaring
legal flash operations dead, which is the failure mode the review named.
`scripts/check_nvm_record_space.py` asserts the relation at every shape, so a
shape that grows the image past the deadline reddens a gate instead of
shortening a commit.

**`T-NVM-WRITER-ALIVE` = 2,000 ms**, with a required heartbeat period of at
most **500 ms**, so four heartbeats fit inside the deadline. It is deliberately
SHORTER than the commit timeout, and that is only sound because of a normative
requirement on the writer: **the heartbeat is serviced from the same status-poll
loop the writer already runs while an erase is in progress.** The writer is a
CPU driving the LiteSPI command master and polling RDSR; it is not blocked
during `tSE`, it is spinning. A writer that cannot kick the heartbeat during an
erase is not conformant, and the alternative -- stretching the liveness deadline
past the commit timeout -- would leave a dead writer advertised as durable
backing for over eight seconds.

The 2,000 ms value is an NVM-local writer contract: it admits four required
heartbeat opportunities at the 500 ms maximum period while remaining well
below the commit timeout. `CLKV_CTRL` at `0x778` is an inert compatibility
address in the current map and supplies no timer or refresh mechanism to this
contract.

**The relation, stated once**, and asserted by the gate:

```
T-NVM-HEARTBEAT     <=  T-NVM-WRITER-ALIVE / 4          =  500 ms
T-NVM-WRITER-ALIVE                                      = 2000 ms
T-NVM-COMMIT-TIMEOUT >= 2 x T_commit_worst(every shape) = 8000 ms
```

`T-NVM-DEBOUNCE` is a different quantity and is still open; section 14 says so
and section 13 says what the PR that picks it owes.

## 10. Boot-side work

Cited by the retired flash-partition emitter as
where the previous target-side experiment lived; it is not part of the current
bare-metal persistence contract.

1. **The slot offsets are generated, not hand-written.** `journal@ee0000` and
   `user@f00000` come from the same `FLASHBOOT_RESERVED` reader `milan_soc.py`
   uses, so there is no second copy to drift.
2. **The previous block layer never bound this controller.** In the superseded
   profile the slots were declared and never parsed, which is the reason G1 in
   section 11 is a falsifier rather than a pass criterion.
3. **The write path is the LiteSPI CSR master either way.** Nothing in this
   design needs a block layer.
4. **On the shipping `--flashboot baremetal` profile** the second-stage boot
   chain is gone entirely (#259). The equivalent obligation is that the
   firmware resolves the slot offsets
   from the generated map rather than from literals, which is what keeps
   `milan_soc.py` the single source of truth for the firmware as well.
5. **A reflash must not erase either reserved slot.** A gateware update that
   silently wipes saved bindings is worse than having none.

## 11. Bench recipe

**G0 -- build with the layout (workstation only, no board).** `sw/builder/test_builder.py`
checks the map's internal consistency, including that every image still fits under
the reserved slots. It passes today.

**G0b -- the record set is complete and fits the namespace (workstation only, no
board).** `scripts/check_nvm_record_space.py`, and `--self-test` for its eleven
negative controls. Both pass today. The gate also publishes the F07.8
conformance floor of section 4.3 and the worst-case commit time of section 9.4
per shape, so those two figures are re-derived on every run rather than quoted
from this page.

**G1 -- the partition appears.** This gate belonged to a superseded target
profile, where the two reserved slots were published to a block layer that
never bound this controller, so they were declared and never parsed. **On the
shipping baremetal profile G1 does not apply**; section 10 item 4 is the
equivalent.

**G2 to G5** -- restore from a preloaded image, fast connect with no
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

- **The firmware writer is missing.** The shipping profile is
  `--flashboot baremetal` and the current firmware only reads. The write path
  must be implemented in `sw/firmware/milan_baremetal/` against the same CSRs.
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
- **The record contract has no external dependency left, and the gate says
  so.** Section 4.2 is the donor's F07.8 rule unchanged, so no donor amendment
  gates the names allocation; the 2026-08 proposal, its correction and its
  reversal are recorded in section 4.3. What stays external is the donor pin
  itself: `REC_ID_BASE_P` and `LAYOUT_VER_P` are read from the pinned RTL, and
  a donor that moves either reddens `scripts/check_nvm_record_space.py`.
- **Both liveness deadlines are derived from a datasheet maximum, not from the
  bench.** `tSE` = 3 s is the N25Q128's specified worst case; the parts on the
  board will be far faster. If a future device is slower, section 9.4's
  relation, not its number, is what has to be re-evaluated, and check 7 of the
  gate is where that shows up.

## 14. What this page does NOT decide

Two things. Round 2 said two and listed neither of the deadlines it had made
load-bearing; the deadlines are decided in section 9.4 now, and the names
allocation that rounds 3 and 4 listed here is decided in section 4.2.

- **The debounce window's value.** `T-NVM-DEBOUNCE` is a wear-versus-loss trade
  that needs a bench, and section 13 says what the PR that picks it owes. It is
  a different quantity from the two deadlines of section 9.4, which are fixed
  here.
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
      its `--self-test` still reddens on all fifteen negative controls,
      including the four omission arms, the two index-set arms, the shrunken
      namespace and the two that restore a round-3 decoder rule.
- [ ] Every user name of the largest shipped shape is encoded by one
      implementation and decoded by the other, byte for byte, as one record per
      writable-name ordinal at the section 4.2 ids.
- [ ] A mutation that makes the record index and the name ordinal disagree is
      caught rather than silently mis-restored.
- [ ] A user name SET to the EMPTY string survives a power cycle as the empty
      string, proven against a vendor default that is not empty.
- [ ] The manager emits records at the section 4.2 ids, and a record whose id is
      outside its group's block is refused rather than written.

**The container**

- [ ] A pinned golden image per shape, byte for byte, with its CRC, produced by
      the firmware encoder and reproduced by the fabric decoder.
- [ ] One refused case per verdict code in section 6.2, each proving **zero**
      records were applied: foreign entity, foreign model, bad magic, wrong
      major, truncated, overrun, bad digest, unknown record id, duplicate record
      id, mixed layout_version, torn slot, stale sequence.
- [ ] Records are emitted in ascending `record_id` (section 6.1), and a decoder
      that computes offsets from the shape agrees with one that walks the
      records.
- [ ] Deleting each mandatory record in turn from a CRC-RECOMPUTED image is
      refused with `VD_INCOMPLETE` and **zero** records applied (rule 12).

**The status bits**

- [ ] `nvm_backed` reports the truth on a build with and without a writer,
      proven both ways.
- [ ] A writer that answers once and then stops drives `nvm_backed` to 0 and
      `nvm_stale` to 1 within `T-NVM-WRITER-ALIVE`, with `nvm_dirty` reporting
      whether anything was outstanding.
- [ ] A failed erase, a failed program and a failed read-back-verify each revoke
      `nvm_backed` independently.
- [ ] **Every reachable row of the section 9.3 table is produced**, and the one
      marked unreachable, `(backed=1, dirty=0, stale=1)`, is never observed at a
      CSR read boundary.
- [ ] **Recovery**: after a writer is lost with data outstanding and then comes
      back, `nvm_stale` stays 1 until a commit completes with `nvm_dirty` 0, and
      clears then. A writer that merely answers again does NOT clear it.
- [ ] **A healed outage does not contaminate later commits**: after a loss with
      nothing outstanding and a clean recovery, an ordinary controller change
      reads `(backed=1, dirty=1, stale=0)`, and a keep-the-latch implementation
      fails that check.
- [ ] **A late-but-valid completion** -- a commit that finishes after
      `T-NVM-COMMIT-TIMEOUT` has already revoked `nvm_backed` -- is accepted as
      data and does not resurrect the claim by itself.
- [ ] **A legal flash operation is never declared stale early**: a commit taking
      the datasheet worst case of section 9.4 completes inside
      `T-NVM-COMMIT-TIMEOUT` at both shapes, and the heartbeat is serviced
      throughout the erase.
- [ ] A timeout injected during each of erase, program and read-back produces
      the same revocation and the same verdict, and the three are distinguished
      in `nvm_verdict`.
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

**The area**

- [ ] `scripts/area_baseline.py --compare` post-place at both
      `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`, against the
      section 8.3 OOC bound. The OOC figure is an upper bound and the in-context
      delta should come in under it; a post-place delta ABOVE 781 LUT means the
      shipping module diverged from the candidate that was priced, and the
      divergence has to be explained rather than absorbed. Distributed RAM
      counts: `ooc.sh`'s `LUT_TOT` column exists because 128 LUT6 of SLICEM were
      being priced at zero.
