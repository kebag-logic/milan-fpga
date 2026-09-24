[R276] NEGATIVE - exact head 0f003fab3303858ba4db955ad3c0512e67a8018b

Round R276-6 is the internal cleared-context re-review of issue #387 / PR #555 (acceptance 3, the datapath half), round 3 of the lane.

- Head `0f003fab3303858ba4db955ad3c0512e67a8018b`, tree `c8af797b92f6961339b6f51b8349c09a48cd7faf`, one commit on `a21cd358`.
- Round-3 delta `a21cd358..0f003fab`: 12 files, +90/-37. The whole PR `57456af9..0f003fab`: 28 files, +1236/-154, twelve commits including the merge `e68c1b1a` of dev `57456af9`.
- All five lenses were applied at this head.

Every finding of my round 2 (R276-5) and of the other reviewer's round 2 (R277-4) is resolved at this head:
- the `milan_dp` deadline is 3600 s in the runner, its contract and the self-test, per decision 5820240308;
- `is_fresh()` reads the recipe inputs under nested GNU make 4.3, and both positive legs are graded without a rebuild;
- the FPGA design page, the compliance matrix and the roadmap scope the selection gate to the CRF triggers;
- the PR body cites decisions 5819379503 and 5820240308;
- the render-stage summary and the restart-engine comment are in;
- a settime render check with a failing omission control is in.

The round-3 `hdl/` delta is comments only. It introduces no regression in anything I ran.

The verdict is NEGATIVE on one MINOR:
- **F1 (Docs).** Decision 5820240308 changed the `milan_dp` deadline to 3600 s. `TESTING.md`, `RUNNING_TESTS.md`, the `milan_dp_gptp` README and the `render_mutants.py` docstring still state 2700 s in the present tense. `run_all_suites.sh` names `TESTING.md` as its reference.

Conformance, RTL, Robustness and Tests are covered clean. Docs is unclean.

## Reconstruction

The sources were read in this order:
1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The issue #387 body and its frozen acceptance.
3. The decisions and rulings:
   - 5606198212 part b;
   - 5794731090 (the owner's step policy);
   - 5802264260 items 1-2;
   - 5810378282 (aligner);
   - 5816509317 (#545 slew coupling);
   - 5818091077 (pending ends on the wire);
   - 5819379503 (report = launched; controls stay; the 10% trigger);
   - 5820240308 (deadline 3600 s).
4. Assignment 5820585975, and [A277] REVIEW READY 5821088465.
5. The PR #555 body and the review-start comment 5821175395.
6. `git diff 57456af9..0f003fab` and `a21cd358..0f003fab`, with history.
7. The exact-head hosted check runs.

The public evidence tree at `afb421cf` was consulted for its manifest only.

Prior public review findings (R276-4, R277-3, R276-5, R277-4) were read after this round's verdict, findings and ledger were fixed in a draft of this file. See "Prior public findings".

## Findings

### F1 - MINOR - Docs - `docs/testing/TESTING.md:166-167`, `docs/testing/RUNNING_TESTS.md:79`, `tb/verilator/milan_dp_gptp/README.md:31`, `tb/verilator/milan_dp/render_mutants.py:37`

**The `milan_dp` deadline is still stated as 2700 s after the change to 3600 s.**

- **Authority and evidence.**
  - Decision 5820240308: "The `milan_dp` deadline becomes 3,600 s."
  - This head implements it: `scripts/run_all_suites.sh:245` (`${SUITE_TIMEOUT:-3600}`), its header comment `:39`, `scripts/measure_test_evidence.py:718-724` and the self-test arm.
  - `CI_WORKFLOWS.md:159` and `tb/verilator/milan_dp/README.md:244,864` were updated.
  - Four present-tense statements were not updated (`receipts/finding_evidence.txt`):
    - `TESTING.md:166`: "The default driver permits 1800 seconds per suite, and 2700 seconds for `milan_dp`." `:167` gives its basis as "the suite's measured hosted worst case plus a stated margin (#444)".
    - `RUNNING_TESTS.md:79`: "... except `milan_dp`, which has 2700 seconds (#444)."
    - `milan_dp_gptp/README.md:31`: "The historical `milan_dp` suite has its own 2700-second budget (#444)."
    - `render_mutants.py:37`: "per-suite guard, suite_timeout = 2700 s (#444)".
  - `run_all_suites.sh:41` sends its reader to `docs/testing/TESTING.md`. The `milan_dp_gptp` README cites the testing guide as the authority for deadlines.
  - The two remaining mentions of 2700 are correctly historical: `CI_WORKFLOWS.md:167,185`, and the self-test's mutation arm.
- **Lens.** Docs: "Changed contracts are reflected in authoritative docs". No executable surface is affected: the runner, the contract and the self-test all agree on 3600 s.
- **Impact.** The testing guide and the running-tests page state a suite deadline that the runner no longer applies. They also give a basis for it that decision 5820240308 replaced. A reader who sizes a local run from them, or judges a hosted timeout against them, is off by 900 s.
- **Required outcome.** Each present-tense statement of the `milan_dp` deadline says 3600 s and cites decision 5820240308 or the workflow policy. `TESTING.md:167` and `:259` give the basis the decision gives. `:259` currently says the budget "covers the unchanged suite".
- **Verification.** At the corrected head, `git grep -n 2700` outside the submodules leaves only historical statements and the self-test arm. The docs gates pass.

### Suggestions (do not affect coverage)

- **S1 (Docs), `tb/verilator/milan_dp/README.md:763`.**
  - The census row for `obj_aclk` still reads **139 / 0**. This head adds the four RENDER-SETTIME checks, and the leg measures **143 / 0** (`receipts/aclk_head.log`).
  - The row is undated, so it reads as the older broad-run measurement, not a false claim. This PR refreshed the rows of the other legs it changed with a date, and this one could match them.
- **S2 (Tests), `tb/verilator/milan_dp/gmstep_mutants.py:185-199`.**
  - The docstring says a clean binary is fresh when it is "no older than any input of its recipe". The check reads only `SRCS`, the harness and the Makefile.
  - The recipes' other prerequisites are not read: `ltn_rom.hex`, `ucode.hex`, `gptp_ucode.hex`, `$(GEN_ALL)` (`Makefile:323,370`), and for gmstep the builder-generated `aemi.bin`.
  - In the sweep this is moot, because `run` rebuilds `obj_gmstep` first. A direct run after regenerating a ROM or a shape header would grade a stale binary.
  - Either the docstring could name what is read, or the check could add those prerequisites.

## Round-3 items the assignment asked me to verify

| Item | Result | Evidence |
|---|---|---|
| 3600 s deadline and its contract | Closed in code; F1 for the prose | `run_all_suites.sh:39,245`; `measure_test_evidence.py:718-724`; `--check` and `--selftest` (101/101) exit 0 (`receipts/static_gates.log`). My mutation probe: 2700, 3599 and 7200 each fail the runner contract with "the declared 1800/3600/5400-second suite budgets changed" (`receipts/deadline_contract_probe.txt`). `milan_dp` runs alone on shard 4/5 (`suite_shards.py --shard 4/5`), and `.github/workflows/rtl.yml:152` gives the shard 120 minutes |
| Cited samples | Reproduced exactly | My `scripts/milan_dp_window.py` ran unchanged (its 2700 s margin column is the old budget). The results are 1296.1 s (dev `9d328810`), 2133.3 s (`57456af9`), 2264.9 s (`a9636e0f`) and 2459.9 s (`a21cd358`), with the job ids, windows and check counts of the `CI_WORKFLOWS.md:176-181` table and the PR table. Against 3600 s, 2459.9 s leaves 1140.1 s (31.7%) (`receipts/milan_dp_hosted_windows.txt`) |
| gmstep freshness under nested GNU make 4.3 | Closed | My probe runs inside a recipe of the suite's own parent make, loading the Makefile beside a probe file. Under make 4.3 the head's `is_fresh()` is True for both legs. The `a21cd358` runner is False for both, because `print-srcs` stdout carries `make[1]: Entering directory` (`receipts/freshness_make43_raw.log`). Under 4.4.1 both runners are True (`freshness_make441_raw.log`). Touching `KL_media_clock_restart.sv` still makes both legs stale (`freshness_stale_direction.txt`). The other reviewer's `repro_gmstep_freshness.sh` (sha256 `370ea465...`), run unchanged, prints `is_fresh: True` inside the parent recipe under make 4.3 and 4.4.1 (`receipts/repro_gmstep_freshness_r277-4_unchanged.txt`). The exact-head hosted log check is under "Hosted evidence" |
| Both positive legs | Pass, graded without a rebuild | Under a parent make 4.3 recipe: the default `python3 gmstep_mutants.py` gives 4/4 with no `[INFO] ... rebuilt` line (`receipts/gmstep_default_controls_make43.log`). Through the head's runner functions, positive gmstep and option-off pass, and controls 3-10 are each caught by their named check. So is my extra control, a second restart 3000 cycles after the step (`gmstep_controls_part1.log`, `part2.log`). That makes all eleven lane controls caught |
| `FPGA_DESIGN.md` `mr` scope, compliance matrix, roadmap | Closed | `FPGA_DESIGN.md:169-180` gates "the CRF triggers of IEEE 1722-2016 4.4.4.3 `mr`" and states that a PHC step toggles `mr` whatever the selection. `MILAN_COMPLIANCE_MATRIX.md:120` and `MILAN_V12_ROADMAP.md:356-362` say the same. This matches `REGISTER_MAP.md:124-133` and `milan_datapath.sv:3110-3113` |
| PR body decision citations | Closed | The body cites 5819379503 (report = launched; three controls in `run`) and 5820240308 (3600 s, with the four hosted samples), and it says "Relates to #387" |
| `KL_render_setpoint` summary | Closed | `:120-121`: "re-centred once on a PHC step or a settled clock-source change" |
| `KL_media_clock_restart` comment | Closed | `:236-237`. It is correct: `hold_r == 0` with `streaming_i[t] == 0` is only the first cycle after a stop, and the term keeps that talker on the non-streaming track-the-target rule (`:250-254`) |
| Settime re-base render check and its omission control | Closed | `sim_aclk.cpp:1394-1411` writes `PTP_CMD[0]` at `0x520` (`REGISTER_MAP.md:665`) and requires one `render_recentre_p_w` pulse and one `rsp_recentres_w` count, still one after 100 more PDUs. The leg gives 143/0 (`receipts/aclk_head.log`). My controls, planted and built through `make aclk-build`: removing only the settime from the render trigger fails all four RENDER-SETTIME checks, and a second re-base 30 PDUs later fails the two "no later"/"remains once" checks. Nothing else fails (`receipts/aclk_settime_controls.log`). The #386 `render_mutants.py` gives 6/6 on the same leg (`render_mutants_head.log`) |
| Delta changes no functional RTL | Confirmed | After `//` and `/* */` comments are stripped, the round-3 `hdl/` token streams are identical (2 files). The detector does see the PR's real code changes in `milan_datapath.sv` and `KL_media_clock_restart.sv` over `57456af9..0f003fab` (`receipts/hdl_comment_only.txt`) |

## Whole PR at this head (conformance judgement)

- **IEEE 1722-2016 4.4.4.3 / 10.4.3, Milan Table 5.4, decision part b, 5794731090.** Conforms.
  - `media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load` (`milan_datapath.sv:3110`) is ORed into `mcr_restart_p_w` outside the `crf_clk_selected_r` gate (`:3111-3113`). The CRF disruption and echo stay gated.
  - The render stage re-centres on `media_rebase_p_w | src_recentre_p_r` only (`:6026-6028`), so a grandmaster identity change is no longer a separate trigger.
  - Every term is on `axis_clk`, and `ptp_csr_sync` already took the same pulses on `aclk = axis_clk` (`:2779-2787`), so no crossing is added.
- **Rulings 5802264260 item 2, 5818091077 and 5819379503 item 1.** Conform.
  - `tgt_r <= ~mr_o` on a request, and a streaming talker at `hold_r == 0` keeps its adopted level (`KL_media_clock_restart.sv:229-240`). So a request merges until the first reported PDU at the adopted level, and nothing is cancelled.
  - The launch-to-report residue is documented at `:79-91`.
- **Executable evidence at this head:**
  - gmstep 48/48 (`receipts/gmstep_head.log`);
  - option-off `obj_dir` 233/0, including the three #387 checks (`optionoff_head.log`);
  - true-ratio `obj_aclk` 143/0;
  - tkdiag 96/96 with `mcr_mutants.py` 5/5 (`tkdiag_head.log`);
  - my engine property probe (`scripts/mcr_property/`, 60 seeds x 2 modes, 300k cycles): the head engine is clean on 120/120 runs with 229,975 requests, 0 spurious toggles, 0 hold violations and 0 left pending. Six planted engines each fail 116-120 of 120 (`mcr_property_summary.txt`). The result is identical to round 2, as expected: the engine code is unchanged.
- **Part b aligner decision.** Untouched: no aligner, servo or `hdl/ieee8021as` change in the range.

## Lens results (clean lines carry their evidence)

- `[R276] PASS Conformance - hdl/milan/milan_datapath.sv:2743-2751,3097-3113,6017-6028; hdl/ieee1722/avtp/KL_media_clock_restart.sv:55-104,199-259; docs/testing/CI_WORKFLOWS.md:156-192 and scripts/run_all_suites.sh:239-249 against decision 5820240308; receipts/gmstep_head.log, optionoff_head.log, aclk_head.log, tkdiag_head.log, mcr_property_summary.txt - checked against 1722-2016 4.4.4.3 and 10.4.3, Milan Table 5.4, decision 5606198212 part b, 5794731090, rulings 5802264260 items 1-2, 5818091077, 5819379503 items 1-2 and 5820240308, and assignment 5820585975 items 1-3 plus its taken suggestions: every item is implemented as decided.`
- `[R276] PASS RTL - hdl/ieee1722/avtp/KL_media_clock_restart.sv:199-259 (per-talker tgt_r width and reset, the adoption-cycle and report-cycle requests, the stop-cycle term at :239); milan_datapath.sv:2750,3110-3143,6026-6028 (axis_clk only, no new crossing); receipts/hdl_comment_only.txt (round-3 hdl delta comment-only); lint_rtl --check, check_rtl_source_lists and gen_module_matrix --check exit 0 (receipts/static_gates.log); hosted yosys-elaboration, Yosys shards 0-3, verilator-lint and elaborate succeeded at 0f003fab (receipts/hosted_checkruns_head.tsv).`
- `[R276] PASS Robustness - scripts/mcr_property/ against the head engine: request storms, a source change and a restart in one cycle, streams stopping mid-pending, 0-3 cycle report latency, AAF-like and CRF-like rates; 120/120 clean, six planted engines killed; tkdiag T12, T15, T17 and T18 with four engine mutants; the INTERNAL and plane-off paths in the option-off leg; a settime to PHC 0 in the true-ratio leg, after which its remaining phases still pass (143/0); gmstep_mutants freshness in both directions under make 4.3 and 4.4.1.`
- `[R276] PASS Tests - tb/verilator/milan_dp/gmstep_mutants.py (positives plus all 11 controls, nested under make 4.3), sim_aclk.cpp:1394-1411 with two planted controls, sim_main.cpp:970-979,1028-1072, tb/verilator/tkdiag/sim_main.cpp with mcr_mutants.py, render_mutants.py 6/6, scripts/measure_test_evidence.py:715-724 with --selftest 101/101 and my 3-arm contract probe - each new or changed check fails for the defect it names, and the positive legs are graded, not rebuilt. S2 is optional.`
- `[R276] MINOR Docs - docs/testing/TESTING.md:166-167 - F1.` Also applied and found sound:
  - `FPGA_DESIGN.md:169-180`, `MILAN_COMPLIANCE_MATRIX.md:120`, `MILAN_V12_ROADMAP.md:356-362`, `CI_WORKFLOWS.md:156-192`, the milan_dp README (`:244`, `:436-438`, `:864`), the `KL_render_setpoint.sv` and `KL_media_clock_restart.sv` comments, the PR body;
  - unchanged since round 2 and re-read: `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `CHANGELOG.md`;
  - `docs_check`, `check_em_dash --base 57456af9`, `gen_toc --check`, `check_doc_style`, `check_doc_paths`, `check_gptp_docs` and `ci_events --check` exit 0 with the locked renderer (`receipts/static_gates.log`).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv` #387 hunks; `KL_media_clock_restart.sv`; the #387 decisions and rulings and assignment 5820585975; `run_all_suites.sh` and `CI_WORKFLOWS.md` against 5820240308; gmstep, option-off, aclk, tkdiag and the engine property probe | R276-6 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| RTL | CLEAN | `KL_media_clock_restart.sv`, `milan_datapath.sv` hunks, `KL_render_setpoint.sv`, `KL_crf_tx.sv`; comment-only proof of the round-3 delta; lint ratchet, source lists, module matrix; hosted Yosys, lint and elaborate at the head | R276-6 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| Robustness | CLEAN | Engine property probe (120 runs, 6 planted engines); tkdiag T12/T15/T17/T18 plus 4 mutants; option-off INTERNAL and plane-off paths; settime to PHC 0 in the aclk leg; freshness both directions | R276-6 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| Tests | CLEAN | `gmstep_mutants.py` (2 positives, 11 controls plus 1 reviewer control, nested make 4.3); `sim_aclk.cpp` RENDER-SETTIME plus 2 controls; `render_mutants.py`; `sim_main.cpp`; tkdiag and `mcr_mutants.py`; `measure_test_evidence.py` and its self-test plus a 3-arm probe | R276-6 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| Docs | UNCLEAN (F1) | `TESTING.md`, `RUNNING_TESTS.md`, `CI_WORKFLOWS.md`, `FPGA_DESIGN.md`, compliance matrix, roadmap, milan_dp and milan_dp_gptp READMEs, `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, CHANGELOG, RTL comments, PR body; docs gates | R276-6 | 0f003fab3303858ba4db955ad3c0512e67a8018b |

## Prior public findings (read after this round's verdict, findings and ledger were drafted)

| Finding | Status at `0f003fab` | Evidence |
|---|---|---|
| R276-5 F1 = R277-4 F2 (MINOR, `milan_dp` margin under the 10% trigger) | Resolved | Decision 5820240308 raised the deadline to 3600 s. The runner, contract and self-test pin it. `CI_WORKFLOWS.md:173-191` and the PR record the exact-head `a21cd358` window (2459.9 s) and the day's spread, and I reproduced both. The prose left at 2700 s elsewhere is this round's F1, which is a different defect |
| R277-4 F1 (MINOR, `is_fresh()` always stale in the nested sweep) | Resolved | `gmstep_mutants.py:189-192` passes `--no-print-directory`. My probe and the finding's own repro, run unchanged, give `is_fresh: True` inside the parent recipe under make 4.3, and the `a21cd358` runner gives False. The finding's hosted verification also holds: the exact-head shard 4/5 suite log has no `[INFO] ... rebuilt` line (see "Hosted evidence") |
| R276-5 F2 (MINOR, `FPGA_DESIGN.md` `mr` scope; matrix and roadmap) | Resolved | `FPGA_DESIGN.md:169-180`, `MILAN_COMPLIANCE_MATRIX.md:120`, `MILAN_V12_ROADMAP.md:356-362` |
| R276-5 S1 = R277-4 S1 (PR body predates 5819379503) | Resolved | The PR body's "Decisions" section cites 5819379503. The stale "decision requested" passages are gone |
| R276-5 S2 (render-stage summary) | Resolved | `KL_render_setpoint.sv:120-121` |
| R276-5 S3 (no settime render re-base in simulation) | Resolved | `sim_aclk.cpp:1394-1411`, and my two controls are caught |
| R277-4 S2 (`streaming_i[t]` term not graded) | Resolved as a comment, the option offered | `KL_media_clock_restart.sv:236-237`. The comment is accurate (see the table above) |
| R276-4 F1-F4, S1-S2 and R277-3 F1-F4, S1-S4 | Remain resolved | They were resolved at `a21cd358` (R276-5, R277-4). Round 3 changes none of their artifacts except adding comments and the deadline, and the builder gate 1b pins are unchanged (`sw/` is untouched since `a21cd358`) |

Reading them changed no finding and no ledger row.

## Hosted evidence at the exact head (inspected, not owned)

See `receipts/hosted_checkruns_head.tsv`, `milan_dp_hosted_windows.txt` and `hosted_head_gmstep_lines.txt`.

- **Required contexts.** All seven concluded `success` for pull_request run 36050997581 and its sibling workflows: `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites` and `yosys-portability`.
  - Verilator shards 0-4/5 executed.
  - Yosys shards 0-3/4 and `yosys-elaboration` executed.
  - "Physical gPTP (nightly and manual)" is a skipped context: it is the scheduled suite, and it is not hardware or physical-rate evidence.
- **Shard 4/5 (`milan_dp`), job 107806587623.** The suite ran from `shard: 4/5` to `PASS milan_dp` in **2454.1 s**, with 9785 checks and 0 failures. Against the 3600 s deadline that leaves 1145.9 s (31.8%), above the 10% level of decision 5820240308. My window script is unchanged, so its margin column is still against 2700 s.
- **Suite artifact `suite-logs-4`** (zip sha256 `2626a800...`), `milan_dp.log`:
  - gmstep 48/0 (`:1643`);
  - `media_aclk` 143/0, with the four RENDER-SETTIME checks (`:16894-16897`, `:17060`);
  - `python3 gmstep_mutants.py` graded the clean leg directly and caught its three controls, 4/4 (`:17096-17105`);
  - **zero** `[INFO] ... the positive control is rebuilt` lines. At `a21cd358` the same log carried one, per R277-4 F1.
- The manager owns the acceptance of hosted and act evidence, and the candidate build. This section records what I inspected.

## Receipts and scripts (all under MANIFEST.sha256)

- **Scripts** (portable; each takes its paths as arguments):
  - `scripts/fresh_probe.py` and `scripts/fresh_probe.mk`: `is_fresh()` of both legs inside a parent-make recipe, for any runner file;
  - `scripts/repro_freshness_r276.sh`: the make 4.3 / 4.4.1 driver, with the head and the `a21cd358` runner;
  - `scripts/nested_runs.mk`: runs the head's runners inside the suite's own parent make;
  - `scripts/run_gmstep_controls.py`: the head's controls by index plus my extra control (from R276-5);
  - `scripts/aclk_settime_controls.py`: the two RENDER-SETTIME controls;
  - `scripts/hdl_comment_only.py`: the comment-only proof;
  - `scripts/milan_dp_window.py` (unchanged from R276-5): the read-only hosted window;
  - `scripts/mcr_property/` (from R276-5): the engine property probe.
- **Receipts:** the leg logs, the control logs, freshness logs, hosted windows and check runs, the comment-only proof, static and docs gates, deadline-contract probe, finding evidence, tool identity and clone integrity.
- Host paths are redacted (`$PACKET`, `$CLONE`, `$DATA`, `$HOME`, `$IMAGE_LAYER`, `$PINNED_BIN`, `$TMP`).

## Real limits

- **Not run here:**
  - the full `milan_dp` default sweep, which exceeds one foreground command;
  - the full builder, parent, PP and gPTP banks;
  - Yosys, xvlog, behave and `run_all_suites.sh`;
  - act.

  I ran gmstep, option-off, aclk, render_mutants, all eleven gmstep controls plus three reviewer controls, tkdiag, the engine property probe, lint and the static and docs gates. The builder is unchanged since `a21cd358`. Its coverage at this head rests on the hosted `elaborate` and `docs-check` successes and on the manager's stated source banks, which I did not re-run.
- **The GNU make 4.3 binary** is a distribution build taken from a local image layer (sha256 in `receipts/tool_identity.txt`). The hosted runner's make version was not read directly.
- **Standards text.** Standards clauses were read as quoted in the tree and the decisions, not from the standards documents.
- **Not claimed.** Physical calibration and the #117 two-board handover (acceptance 4) were NOT RUN and are not claimed. Field skips are not hardware proof.
- **Clone integrity.** The review clone is byte-exact at the head (`receipts/review_clone_integrity.txt`):
  - HEAD `0f003fab`, and `write-tree` equals `c8af797b`;
  - empty `status --ignored`;
  - no assume-unchanged or skip-worktree flags;
  - 887 tracked entries with 0 byte or mode mismatches;
  - gitlinks `gptp-processor` e5dcea6e, `protocol-processor` 09f9bf38 and `third_party/verilog-axis` 48ff7a7e are clean at their pins, with `external` uninitialised as at the start.

  Every build and probe ran in a copy under the unpublished scratch directory. The static and docs gates ran read-only in the clone. Verilator 5.050 rev v5.050 was used, with at most 8 jobs.

## Pending manager duties

- Obtain the F1 prose correction, then commission a re-review of the corrected head. The Docs lens re-covers there; the other four lenses are banked at this head, and a prose-only change does not touch their scope.
- Build and validate the final current-dev candidate: source base `57456af9`, live dev `573f0052`.
- Own the hosted and act acceptance. The exact-head shard 4/5 window of 2454.1 s leaves 31.8% of 3600 s. Re-check it against decision 5820240308's 10% level at the candidate.
- Run the #117 bench step (acceptance 4) after merge.

R276-6 FINISHED
