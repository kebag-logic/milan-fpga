[R678] NEGATIVE - exact head 2ff30f0dc5e89be46f8103272883885e8553f4b8

Round R678-2, external independent review of PR #770 for issues #632 and #764. Tree: `2a2cc5362850cee5a857d7d277d8e8ec3aaeae7a`. All five lenses were applied. One MAJOR finding remains, attributable to all five lenses. Two RESIDUE items do not independently affect the verdict.

The circular detector, snapshot-edge hold and blend fixes address their causes. The new shared offset path introduces a CRF overflow regression: it discards the carry needed by a 64-bit CRF timestamp. The existing offset test passes that defect. Listener presentation at the pin is outside this PR under the manager's ruling and is not counted as a finding.

## Scope and review method

Read AGENTS.md / CONTRIBUTING.md and docs/README.md, then the issue bodies and public decisions, linked requirements and interface authorities, the source-base diff/history, the twelve-commit delta from `f1fda3f1`, and public executable evidence. The independent verdict and ledger were written before reading the prior public review reports; their findings were then reconciled below. No private author material, other checkout, management directory, or current-round peer report was used.

Authorities:

- [Initial assignment](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284510903), [latency addendum](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284578201), and [one-domain-reference addendum](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284659263).
- [Investigation and measurement method](https://github.com/kebag-logic/milan-fpga/issues/764#issuecomment-6283948176).
- [Round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6300015619) and [superseding listener scope ruling](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306187740), both read exactly.
- REQUIREMENTS.md; docs/design/MEDIA_CLOCK_FOLLOWING.md, especially Phase alignment; docs/design/TIME_SYNC.md, especially Media boundary and Listener render latency; the register map, compliance matrix and testing contracts.
- IEEE 1722-2016 4.3.5, 10.7 Equation (14), 10.8 Equation (15); the assigned Milan v1.2 7.6.1 frequency-and-phase requirement.

This PR retains the domain phase loop, talker capture timestamps/constants, whole-period output offsets and circular aggregation. The listener keeps the #386 fill law at the crossbar grid and the documented post-grid delays. #632 remains open. Hardware acceptance is deferred explicitly, not treated as simulation proof.

The full source range is `e26f1816..2ff30f0d`; this round concentrates on `f1fda3f1..2ff30f0d` and changed dependencies. Unchanged earlier artifacts retain their earlier examination; no later clean result is inferred merely from an earlier verdict. Source validation is distinct from the final current-dev merge candidate.

## R678-2-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs

**Title:** The shared rounder loses the CRF timestamp's overflow carry.

**Artifacts:** hdl/ieee1722/crf/KL_mtt_round.sv:186 and :193; hdl/ieee1722/crf/KL_crf_tx.sv:394; hdl/milan/milan_datapath.sv:6375; tb/verilator/media_phase/sim_ofs.cpp:216 and :222; docs/design/MEDIA_CLOCK_FOLLOWING.md:1682; docs/reference/MILAN_COMPLIANCE_MATRIX.md:224; PR #770's offset limitation.

**Authority/evidence:** Round 2 requires every output to use the existing CRF Equation (14) rule, including boundary offsets. The transmitter's existing explanation at KL_crf_tx.sv:296 explicitly preserves extra bits because rounding a 32-bit maximum transit time can exceed 2^32. CRF carries a 64-bit timestamp.

The shared rounder instead exports only `dv_quot_r[31:0]`. The integration disables the transmitter's own converter, and its applied-value arm zero-extends that truncated value. For an accepted CRF offset of `0xFFFFFFFF`:

- Equation (14): 206,159 periods, rounded to **4,294,979,167 ns**.
- Shared output: **11,871 ns**.
- CRF therefore stamps **2^32 ns earlier** than the required result.
- 2^32 ns is not an integer number of 48 kHz periods. The resulting phase error is approximately **8,962 ns**, versus the allowed **1,041.667 ns**.

The independent probe retains the existing A-D stimulus and adds two checks: subtract the full mathematical offset from each full 64-bit CRF timestamp and require an actual generated frame instant; independently fold each full timestamp against the known physical grid. Case D fails both checks for all four CRF PDUs; A-C pass. The original fifteen checks still pass.

The original grader casts CRF timestamps to 32 bits at line 216, then returns before phase grading whenever the raw CRF offset is at least 2^31. Thus its purported boundary coverage cannot detect this defect. The stimulus supplies the exact frame instants, so a full-width oracle has no ambiguity.

**Receipts:** `receipts/probe-ofs.log` and `probe-ofs-binary.log`; binary exit 1, make exit 2, 23 checks with two failures. `receipts/control-ofs.log` passes 15/15 on the reviewed source. A separate disposable integration control feeds the raw CRF row to the transmitter's existing full-width converter: `receipts/control-full-width.log` passes the same 23 checks, including D. This control changes only probe wiring, not reviewed source.

**Impact:** A supported boundary setting violates the promised whole-period relationship and Equation (15), and no longer applies the requested maximum transit time. The low-word wrap explanation is valid for AAF's transmitted low word; it cannot justify truncating the addend before a 64-bit CRF sum. The design and PR's claims that every output remains coherent at this boundary are therefore substantive, not wording residue.

**Required outcome:** Preserve the complete rounded offset through the CRF timestamp addition while maintaining the shared-rounding and coherent-readback contract. Explicitly reconcile any 32-bit control-field representation at this boundary; do not silently turn a multi-second offset into 11.871 microseconds. Correct the design/PR wrap claim and test oracle. Any restriction of supported settings needs an authorized public contract change.

**Verification:** Grade full CRF timestamps at the largest non-overflowing input, the first overflowing input, and 0xFFFFFFFF, at initialization and runtime, alongside four AAF outputs. Compare against independent full Equation (14) arithmetic and the known reference grid. A dropped-carry mutation must fail its named check. Retain the ordinary offset and readback checks.

## R678-2-R1 | RESIDUE | Docs

**Title:** New source comments contain reviewer identifiers.

**Artifacts:** Twenty-one added source/comment lines, enumerated with exact paths and head line numbers in `receipts/comment-delta-audit.txt`. Production examples: KL_aaf_capture_i2s.sv:141, KL_mtt_round.sv:14, milan_datapath.sv:1245 and :3430. The remaining lines are in media_phase's Makefile, wrappers, mutation driver and C++ graders, plus milan_dp/sim_nxn.cpp:7217.

**Authority/evidence:** The assignment's comment rule prohibits reviewer IDs and review rounds in new source comments. These added lines include `R677-1-F1`, `R678-1-F2` and related identifiers.

**Impact:** Comment wording only; no code, measurement, oracle, generated artifact or clause claim changes. No privacy breach is asserted. This does not make a lens unclean.

**Exact fix:** Remove reviewer identifiers from all twenty-one listed comments, retaining issue IDs and the behavior/reason. Replace the nine leading `#: R...:` prefixes in phase_mutants.py with `#: #632:`. Replace sim_blend.cpp:15's `before #632's R677-1-F1` with `before the #632 frame-assembly correction`. Elsewhere remove the comma plus reviewer token, or the parenthesized reviewer token, retaining `#632`.

**Verification:** Re-run the added-line comment audit over the same delta and confirm no reviewer token remains. Findings and PR prose may continue to name reviewers.

## R678-2-R2 | RESIDUE | Docs

**Title:** Scope prose still describes the listener ruling as undecided.

**Artifacts:** PR #770 Status, Linked Issue / roles, Known limitations and Definition of Done; docs/design/MEDIA_CLOCK_FOLLOWING.md:1724 and :1751; docs/design/TIME_SYNC.md:519; related CHANGELOG.md listener sentence.

**Authority/evidence:** The later ruling removes R678-1-F1 from this PR, retains it under #632, and explicitly asks the PR body and design page to say so and cite the ruling. The body still opens “BLOCKED on one decision”; the design still says compensation was ruled in and awaits a decision. Neither includes the superseding ruling. The actual listener behavior and #386 grid law are accurately described.

**Impact:** Stale scope/status wording only. The controlling public ruling is unambiguous and is applied in this review. This is not a renewed finding against missing listener implementation, and the historical measurement figures need no change.

**Exact fix:** In the affected scope/status sentences, state: “Listener presentation at the pin is outside PR #770 under the [scope ruling](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306187740). It remains open under #632. The listener keeps the #386 law at the crossbar grid and the documented post-grid delays.” Replace the design subsection title with “The listener: outside this PR, retained under #632”. Label the earlier decision/cost discussion as background. Remove the obsolete listener-specific BLOCKED/pending-decision language without claiming this review is positive.

**Verification:** The live PR body and authoritative design page cite the ruling, retain #632 as open, and state the unchanged grid law. Carry as wording residue.

## Prior public findings: disposition at this head

Read [R678-1](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6299647615) and [R677-1](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6299997695) after the independent pass.

| Prior ID | Disposition and cause-level evidence |
|---|---|
| R678-1-F1 | Outside this PR by the superseding ruling, still open under #632. Not counted as a finding here. R2 above records only stale scope prose. TIME_SYNC.md:369 retains the crossbar-grid law. |
| R678-1-F2 | The original raw AAF offset cause is fixed: KL_mtt_round serves the four AAF rows and CRF row; milan_datapath:1447/:5238/:6375 uses applied values for stamping/readback. The 2,010,000 ns case now applies 2,020,834 ns. The broader output-offset acceptance is **not clean**, because the newly shared CRF path introduces F1 above. |
| R678-1-F3 | Resolved. KL_mmcm_drp_servo:789-814 tracks/unfolds samples, re-folds the window, and requires both the mean and every sample in band for four full windows. The first sample seeds a reference; holds invalidate it. Samples beyond the accumulation cap still affect the all-in-band predicate. Detector balanced, 129:127, 160:96, jitter, meanin, inband and cross cases pass independently. Published edge/edge2 with 8 ns truncation and +/-48 ns jitter acquire in 26.44/26.64 s, held maxima 618.9/598.7 ns, no false settled window. |
| R678-1-F4 | Resolved. KL_mmcm_drp_servo:1023 tests the current hold on T0 as well as prior validity. Independently ran all eighteen sim_det.cpp:354 snapshot checks: six hold causes before/on/after T0 commit zero/zero/full correction. Later-event behavior remains the documented separate policy. |
| R678-1-R1 | Resolved. Live PR role lines identify internal R677 and external R678. |
| R677-1-F1 | Resolved. close_slot()/close_is_i2s() at KL_media_if_latency_pkg:105/:111 select the blend's I2S closing pair and its latency; root and capture crossbar use it consistently. KL_aaf_capture_i2s:153 aliases the FIFO's registered result, removing the one-frame-late pop; the flat I2S counterpart is changed consistently. The independent blend run passes 24/24 across six reset phases, grading actual sample identities against their pin instants, unfolded. I2S error is -29 to -11 ns, TDM +11 to +29 ns. Published controls kill both old-close and late-pop defects. |
| R677-1-F2 | Resolved. sim_main.cpp:541 supplies the isolated +7 us PHC step; the published exact-head run drops the term and settled flag, reacquires in 22.27 s and holds within 562.7 ns. step_hold_removed is killed by the required let-go check. |
| R677-1-F3 | Resolved. sim_det.cpp:158/:262 grade the fourth full window, hold/reset of settled, status mirror, and +/-2^25 acceptance boundary. Independent controls pass. Published settled_is_engaged and fold_range_guard_removed are killed at their named checks. |
| R677-1-F4 | Resolved. The fresh default-target receipt measures 578 s including five builds, consistent with Makefile, CI_WORKFLOWS.md:432 and run_all_suites.sh. The 900 s limit remains explicitly provisional until hosted measurement. The separate campaign receipt is 751 s at four jobs. |
| R677-1-F5 | Resolved. The three assigned stale divider statements in the root and two builder files are corrected as requested. |
| R677-1-F6 | Optional SUGGESTION, explicitly not assigned. The root still has the separately literal data-delay coupling; no correctness failure was found and it does not affect coverage. |

## Applied-lens evidence and completion ledger

All table entries refer to the exact head below. “UNCLEAN” reflects F1, not the excluded listener item or the residues.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Public assignment/ruling; MEDIA_CLOCK_FOLLOWING.md:1533-1838; KL_mmcm_drp_servo:789-814; KL_mtt_round:24-32/:186; KL_crf_tx:394; full-width offset oracle. Single-master and ordinary phase/offset behavior checked against 4.3.5, Eq. 14/15; F1 violates the boundary contract. | R678-2 | 2ff30f0dc5e89be46f8103272883885e8553f4b8 |
| RTL | UNCLEAN | Servo reference/sum widths, cap, signed extension, reset/hold and T0 pipeline; KL_media_if_latency_pkg:105, KL_chan_map_capture:643/:661 and I2S FIFO output; root offset and readback wiring; source lists and synthesis deltas. New arithmetic stays in the datapath clock domain; existing FIFO crossings retained. F1 loses a significant carry. | R678-2 | 2ff30f0dc5e89be46f8103272883885e8553f4b8 |
| Robustness | UNCLEAN | sim_det.cpp fold/range/eighteen hold-edge cases; sim_main.cpp edge/edge2/phcstep; sim_blend.cpp six reset phases; sim_ofs.cpp A-D and full-width probe. Reset, stale history, disabled phase, wrap boundaries and sample-cap behavior examined. F1 fails a supported maximum setting. | R678-2 | 2ff30f0dc5e89be46f8103272883885e8553f4b8 |
| Tests | UNCLEAN | All delta graders and phase_mutants.py rejection predicate; capture_coherence changed anchors; milan_dp/sim_nxn.cpp:7217 readback check; exact-head source receipts. Original offset grader passes while independent full-width grader fails, F1. | R678-2 | 2ff30f0dc5e89be46f8103272883885e8553f4b8 |
| Docs | UNCLEAN | MEDIA_CLOCK_FOLLOWING phase contract, TIME_SYNC, REGISTER_MAP:2152, compliance row, CHANGELOG, testing/budget tables, source-comment delta, PR body and receipt provenance. Settled and hold descriptions now match their checks. F1's all-output overflow claim remains wrong; R1/R2 are residue only. | R678-2 | 2ff30f0dc5e89be46f8103272883885e8553f4b8 |

No top-level port or register-layout change was found in this delta. The reserved read-only settled bit has the tightened meaning documented. AAF-input following remains rate-only. The output rounder's non-idempotence for non-multiple-of-three period counts follows the assigned two-ceiling Equation (14) rule and is documented; it is not filed as an additional finding.

## Evidence and reproducibility

The [published source packet](https://github.com/kebag-logic/milan-fpga/tree/6576850939843f0356182fb63f8ba50008027d88/review-evidence/632-r1) is the evidence source. Its author receipt subtree was verified against MANIFEST.json: **538/538 published SHA-256 values match**, including the round-2 receipts. This verifies the published/redacted bytes, not unavailable original logs.

Signature limit: neither the evidence commit nor the reviewed source commit contains an embedded commit signature; verification returned 1 for both. No detached signature was supplied in the named packet. Thus content identity is verified, but a “signed packet” authentication claim is **not verified**. See published-hash-verification.json.

| Evidence | Result and provenance |
|---|---|
| Independent detector, blend and offsets | 46 detector checks, 24 blend checks, 15 original offset checks; zero failures. Built from exact-head disposable copies. |
| Independent full-width probe | 23 checks, two expected failures in case D; binary exit 1 / make exit 2. A-C are positive controls. Existing full-width-converter integration control passes 23/23. |
| Author exact-head full sweep | Four HEAD receipts name 2ff30f0d; 64/64 suites, 2,187,770 checks, no in-suite failure or timeout. Shards: 53,842; 331,603; 262,057; 1,540,268 checks. capture_coherence now passes inside the sweep, including its 35-check campaign. |
| Author phase campaign | f1643214: eighteen clean controls and 28/28 named rejections, 46/0 total. Reviewed the source predicate: compilation failure is never a kill; rc=1, RESULT: FAIL and the required failure substring must all occur. The printed first failure can differ from the required one. mutant-receipt-audit.json maps every mutant to its required check. No executable campaign input changed afterward. |
| Author root spot-check | milan_dp's published extraction records SET/GET_STREAM_INFO on AAF and CRF rows: 2,010,000 set, 2,020,834 read, emitted timestamps checked. Does not cover F1's full-width maximum. |
| Author lint/docs | Exact-head lint reports 89 <= 89; exact-head docs summary records 49 successful commands. These mechanical passes do not clear the semantic findings. |
| Author open synthesis | 60/60 tops at dd256343, plus six affected tops and structural gates at f1643214. Checked the intervening production-file diff: changes affect the servo, rounder, CRF TX and root, all included in the six-top rerun. |
| Author builder | f1643214, exit 0 with one arm NOT RUN: gate 11 needs the separate retired-board build report. This is not calibration or hardware proof. No builder input changes afterward. |
| Author route-1x1 | f1643214, matching processor pins and unchanged build inputs afterward. Gate exit 0: LUT 49,709 (+96 / allowance +500), FF 52,760 (+407 / +600), slices 15,797 (+72 / +80), RAMB36/RAMB18 74/25 (+0), DSP 13 (-1), WNS +0.305 ns, WHS +0.036 ns, complete route. Receipt recommends re-recording the improved DSP endpoint. This is source evidence, not merge-candidate evidence. |
| Exact checkout integrity | 1,436 parent tracked blobs and the full index match HEAD bytes/modes; required submodule gitlinks, initialized-superproject identity, tracked bytes/modes and indexes match. Counts: processor 588, timing processor 107, stream library 214, firmware stack 98. No tracked file was changed. |

The complete f1643214-to-head delta changes only a resource-headroom paragraph and a campaign timing comment. That supports carrying executable/route evidence forward; it does not turn ancestor documentation evidence into an exact-head docs run. The published docs run separately names the exact head.

Portable commands, from this packet directory:

```sh
python3 run_focused.py /absolute/path/to/review-clone /absolute/path/to/scoped-compiler
python3 verify_evidence.py /absolute/path/to/review-clone
python3 verify_state.py /absolute/path/to/review-clone
```

run_focused.py uses concurrent focused builds with bounded compiler jobs, waits for every subprocess, and keeps all disposable source/build material under scratch/. Its successful driver exit means the expected clean controls **and expected failing witness** occurred. It is not a clean-design verdict. The named compiler's 5.050 identity was checked before use. Published receipts are exactly those listed in MANIFEST.sha256, plus this report; scratch/ is excluded.

## Real limits and pending manager duties

- No manager source bank exists at this head, and none is claimed. Source gates above are author receipts; independent executions are limited to the focused controls/probe.
- The long closed-loop cases are accepted from verified public receipts and reviewed graders. They scale clocks while retaining the 512 ms control window. Pin/blend evidence is compositional; it is not a long physical multi-interface run.
- No full parent/processor/timing-processor, builder, synthesis or route bank was run by this reviewer. No hosted job completion, skipped context, local workflow replica or merge acceptance was inferred. Hosted/act acceptance remains the manager's duty.
- Physical calibration **NOT RUN**. Field skips and the builder's missing calibration arm are not hardware proof. The #764 ten-minute method and re-engagements remain post-merge hardware work.
- The final candidate must be built and validated against live dev, identified by the assignment as `59740e3c9d0420e2e7fef185978954710448dc4a`, refreshed at the merge turn. A conflict-free test merge does not establish composition correctness. Builder/native candidate receipts, required hosted contexts, resource endpoint recording and post-merge containment remain pending.
- Fix F1 and obtain corrected-head review coverage, finish all review rounds, and satisfy the required independent-review bar before any authorized merge. The excluded listener work remains under #632; the AAF phase follow-on remains separate.
- No GitHub writes, source fixes, commits, pushes, merges, hardware actions or author contact were performed.

R678-2 FINISHED
