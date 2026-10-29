# [A683m] #665 lane S2b round 11: R711-1 and R712-1 on PR #810 (HANDOFF)

**Status: STOP** (2026-10-30). Head `c36a76405fc3e98833a6c5649f81eaba0900e375`: seven commits on `f884c7e9fb71cdb94c12e3228b1412801c34e1f4` (PR #810), no rebase, no force, nothing pushed by this session. At the product's split CPU clock, 50 MHz, the 8x8/2if last AECP and SRP records miss their bounds and 8x8 passes miss the 2.0 ms per-pass share; 1x1/1if fits every row and pass. At the labelled 100 MHz option every row the CPU decides fits, and one or two 8x8 passes miss the share. Every figure here names its CPU clock.

- Remote `https://github.com/kebag-logic/milan-fpga.git` (checked). Lane base `origin/dev-soft-core` `e76a755a` is an ancestor (checked; not dev). The PR targets `dev-soft-core` (`f4c9ad4f`).
- No git command changed a submodule of the lane. The drafts were staged only in a scratch clone's submodules, each first checked to be its own top level with the lane's submodule as its origin, and fetched there from round 10's scratch clone, with no network.
- Vivado: only under `$VIVADO_LOCK`, exclusive, after the sweep, one job at a time: the xvlog front-end gate, then the record mover out of context (52 s). No route of the split CPU: its netlist is round 9's.
- Assignment: issuecomment-6508235352 (`ASSIGNMENT-A10-6508235352.md`). TAKEN: issuecomment-6508368437 (`TAKEN-COMMENT.md`). STOP: issuecomment-6511234544 (`STOP-COMMENT.md`). Reviews: R711-1 (PR #810 issuecomment-6508189374), R712-1 (issuecomment-6508223902). The clock question: issuecomment-6508196970, with the owner.

## Contents

1. Outcome against the assignment
2. Changes (file:line, reason)
3. New checks, planted defects and failing words
4. Method
5. Measurement (every figure labelled with its CPU clock)
6. Gates
7. Findings, conflicts, decisions needed
8. Run history

## 1. Outcome against the assignment

**STOP**, the expected outcome while the clock question is open: at the product's split CPU clock, 50 MHz, the 8x8/2if last AECP and SRP records miss their bounds and 8x8 passes miss the per-pass share. Every figure below names its CPU clock.

| Item | Outcome |
|---|---|
| 1. R711-F1, the clock: the harness measures the product's split CPU clock by default; `build.json`'s `cpu_hz` equals the product's | Done (`c4ed271f`). The default is the point's `milan_clk_hz`, the Milan clock `milan_soc` drives the CPU from, which the builder's loader holds to the bare-metal contract's 50 MHz. Every leg's `build.json`: `cpu_hz` and `product_cpu_hz` 50,000,000, `cpu_clock` `product` (section 5) |
| Any other clock an explicit, labelled option, never the default | `--cpu-hz`; `build.json` `cpu_clock` `option` and `cpu_hz_option`; a reused build at another clock refused; `CLOCK` first and last on every run, first in every `table.md`; checked by the self-test with three mutants |
| Re-measure every composed row at 1x1/1if and 8x8/2if, both arms, with and without the drafts, at 50 MHz and at 100 MHz | 16 legs, 0 refusals (section 5) |
| `SPLIT_CONTROL_MEMORY.md` section 13, the harness README and the PR body state the clock of every figure; none presents 100 MHz as the product's | Done (`b58274ad`, `c4ed271f`, `PR-BODY.md`): sections 11 to 13 call 100 MHz a test clock; section 13's new subsection has both clocks |
| Do not change the SoC's clock | Not changed |
| 2. R711-F2 = R712-F1, the mover's length wrap: every length the field accepts obeys the burst and byte contract, or a refusal | The sum in 13 bits (`f52e65a9`): every length obeys the contract, so no refusal is defined |
| Check 4092 to 4095 both ways, the CPU access and a recovery transfer after; keep the 17 plants | D10 (`dma_main.cpp:479-497`); 21 plants, the 17 kept; R712's probe (27,678 checks, 0 failures) and R711's (0 of 22 hang) pass on the fixed mover (`receipts/mover/`) |
| 3. R711-F3: bench checks that fail for each property the bench claims | The three escaping plants now caught by named checks; R711's ten plants 10 of 10 |
| R711-F4: a test that compiles the record-mover arm and runs its error arms | `test_mbx_dma_driver.cpp` (`56f563e3`): R1, R2, T1, T2, T3; eight plants caught; in the coverage ratchet |
| 4. R712-F2: the share, 18 / 9 = 2.0 ms, reported and asserted at both points, both arms, with and without the drafts, separately from the rows | `share.py`, `grade.pass_share`, `run.share_misses`; every leg's table and `results.json` (section 5) |
| A planted pass over the share fails even when every row fits | Self-test check "a pass over the share fails a run whose rows all fit ..."; three mutants caught |
| Where a pass is over the share, split it or bound its work, and give the figure at both clocks | Over: 8x8 at 50 MHz (23 to 32 passes a run, longest 3.47 ms) and 8x8 at 100 MHz (1 or 2, longest 2.30 ms). The loop's named constant split, measured at both clocks as a labelled experiment: it does not fit both the share and the rows, so it is not committed (section 5, 7) |
| 5. R711 residue | R1, R2 and the README's RV32IM: wording, folded in (`37e200e6`, `c4ed271f`) |
| Exit: REVIEW READY if every CPU-decided row and every pass fits at 50 MHz, else STOP with the full figures at both clocks and the residual | STOP (section 5) |

## 2. Changes

Commits on `f884c7e9` (one-line subjects, no body, no trailers):

| Commit | Subject |
|---|---|
| `f52e65a9` | Form the record mover's word count in 13 bits, so the length field's 4093 to 4095 move their whole words instead of none, and give its bench the field's largest lengths, a held partial write, a move started beside a CPU access and an error on a burst's first beat, each with its plant |
| `56f563e3` | Test the mailbox driver as the split image builds it, each payload moved by the record mover over a register model of it, a move ending in ERR in each direction and a frame off a word included, with eight plants, and record its arm's lines and branches in the coverage ratchet |
| `c4ed271f` | Run the CPU budget harness's split CPU at the product's split CPU clock unless --cpu-hz names a labelled option, name the clock in build.json, on every table and run line, and hold every work pass to the 2.0 ms per-pass share apart from the rows, a pass over it failing the run unless --record-share-findings records it |
| `37e200e6` | Say that the memory primitives' cycle figures are the cacheless RV32I core's and that the uncached side of the split core is its mailbox window |
| `cf0f978b` | Name the CPU budget harness's per-pass share among the files that name the firmware's tree and compile nothing, so the firmware boundary gate takes it |
| `b58274ad` | Give every composed row and pass at the product's split CPU clock, 50 MHz, and at the labelled 100 MHz option, the per-pass share and a split's measured cost, and call the earlier 100 MHz figures a test clock |
| `c36a7640` | Name the record-mover arm's eight plants mover-*, since the bare-metal scope gate keeps dma-rx, dma-tx and the DMA ring for the retired host plane |

### 2.1 The mover's length (R711-F2 = R712-F1), `f52e65a9`

| file:line | Change | Reason |
|---|---|---|
| `hdl/milan/mailbox/KL_mbx_dma.sv:174-176` | `start_words_w = 11'(({1'b0, len_bytes_i} + 13'd3) >> 2)`: the sum in 13 bits | In 12 bits, 4093 + 3 to 4095 + 3 wrapped to 0 to 2, so those lengths took zero words: a receive held the host port forever in FILL with no request, and a transmit issued ARLEN 255 or 31. Every length the field takes now has its whole words, at most 1,024, which `left_r` (11 bits) holds. No refusal is needed, because every accepted length obeys the burst and byte contract |
| `KL_mbx_dma.sv:57` | the port's comment: "any of 0 to 4095" | The contract the bench now checks |
| `tb/verilator/mbx/dma_main.cpp:22-54` | the header: D1 includes the field's largest lengths; D4 covers the held write's strobes and a transfer started beside a CPU access; D6 covers no burst after an error; D10 is new | R711-F3, R711-F2 / R712-F1 |
| `dma_main.cpp:120-123` | the host model drives noise (`0xA5000000 ^ cycle`) on `host_rdata_i` in a cycle with no answer | The model used to keep the last answer, so data taken from an unanswered cycle could match by chance |
| `dma_main.cpp:73`, `:242`, `:330-338` | a one-word SLVERR range at a line's start (`kErrWord`); the bench counts the AR and AW bursts issued after an errored read beat or an error write response | R711's `error-burst-continues`: the old error range erred on every beat, so the last beat's own error ended the transfer, and the `rerr_r` term was never needed |
| `dma_main.cpp:389-401`, `:409`, `:430-436` | `Ring` (base, mask) for `receive_case` / `transmit_case`, the AECP ring by default and a 2,048-word ring for the largest lengths; the partial-strobe count compared against its value at the case's start | 1,024 words do not fit the 512-word AECP ring |
| `dma_main.cpp:479-497` | `largest()`: 4092 to 4095 bytes, both directions, at 0 % and 30 % stalls, from index 2040 so the ring's end is crossed; after each, a CPU read of a known word (D10) and a recovery receive and transmit of 18 bytes on the AECP ring | R712-F1's required verification |
| `dma_main.cpp:524-532` | a held CPU write with strobes `0x3`: it must reach `KL_mbx`'s model with them, so it is refused and counted, and the ring word stays | R711's `held-partial-write-widened` |
| `dma_main.cpp:534-549` | the start-cycle case in both directions over a patterned ring: the moved bytes must be the ring's or memory's own | R711's `fill-during-cpu-answer` |
| `dma_main.cpp:592`, `:612-621` | D6: no write burst after an error response; no read burst after an errored beat, with the error on the burst's first beat only | R711's `error-burst-continues` |
| `tb/verilator/mbx/dma_mutants.py:82-91` | four arms: `length-sum-wraps`, `error-burst-continues`, `fill-during-cpu-answer`, `held-partial-write-widened`; the 17 kept | 21 of 21 |
| `tb/verilator/mbx/README.md:26-33` | D1 to D10, 21 plants | Documentation |

### 2.2 The firmware's record-mover arm (R711-F4), `56f563e3`

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/test/test_mbx_dma_driver.cpp` (new) | `mbx.c` built as the split image builds it, the window in place and `CTRL_MBX_DMA_BASE` set, over a register model of `KL_mbx_dma` written from its register contract. R1: a record moved and released, 60 to 63 bytes across the ring's end, CFG/MEM/CMD as the contract says, STATUS polled until BUSY falls. R2: ERR resynchronises to RX_HEAD. T1: a frame on a word moved and committed. T2: ERR is not committed and the next frame reuses the head and sequence. T3: a frame off a word takes the word loop and starts no move | No test compiled the arm: `CTRL_MBX_DMA_BASE` was defined only for the split image |
| `sw/firmware/ctrl/test/mmio_dma.h` (new) | the register bank and `ctrl_test_dma_base()`, force-included | The driver forms each register's address from `CTRL_MBX_DMA_BASE` at every access (`plat/mbx_dma.h`), so a function there lets the model see each access before it is made and take a written CMD as a start |
| `sw/firmware/ctrl/test/ctrl_arms.py:210-215`, `:219-220` | the unit arm builds and runs it | Every unit-arm run, the coverage build and every plant run it |
| `sw/firmware/ctrl/test/mbx_dma_mutants.py` (new), `ctrl_mutants.py:27`, `:589` | eight plants in `mbx.c`'s arms and `plat/mbx_dma.h`, appended to the campaign | `ctrl_mutants.py` is at 998 of the idiom gate's 1,000 lines, so the table is its own module, as `acmp_review_mutants.py` is |
| `sw/firmware/gtest/coverage.ratchet` | regenerated by `fw_coverage.py --write`: `mbx/mbx.c` 330/330 lines and 164/164 branches (was 324/158, the arms' 6 lines and 6 branches); `plat/mbx_dma.h` 10/10 and 4/4, a new measured file; 34 files | Its generator |
| `sw/firmware/ctrl/README.md:479` | the unit arm's row names the test and R1 to T3 | Documentation |

### 2.3 The clock and the per-pass share (R711-F1, R712-F2), `c4ed271f`

| file:line | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/split_soc.py:444-470`, `:492` | `build(..., core)`: `core.cpu_hz` None is the product's split CPU clock, the point's `milan_clk_hz`; a number is the labelled option. `soc.json` and `build.json` record `cpu_hz`, `product_cpu_hz` and `cpu_hz_option` | R711-F1: the default must be the product's; any other clock explicit and labelled. The selection object keeps `build` within the idiom gate's six parameters |
| `build.py:577`, `:580-592`, `:607` | `Core.cpu_hz`; `clock_line(spec)`; `build.json`'s `cpu_clock`, `product` or `option` | Every figure names its clock |
| `run.py:238-244` | `--cpu-hz HZ` and `--record-share-findings` | |
| `run.py:352-362` | `selected()` and `built_as()` carry the clock option; a reused build at another clock is refused | A 100 MHz build must never be graded as the product's |
| `run.py:393`, `:408`, `:423` | `CLOCK` first and last on the run's output; `results.json` `clock` | |
| `run.py:125-160`, `:186-192` | `share_misses()`, `share_table()`: a `SHARE` line per group with a pass over the share; the table's per-pass share section; the clock line first in `table.md` | R712-F2: reported and asserted separately from the rows |
| `run.py:343-350` | `verdict()`: a pass over the share fails the run unless `--record-share-findings`; `--record-budget-findings` does not record it | "A planted pass over the share must fail even when every row fits" |
| `share.py` (new) | `SHARE_PASSES = 9`; `bound_ms()`, the least of min(T_svc, ceiling) over the families (18 ms, SRP); `share_ms()` 2.0; `share_cycles(cpu_hz)` | The share is derived from the bounds table, not restated |
| `grade.py:788-794`, `:833` | `pass_share(log)`: every work pass against the share at the log's CPU clock; in each group's `passes` | |
| `selftest_share.py` (new), `selftest.py:55`, `:844-846`, `:895`, `:907-908` | the share and clock checks (below); the build stub takes the selection and records the clock as `split_soc.build` does; the reuse refusal's words | `selftest.py` is at 973 lines |
| `selftest_mutants.py:316-325`, `:511-529` | 11 mutants (below) | |
| `README.md:7-9`, `:15`, `:38-42`, `:61-86`, `:202`, `:925-927`, `:1009-1019` | the clock of every figure; the clock and the share in Run and reproduce; the conversion's ratio; the self-test's new checks and mutants; RV32IM and the split's caches (R711 residue) | R711-F1's docs; R711 residue |

### 2.4 R711 residue R1 and R2, `37e200e6` (wording only)

| file:line | Change |
|---|---|
| `sw/firmware/ctrl/plat/ctrl_mem.c:7-10` | "The cacheless RV32I core this was written for is fetch-bound: ..." |
| `sw/firmware/ctrl/mbx/mbx_wire.h:62-63` | "(#665: the mailbox window is uncached, and each byte access is a bus transaction of 9 CPU cycles)" |
| `tb/verilator/ctrl_service_budget/README.md:113-115` (in `c4ed271f`) | "RV32IM, one hart"; the split's 16 KiB two-way fetch L1 and coherent 8 KiB data cache; the clock |

### 2.5 The boundary gate's classification, `cf0f978b`

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/test/ctrl_configs.py:204-205` | `share.py` in `OUTSIDE`: it names `ctrl_loop.h`'s derivation and compiles nothing | `ctrl_boundary.py --without verilator` refused it at `37e200e6`: `REFUSED: tb/verilator/ctrl_service_budget/share.py names the firmware's tree, compiled nothing in the capture, and is neither a known builder ...` |

### 2.6 The plants' names, `c36a7640`

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/test/mbx_dma_mutants.py:20-41` | the eight plants named `mover-*`; one line wrapped | The bare-metal scope gate refused `dma-rx`, `dma-tx` and `dma-ring` in the names: `[H] retired target host-plane surface 'dma-rx' ... (#259: no dormant target driver/memory-ring contract)`, five findings (`receipts/findings/baremetal_check-b58274ad.log`). The Python idiom gate then refused one line at 124 columns (`over-long line 1 > ratchet 0`) |

### 2.7 The record, `b58274ad` (Markdown only)

| file:line | Change | Reason |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:24-26` | the contents entries of sections 11 to 13 name the test clock and the product's | R711-F1 |
| `SPLIT_CONTROL_MEMORY.md:580-581`, `:707`, `:711-713`, `:846-849`, `:975`, `:978`, `:1005`, `:1022` | sections 11, 12 and 13 call their 100 MHz figures a test clock, not the product's 50 MHz, and the owner's decision "the product's clocks, the CPU at 50 MHz and its bus at 100 MHz" | R711-F1: "none of them presents 100 MHz as the product clock" |
| `SPLIT_CONTROL_MEMORY.md:905-908` | the mover: the 13-bit sum, its route at this head (396 LUTs, 700 FFs, no block RAM, +4.775 / +0.189 ns), D10 and 21 plants, the driver's arm test | R711-F2/F3/F4 |
| `SPLIT_CONTROL_MEMORY.md:1058-1149` | new subsection "At the product's clock, and the per-pass share": both clocks' row tables, the share table, the two kinds of pass over it, the experiment | Items 1 and 4 |
| `SPLIT_CONTROL_MEMORY.md:1151-1161` | "What is left" at both clocks, and the two decisions | Items 1 and 4 |
| `tb/verilator/ctrl_service_budget/README.md:10`, `:1088` | the pointer to the new subsection; the controls run again with the share and the clock option | |

## 3. New checks, planted defects and failing words

| Check | Planted defect | Failing words |
|---|---|---|
| mover D10 | `length-sum-wraps`: the 12-bit sum | `[FAIL] D10 after the field's largest lengths a CPU access gets its own word` (and `D1 a receive transfer ends, 4093 bytes, the field's largest, stall 0%`) |
| mover D6, a burst's first beat erred | R711's `error-burst-continues`: `rerr_r` dropped from R_S's end | `[FAIL] D6 no read burst is issued after an errored beat` |
| mover D4, start-cycle data | R711's `fill-during-cpu-answer`: `!ack_cpu_r` dropped from `fill_req_w` | `[FAIL] D4 a transfer started in the cycle of a CPU access moves its own bytes` |
| mover D4, held strobes | R711's `held-partial-write-widened`: `pend_be_r <= 4'hF` | `[FAIL] D4 a held CPU write keeps its byte strobes: a partial one is still refused` |
| firmware R2 | `mover-receive-error-trusted` | `[FAIL] MbxDma.R2AMoveEndingInErrorResynchronises: R2 a move that ends in ERR leaves no record` |
| firmware R1 | `mover-receive-index-at-the-header` | `[FAIL] MbxDma.R1ARecordsPayloadIsMovedAndReleased: R1 the move starts at the payload's first ring word, 60 bytes` |
| firmware T2 | `mover-transmit-error-committed` | `[FAIL] MbxDma.T2AMoveEndingInErrorIsNotCommitted: T2 a move that ends in ERR is refused` |
| firmware T3 | `mover-transmit-frame-off-a-word-moved` | `[FAIL] MbxDma.T3AFrameOffAWordTakesTheWordLoop: T3 a frame off a word takes the word loop` |
| firmware R1, the poll | `mover-status-read-once` (`mbx_dma.h`) | `[FAIL] MbxDma.R1ARecordsPayloadIsMovedAndReleased: R1 the driver polls STATUS until BUSY falls, 60 bytes` |
| firmware R2 and T2 | `mover-error-ignored` (`mbx_dma.h`) | `R2 a move that ends in ERR leaves no record`, and T2's `T2 a move that ends in ERR is refused` |
| firmware R1, CFG | `mover-ring-size-unshifted` (`mbx_dma.h`) | `[FAIL] MbxDma.R1ARecordsPayloadIsMovedAndReleased: R1 CFG names the ring's base and size, 60 bytes` |
| firmware T1, CMD | `mover-direction-dropped` (`mbx_dma.h`, `(to_ring ? 0u : 0u)`) | `[FAIL] MbxDma.T1AFrameOnAWordIsMovedAndCommitted: T1 the move runs memory to the ring from the payload's first word, 60 bytes` |
| harness: the share's value | `share: T_svc over the passes, not the tightest family bound`; `the bound over eight passes`; `a pass at the share is over it`; `in bus cycles, not CPU time` | `the per-pass share is SRP's 18 ms, the tightest family bound, over nine passes: 2.0 ms, 100,000 CPU cycles at 50 MHz` |
| harness: a pass at and over it | `share: the passes are not held to it` | `a work pass at the share fits it and one a cycle over it does not` |
| harness: the verdict, rows apart | `share: a pass over it is no finding`; `the rows option records the passes too`; `a pass over it fails the run only beside a row miss` | `a pass over the share fails a run whose rows all fit, unless --record-share-findings records it; --record-budget-findings does not` |
| harness: the default clock | `clock: a labelled option is recorded as the product's clock`; `the option is built at the product's clock` | `by default the CPU runs at the product's split CPU clock and build.json says so; another clock is a labelled option` |
| harness: reuse at another clock | `clock: a reused build at another CPU clock is taken` | `the run refuses a reused build at another CPU clock and reuses one at the selected clock` |

The mover's planted defects run through `dma_mutants.py` (21 of 21, `receipts/mover/`), the firmware's through the self-test's campaign (`ctrl_mutants.MUTANTS`, which now holds 561), and the harness's through its self-test (91 mutants).

## 4. Method

- **The legs** (`receipts/measure/`, each with its `label.txt`, `build.json`, image digest, `results.json.gz`, `run.log` and `table.md`):
  - S2's harness as committed at `37e200e6`, the four backlog groups (`backlog`, `backlog-adp`, `backlog-adp-refill`, `backlog-owed`), `--record-budget-findings --record-share-findings`;
  - at 1x1/1if and 8x8/2if, arm A and arm B (`--variant answering-ports`);
  - `N11-*` from a clean clone at `37e200e6`, and `D11-*` from a clean clone at `37e200e6` with both drafts staged as rounds 8 to 10 staged them (`receipts/variants/drafts-staged.patch`);
  - `-50`: the product's split CPU clock, 50 MHz, the harness's default; `-100`: the labelled `--cpu-hz 100000000` option. The bus is 100 MHz in every leg.
  - No harness variant: round 10's profiling patch (`CSB_CPU_HZ`) is not applied anywhere. Each `build.json` records `cpu_hz`, `product_cpu_hz` (50,000,000), `cpu_clock` and `cpu_hz_option`; `scripts/rows11.py` refuses a leg whose recorded clock is not the one its name says.
  - Every leg's image is byte-identical to round 10's leg of the same point, arm and draft state (`image.txt`; for example 8x8 arm A `f80111d8...3e3f7f`, the image R711 measured). The CPU netlist is `VexiiRiscvLitex_c05c5a8e0bd42fc384567409f2a37e64`, round 9's.
- **The labelled experiment** (`X11-A8-50`, `X11-A8-100`; `receipts/variants/experiment-rx-per-pass-1.patch`): `CTRL_LOOP_RX_PER_PASS` 1 instead of 2 in a scratch clone at `37e200e6`, not on the branch, 8x8 arm A without the drafts, at both clocks. It is the loop's own named constant for the records one pass takes per channel (owner decision D4(b), 2026-10-27), so it measures whether a split by that constant brings the passes within the share and what it costs the rows.
- **The analysis** (`scripts/rows11.py`): each composed row's worst instance over the four groups, against min(T_svc, the family's ceiling) + W from the lane's `scenario.py`; each group's work passes against `share.py`'s share; the residual of each row and pass over its bound (`receipts/rows/`).
- **CPU and memory:** the legs ran as their own units (MemoryMax 8 GB, four CPUs each) on 16-31, four at a time; the experiment's legs on this session's 76-79; the gates as units on 64-79; the full sweep as four `native-shards.py` units on 0-15, started at 52 GB MemAvailable. MemAvailable stayed above 44 GB.

## 5. Measurement

Every leg: `4 groups graded, 0 refusals`; the misses below; `receipts/measure/*/run.log`. Images byte-identical to round 10's of the same point, arm and draft state; CPU netlist `VexiiRiscvLitex_c05c5a8e`. At 100 MHz every probe's CPU cycles at 1x1 arm A are identical to round 10's variant-based leg `N10-A1`, so the committed option reproduces the variant.

| Leg | CPU clock (bus 100 MHz) | Budget misses | Passes over the share |
|---|---|---|---|
| N11-A1-50, N11-B1-50 | 50 MHz, product | 6 (the egress-held) | 0 of 1,273; 0 of 1,245 |
| D11-A1-50, D11-B1-50 | 50 MHz, product, both drafts | 6 | 0 of 1,264; 0 of 1,246 |
| N11-A8-50, N11-B8-50 | 50 MHz, product | 13: the egress-held 6 and 7 AECP/SRP last records | 32 of 1,310; 30 of 1,286 |
| D11-A8-50, D11-B8-50 | 50 MHz, product, both drafts | 13 | 24 of 1,307; 23 of 1,285 |
| N11-A1-100, N11-B1-100 | 100 MHz, option | 6 | 0 of 1,272; 0 of 1,248 |
| D11-A1-100, D11-B1-100 | 100 MHz, option, both drafts | 6 | 0 of 1,273; 0 of 1,249 |
| N11-A8-100, N11-B8-100 | 100 MHz, option | 6 | 1 of 1,311; 2 of 1,284 |
| D11-A8-100, D11-B8-100 | 100 MHz, option, both drafts | 6 | 1 of 1,332; 1 of 1,298 |
| X11-A8-50 (experiment) | 50 MHz, product | 13 | 18 of 1,380 |
| X11-A8-100 (experiment) | 100 MHz, option | 8: the egress-held 6 and 2 SRP last records (20.86, 20.70 ms) | 0 of 1,380 |

Every composed row, worst instance over the four groups, ms, arm A / arm B, bold over its own bound (`receipts/rows/doc-tables.md`; per leg and with the residual of each miss, `rows-1x1.md`, `rows-8x8.md`):

CPU at the product's split CPU clock, 50 MHz, bus 100 MHz:

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

CPU at the labelled 100 MHz option, bus 100 MHz:

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

Per-pass share, 2.0 ms of CPU time; each cell is arm A / arm B: the work passes over it of the four groups' runs, and the longest pass in ms:

| CPU clock | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 50 MHz (product) | 0 of 1273, 1.89 / 0 of 1245, 1.89 | 0 of 1264, 1.71 / 0 of 1246, 1.72 | **32 of 1310, 3.46** / **30 of 1286, 3.47** | **24 of 1307, 3.28** / **23 of 1285, 3.30** |
| 100 MHz (option) | 0 of 1272, 1.14 / 0 of 1248, 1.14 | 0 of 1273, 1.04 / 0 of 1249, 1.06 | **1 of 1311, 2.29** / **2 of 1284, 2.30** | **1 of 1332, 2.20** / **1 of 1298, 2.20** |

The passes over the share at 8x8 and 50 MHz are of two kinds:
- **Before any load:** in every group, three passes at about 172, 368 and 568 ms of the run, of 101,111 to 120,378 cycles (2.02 to 2.41 ms). About half of each is lwSRP's MRP work (`mrp_mad` 59,778 of 119,836 cycles in the experiment's leg, where it is the longest).
- **In each composed window:** up to six of its first passes, of 100,328 to 173,282 cycles (2.01 to 3.47 ms). Their largest modules: `ctrl_mem` 39,443, `acmp` 34,805, `mrp_mad` 17,320, `srp_mbx` 13,711 in the longest.

At 100 MHz only the composed window's first pass of `backlog` (and one more in B8) is over: 200,101 to 230,298 cycles.

The residual at 50 MHz, 8x8/2if: the last AECP record +4.02 to +5.61 ms, the last SRP record +7.45 to +10.25 ms, the longest pass +1.28 to +1.47 ms. At 100 MHz: the longest pass +0.20 to +0.30 ms.

**The labelled experiment**, `CTRL_LOOP_RX_PER_PASS` 1 (`receipts/rows/experiment.md`):

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

At 50 MHz it shortens the composed windows' longest pass, leaves the three passes before any load as they were (119,836, 101,022, 101,437 cycles), and lengthens the SRP and ACMP rows. At 100 MHz it fits every pass and breaks the last SRP record.

The controls, at `cf0f978b` (`receipts/controls/`), product clocks, all rc 0: `CONTROL slow-adp-rx caught` (48.697 ms over its 20 ms budget), `CONTROL slow-adp-shutdown caught` (48.933 ms), `CONTROL as-built caught` on the cacheless core (`TRAP 166 0 5 00000020`) and behind the split's caches (`TRAP 390 0 5 00000020`), round 10's figures.

## 6. Gates

Each gate ran in a clean clone of its head (`scripts/clone.sh`), as its own unit on four of this session's 64-79 unless named, its log in `receipts/gates/` with host paths replaced. "Since" says what changed after a gate's head: `cf0f978b` adds one entry to `ctrl_configs.OUTSIDE`, which only the boundary gate reads; `b58274ad` is Markdown only.

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| Firmware self-test, four shards (every firmware mutant driver, the service-bounds arm, the hot list's arm) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard k/4 --jobs 4` | `37e200e6`; shard 1 again at `c36a7640` (since: docs) | rc 0, `test_ctrl_firmware: PASS` each (362, 1,472, 659, 841 s; shard 1 at `c36a7640` the same, `mutants: 561 of 561 caught` with the `mover-*` names); shard 0 `== ctrl service bounds: checks: 46   failures: 0 ==`, `== ctrl mailbox driver with the record mover (host register model): checks: 5   failures: 0 ==`, `[ok] arm hot`, `named plants not caught: none`; shard 1 `mutants: 561 of 561 caught`, the eight `mover-*` among them; no `ESCAPED` | `selftest-shard0.log` to `selftest-shard3.log` |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check` | `37e200e6` | rc 0, `firmware coverage: PASS (34 files)` | `head-fw_coverage-check.log` |
| Coverage's plant: the arm's build removed (`ctrl_arms.py` at `f884c7e9`) | same | `cf0f978b` + plant | rc 1, `FINDING: sw/firmware/ctrl/plat/mbx_dma.h: recorded in the ratchet, but nothing measured it`, `firmware coverage: FAIL (33 files)` | `../findings/plant-coverage-without-dma-arm.log` |
| RV32 self-test | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | `37e200e6` | rc 0, `RV32 build self-test: 25 checks PASS` | `head-fw_rv32_selftest.log` |
| The mover's bench and plants, pinned Verilator 5.050 | `make` in `tb/verilator/mbx` (the sweep's `mbx` suite: `run-dma`, `dma-mutants`) | `37e200e6` | `== mbx record mover (KL_mbx_dma): checks: 420827   failures: 0 ==`, `mbx record mover mutants: 21 of 21 caught`; the suite PASS | `../sweep/sweep-37e200e6/shard-3/logs/mbx.log` |
| The reviewers' probes on the fixed mover | R712's `probe_dma_length.py`, R711's `dma_reviewer_plants.py` and `dma_len_probe.cpp`, unchanged | working tree = `f52e65a9`'s RTL and bench | rc 0, 27,678 checks 0 failures; `reviewer plants: 10 of 10 caught`; `length probe: 0 of 22 moves hang` | `../mover/` |
| Mailbox generator | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | `37e200e6` | rc 0, `selftest: 0 arm(s) failed` | `gen_mailbox.log` |
| rtl-fast `publication-census` | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 4`, `SV2V` sv2v v0.0.12, `YOSYS` Yosys 0.66 | `37e200e6` | rc 0, `RESULT: PASS`, `mutations: 0 of 43 rule(s) no arm proves` | `publication_census.log` |
| RTL lint ratchet | `python3 scripts/lint_rtl.py --check` | `37e200e6` | rc 0, `LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off)` | `lint_rtl.log` |
| Yosys: the mover and its adapter | `syn/yosys/run.sh --top KL_mbx_dma --top KL_mbx_wb` | `37e200e6` | rc 0, `[PASS] KL_mbx_dma cells=2294` (2,302 before the 13-bit sum), `[PASS] KL_mbx_wb cells=5`, `TAP-PURITY RESULT: PASS` | `yosys-KL_mbx_dma-KL_mbx_wb.log` |
| Vivado front-end, under the lock, after the sweep | `python3 scripts/xvlog_gate.py --check` | `cf0f978b` | rc 0, `xvlog gate: PASS (0 finding(s) == ratchet; 0 hdl/, 0 pinned processors)` (167 s) | `xvlog_check.log` |
| The mover out of context, under the lock, after the sweep | `scripts/dma_ooc.sh` (xc7a100tfgg484-2, 10 ns, default directives) | `cf0f978b` | rc 0: 396 LUTs, 700 FFs, 0 block RAM; WNS +4.775 ns, WHS +0.189 ns; 900 nets fully routed, 0 with routing errors (round 9: 395 LUTs, +4.086 ns) | `../area/dma-ooc/` |
| CPU option test | `python3 sw/builder/test_soc_options.py` | `cf0f978b` | rc 0, `RESULT: PASS` | `soc_options.log` |
| Split memory test | `python3 sw/litex/test_ctrl_memory.py` | `cf0f978b` | rc 0, `RESULT: PASS` | `test_ctrl_memory.log` |
| End-station builder | `python3 sw/builder/test_builder.py --require-rv32` | `cf0f978b` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11, the historical Arty report not on disk, as in rounds 3 to 10 (1,732 s) | `builder_require_rv32.log` |
| rtl-fast `firmware-boundary` | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `c36a7640` (and `cf0f978b`) | rc 0, `ctrl_boundary: PASS` (0 findings, 6 boundary, 167 pin and 4 figure controls, 0 misbehaved). At `37e200e6` it refused `share.py` (section 7) | `ctrl_boundary_without_verilator-final.log` (`c36a7640`), `-cf0f978b.log`, `-37e200e6.log` |
| rtl-fast `firmware-verilator` | `... --only verilator` | `c36a7640` (and `cf0f978b`, `37e200e6`) | rc 0, `ctrl_boundary: PASS` (0 findings, 112 boundary controls) each | `ctrl_boundary_only_verilator-final.log` (`c36a7640`), `-cf0f978b.log`, `-37e200e6.log` |
| The full sweep, four `native-shards.py` units on 0-3, 4-7, 8-11, 12-15 | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, pinned Verilator 5.050 and sv2v v0.0.12 | `37e200e6` (since: `cf0f978b`, docs) | rc 0 each (4,520, 3,838, 5,063, 3,646 s): 15, 17, 16 and 16 suites pass, 64 of 64; 250,913 + 1,536,446 + 380,086 + 445,349 = 2,612,794 checks, 0 in-suite failures, 0 timed out. Shard 3's 60,354 more than round 10's are the mover bench's new checks | `../sweep/sweep-37e200e6/` (`tally.md`; files over 200 KB in `large-files.txt`) |
| The harness's self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | `c36a7640` | rc 0, `self-test: 0 failures`: 118 checks, 91 mutants caught (109 and 80 before this round) | `docs/harness_selftest.log` |
| S2's harness, 16 legs and the experiment's 2 | `run.py --point 1x1/8x8 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings --record-share-findings`, arm B `--variant answering-ports`, `--cpu-hz 100000000` for the 100 MHz legs | `37e200e6` (D11: + the drafts; X11: + the experiment) | rc 0 each, `4 groups graded, 0 refusals` (section 5) | `../measure/` |
| The harness's controls | `--fetch-l1 none --mutation slow-adp-rx`; `--fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown`; `--fetch-l1 none --cpu-regions as-built`; `--cpu-regions as-built` | `cf0f978b` | rc 0 each: `CONTROL slow-adp-rx caught` (48.697 ms), `CONTROL slow-adp-shutdown caught` (48.933 ms), `CONTROL as-built caught` (cause 5) on both cores | `../controls/` |
| Python, C++, SV idiom and naming gates | `scripts/check_py_idiom.py`, `check_cpp_idiom.py`, `check_sv_idiom.py`, `measure_naming.py --check` | the working tree before `c4ed271f`; again in the docs runner at `c36a7640` | rc 0: `too many parameters: 7 <= 7`, the others within their ratchets | `docs/` |
| Docs workflow, bare-metal scope, idiom gates, `ci_events`, harness self-test, CPU option test, `behave` (96 gates) | `scripts/docs_gates.sh` (`gates_s2b3.py`), with round 10's HDL-reference interpreter | `c36a7640` | rc 0, `0 of 96 gates nonzero or left the tree dirty`: `docs_check: 0 finding(s) across 211 md files`, `check_em_dash: 0 finding(s) over 3548 added line(s)`, `TOC gate: OK`, `baremetal-only: OK (0 findings across 1455 tracked first-party file(s))`, `NAMING RATCHET: PASS`, the Python idiom gate within its ratchets (`too many parameters: 7 <= 7`, `over-long line: 0 <= 0`), `ci_events: OK`, the harness `self-test: 0 failures`; `cd tests && behave`: 14 features, 406 scenarios, 1,977 steps passed. At `b58274ad` the bare-metal scope gate refused the plants' names (section 2.6) and the run was stopped | `docs/` (`bdd_conformance.log` and `ci_events_selftest.log` over 200 KB, in `large-files.txt`; `bdd_conformance-tail.log`) |

Not run:
- lwSRP's own suite on the draft `fc06e7c0`: the draft is unchanged since round 8 and this round does not touch lwSRP; round 9's result stands (`Completed "main": 26690 passes`), and the draft's code runs in the eight with-drafts legs.
- the CI command table's checker (`scripts/ci_tool_inventory.py --check`), which needs the CI image's checksum-pinned shell parser, as in rounds 8 to 10. This round changes no CI command.
- an out-of-context route of the split CPU: its netlist is round 9's.
- the linked images at four points: no firmware source changed but two comments, and the 1x1 and 8x8 images are byte-identical to round 10's, so the planned block RAM is round 10's, 36.5 / 40.0 / 50.0 / 56.5 RAMB36.

## 7. Findings, conflicts, decisions needed

- **STOP.** At the product's split CPU clock, 50 MHz, with the bus at 100 MHz:
  - 1x1/1if fits every row the CPU decides and every pass, in both arms, with the drafts or not; the least margin is the last SRP record's, 17.81 ms against 18 (0.19 ms);
  - 8x8/2if misses: the last AECP record 24.02 to 25.61 ms against 20, the last SRP record 25.45 to 28.25 ms against 18, and 23 to 32 passes of each run over the 2.0 ms share, the longest 3.47 ms. The drafts take 0.9 to 2.6 ms off those rows and do not close them (R711's inference, now measured).
- **Decision needed (owner): the split CPU's clock.** At the 100 MHz option every row the CPU decides fits at both points (round 10's figures, reproduced cycle for cycle through the committed option), and one or two 8x8 passes are over the share by up to 0.30 ms. The SoC's clock is unchanged, as assigned.
- **Decision needed (owner): the share against the rows at 8x8.** Splitting a pass by the loop's own constant (`CTRL_LOOP_RX_PER_PASS` 1, a labelled experiment at both clocks) does not fit both: at 100 MHz every pass fits and the last SRP record misses (20.86 ms against 18); at 50 MHz 18 passes stay over and the SRP and ACMP rows lengthen. The constant is owner decision D4(b)'s, and the bounds of ADP, ACMP, MAAP and SRP (`*_PASS_MAX`, `ACMP_MBX_RX_PASSES`, `srp_bounds.h`) and MAILBOX_SPLIT's pinned table are charged per record a pass, so changing it is a restatement of those bounds too. Not committed.
- **Finding: the passes over the share before any load are lwSRP's MRP work** (three a group at 8x8 and 50 MHz, about 200 ms apart, 2.02 to 2.41 ms; about half `mrp_mad`). No record count reaches them; bounding them is a change to lwSRP's transmit or to SRP's per-pass MRPDU (`SRP_MBX_POLL_FRAMES`), which this round did not attempt. At 100 MHz they fit.
- **Finding: the coverage ratchet compares fractions.** With the record-mover arm's build removed, `mbx.c` measures 324/324, the fraction recorded as 330/330, so it is not refused; the refusal comes from `plat/mbx_dma.h`, which only that build measures (`FINDING: sw/firmware/ctrl/plat/mbx_dma.h: recorded in the ratchet, but nothing measured it`, `receipts/findings/plant-coverage-without-dma-arm.log`).
- **Finding: the firmware boundary gate refused the new `share.py`** because its docstring names `ctrl_loop.h` by path (`receipts/findings/ctrl_boundary_without_verilator-37e200e6-share-unclassified.log`); `cf0f978b` classifies it as compiling nothing.
- **For review:** the share counts every work pass of a group's run, the boot's included, since a pass is the only opportunity to take an input whenever it runs. FR_NFR's 12 ms IN_PROGRESS bound is not one of the harness's families (no measured row answers IN_PROGRESS), so the tightest family bound stays SRP's 18 ms, as the assignment states; with it the share would be 12 / 9 = 1.33 ms.
- **For review:** the mover's fix forms the word count in 13 bits instead of defining a refusal; every length the field takes then obeys the contract, so a refusal range would only narrow the interface.
- **Not in this round, as before:** the egress-held rows (tsn-c-stack #26), the drafts' repository reviews, the block-RAM ledger, the host suites' 10 ms.

## 8. Run history

- 2026-10-29 22:02 CET start; assignment, both reports and round 10's handoff read; 22:07 TAKEN (issuecomment-6508368437).
- 22:0x-22:14 the mover's 13-bit sum, its bench's D10 and the three checks, four plants; the bench (420,827 checks) and 21 of 21 plants; the reviewers' probes against it (`receipts/mover/`).
- 22:14-22:20 the driver's record-mover arm test, its eight plants (the direction plant first broke the build, `unused parameter 'to_ring'`, and was rewritten), `fw_coverage.py --write`.
- 22:20-22:33 the harness's clock option and per-pass share, the self-test's checks and mutants; the Python idiom gate refused two functions over six parameters (`too many parameters 9 > ratchet 7`), fixed before the commit.
- 22:35 `f52e65a9`, `56f563e3`, `c4ed271f`, `37e200e6`.
- 22:40 the sweep's four shards on 0-15; 22:41 the first four legs on 16-31; 22:42 the firmware self-test's four shards on 64-79.
- 23:0x the gates; `ctrl_boundary.py --without verilator` refused `share.py` (it names `ctrl_loop.h` by path and was not classified); 23:19 `cf0f978b`, the gate again.
- 22:41-00:01 the 16 legs in four batches on 16-31 (17 to 21 minutes each); 23:01-23:42 the experiment's two legs on 76-79.
- 23:26 the coverage gate's plant; 23:42 the controls at `cf0f978b`; 23:36 the builder.
- 23:45-00:05 the sweep's shards finish, rc 0 each; 00:06-00:10 under the Vivado lock: `xvlog_gate.py --check`, then the mover out of context.
- 00:10 `b58274ad`; the docs runner refused at the bare-metal scope gate (`dma-rx`, `dma-tx`, `dma-ring` in the plants' names, five findings), stopped; 00:14 `c36a7640`; the campaign's shard 1, both boundary steps and the docs runner again at it.
- 00:46 STOP posted: issuecomment-6511234544.
