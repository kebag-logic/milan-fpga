[A752d]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 4](#round-4)** — The round 4 ruling's items 1 to 5, item by item.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally, review ready: every gate rc 0 on clean clones of the head — `665-s15-32x32` -> `dev-soft-core`, head `936e0a566867aa648fb48e772a26fec99e3619c9`. The donor change for tsn-c-stack#31 is its own branch, `31-acmp-mask-width` at `c6013804d0fec6bc763a64b496f1a52d4a5d9f6a`, with its own PR.

- Workflows: 139 steps run, each rc 0; 226 not runnable here, each with a reason.
- The full sweep in four shards: 65 of 65 suites, 2,192,899 checks, 0 failures, 0 timed out.
- The firmware self-test and every mutant driver; `fw_coverage.py --check`; `test_builder.py --require-rv32`; `cd tests && behave`; the docs gates; `git diff --check` against the merge base.
- The harness on the resized layout, each point on its own clean clone (misses are recorded, not graded):

| Point | Groups graded | Refusals | T_svc misses (probe instances; paths) | Save groups | Build | Run |
|---|---:|---:|---|---|---|---|
| 1x1/1if | 18 | 0 | 34 of 141; 13 of 81 | run | 31.1 s, 358 MB peak | 39 min 30 s, 50 MB peak |
| 8x8/2if | 17 | 0 | 63 of 182; 31 of 129 | run | 34.8 s, 356 MB | 43 min 59 s, 47 MB |
| 32x32/2if | 17 | 0 | 90 of 182; 56 of 129 | 10 owed to #823 by name | 15.7 s, 358 MB | 53 min 29 s, 53 MB |

At 1x1/1if and 8x8/2if every `BUDGET`, `OWED` and summary line equals round 3's, and their scripts are the base's byte for byte. At 32x32/2if the same 90 probes miss T_svc as in round 3; only the owed row's figures moved, since it now fills the 51-record ring.

## Linked Issue / roles

Relates to #665
Relates to #859

#859 stays open (the round 4 ruling, item 4): the per-item costs this base cannot measure (`events`, `events_none`, `polls_least`, `base`, `event.*` and `item.*` in S2b round 22's projection) stay owed there.

Executor: `[A752d]` (rounds 1 to 3: `[A752]`, `[A752b]`, `[A752c]`)
Internal cleared-context reviewer: `[R807]`
External reviewer: `[R808]`

## Description

The 32x32 shape (#859, part of #665's Mark II split): a 32x32 shape on two AVB interfaces, built for simulation only and without saved state, run through S2's CPU budget harness.
Rounds 1 to 3 built it under the round 2 ruling on #859 and synced it with `dev-soft-core` `1d6bf555`; round 4 answers R807-1 and R808-1 under the round 4 ruling (next section).

| Piece | What this PR does |
|---|---|
| Without saved state | `configs/endstation_ax7101_32x32.yaml` declares `simulation_only: true` and `saved_state: none`. The end-station builder refuses `saved_state: none` on any shape that does not declare `simulation_only`, and refuses the simulation shape every routed output (`--write-rtl`, `--write-fragment`, `srp.rtl_table`). Its argv carries `--simulation-only`, with which `milan_soc.py` refuses `--build` and `--load`. The firmware links no store, no flash port and no record space (`CTRL_SAVED_STATE_NONE`). The harness reports each save group by name as owed to #823 and grades none |
| Contract layout at the shape | `gen_mailbox.py --variant-interfaces 2 --variant-shape CONFIG` lays the contract out from the shape's per-interface streams, each interface's own by ordinal (17 on the primary, with both CRF streams), and sizes its ACMP transmit ring from the census rule (1,024 words at `0x7000`). The tracked 2.4 outputs are byte-identical. No major contract version |
| Datapath guards | The five guards are recorded in the census as owed to #640 |
| Lifted by a rule | ACMP at 33 sinks and sources through `ACMP_MAX_SINKS` and `ACMP_MAX_SOURCES` from the generated counts; the SRP pool from its formula (144,832 B); a simulation-only memory map in `ctrl_memory.py` (`rom` 256 KiB, `sram` 512 KiB), the shipped map unchanged and every byte over the 56-RAMB36 budget ledgered to #640 |
| The point | `ctrl_service_budget/run.py --point 32x32`: every non-save group graded; T_svc misses recorded, not graded, beside 1x1/1if and 8x8/2if |

The existing shapes are unchanged: every builder output, the three firmware entity headers and the 8x8 two-interface mailbox variant of the five shipped configs equal the base generators' (79 outputs; builder gate 41 pins the 1x1 and 8x8 ones), the firmware images at 1x1/1if, 8x8/1if and 8x8/2if link to the base's bytes, and their harness scripts are unchanged.

## Round 4

The round 4 ruling on #859 (issuecomment-6746289265), on R807-1 and R808-1 (both NEGATIVE at `7aa6ef0c`); owners filed by the manager: kebag-logic/tsn-c-stack#31, #865 and #866.

1. **The ACMP owed-release mask (R807-1-F1, R808-1-F1).** At the pin this branch keeps, `70936b77`, tsn-c-stack's mask is one `uint32_t` (`third_party/tsn-c-stack/include/acmp.h:400`). `bind_response` and the unbind response shift `1u << k` by sink (`src/acmp.c:816`, `:871`), and the change-owed and release loops read `(release >> k) & 1u` (`:310`, `:1225`). The 32x32 image builds ACMP at 33 sinks, so these shifts reach 32, which C11 leaves undefined (6.5.7p3).
   **What the RV32 image does:** its shifts are `sll` and `srl` with the count in a register (`bind_response` `sll a3,a3,s3`; `transmit`'s and `acmp_poll`'s loops `srl`; image `2e47b49e...`). RV32I uses the count's low five bits, so sink 32 (the CRF sink) and sink 0 share one release bit. An owed response for either holds the change notices of both, and its acceptance releases both: each sink holds the other's notices. The owner is tsn-c-stack#31, in place of the closed #653.
   The donor change is drafted for tsn-c-stack#31 on its own branch (head `c6013804`, from `main` `ea4af6f`; reviewed and merged on its own). It sizes the mask from `ACMP_MAX_SINKS`, refuses at build time a mask that cannot hold every sink, and adds a 33-sink test under `-fsanitize=shift,undefined`. R807-1's probe exits 0 against it and 1 against the pin. This PR does not move the pin, so the image the harness measures carries the alias, and no harness script binds a sink past 1. Round 5 syncs onto the pin move.
2. **The ACMP transmit ring at the shape (R808-1-F2, R807-1-F2).** `gen_mailbox.shape_variant` sizes the layout's ACMP transmit ring from the census rule: a PROBE_TX_COMMAND from every bound sink in one pass (Milan v1.2 5.5.2.3), 33 records of 20 words, in the smallest power of two that holds them, 1,024 words (`acmp_tx_words`).
   The form is the ring: a ring is a power of two aligned to its size, and `with_tx_ring` places it at `0x7000`, the lowest such 4 KiB span the layout leaves free. The owed-frame count is not a form this pin allows, because `ACMP_OWED_MAX` is a fixed tsn-c-stack definition (`acmp.h:164`).
   `gen_mailbox.py --selftest` requires the shape's ring to hold the rule's 33 records and refuses the layout with the contract's ring by its words; `shape_findings` refuses such a layout for every build of the shape. The tracked outputs are unchanged (`--check`: 0 findings).
   The ring ends at the window's last byte. The generated decode bounded each ring with `off_w < AW2_C'(base + 4 * words)`, a 15-bit cast for the 32 KiB window, which wraps to 0 there, so at the round's first head no host write reached the ring and no ACMP frame left (the 32x32 point refused three groups). The skeleton now decodes a ring that ends at the window's top with no upper bound, and `--crosscheck` evaluates every ring's decode at its first and last word; a self-test arm restores the wrapping bound and requires the finding. No tracked ring ends at the top, so the tracked outputs are unchanged.
   The harness reads each point's transmit records from its build's layout (`grade.tx_rings`). Its owed row fills the layout's ring with the egress held, one admitted ACMP burst (12 commands) at a time: 51 responses at 32x32, and at 1x1 and 8x8 the unchanged 12. The 32x32 point was re-run on the resized layout (Status).
   **Ring items:** met, the ACMP transmit ring at 32x32, sized from its rule. Owed, the ACMP receive ring (12 of its bucket's 16 at every shape) and the MAAP receive ring (7 of 8), both to #865, which the census rows link. Every other ring and bucket at the shape is the contract's, as at every shape.
3. **Census owners (R808-1-F3, R807-1-F3).** The census adds the AEM ROM's 16-bit store, 65,536 B less 64 B of MVU scratch: 4,527 B at 1x1/1if, 11,753 B at 8x8/2if and 41,465 B at 32x32/2if. On the shipping 1x1 TDM8 interface, the builder refuses a 32x32 model at 87,545 B + 64 B (972 descriptors, 800 AUDIO_CLUSTERs). The shape takes the 8x8's TDM32 interface so that the 8x8 two-interface measurement groups scale by the stream count alone.
   #866 owns the ROM store, the 64 KiB `aem` flash slot (69,488 B), COUNTERS_CHANGED (16 bits a direction against 33), SRP's declaring every source on each interface, and the second AVB_INTERFACE (#394 is closed). Section 5 gives the hook harness its reasons: the platform image has no simulation-only map (#640), and its counter push crosses COUNTERS_CHANGED (#866). The F5 stream counters' point is #866's COUNTERS_CHANGED item. The datapath guard is cited at `hdl/milan/milan_datapath.sv:5354-5358`.
4. **Item 5's costs (R807-1-F4).** The costs this base measures the same way (`record.*`, `rebuild`, `centisecond`), measured on the round 4 32x32 image (`2e47b49e...`), beside S2b round 22's projection with the error:

   The 32x32/2if image: `ctrl_app.elf` SHA-256 `2e47b49efd9262d3dc1628c355ee646e24a2b758ae550c12ee8bb07c6e2facae`, the one this head links (its instrumented leg adds trace tables to the testbench, not to the image). Stated costs throughout: the most measured plus 5 %, rounded up to 5 us at 100 CPU cycles a microsecond. S2b's projection is arrivals2.py's line through its 1x1/1if and 8x8/2if costs, in streams 2 and 16, at 64. The error is projected less measured.

   | Cost | S2b 1x1/1if, us | S2b 8x8/2if, us | S2b projected 32x32/2if, us | Measured 32x32/2if, us (most cycles, instances) | Error, us |
   |---|---:|---:|---:|---:|---:|
   | `record.srp` | 250 | 395 | 892.1 | 1,085 (102,945, 70) | -192.9 |
   | `record.aecp` | 200 | 255 | 443.6 | 2,245 (213,463, 148) | -1,801.4 |
   | `record.acmp` | 280 | 430 | 944.3 | 2,365 (224,785, 127) | -1,420.7 |
   | `record.adp` | 105 | 230 | 658.6 | 1,920 (182,813, 54) | -1,261.4 |
   | `record.maap` | 90 | 125 | 245.0 | 615 (58,305, 30) | -370.0 |
   | `centisecond` | 120 | 390 | 1,315.7 | 1,470 (139,926, 7,354) | -154.3 |
   | `rebuild` | 290 | 690 | 2,061.4 | 7,215 (687,033, 41) | -5,153.6 |

   Every projection is below the measured cost. The other costs of the projection (`events`, `events_none`, `polls_least`, `base`, `event.*`, `item.*`) are not measured on this base, each for the reason in Known limitations, and #859 stays open for them.

5. **Residue and suggestions.**
   - `endstation_builder.py:201` reads `#: at that shape (#859).` (R807-1-R1, R808-1-F5).
   - The census's aecp and srp transmit row reads "AECP's change-notice retries and the participants' MRPDUs" (R808-1-F6).
   - `SPLIT_CONTROL_MEMORY.md` section 8's fit is at `41f963d5` (rom need 155,196 B, total 465,740 B; R807-1-S1, R808-1-F4).
   - Gate 39 plants the `srp.rtl_table` refusal; `ctrl_memory.simulated()` refuses an image off its map under its own rule, `simulation identity`, with its documented row, refusal arm and mutant (R807-1-S2).
   - `gen_mailbox.py --selftest` compiles the ACMP adapter against the layout one sink entry short and requires both static assertions to refuse it (R808-1-F7).

## Authoritative references

- #859: the round 4 ruling and its owners comment; the round 2 ruling (items 1 to 5) and the assignment.
- [32x32 shape census](docs/design/SHAPE_32X32_CENSUS.md), sections 2 to 5.
- The mailbox contract `sw/mailbox/mailbox.yaml` and [the split mailbox](docs/design/MAILBOX_SPLIT.md).
- [Split control memory](docs/design/SPLIT_CONTROL_MEMORY.md), sections 3 and 8.
- [The CPU budget harness](tb/verilator/ctrl_service_budget/README.md) and FR_NFR.md 3.4.1 (T_svc).
- Milan v1.2 5.5, 5.5.2.2 and 5.5.2.3 (the owed response before its notice; the ACMPDU; the probes in one pass); C11 6.5.7p3.
- Milan v1.2 Tables 4.3, 5.26 and 5.50 and 5.4.5.3; IEEE 1722.1-2021 6.2.2.5 and Figure 6-1; IEEE 1722-2016 B.3.4 and Table B.8; IEEE 802.1Q-2018 10.7.4.1 and Table 10-7, for the rings and buckets.
- Owners: kebag-logic/tsn-c-stack#31 (the mask), #865 (the receive rings), #866 (the crossed limits), #823 (the record space at the shape), #640 (the datapath at the shape and the 56-RAMB36 budget), #810 (S2b, which grades the rows).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s15-32x32
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness needs the [capture prerequisites](tb/verilator/nvm_capture_cpu/README.md#run): the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o /tmp/shape32
python3 sw/builder/test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged
python3 scripts/check_py_idiom.py
python3 sw/builder/test_soc_options.py
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 sw/mailbox/gen_mailbox.py --variant-interfaces 2 --variant-shape configs/endstation_ax7101_32x32.yaml --out /tmp/shape32-mbx
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/build.py /tmp/budget-32x32 endstation_ax7101_32x32 2
python3 -B tb/verilator/ctrl_service_budget/run.py --point 32x32 --build-dir /tmp/budget-32x32 --reuse-build --record-budget-findings
python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir /tmp/nvm-target-32x32
```

Expected result / pass criteria: every command exits 0 except the last. The builder writes the 32x32 shape's outputs and no routed output, and the tree stays clean. The `test_builder.py` subset prints "ALL GATES PASS" for its 3 of 108 gates: gate 39 with 3/3 plants turned red, gate 41 with 1/1. `check_py_idiom.py` exits 0. `test_soc_options.py` and `test_ctrl_memory.py` print "RESULT: PASS". `gen_mailbox.py --check --crosscheck` prints "gen_mailbox: 0 finding(s)"; `--selftest` prints "selftest: 0 arm(s) failed", among its arms the 32x32 layout's ACMP transmit ring (51 records of the 33 one pass sends), the layout with the contract's ring refused, the wrapping decode bound refused and the ACMP adapter refused against a layout one sink entry short. The variant's `mbx_contract.h` defines `MBX_CH_ACMP_TX_BASE 0x7000u` and `MBX_CH_ACMP_TX_WORDS 1024u`. The harness self-test prints "self-test: 0 failures". The 32x32 run ends "17 groups graded, 0 refusals, 90 T_svc misses (90 of 182 probe instances, 56 of 129 paths), 10 save groups owed to #823". The last command lists the 10 save groups owed to #823 and exits 1, building nothing.

## Known limitations / out of scope

- The shape is for simulation only: no route, no bitstream, no flash. The image build refuses to route or load it.
- The tsn-c-stack pin is not moved here, so the 32x32 image carries the owed-release alias of item 1 (sinks 0 and 32 share a bit) until round 5 syncs onto the pin move to tsn-c-stack's `main`. The donor change is tsn-c-stack#31's own PR.
- The record space at 32x32 is #823's: no save group runs at the shape, and each is reported by name as owed to #823.
- The datapath at 32x32 and the 56-RAMB36 budget are #640's: the five guards and every byte over budget are recorded as owed to #640.
- The ACMP and MAAP receive rings hold less than their bucket's burst at every shape (#865); the crossed limits without an owner before this round are #866's.
- S2b round 22's `events`, `events_none`, `polls_least`, `base`, `event.*` and `item.*` costs are not measured here. The first three cut a pass at `ctrl_loop`'s `service_rx`, which this base's image inlines; the rest are graded by S2b round 22's own head's event and poll graders, which this base does not carry. #859 stays open for them.
- The twin runs at the shipping 1x1 shape only; it does not take the 32x32 shape.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
