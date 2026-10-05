<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ctrl_nvm: the bare-metal saved-state store (#665 F1)

Portable C11 for the on-chip RISC-V, and for a hard core: the saved entity
state read from the flash at boot, judged, applied and written back on
change, with no OS and no heap. Every buffer is a static array sized from the
entity shape at build time. It is the firmware side of the #70 saved-state
design ([backing store](../../../docs/design/SAVED_STATE_FASTCONNECT.md),
[materialization](../../../docs/design/SAVED_STATE_MATERIALIZATION.md)) for
the Mark II split of #665. Nothing here is linked into any image yet: the
store sits behind the #665 build switch, whose default is the all-fabric
build, and the shipping writer in
[`milan_baremetal`](../milan_baremetal/milan_baremetal.c) is unchanged.

`python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`
is the gate. Exit 0 means every check passed on every shipped shape, both
flash ports and every planted defect was caught.

## Contents

- **[Layout](#layout)** -- The codec, the store, the two ports, the host models and the suite.
- **[The flash port](#the-flash-port)** -- Five calls, two implementations, and the seam with F0's mailbox HAL.
- **[Boot](#boot)** -- Both slots judged by section 6.2, the newer one staged, re-judged and applied as one transaction.
- **[Write-back](#write-back)** -- One bounded step per service call: capture, seal, erase, blank check, program, read back.
- **[Static sizes](#static-sizes)** -- What each shipped shape costs, measured on the RV32I build.
- **[The host suite](#the-host-suite)** -- Twenty-six checks per shape, 24 of them on both ports, the power-cut sweep and the planted defects.
- **[What this does not prove](#what-this-does-not-prove)** -- The board, the generated headers and the switch.

## Layout

| Path | What it holds |
|---|---|
| [`nvm_shape.h`](nvm_shape.h) | the record set and the container sizes, derived from the generated `MILAN_NVM_*` constants |
| [`nvm_klj2.c`](nvm_klj2.c) | the KLJ2 container and F07.8 record codec, and the section 6.2 acceptance order |
| [`nvm_flash.h`](nvm_flash.h) | the flash port; [`nvm_flash.c`](nvm_flash.c) its one blocking helper |
| [`nvm_state.h`](nvm_state.h) | the state port: where a saved value is applied and a changed one latched |
| [`nvm_store.c`](nvm_store.c) | the boot restore and the write-back |
| [`plat/`](plat) | the LiteSPI flash port and the target's constants header |
| [`host/`](host) | the flash model with its faults, the LiteSPI command-master model, the state model |
| [`test/`](test) | the scenario runner, the checks, the planted defects and the RV32 arm |

## The flash port

[`nvm_flash.h`](nvm_flash.h) is the whole media face: `read`, `program` (one
page at most), `erase` (one 64 KiB block), `busy` and `now_us`. A program or
an erase only starts; `busy` reports its end, so the store never spins on the
media in service.

- [`plat/nvm_flash_litespi.c`](plat/nvm_flash_litespi.c) is the on-chip
  implementation, ported from the shipping writer's access code: reads
  through the memory-mapped QSPI window; write enable, page program, sector
  erase and status through the LiteSPI command master; time from the fabric
  PHC. It refuses a program or erase outside the reserved journal, and its
  time never steps backwards.
- [`host/nvm_fmodel.c`](host/nvm_fmodel.c) is the host flash model. It can
  cut the power inside any erase or page program, leaving the edge cells half
  way. It can also hang or fail an erase or a program, flip a programmed bit,
  fail a read, flip a bit a read returns, or flip a bit at rest. It refuses
  and counts a program that crosses a page or arrives while the device is
  busy, a write outside the journal, and a write into the authoritative slot.

**The seam with F0.** F0's HAL (`sw/firmware/ctrl/mbx/mbx_hal.h` on its own
lane, not merged) carries the mailbox's bus port; this port carries the media.
The two meet in time, which both need: here `now_us` reads the PHC as the
shipping writer does. When F0's time call lands, the LiteSPI port's `now_us`
becomes a call to it, and nothing above the port changes. The event loop F0
owns calls `nvm_store_service()` once per pass and `nvm_store_changed()` from
the protocol adapters.

## Boot

`nvm_store_boot()` runs before the event loop, with the entity model loaded:

1. An unproven model ends **CLOSED**: nothing is judged, AECP is never
   released and no writer runs (D3 section 8.1 step 6).
2. Both slots are judged by the section 6.2 order, including the
   erased-record rule. The CRC-32 is streamed through the stage, so a slot of
   any `IMG_LEN` is judged without a buffer of its size. The verdicts equal
   `scripts/nvm_klj2.py`'s `klj2_decode` for the same bytes. One difference
   from the shipping writer: a framed record whose length runs past the
   record area is `VD_LEN` here, as in `klj2_decode`; the shipping writer
   says `VD_REC`.
3. The newer accepted slot (the wrap-safe compare of section 7) is read into
   the stage again and judged again in RAM; only those bytes are applied. A
   slot that does not read back as it was judged gives way to the other.
4. The restore is one transaction, the D3 section 8.6 rule. Every record in
   ascending id goes through the state port's `apply`; a value its rule
   refuses keeps its image default and the walk goes on. An erased record
   applies nothing. `settle` runs once, after the maps and before the names:
   it judges the restored formats against the final maps (section 8.4).
   #658's restore clip, the identity default clipped to a restored narrower
   format, lands in that step ([ruling](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5988843004)
   item 3); the store does not depend on it. A value that cannot be judged
   aborts the restore and `rollback` puts every value back to its image
   default: **DEFAULTS**. A roll-back that fails is **CLOSED**.
5. AECP is released once, at **COMPLETE**, **BLANK** (no slot accepted) or
   **DEFAULTS**.

## Write-back

An accepted command that changes a persisted value calls
`nvm_store_changed()`. Each `nvm_store_service()` call then does one bounded
step:

| Phase | One step |
|---|---|
| idle | after the 1,000 ms first-dirty window (DR2a) and any backoff, start a capture |
| capture | latch ONE dirty record from its owner, compare it, frame it into the stage |
| seal | the header at the next sequence, then 256 bytes of CRC-32 per step |
| erase | start the erase of the slot that is NOT authoritative |
| erase wait, blank check | poll once; then read back 256 bytes per step, all `0xFF` |
| program, program wait | one page, in ascending order: the header page first, the trailer last |
| verify | read back 256 bytes per step and compare with the stage |

The atomicity rules, from section 7 and the D3 register:

- **The authoritative slot is never erased or programmed.** At every instant
  of a commit one slot holds a complete container whose CRC closes.
- **The trailer is the commit mark.** A container is accepted only once its
  last page closes the CRC, and the authority moves only on a verified read
  back. A power cut at any step boots the old values or the new ones, never a
  mix.
- **DR2c.** A failed attempt names its stage (`VD_ERASE`, `VD_PROGRAM`,
  `VD_VERIFY`), returns its records to dirty and marks the claim stale. An
  unchanged work set gets at most three attempts, the first included, each
  1,000 ms after the last failure; a new change starts a new work set.
- **DR2b.** A capture that changed no staged byte of a VERIFIED container is
  not written. After a failed attempt the stage is not verified, so the retry
  is written.
- **DR5.** With no slot accepted, a blank slot takes the first commit before
  a refused one, so a refused image is not erased merely for being refused.

**The service bound.** No step touches more than `max(256, 2 x P + 6)` bytes,
where P is the shape's largest payload: one latched record's copy and crc16,
or one 256-byte stretch. That is 278 bytes at 1x1 and 1,158 at 8x8. No call
holds the loop longer than one 256-byte transfer on the 1x link. The parent
pins the capture at 24.5 ms at 8x8 (`scripts/check_nvm_capture.py`), for a
capture that copies the whole 13,210-byte record set. Here a capture holds
the loop for one record per step. At the receipt's measured rate of 1.05 us
per captured byte (13.86 ms for 13,210 bytes at 8x8 and 50 MHz), the longest
step is about 1.2 ms. That figure is DERIVED, not measured on the CPU
harness.

## Static sizes

The RV32I freestanding build (`-march=rv32i -Os`) of the codec, the store,
the helper and the LiteSPI port, per shipped shape, in bytes. The stage is
the container plus one record header; the payload buffer is the shape's
largest payload; the chunk is one read-back step.

| Shape | Records | Container | Stage | Payload | Chunk | Store state | bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 42 | 2,516 | 2,524 | 66 | 256 | 256 | 3,112 | 10,348 |
| `endstation_ax7101_1x1_tdm8` | 54 | 3,336 | 3,344 | 136 | 256 | 256 | 4,000 | 10,364 |
| `endstation_arty_4x4` | 88 | 4,808 | 4,816 | 66 | 256 | 256 | 5,404 | 10,356 |
| `endstation_arty_8ch` | 120 | 7,368 | 7,376 | 66 | 256 | 256 | 7,964 | 10,356 |
| `endstation_ax7101_8x8` | 164 | 13,256 | 13,264 | 576 | 256 | 256 | 14,360 | 10,368 |

#640 D4 removes DDR3, so the stage lives in block RAM: one container, not the
64 KiB slot. The shipping writer keeps a live window and a private stage in
DDR3. Here the live values stay with their owners and are latched when they
are saved, so there is one buffer. The record table is walked, not stored.

## The host suite

[`test/test_ctrl_nvm.py`](test/test_ctrl_nvm.py) builds the store per shipped
shape against the constants `sw/litex/milan_soc.py` publishes for the shipping
writer. It runs [`test/nvm_test.c`](test/nvm_test.c) over the flash model
directly and over the LiteSPI port on the command-master model. Every byte
and every verdict is compared with `scripts/nvm_klj2.py`.

- **Boot** ([`test/nvm_checks.py`](test/nvm_checks.py)): blank, golden and
  erased-record slots; newer wins, including across the sequence wrap; a torn
  newer slot, two torn slots, a wrong major version; verdict parity over the
  shipping suite's refusal table plus three more; a bit flipped on the
  re-stage; apply, settle and roll-back faults; an unproven model; refused
  values.
- **Write-back** ([`test/nvm_checks_write.py`](test/nvm_checks_write.py)): the
  first commit and a change commit byte for byte; the debounce; DR2b both
  ways; five media failures and the recovery; DR5; the service bound through
  a 3 s erase; the port guard.
- **Power loss.** `--powercut` cuts the power inside every media effect of a
  commit, at 0, 1/256, 1/2 and 255/256 of it, and during the read-back. It
  starts from blank media, one slot and two slots. Every case boots the old
  values, or the new ones only when the new container is whole, and the next
  change commits.
- **The round trip.** Given the records of the recorded vectors
  [`records_endstation_ax7101_1x1_tdm8.txt`](../../../tb/verilator/nvm_backend/records_endstation_ax7101_1x1_tdm8.txt)
  and its 8x8 twin, the store commits the container `tb/verilator/nvm_backend`
  grades the RTL against: its length, its CRC-32 and every record's offset. It
  then boots the same values back.
- **The RV32 arm** cross-compiles freestanding and fails on any undefined
  symbol other than a C-library memory function or a libgcc helper.

`--self-test` plants every defect of [`test/nvm_mutants.py`](test/nvm_mutants.py),
one per copy, and requires each check it names to fail; every check is named
by at least one.

## What this does not prove

- The board: the real LiteSPI timing, a real power cut, the real N25Q128.
- The LiteX-generated headers: the RV32 arm compiles against MMIO stand-ins
  (`test/rv32/`), and the host suite against models of the command master.
- The #665 switch and its link: F0's switch is not merged, so no image links
  this store, and the capture time on the CPU is derived, not measured.
- The owners: the state model stands in for the AECP, ACMP and map stores of
  F3 and F5.
