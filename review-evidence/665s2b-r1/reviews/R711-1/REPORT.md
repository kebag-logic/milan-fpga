[R711] NEGATIVE - exact head f884c7e9fb71cdb94c12e3228b1412801c34e1f4

Round R711-1, internal cleared-context review of PR #810 (#665 lane S2b) into `dev-soft-core`. Head `f884c7e9fb71cdb94c12e3228b1412801c34e1f4`, tree `40ee92bf67435d4a2dd31ab2373ad05c9bdf24f5`, source base `f4c9ad4f`. Whole-PR review of `git diff f4c9ad4f..f884c7e9` (79 files, 46 commits, the merge `c5676878` included). All five lenses applied. Prior review findings on this PR: none exist (its only comment is the review-start notice), so none to resolve or retain.

## Verdict in one paragraph

The grading rule, the record mover, the word-wise primitives, the merge and the block-RAM ledger statement hold up. The PR's central claim does not. "Every row the CPU decides fits its own bound, at both points" comes from an uncommitted harness variant that runs the split CPU at 100 MHz. At this head the product clocks the split CPU from the 50 MHz Milan clock, the tree's own documents say so, and the owner decided on 2026-10-29 05:33 that there would be no clock increase. The PR's own `How to validate` command, run with the committed harness at the product clocks on byte-identical images, gives these 8x8/2if results:

- the last AECP record takes 22.8 to 25.0 ms against its 20 ms bound;
- the last SRP record takes 22.9 to 28.2 ms against its 18 ms bound.

That is a measured NFR-SCOUT-03 breach at the product configuration (F1, BLOCKER). There are three MINOR findings: a length-wrap hang in `KL_mbx_dma` (F2), gaps in the mover's bench (F3), and an untested firmware DMA arm (F4). Two items are RESIDUE.

## Findings

### F1 - BLOCKER - Conformance, RTL, Tests, Docs - the composed rows fit only at a CPU clock the product does not run

**Where:**
- `docs/design/SPLIT_CONTROL_MEMORY.md:844`, `:968` and `:998`: "Every figure here is at the 100 MHz CPU clock, measured with section 11's profiling variant".
- Section 13's tables and conclusions, `:990`-`:1060`.
- The PR body: Status ("Every row the CPU decides fits its own bound"), the rows table "at 100 MHz", and "How to validate" with its stated expected result.
- `tb/verilator/ctrl_service_budget/README.md:7` and `:113`.
- The author's evidence:
  - `review-evidence/665s2b-r1/author/receipts/measure/*/label.txt`: "CPU 100 MHz, bus 100 MHz ... CSB_CPU_HZ=100000000";
  - `author/receipts/variants/harness-profile-merged.patch`: "Labelled test-only variant ... not committed: the CPU clock from CSB_CPU_HZ".

**Authority:**
- NFR-SCOUT-03 (`docs/reference/FR_NFR.md:324`) and FR_NFR 3.4.1 (`:334`-`:350`) require each moved path to meet min(T_svc, C). That is SRP 18 ms (`:343`) and AECP 20 ms (`:345`).
- The owner decided on 2026-10-29 05:33 (#665 issuecomment-6488028169): "no clock increase. The split CPU and its bus keep their present clocks."
- The round-9 and round-10 exits (issuecomment-6495692075 and -6502579312): STOP if a CPU-decided row misses its bound at either point.

**The product's split CPU clock at this head is the Milan clock:**
- `sw/litex/milan_soc.py:3200`: `self.cpu.cpu_clk.eq(ClockSignal("milan"))`.
- `milan_clk_hz: 50000000` in `configs/endstation_ax7101_8x8.yaml:56` and in `configs/endstation_ax7101_1x1_tdm8.yaml:44`.

**The tree's own documents call these the product or shipping clocks:**
- `SPLIT_CONTROL_MEMORY.md:462`: "the product clocks are unchanged, the CPU at 50 MHz and its bus at 100 MHz".
- `SPLIT_CONTROL_MEMORY.md:322`, `:356` and `:445`: "the shipping clocks, the CPU at 50 MHz".
- The harness README, `:7`: "Every figure is a measured clock count at the CPU's 50 MHz".
- The author's own controls receipt, `author/receipts/controls/README.md`: "product clocks (CPU 50 MHz, bus 100 MHz), no variant".

**Measured** (`receipts/h50-8x8-A.*`, `receipts/v100-8x8-A.*`, `receipts/clock_ab.md`). I ran the committed harness at this head, no variant:

```
run.py --point 8x8 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings
```

- The run's `build.json`: `cpu_hz` 50,000,000, `sys_hz` 100,000,000, netlist `VexiiRiscvLitex_c05c5a8e0bd42fc384567409f2a37e64`.
- The image is byte-identical to the author's leg N10-A8 (sha256 `f80111d8...3e3f7f`).
- Result: `13 budget misses (13 of 49 probe instances, 4 of 17 paths)`, against the author's 6.
- The seven extra misses are all CPU-decided:

| 8x8/2if arm A, last record | bound | CPU 50 MHz (product clocks, committed harness) | CPU 100 MHz (published variant) |
|---|---:|---:|---:|
| `backlog.service.aecp.last.if1` | 20 | **22.844** | 13.959 |
| `backlog-adp.service.aecp.last.if1` | 20 | **25.023** | 15.096 |
| `backlog-adp-refill.service.aecp.last.if1` | 20 | **25.001** | 15.080 |
| `backlog.service.srp.last.if1` | 18 | **24.707** | 14.286 |
| `backlog-adp.service.srp.last.if1` | 18 | **28.249** | 16.949 |
| `backlog-adp-refill.service.srp.last.if1` | 18 | **27.611** | 16.572 |
| `backlog-owed.service.srp.last.if1` | 18 | **22.886** | 13.655 |

**The clock is the only difference.** I applied the author's published variant patch in a scratch clone at the same head and ran with `CSB_CPU_HZ=100000000`. Its `table.md` is identical to the author's N10-A8 `table.md`.

**At 1x1/1if at the product clocks** (`receipts/clock_1x1_50.md`, `receipts/h50-1x1-A.*`):
- only the egress-held rows miss;
- the last SRP record takes 17.807 ms against 18, a margin of 0.19 ms;
- the last AECP record takes 15.950 ms.

**Not measured: the with-drafts legs at 50 MHz.** At 100 MHz the drafts took at most 1.4 ms off these rows (the PR's own table). The excess at 50 MHz is 2.8 to 5.0 ms on AECP and 4.9 to 10.2 ms on SRP. That suggests the drafts would not close the misses, but it is an inference, not a measurement.

**The conflict is not published,** as AGENTS.md section 2 requires:
- `SPLIT_CONTROL_MEMORY.md:706` says "The owner kept the product clock", and `:711` measures every figure "at the 100 MHz CPU clock".
- The round-7 to round-10 assignments call 100 MHz "the product clock", while the tree clocks the CPU at 50 MHz.
- Neither the PR nor the docs raise this.

**Impact:**
- As built at this head, the split placement misses NFR-SCOUT-03 at 8x8/2if on the AECP and SRP record paths.
- The STOP condition of rounds 9 and 10 is met at the product configuration.
- A merge would record in the authoritative design page, and in FR_NFR's evidence, that every CPU-decided row fits. That is false for the product.
- The PR's own validation command does not reproduce its stated expected result: it gives 13 misses, not 6.

**Required outcome:** one of the following.
- (a) The owner records that the split CPU's product clock is 100 MHz, and then:
  - the tree clocks the split CPU at 100 MHz: the SoC change, its out-of-context and integrated timing, with the all-fabric placement unchanged;
  - the committed harness measures that clock by default.
- (b) The rows are graded at the product's clocks, and the lane STOPs or publishes the residual and the clock conflict for decision.

Either way, `SPLIT_CONTROL_MEMORY.md` section 13, the harness README and the PR body must state the clock of each figure. None of them may present a variant clock as the product's.

**Verification:** at the merge candidate, the PR's own commands with no variant:
- `run.py --point 8x8` and `--point 1x1`, the four backlog groups, arms A and B, with and without the drafts;
- each leg shows only the egress-held misses;
- `build.json`'s `cpu_hz` equals the product SoC's split CPU clock.

### F2 - MINOR - RTL, Robustness, Tests - `KL_mbx_dma` wraps lengths 4093 to 4095 to zero words: a receive holds the host port forever, a transmit overruns

**Where:**
- `hdl/milan/mailbox/KL_mbx_dma.sv:174`: `start_words_w = 11'((len_bytes_i + 12'd3) >> 2)`. The sum is formed in 12 bits.
- The port contract, `:57`: `len_bytes_i` is "the bytes to move; 0 moves nothing".
- CMD `[27:16]`, "the bytes to move", in `sw/litex/milan_soc.py`'s `CtrlMailboxDma` and in `sw/firmware/ctrl/plat/mbx_dma.h`.

**Evidence:** `scripts/dma_len_probe.cpp` and `receipts/dma_len_probe.log`. The probe drives the mover alone, answers the host port the cycle after each request, and keeps the AXI port always ready.
- Lengths 0 to 4092 behave.
- At 4093, 4094 and 4095, a receive move:
  - stays BUSY for 200,000 cycles with no host-port request (`chunk_r` = 0 in FILL_S);
  - so every CPU access to the mailbox window is held forever, because the mover has no timeout by design (`:37`-`:39`).
- At the same lengths, a transmit move:
  - issues ARLEN 31, a 32-beat burst, which breaks the module's own "at most sixteen beats inside one 64-byte line";
  - makes 256 ring writes.

**Reachability:**
- The shipped driver cannot reach this: `mbx.c` bounds `len` by `max_frame[ch]` before every move (`:419`-`:425` and `mbx_tx_send`'s guard).
- The RTL's documented input range does accept these lengths.
- #665 requires the mailbox to port to a hard core, whose host owns these registers.

**Impact:** an out-of-range length from any host deadlocks the whole mailbox window instead of being refused.

**Required outcome:**
- Compute the word count without the 12-bit wrap, or refuse with ERR any length the field allows but no record can have.
- Add the field's maximum to the bench's lengths. Its D1 covers "every length to 96 bytes and the largest frame".

**Verification:**
- `dma_len_probe` reports 0 of 22 moves hanging, and every burst within 16 beats.
- A bench case at 4095 fails on the unfixed RTL.

### F3 - MINOR - Tests - the mover's bench cannot fail for three properties it claims

**Where:** `tb/verilator/mbx/dma_main.cpp`: D4 at `:447`-`:474`, D6 at `:507`-`:535`, and the header's D4 and D6 at `:30`-`:36`.

**Evidence:** `scripts/dma_reviewer_plants.py` and `receipts/dma_reviewer_plants.log`. I wrote ten plants and built each with the Makefile's own recipe against the tree's bench. Seven are caught. Three escape with rc 0:

- **`error-burst-continues`:** the `rerr_r` term is dropped from R_S's end test, so a transmit move that saw an error goes on reading later bursts. D6 claims "an error response ends the transfer at that burst", but it checks only ring words.
- **`fill-during-cpu-answer`:** `!ack_cpu_r` is dropped from `fill_req_w`. The first ring read of a move started in the cycle a CPU access issues is then never made, and its buffer word is taken from an unanswered cycle. D4's "a CPU read in the cycle a transfer starts" checks the CPU's word and that the move ends, but not the moved data.
- **`held-partial-write-widened`:** a held CPU write's byte strobes become `4'hF`. The contract refuses a partial strobe and counts it (`KL_mbx.sv:175`), but no bench case holds a partial write across a move.

The bench itself is sound otherwise:
- the control run gives `checks: 360473 failures: 0`;
- the author's 17 plants are all caught (`receipts/dma_bench_control.log`, `receipts/dma_author_mutants.log`);
- the RTL at this head has none of these three defects. The bench just would not see them.

**Impact:** three stated behaviours have no regression guard:
- "an error response ends the transfer at its burst";
- "an access the CPU makes meanwhile is held and made when the transfer ends";
- the data of a move started beside a CPU access.

**Required outcome:** bench checks that fail for each plant, for example:
- the AR bursts issued after an errored beat;
- the moved bytes of the start-cycle case;
- a held partial-strobe write that is still refused and counted.

**Verification:** each of the three plants is caught by a named check, and the unmodified mover passes.

### F4 - MINOR - Tests - no test compiles the firmware's record-mover arm, and its error arms never run

**Where:**
- `sw/firmware/ctrl/mbx/mbx.c:426`-`:437` (receive) and `:510`-`:521` (transmit), the `#ifdef CTRL_MBX_DMA_BASE` arms, including:
  - the ERR arm `rx_resync` at `:430`;
  - the ERR arm `MBX_STATUS_BAD` at `:515`;
  - the unaligned-frame fallback.
- `sw/firmware/ctrl/plat/mbx_dma.h`.

**Evidence:**
- `CTRL_MBX_DMA_BASE` is defined only in `ctrl_build.SPLIT_RV32_FLAGS` (`sw/firmware/ctrl/test/ctrl_build.py:81`-`:83`), and only the split image uses those flags (`ctrl_srp_image.py:90`).
- No GoogleTest, host build or plant defines it or names `mbx_dma`. I searched `sw/` and `tb/`.
- `fw_coverage.py --check` reports `mbx/mbx.c 324/324 lines, 158/158 branches` (`receipts/fw_coverage.log`). That covers the host build, which preprocesses these arms out.
- The CPU budget harness runs only the success arm; nothing there plants a DMA error response.
- The round-6 and round-7 gates, kept by every later round (issuecomment-6486770462 and -6489248781), require GoogleTest for each changed function at 100 % line and branch coverage.

**Impact:** the image's actual driver has three paths that never execute and carry no plant: the receive-error resynchronisation, the transmit refusal and the unaligned fallback. A defect there, such as a wrong ring index or an ignored ERR, would pass every gate this PR lists.

**Required outcome:** one of these:
- a host test of the mover arm: `mbx.c` built with `CTRL_MBX_DMA_BASE` over a register model of the mover, as `test_mmio_driver.cpp` does for the window. It must cover success, ERR in each direction and the unaligned fallback, be in the coverage ratchet, and carry planted defects;
- an exclusion naming these lines, published and accepted.

**Verification:** the coverage report lists the arm at 100 % lines and branches, and a plant in each arm is caught.

### RESIDUE (wording only; no verdict effect, carried to the residue checklist)

**R1:** `sw/firmware/ctrl/plat/ctrl_mem.c:7` says "The core is a cacheless RV32I hart and fetch-bound". At this head the split core is RV32IM behind a 16 KiB fetch L1 and an 8 KiB data cache.
- Fix: "The cacheless RV32I core this was written for is fetch-bound: ...", or state the split core's cached RV32IM and keep the measured reason.

**R2:** `sw/firmware/ctrl/mbx/mbx_wire.h:62`-`:64` says "(#665: the split core's data side is uncached, ...)". The split core's data side now has its data cache; only the mailbox window is uncached.
- Fix: "(#665: the mailbox window is uncached, and each byte access is a bus transaction ...)".
- `tb/verilator/ctrl_service_budget/README.md:113` says "The CPU ... RV32I", which for the split CPU should read RV32IM. Its clock statement on the same line belongs to F1, not here.

## What each lens examined (evidence for the clean parts)

**Conformance**
- The grading code matches the owner's table of 2026-10-29 12:40:
  - `scenario.py:89`-`:98`: `T_SVC_MS = 20.0`; `srp` 18, `acmp` and `disc` 20, `aecp` and `notify` 24, `maap` 50, `adp` 200;
  - `grade.py:431`-`:440`: `budget_ms` = min(T_svc, C) + W;
  - `selftest.py:228`-`:293`.
- Optional identification (15 ms) is in FR_NFR. It is not in the harness, since it is not enabled.
- Harness self-test (`receipts/harness_selftest.log`): rc 0, 109 PASS checks, 80 mutants caught, 0 escaped. It catches "SRP graded against T_svc alone" on an 18.00001 ms SRP instance, and "T_svc pinned at the 10 ms proposal".
- Five reviewer plants in a throwaway clone are all caught (`receipts/grade_reviewer_plants.log`): an SRP ceiling of 20, T_svc 10, a T_svc-only `budget_ms`, a strict budget, and an AECP ceiling of 20.
- The FR_NFR 3.4.1 margin table (`FR_NFR.md:412`-`:415`) adds up:
  - 200-1-20-1 = 178, 240-1-20-1 = 218, 250-1-20-1 = 228;
  - 256 records x 84 wire bytes = 21,504 B, which takes 0.688 ms at 250 Mb/s.
- The IN_PROGRESS 12 ms row applies the owner's min rule to the adopted 120 ms cadence and is stated as for review. It has no measured CPU row, and the PR says so.
- F1 leaves this lens UNCLEAN.

**RTL**
- `KL_mbx_dma.sv`, read in full, is correct on these points:
  - AXI4 INCR bursts of 4-byte beats, with chunks cut at the 64-byte line (`:163`-`:167`);
  - AW before W, payload held while VALID waits, BREADY and RREADY gated by state;
  - tail strobes on receive and tail lane masking on transmit;
  - ring index wrap by mask;
  - a CPU access is held (`:401`-`:406`) and issued first when idle;
  - the CPU's answer is routed by `ack_cpu_r`, under `KL_mbx`'s fixed one-cycle answer (`KL_mbx.sv:1133`, `:1146`) and `KL_mbx_wb`'s single-issue `busy_r` (`KL_mbx_wb.sv:53`-`:65`);
  - ERR is set on misalignment, a busy start, BRESP and RRESP, and cleared by an accepted start;
  - every register is reset, and naming and the file head follow CONTRIBUTING section 1.
- Wiring: in `milan_soc.py`, `CtrlMailboxDma` and `add_ctrl_mailbox_dma` register the start off `cmd.re` and chain `KL_mbx_wb`, the mover and `KL_mbx`. The harness's `split_soc.py` uses the same class.
- The mailbox contract is unchanged against `f4c9ad4f`: `sw/mailbox/mailbox.yaml`, `KL_mbx_pkg.sv`, `KL_mbx.sv` and `docs/reference/MAILBOX_CONTRACT.md`. `gen_mailbox.py --check --crosscheck --selftest` is rc 0 (`receipts/gen_mailbox.log`).
- Gates:
  - `lint_rtl.py --check` PASS, 89 <= 89 (`receipts/lint_rtl.log`);
  - Yosys PASS for `KL_mbx_dma` (cells=2302) and `KL_mbx_wb` (cells=5) (`receipts/yosys_dma_wb.log`);
  - `test_soc_options.py` PASS (`receipts/soc_options.log`): the split CPU has RV32M, the 16 KiB two-way fetch L1 and the 8 KiB data cache, with 16 killed controls; the all-fabric CPU is killed with caches or RV32M added; the flash window is uncached and not executable.
- The author's out-of-context route receipt (`author-r8/receipts/area/cpu16k2-ooc-10ns`) shows 0 routing errors, with both clocks at 10 ns.
- F1 (the measurement's clock assumption against the SoC's clocking) and F2 leave this lens UNCLEAN.

**Robustness**
- The mover handles a mid-transfer error response, a busy start, a misaligned start and a zero length. I read each against the RTL, and the bench's D5 to D8 pass. F2's boundary probe covers lengths 0 to 4095 in both directions.
- The driver bounds `len` before any move (`mbx.c:419`-`:425`, `mbx_tx_send`'s guard), so the shipped firmware cannot reach F2.
- AECP no longer clears the 1,514-byte frame, and that change is guarded:
  - `aecp_commands.c`'s `body()` zeroes each fixed body;
  - S1's `refuse()` re-runs `aecp_command`, which writes every byte it answers;
  - `test_aecp.cpp:752`-`:760` compares more than 2,000 frames over a poisoned and a cleared buffer, and shard 2 passes it.
- F2 leaves this lens UNCLEAN.

**Tests**
- The firmware self-test passes on all four shards with `--require-rv32` (`receipts/fw-shard{0..3}.log`): each shows `test_ctrl_firmware: PASS` and rc 0. Shard 1 reports `mutants: 553 of 553 caught`, and shard 0 reports `ctrl service bounds: checks: 46 failures: 0`.
- `fw_coverage.py --check` PASS over 33 files (`receipts/fw_coverage.log`). `fw_rv32_selftest.py --require-rv32` passes 25 checks. `test_ctrl_memory.py` PASS.
- `ctrl_mem.c`: my exhaustive probe (`scripts/ctrl_mem_probe.c`, `receipts/ctrl_mem_probe.log`) runs 727,392 cases with 0 failures at -O0, -O2, -Os and -O3. It covers:
  - every offset pair, and lengths up to 200;
  - overlap both ways;
  - memcmp sign and value;
  - no access past PROT_NONE fences on either side.
- The mover bench: the control passes 360,473 checks with 0 failures, the author's plants are caught 17 of 17, and my plants 7 of 10 (F3).
- The merge (`scripts/merge_sides.py`, `receipts/merge_sides.txt`): in the 11 conflicted files, every line either side added is either at the head or part of a reviewed move or rewrite:
  - the lane's index plants are in `aecp_index_mutants.py`;
  - S1's face plants are retargeted to `mbx_bus_*`;
  - S1's face TearDown and its CLOCK_DOMAIN move are rebuilt around `aecp_index`;
  - the FR_NFR rows are re-derived at 20 ms.
- F1, F2, F3 and F4 leave this lens UNCLEAN.

**Docs**
- NFR-SCOUT-01 is stated consistently in `FR_NFR.md:322`, `ARCHITECTURE_HW_SW_SPLIT.md:65`, `MARK_II_AREA_PLAN.md:383` and `SPLIT_CONTROL_MEMORY.md` section 13. The text matches the owner's amendment of 2026-10-29 10:01:
  - in the split placement, RV32IM with a 16 KiB two-way, LRU, one-refill instruction cache and the coherent 8 KiB data cache;
  - the all-fabric hart stays RV32I and cacheless.
- `docs/history` is untouched.
- The block-RAM ledger (item 7) is stated as open, not hidden:
  - `MARK_II_AREA_PLAN.md:871`-`:872`, `:895` and `:908` ("124 is 2.5 over");
  - `SPLIT_CONTROL_MEMORY.md:1059` ("commissioned separately");
  - the PR body's "Not in this round".
- The egress-held rows (item 6) are stated as open with tsn-c-stack #26 in the PR body, in section 13 and in `FR_NFR.md:424`. The PR says "Relates to #665".
- The comment rule (owner, 2026-10-15) holds. I scanned every non-Markdown line the delta adds for lane labels, rounds, reviewer IDs and comment IDs and found no instance. All 50 hits were byte "lanes", binary literals or variable names.
- F1 leaves this lens UNCLEAN. R1 and R2 are RESIDUE.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `FR_NFR.md` 3.4.1, NFR-SCOUT-01 and NFR-SCOUT-03; `scenario.py`, `grade.py`, `selftest*.py`; the committed harness at 8x8 and 1x1 at the product clocks; the published 100 MHz variant, reproduced | R711-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| RTL | UNCLEAN (F1, F2) | `KL_mbx_dma.sv`, `KL_mbx_wb.sv`, the `KL_mbx.sv` host port; `milan_soc.py` (`CtrlMailboxDma`, `ctrl_cpu_args`, the cpu_clk wiring); `split_soc.py`; lint, Yosys, `test_soc_options`, `gen_mailbox` | R711-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| Robustness | UNCLEAN (F2) | the mover's error, busy, misalignment, zero and maximum lengths; the driver's length bounds; the AECP stale-byte guard | R711-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| Tests | UNCLEAN (F1, F2, F3, F4) | the four firmware shards, coverage, the RV32 self-test; the `ctrl_mem` probe; the mover bench and 27 plants; the harness self-test and 5 grader plants; the merge-sides check | R711-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| Docs | UNCLEAN (F1); RESIDUE R1, R2 | `SPLIT_CONTROL_MEMORY.md` sections 5 and 9 to 13; `MARK_II_AREA_PLAN.md`; `FR_NFR.md`; `ARCHITECTURE_HW_SW_SPLIT.md`; the harness README; the PR body; the comment-rule scan | R711-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |

## Real limits

- **Harness legs I ran:** arm A without drafts at 8x8 and 1x1, at the product clocks, plus one 8x8 arm A leg with the published 100 MHz variant. I did not run arm B, or the with-drafts legs at 50 MHz. F1's statement about the drafts is an inference from the PR's 100 MHz deltas.
- **Gates not run here; their status rests on the author's receipts:**
  - the full suite sweep;
  - `xvlog_gate.py` (Vivado) and the out-of-context route;
  - the publication census and `test_builder.py`;
  - the docs-gate runner, `behave` and `ctrl_boundary.py`;
  - lwSRP's own suite;
  - the mailbox suite's targets other than the mover (`make` all).
- **Read only through the passing shards and coverage, not reviewed in depth:**
  - `ctrl_split.ld` and the hot-list gate (`ctrl_hot.py`);
  - the SRP adapter changes (`srp_mbx.c`, `srp_bounds.h`);
  - `ctrl_pool.c`;
  - `aecp_nvm.c`'s word scan;
  - `nvm_flash_litespi.c`.
- **Desk evidence only:** no physical calibration and no hardware. No manager source bank ran at this head, and none is claimed.
- **Clone state:** probes ran only in scratch clones or scratch build directories. The review clone is back at the head's exact bytes:
  - the index and worktree match HEAD, and the `git ls-files -s` digest is unchanged;
  - the six gitlinks (mode 160000, stage 0) match the head, and the submodules are clean;
  - the ignored files the gates generated were removed.

## Pending manager duties

- Take F1's clock conflict to the owner: the 100 MHz rows, the tree's 50 MHz CPU and the owner's "no clock increase" cannot all stand.
- Validate the current-dev merge candidate (live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks, and own hosted and act acceptance.
- Carry R1 and R2 to the residue checklist.
- Keep the external review independent of this one.

R711-1 FINISHED
