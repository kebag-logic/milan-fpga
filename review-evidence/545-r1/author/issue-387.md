# 387 [Fabric] GM step re-base: decide and prove how the media plane re-bases on a PHC step now that the fabric plane owns the servo

Drafted from the README product roadmap, phase P1 (README.md lines 334 to 336: "software DLL (GM step re-base)"). No open issue owns it at dev f46215cf. The wording predates the fabric gPTP plane: REQUIREMENTS.md lines 26 to 27, REQ-PTP-05 and REQ-PTP-09 make the fabric plane the sole PHC and servo owner and forbid software from manufacturing gPTP health, so a software DLL is no longer a product path. What the item still names is the media plane's reaction to a PHC step.

## Objective and evidence

Decide, document and prove the behaviour of the media plane when the fabric gPTP plane steps the PHC (grandmaster change, first sync, settime), so that a locked stream returns to its steady state through one bounded, counted event rather than a minutes-long walk.

- The plane exposes a step interface and no policy. `gptp-processor/docs/INTEGRATION.md` lines 96 to 106 list `phc_addend_we_o` (rate) and `phc_step_we_o` / `phc_step_o` (phase step) as pulses; `hdl/milan/milan_datapath.sv` lines 6124 to 6125 wire them. Whether the microcode steps above some offset and slews below it, and what that threshold is, is recorded nowhere in the parent tree; `docs/design/TIME_SYNC.md` lines 58 to 59 say only "Rate updates steer PHC frequency. Phase updates step PHC time".
- The one media consumer of a step is pruned on the shipping shape. `milan_datapath.sv` lines 5600 to 5617 derive `gm_recentre_p_r` from a change of the published GM identity (not from `phc_step_we_o`) and feed it to `KL_i2s_playback` (`recenter_p_i`, line 5634; `hdl/ieee1722/aaf/KL_i2s_playback.sv` lines 103 to 108 and 325 to 333, task #22). `configs/endstation_ax7101_1x1_tdm8.yaml` line 35 prunes that block, and the TDM render path (`KL_chan_map_render`, `KL_tdm_render`), `KL_media_grid_align`, `KL_media_nco` and `KL_mmcm_drp_servo` have no step input (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` lines 36 to 38 only guard one window against a local `ptp_now` step).
- The publication side is defined: a GM change or PHC step raises `tu` immediately and holdover lasts at least 0.25 s (`docs/design/TIME_SYNC.md` lines 134 to 138; `docs/design/GM_LOSS_RECOVERY.md` lines 61 to 63 and 87 to 103; REQ-PTP-08). `docs/integration/BAREMETAL_FIRMWARE.md` lines 687 to 688: "the fabric plane owns adjfine and adjtime. When an external grandmaster is selected, that plane steps and disciplines the PHC".
- The failure this item was written against was measured before the plane existed: a handover that stepped the PHC by tens of seconds left the media servo grinding for about two minutes (README.md P1.7; the task #22 comment at `milan_datapath.sv` lines 5600 to 5606). No measurement of the fabric plane's handover on the shipping image exists; #117 owns that bench.

## Authority and scope

- REQUIREMENTS.md REQ-PTP-05, REQ-PTP-07, REQ-PTP-08, REQ-PTP-09; docs/design/TIME_SYNC.md, docs/design/GPTP_PLANE.md, docs/design/GM_LOSS_RECOVERY.md; docs/reference/FR_NFR.md NFR-REL-01.
- Milan v1.2 4.2.6, Table 5.4, 5.3.8.10 with Table 5.6, Annex B.1.1 (cited at `milan_datapath.sv` line 162); IEEE 1722-2016 4.4.4.3 and 4.4.4.7; IEEE 802.1AS-2011 10.2 and 10.3.
- Context: the `gptp-processor` servo microcode and `docs/INTEGRATION.md`; `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv` lines 83 to 84 and 528 to 529; `milan_datapath.sv` lines 5255 to 5296 and 5599 to 5660; `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv`; `tb/verilator/gptp_shadow`, `clkvalid`, `media_grid_align`, `milan_dp` `obj_gptp`.
- Two design decisions first, recorded here: (a) the plane's step policy (step above what offset, slew below it, whether a GM identity change always steps), owned by the donor and recorded in the parent; (b) the media plane's re-base on a step: which elements re-center (the render elastic stage of the deterministic-latency item, the grid aligner's phase reference, the CRF servo's window), whether the re-base pulses `mr` (4.4.4.3) and counts MEDIA_RESET, and that it never stops a licensed stream (REQ-PTP-08).

Out of scope: any software servo or time daemon (REQ-PTP-09, #116, #259); the timestamp latency split (#64), the egress window (#213, #360); the two-board bench itself (#117); the CRF rate loop design (#74).

## Acceptance and validation

1. Both decisions are recorded here before any edit, with the donor issue number for the step policy.
2. `docs/design/TIME_SYNC.md` and `GM_LOSS_RECOVERY.md` state the step policy and the media re-base in one place each; `scripts/check_gptp_docs.py` and `python3 -B scripts/docs_check.py` pass.
3. `tb/verilator/milan_dp` (the gPTP-ON consistent-clock leg of #367) drives a GM change that steps the PHC by more than one second while an AAF stream is bound and locked under CRF selection, and asserts: `tu` rises on the commit edge and clears after holdover; the stream stays licensed; the render delay returns to its constant through one counted event; MEDIA_RESET and `mr` behave as decided; a negative control (re-base disabled) shows the drift back and fails.
4. On two boards, the #117 GM handover measurement records the time from the step to relocked media (`MEDIA_LOCKED` and `MEDIA_UNLOCKED` per Table 5.6, `CLKV_STAT` `tu`, `A_MCSRV_STAT`) inside the bound recorded in item 2, with the raw artifacts retained per docs/testing/TESTING.md 6b.
5. Yosys and Verilator gates green on the exact candidate; the gPTP ROM regenerates from the configuration through `scripts/regen.sh`, never hand-edited.

## Lane and review

Executor: unassigned. Independent reviewer: unassigned. Assigned by the manager when the lane opens.

Dependencies: the donor `gptp-processor` for the step policy; #117 for the bench; #367 for the consistent-clock gPTP-ON simulation; the deterministic-listener-latency item for the render element that re-centers. Lane conflicts: #74 (grid chain), #358 (admission bring-up), any branch touching `KL_gptp_shadow.sv` or the clock-validity block.

Unresolved decisions: the two above. Backlog until recorded.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5606198212
[A10] Decisions recorded from the owner's approval of 2026-09-09 (acceptance 1):

(a) Step policy of the gPTP plane, owned by the donor and recorded there as https://github.com/Mister-M-alt/FPGA-gPTP/issues/68: the plane steps the PHC only on the first synchronization after asCapable and when the offset to the selected grandmaster exceeds one second; below that it slews through the rate path; a grandmaster identity change alone does not step when the new offset is below the threshold.

(b) Media re-base on a step: the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event; the CRF servo keeps its window guard; the re-base pulses `mr` (IEEE 1722-2016 4.4.4.3) once and increments MEDIA_RESET once; a licensed stream is never stopped (REQ-PTP-08).

The lane opens once #386's render element is in the tree (dependency named in the body); acceptance 2, 3 and 5 in that lane, acceptance 4 on the #117 bench.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5652830424
[A114] Milestone board reconciliation

This Issue is open but its card showed Done. The owner decisions are recorded in comment 5606198212, and PR #435 has now landed the render element dependency. Donor issue Mister-M-alt/FPGA-gPTP#68 remains open; the step-policy implementation, remaining parent acceptance evidence and the booted-board measurement in acceptance 4 have not been recorded as complete here.

Returning the card to Ready with that dependency explicit. The next lane follows the donor policy into the parent and verifies the remaining digital acceptance; physical acceptance stays on the #117 bench. No completion claim or deadline change.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5772966033
[A10] gPTP processor dependency audit; this remains the existing adoption owner.

Donor https://github.com/Mister-M-alt/FPGA-gPTP/issues/68 is already linked by the [2026-09-09 decision](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5606198212). No duplicate parent tracker is needed.

Parent dev `b17580b91deb11f3441dfc5d7f9fafe539d929b8` pins donor main `c1b617435824929a790739ea8585c3fe1a328cc0`, whose [generator still sets STEP_NS_C=20000](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/hdl/ucode/gen_gptp_ucode.py#L378) and [uses it in the servo](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/hdl/ucode/gen_gptp_ucode.py#L741). Being pinned to donor main therefore does not implement the recorded one-second policy.

This issue continues to own adoption of the reviewed donor fix, configuration-generated ROMs, the media re-base and digital acceptance. #117 retains the physical evidence. The recorded first-sync/threshold/GM-change decision and frozen acceptance remain authoritative; no new interpretation or completion is asserted by this mapping.

[Complete gPTP processor audit and donor ownership index](https://github.com/kebag-logic/milan-fpga/issues/415#issuecomment-5772965268).


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5794731090
[A10] OWNER DECISION 2026-09-23 14:15 (supersedes the 2026-09-09 step rule, https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5606198212 part a): the gPTP servo steps the PHC at link-up (the first synchronization after asCapable) when the offset exceeds 20 us; once locked, including after a grandmaster change, it slews offsets up to 100 us and steps above 100 us; every step is one counted event (tu, one mr toggle, one MEDIA_RESET, per decision part b, unchanged); the total written rate, proportional plus integral, is always clamped to the parent's +-200 ppm reconstruction envelope. Basis: the reference Linux implementation's default first-step threshold is 20 us; a widely used embedded gPTP stack slews only up to 100 us and jumps beyond; this plane's slew authority is +-200 ppm, so 100 us settles in at most 0.5 s and the device stays aligned with third-party peers after a real grandmaster time jump. Both reviews on the donor PR (R258-1, R259-1) found the unclamped slew; this decision also fixes that.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5800693336
[A10] ASSIGNMENT: A214 author, parent adoption of donor FPGA-gPTP main e5dcea6e (merge of PR #74; tree identical to the reviewed head ba926810; R258-3 and R259-3 POSITIVE), under the standing exact-reviewed-head pin rule. Scope: the gptp-processor pin bump with the ROM regenerated through scripts/regen.sh and the yosys ROM digests re-recorded; acceptance 2 (TIME_SYNC.md and GM_LOSS_RECOVERY.md state the step policy of 5794731090 as ruled in FPGA-gPTP#68 5798089412, and the media re-base, once each); acceptance 3 (the milan_dp gPTP-ON leg drives a GM change that steps the PHC by more than 1 s while an AAF stream is bound and locked, and asserts tu, the licence, one counted re-base event, and MEDIA_RESET and mr as decided); acceptance 5 (yosys and Verilator gates). #529 holds milan_datapath.sv, sim_nxn.cpp and CHANGELOG.md, so any edit there waits for it. Acceptance 4 (the booted-board handover measurement) is the manager's bench step after merge. Branch 387-gm-step-rebase from dev 759da623.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802234836
[A214] REVIEW READY

Author lane for #387 under the [assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5800693336). The branch is committed locally only: no push, no PR edit, no merge.

| Item | Value |
|---|---|
| Branch | `387-gm-step-rebase` (lane checkout `$DATA/lanes/387-gm-step-rebase`), from dev `759da623072358afdb0e9d570a7b4b6a788492c9` |
| Commit | `44bf089108fec666d50873445720b51090ceede0`, tree `48f1348f589dd7e75873df22dde4ab2f4eaf6f97`; four one-line commits, no trailers; working tree clean |
| Lane record | `$DATA/reviews/387-a214-packet` (linked from `$HOME/milan-fpga-management/2026-09-23/387-a214`): `HANDOFF.md`, `PR-BODY.md` ("Part of #387"), `receipts/`, `work/` (the proposed datapath patch, its verified copy, the negative-control runner), `MANIFEST.sha256` |

**Changed.**
- `6caee191`: `gptp-processor` `c1b61743` -> `e5dcea6e` (donor main, the merge of FPGA-gPTP PR #74; tree equal to the reviewed `ba926810`). `syn/yosys/rom_digests.tsv` gains the pin's row through `./ooc.sh --record-rom-digests` (`4afe436d...`). The donor deep links, the pin table and the two pin-bearing diagrams follow the gitlink through their own generators.
- `6273e4be`, `44bf0891`: `TIME_SYNC.md` "Step policy" and `GM_LOSS_RECOVERY.md` "Media re-base on a PHC step", once each.
- `f0ba7ba1`: `tb/verilator/milan_dp/sim_gmstep.cpp` and the `gmstep` target, a separate harness. No hot file is touched.

| Acceptance | State | Evidence |
|---|---|---|
| 1. Decisions recorded | Met before this lane | 5606198212, 5794731090; donor FPGA-gPTP#68 with ruling 5798089412 |
| 2. Policy and re-base in the two docs, gates pass | **Met** | `check_gptp_docs.py` OK (also `--with-submodule`); `docs_check.py` 0 findings; style, em dash, paths, TOC, feature status and diagrams OK |
| 3. `milan_dp` gPTP-ON leg drives a >1 s GM step under CRF selection | **Not met: blocked by the hot file** | `gmstep`: 40 checks, 37 pass on this tree. The three failures are the decided behaviour the datapath lacks: 2 counted render re-bases instead of 1 (the identity trigger and the step), 0 `mr` toggles, 0 MEDIA_RESET. The exact edit (`milan_datapath.sv` lines 3091-3092 and 5958-5967) on a scratch copy gives 40/40, and 7/7 negative controls are caught, one or more per assertion |
| 4. Two-board handover measurement | The manager's bench step after merge | not attempted |
| 5. Yosys and Verilator gates; ROM regenerated, never hand-edited | **Met** (not-run items below) | table below |

The pin regenerates every ROM. `scripts/regen.sh` does not exist in this tree, and no gPTP ROM is tracked here. Each consumer regenerates the image from the pinned generator: the builder per configuration, the Yosys and OOC flows, and every suite's Makefile. Every configuration's image changes (`receipts/per-config-gptp-rom-digests.txt`). The donor images match PR #74's table.

**Validation** (Verilator 5.050 pinned wrapper, at most 8 jobs):

| Gate | Result |
|---|---|
| `gptp_shadow` / its mutants / lifecycle | 309/309; 9/9 caught; PASS |
| `gptp_plane`; `gptp_txts` | 29/29; 85/85 with 6/6 controls |
| `clkvalid`; `media_grid_align` | 55 checks, 0 failures; 25/25 with the negative control red |
| `milan_dp` gptp, gptp-lat (new ROM) | 181/181 each |
| `milan_dp` option-off, ax1x1, aclk | 230/0, 227/0, 139/0 |
| `test_builder.py` | all gates pass except gate 11, NOT RUN (needs a hardware build tree) |
| Yosys full: `KL_gptp_shadow`, `milan_datapath` | PASS, with tied-input and tap purity |
| `ooc.sh tcam` (validates the new ledger row); OOC and cache self-tests | PASS |
| `check_rtl_source_lists`, `xvlog_gate --check` (4 == ratchet), `lint_rtl --check`, `check_baremetal_only --check`, `check_cpp_idiom`, `check_py_idiom` and the other code-quality ratchets | PASS, nothing raised |
| `git diff --check 759da623 HEAD` | clean |

Not run:
- The full `milan_dp` `run` recipe exceeds this session's per-command limit. Its source list and option-off flags are byte-identical to the base (sha256).
- The physical `milan_dp_gptp` leg is nightly. Its 10 us peer slews under both the old and the new rule.
- The `tsn_fuzz` gPTP campaign needs `tsn-gen`, which is not installed here. Its 1 to 6 us offsets slew under both rules; the hosted job confirms.

**Open questions:**
1. **Acceptance 3's negative-control wording needs a decision.** It asks for "re-base disabled shows the drift back and fails". The #386 render stage is timed from accept, not from presentation time, and late or early PDUs are still accepted. So disabling the step's re-centre leaves the fill constant: measured, and only the count check fails. The failing arms that exist are the count and a mis-snapping re-centre. Please rule whether that satisfies the criterion, or name a PHC-dependent element that should drift.
2. **Two `mr` requests can cancel.** Inside `KL_media_clock_restart`'s 8-PDU hold, a CRF disruption plus a step would flip the target twice. The edit's lane should decide whether a re-base coalesces with a pending restart.
3. **Proposed new issue (derived from reading, not simulated).** `KL_mmcm_drp_servo` discards a window only above 1024 ppm, but steps of about 108 to 524 us fall between that and the ~211 ppm legitimate bound. Every locked step is now above 100 us.
4. The I2S element (Arty shapes, line 5983) still re-centres on the GM identity. It is left as is, because the decision names only the render stage and the aligner.
5. The talker in `gmstep` is opened by `AAF_CTRL[1]`, not an lwSRP licence.

Remaining after #529 releases `milan_datapath.sv`:
- apply `work/proposed-milan_datapath.patch`;
- wire `gmstep` and `gmstep_mutants.py` into the sweep, with its test-evidence reader disposition;
- turn the "Not yet" rows;
- add the CHANGELOG entry.

Then #387 can close on the #117 bench step. `HANDOFF.md` has the list.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260
[A10] RULINGS on A214's open points (manager, technical conformance, 2026-09-23):
1. Acceptance 3, "re-base disabled shows the drift back": A214 measured that the render stage is timed from PDU acceptance, not from presentation time, so a PHC step does not move its fill. The clause cannot fail as worded. It is replaced by: disabling the re-centre must fail the one-counted-event check. The other acceptance 3 assertions stand.
2. A step that lands while an `mr` restart is pending (for example a CRF disruption plus a step) merges with it. The result is exactly one restart, never a cancellation, and the step's MEDIA_RESET is still counted. The follow-up edit implements this with a failing arm.
3. The CRF servo guard gap is filed as https://github.com/kebag-logic/milan-fpga/issues/539.
PR for this lane: the pin bump to donor e5dcea6e, the docs (acceptance 2) and the gmstep harness, as a partial change (Relates to #387). The milan_datapath.sv half of acceptance 3 waits for #529 to release that file; A214's patch in the packet is its starting point.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5804878668
[A10] ASSIGNMENT: A224 author, correction round 1 of PR #540 for R276-1 (F1-F5 MINOR, https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804105668) and R277-1 (F1-F3 MINOR, https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804873088). On the grid-aligner row: the Decided column quotes decision part (b) verbatim, and the tree column records the observed gap: the aligner has no PHC or step input, and a step reaches it only through the CRF-steered grid (#539). The aligner question goes to the owner for a ruling; this page does not settle it. Ruling 5802264260 item 2 (a step merges into a pending restart) is recorded in the decided column. The gmstep claims are narrowed to what it grades, the counted event is tied to the step, the licence check must see a talker that stops for good, and the render-law arms must be independent of start phase. R276 and R277 re-review.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5805175917
[A224] REVIEW READY

Correction round 1 of PR #540 (Relates to #387), under the [assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5804878668). It answers the eight MINORs of [R276-1](https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804105668) and [R277-1](https://github.com/kebag-logic/milan-fpga/pull/540#issuecomment-5804873088).

Commit: `021b2e07b009158bcb0ce19529126eb1d330bba5`, tree `a7ffb35beea95d5bba593029f382e8c0ab0b1c27`. It is local on branch `387-gm-step-rebase` and **not pushed**; this lane may not push. It descends linearly from the reviewed head `44bf0891` through two one-line commits with no trailers: `fdd613a1` (harness and Makefile) and `021b2e07` (docs). The hot files `milan_datapath.sv`, `sim_nxn.cpp` and `CHANGELOG.md` are untouched.

Changed: `tb/verilator/milan_dp/sim_gmstep.cpp`, `tb/verilator/milan_dp/Makefile` (comments, and an optional `GMSTEP_FEED_DELAY`), `tb/verilator/milan_dp/README.md`, `docs/design/GM_LOSS_RECOVERY.md` and `docs/design/TIME_SYNC.md`. No RTL changed.

## Per-finding disposition (lenses as the reviewers assigned them)

| Finding | Lens | Change | Evidence |
|---|---|---|---|
| R276-1 F1 = R277-1 finding 1: the aligner row's Decided column | Conformance, Docs | `GM_LOSS_RECOVERY.md:119`. The Decided column quotes part (b) verbatim: "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event". This tree: `KL_media_grid_align.sv` has no PHC or step input; under CRF selection a step reaches it only through the CRF-steered grid (#539); the question is with the owner. The packet NCO has its own row, "Not named by the decision" | The row is traceable to 5606198212(b). The question is below |
| R276-1 F2: ruling 5802264260 item 2 missing | Conformance, Docs | New row `GM_LOSS_RECOVERY.md:124`. Decided: the step merges with a pending restart, giving exactly one restart, never a cancellation, and the step's MEDIA_RESET still counted. This tree: "Not yet", because `KL_media_clock_restart.sv:167` flips once per request | Docs gates green |
| R276-1 F3 = R277-1 finding 2: "measures all of this" | Docs (R277-1: Docs, Tests) | `GM_LOSS_RECOVERY.md:135-151` lists the graded rows (tu, render re-base, render law, `mr` and MEDIA_RESET, streams) and the ungraded ones with where each is covered or left open: the aligner (TDM clocks held), the CRF servo (#539), the lwSRP licence (escape bit), the pending-restart merge (arm with the datapath edit) and the physical re-base (#117). The verification row (`:179`), the leg's banner and the README say the same | Each graded row maps to named checks in `sim_gmstep.cpp:886-1024` |
| R276-1 F4: the counted event is not tied to the step | Tests | New checks: "render: every counted re-base lands at a PDU end right after the step" (within 500 cycles of the plane's step pulse); "restart: every mr toggle is first sent right after the step" (within two talker intervals); "restart: MEDIA_RESET does not move between the commit and the step" (a GET_COUNTERS read after the commit, with a check that it lands before the step) | R276-1's own `edit-identity-keyed-rebase` and R277-1's E8 now fail all three new checks |
| R276-1 F5: the licence checks cannot see a talker that stops for good | Tests, Robustness | The pause and rate measures run to the end of the graded window. The tu grading requires more than 100 talker PDUs after `tu` clears | R276-1's `edit-talker-silent-after-event` and R277-1's E9 now fail "licence: the talker never pauses beyond four of its intervals" (440726 cycles), the 1% rate check and "tu: talker PDUs graded after tu clears" |
| R277-1 finding 3: the render arms depend on the start phase | Tests, Robustness, Docs | The law is graded where `KL_render_setpoint` judges its bands: the fill right after every PDU push is TARGET_C = 14. The leg reads it as the peak of `rsp_fill_w` between two accepts. The fill at accept is printed, not graded. The leg takes an optional feed delay, inserted where the reviewer's probe inserted it | With the edited datapath copy, the clean leg passes **42/42 feed delays (0 to 41)**, fill after push 14 at every delay, fill at accept 9 or 10. The stage mutant (snap one off) is caught at delays 0 and 12 by "render: every PDU push leaves the target fill across the event" alone |

The suggestions are also taken:

- The Makefile no longer names an untracked runner.
- The Stream Input answers must carry the MEDIA_UNLOCKED and FRAMES_RX valid bits, and FRAMES_RX must move by the accepts seen. R277-1's H9 now fails.
- Stream Output validity is checked on all three reads.
- The CRF-servo row cites #539.
- `TIME_SYNC.md:95-97` says the microcode clamps the trim and `KL_gptp_txret` refuses egress timestamps outside the bound.

## Validation (Verilator 5.050 through the pinned wrapper, at most 8 jobs)

| Gate | Result |
|---|---|
| `make -C tb/verilator/milan_dp gmstep` at `021b2e07` | 48 checks, **4 failures**, all decided behaviour pending the datapath edit. The render stage counts 2 re-bases, the identity-keyed one outside the step window. There is no `mr` toggle and no MEDIA_RESET |
| Clean leg on the edited copy (tree datapath plus A214's published patch, byte-identical to A214's published copy), feed delays 0 to 41 | 42/42 PASS, 48/48 each |
| Failing-arm runner, 10 controls at feed delays 0 and 12 | 20/20 caught by their named checks, with identical failure sets at both delays. The controls: tu late; holdover not re-armed; tu stops the talker; talker stops for good; Stream Input counters dead; no step re-centre; identity re-centres too; re-base keyed to the identity; snap one off; no restart |
| Both reviewers' probe scripts, unmodified, from `387-review-evidence` at `dbfab84f` | as in the table above. R277-1's H3 (at head) now also fails the window check. `phase_probe.sh` was superseded by the leg's own feed delay, because its anchors patch the old harness text |
| `docs_check`, `check_doc_style`, `check_em_dash --base 759da623`, `check_gptp_docs` (with and without the submodule), `check_cpp_idiom`, `check_py_idiom`, `gen_toc --check`, `measure_test_evidence --check`, `check_feature_status`, `check_submodule_docs`, `git diff --check 759da623 HEAD` | all exit 0 |
| Makefile `print-srcs`, `print-pp-srcs`, `print-dp-vflags` | byte-identical to `44bf0891` |

The `gptp_shadow`, `clkvalid` and `media_grid_align` suites were not run, because no RTL or suite source changed. The same holds for `milan_dp gptp` and the full `run` recipe: their source lists and flags are unchanged. Hosted CI, act and hardware are outside this lane. The runner, the edited copy, every log, the HANDOFF and the proposed PR body (starting "[A224]", with "Relates to #387") are in the A224 author packet, `$HOME/milan-fpga-management/2026-09-23/387-a224/` (`MANIFEST.sha256`).

Acceptance criteria:

- Acceptance 1 and 5: unchanged from A214 and met.
- Acceptance 2: met, with the aligner question open as stated in the page.
- Acceptance 3: **not met**. It waits for the datapath edit after #529, and the leg's 4 failures are that edit.
- Acceptance 4: the #117 bench.

Open risks/questions:

1. **For the owner: does the media grid aligner's phase reference need its own re-centre on a step?** Decision part (b) names it. The tree gives it no PHC or step input, and its reference is captured against the physical frame marker. Under CRF selection, a step reaches it only through the CRF-steered grid, whose servo guard has the #539 gap. The page quotes the decision and records the gap; it does not settle the question. The gmstep leg holds the TDM clocks and cannot grade it.
2. The pending-restart merge (ruling item 2) is recorded as "Not yet". Its failing arm belongs to the datapath edit.
3. Observation: across the event, the listener's EARLY_TIMESTAMP moves by 2 at every phase. The peer's media timestamps step with its first GM B Sync, just before the DUT steps. The leg prints this and does not grade it.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5810378282
[A10] OWNER DECISION (2026-09-24): decision part b, the media grid aligner

The grid aligner gets no re-centre of its own.

Part b's "the media grid aligner's phase reference re-centre[s] in one bounded, counted event" is met for the aligner by keeping the step out of its reference, not by a literal re-centre:
- `KL_media_grid_align.sv` locks to the physical sample grid (the TDM frame marker). It has no PHC or step input, so a PHC step leaves its reference unchanged. A forced re-lock would itself put a phase jump into the TDM and packet grids.
- Under CRF selection the only path from a step to the aligner is the CRF-steered grid. #539 closes it at the servo by discarding the window that contains a step. #545 (servo slew) and #546 (talker step) cover the remaining indirect paths.
- Under INTERNAL selection a step never reaches the audio clocks.

What changes:
- The `docs/design/GM_LOSS_RECOVERY.md` grid-aligner row stops calling this an open question and states the decided behaviour. That happens in #539's PR, which already rewrites that row.
- No aligner RTL is added.
- The four open `gmstep` checks are unaffected; none of them concerns the aligner.

Revisit option B, an explicit counted re-lock, only if #545 or #546 cannot close its path.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5811705085
[A10] ASSIGNMENT [A249]: dev silicon check of the #540 gPTP pin

Dev `3d2f3e31` carries #540's gPTP processor pin `e5dcea6e`, and with it a new `gptp_ucode.hex` and the step policy. That microcode had never run on the bench. The dev image is now flashed: best seed WNS +0.107, flash-pair verified, cold boot to VERSION `0x00020060` with the fabric entity enabled.

Check on silicon, bench rules as for [A237]:
- DUT identity;
- gPTP lock against the reference peer, with the grader and asCapable;
- a steady-state soak of at least 10 minutes, with no spurious step: the plane's step counters and `tu` stay quiet while the grandmaster is stable;
- la_avdecc enumeration classifies the DUT as Milan, as in the #529 check.

No CRF binding: the #530 talker fix is not on dev yet. The exact-image check that includes #530 follows once it merges.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5812223671
[A249] DEV SILICON CHECK: **PASS** on dev `3d2f3e31`, with the #540 gPTP pin `e5dcea6e`

Nothing was bound, flashed, power-cycled or rewired. Times are UTC.

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | DUT identity | **PASS** | Console `ID=4d494c4e`, `VERSION=00020060`. The QSPI bitstream payload reads CRC32 `b07f8550`, the eppo seed of `3d2f3e31`. It is not any `c593cbef` seed. ROM `f6afa4ec`, AEM `93742dd2` |
| 2 | gPTP lock, grader, asCapable | **PASS** | Bare-metal grader **10/10** four times, 09:48 to 10:11. The grandmaster is the bench AVB switch. The DUT's path is [GM]. The reference peer is in the same domain, with path [GM, peer]. `SYNC=1 ASCAPABLE=1 TU=0` and `CLKV_STAT=00010002` in **900/900** console samples. The controller's GET_AVB_INFO read as_capable 1 in **900/900** polls on the DUT and 900/900 on the reference peer. Peer delay 375 to 391 ns |
| 2 | Offset and rate (tap, 907 s) | recorded | 904 samples of DUT PHC minus grandmaster time, from the DUT's Pdelay timestamps against the switch's Sync/Follow_Up on the tap clock. **Median +1.7 ns, stdev 10.0 ns, range -24 to +32 ns. Frequency difference -0.006 ppb.** The previous pin on the previous image read median -1.4 ns and stdev 10.1 ns in this morning's A237 capture |
| 3 | Soak >= 10 min, grandmaster stable, no spurious step or `tu` | **PASS, 0 events** | **900 s** sampled every 1 s, 09:51:59 to 10:06:58. The grandmaster was stable: 907 Announces, one GM, stepsRemoved 0, and 7264 Syncs with 0 sequence gaps. `tu` and the step holdover bit were never set (0/900). **`CLKV_TUCNT` (TIMESTAMP_UNCERTAIN) read 10 throughout, and also from 09:48 to 10:11.** It latches every 1 s interval in which a step raised `tu`, so it cannot miss a step between samples. Stream Output `TIMESTAMP_UNCERTAIN` 0 and `GPTP_GM_CHANGED` 0 in 900/900 reads. gPTP drop counters 0. On the wire, the largest 1 s change of the offset was **47 ns, with none above 1 us**. The step policy only steps above 20 us |
| 4 | la_avdecc enumeration, 3 runs | **PASS 3/3** | The DUT was `IEEE17221\|Milan` in all three runs, before and after the soak and at the end. No compatibility events, 0 complaints, 0 query errors, and 0 AECP retries or timeouts. Same binary, libraries and arguments as #529. Each log is identical to #529's step-2 log apart from the order of the online/offline events. The counters probe was CLEAN, with the same transcript as #529 |
| 5 | Restore | **PASS** | The end census equals the start: ACMP 18/18 unbound, AEM settings 15/15. The start census also equals A237's end census from this morning |

**Step counters.** This image has no CSR that counts the plane's steps. The step pulse drives the PHC, the clock-validity holdover (which raises `tu`) and the render re-centre, whose tally is visible in simulation only. So a step was looked for in three places: `CLKV_TUCNT`, `CLKV_STAT` at 1 s, and the wire offset. All three were quiet.

**Not covered.**
- No grandmaster change or link-up was provoked, so the step branch of the policy did not run on silicon here.
- There was no CRF binding, because the #530 talker fix is not on dev.

**The exact-image check that includes #530 follows after #530 merges.**

The handoff, raw captures, logs, commands and tool hashes are in the A249 bench packet.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5812254272
[A10] The [A249] evidence is archived at 42cf9885b277c2a7149d11731d86ed87f689213e (`review-evidence/387-r1/silicon-a249/`). The token scan and the capture field census are clean. Dev `3d2f3e31` with #540's gPTP pin `e5dcea6e` passes the steady-state silicon check. The step branch of the policy was not exercised on the bench: no grandmaster change was provoked. The exact-image check including #530 follows after it merges.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5814963103
[A10] ASSIGNMENT [A256]: #387 acceptance 3, the datapath half

Base: dev `59b81670` (#530 merged, so `milan_datapath.sv` is free).

Starting point: [A214]'s proposed patch from the #540 round, archived with the #387 evidence. It adds three things:
- a PHC step is one counted media event;
- `mr` toggles on it whatever the clock source, and Table 5.4 MEDIA_RESET counts that toggle;
- the render stage re-centres once, and a grandmaster identity change is no longer a separate trigger.

Also required, per ruling 5802264260 item 2: a step while an `mr` restart is pending merges with it. There is exactly one restart and never a cancellation, and the step's MEDIA_RESET is still counted. Today `KL_media_clock_restart` flips its target once per request, so a second request cancels the first.

Acceptance:
- The `gmstep` leg passes 48/48. The four decided-behaviour checks now pass.
- The leg joins the default `run` sweep together with its negative-control runner, as its README requires.
- Mutants must each fail a named check: the step not toggling `mr`, a double re-base, and a cancelled pending restart.
- The `GM_LOSS_RECOVERY.md` "Not yet" rows become "Yes" with evidence. `TIME_SYNC.md`, `REGISTER_MAP.md` and the CHANGELOG are updated where needed.
- The #387 part b aligner decision (comment 5810378282) is unchanged.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816509317
[A10] DECISION (manager), #545 acceptance 1: the CRF servo does NOT follow a gPTP policy slew; it discards the windows the slew overlaps

The owner's step policy slews a locked offset of up to 100 µs at the 200 ppm clamp. Only the local PHC moves: the talker's CRF timestamps are in grandmaster time, and they do not change. A servo that follows the slew would steer the local media clock up to 200 ppm off, twice Milan v1.2 Annex B.1.1's ±100 ppm.

Decided coupling:
- While the plane is slewing, the servo treats each rate window that overlaps the slew as untrusted. It discards and counts it, as it does the #539 step window, and holds its integrator.
- It stays LOCKED, and the audio clock runs on the held integrator. A slew lasts at most 0.5 s: 100 µs at 200 ppm.
- When the slew ends, windows are trusted again, with no ACQUIRE.
- The implementation takes the slew-active indication from the gPTP plane, which knows it is slewing. It must not infer the slew from the measurement.

Implementation: #545. #546 (the talker's own step) is decided by its own acceptance: discard the CRF rate sample that spans a talker discontinuity.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816940740
[A256] REVIEW READY

#387 acceptance 3, the datapath half, under the [assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5814963103), with [ruling 5802264260](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260) item 2.

Commit: `00d388d832189a93335935de7726b5e07dd6f0dc` (tree `6e279c35017d72528d1ea527aa83bee4efbee25a`) on branch `387-media-rebase` from dev `59b81670`. Local only: this lane may not push or open the PR. Four one-line commits, no trailers: `29036eb4` restart engine and its tkdiag arm, `f7948582` datapath, `f0e00c22` sweep wiring, `00d388d8` docs.

**Changed.**
- `milan_datapath.sv`: `media_rebase_p_w` (the plane's step, CLKV adjtime with the plane off, a software settime) joins `mcr_restart_p_w` ungated by the clock source, so every step is one `mr` toggle and one MEDIA_RESET. The render stage re-centres on the step and a settled source change only; the grandmaster identity is no longer a trigger. This is the #540-round patch, plus comments.
- `KL_media_clock_restart.sv`: a request sets each stream's target to the complement of the level it stamps (`tgt_r <= ~mr_o`). A request landing on a pending one merges: exactly one toggle, never a cancellation. The target is per stream.
- `tb/verilator/tkdiag`: T17 (7 checks) and `mcr_mutants.py` in its default target. `tb/verilator/milan_dp`: `run` now runs the gmstep leg and `gmstep_mutants.py` (the acceptance's three controls); `make gmstep-mutants` runs all nine. `sim_nxn.cpp`'s q2 injection flips every context's target.
- Docs: `GM_LOSS_RECOVERY.md` "Not yet" rows are now "Yes" with evidence; `TIME_SYNC.md` render row; `REGISTER_MAP.md`; `TESTING.md`; the suite README; `CHANGELOG.md`.

**Validation** (Verilator 5.050, eight jobs):

| Gate | Result |
|---|---|
| gmstep on dev `59b81670` | 44/48 (2 re-bases, 0 `mr` toggles, 0 MEDIA_RESET) |
| gmstep at the head, feed delays 0 to 41 | **48/48 at all 42**; one re-base at step pulse +132 cycles; one `mr` toggle at +75 to +116 |
| `make -C tb/verilator/milan_dp` from `make clean` | all 47 recipe commands exit 0; 9775 checks, 0 failures |
| `make -C tb/verilator/tkdiag` | 90/90; mutants 3/3 |
| tkdiag against the dev restart engine | fails exactly T17's two merge checks (0 toggles, 0 MEDIA_RESET) |
| `make gmstep-mutants` | 10/10 (clean + 9) |
| Yosys `--top milan_datapath` full; `--top KL_crf_tx` | PASS, 1,632,236 cells, tied-input and tap purity PASS; PASS |
| `docs_check.py` (with git, and on a `git archive` extract with `check_feature_status.py`), `check_em_dash --base 59b81670`, `check_doc_style`, `gen_toc --check`, `check_doc_paths`, `check_gptp_docs` (+ `--with-submodule`), `xvlog_gate --check` (4 == ratchet, 0 `hdl/`), `check_rtl_source_lists`, `check_cpp_idiom`, `check_py_idiom`, `lint_rtl --check`, `measure_test_evidence --check`, `git diff --check` | all exit 0 |

The sweep and tkdiag ran at `1dc93828`. It differs from the head only in two table cells of `GM_LOSS_RECOVERY.md`. The static and docs gates and Yosys ran at the head. The `run` recipe is longer than this session's command limit, so its `make -n run` listing ran command by command in order, each exit code recorded.

Negative controls, each failing its named check:

| Control | Named check |
|---|---|
| step without `mr` toggle | restart: the outgoing mr toggles exactly once |
| double re-base (identity as well as step) | render: the GM change is one counted re-base event |
| no step re-centre (ruling item 1) | render: the GM change is one counted re-base event |
| cancelled pending restart (the dev engine's rule) | T17 talker 1 puts exactly ONE toggle on the wire, never none |
| one shared target merging while any stream is pending | T17 talker 0 had stamped the disruption: the step is its 2nd toggle |

**Existing check changed (Tests lens).** In `sim_main.cpp`, "CLKV: ownerless frame keeps tv=1" compared the whole header byte to `0x81`, which also asserted `mr = 0`. The leg's earlier CLKV adjtime is a step under the decision, and the byte now reads `0x89`. The check now grades every bit but `mr`. A new check grades `mr` against the parity of the PHC steps the harness commanded. Counts: obj_dir and obj_nolpf 230 -> 231, obj_ax1x1 227 -> 228.

Acceptance criteria:
- 3: **met digitally**: gmstep 48/48 in the default sweep with its negative controls; ruling item 1's control fails the one-counted-event check; ruling item 2's merge in the engine, graded by T17 and two mutants.
- 1, 2, 5: as before; the rows this lane owned are "Yes".
- 4: the #117 bench step after merge.

Open risks and questions:
1. **The target is now per stream.** A shared target cannot merge where a restart is pending and restart where it is already stamped; the CRF output's 8-PDU hold outlasts an AAF talker's. So streams can end on opposite `mr` levels. The old "never on opposite levels" note is removed. "Pending" is read as requested and not yet stamped; a request after the stamp is a new restart, sent after the hold. Please confirm this reading of item 2.
2. **Sweep time.** This change adds about 182 s to the 1367 s measured here: the leg 36 s, the three controls 147 s. At the documented 1.58x hosted slowdown, about 595 s of the 2700 s budget remains, down from 885 s. The deadline is not raised.
3. **Lane conflict with PR #547 (#539).** It rewrites the aligner and CRF-servo rows next to the rows turned here, and the adjacent README bullet. It is a textual conflict only; those rows are untouched here.
4. `KL_i2s_playback` (Arty) still re-centres on the identity, since the decision names the render stage and the aligner only. No datapath leg drives a CRF disruption and a step inside one hold; T17 grades the merge on the engine.

The HANDOFF (change list with file:line, test, mutant and gate tables), the proposed PR body (`[A256]`, `Closes #387`) and every log are in the A256 author packet, `$HOME/milan-fpga-management/2026-09-23/387-a256/`.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816975318
[A10] ASSIGNMENT [A268]: merge round for [A256]'s acceptance-3 branch (head `00d388d8`). #547 (#539) has merged into dev `57456af9`, and the branch now conflicts in `docs/design/GM_LOSS_RECOVERY.md` on adjacent rows. Make one merge commit of dev `57456af9`, keeping both sides:
- #539's CRF servo and grid-aligner rows (with the aligner decision);
- this branch's `tu`, render-stage, `mr`, MEDIA_RESET and pending-restart rows.

Re-check the other files both sides touched. There are no other changes.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5817241898
[A268] REVIEW READY

Commit: `e68c1b1ac08c8b1e12a28e281b266d06f881e402` on `387-media-rebase` (local only).

One merge commit, parents `00d388d832189a93335935de7726b5e07dd6f0dc` and `57456af96b3127b9d309a995bbbd35a6113ce52d`, under the [merge-round assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816975318). One-line subject, no body or trailers.

Resolved `docs/design/GM_LOSS_RECOVERY.md`: kept #539's CRF-servo and grid-aligner rows, including the #387 aligner decision, and the branch's Yes rows for `tu`, render re-centre, `mr`, MEDIA_RESET and pending-restart merge, with their evidence. Each selected row is unchanged from its owning parent.

Clean-merged overlaps checked for coherence: `docs/design/TIME_SYNC.md`, `docs/reference/REGISTER_MAP.md`, `docs/testing/TESTING.md`, and `tb/verilator/milan_dp/README.md`. Both sides are retained. `CHANGELOG.md` was also checked: only the branch changed it since the common ancestor, and its entry remains intact. No additional edits were needed.

Validation at this exact merge head, all final exit codes 0:

| Gate | Result |
|---|---|
| `python3 scripts/docs_check.py`, Git and no-Git CI modes; no-Git `check_feature_status.py` | PASS |
| `check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d`, `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `docs/traceability/gen_module_matrix.py --check` | PASS |
| `xvlog_gate.py --check`, `check_rtl_source_lists.py` | PASS; live parsing has 4 findings equal to the existing ratchet, 0 in repository RTL |
| `cd tests && behave --no-capture -f plain` | 344 scenarios, 1739 steps; 0 failures or skips |
| `git diff --check`, also the committed diff against the specified dev base | PASS |
| `make -C tb/verilator/milan_dp gmstep` | 48/48 |
| `make -C tb/verilator/tkdiag` | 90/90; mutation runner 3/3, including both named pending-restart mutants |
| `make -C tb/verilator/mmcm_servo` | Unit 78/78, rails 8/8, PHC-step 113/113 |

The em-dash and contents checks initially refused missing pinned Markdown dependencies. Installing the locked requirements in an isolated environment and rerunning those two checks resolved that setup issue; the commit stayed unchanged. Original and retry logs are retained.

All three required submodules were initialized after the merge and match their pins. The worktree is clean. The merge-round contract is met; this is author evidence for independent review. No push, PR operation, merge to dev or hardware operation was performed.

`HANDOFF.md` contains the resolution with file:line, overlap census and full gate table. It and all evidence are in the A268 author packet, `$HOME/milan-fpga-management/2026-09-23/387-a268/`.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5817362105
[A10] ASSIGNMENT [A269]: PR #555 round 1b. The manager's SDK builder run fails gate 1b at `e68c1b1a`. `sw/builder/test_builder.py` (`assert_boot_contract`, around :8861) still pins the #386 `render_recentre_p_w` initializer and message: GM change, adjtime, settime and the settled clock source. This PR decides a different initializer: the one-event `media_rebase_p_w` plus the settled clock-source change. Update the pin, the message and every related mutation or doc entry to the decided expression. Acceptance 4 still applies: no mutation entry lost, and a mutant restoring the GM-change term fails. There is no RTL change.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5817737327
[A269] REVIEW READY

Commit: `a9636e0f670f90f411da3024a141e93efa1872df` on `387-media-rebase`, local only. One-line subject, no body or trailers; worktree clean.

Under the [round 1b assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5817362105), changed only `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md`. No RTL changed.

The render pin, message and retained ADP mutant now use `media_rebase_p_w | src_recentre_p_r`. The shared re-base initializer, both readers, restart initializer and direct engine connection are pinned exactly. The PHC strobe counts remain 5 and 3; new re-base/restart counts are exactly 3 and 2. The gate print and firmware constraint rows match.

| Validation | Result |
|---|---|
| Full builder, bank wrapper with pinned SDK and `--require-rv32` | rc 0; 224/224 mutations rejected; 53/53 RTL variants elaborated; 115 RV32 census compiles; 239 audited SDK invocations |
| `python3 sw/builder/test_builder.py`, all three cross candidates masked absent | rc 0; 189/189 applicable mutations rejected; 53/53 RTL variants elaborated |
| `docs_check.py`, both CI modes; no-Git `check_feature_status.py` | rc 0 |
| `check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d`, `check_doc_style.py`, `check_baremetal_only.py --check`, `check_py_idiom.py` | rc 0 |
| `git diff --check`, plus committed diff against that base | rc 0 |

No reduction: all 195 existing literal mutation entries remain, with seven added (202); every generated collection and conditional addition is unchanged. Restoring `gm_recentre_p_r` fails the new render pin. Adding another reader of `phc_load_ts_w` fails its exact reference census. Both controls fail by their named reasons and elaborate in both runs.

The SDK suite's only NOT RUN arm is gate 11's missing hardware-report calibration. The absent-compiler run additionally reports the expected gate 1b compiler-instrument stand-down. No coverage is claimed for those arms.

Round 1b acceptance met; no new open question. `HANDOFF.md` records every pin/row before and after, each mutation, commands, receipts and source hashes in `$HOME/milan-fpga-management/2026-09-23/387-a269/`. The SDK wrapper copy changes only its receipt destination; its compiler mapping and arguments are unchanged. The no-Git gate used a source archive of this exact head.

No push, PR edit, merge or hardware action performed. This is author evidence for independent review.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5818091077
[A10] DECISION + ASSIGNMENT [A270]: PR #555 round 2

**Ruling (manager), R276-4 F2 = R277-3 F3: "pending" ends on the wire, not at adoption.** Ruling 5802264260 item 2 exists so that listeners see exactly one restart. Until a PDU carrying the adopted `mr` level has launched, no listener has seen that toggle. A step that lands between adoption and that first PDU therefore merges into it: one toggle and one MEDIA_RESET. The previous rationale ("listeners have already seen the earlier toggle") was false in that gap. This is reading (b) of both reviews.

Required (base `a9636e0f`, which already fixes R276-4 F1 = R277-3 F1):
1. `KL_media_clock_restart`: a stream stays pending until a PDU at the adopted level has launched.
   - Add a tkdiag arm that places a request in the adoption-to-launch gap and grades one toggle and one count.
   - Update T17's expectation to match the ruling.
   - The reviewers' D3/D4 and `probe_pending_boundary` probes give the ruled count, and P1-P4 stay clean.
   - The banner, the `GM_LOSS_RECOVERY.md` row and the PR text state the wire boundary.
2. R277-3 F2: add a check that fails when a software settime does not toggle `mr` once and count once, plus the planted control (`settime_no_mr`).
3. R276-4 F3 = R277-3 F4: the `KL_render_setpoint` banner and port spec name the #387 trigger set: the PHC step and the settled clock-source change.
4. R276-4 F4: the sweep-margin statement rests on what was actually measured.
5. Suggestions from both reviews, if cheap.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819357818
[A270] REVIEW READY
Commit: a21cd3585abdd3cdf4ac5774a048361a66fed043 (branch `387-media-rebase`, local, not pushed; five one-line commits on `a9636e0f`)

Changed (assignment 5818091077, items 1-5):
1. **Wire boundary.** `KL_media_clock_restart.sv:236-238`: a streaming talker that has adopted a level no reported PDU has carried yet (`hold_r == 0`) keeps it as its target on a request, so the request merges. The merge line at `:230` is unchanged.
   - The banner (`:55-92`), the `GM_LOSS_RECOVERY.md` pending row and the PR text state the wire boundary. They also state where the engine measures it: the transmitted-PDU feed, the one the hold and MEDIA_RESET count.
   - tkdiag: T17 now expects one toggle and one MEDIA_RESET on talker 0 as well, because the step lands after its adoption and before any PDU at that level. The new T18 grades a step after the first PDU at the adopted level: a second toggle, counted twice.
   - `mcr_mutants.py` plants four engine defects, adding a window that ends at the adoption and one that stays open for the whole hold. T12 and T15 send one talker-1 PDU so their per-stream-hold checks still grade a hold.
2. **settime** (R277-3 F2). `sim_main.cpp:1028-1072` grades the leg's software settime as one more `mr` toggle and one MEDIA_RESET, in `obj_dir`, `obj_nolpf` and `obj_ax1x1` (233/233/230). `settime_no_mr` and the CRF-gated step are controls on a new option-off leg of `gmstep_mutants.py`, in the explicit `gmstep-mutants` campaign.
3. **Render stage.** `KL_render_setpoint.sv` banner and `recentre_p_i` spec name the PHC step and the settled clock-source change. Comment only.
4. **Margin.** The exact-head hosted shard 4/5 at `a9636e0f` (job 107720800104, candidate merge `1e3a115`) measured the `milan_dp` window at 2264.9 s, which leaves 435 s (16%) of 2700 s. Dev `57456af9` measured 2133.3 s. `CI_WORKFLOWS.md` records these next to the unchanged budget, and the PR text states the margin from them.
5. **Suggestions.** The PR status, the INTERNAL-source citation, the measurement next to the budget, and both runners now rebuild a stale clean binary.

Validation (all rc 0, never piped; Verilator 5.050, eight jobs):
- **`milan_dp` default `run`.** It ran as its 47 recipe commands from `make clean`, in six chunks, with every exit code recorded: 9781 checks, 0 failures. It ran at `c14f96ed`; the head differs by one README line.
- **gmstep.** gmstep passes 48/48. `make gmstep-mutants` gives 13/13: both positive legs and all eleven controls caught.
- **tkdiag.** 96/96, and mcr_mutants 5/5.
- **Full builder.** With the pinned SDK: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 report), 224/224 mutations. Without a compiler: EXCEPT 2 NOT RUN, 189/189.
- **Docs.** `docs_check` passes in both CI modes. `check_em_dash --base 57456af9`, `check_doc_style`, `gen_toc --check` and `check_doc_paths` pass.
- **Static.** `gen_module_matrix --check`, `xvlog_gate --check`, `check_rtl_source_lists`, `check_cpp_idiom` and `check_py_idiom` pass. `behave` passes 344 scenarios, and `git diff --check` is clean.
- **Extra.** `measure_test_evidence --check`, `lint_rtl --check` (90 <= 90), `test_firmware_compiler --absent` and the Yosys `milan_datapath` elaborate smoke all pass.

Reviewer probes, re-run unchanged:
- R276 `probe_pending_boundary.sh`: tkdiag 96/96, talker 0 one toggle.
- R276 `probe_step_gated_by_crf.sh`: killed, 233 checks with 2 failures.
- R277 D3/D4: pending=0 and one toggle, where the previous head gave 2.
- R277 base engine: killed, P1 = 21 and P4 = 21.
- R277 `plant.py`: `settime_no_mr`, `adjtime_no_mr` and `step_gated_by_source` are all killed in the option-off leg. `settime_no_mr` survived there before. On the gmstep leg it still survives 48/0, because that leg issues no settime.
- Every previously killed mutant still dies.
- Not run as-is: R276's builder clone script and R277's `cp -a` wrappers need a second git checkout, which this round may not create. Instead, `plant.py` ran unchanged and the same make recipe built the planted file. The builder banks cover F1.

Acceptance criteria: acceptance 3 is met digitally at this head, except for the open question below. Acceptance 4 stays the #117 bench step after merge.

Open risks/questions:
- **Decision requested.** R277-3's property probe P1 is NOT clean. It flags 10 requests over seeds 2, 3, 5 and 6; seeds 1 and 4 are clean, and P2-P4 are clean on all six.
  - A print-only copy places every one 0-3 cycles after the first launch at the adopted level. That is inside the probe's 3-cycle launch-to-report latency.
  - The engine sees a PDU only when the feed reports it. At such a request, its inputs are the same as in D3. So no engine on the existing ports can meet both D3/D4 = 1 and P1 in that model.
  - The same residue exists in hardware: a talker latches `mr` at launch (`KL_aaf_packetizer.sv:616`, `KL_crf_tx.sv:502`) and reports the PDU after sending it.
  - Options: (a) rule the feed report as "launched" and grade P1 there (implemented); or (b) add launch strobes from both talkers as new engine ports, with the probe driving them.
- **Margin.** 435 s hosted. Whether the three gmstep controls stay in the default `run` is a maintainer decision.

Packet: this round's output directory (`HANDOFF.md`, `PR-BODY.md`, `receipts/`, `MANIFEST.sha256`).


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819379503
[A10] DECISIONS on [A270]'s two open points:
1. **Report latency: option (a).** The engine treats the talker's PDU report as "launched". The report arrives 0-3 cycles, a few tens of ns, after the actual launch. A request inside that window merges into the restart already on the wire. The ruling still holds: one restart, never a cancellation, and the step's MEDIA_RESET is still counted. The window is negligible, so adding launch inputs to both talkers is not worth the change. The residual is documented, as [A270] did.
2. **Sweep controls:** the three `gmstep` negative controls stay in the default `run` sweep, as the leg's README requires. The new settime controls stay in the explicit `gmstep-mutants` campaign. The measured hosted margin is 435 s of 2,700 s (16%). If a later change brings it under 10%, the budget or the split is revisited.

https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308
[A10] DECISION under 5819379503 item 2 (R276-5 F1): raise the `milan_dp` deadline to 3,600 s

The trigger has fired. At this exact head, hosted shard 4/5 ran `milan_dp` in 2,459.9 s, leaving 240 s (8.9%) of 2,700 s. The reviewer's samples show that runner noise dominates. Near-identical content ran from 1,296 s to 2,460 s across today's pushes, and this PR adds about six checks over `a9636e0f`.

Moving the three `gmstep` controls out would save about 180 s. That margin is still smaller than the noise, and CI would stop proving each run that the leg can fail. So:
- The `milan_dp` deadline becomes 3,600 s. At the worst observed sample that is a 32% margin, and the deadline still catches a hang.
- The hosted job timeout must allow it; check `timeout-minutes` for the rtl-full shards.
- `CI_WORKFLOWS.md` records the budget with the cited samples: the exact-head window and the day's spread.
- If a later exact-head sample falls under 10% of the new budget, the split into more shards is the next step.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820585975
[A10] ASSIGNMENT [A277]: PR #555 round 3

Round 2 at `a21cd358`: R276-5 and R277-4 are NEGATIVE, on MINOR findings only.

Required:
1. **R276-5 F1 = R277-4 F2:** implement decision 5820240308.
   - The `milan_dp` deadline becomes 3,600 s. Check the hosted rtl-full shard `timeout-minutes` allows it.
   - `CI_WORKFLOWS.md` and the PR record the budget with the cited samples: this head's hosted window of 2,459.9 s, and the day's spread of 1,296-2,460 s.
2. **R277-4 F1:** make `gmstep_mutants.py`'s `is_fresh()` read the recipe's input list correctly whatever the make version and nesting. For example, run `make --no-print-directory -s ... print-srcs`, or filter non-path tokens. A fresh clean binary is then graded, not rebuilt. Fix the `option-off` positive control the same way. The reviewer's `repro_gmstep_freshness.sh` must print `is_fresh: True` inside the parent recipe under GNU make 4.3.
3. **R276-5 F2:** `docs/fpga/FPGA_DESIGN.md:170-175` scopes the verdict to the CRF triggers and states that a PHC step toggles `mr` whatever the selection, as `REGISTER_MAP.md` does. Scope `MILAN_COMPLIANCE_MATRIX.md:120` and the roadmap note the same way.

Taken:
- R276-5 S1 and R277-4 S1: the PR body cites decision 5819379503.
- R276-5 S2: the `KL_render_setpoint` summary line.
- R277-4 S2: a tkdiag arm or comment for the `streaming_i[t]` term.
- R276-5 S3, if cheap: a simulation leg that issues a settime and counts one render re-base.

No other RTL change.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5821088465
[A277] REVIEW READY

Commit: `0f003fab3303858ba4db955ad3c0512e67a8018b` (local head on `387-media-rebase`; not pushed).

Round 3 implements assignment [5820585975](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820585975): the 3600-second deadline and its contract, nested recipe freshness for both positive legs, the three documentation scope corrections, both requested RTL comments, the decided PR-body citations, and the live-CSR settime render check. The hosted shards already allow 120 minutes. No functional RTL changed this round.

Validation: all assigned commands exited 0. The chunked default `milan_dp` sweep ran 44 commands, 9785 checks, 0 failures; `gmstep-mutants` passed 13/13; tkdiag passed 96/96 with all four mutants caught. The reviewer's unchanged GNU make 4.3 repro prints `is_fresh: True` inside the parent recipe. Both positive legs also pass nested assertions, and the old behavior fails them. The settime omission control fails the named render check.

Both documentation CI modes, the requested static gates, and 344 behavior scenarios pass. The full builder without an RV32 compiler rejects 189/189 applicable mutations; compiler-dependent instruments and physical calibration remain explicitly NOT RUN. The deadline contract and its 101-check self-test pass. The em-dash gate used base `57456af96b3127b9d309a995bbbd35a6113ce52d`.

`HANDOFF.md`, the full replacement `PR-BODY.md`, and command/exit receipts are prepared in the assigned output packet. No PR edit or push was made. Independent re-review, publication, hosted/candidate validation, and merge remain pending. Issue #387 acceptance 4 remains the manager's #117 bench step after merge.


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5821889812
[A10] Round 4 assignment for PR #555. R276-6 and R277-5 report the same single F1 MINOR (Docs); every earlier finding is closed.

Scope for [A283]: state the `milan_dp` deadline as 3600 s, per decision 5820240308, wherever the tree still presents 2700 s as current:
- `docs/testing/TESTING.md:166-167`. Give the reason as decision 5820240308 and the samples recorded in `CI_WORKFLOWS.md`, not the #444 measurement alone.
- `docs/testing/RUNNING_TESTS.md:79`.
- `tb/verilator/milan_dp_gptp/README.md:31`.
- the `tb/verilator/milan_dp/render_mutants.py:37` docstring.

Leave these as they are: the history lines in `CI_WORKFLOWS.md`:167 and :185 (they describe the past budget) and the self-test mutation string in `measure_test_evidence_selftest.py`. Change nothing else.

Gates: `python3 scripts/docs_check.py` (both CI modes), `check_em_dash --base 57456af96b3127b9d309a995bbbd35a6113ce52d`, `check_doc_style`, `gen_toc --check`, `check_doc_paths`, `check_py_idiom`, `python3 -m py_compile tb/verilator/milan_dp/render_mutants.py`, `git diff --check`.

Review: delta reviews at the new head by [R276] and [R277].


https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5821996548
[A283] REVIEW READY

Commit: `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` (local, unpushed; parent `0f003fab3303858ba4db955ad3c0512e67a8018b`).

Changed: only `docs/testing/TESTING.md`, `docs/testing/RUNNING_TESTS.md`, `tb/verilator/milan_dp_gptp/README.md`, and the `tb/verilator/milan_dp/render_mutants.py` docstring. All four current deadline statements say 3600 s under [decision 5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308); the testing guide retains the recorded-samples link.

Scope proof: `git diff --stat 0f003fab3303858ba4db955ad3c0512e67a8018b 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` reports four files, +7/-5. Exact replacements were checked against the parent. The executable syntax tree is unchanged outside the module docstring. The workflow history and self-test file are byte-identical. `git grep -n -w 2700 -- docs scripts tb` leaves only the two historical lines and the planted mutation.

Validation: all commands below returned 0 at this head, in the foreground without pipelines:

```sh
python3 scripts/docs_check.py
# Repeated from an archive of this head without Git metadata.
python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py
python3 -m py_compile tb/verilator/milan_dp/render_mutants.py
git diff --check
git diff --check 0f003fab3303858ba4db955ad3c0512e67a8018b 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b
```

Both documentation modes reported zero findings over 165 Markdown files and 859 text files. The no-metadata mode reported its expected inventory-parity skip. The em-dash gate reported zero findings and 339/339 controls.

Acceptance: the [Round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5821889812) is implemented; F1 from both reviews is ready for independent delta review. Acceptance 4 remains open under #117.

Handoff: `HANDOFF.md`, the full updated `PR-BODY.md`, the complete delta, scope proof, and gate receipts are prepared in the assigned output packet. The PR body preserves `Relates to #387` and the acceptance-4 note. No push or PR edit was made.

Open risks/questions: no new implementation question. Independent delta reviews, publication, and candidate validation remain pending.

