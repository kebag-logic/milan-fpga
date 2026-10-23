[R677] NEGATIVE - exact head 417ec52864efc09f1e3ecd0f755cb0daa7604426

Internal cleared-context review, round R677-4, PR #770 (issues #632 and #764). Tree `aea3f763c8a6eea72a5f9bb8dec0bfe5af13b268`. Source base `e26f1816`; live dev `e5b480a385841f19420570bbba7c46da101d1303`.

**Verdict.** The RTL, the merge, the resource record and the test repair hold, and every prior finding is resolved at its cause. Three MINOR documentation findings remain. Two authoritative pages still state the whole-PDU late rule that round 6 retired. A GM-step control count is stale. The test catalogue still says the `[NOTIFY]` case fails "until the pin moves". These leave `Docs` UNCLEAN, so the verdict is NEGATIVE. `Conformance`, `RTL`, `Robustness` and `Tests` are CLEAN at this head. No RESIDUE item was found.

## Scope

- **Delta judged.** `ee5ece60..417ec528`:
  - round 6 (`f98d00dd..d40e2ee8`);
  - the merge of dev `e5b480a3` (`dc9cda7d`);
  - round 7 and 7b (`5282b8b6`, `17280d2d`, `d835ba12`);
  - round 7c (`c2c996fa`);
  - the manager's citation commit (`417ec528`).
- **Context.** `e26f1816..417ec528`.
- **Read first.** AGENTS.md and CONTRIBUTING.md; issues #632 and #764; the round-6 assignment (issuecomment-6341411985); the round-7 assignment (issuecomment-6351804497); the owner's area decision and round-7b assignment (issuecomment-6357449062); the round-7c rulings (issuecomment-6360257772) and the citation correction (issuecomment-6365323716); the block-RAM exception (#632 issuecomment-6309313685).
- **Prior findings.** I read the R677-3 (issuecomment-6341403630) and R678-3 (issuecomment-6339307135) findings only after my own pass over the diff.
- **Evidence used.** The author's published receipts at `0ca01426:review-evidence/632-r1/author-r7/receipts/round6|round7`. My own probes are under `receipts/`.
- **Not claimed.** No manager source bank runs at this head, and none is claimed or inferred.

## Findings

### R677-4-F1 - MINOR - Docs - two authoritative pages still state the whole-PDU late rule round 6 retired

- **Where:**
  - `docs/reference/MILAN_COMPLIANCE_MATRIX.md:221`, the 4.4.4.5 / .9 row: "`KL_render_queue`: a clear `tv` is untimed and not presented; late and too-early PDUs are dropped and counted".
  - `docs/AAF_LATENCY_TAPS.md:105`: "late, too-early and untimed PDUs are dropped and counted".
- **Authority/evidence:**
  - Round 6 (R677-3-F1, assignment item 1) made lateness per event. `KL_render_queue.sv:73-91` says a PDU stamped behind the latest event "is judged so too: its events still ahead of R are written". The walk stores per event (`:516-532`).
  - `docs/design/TIME_SYNC.md:400` and the CHANGELOG ("Late and too-early events are dropped and counted. Each event is judged on its own frame.") were brought to that rule. These two pages were not.
  - The matrix row was kept from the lane side in the merge, so it carries the pre-round-6 text.
  - Receipt: `receipts/findings/F1_whole_pdu_wording.txt`.
- **Impact:** The compliance matrix and the latency-chain page describe the defect R677-3-F1 removed, as if it were the shipped behaviour. This is a conformance-status claim, so it is not RESIDUE.
- **Required outcome:** Both places state the per-event rule. A late or too-early event is dropped while the PDU's other events are presented. A PDU with such an event counts once (late, early, refused). An untimed PDU is not presented and counts once. For example: "late and too-early events are dropped, the PDU's other events presented, each such PDU counted once".
- **Verification:** `git grep -n 'late and too-early PDUs are dropped\|late, too-early and untimed PDUs are dropped'` returns nothing outside `docs/history`. The docs gates pass.

### R677-4-F2 - MINOR - Docs - stale GM-step control count, and a stale gmstep leg description

- **Where:**
  - `docs/design/GM_LOSS_RECOVERY.md:321`: "five negative controls in the sweep, 20 in `gmstep-mutants`".
  - `tb/verilator/milan_dp/README.md:90`, the `obj_gmstep` row: "asserts `tu` and counts one render re-base". This text predates the delta and is identical on dev `e5b480a3`. This PR retired the re-base, though, and round 7c edited this README's gmstep section.
- **Authority/evidence:**
  - `gmstep_mutants.py` `CONTROLS` has 21 entries.
  - The same page says "plants all 21 controls" (`GM_LOSS_RECOVERY.md:253`), `TESTING.md:278` says sixteen plus five, and the campaign at `c2c996fa` ran 21 controls plus 2 clean legs (23 of 23).
  - Since #632 the leg grades refusals and slips, not a re-base (`sim_gmstep.cpp:9`, `:1252`; `GM_LOSS_RECOVERY.md:150`).
  - Receipt: `receipts/findings/F2_gmstep_counts.txt`.
- **Impact:** An authoritative recovery page contradicts itself on the campaign inventory. That is a figure, so it is not RESIDUE. The milan_dp catalogue row describes a check the leg no longer makes.
- **Required outcome:** `GM_LOSS_RECOVERY.md:321` reads 21. `README.md:90` describes the current leg: `tu`, and the presentation stage refusing and counting the PDUs stamped across the step, with no re-base.
- **Verification:** The counts agree with `CONTROLS` in every page that states one. The docs gates pass.

### R677-4-F3 - MINOR - Docs - the test catalogue still says the `[NOTIFY]` case fails "until the pin moves"

- **Where:** `docs/testing/TESTING.md:647`, the `tb/verilator/milan_dp` row: "at a processor pin whose gate reads GET_STREAM_INFO's word it fails its steps 3 and 4, and `sim_pool.py` then starts no later leg, so each is run by its own `run-<case>` target until the pin moves".
- **Authority/evidence:**
  - Round-7 assignment item 2 requires removing every "fails at the current pin" statement from the PR body and the docs.
  - The pin is `93fb0b2d` (gitlink at HEAD), which carries the stored-offset gate. The notify leg passes, 461 checks and 0 failures (`round7/notify_dc9cda7d`), and `notify` is an ordinary pool case again (`tb/verilator/milan_dp/Makefile:614`).
  - The PR body says only the design page's statements are gone, and this row survived.
  - Receipt: `receipts/findings/F3_notify_pin_statement.txt`.
- **Impact:** The authoritative test catalogue tells a reader the pool cannot run past the notify leg, and gives a workaround for a state the pin has left. That is a stale verdict and validation-method claim, so I classify it MINOR rather than RESIDUE.
- **Required outcome:** The row states that the case passes at the adopted processor pin. A gate that compares with GET_STREAM_INFO's word fails CRF steps 3 and 4, and `gsi-mutants` plants that gate. The "until the pin moves" workaround is removed.
- **Verification:** `git grep -n 'until the pin moves'` is empty. The docs gates pass.

### RESIDUE

None found. The comment-rule scan of the lane's own added source lines (`ee5ece60..d40e2ee8` and `dc9cda7d..HEAD`, under hdl, tb, sw, scripts, syn, configs and ci) shows no review round, reviewer ID, lane label or issue-comment ID in a source comment. The resource record's `measured` strings cite the owner exceptions by URL, as the record recipe requires. Those strings are data, not source comments.

### SUGGESTIONS (optional)

- **S1.** `sim_gmstep.cpp:986-990`: the boot record's ordering term compares the pulse with `talker_[talker0]`, the first baseline PDU. Comparing it with the first talker PDU at all (`talker_[0]`) would witness "the talker, opened after it" directly. So would sampling `aaf_stream_en_raw_w` low at the pulse. The ordering holds structurally today, because `acquire()` asserts GM A published before `provision_media()` configures the talker.
- **S2.** `round7/cc-rerun-c2c996fa/` carries no `HEAD.txt`. Only its directory name ties it to `c2c996fa`; its sibling `capture_coherence_rerun_c2c996fa/` has one.
- **S3.** Retained from R677-3 S1 and S2, both still open:
  - the builder accepts `buffer_length_ns` above the queue's 2,126,000 ns backed hold;
  - `ci/image/command-table.json` still lists `KL_render_setpoint.sv` and has no `render_queue` entry (an allow-list superset; no workflow fails on it).
- **S4.** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1964` dates a figure "as of round 6 of PR #770". The comment rule covers source comments only, but a design page reads better as "with the per-event late rule (#632)".
- **S5 (note, outside this PR).** Dev's #771 adoption brought `IEEE 802.1AS-2020` clause citations for gPTP behaviour into `sim_gmstep.cpp`, the milan_dp README and the pin page, for example `10.3.13.2.4 f) 5)`. They are not in this PR's diff against dev. Every citation this PR adds names 802.1AS-2011. This is for the #771 owner's residue list.

## Check-by-check result for the assigned focus

1. **R677-3 and R678-3.**
   - **Per-event late rule.** `KL_render_queue.sv` takes `db_w = ts - E_n + LATE_C x Ps` and sets `F0 = n - LATE_C + round(N/Ps)`. It judges each walked event `F <= R` as late. Only `db_w < 0` (more than `LATE_C` = 504 frames behind) refuses the whole PDU. That is sound, because its last event is at most `n - 1 < R`.
   - **Its bound.** 504 comes from the depacketizer's 2048-byte `axis_fifo` with `DROP_OVERSIZE_FRAME`: 252 payload beats, 2 samples each (`milan_datapath.sv:7549-7561`). `refused_o` counts once per PDU with either refusal.
   - **Widths.** The frame width (`DMAX_C`), the divider width (`QW_C` 10) and the lead guard (`PAY_LEAD_CYC_P` 16 >= `QW_C + 3`) are elaboration-checked.
   - **Pages.** REGISTER_MAP, TIME_SYNC, the datapath comment and the design page state the rule; F1 lists the two pages that do not.
   - **Figures.** 531/236 and 883/402 match `round6/ooc_2700584e/q1x1.rpt`, `q8x8.rpt`, and round 4's 553/228 and 890/387 are kept as provenance. 26 defects, sixteen follow_ring controls; "two frames past" is gone.
   - **My runs** in a disposable copy of the head (pinned Verilator 5.050):
     - `render_queue`: 39 and 38 checks, 0 failures on both shapes;
     - `make mutants`: 28 of 28, the 2 clean shapes and 26 mutants. The whole-PDU drop is caught on both shapes by `[behind]`, the short late reach by `[behind]`, and the double count by `[refused]` (`receipts/probes/rq_*`).
   - **Campaigns** (author's receipts):
     - `tdm8render-mutants`: 31 of 31 at `d835ba12`. The ungated commit is caught by T26 on the multi-stream leg.
     - Pull-in: 18 boot phases plus the history leg, 19 runs in all (the assignment's "19 legs plus history" counts the history leg twice). Each phase gave 28 checks, 0 failures; the history leg 272, 0.
     - GM-step: 23 of 23 at `c2c996fa`.
     - The campaign audit at `c2c996fa` matches each inventory one for one: 20, 3, 3 and 21.
     - `d835ba12..c2c996fa` touches no hdl, syn, configs or `milan_dp_render` input.
2. **Merge `dc9cda7d`.**
   - **Conflicts.** `git merge-tree` of `d40e2ee8` and `e5b480a3` gives 9 conflict regions in the 7 named files, 12 table rows and paragraphs counted singly. The merge differs from git's auto-merge only in those 7 files (`receipts/merge/markers_to_merge.stat`), so no other file was hand-edited.
   - **Each region against the base** (`receipts/merge/diff3_hunks.txt`):
     - kept from dev: the #761 lock-loss row and the "lock edges" wording (MEDIA_CLOCK_FOLLOWING, test_builder); dev's `mcr_restart_p_w` row (BAREMETAL_FIRMWARE); the #761 sentence (MATRIX); the #637 63-control row and the eighteen mclk mutants (TESTING); the #761 B row (mclk README); both CHANGELOG sections.
     - kept from this PR: the four/two census and the bind-wipe-only `flush_i` pin; the retired `media_rebase_p_w` and `render_recentre_p_w` rows; the settle-recentre switch wording; the gmstep and tdm8render presentation-law rows.
   - **Dev changed nothing in the rows taken from this PR**, so no dev fact is lost.
   - **RTL at the head.** `mcr_restart_p_w` is `(crf_clk_selected_r & ((tkd_crflk_q_r ^ crf_locked_w) | crf_mr_toggle_p_w)) | aafm_disrupt_p_w | aafm_mr_toggle_p_w`, both lock edges (`milan_datapath.sv:3344-3347`). `flush_i` is `strtbl_bind_fall_w` (`:8028`). No `media_rebase_p_w`, `render_recentre_p_w` or `KL_render_setpoint` remains in hdl, tb, sw or scripts.
3. **`[NOTIFY]`.** At `dc9cda7d` with processor `93fb0b2d` (`pp_HEAD.txt`): 461 checks, 0 failures. `gsi-mutants` 12 of 12, the clean leg and 11 mutants; the three #632 controls each fail 3 of 461. The gitlinks at HEAD equal dev's (`93fb0b2d`, `55680bff`). One "until the pin moves" statement remains (F3).
4. **The eleventh resource record.**
   - **Route figures.** `syn/ooc/pp_resource_baseline.json`: route-1x1 51,259 LUT, 53,208 FF, 15,835 slices, 74/27 RAMB, DSP 13, WNS +0.236 / WHS +0.028.
   - **Against #771's record:** +500, +376, +107 slices and +2 RAMB18, the deltas the owner accepted.
   - **ooc-1x1 and ooc-8x8.** Figures, scopes and identity equal #771's; only the input digests and `measured` text move. Policy fields are unchanged.
   - **Gate runs.** The author's printed records at `5282b8b6` equal the committed record in figures, inputs and identity, and the three `check` logs read PASS. My `pp_resource_gate.py check-baseline` at HEAD: "baseline PASS: 3 endpoints", rc 0 (`receipts/resource/`).
   - **Docs.** Both exceptions are cited, along with the 15 free slices and Mark II #640. I checked the AREA_BUDGET arithmetic: 80.85 %, 13,219 over, 10,557, 56 %, a 0.206 ns fall to the floor, 47.5 tiles.
5. **GM-step repair.**
   - **Test-only.** `git diff --name-only d835ba12..HEAD` touches no file under hdl, syn or configs.
   - **The control.** It latches on `gm_recentre_p_r && |aaf_stream_en_raw_w`. The probe file is `public_flat_rd` only.
   - **Lane patch equals the dev patch.** The archived dev patch equals `d835ba12..c2c996fa` on the four test files line for line.
   - **Planted alone** (author's receipts): caught by its named pause check at the head and on clean dev `e5b480a3` with only that patch; 12 failures, baseline streaming.
   - **My falsification probe** (`receipts/probes/gmstep_delay_*`, driver `scripts/gmstep_delay_probe.py`, built through the campaign's own plant and recipe), at a non-default feed delay of 777 cycles:
     - the clean leg passes, 196 checks and 0 failures, with GMDET at cycle 6,001,430, `02a1b2fffec3d4e5 -> 00aaccfffe010203`;
     - the planted control is caught by "licence: the talker never pauses beyond four of its intervals" (176 checks, 12 failures), and the baseline still streams.
   - **No boot-timing dependence.** The boot pulse precedes the talker gate by sequence: `acquire()` asserts GM A published before `provision_media()` configures the talker. The pulse cycle is the same at delays 0 and 777.
   - **The boot record and its control** behave as stated: the exempt-boot-identity control fails exactly that record.
   - **Campaign.** `gmstep-mutants` 23 of 23.
6. **Full sweep at `c2c996fa`.**
   - **Shards.** 15+16+16 of their suites, plus 16 of 17 in shard 2. That is 63 of 64; checks 54,917 + 331,530 + 262,031 + 1,541,583 = 2,190,061, with 0 in-suite failures.
   - **`capture_coherence`.** It hit the 2,400 s wall clock (TIMEOUT, rc 92 on the shard). Run alone it passed twice: `capture_coherence_rerun_c2c996fa` gave 20,832 and 447 checks, 0 failures, campaign 35 of 35, rc 0; `cc-rerun-c2c996fa` gave rc 0.
   - **Other gates** (author's receipts): the docs gates under make 4.3 at `c2c996fa`, with `417ec528`'s docs re-run; lint 89 <= 89; firmware boundary; builder bank at `d835ba12`; Yosys at `d835ba12`.
   - **Citations.** Every 802.1AS citation this PR adds names the 2011 edition (9.6.2.1, 10.2.3.13), including `417ec528`'s four edits; S5 covers dev's.

## Prior findings, resolved or retained at this head

| Finding | State | Evidence at 417ec528 |
|---|---|---|
| R677-3-F1 (MINOR) whole-PDU late drop | **Resolved** | Per-event RTL (above); `[behind]` phase on both shapes; whole-PDU, late-reach and double-count mutants killed in my run. Two documentation residues of the old rule are filed as R677-4-F1 |
| R677-3-F2 (MINOR) stale figures | **Resolved** | 531/236, 883/402 with the old 553/228 and 890/387 as provenance; 26 defects; "twenty-six" in the reader script; "past the queue" |
| R677-3-F3 (MINOR) tdm8render red, T26 | **Resolved** | T26 on the multi-stream leg grades the gate with a live crossbar; 31 of 31 at `d835ba12` |
| R677-3-R1 (RESIDUE) round names in comments | **Resolved** | `phase_mutants.py`, `sim_ofs.cpp`, `gsi_mutants.py` reworded |
| R678-3-F1 (MINOR) retired render law | **Resolved** | TIME_SYNC.md:108 "A step re-bases no render queue"; GM_LOSS_RECOVERY.md:150 and :241 describe the queue-emptying controls; the MCF bind measurement is marked pre-#632 |
| R678-3-F2 (MINOR) stale figures and counts | **Resolved** | As R677-3-F2; follow_ring "sixteen" |
| R678-3-F3 (MAJOR) full campaigns | **Resolved** | tdm8render 31/31, pull-in 18 + history, GM-step 23/23 with the audit; the small-step phase included (`--all`, the whole leg) |
| R678-3-R1 (RESIDUE) | **Resolved** | As R677-3-R1 |
| R677-3 S1, S2 | Retained as suggestions | S3 above |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_render_queue.sv:6-91,:287-316,:440-532,:776-794` per-event rule against IEEE 1722-2016 4.4.4.9 / 7.5 and the stage's stated law; `milan_datapath.sv:3344-3347` (#761 both lock edges); `milan_datapath.sv:7703-7712` detector against 802.1AS-2011 9.6.2.1 / 10.2.3.13 and the round-7c ruling; `[NOTIFY]` 461/0 at `93fb0b2d` (Milan v1.2 5.4.2.9/.10.2); resource record against both owner exceptions | R677-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| RTL | CLEAN | `KL_render_queue.sv` LATE_C/BIAS_L/DMAX_C/FW_C/QW_C, `g_chk_wrap`, `g_chk_div`, `g_chk_max_ev`, `g_chk_lead_cyc`; `milan_datapath.sv:7549-7561,:8009` MAX_EV derivation against `KL_aaf_rx_depacketizer.sv:183-199` (2048-byte frame FIFO, oversize drop); merge `dc9cda7d` RTL against both parents; `git diff --name-only d835ba12..HEAD` has no hdl, syn or configs file | R677-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| Robustness | CLEAN | Late-reach boundary (-504 and -505 frames, ±0.3 Ps), the wrap window read, a PDU with both refusals counted once, the longest PDU early hold, oversize frames dropped upstream; gmstep control at feed delay 777 (`receipts/probes/gmstep_delay_*`); detector sequence `acquire()` before `provision_media()` (`sim_gmstep.cpp:883-953`) | R677-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| Tests | CLEAN | My `render_queue` 39/0 + 38/0 and mutants 28/28 (`receipts/probes/rq_*`); my gmstep clean 196/0 and planted control caught by its named check; author receipts gmstep 23/23 (`c2c996fa`), stop probe at head and dev, tdm8render 31/31, pull-in 18 + history, gsi 12/12, campaign audit, sweep 63/64 + capture_coherence alone; `sim_gmstep.cpp:973-990`, `gmstep_mutants.py:86-93,:203-213,:263-271,:358-374` | R677-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| Docs | UNCLEAN | R677-4-F1 (`MILAN_COMPLIANCE_MATRIX.md:221`, `AAF_LATENCY_TAPS.md:105`), R677-4-F2 (`GM_LOSS_RECOVERY.md:321`, `tb/verilator/milan_dp/README.md:90`), R677-4-F3 (`TESTING.md:647`). Checked clean: TIME_SYNC.md:396-401, REGISTER_MAP `RENDER_STAT`, MEDIA_CLOCK_FOLLOWING.md:1902-1968 and :1730-1744, AREA_BUDGET, MARK_II_AREA_PLAN, 234 findings section, findings README, CHANGELOG, milan_dp README gmstep section, GM_LOSS_RECOVERY.md:144-300 | R677-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |

## Real limits

- **What I did not run.** No full sweep, no TDM8, pull-in or GM-step campaign, no Vivado, no Yosys, no builder bank and no docs-gate run. Those results are the author's published receipts, which I verified by content, tallies and heads. My own executions are:
  - `render_queue` (both shapes) and its 26-mutant campaign;
  - one GM-step clean leg and one planted control at feed delay 777;
  - `pp_resource_gate.py check-baseline`;
  - the merge reconstruction (`git merge-tree`, diff3).
- **Resource figures.** These come from the author's Vivado receipts at `5282b8b6`. No RTL changed after that head, and `check-baseline` reruns cleanly at HEAD; the input digests themselves were not recomputed without Vivado.
- **Auto-merged files.** For the merge's non-conflicted files I relied on git's three-way merge, the retired-identifier search, and the author's sweep at `c2c996fa`.
- **Hosted CI.** At my snapshot (`receipts/hosted/check_runs_snapshot.txt`) the exact-head Verilator shards were mostly in progress and the Yosys shards queued. Docs, lint, firmware and elaboration contexts had succeeded. "Physical gPTP (nightly and manual)" was skipped, which is not an executed job.
- **No hardware.** Physical calibration was NOT RUN. Field and bench skips are not hardware proof, and #632's and #764's bench items follow after merge.
- **Clone integrity after my work.** The clone is byte-exact: HEAD and tree as above, `git write-tree` equals the tree, the index and worktree are clean, and the ignored `syn/ooc/__pycache__` from my gate run was removed. The submodule worktrees are clean at their gitlinks (`55680bff`, `93fb0b2d`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`). All probes ran in a disposable copy under `scratch/`.

## Pending manager duties

- The current-dev merge-candidate validation (builder and native banks) at the merge turn, with its receipts linked on the PR.
- Hosted exact-head acceptance (Verilator, Yosys) and act replication.
- Re-review of the fixes for R677-4-F1 to F3 at the corrected head.
- The external review's verdict; merge requires two independent positives and the full completion bar.
- Carry S5 to the #771 owner's residue list, if wanted.

R677-4 FINISHED
