[R956] NEGATIVE - exact head 5d03517f2ab42416654a8f2be2f71cfc51d82440

Independent external review, R956-1, of kebag-logic/tsn-c-stack PR #41 for kebag-logic/milan-fpga #977. Tree: ea28576a2e51dde5c38be79be870c339f920460f. Comparison base: c3bff8f3dea03870ea7ae62965db360b509ee3b3.

The implementation inspected preserves the base behavior. Both targets and the registered mutation campaign pass. Approval is withheld because three non-equivalent defects in the newly expanded binding-record comparison survive every shipped hosted test. Public-input witnesses demonstrate their effect on required persistence. No source fix was made.

## Scope and authorities

Reconstruction began with the supplied repository instructions, CONTRIBUTING.md, README.md and the documentation index, then public issue acceptance and scope decisions, requirements and port contracts, the complete base-to-head diff and its two implementation commits, then published evidence. No private author material or another reviewer's report was used.

- [Issue #977](https://github.com/kebag-logic/milan-fpga/issues/977): registering-burst measurement, registration count times cost, unchanged SRP unit and owner bounds. The [November 23 ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7091882145) requires the MRP-rate count and includes per-pass and transmit bounds. The [subsequent stack ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7180135694) requires the stack's own review and eventual consumer pin to its main merge commit.
- [Stack issue #32](https://github.com/kebag-logic/tsn-c-stack/issues/32), ACMP-13, docs/PORTING.md:343: retain callback order and arguments, mark ownership and completion clearing. ACMP-02/03/07/09/10 cover replies, persistence, backpressure and publication ordering.
- docs/PORTING.md, “Persistence and startup”: local 20-byte record, flags, reserved zero byte, big-endian unique/Talker/controller IDs and all-zero unbound record. Binding persistence traces to Milan v1.2 5.5.2.4 and 5.5.3.5.2. GET_RX_STATE follows the repository's IEEE 1722.1-2021 8.2 and Milan v1.2 5.5 interpretation, with Table 5.37–5.39 response witnesses in tests/test_acmp.cpp.
- CONTRIBUTING.md and docs/VERIFICATION.md require runnable planted defects and assertion-specific kills. The assignment additionally requires killing coverage of every new path.
- [Published stack packet](https://github.com/kebag-logic/milan-fpga/tree/53ac1c2ed5af48bf961c85b0184f6dfa99df02a2/review-evidence/tsn977-r1): PR-BODY-tsn.md and HANDOFF-r8.md. Also inspected the full-receipt index in [977-r1](https://github.com/kebag-logic/milan-fpga/tree/977-review-evidence/review-evidence/977-r1). Consumer CPU figures belong to PR #993; they were not independently remeasured here.

The [IEEE edition page](https://standards.ieee.org/ieee/1722.1/6670/) was accessible but did not provide clause text; the linked [Avnu resource](https://avnu.org/resource/milan-specification/) returned 403. Conformance here is an independent behavioral-identity review against the pinned repository requirements, interface contracts, source and executable clause witnesses, not a fresh audit of the complete standards or device certification.

## Findings

### R956-1-F1 — MAJOR — Tests

**Artifact:** src/acmp.c:522, :524 and :526; tests/mutations.json; tests/test_acmp.cpp:480 and :507; tests/test_acmp_walk.cpp:157–169.

**Defect:** The new explicit octet comparisons lack effective regression coverage. Independently replacing any one of these terms with `0u` compiles and passes all 477 registered test instances across all ten hosted binaries, without skipped, disabled or incomplete cases:

| Disposable plant | Omitted comparison | Public input distinguishing the defect |
|---|---|---|
| omit-talker-top-octet | `p[4] ^ (th >> 24)` | Rebind, changing only the Talker entity ID's top octet from 00 to 02 |
| omit-controller-top-octet | `p[12] ^ (ch >> 24)` | Rebind the same source, changing only the controller entity ID's top octet from 00 to 02 |
| omit-unique-high-octet | `p[2] ^ (unique >> 8)` | Rebind, changing only the Talker unique ID from 0001 to 0101 |

The random walk compares two instances of the same compiled implementation, one with all marks set. It tests marking well but shares `record_moved` on both sides. Existing binding cases change multiple fields or fixed values together and do not expose these omissions.

**Authority/evidence:** The test-sensitivity obligation above; [probe results](receipts/probes/results.json) and each plant's ten raw XML/log pairs. [probe_sensitivity.py](probe_sensitivity.py) applies isolated defects without editing the checkout. [witness_persistence.py](witness_persistence.py) adds three disposable public-input witnesses: the unmodified head passes 3/3; each mutant fails precisely its corresponding witness, returning zero persistence calls instead of one and leaving the saved octet stale. See [witness results](receipts/witness/results.json) and raw XML. Compilation errors, crashes and unrelated failures are not counted as kills.

**Impact:** The regression suite accepts a version that acknowledges a changed binding but omits its persistence notification. A store driven by that notification can retain the old binding across restart. This is a validation defect in the reviewed delta, not a claim that the current implementation omits those bytes. The recorded 512/512 registered kills remain true but do not cover these failure modes.

**Required outcome:** Add independently expected persistence checks for isolated significant-octet changes in the Talker ID, controller ID and unique ID, including these three cases. Register executable defects against the new comparison terms with unique named assertion needles. Extend cases across the expanded field comparisons so simultaneous changes cannot mask an omitted term. Preserve existing mutation coverage and the coverage ratchet.

**Verification:** Unmodified Linux and RV32 gates remain green; each new plant compiles, completes and fails its intended assertion. The full hosted suite must reject each supplied plant. Regenerate affected test inventory/traceability as required. Tests remains UNCLEAN until demonstrated at a new reviewed head.

### R956-1-R1 — RESIDUE — Docs

**Artifact:** [PR #41 body](https://github.com/kebag-logic/tsn-c-stack/pull/41), opening paragraph; public-pr-body.md.

**Authority/evidence and impact:** “Branch `977-settle` (local, for the manager to push)” is stale after publication of this exact head. This is only publication-status wording; it changes no measurement, requirement, clause claim, code, test or verdict.

**Exact fix:** Replace `(local, for the manager to push)` with `(published at 5d03517f2ab42416654a8f2be2f71cfc51d82440)`.

**Verification:** Read the published PR opening after the manager's edit. This residue does not make Docs unclean and does not determine the negative verdict.

## Independent lens evidence

**Conformance.** Inspected every changed function and its callers. `record_moved` compares exactly the bytes `record_of` generates, including byte 1 and all-zero unbound values. `view_moved` retains the former comparison set and excludes binding/discovery/state-only changes just as `view_equal` did. Stream fields are zero outside settlement; registration failure is masked outside SETTLED_RSV_OK. Field copies cover every binding and stream member. Completion retains publication, rearm, admission, persistence, then permitted notification ordering. GET_RX_STATE construction is unchanged and reads the live sink, not the reported cache. Existing A2/A4/A5/A6/A19/A24/A25/A31 cases cover response fields, state changes, restore/latch and deferred notifications. The three added witnesses pass at the head. A separate base/head helper comparison passed 100,000 seeded states and 2,000,000 single-bit saved-record differences under address/undefined-behavior checks ([receipt](receipts/helper-equivalence.log)).

**RTL.** The delta contains no RTL, register/mailbox definitions, public header/layout changes, target flags or hardware configuration. Inspected include/acmp.h, include/wire.h, CMakeLists.txt, cmake/rv32.cmake and the port ownership/boundary contracts. RV32 Debug and Release link the whole core archive, audit dependencies/symbols, and execute the smoke port successfully. [RV32 results](receipts/rv32/results.json) record ELF identities, no unresolved final symbols and permitted imports. This establishes the portable software boundary; it does not establish physical latency, calibration, timing closure or consumer CPU cost. No hardware or RTL bank was run.

**Robustness.** Checked shift bounds, word reload at sinks 0/32, configured loop bounds, all-word clearing, and serialization/re-entry preconditions that make cached mark-word traversal safe. The record comparison adds no allocation, alignment dependency or input access. Sanitized wide/walk tests exercise 1/8/32/33 sinks and backpressure. Independent wrong-word defects in admission and finish are caught by walk/wide suites (receipts/probes/admit-word-zero and finish-word-zero). Bytewise comparisons and field copying also pass the independent helper comparison.

**Tests.** GCC coverage and Clang address/undefined-behavior builds pass all ten binaries. The complete registered campaign reports 512 CAUGHT, 0 ESCAPED, 0 ERROR, including all nine re-anchored entries. ACMP coverage is 877/877 lines and 468/468 branches. Comments, assertion needles, port contracts, traceability, test inventory, licence and boundary checks pass. F1 is retained despite these green gates. Local versions: GCC 16.2.1, Clang 23.1.5, GoogleTest/GMock 1.14.0; source-token checks used pinned Clang 18.1.3. RV32 used riscv64-elf-gcc 16.2.0 and QEMU 11.1.3. These are distinct from hosted toolchain evidence.

**Docs.** Reviewed the changelog, PR body, published handoff, verification/traceability documentation and every changed source comment. New comments contain requirement IDs only, without prohibited review/role/lane residue. The nine re-anchored mutation claims and coverage figures reproduce. R1 is obsolete publication wording. The merge audit confirms that the changelog retains both sides' additions and mutations.json is the exact intended union, preserving main's ADP cases.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP source/header, ACMP-02/03/07/09/10/13, PORTING, response/persistence tests, helper comparison and public-input witnesses | R956-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| RTL | CLEAN | Complete diff, headers/wire helpers, CMake/RV32 toolchain, dependency/symbol audit and Debug/Release smoke | R956-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| Robustness | CLEAN | Mark-word loops, bounds, clearing and guards; sanitized wide/walk suites; wrong-word probes; helper equivalence | R956-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| Tests | UNCLEAN — F1 | mutations.json, 512 registered kills, all hosted binaries, three surviving octet omissions and distinguishing witnesses | R956-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| Docs | CLEAN; R1 residue | CONTRIBUTING, README, requirements/port/verification/traceability docs, CHANGELOG, PR body, published evidence and source comments | R956-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |

## Execution evidence, prior findings and limits

[run_checks.py](run_checks.py) reproduces the local checks; the other four scripts reproduce sensitivity, witnesses, helper comparison and identity/provenance checks. Dependencies are supplied through the environment; no shared installs were made. Host builds use `make -j16` and are serialized to respect the total job cap. Independent mutation/RV32 campaigns run concurrently within a foreground controller: eight mutation workers and two four-job RV32 builds. Every launched process completed before finalization. Disposable artifacts are confined to scratch/.

Exact-head hosted runs [45942571101](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45942571101) and [45942567069](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45942567069) report successful quality and bare-metal jobs. Job metadata and raw logs of the first run confirm checkout of this exact SHA and execution of validation, with no skipped validation contexts. Its quality log records 28 gates at rc 0. These are hosted source results, not manager source-bank receipts. Author publication and reviewer execution are separately identified.

After the independent diff pass, the public PR conversation/review collection contained only two review-start notices, including [this review's start](https://github.com/kebag-logic/tsn-c-stack/pull/41#issuecomment-7210238486). It contained no prior public FINDINGS to resolve or retain. No other review report was opened before this verdict and ledger were written.

[Identity receipt](receipts/identity.json) verifies all 100 tracked entries by blob bytes and executable modes, the full stage-zero index, exact head/tree and an empty status. This repository has no submodule gitlinks. Merge parents are 175cf9e052d5f38d81274436262b08a666447edb and the stated main base. Every main-only file equals main, the ACMP-only file equals the implementation parent, and both overlapping files are the exact intended combination. No source edit, commit, push, merge, GitHub write, author contact or other-checkout edit was made.

Pending manager duties: obtain the required positive independent reviews after F1 closes; carry R1 on the residue checklist; own hosted/act acceptance; build and validate the final current-dev consumer merge candidate and publish builder/native receipts at the merge turn. Source validation here is distinct from that candidate (the assignment names live dev e275d7950ef3385753e6a15d2e191ba855b171ed). Move the consumer pin to the stack main merge commit and perform the required rebuild/measurement. Physical calibration remains NOT RUN; skipped field contexts and simulation are not hardware proof. No manager source bank at this head is asserted or inferred.

MANIFEST.sha256 lists publishable scripts and receipts. scratch/ is excluded. Receipt paths are normalized for publication; normalization.json retains original and published SHA-256 values. No test results or diagnostics are changed by path normalization.

R956-1 FINISHED
