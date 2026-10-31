[R755] POSITIVE - exact head 4ee2aa9654196a00876dedade4b2e987c9c06e64

# R755-2 internal cleared-context review: kebag-logic/milan-fpga PR #826 (issue #814), round 4 delta

- Head under review: `4ee2aa9654196a00876dedade4b2e987c9c06e64`, tree `ec3c136a86bad6c8e27cc4fefae4d8c23e81582d`. PR head and base read with `gh pr view --json` and `gh api .../pulls/826`: head `4ee2aa96…`, base `dev` `1e80128f…`, 7 commits.
- Previously reviewed head: `8b28ebaf` (R755-1, issuecomment-6532204298). The delta is two commits:
  - `0d4a899f`: `sw/litex/milan_soc.py` (`RegisteredRefresher`, +21 −3), the test and `docs/testing/TESTING.md`;
  - `4ee2aa96`: the test and TESTING.md only.
  - `git diff --stat 0d4a899f..4ee2aa96`: `docs/testing/TESTING.md` and `sw/litex/test_soc_timing_cuts.py` only. Neither is a build input.
- Reviewer environment: the pinned LiteX set from `sw/litex/litex_pins.txt` at exactly those revisions (migen `4c2ae8df`, litex `a1e1c365` plus the tree's VexiiRiscv patches, litedram `f9b75e03`, litespi `02d5a209`), Python 3.14.8.

## Verdict

**POSITIVE.** Both round-3 MINORs are fixed at their cause, and S-1 is addressed. All five lenses were applied to the delta and none has an open BLOCKER, MAJOR or MINOR.

- **ZQCS (R755-1 F-2, R756-1 F-1).** The ZQCS timer is now held in reset for one cycle after sys reset. On an idle controller, every DFI command (precharge-all, REFRESH and ZQCS) is LiteDRAM's own exactly one cycle later. This held across nine ZQCS periods, through up to eight ZQCS and seven timer re-phases. Z4 fails on the undelayed stage, on a done-pulse delay, on a two-cycle hold and on a hold on the wrong timer.
- **Stall paths (R755-1 F-1, R756-1 F-2).** The F6 and D6 arms put beats into every registered READY: tx 74 / rx 36 held cycles, aw 131 / ar 141. They also kill every planted stall-path defect: 28 mutants across three runners, including the drop-held, duplicate-held and VALID-waits-on-READY stages that survived or were never planted at `8b28ebaf`.
- **S-1.** F2 now takes its starts from the AXI-Lite bridge's own registers.

The open items are three SUGGESTIONs and one RESIDUE, listed below.

## Reconstruction (public state only)

- AGENTS.md (lenses, severities, ledger rule), CONTRIBUTING.md by reference, and docs/README.md.
- Issue #814 rulings, read by ID:
  - the assignment and its STOP (issuecomment-6514717735);
  - #814 back in the release, judged by the #818 gate (issuecomment-6527475726);
  - the record rule (issuecomment-6525285974);
  - **the round-4 ruling (issuecomment-6532211135)**: ZQCS option (a); stall arms with the shipping cs_delay; the lossy-ready plants must die; S-1 if cheap; re-route on three directives under #818 at `50e5d08d`; no re-record.
- The author's round-4 REVIEW READY (issuecomment-6537150512).
- The PR body: read through `gh pr view --json body`.
- `git diff 8b28ebaf..4ee2aa96` in full, and `git diff 1e80128f..4ee2aa96 --stat`.
- My own round-1 report.
- Published evidence: tree `fdae2980`, `review-evidence/814-r1/author-r4`. I fetched and read:
  - `receipts/test-4ee2aa96/checks.txt`
  - `receipts/gate818/*`
  - `receipts/route-0d4a899f/*`: signoff grades, route status, per-corner timing tables, the Verilog difference, the files changed after the routed commit
  - `receipts/litex-4ee2aa96/*`
  - `receipts/rtlfast-4ee2aa96/{table.txt,run.out,base.txt}`
  - `receipts/builder-4ee2aa96/builder_bank.rc`
  - `receipts/docs-4ee2aa96/{all,md312,leg1-litex}.rc`, `all.out` and `nogit_summary.txt`
  - `receipts/sweep-4ee2aa96/shard-{0..3}`
  - `receipts/{r756-mutants,round4-mutants}-4ee2aa96/*.rc`
  - `scripts/{r756_mutate_timing_cuts.py,mutants_round4.py}`
- Hosted, exact head: the check-runs list for `4ee2aa96`, and the log of job `elaborate-gates-1` (124401342992). I read it for the LiteX aggregate step only.

## What was checked, and how

### `RegisteredRefresher`: the ZQCS hold (`sw/litex/milan_soc.py:2430-2469`)

**How LiteDRAM issues ZQCS** (`litedram/core/refresher.py:103-128, 225-300` at the pin):
- `RefreshTimer` counts from `trefi-1` at reset and pulses `done` for one cycle every period.
- The ZQCS timer's `wait` is `~zqcs_executer.done`, so it re-phases when a ZQCS ends.
- DO-REFRESH starts a ZQCS only when `wants_zqcs` is high on the cycle `sequencer.done` is.
- The tREFI timer runs free (`wait = ~done`).

**Why one cycle of hold is the right fix**
- The registered `cmd.valid` delays the grant, and so every refresh sequence and its end, by exactly one cycle on an idle controller.
- Holding the ZQCS timer in reset for one cycle moves its first pulse from Z−1 to Z, so the pulse meets the delayed sequence end in the same refresh as LiteDRAM's own.
- After that, the timer re-phases on the delayed `zqcs_executer.done`, so every later pulse also lands one cycle later.
- The tREFI timer is not held, and need not be: the refresh request it raises reaches the controller one cycle later through the stage.

**The netlist matches.** The routed Verilog difference `8b28ebaf → 0d4a899f` (`receipts/route-0d4a899f/verilog-difference-8b28ebaf-to-0d4a899f.txt`) adds exactly one register, `sdram_started` (reset to 0 in the sys reset block, then set to 1). It adds one override, `if (sdram_reset) refresher_zqcs_timer_count1 <= 27'd99999999` (Z−1 for Z = 10^8). Nothing else in the SoC changes.
- The ZQCS timer's only register is its count, so no other state is held.
- Migen's `ResetInserter` appends the reset assignment after the module's own statements, so it overrides them.

**Guard and domain**
- `hasattr(refresher, "zqcs_timer")` matches LiteDRAM, which builds the timer only when `tZQCS is not None` (`refresher.py:251-259`).
- `started` is a sys flip-flop reset with sys, so every sys reset re-holds the timer for one cycle, as LiteDRAM's own timer restarts on that reset.

**Reviewer sweep** (`scripts/probe_r2.py zqcs <period> 8000`): the shipping stage against LiteDRAM's `Refresher`, idle, on the gate's DramSoC (MT41J256M16, 100 MHz). The criterion is that every DFI command list equals LiteDRAM's shifted by one cycle. All nine periods pass (`receipts/campaign/zqcs_*.log`):

| ZQCS period | gcd with 782 | Staged ZQCS cycles | LiteDRAM ZQCS cycles |
|---|---|---|---|
| 6 | 2 | 2411, 3193, 3975, 4757, 5539, 6321, 7103, 7885 | 2410, 3192, 3974, … , 7884 |
| 10 | 2 | 3975, 7885 | 3974, 7884 |
| 14 | 2 | 1629, 4757, 7885 | 1628, 4756, 7884 |
| 26 | 2 | 7103 | 7102 |
| 12 | 2 | 4757, 7885 | 4756, 7884 |
| 7 | 1 | 1629, 4757, 7885 | 1628, 4756, 7884 |
| 9 | 1 | 4757 | 4756 |
| 391 | 391 | none | none |
| 1564 | 782 | none | none |

- In every run the REFRESH spacing is 782 cycles. The period-6 run has seven re-phases after its first ZQCS.
- Round 1's direct probe found no staged ZQCS at period 10. At this head the same period gives 3975 and 7885, LiteDRAM's own plus one cycle.

**Declared intervals.** LiteDRAM's settings for the gate's part are tREFI 782, tRP 3, tRFC 52 and tZQCS 16 sys cycles (64 nCK at 1:4). Because each staged DFI list equals LiteDRAM's shifted by one, the staged refresher has exactly LiteDRAM's tREFI, tRP, tRFC, tZQCS and ZQCS-period behaviour at idle.
- The 1 Hz ZQCS rate and the 782-cycle tREFI round-up are LiteDRAM's own and unchanged by this PR.
- Under traffic, whether ZQCS coincides depends on the traffic for both refreshers. The docstring and the PR's Known limitations say so.

### Stall arms F6, F7, D5 to D7 (`sw/litex/test_soc_timing_cuts.py:251-277, 400-551, 693-845`)

**`FaceWatch`** counts held cycles only while a beat is inside the stage and its output shows VALID without READY. It counts a broken hold when an offered beat's VALID drops or its payload changes before it is taken. That is the valid-until-ready and payload-stable rule at the stage's output face.

**`stalled_phy_stage`**
- Gates the PHY command handshake with `LiteSPICSControl(...).enable` at its default `cs_delay`. That is the hold the SDR PHY's WAIT-CMD-DATA applies, so a new chip select stalls the tx skid as the real PHY does.
- Also gates the core-side data READY at random.

**`stalled_axi_stage`** gates aw and ar into LiteDRAM at random. `dram_stalled` sends:
- 12 back-to-back single-beat writes;
- then 8 more writes beside 12 reads of the first 12.

It grades the native port's write commands, write words and read commands per direction and in order, and one B or R per request.

**At this head (reviewer run, `receipts/campaign/head_test.log`):**
- F6: 12 of 12 words, held cycles tx 74 / rx 36, 0 broken.
- D6: 20 of 20 writes and 12 of 12 reads, held aw 131 / ar 141, 0 broken.
- D5 (wired): the same transfers, with 0 holds as expected.

**VALID does not wait on READY.** This is a structural probe (`scripts/probe_r2.py validdep`, `receipts/campaign/validdep_*`). In the shipping flash and DRAM builds, no output face's VALID or payload reads that face's READY through logic. That covers the SPI tx PHY face, the SPI rx core face, and the aw and ar LiteDRAM faces.
- The probe is sensitive: it fails on both planted VALID-waits stages.
- The harness drivers (`send`, `master`) raise VALID before looking at READY.

### Kill power: every mutant KILLED (`receipts/campaign/SUMMARY.tsv`)

**The R756-1 runner** (`r756_mutate_timing_cuts.py`, the author's published copy, blob `d7c4fd18`). All 10 KILLED: axi_ar_unstaged, axi_lossy_ready, axi_pipevalid, spi_cs_comb, spi_tx_no_pipe_ready, spi_tx_lossy_ready, spi_rx_lossy_ready, ref_last_comb, ref_ready_registered and ref_no_last.
- The three lossy-ready mutants that survived at `8b28ebaf` are now killed by F6 or D6.

**The author's round-4 runner** (`mutants_round4.py`, blob `dc83655f`). All 4 KILLED:
- axi_dropheld, by D6;
- spi_tx_dropheld and spi_rx_dropheld, by F6;
- ref_zqcs_done_delayed, by Z4 (ZQCS at [2411], against LiteDRAM's [2410, 3192]).

**The reviewer's own runner** (`scripts/probe_r2.py mutant`, each mutant run through its behaviour arm only, so the kill is behavioural). All 14 KILLED:

| Mutant | Killed by | How it shows |
|---|---|---|
| axi-dropheld, -aw, -ar | D6 | aw-only: 1 of 20 writes, broken aw 1 |
| axi-duphold | D6 | 19 reads for 12 issued |
| axi-validwait | D6 | 0 holds |
| spi-tx-dropheld, spi-rx-dropheld | F6 | |
| spi-tx-duphold, spi-rx-duphold | F6 | stopped at the cycle limit with 3 and 6 of 12 words |
| spi-tx-validwait | F6 | 0 tx holds |
| ref-undelayed | Z4 | |
| ref-donedelay | Z4 | the reviewer's own done-pulse-delay construction, independent of the author's |
| ref-hold2 | Z4 | |
| ref-holdrefresh | Z3, Z4 | |

### S-1 (`sw/litex/test_soc_timing_cuts.py:334-398`)

- `flash_crossings` now returns the forward paths whose start is in `registers(bridges[0])`.
- F2 requires one of them to end in a `_cnt` PHY counter.
- At this head: `fsm_state -> litespiclkgen_cnt` and `fsm_state -> litespisdrphycore_sr_out_cnt`, both starting at the bridge's own FSM.

### Harness changes

- **The model PHY now holds only the image.** `total_size = 4 * len(image)`, while `phy.flash` stays the real module, so LiteSPI's mmap and LiteX's region still see the real part.
- **Each build clears migen's tracer registry.** That only resets name-index suffixes, as a fresh process would.
- Neither weakens a check:
  - F3 still returns the image;
  - F4 still gives +2 / +8 cycles;
  - F5 still gives 30 commands and the same chip-select edges as the wired build.

### Route set and the gates (author evidence, spot-checked)

**#818 gate at `50e5d08d`** (`receipts/gate818/check-set.log`, rc 0, `RESULT: PASS`):
- It selects ExtraTimingOpt at +0.406 / +0.036 ns.
- Resources: LUT −119, FF +320, slices +31; RAMB36, RAMB18 and DSP unchanged.
- The fall is 0.034 ns.
- The gate controls behave as expected: shipping alone rc 0; no set rc 2; a comparison alone rc 2.

**Floors at every corner.** I recomputed every corner from the per-directive timing tables (`receipts/route_corners_0d4a899f.txt`). Every directive meets WNS ≥ +0.030 and WHS ≥ 0 at all four corners:

| Directive | Slow 0C / 85C | Fast 0C / 85C | Route status |
|---|---|---|---|
| ExtraPostPlacementOpt | +0.322 / +0.058 | +1.522 / +0.031 | 0 routing errors |
| AltSpreadLogic_high | +0.126 / +0.087 | +1.583 / +0.035 | 0 routing errors |
| ExtraTimingOpt | +0.406 / +0.099 | +1.583 / +0.036 | 0 routing errors |

**Routed commit.** The routed commit is `0d4a899f`. Its routed Verilog carries the ZQCS hold (see above), and `0d4a899f..4ee2aa96` touches no build input (checked with git here).

**Author receipts at the head, read**
- Test: 23 `[ok]`, `RESULT: PASS`, 585 s user. The test file's sha256 `62022e07…` equals the head blob.
- LiteX: self-test 10 of 10; aggregate 8 of 8.
- rtl-fast against dev `56df0894`: `success; failed jobs: none`.
- Builder bank: rc 0.
- Docs: all, md312 and leg1 rc 0; 44 steps, 0 failed; gate_42 not run.
- Sweep: four shards, 14 + 17 + 17 + 16 = 64 of 64 PASS. Each `complete.json` carries the head and exit 0, and each cancellation self-test passed.

**Hosted at the exact head.** `elaborate-gates-1` (job 124401342992) executed. Its "Standalone LiteX simulation aggregate" step succeeded with 8 of 8, and `test_soc_timing_cuts` took about 369 s wall there (`receipts/hosted_litex_aggregate.txt`). The manager owns hosted acceptance.

### Comment rule and docs

- **Comment rule.** I scanned every added line of `git diff 8b28ebaf..4ee2aa96` for lane labels, review rounds, reviewer IDs and comment IDs. There are none.
- **Docs.** I checked the `RegisteredRefresher` docstring, the `ZQCS_PERIOD` comment (`:926-930`; 2410 / 3192 matches the run), the `dram_stalled` docstring, `docs/testing/TESTING.md:736-756` and the PR body (including the line references `:2397`, `:2430`, `:2466-2469`, `:2483`, `:3688`) against the code and the runs above. They are accurate.
- **Round-3 claims.** The docstring no longer says ZQCS keeps its spacing unconditionally. It says what holds at idle and under traffic. The PR's "Known limitations" no longer calls the ZQCS behaviour "upstream, unchanged".

## Findings

No BLOCKER, MAJOR or MINOR.

### S-2 SUGGESTION — Tests — `sw/litex/test_soc_timing_cuts.py:736`, `docs/testing/TESTING.md:751-752`: D7 plants aw and ar together

- **Evidence.** D7 plants `LossyAXIStage` on aw and ar at once, and its kill comes from aw (`broken holds aw 1 ar 0`). TESTING.md says "A planted lossy registered READY on each of those streams must fail".
- **Why it is only a suggestion.** D6 is sensitive to ar alone: the reviewer's `axi-dropheld-ar` is KILLED by D6. So nothing is untested today. The gate just does not encode the per-channel case.
- **Optional change.** Plant aw-only and ar-only in D7, or reword the sentence as "on the flash tx and rx streams, and on aw and ar together".

### S-3 SUGGESTION — Tests and Conformance — `sw/litex/test_soc_timing_cuts.py:251-277`: no check that a stage's VALID never waits on its READY

- **Evidence.** `FaceWatch` grades valid-until-ready and payload stability, but not that the output VALID is independent of READY (AXI's "a source must not wait for READY").
- **Today.** A fully VALID-waiting stage is caught only because it then holds no beats (`axi-validwait`, `spi-tx-validwait`: 0 holds). A stage that waited only while holding could slip through.
- **Shipping is clean.** The shipping stages are clean structurally (`validdep` PASS).
- **Optional change.** Reuse `Netlist.cone` on each output face, as `scripts/probe_r2.py validdep` does: about 15 lines and no simulation.

### S-4 SUGGESTION — Tests and Robustness — `sw/litex/test_soc_timing_cuts.py:944-972`, `scripts/run_litex_sims.sh:110`: runtime margin against the 900 s member limit depends on host load

- **Evidence.**
  - Hosted: about 369 s wall.
  - Author host: 585 s user.
  - Reviewer host, beside 15 other single-thread simulations on 16 CPUs: 953 s user, 973 s wall (`receipts/campaign/head_test.log`). Inside the aggregate, that would be a timeout (rc 124), not a PASS.
- **Recorded honestly.** The author records the risk, so the figures are honest. It is not a defect at the hosted context.
- **Optional change.** Most of the time is the refresh DFI simulations:
  - Z3's two 3,200-cycle runs repeat what Z4's two 3,300-cycle runs already cover, except for "no ZQCS at the shipping period".
  - Z5 could stop at the first ZQCS cycle.

### R-1 RESIDUE — Docs — `docs/testing/TESTING.md:746`: one line is not re-wrapped

- The line "at reset, which issues no ZQCS there, must fail that arm. Then each stage's output is stalled" runs to 94 columns inside a paragraph wrapped at about 78.
- **Exact fix:** re-wrap the paragraph at lines 741-756 to the file's width. This is wording only.

## Clean results

- [R755] PASS Conformance — `sw/litex/milan_soc.py:2430-2469`; routed Verilog difference `8b28ebaf→0d4a899f`; `receipts/campaign/zqcs_{6,7,9,10,12,14,26,391,1564}.log`; `receipts/route_corners_0d4a899f.txt`; `receipts/campaign/validdep_*.log` — checked against:
  - ruling issuecomment-6532211135 option (a): LiteDRAM's own ZQCS decision, one cycle later at idle, through up to eight ZQCS and seven re-phases;
  - LiteDRAM's declared tREFI 782, tRP 3, tRFC 52 and tZQCS 16, which the shifted equality preserves;
  - #818 at `50e5d08d`: the floors at every corner on all three directives, best ExtraTimingOpt at +0.406 ns;
  - the AXI and stream VALID/READY rules at each stage output face.
- [R755] PASS RTL — `sw/litex/milan_soc.py:2463-2469`, with LiteDRAM `refresher.py:103-128,225-300` and the routed Verilog difference — checked:
  - the `ResetInserter` override on the ZQCS timer's only register;
  - the `started` flip-flop reset with sys;
  - the `hasattr` guard matching `tZQCS is not None`;
  - the sys-domain sync;
  - no other netlist change; `0d4a899f..4ee2aa96` touches no build input.
- [R755] PASS Robustness — `sw/litex/test_soc_timing_cuts.py:400-551,693-845` at this head (`receipts/campaign/head_test.log`) and `receipts/campaign/zqcs_*.log` — checked:
  - random backpressure on all four registered READYs, with beats held: tx 74, rx 36, aw 131, ar 141;
  - the shipping cs_delay hold;
  - reset re-holding the ZQCS timer;
  - ZQCS periods in gcd classes 1, 2, 391 and 782 with tREFI.
- [R755] PASS Tests — `sw/litex/test_soc_timing_cuts.py` (993 lines at the head), `receipts/campaign/SUMMARY.tsv` — checked:
  - 23 of 23 checks at the head;
  - 28 of 28 mutants KILLED across the R756-1 runner (10), the author's round-4 runner (4) and the reviewer's runner (14), each stall-path and ZQCS kill coming from a behaviour arm (F6, D6, Z3, Z4);
  - S-1 satisfied at `:334-398`.
- [R755] PASS Docs — `sw/litex/milan_soc.py:2431-2455`, `sw/litex/test_soc_timing_cuts.py:758-768,926-930`, `docs/testing/TESTING.md:736-756`, the PR body at the head, and the comment-rule scan of `git diff 8b28ebaf..4ee2aa96` — checked against the code and the runs above. They are accurate; R-1 is formatting only.

## Executed at this head (reviewer)

All runs used `scripts/campaign.sh` (16 parallel), one log and one rc file per job under `receipts/campaign/`. The job list is `receipts/campaign/JOBS.tsv`, and the summary is `SUMMARY.tsv`.
- `cd sw/litex && PYTHONHASHSEED=0 python3 test_soc_timing_cuts.py`: rc 0, 23 `[ok]`, 0 `[FAIL]`, `RESULT: PASS`.
- The R756-1 runner, 10 mutants; the author's round-4 runner, 4 mutants. Both are the published copies, with blob shas recorded in `receipts/author_scripts_run.txt`.
- `scripts/probe_r2.py`: 14 mutants, 2 validdep sensitivity runs and 9 ZQCS-period runs. A shipping-only `validdep` run (PASS) was made in the foreground before the campaign; its result is quoted above.
- Host paths in the receipts are replaced by `<clone>`, `<packet>`, `<litex-env>`, `<author-r4-evidence>`, `<home>` and `<tmp>`.
- No probe edited the clone. Mutants were installed in-process only.
- Afterwards I removed the ignored `__pycache__` directories the imports created, then checked the clone (`receipts/clone_restore_check.txt`):
  - HEAD `4ee2aa96…`;
  - tree and index tree `ec3c136a…`;
  - `git status --porcelain --ignored` empty and `diff-index` empty;
  - the delta files' blob bytes and modes equal to the index;
  - all six gitlinks as at the head.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 6532211135; `milan_soc.py:2430-2469`; LiteDRAM refresher at the pin; `zqcs_*` sweep; routed Verilog difference; #818 `check-set.log` and per-corner tables; `validdep` | R755-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| RTL | CLEAN | `milan_soc.py:2397-2469` (the delta at `:2463-2469`; `AXIReadyStage` and `SPIPHYStage` unchanged since `8b28ebaf` and covered there); routed Verilog difference; `0d4a899f..4ee2aa96` stat | R755-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| Robustness | CLEAN | F6, D5 and D6 at the head; `zqcs_*` across four gcd classes; reset behaviour of `started` | R755-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| Tests | CLEAN (S-2, S-3, S-4 optional) | `test_soc_timing_cuts.py` at the head; 28 mutants; head run; author and hosted gate receipts | R755-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |
| Docs | CLEAN (R-1 residue) | `milan_soc.py` docstring; test docstrings; `TESTING.md:736-756`; PR body; comment-rule scan | R755-2 | 4ee2aa9654196a00876dedade4b2e987c9c06e64 |

## Real limits

- **No hardware.**
  - The real LiteSPI PHY cannot be elaborated in migen simulation, so the flash stall arm stands in for the PHY's chip-select hold with LiteSPI's own `LiteSPICSControl`.
  - The flash stage has not been on a board.
  - Physical calibration was NOT RUN, and field skips are not hardware proof.
- **ZQCS is graded at idle only.** Under traffic, both refreshers issue ZQCS only by coincidence. That is LiteDRAM's design, and the PR says so.
- **DRAM read data are not graded** by the DRAM arms. This predates this round and is recorded in the PR and in TESTING.md. The reviewer did not re-derive the stated cause (a masked DFI write burst on the model PHY).
- **Not re-run by the reviewer.** These are author receipts: the full sweep, rtl-fast, the docs gates, the builder bank, the Vivado routes and the #818 gate with its self-tests. They were read and spot-checked as above.
- **No manager source bank** exists at this head, and none is claimed.

## Pending manager duties

- Build and validate the current-dev merge candidate: source base `1e80128f`, live dev `71d6ed07a59ec35b703b658edc9157d6b454d131`. That means the builder and native banks, linked on the PR.
- Hosted and act acceptance at the exact head. Several Verilator and Yosys shards were still in progress when read.
- Carry R-1 to the residue checklist.
- Re-record the area record on dev after the last release merge, per the record rule. It is not a finding here.

## Prior public findings on this PR

This section was written after the verdict and the ledger above were on disk.

**What PR #826 carried when read:**
- Manager review-start notices: 6530896916, 6530905878, 6537198680 and 6537204407.
- Two review rounds, both at `8b28ebaf`: `[R756] NEGATIVE` (6532064254) and `[R755] NEGATIVE` (6532204298).
- No review bodies and no inline review comments.
- The R756-2 round started at this head, but nothing from it was published when read.

| Prior finding | Status at `4ee2aa96` | Evidence |
|---|---|---|
| R755-1 F-2 / R756-1 F-1 MINOR (Conformance, RTL, Tests, Docs): ZQCS issuance changed, and the claims said otherwise | **RESOLVED**, option (a) per ruling 6532211135 | ZQCS hold at `milan_soc.py:2463-2469`. The docstring is corrected. The PR text no longer says "unchanged". Z4 passes, and Z5 shows the undelayed plant fails. Z4 also kills the done-delay, two-cycle-hold and wrong-timer plants. The reviewer's nine-period sweep gives staged == LiteDRAM + 1 every time. R756-1's verification (a shortened period of the shipping parity class, staged equal to unstaged shifted, a planted variant failing) is met. |
| R755-1 F-1 MINOR (Tests) / R756-1 F-2 MINOR (Tests, Robustness): the stall paths were never exercised; lossy and drop-held stages survived | **RESOLVED** | F6 and D6 hold beats in all four registered READYs. R756-1's verification is met: `axi_lossy_ready`, `spi_tx_lossy_ready` and `spi_rx_lossy_ready` are KILLED, and the shipping stages pass. R755-1's verification is met: the drop-held mutants for aw, ar, SPI tx and SPI rx are KILLED by the behaviour arms. Duplicate-held and VALID-waits plants are KILLED too. Robustness, recorded for this finding under AGENTS.md section 3, is covered clean this round. |
| R755-1 S-1 SUGGESTION (Tests): F2's start filter | **ADDRESSED** | `test_soc_timing_cuts.py:334-398`: the starts are the bridge's registers. |

No prior finding is retained.

R755-2 FINISHED
