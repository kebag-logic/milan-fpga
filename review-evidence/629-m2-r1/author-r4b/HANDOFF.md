# HANDOFF: lane M2 round 4b ([A517]), issue #629, PR #634

Status: REVIEW READY at `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` (two commits on `c1288648`; local, not pushed). Every item done; every gate and re-run rc 0 at that head; no STOP condition; no open finding of this round's.

- Start head: `c12886486c1e4acf2003bfaba25db2a307446428` on `629-media-clock-impl` (round 4, the merge of dev `1269cdaf`).
- Head: `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee`, two commits on `c1288648`, none amended; local, not pushed.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5966355350
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5966361517
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5966931872
- Live `dev`: `1269cdafb4bb964c757baae0f0c5a932d43f540b`, unchanged since round 4 (`git ls-remote origin dev` at the start). PR #634's recorded base oid is `cdf49d1a` (frozen at open); its pushed head is still round 3's `0b066b6e`.

## Items

| # | Item | Commit | State |
|---|---|---|---|
| 1 | Fix the `gmstep-mutants --all` control (F-A512-1) so it plants its defect on the reshaped restart request; check the render, crflic and gsi controls against that request the same way | `917a78ec6df69aaa6b37a64119101d3c08cc1992` | done: `gmstep-mutants --all` **22/22**; the control breaks exactly 1 check, its named one; the 45 control anchors of the five `milan_dp` campaigns checked, none of the render, render-csr, crflic or gsi anchors lies in the request or on a line this lane changed; every campaign green |
| 2 | RESIDUE R432-3-R1 = R433-3-R1: the design page's "The last two" sentence, in the reviewers' exact text | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` | done: exact text present once, "The last two" gone |
| 3 | Re-run what the change touches: the `milan_dp` suite and every `milan_dp` campaign with `--all`; the hosted Verilator shard holding `milan_dp` and the docs gates under GNU make 4.3 | (no tree change) | shard 4 rc 0 (1/1 suite, 11,839 checks, 0 failures; sweep campaigns 6/6 and 6/6); `crflic-mutants` 7/7, `gsi-mutants` 9/9, `gmstep-mutants` (`--all`) 22/22, `render-csr-controls` 4 checks 0 failures; `docs.yml` `docs-check` (46 of 46 run steps, entity shape 222/0), `wire-accountability` (77/0) and `docs-check-no-git` rc 0 under make 4.3; light gates 31/31 rc 0 |

No RTL change: `git diff --name-only c1288648 HEAD -- hdl sw syn configs constraints avdecc protocol-processor gptp-processor third_party external` is empty. The round's whole diff is two files, +9 / -7: `tb/verilator/milan_dp/gmstep_mutants.py` and `docs/design/MEDIA_CLOCK_FOLLOWING.md`. Round 4's shipping image stands.

## Item 1: the control fix

**Change** (`917a78ec6`, `tb/verilator/milan_dp/gmstep_mutants.py`):
- `:231-232`: the control "a PHC step suppresses a coincident CRF restart" now anchors on `CRF_RESTART_TERMS` (`:68`, the selected CRF stream's two terms) and plants `CRF_RESTART_TERMS[:-1] + " & ~media_rebase_p_w)"`. Round 4 anchored it on `RESTART_TRIGGER` (`:64`, the request's last line) with `RESTART_TRIGGER[:-1] + " & ~media_rebase_p_w;"`. Both are derived from the anchors already defined in the file; no literal is restated.
- `:65-67`: the comment on `CRF_RESTART_TERMS` now says why a veto goes there: on `RESTART_TRIGGER` the `&` binds to the AAF toggle alone. Two comment lines beyond the one-line fix the assignment names; they record the precedence trap beside the anchor that avoids it.

**The request and the planted forms** (`hdl/milan/milan_datapath.sv:3229-3232`, unchanged):

| Form | Request after planting | Selected-CRF-only requests suppressed when `media_rebase_p_w` = 1 / 0 | AAF-only requests suppressed when `media_rebase_p_w` = 1 |
|---|---|---|---|
| clean | `(crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) \| crf_mr_toggle_p_w)) \| aafm_disrupt_p_w \| aafm_mr_toggle_p_w` | - | - |
| round 4 (`RESTART_TRIGGER`) | `(...CRF terms...) \| aafm_disrupt_p_w \| aafm_mr_toggle_p_w & ~media_rebase_p_w` | 0 of 5 / 0 of 5 | 11 of 33 |
| round 4b (`CRF_RESTART_TERMS`) | `(crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) \| crf_mr_toggle_p_w) & ~media_rebase_p_w) \| aafm_disrupt_p_w \| aafm_mr_toggle_p_w` | **5 of 5** / 0 of 5 | **0 of 33** |

The figures are the probe's exhaustive truth table over the request's inputs (`scripts/restart_controls_probe.py`, `receipts/campaigns/restart_controls_probe.log`). The fixed form vetoes exactly the selected-CRF restart on a PHC re-base cycle and nothing else; that is the defect dev's control planted on dev's pure AND chain (`crf_clk_selected_r & (...) & ~media_rebase_p_w`). The round 4 form vetoed only the AAF toggle, which the gmstep leg (CRF selected) never raises, so it was the clean design there.

**Clause.** The check this control guards, "coincident: a PHC step does not suppress the CRF restart" (`tb/verilator/milan_dp/sim_gmstep.cpp:1164`), grades IEEE 1722-2016 4.4.4.3 (third paragraph: streams deriving timestamps from a received CRF stream "shall toggle the mr bit if a disruption of the CRF stream occurs or if the mr bit in the CRF stream has been toggled") and 10.4.3 (the CRF Listener shall toggle `mr` in outgoing media streams deriving timestamps from it), as kept by the #602 ruling: a PHC-only re-base is no `mr` cause, but selected-CRF disruption and `mr` propagation still request a restart "even alongside a PHC step" (`milan_datapath.sv:3212-3214`).

**Result** (`make -C tb/verilator/milan_dp gmstep-mutants`, GNU make 4.3, pinned Verilator 5.050, head `2bc5adc0`, `receipts/campaigns/milan_dp_gmstep-mutants.log`): rc 0, **22 checks: 22 PASS, 0 FAIL**. The fixed control: "[PASS] control caught: a PHC step suppresses a coincident CRF restart - breaks "coincident: a PHC step does not suppress the CRF restart"", "it broke 1 check(s): coincident: a PHC step does not suppress the CRF restart". Round 4 at `c1288648`: 21/22, this control SURVIVED.

**The other campaigns against the reshaped request.** The probe reads every control's anchor and replacement from the campaign scripts themselves (`render_csr_controls.py`'s from its own text) and reports, at `2bc5adc0` against the lane's delta from `1269cdaf`: the anchor's count and line span, whether it lies inside the request (`:3229-3232`), whether it touches a line this lane changed, and for each control that edits the request, the planted request and its truth table. 45 anchors, each found exactly once; the log's 46th row is round 4's form of the veto, kept for the contrast.

| Campaign | Controls (anchors) | Inside the request | On a line this lane changed | Verdict |
|---|---|---|---|---|
| `render_mutants.py` (sweep) | 4 (4): 3 in `KL_render_setpoint.sv`, 1 in the datapath's render trigger `:6323` | none | none | not reshaped. The datapath control removes `src_recentre_p_r` at its one consumer, `render_recentre_p_w` (`:6321-6323`). This lane changed only that term's settle gate, `crf_clk_selected_r` to `follow_sel_r` (`:6276`, `:6300`); removing the term still drops the clock-source trigger whole. 6/6 in shard 4 |
| `render_csr_controls.py` | 3 (3): `milan_datapath.sv:6455`, `milan_csr.sv:2424`, and the `KL_render_setpoint` instance `:6458-6495` cut whole | none | none | not reshaped; 4 checks, 0 failures |
| `crflic_mutants.py` | 6 (6): the talker gates `:1997`, `:5434`, `:6920-6921` | none | none | not reshaped; 7/7 |
| `gsi_mutants.py` | 8 (11): 10 in the processor top at `631eeb34` (a copy), 1 in the datapath `:4936-4937` | none | none | not reshaped; 9/9 |
| `gmstep_mutants.py` | 20 (20) | 8: the four PHC-cause restorations at `:3232`, the CRF-propagation removal and the coincident veto at `:3231`, the two delayed adjtime causes over `:3229-3232` | the same 8 (round 1 wrote the request) | the six OR-appended causes (four restorations, two delayed) each OR into the whole request and suppress nothing (truth tables of the four: 0 suppressed; the two delayed append the same `| <cause>`); the CRF-propagation removal suppresses the 3 of 5 selected-CRF requests that only the received toggle raises; the coincident veto is fixed as above. 22/22 |

So the coincident veto was the only control whose operator binding the reshaped request changed. Every other control that edits the request appends `| <cause>`, which binds to the whole request, or rewrites the CRF term group in place.

## Item 2: the design page

`docs/design/MEDIA_CLOCK_FOLLOWING.md:1000-1003` (`2bc5adc0b`): "The last two are the bench's measurement of a talker's timestamp regularity." is replaced by the reviewers' exact text, "The history-restart count and the largest deviation are the bench's measurement of a talker's timestamp regularity." (R432-3-R1, R433-3-R1, identical wording). Lines `1000-1003` are re-wrapped to the paragraph's width; the following sentence is unchanged. Whitespace-normalized, the replacement occurs once and "The last two" zero times. No other copy of the sentence exists outside the submodules.

## Item 3: re-runs

### The hosted Verilator shard holding `milan_dp`, under GNU make 4.3

`rtl.yml` `verilator-shards` with `shard=4`, `total=5`, replayed at `2bc5adc0` by round 4's driver (`scripts/replay_workflow.py`, paths adapted; `scripts/run_job.sh`, `scripts/shard4.sh`): every `run:` step verbatim with `bash -e`, the workflow, job and step env and the pull_request expressions resolved. A `make` shim first on PATH logs each call and execs GNU make 4.3, built here from the GNU tarball (sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19`, binary sha256 `547f2c100f47fb603a5d32e22f1b87fe1c7f564b369d72669394460b1b378209`). A fresh Python 3.12.13 venv with PyYAML 6.0.3 stands in for the runner's `python3`; `/opt/verilator` maps to a local Verilator 5.050 install.

| Job | Steps: verbatim (of them path-mapped) / substituted; actions; skipped by `if:` | make calls, all GNU make 4.3 | Result |
|---|---|---|---|
| rtl.yml `verilator-shards` (shard 4) | 14: 5 (1) / 0; 3; 6 | 34 (step 13) | rc 0: 1/1 suite, `milan_dp` PASS, **11,839 checks, 0 failures** (round 4's tally), 1,772.7 s |

Inside it (`receipts/replay/vshard4.milan_dp.excerpt.log`; the full log is 2,060,966 B, sha256 `e6d8486838fd4ca8f7ded2738dbb12c4d66aa5e4c4851050802016365aacb669`): `obj_gptp` 182/0, `obj_gptplat` 182/0, gmstep 104/0, `obj_dir` 236/0, notify 383/0, crflic 416/0, nxn 1,961/0, nxndv 1,961/0, nxn8 3,746/0, nxn4c 1,961/0, nolpf 236/0, prune 33/0, ax1x1 233/0, media_aclk 193/0; `render_mutants.py` **6 checks: 6 PASS** and `gmstep_mutants.py` (the sweep's default inventory) **6 checks: 6 PASS**. The legs and the two campaigns sum to 11,839. Every `[CLKSRC-WALK]` and `[CLKSRC-RANGE]` line reads `ok` (264 result lines in the excerpt).

Build state: before the shard, `git clean -fdX -- tb/verilator/milan_dp/` removed the suite's 20 ignored build products (listed first with `-n`, `logs/clean_milan_dp.dryrun.txt` in scratch), so every leg built from this head as on a fresh runner.

Launch artifact, disclosed: the first launch (08:34) ran the sequence under `setsid nohup`. `nohup` leaves SIGHUP ignored in every child, so the sweep's preflight control `test_suite_cancellation.py` "hard-HUP" could not stop its probe sweep and timed out after 12 s; step 13 aborted rc 2 after 46 s with "ABORTING: sweep cancellation controls failed" before any suite ran (`receipts/replay/vshard4.nohup-attempt.log`, `.step13.log`). The tree was clean after it. The relaunch (08:36, SIGHUP not ignored) passed the preflight and is the reported run.

### `milan_dp`'s explicit campaigns

Each by its documented command, `make -C tb/verilator/milan_dp <target>`, after shard 4 (they reuse its clean legs), under GNU make 4.3 with the pinned Verilator 5.050 first on PATH (`scripts/campaign.sh`). `gmstep-mutants` ran beside the chain `crflic-mutants`, `gsi-mutants`, `render-csr-controls` (separate build directories; the shared ROM and shape prerequisites were already current). Peak sampled memory 6.6 GB (2.9 GB anonymous) of the 12 GB cap, no OOM kill.

| Campaign | Command | Result | Log |
|---|---|---|---|
| gmstep, whole inventory (`--all`) | `make ... gmstep-mutants` | rc 0, **22 checks: 22 PASS**: both clean legs pass, 20 controls caught | `receipts/campaigns/milan_dp_gmstep-mutants.log` |
| crflic licence | `make ... crflic-mutants` | rc 0, **7 checks: 7 PASS**: the clean `obj_crflic` leg, 6 mutants | `milan_dp_crflic-mutants.log` |
| GET_STREAM_INFO seam | `make ... gsi-mutants` | rc 0, **9 checks: 9 PASS**: the clean `obj_notify` leg, 8 mutants (processor half planted in copies of its `hdl/` at `631eeb34`) | `milan_dp_gsi-mutants.log` |
| render CSR | `make ... render-csr-controls` | rc 0, **4 checks, 0 failures**: clean, `wrong_fill` and `bit9_window_selection` caught by their named checks, `absent_stage` passes as designed | `milan_dp_render-csr-controls.log` |
| render law (sweep) | inside shard 4's `make` | **6 checks: 6 PASS** | `receipts/replay/vshard4.milan_dp.excerpt.log` |
| gmstep, acceptance inventory (sweep) | inside shard 4's `make` | **6 checks: 6 PASS** | the same |

`render-csr-controls` is an explicit `milan_dp` campaign (`docs/testing/TESTING.md:269`) owed by changes to `milan_csr.sv` or `sim_aclk.cpp`, both of which this lane changed in round 1. No earlier author packet of this lane (rounds 1 to 4) records a run of the campaign; round 2's `aclk1.log` holds only the clean leg's RENDER-CSR checks. It has no `--all` switch; only `gmstep_mutants.py` has one, and `make gmstep-mutants` passes it.

### The docs gates under GNU make 4.3

`docs.yml`'s three jobs, replayed the same way at `2bc5adc0` in sequence after the campaigns, because `docs-check`'s self-tests rewrite tracked files that the `milan_dp` builds read (`scripts/docs_jobs.sh`; 09:23:27 to 09:48:34). Each ran in its own scratch HOME.

| Job | Steps: verbatim (of them path-mapped) / substituted; actions; skipped by `if:` | make calls, all GNU make 4.3 | Result |
|---|---|---|---|
| docs.yml `docs-check` | 50: 43 (0) / 3; 4; 0 | 2,947 (step 19: 1, 25: 1,031, 26: 1,538, 31: 14, 50: 363) | rc 0, 46 of 46 run steps PASS. Step 9 em-dash: 0 findings over 541 added lines `[1269cdaf..HEAD]` (base derived from `origin/dev`). Step 26 builder gates: `ALL GATES PASS EXCEPT 14 NOT RUN` (the LiteX arms; the hosted job has no LiteX either). Step 43: NOT RUN (AGENTS.md section 5); `scripts/act_ci.py` is byte-identical to live dev `1269cdaf`. Step 50 `check_entity_shape.py --self-test`: 222 checks, 0 failures, 363 make calls |
| docs.yml `wire-accountability` | 3: 2 (0) / 0; 1; 0 | 0 | rc 0, 77 checks, 0 findings |
| docs.yml `docs-check-no-git` | 2: 0 (0) / 1; 1; 0 | 0 | rc 0 in a `git archive` export of the head: `docs_check` 0 findings across 186 md files (inventory parity skipped without git, as designed), `feature_status` 0 findings |

The three substituted `docs-check` steps are round 4's: step 7, the diagram dependencies (a presence check plus the workflow's pip line); step 21, the pinned sv2v release (same zip and digest, into the replay's own bin); and step 43. `git status --porcelain` was empty after the sequence.

## Test rows and failing mutants

Round 4b adds no test and changes one control's anchor. Every control of every `milan_dp` campaign, with the check it fails, at `2bc5adc0`:

`gmstep-mutants` (`--all`), 20 controls (the sweep runs the five marked S, plus its clean gmstep leg):

| Control | Named check it fails | Checks it broke |
|---|---|---|
| the policy level is tied low at the servo | slew path: the actual servo receives the level | 2 |
| the policy level omits the applied-rate tail | slew path: every staged sample covers the PHC tail | 1 |
| the policy level misses an extra addend stage | slew path: every staged sample covers the PHC tail | 1 |
| the PHC re-base restart term is restored (S) | restart: a PHC-only step leaves outgoing mr unchanged | 2 |
| the source-change term is removed (S) | source control: a real source change toggles mr once | 1 |
| selected CRF mr propagation is removed (S) | CRF control: selected CRF mr propagates exactly once | 2 (with "coincident: ... does not suppress the CRF restart") |
| the grandmaster identity re-bases the render stage as well as the step (S) | render: the GM change is one counted re-base event | 2 |
| the step does not re-centre the render stage (S) | render: the GM change is one counted re-base event | 1 |
| the render re-base is keyed to the identity, not the step | render: every counted re-base lands at a PDU end right after the step | 1 |
| tu reaches the talkers four cycles late | tu: set in the first cycle the bank names GM B | 1 |
| the plane's step does not re-arm the holdover | tu: held at least the 0.25 s holdover after the step | 1 |
| tu stops the talker | licence: the talker never pauses beyond four of its intervals | 6 |
| the grandmaster change stops the talker for good | licence: the talker never pauses beyond four of its intervals | 8 |
| the step's re-centre snaps one event off the setpoint | render: every PDU push leaves the target fill across the event | 1 |
| software settime is restored as an mr cause (option-off leg) | CLKV: the settime leaves mr unchanged (#602) | 2 |
| PHC adjtime is restored as an mr cause (option-off) | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1 |
| both PHC restart causes are restored (option-off) | CLKV: the settime leaves mr unchanged (#602) | 3 |
| PHC adjtime becomes an mr cause 16 cycles later (option-off) | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1 |
| PHC adjtime becomes an mr cause 256 cycles later (option-off) | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1 |
| **a PHC step suppresses a coincident CRF restart** (fixed) | **coincident: a PHC step does not suppress the CRF restart** | **1** |

`render_mutants.py` (sweep): prefill target three events high, "RENDER-INT: every PDU's first event inside the law band"; recentre pulse ignored, "RENDER-RC-INT: ... (late)"; recentre counted and cleared but not snapped, "RENDER-RC-INT: ... (early)"; clock-source trigger dropped from the recentre set, "RENDER-LIVE-CRF: the fill at accept is the setpoint for every PDU"; and the clean leg in both short modes.

`render-csr-controls`: wrong_fill, "RENDER-CSR: filling mirrors taps" (got 256, exp 262); bit9_window_selection, "RENDER-CSR: bit 9 preserves talker rejection" (got 65550, exp 0); absent_stage passes with the CSR structurally zero.

`crflic-mutants`: every gate reads the raw verdict, "the CRF licence never opened (every cycle sampled)"; the CRF licence alone reads the raw verdict, "the CRF licence equals ACTIVE[CRF] AND real grant"; the AAF source 0 gate alone reads the raw verdict, "the AAF gate never opened"; every gate drops the real grant, "refused CRF licence never opened"; the CRF licence alone drops the real grant, "refused CRF licence never opened"; the AAF source 0 gate alone drops the real grant, "refused AAF gate never opened".

`gsi-mutants`: failure bridge id tied to zero, "[GSI] G5 sink 0 Talker Failed: msrp_failure_bridge_id"; selector 5 back to the parent, the same check; failure code tied to zero, "[GSI] G5 sink 0 Talker Failed: msrp_failure_code"; failure-code byte left to the parent, "[GSI] G5 sink 1 Talker Failed: msrp_failure_code"; probing/ACMP status tied to zero, "[GSI] G2 sink 0 two probes unanswered: acmp_status"; the other sink's owners, "[GSI] G5 sink 0 beside the other sink's failure: msrp_failure_bridge_id"; the parent's selector-7 approximation, "[GSI] G1 sink 0 bound: probing_status"; the duplicated withdrawal push, "[GSI] G8 sink 0 withdrawn: unsolicited GET_STREAM_INFO(sink 0) to A".

## Area against the design estimate

No RTL change this round (`git diff c1288648 HEAD -- hdl` is empty). Re-measured at `2bc5adc0` anyway, after the docs jobs: `(cd syn/yosys && ./ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo)` (Yosys 0.66, `synth_xilinx -family xc7 -flatten`), rc 0 (`receipts/ooc_head.log`). Equal to round 4's figures.

| Block | LUT (LUTRAM) | FF | RAMB18 | DSP | Design estimate | Verdict |
|---|---:|---:|---:|---:|---|---|
| `KL_aaf_clock_meter` | 574 (16) | 636 | 0 | 0 | 380 to 580 LUT, 270 to 420 FF, 0 RAMB18 | LUT inside, FF over (accepted, #629 STOP ruling item 8) |
| `KL_mmcm_drp_servo` | 865 | 792 | 0 | 1 | 871 LUT, 792 FF at the design base | unchanged |

## Timing summary of the shipping image

Not rebuilt: the assignment rules no RTL change and no Vivado run, and no input of the image changed (the round's diff touches no file under `hdl`, `sw`, `syn`, `configs`, `constraints`, `avdecc` or any submodule). Round 4's image at `c1288648` stands: WNS **+0.193 ns**, TNS 0 (0 of 181,419 endpoints failing); WHS +0.024 ns; WPWS +0.264 ns; all four sign-off corners clean; 106,622 of 106,622 nets routed; 0 CRITICAL WARNING; #607 clean; slice LUTs 50,767 (80.07 %); slices 15,832 of 15,850 (**99.89 %**); bitstream sha256 `d2742a8652a114c65e1a352338efef570ad57bd708acd0788b0448b8204fc2ec` (round 4's receipts).

## Gates

All at the committed head `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee`, from the physical `$LANES/629-m2-impl` worktree, never piped, each to its own log (copies in `receipts/`, home prefix written `$HOME`). `git status --porcelain` was empty before and after every run, and the submodules stayed at their gitlinks (`gptp-processor` `5dce647a`, `protocol-processor` `631eeb34`, `third_party/verilog-axis` `48ff7a7e`; `external` not checked out, as before).

| Gate | Command | Make | Result |
|---|---|---|---|
| Markdown gates (pinned md venv) | `docs_check.py`; `check_doc_style.py`; `gen_toc.py --check`; `gen_toc.py --verify-anchors`; `check_em_dash.py --base` `1269cdaf`, `cdf49d1a` and `c1288648`; `check_doc_paths.py` | none | rc 0 each: 0 findings over 186 md files; 22 documents; 128 pages; 300 anchors; em-dash 0 findings over 541 / 609 / 4 added lines; 891 cited paths |
| `git diff --check` | worktree; `c1288648 HEAD`; `1269cdaf HEAD`; `cdf49d1a HEAD` | none | rc 0 each |
| Ratchets and records | `measure_test_evidence.py --check`; `check_hygiene.py --check`; `check_{py,sh,cpp,sv}_idiom.py`; `lint_rtl.py --check`; `measure_naming.py --check`; `check_port_contracts.py`; `measure_fail_fast.py --check`; `check_todo_ownership.py`; `check_rtl_source_lists.py`; `check_submodule_docs.py`; `submodule_boundaries.gen.py --check`; `check_baremetal_only.py --check`; `check_nvm_capture.py`; `ci_scope.py --selftest`; `pp_srcs.py --check --selftest`; `check_feature_status.py --self-test` | none, or `make -pqrR` reads (host make) | rc 0 each (`receipts/gates/head_gates.txt`): test evidence 72 <= 77; hygiene PASS over 850 files; py idiom over-long lines 0 <= 0; lint 90 <= 90; naming 95 recorded; port contracts `hdl 1940`; fail fast 81 <= 84; capture census and receipt agree; feature status 46/46 |
| Shard holding `milan_dp` | `rtl.yml` `verilator-shards` shard 4, replayed (`scripts/shard4.sh`) | 4.3 (shim), 34 calls | rc 0: 1/1 suite, 11,839 checks, 0 failures |
| `milan_dp` explicit campaigns | `make -C tb/verilator/milan_dp` `gmstep-mutants`, `crflic-mutants`, `gsi-mutants`, `render-csr-controls` (`scripts/campaign.sh`) | 4.3 | rc 0 each: 22/22, 7/7, 9/9, 4 checks 0 failures |
| Docs jobs | `docs.yml` `docs-check`, `wire-accountability`, `docs-check-no-git`, replayed (`scripts/docs_jobs.sh`) | 4.3 (shim), 2,947 calls | rc 0 each |
| Entity shape self-test, host make | `check_entity_shape.py --self-test` under GNU Make 4.4.1, run alone | 4.4.1 | rc 0, 222 checks, 0 failures; tree clean after (`receipts/gates/head_entity_shape_selftest_host.log`) |
| Restart-request probe | `scripts/restart_controls_probe.py <tree> 1269cdaf` | none | rc 0: 45 anchors, each once; the published veto suppresses no CRF request, the fixed one all |
| OOC area | `syn/yosys/ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo` | none | rc 0: 574 / 636 and 865 / 792, unchanged |
| Shipping image | not rebuilt (assignment: no Vivado run; no image input changed) | - | round 4's stands: WNS +0.193 ns, slices 99.89 % |

## Parent-visible changes

None to the gateware or its interfaces: no RTL, port, parameter, register, CSR, AEM, builder, configuration, generated file or gitlink change; no processor-boundary port change; no protocol-processor edit; VERSION stays `0x0002_0060`.

- `tb/verilator/milan_dp/gmstep_mutants.py`: one `--all` control re-anchored; the inventory's count (20), names and named checks are unchanged, so the suite README's control table (`tb/verilator/milan_dp/README.md:710-728`) and `docs/testing/TESTING.md:273` stay true.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1000-1003`: one sentence, the reviewers' text.

## Observations outside the round 4b items

- Still open from round 4, not a round 4b item: `scripts/measure_test_evidence.py:681` says the `milan_dp_mclk` campaign plants "the #629 design's fourteen named root defects"; it plants sixteen since round 2. Wording only.
- R432-3-S1 = R433-3-S1 (the entity shape gate's database read counts a parse stopped by `$(error)` as readable): the manager's to file, unchanged.
- `tb/verilator/milan_dp_render`'s `tdm8render-mutants` (the render lane split out of `milan_dp` for #447) is outside the named suite and was not run this round.

## Receipts and scripts in this directory

- `receipts/campaigns/`: the four campaign logs (`milan_dp_gmstep-mutants.log`, `milan_dp_crflic-mutants.log`, `milan_dp_gsi-mutants.log`, `milan_dp_render-csr-controls.log`) and `restart_controls_probe.log`.
- `receipts/replay/`: shard 4's driver log, summary, make calls per step, step 13 log and the `milan_dp` excerpt; the aborted `nohup` launch's driver and step 13 logs; the three docs jobs' driver logs, summaries and key step logs (`docs-check` steps 9, 26, 43, 50; `wire-accountability` step 3; `docs-check-no-git` step 2); `replay_table.md`; the sequence logs; the `git clean -n` listing.
- `receipts/gates/`: every light gate log at the head (`head_*`) with `head_gates.txt` (one `rc label` line each) and the host-make entity shape self-test.
- `receipts/ooc_head.log`: the OOC area run.
- `scripts/`: `restart_controls_probe.py` (the static check of every control against the request), `campaign.sh`, `shard4.sh`, `docs_jobs.sh`, `gates.sh`, and round 4's `replay_workflow.py`, `replay_subst.json`, `run_job.sh`, `collect_receipts.sh` and `tabulate_replay.py` with their paths moved to this round's scratch.
- Every file here is under 200 KB; the home-directory prefix in receipts is written `$HOME`.

## Scratch

`$VALIDATION_STORAGE/629-a517/` (outside the tree and this directory): the make 4.3 build, the replay venv, replay outputs, campaign and gate logs, the memory samples.
