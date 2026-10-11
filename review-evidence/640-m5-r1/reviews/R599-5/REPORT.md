[R599] POSITIVE - exact head 2bef9e50489a60f216a8073a9f5ea0645752b33f

R599-5, external independent delta review of issue #640 / PR #722.
Tree: `9777e890c07850052a0d9134cdb22388a651c5f1`.
Source base and observed live dev: `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`.
[Public review start](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6112090063).

All five lenses are CLEAN. R599-4-F1 is RESOLVED: the complete current PR body contains no 38,436/396 figure, and Status, Known limitations and Composition repair consistently state 38,784 LUTs, 744 over 38,040. No BLOCKER, MAJOR or MINOR remains open. Four inherited wording residues and two optional suggestions remain below. This verdict covers the source delta and public-body correction; it does not authorize merge or close umbrella issue #640.

I reconstructed AGENTS.md, CONTRIBUTING.md and docs/README.md, the issue's frozen scope and public decisions, requirements/interfaces, then the complete base-to-head diff and history, followed by public executable evidence. The independent verdict and five-lens ledger were written to `raw/independent-pass.md` before prior review reports were read. No private author material, management checkout, other reviewer's local report, source edit, GitHub write, or delegated work was used.

**The corrected figure and unchanged review object.**

The governing [M5 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098404907) preserves the register ABI, snapshots and bus contract, and requires honest measurement against the estimate. The [D1/D3/D7/D8 rulings](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268) distinguish this intermediate lane from final target closure and re-recording.

The calculation is:

`37,957 + (200 - 34) + (600 - 121) + (600 - 418) = 38,784`

`38,784 - 38,040 = 744`

Plan `docs/design/MARK_II_AREA_PLAN.md:699` defines M2's reproducible 34; `:960` defines M6's 418 post-synthesis; `:1048` is the 37,957 planning row; `:1106` substitutes those two figures and M5's 121 routed in its CSR scope. The cumulative tables explicitly retain planning estimates pending the week-4 re-measure. The combined consequence is arithmetic using the stated individual-lane bases, not a measurement of a combined routed image.

[R599-4](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6108273466) records precisely the same full head and tree as this checkout and the live PR. Its unchanged-tree receipts remain applicable: `receipts/delta.log` for composition and plan arithmetic; the six successful documentation-gate receipts; and `receipts/test-evidence.*` for the merged reader registry. Its earlier dependency refusals are not counted as passes. This round does not relabel its deliberately failing PR-body check as a pass; `raw/verify-final.log` supplies the new passing body check.

Both current PR snapshots have identical body bytes. The entire body was inspected, including historical round-two sections, and scanned for the obsolete pair. A negative control reintroduced the old figure and was rejected. Head/tree equality is independently checked against R599-4's public record; complete pre-correction body-byte identity is not claimed, because that earlier body snapshot was not supplied locally.

**Independent application of the five lenses.**

- Conformance: REQ-CSR-01 through REQ-CSR-05 and the register-map access rules were checked against the read-path diff. The port and parameter contract remains unchanged. The estimate shortfall is disclosed without claiming NFR-RES-01 closure.
- RTL: `milan_csr.sv:2300`, `:2487`, `:2636` and `:2655` preserve the default-zero decode and read-window precedence. The shadow word is zeroed whenever the live path claims the read, so the stage-two OR does not combine two active words. Pipeline enables, slow-read completion and reset behavior retain their prior ordering. The SNAP changes at `:2930` and `:3034` update each raw word and its kind together. No new clock crossing or interface is introduced.
- Robustness: the zero/raw/poison transitions, out-of-range snapshots, talker-to-listener updates, extra-context burst, reset during reads, unmapped and unaligned addresses, and response stalls were examined in the RTL and harness. `sim_lock.cpp` exercises those cases; bounded waits turn missing completion into failure. Random traffic includes noncompliant traffic as an equivalence stressor, so it is not treated as an exhaustive protocol proof.
- Tests: the frozen reference was compared to the original committed bytes after only module-name normalization. Both shipping shapes retain 302 identical ports. The generated comparison covers all outputs; snapshot expectations also come from the harness. The seven mutation definitions require the named failing check and reject build failures or crashes as catches. The random phase requires completed reads. The read-window removal's separate integration control remains necessary because that deletion is unobservable in today's lockstep map.
- Docs: the module page describes the two registered words and OR stage; the CSR README describes the reference and mutation limits. The plan separates standalone, proxy and in-datapath figures. The live PR now agrees with the combined figure throughout. Historical author receipts remain tied to their stated revisions.

**Prior public findings, explicitly reconciled.**

The original findings were read after the independent pass from [R598-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105288411), [R599-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105370578), [R598-2](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105610437), [R599-2](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105856251), [R598-3](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6108060229), R599-4, and [R598-4](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6112084379). Submitted-review and inline-comment lists were empty.

| ID; original severity and lenses | Disposition at this head and current body |
|---|---|
| R599-4-F1; MINOR; Docs | RESOLVED. Known limitations now substitutes all three measured lanes. The required complete-body check against plan :699, :960, :1048 and :1106 passes. The previous 348-LUT understatement is absent. |
| R598-4-RES-2; RESIDUE; Docs | RESOLVED by the same correction. Its original classification is recorded separately from R599-4-F1; neither finding remains open. |
| R599-1-F1; MINOR; Conformance, Docs | RESOLVED. Plan :1102-1103 labels #649's 211 in-datapath slope separately from standalone/proxy slopes 12/62 and 49/56. The original evidence and `649_RESOURCE_MAP_AND_SENSITIVITY.md:623,647,657` support those distinct bases. No unsupported non-reproduction claim remains. |
| R598-1-F1 = R599-1-F2; MINOR; Docs | RESOLVED in current public attribution. PR Description gives disjoint CSR -121, wrapper -342, and remainder -227, summing to -690; nested `u_pp` -344 is explicitly not added. The public round-two correction supersedes the immutable round-one attribution prose. No unpublished revised author document was inspected or certified. |
| R599-1-RES-1; RESIDUE; Docs | RESOLVED. `milan_csr.sv:1066` describes the OR stage, matching :2660. |
| R599-1-RES-2; RESIDUE; Docs | RESOLVED. Plan :539 says M5 saved 121 routed and 127 post-synthesis. |
| R599-1-RES-3; RESIDUE; Docs | RESOLVED. PR test row says apart from the module name; the byte comparison confirms that qualification. |
| R598-1-S1; SUGGESTION; Docs, later required by the manager | RESOLVED and superseded by the combined consequence at plan :1106. |
| R598-2-S1; SUGGESTION; Conformance, Docs | Superseded by R598-3-F1, now RESOLVED through the combined arithmetic. |
| R598-3-F1; MINOR; Conformance, Docs | RESOLVED in both lenses. Plan :1106 includes M2, M5 and M6 and recomputes exactly. The unchanged-tree documentation receipts remain applicable. Its remaining wording request is recorded separately as R598-4-RES-3. |
| R598-2-RES-1, R598-2-RES-2; RESIDUE; Docs | RETAINED, exact fixes below. |
| R598-4-RES-1; RESIDUE; Docs | RETAINED, exact fix below. |
| R598-4-RES-3; RESIDUE; Conformance, Docs | RETAINED in both original lenses, exact fix below. |
| R599-1-S1; SUGGESTION; RTL, Docs | RETAINED, optional; no alternate implementation run occurred. |
| R598-3-S1; SUGGESTION; Docs | RETAINED, optional; no documentation edit occurred. |

**Retained R598-2-RES-1: RESIDUE; all attributable lenses: Docs.** Artifact: PR Round 2, first attribution bullet. Evidence: `syn/ooc/pp_resource_gate.py:255` lists scopes within the wrapper; CSR is a sibling and -227 is the remainder. Impact: readers look in the wrong receipt; the numbers and result remain correct. Exact fix: replace the source-attribution sentence with: "The wrapper and `u_pp` figures are the route gate's sub-block figures for the M5 route; `csr` -121 is the routed hierarchy report's `milan_datapath/csr` scope, and about -227 is the remainder." Verification: re-read against those hierarchy scopes.

**Retained R598-2-RES-2: RESIDUE; all attributable lenses: Docs.** Artifact: PR Description, Saving against the plan. Evidence: -344 nested within -342 implies +2 elsewhere in the wrapper. Impact: the phrase nearly all is imprecise; no figure changes. Exact fix: "the processor wrapper -342, which nests `u_pp` (-344; the rest of the wrapper moved +2; not added)". Verification: re-read and retain the disjoint total -690.

**Retained R598-4-RES-1: RESIDUE; all attributable lenses: Docs.** Artifact: PR How to get into the same state, expected-output comment after `git rev-parse HEAD`. Evidence: the comment still names the historical round-two head while Status and the live PR name this head. Impact: stale reproduction annotation; it changes no executable command or measurement. Exact fix: `git rev-parse HEAD   # 2bef9e50489a60f216a8073a9f5ea0645752b33f`. Verification: re-read the annotation against live PR metadata.

**Retained R598-4-RES-3: RESIDUE; all attributable lenses: Conformance, Docs.** Artifact: plan :1106. Evidence: measurement bases are already defined at :454, :539 and :557 but are not repeated beside the three parenthetical values. Impact: readers must follow those definitions; arithmetic, scope and result remain unchanged. Exact fix: "With the measured savings of M2 (34, post-synthesis), M5 (121, routed in its scope) and M6 (418, post-synthesis) in place of their central figures, the partial-central scenario becomes about 38,784, 744 over 38,040, pending the week-4 re-measure (D8)." Verification: recalculate the same 38,784/744 result and run the affected documentation gates. This adds labels to established bases; it does not create a new measurement or conformance claim.

**Retained R599-1-S1: SUGGESTION; all attributable lenses: RTL, Docs.** Artifact: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:142` and public route evidence. Evidence: the recorded WNS fall is 0.202 ns, within the 0.25 tolerance and above the 0.03 floor. Impact: less margin for later lanes. Optional outcome: run the recipe's alternate placement directives to characterize sensitivity. Verification: compare full timing receipts and flow identities. No such run is claimed here.

**Retained R598-3-S1: SUGGESTION; all attributable lenses: Docs.** Artifact: `docs/design/AREA_BUDGET.md:197,208`. Evidence: M2 and M6 have measurement links there, whereas M5's required measurement is in the plan. Impact: navigation only; no existing claim is false. Optional outcome: add an M5 link naming 121 routed/127 post-synthesis and no block-RAM growth. Verification: check the linked ledger and documentation gates.

**Executed checks and public evidence.**

| Check | Result and receipt |
|---|---|
| Raw source bytes, filesystem modes, stage-zero index, head and tree | PASS; `raw/verify-initial.log` and `raw/verify-final.log`, both rc 0. Parent: 1,284 blobs and five gitlinks. |
| Three required submodules | PASS; same logs verify protocol processor 562 blobs, gPTP processor 104, and axis 214 at their committed gitlinks. |
| Frozen oracle and interfaces | PASS; original SHA-256 `c3106a1410035f33eef9e634750ffc534be4d04293263bdbfd4ea144dfd523d8`; 302 ports at each shape. Planted reference-byte drift is rejected. |
| Resource arithmetic and complete-body consistency | PASS; final log lists all four plan anchors. Planted obsolete figure is rejected. |
| Prior head/tree and stable current public body | PASS; `raw/reconciliation.log`, rc 0. |
| Published author packet integrity | PASS; published HANDOFF digest `f45a1b972e7ec7bf37d75836af18937ff3ecbbb21025c6f27874b1711cfbd474` matches its public manifest. Historical scope limitations remain. |
| Diff whitespace and final tracked status | PASS; included in final verification. No source mutation or restoration was necessary. |
| Hosted snapshot | `raw/hosted-jobs-final.json` and `raw/public-final.log`, observed 2026-10-11 18:15 UTC; details below. |

The [public author packet](https://github.com/kebag-logic/milan-fpga/tree/648503cfeee36d03d7baf2a7b8608e1310caae49/review-evidence/640-m5-r1) and [round-two receipts](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105430562) report both lockstep shapes, seven named mutant catches, broader source checks and individual-lane route measurements. Those runs retain their published source revisions; none is relabelled as a new run by this reviewer at this head.

The hosted API ties four completed successful workflows to this exact head. All seven required contexts report success, with nonzero step lists. Five simulation shards and four synthesis shards also report completed success with executed steps. The physical job reports SKIPPED and has zero steps. These are observed job metadata, not a new local execution or an independent audit of every hosted log. Hosted acceptance and the local workflow replica remain manager duties.

**Reviewer-owned completion ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue assignment 6098404907; D1/D3/D7/D8; REQUIREMENTS.md:128; docs/reference/REGISTER_MAP.md:155; docs/design/MARK_II_AREA_PLAN.md:699,960,1048,1106. ABI, snapshot and accurately scoped area obligations checked. | R599-5 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| RTL | CLEAN | hdl/common/csr/milan_csr.sv:2300,2487,2591,2636,2655,2930,3034; raw/source.diff; verify-final.log. Read precedence, exclusive word selection, unchanged pipeline and same-cycle SNAP kind/data checked. | R599-5 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| Robustness | CLEAN | tb/verilator/csr/sim_lock.cpp:429,477,522,598,644; lock_mutants.py:47; milan_csr.sv:2935. Reset, invalid address/index, stale/poison transitions, burst and stall coverage checked against preserved behavior. | R599-5 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| Tests | CLEAN | tb/verilator/csr/gen_lockstep.py:89; sim_lock.cpp:703; lock_mutants.py:113; Makefile; frozen reference; scripts/measure_test_evidence_readers.py. Oracle identity, interface population, named mutation grading and nonzero random reads checked; unchanged-tree receipts retained. | R599-5 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| Docs | CLEAN | hdl/common/csr/doc/milan_csr.md:159; tb/verilator/csr/README.md:84; plan:1102,1106; raw/pr-final.json, reconciliation.log, verify-final.log. Contracts and entire current body agree; F1 resolved. | R599-5 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |

**Real limits and pending manager duties.**

This round performed no simulation, implementation, full parent/processor/gPTP/synthesis/builder bank, workflow replica, hardware operation or merge. The source tree is identical to R599-4's reviewed tree. The manager has no source bank at this exact head; none is claimed or inferred. Source validation and the final current-dev merge candidate are distinct. At the merge turn, the manager must construct and validate that candidate, run the builder/native banks, and link its receipts on the PR. Any movement from the observed live dev must be accounted for then.

Physical calibration: NOT RUN. Field skips and the skipped physical hosted job are not hardware proof. The selected-split route retains its prerequisite STOP; the author's 8x8 integrated synthesis was not completed. Individual route receipts and estimated arithmetic do not establish a combined route or physical release qualification.

Before merge, carry the four retained residues to the residue checklist, complete the independent review bar with no round in flight, accept required hosted/local evidence, publish current-dev candidate receipts, and obtain maintainer merge authorization. Afterward perform containment and the plan's boot readback. D8's measured planning update, M9 target closure/re-recording, selected-placement qualification and physical release obligations remain outstanding. M5 must not close #640.

Portable commands are in `scripts/REPRODUCE.txt`. Only REPORT.md and files named in MANIFEST.sha256 are publishable. Scratch downloads and disposable material are excluded.

R599-5 FINISHED
