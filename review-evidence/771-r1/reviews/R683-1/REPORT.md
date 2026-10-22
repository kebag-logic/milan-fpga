[R683] NEGATIVE - exact head a97aea01449492b1f640924f5a34726f602cabed

Round R683-1, internal cleared-context review of kebag-logic/milan-fpga PR #772 (Closes #771, the fourth pin adoption), head `a97aea01449492b1f640924f5a34726f602cabed`, tree `ea69f3b4c4c4b2f50a38a868b5f1dba56b248249`, source base `d77a8afd`. All five lenses applied. One BLOCKER and two MINOR findings are open, so the verdict is NEGATIVE.

## Summary

- **The verdict-deciding defect:** a required parent gate is red at this head. The processor pin carries processor PR #195 (issue #189), which changes the processor's Milan Table 5.30 listener model. The parent's firmware ACMP walk replays that model against the firmware's ACMP core, and it now fails one cell (`TK_REG x SETTLED_RSV_OK`).
  - The hosted `firmware-unit` job at this head fails the same way, and I reproduced it locally.
  - The same suite passes at dev `d77a8afd`.
  - None of the eight supplied patches covers this.
  - The author's validation never ran this gate, so the PR's "every parent gate and suite passes" claim, and #771 acceptance 4, are not met.
- **Most of the lane checks out:**
  - Both gitlinks are exactly the two donor `main` tips, and nothing else in the donors changed.
  - The eight patches apply alone at `d77a8afd` and equal their commits byte for byte. Applied in order, they produce the head's bytes.
  - Every pin-derived record regenerates byte-identically through its generator.
  - The resource figures reproduce exactly from the published receipts, and the policy fields are unchanged.
  - The image-build corners meet the gate.
  - The only donor→parent interface change is the TSpec port the patch carries.
  - The adapted suites pass on my own runs: physical leg 209/0, gptp 185/0, gptp-lat 185/0, nxn 1,983/0, gm_steps 196/0, gptp_shadow 310/0, pp_shadow 2,187/0.
- **Two MINOR documentation defects:**
  - The parent's authoritative pages say thisClock is always appended to the path. At the 8-entry bound it is not, and I showed this with a probe.
  - Four parent places still describe the pre-#85 "count one is `[GM]`" meaning.

## Findings

### R683-1-F1 — BLOCKER — Conformance, Tests, Docs
- **Artifact:** `sw/firmware/ctrl/test/acmp_walk.cpp:472-488` (gate `sw/firmware/ctrl/test/test_ctrl_firmware.py`, arm `acmpwalk`). The changed model is at `protocol-processor/tb/acmp_listener/sim_main.cpp:404-408` at `93fb0b2d`. The firmware view is at `third_party/tsn-c-stack/src/acmp.c:431-432`.
- **Title:** The processor pin's #189 Table 5.30 model change makes the parent's firmware ACMP walk fail; the hosted `firmware-unit` job is red at this exact head.
- **Authority and evidence:**
  - #771 acceptance 4 says "Every parent gate and suite passes".
  - The assignment (issuecomment-6325107889) says to STOP if "a parent gate fails for a reason a patch does not cover". The owner decision (issuecomment-6333175429) keeps "the eight patches failing together" as a STOP condition.
  - `docs/testing/CI_WORKFLOWS.md:3158-3172` lists `test_ctrl_firmware.py` among the local gates.
  - **Hosted, exact head:** check run 119824279883 (`firmware-unit`) fails with `ctrl ACMP walk (processor stimulus and models): checks: 127 failures: 1`. The failing checks are `Table530/ListenerWalk.Graded/TK_REG_SOK`: "the talker's discovered and registered state" and "notified exactly when a Table 5.22 item moved". Receipt: `receipts/hosted/firmware-unit-119824279883.log`.
  - **Local, head:** `receipts/runs/fw_head_ctrl_firmware.log` gives the same 127/1 and rc 1.
  - **Local, base `d77a8afd`:** `receipts/runs/fw_base_ctrl_firmware.log` gives `acmpwalk` 127/0 and `test_ctrl_firmware: PASS`. Hosted `firmware-unit` at `d77a8afd` is also a success (run 39550668025).
  - **Cause:** between `2cbed0a9` and `93fb0b2d`, the only behavioural change to the processor's listener model is processor PR #195's hunk for issue #189 (Milan Table 5.39). In SETTLED_RSV_OK, a Talker registration now moves REGISTERING_FAILED to follow the registered type. The firmware core does not move its REGISTERING_FAILED view and notifies nothing.
  - A probe that removes that hunk from the processor model was refused by the walk's own pinned-blob guard (`receipts/runs/probe_fw_no189model.log`). Attribution therefore rests on the failing cell and the model diff.
  - The author's validation lists (REVIEW READY issuecomment-6340721641 and the PR body "How to validate") do not include `test_ctrl_firmware.py`, yet the PR body says every local gate is green.
- **Impact:**
  - Merging turns dev's `firmware-unit` red.
  - The firmware's Table 5.30 implementation and the adopted processor now disagree on GET_RX_STATE REGISTERING_FAILED, and on the Table 5.22 notification, for an in-place Talker Advertise↔Failed swap while settled.
  - The other firmware jobs at this head (`firmware-control-mutants`, `firmware-srp-mutants`, `firmware-boundary`, `firmware-verilator`) were cancelled by fail-fast, so their results at this pin are unknown.
- **Required outcome:**
  - Publish the STOP or decision for this gate failure.
  - At a new head, the parent's firmware gates must pass. That means either the firmware ACMP core follows the #189 behaviour, or the walk records the divergence under a published owner decision.
  - The local firmware gate set in `CI_WORKFLOWS.md:3158-3172` must be run and its receipts posted.
  - The PR's gate claims must match what was run.
- **Verification:**
  - `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test` passes, with `acmpwalk` at 0 failures.
  - The hosted `firmware-unit` job and the jobs fail-fast cancelled at this head succeed at the new exact head.

### R683-1-F2 — MINOR — Docs, Conformance
- **Artifacts:** `docs/reference/REGISTER_MAP.md:1473-1475`, `docs/reference/SUBMODULES.md:244`, `CHANGELOG.md:73-74`.
- **Title:** The parent states, without qualification, that the served path is the received pathSequence with thisClock appended and that every count gains one entry. At 8 or more received entries, the served path omits thisClock.
- **Authority and evidence:**
  - Donor PR #86 says: "Eight or more received entries still publish their first eight… widening it would be a port change."
  - The parent's own maximum-path tests expect count 8 with the peer as the final identity: `tb/verilator/gptp_shadow/sim_main.cpp:950-955` and `tb/verilator/milan_dp/sim_gptp.cpp:1497-1527`.
  - My disposable probe on an 8-entry received path, `receipts/runs/probe_bound_thisclock.log`: "ends with thisClock" FAIL, got `0080e1fffe112233` (the peer); "count includes thisClock (9)" FAIL, got 8.
  - The changed text cites IEEE 802.1AS-2020 10.3.13.2.4 f) 5) as unconditional.
- **Impact:** A cold integrator, or a controller-side reader, would expect GET_AS_PATH always to end with thisClock. The bounded deviation from the cited clause is not disclosed where the parent states the contract.
- **Required outcome:** All three statements name the bound. At 8 or more received entries, the served sequence is the first eight received entries, the count stays 8 and thisClock is not appended (donor #86).
- **Verification:** Text review against `sim_gptp.cpp:1497-1527`. The docs-check gates stay green.

### R683-1-F3 — MINOR — Docs, RTL
- **Artifacts:**
  - `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:635-640`
  - `hdl/milan/milan_datapath.sv:2152-2158`
  - `hdl/milan/KL_pp_shadow.sv:456-461` (the `gsi_asp_chg_i` port contract)
  - `README.md:170-172`
  - `docs/reference/REGISTER_MAP.md:334-335`
- **Title:** The adoption leaves the pre-#85 count semantics in parent contracts.
- **Authority and evidence:**
  - `KL_gptp_shadow.sv:637-638` says "count one is the explicit one-entry `[GM]` sequence". At this pin, an explicit one-entry PathTrace publishes count two. `tb/verilator/gptp_shadow/sim_main.cpp:929-932` expects exactly that, and the old-pin probe below fails on it.
  - Count one now occurs only as `{thisClock}` before a peer (#82).
  - The other four places describe the 0/1 boundary as empty/`[GM]` without that meaning.
  - AGENTS.md section 5 says to update authoritative documentation when behaviour changes.
  - The author disclosed only the first two (REVIEW READY item 4), and no public issue tracks them.
- **Impact:** A maintainer reading the port contract or the README misreads what count one and count two mean when changing the AS_PATH notification comparator.
- **Required outcome:** The five places state the adopted semantics: 0 means absent, `{thisClock}` means count one before a peer, and a received sequence gains thisClock. Cite FPGA-gPTP #82 and #85.
- **Verification:** Text review. `scripts/check_port_contracts.py` and `scripts/lint_rtl.py --check` stay green. A comment-only RTL change moves the resource input digests but no figure; `pp_resource_gate.py check` returns 0.

### R683-1-R1 — RESIDUE (comment rule, owner 2026-10-15) — RTL, Docs
- **Artifact:** `hdl/milan/KL_pp_shadow.sv:1278-1279`. The new comment opens "scratch only:", which carries the consumer bank's scratch-parent context into shipping RTL and calls the shipped connection scratch.
- **Exact fix:** replace the two lines with:
  - `//! processor issue #190: one MaxFrameSize per talker source; every slot is`
  - `//! driven with this wrapper's one value, so each declaration is unchanged`
- Wording only. It does not affect the verdict or lens coverage.

### R683-1-S1 — SUGGESTION — Tests, Robustness
- **Artifacts:** `tb/verilator/milan_dp/Makefile:386`, `tb/verilator/pp_shadow/Makefile:137`, `tb/verilator/capture_coherence/Makefile:122`, `tb/verilator/milan_dp_mclk/Makefile:107`, `tb/verilator/milan_dp_render/Makefile:152`.
- **Finding:** `ucode.hex` depends only on `gen_ucode.py`. From `93fb0b2d`, the generator also reads `protocol-processor/hdl/aecp/ucode/aecp_commands.json` and `aecp_fields.json` (processor #73; `receipts/donor_file_lists.out`). A later pin that changes only those JSON files would leave an incremental tree's ROM stale. `syn/yosys/ooc.sh` regenerates on every run, and fresh CI trees are unaffected.
- **Suggestion:** Add the two JSON files as prerequisites.

### Prior public findings
At this head the PR has no reviews, no review comments, and only the two review-start notices. #771 has no reviewer findings. There is nothing to resolve or retain.

## Check-by-check (the brief's items)

1. **Only the two gitlinks change in the donors.**
   - `protocol-processor` moves `2cbed0a9`→`93fb0b2d736b36588ea7321e25fba2f8819ea41f` and `gptp-processor` moves `e4869fd0`→`55680bff3b287b9a7b0c759f51471fa617c17335`. Each is its donor's `refs/heads/main`, and each old pin is an ancestor of its new one.
   - The first-parent merges are processor #173, 175, 174, 180, 182, 183, 187, 191, 194, 196, 195, 197, 199 and 198, and FPGA-gPTP #78, #83 and #86, exactly #771's list. `external` and `third_party/*` are unchanged.
2. **The eight patches as validated.**
   - `receipts/check_patches.out`: each patch applies alone at `d77a8afd`. Each commit equals its patch applied to the commit's parent. All eight in commit order reproduce the head's bytes for the seven touched files, and nothing later touches them.
   - Composed files: `sim_nxn.cpp` (#67 and G9), `sim_gptp.cpp` (#85 and #82) and `sim_ax1x1gptp.cpp` (#85, #82 and #84). Their hunks are disjoint, every check from every patch is present at head, and my runs of those suites pass.
   - The patches' contents match the donor PR descriptions (processor #194/#183/#197; FPGA-gPTP #86 "Parent companions").
   - **Limit:** no public byte anchor of the lanes' consumer-bank patch files exists. I compared against the published evidence copies and the donor PR descriptions.
3. **Pin-derived records.**
   - Regenerated byte-identically: `bash syn/yosys/ooc.sh --record-rom-digests` (the ROMs come from the generators) and `check_port_contracts.py --write-budget`. In both cases `git diff` is empty (`receipts/regen/`).
   - `rc 0` (`receipts/quick_gates/`): `submodule_boundaries.gen.py --check`, `timesync_chain.gen.py --check`, `check_submodule_docs.py`, `check_gptp_docs.py --with-submodule`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `lint_rtl.py --check` and `check-integrator-params.py`.
   - `ltn_rom.hex` is unchanged. `ucode.hex` and `gptp_ucode.hex` change.
4. **Re-baseline.**
   - `receipts/baseline_records.out`: tolerance, floor and ceiling are identical to `d77a8afd` at all three endpoints. Each head record equals the author's `record-head-*` receipt, and the identities match across the #708 record, dev and head.
   - Deltas recomputed from the receipts: route-1x1 +770/+210 vs dev (+1,146/+479 vs #708); ooc-1x1 +462/+177 (+514/+179); ooc-8x8 +2,185/+769 (+2,256/+769).
   - The route split checks out: gPTP plane +415, wrapper +353, datapath 42,248. So does the 8x8 listener at +2,112/+720 (`receipts/scope_deltas.out`). The AREA_BUDGET arithmetic also checks out: 80.06 %, 12,719 over, 122 free slices, wrapper ≤ 11,070, and the WNS fall limit binds at +0.041 ns.
   - The records follow the recipe (`synth.maxThreads 1`, `record --write`, `check-baseline` rc 0), cite issuecomment-6333175429, and carry the per-donor ledger.
   - **8x8 share:** I judge it clearly stated as recorded under the owner's exception. It appears in the 8x8 `measured` note, the findings section, `AREA_BUDGET.md:114-115` and `:499-503`, and the PR's Known limitations. The decision accepts "the adoption's area" and orders "the baseline record write" and "the 8x8 standalone", but quantifies only the 1x1 figures, so confirming it is the owner's call (pending duty below).
5. **Image build.**
   - From `image-builds.json`: ExtraPostPlacementOpt Slow +0.291/+0.102 and Fast +1.660/+0.036. AltSpreadLogic_high +0.083/+0.004 and +1.633/+0.011. ExtraTimingOpt +0.297/+0.004 and +1.633/+0.008. All nets routed, IOB 21/0.
   - Every corner of every directive meets WNS ≥ +0.03 and WHS ≥ 0.
   - The thread count (2 and 1 instead of `BUILDING.md:344`'s 32) does not affect validity. The gate judges the routed image's own corners, the rule's stated reason is Vivado's cap, and the 2-thread selected image reproduces the recipe route's figures exactly (50,759 / 52,832 / 15,728, +0.291 / +0.036).
   - **Limit:** `parent_head_at_launch` is null in that receipt. Validity rests on the RTL inputs being unchanged after `8de4b80b`, which I confirmed for `hdl/`.
6. **Sweep and gates.**
   - The author's tally sums to 63 suites, 2,189,520 checks and 0 failures; physical 209.
   - My own runs at this head:
     - physical `milan_dp_gptp` 155+6+20+14+14 = 209/0, rc 0, including the #84 holdover, "loss leaves this station grandmaster" and thisClock-tail checks;
     - `milan_dp` `gptp` 185/0, `gptp-lat` 185/0 and `nxn` 1,983/0 (#67 and G9 rows);
     - `milan_dp_gm_steps` 190+6/0;
     - `gptp_shadow` 310/0;
     - `pp_shadow` 2,187/0.
   - Old-gPTP-pin probe: exactly the five #85 rows fail (305/310), so the adapted expectations detect the change.
   - Yosys 58/58, behave 406 and xvlog 0 come from the author's receipts. The hosted docs-check replica has 42 run steps at rc 0 and 2 skipped by rule.
   - **This item fails on F1.** The firmware gate set was not run, and hosted `firmware-unit` is red.
7. **Interface.** `receipts/interface_diff.out`: of the donor modules the parent instantiates, `protocol_processor_top` differs only in `cfg_tspec_max_frame_i` `[15:0]`→`[N_STREAM_OUT_P*16-1:0]` (carried by the scratch-TSpec patch). `KL_gptp_engine`'s header is identical. No donor HDL file was added or removed, apart from two new generator JSON inputs.

## Lens results

- [R683] BLOCKER Conformance — `sw/firmware/ctrl/test/acmp_walk.cpp:472-488` — #771 acceptance 4 unmet (F1); MINOR Conformance — `docs/reference/REGISTER_MAP.md:1473-1475` (F2).
- [R683] MINOR RTL — `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:635-640`, `hdl/milan/KL_pp_shadow.sv:456-461` — stale count contract (F3). Otherwise the RTL is correct:
  - the TSpec replication width matches `protocol_processor_top.sv:303`;
  - the public path clamp at `KL_gptp_shadow.sv:643-658` holds at count 8;
  - `KL_gptp_engine`'s ports are unchanged;
  - no CDC or reset path changed.
- [R683] PASS Robustness — Checked boundary and failure paths against the adopted clauses at this head. The artifacts are `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:643-658` (hostile and maximum count clamp) and `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` reset, peer-loss and holdover arms (my run 209/0). Also:
  - maximum-path cases at `sim_gptp.cpp:1497-1527` and `gptp_shadow/sim_main.cpp:950-955`;
  - #67 malformed/bit-31 SET_STREAM_INFO rows in `sim_nxn.cpp` (1,983/0);
  - `hdl/milan/KL_pp_shadow.sv:1280`, every slot driven: the width is exact, and an under-driven port is a lint WIDTHEXPAND error per processor PR #194.
  - The bound behaviour is safe (no overflow or garbage tail). Its documentation is F2, not a robustness defect.
- [R683] BLOCKER Tests — required gate red at head (F1); SUGGESTION Tests (S1).
- [R683] BLOCKER Docs — the PR's gate claims (F1); MINOR Docs (F2, F3); RESIDUE (R1).

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 BLOCKER, F2 MINOR) | #771 acceptance 1-5; the patches against IEEE 802.1AS-2020 10.3.13.2.4 b) f) 5) i), IEEE 1722.1-2021 7.4.41 and Milan v1.2 5.4.5.1 / Table 5.22 / Annex B.1.1; GET_AS_PATH cdl/length arithmetic; `REGISTER_MAP.md`, `SUBMODULES.md`; hosted and local `firmware-unit` | R683-1 | a97aea01449492b1f640924f5a34726f602cabed |
| RTL | UNCLEAN (F3 MINOR) | `KL_pp_shadow.sv:1278-1280`, `:456-461`; `KL_gptp_shadow.sv:635-658`; `milan_datapath.sv:2152-2158`; donor `protocol_processor_top`/`KL_gptp_engine` headers at both pins; lint and port gates | R683-1 | a97aea01449492b1f640924f5a34726f602cabed |
| Robustness | CLEAN | clamp `KL_gptp_shadow.sv:643-658`; reset, loss and holdover arms in `sim_ax1x1gptp.cpp` (209/0); max-path tests; #67 malformed rows; TSpec width | R683-1 | a97aea01449492b1f640924f5a34726f602cabed |
| Tests | UNCLEAN (F1 BLOCKER) | eight patches (alone, commit-equal, sequence = head); my suite runs; old-pin probe 305/310; bound probe; firmware walk at head (127/1) and base (127/0) | R683-1 | a97aea01449492b1f640924f5a34726f602cabed |
| Docs | UNCLEAN (F1, F2, F3) | findings section, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, `SUBMODULES.md`, `REGISTER_MAP.md`, `CHANGELOG.md`, `README.md`, the PR body and REVIEW READY, the record notes | R683-1 | a97aea01449492b1f640924f5a34726f602cabed |

## Real limits

- I ran no Vivado, no full parent sweep, no Yosys bank and no builder bank, as the brief requires. The resource, image, Yosys, behave, xvlog and docs-check figures are the author's receipts, which I checked for internal consistency and arithmetic. Resource input digests cannot be recomputed without the Vivado measurement directories.
- No RV32 compiler was present, so my `test_ctrl_firmware.py` runs were host-only: RV32 arms skipped, no `--self-test`.
- The firmware jobs that fail-fast cancelled at this head (control, srp mutants, boundary, verilator) were not run.
- The #189-hunk removal probe was refused by the walk's pinned-blob guard.
- No public byte anchor exists for the lanes' consumer-bank patch files.
- No manager source bank runs at this head, and I claim none.
- The current-dev merge candidate was not built by me.
- Physical calibration was NOT RUN, and no hardware was used.

## Pending manager duties

- **F1:** decide the STOP or disposition, and own the hosted `firmware-unit` result and the jobs fail-fast cancelled at this head.
- Confirm or refuse that the owner exception covers the ooc-8x8 share (+2,185 LUT / +769 FF over dev), as asked in the author's open question 1.
- **Acceptance 5 lists processor #190 for closure after merge.** Processor PR #194 states that #190's first item, the CRF stream's own MaxFrameSize, is not done. The CRF still declares the AAF value (the issue's 217). No parent issue tracks it, so closing #190 would leave that defect untracked.
- Accept the image build's reduced Vivado thread count, a deviation from `BUILDING.md:344`.
- Carry R1 to the residue checklist.
- At the merge turn: hosted and act acceptance at the exact head, the current-dev candidate build, and the post-merge bench (DUT identity gate, #637 cold power cycle, soak).

## Receipts

Every published receipt is listed in `MANIFEST.sha256`. They are under `receipts/` (gate logs, regenerations, baseline and scope recomputation, interface diff, patch check, suite and probe logs, hosted check runs and the `firmware-unit` log), and the scripts are under `scripts/`. Local paths are redacted to `$REPO`, `$PACKET` and `$HOME`.

R683-1 FINISHED
