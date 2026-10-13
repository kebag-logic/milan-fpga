Prior public findings at `313616d1a18549d41907db389d378f0beb9bc543`

This is part of R559-10's verdict. The independent pass and five-lens ledger
were written before prior reports were opened. Original public findings were
then read on PR #706. The formal-review and inline-comment endpoints contained
no additional findings. Original severities and all assigned lenses are retained.

Resolved findings:

| IDs; severity; lenses | Authority, impact and required outcome | Verification at this head |
|---|---|---|
| R558-9-F1; MINOR; Docs | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6113540239): M2/M6 confused their historical comparison with the current gate record. Name both accurately. | **Resolved.** `MARK_II_AREA_PLAN.md:696-697,952` contains the requested wording. `record-vs-lane-routes.log` and `lane-records.log` confirm historical equality, current inequality and both route verdicts against both records. |
| R558-9-R1; RESIDUE; Docs | Same authority: lane-scoped no-re-record wording needed explicit subjects. | **Resolved.** Plan `:707,973` says M2/M6 do not re-record under D7. |
| R558-11-F1; MINOR; Docs | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6118370609): M5 introduced the same misleading record identity. | **Resolved.** Plan `:1099-1100` dates #645/#647's record and names #696's replacement. `plan-composition.log` and `lane-records.log` confirm M5 passes both. |
| R558-11-R1; RESIDUE; Docs | Same authority: M5 needed lane-scoped no-re-record wording. | **Resolved.** Plan `:1115` says `M5 does not re-record the gate under D7.` |
| R558-5-F1; MINOR; Docs | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097253076): M0s named the old record as current. | **Still resolved.** `AREA_BUDGET.md:381` and plan `:656-657` name the dated comparison and 50,013-LUT replacement. |
| R558-6-F1; MINOR; Conformance, RTL, Robustness, Tests | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097490649): raw low seed bits produced colliding first blocks. First draws must use the stepped full seed under the subsequently ruled criterion. | **Still resolved.** `KL_maap.sv:154-184,202,337-339` is unchanged from `32582421`. Unit and datapath p7 plants fail their named first-block checks in this round's full campaign. |
| R558-7-F1; MINOR; Tests | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6102796423): overlap-start echo escaped the test. Grade a PROBE starting below the local range. | **Still resolved.** `sim_main.cpp:433-440`, `mutants.py:125-127`: clean below-offset echo assertion passes; `m2_echo_overlap_start` is detected by name. |
| R559-6-F1; MINOR; Tests, Conformance | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6102829355): test names and an impossible all-high-half-pairs criterion disagreed. Record a feasible criterion and name checks precisely. | **Still resolved.** [Ruling 6102832618](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618), `MAAP_FABRIC.md:110-120`, `sim_main.cpp:1126-1138`: power-of-two pairs, word bijection and fixed pairs are distinct. All corresponding clean checks pass. |
| R559-6-F2; MINOR; Tests, Docs | Same authority: universal fold claims lacked sensitive executable evidence. Test the actual RTL maps and altered constants. | **Still resolved.** `sim_main.cpp:1180-1276` learns both maps, exercises 65,536 words, eight block sizes and 528 carry runs. Row-0, row-6, unstepped, nonlinear and dependent-row plants are all detected by name. Sampled-linearity limits remain explicit. |
| R558-3-F1 = R559-3-F1; BLOCKER; Conformance, Robustness, Tests | [Internal](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095037677), [external](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095122585): inherited make output polluted the derived sources/flags and stopped integration compilation. | **Still resolved.** `integration.mk:8-24` clears inherited flags for both captures and passes the compilation bound. Bytes match `32582421`; all six integration campaign builds complete. This round uses make 4.4.1; acceptance of the hosted environment remains separately attributed. |
| R558-1-F1; MINOR; Docs | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093137183): pre-merge area was attributed to a merged head. Date each measurement correctly. | **Still resolved.** `MAAP_FABRIC.md:161-173` distinguishes 441/340, 445/340 and 490/340. The new published 446/340 measurement is separately tied to `313616d1`, not substituted into historical statements. |
| R559-1-F1; MINOR; Tests | [Original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093167069): short outages could not distinguish restart on loss from restart on return. | **Still resolved.** `sim_main.cpp:836-872` outlasts a complete walk; `m5_restart_on_link_loss` fails its named assertion in this round. |
| R559-1-F2; MINOR; Docs | Same authority: current inventory differed from the new resource record. | **Still resolved.** Plan `:110-147`: 66/66 figures agree with the three endpoints; `plan-composition.log`. |
| R559-1-F3; MINOR; Docs, Tests | Same authority: zero-seed fixture named the superseded MAC. | **Still resolved.** Harness and `MAAP_FABRIC.md:251` name `02:00:00:00:00:00` at clock zero; clean zero-seed checks pass and both associated plants are detected. |
| R559-1-R1/R2/R3; RESIDUE; Docs | Same authority: dated area, remaining deviations and the findings-index record description needed correction. | **Still resolved.** `MAAP_FABRIC.md:154-201` and `docs/findings/README.md` retain the corrected scope and attribution. R1 overlaps R558-1-F1 above. |
| R558-7-R1, R559-6-R1; RESIDUE; Docs | Original round-7/internal and round-6/external comments above: interval-pair scope and word-versus-block wording. | **Still resolved.** `MAAP_FABRIC.md:117,260` distinguishes pool-folded blocks, fixed pairs and universal criteria. The public PR limitations retain the distinction. |
| R558-4-R1/R558-6-R1/R558-10-R1; RESIDUE; Docs | Earlier public PR bodies named a stale source head. | **Resolved.** Current Status and checkout command name full `313616d1`; the new merge and prior review head are dated separately. Publication wording is now R559-10-R1 in REPORT.md. |
| R559-7-R1; RESIDUE; Docs | Earlier body said checks needed a pushed head after publication. | **Superseded by current wording.** The old sentence is gone. The remaining unpublished/pending-publication wording is retained as R559-10-R1. |
| R558-1-S1; SUGGESTION; Docs | Old binding timing-margin sentence. | **Applied.** Plan `:56` gives +0.233 ns record, +0.030 floor and 0.203 margin. |
| R559-1-S2; SUGGESTION; Tests, Docs | Integration executable needed the ROM-containing working directory. | **Applied.** Public reproduction changes into the integration build directory; the campaign does likewise. |
| R558-7-S1 = R559-6-S1; SUGGESTION; Tests | Unstepped probe-fold plant escaped. | **Applied.** Every-carry-run probe assertion detects `m4_probe_fold_unstepped` in this round. |
| Empty-list half of R558-3-S1 = R559-3-S1; SUGGESTION; Robustness, Tests | Empty derivation needed explicit rejection. | **Applied.** `integration.mk:16-18` rejects it. Directory half remains below. |

Retained prose residue (Docs; no lens effect under the supplied rule):

| IDs; severity | Artifact, evidence and impact | Exact repair; verification |
|---|---|---|
| R558-2-R1 = R559-2-R1; RESIDUE | `MARK_II_AREA_PLAN.md:66-67,317,1129`; [original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093606049). Dated historical sections still link the live record using loose wording. Historical figures and current-record sections already distinguish the two. | Replace the source sentence with: `Source: the three record objects of pp_resource_baseline.json as stored at dev 5603c353; #696's record has since replaced them (see Current processor inventory).` Preserve existing Markdown links. Replace the ledger sentence with `The [current ledger](#ledger) starts from the 50,267 route figure of the #645/#647 record.` Replace `Adopted processor pin and current three-endpoint record` with `Adopted processor pin and the #645/#647 three-endpoint record`. Check dated scope and docs gates; change no figure. |
| R558-5-R1; RESIDUE | `AREA_BUDGET.md:372,389`, plan `:669`; [original](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097253076). M0s-scoped unchanged-record wording could sound page-wide. | Replace each applicable sentence with `M0s changes no acceptance record, schema or policy value.` Verify paragraph scope and docs gates without changing records or policy. |

Retained optional suggestions. These are ungraded correct details or possible
improvements, not identified incorrect implementation at this head. Their
original probes are not claimed as newly executed unless named above.

| IDs; severity; all lenses | Artifact, evidence and impact | Optional outcome; verification |
|---|---|---|
| R559-1-S1; SUGGESTION; Tests | `sim_main.cpp:977-984`, `mutants.py`: a trap in the explicit linearity sample cannot establish arbitrary nonlinear sensitivity. | Add another out-of-sample trap if desired and require a named rejection; retain structural review. |
| R559-1-S3; SUGGESTION; RTL, Docs | `KL_maap.sv:142-184,337-339`: shipping 50 MHz timing does not qualify a possible 100 MHz configuration. | Qualify any supported faster configuration or explicitly retain the measured clock scope; inspect dated timing evidence. |
| R559-1-S4; SUGGESTION; Tests | `mutants.py:main`: category completeness guards #686 but not every M1-M8 category. | Add a category guard; deleting the last plant for an item must fail it. |
| Directory half of R558-3-S1/R559-3-S1; R558-4-S1/R559-4-S1; SUGGESTION; Robustness, Tests | `integration.mk:19-21`: wildcard existence admits directories. Compilation still fails and cannot count as a detected plant. | Reject directories at derivation; exercise its named refusal. |
| R558-3-S2 = R559-4-S2; SUGGESTION; Tests | `mutants.py`: no dedicated fixture forces the historical inherited-directory-output/unavailable-jobserver setup. | Add that fixture and assert clean captures. |
| R558-4-S2; SUGGESTION; Docs | `integration.mk:8-10`: the comment could name the unavailable-jobserver trigger more exactly. | Name the trigger and compare with its reproduction. |
| R559-5-S1; SUGGESTION; Tests, Docs | Plan/budget record identity lacks a repository semantic prose-to-record gate. The repeated composition repairs show drift risk. | Add a gate with a planted historical/current-record confusion; require rejection. |
| R558-6-S1; SUGGESTION; Tests | `KL_maap.sv:272,282,480`: own-count snapshot substitution was ungraded; reconfiguration during a frame is outside the documented protection. | Add a focused snapshot check if desired and detect the live-count substitution. |
| R558-6-S2; SUGGESTION; Docs | Fabric, firmware and processor MAAP contracts differ on loss, while fabric return behavior follows its ruling. | Document the placement distinction; compare `MAAP_FABRIC.md:122-130` with firmware and processor loss handling. |
| R558-7-S2 = R559-6-S3; SUGGESTION; Tests | `KL_maap.sv:337-339`, `MAAP_FABRIC.md:110`: later Begin! draw selection remains an ungraded correct detail. | Grade Release!/Begin! draws at a controlled clock and reject repeated-first-fold selection. |
| R559-6-S2; SUGGESTION; Robustness, Tests | `KL_maap.sv:193-198,337-339`: random pool clipping above eight addresses lacks targeted coverage; predates this lane. | Exercise larger blocks specifically inside the clip region and detect fixed-eight clipping. |
| R558-8-S1; SUGGESTION; Docs | `docs/testing/TESTING.md`, MAAP suite row still omits its real-datapath campaign. | Add: `Since #696 its default target also builds the real milan_datapath CSR-to-MAAP path (sim_integration.cpp) and plants its M3, M4 and M5 datapath defects there.` Verify against default make. |
| R559-7-S1; SUGGESTION; Tests, Robustness | `KL_maap.sv:464-466,332,203`: fresh return range, zero-count seed-bound rejection and announce bit selection are individually ungraded correct details. | Add specific assertions and require each corresponding plant to fail. |

No finding is resolved by moving it to another issue. No BLOCKER, MAJOR or
MINOR remains open. Residues remain on the manager's checklist; suggestions
remain optional.
