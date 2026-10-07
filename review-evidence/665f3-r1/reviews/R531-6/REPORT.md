[R531] POSITIVE - exact head d8060d87f892239ac4e598d0a8556cbfcd4a52ec

R531-6, external independent delta review of issue #665 / PR #688, implementation round 7. All five lenses are CLEAN. R530-5-F1 is resolved; S1 and S2 are addressed. No new BLOCKER, MAJOR or MINOR was found. The previously classified historical wording RESIDUE and optional suggestions are retained below. This is a source-review verdict, not merge or physical acceptance.

Tree: `7db44a4a68c725ee0f4a74cd453eb82134c8bfcd`. Source base: `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`. Delta baseline: `13e715136b0b7c8d9763e0b730d9709f2c9f5932`. The three commits change exactly four files: `test_acmp_mbx.cpp`, `acmp_review_mutants.py`, the ctrl README and `MAILBOX_SPLIT.md`. All production sources, RTL, interfaces, generated contracts, image fixture and coverage ratchet are unchanged from the baseline. `delta.diff` and `audit-results.json` preserve the scope and history.

Reconstruction followed the operating contract, contribution rules, documentation index, public issue acceptance and scope decisions, linked repository requirements/interfaces, then the cumulative source inventory, delta and history, followed by public executable evidence. The controlling scope is [round-7 assignment 6041160063](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6041160063), with [REVIEW READY 6042044802](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6042044802). Earlier authorities are the [F3 acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026721148), [per-interface admission decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6029368753), [linked-size requirement](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), and [three-module composition assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6037650104).

The independent provisional verdict and five-lens ledger were written before reading prior reviewer reports. Prior findings were then reconciled against the baseline and current artifacts. No private author material, management checkout, concurrent review report, or author contact was used. The immutable [c961acab public packet](https://github.com/kebag-logic/milan-fpga/tree/c961acabf3a36cb17085868b5c0f779145cf97aa/review-evidence/665f3-r1) was hash-checked against its manifest; it describes round 1 at `351ae81f`, not this head. Its historical measurements were not promoted to current execution evidence.

**Applied lenses and requested checks**

[R531] PASS Conformance - `REQUIREMENTS.md:61`, `docs/reference/FR_NFR.md:333`, `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1053`, `sw/firmware/ctrl/app/ctrl_app.c:16,57` - The outgoing MAAP source comparison uses bytes 6 through 11 and the captured frame's interface to select `model.own_mac`. This matches the own-unicast admission contract and the cited IEEE 1722-2016 B.2.1 destination rule. U6 examines every captured MAAP frame, requires at least three correct frames on each interface, and permits zero mismatches. The same test source runs in `acmp` and the generated two-interface `acmpif2` arm. Both pass without changing production behavior.

[R531] PASS RTL - `delta.diff`, `sw/firmware/ctrl/app/ctrl_app.h:62`, `sw/firmware/ctrl/acmp/acmp_mbx.h:139`, `sw/firmware/ctrl/maap/maap_mbx.h:19`, `audit-results.json`, `images.log` - No RTL, clock/reset, CDC, register, slot, bus, firmware architecture or shipping-image artifact changed. The composed bound counts the common event-ring read once. Independent compiled header probes give `1012 + 616 - 48 = 1580` at one interface and `1043 + 664 - 48 = 1659` at two. Both linked measurement ELFs are byte-identical to round 6 with the same pinned compiler and unchanged harness. No new HDL execution is claimed for this delta.

[R531] PASS Robustness - `sw/firmware/ctrl/test/test_acmp_mbx.cpp:918,1002,1089`, `sw/firmware/ctrl/test/acmp_review_mutants.py:403`, `focused.log`, `ctrl-suite.log` - Applied interface isolation, absent-frame prevention, backlog, configuration and refusal checks. Each wrong source/filter identity fails only U6's interface-1 assertion. The one-interface controls pass because adding index zero changes nothing. Dropping the whole MAAP share fails F6 at both shapes; dropping the second interface's poll fails F6 only at two interfaces. U6/U7/F6 and the existing malformed, timeout, wrap, re-entry, queue and saved-state cases pass in the complete ctrl suite.

[R531] PASS Tests - `sw/firmware/ctrl/test/test_acmp_mbx.cpp:970,1053`, `sw/firmware/ctrl/test/ctrl_arms.py:44,57`, `catalog-audit.json`, `campaign-audit.json`, `coverage.log` - The checks compare independently observable MAC/register values and separately published module bounds. They can fail at their named assertions, without relying on compilation failure or unrelated test failures. The four new fixtures are additive; all earlier review fixtures retain their exact definitions. All 16 ctrl arms pass. All 469 catalog defects are caught exactly once across the complete, disjoint supported slices. All 20 measured files remain at 100% line/branch coverage after the existing exclusions; the ratchet and exclusion document are unchanged.

[R531] PASS Docs - `docs/design/MAILBOX_SPLIT.md:655,692,709`, `sw/firmware/ctrl/README.md:107,123,226`, `audit-results.json`, `docs-check.log` - Recomputed both pass bounds, the shared 48 accesses, the new four time figures, and the updated 273 ACMP / 469 total fixture counts. The paragraph states the assumed access cost and distinguishes T_svc from the 20 ms ceiling. Existing A1-A4 assumptions, room-wait exclusion and unmeasured wire timing remain visible. The source documentation gate reports zero findings.

The exact focused outcomes are below. A failing cell means exactly one failure in the entire arm, with return code 1 and the required test/assertion. Every passing cell returns 0 with no failure line. Full raw logs are `focused-<defect>-<arm>.log`; `focused.log` and `focused_probes.py` record the independent grading.

| Planted defect | `acmp` | `acmpif2` |
|---|---|---|
| `app-maap-mac-per-interface` | PASS control | U6, `MAAP sends from its own unicast MAC, where a DEFEND is admitted, interface 1` |
| `app-own-mac-per-interface` | PASS control | The same U6 interface-1 check |
| `app-three-way-bound-drops-maap` | F6, `the three-way bound is both modules' passes with each event record taken once` | The same F6 check |
| `app-three-way-bound-one-maap-poll` | PASS control | The same F6 check |

F6's measured worst passes remain 231 and 233 accesses. The symbolic tie prevents a much smaller but still above-observed bound from passing silently. The timing paragraph uses the published bound, not those smaller observed passes:

| Input | Calculation at 1 us/access | Fits 10 ms T_svc | Fits 20 ms ceiling |
|---|---:|---|---|
| Event backlog | `(2 + 1) × 1580 = 4740` accesses = 4.74 ms | Yes | Yes |
| Seven frames owed ahead | `(8 + 1) × 1580 = 14220` = 14.22 ms | No | Yes |
| Full ACMP ring | `(10 + 1) × 1580 = 17380` = 17.38 ms | No | Yes |
| Full ADP ring | `(21 + 1) × 1580 = 34760` = 34.76 ms | No | No |

The owed-frame figure starts after room returns under A3. It is not an end-to-end backpressure or hardware deadline measurement.

**Execution and linked images**

| Check executed here | Result | Receipts |
|---|---|---|
| Complete ctrl suite with required RV32 build | 16 arms PASS | `ctrl-suite.log`, `.rc`, `.command.json` |
| Supported full ctrl campaign, `--slice K/3`, K=1..3, `--jobs 5` | 157 + 157 + 155 = 469 caught; zero escapes or unnamed tests | `campaign-0/1/2.log`, `.rc`, `.command.json`; `campaign-audit.json` |
| Four defects, each through both full ACMP arms, plus clean controls | All expected single-assertion kills and unaffected controls pass | `focused*.log`, `focused.rc` |
| Firmware coverage `--check --jobs 2` | 20 files, 100% after existing exclusions | `coverage.log`, `.rc` |
| Coverage self-test | 28/28 | `coverage-selftest.log`, `.rc` |
| Fresh digest-verified SDK extraction and identity | PASS | `sdk.log`, `.rc` |
| Head and round-6 image at both shapes | PASS, byte-identical pairs | `images.log`, `.rc`; `audit-results.json` |
| Header arithmetic and documentation numbers | PASS | `audit-results.json` |
| Documentation gate and delta whitespace check | PASS | `docs-check.log`, `.rc`; `diff-check.log` |
| Direct blob, mode, index and required-submodule verification | PASS before and after | `integrity-before.json`, `integrity-after.json` |

The SDK archive SHA-256 is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`; compiler version 14.3.0, build `2021.11-18033-g83947c7bb6`. Unlinked `libgcc.a` has SHA-256 `d8ebca8cf6ad31cd50695f79e91e86a716d3b1761fbbefd5ee7b0627a2d0af58`. Each image passes the repository's RV32I/ILP32 executable audit.

| Shape | Text | Rodata | Data | BSS | Accounted total | Round-6 delta | Head and round-6 ELF SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| `endstation_ax7101_1x1_tdm8` | 33,444 | 748 | 0 | 12,416 | 46,608 | 0 | `3d797e8f19a8b06532aa0b7beb4d64cda6e35f1b965635a4466ea0d2eae4788f` |
| `endstation_ax7101_8x8` | 33,448 | 748 | 0 | 22,784 | 56,980 | 0 | `96eaa98578ea8eee4c516da408ba1d1050c152a245388d6b64cecc396fe01671` |

These section totals include BSS; each ELF file itself occupies 49,904 bytes. The image fixture still excludes the final stack and integration-owner/pool sizing and uses the disclosed runtime/arithmetic stand-ins. It is not a shipping image.

Independent suites, probes, coverage, images and campaign partitions ran concurrently under a foreground runner. Maximum configured compilation concurrency was 16 jobs; campaign-only rerun concurrency was 15. `resource-receipt.json` records the unit peak, cap and zero out-of-memory events. No hardware, shared installation, source fix, commit, push, GitHub write, full builder/parent/processor/synthesis bank or local workflow replica was run.

A superseded interleaved campaign attempt is retained in `interleaved-attempt-*`. `--mutation-shard` filters the catalog before the complete naming audit, so those partial catalogs reported missing mappings. Those processes were deliberately stopped, not counted as a pass. The documented `--slice` invocation partitions execution while retaining the full naming catalog and passes. No test or source was weakened. `REPRODUCE.md` and the portable scripts describe the accepted commands and receipts.

**Prior public findings at this head**

The controlling baseline reports are [R530-5](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6041153387) and [R531-5](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6040763444). Earlier public reports were examined after the independent pass; their URLs/body hashes and the unchanged-artifact check are recorded in `prior-findings-reconciliation.json`. Resolved baseline findings are not reopened without a changed artifact or new contrary evidence.

| Prior ID; original severity and lenses | Disposition at d8060d87 and evidence |
|---|---|
| R530-5-F1; MINOR; Tests | RESOLVED. U6 at `test_acmp_mbx.cpp:1053` compares every captured MAAP source with its own interface's MAC, at both shapes. Both planted identity defects produce only the required interface-1 failure. |
| R530-5-S1; SUGGESTION; Tests | ADDRESSED. F6 at line 970 ties both module bounds minus shared event reads; both bound defects are caught at the required shapes. |
| R530-5-S2; SUGGESTION; Docs | ADDRESSED. `MAILBOX_SPLIT.md:709` states all four conditional times and their T_svc/ceiling consequences; independent arithmetic agrees. |
| R531-1-F1; MAJOR; Conformance/RTL/Robustness/Tests | Resolution retained. Unsupported-version guards and A26/B9 are unchanged; ctrl suite and current campaign pass. |
| R531-1-F2; MAJOR; Conformance/RTL/Robustness/Tests; R531-2-F1; MAJOR; all five lenses | Resolution retained. Accepted-send clock refresh, deferred-probe matching and A27/A30 are unchanged; tests pass. The relevant latency formulas remain intact. |
| R531-1-F3; MINOR; Conformance/RTL/Robustness/Tests | Resolution retained. Subtractive slot-range check before narrowing and B7 boundary cases are unchanged and pass. |
| R531-1-F4; MINOR; Docs | Resolution retained. Two-module owed bound remains 9,108 accesses / 9.108 ms with room wait excluded; the new paragraph explicitly distinguishes the three-module bound. |
| R531-1-F5; MINOR; Docs | Resolution retained. `acmp.h:425` still promises one oldest owed frame per poll; A19/E2 pass. |
| R530-1-F1; MINOR; Tests/Robustness | Resolution retained. Generated two-interface arm passes all 22 cases. |
| R530-1-F2; MINOR; Tests | Resolution retained. A24 literal BINDING bytes/flags/length guards are unchanged and pass. |
| R530-1-F3; MINOR; Tests | Resolution retained. N7 preserves bindings through D3 rollback; all seven NVM integration cases pass. |
| R530-1-F4; MINOR; Tests/Robustness | Resolution retained. A28 wrap/deadline cases and their fixtures are unchanged and pass. |
| R530-1-F5; MINOR; Conformance/Docs | Resolution retained. LD1-LD3 executed comparisons and TD1 source-read evidence remain distinguished under the recorded clause ruling; the 127-case ACMP walk passes. |
| R530-2-F1; MINOR; Tests | Resolution retained by unchanged baseline. Q22/Q23, interface/owed-copy fixtures and mailbox RTL are byte-identical to round 6. This delta review did not rerun their HDL bank. |
| R531-2-F2; MINOR; Conformance/Tests/Docs; R530-2-F2; MINOR; Conformance/Docs; R531-3-F1 and R530-3-F1; MINOR; Conformance/Tests/Docs | Resolution retained. Fresh pinned-SDK builds reproduce both section tables and exact round-6 ELF hashes; image audit code and fixture are unchanged. |
| R530-2-F3; MINOR; Docs | Resolution retained. Two-module access limits remain 0.89/0.44 us; three-module limits remain 0.57/0.28 us. New prose agrees with the table. |
| R530-1-R1 and R530-2-R1/R2/R3; RESIDUE; Docs | Resolved status retained. Admission decision, accepted area result and historical round labels remain intact. |
| R530-3-R1; RESIDUE; Docs | Resolved status retained. Public PR title remains “Mark II F3: bare-metal ACMP core on the mailbox”. |
| Earlier co-simulation relink obligation | Resolution retained by unchanged `tb/verilator/mbx/Makefile` and its prior baseline disposition. No new relink experiment claimed. |
| R530-4-R1; RESIDUE; Docs | RETAINED with the exact historical correction below. |
| R530-2-S1/S2/S3; SUGGESTION | RETAINED as optional public area excerpts, copy-window/general-interface-bound wording, and complete area-table rows. Their artifacts are unchanged; no clean-lens effect. |
| R530-4-S1/S2; SUGGESTION; Robustness | RETAINED as optional checked compiler-pin identity and isolated-interpreter support. The explicit pinned-compiler recipe works and was used here. No clean-lens effect. |

ID: **R530-4-R1**. Severity: **RESIDUE**. All attributable lenses: **Docs**. Artifact: [public round-6 HANDOFF.md:483](https://github.com/kebag-logic/milan-fpga/blob/16497e023fd082b4dd8e9f57969d4f3b47ef053a/review-evidence/665f3-r1/author-r6/HANDOFF.md#L483), in the historical round-5 section; also the surviving round-5 copy. Authority/evidence: the baseline finding's alternate-compiler receipt and the still-present sentence. Impact: the historical optional compiler-selection aside gives the wrong expectation; the current pinned measurements and source audit remain unaffected. Required outcome / exact fix: replace `and its images would fail the audit (as round 4's do)` with `and, since no library is linked, its images pass the audit with the same figures; only round 4's library-linked images fail it`. Verification: inspect the corrected current public copy or an explicit historical erratum against the already published receipt. The author reports a local wording correction in REVIEW READY, but that does not alter the immutable public copy inspected here. Preserve the baseline's verdict-neutral classification and carry the public correction on the manager's residue checklist.

The older optional suggestions retain their original public outcomes and verification: R530-2-S1 asks for exact-head utilization/timing excerpts (Docs; area evidence artifact; improves reproducibility; verify provenance against the accepted area result); S2 asks for the copy-suspension and interface-scaled copy bound in `mailbox.yaml` / `MAILBOX_CONTRACT.md` (Docs/RTL; improves contract clarity; verify against copier behavior); S3 asks for the omitted small-block rows in the historical area table (Docs; improves accounting visibility; verify row sums). R530-4-S1 concerns `ctrl_image.py:312` (Robustness; printed identity is not enforced; optionally reject a compiler outside the pin and test refusal); S2 concerns the same command's imports (Robustness; `python3 -I` is unsupported; optionally make isolated invocation work and test it). These are retained SUGGESTIONs, not new blocking findings or claimed fixes.

**Reviewer-owned completion ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REQUIREMENTS.md:61`; `FR_NFR.md:333`; `test_acmp_mbx.cpp:1053`; `ctrl_app.c:16,57`; `focused.log` | R531-6 | d8060d87f892239ac4e598d0a8556cbfcd4a52ec |
| RTL | CLEAN | `delta.diff`; `ctrl_app.h:62`; `acmp_mbx.h:139`; `maap_mbx.h:19`; `audit-results.json`; linked ELFs | R531-6 | d8060d87f892239ac4e598d0a8556cbfcd4a52ec |
| Robustness | CLEAN | U6/U7/F6 in `test_acmp_mbx.cpp`; `acmp_review_mutants.py:403`; both complete ACMP arms and focused fault logs | R531-6 | d8060d87f892239ac4e598d0a8556cbfcd4a52ec |
| Tests | CLEAN | `ctrl_arms.py:44,57`; complete ctrl suite; four focused defects; all three campaign slices; coverage ratchet/exclusions | R531-6 | d8060d87f892239ac4e598d0a8556cbfcd4a52ec |
| Docs | CLEAN | `MAILBOX_SPLIT.md:655,692,709`; ctrl README:107,123,226; current issue evidence; public historical residue | R531-6 | d8060d87f892239ac4e598d0a8556cbfcd4a52ec |

Short code paths in the ledger are under `sw/firmware/ctrl/` and its `test/`, `app/`, `acmp/` or `maap/` directory as qualified above. Clean coverage is for the assigned delta at this exact head, preserving settled baseline findings by byte identity. It does not claim a new full HDL, standards-PDF or release qualification campaign.

**Real limits and pending manager duties**

Physical calibration was NOT RUN. Field skips and the skipped Physical gPTP context are not hardware proof. A4 access cost, full wire round-trip margin, final resource placement, all-stream/counter/audio bench acceptance and the default-flip obligations remain open. MAAP allocation is still not connected to the talker's `source` port inside this app; three-module integration is tested on the host model, while the existing co-simulation covers ADP and ACMP. Those disclosed baseline limits are unchanged.

`hosted-snapshot.json` is a read-only observation attached to this head: firmware-unit and several other jobs had successful check conclusions; several exhaustive jobs/aggregates were still pending; Physical gPTP was skipped. It is not final hosted acceptance. The manager owns hosted and local-replica acceptance and the separate full source banks. The supplied source-bank pass does not validate a future current-dev merge candidate. The manager must build and gate that candidate at the merge turn against live dev, initially identified here as `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`, and reviewed source head `d8060d87`.

The manager must publish this report and its manifest-listed receipts, carry the retained residue/suggestions, refresh the PR's explicitly round-6 evidence with round-7 results, obtain the other independent current-head verdict, finish required hosted/local evidence, ensure no review is in flight, obtain explicit merge authorization, and perform candidate validation and post-merge containment. This review does not close multi-lane issue #665 or authorize a merge.

All probes used disposable copies under `scratch/`; no candidate source needed restoration. Final direct verification covers 1,186 superproject blobs, their modes/index, and the required registered submodules: protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 blobs), gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), and axis library `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). The worktree is clean. Only `REPORT.md` and manifest-listed files are publishable; `scratch/` is excluded.

R531-6 FINISHED
