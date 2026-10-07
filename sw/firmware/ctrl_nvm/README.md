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
is the gate. Exit 0 means every check passed on every shipped shape, each
built at its own system clock, on both flash ports, and every planted defect
was caught.

The [split verification contract](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#6-verification-boundary)
requires FT before F2 to F5.
FT ports these checks to GoogleTest/GoogleMock and adds coverage gates.
Existing mutation arms remain required.
The [service budget](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)
is an integration obligation, not a target-time result established here.

## Contents

- **[Layout](#layout)** -- The codec, the store, the two ports, the host models and the suite.
- **[The flash port](#the-flash-port)** -- Five calls, two implementations, a local time base, bounded waits and calls, and the seam with F0's mailbox HAL.
- **[Boot](#boot)** -- Each slot judged on as few as one read, the newer one staged, re-judged and applied in two walks, and the writer held while a slot is unread.
- **[Write-back](#write-back)** -- One bounded step per service call: capture, seal, erase, blank check, program, read back.
- **[The service bound](#the-service-bound)** -- What one step can cost, what is asserted, what is derived, and on what assumptions.
- **[Static sizes](#static-sizes)** -- What each shipped shape costs, measured on the RV32I build.
- **[The host suite](#the-host-suite)** -- Forty-two checks per shape at its own clock, 29 of them on both ports, the power-cut sweep and the planted defects.
- **[What this does not prove](#what-this-does-not-prove)** -- The board, the generated headers, the switch, and a read fault that repeats itself exactly.

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
media in service. Every call returns in bounded time. A `read` that fails is
a media fault, never a verdict on the bytes.

- [`plat/nvm_flash_litespi.c`](plat/nvm_flash_litespi.c) is the on-chip
  implementation, ported from the shipping writer's access code: reads
  through the memory-mapped QSPI window; write enable, page program, sector
  erase and status through the LiteSPI command master. It refuses a program
  or erase outside the reserved journal.
- [`host/nvm_fmodel.c`](host/nvm_fmodel.c) is the host flash model. It can
  cut the power inside any erase or page program, leaving the edge cells half
  way. It can also hang, refuse or fail an erase or a program, flip a
  programmed bit, fail a read (any read, or the reads covering one chosen
  address), flip a bit a read returns (anywhere, or in one chosen byte),
  return one chosen byte wrong in a different way on each read (XOR 8, then
  16, then 32), answer a read from the neighbouring block, or flip a bit at
  rest. It refuses and counts a program that crosses a page or arrives while
  the device is busy, a write outside the journal, and a write into the
  authoritative slot.

**Time is a local counter, never the PHC.** The debounce window, the
backoff and the media deadlines need elapsed time. A gPTP step moves the PHC
either way, by any amount: a grandmaster restart moves it back by the old
grandmaster's uptime. So `now_us` must come from a counter that only counts
up. The LiteSPI port owns LiteX `timer0`: free-running down from
`0xffffffff` at the system clock, its 32-bit difference accumulated into 64
bits at every read. The system clock is `CONFIG_CLOCK_FREQUENCY`, which LiteX
writes from the shape's `sys_clk_hz`: 83,333,000 Hz on the three Arty shapes
and 100 MHz on the two AX7101 ones. Clocks become microseconds exactly at any
clock, whole MHz or not. The port takes whole seconds first, then multiplies
the remainder by 10^6 in 64 bits, so there is no whole number of clocks per
microsecond. Two obligations follow for the image that links it:

- `nvm_flash_litespi_power_on()` starts the counter, once, before
  `nvm_store_boot()`, and nothing else reprograms `timer0`;
- the counter wraps every 2^32 clocks, so it must be read at least that
  often: every 42.9 s at 100 MHz and every 51.5 s at 83.333 MHz. The store
  reads it on every `nvm_store_service()` call. An event loop that calls the
  service at least once per wrap of its shape's clock therefore keeps every
  elapsed time exact. A longer stall loses whole wraps and delays a
  deadline; it never brings one forward.

**Every wait on the command master is bounded, and so is every call.**
`ls_open` drains the receive side, and `ls_xfer` waits for TX and then RX
readiness. Two limits end a wait:

- **Per wait.** `LS_POLL_MAX` = 4,096 status reads without the readiness it
  waits for. This counts reads without progress, the rule of D3 section 8.8.
- **Per call.** A master that is slow but moving keeps every wait under
  4,096 reads, and a page program makes 522 waits and two drains. So a call
  that is still waiting on the master once it has run `LS_CALL_US` = 2,000
  us of `timer0` time since it began fails too. That is twelve times the
  167 us a page program's 261 bytes take on the 1x link. In clocks the
  deadline is `nvm_flash_litespi_call_ticks`, computed in 64 bits:
  166,666 at 83.333 MHz and 200,000 at 100 MHz. The port reads `timer0` when
  the call begins, and then once every `LS_LATE_EVERY` = 64 status reads
  that find the master not ready, counted over the whole call. So a master
  that shows readiness at every first status read, as the host model does,
  costs one timer read; on chip, each byte's link time makes some RX status
  reads find it not ready, so a healthy call reads `timer0` about once per
  64 of those. A master that stops being slow just before the deadline lets
  the call finish at the ready pace.

Either way the call releases chip select and fails, and the store fails that
attempt under the step's verdict: `VD_PROGRAM` for a program, `VD_ERASE` for
an erase or a status poll. A command cut short reaches at most the slot being
written, which is never the authoritative one, and the next attempt erases
that slot first.

**The seam with F0.** F0's merged HAL (`sw/firmware/ctrl/mbx/mbx_hal.h`) carries the mailbox's bus port; this port carries the media.
The two meet in time, which both need. Whichever time call the split image
settles on must keep this port's contract: a local counter that only counts
up, never the PHC. The event loop F0 owns calls `nvm_store_service()` once
per pass and `nvm_store_changed()` from the protocol adapters.

## Boot

`nvm_store_boot()` runs before the event loop, with the entity model loaded:

1. A record walk that disagrees with the build turns persistence off: no
   slot is read, and the entity runs on its defaults (**DEFAULTS**, DR3b),
   or **CLOSED** if its model is unproven too.
2. Each judgement of a slot reads it into the stage in ONE read and judges
   it there by the section 6.2 order, including the erased-record rule. Its
   CRC, its records
   and the sequence the pick uses all come from the same bytes. The verdicts
   equal `scripts/nvm_klj2.py`'s `klj2_decode` for the same bytes. A
   container longer than the stage can never be this shape's; its CRC is
   streamed only to name the refusal in the 6.2 order. One difference from
   the shipping writer: a framed record whose length runs past the record
   area is `VD_LEN` here, as in `klj2_decode`, where the shipping writer says
   `VD_REC`.
3. **A slot's verdict stands on at most `NVM_READ_TRIES` = 3 reads.** An OK
   verdict stands on one read, because its CRC-32 covers every byte, the
   sequence included. Any other verdict, BLANK included, stands only when
   two reads return the same bytes
   ([#665 round 4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999350068)).
   Each read keeps a CRC-32 digest over every byte the port delivered for
   it, with their count. That is the 40 header bytes for a verdict the
   header decides (blank, magic, version, length), and the header plus the
   whole container otherwise. Two reads agree when their verdicts, counts
   and digests are all equal. Two reads whose bytes differ are a media
   fault, however alike their verdicts: the fault is counted in
   `read_faults` and the slot is read again, so a clean read inside the
   bound is judged and applied. A read the port fails is a media fault too,
   and is not a verdict at all. A slot that gives no standing verdict within
   three reads is **UNREAD**: its verdict is `VD_LEN` (rule 4, it did not
   deliver its bytes), its bit is set in the status field `unread`, and no
   sequence is taken from it. Why a refusal needs a second read of the same
   bytes: a read that went wrong without the port saying so looks like a
   refusal or like a blank slot, and two different wrong reads can look
   like the same refusal. Either one would let the next commit restart the
   sequence below a container that survives it, which a later clean boot
   then prefers.
4. The newer accepted slot is picked by the wrap-safe compare of section 7,
   `(int32_t)(A.seq - B.seq) >= 0`. On equal sequences slot A is picked
   ([#665 decision 1](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153),
   as in the shipping writer). It is then read into the stage again and
   judged again, CRC included. Its sequence must be the one it was picked
   by, and only those bytes are applied and published. A re-stage that
   fails, or reads other bytes, is a media fault and is tried again, three
   re-stages in all. A slot that never reads back as it was judged is
   UNREAD, and the other slot is offered and re-staged the same way.
5. **The binding walk** runs first (D3 section 8.1 steps 4 and 5). Every
   binding record goes through the state port's `apply`, in ascending id. It
   is its own unit: a binding whose rule cannot be judged fails the walk
   whole, and `rollback(NVM_W_BIND)` drops every binding it preloaded. The D3
   walk runs either way. A walk whose preloads cannot be dropped leaves the
   listener unproven and ends **CLOSED**.
6. **The model check** (D3 section 8.1 step 6). The binding walk needs no
   entity model, so it ran already. An unproven model ends the restore **CLOSED**: nothing of
   the D3 walk is applied, AECP is never released and no writer runs. The
   bindings stay, because CLOSED "does not take the listener's faces back"
   (section 8.1). Blank media with an unproven model is CLOSED too.
7. **The D3 walk** restores every other record as one transaction (section
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
8. AECP is released once, at the D3 walk's **COMPLETE** or **DEFAULTS**, or
   at **BLANK** (no slot accepted).
9. **An UNREAD slot holds the writer**
   ([#665 decision 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153)).
   A slot refused by a media read fault, unlike a cleanly read invalid one,
   leaves the authority unknown: it may hold a newer container than any slot
   that was read. So the restore still applies what was accepted (section 7
   offers the other slot), but the write path enters **HELD** until reset.
   While HELD, a change is marked and reported in `dirty`, nothing is
   captured, erased or written, and `nvm_store_commit_now()` is refused. The
   read retry is bounded at boot. The next reset's boot reads the slot again,
   and a clean read ends the hold. A slot that never reads cleanly, because
   of a permanent read fault or because its reads differ on every boot,
   therefore holds the writer on every boot. The device serves and reports
   the hold, but nothing persists until a boot reads every slot cleanly.

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
| held | nothing, until reset: a slot is UNREAD (Boot, item 9) |

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
  them. `stale` follows FASTCONNECT section 9.2 instead: it clears once
  nothing changed is left outside a verified slot. That is checked at a
  verified commit, and also when DR2b finds that the verified container
  already holds every value a capture took. Section 9.2
  and D3 section 6.3 rule that firmware exhaustion has no reset-sticky alarm
  of its own, and that `nvm_alarm` is the producers' alone. So the record is
  this store's status, not a `PP_STAT` bit.
- **DR2b.** A capture that changed no staged byte of a VERIFIED container is
  not written. After a failed attempt the stage is not verified, so the retry
  is written.
- **DR5.** With no slot accepted, a blank slot takes the first commit before
  a refused one, so a refused image is not erased merely for being refused.

## The service bound

Four statements, each with what it rests on. MODEL time is what the host
models charge: each byte on the 1x 12.5 MHz link costs 0.64 us, each CSR
access to the command master costs 40 ns, and CPU work costs none of it.

- **Bytes, asserted.** No step touches more than `max(256, 2 x P + 6)` bytes,
  where P is the shape's largest payload: one 256-byte stretch, or one
  latched record's copy and its crc16. That is 278 bytes at 1x1 and 1,158 at
  8x8. `service_bound` asserts the figure exactly per shape. It counts
  payload and CRC bytes only. It leaves out the owner's own `latch()` work,
  the walk to the next dirty record (at most one pass over the shape's
  records), and the CPU cost of a byte, which differs between a copy, a
  compare and a nibble-table crc16.
- **Nominal calls, asserted and measured in model time.** Every run with no
  command-master stall armed holds every service call under
  `NOMINAL_CALL_US` = 250 us. That figure is a page program's link time,
  (5 + 256) x 0.64 us = 167 us, plus its 1,050-odd command-master accesses,
  42 us, with room for the few around them. Measured over every such run of
  the suite, at every shape: the longest call is 168 us on the model port
  and 210 us on LiteSPI.
- **The cumulative bound for a slow or stalled master, asserted in model
  time.** Every run, stalled or not, holds every service call under
  `CALL_BOUND_US` = 2,213 us. That is the sum of four terms:
  - the port's deadline, 2,000 us;
  - one check interval: 64 status reads and two timer reads at 40 ns, 3 us;
  - the rest of the call at the ready pace, when the master stops being slow
    just before the deadline: at most a page program's accesses, 42 us;
  - the link time of the window the call closes, which the model charges
    when chip select rises: at most 168 us.

  Measured at 1x1 and 8x8 (`port_stall`, `port_deadline`):

  | Master | Longest call | Outcome |
  |---|---:|---|
  | two TX or two RX waits of one page program slowed by 4,000 reads | 539 us | the commit completes |
  | two drains slowed by 4,000 reads | 859 us | the commit completes |
  | ten TX waits slowed by 4,000 reads | 1,859 us | the commit completes |
  | twelve TX waits slowed by 4,000 reads, the last ending just before the deadline | 2,189 us | the call finishes past the deadline at the ready pace; the commit completes |
  | every TX wait slowed by 4,000 reads, none reaching `LS_POLL_MAX` | 2,009 us | each page program fails at the deadline, three attempts, the set abandoned, the authority untouched |
  | TX stalled for good in one wait | 210 us | that call fails after 4,096 reads, 164 us; the retry commits |
  | a drain that never empties | 333 us | that call fails after 4,097 drain reads; the retry commits |
  | a master that never answers | 170 us | every call fails; three attempts, the loop running |

  Without the deadline, the every-wait case holds one call for 41,970 us of
  model time (the planted defect `call_deadline_ignored`).
- **CPU time, not measured.** This store is in no image, so nothing ran it on
  the CPU. What can be said:
  - a port call on chip is held to its own deadline, which is `timer0` time
    and so real time. A call still waiting on the master 2,000 us after it
    began fails within 64 more status reads, two timer reads and the
    chip-select release. One that stops waiting before then finishes at the
    ready pace, at most the rest of one page program. That holds whatever a
    CSR access costs, provided `timer0` runs as "The flash port" requires.
    If it does not run, only the per-wait limit is left, and each of a page
    program's 522 waits and two drains could take 4,096 reads;
  - the store's own work in one step is DERIVED, as a floor only. The
    longest is the capture of the largest record. At the capture receipt's
    measured 1.05 us per captured byte
    (`tb/verilator/nvm_capture_cpu/measurements.json`: the shipping writer's
    copy of 13,210 bytes at 8x8 and 50 MHz in 13.86 ms), 1,158 bytes cost
    about 1.2 ms. This store's copy, compare and crc16 do more work per
    byte than that copy loop, so the figure is a floor and no ceiling is
    claimed for it. Measuring it needs the store linked into an image behind
    F0's switch.

## Static sizes

RV32I object sizes, compiled with the pinned SDK at `-Os`.
Each shape uses its own system clock and ILP32 ABI.
Both builds disable compiler stack-protector instrumentation.
The largest static frame is 128 bytes per shape.
That figure does not bound the complete runtime stack.
See [the harness](../gtest/README.md#rv32-object-builds) for validation limits.
The stage is the container plus one record header; the payload buffer is the
shape's largest payload; the chunk is one read-back step; the clock counters
are the port's time base and its per-call deadline state. bss includes
alignment. A boot read's digest is three words on the stack per read, kept
only while the slot is judged.

| Shape | Clock (Hz) | Records | Container | Stage | Payload | Chunk | Store state | Clock counters | bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 83,333,000 | 42 | 2,516 | 2,524 | 66 | 256 | 288 | 20 | 3,160 | 12,116 |
| `endstation_ax7101_1x1_tdm8` | 100,000,000 | 54 | 3,336 | 3,344 | 136 | 256 | 288 | 20 | 4,048 | 12,132 |
| `endstation_arty_4x4` | 83,333,000 | 88 | 4,808 | 4,816 | 66 | 256 | 288 | 20 | 5,452 | 12,124 |
| `endstation_arty_8ch` | 83,333,000 | 120 | 7,368 | 7,376 | 66 | 256 | 288 | 20 | 8,012 | 12,124 |
| `endstation_ax7101_8x8` | 100,000,000 | 164 | 13,256 | 13,264 | 576 | 256 | 288 | 20 | 14,408 | 12,136 |

#640 D4 removes DDR3, so the stage lives in block RAM: one container, not the
64 KiB slot. The shipping writer keeps a live window and a private stage in
DDR3. Here the live values stay with their owners and are latched when they
are saved, so there is one buffer. The record table is walked, not stored.

## The host suite

[`test/test_ctrl_nvm.py`](test/test_ctrl_nvm.py) builds the store per shipped
shape against the constants `sw/litex/milan_soc.py` publishes for the shipping
writer. Each shape is built at its own system clock: the suite writes
`generated/soc.h` with `CONFIG_CLOCK_FREQUENCY` set to the config's
`sys_clk_hz`. It holds that figure to the `--sys-clk-freq` the builder hands
`milan_soc.py`, or to that option's 100 MHz default when the builder passes
none. The host build and the RV32 arm both read that header, and the model's
`timer0` counts at that clock. So the three Arty shapes are built and graded
at 83,333,000 Hz, and the two AX7101 shapes at 100 MHz. The suite is a set
of GoogleTest binaries ([the harness page](../gtest/README.md)) that run the
store in process, over the flash model directly and over the LiteSPI port on
the command-master model ([`test/nvm_rig.cpp`](test/nvm_rig.cpp)). Every
byte and every verdict is compared with the fixture
[`test/nvm_fixture.py`](test/nvm_fixture.py) writes from
`scripts/nvm_klj2.py`, the reference codec. Per shape, 53 checks in 85
tests: 32 on both ports, ten on the model port alone (its read and refusal
faults do not reach memory-mapped LiteSPI reads), five on the LiteSPI port
alone (the PHC, `timer0`, the command master and the guard exist only
there), four that ask the codec directly and two on GoogleMock's flash
port. The recorded vector's round trip runs on both ports at the two shapes
that have one. At the shipping 1x1 shape three more binaries run: two
builds against a doctored shape header, and the LiteSPI port alone on
GoogleMock's command master and `timer0`.

- **Boot** ([`test/test_nvm_boot.cpp`](test/test_nvm_boot.cpp)):
  - blank, golden and erased-record slots;
  - newer wins, across the sequence wrap, and on a tie, at the wrap too;
  - a torn newer slot, two torn slots, a wrong major version;
  - verdict parity over the shipping suite's refusal table plus three more;
  - read faults: a flipped bit on one re-stage and on every one; a flipped
    sequence bit on every boot read of either slot, across the wrap; an
    aliased re-stage, once and every time; failed reads at the bound and
    past it, of the header, the container and the re-stage; both re-stages
    flipped, the fallback's included;
  - the two walks: a D3 apply or settle fault that rolls back and leaves the
    bindings applied, and a binding fault that fails only the binding walk;
  - roll-back faults, an unproven model after the binding walk, and refused
    values.
- **Write-back** ([`test/test_nvm_write.cpp`](test/test_nvm_write.cpp)):
  - the first commit and a change commit, byte for byte;
  - the debounce, with changes before, during and after a capture, the one
    to the record the capture examines next included;
  - DR2b both ways;
  - five media failures and the recovery, `stale` healing after a DR2b
    suppression too;
  - DR2c for an unchanged set held across 13 change calls and the medium
    healing, and for the console inside the backoff and after exhaustion;
  - a dropped last page and a last byte left programmed;
  - each failure named by its own step;
  - DR5;
  - an unknown authority (decision 2): one valid slot and one blank, both
    ways round, at sequence 1, 5, 0x80000000 and 0xFFFFFFFF; failed reads
    past the bound hold the writer, and failed reads within it, a flipped
    bit or an aliased read do not; each case runs on through a clean
    reboot, a change, its commit and another clean reboot, and the restored
    values are compared;
  - reads that disagree (`read_disagreement`, R501-3's probe kept as a
    check). One valid slot and one blank, both ways round, at the same four
    sequences. The valid slot's first header byte, or its byte at offset
    0x100, reads XOR 8 and then XOR 16: two reads refuse it alike on
    different bytes. The third, clean read is applied, with one media fault
    counted, and a third wrong read (XOR 32) leaves the slot UNREAD and the
    writer held. Every case runs on as above, and no saved value is lost;
  - the time base under PHC steps of 60 s either way in the window, the
    backoff, an erase and a program, and across the counter's wrap at the
    shape's own clock;
  - the clock itself (`port_clock`). The runner is built at the config's
    clock, the deadline in clocks is `LS_CALL_US` of it (166,666 at
    83.333 MHz), and over 120 s the port's elapsed time matches the model's
    to 2 us;
  - a command master slowed in two waits, stalled on TX, RX or the drain,
    and dead; slowed in ten waits, in twelve and in every wait (the per-call
    deadline);
  - the service bound through a 3 s erase, and the port guard.
- **Power loss.** `--powercut` cuts the power inside every media effect of a
  commit, at 0, 1/256, 1/2 and 255/256 of it, and during the read-back. It
  starts from blank media, one slot and two slots. Every case boots the old
  values, or the new ones only when the new container is whole, and the next
  change commits.
- **Paths written for branch coverage** (#665 lane FT), each graded as the
  checks above are:
  - [`test/test_nvm_more.cpp`](test/test_nvm_more.cpp): a container
    longer than the stage, each of its reads failing once and its CRC not
    closing; a console commit of an unchanged container; the first commit
    with neither slot blank (DR5's other face); a change whose owner has
    nothing to save; a change to a record the shape does not have; and the
    capture's window edges (DR2a);
  - [`test/test_nvm_codec.cpp`](test/test_nvm_codec.cpp): the codec asked
    directly, every refusal of the parity table, the room a container is
    held in, a loaded prefix that ends before a record header or its
    payload (each guard pinned at its exact end), and the record lookups;
  - [`test/test_nvm_flashmock.cpp`](test/test_nvm_flashmock.cpp): two
    refusals of different verdicts, and two alike in verdict and CRC-32
    digest over different byte counts (a collision the test forges), are a
    media fault, on a flash port GoogleMock answers read by read;
  - [`test/test_nvm_shapes.cpp`](test/test_nvm_shapes.cpp): a shape whose
    record walk and sizes disagree disables persistence (DR3b), and a shape
    with no name record settles after its last record;
  - [`test/test_nvm_litespi.cpp`](test/test_nvm_litespi.cpp): the port's
    own refusals before the command master is touched, and a drain that ends
    on the call's deadline.
- **The round trip** ([`test/test_nvm_vector.cpp`](test/test_nvm_vector.cpp)).
  Given the records of the recorded vectors
  [`records_endstation_ax7101_1x1_tdm8.txt`](../../../tb/verilator/nvm_backend/records_endstation_ax7101_1x1_tdm8.txt)
  and its 8x8 twin, the store commits the container `tb/verilator/nvm_backend`
  grades the RTL against: its length, its CRC-32 and every record's offset. It
  then boots the same values back.
- **The RV32 arm** cross-compiles freestanding and fails on any undefined
  symbol other than a C-library memory function or a libgcc helper.

`--self-test` plants every defect of [`test/nvm_mutants.py`](test/nvm_mutants.py),
one per copy, and requires each check it names to fail; every check is named
by at least one (109 defects). They are graded at the 1x1 shape, except a defect that only
shows at a clock that is not a whole number of MHz. That one,
`ticks_per_us_truncated`, is graded at `endstation_arty_current`.

The host gate also runs exact-sized erased prefixes under AddressSanitizer.
`test_nvm_prefix.cpp` checks 40, 47 and 48 loaded bytes.
It pins both boundaries of the last erased payload.
The three related defects restore `end` or shift `loaded`.

## What this does not prove

- The board: the real LiteSPI timing, a real power cut, the real N25Q128.
- The CPU time of a step: it is derived above, not measured.
- A read fault that repeats itself exactly. Two reads of a slot that return
  the same bytes are taken as its content. A fault that corrupts a valid
  slot the same way on every boot read, without the port reporting it,
  therefore looks like a refusal. The next commit can then restart the
  sequence below that slot, and a later clean boot prefers it. No reading of
  the bytes can tell that from a slot that really is corrupt, and decision 2
  takes no sequence from an unvalidated slot.
- Two different reads that the digest calls the same. The digest is a
  CRC-32. It always tells apart two reads that differ in one or two bits,
  or only within 32 consecutive bits. Reads that differ in any other way
  are told apart except with a probability of about 2^-32.
- The LiteX-generated headers: the RV32 arm compiles against MMIO stand-ins
  for the CSR and memory maps (`test/rv32/`), and the host suite against
  models of the command master and `timer0`. Only the clock is each shape's
  own.
- The #665 switch and its link: F0's switch is not merged, so no image links
  this store.
- The owners: the state model stands in for the AECP and map stores of F5.
  The binding group's owner is F3's
  [`acmp_nvm.c`](../ctrl/acmp/acmp_nvm.c); its arm `acmpnvm` in
  [`../ctrl/test/`](../ctrl/test/) boots it from this store. No image links
  the two either.
