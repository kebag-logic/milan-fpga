[R756] POSITIVE - exact head 4ee2aa9654196a00876dedade4b2e987c9c06e64

# R756-2: external independent review of PR #826 (#814), round 4 delta

- PR: kebag-logic/milan-fpga #826, `814-soc-timing-cut` -> `dev`.
- Exact head: `4ee2aa9654196a00876dedade4b2e987c9c06e64`, tree `ec3c136a86bad6c8e27cc4fefae4d8c23e81582d`. These match `gh pr view` (`receipts/pr826_view.json`): base `dev` at `1e80128f`, seven commits.
- Delta reviewed: `8b28ebaf..4ee2aa96`, the head R756-1 reviewed. It is two one-line commits with no trailers:
  - `0d4a899f`: the ZQCS timer hold in `sw/litex/milan_soc.py` and its test arm.
  - `4ee2aa96`: the stall arms, the S-1 fix to F2, two harness fixes and `docs/testing/TESTING.md`.
  - `git diff --stat`: `milan_soc.py` +21 -3, `test_soc_timing_cuts.py` +405 -30, `TESTING.md` +15 -1.
- Code the delta does not touch keeps its R756-1 lens verdict unless the delta changes what it depends on: `AXIReadyStage`, `SPIPHYStage`, `stage_spi_phy`, `MilanSoC.add_spi_flash`, `add_staged_sdram`, the inventory entry, the stand-in and `CLOCK_DOMAINS.md`. None of their dependencies changed.
- Authorities read:
  - AGENTS.md;
  - the #814 round-4 ruling, issuecomment-6532211135 (option (a); stall arms; re-route on three directives under #818 at `50e5d08d`; record not re-recorded);
  - my own R756-1 report, issuecomment-6532064254;
  - the pinned LiteDRAM `core/refresher.py` (`RefreshTimer`, `Refresher`), `core/controller.py` (`refresh_cls`, `refresh_zqcs_freq`) and `modules.py` (`MT41J256M16`);
  - the executor's round-4 packet `review-evidence/814-r1/author-r4` at `fdae2980`, fetched read-only into a scratch bare repository.
- Stack: migen `4c2ae8df`, litex `a1e1c365`, litedram `f9b75e03`, litespi `02d5a209`, on Python 3.14.8 (`receipts/litex_stack_identity.txt`).
  - LiteX carries the project patch series: the VexiiRiscv core and the BIOS `main.c`, plus an untracked BIOS `xz/` source directory.
  - None of the classes under review touches those files.

## Verdict

POSITIVE. Both round-1 MINORs are fixed at their cause, and so is S-1. Every lens is clean at this head. No BLOCKER, MAJOR or MINOR is open.

1. **ZQCS (R756-1 F-1): fixed by option (a).** `RegisteredRefresher` holds LiteDRAM's ZQCS timer in reset for one cycle after sys reset (`milan_soc.py:2466-2469`). On an idle controller, every DFI command is LiteDRAM's own exactly one cycle later. That includes precharge-all, REFRESH and every ZQCS, also after the timer re-phases. I checked this past the test's window, at three ZQCS periods, against independent mutants.
2. **Stall paths (R756-1 F-2): fixed.** F6 and D6 stall each stage output at random, and both kill every lossy, drop-held, duplicating and VALID-waits-on-READY stage I or the executor planted.
   - The planted stages that survived at `8b28ebaf` are now KILLED.
   - All 10 of R756-1's mutants and all 4 of the executor's are KILLED.
   - All 11 of my new independent mutants are KILLED, and the one equivalence control survives as it should.
3. **S-1 (F2's planted path start): fixed.** F2 now counts only forward paths that start at a register of the AXI-Lite-to-Wishbone bridge (`test_soc_timing_cuts.py:394`).

Three SUGGESTIONs and two RESIDUEs are recorded below. None of them makes the verdict NEGATIVE.

## Findings

No BLOCKER, MAJOR or MINOR.

### S-A SUGGESTION - Tests - `sw/litex/test_soc_timing_cuts.py:944-979` (refresh DFI arms), `scripts/run_litex_sims.sh:110` - the member's wall time is close to the aggregate's 900 s limit and goes over it on a loaded host

**Evidence.**

- Standalone at the head, I measured 597.5 s user and 600.7 s wall, 23 checks `RESULT: PASS` (`receipts/head_test_timed.log`). The executor measured 585 s.
- The same run beside 15 other simulation jobs, on a host with a load average up to 44 on 16 CPUs, took 981 s wall (`receipts/head_test_soc_timing_cuts.rc`). That is over `LITEX_SIM_TIMEOUT`'s default of 900 s wall a member.
- The aggregate fails safe. Its self-test proves a wall-clock kill is UNKNOWN (exit 92), never a pass. So this is not a vacuous gate.
- The hosted `elaborate` job runs both the aggregate's self-test and the full aggregate (`.github/workflows/elaborate.yml:487-488`), so the limit binds hosted CI as well as local runs. That job was still queued at this head when I sampled it.
- The other reviewer's R755-2, read after this verdict was written, reports about 369 s wall on the hosted runner. So the hosted margin is wider than the local one.
- The executor records the risk openly. The REVIEW READY says "about 585 s CPU against the aggregate's 900 s member limit (about 405 s before)", which matches my measurement.

**Impact.** On a busy bench, or a slow hosted runner, an aggregate run can come back UNKNOWN for this member, costing a rerun. It cannot pass a defect.

**Suggested outcome.** Cut the cost of the six refresh DFI simulations, which take most of the time. Each builds and simulates the whole `DramSoC` for 3,200 to 3,300 cycles. Possible ways:

- Z3's two runs could stop at their last expected command.
- The plain runs could be shared between Z3 and Z4.
- The member could get an explicit, larger limit.

The executor already lists this as an open risk, so no action is required for this PR.

**Verification.** The member's standalone wall time, with a margin against 900 s that is recorded on the PR.

### S-B SUGGESTION - Tests, Robustness - `sw/litex/test_soc_timing_cuts.py:530-549`, `:712-736` - each stall arm runs one random seed

**Evidence.**

- F6 and D6 each use seed 814.
- That seed holds beats on every registered READY: tx 74, rx 36, aw 131 and ar 141 held cycles (`receipts/head_test_timed.log`).
- It kills every planted mutant in this round (table below), so the single seed is sufficient for the defects planted.
- The flash arm costs about 15 s a run.

**Suggested outcome.** Optionally, run F6 on two or three seeds. My R756-1 transparency probe ran 3 seeds. That covers more stall interleavings, such as a stall on the last beat of a burst, at little cost.

### S-C SUGGESTION - Conformance - LiteDRAM `modules.py` `MT41J256M16` with LiteDRAM's `ns_to_cycles` (pinned `f9b75e03`) - LiteDRAM rounds tREFI up. This predates the PR and the PR does not change it.

**Evidence.**

- LiteDRAM declares tREFI = 64 ms / 8192 = 7,812.5 ns. At 100 MHz its controller settings give 782 sys cycles, which is 7,820 ns (`receipts/equiv_842_staged.log`: `tREFI 782 tRP 3 tRFC 52 tZQCS 16`).
- JEDEC DDR3 specifies an average refresh interval of 7.8 µs for Tcase up to 85 °C.
- The staged and unstaged REFRESH spacing are both exactly 782 cycles (`receipts/compare_equiv.log`). So this PR keeps LiteDRAM's declared interval exactly, which is the property the round asks for.

**Suggested outcome.** If the project wants the interval at or under JEDEC's figure, open a separate issue to evaluate it: LiteDRAM's rounding, or a project override of tREFI. It is out of #814's scope.

### R-1 RESIDUE - Docs - `docs/testing/TESTING.md:746` - one line is not wrapped like the paragraph around it

The paragraph wraps at 72 to 77 characters, but line 746 is 93 characters long. That line reads "at reset, which issues no ZQCS there, must fail that arm. Then each stage's output is stalled". This is layout only. It renders the same, and it changes no claim.

**Exact fix.** Rewrap lines 746-747 so that "Then each stage's output is stalled" starts line 747.

### R-2 RESIDUE - Docs - `sw/litex/milan_soc.py:2447` - "again" in the `RegisteredRefresher` docstring

The line reads "10^8, with gcd 2, so an idle controller would never issue ZQCS again". Without the hold, the staged controller issues no idle ZQCS at all, not none after a first one (R756-1's `probe_zqcs_phase.log`). This is wording only.

**Exact fix.** Replace "would never issue ZQCS again" with "would never issue ZQCS".

## Evidence for each lens

### Conformance - CLEAN

- **The ruling's item 1, option (a), is met.**
  - `milan_soc.py:2466-2469` adds a `started` flip-flop, reset to 0. It wraps `refresher.zqcs_timer` in `ResetInserter`, with reset `~started`.
  - The exported Verilog diff between `8b28ebaf` and `0d4a899f` is the executor's receipt `route-0d4a899f/verilog-difference-8b28ebaf-to-0d4a899f.txt`. It shows exactly that change, and nothing else in the logic:
    - `milansoc_milansoc_sdram_started`, set to 1 every cycle and cleared by sys reset;
    - `if (milansoc_milansoc_sdram_reset) zqcs_timer_count1 <= 27'd99999999`, which is the timer's reload value of 10^8 - 1.
- **Why one cycle is exact.** In LiteDRAM's `Refresher`, the free-running refresh timer starts the request.
  - The registered `cmd.valid` delays the grant, `sequencer.start`, and so every `sequencer.done`, by exactly one cycle.
  - DO-REFRESH starts a ZQCS only when `zqcs_timer.done` lands on `sequencer.done`. Starting that timer one cycle late keeps the coincidence.
  - The timer re-phases on `zqcs_executer.done`, which is itself one cycle late, so later re-phases keep the shift on their own.
- **Measured inside the test.** Z4, with a 6-cycle period in gcd class 2 with tREFI 782, gives staged ZQCS at [2411, 3193] against LiteDRAM's [2410, 3192]. The full command lists are equal after the one-cycle shift. Z5, the undelayed stage, fails (`receipts/head_test_timed.log`).
- **Measured past the test's window.** `scripts/probe_zqcs_equiv.py` and `scripts/compare_equiv.py` cover 12,000 idle cycles, three periods and three refresher classes (`receipts/compare_equiv.log`, `RESULT: PASS`).

  | Period (gcd with 782) | LiteDRAM's ZQCS | Staged ZQCS | Staged equals LiteDRAM +1 | Undelayed stage |
  |---|---|---|---|---|
  | 842 (2, R756-1's probe period) | [846] | [847] | yes, 32 commands | no ZQCS; differs at command 2 |
  | 10 (2) | [3974, 7884, 11794] | [3975, 7885, 11795] | yes, 36 commands, through two re-phases | no ZQCS; differs at command 10 |
  | 1001 (1) | none in window | none | yes, 30 commands | equal (uninformative) |

- **JEDEC and the declared intervals.** Both the staged and the unstaged runs have:
  - REFRESH spacing exactly 782 cycles, LiteDRAM's declared tREFI;
  - precharge-to-command spacings identical to LiteDRAM's, so tRP 3, tRFC 52 and tZQCS 16 sys cycles are LiteDRAM's own.

  The ZQCS period is LiteDRAM's `refresh_zqcs_freq` of 1 Hz, unchanged, and it is only phase-shifted by one cycle. DDR3 sets no maximum ZQCS interval. LiteDRAM's tREFI rounding is S-C, outside the delta.
- **Under traffic.** The docstring (`milan_soc.py:2452-2454`) and the PR body say that whether a ZQCS coincides depends on the traffic, with or without the stage. That is correct: the grant waits on the bank machines in both designs. It is no change of contract, and option (a) asks only for the idle decision.
- **Ruling item 4 (re-route), from the executor's receipts. I did not reproduce them.**
  - `gate818/gate-head.txt` is `50e5d08d`. `gate818/check-set.log` gives `RESULT: PASS`, rc 0, and selects ExtraTimingOpt at +0.406 ns.
  - The worst corners are: ExtraPostPlacementOpt +0.322 / +0.031, AltSpreadLogic_high +0.126 / +0.035, ExtraTimingOpt +0.406 / +0.036.
  - The selected route is Slow +0.406 / +0.099 and Fast +1.583 / +0.036, so every directive meets the floor (WNS +0.030, WHS 0) at every corner. No STOP applies.
  - The controls behave as expected: shipping alone rc 0, no set rc 2, a comparison directory alone rc 2. All three directives report rc 0 in `vivado-rc.txt`.
  - `git diff --name-only 0d4a899f 4ee2aa96` is `docs/testing/TESTING.md` and `sw/litex/test_soc_timing_cuts.py`. No build script, tcl, Makefile or workflow imports the test; `milan_soc.py` names it only in a docstring. So the route at `0d4a899f` stands for the head's bitstream inputs.
- **Record rule.** The area record is not re-recorded, as issuecomment-6525285974 requires. That is not a finding.

### RTL - CLEAN

- `ResetInserter()(refresher.zqcs_timer)` is applied before the outer module is finalized, so its reset reaches the timer's only sync statement. The exported Verilog confirms it at the highest priority.
- `started` is in the sys domain under the same reset as the controller, so every sys reset re-arms the one-cycle hold.
- The `hasattr(refresher, "zqcs_timer")` guard matches LiteDRAM, which builds the timer only when `tZQCS` is set. Modules without ZQCS get no hold and have no ZQCS.
- The hold adds one flip-flop and one reset term to a 27-bit counter, with no new path from the timer into the bank machines. Z0 to Z2 are still green: the request is the stage's own flip-flops, 143 readers, and the planted unstaged refresher is named.
- The registered request and the `ready` pass-through are unchanged from `8b28ebaf`.
- `AXIReadyStage` and `SPIPHYStage` are unchanged since R756-1's RTL pass.

### Robustness - CLEAN

- **The backpressure paths now under the gate.**
  - F6: the PHY's command READY is random and also gated by LiteSPI's own `LiteSPICSControl`, at its default cs_delay, on the delayed chip select. The core-side data READY is random. Result: 12 of 12 words, tx 74 and rx 36 held cycles, no broken hold, the same chip-select edges and commands as the wired build.
  - D6: LiteDRAM's aw and ar READY are random, under back-to-back writes and then reads beside writes, with random VALID gaps on every master channel. Result: 20 of 20 writes and 12 of 12 reads in issue order, one response each, aw 131 and ar 141 held cycles, no broken hold.
- **The harness never makes VALID wait on READY.** `gated()` (`test_soc_timing_cuts.py:400-404`) drives the downstream VALID from the upstream VALID and the random gate, never from READY.
- **`FaceWatch`** (`:251-276`) counts a broken hold whenever an offered beat's VALID drops or its payload changes before it is taken.
- **Reset during activity.** The hold re-arms on every sys reset.
- **Configuration-dependent behaviour.** The tZQCS guard handles modules without ZQCS.
- **Idempotent re-phase.** It is shown by the period-10 run through two re-phases and by the killed `zqcs_rephase_extra` mutant.

### Tests - CLEAN

- **The head test.** `cd sw/litex && PYTHONHASHSEED=0 python3 test_soc_timing_cuts.py` gives 23 checks, `RESULT: PASS`, rc 0, both in the campaign run and standalone (`receipts/head_test_soc_timing_cuts.log`, `receipts/head_test_timed.log`).
- **Every mutant is KILLED** (`receipts/mut1_*`, `receipts/authmut_*`, `receipts/mut2_*`):

  | Set | Mutant | Result | Killing arm |
  |---|---|---|---|
  | R756-1 runner | axi_ar_unstaged, axi_pipevalid, spi_cs_comb, spi_tx_no_pipe_ready, ref_last_comb | KILLED | D0/D1, D0/D4, F0/F1, F0/F1, Z0/Z1 |
  | R756-1 runner | **axi_lossy_ready** | KILLED (survived at `8b28ebaf`) | D6 |
  | R756-1 runner | **spi_tx_lossy_ready**, **spi_rx_lossy_ready** | KILLED (survived at `8b28ebaf`) | F6 |
  | R756-1 runner | ref_ready_registered, ref_no_last | KILLED | Z3 (Z4) |
  | executor `mutants_round4.py` | axi_dropheld | KILLED | D6 |
  | executor | spi_tx_dropheld, spi_rx_dropheld | KILLED | F6 |
  | executor | ref_zqcs_done_delayed (the done pulse delayed instead of the start) | KILLED | Z4 |
  | new, `mutate_r2.py` | zqcs_hold2 (timer held two cycles) | KILLED | Z4 |
  | new | zqcs_rephase_extra (one more hold the cycle after every ZQCS end) | KILLED, ZQCS [2411] only | Z4 |
  | new | zqcs_hold_both (the refresh timer held too) | KILLED | Z3, Z4 |
  | new | ref_last_comb_h, ref_ready_registered_h, ref_no_last_h (R756-1's refresher mutants with the shipping ZQCS hold, so each tests its own defect) | KILLED | Z0/Z1; Z3; Z0/Z3 |
  | new | axi_valid_waits_ready, axi_dup | KILLED | D6 |
  | new | spi_tx_valid_waits_ready, spi_rx_valid_waits_ready | KILLED | F0 and F6 |
  | new | spi_rx_dup | KILLED | F6 |
  | control | ref_shipping_equivalent (the shipping hold, rebuilt independently) | SURVIVED, as a control must | Z3 to Z5 ok |

- **A first `zqcs_rephase_extra` was equivalent, and was replaced.** It held the timer on the ZQCS-end cycle itself, which is LiteDRAM's own reload cycle. It survived for that reason. Its log is kept as `receipts/mut2_zqcs_rephase_samecycle_v1.log`. The corrected mutant holds on the cycle after and is KILLED.
- **Z5 is a real check.** It runs the planted undelayed stage against the expected shifted list and stops at the first difference, after 6 commands with no ZQCS, so it can fail.
- **S-1.** F2 still names `fsm_state -> litespiclkgen_cnt` from the bridge's own registers.
- **The two harness fixes change no graded behaviour.**
  - The model PHY's memory is sized to the image, while `phy.flash` stays the real N25Q128A13, so LiteSPI and the region are unchanged. Every read is inside the image.
  - Clearing migen's tracer registry before each build gives the names a fresh process gives.
- **The executor's other gates, read and not reproduced:**
  - the LiteX aggregate: 8 of 8, none timed out, rc 0 in 1,183 s; self-test 10 of 10; the clone at the head with the six gitlinks above;
  - rtl-fast replayed against dev `56df0894`: `success; failed jobs: none`, head before and after `4ee2aa96`, tracked changes none;
  - the builder bank: `ALL GATES PASS EXCEPT 2 NOT RUN`, rc 0;
  - the docs gates: `44 steps, 0 failed, head 4ee2aa96`;
  - the full sweep: four shards, all with `complete.json` head `4ee2aa96` and exit 0, `suites: 14/17/17/16 passed`, so 64 of 64, none failed and none timed out.
- **Open risks.** Both are recorded honestly in the REVIEW READY and the PR body:
  - the runtime, 585 s CPU against 900 s (see S-A);
  - DRAM read data is not graded, because the model PHY setup masks the DFI write burst. This predates the round. D6 grades the native port's transfers and one response each.

### Docs - CLEAN

- **The `RegisteredRefresher` docstring** (`milan_soc.py:2430-2455`) now states the actual contract: idle every command is one cycle later, and under traffic coincidence depends on the traffic in both. That is R756-1 F-1's Docs part. The figures in it are what I measured: tREFI 782, period 10^8, gcd 2, LiteDRAM's first idle ZQCS at 76 s. The one wording slip is R-2.
- **The test module docstring** (`test_soc_timing_cuts.py:27-33`) and `refresh_behaviour`'s docstring match the arms.
- **`TESTING.md:738-756`** matches the code: a 6-cycle period with gcd 2, two ZQCS across a re-phase, the undelayed stage failing, the three stalled READYs, lossy plants failing, and read data not graded with its reason. The one layout nit is R-1.
- **The PR body** (`receipts/pr826_view.json`) matches the code and the receipts: 23 checks, ZQCS [2411, 3193] against [2410, 3192], route figures, `0d4a899f..4ee2aa96` touching only the test and TESTING.md.
- **Comment rule.** The delta's added lines carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID. I scanned the `+` lines of `git diff 8b28ebaf..4ee2aa96` with no hit.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_soc.py:2430-2469`; LiteDRAM `refresher.py`, `controller.py`, `modules.py`; Z4/Z5 output; `receipts/compare_equiv.log` (periods 842, 10, 1001, 12,000 cycles); executor's `gate818/*` and `route-0d4a899f/*`; `git diff --name-only 0d4a899f 4ee2aa96`; ruling issuecomment-6532211135 | R756-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| RTL | CLEAN | `milan_soc.py:2430-2469`; exported-Verilog diff `8b28ebaf` to `0d4a899f`; Z0 to Z2 at head; unchanged stages (R756-1 RTL pass, no dependency changed) | R756-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| Robustness | CLEAN | `test_soc_timing_cuts.py:194-276,400-549,712-842`; F6/D6 hold counts; stall-mutant kills; reset and tZQCS guard | R756-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| Tests | CLEAN | head test (23 checks, two runs); 25 mutants plus 1 control (`receipts/mut1_*`, `authmut_*`, `mut2_*`); executor's aggregate, rtl-fast, builder, docs and sweep receipts | R756-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| Docs | CLEAN (R-1, R-2 RESIDUE only) | `milan_soc.py` docstrings; test docstrings; `TESTING.md:738-756`; PR body; delta comment-rule scan | R756-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |

## Executed here (exact head, pinned stack, at most 16 jobs)

| What | Result | Receipt |
|---|---|---|
| `PYTHONHASHSEED=0 python3 test_soc_timing_cuts.py`, in the campaign | 23 checks, `RESULT: PASS`, rc 0, 981 s wall under load | `receipts/head_test_soc_timing_cuts.log`, `.rc` |
| The same, standalone under `time` | `RESULT: PASS`, 597.5 s user, 600.7 s wall, 87 MB | `receipts/head_test_timed.log`, `.rc` |
| `scripts/mutate_timing_cuts.py` (R756-1) × 10 | 10 KILLED | `receipts/mut1_*.log`, `.rc` |
| `scripts/author_mutants_round4.py` (the executor's, copied unchanged) × 4 | 4 KILLED | `receipts/authmut_*.log`, `.rc` |
| `scripts/mutate_r2.py` × 11, plus 1 control | 11 KILLED; control SURVIVED; the first, equivalent re-phase mutant is kept | `receipts/mut2_*.log`, `.rc` |
| `scripts/probe_zqcs_equiv.py` × 9 and `scripts/compare_equiv.py` | staged equals LiteDRAM's own one cycle later at every period; undelayed differs wherever a ZQCS falls | `receipts/equiv_*.log`, `receipts/compare_equiv.log`, `.rc` |
| `scripts/run_campaign.sh` | the job list and runner for the rows above | the script itself |
| Clone restore check | HEAD, tree and index tree equal the head; status empty including ignored; index modes and blobs equal the HEAD tree; six gitlinks as at head | `receipts/clone_restore_check.txt` |

Hosted, read only (`receipts/hosted_check_runs_4ee2aa96.tsv`, sampled during this round), 54 check runs at the head:

- 26 completed success;
- 1 skipped (Physical gPTP, nightly and manual);
- 27 queued or in progress, mostly the Verilator and Yosys shards;
- none failed.

The manager owns hosted and act acceptance. I neither claim nor infer a hosted verdict.

## Real limits

- No hardware. The flash stage has not been on hardware, and physical calibration was NOT RUN. The stall arm models the real PHY's chip-select hold with LiteSPI's own `LiteSPICSControl`, not the real PHY.
- I ran no Vivado route, no #818 gate, no full sweep, no rtl-fast, no builder bank, no docs gates, no LiteX aggregate and no manager source bank. Those figures are the executor's published receipts, which I read and spot-checked; I did not reproduce them.
  - I did not inspect the #818 gate's source at `50e5d08d`.
  - Its set self-test log in the executor's packet is empty, with rc 0 in 0 s (`gate818/selftests.txt`). I took that self-test from the receipt as given.
- The shipping one-second ZQCS period cannot be simulated. That it is equivalent rests on three facts:
  - the measured equality at periods 6, 10 and 842, all in the shipping gcd class;
  - the mutant kills;
  - the argument that every idle refresher event is shifted by exactly one cycle.
- Under DRAM traffic, ZQCS coincidence is traffic-dependent in both designs. I did not measure its rate.
- DRAM read data is not graded by the test. This is the executor's recorded risk, and it predates the round.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link the receipts. Live dev is `71d6ed07`; the source base is `1e80128f`.
- Accept the hosted and act exact-head evidence, including the 27 runs still in flight when sampled. Among them is the `elaborate` job, which runs this member inside the full LiteX aggregate.
- Carry R-1 and R-2 to the residue checklist.
- Optionally route S-A, S-B and S-C. S-C would be a separate issue, outside #814.
- Re-record the area record on dev after the last release merge (record rule). This is not a finding here.

## Prior public findings on this PR

I read and wrote this section after the verdict, the findings and the ledger above were on disk. One correction to S-A came from it: the hosted `elaborate` job also runs the full aggregate, so the 900 s limit binds hosted CI too. The S-A evidence above is now corrected. The verdict and the ledger are unchanged.

PR #826 has no review bodies and no inline review comments. Its issue comments are the manager's review-start notices, R756-1, R755-1, and the other reviewer's R755-2 at this head (6537580432, POSITIVE).

| Prior finding | Status at `4ee2aa96` | Evidence |
|---|---|---|
| R756-1 F-1 MINOR (Conformance, RTL, Tests, Docs): the registered refresher changed whether LiteDRAM issues ZQCS, and the docs said otherwise | **RESOLVED** (option (a), ruling 6532211135) | The ZQCS timer hold is at `milan_soc.py:2466-2469`, and the docstring and PR text are corrected. Z4 passes and Z5 fails the undelayed plant. My period sweep gives staged equal to LiteDRAM's own one cycle later at periods 842, 10 and 1001. The done-delayed, two-cycle-hold, extra-re-phase and both-timers plants are KILLED. |
| R756-1 F-2 MINOR (Tests, Robustness): the stall path of both registered-READY stages was never exercised | **RESOLVED** | F6 and D6 hold beats in all four registered READYs. `axi_lossy_ready`, `spi_tx_lossy_ready` and `spi_rx_lossy_ready` are KILLED, and the shipping stages pass. |
| R755-1 F-1 MINOR (Tests): the behaviour arms never exercise a stage's stall path; drop-held stages survived | **RESOLVED** | It is the same defect as R756-1 F-2. Its verification is met: the hold counts are non-zero (tx 74, rx 36, aw 131, ar 141). The equivalent drop-held mutants for aw/ar, SPI tx and SPI rx are KILLED by D6 and F6 (`receipts/authmut_*`). Duplicating stages are also KILLED (`receipts/mut2_axi_dup`, `mut2_spi_rx_dup`). |
| R755-1 F-2 MINOR (Conformance, RTL, Tests, Docs): idle ZQCS stopped behind the registered refresher | **RESOLVED** | It is the same defect as R756-1 F-1. A shortened-period arm, Z4, passes on the fix and fails on the other refresher, Z5. |
| R755-1 S-1 SUGGESTION (Tests): F2's filter did not tell the bridge from the core | **ADDRESSED** | `test_soc_timing_cuts.py:394`: F2 now filters on starts within `registers(bridges[0])`, and still names `fsm_state -> litespiclkgen_cnt`. |
| R755-2 S-2 SUGGESTION: D7 plants aw and ar together | Not a finding of mine. I **concur** that it is optional | My `axi_*` mutants plant both channels, as D7 does. So I have no ar-only evidence of my own, and I rely on that report's `axi-dropheld-ar` kill. |
| R755-2 S-3 SUGGESTION: no structural check that VALID never waits on READY | I **concur** that it is optional | My full VALID-waits-on-READY plants are KILLED by D6 and F6, through zero holds. A stage that waits only while it holds a beat is not planted by me either. |
| R755-2 S-4 SUGGESTION: runtime margin against 900 s | The **same** as my S-A | Independent figures agree: 981 s wall here under load, and 973 s there. |
| R755-2 R-1 RESIDUE: `TESTING.md:746` wrap | The **same** as my R-1 | — |

No prior finding is retained as open.

R756-2 FINISHED
