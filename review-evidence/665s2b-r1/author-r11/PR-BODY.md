[A683m]

## Contents

- **[Status](#status)** — STOP: at the product's split CPU clock, 50 MHz, the 8x8 last AECP and SRP records miss their bounds, and 8x8 passes miss the per-pass share. At 1x1 every row and pass fits. `665-s2b-cycles` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions it needs.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOP at `c36a76405fc3e98833a6c5649f81eaba0900e375`: seven commits on `f884c7e9`. The earlier rounds' commits stay; nothing was rebased.

This round answers R711-1 and R712-1. Every figure below names its CPU clock. The product clocks the split CPU from the Milan clock, 50 MHz, with its bus at 100 MHz. The 100 MHz CPU figures earlier rounds published were at a test clock, and this PR no longer presents them as the product's.

- **At the product's 50 MHz:**
  - 1x1/1if: every row the CPU decides fits, and every pass fits the 2.0 ms per-pass share. The least margin is the last SRP record's, 17.81 ms against 18.
  - 8x8/2if: the last AECP record takes 24.02 to 25.61 ms against 20, and the last SRP record 25.45 to 28.25 ms against 18, with the drafts staged or not. In each run, 23 to 32 work passes are over the share, the longest 3.47 ms.
- **At the labelled 100 MHz option:** every row the CPU decides fits at both points, as in round 10. One or two 8x8 passes are over the share, the longest 2.30 ms.
- **The exit:** this round is REVIEW READY only if every CPU-decided row and every pass fits at 50 MHz. They do not, so this is a STOP, with the residual of each row and pass below. The split CPU's clock is with the owner (#665 issuecomment-6508196970).
- **Gates:** see "How to validate". Every one is rc 0 at the head, or names what changed since. The full sweep ran as four shards.

## Linked Issue / roles

Relates to #665

Executor: `[A683m]`
Internal cleared-context reviewer: to be named
External reviewer: to be named

## Description

| Commit | Finding | What and why |
|---|---|---|
| `f52e65a9` | R711-F2 = R712-F1; R711-F3 | **The record mover's length.** `KL_mbx_dma` formed its word count in 12 bits, so the length field's 4093 to 4095 wrapped to zero words. A receive then held the host port forever, and a transmit issued an oversized burst. The sum is now in 13 bits, so every length the field takes moves its whole words, at most 1,024, within the burst and byte contract. No refusal is needed. The bench gains D10: 4092 to 4095 in both directions across the ring's end, each followed by a CPU access and a recovery transfer. It also gains checks for R711's three escaping plants: a held partial write still refused, a move started beside a CPU access moving its own bytes, and no burst after an error on a burst's first beat. The host model now drives noise on an unanswered cycle. The 17 plants are kept and four added: 21 of 21 caught. |
| `56f563e3` | R711-F4 | **The driver's record-mover arm under test.** `test_mbx_dma_driver.cpp` builds `mbx.c` as the split image builds it, over a register model of the mover written from its register contract. It covers a record moved and released, ERR on receive resynchronising, a frame moved and committed, ERR on transmit not committed, and a frame off a word taking the word loop. It has eight plants, and the coverage ratchet now records the arm (`mbx.c` 330/330 lines and 164/164 branches; `plat/mbx_dma.h` 10/10 and 4/4). |
| `c4ed271f` | R711-F1; R712-F2 | **The clock and the per-pass share.** By default the harness runs the split CPU at the product's split CPU clock, the point's `milan_clk_hz`. `--cpu-hz` is a labelled option, never the default. `build.json` records `cpu_hz`, `product_cpu_hz`, `cpu_clock` and `cpu_hz_option`, a reused build at another clock is refused, and every table and run line names the clock. Every work pass is held to the per-pass share, SRP's 18 ms over nine passes, 2.0 ms (`share.py`), apart from the rows. A pass over it fails the run, even when every row fits, unless `--record-share-findings` records it. The harness self-test has nine new checks and eleven new mutants: 118 checks, 91 mutants caught. |
| `37e200e6` | R711 residue R1, R2 | Wording: `ctrl_mem.c`'s cycle figures are the cacheless RV32I core's, and the split core's uncached side is its mailbox window. The harness README states RV32IM and the split's caches (in `c4ed271f`). |
| `cf0f978b` | — | The firmware boundary gate refused `share.py`, which names `ctrl_loop.h` by path, until it was classified as compiling nothing. |
| `b58274ad` | R711-F1; R712-F2 | `SPLIT_CONTROL_MEMORY.md` section 13 has a new subsection, "At the product's clock, and the per-pass share", with every row and pass at both clocks and the split experiment. Sections 11 to 13 call their 100 MHz figures a test clock. The mover's paragraph is updated. |
| `c36a7640` | — | The eight plants are named `mover-*`: the bare-metal scope gate keeps `dma-rx`, `dma-tx` and the DMA ring for the retired host plane (#259). |

**Every composed row at the product's split CPU clock, 50 MHz, bus 100 MHz** (worst instance over the four backlog groups, ms, arm A / arm B, bold over its own bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 8.65 / 8.90 | 7.64 / 7.46 | 14.37 / 14.72 | 13.79 / 13.80 |
| ADP record, last | 20 | 6.08 / 6.38 | 5.51 / 5.36 | 11.20 / 11.23 | 10.59 / 10.61 |
| MAAP record, last | 20 | 6.11 / 6.42 | 5.50 / 5.34 | 11.19 / 11.21 | 10.57 / 10.59 |
| AECP record, last | 20 | 15.95 / 17.05 | 14.87 / 15.76 | **25.02** / **25.61** | **24.02** / **24.11** |
| SRP record, last | 18 | 17.81 / 17.02 | 16.34 / 16.26 | **28.25** / **27.25** | **25.66** / **25.45** |
| An ACMP command behind a full ACMP ring | 20 | 6.83 / 6.78 | 6.01 / 6.09 | 13.57 / 13.60 | 12.71 / 12.72 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 4.55 / 4.88 | 4.38 / 4.26 | 7.63 / 7.87 | 7.32 / 7.23 |
| An event behind 15 others | 20 | 2.06 / 2.06 | 1.88 / 1.89 | 3.63 / 3.64 | 3.46 / 3.48 |
| AECP record, last, in the owed window | 20 | **64.73** / **64.67** | **64.66** / **64.65** | **68.53** / **68.46** | **68.71** / **68.75** |
| A response with 7 frames owed ahead of it | 20 | **63.41** / **63.33** | **63.35** / **63.33** | **66.26** / **66.20** | **66.41** / **66.45** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

**The same rows at the labelled 100 MHz option** (`--cpu-hz 100000000`, bus 100 MHz). These are round 10's figures: every probe's CPU cycles at 1x1 arm A are identical to round 10's variant-based leg.

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.51 / 5.30 | 4.60 / 4.76 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, last | 20 | 3.93 / 3.77 | 3.28 / 3.41 | 6.67 / 6.69 | 6.31 / 6.33 |
| MAAP record, last | 20 | 3.97 / 3.81 | 3.26 / 3.44 | 6.65 / 6.68 | 6.29 / 6.32 |
| AECP record, last | 20 | 10.25 / 10.43 | 9.36 / 9.98 | 15.10 / 15.84 | 13.74 / 14.61 |
| SRP record, last | 18 | 10.53 / 10.40 | 9.97 / 10.19 | 16.95 / 16.32 | 15.60 / 15.40 |
| An ACMP command behind a full ACMP ring | 20 | 4.07 / 4.04 | 3.64 / 3.70 | 8.13 / 8.15 | 7.64 / 7.45 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 3.02 / 2.87 | 2.58 / 2.60 | 4.13 / 4.32 | 3.33 / 4.03 |
| An event behind 15 others | 20 | 1.24 / 1.23 | 1.14 / 1.15 | 2.09 / 2.10 | 2.01 / 2.02 |
| AECP record, last, in the owed window | 20 | **62.81** / **62.90** | **62.84** / **62.83** | **65.03** / **64.94** | **65.02** / **65.09** |
| A response with 7 frames owed ahead of it | 20 | **61.99** / **62.06** | **62.01** / **62.00** | **63.70** / **63.64** | **63.69** / **63.74** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

**The per-pass share**, 2.0 ms of CPU time: 100,000 CPU cycles at 50 MHz and 200,000 at 100 MHz. Each cell gives the work passes over the share out of the passes run, then the longest pass in ms, arm A / arm B:

| CPU clock | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 50 MHz (product) | 0 of 1273, 1.89 / 0 of 1245, 1.89 | 0 of 1264, 1.71 / 0 of 1246, 1.72 | **32 of 1310, 3.46** / **30 of 1286, 3.47** | **24 of 1307, 3.28** / **23 of 1285, 3.30** |
| 100 MHz (option) | 0 of 1272, 1.14 / 0 of 1248, 1.14 | 0 of 1273, 1.04 / 0 of 1249, 1.06 | **1 of 1311, 2.29** / **2 of 1284, 2.30** | **1 of 1332, 2.20** / **1 of 1298, 2.20** |

At 8x8 and 50 MHz the passes over the share are of two kinds:
- **Before any load:** in every group, three passes at about 172, 368 and 568 ms of the run, of 2.02 to 2.41 ms. About half of each is lwSRP's MRP work for the two interfaces.
- **In each composed window:** up to six of its first passes, of 2.01 to 3.47 ms.

**The residual at 50 MHz**, worst instance per leg (the egress-held rows are left out; they miss at both clocks):

| Row or pass at 8x8/2if, 50 MHz | Bound | Arm A | Arm B | Arm A, both drafts | Arm B, both drafts |
|---|---:|---:|---:|---:|---:|
| AECP record, last | 20 ms | 25.02 (+5.02) | 25.61 (+5.61) | 24.02 (+4.02) | 24.11 (+4.11) |
| SRP record, last | 18 ms | 28.25 (+10.25) | 27.25 (+9.25) | 25.66 (+7.66) | 25.45 (+7.45) |
| Longest pass | 2.0 ms | 3.46 (+1.46) | 3.47 (+1.47) | 3.28 (+1.28) | 3.30 (+1.30) |
| Passes over the share | 0 | 32 | 30 | 24 | 23 |

At the 100 MHz option the residual is the share's alone: 2.29 / 2.30 ms against 2.0 without the drafts (+0.29 / +0.30), and 2.20 / 2.20 with them.

**A pass split, as a labelled experiment, not on this branch** (`CTRL_LOOP_RX_PER_PASS` 1 instead of 2, 8x8/2if, arm A, without the drafts):

| 8x8/2if, arm A, without the drafts | Bound, ms | CPU 50 MHz (product): two records a pass (the branch) | one (the experiment) | CPU 100 MHz (option): two | one |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 14.37 | 19.25 | 8.79 | 11.79 |
| ADP record, last | 20 | 11.20 | 13.99 | 6.67 | 8.32 |
| MAAP record, last | 20 | 11.19 | 12.64 | 6.65 | 7.50 |
| AECP record, last | 20 | **25.02** | **22.84** | 15.10 | 14.11 |
| SRP record, last | 18 | **28.25** | **34.87** | 16.95 | **20.86** |
| An ACMP command behind a full ACMP ring | 20 | 13.57 | 17.69 | 8.13 | 10.42 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 7.63 | 11.69 | 4.13 | 7.29 |
| An event behind 15 others | 20 | 3.63 | 3.02 | 2.09 | 1.77 |
| Work passes over the 2.0 ms share | 2.0 | **32 of 1310, longest 3.46 ms** | **18 of 1380, longest 2.84 ms** | **1 of 1311, longest 2.29 ms** | 0 of 1380, longest 1.67 ms |

One record a pass shortens the composed windows' longest pass, but leaves the passes before any load as they were. It also lengthens the last SRP and ACMP records, which then take twice as many passes. At 100 MHz every pass then fits the share, and the last SRP record misses its bound. No record count serves both the share and the rows at 8x8, so the branch keeps two (owner decision D4(b)).

## Authoritative references

- The round-11 assignment ([#665](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508235352)); R711-1 (PR #810 issuecomment-6508189374) and R712-1 (issuecomment-6508223902); the clock correction ([#665](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508196970)); the S2b items 3 and 6 ([#665](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6414297191)).
- NFR-SCOUT-03 and FR_NFR 3.4.1 ([`docs/reference/FR_NFR.md`](../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)): T_svc = 20 ms (owner, 2026-10-29), each path against min(T_svc, its family's ceiling); SRP's 18 ms is the tightest, so the share is 18 / 9 = 2.0 ms (`sw/firmware/ctrl/loop/ctrl_loop.h`, THE SHARE; #397's one-hart rule).
- The mover's contract: [`hdl/milan/mailbox/KL_mbx_dma.sv`](../hdl/milan/mailbox/KL_mbx_dma.sv) and [`sw/firmware/ctrl/plat/mbx_dma.h`](../sw/firmware/ctrl/plat/mbx_dma.h); AMBA AXI IHI0022H A3.2.1 for the bench's monitor.
- [`docs/design/SPLIT_CONTROL_MEMORY.md`](../docs/design/SPLIT_CONTROL_MEMORY.md#at-the-products-clock-and-the-per-pass-share) section 13; [`tb/verilator/ctrl_service_budget/README.md`](../tb/verilator/ctrl_service_budget/README.md#run-and-reproduce).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2b-cycles
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The split image and the harness need the pinned RV32 SDK and the product LiteX environment, as for S2's harness ([`tb/verilator/ctrl_service_budget/README.md`](../tb/verilator/ctrl_service_budget/README.md)). The with-drafts legs stage lwSRP's draft `fc06e7c0` and tsn-c-stack's draft `6532c3b0` by gitlink in a scratch clone, with `ctrl_arms.LWSRP_REV` moved and the runtime's `__lshrdi3` hot-list entry removed, as rounds 8 to 10 did; none of that is committed. No leg uses a harness variant.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-100 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings --record-share-findings --cpu-hz 100000000
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-adp --fetch-l1 none --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-shutdown --fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-as-built --fetch-l1 none --cpu-regions as-built
make -C tb/verilator/mbx run-dma dma-mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest
python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
python3 sw/builder/test_builder.py --require-rv32
python3 sw/builder/test_soc_options.py
python3 sw/litex/test_ctrl_memory.py
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_py_idiom.py
syn/yosys/run.sh --top KL_mbx_dma --top KL_mbx_wb
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
bash scripts/run_all_suites.sh /tmp/suite-logs --wait
(cd tests && behave)
```

Expected result / pass criteria, as run for this PR (the head each ran at; what changed since is named):

- The harness self-test: `self-test: 0 failures`, 118 checks, 91 mutants caught (head).
- The harness at both points, both arms, with and without both drafts, at both clocks (16 legs, `37e200e6`; since: one boundary-table entry and Markdown): rc 0 and `4 groups graded, 0 refusals` each. At 50 MHz: 1x1 `6 budget misses`, the egress-held ones, and `0 of 1245` to `0 of 1273 work passes over the per-pass share`; 8x8 `13 budget misses` and 23 to 32 passes over it. At 100 MHz: `6 budget misses` everywhere, and 0 (1x1) or 1 to 2 (8x8) passes over it. Every `build.json` records its clock; the images are byte-identical to round 10's legs.
- The controls on the cacheless core, at the product's clock: `CONTROL slow-adp-rx caught` (48.697 ms over its 20 ms budget), `CONTROL slow-adp-shutdown caught` (48.933 ms), `CONTROL as-built caught` with a load access fault, cause 5, there and behind the split's caches (`cf0f978b`).
- The mover's bench, in the sweep's `mbx` suite with the pinned Verilator 5.050: `== mbx record mover (KL_mbx_dma): checks: 420827   failures: 0 ==` and `mbx record mover mutants: 21 of 21 caught` (`37e200e6`).
- The firmware self-test, all four shards: `test_ctrl_firmware: PASS` (`37e200e6`; shard 1 again at the head). Shard 1 reports `mutants: 561 of 561 caught`, the eight `mover-*` plants among them. Shard 0 reports `== ctrl service bounds: checks: 46   failures: 0 ==` and `== ctrl mailbox driver with the record mover (host register model): checks: 5   failures: 0 ==`.
- `fw_coverage.py --check`: `firmware coverage: PASS (34 files)`. `fw_rv32_selftest.py`: `25 checks PASS` (`37e200e6`).
- `gen_mailbox.py --check --crosscheck --selftest`: `selftest: 0 arm(s) failed`. The census, with the pinned sv2v v0.0.12 and Yosys 0.66: `RESULT: PASS`, `mutations: 0 of 43 rule(s) no arm proves` (`37e200e6`).
- `test_builder.py --require-rv32`: `ALL GATES PASS EXCEPT 1 NOT RUN`, the historical Arty report, as in rounds 3 to 10 (`cf0f978b`).
- `test_soc_options.py`: `RESULT: PASS`. `test_ctrl_memory.py`: `RESULT: PASS` (`cf0f978b`).
- `lint_rtl.py --check`: `LINT GATE: PASS (89 violation(s) <= ratchet 89 ...)` (`37e200e6`). `xvlog_gate.py --check`, under the lock after the sweep: `xvlog gate: PASS (0 finding(s) == ratchet ...)` (`cf0f978b`). Yosys: `[PASS] KL_mbx_dma cells=2294`, 2,302 before the 13-bit sum, and `[PASS] KL_mbx_wb cells=5` (`37e200e6`). The mover out of context at 10 ns: 396 LUTs, 700 FFs, no block RAM, WNS +4.775 ns, 0 routing errors (`cf0f978b`).
- rtl-fast's firmware-boundary step (`--without verilator`): `ctrl_boundary: PASS` (head; at `37e200e6` it refused `share.py` until `cf0f978b` classified it). The firmware-verilator step (`--only verilator`): `ctrl_boundary: PASS` (head).
- The full sweep as four shards: 64 of 64 suites pass, 2,612,794 checks, 0 in-suite failures, 0 timed out (`37e200e6`; since: one boundary-table entry and Markdown).
- The docs workflow's gates, the bare-metal scope gate, the idiom gates and `behave`, 96 in all: `0 of 96 gates nonzero or left the tree dirty`. `baremetal-only: OK`; the Python idiom gate `too many parameters: 7 <= 7`; `behave`: 14 features, 406 scenarios, 1,977 steps passed (head). At `b58274ad` the bare-metal scope gate refused the plants' former `dma-*` names, which `c36a7640` changes.
- Not run:
  - lwSRP's own suite on the unchanged draft `fc06e7c0`: this round does not touch lwSRP, round 9's result stands for the same commit, and the draft's code runs in the eight with-drafts legs.
  - The CI command table's checker, which needs the CI image's pinned shell parser. This PR changes no CI command.
  - The linked images at four points: no firmware source changed except two comments, and the 1x1 and 8x8 images are byte-identical to round 10's. So the planned block RAM is round 10's, 36.5 / 40.0 / 50.0 / 56.5 RAMB36.

## Known limitations / out of scope

- **The split CPU's product clock** is the owner's decision (#665 issuecomment-6508196970). This PR does not change the SoC's clock. At 50 MHz the 8x8 last AECP and SRP records and the 8x8 passes miss; at 100 MHz only one or two 8x8 passes miss the share.
- **The share against the rows at 8x8** is a decision too: no figure of the loop's records per pass meets both (the experiment above). The passes before any load are lwSRP's MRP work, which a record count does not reach.
- **The egress-held rows** (the 60 ms egress hold, `ACMP_OWED_MAX`, the command behind the owed input) stay over their bound at both clocks, with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26). So this PR relates to #665 and does not close it.
- **The coverage ratchet compares fractions.** Without the record-mover arm's build, `mbx.c` measures 324/324, the same fraction as 330/330, so the ratchet refuses the missing build through `plat/mbx_dma.h`, which nothing else measures (`recorded in the ratchet, but nothing measured it`).
- **As before:** no measured row answers IN_PROGRESS (12 ms bound); the firmware's own host suites still hold their paths to 10 ms; the controls are the cacheless core's; the block-RAM ledger (124 against 121.5) and the drafts' repository reviews are not in this round.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
