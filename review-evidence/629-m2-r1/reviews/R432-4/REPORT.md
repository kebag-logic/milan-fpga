[R432] NEGATIVE - exact head 2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee

Round R432-4, internal cleared-context review of issue #629 / PR #634 (lane M2): the delta from round 3's `0b066b6e` to `2bc5adc0` (tree `0a3979f48d426c6dbb50d00d2204fb6b4e5fba8c`). That covers round 4's merge `c1288648` of dev `1269cdaf` (PR #636, processor pin `b2db3a97` -> `631eeb34`) and round 4b's `917a78ec` (F-A512-1) and `2bc5adc0` (R432-3-R1).

The verdict is NEGATIVE on one open MINOR, which is in Docs only: a per-campaign count in the PR body's Round 4b section contradicts the author's own published receipt. The fix is a PR-body edit; no commit is needed. Conformance, RTL, Robustness and Tests are covered clean at this head. The merge keeps both sides, F-A512-1 is fixed and load-bearing, and every `milan_dp` campaign, the `milan_dp` suite and `milan_dp_mclk` pass at this head.

Reconstructed from: AGENTS.md and CONTRIBUTING.md; docs/README.md; the #629 body and the round 4 and 4b assignments (#629 comments 5964785948 and 5966355350) with their TAKEN and REVIEW READY comments; `docs/design/MEDIA_CLOCK_FOLLOWING.md`; `git diff 1269cdaf..2bc5adc0` and `0b066b6e..2bc5adc0` with history; the PR body; the author's public packets `review-evidence/629-m2-r1/author-r4` and `author-r4b` on `629-m2-review-evidence` at `08719f06` (the round-1 tree at `f7cb2d68` holds only round-1 material). I read the round-3 findings (R432-3, R433-3) only after my own pass over the diff. I read no other reviewer's round-4 report.

## Findings

### R432-4-F1 - MINOR - Docs - PR #634 body, "Round 4b" table, the second row numbered 1 ("The other campaigns' controls against the reshaped request") - the gsi anchor count contradicts its receipt

- **Requirement/evidence:**
  - The PR body says: "A probe reads all 45 control anchors of the five `milan_dp` campaigns ... None of the render (4), render-CSR (3), crflic (6) or gsi (11, ten in the processor top) anchors ...".
  - The author's receipt `author-r4b/receipts/campaigns/restart_controls_probe.log` (evidence branch `08719f06`) prints **12** `[gsi]` rows, **11** of them at `protocol_processor_top.sv` and one at `milan_datapath.sv:4936-4937`.
  - `tb/verilator/milan_dp/gsi_mutants.py:99-131` plants 12 edits: 1+2+1+1+1+1+3+2. My `anchor_probe.py` reads the same table and gets 12 gsi edits, 11 in the processor top (`receipts/anchor_probe.log`).
  - The body's own breakdown, 20 + 4 + 3 + 6 + 11, sums to 44, not its stated 45. The 45 is right: the receipt's "46 anchors" line includes one round-4 contrast row.
  - The REVIEW READY comment 5966931872 repeats "gsi (11)".
  - AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer."
- **Why MINOR, not RESIDUE:** the defect is a wrong figure, not wording. The owner rule of 2026-10-02 excludes figures from RESIDUE.
- **Impact:** a cold reviewer cannot reconcile the published breakdown with its total or with the receipt it summarises. The conclusion it supports still holds at both counts: every anchor is found exactly once, and no non-gmstep anchor lies in the request or on a lane-changed line (`receipts/anchor_probe.log`). No test, code, measurement or verdict is affected.
- **Required change:** the Round 4b row reads "gsi (12, eleven in the processor top)", so the per-campaign counts sum to 45 and match the receipt. Comments stay unedited (assignment rule); the PR body is the place.
- **Verification:** 20 + 4 + 3 + 6 + 12 = 45 in the corrected row, and it matches `restart_controls_probe.log`'s per-campaign rows.

### R432-4-S1 - SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp/sim_gmstep.cpp:1121-1165` and `tb/verilator/milan_dp_mclk/sim_mclk.cpp` - no check grades a followed-AAF restart on a PHC re-base cycle

- **Evidence:** `veto_probe.py` (`receipts/veto_probe.log`) plants controls through the campaign's own `run_control` at this head:
  - P1, round 4's form (`... | aafm_mr_toggle_p_w & ~media_rebase_p_w`): SURVIVED.
  - P2, round 4b's shipped form: caught, breaking exactly "coincident: a PHC step does not suppress the CRF restart".
  - P3, `| ((aafm_disrupt_p_w | aafm_mr_toggle_p_w) & ~media_rebase_p_w)`: SURVIVED on the gmstep leg.
  - The gmstep leg runs CRF-selected, and `milan_dp_mclk/sim_mclk.cpp` issues no settime or adjtime, so no suite steps the PHC while it follows an AAF stream.
  - The request (`hdl/milan/milan_datapath.sv:3229-3232`) ORs the AAF terms outside any veto. So the property holds by construction today and is ungraded.
- **Impact:** none today. A later edit that vetoes the AAF terms on a re-base cycle would pass every suite.
- **Outcome (optional, separate Issue):** a coincident AAF-following trial, the AAF counterpart of `check_coincident_restart`, with P3 as its failing control.

### Prior findings at this head

| Finding | Severity | State at `2bc5adc0` | Evidence |
|---|---|---|---|
| R432-3-R1 = R433-3-R1, "The last two" | RESIDUE | **TAKEN**, exact text | `MEDIA_CLOCK_FOLLOWING.md:1000-1003` reads "The history-restart count and the largest deviation are the bench's measurement of a talker's timestamp regularity."; "The last two" is gone (`git diff 917a78ec 2bc5adc0`) |
| R432-3-S1 = R433-3-S1, `$(error)` database parse counts as read | SUGGESTION | **RETAINED** (optional Issue, manager's) | `scripts/shape_consumer_inventory.py` and `milan_dp_mclk/Makefile` are untouched by `0b066b6e..2bc5adc0` |
| F-A512-1 (author-found, Tests) | ruled in-PR | **RESOLVED** | `gmstep_mutants.py:230-233`; `make gmstep-mutants` 22/22 at this head, the control breaking exactly 1 check, its named one (`receipts/gmstep_mutants_all.log:655-656`); P1 survives and P2 is caught (`receipts/veto_probe.log`), so the fix is load-bearing |

## The four questions

1. **The merge keeps both sides.** I redid it (`remerge_check.sh`, `receipts/remerge_check.log`):
   - **Parents and conflicts:** the merge's parents are `0b066b6e` and `1269cdaf`, with merge-base `cdf49d1a`. It conflicts in exactly `CHANGELOG.md`, `MEDIA_CLOCK_FOLLOWING.md` and `scripts/naming.budget`.
   - **Auto-merged paths:** every one equals the committed blob, including the `protocol-processor` gitlink `631eeb34`, `KL_pp_shadow.sv`, `REGISTER_MAP.md` and `measure_test_evidence.py`. The exception is `port_docs.budget`, whose only difference is the generator's comment line `hdl 1916` -> `hdl 1940`.
   - **Both deltas carried:** in `REGISTER_MAP.md` and `measure_test_evidence.py`, dev's delta and the lane's delta are each carried exactly.
   - **naming.budget:** the committed `scripts/naming.budget` equals the lane parent's.
   - **CHANGELOG:** both sections are byte-identical to their parents.
   - **Design page header:** keeps "Implemented by lane M2", "then-pinned submodule commit `b2db3a97`" and "landed at `631eeb34`". The link target `#protocol-processor-changes` resolves (`gen_toc --verify-anchors` rc 0).
   - **Ratchets regenerated at head:** `measure_naming.py --write-budget` and `check_port_contracts.py --write-budget` leave the tree byte-identical (`receipts/budget_regen.log`). The checks pass at 95 and at hdl 1940 / 217 <= 217.
2. **The shipping image at the merge,** judged from the author's receipts (no Vivado run here):
   - **Timing** (`alinx_ax7101_timing_summary_excerpt.txt:141`): WNS 0.193, WHS 0.024 and WPWS 0.264 ns, with 0 failing endpoints of 181,419 / 181,338. All four `signoff_*_negative.rpt` say "No timing paths found".
   - **Routing** (`route_status.rpt`): 106,622 of 106,622 nets routed, 0 errors.
   - **Utilisation** (`utilization_place.rpt:35,76`): Slice LUTs 50,767 (80.07 %), slices 15,832 of 15,850 (99.89 %), BRAM 68.52 %, DSP 5.83 %.
   - **#607 check:** `build_launch_tail.txt` carries the line "no 12-4739, 20-1307 or 12-5201 diagnostics".
   - **Not checkable:** the "0 CRITICAL WARNING" count is stated in the author's HANDOFF and PR body only, since `vivado.log` is not published. See the limits below.
   - Round 4b changes no RTL (`git diff c1288648 2bc5adc0` touches only `gmstep_mutants.py` and the design page), so the image stands for this head.
3. **F-A512-1.**
   - **The fix:** the planted request is `(crf_clk_selected_r & ((...) | crf_mr_toggle_p_w) & ~media_rebase_p_w) | aafm_disrupt_p_w | aafm_mr_toggle_p_w`, the same veto dev's control planted on dev's AND chain (`git show cdf49d1a:hdl/milan/milan_datapath.sv`, lines 3155-3156).
   - **Truth table** (`restart_truth_table.py`, 128 rows): on re-base cycles there are 5 selected-CRF-only requests and 33 AAF-only ones. Round 4's form suppresses 0 CRF and 11 AAF requests; 4b's form suppresses all 5 CRF requests and 0 AAF. That matches the PR body.
   - **The named check:** `check_coincident_restart` (`sim_gmstep.cpp:1121-1165`) sweeps 32 phase offsets of a received CRF toggle against a software settime, and counts outgoing toggles.
   - **The author's anchor claim, spot-checked:** `anchor_probe.py` imports the five campaigns' own tables. It finds every one of 46 edits (42 controls; it counts the absent-stage cut as two anchors) exactly once.
   - **Which controls edit the request:** exactly 8 gmstep controls, all inside `:3229-3232`. Four OR a cause onto `:3232`, two OR a delayed cause onto the whole declaration, one rewrites the CRF group, and the veto is the eighth.
   - **The other campaigns:** no render, render-CSR, crflic or gsi anchor lies in the request or on a line the lane changed since `cdf49d1a`. The claim holds, apart from the gsi sub-count (F1).
4. **Re-measure.** The `milan_dp` suite at this head (`make run`, pinned Verilator 5.050): rc 0, **11,839 checks, 0 failures** (`suite_tally.py`), with the round-4 tally, the sweep's `render_mutants.py` 6/6 and `gmstep_mutants.py` 6/6, and 264 of 264 [CLKSRC-WALK]/[CLKSRC-RANGE] lines `ok`.
   - **Campaigns:** `gmstep-mutants` 22/22, `crflic-mutants` 7/7, `gsi-mutants` 9/9 (processor half planted at `631eeb34`), `render-csr-controls` 4 checks / 0 failures.
   - **`milan_dp_mclk`:** legs 55/0, 32/0 and 50/0, campaign 31/31.
   - **Author receipts:** five shards, 11+23+12+12+1 = 59 suites and 401,934+197,119+1,523,725+14,649+11,839 = 2,149,266 checks, target SHA 5/5. Yosys reports expected=55 observed=55. The entity-shape self-test is 222/0, the 4b shard-4 relaunch 11,839/0, and the `nohup` attempt is disclosed.
   - **Capture gate:** `check_nvm_capture.py` passes at head ("census, clocks, both timing arms and receipt agree").
   - **Em-dash:** 538 added lines at `c1288648` and 541 at head against `1269cdaf`, 0 findings, as the PR body states.

## Lens results

[R432] PASS Conformance — `hdl/milan/milan_datapath.sv:3205-3232` (#602 ruling and IEEE 1722-2016 4.4.4.3/10.4.3: a selected-CRF restart is not suppressed by a PHC step, now graded again by `gmstep_mutants.py:230-233` -> `sim_gmstep.cpp:1121-1165`); [CLKSRC-WALK]/[CLKSRC-RANGE] 264/264 ok at pin `631eeb34` (Milan 5.4.2.15/16) in `receipts/milan_dp_suite.log`; `MEDIA_CLOCK_FOLLOWING.md:6-12,1281-1292` processor status against #635; #629 acceptance "switching and lock loss each graded by a failing mutant" (gmstep 22/22, mclk 31/31) — no conformance claim changed by the delta

[R432] PASS RTL — merge composition: auto-merged blobs equal the committed merge (`receipts/remerge_check.log`); `hdl/milan/KL_pp_shadow.sv:1094-1140` is the only parent instantiation of `protocol_processor_top` and ties `EN_IDENTIFY_NOTIF_P`/`identify_button_i`; no lane RTL in rounds 4/4b; shipping-image receipts (WNS +0.193, WHS +0.024 ns, slices 99.89 %, 106,622/106,622 routed, four sign-off corners empty); `lint_rtl --check` 90 <= 90, `check_rtl_source_lists`, `check_port_contracts` (hdl 1940), `check_sv_idiom` rc 0 (`receipts/gates/`)

[R432] PASS Robustness — `gmstep_mutants.py:303` refuses a missing or repeated anchor (all 46 edits found once, `receipts/anchor_probe.log`); veto truth table over all 128 request inputs (`receipts/restart_truth_table.log`); the reshaped request's OR structure keeps the AAF terms outside any veto (S1 records the ungraded side); lock-loss/switch legs `milan_dp_mclk` 55/32/50 and campaign 31/31, crflic 7/7, gsi 9/9 at the new pin

[R432] PASS Tests — `tb/verilator/milan_dp/gmstep_mutants.py:62-70,230-233`: `--all` 22/22 at head, the veto control breaks exactly its named check; round 4's form survives and 4b's is caught through the campaign's own `run_control` (`receipts/veto_probe.log`), so the fix is load-bearing; `milan_dp` 11,839/0; render 6/6 (sweep), render-CSR 4/0; README `:728,733` and TESTING.md `:273` counts (20 controls) match the inventory

[R432] MINOR Docs — PR #634 body, Round 4b table, second "1" row — R432-4-F1 (gsi anchor count 11/ten against the receipt's 12/eleven). Otherwise checked clean: `CHANGELOG.md` both sections byte-identical to their parents; the `MEDIA_CLOCK_FOLLOWING.md:6-12` header; `:1000-1003` the residue text; `docs_check`, `check_doc_style`, `gen_toc --check/--verify-anchors`, `check_doc_paths`, `DOC_MAP --check`, the boundary diagram `--check`, `check_em_dash` against `1269cdaf`/`0b066b6e`/`c1288648`, and `git diff --check` against `1269cdaf`/`c1288648`/`cdf49d1a`, all rc 0 (`receipts/docs_gates/`); PR body Round 4/4b figures checked against the receipts (all others agree)

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | restart request `milan_datapath.sv:3205-3232` vs #602/4.4.4.3/10.4.3; CLKSRC-WALK/RANGE at `631eeb34`; design page processor status; #629 acceptance mutants | R432-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| RTL | CLEAN | re-done merge vs committed blobs; `KL_pp_shadow.sv:1094-1140`; processor top instantiation set; shipping-image receipts; lint, source-list, port-contract and sv-idiom gates | R432-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Robustness | CLEAN | anchor guard and 46-edit probe; 128-row request truth table; veto probes P1-P3; mclk/crflic/gsi legs at the new pin | R432-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Tests | CLEAN | `gmstep_mutants.py` fix and `--all` 22/22; P1/P2 load-bearing proof; `milan_dp` 11,839/0; render-CSR 4/0; inventory counts in README/TESTING | R432-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |
| Docs | UNCLEAN (R432-4-F1 MINOR open) | CHANGELOG sections; design header and residue; docs gates; PR body Round 4/4b vs author receipts | R432-4 | `2bc5adc0bfd981e63e82ada5e673ce69cab4f4ee` |

**Re-review scope for F1:** only the PR body changes. A Docs re-check of the corrected Round 4b row against `restart_controls_probe.log` closes it. No tree content changes, so the other four lenses stay banked at this head if the head does not move.

## Real limits

- **Make version:** my runs used the host's GNU make 4.4.1, not the hosted runner's 4.3. I ran the `milan_dp` and `milan_dp_mclk` suites by their documented `make` targets, not through `run_all_suites.sh`'s shard harness. My 11,839/0 and 31/31 agree with the author's make 4.3 replays.
- **Not re-run here:** the Verilator shards 0 to 3, the Yosys gate, the builder and native banks, `aaf_clock_meter`, `tdm8render-mutants`, the full `docs.yml` job (builder gates, firmware controls), `act` and `act_ci.py --selftest`. Of the docs job I ran the listed subset only.
- **Shipping image:** no Vivado run. The image is judged from the author's published reports. The CRITICAL WARNING count of 0 rests on the author's statement, because `vivado.log` is not published. I did not check the bitstream digest `d2742a86...c2ec`.
- **Hosted contexts:** a snapshot at this head, taken 2026-10-03T08:32Z (`receipts/hosted_checks_snapshot.tsv`). 17 had succeeded, `Physical gPTP` was skipped (schedule-only), and Verilator shards 1 and 2 were in progress. `verilator-suites` and `yosys-portability` had not been emitted yet.
- **Hardware:** physical calibration NOT RUN. No hardware or bench evidence; field skips are not hardware proof.
- **Path normalisation:** after the runs, receipts were path-normalised (`$PACKET`, `$CLONE`, `$COPY`, `$HOME`, `$TOOLS`, `$TMP`). The hashes in MANIFEST.sha256 are of the normalised files.

## Pending manager duties

- Carry R432-4-F1's PR-body correction and route a Docs re-check of that row.
- Accept the exact-head hosted `verilator-suites` and `yosys-portability` contexts once emitted, and the `act` run.
- Run the builder (48) and native (5) banks, and the candidate merge on live dev `1269cdaf`, at the merge turn.
- Optionally file Issues for R432-4-S1 and R432-3-S1 = R433-3-S1.
- Clone integrity after the review: worktree, index and tree equal `2bc5adc0` / `0a3979f4`. The gitlinks for `protocol-processor` `631eeb34`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` are checked out clean (`receipts/head_integrity.log`).

R432-4 FINISHED
