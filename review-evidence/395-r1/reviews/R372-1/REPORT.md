[R372] NEGATIVE - exact head 66001a307ce5de57577e66d6e3a18b9f4020764b

# R372-1: internal independent review of PR #605 for #395 items 1, 2 and 5

- Head `66001a307ce5de57577e66d6e3a18b9f4020764b`, tree `2b9a0759a17be8b417441a6d565d4522a0fe23b6`. It is one commit on dev `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
- The commit message is one line with no trailers. The PR body says "Relates to #395", with no closing keyword.
- Context was cleared. I reconstructed the work from public material only:
  - AGENTS.md and CONTRIBUTING.md
  - the #395 body, the owner decision (comment 5789765635), the assignment (5859935504), TAKEN (5859944584) and REVIEW READY (5860231405)
  - the linked BUILDING, RUNNING_TESTS, LITEX_SOC and AREA_BUDGET clauses
  - the diff `8bc97021..66001a30`
  - the public evidence tree `42822357:review-evidence/395-r1`
  - the exact-head hosted checks
- No prior public review findings existed on PR #605 when this round started. The only PR comments were the two review-start notices. There is nothing to resolve or retain.

## Verdict summary

The code does what the lane was asked to do, and I reproduced its measurements:

- The declaration, the platform derivation, the checkpoint reporter and the four-endpoint table are correct.
- A reviewer rerun of the PR's own reporter on the shipping checkpoint gives the published numbers exactly. The input hashes match.
- The reading "two fixed timing models repeated at the temperature endpoints" is correct, and I confirmed it by experiment. Changing the grade and junction temperature over commercial 0/25/85 C, industrial -40/100 C and extended 100 C leaves Slow and Fast WNS/WHS unchanged to the picosecond.

The verdict is NEGATIVE for one MAJOR and two MINOR findings:

- **F1 (MAJOR):** the signoff record does not detect or report that the shipping build's own clock-crossing constraints were never applied. There are 15 CRITICAL WARNINGs in the shipping build log. This is the direct cause of the two "unsafe" clock pairs. It also means the eth-to-sys protection that `sw/litex/milan_soc.py` documents against a warm-die failure is not present in the build.
- **F2 (MINOR):** the builder test misses five of my planted faults. It does not guard the refusal inside the hook the platform actually runs, and it does not guard the report arguments that carry item 2's content.
- **F3 (MINOR):** item 2 is scored against a margin that #395 lists as an unresolved decision. The record also cites "WNS >= 0" where BUILDING already gives the AX7101 +0.03 ns caveat.

## Findings

### F1 - MAJOR - Conformance, RTL, Docs

**Location:**

- `docs/findings/COMMERCIAL_TIMING_395.md:65-69` (clock-interaction paragraph) and `:93-95` (limits)
- shipping artifacts `alinx_ax7101.xdc:583-595` and the shipping build `vivado.log`
- source `sw/litex/milan_soc.py:1499-1534` and `:1550-1556`

**Title:** The signoff record misses that the shipping image's intended clock-crossing constraints did not apply.

**Authority and evidence:**

- #395 item 2 and the assignment ask for clock-interaction and CDC summaries for the shipping candidate. The record is the release timing signoff for the declared range, and static timing proves only what the applied constraints ask.
- The shipping build log has 15 CRITICAL WARNINGs (`receipts/shipping-build-critical-warnings.txt`):
  - `[Vivado 12-4739] No valid object(s) found` for every `get_clocks {crg_clkout0 crg_clkout1}` at xdc:583/585/587/589, and for the audio clock group at xdc:591.
  - `[Designutils 20-1307] Command 'if' is not supported in the xdc constraint file` at xdc:595.
- The real clock names are `milansoc_crg_clkout0/1/2/3/4`, `milansoc_crg_audio_*` and so on. `get_clocks crg_clkout0` matches 0 clocks (`receipts/v2-probe-results.txt`, P3).
- Consequences in the shipping checkpoint:
  - The intended `set_false_path -hold` / `set_max_delay -datapath_only 8.000` between `eth_clocks0_rx` and the sys/milan clocks does not exist. This is why `eth_clocks0_rx -> milansoc_crg_clkout1` is `Timed (unsafe)` at a 4 ns requirement and the reverse pair is `Partial False Path (unsafe)`.
  - The eth-to-sys crossings (13 and 16 endpoints) stay `False Path` through LiteX's generic MultiReg false path. That false path would also take precedence over the intended max-delay if the names were fixed.
  - The quasi-static multicycle relaxation for 112 tagged cells is also absent. This last one makes analysis stricter, not looser.
- `sw/litex/milan_soc.py:1499-1509` says why the bounded crossings exist. An unbounded eth crossing "shipped a bitstream whose CPU-bound RX/ARP died as the die warmed". That is a temperature-dependent failure mechanism, and a temperature-range signoff should surface it.
- The record lists "six Ignored" and two unsafe pairs, and says positive slack does not prove CDC correctness. It does not say that the design's own bounding constraints silently failed to apply, and the constraint-application log was not examined. `report_methodology` was not run either: the per-corner summaries say so.

**Reviewer measurement (context, not a waiver):** I cleared the in-memory constraints on the read-only checkpoint and re-applied only the two primary clocks plus the intended 8 ns datapath-only bound (`receipts/v3-crossings-results.txt`, `receipts/v2-probe-results.txt` P3). The shipping placement meets that bound at both corners:

| Crossing | Worst Slow datapath | Worst slack |
|---|---:|---:|
| eth to sys | 2.179 ns | 5.746 ns |
| sys to eth | 3.395 ns | 4.313 ns |
| eth to milan | 5.373 ns | 2.560 ns |
| milan to eth | 0.875 ns | 7.066 ns |

So the shipping image itself is not shown to be at risk on these crossings. The risk is that no candidate, including every sweep seed, is checked against the bound the source says it is.

**Impact:** A reader of the record concludes that the clock interactions of the signed-off image were analysed under the design's constraints, and that the only open items are generic CDC diagnostics and I/O delays. In fact the constraint set that protects a known warm-die failure never reached the tool, and nothing makes the build fail when that happens.

**Required outcome:** No timing fix in this lane.

1. The record (and the BUILDING/RUNNING_TESTS retention list, if the lane agrees) states:
   - that the shipping build's clock-crossing constraints at xdc:583-595 did not apply, with the warning IDs;
   - that this is the cause of the two unsafe pairs;
   - that the eth-to-sys crossings are unbounded false paths;
   - measured slack against the intended bound, or an explicit statement that it was not measured.
2. The retained signoff evidence includes the build log's CRITICAL WARNING census, or an equivalent constraint-application check such as `report_methodology`.
3. A public follow-up Issue owns the constraint defect: the names, precedence against the MultiReg false path, and failing the build on 12-4739. The record links it.

**Verification:** Re-review the record at the new head. Confirm the Issue exists and is linked. Recount the warnings from the shipping build log.

### F2 - MINOR - Tests

**Location:** `sw/builder/test_timing_grade.py:84-113` and `sw/litex/timing_grade.tcl:39-40, 61, 74-76`

**Title:** The builder test does not guard the hook-level refusal or the per-corner report content.

**Authority and evidence:**

- The assignment requires that "a candidate analysed at other conditions is refused", and AGENTS section 6 (Tests) requires tests that can fail for the defect they claim.
- The refusal controls at `:93-97` call `kl_timing_grade_check` directly. The hook the platform actually runs, `kl_timing_grade_reports` (`receipts/t7-litex-generated-build-tcl-excerpt.txt` line 80), is exercised only on the good path and the planted-report-failure path.
- I planted 22 faults (`scripts/mutation_probes.py`, `receipts/t3-mutation-probes.log`). The test killed 17 as expected. It passes with each of these:
  - `reports-no-leading-check`: deleting the leading `kl_timing_grade_check` at timing_grade.tcl:40. Driving the hook directly (`scripts/hook_refusal_probe.py`, `receipts/t4-hook-refusal-probe.log`) shows what that loses. At the head the hook refuses all four wrong conditions (Fast hold off, Slow off, industrial, Tj 25). With that one line removed it accepts three of them, because the `finally` restore repairs the configuration before the trailing check runs.
  - `reports-corner-setup-only`: per-corner `report_timing_summary -delay_type max`, which drops WHS/THS from every per-corner report.
  - `reports-corner-no-unconstrained`: dropping `-report_unconstrained`.
  - `reports-all-no-check-verbose`: dropping `-check_timing_verbose`.
  - `reports-clock-interaction-setup-only`: `report_clock_interaction -delay_type max`.
- The code at this head is correct. The live Vivado controls in `receipts/v2-probe-results.txt` P2 refuse all six real mutations and accept the restored state.

**Impact:** A later edit could remove item 1's hook-level refusal, or item 2's hold, unconstrained or verbose content, and the builder bank would stay green.

**Required outcome:** Each of the five planted faults above makes the builder bank fail. For example, run the refusal controls through the hook as well as the check proc, and assert the report arguments that carry item 2's content.

**Verification:** Rerun `scripts/mutation_probes.py` and `scripts/hook_refusal_probe.py` against the new head. Expect `unexpected=0`, and hook rc=1 for every mutation.

### F3 - MINOR - Conformance, Docs

**Location:** `docs/findings/COMMERCIAL_TIMING_395.md:61`; REVIEW READY (issue comment 5860231405, "Acceptance: items 1, 2 and 5 delivered")

**Title:** Item 2's margin clause is scored against a decision that was never recorded.

**Authority and evidence:**

- The #395 body lists as unresolved decisions "the grade and the margin", and says the decision comes first.
- Acceptance item 2 reads "WNS at or above the margin decided in item 1 at every corner".
- The owner decision of 2026-09-23 records the grade only. The assignment does not set a margin.
- The record says the result "clears the existing WNS >= 0 rule, without inventing a new margin". BUILDING's own gate (`docs/integration/BUILDING.md:72`, `:614-616`) already says to keep AX7101 margin above +0.03 ns (QSPI flashboot corruption), and the record does not cite it.
- The measured 0.123 ns meets both 0 and +0.03 ns, so no timing outcome changes.

**Impact:** Item 2 is reported as delivered against a criterion that depends on an open decision. AGENTS section 2 says to publish the conflict rather than choose an interpretation.

**Required outcome:** One of two things:

- #395 records the margin decision and the record cites it; or
- the record and the handoff state that item 2's margin clause is pending that decision.

In either case the record cites the existing AX7101 +0.03 ns caveat and the measured result against it.

**Verification:** Read the #395 thread and the record at the new head.

### Suggestions (no effect on coverage)

- **S1 (Docs), `COMMERCIAL_TIMING_395.md:57` and `BUILDING.md:529-534`.** "UG835 documents that operating-condition temperature is not used for timing" is stronger than the tool's own help text. The help says the conditions are used for power analysis, and warns that a Vccint change can change the speed grade and affect timing (`receipts/v4-help-set_operating_conditions.txt`). The claim is true in substance: my probe P1 shows identical timing across grade and Tj. Consider citing that measurement.
- **S2 (Docs).** The pre-placement hook fixes Tj at 85 C before `report_power` (`receipts/t7-litex-generated-build-tcl-excerpt.txt` lines 49 and 79). New builds' `*_power.rpt` are therefore worst-case at 85 C, where they used to be at an ambient-derived Tj (the shipping report says 28.5 C). No consumer depends on this, but it is worth one sentence.
- **S3 (Robustness), `sw/litex/report_timing_grade.py:17-20`.** A missing checkpoint exits with a traceback rather than a usage error. An output path containing a brace creates the directory before `tcl_word` refuses it. Both fail closed (`receipts/t5-reporter-robustness.log`).
- **S4 (Docs), `docs/findings/README.md`.** The "Current entries" table does not list the new record. `397_SERVICE_BUDGET.md` from the previous PR is listed; `PP_SHADOW_BASELINE.md` is not, so the convention is loose.

## Answers to the assigned checks

1. **Single declaration.**
   - `sw/litex/platforms/ax7101_timing.py:13-19` is the only analysis-side source of part, grade, Tj range and corners.
   - The platform takes its part and its pre-placement and bitstream hooks from it. LiteX places the hooks correctly in a real generated build script: configure after `opt_design` and before `place_design`, signoff after route and power and before `write_bitstream` (`receipts/t7-litex-generated-build-tcl-excerpt.txt`).
   - The checkpoint reporter derives from the same function, and it refuses output inside the checkpoint directory, including through a symlink.
   - The remaining part strings in code are the programmer part (`sw/litex/build.sh:69`) and area-budget tables, with no speed grade and no analysis role. Test oracles restate the declaration on purpose.
   - Refusal controls are real. My 17 killed plants include every declaration change, the grade/Tj/corner/part checks, the restore and the platform wiring. The live Vivado refusals work (P2). The survivors are in F2.
2. **Per-corner table.**
   - The checkpoint sha256 `5f7a442b...f5d1` (115715651 bytes) matches, as do the bitstream, implementation Tcl and XDC (`receipts/shipping-inputs.sha256`; rechecked unchanged after the probes in `receipts/t9-shipping-inputs-recheck.txt`).
   - The reviewer rerun reproduces every value: Slow 0.123/0.000/0.101/0.000, Fast 1.429/0.000/0.036/0.000, combined 0.123/0.036, 175907 endpoints, WPWS 0.264, no negative paths (`receipts/v1-pr-reporter-summary.txt`).
   - The fixed-model reading is correct for this -2 Artix-7 speed file (PRODUCTION 1.23). Grade and Tj change only the power operating conditions (P1).
   - The report covers what item 2 asks: WNS/TNS/WHS/THS per model and endpoint, clock interaction, CDC, and verbose unconstrained-path and check_timing output. F1 is about interpreting the clock-interaction result, not about coverage.
3. **Visible findings.**
   - Every count is accurate and none is waived. CDC: 10 Critical, 503 Warning, 22 Info. Clock pairs: 16, of which 8 Clean, 6 Ignored and 2 No Common Clock. I/O: 46 inputs and 87 outputs without delay constraints; the port groups match the record's list (DDR3, GMII, TDM, UART, SPI flash, MDIO, reset button).
   - Real risk and own Issue:
     - **Unsafe pairs:** yes. These are the F1 constraint defect.
     - **GMII RX (`eth0_rx_data[7:0]`, `eth0_rx_dv`) and GMII TX (`eth0_tx_data`, `eth0_tx_en`, forwarded `eth_clocks0_gtx`) without I/O delays:** yes. This 125 MHz source-synchronous interface is not covered by static timing at any corner, so the 0 to 85 C claim does not reach the external Ethernet timing. The record discloses this; it needs an owning Issue.
     - **DDR3:** relies on LiteDRAM calibration. Record that rationale.
     - **TDM:** partly owned by #452.
     - **UART, flash, MDIO and the reset button:** low rate, low risk.
     - **The 10 critical CDC diagnostics:** nine are asynchronous-assert reset-synchronizer PRE inputs fed by combinations of resets from several domains (PHY reset storage, link-guard `eth_rst_r`, SoC reset storage, gPTP `recov_req_o`). That is a glitch-only risk. The tenth is combinational PLIC logic in front of the CPU's `mei_flag` synchronizer, a possible one-cycle spurious interrupt. None is a static-timing risk. One low-priority triage Issue is warranted.
4. **Docs sections.** BUILDING section 5 (lines 517-553), RUNNING_TESTS section 5 (lines 160-177) and LITEX_SOC section 7 (lines 144-160) each state the commercial 0 to 85 C grade and the Slow/Fast setup-and-hold corner rule. `docs_check.py` and `check_doc_paths.py` pass, and `git diff --check` is clean (`receipts/t6-docs-gates.log`).
5. **Items 3 and 4** are left open: "Relates to #395", with no closing keyword, and the record and all three docs say so. No timing fix is in the diff.

## Reviewer-owned ledger

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | #395 body, owner decision and assignment against: the diff; `ax7101_timing.py`, `alinx_ax7101.py:294-310`, `report_timing_grade.py`; reviewer reporter rerun on the shipping checkpoint (`v1-*`); grade/Tj sensitivity P1; shipping build log and xdc:579-595 | R372-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| RTL | UNCLEAN (F1) | No HDL in the diff. Examined: the signed-off image's clock and CDC architecture (`v1-signoff_clock_interaction.rpt`, CDC report critical rows, `v2-probe-results.txt` P3, `v3-crossings-results.txt`); `milan_soc.py:1490-1556`; hook placement in the generated build script (t7) | R372-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| Robustness | CLEAN | `timing_grade.tcl` failure and restore paths (stub planted failure, live P2 refusals and restore); reporter argument edges (missing checkpoint, same and symlinked directory, brace, space/`$`/`[` literals; t5); hook under four wrong conditions (t4, head arm); only S3 open | R372-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| Tests | UNCLEAN (F2) | `sw/builder/test_timing_grade.py`; `test_builder.py:27556-27573`; focused runs t1/t2 rc 0; 22 planted faults (t3); hook probe (t4); hosted elaborate job 108717778140 executed both timing-grade arms | R372-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |
| Docs | UNCLEAN (F1, F3) | `COMMERCIAL_TIMING_395.md`; BUILDING section 5 (517-553); RUNNING_TESTS section 5 (160-177); LITEX_SOC section 7 (144-160); `docs/findings/README.md`; tool help text (v4); docs gates (t6) | R372-1 | 66001a307ce5de57577e66d6e3a18b9f4020764b |

## Real limits

- All timing work was read-only static analysis of the saved routed checkpoint with the installed Vivado 2026.1 (build 6511674), limited to 8 threads. No synthesis, placement, routing or bitstream was run. A LiteX build script was generated with `run=False` only.
- The crossing measurement in F1 used in-memory constraint replacement (`reset_timing` plus two clocks and the intended bound). It measures data-path delay against that bound. It does not prove CDC correctness.
- The CDC risk statements come from report rows and signal names, not from reading the RTL of each synchronizer.
- No physical or temperature measurement was made. Items 3 and 4 remain unmeasured.
- Hosted status was read at review time. rtl-fast, elaborate, verilator-lint, Yosys shards 0-3, yosys-elaboration, Verilator shards 0 and 3, and the other listed jobs were complete and successful. docs-check (its builder step had succeeded) and Verilator shards 1, 2 and 4 were still in progress. "Physical gPTP" was skipped, which is not hardware proof.
- I did not run the full builder banks (not permitted); the manager's banks stand as published.
- To read the public evidence commit `42822357`, I fetched it into the review clone. That added an object and FETCH_HEAD, but no tracked content changed.
- Clone integrity after the probes: HEAD, the index write-tree and the worktree equal the head tree. All 945 tracked blobs match by hash. The four gitlinks match the tree (`receipts/t8-clone-integrity.txt`).

## Pending manager duties

- Publish this verdict. Relay F1 to F3 to the executor lane.
- Open or assign the follow-up Issues named in F1 and check 3:
  - the unapplied eth/sys/milan and audio clock constraints, and the unsupported XDC `if`;
  - GMII I/O delay constraints;
  - CDC critical-diagnostic triage.
- Obtain or record the #395 margin decision (F3).
- Own hosted and local-replica acceptance at the final head, and the current-dev candidate build at the merge turn.
- Re-review is needed at any new head. F1 and F3 are Docs/Conformance-scope changes and F2 is a Tests-scope change. Robustness coverage stays valid only if `sw/litex/timing_grade.tcl` and `sw/litex/report_timing_grade.py` are unchanged.

R372-1 FINISHED
