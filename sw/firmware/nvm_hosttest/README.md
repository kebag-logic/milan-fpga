<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# nvm_hosttest: the saved-state writer on a host model

`python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` - exit 0 =
every shipped shape passed and every planted defect reddened.

## Contents

- **[What it drives](#what-it-drives)** -- the shipping firmware translation unit, compiled unchanged against stub headers
- **[The model](#the-model)** -- the CSR face, the flash, the LiteSPI master and the clock, in `nvm_host.c`
- **[What is graded](#what-is-graded)** -- fourteen checks per shape, all on bytes
- **[The negative controls](#the-negative-controls)** -- twenty-three writer defects planted into a copy, each of which must be caught
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
  window of those reads from a copy whose bytes of one slot are wrong: one
  byte XORed with a different value on every faulty read
  (`--read-fault SLOT:OFF:SKIP:COUNT[:BASE]`), the same with the CRC-32
  trailer the slot's length word places rewritten over the faulty bytes, so
  every faulty read is a different container whose CRC closes
  (`--read-sealed SLOT:OFF:SKIP:COUNT[:BASE]`), every byte of the slot read
  as `0xFF` (`--read-ff SLOT:SKIP:COUNT`), or the slot read as the other
  slot's bytes (`--read-other SLOT:SKIP:COUNT`). An `OFF` below zero counts
  back from the end of the container the slot's length word names: `-1` is
  the trailer's last byte and `-5` the last byte its CRC covers. Two more
  faults forge the four bytes before the trailer so that the CRC-32 over
  every byte before it is a value the fault fixes, and so change one term of
  the writer's comparison of two refused reads and keep the others:
  `--read-length SLOT:SKIP:COUNT` grows the length word by four on every
  faulty read, moves the slot's trailer value to the end that length names
  and forges the CRC to its complement, so each read is refused `VD_CRC`
  with another byte count; `--read-verdict SLOT:SKIP:COUNT` XORs the entity,
  model or record-layout word in turn and closes the CRC on the slot's own
  trailer, so any three faulty reads in a row are refused `VD_ENT`,
  `VD_SHAPE` and `VD_REC`. Counted from the read the
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
the restart opens (`restart_reads=`). A boot or a restart that opens more
than 1,000 reads, far past any bound the writer states, is ended as a read
storm with its summary and its reads counted, as a run that opens 1,000,000
is, so a planted unbounded read loop costs no more than a bounded one.

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
    ([#671](https://github.com/kebag-logic/milan-fpga/issues/671)). The
    cases are generated, never picked (`read_fault_cases.fault_cases`). Four
    groups place the slots and the fault. A sealed fault (`--read-sealed`)
    flips the entity ID's low byte or a record-area byte and closes the CRC
    over the faulty bytes, so each faulty read is a different container
    whose CRC passes and that is refused after it, `VD_ENT` or `VD_REC`; a
    CRC-32 over every byte of such a container is one constant, so these
    are the reads a comparison by that CRC alone calls the same
    (R603-4-F1). With one slot valid and the other
    blank, the fault is on the valid slot (its magic byte, the top byte of
    its sequence word, a record-area byte, which only the CRC over every
    byte read refuses, a sealed entity or record-area byte, or every byte
    read as `0xFF`) or on the blank slot
    (its magic byte, or its reads answered with the valid slot's container,
    `--read-other`). With both slots valid, the newer at 0x5A5A5 or at 0
    (the wrap, the older at 0xFFFFFFFF) and differing in two names, the
    fault is on the newer slot (its magic byte, a record-area byte, a sealed
    entity or record-area byte, or the older's container) or on the older
    (its magic byte, a record-area byte or a sealed entity or record-area
    byte). Each group's every manner of fault meets every window, both ways
    round, on a cold boot and on a writer restart without a fabric reset
    (the re-attach path) after a clean cold boot. A window starts at any
    read within the complete bound (13 on a cold boot, 12 on a restart)
    and lasts one to four reads, one past the three a judgement or a
    re-stage gives a slot, or it lasts the whole boot. Starts after the
    clean boot would end are included too; they must leave its schedule
    unchanged. The sequence takes 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF
    in turn with one slot blank, and 0x5A5A5 and 0 with both valid, one per
    case: crossed with every window it would not fit the suite's time.
    R603-4-F1's class, two sealed faulty reads that open one slot's
    judgement and then a clean read, meets every sequence of its group
    besides, both ways round and on both entry paths, for each sealed
    manner (`read_fault_cases.sealed_class`). The writer compares two
    refused reads by four terms, listed once in
    `read_fault_cases.COMPARISON`: the verdict, the byte count, the CRC-32
    over all but the last four bytes (the prefix CRC) and those four bytes
    (the trailer). Each term has a class of its own
    (`read_fault_cases.term_class`): two faulty reads that differ from one
    another in that term alone open the faulted slot's judgement, the window
    the reference model finds, and its third read is clean. The verdict
    class is `--read-verdict`, the byte count's `--read-length`, the prefix
    CRC's the last byte before the trailer (`--read-fault SLOT:-5`) and the
    trailer's its last byte (`--read-fault SLOT:-1`), so only the term keeps
    the two reads from agreeing (R602-5-F1, R603-5-F1). Each class runs at
    every sequence of each group whose faulted slot holds a container (1,
    0x5A5A5, 0x80000000 and 0xFFFFFFFF with the other slot blank), both ways
    round and on both entry paths: 32 cases per term. A finding that a
    refused verdict stood on such a case's faulted slot names the term
    ("which differ only in their trailer"). The suite
    fails when the firmware's `nvm_reads_agree` compares by other terms
    than the list, or when a listed term has no class at one of those
    places or no control (`read_fault_cases.comparison_findings`, checked
    against the firmware as shipped).
    A reference model of the writer's reads (`read_fault_cases.expect`),
    written once from the rule, gives each case the reads it opens, the
    slots it leaves unread and why. A case it finds outside the rule's
    stated detection limit is not run: two faulty reads of one judgement
    return the same bytes (all `0xFF` twice), or a faulty read returns the
    other slot's valid container and it stands. That leaves 3,550 of 3,636
    cases per shape, 1,711 restarts and 1,839 cold boots, 128 of them the
    terms' classes; every window keeps its byte faults, sealed or not, which
    are always inside the limit. Each case makes a real
    change, lets the debounce commit it and boots again clean. The faulty
    boot's line names each slot as its bytes read, or UNREAD (`VD_LEN`, its
    bit in `unread=`), and offers the newer slot it accepts, and its window
    holds that slot's container byte for byte, or the blank image when none
    is offered; a restart leaves the window it re-attaches to as it was.
    Every saved record and the change survive the reboot, or the faulty
    boot HELD the writer. The boot opens exactly the reads the model opens
    and never more than 13 (the AEM image and three judgements and three
    re-stages per slot), a restart never more than 12, so each judgement's
    and each re-stage's bound is pinned from both sides. The writer holds
    exactly when a slot is left unread, by its own line or by the model,
    and the hold names each unread slot and why: "gave no standing verdict
    in 3 reads", or "did not read back as it was judged in 3 reads" for a
    re-stage that never read back. A held writer erased, programmed and
    acknowledged nothing, never heartbeated, and the clean reboot restores
    every saved record; that case then runs on through a change, its commit
    and another clean reboot. A held restart did none of those after the
    restart either, let the fabric revoke `nvm_backed` (`backed=0 stale=1`,
    after a 3 s idle) and printed "re-attached and HELD". A held writer
    refuses `milan_nvm commit` and reports the hold on `milan_nvm`; an
    explicit `milan_nvm wipe` still erases both slots, as for a retired
    writer; and a writer that retires at boot with a slot unread names the
    retire, not the slot, for each cause: an older backend contract, a boot
    load ended with none accepted, a window gone live
    (`--boot-backend contract|over|live`) and four refused window loads. The
    cases run on `--jobs` threads, every CPU by default, the groups and the
    terms' classes interleaved; the harness is deterministic, so a clean reboot of slots an
    earlier case already booted is not run again;
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

Those five are graded by checks 1 to 12. Eighteen #671 defects are graded
by checks 13 and 14. Each is planted into the first shape and into both
product shapes (`endstation_ax7101_1x1_tdm8`, `endstation_ax7101_8x8`), and
must be caught on every one by a finding carrying its own words. Check 14
runs first, and check 13 stops at the first such finding, so a control's
other findings are not counted; that keeps `--self-test` inside the twenty
minutes the builder gate gives it. Each group's windows run the whole boot
first, then the longest, and the terms' classes run beside the groups. The
four `r_omit_` controls are generated from `read_fault_cases.COMPARISON`,
one per term. The `r_` and `p_` controls and
`restage_fail_not_unread` are the plants of PR #715's reviews, under their
names:

| control | the defect | the finding that must catch it |
|---|---|---|
| `restart_at_zero` | an unread slot no longer holds the writer, so the sequence restarts at 0 | "was lost on the clean reboot" |
| `unbounded_retry` | the read of a slot has no bound | "over the bound" |
| `generation_from_refused_slot` | a refused slot's header sequence continues the generation | "generation was taken from a refused slot" |
| `verdict_only_agreement` | two refused reads agree by verdict, not by bytes (R501-3's probe on #665) | "was lost on the clean reboot" |
| `r_digest_header_only` | a refusal's digest covers the 40 header bytes, so two reads whose record areas differ agree | "on reads that returned different bytes" |
| `r_digest_with_trailer` | the round-4 comparison: one CRC-32 over every byte read, the trailer included, which is one constant over every container whose CRC closes, so two sealed refusals agree (R603-4-F1) | "on reads that returned different bytes" |
| `r_fill_from_flash` | the window is filled by a fresh read of the slot, as before #671, not from the judged stage: a read the rule does not make | "want exactly" |
| `r_restage_fail_offers_none` | a pick that never reads back offers nothing, not the other slot | "yet the boot offered" |
| `restage_fail_not_unread` | a pick that never reads back is not marked UNREAD, so the writer goes live | "yet the boot line does not name it unread" |
| `r_restage_any_seq` | the re-stage takes any VD_OK read, whatever sequence it names | "another valid container than the one the boot offered" |
| `r_reattach_goes_live` | a writer restart without a fabric reset (the re-attach path) goes live with a slot unread, while the cold boot still holds | "yet the writer re-attached live" |
| `r_judge_four_tries` | a judgement takes four reads, over the stated three, inside the total bound | "want exactly" |
| `p_restage_unbounded` | the picked slot's re-stage has no bound, so a fault after its judgement read is read until it ends | "want exactly" |
| `r_restage_four_tries` | a re-stage takes four reads, over the stated three | "want exactly" |
| `r_omit_verdict` | the verdict term is removed from the comparison, the other three kept (R602-5-F1, R603-5-F1) | "which differ only in their verdict" |
| `r_omit_byte_count` | the byte count term is removed from the comparison | "which differ only in their byte count" |
| `r_omit_prefix_crc` | the prefix CRC term is removed from the comparison | "which differ only in their prefix CRC" |
| `r_omit_trailer` | the trailer term is removed from the comparison, which looks redundant for a sealed container and is not for a faulted trailer | "which differ only in their trailer" |

The self-test also requires the comparison check to fail, by its own
words, for each term with its class taken out of the campaign, for each
term with its control taken out, and for a firmware that compares by one
term more than the list.

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
only when two reads of a slot return different bytes. It compares two
refused reads by their byte count, a CRC-32 over all of their bytes but the
last four, and those four whole, so it always tells apart two reads that
differ in one or two bits or only within 32 consecutive bits, and any other
two except with a probability of about 2^-32. A fault that returns
the same wrong bytes on two reads is a refusal of those bytes by the rule,
and a slot read as all `0xFF` twice is blank. Either can still let the next
commit restart the sequence below a container a later clean boot prefers.
A judgement read answered with the other slot's valid container is an
address fault no rule over the bytes can see, because a container does not
name its slot: with both slots valid, the boot can then offer the older one
and live, and the next commit overwrites the newer container with the older
one's records. The re-stage's sequence check refuses that fault on the
picked slot only. Check 13 runs every all-`0xFF` and address fault its
reference model finds the rule can see, and none it cannot.

Console tests reject shape and identity mismatches on every shape.
Every Milan command and empty input keep `hb=0 backed=0 stale=0`.
Removing startup admission must fail both cases.
Removing the BIOS dispatch marker must fail linking.
A negotiation-stage NAK also kills the ignored-ACK mutant.
