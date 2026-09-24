# [A270] handoff: PR #555 (issue #387, acceptance 3), round 2

Status: DONE. REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819357818. Nothing pushed; the PR body is proposed in `PR-BODY.md`.

| Item | Value |
|---|---|
| Assignment | https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5818091077 |
| Branch / worktree | `387-media-rebase`, `$LANES/387-media-rebase`, local only |
| Start head | `a9636e0f670f90f411da3024a141e93efa1872df` |
| Final head | `a21cd3585abdd3cdf4ac5774a048361a66fed043`, tree `5376deee90b2e0732f533f287daaf7dfc666f32e` |
| Worktree | clean; submodules at their pins (`receipts/final-status.txt`) |
| Toolchain | Verilator 5.050 (`$VALIDATION_TOOLS/verilator-v5.050` for suites and probes; the manager's `pinned-tool-bin` for the builder), eight build jobs |

## Inputs read

- Assignment and ruling 5818091077; ruling 5802264260.
- R276-4 (PR #555 comment 5817943136) and R277-3 (comment 5818080648), with their probes and receipts from `387b-review-evidence` at `07f82c38` / `4e03acb7`, fetched read-only into /tmp scratch (deleted afterwards).
- Predecessor handoffs on that branch: author (A256), author-merge (A268), author-r1b (A269).

## Commits (one-line subjects, no body, no trailers)

| Commit | Subject |
|---|---|
| `d5dc47c0` | End a pending mr restart at the first PDU carrying the adopted level, graded by tkdiag T17 and T18 and four engine mutants |
| `94e5ae74` | Grade a software settime as one mr toggle and one MEDIA_RESET in the option-off leg, with its planted control and a source-gated one |
| `018329b1` | Name the #387 re-centre triggers in the KL_render_setpoint banner and port spec |
| `c14f96ed` | Record the wire boundary, the settime evidence and the measured milan_dp margin in the design, test and CI pages |
| `a21cd358` | Record the eleven-control gmstep campaign time in the milan_dp README |

The `milan_dp` sweep and `gmstep-mutants` ran at `c14f96ed`. `git diff c14f96ed a21cd358` is one README timing line (the measured campaign time). Every other gate and probe ran at `a21cd358`.

## Items of the assignment

1. **Wire boundary** (R276-4 F2 = R277-3 F3). `KL_media_clock_restart.sv:230` keeps the merge line byte-exact, so R276's probe and the existing mutant anchors still apply. `:236-238` adds the wire boundary: on a request, a streaming talker with `hold_r == 0`, meaning it has adopted a level no reported PDU has carried yet, keeps that level as its target. The request merges. The merge is gated on the request, so a direct `tgt_r` poke (`sim_nxn.cpp` q2) is not undone.
   - The banner (`:55-92`) states the boundary and where "gone out" is measured. That is the transmitted-PDU feed, the one the hold and MEDIA_RESET count. It also names the residue: a request between the first PDU's launch and its report still merges.
   - tkdiag T17: the step now lands one observation interval after talker 0's adoption, with no PDU at that level. Talker 0 expects one toggle and one count. T18 (new, 6 checks) grades the other side: after one PDU at the adopted level the step is a second toggle, counted twice, while talker 1 (in its hold) merges.
   - T12 and T15: talker 1 sends one PDU at its adopted level before the second request, so their per-stream-hold checks still grade a hold. Expected values are unchanged.
   - `mcr_mutants.py` has four mutants. The shared-target mutant is re-pointed at T18. The new ones are the window ending at the adoption (the `a9636e0f` engine) and the window open for the whole hold.
   - GM_LOSS_RECOVERY row 157, the README bullet, TESTING.md, CHANGELOG and the PR text state the wire boundary.
2. **settime** (R277-3 F2). `sim_main.cpp:1028-1072`: after the leg's software settime, one check grades that the post-holdover frame's `mr` toggled once more (parity), and one that MEDIA_RESET (read at `talker_diag.mreset_r[0]`) counted it once. A 4096-cycle settle before and after closes the counter intervals.
   - The planted control `settime_no_mr` and the source-gated one (R277's `step_gated_by_source`) are in `gmstep_mutants.py`'s new option-off leg, built with `make option-off-build OPTOFF_MDIR= DP_SRC=`. They run in the explicit `gmstep-mutants` campaign.
3. **Render stage** (R276-4 F3 = R277-3 F4). `KL_render_setpoint.sv` banner `:81-89` and port spec `:169-173`. Comment only.
4. **Margin** (R276-4 F4). Hosted shard 4/5 at `a9636e0f` (job 107720800104, candidate merge `1e3a115` onto `57456af9`) measured the `milan_dp` window at 2264.9 s, 9775 checks (`receipts/hosted-milan_dp-window.txt`). That leaves 435 s (16%) of 2700 s. The window on dev was 2133.3 s (`57456af9`) and 2099.5 s (`59b81670`), both from R276-4's receipt.
   - `CI_WORKFLOWS.md` records these beside the unchanged budget. The PR's Known limitations states the margin from them.
   - Round 2 adds no elaboration to the sweep; the local sweep took 1339 s.
5. **Suggestions.**
   - R276-4 S1 and R277-3 S2 (PR status): in `PR-BODY.md`.
   - R277-3 S1 (record the measurement beside the budget): `CI_WORKFLOWS.md`.
   - R277-3 S3 (cite the INTERNAL-source evidence): GM_LOSS_RECOVERY `mr` and MEDIA_RESET rows.
   - R276-4 S2 = R277-3 S4 (stale clean binary): both runners rebuild a clean binary older than its recipe's inputs and say so.

## Open decision (published in REVIEW READY and PR-BODY decision 1)

R277-3's property probe, run unchanged, gives D3/D4 = 1 and P2-P4 clean over seeds 1-6, but **P1 is not clean**: 10 requests over seeds 2, 3, 5 and 6.

- A print-only copy of the probe places every one 0-3 cycles after the first launch at the adopted level (`receipts/probes/r277-mcr-prop-diagnostic-head.log`, diff `r277-mcr-prop-diagnostic-print-only.diff`). The probe reports completions LAT = 3 cycles after the launch it grades P1 against.
- No engine with the existing ports can meet both D3/D4 = 1 and P1 in that model, because the engine's inputs at such a request equal those at D3.
- Measured before implementing: R276's own wire-boundary engine gives the identical P1 result.
- Two ways to close it:
  - (a) rule the feed report as "launched" (implemented);
  - (b) add launch strobes from `KL_aaf_packetizer` (grant, `:616`) and `KL_crf_tx` (`:502`) as new engine ports, and the probe drives them.
- The assignment's "P1-P4 stay clean" is therefore NOT met for P1.

## Reviewer probes and mutants, re-run unchanged (`receipts/probes/`)

| Probe | Result at `a21cd358` | Before |
|---|---|---|
| R276 `probe_pending_boundary.sh` | tkdiag 96/96: its wire-boundary engine gives talker 0 one toggle and one count | failed T17's two talker-0 checks |
| R276 `probe_step_gated_by_crf.sh` (build, run) | killed: 233 checks, 2 failures (the adjtime parity check and the new MEDIA_RESET check) | killed, 231/1 |
| R276 `probe_builder_render_pin.sh` | not run: it clones three checkouts (not allowed in this round) at the old head. Its verification command `test_firmware_compiler.py --absent` exits 0, and both builder banks pass | reproduced F1 |
| R277 `mcr_prop` head, seeds 1-6 | D3 pending=0, D4 = 1; P2-P4 clean; P1 = 0, 2, 1, 0, 1, 6 | D3/D4 = 2 |
| R277 `mcr_prop` dev `57456af9` engine | killed: P1 = 21, P4 = 21 | the same |
| R277 `mcr_prop` previous head `a9636e0f` engine | D3/D4 = 2 (adoption boundary), 8/8 | (contrast) |
| R277 `plant.py settime_no_mr`, option-off leg | killed: 233 checks, 2 failures | survived, 231/0 |
| R277 `plant.py adjtime_no_mr`, option-off leg | killed: 2 failures | killed |
| R277 `plant.py step_gated_by_source`, option-off leg | killed: 2 failures | killed |
| R277 `plant.py settime_no_mr`, gmstep leg | survives 48/0: the gmstep scenario issues no settime, and the option-off leg kills it | survived |
| R277 `builder_pin_probe.py` | refuses: "anchor count 0 != 1". The pre-#387 text it re-points was already replaced by `[A269]`; both builder banks pass | re-pointed |
| tkdiag against the `a9636e0f` engine | fails exactly T17's two talker-0 checks | (contrast) |
| tkdiag against the dev engine | fails 6: T17 and T18 talker 1, T17 talker 0 | (contrast) |

R277's `run_optoff.sh` and `run_gmstep_probe.sh` wrappers were not run as-is. They `cp -a` a whole tree, and the build's `scripts/pp_srcs.py` needs git metadata, so only a checkout copy would build. `plant.py` ran unchanged into a scratch copy of the one file it plants. The suite's own recipe (`option-off-build`, `gmstep-build` with `DP_SRC`) built it, which is the recipe those wrappers invoke through `make option-off` / `make gmstep`.

Every previously killed mutant still dies:
- all gmstep controls, 9 + 2 new (`receipts/gmstep-mutants-all.log`);
- the render mutants, 6/6 (sweep);
- the tkdiag mutants, 2 + 2 new;
- the builder's mutation loops, 224/224 and 189/189;
- R276's CRF-gating probe, and R277's adjtime and source probes;
- the dev engine under the property probe.

## Gates (all rc 0, never piped; `receipts/<label>.json` has command, cwd, PATH, rc, seconds, log hash)

| Gate | Result | Receipt |
|---|---|---|
| `milan_dp` default `run`, 47 recipe commands in 6 chunks from `make clean` | all rc 0; 9781 checks, 0 failures; `log_reports_failure` none; 1338.8 s | `receipts/sweep/` (`run-recipe.txt`, `sweep-state.txt`, `sweep.log`, `sweep-tally.json`) |
| of which gmstep | 48/48; toggle at step +116 | sweep |
| of which obj_dir, obj_nolpf, obj_ax1x1 | 233/0, 233/0, 230/0 | sweep |
| of which render_mutants, gmstep_mutants (sweep subset) | 6/6, 4/4 (133 s) | sweep |
| `make gmstep-mutants` | 13/13 (2 positive + 11 controls), 404.9 s | `gmstep-mutants-all` |
| `make -C tb/verilator/tkdiag` from clean | 96/96; mutants 5/5 | `tkdiag` |
| full builder, pinned SDK (the manager's wrapper, argv-receipt path changed) | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 report); 224/224 mutations; 53/53 variants; 239 SDK invocations | `builder-sdk`, `full-builder-sdk.py`, `full-builder-sdk-argv.jsonl` |
| full builder, no compiler (sitecustomize control) | ALL GATES PASS EXCEPT 2 NOT RUN (gate 11, gate 1b instruments); 189/189; 53/53; 3 candidates absent | `builder-no-compiler`, `compiler-absent-sitecustomize.py`, `full-builder-absent-argv.jsonl` |
| `docs_check.py` git / no-git (`git archive` export in /tmp), `check_feature_status.py` no-git | 0 findings each | `docs-check`, `docs-check-no-git`, `feature-status-no-git` |
| `check_em_dash --base 57456af9` | 0 findings, 128 added lines, 8 pages | `em-dash` |
| `check_doc_style`, `gen_toc --check`, `check_doc_paths` | OK (22 docs), OK (107 pages), OK (841 paths) | |
| `gen_module_matrix.py --check` | up to date, 69 modules | `module-matrix` |
| `xvlog_gate --check` | PASS, 4 == ratchet, 0 hdl/ | `xvlog-gate` |
| `check_rtl_source_lists`, `check_cpp_idiom`, `check_py_idiom` | OK, OK, OK | |
| `cd tests && behave --no-capture -f plain` | 14 features, 344 scenarios, 1739 steps | `behave` |
| `git diff --check`, and against `57456af9` | clean | `diff-check`, `diff-check-base` |
| extra: `measure_test_evidence --check`, `lint_rtl --check`, `test_firmware_compiler --absent`, Yosys `--mode elaborate --top milan_datapath` | PASS; 90 <= 90; rc 0; PASS 50772 cells | |

## Not run, and why

- The full Yosys synthesis of `milan_datapath` and the other tops: an elaborate smoke only, and the hosted Yosys shards run on push.
- `scripts/run_all_suites.sh` as a whole, `act`, and the hosted runs: no push in this round.
- R276's builder clone script, and R277's `cp -a` wrappers (see above).
- Hardware: not allowed.

## Files here

- `PR-BODY.md`: the full proposed PR #555 body.
- `REVIEW-READY.md`: the posted comment.
- `run_gate.py`, `sweep_chunk.py`, `full-builder-sdk.py`, `compiler-absent-sitecustomize.py`: the runners.
- `receipts/`: every log.
- `MANIFEST.sha256`.
