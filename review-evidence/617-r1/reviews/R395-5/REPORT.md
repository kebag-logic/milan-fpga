[R395] POSITIVE - exact head 2cc926da316c3e1c64e94ebeaab982672013fa57

# R395-5: composition review of issue #617 / PR #618 on the merge-train candidate

Role: independent composition reviewer, cleared context.

Scope: composition acceptance only. The PR source head `35f58b9cca1de9215f787872734e6a9040f82c19` already carries two independent POSITIVE source reviews: [R394-4](https://github.com/kebag-logic/milan-fpga/pull/618#issuecomment-5884180493) and [R395-4](https://github.com/kebag-logic/milan-fpga/pull/618#issuecomment-5884235561). This round asks one question: does the composed tree introduce a defect that the reviewed sources do not have?

Public start: [R395-5](https://github.com/kebag-logic/milan-fpga/pull/618#issuecomment-5884250605).

## Verdict in one paragraph

No. The candidate is a clean three-way merge of C_495b (`0cc00731`) and the PR head (`35f58b9c`). Its tree `578218ee` is exactly what `git merge-tree` produces. In each of the six files both sides changed, each side's changes carry over line for line.

Structurally, #602's restart and re-base signals reach only the `mr` engine and the render recentre. No port of the media NCO, the grid aligner or the capture crossbar reads them, and the restart engine reads none of this PR's signals.

Dynamically, a disposable probe fired the #602 PHC-only re-base (a `PTP_CMD` settime) into the composed datapath while the aligner was acquiring and while it held the CRF lock. Result: 0 torn columns, 0 slips and `SLIP_TDM` 0/0 at all eight lock phases. Planting a coupling of the re-base into the crossbar tick, or into the NCO reset, turned the same probe red.

The composed `TIME_SYNC.md`, `REGISTER_MAP.md`, `FPGA_DESIGN.md`, `TESTING.md` and `CHANGELOG.md` state both lanes' contracts without contradiction. All 36 static and Markdown gates pass in the pinned environment.

Every assigned suite passes on the candidate, with the figures the source reviews recorded:

- `capture_coherence`: junction 20,832/0, dp 332/0, mutation arm 30/30;
- `milan_dp`, including the #602 gmstep leg (103/0, all five controls caught);
- `milan_dp_render`, where T30 reproduces the `TIME_SYNC.md` figure of -0.5339 ppm.

The builder test with `--require-rv32 --require-elaboration` passes (rc 0). One arm did not run for a recorded, environment-only reason.

No MINOR, MAJOR or BLOCKER is open, so all five lenses are clean at this head.

## 1. What was composed

| Item | Value | Receipt |
|---|---|---|
| Candidate | `2cc926da316c3e1c64e94ebeaab982672013fa57`, tree `578218ee140123445679eb1ef9e84b4786cece61` | `receipts/composition_identity.txt` |
| Parents | `0cc00731`: C_495b, i.e. dev `13eda870` (#395, #595, #602, #607, #609 on `ce550952`) plus #616 and the #619 residue lane. `35f58b9c`: the PR #618 source head | same |
| Merge base | `ce550952`, the PR's cut point | same |
| Mechanical merge | `git merge-tree --write-tree 0cc00731 35f58b9c` prints `578218ee`, rc 0. It is a clean three-way merge, so no hand resolution entered the tree | same |
| Candidate vs `0cc00731` | Exactly the PR's 40 files. No train file differs | same |
| Per-side hunks in the shared files | For each shared file, the candidate's diff against `35f58b9c` equals the train's diff `ce550952..0cc00731`. Its diff against `0cc00731` equals the PR's diff `ce550952..35f58b9c`. Both hold line for line (hashed `-U0` bodies) | `receipts/composition_hunks.txt` |
| Gitlinks | All four are identical at the candidate and at `0cc00731`. The PR changes none | `receipts/composition_identity.txt` |

**Files both sides changed since `ce550952`.** Verified with `git diff --name-only`; the list matches the manager's exactly:

- `CHANGELOG.md`
- `docs/design/TIME_SYNC.md`
- `docs/fpga/FPGA_DESIGN.md`
- `docs/reference/REGISTER_MAP.md`
- `docs/testing/TESTING.md`
- `hdl/milan/milan_datapath.sv`

**Semantic interactions beyond the shared files.** Each is examined in section 2.

- The dp leg of `tb/verilator/capture_coherence` takes its source list and flags from `tb/verilator/milan_dp/Makefile` (`print-srcs`, `print-dp-vflags`). The train changed that Makefile: #602 added `MCR_SRC`, and the AX 1x1 clock now comes from a parse-time `$(shell python3 ... recipe.py)`.
- The PR edits generated inventories that the train's new suites could have made stale: `docs/traceability/MODULE_MATRIX.md` and 14 `hdl/**/README-tests.md` files.
- Shared registries and ratchets:
  - `scripts/measure_test_evidence.py` (`DUT_READER_DISPOSITIONS`);
  - the CI event contract (`ci_events.py`);
  - the hosted shard allocation.
- TOC and anchors: both sides extend the CHANGELOG contents list, and the PR adds new `TIME_SYNC.md` anchors that other pages link to.

## 2. Composition analysis

### 2.1 RTL: the #602 restart/re-base logic against this PR's aligner, NCO and capture binding

The train's change to `hdl/milan/milan_datapath.sv` is:

- `:3137-3147`: `mcr_restart_p_w` drops `media_rebase_p_w`, so a PHC-only re-base no longer requests an `mr` restart;
- `:3108-3111`: the matching comment.

This PR's changes are:

- `:1208-1223`: `CMAP_TDM_SLOTS_C`, `CMAP_TDM_FRAME_PAIRS_C`, and the crossbar's `TDM_FRAME_PAIRS_P`;
- `:5716-5737`: `MGA_KEEPOFF_CYC_C`, the one-cycle-late `media_tick_q_r`, and the aligner's frame close marker;
- `:5650-5702`: comments.

The regions are far apart, and neither side's hunk was altered by the merge (`receipts/composition_hunks.txt`).

**Signal cone** (`cone_check.sh`, `receipts/cone_check.log`):

- **NCO** (`:763-777`): the ports read `axis_clk`, `axis_resetn`, `18'sd0`, `mnco_servo_trim_w` and `mnco_servo_en_w`. `mnco_servo_en_w` = `crf_clk_selected_r` (`:5739`), and `crf_clk_selected_r` is registered from the AECP clock-source index alone (`:1560-1570`).
- **Aligner** (`:5724-5738`): the ports read `crf_clk_selected_r`, the frame close, `media_tick_q_r` and the keep-off constant.
- **Capture crossbar** (`:1220-1295`): 65 port lines, none of them a restart or re-base signal.
- **Readers of the #602 signals:**
  - `media_rebase_p_w` feeds only `render_recentre_p_w` (`:6127-6129` → `KL_render_setpoint` `:6283`).
  - `mcr_restart_p_w` feeds only `KL_media_clock_restart` (`:3176`).
  - The engine's `mr_o` feeds only the packetizer's and CRF talker's header bits (`:3193-3194`).
- **The other direction:** the restart engine's port block names none of `mnco_*`, `mga_*`, `media_tick_q_r`, `MGA_KEEPOFF_CYC_C`, `CMAP_TDM_*` or `aafcap_*`.
- **Negative control:** planting `media_rebase_p_w` into the aligner's `tick_i` in a scratch copy makes the check fail with rc 1 (`receipts/cone_check_negative.log`).

So a PHC-only re-base, and a media-clock restart from a source change, a selected-CRF disruption or an `mr` echo, cannot move the NCO trim, the aligner's state or the capture walk. The two shared readers are unchanged by the merge:

- `crf_clk_selected_r`, which both lanes read and neither changed.
- #386's `g_src_recentre` (`:6070-6117`), which reads `mga_engaged_w` and `mga_err_w`. #602 does not touch it. The PR's wider keep-off only lengthens the pull the settle waits for, which the source reviews and `TIME_SYNC.md` "Engagement cost" already cover.

**Dynamic probe: a PHC-only re-base during acquisition and in the lock.** Files: `probe_rebase/sim_dp_rebase.cpp`, `probe_rebase/run_probe.sh`, `receipts/probe_rebase_*.log`. The probe is an untracked copy of the `capture_coherence` dp recipe, built against the composed `milan_datapath.sv`. It issues `PTP_CMD[0]` settimes through the CSR face; that is `cfg_ptp_cmd_load`, and so `media_rebase_p_w`.

- **Where the settimes land:**
  - Under CRF, at eight lock phases: at column ~23 (inside acquisition) and at columns 305, 803 and 1205 (inside the locked tail).
  - At INTERNAL, on a -1000 ppm drift, three settimes.
- **How they are graded:** by the leg's own checks: `[A]` torn columns and pair splits, `[C]` continuity, the CRF law (net zero, only inside the engagement window, none in the lock), `[V]` lock phase, and `SLIP_TDM` equal to the columns' repeats and skips.
- **Non-vacuity:** every settime must produce a `render_recentre_p_w` pulse. The run observed 8 pulses per 4 settimes, and 6 per 3 at INTERNAL.

| Variant (datapath copy) | Result |
|---|---|
| composed tree, unmodified | 141 checks, 0 failures. Every CRF phase: 0 torn, 0 repeats, 0 skips, `SLIP_TDM` 0/0 |
| P1: re-base ORed into the crossbar's `tick_i` | 26 failures: CRF net zero, slips outside the window, slips in the lock, INTERNAL cluster law |
| P2: re-base resets the media NCO | 23 failures: lock phase spread, CRF net zero, slips in the lock |
| P3: re-base resets the grid aligner | 0 failures. At the true plan an aligner reset mid-lock re-engages where it stands, so the columns see nothing. That is a limit of this probe, not a finding: the structural check above is what excludes that coupling |

### 2.2 Tests: the gates, suites and inventories that read both lanes' files

**The dp leg's derived source list.** On the composed tree, `make -C tb/verilator/milan_dp print-srcs` emits 112 sources:

- #602's `KL_media_clock_restart.sv` arrives through `MCR_SRC`;
- `print-srcs` is byte-identical with and without an inherited `MAKEFLAGS=w`, with no "Entering directory" line;
- `print-dp-vflags` is identical too;
- a control run without `--no-print-directory` shows the contamination that flag guards against.

Receipt: `receipts/milan_dp_print_srcs_composed.txt`. The arm's own check "the dp recipe builds under an inherited MAKEFLAGS=w" passes on the candidate.

**Suites on the candidate.** Verilator 5.050, 8 CPUs, run as `make -C tb/verilator/<suite>` (the way `scripts/run_all_suites.sh` does). Receipts: `receipts/suite_*.log`, `receipts/suites_summary.txt`.

| Suite | rc | Verdict lines |
|---|---|---|
| `capture_coherence` (junction, dp, dp-band and the mutation arm) | 0 | junction 20,832/0; dp 332/0; arm 30/30, including both build checks and every dp/dp-band mutant |
| `chmap_capture` | 0 | 371/0 and 20/0 |
| `media_nco` | 0 | 410/410 |
| `media_grid_align` | 0 | 45/0; three negative controls red as required |
| `crf_rx` | 0 | discontinuity 2201/0; talker_step 69/0; mutants 10/0 |
| `crf_tx` | 0 | 127/0 |
| `mmcm_servo` | 0 | phc_step 113/0 and 90/0 |
| `tdm` | 0 | 58/0 |
| `milan_dp` | 0 | every leg RESULT: PASS; gmstep 103/0; the five #387/#602 controls caught; render-law 6/6 |
| `milan_dp_render` | 0 | 152/0 and 65/0; leg defects 5/5; T30 walk +10.6844 ppm at INTERNAL and -0.5339 ppm under CRF |

These are the source-head figures the round-4 reviews report (junction 20,832/0, dp 332/0, arm 30/30). The composition changed none of them.

**Builder bank.** Command: `sw/builder/test_builder.py --require-rv32 --require-elaboration`, with the pinned RV32 SDK (release `riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256 `d42680e9...`, installed offline and verified by `scripts/ci_rv32_sdk.py`) and a LiteX interpreter whose `ci_litex_env.py --check` passes. Result: rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN". The one arm is gate 11, which needs a local mf48 build report on disk. Receipts: `receipts/builder_test_litex.log`, `receipts/builder_sdk_install.log`, `receipts/builder_litex_env_check.log`.

- A first run without a LiteX interpreter reported the same verdict with 13 arms not run, so `--require-elaboration` refused it (rc 1): `receipts/builder_test.log`. That run's two `disabled-writer endstation_arty_4x4 ... FAIL` lines belong to the saved-state writer gate's planted mutant ("caught in both states", "every planted defect reddened").
- A file-level snapshot of the LiteX install before and after the elaboration run differs in 0 of 64,637 files (`receipts/builder_litex_tree_writes.txt`).

**Inventories and ratchets.** All pass (section 3): `gen_module_matrix.py --check` (which also regenerates the `hdl/**/README-tests.md` files), `measure_test_evidence.py --check`/`--selftest`, `ci_events.py --check`/`--selftest`, `suite_shards.py --selftest` and the five `--shard k/5 --list` partitions.

**Hosted scheduling.** The composition places `capture_coherence` (this PR) and the train's `fw_service_budget` and `nvm_cosim` in shard 1/5.

- Hosted shard 1 took 30m47s at dev `13eda870` and 47m25s at the PR head. `capture_coherence` took 993 s of the latter.
- The composed shard 1 is therefore about 47 minutes: inside the 120-minute shard job limit (`docs/testing/CI_WORKFLOWS.md`), with `capture_coherence` at 993 s against its 1,800 s guard.
- Receipt: `receipts/hosted_shard_timing.txt`. This is a projection from the two exact-head hosted runs, not a hosted run of the candidate.

### 2.3 Docs: both lanes' contracts in the composed pages

| Page | #602 text (train) | #617 text (PR) | Composed reading |
|---|---|---|---|
| `docs/design/TIME_SYNC.md` | `:107-113` decision rows; `:256-262` PHC-only re-base keeps `mr`; `:355` Recentre row | `:168` NCO trim row; `:178-180` aligner rows; `:410` T30 walk; `:463-607` "Talker capture handoff" and "The guarded crossing" | Separate subjects. `:356` (#386 settle) is unchanged, and the PR's "Engagement cost" row states that the settle waits for the pull, which is consistent. The ±100 ppm local-oscillator bound the PR cites "(above)" is still at `:129`/`:280`. The T30 figure is reproduced on this tree |
| `docs/reference/REGISTER_MAP.md` | `:127-130` the PHC-only re-base preserves `mr`; `:413-418` PHY link text | `:1843-1995` `SLIP_TDM` crossing, guarded crossing, reading table | Separate sections, no contradiction. The PR's link to `TIME_SYNC.md#the-guarded-crossing` resolves |
| `docs/fpga/FPGA_DESIGN.md` | `:177-180` | `:259`, `:293` module rows | Separate |
| `docs/testing/TESTING.md` | `:273` gmstep row; `:941-945` soak note | `:490` `capture_coherence` row; `:514` `media_nco` row | Separate. The PR's `milan_datapath` edits touch none of the symbols `:273` names as the trigger for the full `gmstep-mutants` inventory |
| `CHANGELOG.md` | its "one media event per PHC step" entry | new top entry `:11`, `:37-66`; "VERSION remains `0x0002_0060`" | The contents list is ordered and regenerated consistently (`gen_toc.py --check`). VERSION is still `0x0002_0060` at the candidate |

Gates: `gen_toc.py --check`, `--verify-anchors` (245 cross-page fragments) and `--selftest`; `check_em_dash.py` with base `0cc00731` (373 added lines, 0 findings), base `13eda870` (842 lines, 0) and base `ce550952` (1,956 lines, 0); `docs_check.py`; and the rest listed in section 3.

## 3. Static and Markdown gates on the candidate

Pinned Markdown environment: `cmarkgfm==2025.10.22`, `html5lib==1.1` and the rest, matching `tools/markdown/requirements.txt`. All rc 0; one receipt each, `receipts/static_*.log`; summary in `receipts/static_gates_summary.txt`. Run by `run_static_gates.sh`.

`check_em_dash.py --base 0cc00731` and `--selftest`; `gen_toc.py --selftest`, `--verify-anchors` and `--check`; `docs_check.py`; `check_feature_status.py`; `check_doc_style.py` and `--selftest`; `check_gptp_docs.py`; `DOC_MAP.gen.py --check`; `timesync_chain.gen.py --check`; `check_solution_docs.py`; `check_submodule_docs.py`; `check_diagram_pngs.py`; `gen_module_matrix.py --check`; `measure_test_evidence.py --check` and `--selftest`; `ci_events.py --check` and `--selftest`; `check_rtl_source_lists.py`; `check_port_contracts.py`; `measure_naming.py --check`; `measure_fail_fast.py --check`; `check_todo_ownership.py`; `check_hygiene.py --check`; `check_sv_idiom.py`; `check_cpp_idiom.py`; `check_py_idiom.py`; `check_sh_idiom.py`; `check_archive.py`; `check_soc_sources.py`; `check_baremetal_only.py --check`; `check_nvm_record_space.py`; `pp_srcs.py --check`; `lint_rtl.py --check`. That is 36 in total, plus the extra em-dash bases (`receipts/static_em_dash_other_bases.log`) and the shard listing (`receipts/static_suite_shards.log`).

Observation, not a finding: `measure_test_evidence.py --check` prints "the mutation ratchet can be lowered to 75". Lowering a ratchet is optional, and it is outside this PR.

## 4. Findings

None. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised by this round.

## 5. Lens results at this head

```text
[R395] PASS Conformance - hdl/milan/milan_datapath.sv:1208-1223,5716-5737,3137-3147; receipts/suite_capture_coherence.log, suite_milan_dp.log, suite_milan_dp_render.log, probe_rebase_clean.log - on the composed tree #617 acceptance 1-3 still hold (every AAF column one TDM frame: junction 20,832/0, dp 332/0; drift in INTERNAL and CRF; the ce550952-law mutant still killed; render path: milan_dp_render T30 and milan_dp aclk pass) and #602's contract still holds (gmstep 103/0, restored-PHC-cause and missing-source/CRF controls caught); a PHC-only re-base in acquisition and in the lock leaves the columns whole
[R395] PASS RTL - hdl/milan/milan_datapath.sv (candidate 2cc926da), receipts/composition_hunks.txt, cone_check.log, cone_check_negative.log, static_lint_rtl_check.log, the dp/milan_dp elaborations - both lanes' hunks land unaltered; the #602 restart/re-base signals reach no NCO, aligner or crossbar port and the restart engine reads no #617 signal (check proven able to fail); the lint ratchet and every milan_datapath elaboration pass; no duplicate port or declaration
[R395] PASS Robustness - probe_rebase/sim_dp_rebase.cpp and receipts/probe_rebase_{clean,P1_crossbar_tick,P2_nco_reset,P3_aligner_reset}.log; receipts/milan_dp_print_srcs_composed.txt - PHC settime during CRF acquisition and inside the lock at eight phases, and during INTERNAL drift: 0 torn, 0 slips, SLIP_TDM 0/0; planted crossbar and NCO couplings go red; the composed milan_dp Makefile gives the dp leg identical source and flag lists under an inherited MAKEFLAGS=w
[R395] PASS Tests - receipts/suites_summary.txt with suite_*.log; builder_test_litex.log; static_module_matrix_check.log, static_test_evidence_check.log, static_ci_events_*.log, static_suite_shards.log; hosted_shard_timing.txt - every assigned suite rc 0 on the candidate with the source-head figures (arm 30/30); builder rc 0 with --require-rv32 --require-elaboration; generated inventories and ratchets current after the train's added suites; composed shard 1 about 47 min against a 120 min limit
[R395] PASS Docs - docs/design/TIME_SYNC.md:107-113,129,168,178-180,256-262,355-356,410,463-607; docs/reference/REGISTER_MAP.md:127-130,1843-1995; docs/fpga/FPGA_DESIGN.md:177-180,259,293; docs/testing/TESTING.md:273,490,514,941-945; CHANGELOG.md:11,37-66; receipts/static_gen_toc_*.log, static_em_dash_*.log, static_docs_check.log - both lanes' contracts read together without contradiction; the -0.5339 ppm T30 figure reproduces on this tree; anchors resolve; no em dash added against the train parent, live dev or the PR's base
```

## 6. Reviewer-owned completion ledger (composition)

Every lens's scope is touched by the composition: a shared RTL file, shared docs, and the dp leg's dependency on the train's `milan_dp` Makefile. So every lens is covered here at the candidate. For the PR's files the composition did not change, the source rounds' coverage carries over unchanged: those files are byte-identical between `35f58b9c` and the candidate (`receipts/composition_identity.txt`).

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #617 acceptance 1-3 and scope rulings; #602's PHC-only contract; `capture_coherence`, `milan_dp` (gmstep), `milan_dp_render` on the candidate; re-base probe | R395-5 (composition); R394-4 and R395-4 (source scope) | `2cc926da316c3e1c64e94ebeaab982672013fa57`; source `35f58b9cca1de9215f787872734e6a9040f82c19` |
| RTL | CLEAN | `milan_datapath.sv` composed hunks; signal cone and its negative control; lint ratchet; composed elaborations | R395-5; R394-4 and R395-4 | `2cc926da316c3e1c64e94ebeaab982672013fa57`; source `35f58b9cca1de9215f787872734e6a9040f82c19` |
| Robustness | CLEAN | Re-base during acquisition and lock (8 CRF phases and INTERNAL drift) with 3 planted couplings; `print-srcs` under `MAKEFLAGS=w` | R395-5; R394-4 and R395-4 | `2cc926da316c3e1c64e94ebeaab982672013fa57`; source `35f58b9cca1de9215f787872734e6a9040f82c19` |
| Tests | CLEAN | 10 suites; builder bank; module matrix, test-evidence, ci_events and shard gates; hosted shard projection | R395-5; R394-4 and R395-4 | `2cc926da316c3e1c64e94ebeaab982672013fa57`; source `35f58b9cca1de9215f787872734e6a9040f82c19` |
| Docs | CLEAN | `TIME_SYNC.md`, `REGISTER_MAP.md`, `FPGA_DESIGN.md`, `TESTING.md`, `CHANGELOG.md` as composed; TOC, anchor, em-dash and docs gates | R395-5; R394-4 and R395-4 | `2cc926da316c3e1c64e94ebeaab982672013fa57`; source `35f58b9cca1de9215f787872734e6a9040f82c19` |

## 7. Prior public findings, resolved or retained at this head

This section was read after my own pass over the composition diff.

| Finding | State at `2cc926da` | Evidence |
|---|---|---|
| Rounds 1-3: R394-1 F1; R395-1 F1-F3; R394-2 F1-F2; R395-2 F1-F3; R394-3 F1 = R395-3 F1 | **REMAIN RESOLVED** | Resolved at `35f58b9c` by R394-4 and R395-4. The composition changes no PR file except the six shared ones, and it alters no PR hunk in those. On the candidate the arm kills every guard mutant: the band and dp-band bindings, the RM1-class `[F1]`, the NCO `==` restore (nco and fine), RM5, RM7, RM8 and the RM9 build refusal. Both dp build checks pass. Hosted shard 1 fits (section 2.2) |
| R394-4 S1 = R395-4 S1: `mutants.py` kill path and temp-directory cleanup | **RETAINED as SUGGESTION** (optional; no effect on coverage) | `mutants.py` is identical at the source head and the candidate |
| R394-4 S2: dead helpers and nested oversubscription | **RETAINED as SUGGESTION** | same |
| R395-4 S2: the nested-make pattern in the `pp_shadow` and `milan_dp_render` explicit campaigns | **RETAINED as SUGGESTION**, outside this PR | The train changed `milan_dp/Makefile`, but its parse-time `$(shell ...)` is assigned, not printed; `print-srcs` stays clean (`receipts/milan_dp_print_srcs_composed.txt`) |

## 8. Real limits

- **Simulator path.** The assigned Verilator path did not exist. I used the same Verilator 5.050 installation that two sibling manager directories' byte-identical wrappers name, through my own wrapper (binary sha256 in `receipts/00_tool_identity.txt`). The system Verilator (5.052) was not used.
- **Suite-run incident.**
  - My first suite runner outlived its tool call. While it was running `mmcm_servo`, I mistakenly believed it had stopped: I started a second queue and cleaned that suite's build directory.
  - All queues were then stopped. No verdict from the disturbed runs is counted.
  - A single fresh queue ran `mmcm_servo` and every later suite, and those are the verdicts above.
  - The four earlier suites (`media_nco`, `media_grid_align`, `crf_rx`, `crf_tx`) had finished rc 0 in their own directories before this happened. `receipts/suites_summary.txt` records it.
- **Not run by me:** Yosys, `xvlog`, the full parent/PP/gPTP banks, the explicit `gmstep-mutants` inventory (TESTING.md `:273`'s trigger symbols are untouched by this PR), `tkdiag`, act and hosted CI. The builder's gate 11 did not run (it needs a local build report).
- **Probe scope.**
  - The re-base probe runs on the true plan under CRF and on -1000 ppm at INTERNAL.
  - It does not exercise a CRF disruption or an `mr` echo dynamically, since the dp leg has no CRF input stream. The structural cone check covers those triggers.
  - The P3 coupling (an aligner reset) is invisible to column grading at the true plan.
- **Hosted evidence.** The candidate is not on GitHub, so it has no hosted run. Shard fit is projected from the exact-head hosted runs of dev `13eda870` and of `35f58b9c`. Local wall times were measured on a shared machine under an 8-CPU cap, and they are not budget evidence.
- **No hardware.** Physical calibration was NOT RUN. Simulation is not silicon proof, and bench acceptance 4 remains open (the PR says "Relates to #617").
- **Receipts carry local absolute paths.** Redact them at publication as needed.

## 9. Pending manager duties

- Build and gate the final current-dev candidate at the merge turn. This candidate composes onto C_495b, not onto live dev.
- Take hosted and act acceptance at the exact head that merges.
- Decide the retained round-4 suggestions, and file the follow-up Issue for the nested-make pattern in the `pp_shadow` and `milan_dp_render` explicit campaigns.
- Merge only with explicit maintainer authorization, then run post-merge containment.
- Keep #617 open for bench acceptance 4.
- Publish this packet.

## 10. Restoration

The clone ends at `2cc926da`, tree `578218ee`.

- The index digest equals the pre-run baseline.
- `git diff --quiet HEAD` and `git diff --cached --quiet HEAD` both give rc 0 after `update-index --really-refresh`.
- No assume-unchanged or skip-worktree flags are set, and there are no untracked non-ignored files.
- All four gitlinks match `HEAD`. The three initialised submodules are at their pins with clean trees; `external` is uninitialised, as at the start.
- The probe directory was removed. Only ignored build output remains.

Receipt: `receipts/restore_check.txt`.

R395-5 FINISHED
