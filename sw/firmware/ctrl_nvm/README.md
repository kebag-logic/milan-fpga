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
- **[The flash port](#the-flash-port)** -- Five calls, two implementations, a local time base, bounded waits, and the seam with F0's mailbox HAL.
- **[Boot](#boot)** -- Each slot judged on one read, the newer one staged, re-judged and applied in two walks.
- **[Write-back](#write-back)** -- One bounded step per service call: capture, seal, erase, blank check, program, read back.
- **[The service bound](#the-service-bound)** -- What one step can cost, what is asserted, what is derived, and on what assumptions.
- **[Static sizes](#static-sizes)** -- What each shipped shape costs, measured on the RV32I build.
- **[The host suite](#the-host-suite)** -- Thirty-seven checks per shape, 29 of them on both ports, the power-cut sweep and the planted defects.
- **[What this does not prove](#what-this-does-not-prove)** -- The board, the generated headers and the switch.

## Layout

| Path | What it holds |
|---|---|
| [`nvm_shape.h`](nvm_shape.h) | the record set and the container sizes, derived from the generated `MILAN_NVM_*` constants |
| [`nvm_klj2.c`](nvm_klj2.c) | the KLJ2 container and F07.8 record codec, and the section 6.2 acceptance order |
| [`nvm_flash.h`](nvm_flash.h) | the flash port |
| [`nvm_state.h`](nvm_state.h) | the state port: where a saved value is applied and a changed one latched |
| [`nvm_store.c`](nvm_store.c) | the boot restore and the write-back |
| [`plat/`](plat) | the LiteSPI flash port and the target's constants header |
| [`host/`](host) | the flash model with its faults, the LiteSPI command-master model, the state model |
| [`test/`](test) | the scenario runner, the checks, the planted defects and the RV32 arm |

## The flash port

[`nvm_flash.h`](nvm_flash.h) is the whole media face: `read`, `program` (one
page at most), `erase` (one 64 KiB block), `busy` and `now_us`. A program or
an erase only starts; `busy` reports its end, so the store never spins on the
media in service. Every call returns in bounded time.

- [`plat/nvm_flash_litespi.c`](plat/nvm_flash_litespi.c) is the on-chip
  implementation, ported from the shipping writer's access code: reads
  through the memory-mapped QSPI window; write enable, page program, sector
  erase and status through the LiteSPI command master. It refuses a program
  or erase outside the reserved journal.
- [`host/nvm_fmodel.c`](host/nvm_fmodel.c) is the host flash model. It can
  cut the power inside any erase or page program, leaving the edge cells half
  way. It can also hang, refuse or fail an erase or a program, flip a
  programmed bit, fail a read, flip a bit a read returns (anywhere, or in one
  chosen byte), answer a read from the neighbouring block, or flip a bit at
  rest. It refuses and counts a program that crosses a page or arrives while
  the device is busy, a write outside the journal, and a write into the
  authoritative slot.

**Time is a local counter, never the PHC.** The debounce window, the
backoff and the media deadlines need elapsed time. A gPTP step moves the PHC
either way, by any amount: a grandmaster restart moves it back by the old
grandmaster's uptime. So `now_us` must come from a counter that only counts
up. The LiteSPI port owns LiteX `timer0`: free-running down from
`0xffffffff` at the system clock (`CONFIG_CLOCK_FREQUENCY`, 100 MHz), its
32-bit difference accumulated into 64 bits at every read. Two obligations
follow for the image that links it:

- `nvm_flash_litespi_power_on()` starts the counter, once, before
  `nvm_store_boot()`, and nothing else reprograms `timer0`;
- the counter wraps every 2^32 clocks (42.9 s at 100 MHz), so it must be read
  at least that often. The store reads it on every `nvm_store_service()`
  call, so an event loop that calls the service at least once per 42.9 s
  keeps every elapsed time exact. A longer stall loses whole wraps and
  delays a deadline; it never brings one forward.

**Every wait on the command master is bounded.** `ls_open` drains the
receive side, and `ls_xfer` waits for TX and then RX readiness. Each wait
gives up after `LS_POLL_MAX` = 4,096 status reads without the readiness it
waits for. The call then releases chip select and fails, and the store fails
that attempt under the step's verdict (`VD_PROGRAM` for a program, `VD_ERASE`
for an erase or a status poll). The bound counts reads without progress, the
rule of D3 section 8.8, so a master that is slow but moving never trips it.
A command cut short reaches at most the slot being written, which is never
the authoritative one, and the next attempt erases that slot first.

**The seam with F0.** F0's HAL (`sw/firmware/ctrl/mbx/mbx_hal.h` on its own
lane, not merged) carries the mailbox's bus port; this port carries the media.
The two meet in time, which both need. Whichever time call the split image
settles on must keep this port's contract: a local counter that only counts
up, never the PHC. The event loop F0 owns calls `nvm_store_service()` once
per pass and `nvm_store_changed()` from the protocol adapters.

## Boot

`nvm_store_boot()` runs before the event loop, with the entity model loaded:

1. An unproven model ends **CLOSED**: nothing is judged, AECP is never
   released and no writer runs (D3 section 8.1 step 6).
2. Each slot is read into the stage in ONE read and judged there by the
   section 6.2 order, including the erased-record rule. Its CRC, its records
   and the sequence the pick uses all come from the same bytes. The verdicts
   equal `scripts/nvm_klj2.py`'s `klj2_decode` for the same bytes. A
   container longer than the stage can never be this shape's; its CRC is
   streamed only to name the refusal in the 6.2 order. One difference from
   the shipping writer: a framed record whose length runs past the record
   area is `VD_LEN` here, as in `klj2_decode`, where the shipping writer says
   `VD_REC`.
3. The newer accepted slot is picked by the wrap-safe compare of section 7.
   On equal sequences slot A is picked, as in the shipping writer. It is
   then read into the stage again and judged again, CRC included. Its
   sequence must be the one it was picked by, and only those bytes are
   applied and published. A slot that does not read back as it was judged
   gives way to the other.
4. **The binding walk** runs first (D3 section 8.1 step 4). Every binding
   record goes through the state port's `apply`, in ascending id. It is its
   own unit: a binding whose rule cannot be judged fails the walk whole, and
   `rollback(NVM_W_BIND)` drops every binding it preloaded. The D3 walk runs
   either way. A walk whose preloads cannot be dropped leaves the listener
   unproven and ends **CLOSED**.
5. **The D3 walk** restores every other record as one transaction (section
   8.6), in ascending id. A value its rule refuses keeps its image default
   and the walk goes on, and an erased record applies nothing. `settle` runs
   once, after the maps and before the names: it judges the restored formats
   against the final maps (section 8.4). #658's restore clip, the identity
   default clipped to a restored narrower format, lands in that step
   ([ruling](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5988843004)
   item 3); the store does not depend on it. A value that cannot be judged
   aborts the walk, and `rollback(NVM_W_D3)` puts every D3 value back to its
   image default: **DEFAULTS**. The bindings stay applied, because a D3
   roll-back's owners are the two stores and the map plane, never the
   listener. A roll-back that fails is **CLOSED**.
6. AECP is released once, at the D3 walk's **COMPLETE** or **DEFAULTS**, or
   at **BLANK** (no slot accepted).

## Write-back

An accepted command that changes a persisted value calls
`nvm_store_changed()`, which only marks the record. Each
`nvm_store_service()` call then does one bounded step:

| Phase | One step |
|---|---|
| idle | after the 1,000 ms first-dirty window (DR2a) and any backoff, start a capture; or retry a failed work set |
| capture | latch ONE dirty record from its owner, compare it, frame it into the stage |
| seal | decide (DR2b, DR2c below); then the header at the next sequence, then 256 bytes of CRC-32 per step |
| erase | start the erase of the slot that is NOT authoritative |
| erase wait, blank check | poll once; then read back 256 bytes per step, all `0xFF` |
| program, program wait | one page, in ascending order: the header page first, the trailer last |
| verify | read back 256 bytes per step and compare with the stage |

The atomicity rules, from section 7 and the D3 register:

- **The authoritative slot is never erased or programmed.** At every instant
  of a commit one slot holds a complete container whose CRC closes.
- **The trailer is the commit mark.** A container is accepted only once its
  last page closes the CRC, and the authority moves only on a read-back that
  covered the whole container. A power cut at any step boots the old values
  or the new ones, never a mix.
- **DR2a.** The window opens at the first change still waiting for a
  capture. A change the running capture has yet to reach is taken by that
  capture and opens no window; a change it has passed opens its own.
- **DR2c.** A failed attempt names its step (`VD_ERASE`, `VD_PROGRAM`,
  `VD_VERIFY`), keeps its records in flight and marks the claim stale. The
  captured work set gets three attempts in all, the first included. Each
  attempt waits 1,000 ms after the failed one, the console's
  `nvm_store_commit_now()` too. A capture that changes no staged byte
  continues the same work set: a change call that leaves the value as it
  was buys no new attempt, and neither does the console. A capture that
  changes a staged byte is a new work set with three attempts of its own.
- **The exhaustion record.** A work set's third failure abandons it. The
  status keeps `abandoned` (how many sets were abandoned) and `abandoned_vd`
  (the last one's first failure) until reset, and no later success clears
  them. `stale` follows FASTCONNECT section 9.2 instead: it clears when a
  later commit leaves nothing changed outside a verified slot. Section 9.2
  and D3 section 6.3 rule that firmware exhaustion has no reset-sticky alarm
  of its own, and that `nvm_alarm` is the producers' alone. So the record is
  this store's status, not a `PP_STAT` bit.
- **DR2b.** A capture that changed no staged byte of a VERIFIED container is
  not written. After a failed attempt the stage is not verified, so the retry
  is written.
- **DR5.** With no slot accepted, a blank slot takes the first commit before
  a refused one, so a refused image is not erased merely for being refused.

## The service bound

Three statements, each with what it rests on:

- **Bytes, asserted.** No step touches more than `max(256, 2 x P + 6)` bytes,
  where P is the shape's largest payload: one 256-byte stretch, or one
  latched record's copy and its crc16. That is 278 bytes at 1x1 and 1,158 at
  8x8. `service_bound` asserts the figure exactly per shape. It counts
  payload and CRC bytes only. It leaves out the owner's own `latch()` work,
  the walk to the next dirty record (at most one pass over the shape's
  records), and the CPU cost of a byte, which differs between a copy, a
  compare and a nibble-table crc16.
- **Model time, asserted.** Every run of the suite holds every service call
  under 1,000 us of MODEL time. Model time is what the host models charge,
  and CPU work costs none of it:
  - each byte on the 1x 12.5 MHz link costs 0.64 us;
  - each CSR access to the command master costs 40 ns;
  - a stalled wait costs its 4,096 reads, 164 us, before the call gives up.

  The longest call in the bound run is at most 168 us on the model port and
  210 us on LiteSPI, at 1x1 and at 8x8. A dead master's calls are 164 us.
- **CPU time, DERIVED, not measured.** This store is in no image, so nothing
  measured its steps on the CPU. Two figures follow from stated assumptions:
  - the longest store step is the capture of the largest record. At the
    capture receipt's measured 1.05 us per captured byte
    (`tb/verilator/nvm_capture_cpu/measurements.json`: the shipping writer's
    copy of 13,210 bytes at 8x8 and 50 MHz in 13.86 ms), 1,158 bytes cost
    about 1.2 ms. That assumes this store's copy, compare and crc16 run at
    the shipping copy loop's rate. They do more work per byte, so the figure
    is a floor, not a ceiling;
  - the longest port call is a page program of 262 bytes. Each byte costs
    the link's 0.64 us plus four or more CSR accesses. A stalled wait adds
    its 4,096 reads; at an assumed 0.5 us per CSR read on the CPU's bus,
    that is at most 2 ms.

  Both sit well inside the 24.5 ms the parent pins for the shipping
  writer's capture (`scripts/check_nvm_capture.py`), which holds producers
  for the whole record set in one step. Turning either figure into a
  measured bound needs the store linked into an image behind F0's switch.

## Static sizes

The RV32I freestanding build (`-march=rv32i -Os`) of the codec, the store
and the LiteSPI port, per shipped shape, in bytes. The stage is the
container plus one record header; the payload buffer is the shape's largest
payload; the chunk is one read-back step; the clock is the port's two
counters. bss includes alignment.

| Shape | Records | Container | Stage | Payload | Chunk | Store state | Clock | bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 42 | 2,516 | 2,524 | 66 | 256 | 280 | 12 | 3,144 | 10,981 |
| `endstation_ax7101_1x1_tdm8` | 54 | 3,336 | 3,344 | 136 | 256 | 280 | 12 | 4,032 | 10,997 |
| `endstation_arty_4x4` | 88 | 4,808 | 4,816 | 66 | 256 | 280 | 12 | 5,436 | 10,989 |
| `endstation_arty_8ch` | 120 | 7,368 | 7,376 | 66 | 256 | 280 | 12 | 7,996 | 10,989 |
| `endstation_ax7101_8x8` | 164 | 13,256 | 13,264 | 576 | 256 | 280 | 12 | 14,392 | 11,001 |

#640 D4 removes DDR3, so the stage lives in block RAM: one container, not the
64 KiB slot. The shipping writer keeps a live window and a private stage in
DDR3. Here the live values stay with their owners and are latched when they
are saved, so there is one buffer. The record table is walked, not stored.

## The host suite

[`test/test_ctrl_nvm.py`](test/test_ctrl_nvm.py) builds the store per shipped
shape against the constants `sw/litex/milan_soc.py` publishes for the shipping
writer. It runs [`test/nvm_test.c`](test/nvm_test.c) over the flash model
directly and over the LiteSPI port on the command-master model. Every byte
and every verdict is compared with `scripts/nvm_klj2.py`. Thirty-seven checks
per shape: 29 on both ports, five on the model port alone (its read and
refusal faults do not reach memory-mapped LiteSPI reads), and three on the
LiteSPI port alone (the PHC, `timer0`, the command master and the guard
exist only there).

- **Boot** ([`test/nvm_checks.py`](test/nvm_checks.py)):
  - blank, golden and erased-record slots;
  - newer wins, across the sequence wrap and on a tie;
  - a torn newer slot, two torn slots, a wrong major version;
  - verdict parity over the shipping suite's refusal table plus three more;
  - read faults: a flipped bit on the re-stage; a flipped sequence bit on
    every boot read of either slot, across the wrap; an aliased re-stage
    read; failed reads;
  - the two walks: a D3 apply or settle fault that rolls back and leaves the
    bindings applied, and a binding fault that fails only the binding walk;
  - roll-back faults, an unproven model, and refused values.
- **Write-back** ([`test/nvm_checks_write.py`](test/nvm_checks_write.py)):
  - the first commit and a change commit, byte for byte;
  - the debounce, with changes before, during and after a capture;
  - DR2b both ways;
  - five media failures and the recovery;
  - DR2c for an unchanged set held across 13 change calls and the medium
    healing, and for the console inside the backoff and after exhaustion;
  - a dropped last page and a last byte left programmed;
  - each failure named by its own step;
  - DR5;
  - the time base under PHC steps of 60 s either way in the window, the
    backoff, an erase and a program, and across the counter's wrap;
  - a command master slow by 4,000 reads a wait, stalled on TX, RX or the
    drain, and dead;
  - the service bound through a 3 s erase, and the port guard.
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
- The CPU time of a step: it is derived above, not measured.
- The LiteX-generated headers: the RV32 arm compiles against MMIO stand-ins
  (`test/rv32/`), and the host suite against models of the command master and
  `timer0`.
- The #665 switch and its link: F0's switch is not merged, so no image links
  this store.
- The owners: the state model stands in for the AECP, ACMP and map stores of
  F3 and F5.
