[A683m] STOP

Head: `c36a76405fc3e98833a6c5649f81eaba0900e375` on `665-s2b-cycles` (local, not pushed): seven commits on `f884c7e9`, the head of PR #810, whose commits stay. RTL changed: one adder in `KL_mbx_dma`. The mailbox contract, both stack pins, the SoC's clocks and the CPU's netlist are unchanged.

**The STOP condition holds.** At the product's split CPU clock, 50 MHz, with the bus at 100 MHz:
- **8x8/2if misses:**
  - the last AECP record takes 24.02 to 25.61 ms against 20;
  - the last SRP record takes 25.45 to 28.25 ms against 18;
  - 23 to 32 work passes of each run are over the 2.0 ms per-pass share, the longest 3.47 ms.
  This holds in both arms, with both drafts staged or not.
- **1x1/1if fits every row the CPU decides and every pass.** The least margin is the last SRP record's, 17.81 ms against 18.

At the labelled 100 MHz option every row the CPU decides fits at both points (round 10's figures, reproduced cycle for cycle through the committed option). One or two 8x8 passes are over the share, the longest 2.30 ms. Every figure here names its CPU clock.

**Item 1, the clock (R711-F1)** (`c4ed271f`):
- The harness runs the split CPU at the product's split CPU clock by default: the point's `milan_clk_hz`, the Milan clock `milan_soc` drives the CPU from. Every leg's `build.json` records `cpu_hz` = `product_cpu_hz` = 50,000,000 and `cpu_clock` `product`.
- `--cpu-hz` is a labelled option, never the default. `build.json` records it as `option`, a reused build at another clock is refused, and every table and run line names the clock.
- `SPLIT_CONTROL_MEMORY.md` sections 11 to 13 now call the earlier 100 MHz figures a test clock (`b58274ad`). Section 13's new subsection, "At the product's clock, and the per-pass share", has both clocks. The SoC's clock is unchanged.

**Every composed row**, worst over the four backlog groups, ms, arm A / arm B, bold over its own bound:

| Row | Bound | 1x1, 50 MHz | 1x1, 50 MHz, drafts | 8x8, 50 MHz | 8x8, 50 MHz, drafts | 1x1, 100 MHz | 8x8, 100 MHz | 8x8, 100 MHz, drafts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 8.65 / 8.90 | 7.64 / 7.46 | 14.37 / 14.72 | 13.79 / 13.80 | 5.51 / 5.30 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, last | 20 | 6.08 / 6.38 | 5.51 / 5.36 | 11.20 / 11.23 | 10.59 / 10.61 | 3.93 / 3.77 | 6.67 / 6.69 | 6.31 / 6.33 |
| MAAP record, last | 20 | 6.11 / 6.42 | 5.50 / 5.34 | 11.19 / 11.21 | 10.57 / 10.59 | 3.97 / 3.81 | 6.65 / 6.68 | 6.29 / 6.32 |
| AECP record, last | 20 | 15.95 / 17.05 | 14.87 / 15.76 | **25.02** / **25.61** | **24.02** / **24.11** | 10.25 / 10.43 | 15.10 / 15.84 | 13.74 / 14.61 |
| SRP record, last | 18 | 17.81 / 17.02 | 16.34 / 16.26 | **28.25** / **27.25** | **25.66** / **25.45** | 10.53 / 10.40 | 16.95 / 16.32 | 15.60 / 15.40 |
| ACMP command behind a full ring | 20 | 6.83 / 6.78 | 6.01 / 6.09 | 13.57 / 13.60 | 12.71 / 12.72 | 4.07 / 4.04 | 8.13 / 8.15 | 7.64 / 7.45 |
| ENTITY_AVAILABLE behind a full ADP ring | 20 | 4.55 / 4.88 | 4.38 / 4.26 | 7.63 / 7.87 | 7.32 / 7.23 | 3.02 / 2.87 | 4.13 / 4.32 | 3.33 / 4.03 |
| An event behind 15 others | 20 | 2.06 / 2.06 | 1.88 / 1.89 | 3.63 / 3.64 | 3.46 / 3.48 | 1.24 / 1.23 | 2.09 / 2.10 | 2.01 / 2.02 |
| The three egress-held rows | 20 | miss | miss | miss | miss | miss | miss | miss |

The 1x1 100 MHz rows with the drafts are round 10's too (all fit). The first records and the refilling bucket fit everywhere.

**Item 4, the per-pass share (R712-F2)** (`c4ed271f`):
- The share is SRP's 18 ms over nine passes, 2.0 ms of CPU time (`share.py`, derived from the bounds table): 100,000 CPU cycles at 50 MHz, 200,000 at 100 MHz.
- Every work pass is graded against it apart from the rows. A pass over it fails the run, even when every row fits, unless `--record-share-findings` records it. The self-test plants such a pass, and three mutants of the verdict are caught.
- The passes over it, out of the passes of the four groups' runs, arm A / arm B:

| CPU clock | 1x1 | 1x1, drafts | 8x8 | 8x8, drafts |
|---|---:|---:|---:|---:|
| 50 MHz (product) | 0 of 1273 / 0 of 1245, longest 1.89 | 0 / 0, 1.72 | **32 of 1310 / 30 of 1286, longest 3.47** | **24 of 1307 / 23 of 1285, 3.30** |
| 100 MHz (option) | 0 / 0, 1.14 | 0 / 0, 1.06 | **1 of 1311 / 2 of 1284, 2.30** | **1 / 1, 2.20** |

  - **Before any load,** at 8x8 and 50 MHz: in every group, three passes at about 172, 368 and 568 ms of the run, of 2.02 to 2.41 ms. About half of each is lwSRP's MRP work (`mrp_mad`).
  - **In each composed window:** up to six of its first passes, of 2.01 to 3.47 ms. Their largest modules are `ctrl_mem`, ACMP's core, `mrp_mad` and `srp_mbx`.
- **The split, measured as a labelled experiment** (`CTRL_LOOP_RX_PER_PASS` 1 instead of 2, 8x8 arm A, no drafts, not committed):
  - At 50 MHz, 18 passes stay over (longest 2.84 ms). The last SRP record goes from 28.25 to 34.87 ms, and the last ACMP record from 14.37 to 19.25.
  - At 100 MHz every pass fits, and the last SRP record misses its bound: 20.86 ms against 18, where it was 16.95.
  - No record count serves both, so the branch keeps D4(b)'s two.

**The residual at 50 MHz, 8x8/2if** (over the bound; the egress-held rows aside):

| | Arm A | Arm B | Arm A, drafts | Arm B, drafts |
|---|---:|---:|---:|---:|
| AECP record, last (20 ms) | +5.02 | +5.61 | +4.02 | +4.11 |
| SRP record, last (18 ms) | +10.25 | +9.25 | +7.66 | +7.45 |
| Longest pass (2.0 ms) | +1.46 | +1.47 | +1.28 | +1.30 |

At 100 MHz the residual is the longest 8x8 pass alone: +0.29 / +0.30 ms, and +0.20 with the drafts.

**Item 2, the mover's length (R711-F2 = R712-F1)** (`f52e65a9`):
- The word count is formed in 13 bits, so every length the field takes, 4093 to 4095 included, moves its whole words within the burst and byte contract. No refusal is needed.
- The bench's D10 checks 4092 to 4095 in both directions across the ring's end, each followed by a CPU access and a recovery transfer.
- 21 plants, the 17 kept. The bench: 420,827 checks. R712's probe (27,678 checks) and R711's (0 of 22 moves hang) pass on the fixed mover.
- Out of context at 10 ns: 396 LUTs, 700 FFs, no block RAM, WNS +4.775 ns.

**Item 3:**
- **R711-F3:** the bench now catches R711's three escaping plants by named checks: a held partial write is still refused; a move started beside a CPU access moves its own bytes; no burst follows an error on a burst's first beat. R711's ten plants: 10 of 10.
- **R711-F4** (`56f563e3`): `test_mbx_dma_driver.cpp` builds `mbx.c` as the split image builds it, over a register model of the mover. It covers success, ERR in each direction and a frame off a word, with eight plants caught. The coverage ratchet records `mbx.c` at 330/330 lines and 164/164 branches, and `plat/mbx_dma.h` at 10/10 and 4/4.

**Item 5:** R711's residue R1 and R2 and the README's RV32IM: wording, folded in (`37e200e6`).

**Validation** (at the head each ran; since: `cf0f978b` adds one boundary-table entry, `b58274ad` is Markdown, `c36a7640` renames the eight plants), all rc 0:
- the firmware self-test, four shards: `mutants: 561 of 561 caught`;
- `fw_coverage.py --check` `PASS (34 files)`; `fw_rv32_selftest.py` 25 checks;
- the harness self-test: 118 checks, 91 mutants;
- the 16 legs and the experiment's 2; the controls caught (48.697 / 48.933 ms, cause 5);
- `gen_mailbox.py` and the census; `lint_rtl.py`; Yosys (`KL_mbx_dma cells=2294`); `xvlog_gate.py` under the lock;
- `test_builder.py --require-rv32` (`ALL GATES PASS EXCEPT 1 NOT RUN`, the historical Arty report); `test_soc_options.py`; `test_ctrl_memory.py`;
- `ctrl_boundary.py`, both steps;
- the full sweep as four shards: 64 of 64 suites, 2,612,794 checks, 0 failures;
- the docs runner's 96 gates, `behave` among them (406 scenarios): `0 of 96 gates nonzero`. The campaign's shard 1 and both `ctrl_boundary.py` steps ran again at the head after the plants were renamed `mover-*`, because the bare-metal scope gate keeps `dma-rx` and `dma-tx` for the retired host plane.

Not run: lwSRP's own suite on the unchanged draft; the CI command table's checker.

**Decisions for the owner:**
- **The split CPU's clock.** At 50 MHz the 8x8 rows and passes above miss. At 100 MHz only the 8x8 passes miss the share, by up to 0.30 ms.
- **At 8x8, the share against the rows.** No record count fits both. The passes before any load are lwSRP's MRP work, which a record count does not reach.

Handoff, receipts and PR body: in the lane's output directory (`HANDOFF.md`, `PR-BODY.md`, `receipts/INDEX.md`).
