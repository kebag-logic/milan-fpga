[R958] NEGATIVE - exact head 3181a3ec372b6473175cc1c842ada8133a96b127

All five lenses were applied to `25ff0632c4ed312d57cad78783474308c92dd21f..3181a3ec372b6473175cc1c842ada8133a96b127`, tree `da2f2b0635071acfcfe49efb6c9e2cb0450e85da`. One new MINOR test defect remains. Acceptance at the proposed 0.78 ceiling also awaits the owner's answer. The corrected load is **0.7786365** using the median baseline: **this PR does not pass at 0.77 without the ceiling increase**. It also fails 0.77 using the dearest-before baseline, 0.7741365.

The previous accounting omission is corrected, the platform refusal thresholds are corrected, D8-D10 address the requested fault cases, and the EOF whitespace failure is corrected. Published hash receipts establish 80/80 identical product ELF entries across the measured images, the previous reviewed head and this exact head. This verifies published receipts, not an independent rebuild of the binaries.

**Scope and reconstruction.** Read AGENTS.md / CONTRIBUTING.md, docs/README, the issue's acceptance and public decisions, REQUIREMENTS.md ownership and NFR-SCOUT-03, FR_NFR section 3.4.1, relevant mailbox/SRP interfaces and SPLIT_CONTROL_MEMORY section 13. Examined the full source-base diff inventory/history against `dev-soft-core` (`0b5940237e8de8bd5912db87e5e036a78f59b5a6`) and independently inspected the eight-commit, 21-file re-review delta. Unchanged implementation keeps its previous assessment unless a changed dependency affects it. The narrow delta adds no RTL, CDC, mailbox ABI, linker placement or submodule changes.

An independent pass and preliminary lens ledger were recorded before opening the [prior internal findings](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7226275798) and [prior external findings](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7226304210). No other current-round review was consulted. Public scope is preserved in `public-scope.json`; the assignment is [the review-start comment](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7229469285).

**R958-3-F1 - MINOR - Tests, Robustness - `tb/verilator/ctrl_service_budget/flip_grade.py:197,421,454`: a renamed failed ceiling control disappears in the harness adapter.**

Authority/evidence: AGENTS.md Tests requires tests to fail for their claimed defect. `controls()` now returns `the flip ceilings not 0.70 at 8x8/2if and 0.78 at 8x8/1if`; `CONTROLS` still lists the version ending in `0.77`. `flip_checks()` tests membership only against that list. Its caller is `load_grade.ceiling_checks()`, used by the harness self-test. This string is executable test routing, not wording residue.

The disposable in-memory probe changes only `FLIP['8x8/2if']` from 0.70 to 0.71, leaving the proposed 1if ceiling at 0.78. `controls()` returns the failed fixed-ceiling control; **all 628 `flip_checks()` results nevertheless pass**. Injecting that single failure directly also produces no failed adapter check. Baseline controls return no escapes. See `probe_model.py` and `model-probe.json`.

Impact: a prohibited ceiling configuration is silently reported clean by the harness adapter. Standalone `flip_grade.py --selftest` still examines returned escapes directly and detects it, limiting the defect's reach. No current product load or firmware behavior changes because of this finding.

Required outcome: the adapter must report this failed control, with names synchronized or unknown returned failures rejected. Keep the intended 0.780-pass / 0.781-fail boundary behavior.

Verification: run the focused ceiling mutation through both `controls()` and `flip_checks()`; both must fail the fixed-ceiling check. The unmutated head and existing boundary controls must remain green. This MINOR leaves Tests and Robustness UNCLEAN until corrected and re-reviewed.

**R958-3-F2 - MAJOR - Conformance - `flip_grade.py:69`, `docs/reference/FR_NFR.md:427`, commit `9976b94f`: the 0.78 acceptance decision remains pending.**

Authority/evidence: the [owner's 0.77 decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7213594113) is reiterated in the [80 ms TRANSMIT approval](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7217388999). The latter changes TRANSMIT only. Rulings 7210763364 item 6 and 7212897415 item 5 require escalation when the load fails. The reviewed commit and live PR body explicitly say the 0.78 decision is pending. A final read of both public discussions found no later owner answer.

The independent model probe reproduces 0.7786365000000001 with the median-based deliveries term. The 0.78 check passes; the 0.77 check returns `8x8/1if: the load 0.779 at the pin is over the flip ceiling 0.77`. At the dearest-before cost the load is 0.7741365, also over 0.77. This is the remaining acceptance part of R957-2-F1, not a new omission in the accounting.

Impact: the proposed bound is reviewable, but its passing result does not establish satisfaction of the currently published owner bound. I judged everything else against 0.78 as requested; there is no inferred authorization to raise it.

Required outcome: publish the owner's answer. If approved, cite it in the ceiling's authority and current requirement text. If refused, revert the ceiling increase and retain the failed 8x8/1if status pending authorized margin work. Do not drop the deliveries term to obtain a pass.

Verification: reconcile the published decision, `FLIP`, FR_NFR and the same load calculation at the resulting head. No product rebuild is needed solely for an authority citation. Conformance remains UNCLEAN pending that acceptance decision. The accounting implementation itself is accepted under all four lenses originally attached to R957-2-F1; its unresolved part is now the owner-bound decision.

**R958-3-R1 - RESIDUE - Docs - PR #993 Status, first paragraph: duplicated role words.**

Evidence: current link labels read `internal internal review ` and `external external review `. Impact: wording only. Exact fix: `internal review` and `external review`, removing trailing spaces inside the labels. Verification: inspect the live body. No lens is unclean for this residue.

**R958-3-R2 - RESIDUE - Docs - public `author-r11/REVIEW-READY.md:15` and `author-r10/receipts/INDEX.md`: claimed historical supersession note is absent from the published packet.**

Evidence: REVIEW-READY says a dated supersession note was appended to the earlier index. The index at evidence commit `be39b0e1` has no such note. Current PR prose does correct the run counts, default-option image explanation, review assignments and 80 ms approval. The earlier index and new receipts index also retain `.txt.gz` names for logs published as `.txt`; `MANIFEST.json` correctly identifies the actual files and hashes.

Impact: historical/current prose navigation only; measurements, binary identities, verdicts and executable evidence are unchanged. This retains the publication portion of R958-2-R3 and R957-2-R3.

Exact fix: append a dated note to the earlier published index stating that the current PR / author-r11 supersedes the earlier pending-80-ms wording, reviewer placeholders, all-zero run-count wording and default-option explanation. Preserve historical receipt bytes. Add a publication note mapping compressed log names to their actual `.txt` paths, with the published manifest as hash authority. Until published, replace `is appended` with `remains to be appended` in current handoff prose.

Verification: fetch the updated public index and follow its links. No lens is unclean for this residue.

**Prior findings, resolved or retained at their causes.**

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R957-2-F1, MAJOR, Conformance/RTL/Tests/Docs | Accounting cause CLOSED; owner acceptance retained as F2 | `load_grade.py:8,376,610,685` names, computes and checks `deliveries`; design section 13 describes baseline and source. Independent arithmetic and four negative controls agree. F1 above is a separate adapter regression introduced by the ceiling edit. |
| R957-2-S1, SUGGESTION, Tests | ADDRESSED | `srp_binding.hpp:519,536,557` adds D8 loss-turn starvation, D9 alternation after loss, D10 no turn in a record pass. `srp_deliver_mutants.py:61` supplies four causal mutations. Final shard 3 lines 1681/1685/1689/1965/2037 and focused receipts show intended assertions caught. |
| R957-2-R1 and R958-2-R1, RESIDUE, Docs | CLOSED at named sites | Comments identify the population or delivery ruling, preserve issue/clause references, and remove the three B-number prefixes. Added source comments/docstrings contain no new forbidden review-round or reviewer labels. |
| R957-2-R2, RESIDUE, Docs | CLOSED | `ctrl_loop.h:395`, FR_NFR's SRP row and design section 13 state 79.49 ms, distinguishing the ruling's former 79.48 ms at 415 us SETTLE. |
| R957-2-R3, RESIDUE, Docs | Current counts CLOSED; index publication retained in R2 | PR says 285 zero exits plus four expected standalone pairing refusals and two passing paired reruns per point. It no longer calls all 289 zero exits. |
| R958-2-F1, MINOR, Docs | CLOSED | `SPLIT_CONTROL_MEMORY.md:172` gives platform refusal thresholds 65.5/61.5; `ctrl_memory_ledger.py:90,99` tests them. Entries remain 65.0/61.0, and the exact-head platform ledger receipt accepts the 61.0 image. |
| R958-2-R2, RESIDUE, Docs | CLOSED in current prose | PR Pins row says the zero-option arm is used by default-option shapes; the 80-path image identity proof covers those shapes. Historical packet bytes remain historical. |
| R958-2-R3, RESIDUE, Docs | Current authority/roles CLOSED; historical note retained in R2 | Current design and PR link the 80 ms approval and name assigned reviewers. Remaining pending-owner language concerns the distinct 0.78 decision and is accurate. |
| R958-2-S1, SUGGESTION, Conformance/Tests/Docs | Accounting explanation ADDRESSED | Design section 13 distinguishes source-term load from response rows and records the 300-to-350 us base sensitivity: load unchanged, TRANSMIT 77.89-to-79.49 ms. The new sourced term is additional accounting, not a measured total-utilization claim. |
| EOF builder failure | CLOSED | Independent `git diff --check` against `dev-soft-core` exits 0; the pre-fix `9976b94f` comparison exits 2 on that exact EOF blank line. |

Round-1 closures recorded by round 2 remain standing: this delta does not change the population/charge/LeaveAll logic, alone-admission guards, published dependency pins or public ADP decision that resolved them. No new broad implementation review is claimed.

**Baseline and evidence judgment.** I accept the **median ordinary-pass baseline** for the explicitly amended source-term model. The dearest-before baseline subtracts unusually expensive prior passes and supplies a lower sensitivity estimate, not the accepted substitute. The method subtracts already attributed heavy items, takes the prior 50 ms of ordinary poll sections, and sums nonnegative excess over the record's section plus the next `2 * n_sinks` sections. `deliv11.py` uses the upper middle observation for an even-size sample; I accept that estimator here. At 8x8/1if the maximum is 104,157 cycles / 9 = 11,573 cycles per sink; 5 percent margin and a 5 us grid give 125 us. At 1x1/1if, 36,153 / 2 = 18,076.5 gives 190 us. The source rate is V * 3 / (1.5 * 180 ms), with V=9/4, under the ruled interpretation of IEEE 802.1Q-2018 10.7.11 and Milan Table 4.3.

| Independent receipt check | Result |
|---|---|
| `audit_evidence.py`, public manifest | 263 author/author-r10/author-r11/author-text files match `published_sha256`; no review report needed for this audit. |
| Three ELF identity receipts | Each has two identical maps of exactly 80 paths. All maps agree across `e59cf6ea`, `25ff0632`, `9976b94f` and `3181a3ec`. Routed platform identities remain `2e3b1fe8...` and `f36a050a...`. Measurements and routes stand under the requested identity rule. |
| Delivery arithmetic | 80 median/dearest rows per shape checked for window length, per-sink division and maximum rounded statement: 190/125 us median, 130/80 us dearest. |
| Source terms at the pin | 1x1/1if 0.5320957632, including deliveries 0.0084444444. 8x8/1if 0.7786365, including deliveries 0.0125. |
| Focused checks, `checks.json` | Load check + 32-control self-test, both held-point flip checks, direct 628-control self-test and 25-control shape self-test pass. 8x8 TRANSMIT is 79.49 ms against 80. F1 demonstrates the distinct harness-adapter weakness despite these baseline passes. |
| Final author firmware receipts | Four shards at `9976b94f` end PASS / rc=0. The only later commit removes the EOF blank line. D8-D10 causal failure words appear in final shard 3 and focused receipts. |
| Author builder receipt at `3181a3ec` | Step 43 passes. Step 32's initial skip is superseded by its executed passing rerun. Step 47 explicitly reports one NOT RUN calibration arm. This is an author source-head receipt using the builder recipe, not a manager source bank or final merge-candidate proof. |
| Packet signature | Public commit metadata says `verified=false`, `reason=unsigned`, matching local Git. Hash integrity is verified; a cryptographic packet signature is not established. This is a provenance limit, not a newly invented gate. |

Full CPU trace logs and ELF binaries are not published in this packet; summarized measurement arithmetic, extraction code and hash maps were checked without pretending to replay missing raw data. No physical timing campaign or hardware observation was rerun. Existing routes and measurement envelopes are inherited through identity, not newly measured.

**Independent lens results and reviewer-owned ledger.**

[R958] MAJOR Conformance - `load_grade.py:376,610`, `flip_grade.py:69`, FR_NFR section 3.4.1 and owner decisions - the term and rate are accepted; F2 prevents accepting the proposed ceiling as authorized. Remaining checks were judged at 0.78.

[R958] PASS RTL - `ctrl_app_srp.c:134`, `ctrl_app.h:107`, `ctrl_loop.h:344`, `srp_mbx.c:554,1015`, `srp_mbx.h:161`, hot list and exact gitlinks - production token streams and hot-list entries equal the previous head. Scheduling/reset/index contracts retain their prior assessment. ELF identity preserves resource/route evidence; no new implementation risk was found.

[R958] MINOR Robustness - `flip_grade.py:196,454`, `srp_binding.hpp:519`, `srp_deliver_mutants.py:61` - loss rotation, both alternation directions, record-pass suppression and pending behavior are addressed. F1 leaves failure reporting for prohibited ceiling configurations unclean.

[R958] MINOR Tests - `load_deliveries.py`, `load_grade.py:685`, `flip_grade.py:421,454`, D8-D10, final shard 3 and the focused probe - term omission/rate/cost controls work; delivery tests exercise their claimed faults; F1 remains open.

[R958] PASS Docs - `SPLIT_CONTROL_MEMORY.md:172,2548`, FR_NFR section 3.4.1, SRP README delivery contract, `ctrl_loop.h:395`, PR body and public receipts - current thresholds, source-term premise, corrected row and 80 ms approval agree. The 0.78 approval is explicitly pending, not falsely claimed. R1-R2 are wording/publication residue only.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F2 | Issue rulings; FR_NFR; load/delivery rate; median arithmetic; ceiling probe | R958-3 applied; no clean covering round | 3181a3ec372b6473175cc1c842ada8133a96b127 |
| RTL | CLEAN | Production token equality; delivery interfaces; hot list; gitlinks; 80-path ELF chain | R958-3, retaining unaffected R958-2 assessments | 3181a3ec372b6473175cc1c842ada8133a96b127 |
| Robustness | UNCLEAN - F1 | D8-D10 loss/turn cases and plants; invalid-ceiling failure propagation | R958-3 applied; no clean covering round | 3181a3ec372b6473175cc1c842ada8133a96b127 |
| Tests | UNCLEAN - F1 | Load controls; flip adapter mutation; published final shards; whitespace before/after | R958-3 applied; no clean covering round | 3181a3ec372b6473175cc1c842ada8133a96b127 |
| Docs | CLEAN | Platform threshold; load premise; row/approval citations; comment changes; PR/evidence distinction | R958-3 | 3181a3ec372b6473175cc1c842ada8133a96b127 |

**Limits and manager duties.** No manager source bank exists at this head, and none is claimed or inferred. This review did not run full parent/protocol/gPTP/synthesis/builder banks, local workflow replication, hardware or calibration. Physical calibration is **NOT RUN**; field skips are not hardware proof. Hosted job execution was not audited in this narrow round; hosted/local-replica acceptance remains the manager's duty.

The manager must obtain the owner decision, have F1 corrected and re-reviewed, carry residues, complete the independent-review bar, and validate the actual then-current `dev` merge candidate with builder/native banks and publish its receipts. Supplied live `dev` is `e275d7950ef3385753e6a15d2e191ba855b171ed`; the source base is `dev-soft-core`. Source-head evidence does not validate that future candidate. Protected contexts, explicit merge authorization, containment and issue/project completion remain separate duties. This session made no source fix, commit, push, GitHub write or merge.

**Reproduction and integrity.** Run `audit_evidence.py`, `probe_model.py`, `run_checks.py`, and `audit_checkout.py` with the checkout path as their first argument. The evidence audit needs the named public evidence commit fetched. Scripts wait for every child; independent checks ran concurrently with four workers. Mutations were in memory only. Disposable extraction and temporary trees are under `scratch/`, excluded from publication. `checkout-audit.json` verifies 3,374 tracked blobs across root and five initialized dependencies, modes, indexes and all gitlink oids. The unchanged `external` gitlink remains uninitialized. All audited worktrees are clean; head and tree match the assignment. Only REPORT.md and MANIFEST.sha256-listed files are publishable.

R958-3 FINISHED
