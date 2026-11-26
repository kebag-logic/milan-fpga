[A847]

[A847]

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

`970-discovery` -> `dev-soft-core`. Both dependencies have merged: #1016 into `dev-soft-core` as `4df125b8`, and
kebag-logic/tsn-c-stack#40 into its `main` as `c3bff8f3`. Since the reviewed head `0ad0e518`:

1. a merge of `1013-pins` (#1016's branch);
2. the pin of tsn-c-stack `5e6ab995`, with this repository's side of it;
3. the pin of `95902060`, #40's second commit: the plain sum, no sample at an ENTITY_DISCOVER;
4. a merge of `dev-soft-core` `4df125b8` (#1016 as merged; it carries the same consumer change, kept once);
5. the pin of `c3bff8f3`, the merge commit of #40, whose tree equals `95902060`'s.

## Linked Issue / roles

Relates to #970 (the draw)
Relates to #1013, #972, #665

Executor: to be assigned
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

At `0ad0e518` the first draw after a boot was uniform, but a qualified LINK_UP took no fresh sample. The pinned core
asked for its seed only at its enable, so a LINK_UP drew from the state formed then.

What changes:

- **tsn-c-stack `c3bff8f3`** (the merge of kebag-logic/tsn-c-stack#40 on `a795471c`):
  - On each transition out of DOWN, the startup draw and each qualified LINK_UP (Milan v1.2 5.6.3.5.2, 5.6.3.5.3), the
    core takes one sample from its seed port. A duplicate LINK_UP and a LINK_UP while disabled take none.
  - It seeds with the least significant 32 bits of the sum of the MAC address and the sample, modulo 2^32 (IEEE
    1722.1-2021 6.2.4.2.2), mixed with the entity ID, the interface and its earlier state.
  - An ENTITY_DISCOVER, a TMR_ADVERTISE expiry and a grandmaster change draw without a sample.
  - The draw ranges and the 2^32 - 1 generator are unchanged.
- **`sw/firmware/ctrl/adp/`:** the adapter only supplies the sample. It reads the platform's microsecond clock, or
  NOW_MS where a composition wires none, and writes no core state. `ADP_MBX_LAT_LINK` is 12 accesses (11 before): the
  NOW_MS read where no clock is wired. The platform wires a clock, and its LINK_UP row stays at 11.
- **Tests through the real adapter and the platform:**
  - `AdpDraw.H9` counts one clock read for each qualified rise and for the startup draw, and none for a duplicate or
    disabled LINK_UP.
  - `H10`: boots alike up to a LINK_UP, their clocks apart only then, draw 915 distinct first delays of 1,024, uniform.
  - `Boot.B25`: three boots one microsecond apart in the clock's origin seed apart. That fails for a clock read in
    milliseconds, one in 1,024 us granules, and one wired after ADP's startup draw.
  - `Boot.B27`: a LINK_UP after ready reads the platform clock at that LINK_UP on either interface, and leaves every
    other interface's generator.
  - Each rule has a planted defect that its test catches by name.
- **Harness waits.** The CPU budget harness awaits the first ENTITY_AVAILABLE for the full 4 s LINK_UP draw, as at
  `0ad0e518`, now as literals. The co-simulation shuts down at 32 s, when the fourth ENTITY_AVAILABLE has come whatever
  the draws; its fixed 20 s held only for some draws. No probe's budget changes.
- **Documents.** `FR_NFR.md` 2.1.1 (the 6.0 s and 4,311 ms unchanged), `MAILBOX_SPLIT.md`, `SUBMODULES.md` with its
  diagram, `SPLIT_CONTROL_MEMORY.md`, the change log with its contents line, and the reboot and co-simulation READMEs.

## Authoritative references

- IEEE 1722.1-2021 6.2.4.2.2: a uniform distribution; "different hosts do not generate the same sequence"; a maximum
  length sequence of no less than 2^32 - 1; seeded "using the least significant (most rapidly varying) octets of the sum
  of the requestor's IEEE 802 MAC address and the local real time clock".
- Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.4, 5.6.3.5.5, 5.6.3.5.7, Tables 5.49 to 5.51.
- #970 and its ruling of 2026-11-25; `docs/reference/FR_NFR.md` 2.1.1; `sw/firmware/ctrl/adp/adp_mbx.h`, THE DRAW.

## How to get into the same state

```sh
git fetch origin 970-discovery && git switch 970-discovery
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4
python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 8
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <work>/ledger
python3 scripts/check_py_idiom.py && python3 scripts/gen_toc.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <work>/b8 --record-budget-findings --record-share-findings
```

| Check | Result |
|---|---|
| firmware gate, every suite; coverage ratchet | PASS (85 suite verdicts); PASS, 40 files |
| planted defects for the draw and the first advertisement | 28 of 28 caught; every host test is named by a plant |
| H9, H10 and B27 against the core pinned at `0ad0e518` | fail there, pass here |
| split boot simulation, 1x1 and 8x8 | PASS, 0 findings |
| platform images against the memory ledger | PASS at four points; against `c34e7d8b`, `rom` is +264 / +272 / +264 / +256 B; `sram`, tiles and `ctrl_plat` unchanged; the pin to `a795471c` adds nothing |
| twin and its plants; co-simulation; reboot simulation; hooks and budget harness self-tests; memory plan tests | PASS |
| CPU budget legs against the base, 1x1/1if | 75 probes paired, 0 misses on both sides, 0 passes over the share; composed maximum 1.465 -> 1.468 ms; 10 rows past 0.1 ms, -0.10 to +0.41 ms |
| CPU budget legs against the base, 8x8/1if | 90 probes paired, the same 7 known misses on both sides, 0 passes over the share; composed maximum 1.759 -> 1.820 ms; the egress ledger PASS |
| the load table (1x1/1if 0.512 against 0.70) and the flip check | the base's output, unchanged |
| the docs workflow's local gates, Python idiom and per-page contents included | 37 of 37 pass |

The budget legs' simulated hardware is the base's: the verilated sources differ only in path strings. Cycles per
instruction is not a cost measure in these legs. A group runs a fixed simulated time, so its instruction count follows
what the idle loop polls, which the draws change. At 8x8 the backlog groups' rows are up to 0.62 ms later, every one
within its budget. That rise comes with the per-LINK_UP sample: a build pinning `a795471c` alone sits at the base on
those rows.

## Known limitations / out of scope

- The first frames once lost on the bench in the first 1.2 to 1.45 s after a link-up were attributed on #970 to the
  test path, not the device. In the direct-cable run after the link partner's PHY interrupt fix, every
  ENTITY_AVAILABLE of 20 link-ups arrived (44 frames, consecutive `available_index`). The one frame lost was a MAAP
  PROBE: the device sent it as its link came up, about 1 ms before the partner's receive path came up. No change to
  ADP follows.
- ACMP's and MAAP's seeds are outside this change.
- The split boot simulation was run with `PYTHONHASHSEED=0`. The generated CSR map's ISA string can order differently
  from one generator run to the next (a separate issue).

## Definition of Done

- [x] New and changed behaviour has self-checking tests with planted defects
- [x] Required local verification passes (the table)
- [x] #1016 merged, and the tsn-c-stack change reviewed and merged (#40)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Candidate merge result validated per CONTRIBUTING.md
