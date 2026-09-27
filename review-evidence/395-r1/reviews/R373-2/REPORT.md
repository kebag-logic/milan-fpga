[R373] NEGATIVE - exact head 3a0cb4cf4fed2d71436a43f4b96cb375f9178342

# R373-2: external re-review of PR #605 for #395 items 1, 2 and 5

- **What was reviewed:** head `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`, tree `f6398593ff7a0449150cc18dd361e85cff6675d6`.
  - The PR base is dev `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
  - The round-2 delta is `66001a30..3a0cb4cf`. It has two commits, `09de469c7` and `3a0cb4cf4`. Each commit message is one line with no trailers (`git cat-file`).
- **Role:** external independent reviewer, working in a cleared context.
- **Reading order:**
  1. AGENTS.md, CONTRIBUTING.md and docs/README.
  2. The #395 body.
  3. The owner grade decision (5789765635) and the margin decision (5860418611).
  4. The round-2 assignment (5860419679), TAKEN (5860428534) and REVIEW READY (5860663722).
  5. #607.
  6. The diff and history.
  7. The public evidence.
  8. The exact-head hosted checks.
- **Evidence sources:**
  - The brief names evidence tree `42822357:review-evidence/395-r1`. That is the round-1 archive.
  - The round-2 packet is on the same evidence branch, one commit later: `fa9b0b5373abcb31b2ca6b20c3616b069d8672c4`, under `review-evidence/395-r1/author-r2/`.
  - I verified all 219 published blobs against the manager's `MANIFEST.json` `published_sha256`: 0 bad, 0 unlisted, and 78 path-redacted (`receipts/public_evidence_r2_check.txt`).
  - The author's own `MANIFEST.sha256` differs on 41 files. Every one of those 41 is marked `path_redacted` in the manager's manifest, and the published hashes match.
- **Verdict: NEGATIVE, on one open BLOCKER, R2-F1 (Tests, Docs).**
  - The round-2 record text fails the repository's bare-metal scope gate.
  - The hosted `docs-check` context therefore **fails at this exact head**, and every later step of that job, including the end-station builder gates, was skipped.
  - I reproduced the failure locally.
  - Everything the assignment asked for is otherwise delivered and independently verified: round-1 F1, R372-1 F1/F2/F3, and the taken S2.
- **Brief versus this head:** the brief says the manager's full source static bank passed at this head. The bare-metal scope gate (`docs/testing/RUNNING_TESTS.md:123-124`, `.github/workflows/docs.yml:185`) does not pass here.

## Answers to the assigned verification points

### (1) The record states the rejected exceptions, their cause and their consequence. Met.

**Rejected exceptions.** `docs/findings/COMMERCIAL_TIMING_395.md:78-110` names the rejected exceptions.

- **Codes, source lines and log lines:**
  - 12-4739 at `alinx_ax7101.xdc:583, 585, 587, 589` and 591;
  - 12-5201 at 591;
  - 20-1307 at `:595`;
  - log lines 1705/1710/1719/1721/1723/1724 and 4118/4123/4128/4133/4142/4144/4146/4147.
- **Cause:** the clock-name prefix. The XDC names `crg_clkout0/1` where the real clocks are `milansoc_crg_clkout0/1`, and the audio group is missing the same prefix.
- **Source:** `sw/litex/milan_soc.py:1520-1534` and `:1550-1556`. They are unchanged at this head: the only change to `milan_soc.py` is a one-line edit at :215.
- **My census of the shipping `vivado.log`** (sha256 `4519c33a…60a6`, 832920 bytes; `receipts/critical_warning_census.txt`):
  - 14 lines start with `CRITICAL WARNING:`: ten 12-4739, two 12-5201 and two 20-1307. These are exactly the record's lines.
  - A substring search gives 15 matches. The extra one is line 6400, which echoes the IOB-check source.
  - The log's own summary line 4167 reads "14 Critical Warnings".
  - The shipping XDC at 583-595 reads as the record says.
- **Correction of my round-1 report:** it put the implementation pass at "seven 12-4739 and one 12-5201". The correct implementation-pass count, lines 4118-4147, is six 12-4739, one 12-5201 and one 20-1307. The record's census is the correct one.

**Consequence.** `:112-119` states that the rejections cause both unsafe pairs, and that the eth↔sys crossings are unbounded false paths in both directions. It also says the LiteX MultiReg false path outranks max-delay, so fixing the names alone would not restore the bound. It links #607, which is open and owns the fix and the build refusal. I re-measured all of this on a scratch copy of the routed checkpoint (`scripts/crossing_probe_r2.tcl`, `receipts/crossing-probe/results.txt`). No `crg_*` name resolves, and 112 `quasi_static` cells exist (record `:101`).

**Measured slack per state.** The probe measured three constraint states:

| State (Slow/Fast, ns) | eth→sys (clkout0) | sys→eth | eth→milan (clkout1) | milan→eth |
|---|---|---|---|---|
| A: as shipped | 13 endpoints, all false path | 16, all false path | 50 timed at **4 ns**: setup 0.546/1.458, hold 1.095/0.182 | 6 timed at 4 ns (0.203/1.429); the rest false path |
| B: intended names added, other exceptions kept | still all false path | still all false path | 8 ns: **2.560/4.823** | 6 visible at 8 ns: **7.066/7.538**, datapath 0.875/0.432 |
| C: all constraints reset, 8 ns only | 5.746/6.717, datapath 2.179/1.240 | 4.313/5.895, datapath 3.395/1.979 | 2.560/4.823, datapath 5.373/3.092 | **14 endpoints**, 4.056/5.878, datapath 3.652/1.996, worst `FDPE_18/PRE` |

- Every figure in the record's table (`:132-137`) and in its "fully exposed" paragraph (`:140-145`) equals state C. The second commit's distinction is correct.
- In state C, eight of the fourteen milan→eth endpoints are the `FDPE_12..21/PRE` reset inputs driven from `milan_datapath/link_guard/eth_rst_r_reg`. The other six are the gPTP CDC data and handshake bits.
- State B reproduces my round-1 figure of 7.066 ns and the Fast figure of 7.538 ns. That population keeps the generic false paths, which is what the record says of "the review's narrower measurement".

**Retained census.**
- `author-r2/shipping-build-critical-warnings.txt` is published verbatim and equals my census line for line.
- `docs/integration/BUILDING.md:554-557` puts the census, with codes, source locations and original log line numbers, in the §5 retention list. `docs/litex/LITEX_SOC.md:157` and `docs/testing/RUNNING_TESTS.md:175` add it too.

### (2) Each of R372-1's five surviving planted faults now fails the builder bank. Met.

- **How the probe runs:** `scripts/mutation_probes.py` runs each mutant in a full disposable copy of the clone, git metadata included. The SoC import lists submodule files through git. A copy without that metadata made the unmodified control fail, so I widened the copy until the control passed.
- **What it runs:** the builder bank's first arm, `test_builder.test_commercial_timing_grade()`, with a LiteX interpreter available. An exception there aborts the bank's main loop nonzero (`sw/builder/test_builder.py:27573-27575`).
- **Result:** 38 mutants, 0 unexpected, and the unmodified control survives (`receipts/mutation_probes.txt`). The five named faults are each killed by a timing-grade assertion:
  - leading `kl_timing_grade_check` removed: `test_timing_grade.py:126`, stdout written before the refusal;
  - per-corner summary setup-only: `:78`;
  - per-corner summary without `-report_unconstrained`: `:79`;
  - combined summary without `-check_timing_verbose`: `:82`;
  - `report_clock_interaction -delay_type max`: `:89`.
- **My round-1 report-argument survivors are now killed:** the combined summary without `-report_unconstrained`, and `report_cdc` without `-details`. So are these neighbouring faults:
  - `check_timing` without `-verbose`;
  - combined summary setup-only;
  - per-corner hold-only;
  - negative-slack report setup-only, or with the wrong filter;
  - refusal moved after the grade file is written (`:127`).
- All 22 round-1 mandatory mutants remain killed at this head.
- One defense-in-depth mutant still survives: removing the trailing post-restore `kl_timing_grade_check` (`timing_grade.tcl:73`). Restoration itself stays pinned by the combined-state assertion at `test_timing_grade.py:133`, and the round-2 assignment did not name this fault. See S-A.
- Head runs pass (`receipts/head_timing_grade_test.txt`):
  - the standalone file rc 0;
  - the builder arm with LiteX rc 0, "19 wrong-condition refusals, including the report hook" plus the PLL control;
  - the builder arm with LiteX hidden rc 0, with the platform half recorded as a skip.

### (3) Item 2 is graded against the recorded margin decision and cites it. Met.

- The record links the decision and requires WNS >= +0.03 ns and WHS >= 0 at every declared corner (`COMMERCIAL_TIMING_395.md:61-68`). It says every row meets both, that worst WNS exceeds the margin by 0.093 ns, and that worst WHS is +0.036 ns.
- BUILDING (`:536-539`), LITEX_SOC (`:158-160`) and RUNNING_TESTS (`:168-170`) cite the same decision. The REVIEW READY handoff grades against it.
- The per-corner rows were recomputed:
  - The reporting chain (`timing_grade.tcl`, `ax7101_timing.py`, `alinx_ax7101.py`, `report_timing_grade.py`) is byte-unchanged since `66001a30`.
  - My round-1 real-tool run of the committed reporter therefore still applies. Its Design Timing Summary rows equal the author's round-2 fresh reports for all five reports (`receipts/corner_summary_crosscheck.txt`).
  - Slow WNS/WHS is 0.123/0.101, Fast is 1.429/0.036, and TNS and THS are 0. The decision is met.
- The record keeps the qualification that the result holds "for the applied constraints", and that missing constraints still limit the evidence (`:65-68`). State C shows that the intended crossing bound is met with at least 2.560 ns. So restoring the intended exceptions could not bring any crossing below the margin on this placement.

### (4) The PLL speed grade derives from the single timing-grade declaration. Met.

- `sw/litex/milan_soc.py:215` is now `S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))`. `platform.device` is `TIMING_GRADE["part"]` (`sw/litex/platforms/alinx_ax7101.py:298`).
- Only the `arty` board takes the other branch (`milan_soc.py:210-212`), and no third board reaches `_CRG`.
- `test_pll_grade` (`sw/builder/test_timing_grade.py:166-183`, called from `test_builder.py:27564`) patches the declaration, and the real constructor follows it. Restoring the literal `-2` or using `-1` is killed ("call(speedgrade=-2)").
- `receipts/pll_suffix_probe.txt`:
  - `-1`, `-2` and `-3`, and the hyphen-less `xc7a100tfgg484-2`, derive correctly;
  - the low-power `-2L` and `-1L` fail closed with a ValueError at elaboration.

### Scope

- Items 3 and 4 stay open: the PR says "Relates to #395" and has no closing keyword (`closingIssuesReferences` is empty).
- The diff has no firmware, XADC, XDC or constraint change. `milan_soc.py` changes only at :215. The record says (`:149`, `:175`) that no timing or constraint fix is included.

## Findings

### R2-F1 - BLOCKER - Tests, Docs - the round-2 record fails the bare-metal scope gate, so hosted docs-check fails at this head

- **Where:** `docs/findings/COMMERCIAL_TIMING_395.md:115`, which reads "Ethernet/sys crossings remain **unbounded false paths**, in both directions."
  - Commit `09de469c7` introduced it. The line is absent at `66001a30`, whose hosted `docs-check` succeeded (round-1 receipt).
- **Authority:**
  - `docs/testing/RUNNING_TESTS.md:123-124` lists `python3 scripts/check_baremetal_only.py --check` and `--selftest` among the §4 static gates.
  - `.github/workflows/docs.yml:185-186` runs them in the hosted `docs-check` job.
  - AGENTS §6 (Tests): "Existing regressions remain green."
  - AGENTS §7: required tests and local gates pass.
  - The round-2 assignment: "Gates: … all rc 0 at the committed head."
- **Evidence:**
  - `receipts/baremetal_gate.txt`: at this head, `check_baremetal_only.py --check` returns rc 1 with `docs/findings/COMMERCIAL_TIMING_395.md:115: [R] prohibited target runtime/service surface '/sys'`. Its self-test passes (700 arms).
  - `receipts/hosted_docs_check_failed_step.txt` and `receipts/hosted_check_runs.txt`: hosted `docs-check` job 108727991180 (run 36357487267) failed at exact head `3a0cb4cf` on that step and that line.
  - Steps 24-51 of the job were skipped, including "End-station builder gates", "Doc cited-path gate" and "Per-page contents gate".
  - The REVIEW READY gate list, and `author-r2/gates/`, contain no bare-metal scope gate run.
- **Impact:**
  - A required repository gate is red on the head offered for merge.
  - Hosted evidence for the builder bank, including the timing-grade arm, does not exist at this head.
  - The handoff's "documentation gates … all rc 0" is true for the gates it lists, but it does not cover the repository's documentation-side static gate that fails.
- **Required outcome:**
  - The record's wording no longer trips the gate, and the gate is not weakened or allowlisted to get there. For example, write "Ethernet-to-sys".
  - `check_baremetal_only.py --check` and `--selftest` return rc 0 at the new head.
  - Hosted `docs-check` succeeds at that exact head, with its builder-gate step executed rather than skipped.
  - The handoff's gate list includes this gate.
- **Verification:** rerun the gate locally, read the exact-head hosted `docs-check` job steps, and re-read the changed record lines. Their meaning must stay equivalent to the current `:112-119`.

### Suggestions (non-blocking; they do not affect lens coverage)

- **S-A (Tests).** Removing the trailing post-restore check at `sw/litex/timing_grade.tcl:73` survives (`receipts/mutation_probes.txt`). This is the remaining part of round-1 S3. The combined-state assertion at `test_timing_grade.py:133` still pins restoration, so it is optional.
- **S-B (Tests, Docs).** This is round-1 S4, unchanged. `sw/builder/test_builder.py:27561` still reuses the shared LiteX skip text about an "argv -> Instance parameter chain" for the timing-grade platform arm.
- **S-C (Docs).** This is round-1 S5, and R372-1 S2 says the same. The record still does not say that pinning Tj to 85 C before placement makes every candidate's `*_power.rpt` a worst-case estimate.
- **S-D (Robustness).** This is round-1 S6, unchanged. `sw/litex/report_timing_grade.py:21` creates the output directory before `tcl_word` (`:25`) refuses a brace path.
- **S-E (Docs).** The BUILDING gate rows at `docs/integration/BUILDING.md:72` and `:623-625`, and `docs/testing/RUNNING_TESTS.md:156`, still headline "WNS ≥ 0" and "comfortable margin". §5 now carries the decided +0.03 ns / WHS ≥ 0 rule. Linking those rows to the decision would leave one statement of the threshold.
- **S-F (Tests).** The `__main__` block of `sw/builder/test_timing_grade.py` (`:186-189`) does not run `test_pll_grade`. Only the builder entry does, and that is the gate the docs name.

## Prior public findings on this PR, resolved or retained at this head

I read these only after my own pass was complete.

| Finding | Status at `3a0cb4cf` | Evidence |
|---|---|---|
| R373-1 F1 (MINOR; Conformance, Docs): record omits the cause of the unsafe pairs | **Resolved** | Answer (1). Every required element is present and re-measured. The optional BUILDING retention step was added. |
| R372-1 F1 (MAJOR; Conformance, RTL, Docs): constraints never applied | **Resolved** | Answer (1). The census count is corrected from 15 to 14 plus one echoed line, which is right. #607 is linked. |
| R372-1 F2 (MINOR; Tests): five planted faults survive | **Resolved** | Answer (2). All five are killed through the builder arm. |
| R372-1 F3 (MINOR; Conformance, Docs): margin not decided | **Resolved** | Answer (3). The decision is recorded on #395 and cited in the record, the three docs and the handoff. |
| R373-1 S1 (margin) | Resolved | Same as R372-1 F3. |
| R373-1 S2 (PLL literal) | Resolved | Answer (4). |
| R373-1 S3 (report-argument mutants) | Resolved except the defense-in-depth mutant | S-A. |
| R373-1 S4, S5, S6 | Retained as suggestions | S-B, S-C, S-D. |
| R372-1 S1-S4 | Not findings; outside my ledger | For example, `docs/findings/README.md` still does not list the record (R372-1 S4). |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts (at head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #395 body; decisions 5789765635 and 5860418611; assignment 5860419679; #607. These were checked against `COMMERCIAL_TIMING_395.md:37-149`, the shipping `vivado.log` census (`receipts/critical_warning_census.txt`), shipping XDC 557-595, `milan_soc.py:1495-1556`, the three-state crossing re-measurement (`receipts/crossing-probe/`) and the corner rows (`receipts/corner_summary_crosscheck.txt`). Also `milan_soc.py:215` against `ax7101_timing.py:13-19`. Acceptance items 1, 2 and 5 are met; items 3 and 4 are open by scope. | R373-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| RTL | CLEAN | `milan_soc.py:195-233`. The PLL derivation is value-identical (-2) for the declared part, the arty branch is unchanged, and no other board exists (`receipts/pll_suffix_probe.txt`). `timing_grade.tcl`, `alinx_ax7101.py` and the reporter are byte-unchanged since `66001a30`, where my round-1 real-tool emission and hook analysis applies. Shipping clock interaction as shipped and as intended is in `receipts/crossing-probe/r2_clock_interaction_*.rpt`. The pre-existing constraint defect lies outside the diff and is owned by #607. | R373-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| Robustness | CLEAN (S-D only) | PLL grade derivation for -1/-2/-3, hyphen-less and -L parts (fails closed; `receipts/pll_suffix_probe.txt`). Refusal before any report or file write through `kl_timing_grade_reports`, for part, grade, Tj and six corner states (`test_timing_grade.py:118-127`; mutant `hook-check-after-grade-file` killed). Restore-after-failure path (`:135-140`; `reports-no-finally` killed). | R373-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| Tests | **UNCLEAN (R2-F1)** | `sw/builder/test_timing_grade.py:73-183`; `test_builder.py:27556-27575`; head runs (`receipts/head_timing_grade_test.txt`); 38-mutant builder-arm probe with control (`receipts/mutation_probes.txt`); repository static gates at head (`receipts/baremetal_gate.txt`, `receipts/static_gates_skipped_hosted.txt`); exact-head hosted `docs-check` failure (`receipts/hosted_docs_check_failed_step.txt`) | R373-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |
| Docs | **UNCLEAN (R2-F1)** | `COMMERCIAL_TIMING_395.md` (every round-2 claim re-derived: census, table, fourteen-endpoint distinction, margin grading, #607 link); `BUILDING.md:515-561`; `LITEX_SOC.md:145-163`; `RUNNING_TESTS.md:156-179`; REVIEW READY 5860663722 and the `author-r2` packet; `docs_check.py`, `check_doc_paths.py` and `git diff --check` rc 0 (`receipts/docs_gates.txt`); bare-metal scope gate rc 1 on record line 115 | R373-2 | 3a0cb4cf4fed2d71436a43f4b96cb375f9178342 |

## Real limits

- **No hardware.** No physical calibration or temperature measurement was run, and there is no oscillator evidence; items 3 and 4 remain open. Field skips are not hardware proof.
- **Timing re-measurement scope:**
  - Timing was re-measured on a scratch copy of the saved `9e9954e9` routed checkpoint only, at 8 threads.
  - The five shipping inputs (checkpoint, bitstream, Tcl, XDC, log) were byte-identical before and after (`receipts/shipping-inputs-before.sha256`, `receipts/shipping-inputs-after.sha256`).
  - No new candidate was built through the modified platform.
  - I did not re-run the committed reporter this round, because its chain is byte-unchanged since round 1. The corner rows rest on my round-1 run plus the author's round-2 fresh reports.
- **Gates I did not run:**
  - The per-page contents (TOC) gate did not run here: the pinned Markdown renderer is not installed, and installs are out of bounds. The author's `gates/toc.log` reports OK, and the record's headings are unchanged since round 1.
  - I did not run the full builder bank in either compiler mode, the parent/PP/gPTP/Yosys banks, act, or hosted acceptance.
  - The builder-arm mutation probe runs the bank's timing-grade function in isolation, not the whole bank.
- **Hosted state at fetch time (`receipts/hosted_check_runs.txt`):**
  - `docs-check` had failed.
  - `elaborate` and Verilator shards 1, 2 and 4 were still in progress.
  - The physical gPTP job was skipped.
  - `rtl-fast`, `docs-check-no-git`, the Yosys shards and Verilator shards 0 and 3 had succeeded.
  - Skipped contexts are not evidence.

## Pending manager duties

1. Publish this report. R2-F1 must be answered at a new head and re-reviewed there.
   - A change to the record re-opens the Docs lens at that head.
   - If the handoff's gate evidence changes, it also re-opens the Tests lens.
   - It re-opens Conformance if `:112-119` changes meaning.
2. Own hosted, act and candidate-merge acceptance at the final head. That includes exact-head `docs-check` with its builder-gate step executed, the in-flight `elaborate` and Verilator shards, and the current-dev candidate build against live dev `20aa4eabf310a43b654e0c74c5374c3a0458fd4b`.
3. Round-1 NEW-2 (GMII I/O delays) and NEW-3 (CDC-10/CDC-12 triage) were proposed as separate public work. I found no owning Issue, so file them or link existing owners. NEW-1 is #607.
4. The internal review (R372-2) is independent and still required.

## Reproduction

- `scripts/mutation_probes.py <clone> <packet> <litex-python>` runs the builder-arm mutation probe (at most 8 workers).
- `scripts/crossing_probe_r2.tcl` runs in the timing tool against a copy of the routed checkpoint (usage in its header).
- `scripts/pll_suffix_probe.py` runs from `sw/litex` with `PYTHONPATH=sw/litex` and the LiteX interpreter.
- Clone integrity after all probes (`receipts/clone_integrity.txt`):
  - HEAD, HEAD^{tree} and the index write-tree all equal `f6398593…`;
  - 0 worktree or index differences and 0 untracked or ignored files;
  - all 945 tracked non-gitlink blobs match by hash and mode;
  - the gitlinks for `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e` match their checkouts;
  - `external` `efeb541a` is uninitialized in this clone, as before.

R373-2 FINISHED
