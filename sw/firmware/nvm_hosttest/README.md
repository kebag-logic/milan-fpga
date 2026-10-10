<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# nvm_hosttest: the saved-state writer on a host model

`python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` - exit 0 =
every shipped shape passed and every planted defect reddened.

## Contents

- **[What it drives](#what-it-drives)** -- the shipping firmware translation unit, compiled unchanged against stub headers
- **[The model](#the-model)** -- the CSR face, the flash, the LiteSPI master and the clock, in `nvm_host.c`
- **[What is graded](#what-is-graded)** -- fourteen checks per shape, all on bytes
- **[The negative controls](#the-negative-controls)** -- sixteen writer defects planted into a copy, each of which must be caught
- **[Every boot path starts the restore walk](#every-boot-path-starts-the-restore-walk)** -- five boot paths per shape and two planted boot defects
- **[What this suite does NOT prove](#what-this-suite-does-not-prove)** -- the board

## What it drives

[`sw/firmware/milan_baremetal/milan_baremetal.c`](../milan_baremetal/milan_baremetal.c),
the bare-metal firmware the LiteX BIOS links, is compiled as shipped. The
`stubs/` directory answers every include the firmware makes: the generated
memory map, CSR accessors and constants, the BIOS command and init
registries, the CRC helper and the busy-wait. The only edit the driver makes
to the copy it compiles is blanking the two RISC-V `fence` statements, which
a host assembler cannot encode. The constants the stub `generated/soc.h`
carries come from `scripts/nvm_shape.firmware_constants`, the same function
`sw/litex/milan_soc.py` publishes them from, so the firmware is graded against
the Python inventory of the SAME shape rather than a second reading of the
overlay.

## The model

[`nvm_host.c`](nvm_host.c) owns three arrays and a clock:

- **the Milan CSR window**, a word array; the firmware's stores are found by
  comparing the array with a shadow copy on the next access and are replayed
  into a model of `KL_nvm_backend`'s control face (the five words, the two
  channel-map tables, the three strobes) and of its section 9.2 liveness
  machine (the heartbeat re-arms `T-NVM-WRITER-ALIVE`, a start opens the
  commit bracket, an acknowledgement clears `nvm_dirty`, a deadline lapsing
  after the writer was once live is a loss). `PP_STAT`, `PP_NVM_STAT` and
  the PHC time-of-day words are recomposed from that state on every access;
- **the QSPI flash**, a 16 MiB array read through the memory mapping and
  erased and programmed through the LiteSPI command-master stubs, which decode
  `WREN`, `RDSR`, sector erase and page program, hold write-in-progress for a
  configurable erase time, and can be told to fail an erase, hang a program or
  flip a programmed bit. The mapping's base is a host call, so every read the
  firmware opens through it is counted, and a planted read fault answers a
  window of those reads from a copy whose bytes of one slot are wrong: one byte XORed with a different value on every faulty read
  (`--read-fault SLOT:OFF:SKIP:COUNT[:BASE]`), every byte of the slot read
  as `0xFF` (`--read-ff SLOT:SKIP:COUNT`), or the slot read as the other
  slot's bytes (`--read-other SLOT:SKIP:COUNT`). Counted from the read the
  fault is armed at (power-on for one given before `--boot`), the first SKIP
  reads are clean and the next COUNT are faulty. The memory-mapped read
  always returns bytes, so wrong bytes are the only media fault the shipping
  read path can meet ([#671](https://github.com/kebag-logic/milan-fpga/issues/671));
- **the reserved processor window**, a byte array the firmware stages the
  KLJ2 container in and the driver writes a changed record into, as the
  processor's WRITE through the backend would;
- **time**, advanced by the firmware's own `cdelay()` and by every SPI byte,
  so the heartbeat cadence and every timeout are measured in model time.

`--restart` is a CPU-only reset of the writer, a restart without a fabric
reset: every file-scope variable of the writer returns to its initial value
and `nvm_boot()` runs again, while the backend model, the window and the
flash keep their state. [`writer_restart.py`](writer_restart.py) appends it
to every host build and refuses unless it names every such variable; the
co-simulation's W1 to W4 use the same model
([`tb/verilator/nvm_cosim`](../../../tb/verilator/nvm_cosim/README.md)).
The harness prints its state when the restart begins and counts the reads
the restart opens (`restart_reads=`).

An explicit stimulus can reopen one ownership-vector bit after reload.
This leaves closed neighbours beside an open record without modeling a producer.
Concurrent device-side changes remain the real-backend cosimulation's scope.

## What is graded

Per shipped shape (`configs/endstation_*.yaml`), the driver builds the shape
with the end-station builder, encodes images with `scripts/nvm_klj2.py`, runs
the harness through boot, idle time and console commands, and compares bytes:

1. a blank board stages an all-erased container equal to the Python encoder's;
2. `milan_nvm commit` promotes it into slot A, acknowledged once, page-aligned;
3. a golden image in slot B is chosen and copied byte for byte, and after one
   record changes the container committed into slot A equals the Python
   encoder's for the same records at the next sequence, and decodes;
4. the debounce holds the commit for its window and no longer;
5. the A/B rule: newer wins, a torn newer slot falls back, two torn slots boot
   blank naming the failure;
6. verdict parity: for every section 6.2 refusal, both faces of the
   erased-record rule and a blank slot, the firmware's printed verdict equals
   `klj2_decode`'s for the same bytes;
7. a failed erase, program and read-back each publish their transaction
   verdict, withhold the acknowledgement, and the commit deadline lapses;
8. the heartbeat is serviced through a 3 s erase, at most 500 ms apart;
9. an idle board stays backed and never stale;
10. `milan_nvm wipe` erases both slots;
11. an open record beside an unaligned closed predecessor retains its golden
    staged bytes while the predecessor's change commits byte-identically;
12. a rejected shape or identity at startup never heartbeats under
    console input;
13. a boot read fault leaves the authority unknown
    ([#671](https://github.com/kebag-logic/milan-fpga/issues/671)). One slot
    holds a valid container and the other is blank, both ways round, at
    sequence 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF. A read fault on the
    valid slot (its magic byte or its sequence word, and a byte of its
    record area, which only the CRC over every byte read refuses) or on the
    blank slot is walked over every boot read: SKIP 0 to 5, COUNT 1 to 3,
    and one window covering the whole boot. A single all-`0xFF` read of the
    valid slot is walked over SKIP 0 to 5. Both slots also hold valid
    containers, both ways round, the newer at 0x5A5A5 or at 0 (the wrap,
    the older at 0xFFFFFFFF), differing in two names: a fault on the newer
    slot (its magic byte or a record-area byte) is walked over the same
    windows, the older is faulted for the whole boot, and the newer's
    re-stage reads are answered with the older's container (`--read-other`,
    COUNT 1 to 3). The same faults also meet a writer restart without a
    fabric reset, the re-attach path, after a clean cold boot: the valid
    slot is faulted for the whole restart at every sequence (a header byte,
    and once a record-area byte) and by one faulty read at each of the
    restart's first four reads, and with both slots valid the newer is
    faulted for the whole restart or on its three re-stage reads. Each case
    makes a real change, lets the debounce commit it and boots again clean. The faulty boot's line names each slot as its
    bytes read, or UNREAD (`VD_LEN`, its bit in `unread=`), and offers the
    newer slot it accepts, and its window holds that slot's container byte
    for byte, or the blank image when none is offered; a restart leaves
    the window it re-attaches to as it was. Every saved record and the
    change survive the reboot, or the faulty boot HELD the writer. A held
    writer erased, programmed and acknowledged nothing, never heartbeated,
    named the unread slot, and the clean reboot restores every saved
    record; that case then runs on through a change, its commit and another
    clean reboot. A held restart did none of those after the restart either,
    let the fabric revoke `nvm_backed` (`backed=0 stale=1`) and printed
    "re-attached and HELD". One faulty read never holds the writer, and a
    slot left unread, or faulted for the whole boot or restart, always
    does. No boot opens more than 13 reads (the AEM image and three
    judgements and three re-stages per slot) and no restart more than 12. A
    slot faulted for the whole boot opens exactly 6, and for the whole
    restart exactly 5: three reads of that slot and two of the other (two
    agreeing blank reads, or a judgement and a re-stage), so the bound of
    three reads per judgement is pinned, not only the total. A held writer refuses `milan_nvm commit` and reports the hold on
    `milan_nvm`; an explicit `milan_nvm wipe` still erases both slots, as
    for a retired writer; and a writer that retires at boot with a slot
    unread names the retire, not the slot, for each cause: an older backend
    contract, a boot load ended with none accepted, a window gone live
    (`--boot-backend contract|over|live`) and four refused window loads. The
    cases run on `--jobs` threads, every CPU by default;
14. a slot whose bytes read cleanly but fail validation (a foreign entity,
    a bad CRC) names no generation: with the other slot blank, no slot is
    offered, the boot line reports sequence 0, and the first commit is at
    sequence 1.

## The negative controls

`--self-test` plants each defect into a copy of the firmware, rebuilds the
harness and requires the suite to redden:

| control | the defect | what catches it |
|---|---|---|
| `no_ascending_check` | a record id may repeat or go backwards | verdict parity on the duplicate-id image |
| `no_heartbeat_in_wait` | the erase poll loop stops heartbeating | the 3 s erase check |
| `verify_skipped` | the read-back never fails | the failed-verify check sees an acknowledgement |
| `erased_header_only` | an erased header is accepted over a live payload | verdict parity on the torn erased span |
| `edge_cross` | a word copy crosses an unaligned record edge | the open neighbour's poisoned live bytes must never replace its staged bytes |

Those five are graded by checks 1 to 12. Eleven #671 defects are graded by
checks 13 and 14. Each is planted into the first shape and into both
product shapes (`endstation_ax7101_1x1_tdm8`, `endstation_ax7101_8x8`), and
must be caught on every one by a finding carrying its own words. Check 14
runs first, and check 13 stops at the first such finding, so a control's
other findings are not counted; that keeps `--self-test` inside the ten
minutes the builder gate gives it. Check 13 walks its restart cases
first. The `r_` controls and `restage_fail_not_unread` are the plants of
PR #715's reviews, under their names:

| control | the defect | the finding that must catch it |
|---|---|---|
| `restart_at_zero` | an unread slot no longer holds the writer, so the sequence restarts at 0 | "was lost on the clean reboot" |
| `unbounded_retry` | the read of a slot has no bound | "over the bound" |
| `generation_from_refused_slot` | a refused slot's header sequence continues the generation | "generation was taken from a refused slot" |
| `verdict_only_agreement` | two refused reads agree by verdict, not by bytes (R501-3's probe on #665) | "was lost on the clean reboot" |
| `r_digest_header_only` | a refusal's digest covers the 40 header bytes, so two reads whose record areas differ agree | "on reads that returned different bytes" |
| `r_fill_from_flash` | the window is filled by a fresh read of the slot, as before #671, not from the judged stage | "is not the container it judged" |
| `r_restage_fail_offers_none` | a pick that never reads back offers nothing, not the other slot | "yet the boot offered" |
| `restage_fail_not_unread` | a pick that never reads back is not marked UNREAD, so the writer goes live | "yet the boot line does not name it unread" |
| `r_restage_any_seq` | the re-stage takes any VD_OK read, whatever sequence it names | "another valid container than the one the boot offered" |
| `r_reattach_goes_live` | a writer restart without a fabric reset (the re-attach path) goes live with a slot unread, while the cold boot still holds | "yet the writer re-attached live" |
| `r_judge_four_tries` | a judgement takes four reads, over the stated three, inside the total bound | "want exactly" |

The self-test also invokes the PHY host checks.
Their IEEE-timed peer catches missing publication, deferred recovery and
sampling after the rising edge instead of before it.

## Every boot path starts the restore walk

Since processor pin `d352bbaa` the processor holds its ACMP listener and AECP
from reset until the restore walk reaches its terminal, and `PP_CTRL[1]`
starts that walk ([#70](https://github.com/kebag-logic/milan-fpga/issues/70)).
[`test_boot_walk.py`](test_boot_walk.py) boots each shape five ways: a cold
boot, a window the backend refuses on every load, a record set that does not
match the generated shape ("persistence disabled", planted into a copy), and
the cold and persistence-disabled boots again with the model's walk ending
CLOSED (`--walk-closed`: fail and never done, `PP_STAT[16]`). Each boot must
start exactly one walk, never raise the entity enable before it, and end its
wait at the walk's terminal rather than at the restore timeout. The model
counts `PP_CTRL[1]` rising edges (`walks=`) and flags an enable seen before
any walk (`enable_first=`).

`--self-test` plants two boot defects, each caught by a named boot-walk
finding:

| control | the defect | what catches it |
|---|---|---|
| `shape_path_skips_walk` | the persistence-disabled path returns before the walk, as it did before this check | `walks=0` and `enable_first=1` on that path |
| `wait_on_done_only` | the restore wait ends on done alone, which a CLOSED restore never raises | the wait runs out its timeout on a CLOSED restore |

## What this suite does NOT prove

The board. The real LiteSPI master's timing and arbitration, the real DRAM
window, the processor writing records into it and the restore walk reading
them back are the bench's ([design page](../../../docs/design/SAVED_STATE_FASTCONNECT.md)
section 11). The processor's binding records and, since pin `d352bbaa`, its D3
writer's scalar records reach the store; names and channel maps do not yet.
The model follows the backend's contract as `hdl/milan/KL_nvm_backend.sv`
states it; the backend itself is graded by
[`tb/verilator/nvm_backend`](../../../tb/verilator/nvm_backend/README.md).

Nor does it prove that every read fault is seen. The writer sees a fault
only when two reads of a slot return different bytes. A fault that returns
the same wrong bytes on two reads is a refusal of those bytes by the rule,
and a slot read as all `0xFF` twice is blank. Either can still let the next
commit restart the sequence below a container a later clean boot prefers.
Check 13 walks faults that differ from read to read, single all-`0xFF`
reads, and the other slot's container on a re-stage read, and no others. A
judgement read answered with the other slot's valid container is an address
fault no rule over the bytes can see, because a container does not name its
slot: with both slots valid, the boot can then offer the older one and live,
and the next commit overwrites the newer container with the older one's
records. The re-stage's sequence check refuses that fault on the picked
slot only.

Console tests reject shape and identity mismatches on every shape.
Every Milan command and empty input keep `hb=0 backed=0 stale=0`.
Removing startup admission must fail both cases.
Removing the BIOS dispatch marker must fail linking.
A negotiation-stage NAK also kills the ignored-ACK mutant.
