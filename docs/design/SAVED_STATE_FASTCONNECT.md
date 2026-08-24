# Saved state and fast connect — the backing store decision

Milan v1.2 names eight things a PAAD-AE shall keep across a power cycle, plus
the bound state, the binding parameters and the started/stopped state. This
device keeps none of them. `KL_pp_shadow` answers the processor's NVM port with
a blank-flash responder: reads return `0xFF`, writes are accepted and discarded,
erase completes. A restore walk therefore always finds blank flash, restores
zero records, and -- until the wrapper started publishing `nvm_backed_o` --
reported success for it.

This page is the **decision record** issue #70's first work item asks for:
which media backs those records, who owns the write path, and what the fabric is
allowed to claim about a restore. It does not describe a built system. Every row
below is marked with what proves it.

> **A page of this name existed before and was deleted** in `eff99a9c`, the
> commit that substituted the legacy 1722.1/SRP plane for the protocol
> processor. It described an architecture that no longer exists -- a CSR ingest
> group the fabric consumed at boot -- and deleting it with the plane was right.
> What was NOT right is that three source files still cite it by section
> (`sw/litex/milan_soc.py` section 5, `sw/dts/gen_mtd_partitions.py` and
> `sw/builder/test_builder.py` section 11), and nothing caught that:
> `scripts/check_doc_paths.py` reads `git ls-files '*.md'`, so a citation inside
> a `.py` comment is invisible to it. This page restores that path and keeps
> those two section numbers meaningful. The gate gap is filed separately.

## Contents

- **[1. Status](#1-status)** -- A row per piece with the evidence that proves it. The honest bottom line: the media is reserved and the processor frames records, but there is no device behind the port and the shipping firmware profile cannot write flash at all.
- **[2. What the two ends actually look like](#2-what-the-two-ends-actually-look-like)** -- The port offers a per-record region with `ERASE_REGION`; the media offers 64 KiB erase blocks, two of them. They do not compose, and the port's torn-write guarantee is weaker than the media's -- this section is why something has to sit between them.
- **[3. The decision](#3-the-decision)** -- One image, promoted A/B, media owned by firmware through the LiteSPI master that already exists. Three measured reasons rather than a preference: the record set fits one erase block at both shapes, a second fabric master would duplicate logic and contend for the same device, and the write sequence is silicon-proven in history.
- **[4. The record image format](#4-the-record-image-format)** -- The `KLJ1` container carried forward unchanged, holding the processor's own F07.8 record frames. The firmware never parses a record's meaning, only the container.
- **[5. Where it lives in the 16 MB QSPI](#5-where-it-lives-in-the-16-mb-qspi)** -- The two reserved slots and why `journal` is raw rather than a filesystem, plus the rule a reflash must obey. Cited by `milan_soc.py` as the map's single source of truth.
- **[6. Durability: the A/B contract](#6-durability-the-ab-contract)** -- The write and read rules in full, and the property they buy: at every instant of a commit at least one slot holds a complete image whose CRC closes.
- **[7. Risks, stated rather than discovered later](#7-risks-stated-rather-than-discovered-later)** -- The proven writer no longer exists in the tree, persistence now depends on firmware liveness, the debounce window is a data-loss window that a PR must quantify, and four donor defects are open against the port.
- **[8. What this page does NOT decide](#8-what-this-page-does-not-decide)** -- The backend's memory, the backend-to-firmware contract, the debounce window and the transfer mechanism, with a note that section 3.1 sizes them rather than leaving them free.
- **[9. Sequencing](#9-sequencing)** -- Why this page is deliberately ahead of the submodule pin it will be implemented on.
- **[10. Acceptance for the implementation](#10-acceptance-for-the-implementation)** -- Six checks, including the vacuity trap a naive save/restore test falls into and the requirement that deleting an existing `NVM_MARK` must redden something.
- **[11. Bench recipe](#11-bench-recipe)** -- G0 and G1, which run today, and what G1 means on a baremetal profile where no MTD device ever probes. Cited by `gen_mtd_partitions.py` and `test_builder.py`.

## 1. Status

| Piece | State | Evidence |
|---|---|---|
| The flash map reserves the media | **Landed** | `FLASHBOOT_RESERVED` in `sw/litex/milan_soc.py`: `journal` at `0xEE_0000`, 128 KiB, and `user` at `0xF0_0000`, 1 MiB |
| The processor frames and streams records | **Landed** (submodule) | `KL_pp_nvm_port` + `KL_acmp_nvm_shadow`; the donor's nvm_port suite, 90/90 at pin `44489453` |
| The processor emits commit marks | **Landed, unobserved** | `NVM_MARK` in `SET_CONFIGURATION`, `SET_SAMPLING_RATE`, `SET_CLOCK_SOURCE`; both strobes terminate in a no-connect at `protocol_processor_top.sv` |
| A device behind the port | **ABSENT** | `NVM_BACKED_C = 1'b0` in `hdl/milan/KL_pp_shadow.sv`, a localparam and deliberately not a parameter |
| A write path on the shipping profile | **ABSENT** | the baremetal firmware reads flash through the XIP window and has no erase or program path |
| The backing store | **DECIDED HERE**, not built | section 3 |

## 2. What the two ends actually look like

**The port's face** (`KL_pp_nvm_port`, measured from its ports): a region-addressed
byte stream. `{op READ / WRITE / ERASE_REGION, region = record_id (8 bits),
offset (16 bits), len (16 bits)}`, one byte per handshake, `done` and `err` as
one-cycle pulses. One region per record: "a partial update never rewrites
unrelated records". Records carry `{magic 0x1722, layout_version, record_id,
payload_length, crc16 CCITT-FALSE}`; a BINDING payload is 20 bytes at
`record_id = 0x20 + sink`.

**The media's face**: a 16 MB N25Q128 whose smallest erase unit is a 64 KiB
block, of which exactly two are reserved for this purpose, as slot A and slot B.

These do not compose directly, and that is the whole design problem:

- `ERASE_REGION` per record has no meaning on NOR flash unless a region is at
  least an erase block. 256 possible record ids x 64 KiB is the entire device.
- The port's durability guarantee is weaker than the media's. The donor's own
  review states it: a torn commit leaves every OTHER record untouched, but the
  record being rewritten is unprotected, and because the erase precedes the
  write, `err` never means "the saved set is unchanged". Closing that needs the
  specified-but-unimplemented crc16 check or A/B promotion; the port has no slot
  notion at all.

So something between them has to turn a per-record region port into a
whole-image A/B promotion. Section 3 decides where that something lives.

## 3. The decision

**The record set is stored as one image, promoted A/B into the reserved raw
`journal` slots, and the media is owned by the firmware through the LiteSPI
master that already exists. The fabric owns the verdict, never the media.**

Three things make that the answer rather than a fabric-side flash master:

1. **The whole set fits in one erase block, measured.** With the F07.8 framing
   (8-byte header + payload), at the shipping `endstation_ax7101_1x1_tdm8`
   shape: 31 names x 72 B = 2,232 B, plus bindings, formats, offsets, maps,
   clock source, configuration index and system unique id -- on the order of
   **2.5 KiB**. At the 8x8 shape: 235 names x 72 B = 16,920 B, about **20 KiB**.
   Both fit one 64 KiB block with margin, so whole-image promotion is not a
   compromise forced by geometry; it is comfortably affordable, and it upgrades
   the durability guarantee from the port's per-record one to "at every instant
   at least one slot holds a complete CRC-closing image".
2. **The controller already exists and the fabric does not need pads.**
   `sw/litex/milan_soc.py` instantiates `add_spi_flash(mode="1x",
   clk_freq=12.5e6, with_master=True)`. `with_master=True` is a CSR-driven
   command master: write enable, page program and sector erase are reachable
   today from the CPU. A second master in fabric would duplicate that logic AND
   contend for the same physical device with the boot path. The standing
   instruction to keep usage low and re-use existing resources points the same
   way, and the area measured for issue #69 (+4,396 LUT on the datapath, epic
   #229 open against exactly this plane) makes new fabric area expensive.
3. **The recipe is silicon-proven, in history.** The deleted page records that a
   userspace writer, `acmp-persist`, drove RDID / WREN / SE-D8 / PP / RDSR over
   those CSRs against this board, with a JEDEC guard and an address clamp. It is
   no longer in the tree -- see the risk in section 7 -- but the sequence is not
   speculative.

### 3.1 What that means concretely

- The parent gains an **NVM backend** behind `KL_pp_shadow`'s device face which
  holds the record image in fabric memory, not in flash: reads answer from it,
  writes update it, `ERASE_REGION` invalidates a record within it.
- Commits are **published**, not written: the backend raises a "image dirty,
  sequence N" state that the firmware reads, and the firmware performs
  erase / program / read-back-verify / promote on the inactive slot.
- At boot the firmware reads both slots, picks the newer by a wrap-safe
  `(int32_t)(A.seq - B.seq) > 0`, and hands the image to the backend, which
  serves the processor's restore walk from it.
- `nvm_backed_o` stops being a constant `0` and becomes **evidence-driven**: it
  asserts only once a writer has answered at least once since reset. A build
  with no firmware writer must keep reporting `0`, because that is the truth.

## 4. The record image format

Carried forward unchanged from the deleted page, because nothing about it
depended on the legacy plane: a `KLJ1` header `{magic, version, seq, n_rec,
rec_words, crc}`, `n_rec` records of `rec_words`, and a trailer word. The
per-record framing inside it is the processor's F07.8 frame, so the image is a
container for records the processor already produces and validates; the firmware
never parses a record's meaning, only the container.

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

## 6. Durability: the A/B contract

```
write:  new_seq = accepted_seq + 1
        target  = the slot that is NOT currently authoritative
        erase(target) ; program(target, image(new_seq)) ; read back ; verify crc
        the authoritative slot is never erased

read:   read both slots; newer = (int32_t)(A.seq - B.seq) > 0
        push the newer; if the fabric rejects it, push the other
        if both are rejected, do nothing -- boot unbound
```

At every instant of the write sequence at least one slot holds a complete image
whose CRC closes. Power can be removed at any point. This is the guarantee the
port alone cannot give, and it is why the promotion lives above the port rather
than inside it.

## 7. Risks, stated rather than discovered later

- **The proven writer is gone.** `acmp-persist` was a Linux userspace program in
  a rootfs overlay; the shipping profile is `--flashboot baremetal` and the
  baremetal firmware is one C file that only reads. The write path must be
  written again, in `sw/firmware/milan_baremetal/`, against the same CSRs. The
  historical program is recoverable from git if its exact command sequence is
  wanted.
- **Persistence now depends on firmware liveness.** A fabric-owned master would
  not. This is the price of re-using the controller, and it is why
  `nvm_backed_o` must be evidence-driven: a wedged or absent writer has to
  degrade to an honest "nothing is backed", never to a silent lie.
- **The debounce window is a data-loss window.** The processor already debounces
  commits (`T-NVM-DEBOUNCE`, coalescing) and the mapping compliance sequence
  issues a dozen SETs in a row, so a commit per command would burn erase cycles
  for nothing. Whatever window is chosen, the PR that lands it must say what a
  power cut inside it loses.
- **Four donor defects are open against the port** and matter to any consumer:
  an unowned `done_seen_r`, no timeout so a silent device wedges the port,
  restore failures collapsing three situations into one signal, and `record_id`
  never checked against its region.

## 8. What this page does NOT decide

The fabric-memory backend's shape (BRAM versus the existing DRAM masters), the
CSR contract between backend and firmware, the debounce window, and whether the
image is served to the firmware by DMA or by a CSR window. Those are the
implementation ticket's, and they are sized by section 3.1's requirements rather
than free choices.

## 9. Sequencing

The parent-side work starts when issue #69's submodule pin is on `dev`: that pin
is the one carrying the donor's nvm_port power-cut coverage, and there is no donor
commit with one without the other. This page is deliberately ahead of it,
because the decision it records is what the implementation needs first and it
depends on none of that.

## 10. Acceptance for the implementation

- [ ] `nvm_backed_o` reports the truth on a build with and without a writer, proven both ways.
- [ ] A restore walk over blank flash reports "nothing restored", never success.
- [ ] All eight Milan items plus the bound state, the binding parameters and started/stopped survive a reset that is proven to have cleared the rows first (the vacuity trap: a restore that writes nothing and a store that was never reset both pass a naive read-back).
- [ ] The volatile set does NOT survive: after restore the lock is clear, the controller registry is empty, IDENTIFY is 0.
- [ ] A commit interrupted at every stage leaves a complete image in one slot.
- [ ] The three existing `NVM_MARK` call sites become gradeable end to end -- deleting a mark must redden a test, which today it does not.

## 11. Bench recipe

**G0 -- build with the layout (host only, no board).** `sw/builder/test_builder.py`
checks the map's internal consistency, including that the rootfs still fits under
the reserved slots. It passes today.

**G1 -- the partition appears.** On a Linux profile, `journal@ee0000` and
`user@f00000` are in the DTS and the built DTB.
[`sw/dts/gen_mtd_partitions.py`](../../sw/dts/gen_mtd_partitions.py) derives them
from the same map. Note the standing limitation recorded there: no upstream
Linux driver claims `litex,spiflash`, so MTD registers `/proc/mtd` and no device
ever probes -- the partitions are declared but never parsed, and the write path
is the CSR master either way. **On the shipping baremetal profile G1 does not
apply**; the equivalent is that the firmware resolves the slot offsets from the
generated map rather than from literals.

**G2 to G5** -- restore from a host-written image, fast connect with no
controller, the write path, and the reboot drill -- are the implementation
ticket's and need a board. The bench is down at the time of writing.
