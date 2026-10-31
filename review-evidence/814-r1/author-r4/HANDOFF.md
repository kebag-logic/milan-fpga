# #814 round 4 [A703d] handoff

Branch `814-soc-timing-cut`. Round 4 adds two commits on top of `8b28ebaf` (PR #826 head), with no rebase and no force:

- `0d4a899f9c46ef50fe133d79fc550812045278dc`: the ZQCS fix and its first arm;
- `4ee2aa9654196a00876dedade4b2e987c9c06e64` (**head**): the stall arms, the two-ZQCS arm, S-1 and TESTING.md.

Nothing is pushed. REVIEW READY: issuecomment-6537150512. The assignment is the round-4 [A10] comment on #814, covering R755-1 (issuecomment-6532204298) and R756-1 (issuecomment-6532064254). TAKEN: issuecomment-6533388440. Live remote dev when this round ran: `56df0894`.

## Summary

- **ZQCS, option (a).** `RegisteredRefresher` now starts LiteDRAM's ZQCS timer one cycle after reset. On an idle controller every DFI command, precharge-all, REFRESH and ZQCS, is LiteDRAM's own exactly one cycle later. That holds for the first ZQCS and for the next one after the timer re-phases.
  - The arm Z4 grades two ZQCS with a 6-cycle period (gcd 2 with tREFI, the shipping parity class).
  - The planted stage without the delay (Z5) fails it.
  - So does the alternative the ruling names, delaying the timer's done pulse, through my own mutant `ref_zqcs_done_delayed`: that alternative is right for the first ZQCS only.
- **The stall paths.** New arms stall each stage's outputs at random:
  - F6 (flash): the PHY's command READY waits behind LiteSPI's own `LiteSPICSControl` at the shipping cs_delay, and the core's data READY is random too.
  - D5, D6 (DRAM): LiteDRAM's aw and ar READY are random, under back-to-back traffic.
  - In both, every registered READY holds beats (flash tx 74 and rx 36 held cycles; aw 39 and ar 13), and the transfers are the issued ones in order.
  - In-test planted lossy stages fail them (F7 for tx and rx, D7).
  - R756-1's `mutate_timing_cuts.py`: **10 of 10 KILLED**, including the three lossy registered-READY stages that survived at `8b28ebaf`.
  - My drop-held mutants for R755-1's F-1 (READY registered, held beat lost): 3 of 3 KILLED.
- **S-1.** F2's planted-path filter now takes its starts from the AXI-Lite bridge's own registers.
- **Re-route.** route-1x1 at the three directives in parallel at `0d4a899f`, judged by #818's gate at PR #820's head `50e5d08d`: **rc 0, `RESULT: PASS`, ExtraTimingOpt selected at +0.406 ns.**
  - Every directive meets the +0.030 / 0 floor at every corner: +0.322, +0.126 and +0.406 ns. **No STOP.**
  - The head changes only the test and TESTING.md after `0d4a899f`, and the build reads neither (`receipts/route-0d4a899f/files-changed-after-routed-commit.txt`).
- **Found while working (test harness only, now fixed).**
  - LiteSPI's model PHY sized its memory from the whole flash part, 4 Mi words. That cost about 4.5 GB and 100 s of setup per flash simulation.
  - migen's tracer registry kept every SoC the test built alive. My first full run reached 22.6 GB RSS before I stopped it.
  - The round-3 test runs two such flash simulations and keeps both, so it would have held about 9 GB. That figure is inferred from the 4.5 GB measured per simulation, not measured.
  - The full test now peaks at 88 MB and takes 585 s CPU against the aggregate's 900 s member limit.

## 1. Changes (file:line, reason)

| Where | Change | Reason |
|---|---|---|
| `sw/litex/milan_soc.py:50` | import `ResetInserter` | for the timer's start |
| `sw/litex/milan_soc.py:2430-2469` (`RegisteredRefresher`) | `started` flip-flop; `ResetInserter()(refresher.zqcs_timer).reset.eq(~started)`, only when LiteDRAM built a ZQCS timer (`:2466`); docstring `:2436-2457` | ZQCS (R755 F-2, R756 F-1, ruling item 1, option a): the registered request delays the grant and every refresh sequence end by one cycle, but not the ZQCS timer. At 100 MHz, tREFI 782 and the 10^8 period (gcd 2) put the pulse on the other parity, so an idle controller never issued ZQCS (LiteDRAM's own first is at 76 s). Holding the timer in reset one extra cycle shifts its pulse by the same cycle. Later re-phases follow the delayed ZQCS end on their own. The docstring states what holds idle, and that under traffic the coincidence depends on the traffic in both designs |
| `sw/litex/test_soc_timing_cuts.py:913-971` | `UndelayedZQCSRefresher` (planted), `ZQCS_PERIOD = 6`, `short_zqcs()`, Z4 and Z5; `dfi_commands(..., expect=)` stops at the first difference (`:889`) | ruling item 1: a shortened period in the shipping parity class, staged == unstaged + 1 with two ZQCS, and the stage without the delay must fail |
| `:194-248` | `LossyReady`, `LossyBuffer`, `lossy_phy_stage()`, `LossyAXIStage` (planted) | ruling item 2: the lossy registered-READY stages, in the gate |
| `:251-276` | `FaceWatch`: per stream, the cycles the stage holds a beat with its output stalled, and every VALID or payload change before the beat is taken | proves each skid is exercised, and grades the handshake rule at each output |
| `:400-431` | `gated()`, `stalled_phy_stage()` (random READY at both outputs, the PHY face also behind `LiteSPICSControl` at its default cs_delay, which is the shipping one: `milan_soc.py:3201` passes none), `STALL_LIMIT` | ruling item 2, flash: "random READY with the shipping cs_delay stall" |
| `:434-505`, `:528-549` | `flash_reads(..., seed=)`; F6, F7 | the same words, chip-select edges and commands in order as the wired build; both registered READYs hold beats; lossy tx and rx fail |
| `:712-736`, `:739-845` | `stalled_axi_stage()`, `dram_stalled()`; D5, D6, D7 | ruling item 2, DRAM: back-to-back writes, then reads beside writes, random VALID gaps, random aw and ar READY into LiteDRAM. Graded on the native port's write commands, words and read commands in issue order, one B per write and one R per read |
| `:302-305` | the model PHY's memory holds the image only (`SimpleNamespace(total_size=..., read_opcode=...)`); `phy.flash` stays the real part | the full-size model cost 4.5 GB and about 100 s of setup per flash simulation. LiteSPI's mmap reads `phy.flash` and LiteX the region from `module`, so both still see the real part |
| `:309-317` (`build`) | `tracer.classname_to_objs.clear()` before each build | migen's tracer keeps every object it has named, so every SoC the test built stayed in memory |
| `:334-397` | `flash_crossings` returns the forward paths that start at a bridge register; F2 filters on them | S-1 (R755) |
| `:4-38` | module docstring: the stall arms | Docs |
| `docs/testing/TESTING.md:736-756` | the Z4 and Z5 arms, the stall arms, the planted lossy stages, and that the DRAM arms do not grade read data and why | Docs (R755 F-1 and F-2, R756 F-1 Docs) |

The PR body's old "upstream behaviour, unchanged here" line is gone (`PR-BODY.md`).

## 2. New checks, their planted mutants and failing words

All of these were run at `4ee2aa96`, in `test_soc_timing_cuts.py` or through the two mutation scripts. Each grades the unchanged test.

| Check | Planted mutant | Where planted | Result and failing words |
|---|---|---|---|
| Z4 | the stage without the ZQCS delay | in the test (Z5) | `[ok] Z5 the stage with its ZQCS timer starting at reset fails Z4: stopped at its first difference after 6 commands, ZQCS at []` |
| Z4 | the ZQCS timer's done pulse delayed instead of its start | `scripts/mutants_round4.py ref_zqcs_done_delayed` | `KILLED`: Z4 fails. The probe shows that variant issuing ZQCS at 2411 only, against LiteDRAM's 2410 and 3192 (`receipts/probes/probe-rephase-6.log`) |
| F6 | lossy tx buffer (PipeValid, then a READY registered from the last stall) | in the test (F7) | `[ok] F7 a planted lossy registered READY on the tx stream fails F6 (0 of 12 words, ..., broken holds tx 1 rx 0, 10 sys cycles)` |
| F6 | lossy rx buffer | in the test (F7) | `[ok] F7 ... on the rx stream fails F6 (0 of 12 words, ..., broken holds tx 0 rx 1, 58 sys cycles)` |
| D6 | lossy aw and ar | in the test (D7) | `[ok] D7 a planted lossy registered READY on aw and ar fails D6 (1 of 20 writes, 0 of 12 reads, ..., broken holds aw 1 ar 0, 409 sys cycles)` |
| D6, F6 | R756-1's `axi_lossy_ready`, `spi_tx_lossy_ready`, `spi_rx_lossy_ready` | `scripts/r756_mutate_timing_cuts.py`, byte-identical to R756-1's (sha256 `4b51f6e7…`) | **KILLED** x3. They SURVIVED at `8b28ebaf`. Failing words: the D6 or F6 line `[FAIL]` |
| (existing) | R756-1's other seven | same script | **KILLED** x7 (`axi_ar_unstaged`, `axi_pipevalid`, `spi_cs_comb`, `spi_tx_no_pipe_ready`, `ref_last_comb`, `ref_ready_registered`, `ref_no_last`) |
| D6, F6 | drop-held (PipeReady's flag and READY kept, the held copy never presented) on aw and ar, SPI tx, SPI rx | `scripts/mutants_round4.py axi_dropheld`, `spi_tx_dropheld`, `spi_rx_dropheld` | **KILLED** x3 (R755 F-1's verification) |

The shipping stages pass every arm:

- F6: `12 of 12 words, held cycles tx 74 rx 36, broken holds tx 0 rx 0, 1396 sys cycles`;
- D6: `20 of 20 writes, 12 of 12 reads, held cycles aw 39 ar 13, broken holds aw 0 ar 0`;
- D5, the harness on the wired build: the issued transfers, held cycles 0;
- Z4: `ZQCS at [2411, 3193], LiteDRAM's at [2410, 3192]`.

The test has 23 checks, all `[ok]`, `RESULT: PASS`, rc 0: 585 s CPU, 588 s wall, peak 88 MB (`receipts/test-4ee2aa96/`).

## 3. Resources and route timing

route-1x1, recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`), `--single-thread-synthesis`, default seed, in a clean clone at `0d4a899f`:

- The shipping run (ExtraPostPlacementOpt) started at 21:20 UTC.
- AltSpreadLogic_high and ExtraTimingOpt started at 22:03, from its synthesis checkpoint, in parallel.
- All three went through the slot wrapper (slots 0, 1 and 2), each in its own user scope (MemoryMax 14G).
- Vivado rc 0 for each: 3633 s, 1237 s and 1179 s.
- The exported Verilog differs from round 2's `8b28ebaf` export only in:
  - `sdram_started` and its reset of `refresher_zqcs_timer_count1` to 99,999,999 (Z - 1);
  - the module-tree comment's order;
  - the clone paths (`receipts/route-0d4a899f/verilog-difference-8b28ebaf-to-0d4a899f.txt`).

| Directive | WNS / WHS ns, worst corner (round 2, `8b28ebaf`) | Slow WNS / WHS | Fast WNS / WHS | Worst path family | F1 | F2 | F3 | F4 | LUT / FF / slices (round 2) |
|---|---|---|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | +0.322 / +0.031 (+0.128) | +0.322 / +0.058 | +1.522 / +0.031 | F4, CPU DMA write bridge | +2.721 | +1.607 | not in the 5,000 worst | +0.322 | 51,864 / 54,024 / 15,840 (51,827 / 54,022 / 15,764) |
| AltSpreadLogic_high | +0.126 / +0.035 (+0.039) | | | F4 | +2.085 | +1.392 | not in the 5,000 worst | +0.126 | 51,895 / 54,027 / 15,812 (51,895 / 54,024 / 15,839) |
| ExtraTimingOpt (**selected**) | **+0.406** / +0.036 (+0.010) | +0.406 / +0.099 | +1.583 / +0.036 | the milan reset `FDPE_17` into LiteEth MAC status registers (0 levels, 96 % routing) | +1.723 | +1.472 | not in the 5,000 worst | +0.453 | 51,893 / 54,027 / 15,811 (51,882 / 54,029 / 15,839) |

- RAMB36 74, RAMB18 27 and DSP 13 at every directive, unchanged. The route is complete everywhere, with no unrouted net.
- F1 to F3 are more than 1 ns from the worst path at every directive (`receipts/route-0d4a899f/route-1x1-*-top20.md`).
- The stage cells at ExtraPostPlacementOpt (`*-stage_cells.tsv`, cells whose names match each stage's signals):
  - F1: 174 FF and 30 LUT (round 2: 174 and 61);
  - F2: 88 FF and 6 LUT (88 and 6);
  - F3: 3 FF and 5 LUT (3 and 6).
  - The new `started` flip-flop is named `sdram_started`, outside F3's name pattern. In the utilization, FF moves +2, +3 and -2 against round 2 at the three directives.

**#818 gate** (PR #820's head `50e5d08dda6e89cf010a740cea5cf4539807db01`, in a scratch clone and not committed; its `pp_resource_baseline.json` is the lane's own record):

```sh
python3 syn/ooc/pp_resource_gate.py check <w-h1>/ax7101/gateware --endpoint route-1x1 \
  --comparison <w-h1>/ax7101-AltSpreadLogic_high --comparison <w-h1>/ax7101-ExtraTimingOpt
```

- rc 0, `RESULT: PASS`. ExtraTimingOpt is selected at +0.406 ns.
- LUT 51,893 (-119 against the record), FF 54,027 (+320), SLICE 15,811 (+31): all ok.
- WNS 0.44 -> 0.406 (-0.034, ok) and WHS 0.036 -> 0.036. No WARNING.
- Every corner is at or above +0.030 / 0.

| Control | rc | Result |
|---|---|---|
| shipping alone, `--shipping-selection` | 0 | +0.322, fall -0.118, ok |
| no `--comparison` and no `--shipping-selection` | 2 | `NOT COMPARABLE` |
| the ExtraTimingOpt directory as the shipping route | 2 | `NOT COMPARABLE: ... holds 0 recipe scripts, not one` |

#818's self-tests at `50e5d08d`, each rc 0:

- `--selftest`;
- `pp_resource_gate_selftest.py`: 312 arms and 500 fuzz cases, PASS;
- `pp_resource_gate_set_selftest.py`;
- `pp_resource_gate_mutants.py`: control passes, all 236 mutants fail.

The record is not re-recorded (the record rule, issuecomment-6525285974).

## 4. Gate table

Every row runs at the head `4ee2aa96` unless it names another commit. Each was run in the foreground or detached, never piped, and its rc was recorded.

| Gate | Command | rc | Result | Receipt |
|---|---|---|---|---|
| The #814 check | `cd sw/litex && PYTHONHASHSEED=0 python3 test_soc_timing_cuts.py` | 0 | 23 checks `[ok]`, `RESULT: PASS`; 585 s CPU, 88 MB peak | `receipts/test-4ee2aa96/` |
| R756-1's mutants | `python3 scripts/r756_mutate_timing_cuts.py <repo>/sw/litex <m>`, x10 | 0 x10 | 10 of 10 `KILLED` | `receipts/r756-mutants-4ee2aa96/` |
| This round's mutants | `python3 scripts/mutants_round4.py <repo>/sw/litex <m>`, x4 | 0 x4 | 4 of 4 `KILLED` | `receipts/round4-mutants-4ee2aa96/` |
| LiteX self-test | `scripts/run_litex_sims.sh --selftest` (clean clone) | 0 | 10 checks, 10 PASS | `receipts/litex-4ee2aa96/` |
| LiteX aggregate | `scripts/run_litex_sims.sh <out>` (clean clone, pinned Verilator on PATH) | 0 | `simulations: 8 passed: 8 failed: 0 skipped: 0 timed out: 0` (1183 s) | `receipts/litex-4ee2aa96/` |
| Python idiom ratchet | `python3 scripts/check_py_idiom.py` | 0 | `long module: 10 <= 10`, `undocumented public function: 0 <= 0`. Also the docs workflow's `gate_39` (with `--selftest`), rc 0 | `receipts/docs-4ee2aa96/all.out` line 30 |
| Docs workflow gates | `scripts/docs_run.sh 4ee2aa96...` (the run bodies on CPython 3.12.3 and Make 4.3) | 0 | `44 steps, 0 failed`: 42 rc 0, `gate_42` not run by AGENTS.md section 5, and the no-git step run separately | `receipts/docs-4ee2aa96/` |
| Builder leg 1 on the LiteX interpreter | in `docs_run.sh` | 0 | `1 steps, 0 failed` | `receipts/docs-4ee2aa96/leg1-litex*` |
| Markdown gates on CPython 3.12.3 | in `docs_run.sh` | 0 | `5 steps, 0 failed` | `receipts/docs-4ee2aa96/md312*` |
| No-git step | `docs_check.py`, `check_feature_status.py` on a `git archive` export | 0, 0 | pass | `receipts/docs-4ee2aa96/nogit_*` |
| Builder bank | `python3 sw/builder/test_builder.py` (clean clone) | 0 | `ALL GATES PASS EXCEPT 2 NOT RUN` (1831 s). The two not run are the same as dev's bank on this host: gate 1b's `MAKEFLAGS += -e` mutation is inert under Make 4.3, and gate 11 needs the absent mf48 build | `receipts/builder-4ee2aa96/` |
| Full sweep, 4 shard units | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4` | 0 x4 | **64 of 64 PASS** (14 + 17 + 17 + 16), none failed or timed out; each preflight's cancellation self-test PASS | `receipts/sweep-4ee2aa96/` |
| rtl-fast replay | `scripts/rtlfast_run.sh 4ee2aa96...` (the workflow's step bodies, base the live dev `56df0894`) | 0 | `rtl-fast: success; failed jobs: none`: all 12 needed jobs, 56 steps rc 0 (6161 s) | `receipts/rtlfast-4ee2aa96/` |
| route-1x1 x3 directives | `vivado -mode batch -source baseline_integrated.tcl` / `baseline_implementation.tcl` through `vivado-slot.sh`, at `0d4a899f` | 0 x3 | section 3 | `receipts/route-0d4a899f/` |
| #818 gate on the set | `pp_resource_gate.py check ... --comparison ... --comparison ...` at PR #820's `50e5d08d` | 0 | `RESULT: PASS`, ExtraTimingOpt +0.406 ns | `receipts/gate818/` |
| #818 controls and self-tests | section 3 | 0 / 2 / 2; 0 x4 | as expected | `receipts/gate818/` |

Not run:

- `check_nvm_capture.py`, the capture recipe and the service-budget runs: this round changes no firmware, processor or CPU path. They were last run at `8b28ebaf` in round 2.
- ooc-1x1 and ooc-8x8: the processor is unchanged, so they equal the record (round 2).
- The record is not re-recorded, by the record rule.
- No hardware, bench or flashing.

## 5. How the runs were made

- **Vivado.**
  - `scripts/r2_export.sh h1 0d4a899f9c ax7101` (clone, export, `pp_baseline.py`), then `scripts/launch.sh` per run. It runs `setsid nohup vivado-slot.sh systemd-run --user --scope -p MemoryMax=14G ...` with no timeout. `scripts/dir_prep.py` writes the two comparison scripts from the shipping checkpoint.
  - `scripts/paths.tcl` reopened each routed checkpoint, also through the wrapper. `scripts/collect_route.py` gathered the receipts.
  - No lock was taken directly.
- **Simulations.** Run on the bench LiteX interpreter, `PYTHONHASHSEED=0`.
  - The full test and the probes ran in capped user scopes (MemoryMax 10-12G).
  - The first full run, before the two harness fixes, reached 22.6 GB RSS and the lane unit peaked at 23.6 GB of its 24 GB. I stopped it, found the cause with `gc` referrers (migen's `tracer.classname_to_objs`) and `/usr/bin/time` (the model PHY's 4 Mi-word memory), and fixed both in the test.
- **The sweep.** It runs as 4 units through `native-shards.py`, MemoryMax 10G and -j4 each.
  - The CPU booking had only three free 16-CPU ranges: 16-31, 96-111 and 112-127. Others held 0-15 and 32-95.
  - So the four shards took 16-27, 96-107, 108-119 and 28-31,120-127: 12 CPUs each, no core shared and every core free. The fourth range is split in two.
- **Receipts.** Host paths are redacted to `<scratch>`, `<home>` and `<tools>`. Files over 200 KB are recorded by SHA-256 and size in each directory's `large.sha256`.

## 6. Open risks

- **Test runtime.** The test now takes about 585 s CPU against `run_litex_sims.sh`'s 900 s member limit. Before this round it was about 405 s. Most of the time goes to the refresh DFI simulations: Z3 at the shipping period plus Z4 and Z5.
- **The DRAM harness does not land write data.** The DFI write burst leaves masked one cycle before the native port takes the word, so every read returns 0 with and without the stage. This predates this round. The DRAM arms grade transfers and responses, not data.
- **The flash stage has still not been on hardware.** The real PHY cannot be elaborated in migen simulation. The harness uses LiteSPI's own `LiteSPICSControl` for the chip-select hold.
- **The selected directive is now ExtraTimingOpt.** The worst path at that directive is a reset net, outside F1 to F4. Route-to-route spread on unchanged logic was 0.3 to 0.57 ns on this lane.

## 7. Progress log (UTC, from file and commit times)

- 30 Oct 20:58 TAKEN posted. Live remote dev `56df0894`.
- 21:17 `0d4a899f` committed (the ZQCS fix, Z4 at period 842) and exported. 21:20 the shipping route started.
- 21:2x-21:5x the stall arms were written and run arm by arm. The DRAM model's masked write data was found here.
- 22:01 the done-pulse alternative was probed at period 28. 22:03 the two comparison directives started.
- 22:20-22:24 all three routes rc 0. 22:21 the first full run was stopped at 22.6 GB, and the two harness causes were found and fixed.
- 22:39 the #818 gate passed, then its controls and self-tests. 22:57 the period-6 probe.
- 23:17-23:28 R756's ten mutants KILLED, then my four. 23:20 the full test passed (585 s CPU) and `4ee2aa96` was committed.
- 23:32 the sweep started. 23:40 the LiteX aggregate rc 0.
- 31 Oct 00:08 docs gates rc 0. 00:11 builder bank rc 0. 00:27-00:32 sweep shards rc 0. 01:23 rtl-fast `success`. Then REVIEW READY.

## 8. Index

`INDEX.md` lists every file in this directory with its size and SHA-256, generated by `scripts/gen_index.py`.
