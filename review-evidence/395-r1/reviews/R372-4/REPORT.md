[R372] POSITIVE - exact head 895be30712acf8dd80956a5b954690859b080d87

# R372-4: internal independent delta review of the dev merge on PR #605 (#395)

- **Head:** `895be30712acf8dd80956a5b954690859b080d87`, tree `aaf645102ef01bb0480f6bddd34e287fbd54bd9d`.
- **Parents:** `3b5603e3` (the branch; R372-3 and R373-3 POSITIVE) and `1fa2357f` (dev after #582/PR #596, #593/PR #601 and #75/PR #604).
- **Merge base:** `8bc97021`.
- **Scope:** the merge-dev assignment ([issue 395 comment 5866780445](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5866780445)) and its disposition ([5867242613](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5867242613)), under the frozen #395 items 1, 2 and 5. Items 3 and 4 are out of scope and stay open.
- **Method:** I worked in a cleared context from public state only: AGENTS/CONTRIBUTING, docs/README, the issue body and comments, the PR diff and history, the public evidence branch, and exact-head hosted check state. I read the prior public review findings on this PR only after my own pass (see "Prior public findings").

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses are covered clean at `895be307`. There is one SUGGESTION, which does not affect coverage, and one out-of-scope observation for triage.

## Assigned checks

### (1) The two conflict resolutions are exact

Evidence: `check_merge_structure.py` returns 21 of 21 checks, rc 0 (`receipts/merge-structure.log`).

- **Recomputation.** `git merge-tree --write-tree 3b5603e3 1fa2357f` conflicts in exactly `docs/findings/README.md` and `sw/builder/test_builder.py`. The recomputed tree differs from the published merge only in those two files.
- **`docs/findings/README.md:11-12`.** The merged file is dev's file plus one inserted row. The rows are exactly the union of both sides, with no duplicate, and each side's relative order is preserved.
  - Both new current records (`75_RECONNECT_RESTART_MEASUREMENT.md` and `COMMERCIAL_TIMING_395.md`) lead the seven unchanged base rows.
  - The index has no written ordering rule. Its observed convention is newest-first for current records, above the historical block.
  - Both new records state the same measurement date, 2026-09-27 (`75_RECONNECT_RESTART_MEASUREMENT.md:3`, `COMMERCIAL_TIMING_395.md:3`), so the convention allows either order. The resolution is consistent with it (see S1).
- **`sw/builder/test_builder.py:27557-27578`.** The merged file is dev's file plus exactly two changes:
  - the branch's `test_commercial_timing_grade` function (`:27557-27566`), byte-equal to the branch;
  - `test_commercial_timing_grade,` placed first in the `__main__` loop, as on the branch, with dev's four `test_clock_contract` entries re-flowed onto the next line (`:27578`).

  The loop has 91 entries, no duplicate, and is the union of both sides. Dev's import block (`:27569-27572`) and its gate-1b edit (`:17120-17124`) auto-merged unchanged.
- **No collision.** No gate number or name collides: neither `test_timing_grade.py` nor `test_clock_contract.py` prints a `[gate N]` label, and the function names are distinct. No renumbering was needed, and none was made.
- **No shadowing.** Execution order is harmless. `test_timing_grade` prepends `sw/litex` to `sys.path`. The only module names that overlap with what the later clock-contract tests import are `milan_soc` and `board_audio_routing`, which those tests deliberately load from `sw/litex`.

### (2) `milan_soc.py` merged cleanly, and the timing grade and corner reporting compose with #582's contract clock

**The merge side.** `sw/litex/milan_soc.py` is byte-equal to git's clean auto-merge. The two sides touch disjoint regions:

- the branch changed the PLL speed-grade derivation at `:229` and the comment at `:219-221`;
- dev added the recipe import at `:73`, the contract check at `:3707-3710` and help text.

**The author's corrected probe could not be re-run.** It is described in [A415 REVIEW READY 5867344551](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5867344551) and in the PR body's "Merge with dev" section. Its script and receipts were not on the public evidence branch `395-review-evidence` at 09:50Z; the latest commit there was the round-3 archive `de31170b`. Private author material is out of bounds for this review. This is recorded as a limit.

**My own probe.** `probe_composition.py`, run with the LiteX interpreter: every check passes, rc 0 (`receipts/probe_composition.log`). It runs the real `milan_soc.main()` for:

- each of the five tracked configurations' builder-emitted argv;
- the shipping `sweep.sh:48` AX7101 argv.

For each, it builds the real `_CRG` and stops elaboration there. Results:

- **Contract clock.** In all six runs, the effective Milan/CPU clock equals the recipe `CPU_HZ` (`tb/verilator/nvm_capture_cpu/recipe.py:5`, 50 MHz), which equals the builder's `BAREMETAL_CLK_HZ`, which equals the configured `milan_clk_hz`. The parsed system clock equals the configured `sys_clk_hz`:
  - 100 MHz on AX7101, where the argv omits it and the CLI default applies;
  - 83.333 MHz on Arty.

  `_CRG` receives exactly the parsed pair.
- **PLL plan on AX7101** (both configurations and the shipping argv). The real LiteX solver produces every requested output exactly, with margin 0: 100 MHz sys, 50 MHz Milan, 400/400/200 MHz. The VCO is 1.6 GHz, inside the S7PLL `speedgrade=-2` range derived from `TIMING_GRADE["part"]` (`milan_soc.py:229`, `:244`, `:265`). Vivado derives the reported generated clocks from these PLL outputs.
- **Hooks on AX7101.**
  - The platform part equals `TIMING_GRADE["part"]` (`alinx_ax7101.py:298`).
  - The pre-placement commands equal `configure_commands()` and carry no clock literal.
  - The first bitstream command is `kl_timing_grade_reports {build_name}_signoff` (`alinx_ax7101.py:305`).
  - The corner reports in `timing_grade.tcl` name no clock. They analyse whichever clocks the design constrains, so they derive from #582's contract clock through the PLL plan above.
- **Negative controls.** Each is refused with the named "baremetal clock" error before `_CRG` is reached:
  - N1: recipe clock patched to 40 MHz;
  - N2: shipping argv with `--milan-clk-freq 100e6`;
  - N3: shipping argv with `--milan-clk-freq 0`.
- **Positive control P1.** Changing the declared part to `-1` changes the PLL VCO range.

### (3) Nothing else changed beyond the merge

`receipts/merge-structure.log` checks this per path, three ways, over all 952 tree entries, including modes and gitlinks:

- every path changed only on dev equals dev;
- every path changed only on the branch equals the branch;
- every untouched path equals base;
- the only paths changed on both sides are the two conflict files and the cleanly auto-merged `milan_soc.py`.

The protocol-processor gitlink is `16be6768f710e79450aace277abacd6c2c3336e5`, which is dev's. Every artifact behind the branch's timing work is byte-identical to `3b5603e3` (`receipts/prior-findings-artifacts.txt`): the record, BUILDING, RUNNING_TESTS, LITEX_SOC, `test_timing_grade.py`, `timing_grade.tcl`, `report_timing_grade.py`, `ax7101_timing.py` and `alinx_ax7101.py`.

### (4) Gates at the merge head

**Run by this review at `895be307`, all rc 0** (`receipts/light-gates.json`, `receipts/gates/*.log`):

- `ci_scope.py --selftest`;
- `docs_check.py`, `check_doc_paths.py`, `gen_toc.py --check` and `check_em_dash.py --base` against both `8bc97021` and `1fa2357f`, all with the pinned Markdown environment `md-venv-40cdefe08ebd`;
- `check_feature_status.py --self-test`, `check_doc_style.py` and its `--selftest`, `check_solution_docs.py`, `check_py_idiom.py` and its `--selftest`;
- `check_baremetal_only.py --check`: 0 findings over 922 files;
- `check_baremetal_only.py --selftest`: 700 arms;
- `git diff --check` against base, dev and branch;
- pure report-script generation (`report_timing_grade.py` on a dummy input). The generated Tcl was inspected and not executed (`receipts/gates/report-script-generated.tcl`).

**Focused tests at the head, both rc 0:**

- `sw/builder/test_timing_grade.py <litex-python>`: three arms, including 19 wrong-condition refusals (`receipts/focused_test_timing_grade.log`);
- `sw/builder/test_clock_contract.py --soc`: all five arms (`receipts/focused_test_clock_contract.log`).

**Full builder banks.** Running them was outside this review's allowance. The executor's public receipts report `--require-rv32 --require-elaboration` rc 0 in 773.03 s and compiler-absent rc 0 in 571.68 s at this head ([5867228372](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5867228372) and [5867344551](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5867344551)). The manager's assignment states that its own source and native banks passed. Neither set of logs was on the public evidence branch at 09:50Z (see limits).

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R372-4-S1 - SUGGESTION - Docs - `docs/findings/README.md:7-19`

- **Evidence:** the index states no ordering rule. The merge assignment asked for "the index's own ordering rule", and that rule could only be inferred as newest-first from `397` and `117`. For the two new rows, both records carry the same measurement date. Their row-authoring and dev-landing orders point the other way from their file-creation order.
- **Impact:** none at this head. The present order is consistent with the observed convention. The next merge that meets the same situation will face the same unresolvable question.
- **Suggested outcome:** a one-line statement of the ordering key under "Current entries", for example "newest measurement date first; ties by landing order".
- **Verification:** `gen_toc --check` and `docs_check` still pass.

### Out-of-scope observation (not attributed to this PR; for manager triage)

**O1: the Arty clock plan does not solve.** Arty's configured `sys_clk_hz` is 83,333,000 (`configs/endstation_arty_*.yaml`, `sweep.sh:47`). `_CRG` requests every PLL output with `margin=0` (`milan_soc.py:244`). No 100 MHz-input S7PLL can produce that frequency exactly: it would need `100000 | d·D`, which is impossible within the divider ranges. The real solver raises "No PLL config found" (`receipts/probe_composition.log`, the three Arty OBSERVATION lines).

- **Why it is not attributed to this PR:** the `_CRG` Arty path and the Arty configurations are identical at base `8bc97021`, at the branch and at dev.
- **Why the builder bank passes:** gate 23g checks that each recipe reaches the Instance and does not finalise the PLL.
- **Status of Arty:** BUILDING `:629` calls the Arty recipe retired.

If Arty builds are still expected to run, this is new work for a separate issue. It does not affect #395 (AX7101 only) or this merge.

## Mutation and fault evidence

`run_mutations.sh` runs on fresh exports of the head, with the submodules linked read-only. Seven jobs ran in parallel, and the result is `unexpected=0` (`receipts/mutations/SUMMARY.txt`, with each log showing the intended assertion).

| ID | Planted fault | Expected | Observed |
|---|---|---|---|
| C0 | none (control): timing-grade test, clock-contract `--soc`, probe | pass | rc 0 ×3 |
| M1 | per-corner summary loses `min_max` (`timing_grade.tcl`) | timing-grade test fails | rc 1, report-content assertion |
| M2 | PLL speed grade restored to literal `-2` | timing-grade test and probe fail | rc 1 (changed-part control); probe P1 FAIL |
| M3 | corner-report hook dropped from the bitstream commands | timing-grade test and probe fail | rc 1 ×2 (hook assertion) |
| M4 | #582 contract check disabled in `milan_soc.main` | clock-contract `--soc` and probe fail | rc 1 ×2 (clock accepted; N2/N3 FAIL) |
| M5 | recipe `CPU_HZ` changed to 40 MHz | probe fails; timing-grade test unaffected | probe rc 1 (builder refusal); timing-grade rc 0 |
| M6 | declared junction maximum changed to 100 °C | timing-grade test fails | rc 1 (declaration oracle) |

## Prior public findings (read after my own pass)

| Finding | Status at `895be307` | Evidence |
|---|---|---|
| R372-1 F1 (MAJOR; Conformance, RTL, Docs), rejected crossing constraints | Resolved (round 2/3); unchanged | Record blob `9e77d714` equals `3b5603e3` |
| R372-1 F2 (MINOR; Tests), surviving planted faults | Resolved; unchanged | `test_timing_grade.py` blob equal; M1, M3 and M6 killed here |
| R372-1 F3 (MINOR; Conformance, Docs), margin decision | Resolved; unchanged | Record, BUILDING and RUNNING_TESTS blobs equal |
| R373-1 F1 (MINOR; Conformance, Docs), cause of the unsafe pairs | Resolved; unchanged | Record blob equal |
| R372-2-F1 = R373-2 R2-F1 (BLOCKER; Docs, Tests), bare-metal gate | Resolved; re-verified | `check_baremetal_only.py --check` rc 0 (0 findings) and `--selftest` rc 0 at this head. The hosted `docs-check` was still in progress at 09:50Z |
| R372-2 S1–S4, R372-1 S4 | Resolved; unchanged | Artifacts byte-equal (`receipts/prior-findings-artifacts.txt`) |
| R372-3 S1–S4 and R373-3 S1–S4 | Retained as SUGGESTIONs | The files involved are unchanged by the merge |
| Older retained SUGGESTIONs (R372-1 S1–S3; R373-1 S3–S6; R373-2 S-A–S-D) | Retained as SUGGESTIONs | `timing_grade.tcl` and `report_timing_grade.py` are unchanged. `test_builder.py`'s shared LiteX skip text (`:27562`) is unchanged by the resolution |

None of the retained items is a MINOR or above.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merge rules 1–3 of 5866780445 and disposition 5867242613, checked against `receipts/merge-structure.log` (the two resolutions and the `milan_soc.py` auto-merge). #395 items 1, 2 and 5: the part, conditions and corner hooks derive from `ax7101_timing.py` and are unchanged, and `probe_composition.py` shows the grade and hooks composing with the #582 contract clock (`milan_soc.py:73`, `:229`, `:3707-3710`; `recipe.py:5`) | R372-4 | `895be307` |
| RTL | CLEAN | `milan_soc.py:216-265` `_CRG` PLL plan: exact 100/50/400/400/200 MHz at VCO 1.6 GHz within the -2 range, speed grade from the declared part. Contract refusal `:3707-3710`. HDL, generated headers, `rom_digests.tsv` and the PP gitlink in the merge delta are byte-equal to dev (`receipts/merge-delta-files.txt`, `merge-structure.log`). `timing_grade.tcl` is unchanged | R372-4 | `895be307` |
| Robustness | CLEAN | Negative controls N1–N3 are refused before `_CRG`. The M1–M6 fault campaign has `unexpected=0`. The report-failure restore arm of `test_timing_grade.py` passes. Resolution ordering and `sys.path` shadowing were checked (`test_builder.py:27557-27578`). The out-of-scope Arty plan (O1) is identical at base | R372-4 | `895be307` |
| Tests | CLEAN | `test_builder.py:27557-27566` and `:27577-27578`: exact union, no duplicate or collision. Standalone `test_timing_grade.py` and `test_clock_contract.py --soc` rc 0. Mutants show both merged entries bite (M1–M4, M6). Light gate set rc 0 (`receipts/light-gates.json`) | R372-4 | `895be307` |
| Docs | CLEAN | `docs/findings/README.md:11-12`, an exact ordered union. The record, BUILDING, RUNNING_TESTS and LITEX_SOC are byte-equal to `3b5603e3`. The record's `milan_soc.py` line citations are pinned at `66001a30`, and its "100 MHz system and 50 MHz fabric" matches `CPU_HZ`. `docs_check`, doc-paths, TOC and em-dash (vs base and dev) rc 0 in the pinned Markdown environment. The PR body's "Merge with dev" section matches the probe results. S1 is a SUGGESTION only | R372-4 | `895be307` |

Every lens is covered clean at the merge candidate `895be307`, with no BLOCKER, MAJOR or MINOR open under any lens.

## Real limits

- **Full builder banks.** Running them was outside this review's allowance. For both banks I rely on the executor's public receipts and the manager's statement. Their logs were not on the public evidence branch at 09:50Z.
- **The author's corrected composition probe** was not public, so it could not be re-run. My own probe replaces it: it covers the same questions plus the shipping `sweep.sh` argv and controls.
- **No Vivado run.** No routed-timing, synthesis or implementation run was made. The corner numbers in the record concern the fixed `9e9954e9` checkpoint and were not re-measured; the merge does not change that checkpoint or its record. The merged dev tree has no routed candidate in this lane.
- **Verilator** was not used: the PR-owned delta has no RTL, and dev's RTL is byte-equal to dev.
- **Hosted checks were incomplete** at 09:50Z (`receipts/hosted-check-runs.tsv`):
  - completed with success: `rtl-fast`, `yosys-elaboration`, the four Yosys shards, Verilator shards 0 and 3, `verilator-lint`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `changes` and `full-ci-gate`;
  - still in progress: `docs-check`, `elaborate`, and Verilator shards 1, 2 and 4;
  - skipped: Physical gPTP, which is not hardware evidence.
- **Physical evidence.** Physical calibration was not run, and field skips are not hardware proof. Items 3 and 4 remain open.

## Pending manager duties

- Publish the merge-round executor packet: the corrected probe, the gate table and both builder-bank logs. Publish the manager's own bank receipts for `895be307`.
- Hosted exact-head completion (`docs-check`, `elaborate`, Verilator shards 1, 2 and 4), the act replica, the final current-dev candidate build and validation, the composition review, and merge authorisation. The PR remains "Relates to #395"; items 3 and 4 stay open.
- Optionally triage O1 (Arty clock plan) and S1 (the findings-index ordering rule) as follow-ups.

## Receipts and reproduction

The packet contains the scripts (portable; paths are arguments):

- `check_merge_structure.py <repo>`
- `probe_composition.py <repo>`, run with the LiteX interpreter
- `run_light_gates.py <repo> <md-python> <litex-python> <packet>`
- `run_mutations.sh <repo> <litex-python> <packet>`

Receipts are under `receipts/`, and every published file is listed in `MANIFEST.sha256`. After the probes, the clone was restored and verified (`receipts/restore-verification.txt`):

- HEAD and tree are exact;
- status, including ignored files, is empty;
- index entries (mode, blob, path) equal the HEAD tree for all 952 entries;
- all 948 regular files re-hash to their index blobs, with modes matching;
- the four gitlinks are unchanged, and the initialised submodule worktrees are clean at their gitlinks.

R372-4 FINISHED
