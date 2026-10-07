[R529] NEGATIVE - exact head 8b78a8fd36864246336c71c061ac4f21d629952f

Round R529-3 is complete. All five lenses were applied. One MINOR remains under Docs and Tests: the MAAP reproduction command uses the retired compiler selector. One wording-only RESIDUE is recorded separately. The merge retains both parents' required checks, and the release-assertion change preserves the guard's meaning.

**Scope and independence**

Reviewed tree `ee59c5cb2b3adc55d3907eac24f9a5e27466b6c8`. Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #665 and its frozen F2/round-3 decisions, requirements and interface authorities, then diff/history and public evidence. The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6029938743) governs this delta. Authorities include REQUIREMENTS section 1, NFR-SCOUT-02/03/08 and H-MAAP, the mailbox contract, REGISTER_MAP's allocation/window registers, and #678/#679. The established Annex B review is carried from round 2 for unchanged protocol behavior; this round does not claim a new full reading of the external standard.

The assigned `021b9c1fb966e9a1a4acef6b5233edd3518f32a0..8b78a8fd36864246336c71c061ac4f21d629952f` comparison covers 62 files, including FC and imported dev work. The delta from reviewed head `938497af1dffd8a87edebf3ab93663914bf85e5e` covers 32 files. Merge `5901ab0869e0674bb18bbb4df60757f2711e5cd4` has that reviewed head as first parent and authorized dev `910f338dbd050f4efd2d96991ddcf928a583d55f` as second. Commits `a71b8c8072c28c3511254484de5dda4e57e91d3f` and `8b78a8fd36864246336c71c061ac4f21d629952f` follow it. [Scope receipt](receipts/scope.json).

The [independent verdict and ledger](receipts/independent-verdict-before-public-reconciliation.md) were written before reading prior reviewer findings or reports. Prior findings were read only after the independent diff pass. No private author material, management checkout, other current-round report, or author contact was used. The public checkpoint contained no formal or inline reviews beyond the conversation findings reconciled below. [Checkpoint](receipts/prior-findings-checkpoint.json).

**R529-3-F1 - MINOR - Docs, Tests**

Artifact: `sw/firmware/ctrl/maap/README.md:155`, with `sw/firmware/gtest/fw_rv32.py:29` and `sw/firmware/ctrl/test/ctrl_arms.py:187`.

Title: The executable MAAP validation recipe silently ignores its compiler override.

Authority/evidence: The merge adopts #679's shared `MILAN_RV32_CC` selector. The controller README:126 and public round-3 recipe document it correctly. The MAAP README still runs `CTRL_RV32_CC=riscv64-elf-gcc python3 ... --require-rv32 --self-test`. The old variable is no longer read. The independent [selector probe](receipts/selector-probe.log) uses executable sentinel candidates and reproduces both outcomes: with no default, the documented override yields no compiler; with a competing default, it selects that default. Changing only the selector to `MILAN_RV32_CC` selects the requested executable in both cases. [Portable probe](scripts/selector_probe.py).

Impact: The published validation command can measure a different compiler from the one requested, or refuse despite the explicitly selected compiler being available. That makes the SDK reproduction instructions unreliable. Production MAAP behavior and the correctly configured hosted recipe are unaffected.

Required outcome: Replace `CTRL_RV32_CC=` with `MILAN_RV32_CC=` in the MAAP README command, and keep the recipe consistent with the shared selector. This is the exact required documentation correction; no compatibility alias or source redesign is required.

Verification: At the corrected head, check the literal recipe against `fw_rv32.compiler()` with absent and competing defaults; the explicit selection must win. Existing successful object and mutation evidence remains applicable if its inputs are untouched. This is MINOR rather than RESIDUE because the line is an executable validation command whose environment changes the compiler measured, not purely wording.

**R529-3-R1 - RESIDUE - Docs**

Artifact: PR #687 body, Status paragraph, as captured in [public-pr.json](receipts/public-pr.json).

Authority/evidence: The current body says, "The branch has not been pushed." The same public snapshot identifies published head `8b78a8fd36864246336c71c061ac4f21d629952f`.

Impact: Stale publication wording only; no measurement, test, source, generated artifact or conformance claim changes.

Required outcome / exact fix: Replace that sentence with "The branch is published at the exact head above." Historical author statements about not pushing remain valid and need no edit.

Verification: Read the corrected Status paragraph against the public head. Carry this item to the manager's residue checklist. It does not affect the verdict or lens cleanliness.

**Merge and assertion results**

[retention.log](receipts/retention.log) proves all 192 round-2 mutation definitions retain their exact plants, named tests and failure words. The one new control makes 193 controls and 198 obligations. Four partitions are complete and disjoint: 49/48/48/48. Every executable function in `test_ctrl_firmware.py` matches round 2, including MAAP baseline/coverage arms and partition selection. All pre-existing functions from dev's `ctrl_arms.py` match semantically; the F2 arms remain present. All three MAAP translation units appear among the 12 RV32 objects.

The RV32 build still uses isolated freestanding headers, RV32I/ILP32 release flags, ELF/ISA inspection, static-frame inspection, an exact runtime-helper allowlist, and global/weak definitions for external resolution. Same-name static definitions cannot hide an unresolved dependency. The shared helper, its self-test, saved-state RV32 implementation, hosted ordering and required-RV32 commands match dev exactly. The imported #673 deadline changes and AAF startup RTL also match dev; no F2 resolution rewrites them.

No inherited test or named mutation was dropped or re-graded. Relative to the old F2 branch, #679 tightens object/runtime acceptance and adds ABI/frame validation; those are the authorized incoming checks. The release compile failure caused by hosted `assert.h` was repaired, not accepted as a protocol-mutation kill.

For `maap.c:6,17`, release preprocessing differs only by removal of the assertion's void no-op; debug preprocessing differs only in the diagnostic source line, 15 to 18. The first reviewer comparison incorrectly required that line number to remain identical; [the initial receipt](receipts/retention-initial.log) is retained. The final comparator explicitly checks that sole difference. The debug condition, counter, return path and all other preprocessed bytes remain equal. Independent compiled plants disabling the debug assertion and deleting release reentry accounting fail their named tests. Restoring the unconditional hosted include fails the required RV32 object build. These results preserve #678's assert-in-debug, count-and-ignore-in-release contract.

**Fresh executable evidence**

| Execution | Result | Receipt |
|---|---|---|
| Core/CSR, one-interface mailbox, two-interface mailbox, debug | 37 + 12 + 13 + 1 cases, zero failures | [Focused runs](receipts/maap-focused.log) |
| Core/parent shared-stimulus differential | 12 cases, zero failures; strict core cadence and named parent deviations checked | [Differential](receipts/differential.log) |
| Independently planted retained saved range | Compiles; `MaapCore.LinkBounceDrawsAfterSuppliedRange` fails its exact fresh-range assertion | [Focused plants](receipts/maap-focused.log) |
| Independently disabled debug assertion / release count | Both compile; named debug and release checks fail | [Focused plants](receipts/maap-focused.log) |
| Pinned-SDK controller build | 12 release objects including all three MAAP objects; ABI, dependency and frame checks pass | [RV32 runs](receipts/rv32-focused.log) |
| Independent unexpected MAAP runtime dependency, with same-name local definition elsewhere | Rejected specifically as an unresolved unexpected runtime dependency | [RV32 plants](receipts/rv32-focused.log) |
| Restored unconditional hosted assertion include | Expected compilation failure naming `assert.h`; credited only as an SDK integration control | [RV32 plants](receipts/rv32-focused.log) |
| Shared RV32 self-test | 17 checks pass, including both real firmware runtime arms | [SDK self-test](receipts/rv32-selftest.log) |
| Firmware coverage, `--check --jobs 4` | All 17 files meet 100% line/branch ratchet after unchanged existing exclusions; no MAAP exclusions | [Coverage](receipts/coverage.log) |
| Source-byte and index proof | Exact head/tree; 1,161 root blobs plus required submodules verified | [Final integrity](receipts/integrity-final.log) |

All final wrapper commands exit zero; the negative probes have the expected nonzero inner results shown above. The baseline total is 75 MAAP executions including the differential. H-MAAP wake is 4,700 ns per interface; the stalled interface-1 response is 5,004,400 ns including its 5 ms stall, under the documented host-access assumptions. MAAP coverage remains core 209/209 lines and 140/140 branches, adapter 98/98 and 60/60, CSR 39/39 and 18/18.

The [public round-3 archive](https://github.com/kebag-logic/milan-fpga/tree/0b965bbd/review-evidence/665f2-r1/author-r3) and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030259747) report the complete firmware campaign, mailbox and source banks. HANDOFF.md and PR-BODY.md hashes match the posted values. [Archive identity](receipts/public-author-archive.json). The supplied `ee59ec823d11107a4874d57ae472c7216e97dd7e` snapshot contains the earlier author packet; current round-3 evidence was read at `0b965bbd`. These archives publish the handoff/body and receipt inventories, not every underlying log. Their unprovided raw logs were not independently hash-verified. The complete 193-control campaign and 16 differential controls are cited public evidence, not fresh executions here.

**Prior public findings at this head**

The original severities and lens assignments are retained. [R529-2](https://github.com/kebag-logic/milan-fpga/pull/687#issuecomment-6029833929) and [R528-2](https://github.com/kebag-logic/milan-fpga/pull/687#issuecomment-6029935831) cover corrected head `938497af1dffd8a87edebf3ab93663914bf85e5e`. Byte/semantic retention and the fresh baseline runs establish the following dispositions; no old fix is cleared merely by deferral.

| ID; original severity; lenses | Disposition and head evidence |
|---|---|
| R529-1-F1; MAJOR; Conformance, RTL, Robustness, Tests | RESOLVED retained. `ctrl_app.c:55` and `test_maap_mbx.cpp:273` are unchanged; MAAP/ADP/event IRQ mask and real idle wake cases pass at both interface counts. |
| R529-1-F2; MINOR; Conformance, Tests, Docs; R528-1-F2; MINOR; Tests, Docs | BOTH RESOLVED retained. Differential code and timing controls are unchanged; 12 cases pass, including 500/627 ms parent observations, strict core intervals and four-versus-three PROBEs. README:166 still lists the recorded #686 deviations. |
| R528-1-F1; MINOR; Conformance, Robustness, Tests | RESOLVED retained. `maap.c:108,190,235` retains/consumes the Begin preference; `test_maap.cpp:311` passes. Round 3 adds bounce sensitivity. |
| R528-1-F3; MINOR; Tests | RESOLVED retained. Fixed-seed new-base and every deciding priority-octet case at `test_maap.cpp:179,195` pass; prior plants retain identical grading. |
| R528-1-F4; MINOR; Tests, Docs | RESOLVED retained. Direction-aware CSR model and destination-before-enable trace at `test_maap.cpp:391,446` pass; CSR code and documented order are unchanged. |
| R528-1-F5; MINOR; Tests | RESOLVED retained. `test_maap_mbx.cpp:324` drains stalled interface 1 within the original allowance; implementation and defect are unchanged. |
| R528-1-F6; MINOR; RTL, Docs | RESOLVED retained. MAAP README:101 and current PR body preserve the firmware-allocation-to-processor/F3 dependency before use. Shim and datapath consumers are unchanged. |
| R528-1-S1; SUGGESTION; Tests | ADDRESSED retained. Generic predicate controls remain identical; README:144-145 and PR body retain the release-object/host-debug limits. |
| R528-2-S1; SUGGESTION; Tests | ADDRESSED. `test_maap.cpp:331` exercises Begin while down, up/down/up, a fresh in-pool base and complete post-bounce PROBE. The exact retained-preference defect fails the named new assertion. This pins local one-use policy, not a new Annex B requirement. |
| R528-2-R1; RESIDUE; Docs | RESOLVED. `ctrl/README.md:25` now says ten arms and optional `lwsrp`, matching the ten dispatched baseline arms. |

**Reviewer-owned ledger**

Every row applies at the current head. R529-2 coverage is carried only for unchanged artifacts or unchanged behavior proved by the retention audit; the imported delta and assertion/build interaction were examined in R529-3. The old covering head is explicitly `938497af1dffd8a87edebf3ab93663914bf85e5e`, not the merge candidate.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `maap.c:6,17,108,190,235`; `test_maap.cpp:331`; #678/#679; FR_NFR:363,409; unchanged wire/timer/CSR contracts and fresh baseline/differential | R529-3 delta; R529-2 untouched protocol obligations at the old head above | 8b78a8fd36864246336c71c061ac4f21d629952f |
| RTL | CLEAN | `ctrl_app.c:55`, `maap_mbx.c:94,119`, `maap_csr.c:42`; mailbox/CSR/shim interfaces retained from round 2; imported `KL_aaf_packetizer.sv:271,319,591,715,742` equals authorized dev; scope inventory and differential | R529-3 merge/interface pass; R529-2 untouched F2 RTL/interface coverage at the old head above | 8b78a8fd36864246336c71c061ac4f21d629952f |
| Robustness | CLEAN | `maap.c:12`; `test_maap.cpp:311,331,384`; `test_maap_mbx.cpp:273,324`; debug/release, bounce, runtime/header plants; unchanged malformed/tag/wrap/stall cases rerun | R529-3 delta and controls; R529-2 untouched behavior at the old head above | 8b78a8fd36864246336c71c061ac4f21d629952f |
| Tests | UNCLEAN | Conflict files; 193-control/198-obligation retention and partitions; 75 baseline executions, five independent plants, SDK self-test, coverage; README:155 selector failure | R529-3 applied; R529-3-F1 open | 8b78a8fd36864246336c71c061ac4f21d629952f |
| Docs | UNCLEAN | `ctrl/README.md:25,122`; `maap/README.md:29,101,144,155,166`; `gtest/README.md:350`; PR and public archive versus current behavior | R529-3 applied; R529-3-F1 open; R1 is nonblocking residue | 8b78a8fd36864246336c71c061ac4f21d629952f |

**Limits and pending manager duties**

This is source review, separate from the final current-dev candidate. Source base is `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`; the assigned live-dev parent is `910f338dbd050f4efd2d96991ddcf928a583d55f`. The manager must resolve F1 and obtain exact-head re-review of affected lenses, carry R1 to the residue checklist, complete independent review, construct and validate the final candidate against current dev, record head/base/tree identities, and perform post-merge containment and public workflow updates after explicit merge authorization. This report authorizes no merge or shipping-default flip.

The [single hosted snapshot](receipts/hosted-snapshot.json) has successful executed firmware, lint, BDD, no-Git docs, wire-accountability, selector and four synthesis shards. Simulation shards, elaboration and docs were still running. Physical gPTP was SKIPPED, not executed. No completed aggregate is inferred from partial results. Hosted and local-replica acceptance remain manager duties; no replica or its self-test was run here.

Physical calibration was NOT RUN. Field/vendor skips supply no hardware proof. Host model times do not establish target CPU, arbitration, NVM interference, wire departure, media quiescence, redundancy acceptance, target debug linkage, full-image linking or whole-program stack bounds. The allocation-to-ACMP integration condition and unchanged parent deviations remain their documented later obligations.

No full parent, processor, gPTP, synthesis or builder bank was run. This delta review did not rerun the mailbox RTL suite, all mutation campaigns, full saved-state RV32 shape bank or documentation bank; their supplied public evidence and unchanged artifacts are distinguished above from fresh runs. No source fix, commit, push, GitHub write, delegated work, privileged action, container operation or hardware access occurred.

All mutations, SDK extraction and builds stayed under packet scratch. Runs were foreground subprocesses joined before completion; first-batch compiler parallelism was at most 13, below 16. [Resource receipt](receipts/resources.json) records a 12 GiB enforced limit, 2,561,003,520-byte peak and zero OOM events. Final raw-byte proof checks tracked modes and exact index records, 1,161 root blobs, 558 processor blobs, 104 gPTP-processor blobs and 214 axis blobs, plus all required registered gitlinks. The optional external submodule remains uninitialized. The checkout is clean including ignored outputs.

Portable reproduction is provided by `scripts/reproduce.py --repo <exact-head-checkout> --packet <new-packet-directory> --sdk-archive <pinned-archive> --verilator <pinned-simulator>`. Individual probes are independently runnable. The coordinator was syntax-checked; its constituent commands were executed directly in this review. Publication receipts normalize only local path prefixes, with original/published hashes in `receipts/path-normalization.json`; original bytes remain in unpublished scratch. `MANIFEST.sha256` enumerates publishable files; scratch is excluded.

R529-3 FINISHED
