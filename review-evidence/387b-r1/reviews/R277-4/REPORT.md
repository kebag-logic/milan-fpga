[R277] NEGATIVE - exact head a21cd3585abdd3cdf4ac5774a048361a66fed043

Round R277-4, external independent review of issue #387 / PR #555 (acceptance 3, datapath half). Head `a21cd3585abdd3cdf4ac5774a048361a66fed043`, tree `5376deee90b2e0732f533f287daaf7dfc666f32e`, reviewed range `57456af96b3127b9d309a995bbbd35a6113ce52d..a21cd358` (10 commits, 22 files).

Sources, in reading order: AGENTS.md, CONTRIBUTING.md, the issue body, and the decisions and rulings on the issue (5606198212 part b, 5794731090, 5802264260 items 1-2, 5810378282, 5818091077, 5819379503). Then the linked docs, the diff and its history, and executable evidence this reviewer ran. The verdict and ledger were written before the prior public findings were read. Their disposition is in its own section below.

Two MINOR findings. Both concern how the sweep's cost is run and recorded. The RTL, the conformance reading and the new checks hold. Lenses covered: Conformance, RTL, Robustness, Tests, Docs.

## Findings

### F1 MINOR - Tests - `tb/verilator/milan_dp/gmstep_mutants.py:185-196` - in the hosted sweep the freshness check always says "stale", so every sweep elaborates the clean gmstep leg a second time

- Authority/evidence: `is_fresh()` runs `make -s -C <suite> print-srcs` and treats every whitespace token of its stdout as an input path (`:189-193`).
  - The sweep starts this runner from a recipe of a parent `make -C` that prints its directory; the hosted log opens `make: Entering directory ...`. Under GNU make 4.3 the child then prints `make[1]: Entering directory '...'` on stdout despite `-s`.
  - The tokens `make[1]:`, `Entering`, ... are not files, so `is_fresh()` returns False for a binary built seconds earlier.
  - Hosted, exact head: run 36038109516, job 107763352706 (shard 4/5, suite artifact `suite-logs-4`, candidate merge `998393f6`). `receipts/hosted_head_suite_milan_dp.log:17093` prints `[INFO] obj_gmstep/Vmilan_dp_gmstep is missing or older than its sources: the positive control is rebuilt`. Yet `make run` built `obj_gmstep` itself earlier in the same recipe (`:1077-1581`).
  - Reproduced with `scripts/repro_gmstep_freshness.sh` on a built tree (`receipts/repro_gmstep_freshness.txt`). Under GNU make 4.3, inside a parent `make -C` recipe, the first tokens are `['make[1]:', 'Entering', 'directory']` and `is_fresh: False`. Run directly, or under GNU make 4.4.1, the result is `is_fresh: True`, which is why a local run does not show the defect.
  - The check was introduced this round (`94e5ae74d`); the runner at `a9636e0f` had none.
- Impact:
  - Every hosted `milan_dp` run pays one extra `milan_datapath` elaboration: 30-36 s by the same log's Verilator walltimes, inside a suite whose measured margin at this head is under 10% (F2).
  - The docstring (`:17-20`) and the README (`tb/verilator/milan_dp/README.md:502-503`) say a clean binary is rebuilt only when it is older than its inputs. In the sweep every clean binary is rebuilt.
  - The `option-off` leg's positive control under `make gmstep-mutants` has the same defect.
  - The failure mode is safe: the rebuilt positive control is still graded, so nothing goes falsely green.
- Required outcome: the runner reads the recipe's input list correctly whatever the make version and nesting, so a fresh clean binary is graded rather than rebuilt.
- Verification: `scripts/repro_gmstep_freshness.sh <tree> <GNU make 4.3>` prints `is_fresh: True` inside the parent recipe. The next exact-head hosted `milan_dp` log has no `[INFO] obj_gmstep ... rebuilt` line.

### F2 MINOR - Docs, Tests - `docs/testing/CI_WORKFLOWS.md:169-175` (and the PR's "Known limitations") - the recorded `milan_dp` margin is not the head's, and the head's hosted sample is under the decided 10% revisit level

- Authority/evidence:
  - The page and the PR record the hosted shard 4/5 window at `a9636e0f`: 2264.9 s, which leaves 435 s (16%) of the 2700 s budget.
  - Decision 5819379503 item 2 keeps the three controls in `run` on that basis, and adds: "If a later change brings it under 10%, the budget or the split is revisited."
  - Measured the same way (from the `shard: 4/5` line to `PASS milan_dp`) at the exact head, run 36038109516, job 107763352706: **2459.9 s, 9781 checks, which leaves 240.1 s = 8.9% of 2700 s** (`receipts/hosted_milan_dp_window.txt`). The `a9636e0f` figure reproduces from its own job log (2264.9 s).
  - Each figure is one sample. Of the 195 s rise, about 30-36 s is F1's extra elaboration. The head's other additions (six checks and two 4096-cycle settles in three short legs) are negligible, so the rest is runner variance.
- Impact:
  - The committed page and the PR overstate the head's measured margin by about 195 s.
  - On the evidence recorded for this head, the manager's own revisit condition is met.
  - A `milan_dp` timeout (exit 92) turns a required context red. The page already records two runs of the older class killed 1 s and 13 s short of their deadline.
- Required outcome: the decision owner applies decision 5819379503 item 2 to the margin measured at the head. Either revisit the budget or the split, or show a margin of at least 10% at the merge candidate (for example after F1 is fixed). `CI_WORKFLOWS.md` and the PR text record the exact-head figure they rely on.
- Verification: an exact-head (or candidate) hosted shard 4/5 window is recorded on the page. Either that window leaves at least 270 s, or a recorded maintainer decision on the budget or split exists.

### S1 SUGGESTION - Docs - PR #555 body

Three passages predate decision 5819379503, which ruled option (a) (report = launched) and kept the three controls in `run`:

- "Decision 1 ... Decision requested: the probe conflict";
- the Status bullet "Open: ... P1 is not clean";
- the Definition of Done item "the probe conflict awaits a decision".

The PR text could cite that decision. The issue carries it, so a cold reader can still recover it.

### S2 SUGGESTION - Tests - `hdl/ieee1722/avtp/KL_media_clock_restart.sv:237`

No check fails without the `streaming_i[t]` term of the wire-boundary condition: a planted engine without it passes tkdiag 96/96 (`receipts/tkdiag_extra_mutants.txt`, `no_streaming_term`).

- The term only matters in the one cycle a stream stops while `hold_r == 0`.
- There it keeps the stopped talker on the rule every non-streaming talker follows (track the target).
- I found no listener-visible effect, so this is not a defect.

A one-line comment, or a tkdiag arm, would record why the term is there.

## What was checked, per lens (artifact at this head)

- `[R277] PASS Conformance - hdl/milan/milan_datapath.sv:3110-3113, hdl/ieee1722/avtp/KL_media_clock_restart.sv:55-103,:225-257, hdl/ieee1722/aaf/KL_render_setpoint.sv:81-89,:169-173, tb/verilator/milan_dp/sim_gmstep.cpp:963-1025 - checked against IEEE 1722-2016 4.4.4.3 (level toggle, >= 8 AVTPDU hold, "each time a media clock restart is needed"), 10.4.3, Milan Table 5.4 MEDIA_RESET, decision part b, owner decision 5794731090, rulings 5802264260 items 1-2, 5818091077 and 5819379503 item 1, and aligner decision 5810378282.`
  - Trigger set: `media_rebase_p_w` is exactly the set that raises `tu` (`:1941-1943`: a settime; the plane's step, or a CLKV adjtime with the plane off). It joins `mcr_restart_p_w` ungated by the clock source. The CRF disruption and the echo stay gated, as 10.4.3 scopes them.
  - Render stage: its trigger set is the step plus the settled source change. No aligner, servo or grid RTL changed.
  - gmstep at every accept phase: the leg passes 48/48 at all 42 feed delays, with one re-base at step pulse +132 cycles and one `mr` toggle at +75 to +116 (`receipts/gmstep_delays/summary.txt`). This confirms the `GM_LOSS_RECOVERY.md` figures at the head.
  - Pending window: a request stays pending until the first PDU at the adopted level is reported, as ruled. My own randomized property probe checks four properties: one toggle per unmerged need, no lost and no spurious toggle, the 8-PDU hold, and MEDIA_RESET equal to the toggles. It is clean over 36 runs at report latencies 0, 1 and 3, with bursts and source changes (`receipts/probe_mcr_property_head.txt`).
  - Opposite levels: two streams ending on opposite levels breaks no clause. 4.4.4.3 defines `mr` and its hold per stream.
- `[R277] PASS RTL - hdl/ieee1722/avtp/KL_media_clock_restart.sv:200-259, hdl/milan/milan_datapath.sv:3062-3160,:6017-6028, tb/verilator/milan_dp/sim_nxn.cpp:3105-3109 - per-bit NBA override order, same-cycle request/adopt/report interactions, widths, clock domain and reset.`
  - Target width and NBA order: `tgt_r` is widened to `N_TALKERS_P` bits. The whole-vector NBA and the later per-bit NBA resolve last-wins per bit.
  - Same-cycle cases, each traced to one toggle: a request with an adoption; a request with the first report; an adoption with an old-level report.
  - Clock domain: every new term is an `axis_clk` pulse. `cfg_ptp_cmd_load` and `cfg_ptp_cmd_adjust` are one-cycle CSR strobes, and `gptp_step_we_w` already drove `KL_ptp_clock_validity` on `axis_clk`. There is no new CDC.
  - Lint: Verilator 5.050 `-Wall` is clean at `N_TALKERS_P` 1, 3, 5 and 16, apart from the unchanged GENUNNAMED lines 191 and 194 (`receipts/lint_mcr.txt`). `lint_rtl.py --check` passes, 90 <= 90 (`receipts/lint_rtl_check.txt`).
  - `sim_nxn`: the injection mask `(1u << (kNstreamsTb + 1)) - 1u` matches `MCR_CTX_C = N_STREAMS + 1` on every leg.
- `[R277] PASS Robustness - scripts/probe_mcr_property.cpp + receipts/probe_mcr_property_head.txt, receipts/option_off.log, receipts/ax1x1.log - request storms, bursts, source changes, report latency, the feature-off shape and the INTERNAL clock.`
  - Stimulus: about 3,000 requests per 400k-cycle run. A third of them have a second request 1-400 cycles behind, and about 1 in 8 requests is a source change. AAF and CRF rates (19-, 23- and 311-cycle periods) share one feed. All four properties hold.
  - Feature-off and INTERNAL: the feature-off shape (`GPTP_PLANE_EN_P = 0`) and the INTERNAL clock pass, option-off 233/0 and ax1x1 230/0, including the settime toggle and its MEDIA_RESET.
  - Reset and non-streaming behaviour are unchanged from base. The stop-cycle corner is S2, and it is not a defect.
- Tests: **UNCLEAN (F1, F2).** Also covered this round, with no further finding:
  - tkdiag: 96/96, and `mcr_mutants.py` 5/5 (`receipts/tkdiag_make.log`).
  - My extra engine mutants: a window one PDU too long, a source change that is not a request, and a 7-PDU hold. The committed harness catches each (`receipts/tkdiag_extra_mutants.txt`).
  - gmstep controls: `gmstep_mutants.py --all` gives 13/13, and each control breaks its named check (`receipts/gmstep_mutants_all.log`).
  - Probe teeth: my property probe kills the base dev engine and five planted engines, so it can fail (`receipts/probe_mcr_mutants.txt`).
  - The changed legacy check "keeps tv=1" now masks only `mr` (`& 0xF7`). A separate check grades `mr` against the harness's own step parity. That is stronger than the old `mr = 0`, and the CRF-gated control proves it can fail.
  - `measure_test_evidence.py --check` passes.
- Docs: **UNCLEAN (F2).** Checked, with no further finding:
  - The rows of `GM_LOSS_RECOVERY.md:142-208` reproduce at the head (see Conformance), and the aligner row is byte-identical to #539's.
  - Also read against the head: `TIME_SYNC.md:197` (render row), `REGISTER_MAP.md:126-131`, `TESTING.md:267,501`, the suite README, the CHANGELOG, `BAREMETAL_FIRMWARE.md:1193-1196,1236-1242`, and the banners at `KL_media_clock_restart.sv:55-103` and `KL_crf_tx.sv:53-60,148-152`.
  - `git grep` finds no stale pre-#387 statement outside history.
  - `docs_check.py` reports 0 findings, and `check_em_dash.py --base 57456af9` refuses 0 of 128 added lines (`receipts/docs_check.txt`, `receipts/check_em_dash.txt`).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | datapath `:3062-3160,:6017-6028`; `KL_media_clock_restart.sv`; `KL_render_setpoint.sv`; `sim_gmstep.cpp`; gmstep at 42 feed delays; property probe | R277-4 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| RTL | CLEAN | `KL_media_clock_restart.sv:200-259`; datapath re-base, restart and render wiring; `KL_crf_tx.sv` (comment only); lint at four widths; `lint_rtl --check` | R277-4 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| Robustness | CLEAN | property probe (storms, bursts, source changes, latency 0/1/3, mixed rates); option-off and ax1x1 legs; stop-cycle corner (S2) | R277-4 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| Tests | UNCLEAN (F1, F2) | tkdiag + `mcr_mutants.py`; reviewer engine mutants; `gmstep_mutants.py --all`; option-off and ax1x1; the changed tv/mr check; hosted exact-head `milan_dp` log | R277-4 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| Docs | UNCLEAN (F2) | `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md`, `CI_WORKFLOWS.md`, `BAREMETAL_FIRMWARE.md`, CHANGELOG, suite README, banners, PR body; `docs_check`, `check_em_dash` | R277-4 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |

## Disposition of prior public findings

These are the findings of R276-4 (https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5817943136) and R277-3 (https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5818080648), both at `e68c1b1a`. They were read after the verdict and ledger above were written. None of them changed the verdict.

| Prior finding | Disposition at `a21cd358` | Evidence |
|---|---|---|
| R276-4 F1 = R277-3 F1 (BLOCKER, builder gate 1b pins the pre-#387 render trigger) | **Resolved** | `sw/builder/test_builder.py:8794-8887` pins `media_rebase_p_w`, `mcr_restart_p_w`, the render initializer and the direct `restart_p_i` port, and the census counts. Seven refusal entries are added (`:10308-10358`, `:12621-12653`). Exact-head hosted `elaborate` (job 107763180996) and `docs-check` (job 107763181412) succeed. This reviewer did not run the builder bank (not allowed this round); the manager's source banks cover it. |
| R276-4 F2 = R277-3 F3 (MINOR, the pending boundary is the adoption, not the wire) | **Resolved** | Ruling 5818091077 set the boundary on the wire. `KL_media_clock_restart.sv:236-238` keeps a streaming talker pending while `hold_r == 0`. T17 and T18 grade both sides, and four mutants fail them. Decision 5819379503 item 1 rules the feed report as "launched", and the banner (`:79-91`) documents the residue. My independent probe, graded at the report, gives P1-P4 clean. |
| R276-4 F3 = R277-3 F4 (MINOR, the render-stage banner and port spec name the GM identity) | **Resolved** | `KL_render_setpoint.sv:81-89` and `:169-173` name the step and the settled source change. |
| R277-3 F2 (MINOR, no check fails when a settime does not toggle `mr`) | **Resolved** | `sim_main.cpp:1028-1072` adds two checks. The `settime_no_mr` control is caught in my `gmstep_mutants.py --all` run and breaks both new checks (`receipts/gmstep_mutants_all.log`). The checks run in the sweep's three `sim_main` legs. |
| R276-4 F4 (MINOR) and R277-3 S1 (the `milan_dp` margin rests on a stale figure) | **Retained in changed form as this round's F2** | The page now records measured hosted figures, but from `a9636e0f`. The exact-head sample is 2459.9 s: 240.1 s (8.9%) of margin, under the 10% level of decision 5819379503. R276-4's projection of about 280-320 s was in the right range. |
| R276-4 S1 = R277-3 S2 (PR status names an old head) | Resolved | The status names `a21cd358`. It carries a new staleness about decision 5819379503, which is this round's S1. |
| R276-4 S2 = R277-3 S4 (a stale positive control can be graded) | Resolved for a direct run | The added freshness check is this round's F1: in the hosted sweep it reports every binary as stale. |
| R277-3 S3 (INTERNAL-source citation) | Resolved | The `GM_LOSS_RECOVERY.md` `mr` row cites the option-off legs and the CRF-gated control. |

## Judgments requested by the assignment

- **1722-2016 4.4.4.3 and Milan Table 5.4: conformant.** Each step is one requested restart, and the 8-PDU hold is kept. MEDIA_RESET counts the toggle each stream transmits, per interval as before. These are the Conformance and Robustness lines above.
- **"Pending = requested but not on the wire": implemented as ruled**, with the wire measured at the transmitted-PDU report (decision 5819379503 item 1). The residue is at most one PDU's launch-to-report time per restart, and it is documented.
- **Streams ending on opposite `mr` levels: acceptable.** `mr` is a per-stream field with a per-stream hold (4.4.4.3). 10.4.3 scopes validity to the stream a Listener recovers its clock from, and no clause relates two streams' levels.
- **Changed legacy tv/mr check: not weakened.** Only `mr` is masked, `& 0xF7`, and `mr` gets its own harness-owned expectation, which a planted control kills.
- **Sweep time: see F1 and F2.** The +182 s local figure matches this reviewer's local runs: gmstep leg with build about 37 s, `--all` 413 s. On the hosted runner, the exact-head sample leaves 240.1 s (8.9%) of 2700 s.
- **#387 part b aligner decision: untouched.** No aligner, grid, NCO or servo RTL is in the diff. The aligner row of `GM_LOSS_RECOVERY.md` is #539's text unchanged, and the gmstep README bullet keeps the decision.

## Real limits

- Physical calibration was NOT RUN. Acceptance 4, the #117 two-board handover, is not evidenced, and no field skip is hardware proof.
- Not run here, by the round's rules: the full `milan_dp` `run` sweep, the builder, PP, gPTP and Yosys banks, `run_all_suites.sh`, act/Docker, and hardware. The `milan_dp` legs this reviewer ran were:
  - `gmstep`, at all 42 feed delays;
  - `gmstep_mutants.py --all`;
  - `option-off`;
  - `ax1x1`.
  
  The sweep's other legs rest on the manager's source banks and the exact-head hosted shard 4/5, which is green with 9781 checks.
- Hosted margin figures are one sample per head. Runner variance of at least 30-40 s between samples is visible in the dev pair.
- F1 was reproduced with a GNU make 4.3 binary on this host, and the exact-head hosted log confirms the effect. The hosted runner's make version was not read directly.
- The property probe models the talker-to-feed path (launch latches `mr_o`, report after 0-3 cycles, one report per cycle). It does not elaborate the packetizers.
- The IEEE and Milan texts were read as quoted in the tree and in the issue. No standards document was available on this host.
- The hosted suite artifact `suite-logs-4` is copied as `receipts/hosted_head_suite_milan_dp.log`. Its `TARGET_SHA` is the candidate merge `998393f6`, not the head itself.

## Pending manager duties

- Rule on F2 under decision 5819379503 item 2: revisit the budget or the split, or re-measure at the merge candidate after F1.
- Decide F1's fix owner.
- Build and validate the final current-dev candidate (live dev `573f0052`) at the merge turn.
- Hosted and act acceptance on the exact candidate. The `verilator-suites` and `yosys-portability` aggregator jobs at this head succeeded (9 s each); the physical gPTP job was skipped by design.
- Obtain two positive reviews and a reviewer-owned ledger covering all five lenses at the merge candidate.
- Acceptance 4 (#117 bench) after merge. Post-merge containment.

## Clone integrity

- After all probes, the review clone is at `a21cd3585abdd3cdf4ac5774a048361a66fed043`, tree `5376deee90b2e0732f533f287daaf7dfc666f32e`, with no untracked or ignored entries.
- All 883 tracked blobs were re-hashed with `--no-filters` and match HEAD, modes included. The index equals the HEAD tree: 887 entries, all at stage 0.
- `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are at their gitlinks with clean worktrees. `external` was uninitialised at the start and still is; it is not a required submodule.
- All builds and probes ran in a disposable clone under `scratch/`, which is not published (`receipts/clone_integrity.txt`).

## Receipts

Every file below is listed in `MANIFEST.sha256`. Local absolute paths in the logs are replaced by `<packet>`, `<review-clone>`, `<pinned-tool-bin>` and `$HOME`.

- `scripts/`:
  - `probe_mcr_property.cpp`, `run_probe_mcr_property.sh`: the property probe and its driver.
  - `probe_mcr_mutants.py`: the probe's own kill check.
  - `tkdiag_extra_mutants.sh`: reviewer engine mutants against the committed harness.
  - `repro_gmstep_freshness.sh`: the F1 reproduction.
- `receipts/`, local runs:
  - `tkdiag_make.log`, `tkdiag_extra_mutants.txt`;
  - `gmstep_d0.log`, `gmstep_delays/` (`summary.txt`, `rc.txt`, `d0.log`..`d41.log`), `gmstep_mutants_all.log`;
  - `option_off.log`, `ax1x1.log`;
  - `probe_mcr_property_head.txt`, `probe_mcr_mutants.txt`;
  - `lint_mcr.txt`, `lint_rtl_check.txt`, `measure_test_evidence_check.txt`, `docs_check.txt`, `check_em_dash.txt`;
  - `repro_gmstep_freshness.txt`.
- `receipts/`, hosted evidence and tooling:
  - `hosted_jobs_head.txt`, `hosted_milan_dp_window.txt`;
  - `hosted_head_suite_milan_dp.log`, `hosted_head_suite_TARGET_SHA`, `hosted_head_gmstep_rebuild_lines.txt`;
  - `verilator_identity.txt`, `clone_integrity.txt`.

R277-4 FINISHED
