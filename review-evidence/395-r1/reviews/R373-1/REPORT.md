[R373] NEGATIVE - exact head 66001a307ce5de57577e66d6e3a18b9f4020764b

# R373-1: external review of PR #605 for #395 items 1, 2 and 5

- Head `66001a307ce5de57577e66d6e3a18b9f4020764b`, tree `2b9a0759a17be8b417441a6d565d4522a0fe23b6`. The PR is one commit on dev `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. The commit message is one line with no trailers.
- Role: external independent reviewer, working in a cleared context. I reconstructed the task from AGENTS.md, CONTRIBUTING.md and docs/README, then read the #395 body, the owner decision (comment 5789765635), the assignment (5859935504), TAKEN (5859944584) and REVIEW READY (5860231405). After that I read the diff `8bc97021..66001a30`, the public evidence tree `42822357:review-evidence/395-r1` (all 61 blobs downloaded and hash-verified), and the exact-head hosted checks.
- Verdict: **NEGATIVE**. The verdict rests on one open MINOR finding, F1, under Conformance and Docs. The code, the declaration, the tests and the measured numbers all hold up under independent re-measurement. What is missing is in the signoff record: it does not state why the two unsafe clock pairs exist. They exist because the shipping image dropped the design's own Ethernet-crossing exceptions, with CRITICAL WARNING 12-4739.
- Prior public review findings on PR #605: **none exist at this head**. I read the PR after my own pass: 0 reviews, 0 review comments, and the issue comments are only the two start notices. Nothing is carried forward.

## Answers to the assigned verification points

**(1) One declaration, derived consumers, real refusals.** Met.
- `sw/litex/platforms/ax7101_timing.py:13-19` is the only executable declaration of part, grade, endpoints and corners.
- `sw/litex/platforms/alinx_ax7101.py:298-305` derives the part, the pre-placement configuration and the post-route signoff hook from it.
- `sw/litex/report_timing_grade.py:22-26` derives the saved-checkpoint Tcl from the same declaration.
- In the LiteX revision used, the pre-placement hook is emitted before `place_design`, and the signoff is emitted after route and post-route phys_opt but before `write_bitstream`. A failing hook therefore aborts the bitstream.
- No other writer overrides the AX7101 hooks. `milan_soc.py:3894` only appends `opt_design`.
- Refusal controls planted by me run in the real timing tool against the committed hook on a copy of the shipping checkpoint. All 11 refused:
  - part: another device, and a nonexistent part. The nonexistent part fails closed with the tool's own error rather than the hook's message.
  - grade: extended;
  - Tj: 84.9, 100, -40 and auto;
  - `reset_operating_conditions`;
  - corners: `-delay_type max` on both, `-hold` only, `-setup` only.
  
  An equivalent `85.0` was accepted, which is correct. Receipt: `receipts/independent-probe/probe.log`.
- Mutation probe on the builder test: all 22 mandatory mutants were killed, and the unmodified control survived. Receipt: `receipts/mutation_probe.txt`.
- Restatements found outside the declaration:
  - `milan_soc.py:215` `S7PLL(speedgrade=-2)`;
  - the out-of-context flows `syn/ooc/milan_datapath_ooc.tcl:372` and `syn/ooc/pp_shadow_ooc.tcl:98`, plus the `syn/ooc/pp_baseline.py:451` fixture;
  - the programmer part strings in `build.sh:69` and `deploy.sh:78`, which carry no speed grade.
  
  None of these analyses a release candidate, so item 1 holds. See S2.

**(2) Per-corner table for the `9e9954e9` checkpoint.** Reproduced exactly.
- The input sha256 values match the record: checkpoint `5f7a442b…d5f1`, bitstream `1696d1ea…c2c7`, Tcl `a6827b13…895e`, XDC `c94fe242…6d49`.
- The shipping log shows `write_checkpoint … route.dcp` and then `write_bitstream` in the same run. The recipe claims (32 threads, no seed, directives, the tool build 6511674, speed file 1.23 dated 2018-06-13, 100 and 50 MHz clocks) match the retained Tcl and log.
- I re-ran the committed reporter with the thread cap edited from 16 to 8 as my only change; it exited 0 in 64 s. Its WNS/TNS/WHS/THS/WPWS figures equal the published ones for all four endpoint/model reports and for the combined report:

  | Corner | WNS | TNS | WHS | THS | WPWS (ns) |
  |---|---:|---:|---:|---:|---:|
  | Slow | 0.123 | 0 | 0.101 | 0 | 0.264 |
  | Fast | 1.429 | 0 | 0.036 | 0 | 0.264 |

- The CDC, check_timing and clock-interaction reports are identical to the published ones apart from date and path header lines. The negative-slack reports contain 0 paths.
- **Reading of the temperature model: correct.**
  - The tool's own command reference says that operating conditions "are used for power analysis … but are not used during timing analysis" (`report_operating_conditions`).
  - The same reference defines the Slow and Fast corners as PVT extremes (`config_timing_corners`). Receipt: `receipts/help-probe/help.log`.
  - Empirically, from −40 to 100 C, with commercial, industrial or extended grade, `-process maximum`, and Vccint 0.95 or 0.90, the independent per-corner setup/hold slack, TNS/THS and worst-path datapath delay are unchanged at the reported precision. The part and speed grade do not change.
  - So "two fixed timing models repeated at the endpoints" is the right description. For this part, the Slow model bounds the commercial range conservatively.
- **Coverage of item 2:** WNS/TNS/WHS/THS per corner, clock interaction, CDC and unconstrained paths are all present. F1 concerns what the clock-interaction summary says, not whether the report exists.

**(3) Visible findings.**
- The counts are accurate and nothing is waived: 10 Critical, 503 Warning and 22 Info CDC diagnostics; 16 clock pairs (8 Clean, 6 Ignored, 2 No Common Clock); 46 inputs and 87 outputs without delay constraints. I re-derived the port lists: the 46 inputs are 32 DDR3 DQ, 10 GMII RX, MDIO, TDM in, flash MISO, UART RX and reset. The 87 outputs are the DDR3 bus, GMII TX, TDM, flash, UART, MDIO/MDC and PHY reset.
- Whether any of them is a real timing risk:
  - **Unsafe pairs, eth_rx and clkout1.** Root cause: `milan_soc.py:1520-1534` names `crg_clkout0/1` and the `crg_audio_*` clocks, but the design's clocks are `milansoc_crg_*`. All five crossing exceptions are dropped: the shipping implementation log carries seven CRITICAL WARNING [Vivado 12-4739] and one 12-5201 (`receipts/shipping_build_constraint_warnings.txt`). As a result, the eth and milan handshake crossings are timed against a meaningless 4 ns edge relationship, with a 0 ns hold requirement.
  - I applied the intended exceptions in memory. The intended 8 ns datapath-only bound is **met** on the shipping image, with slack 2.560 ns (eth→clkout1) and 7.066 ns (clkout1→eth).
  - The LiteEth eth↔sys gray-pointer, pulse and reset crossings remain false-pathed by the LiteX `mr_ff`/`ars` rules even with correct names, because a false path outranks max-delay. Their Slow-corner datapaths are at most 2.179 ns and 3.395 ns (`receipts/eth-probe/eth.log`, `receipts/skew-probe/skew.log`).
  - **So there is no demonstrated timing violation in the shipping image.** However, the bound the source comment promises, written after a die-temperature field failure (`milan_soc.py:1499-1509`), is not in force for any seed. This needs its own issue (NEW-1).
  - **Unconstrained I/O.** GMII RX (`eth0_rx_data[7:0]`, `rx_dv`) and TX (`tx_data`, `tx_en`, `gtx`) at 125 MHz are source-synchronous and not analysed at any corner. That is a real temperature-dependent gap and needs its own issue (NEW-2). TDM I/O timing is already partly owned by #452. DDR3 relies on PHY calibration. Serial, flash, MDIO and reset are low-rate.
  - **CDC Criticals.** All ten fall on reset synchronizers, plus one PLIC→MEI flag crossing inside the CPU. No timing violation was shown. Two are worth individual triage (NEW-3): gPTP `u_txret/recov_req_o` reaching a reset synchronizer through logic (CDC-10), and the PLIC best-request priority reaching the MEI `buffercc` through three levels of logic.

**(4) Docs.**
- BUILDING §5 (`docs/integration/BUILDING.md:517-553`), RUNNING_TESTS §5 (`docs/testing/RUNNING_TESTS.md:160-176`) and LITEX_SOC §7 (`docs/litex/LITEX_SOC.md:145-160`) each state the commercial grade (0 to 85 C junction) and the corner rule.
- `docs_check.py`, `check_doc_paths.py` and `git diff --check` each returned rc 0 at the head (`receipts/docs_gates.txt`).

**(5) Items 3 and 4 left open.** Yes. The PR body says "Relates to #395", `closingIssuesReferences` is empty, and no firmware or XADC change is in the diff.

## Findings

### F1 - MINOR - Conformance, Docs - the signoff record omits the cause of the two unsafe clock pairs

- **Where:** `docs/findings/COMMERCIAL_TIMING_395.md:65-69` and `:84-95`. Also BUILDING §5's retention list at `docs/integration/BUILDING.md:547-550`.
- **Authority and evidence:**
  - Item 2 of #395 and the assignment ask for clock-interaction and CDC summaries for the shipping candidate. AGENTS §6 (Docs) requires that the PR and Issue carry enough evidence for another cold reviewer.
  - The shipping implementation log (`vivado.log` lines 4115-4146, sha256 `4519c33a…60a6`) shows every exception at XDC:583-591 rejected with CRITICAL WARNING 12-4739. Those exceptions are two false-path-hold, two max-delay-8 ns and one asynchronous group.
  - Those exceptions are the source's intended treatment of the eth_rx ↔ clkout0/1 pairs. The record calls the pairs "Timed (unsafe)" and "Partial False Path (unsafe)" and adds only that positive slack does not establish CDC correctness.
  - Nothing in the published evidence mentions 12-4739 (search over all 61 evidence blobs: no match).
- **Impact:** a cold reader of the durable signoff record cannot tell that the analysed image's constraint set differs from the source's intent. Nor can they tell that the difference sits exactly on the crossing whose earlier thermal failure motivated the constraint. The record's WNS >= 0 at every corner is then read as covering a crossing policy that was never applied. BUILDING's retention recipe also has no step that would surface dropped constraints: they appear only in the build log, not in any retained report.
- **Required outcome:**
  - The record names the dropped exceptions: log lines and codes, the source lines, and the reason (clock-name prefix).
  - It states the measured consequence: the unsafe 4 ns relationship now, and the intended 8 ns bound met with 2.560/7.066 ns slack.
  - It links a follow-up issue for the constraint defect.
  - No timing or constraint fix in this lane.
  - Optionally, the retention list in BUILDING §5 names the implementation log's constraint-application critical warnings.
- **Verification:** the amended record cites these facts, and they are reproducible with `scripts/eth_crossing_probe.tcl` and the log excerpt. The follow-up issue exists and is linked. The docs gates return rc 0 at the new head.

### Suggestions (non-blocking; they do not affect lens coverage)

- **S1 - Conformance, Docs.** The #395 body's "Decision first" bullet asks for the grade *and* the release margin. The 2026-09-23 decision records only the grade. The record applies the existing WNS >= 0 rule (`docs/findings/COMMERCIAL_TIMING_395.md:61`), and the frozen assignment did not ask for a margin, so this is not a defect of this PR. Item 2's "WNS at or above the margin decided in item 1" nonetheless remains conditional on a decision nobody has recorded. The Fast-corner hold margin is +0.036 ns.
- **S2 - Conformance.** `sw/litex/milan_soc.py:215` hard-codes the PLL speed grade that the declared part implies. It could derive it from `TIMING_GRADE["part"]`. The out-of-context flows restate the part for estimates only.
- **S3 - Tests.** Three report-argument mutants survive (`receipts/mutation_probe.txt`): dropping `-report_unconstrained` from the combined summary, dropping `-details` from `report_cdc`, and dropping the final post-restore check. Restoration itself is still proven by the combined-summary state assertion. The stubs already print the arguments, so asserting them would pin the report content that item 2 requires.
- **S4 - Tests, Docs.** `sw/builder/test_builder.py:27561` reuses the shared LiteX skip text, which speaks of an "argv -> Instance parameter chain". That text is misleading for this gate in the hosted docs job, which recorded the skip correctly.
- **S5 - Docs.** Pinning Tj to 85 before placement turns every candidate's `*_power.rpt` into a worst-case estimate. On the shipping checkpoint that is 1.489 W against 1.299 W at auto Tj, the Junction Temperature row reads 85.0, and Max Ambient stays 81.0 C (`receipts/power-probe/`). This is conservative and fine, and it is worth one sentence where the release accounting reads the power report.
- **S6 - Robustness.** `sw/litex/report_timing_grade.py:21` creates the output directory before `tcl_word` refuses a brace path, so a refused run leaves an empty directory behind (`receipts/reporter_robustness.txt`).

## New work outside this lane, for the manager to file (not findings against this PR)

These defects are pre-existing, lie outside the diff, and are explicitly outside this lane ("No timing fix"). Under AGENTS §4 they are new public work, not deferred findings of this PR.

- **NEW-1:** the eth-crossing exceptions at `sw/litex/milan_soc.py:1520-1534` never apply. This is caused by the clock-name prefix; the audio group is dropped too. Separately, the LiteX `mr_ff` false path outranks the intended max-delay for the LiteEth gray pointers, so the "bounded crossing" policy of the 2026-08-06 comment does not exist in any GMII build. The shipping image happens to meet the intended bound. Future seeds are unguarded.
- **NEW-2:** GMII RX/TX I/O has no input or output delays, so the temperature signoff does not cover the Ethernet pin interface.
- **NEW-3:** triage of the CDC-10 and CDC-12 Criticals, in particular the gPTP `recov_req_o` reset-path logic and the PLIC→MEI crossing.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts (at head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #395 body, owner decision and assignment against `ax7101_timing.py:13-19`, `alinx_ax7101.py:298-305`, `report_timing_grade.py`, `timing_grade.tcl`; independent real-tool re-measurement of all corners and of the temperature/grade sweep (`receipts/committed-reporter/`, `receipts/independent-probe/probe.log`); the tool's command reference (`receipts/help-probe/help.log`); shipping build log constraint lines (`receipts/shipping_build_constraint_warnings.txt`) | R373-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| RTL | CLEAN | `sw/litex/timing_grade.tcl:5-79` (configure/check/report flow, try/finally restore, error propagation); `alinx_ax7101.py:298-311` against LiteX `vivado.py` emission order (pre-placement before `place_design`, signoff after route+phys_opt, before `write_bitstream`); other hook writers `milan_soc.py:3773-3916`; shipping clock interaction, CDC and eth-crossing probes (`receipts/eth-probe/`, `receipts/skew-probe/`). The pre-existing constraint defect is outside the diff and filed as NEW-1 | R373-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| Robustness | CLEAN (S6 only) | 11 planted real-tool refusals, covering −40/100/84.9/auto Tj, reset, extended grade, flag-form corner disables and a nonexistent part, plus an equivalent-value acceptance (`receipts/independent-probe/probe.log`); reporter refusals for a missing checkpoint, output inside or nested under the checkpoint directory, and a brace path (`receipts/reporter_robustness.txt`); restore-after-failure mutant killed (`receipts/mutation_probe.txt`) | R373-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| Tests | CLEAN (S3, S4 only) | `sw/builder/test_timing_grade.py`, `sw/builder/test_builder.py:27556-27573`; head run rc 0 with LiteX (`receipts/head_timing_grade_test.txt`); 26-mutant probe, 22/22 mandatory killed, control survived (`receipts/mutation_probe.txt`); hosted `elaborate` ran both halves and hosted `docs-check` ran the contract with the platform half recorded as a skip | R373-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| Docs | UNCLEAN (F1) | `docs/findings/COMMERCIAL_TIMING_395.md` (every numeric claim re-derived), `BUILDING.md:515-553`, `RUNNING_TESTS.md:156-176`, `LITEX_SOC.md:137-160`; `docs_check.py`, `check_doc_paths.py` and `git diff --check` rc 0 (`receipts/docs_gates.txt`) | R373-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |

## Real limits

- No hardware was used, no physical calibration or temperature measurement was run, and there is no oscillator evidence; items 3 and 4 remain open.
- Timing was re-measured only on the saved `9e9954e9` routed checkpoint. It was a scratch copy, and the originals were verified byte-identical before and after (`receipts/shipping-inputs-before.sha256`, `receipts/shipping-inputs-after.sha256`). I did not build a new candidate through the modified platform, so the pre-placement hook's live effect on placement and routing was not observed. It was checked only through LiteX Tcl emission order and the builder platform probe.
- I ran the committed reporter with 8 threads instead of 16, which was the only edit (`receipts/committed-reporter/report8.tcl`).
- The hook guards the part, operating conditions and corner enablement only. Analysis-wide settings such as `config_timing_analysis -ignore_io_paths true` are accepted by it (probe line `CONTROL ignore-io-paths`). That is consistent with the assignment's scope, which is the part and operating conditions, and it is recorded here as a boundary rather than a finding.
- I did not run the full builder bank, the parent/PP/gPTP/Yosys banks, act, or hosted acceptance. At the time of reading, hosted `rtl-full` was still in progress: Verilator shards 1, 2 and 4, while `rtl-fast` had succeeded and the physical gPTP job was skipped (`receipts/hosted_check_runs.txt`). Skipped contexts are not evidence.
- The judgement that the CDC Criticals are low risk comes from report structure and path classes. I did not do an RTL-level proof.

## Pending manager duties

1. Publish this report. F1 must be answered at a new head and re-reviewed. Any doc-only change re-opens the Docs and Conformance lenses at that head, and every other lens whose scope it touches.
2. File NEW-1, NEW-2 and NEW-3, or link existing owners, and have the record link NEW-1.
3. Record the #395 margin decision (S1) before item 2 is treated as closed.
4. Own hosted, act and candidate-merge acceptance at the final head, including the in-flight Verilator shards and the current-dev candidate build.
5. The internal review (R372) is independent and still required.

## Reproduction

- `scripts/independent_probe.tcl`, `scripts/eth_crossing_probe.tcl`, `scripts/falsepath_skew_probe.tcl`, `scripts/power_probe.tcl` and `scripts/help_probe.tcl` run in the timing tool against a copy of the routed checkpoint (usage in each header).
- `scripts/mutation_probe.py <checkout> <packet> <litex-python>` runs the mutation probe.
- Clone integrity after all probes: worktree, index and write-tree equal `2b9a0759…`, there are 0 untracked files, and the submodule gitlinks match (`receipts/clone_integrity.txt`).

R373-1 FINISHED
