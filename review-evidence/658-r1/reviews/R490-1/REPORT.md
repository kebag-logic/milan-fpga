[R490] NEGATIVE - exact head fb4953bd61b0f6ca61ab067081e766fe37f96076

Round R490-1, internal cleared-context review of issue #658 / PR #670.
Head `fb4953bd61b0f6ca61ab067081e766fe37f96076`, tree `e07c63993b62098d0d475d9baa6d937b82bd1846`, source base dev `e617275074e370cec342af99b929e2588fc8d43f`.
Authorities: the stage-2 ruling (issue comment 5988843004) and the power-on ruling (5988293154), Milan v1.2 5.4.2.7, IEEE 1722.1-2021 7.4.44 to 7.4.46, `docs/design/SAVED_STATE_MATERIALIZATION.md`, `docs/ENDSTATION_BUILDER.md` D7/D8, and `docs/design/AREA_BUDGET.md` (resource gate).

The RTL does what the ruling asks, and I found no conformance, RTL or robustness defect.
The verdict is NEGATIVE on two MINOR findings.
F1: none of the boot window's new exclusion and termination arms can fail any check.
F2: the PR body claims coverage of one of those arms that its cited leg does not give.

## Findings

### F1 - MINOR - Tests - the boot window's guard arms are untested

- **Artifact:** these arms in `hdl/milan/milan_datapath.sv`:
  - the CSR hold, `!amap_boot_busy_w` at `:1259`, `:4742`, `:4754` and `:6786`;
  - the edit-face wait, `:4358`;
  - the post-terminal sweep, `:4570-4573`;
  - its drain cycle, `:4569`;
  - the CLOSED terminal, `:4570`.

  The `[DYNMAP]` leg is `tb/verilator/milan_dp/sim_nxn.cpp:4161-4275`.
- **Authority and evidence:**
  - The arms are documented contracts:
    - `docs/reference/REGISTER_MAP.md:2157-2162`: the CSR writer is refused "from reset until one sweep after the restore's terminal (`PP_STAT` done or CLOSED)".
    - `docs/CHANNEL_MAP_64.md:374-375`.
    - The `milan_datapath.sv:4105-4108` comment on the edit-face wait.
  - AGENTS section 6, Tests lens: positive, negative and boundary behavior is covered, and a test can fail for the defect it targets.
  - I planted each arm's removal in a copy of `milan_datapath.sv`, rebuilt the `[DYNMAP]` leg through its own recipe, and ran it. Results:
    - **P1** (no CSR hold), **P2** (no edit-face wait), **P3** (no final sweep), **P5** (window ignores CLOSED) and **P9** (no drain cycle) each SURVIVE with 142 checks and 0 failures.
    - **P4** (clip off by one), **P6** (window ends at restore start), **P7** (writer writes the unclipped image), **P8** (output cluster registers zero), **P10** (writer only after the terminal) and **P12** (clip continues at run time) are each KILLED.
    - **P11** is equivalent on this shape: the declared default equals the wire shape.
  - Receipts: `receipts/reviewer_mutants_summary.txt` and `receipts/reviewer_mutants/*`.
  - By inspection the arms are correct. The defect is that nothing would notice their loss.
  - No other harness reaches them. Every harness that writes `CHMAP_WORD` expects the restore to end done, not CLOSED. The pp_shadow K boots and the nightly gPTP leg write the CSR window only after the window has closed.
- **Impact:**
  - **CLOSED terminal.** A regression that drops it leaves the CSR map window refused, and the boot writer running, for the life of a CLOSED boot. No test would fail.
  - **Hold, wait, sweep and drain.** A regression in any of these reopens the store/RAM split they exist to prevent. That split is a CSR store write, or an output edit validating against `cmap_flat_w` (`:4305`, `:4311`), landing in the cycles after AECP release, before the RAMs agree. No test would fail.
- **Required outcome:** each arm can fail a check when it is removed.
  - The leg already stages processor state through `dynmap_probes.vlt`. The same technique reaches a forced CLOSED terminal.
  - It also reaches a CSR write inside the window on a shape whose cursor leaves the write leg idle (the 8x8 render side).
  - An edit that meets the post-terminal sweep can be staged the same way.
  - For any arm judged ungradable at desk level, the alternative is a public reason in the leg's README section, accepted by a reviewer.
- **Verification:** re-run `probes/r490_mutants.py P1 P2 P3 P5 P9` against the corrected head. Each probe must be KILLED, or covered by an accepted rationale. The positive leg must stay green.

### F2 - MINOR - Docs, Tests - the PR body overstates what the gPTP leg grades

- **Artifact:** PR #670 body, validation line for the nightly physical gPTP leg. The same sentence is in the REVIEW READY comment on #658: "It programs the capture map through the CSR window after the restore walk, so it also grades the boot window's CSR hold."
- **Authority and evidence:**
  - The leg writes only after the walk. Its writes can therefore show only that the hold ends: a hold stuck on would refuse them.
  - It cannot show that writes are refused while the hold is up. Removing the hold (P1) leaves every write it makes unchanged.
  - This is a coverage claim, so the residue rule does not apply.
- **Impact:** a cold reviewer reading the PR would count the CSR hold as graded when it is not (see F1).
- **Required outcome:** the PR body states what the leg grades: the hold ends, and the window is usable after the walk. Alternatively, the claim is backed by a check that fails under P1.
- **Verification:** read the PR body at the next head. If the claim stays, P1 must be KILLED by the cited check.

### R1 - RESIDUE - `CHANGELOG.md:54`

- **Problem:** "The CSR map window waits until the boot writer finishes." The window does not wait. It refuses the write, and `CHMAP_STAT` counts it as a commit (`REGISTER_MAP.md:2160-2162`).
- **Exact fix:** "The CSR map window refuses writes until one sweep after the restore's terminal."

### R2 - RESIDUE - `docs/reference/REGISTER_MAP.md:2157-2158`

- **Problem:** "On a shape with dynamic maps the stores and both crossbars hold the #658 power-on map." On the three Arty configurations only the input direction is dynamic (`ADP_DMAP_OUT_MASK_C = 0`), so the capture crossbar holds no power-on map.
- **Exact fix:** "On a shape with dynamic maps, each dynamic direction's store and crossbar hold the #658 power-on map from boot: stream channel c on the port's cluster c."

### S1 - SUGGESTION - Tests - the talker end-to-end check runs inside the boot window

- **Artifact:** `tb/verilator/capture_coherence/sim_dp.cpp:20-26, 258`.
- **Observation:** the talker's end-to-end check never starts the restore walk, so it runs with the boot writer still rewriting the capture RAM. A shipped device always runs after the release.
- **Coverage today:** the post-release capture RAM is graded by readback in `[DYNMAP]` ("power-on: capture RAM keys 0..7 hold the output map", after the walk). The two checks together close the gap.
- **Suggestion:** a post-release run of the talker check would be the more literal proof. Optional.

### Prior public review findings

At the start of this round PR #670 had no review findings: two review-start comments, no reviews and no review comments.
Issue #658 carries no reviewer findings, so none had to be resolved or retained.

## The six requested checks

1. **The identity map at power-on, held clipped until the terminal. Met.**
   - **The image.** `amap_in_image` and `amap_out_image` (`:4451`, `:4467`) bound stream channel c on cluster c by min(format channels, port clusters). They also apply the ADD bounds (wire shape `SCH`, key range). The image is the stores' reset value (`:4629-4632`).
   - **The clip.** `amap_boot_clip` (`:4535`) re-applies the image against the processor's live format row each cycle while `amap_boot_r` is set (`:4761-4766`). It wins over the CSR assignments.
   - **When the window closes.** The window closes on `pp_restore_done_w || pp_restore_closed_w`. In the processor:
     - `restore_done_o` is `nvm_walk_done_w && lsn_released_w && d3_done_w` (`protocol_processor_top.sv:2768`);
     - the D3 walk starts only at `lsn_released_w` (`:3835`);
     - both of those terms are sticky.

     So `restore_done_o` rises in the same cycle as `d3_done_w`, and `aecp_rx_hold_w` releases AECP at `d3_done_w` (`:2822`).
   - **What a controller reads.** The input stores hold their final clipped value from the edge where the terminal is first seen, before any released command can be served. GET on an input reads only `amap_in_store_r` (`:3930-3941`). GET on an output reads the owner registers and `cmap_flat_w`. Those agree with the clip, because the in-window sweep has already written the clipped image, and because the output clip cannot be reached by a command (`SAVED_STATE_MATERIALIZATION.md` "Which judge").
   - **Notifications.** None is owed: registration is an AECP command, and AECP is held until then.
   - **Executed:** `[DYNMAP]` 142/0 (power-on SPI 0 and SPO 0: 8 identity records each, and both RAMs). Restore case: GET 4 ch, 4 identity mappings, RAMs agree, SET 8 SUCCESS. Output clip staged in the window. Killed P4, P6, P7, P8 and P10.

2. **Milan 5.4.2.7 BAD_ARGUMENTS is intact, and nothing prunes or adds at run time. Met.**
   - No processor file or gitlink changed (`protocol-processor` stays `631eeb34`).
   - `[DYNMAP]`: 8->4 is refused with 7, the format and both maps unchanged. REMOVE 4..7. 8->4 SUCCESS. 4->8 SUCCESS with 4 mappings kept.
   - `#67 a 1ch format that orphans channel 2 is BAD_ARGUMENTS` (`sim_nxn.cpp:6708`) still runs and passes in obj_nxn and obj_nxndv.
   - After the terminal the clip never runs again. P12 (the clip continuing) fails 10 checks.

3. **The boot writer, the edit face and the CSR window. Met by inspection; untested (F1).**
   - **The writer.** It drives the existing `amap_edit_iwr/owr` registers (`:4644-4654`). Its assignments sit before phase 5 in `amap_edit_commit`, so phase 5 would win the legs.
   - **The edit face** waits while `amap_boot_busy_w` (`:4358`).
   - **The CSR writer** is gated off on all four paths.
   - **Busy** covers the window, one sweep from key 0 after the terminal, and the drain cycle in which the last write lands. `KL_chan_map_capture` writes on the strobe edge (`:502-503`), so after the drain `cmap_flat_w` is current.
   - **No race with a controller edit.** No controller edit can start before AECP release. An edit started after release meets the wait at phase 0 at the latest, which is within the processor's bounded timeout, because busy ends within at most `max(keys) + 1` cycles.

4. **Area: +135 LUT after opt_design. Not a finding.**
   - **Where the LUTs are** (manager-published `area_ooc_1x1/hierarchy_delta.txt`): the parent's own cells grow +5 LUT and +6 FF; `pp_shadow` grows +189. The rest is cross-boundary movement in both directions.
   - **The reset image** costs nothing (published microbench: FDCE becomes FDPE, LUT counts identical).
   - **Why `pp_shadow` grows.** The +189 is the processor's existing edit-face wait path. It was pruned while the wait was tied to 0, and any non-constant wait brings it back.
   - **Cheaper alternatives, and why they are not equivalent:**
     - **Leaf reset images** still need a writer for the input clip, and they put hunks in leaves that #645 also edits (ruling item 6).
     - **Dropping the wait** would recover about 189 LUT. But output validation reads the capture RAM (`:4305`, `:4311`). The design would then be safe only because the output clip is unreachable today and AECP dispatch happens to take longer than one sweep, not by construction. The ruling's "same rule to STREAM_OUTPUT" makes that a different design, not a cheaper equivalent.
   - **Gate tolerance.** The growth is inside the resource gate's tolerances (route-1x1 +500, `AREA_BUDGET.md`). Recording it is a merge duty (below).

5. **Re-based, not relaxed. Met.**
   - `[AMAP]`: the power-on map is graded first, cleared through the CSR window, then put back and graded again.
   - `#67` and `#67dv` REMOVE the power-on mappings first and ADD them back afterwards. Their orphan refusals keep their own probe mappings.
   - `0x002C`: "key 0 EMPTY" becomes "key 0 = Pilot word 0x1400". On 8x8 it adds every port's GET page and every capture key.
   - `[T66]`: the capture keys are cleared, with two precondition checks.
   - Render `[MAP]`, `[MULTI]` and T18 prove the power-on map, then REMOVE it. They also decode it end to end after a hard reset (`T18 POWER-ON`).
   - pp_shadow K12 clears through CSR and adds "starts empty" checks.
   - No expectation was deleted without a replacement of equal or greater strength.
   - The ruled planted controls run inside the lane's campaign:
     - empty reset: 39 failures;
     - no clip after the restore: 5 failures.

     I re-ran both, with the clean control: 3/3 PASS.

6. **Docs. Met, with residue R1 and R2.**
   - `SAVED_STATE_MATERIALIZATION.md`: `:188` (reset value is the clipped identity, crossbar RAMs filled by the boot writer); `:595-604` (roll-back target is the clipped identity; stage 3 takes the window over); 8.4 at `:1195-1203` (formats judged on "supported" alone, no record trigger from the clip).
   - `ENDSTATION_BUILDER.md` D7 `:624-643`: the power-on map, the 5.4.2.7 rule, and the REMOVE-first bench consequence (8 -> 4 needs REMOVE 4..7 first).
   - `ENDSTATION_BUILDER.md` D8 `:731-733` and `:760-765`: the unconsumed `AEM_ODMAP_INIT_C`, and 8x8 channels 1..7 on unbacked loopback.
   - **Merge.** The branch merges cleanly with dev `fa450d30`: `git merge-tree --write-tree` gives tree `bf00f45c`, the same as the executor's trial. Dev's delta since the base touches only `sim_ax1x1gptp.cpp` and the milan_dp README. #645 has no open PR.

## Lens results

- `[R490] PASS Conformance - hdl/milan/milan_datapath.sv:4438-4480,4629-4632,4761-4766; protocol-processor/hdl/top/protocol_processor_top.sv:2768,2822,3835; receipts/dynmap_clean_head.log - identity image and clip against rulings 5988293154/5988843004; AECP release coincides with the window's terminal; Milan 5.4.2.7 refusal and run-time no-prune/no-add exercised (8->4 refused 7, REMOVE-first, 4->8 keeps 4, restore 4 ch + SET 8 SUCCESS)`
- `[R490] PASS RTL - hdl/milan/milan_datapath.sv:1155,1259,4358,4519-4616,4644-4654,4761-4766,6786; hdl/ieee1722/aaf/KL_chan_map_capture.sv:495-503 - widths and bounds of the image functions per generated config (5 configs), cursor wrap and width, write-leg priority versus phase 5, drain against the RAM write edge, reset values; lint ratchet 90 <= 90 with no hit in the new code (receipts/lint_rtl_check.log)`
- `[R490] PASS Robustness - milan_datapath.sv:4570-4573 (terminal, CLOSED), 4589-4616 (static ports and non-RPHYS keys), configs/generated/*/gen/adp_shape_defaults.svh (Arty static output, 8x8 empty input image); sw/firmware/milan_baremetal/milan_baremetal.c:1672-1676 (the walk starts on every path); render T19/T18 nested resets (receipts/leg_render.log 258/0) - reset during the window and during the sweep, a boot that never restores, roll-back to defaults (window row invalid again), mixed static/dynamic shapes`
- `[R490] UNCLEAN Tests - F1, F2 - otherwise checked: receipts/dynmap_clean_head.log 142/0, leg_nxn.log 1967/0, leg_nxndv.log 1969/0, leg_nxn8.log 3751/0, leg_render.log 258/0 + 71/0 + 5/5, leg_coherence_dp.log 332/0, leg_lane_mutants_1_2.log 3/3, reviewer_mutants_summary.txt (6 killed, 5 survived, 1 equivalent)`
- `[R490] UNCLEAN Docs - F2 (PR body) - otherwise checked: docs/design/SAVED_STATE_MATERIALIZATION.md:188,597-604,1195-1203; docs/ENDSTATION_BUILDER.md:624-643,731-733,760-765; docs/CHANNEL_MAP_64.md:363-375; docs/reference/REGISTER_MAP.md:2157-2162; docs/fpga/DATAPLANE_WALKTHROUGH.md:87; docs/testing/TESTING.md; tb/verilator/milan_dp/README.md; CHANGELOG.md; docs_check rc 0, doc style rc 0 (residue R1, R2 recorded, not blocking)`

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | rulings 5988843004 and 5988293154; `milan_datapath.sv` image, clip and window terminal; processor `restore_done_o` and AECP hold; `[DYNMAP]` 142/0; `#67` orphan refusal | R490-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| RTL | CLEAN | `milan_datapath.sv:1155-6820` hunks; `KL_chan_map_capture.sv:495-503`; 5 generated shape headers; lint ratchet | R490-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| Robustness | CLEAN | terminal and CLOSED arms, nested resets (render T18/T19), static-output and 8x8 shapes, firmware restore start, roll-back via an invalid row | R490-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| Tests | UNCLEAN (F1, F2) | `sim_nxn.cpp` `[DYNMAP]` and re-bases; render, talker and pp_shadow diffs; 12 reviewer mutants; lane controls 1-2; focused legs | R490-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| Docs | UNCLEAN (F2) | design page `:188`, `:595-604`, 8.4; ENDSTATION D7/D8; CHANNEL_MAP_64; REGISTER_MAP 0x900; walkthrough; TESTING; README; CHANGELOG; PR body | R490-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |

## Executed evidence (this round, at the exact head)

The simulator is pinned 5.050 (`--version`: "5.050 2026-07-01 rev v5.050"; wrapper sha256 `905795b9...e92f`).
All builds ran in a disposable clone of the review clone at `fb4953bd`, with submodules at the recorded gitlinks.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp dynmap` | rc 0, 142 checks, 0 failures | `receipts/dynmap_clean_head.log` |
| `probes/r490_mutants.py --jobs 5 --vjobs 3` (12 probes) | 6 KILLED, 5 SURVIVED (P1, P2, P3, P5, P9), 1 equivalent (P11) | `receipts/reviewer_mutants_summary.txt`, `reviewer_mutants_results.json`, `reviewer_mutants/` |
| `python3 dynmap_mutants.py 1 2` (lane controls) | rc 0, 3/3 PASS (empty reset 39 failures, no clip after restore 5) | `receipts/leg_lane_mutants_1_2.log` |
| obj_nxn, obj_nxndv, obj_nxn8 via `probes/r490_legs.mk` (the suite's own recipe lines) | rc 0: 1967/0, 1969/0, 3751/0 | `receipts/leg_nxn*.log` |
| `make -C tb/verilator/milan_dp_render run` | rc 0: 258/0, 71/0, leg defects 5/5 | `receipts/leg_render.log` |
| `make -C tb/verilator/capture_coherence dp` | rc 0: 332/0 | `receipts/leg_coherence_dp.log` |
| `scripts/lint_rtl.py --check` | rc 0, 90 <= 90 | `receipts/lint_rtl_check.log` |
| `scripts/check_rtl_source_lists.py`, `scripts/pp_srcs.py --check` | rc 0, rc 0 | `receipts/check_rtl_source_lists.log`, `receipts/pp_srcs_check.log` |
| `scripts/docs_check.py`, `scripts/check_doc_style.py` | rc 0, rc 0 | `receipts/docs_check.log`, `receipts/check_doc_style.log` |
| `scripts/check_em_dash.py --base e6172750` | NOT RUN: rc 2, the pinned renderer dependency is absent on this host | `receipts/check_em_dash.log` |
| hosted check runs on the exact head (snapshot 15:04 UTC) | executed and green: rtl-fast, elaborate, yosys-elaboration, Yosys shards 0-3, Verilator shards 0 and 3, lint, bdd, wire-accountability, docs-check-no-git; in progress: docs-check, Verilator shards 1, 2, 4; skipped: Physical gPTP | `receipts/hosted_checks_snapshot.txt` |
| review clone integrity after the round | HEAD and tree exact, porcelain empty, 1015 tracked blobs re-hashed equal, 4 gitlinks unchanged | `receipts/clone_integrity.txt` |

## Real limits

- **Not run in this round:**
  - the full milan_dp `run`, pp_shadow, the all-suites sweep, Yosys, the builder bank, `xvlog_gate.py`, the nightly gPTP leg and the area recipe;
  - the lane's mutants 3 to 6;
  - any Vivado measurement. The area figures are the published evidence, read but not reproduced.
- **Em-dash gate:** not judged here (missing dependency).
- **Not hardware proof:** physical calibration was not run, and no bench read was made. The field skips are not hardware proof.
- **Hosted evidence:** several hosted jobs were still running at the snapshot.
- **Author material:** I did not read the published author handoff or scratch material in `review-evidence/658-r1/author/`. I read only its executable logs and the area reports.

## Pending manager duties

- **Candidate merge.** Build the current-dev candidate (source base `e6172750`, live dev `fa450d30`). Re-run the nightly gPTP leg on it: it is the one dev delta, and it programs the capture map after the walk.
- **Resource gate** (`AREA_BUDGET.md` "A merge that moves the shipping image records its own re-baseline"). This PR carries no `syn/ooc/pp_resource_baseline.json` record. The route-1x1, ooc-1x1 and ooc-8x8 measurements and `record --write` on the merge result are owed in the merge bank.
- **Bench read** of the power-on maps on the AX7101 after flashing. The PR body's "Closes #658" excepts it.
- **Hosted and act acceptance** of the exact-head contexts still in progress.
- **Residue checklist:** R1 and R2.
- **Owner decision**, raised by the executor, non-blocking: on the 8x8 image (not shipped), whether the output identity should be restricted to backed clusters.
- **#645 overlap:** a later merge of #645 must re-run `dynmap` and `dynmap-mutants`, because both lanes edit `milan_datapath.sv`.

R490-1 FINISHED
