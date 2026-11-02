[A683p]

## Contents

- **[Status](#status)** — REVIEW READY at the head below: `dev-soft-core` `a68536fa` merged, the split CPU on `sys` at 100 MHz, every measured row and pass fitting. `665-s2b-cycles` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `{{HEAD}}`. Round 13 of lane S2b, on round 12's `c954b8a9`: commits added on top, no rebase, no force, no merge.

Every measured row the CPU decides and every pass fits at 100 MHz, at both points, in both arms, with the two drafts staged and without them, a save in progress included: a save's flash step is now taken only in a pass that took no input and has 1.0 ms of the 2.0 ms share left. The least margin is the 8x8 last SRP record's, {{SRP_MARGIN}} ms, with a save in progress. The three egress-held rows stay with tsn-c-stack #26.

The 32x32 figures are an estimate, and they miss: the last AECP and SRP records and the per-pass share under every reading (section 14 of `SPLIT_CONTROL_MEMORY.md`).

## Linked Issue / roles

Relates to #665

Executor: `[A683p]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

{{ROUND13}}

### Round 12

| Piece | Change | Why |
|---|---|---|
| Merge | `dev-soft-core` `a68536fa`, contract 2.4 and dev's #806, #814, #818, #787 | Assigned. Three semantic conflicts follow below; each is its own commit |
| Split CPU clock | `milan_soc.CTRL_CPU_CD` `sys`, `ctrl_cpu_domain` refuses any other, no CPU clock of its own, no crossing | The owner's decision of 2026-10-30. The all-fabric CPU and the Milan datapath clock do not change |
| CPU budget harness | Built through `ctrl_cpu_cd`; `build.json` records `cpu_cd`, `cpu_hz`, `sys_hz`; a CPU anywhere else is refused, built or reused; the `--cpu-hz` option is retired | One clock, and no figure at another presented as the product's |
| Split boot simulation | The merged S3 harness still drove the CPU from the Milan clock: now `ctrl_cpu_cd`, the boot graded against the approved T_svc = 20 ms | Merge conflict in meaning: boot at 1x1 24.660 ms, 8x8 64.271 ms |
| Platform image | `ctrl_plat_image.py` built RV32I against the split link: now the split hart's flags and audits, with the record mover and the word-wide primitives; `ctrl_memory.LEDGERED`'s `ctrl_plat` size re-measured, 19,944 B, 58.0 RAMB36 within the ledgered 59.0 | Merge conflict in meaning: it no longer linked |
| SRP link change | `reset_interface` withdraws and destroys in the pass that takes it; the next pass's poll builds; SRP's receive waits; a pass of link edges builds once | It was the one 8x8 pass over the 2.0 ms share, 2.21 and 2.22 ms. Events a pass do not set it (labelled experiments: six 2.207 ms, four 2.108 ms) |
| Saved-state read-back | Blank check and verify read 128 bytes a step (`NVM_READ_BYTES`) | A whole page through the product's uncached window and lwSRP's periodic work in one tick put an 8x8 pass at 2.26 ms. A save's read-back takes twice as many ticks |
| Harness flash window | Uncached and not executable but in the hybrid-XIP arm, refused otherwise | The cached window read the flash through the data cache, which the product never does: 12.39 ms at 8x8 and 4.07 ms at 1x1 for one pass in each save |
| Harness AECP pacing | Each frame waits a refill period of the channel's token bucket | At 100 MHz the groups outran the refill and the filter refused the frames past its burst: 3 refused probes at 1x1, 15 at 8x8 |
| The two refused windows | Each backlog window opens on a drained event ring; its table and any refusal give the records held at its opening | The window's definition was wrong, not the firmware: it named a population only a drained ring can take, and waited a fixed time for one. With k records held only 16 - k + 1 of the fifteen grandmaster changes commit |
| Docs | `ARCHITECTURE_HW_SW_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` sections 5, 11 to 13 and new 14, both harness READMEs, `MAILBOX_SPLIT.md`'s access bounds, the SRP, store and platform READMEs | Every figure names its clock. The bare-metal all-fabric image keeps its own clock contract |

The rows, each family against min(T_svc = 20 ms, its 10 % ceiling).

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

| Row | Bound, ms | 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 / 0.75 | 0.65 / 0.67 | 1.30 / 1.31 | 1.21 / 1.22 |
| ADP record, first | 20 | 0.79 / 0.80 | 0.70 / 0.71 | 1.34 / 1.35 | 1.25 / 1.26 |
| MAAP record, first | 20 | 0.77 / 0.78 | 0.68 / 0.69 | 1.33 / 1.33 | 1.24 / 1.24 |
| AECP record, first | 20 | 0.78 / 0.79 | 0.69 / 0.70 | 1.34 / 1.34 | 1.25 / 1.25 |
| SRP record, first | 18 | 2.79 / 2.80 | 2.50 / 2.56 | 5.35 / 5.29 | 4.99 / 5.00 |
| ACMP record, last | 20 | 5.16 / 5.06 | 4.34 / 4.52 | 7.76 / 7.98 | 7.42 / 7.30 |
| ADP record, last | 20 | 3.65 / 3.59 | 3.18 / 3.22 | 5.81 / 5.85 | 5.26 / 5.08 |
| MAAP record, last | 20 | 3.68 / 3.63 | 3.22 / 3.26 | 5.80 / 5.84 | 5.30 / 5.12 |
| AECP record, last | 20 | 9.67 / 10.02 | 8.72 / 9.48 | 14.41 / 15.16 | 13.79 / 14.05 |
| SRP record, last | 18 | 9.95 / 10.00 | 9.49 / 9.68 | 15.88 / 15.96 | 14.84 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.45 / 3.47 | 3.03 / 3.11 | 6.51 / 6.73 | 6.19 / 6.21 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.73 / 2.74 | 2.42 / 2.45 | 3.53 / 4.19 | 3.95 / 4.11 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.12 / 0.12 | 0.11 / 0.10 | 0.25 / 0.23 | 0.23 / 0.09 |
| an event behind 15 others | 20 | 0.88 / 0.89 | 0.78 / 0.80 | 1.44 / 1.45 | 1.35 / 1.35 |
| AECP record, last, in the owed window | 20 | **62.66** / **62.73** | **62.75** / **62.77** | **64.99** / **64.95** | **64.94** / **65.01** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **61.93** | **61.94** / **61.95** | **63.68** / **63.93** | **63.91** / **63.68** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

The share is 2.0 ms. Passes over it of the work passes run, longest in ms, arm A / arm B:

| 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---:|---:|---:|---:|
| 0 of 1277, 1.07 / 0 of 1250, 1.07 | 0 of 1279, 0.98 / 0 of 1250, 0.98 | 0 of 1319, 1.97 / 0 of 1286, 1.92 | 0 of 1310, 1.77 / 0 of 1302, 1.77 |



Out of context, the split CPU on `sys` closes at 100 MHz, WNS +1.605 ns, WHS +0.070 ns, 3,543 LUTs, 5,643 FFs, 9.5 tiles: 405 LUTs, 1,236 FFs and 5 tiles fewer than behind the crossing. The routed split image is lane S9's.

**The 1x1, 4 KiB windows.** At the CPU's 100 MHz, on a drained ring, all four commit their fifteen grandmaster changes with no record held. The composed maximum covers all four, so it is no longer partial: at least 40.25 ms, a lower bound while the two bound-talker windows close with SRP records unreleased.

**32x32, an estimate, not a measurement.** No such shape exists. U is the assigned four times 8x8/2if; L the line through 1x1/1if and 8x8/2if; S the slope at one interface, from a labelled scratch point.

| Row | Bound, ms | 1x1/1if | 8x8/1if | 8x8/2if | U: 4 x 8x8/2if | L: the line, 1x1/1if to 8x8/2if | S: the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.15 | 1.31 | 5.2 | 3.2 | 2.7 |
| ADP record, first | 20 | 0.80 | 1.20 | 1.35 | 5.4 | 3.3 | 2.7 |
| MAAP record, first | 20 | 0.78 | 1.18 | 1.33 | 5.3 | 3.2 | 2.7 |
| AECP record, first | 20 | 0.79 | 1.19 | 1.34 | 5.4 | 3.2 | 2.7 |
| SRP record, first | 18 | 2.80 | 4.57 | 5.35 | **21.4** (+3.4) | 14.1 | 11.4 |
| ACMP record, last | 20 | 5.16 | 7.23 | 7.98 | **31.9** (+11.9) | 17.7 | 15.1 |
| ADP record, last | 20 | 3.65 | 4.92 | 5.85 | **23.4** (+3.4) | 13.4 | 10.2 |
| MAAP record, last | 20 | 3.68 | 4.99 | 5.84 | **23.3** (+3.3) | 13.2 | 10.3 |
| AECP record, last | 20 | 10.02 | 13.12 | 15.16 | **60.6** (+40.6) | **32.8** (+12.8) | **25.8** (+5.8) |
| SRP record, last | 18 | 10.00 | 14.42 | 15.96 | **63.8** (+45.8) | **36.4** (+18.4) | **31.1** (+13.1) |
| An ACMP command behind a full ACMP ring | 20 | 3.47 | 5.64 | 6.73 | **26.9** (+6.9) | 17.9 | 14.2 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.74 | 3.84 | 4.19 | 16.8 | 9.2 | 8.0 |
| An event behind 15 others | 20 | 0.89 | 1.29 | 1.45 | 5.8 | 3.4 | 2.8 |
| The longest work pass | 2 | 1.07 | 1.58 | 1.97 | **7.9** (+5.9) | **5.0** (+3.0) | **3.7** (+1.7) |

The rows that would not fit, and by how much:

- **AECP record, last, under S, L and U:** over by 5.8, 12.8 and 40.6 ms.
- **SRP record, last, under S, L and U:** over by 13.1, 18.4 and 45.8 ms.
- **The longest work pass, under S, L and U:** 3.7, 5.0 and 7.9 ms, over the 2.0 ms share by 1.7, 3.0 and 5.9 ms.
- **Under U alone:** SRP record, first by 3.4 ms, ACMP record, last by 11.9 ms, ADP record, last by 3.4 ms, MAAP record, last by 3.3 ms, an ACMP command behind a full ACMP ring by 6.9 ms.

**One CPU, measured.** As built, the split placement already has one hart. The figures below are the split firmware on that hart, and on the SoC core as it ships, cacheless, on `sys` at 100 MHz, arm A. The cacheless core does not fit 8x8.

| Row | Bound, ms | Split CPU, 1x1 | Cacheless RV32IM, 1x1 | Cacheless RV32I, 1x1 | Split CPU, 8x8 | Cacheless RV32IM, 8x8 | Cacheless RV32I, 8x8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.56 | 1.58 | 1.30 | 2.90 | 2.93 |
| ADP record, first | 20 | 0.79 | 1.60 | 1.62 | 1.34 | 2.94 | 2.98 |
| MAAP record, first | 20 | 0.77 | 1.58 | 1.60 | 1.33 | 2.92 | 2.96 |
| AECP record, first | 20 | 0.78 | 1.59 | 1.61 | 1.34 | 2.93 | 2.97 |
| SRP record, first | 18 | 2.79 | 5.44 | 5.63 | 5.35 | 11.37 | 11.72 |
| ACMP record, last | 20 | 5.16 | 9.98 | 10.45 | 7.76 | 16.08 | 16.09 |
| ADP record, last | 20 | 3.65 | 7.14 | 7.78 | 5.81 | 11.70 | 11.77 |
| MAAP record, last | 20 | 3.68 | 7.18 | 7.81 | 5.80 | 11.71 | 11.75 |
| AECP record, last | 20 | 9.67 | 17.34 | 19.76 | 14.41 | **26.83** | **28.51** |
| SRP record, last | 18 | 9.95 | 17.98 | **21.63** | 15.88 | **30.26** | **34.52** |
| An ACMP command behind a full ACMP ring | 20 | 3.45 | 6.87 | 7.06 | 6.51 | 14.29 | 14.42 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.73 | 5.50 | 5.94 | 3.53 | 8.75 | 7.78 |
| An event behind 15 others | 20 | 0.88 | 1.82 | 1.84 | 1.44 | 3.16 | 3.20 |
| Passes over the 2.0 ms share, longest ms | 2 | 0 of 1277, 1.07 | **3 of 1267, 2.14** | **3 of 1270, 2.35** | 0 of 1319, 1.97 | **62 of 1314, 3.61** | **64 of 1315, 3.85** |

**gPTP, a labelled assumption.** 46 frames and 16 servo runs a second at 40,000 cycles each: 2.5 % of the CPU (1.2 to 6.2), 1.6 ms on a row, 0.8 ms on a pass. Not measured: no gPTP firmware is linked here. F6's stack in this harness, with these frames on both ports, would measure it. Section 14 gives the basis and what it does to Milan v1.2 4.2.6.2.6's 15 ms Pdelay turnaround.

## Authoritative references

- #665 and #640, "Updated 2026-10-31" and their 2026-10-31 and 2026-11-01 comments; the round 12 assignment (issuecomment-6514866239); the 20 ms decision (issuecomment-6495692075).
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2, NFR-SCOUT-01 and -03; `sw/firmware/ctrl/loop/ctrl_loop.h`, THE SHARE.
- PR #828's `MARK_II_AREA_PLAN.md` and `MARK_II_STREAM_ENGINES.md`, read only.
- IEEE 802.1AS-2011 with Cor1 and Cor2, as Milan v1.2 profiles it; Milan v1.2 4.2.6.2.6; IEEE 802.1Q-2018 10.7.11.

## How to get into the same state

```sh
git fetch origin
git checkout c954b8a91e720f87d2dfa9294c8501058dc55df3
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/builder/test_builder.py --require-rv32
```

Expected result / pass criteria: the self-test reports 0 failures and every mutant caught. Each point grades every group with 0 refusals, 0 work passes over the 2.0 ms share and only the three egress-held paths over budget, so without `--record-budget-findings` a run exits 1 on those alone.

Evidence on the head: the full sweep as four shards, 65 of 65 suites, 2,613,655 checks, 0 failures.

## Known limitations / out of scope

- **The 32x32 rows.** An estimate that misses, listed above. Nothing here builds 32x32.
- **For the owner, none decided here:** which lever closes the last AECP and SRP records and the share at 32x32 (the admitted rings and buckets, D4(b)'s two records a pass, the share, the per-stream polls); which CPU lever 4 means, since the split placement already has one hart; a clock past 100 MHz or a second hart if the firmware's levers do not close it.
- **A pass no group stages:** a save's read-back step, 0.70 ms, in the same pass as a composed window's heaviest, 1.97 ms, would be about 2.67 ms. Derived, not measured; the rows' margin holds it.
- **The three egress-held rows** stay with tsn-c-stack #26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one.
- The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (this round's are; #665 stays open)
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
