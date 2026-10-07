[R533] POSITIVE - exact head 6f7deea15a9160761b30aaa93fe152f20d416695

R533-4, external independent delta review of issue #665 / PR #690.
Tree: `485029d20cffa5d1970a608553b169d547838779`.
All five source-review lenses are CLEAN. R532-3-F1 and R532-3-F2 are resolved. No open BLOCKER, MAJOR or MINOR remains. One optional upstream suggestion and one wording residue are retained below. Hosted acceptance and final merge validation remain manager duties.

The review reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the public issue and frozen decisions, REQUIREMENTS.md, the ownership and mailbox contracts, the source-base file population/history, and the focused delta. The governing [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6036454509) permits tests and documentation only. Public author evidence at `fa19435a` is historical; the current [author-r4 packet](https://github.com/kebag-logic/milan-fpga/tree/76fa75c9cbdf7b557cebecf4d00f0ed41850842d/review-evidence/665f4-r1/author-r4) contains the handoff and PR body. Its claims are distinguished from this review's own executions.

The independent verdict and ledger were written in `receipts/independent-verdict.md` before reading prior public reviewer findings or reports. Earlier findings were then reconciled explicitly below. No private author material, management checkout, concurrent round-4 report or author contact was used.

`receipts/scope-proof.json` proves that this head is one commit after `c1049de1970e93d2c36ace62891ee9d947cd3191`. Only these files change:

| Artifact | Round-4 change |
|---|---|
| `sw/firmware/ctrl/test/srp_mbx.cpp:819` | Three wire regressions, 101 added lines |
| `sw/firmware/ctrl/test/srp_mutants.py:487` | Three matching mutation entries, nine added lines |
| `sw/firmware/ctrl/srp/README.md:65` | Explicit current-Domain VID exception |

No production source, RTL, interface, generated artifact, gitlink, coverage ratchet or exclusion changed from round 3. The full `db9aa8c9b135b34ff3d070a979dee70440b37cc6..6f7deea15a9160761b30aaa93fe152f20d416695` history includes the earlier dev merge. Against integrated dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`, F4 changes no `hdl`, `sw/litex`, `configs`, `syn` or `constraints` path. The source-base AAF changes are inherited dev changes.

**Round-3 findings resolved**

| Finding and original lenses | Exact-head verification | Disposition |
|---|---|---|
| R532-3-F1, MINOR, Tests | `JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves` at `srp_mbx.cpp:819` first proves wire Ready, adds an ineligible binding in the other slot, removes the eligible binding without intervening service, then requires Lv and rejects every stale renewal. `ReboundStreamCannotInheritAnotherStreamsReady` at `:851` requires the rebound StreamID's own wire Ready beside an unrelated Ready stream. Independent RP3 and RP10 plants each compile and fail only their named test at IF=1/2, with both slot orders on every interface. The catalog entries at `srp_mutants.py:487/490` match the independently specified plants and observables. | RESOLVED |
| R532-3-F2, MINOR, Tests and Docs | `FinalDomainVidUnbindKeepsSrClassMembership` at `srp_mbx.cpp:886` requires Listener withdrawal while the current Domain membership renews without MVRP Lv. It covers VID 2 and peer-selected VID 7, both slots, every interface. Independent RP5 removes the guard at `srp_mbx.c:334`; it compiles and fails `d.event` in the named test at IF=1/2, including all eight IF=2 combinations. Catalog entry `srp_mutants.py:493` matches. README lines 65-67 now agree with the existing guard. | RESOLVED |

The positive source passes all three cases. The six negative runs are successful defect-detection controls, not source failures. Every negative binary runs one named test and exits 1 with the required assertion; no build error is counted as a catch. `receipts/probe-results.json` records all trace sets, and the `RP3-if*.log`, `RP10-if*.log` and `RP5-if*.log` files retain the raw diagnostics.

**Independent lens results**

[R533] PASS Conformance - `REQUIREMENTS.md:24`, issue 665 assignment 6036454509, `srp_mbx.c:305-337/493-554`, `srp/README.md:53-67`, `srp_mbx.cpp:819-919` - checked that the new assertions preserve shared per-interface StreamID ownership and current-Domain membership under the frozen scope. The README corrects its description of an existing exception; no protocol rule or production behavior changes. Existing immediate MSRP withdrawal, original LV deadline and generic MVRP cases pass within the 53-case suite, and the selected wire differential passes at both interface counts.

[R533] PASS RTL - `receipts/scope-proof.json`, `srp_mbx.h`, `srp_mbx.c:308-337/599-637/676-697`, mailbox contract - checked applicability, unchanged binding state ownership, current-level interface recovery and serialized output boundaries. The complete round-4 path set contains no runtime, HDL, CDC/reset, ABI, shape or build-selection change. Round-3 architecture coverage is retained against byte-identical artifacts.

[R533] PASS Robustness - `srp_mbx.cpp:681/708/737/775/819/851/886/920/950/963/987/1010`, `srp_fixture.hpp:74-115`, `receipts/adapter-if*.log`, `receipts/RP*-if*.log` - exercised ordering, cross-slot inheritance, cross-StreamID isolation, final-user removal, current and changed Domain VIDs and per-interface independence. Existing lifecycle, malformed-input, allocation, backpressure and reentry cases pass. Conditional latency cases retain the original time origin under an excessive stall. These are host-model results.

[R533] PASS Tests - `srp_mbx.cpp:819-919`, `srp_mutants.py:487-495`, `srp_arms.py:41-78`, `srp_fixture.hpp:74-115`, `scripts/run_probes.py` - checked the independent wire decoder, unmodified test compilation, named-case grading and all three mutation mappings. The new assertions discriminate the three reported defects, including every requested order. Full baseline adapter suites pass, and seven focused documentation/style/contract commands pass. The coverage target and exclusions are unchanged; complete coverage was not rerun by this reviewer.

[R533] PASS Docs - `srp/README.md:65-67`, `srp_mbx.c:329-337`, PR body Round 4, public author-r4 handoff, `receipts/delta-checks.json` - checked the Domain-VID exception against implementation and emitted-wire evidence, accurate test-to-defect claims and separation of source, hosted, candidate and physical evidence. The remaining PR publication tense is only the residue recorded below.

**Reviewer-owned coverage ledger**

This ledger applies to the current exact head. [R533-3](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6036369877) covered all five lenses at `c1049de1970e93d2c36ace62891ee9d947cd3191`. Its unchanged runtime and architecture evidence is carried only where `scope-proof.json` proves byte identity. Changed tests and prose were examined afresh in R533-4; no changed artifact is cleared solely by the prior round.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c:305/493/599/681`; README:53-67; new wire assertions; selected wire receipts | R533-3 unchanged behavior, R533-4 delta and contract confirmation | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| RTL | CLEAN | `scope-proof.json`; unchanged `srp_mbx.h`, mailbox contract and architecture seams | R533-3 at `c1049de1970e93d2c36ace62891ee9d947cd3191`, carried by R533-4 applicability/identity check | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| Robustness | CLEAN | `srp_mbx.cpp`; baseline, wire, latency and six fault receipts; complete interface/slot/VID trace sets | R533-4; untouched runtime baseline retained from R533-3 | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| Tests | CLEAN | Three new cases and catalog entries; fixture decoder; `probe-results.json`, raw logs and command receipts | R533-4 | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| Docs | CLEAN | README:65-67; public scope, PR body and author-r4; `delta-checks.json` | R533-4 | `6f7deea15a9160761b30aaa93fe152f20d416695` |

**Earlier public findings**

The dispositions in both public round-3 reports were checked after the independent pass. The relevant production, prior test bodies and documentation outside the three-file delta are unchanged. Earlier mutation and upstream campaigns cited below are retained round-3 evidence, not executions claimed for this round.

| Prior item | Disposition at this head and evidence |
|---|---|
| R533-1-F1 / R532-1-F1 | RESOLVED, retained. MSRP-only Milan override and D1 are unchanged; `InListenerWithdrawalRevokesLicenceImmediately`, `InTalkerWithdrawalImmediatelyWithdrawsListener`, original-deadline and generic MVRP tests pass now. |
| R533-1-F2 / R532-2-F1 | RESOLVED, retained. Link lifecycle, attach-level sampling and poll-level reconciliation are unchanged. `ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord`, `CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` and other lifecycle cases pass now. R533-3 covered the additional physical-edge sequence in its host probe. |
| R533-1-F3 / R533-2-F1 | RESOLVED, retained and strengthened. Shared replacement code is byte-identical; existing wire rebind/consecutive-replacement cases pass. This round also closes the cross-slot and cross-StreamID test remainder R532-3-F1. |
| R533-1-F4 | RESOLVED, retained from R533-3. The published linked-composition/base measurements and fixture sources are unchanged. No new link was executed in R533-4. |
| R532-1-F2, all three parts / R533-2-F2 | RESOLVED, retained. Exact admission-boundary and Ready-to-ReadyFailed strict callback tests pass now. The public `f4-applicant-notes` topic and note-4/5 reversals were verified in round 3; its cited tests and dependency pin have not changed. |
| R532-2-F2 | SOURCE RESOLVED, retained. The dependency inventory, licence and generated boundary artifacts are unchanged from the clean round-3 review. Focused documentation checks pass now. Hosted dependency access and required context completion remain separate manager obligations. |
| R532-2-F3 | RESOLVED, retained. `LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder` passes; the correct never-requesting setup is preserved. R532-3-F2 closes the complementary Domain-VID boundary. |
| R532-2-F4 | RESOLVED, retained. The three lifecycle/shared-VLAN cases and their existing mutation entries are unchanged; all three positive cases pass in the current full adapter suite. Their defect sensitivity remains the recorded round-3 evidence. |
| R532-1-S1 | ADDRESSED, retained. Upstream LeaveAll scope test/pin unchanged; current selected Run-B differential passes. |
| R532-1-S2 | RETAINED SUGGESTION, detailed below. |
| R532-1-S3 | ADDRESSED, retained. Participant recreation guards are unchanged; allocation/refusal cases pass. |
| R532-2-S1 | ADDRESSED, retained. `MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline` passes at both counts; its mutation entry is unchanged. |
| R532-1-R1 | RESOLVED, retained. TICK centiseconds and NOW_MS remain correctly distinguished. |
| R532-1-R2 | SUPERSEDED/RESOLVED. Linked measurements now exist; the obsolete object-only limitation is not restored. |
| R532-2-R1 | RESOLVED, retained. The dependency fetch/published-pin guidance is unchanged. |
| R532-3-R1 | RESOLVED. PR Status and Round 3 now state REVIEW READY and cite the manager's successful compiler-absent run. |
| R532-2-R2, as retained by R533-3 | PARTLY RESOLVED; publication-tense RESIDUE retained below. The stale STOP claim is gone, but the PR still uses future publication instructions. |

**R532-1-S2 | SUGGESTION | Conformance, RTL**

Artifact: `third_party/lwSRP/src/core/mrp_mad.c:341/347`; `sw/firmware/ctrl/srp/srp_mbx.c:77/619-637`.
Authority/evidence: the earlier reviews identify the generic Table 10-4 LV/rJoin extra Join indication. Those dependency rows are unchanged. The adapter compares Domain values and recomputes retained registrations; no failing adapter behavior was found. Impact: a future bridge consumer may depend on the generic callback distinction. Required outcome: optional upstream evaluation, carried to the dependency follow-up rather than expanded into this lane. Verification: a future change should test the generic transition and callback consumers. This suggestion leaves no lens unclean.

**R532-2-R2 | RESIDUE | Docs**

Artifact: PR #690 body, Status and How to get into the same state (`receipts/pr-body.txt`).
Authority/evidence: [public review start 6036805951](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6036805951) identifies the published exact head, while the body says `This round makes no push or PR edit.` and `After the integration role publishes this head:`. Impact: stale publication tense only; this changes no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule.
Exact fix: replace the first sentence with `At author handoff, no push or PR edit had been performed. The integration role has published this head for review.` Replace the second sentence with `To inspect the published head:`. Required outcome: describe the current publication state without altering historical gate results. Verification: reread those sentences against the public review-start comment. The manager carries this item to the residue checklist; Docs remains CLEAN.

**Executed evidence and reproduction**

| Execution | Result | Receipt |
|---|---|---|
| Adapter suites, IF=1/2 | 53 + 53 pass | `receipts/adapter-if*.log` |
| Selected processor-wire differential, IF=1/2 | 5 + 5 pass | `receipts/walk-if*.log` |
| Conditional service-latency suites, IF=1/2 | 4 + 4 pass | `receipts/latency-if*.log` |
| Independently planted RP3, RP10, RP5 | 6/6 named failures; all required order traces | `receipts/RP*-if*.log`, `probe-results.json` |
| Diff whitespace, documentation wording/paths/style, C++/Python idioms, mailbox generator | Seven commands rc 0 | `receipts/delta-checks.json`, `delta-check-*.log` |
| Final checkout proof | Before/after receipts identical | `receipts/integrity-before.json`, `integrity-after.json` |

`REPRODUCE.md` and `scripts/` reproduce the focused runs. Suite controllers stayed in the foreground, with independent tasks concurrent and at most sixteen compilation jobs. All defect copies and build products are under packet `scratch/`. No source fixes, commits, pushes, GitHub writes, shared installations, container runs, hardware work or edits to another checkout occurred.

The final proof hashes every tracked blob directly, verifies regular-file/symlink/executable modes and complete stage-0 index records, and checks the four required submodule gitlinks: 1169 parent files, 558 processor files, 104 gPTP files, 214 datapath-library files and 55 SRP-dependency files. Parent head/tree remain exact. The optional `external` import remains uninitialized with its original gitlink. No restoration edit was needed because every planted defect used a disposable copy.

**Limits and pending manager duties**

This is source review, not merge approval. The assignment reports that the manager's full source static/builder and native banks passed at this head; those banks were not repeated here. The public author-r4 summary reports 70 SRP plants, 100 control plants and 100% coverage in fifteen files. This reviewer executed the focused population above, not those complete campaigns, target builds or linked-size fixtures. The public evidence branch contains the round-4 summary pages; their referenced large local receipts are not treated as independently executed evidence.

The read-only exact-head hosted snapshot is in `receipts/hosted-snapshot.json`. The firmware job failed at dependency fetch before compilation because SRP-dependency access was unavailable; its firmware, saved-state and coverage steps were SKIPPED. `hosted-firmware-steps.json` and `hosted-fetch-diagnostic.log` preserve that distinction. Several other source jobs had succeeded, while documentation, elaboration and exhaustive simulation jobs were still running. The physical gPTP context was SKIPPED. No skipped context is counted as executed verification. The manager must resolve hosted fetch access and obtain all required exact-head contexts, including the fast aggregate; local replica and hosted acceptance remain theirs.

Round-3 linked spans and the conditional host service envelope are unchanged. The 8192-byte reserved stack is not a whole-call-chain proof. Host access timing is not target scheduling or wire-departure timing. Physical calibration is NOT RUN; field skips, desk tests and compilation establish no hardware or audio-soak proof. ACMP composition, live MAAP/stream inputs and the connected fabric licence output remain the publicly scoped integration work.

The manager also owns the second independent verdict, residue edit, optional upstream follow-up and later reviewed pin move, explicit merge authorization, and post-merge containment. Source base `db9aa8c9b135b34ff3d070a979dee70440b37cc6` with integrated dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` is distinct from the final current-dev merge candidate. Build and validate that candidate at the merge turn, including the delegated builder/compiler-absent obligations, before merge and containment.

Publish only REPORT.md and the files listed in MANIFEST.sha256. Scratch is excluded.

R533-4 FINISHED
