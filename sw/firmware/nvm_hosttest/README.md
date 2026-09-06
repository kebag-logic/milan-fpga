<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# nvm_hosttest: the saved-state writer on a host model

`python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` - exit 0 =
every shipped shape passed and every planted defect reddened.

## Contents

- **[What it drives](#what-it-drives)** -- the shipping firmware translation unit, compiled unchanged against stub headers
- **[The model](#the-model)** -- the CSR face, the flash, the LiteSPI master and the clock, in `nvm_host.c`
- **[What is graded](#what-is-graded)** -- ten checks per shape, all on bytes
- **[The four negative controls](#the-four-negative-controls)** -- writer defects planted into a copy, each of which must be caught
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
  flip a programmed bit;
- **the reserved processor window**, a byte array the firmware stages the
  KLJ2 container in and the driver writes a changed record into, as the
  processor's WRITE through the backend would;
- **time**, advanced by the firmware's own `cdelay()` and by every SPI byte,
  so the heartbeat cadence and every timeout are measured in model time.

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
10. `milan_nvm wipe` erases both slots.

## The four negative controls

`--self-test` plants each defect into a copy of the firmware, rebuilds the
harness and requires the suite to redden:

| control | the defect | what catches it |
|---|---|---|
| `no_ascending_check` | a record id may repeat or go backwards | verdict parity on the duplicate-id image |
| `no_heartbeat_in_wait` | the erase poll loop stops heartbeating | the 3 s erase check |
| `verify_skipped` | the read-back never fails | the failed-verify check sees an acknowledgement |
| `erased_header_only` | an erased header is accepted over a live payload | verdict parity on the torn erased span |

## What this suite does NOT prove

The board. The real LiteSPI master's timing and arbitration, the real DRAM
window, the processor writing records into it and the restore walk reading
them back are the bench's ([design page](../../../docs/design/SAVED_STATE_FASTCONNECT.md)
section 11), and today only the processor's binding records reach the store.
The model follows the backend's contract as `hdl/milan/KL_nvm_backend.sv`
states it; the backend itself is graded by
[`tb/verilator/nvm_backend`](../../../tb/verilator/nvm_backend/README.md).
