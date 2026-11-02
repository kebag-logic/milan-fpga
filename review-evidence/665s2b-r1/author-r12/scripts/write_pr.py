#!/usr/bin/env python3
"""Write PR-BODY.md from the kept tables."""
from pathlib import Path
O = Path('$MANAGEMENT/2026-09-23/665s2b-a683o')
rows = (O / 'receipts/rows.md').read_text()
doc = Path('$LANES/665-s2b-cycles/docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
sec = doc[doc.index('### The estimate'):doc.index('### One CPU, measured')]
est = sec[sec.index('| Row |'):sec.index('The rows that would not fit')].strip()
fits = sec[sec.index('The rows that would not fit'):sec.index('So the last AECP')].strip()
one = doc[doc.index('### One CPU, measured'):doc.index("### gPTP's share")]
one_table = one[one.index('| Row |'):one.index('The cacheless core does not fit')].strip()
head = Path('/tmp/head.txt').read_text().strip()
sweep_tally = Path('/tmp/sweep_tally.txt').read_text().strip()
body = f"""[A683o]

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

REVIEW READY at `{head}`. Round 12 of lane S2b, restated for Mark II. No rebase, no force; the one merge of `dev-soft-core` `a68536fa` keeps both sides' behaviour.

Every measured row the CPU decides and every pass fits at 100 MHz, at both points, in both arms, with the two drafts staged and without them. The least margin is the 8x8 last SRP record's, 2.04 ms. The three egress-held rows stay with tsn-c-stack #26.

The 32x32 figures are an estimate, and they miss: the last AECP and SRP records and the per-pass share under every reading (section 14 of `SPLIT_CONTROL_MEMORY.md`).

## Linked Issue / roles

Relates to #665

Executor: `[A683o]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

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

{rows}

Out of context, the split CPU on `sys` closes at 100 MHz, WNS +1.605 ns, WHS +0.070 ns, 3,543 LUTs, 5,643 FFs, 9.5 tiles: 405 LUTs, 1,236 FFs and 5 tiles fewer than behind the crossing. The routed split image is lane S9's.

**The 1x1, 4 KiB windows.** At the CPU's 100 MHz, on a drained ring, all four commit their fifteen grandmaster changes with no record held. The composed maximum covers all four, so it is no longer partial: at least 40.25 ms, a lower bound while the two bound-talker windows close with SRP records unreleased.

**32x32, an estimate, not a measurement.** No such shape exists. U is the assigned four times 8x8/2if; L the line through 1x1/1if and 8x8/2if; S the slope at one interface, from a labelled scratch point.

{est}

{fits}

**One CPU, measured.** As built, the split placement already has one hart. The figures below are the split firmware on that hart, and on the SoC core as it ships, cacheless, on `sys` at 100 MHz, arm A. The cacheless core does not fit 8x8.

{one_table}

**gPTP, a labelled assumption.** 46 frames and 16 servo runs a second at 40,000 cycles each: 2.5 % of the CPU (1.2 to 6.2), 1.6 ms on a row, 0.8 ms on a pass. Not measured: no gPTP firmware is linked here. F6's stack in this harness, with these frames on both ports, would measure it. Section 14 gives the basis and what it does to Milan v1.2 4.2.6.2.6's 15 ms Pdelay turnaround.

## Authoritative references

- #665 and #640, "Updated 2026-10-31" and their 2026-10-31 and 2026-11-01 comments; the round 12 assignment (issuecomment-6514866239); the 20 ms decision (issuecomment-6495692075).
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2, NFR-SCOUT-01 and -03; `sw/firmware/ctrl/loop/ctrl_loop.h`, THE SHARE.
- PR #828's `MARK_II_AREA_PLAN.md` and `MARK_II_STREAM_ENGINES.md`, read only.
- IEEE 802.1AS-2011 with Cor1 and Cor2, as Milan v1.2 profiles it; Milan v1.2 4.2.6.2.6; IEEE 802.1Q-2018 10.7.11.

## How to get into the same state

```sh
git fetch origin
git checkout {head}
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

Evidence on the head: {sweep_tally}

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
"""
(O / 'PR-BODY.md').write_text(body)
print(len(body))
