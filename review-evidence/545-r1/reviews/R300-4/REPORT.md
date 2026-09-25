[R300] POSITIVE - exact head ddf8151c478fc54c98608589c1afe9525739d6a4

# R300-4: internal independent delta review of #545 / PR #563 (second merge-dev round)

- **Head:** `ddf8151c478fc54c98608589c1afe9525739d6a4`, tree `ea8460263670d159ab4c79005bd57de7d2326041`.
- **Shape:** a merge of dev `5c78ce2e9d831e588e759b696ed549804327e4d8` (#443 and #562 merged) into the reviewed head `4538d7c03dc4f56d7ed4c971603e15bda82050a8`.
- **Delta judged:** `92ad1687..ddf8151c`, where my R300-3 is POSITIVE at `92ad1687`. That range covers:
  - the first merge `b376f611`;
  - the docs round `4538d7c0`;
  - this merge `ddf8151c`.
- **Scope, reconstructed from public state:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - The #545 body.
  - Decisions and assignments 5816509756, 5827358783, 5828714628, 5830332403, 5831902801, 5833028966 and 5835673886 (this round: merge dev `5c78ce2e`, keep both sides in `CHANGELOG.md` and `scripts/measure_test_evidence.py`, change nothing else).
  - The [A320] REVIEW READY comment 5836177064.
  - The public evidence at `dddb8121:review-evidence/545-r1/author-r6`.
  - Exact-head hosted check runs.
- **Order:** I read prior public review findings only after my own pass over the diff and my own runs.
- **Verdict: POSITIVE.**
  - No BLOCKER, MAJOR or MINOR finding.
  - The merge resolution is confined to the two assigned files and keeps both sides.
  - Both parents' content is carried byte-for-byte in changed lines.
  - The #443 render-status path and the #545 slew path elaborate and pass together.
  - Two new SUGGESTIONs are recorded. Neither affects coverage.

## 1. Merge resolution (`git show --remerge-diff ddf8151c`)

The remerge diff (`receipts/remerge_diff_ddf8151c.txt`) touches exactly two paths, `CHANGELOG.md` and `scripts/measure_test_evidence.py`. Both are the conflicts the assignment names.

- **`CHANGELOG.md`:**
  - Both contents rows are kept at `:10-11`.
  - Both sections are kept: `## Unreleased - CRF servo holds through PHC slew` at `:33` and `## Unreleased - render setpoint state` at `:47`, separated by one blank line.
  - No text in either section was changed.
- **`scripts/measure_test_evidence.py`:**
  - The #545 `gmstep_mutants.py` disposition is kept at `:634-637`. The #443 `render_csr_controls.py` disposition is kept at `:638-642`.
  - Dev's stale "plants all eleven" wording was dropped. That is the correct side: the lane's text supersedes it, and the evidence reader's self-test agrees.
  - The `slew_mutants.py` disposition at `:597-602` names all eight defects. It matches `MUTANTS` plus `STREAK_MUTANTS` in `tb/verilator/mmcm_servo/slew_mutants.py`.
- **Carry equality** (`receipts/merge_side_equality.txt`):
  - For every file each side changed, the changed-line content is identical. The comparison is dev side `864b36f5..5c78ce2e` against `4538d7c0..ddf8151c`, and lane side `864b36f5..4538d7c0` against `5c78ce2e..ddf8151c`.
  - 58/58 files are SAME and 0 are DIFF.
  - The PR's net delta against the new dev is the same 38 files, +686/-56, as against the old dev (`receipts/pr_net_stat_5c78ce2e_ddf8151c.txt`).
- **Files both sides touch:** `CHANGELOG.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md`, `milan_datapath.sv`, `measure_test_evidence.py` and `milan_dp/README.md`. All hunks are disjoint, and git resolved them cleanly except the two conflicts above.
- **First merge `b376f611`:** its remerge diff (`receipts/remerge_diff_b376f611.txt`) is confined to the documentation, diagram and manifest paths its assignment named. The same carry-equality holds at this head.
  - `check_submodule_docs.py` reports 4 exact gitlinks.
  - `check_diagram_pngs.py` reports 6 source-bound PNGs.
  - The gitlinks are gPTP `5dce647a` and processor `990f9652`, as decided.
- **Docs round `4538d7c0`:**
  - README `:593-600` says fourteen controls: eleven tabulated plus three #545. That matches `CONTROLS` in `gmstep_mutants.py` (14 entries), and the executed campaign planted 14 controls.
  - The disposition string names eight defects.

## 2. Semantic interaction of dev (#443 and #562) with this PR

- **RTL, `hdl/milan/milan_datapath.sv`:**
  - The #443 hunks are the declaration `render_status_w` at `:1202`, the CSR port `:2591` and `g_render_status` at `:6180`.
  - The #545 hunks are the declaration `gptp_slew_active_w` at `:1464`, `slew_rate_alignment` at `:2766-2770`, the servo port at `:5569`, the shadow port at `:6958` and the tie-off at `:7050`.
  - The two sets share no signal, and both are declared before use.
  - `RENDER_STAT` `0x8DC` (`milan_csr.sv:922`) does not collide with `MCSRV_STAT` `0x8F8` (`:899`).
  - Both elaborations were built with Verilator 5.050 and pass:
    - gPTP off (the #443 `aclk` leg, which uses the tie-off branch): 190 checks, including `RENDER-CSR`.
    - gPTP on (the `gmstep` leg, with the real plane driving the slew level): 58 checks.
- **#562 (`KL_crf_rx`, comment-only RTL; new `crf_rx` checks and mutants that copy the servo):**
  - `crf_rx` passes at this head with the #545 servo: 13,836 unit, 2,201 discontinuity and 69 connected checks.
  - Its campaign passes 10/10, including #562's `validation_error_unlocks` and `validation_error_refreshes_timeout` and the servo-validity controls. Every servo anchor still matches exactly once.
- **Instantiations:** every `KL_mmcm_drp_servo` instance connects `phc_slew_active_i`: `milan_datapath.sv`, `rails_wrap.sv` and `crf_talker_wrap.sv`. The remaining hits in `KL_media_nco.sv` and `KL_media_grid_align.sv` are comments.
- **Docs:** #443's `TIME_SYNC.md` RENDER_STAT block, `REGISTER_MAP.md` `0x8DC` section and `TESTING.md` `render-csr-controls` row sit beside the #545 text without contradiction. The TOC, anchor and em-dash gates pass on the merged pages.

## 3. Executed evidence at this head

Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`) was used; CI pins `VERILATOR_VERSION: v5.050`. All commands ran foreground-supervised, with two streams of at most 4 CPUs each (8 total). Raw logs are under `receipts/`.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/mmcm_servo` (clean build, default target) | rc 0, 801.8 s on 4 CPUs. Unit 100/0, rails 8/0, step 113/0, slew 90/0 | `sim/A_2_servo_default.log` |
| `make -C tb/verilator/mmcm_servo slew-mutants` | rc 0, 10/0. Both positive controls pass. All 8 defects fail their named check (`[S1]` x4, `[S5]`, `[U15]` x3) | `sim/A_3_servo_slew_mutants.log` |
| `make -C tb/verilator/crf_rx` (run + mutants) | rc 0. Counts as in section 2 | `sim/A_4_crf_rx_default.log` |
| `make -C tb/verilator/milan_dp aclk` (#443 leg) | rc 0, 190/0 | `sim/B_1_dp_aclk.log` |
| `make -C tb/verilator/milan_dp render-csr-controls` | rc 0, 4 checks, 0 failures | `sim/B_2_dp_render_csr_controls.log` |
| `make -C tb/verilator/milan_dp gmstep-mutants` (the leg, then `--all`) | rc 0. The leg passes 58/0, then 16/16: 2 positive controls and 14 controls, each breaking its named check | `sim/B_3_dp_gmstep_mutants_all.log` |
| `python3 gmstep_mutants.py --slew` | rc 0, 4/4: the positive control and 3 slew controls | `sim/B_4_dp_gmstep_mutants_slew.log` |
| `measure_test_evidence.py --check` / `--selftest` | rc 0 / rc 0 (101/101). The ratchet passes | `static/measure_test_evidence_*.txt` |
| `docs_check.py`, with Git and on a Git-free `git archive` extraction | rc 0 / rc 0, 0 findings. The no-Git mode skips only inventory parity | `static/docs_check_git*.txt`, `static/docs_check_nogit.txt` |
| `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base 5c78ce2e` | rc 0 each (176 anchors; 0 em-dash findings, 339/339 arms), run with the hash-pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1) | `static/gen_toc_*.txt`, `static/check_em_dash_base_dev.txt`, `static/md_renderer_identity.txt` |
| `check_doc_style`, `check_doc_paths`, `check_py_idiom`, `check_cpp_idiom`, `check_sv_idiom`, `check_rtl_source_lists`, `check_port_contracts`, `lint_rtl --check`, `check_submodule_docs`, `check_diagram_pngs`, `git diff --check 5c78ce2e HEAD` | rc 0 each. Lint 90 ≤ ratchet 90 | `static/*.txt` |
| Restore proof | Head, tree and index tree equal. 0 tracked byte/mode mismatches. Gitlinks match with clean submodules, and there are 0 untracked or ignored entries | `verify_restore.txt` |

## 4. Findings

No BLOCKER, MAJOR or MINOR.

### R300-4 S1 SUGGESTION: Docs, Tests. `tb/verilator/milan_dp/README.md:570` still says the gmstep leg "passes 48 of 48"

- **Evidence:** at this head the leg reports `== gmstep: checks: 58   failures: 0 ==` (`sim/B_3_dp_gmstep_mutants_all.log:536`). The ten additional checks are the #545 `slew path:` checks, which the README describes at `:1019-1026` without a count.
- **Why only a SUGGESTION:** the sentence is the before-and-after figure for the #387 datapath edit ("passed 44 of its 48 ... With the edit it passes 48 of 48"). No gate, control or inventory derives from it. It is outside this round's delta and is the same family as R301-4 S1.
- **Required outcome (optional):** date the figure to #387, or add "58 with the #545 slew phase".
- **Verification:** the README figure matches the leg's summary line.

### R300-4 S2 SUGGESTION: Docs, RTL. `hdl/ieee1722/crf/KL_media_nco.sv:43,147` cites `KL_mmcm_drp_servo.sv:604` for the "u > 0 = speed up" convention

- **Evidence:**
  - The convention is at `KL_mmcm_drp_servo.sv:737` at this head (also stated at `:108`).
  - It was already at `:693` on dev `5c78ce2e` and `864b36f5`, so the citation was stale before this PR. The PR's servo additions move it further.
- **Impact:** a reader following the sign-convention pointer lands on unrelated code. The sign itself is unchanged and is pinned by tests.
- **Required outcome (optional; pre-existing, so a separate Issue):** cite the symbol or comment, not a line number.
- **Verification:** the cited location states the convention.

## 5. Prior public findings on this PR, resolved or retained at this head

| Finding | Severity | Status at `ddf8151c` | Evidence |
|---|---|---|---|
| R300-1 F1 / R301-1 F1 (default servo target over budget) | MAJOR | Resolved | Mutants run behind `slew-mutants`. The default target keeps 100/8/113/90. Local run: 801.8 s on 4 CPUs. The hosted `verilator-suites` at this head passed |
| R300-1 F2 / R301-1 F2 (coincident step+slew dedupe untested) | MINOR | Resolved | `[S5]` passes, and `step_dedupe_removed` fails on `[S5]` at this head |
| R300-1 F3 (TESTING index stale) | MINOR | Resolved | `TESTING.md` campaign rows match the executed inventories (8 defects + 2 controls; 12 + 2 datapath controls) |
| R301-1 F3 / R300-1 S1 (tail oracle copied the RTL) | MINOR / SUGGESTION | Resolved | `the policy level misses an extra addend stage` is caught at this head |
| R301-1 S1 (slew streak reset uncontracted) | SUGGESTION | Resolved | Stated, and pinned by U15 and three controls, all killed here |
| R300-2 F4 (U15 blind to counting variants) | MINOR | Resolved | `slew_discard_extends_streak` and `slew_discard_counts_as_guard_trip` both fail `[U15]` here |
| R300-2 F5 (1800 s basis) | MINOR | Resolved | The `CI_WORKFLOWS.md` `mmcm_servo` row is unchanged since R300-3 |
| R301-2 S-A (tail oracle one-sided) | SUGGESTION | Retained, open | `sim_gmstep.cpp` is unchanged since `92ad1687`. Routed to #495 |
| R301-2 S-B / S-C | SUGGESTION | Resolved | Unchanged since R300-3 |
| R300-3 S1 (U15 blind to a level-gated streak reset on sub-window slews) | SUGGESTION | Retained, open | `sim_main.cpp` and the servo RTL are unchanged `92ad1687..ddf8151c` |
| R300-3 S2 = R301-3 S1 (disposition six-for-eight) | SUGGESTION | Resolved | `measure_test_evidence.py:597-602` names eight, kept through the merge |
| R301-3 F1 (README "all eleven") | MINOR | Resolved | `README.md:593-600` says fourteen, and `CONTROLS` has 14 entries, all planted here |
| R301-4 S1 (dated "eleven" at README `:621`, `:865`) | SUGGESTION | Retained, open | Both lines are unchanged. They are dated records |

## 6. Per-lens results

```text
[R300] PASS Conformance - remerge_diff_ddf8151c.txt; merge_side_equality.txt; CHANGELOG.md:10-11,33,47; measure_test_evidence.py:597-602,634-642 - assignment 5835673886 (merge 5c78ce2e, keep both, change nothing else) met: remerge confined to the two named files, 58/58 side-equal; #545 acceptance (5827358783 items 1-6) content unchanged since R300-3, and its executable arms re-pass here (100/8/113/90, 10/10, 58 + 16/16)
[R300] PASS RTL - milan_datapath.sv:1202,1464,2591,2766-2770,5569,6180,6958,7050; milan_csr.sv:899,922 - #443 render-status and #545 slew hunks disjoint; gPTP-on and gPTP-off elaborations build and pass on 5.050; lint 90<=90, port contracts, source lists and SV idiom OK; servo RTL unchanged 92ad1687..ddf8151c
[R300] PASS Robustness - sim/A_2 (slew S1-S5, U15, reset, saturation, prolonged level), sim/B_1 (gPTP-absent tie-off leg 190/0), sim/A_4 (#562 validation-error lock retention with #545 servo) - boundary, reset, feature-off and validation-error paths pass at the merged head
[R300] PASS Tests - slew_mutants.py 8/8 defects killed by named checks; gmstep_mutants.py 14/14 controls; render_csr_controls.py 4/0; crf_rx mutants 10/10 incl. #562 controls; measure_test_evidence --check/--selftest (101/101) - every campaign can still fail at the merged head; S1 recorded
[R300] PASS Docs - CHANGELOG.md:10-11,33-55; milan_dp/README.md:589-600; TESTING.md campaign rows; REGISTER_MAP.md 0x8DC/0x8F8 rows; TIME_SYNC.md; docs_check both modes, gen_toc --check/--verify-anchors, em-dash vs 5c78ce2e, doc style/paths, submodule docs, diagram PNGs - all rc 0; S1 and S2 are SUGGESTIONs only
```

## 7. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The merge resolution against assignment 5835673886; carry equality; #545 acceptance arms re-executed | R300-4 | `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| RTL | CLEAN | Merged `milan_datapath.sv` #443/#545 hunks; `milan_csr.sv` decode; both elaborations; lint/port/source-list/idiom gates | R300-4 | `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| Robustness | CLEAN (retained SUGGESTIONs R300-3 S1 and R301-2 S-A only) | Servo slew and boundary cases; gPTP-absent tie-off leg; #562 validation-error paths with the #545 servo | R300-4 | `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| Tests | CLEAN (R300-4 S1 SUGGESTION only) | `slew-mutants`, `gmstep-mutants --all` and `--slew`, `render-csr-controls`, `crf_rx` mutants; evidence-reader check and self-test | R300-4 | `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| Docs | CLEAN (R300-4 S1, S2 and R301-4 S1 SUGGESTIONs only) | CHANGELOG, README, TESTING, REGISTER_MAP, TIME_SYNC, SUBMODULES and diagrams; all documentation gates in both modes | R300-4 | `ddf8151c478fc54c98608589c1afe9525739d6a4` |

All five lenses are covered at the merge candidate itself, so no ancestor-coverage argument is needed.

## 8. Limits

- **Verilator:** the assigned 5.050 wrapper path was absent on this host. I used the host's shared v5.050 install, and its `--version` output is recorded in each simulation log. It matches the version CI pins.
- **Markdown renderer:** the default interpreter lacks the hash-pinned renderer. `gen_toc` and `check_em_dash` therefore refuse (rc 2) under it. Their passing receipts come from an existing environment whose `cmarkgfm`, `html5lib` and `cffi` versions match `tools/markdown/requirements.txt`. The renderer module refuses any other release.
- **Not run by me, and not permitted in this round:**
  - the full default `milan_dp` sweep (only the `aclk`, `gmstep` and campaign targets ran);
  - the `gptp_shadow` suite, which is unchanged since `92ad1687`;
  - builder, behave, Yosys/OOC area, parent/PP/gPTP banks, and Docker/act.

  For these I rely on the manager's public source-bank evidence at this head and on the hosted runs.
- **Hardware:** physical calibration was NOT RUN, and the builder calibration arm is absent. Simulation and field skips are not hardware proof.
- **Hosted snapshot** (`receipts/hosted_check_runs_ddf8151c.tsv`, 17:49 UTC):
  - `rtl-fast`, `verilator-suites` (5 shards), `yosys-portability` (4 shards), `elaborate`, `yosys-elaboration`, `docs-check`, `verilator-lint`, `bdd-conformance` and `wire-accountability` completed with success.
  - `Physical gPTP (nightly and manual)` was skipped, which is not execution.
  - `docs-check-no-git` reported status `in_progress` with conclusion `success` at the snapshot.
- **Command count:** the executor's count of default datapath commands (33, versus 34 in the first merge round) is an executor chunking artifact that I did not re-derive. The `milan_dp` `run` recipe is unchanged by #443 and by this PR.

## 9. Pending manager duties

- Build and gate the final current-dev candidate at merge time. The source base and live dev are both `5c78ce2e9d831e588e759b696ed549804327e4d8`, so the head tree is the candidate tree if dev has not moved.
- Own hosted and act acceptance. Confirm the final state of `docs-check-no-git`.
- Decide routing of the SUGGESTIONs: R300-4 S1 and S2, R300-3 S1, R301-2 S-A (#495) and R301-4 S1.
- Run post-merge containment and merge-review integrity as CONTRIBUTING step 7 requires. A merge needs explicit maintainer authorization.

R300-4 FINISHED
