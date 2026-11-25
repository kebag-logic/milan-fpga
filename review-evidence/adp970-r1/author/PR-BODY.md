## Contents

- **[Status](#status)**: local gates, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: public task and roles.
- **[Description](#description)**: what changed and why.
- **[Authoritative references](#authoritative-references)**: clauses and documents.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: commands.
- **[How to validate](#how-to-validate)**: commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this does not do.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

`970-discovery` -> `dev-soft-core`: one change, a merge of `dev-soft-core` `c34e7d8b`, and the reboot simulation's
recorded ADP row. See [How to validate](#how-to-validate) for the local results.

## Linked Issue / roles

Closes #970
Relates to #972, #665

Executor: to be assigned
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

ADP's first draws were not uniform. The core seeds its generator once, at its enable, by an exclusive-or. It then draws
from the top 16 bits of one xorshift32 step, which a small seed barely moves. The adapter's seed was the milliseconds
since reset:

- every boot of one entity drew its first delay between 640 and 890 ms;
- sixteen neighbouring entity IDs drew theirs within 5 ms of each other.

That is neither the uniform, host-distinct draw of IEEE 1722.1-2021 6.2.4.2.2 nor the random value of Milan v1.2
5.6.3.5.2 and 5.6.3.5.3. It is the bunching that Milan v1.2 Table 5.49's delay exists to avoid.

What changes:

- `sw/firmware/ctrl/adp/`: the seed port returns the least significant 32 bits of the sum, with an end-around carry,
  of the MAC address and a clock sample (6.2.4.2.2). That sum is mixed with the entity ID and the interface by two rounds
  of a multiply-free bijection. The core's state is not written.
- `sw/firmware/ctrl/plat/ctrl_plat.c`: the sample is the platform's microsecond clock, read as it is asked.
- No draw range changes, and the declared discovery time stays 6.0 s (FR_NFR 2.1.1, 4,311 ms).
- No mailbox access is added to any pass, and the platform structure is unchanged.
- `tb/verilator/ctrl_service_budget/scenario.py` (and the hooks' order group): the first ENTITY_AVAILABLE after a
  LINK_UP is awaited for the draw's full 0 to 4 s, where the old wait of 2.2 s held only because the draw never passed
  0.9 s. No probe's budget changes.

What this does not do, because it is the stack's: take a fresh sample at each later LINK_UP. The generator's own
seeding is changed in a separate tsn-c-stack change; this repository takes it with a pin move (see
[Known limitations](#known-limitations--out-of-scope)).

## Authoritative references

- IEEE 1722.1-2021 6.2.4.2.2, randomDeviceDelay: a uniform distribution; "different hosts do not generate the same
  sequence"; a maximum length sequence of no less than 2^32 - 1; seeded "using the least significant (most rapidly
  varying) octets of the sum of the requestor's IEEE 802 MAC address and the local real time clock".
- Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.4, 5.6.3.5.5, 5.6.3.5.7, Tables 5.49 to 5.51.
- #970, its ruling of 2026-11-25; `docs/reference/FR_NFR.md` 2.1.1; `docs/design/MAILBOX_SPLIT.md`, "The ADP slice";
  `sw/firmware/ctrl/adp/adp_mbx.h`, THE DRAW.

## How to get into the same state

```sh
git fetch origin 970-discovery && git switch 970-discovery
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4
python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <work>/1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <work>/8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <work>/ledger
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <work>/b8 --record-budget-findings --record-share-findings
```

| Check | Result |
|---|---|
| firmware gate, every suite; coverage ratchet | PASS; 40 files |
| planted defects for the draw and the first advertisement | 19 of 19 caught; every host test named by a plant |
| the draw's tests (`AdpDraw.H4` to `H7`, `Boot.B25`, `B26`) | first delays of 1,024 neighbouring entities and of 1,024 boots, at startup and at LINK_UP, each under the 99 % chi-square bound over 16 bins; the seed's terms; the seed without a clock |
| split boot simulation, 1x1 and 8x8 | PASS, 0 findings |
| platform images against the memory ledger | PASS at four points; `rom` 344 to 384 B more; `sram`, tiles and `ctrl_plat` unchanged |
| twin and its plants, co-simulation, reboot simulation, hooks and budget harness self-tests, memory plan tests | PASS |
| CPU budget legs against the base, 1x1/1if | 75 probes paired, 0 misses on both sides, 0 passes over the share; composed maximum 1.465 -> 1.475 ms |
| CPU budget legs against the base, 8x8/1if | 90 probes paired, the same 7 known misses on both sides, 0 passes over the share; composed maximum 1.759 -> 1.774 ms; the egress ledger PASS |
| rows apart by more than 0.1 ms | 10 of 75 (1x1, -0.10 to +0.21 ms) and 1 of 90 (8x8, +0.22 ms); no verdict changed |
| the load table and the flip check | the base's output, unchanged |
| hot code | every hot-list function at the base's address and size |
| documentation checks | pass |

The merge of `c34e7d8b` changed neither the firmware images nor the simulated hardware of the budget legs: both are
byte-identical before and after it.

## Known limitations / out of scope

- A LINK_UP after the first is not seeded afresh at this stack pin. A tsn-c-stack change takes a sample on each
  transition out of DOWN, seeds with the MAC address and clock sum, and mixes in the entity ID, the interface and the
  earlier state. Its tests check uniform first draws over samples and neighbouring hosts, each seed term, one sample per
  leave of DOWN, and the sequence length of 2^32 - 1. This repository takes it with a pin move, whose adapter then returns
  the raw clock and whose ADP LINK_UP path bound becomes 12 accesses.
- The first frames lost in the first 1.2 to 1.45 s after a link-up on the bench (the ruling's item 3) are not addressed.
  They are to be measured at the device's own port first.
- ACMP's and MAAP's seeds are outside this change.

## Definition of Done

- [x] New and changed behaviour has self-checking tests with planted defects
- [x] Required local verification passes (the table)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] The tsn-c-stack change reviewed and merged, and the pin move
- [ ] Candidate merge result validated per CONTRIBUTING.md
