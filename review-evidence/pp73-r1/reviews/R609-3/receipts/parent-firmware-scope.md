**Owner direction, 2026-10-05:** write the software side of the Mark II split now, in parallel with the protocol-processor program. The requirement change (#664) still waits for the PP program to finish.

## Scope

Bare-metal firmware on the on-chip RISC-V for:
- **ADP**;
- **ACMP** (decided earlier the same day);
- **MAAP**;
- **SRP** (MRP, with MSRP and MVRP);
- **AECP**: descriptor serving, commands, and the unsolicited notifications. The owner added AECP the same day;
- **the NV memory handling**: read the saved entity state from the flash at boot, apply it, and write it back on change (the #70 saved-state design).

It sits behind the packet-mailbox and ingress-filter contract recorded on #640: block RAM rings, doorbell and interrupt, 32-bit accesses, no DMA, a bus adapter per host, portable C behind a small HAL, one YAML contract. It must port to a hard core.

The fabric keeps:
- framing and timestamps;
- the gPTP plane;
- the timers that carry hard deadlines, posted to the core as events;
- the ingress filter.

## Rules while #664 is open

- Everything lands behind a build switch whose default is the current all-fabric placement. No shipping-image change.
- The firmware builds and is tested on the host against a mailbox model. The existing processor suites' stimulus is reused through that model wherever possible, so each protocol's checks carry over.
- Each protocol states its firmware service-latency bound per response path and tests it, as NFR-SCOUT-03 will require after #664.
- Portable C (C11), no compiler intrinsics in protocol code, and a fixed-width, byte-order-explicit wire layer.

## Lanes (in order)

- **F0, the contract and harness (first).** The mailbox and ingress-filter YAML contract and its generator (fabric module skeleton, C header, docs), the HAL, the host mailbox model and test harness. The ADP firmware is the first vertical slice through it.
- **F1, NV memory handling.** Flash read at boot, validation per the #70 saved-state format (KLJ2), apply, and the write and commit path, ported from `sw/firmware/milan_baremetal` and the processor writer's rules. It can start alongside F0 against the HAL draft.
- **F2, MAAP.**
- **F3, ACMP.**
- **F4, SRP (MRP, MSRP, MVRP).**
- **F5, AECP** (descriptor serving, commands, notifications).

F2 to F5 start once F0's contract merges, so the protocols share one interface.

Relates to #640, #664, #70, and milestone 13.

