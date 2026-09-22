[R221] POSITIVE - exact head 1496558d82cf35fc98dda0e781b2a1be643c301a

R221-r2 independently re-reviewed issue #478 / PR #512 at tree `e8d797554a935c5514e25be9e1dda119f4f8c999`. F1's source defect is resolved at this head, with its original MAJOR severity and all four original lens assignments preserved. All five lenses are freshly covered clean in this round. This is a source-review verdict, not a claim that CI or the merge bar is complete.

The review reconstructed the contract from AGENTS/CONTRIBUTING, docs/README, [issue #478](https://github.com/kebag-logic/milan-fpga/issues/478), its [readiness decision](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770832729) and [assignment](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770949009), REQUIREMENTS, the cited Milan/IEEE clauses, pinned processor authorities, parent architecture/interfaces, PR history/diff, and executable evidence. The [public review start](https://github.com/kebag-logic/milan-fpga/pull/512#issuecomment-5778185837) identifies this corrected-head round. No private author reasoning, another reviewer's report, or local author-lane material was used.

The original [R221-1 finding](https://github.com/kebag-logic/milan-fpga/pull/512#issuecomment-5776222482) applied to `d81a302760b84f32d2aa019643f57682bb6e052c`, tree `4903a00f30752bc86a99e9bf112ff5ad01827c5d`. Its prior positive RTL result is not imported into this ledger. The four previously unclean lenses were applied first; RTL was then freshly checked against the current artifacts.

[R221] MAJOR Docs, Conformance, Robustness, Tests - `docs/ENDSTATION_BUILDER.md:963`, `REQUIREMENTS.md:222`, `.github/workflows/docs.yml:52`, `.github/workflows/docs.yml:444` - F1 RESOLVED at `1496558d82cf35fc98dda0e781b2a1be643c301a`: processor reference works before submodule initialization.

Requirement/evidence: REQ-VER-04 requires green documentation gates. The Git job runs `docs_check.py` before initializing submodules, and the archive job removes Git metadata without initializing them. The original relative link required an absent processor file. The correction changes only that URL to the [pinned PP document](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/424c688fa2205b934a7689a58f2aa766420f2326/docs/architecture/07_memory_maps.md#31-descriptor-tree). The URL preserves `#31-descriptor-tree`; the target has heading `3.1 Descriptor tree` and rule L10. Public target bytes equal the pinned local Git blob. `scripts/docs_check.py` and `.github/workflows/docs.yml` are unchanged; no checker weakening or added initialization conceals the failure.

Impact of the original defect: both required documentation configurations failed and the reference depended on unavailable local files. It did not change emitted rates or demonstrate an RTL failure.

Required outcome: retain the existing pinned authority and L10 meaning while removing the dependency on local submodule population. That source outcome is satisfied. The original verification's required hosted documentation results remain a separate manager merge obligation; this report does not infer them from local probes.

Verification: [reproducer](docs_probe.py), [results](docs-final-controls/results.json), [target identity](docs-final-controls/link-target.json), and individual logs establish:

| Population, always without initialized submodules | Git exit | No-Git exit |
|---|---:|---:|
| Corrected exact head, pristine | 0 | 0 |
| Corrected exact head, only old local URL restored in scratch | 1 | 1 |
| Original `d81a3027` head, pristine failure control | 1 | 1 |

Both corrected populations report zero documentation findings; feature-status checks also pass. Restoring the old URL produces the specific broken-link finding at line 963 using the current checker. The no-Git run explicitly skips inventory parity, which requires Git; that skip is not counted as an executed check. F1 is closed as a source-review finding under all four original lenses, without reducing its severity or dropping an attribution.

[R221] PASS Conformance - `sw/builder/endstation_builder.py:1197`, `sw/builder/endstation_builder.py:3788`, `sw/builder/endstation_builder.py:3801`, pinned `protocol-processor/docs/architecture/07_memory_maps.md:92`, `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1330` - frozen acceptance and the producer/consumer bound agree.

L10 requires offset 144 and at most eight complete rate words. The actual microprogram sets `SSR_LIST_OFF = 144`, `SSR_WALK_MAX = 8`, walks pairs at indices 0/2/4/6, compares both 32-bit entries with count guards, and branches to refusal after the eighth. The bound is an integration restriction: IEEE 1722.1-2021 section 7.2.3/Table 7-5 allows up to 91 entries, while Milan v1.2 section 5.3.3.3 requires truthful supported-rate reporting and current-rate membership. Those standards were read directly; [file identities](standards-identities.json) retain their hashes.

The sole production maximum is named beside `BASE_RATE_HZ` and cites L10. Integer conversion precedes count and duplicate checks. A distinct ninth entry receives the walk/L10 refusal; normalized duplicates receive the duplicate refusal. Current-rate membership, omitted-list defaults, and order remain intact. There is no sorting, truncation, donor edit, or shipping-rate change. [Focused receipts](focused-receipts/1496558d/results.json) include all gate-36a functions plus 49 independent checks covering every current-rate position at lengths one through eight, all nine positions in distinct nine-entry lists, and four normalized-duplicate forms.

[R221] PASS Robustness - `sw/builder/endstation_builder.py:3801`, `sw/builder/test_builder.py:23524`, `sw/builder/test_builder.py:23590`, `.github/workflows/docs.yml:444` - count, duplicate, membership, declaration-drift and checkout-population failures are independently detected.

The empty list and missing-current cases refuse by their stated causes. Gate 36a's positive eight-entry fixture is unsorted and places the current rate last; its ninth entry is distinct, so duplicate rejection cannot mask the count check. If a list violates both count and uniqueness, the count check runs first. In isolated exported sources, seven independent loader mutations were caught: bounds nine/seven, missing count/duplicate/membership checks, reversed order, and wrong omitted-list default. Documentation robustness is established by the Git/no-Git probes above.

[R221] PASS Tests - `sw/builder/test_builder.py:23524`, `sw/builder/test_builder.py:23590`, `sw/builder/test_builder.py:23957`, `tb/verilator/pp_shadow/sim_main.cpp:827` - positive, negative, mutation and dispatch controls discriminate the specified defects.

The literal eight-entry test oracle does not import the production maximum. The pristine `AU_RATES_C` comparison and all five committed synthetic controls pass. R221 additionally edited the actual declaration in scratch: value, order, declared length, missing initializer element, commented-out declaration, and duplicate declaration each failed the real gate. The file was restored and the pristine gate passed again. Comment removal, a single-declaration requirement, decimal literal parsing, ordered value equality and declared-length equality are exercised. This verifies the deliberate literal representation currently used; it is not a general C++ parser claim.

All three new gates execute in the exact main dispatch loop when unrelated gates are explicitly stubbed; an independent assertion sentinel in each propagates out. This is focused dispatch evidence, not a full builder rerun. The manager's unmodified full builder log separately records all three executing. Gate 1 builds all five configurations; gate 32 passes its 109-key documentation comparison and planted missing/stale-row controls. Its census still discloses 17 untaken loader arms, which are not claimed as exhaustive coverage.

The positive eight-entry result is specifically a `_load_clocking` result. Independently passing that same list toward image generation produces `unsupported sampling rates`, matching `avdecc/aem_specs.py:219` and its existing 48/96/192 kHz restriction. Gate 36a checks shipping image rate fields; historical whole-image equality is established by this review's separate comparison, not by gate 36a alone.

[R221] PASS Docs - `docs/ENDSTATION_BUILDER.md:963`, `scripts/docs_check.py:642`, `sw/builder/test_builder.py:22904`, `docs/reference/SUBMODULES.md:25` - schema wording, defaults/order/refusals, pinned authority, link availability, and public evidence accurately describe this delivery.

The row identifies the eight-entry processor walk, duplicate refusal and hand-built-array comparison. It does not claim eight arbitrary rates produce a supported shipping image. The single URL correction preserves the fragment and pin. The public task contract keeps [PP89](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/89) generic packer enforcement and [#509](https://github.com/kebag-logic/milan-fpga/issues/509) descriptor ownership separate. Optional S1/S2 remain routed to existing [#495](https://github.com/kebag-logic/milan-fpga/issues/495), are not adopted here, and create no new acceptance requirement or open R221 finding.

[R221] PASS RTL - `avdecc/aem_descriptors.py:240`, `hdl/milan/KL_pp_shadow.sv:431`, `tb/verilator/pp_shadow/sim_main.cpp:827`, `tb/verilator/pp_shadow/sim_main.cpp:876`, pinned `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1377` - current producer layout, descriptor-memory boundary, hand-built integration image and eight-entry consumer walk agree.

The packer writes current rate at 136, offset/count at 140/142, and 32-bit rates from 144. The hand-built bench uses its unchanged three literal rates in the emitted descriptor. `docs/overview/ARCHITECTURE.md:59` and `docs/integration/INTEGRATION_GUIDE.md:78` agree with the unchanged descriptor-memory interface. The current three-file issue diff changes no RTL, ports, clocks/resets, CDC, FSM, backpressure, timeout, firmware, generator implementation, shipping configuration or gitlink. New cycle-level stress tests are inapplicable to this delta; this is not a new whole-product RTL certification.

R221 independently decoded every packed image's AEMI header, total length, checksum, AUDIO_UNIT length, current rate, offset/count, and ordered rate words. All five config hashes and complete packed binaries match independently generated outputs at both original pre-change base `b17580b91deb11f3441dfc5d7f9fafe539d929b8` and integrated base `88e9276b2a220c716f64a843f7e1eb8f9265e896`. [Comparison and hashes](focused-receipts/comparison.json):

| Configuration | Advertised rates, Hz | AUDIO_UNIT bytes | Complete image bytes |
|---|---|---:|---:|
| arty_current | 48000, 96000, 192000 | 156 | 5792 |
| arty_4x4 | 48000 | 148 | 10112 |
| arty_8ch | 48000 | 148 | 15360 |
| ax7101_8x8 | 48000 | 148 | 18288 |
| ax7101_1x1_tdm8 | 48000 | 148 | 7352 |

Every list starts at 144 and every current rate is 48000. This proves equality of the configurations and complete packed `aem_desc.bin` outputs, not every generated artifact, bitstream or deployed hardware behavior. [Diff identity](diff-identity.json) verifies all four gitlinks unchanged across original base, author, first-review, correction, integrated base and current head. The PP pin remains `424c688fa2205b934a7689a58f2aa766420f2326`. Builder/test blobs are unchanged from author `099e191`; the later source correction replaces only the documentation URL. Base integration changes are identified separately in the receipt.

Evidence identity and limits: R221 downloaded and verified 61 Git blobs and 60 applicable published manifest hashes from the immutable [3811227 archive](https://github.com/kebag-logic/milan-fpga/tree/3811227ee1af4ed96493528f1af17e852e2b7176/review-evidence/478-r1). Only selected factual author/manager evidence was downloaded; other reviewer reports were excluded. Original private, pre-neutralization hashes are retained assertions, not independently verified private files. [Verification receipt](evidence-verification.json).

The [manager completion comment](https://github.com/kebag-logic/milan-fpga/pull/512#issuecomment-5777275128), exact command/result/completion records, logs and both clone-integrity receipts consistently identify current head `1496558d`, tree `e8d79755`, and base `88e9276b`. They record 40 static/builder commands and five full native groups exiting zero: parent sweep, Yosys, pinned PP suites, pinned gPTP suites and behave. The inspected logs record 55/55 parent suites, 2,118,264 checks, 14,903 PP checks, 371 parent `pp_shadow` checks and 316 behave scenarios. These are manager executions independently inspected by R221, not R221 reruns. Native Verilator is **5.052**; workflow-pinned **5.050** is a separate execution identity. Four field-campaign skips contribute zero checks. Builder calibration gate 11 remains **NOT RUN**, with no physical evidence inferred.

Original author rate receipts retain `099e191137dd2797407fb8345a452bcc7a965608` attribution, with their baseline at `b17580b9`; their hashes match this review's independent outputs. Original R221-1 and `d81a3027` failure controls retain their original head identity. No old positive is inferred for the corrected head or any later candidate.

Reviewer-owned final ledger:

| Lens | Covering round | Exact head | Result |
|---|---|---|---|
| Conformance | R221-r2, fresh | `1496558d82cf35fc98dda0e781b2a1be643c301a` | CLEAN; F1 resolved |
| RTL | R221-r2, fresh | `1496558d82cf35fc98dda0e781b2a1be643c301a` | CLEAN |
| Robustness | R221-r2, fresh | `1496558d82cf35fc98dda0e781b2a1be643c301a` | CLEAN; F1 resolved |
| Tests | R221-r2, fresh | `1496558d82cf35fc98dda0e781b2a1be643c301a` | CLEAN; F1 resolved |
| Docs | R221-r2, fresh | `1496558d82cf35fc98dda0e781b2a1be643c301a` | CLEAN; F1 resolved |

Open R221 findings: none. No MINOR, MAJOR or BLOCKER remains open, and no new SUGGESTION is filed. The optional residue above is not a deferred defect found by this round.

Outstanding manager duties: complete and measure the trusted act replica and all required hosted contexts, including corrected-head documentation checks. The [actual replica start](https://github.com/kebag-logic/milan-fpga/pull/512#issuecomment-5778014438) preceded hosted inspection, but a start is not a pass. R221 deferred direct hosted inspection and called no Actions/run/check/status/log/dashboard endpoint. Obtain the independent external corrected-head verdict, reviewer-owned aggregate coverage, and completion of every review round before merge.

The manager's [later-base notice](https://github.com/kebag-logic/milan-fpga/pull/512#issuecomment-5778076390) identifies dev `52711029f374650dc93830d5ea28e81cb5c8f410` and candidate `72e16c6172db723734317b105cff6c6e9168571a`, tree `93be2b5788c4b79e88bfe22fbaf985686bbdc8f2`, as separately under validation. This source-head verdict and the completed `88e9276b`-base evidence do not certify that candidate. Finish its mandatory bar, re-evaluate any further dev movement, obtain explicit maintainer merge authorization, verify actual merge/result containment and post-merge checks, and only then close the issue/move it to Done. CI completion, current-base and post-merge duties remain outstanding here until independently measured by the manager.

Final integrity: [initial](integrity-initial.json) and [final](integrity-final.json) snapshots are [identical](integrity-comparison.json): 851 parent tracked files, 222 PP files, 103 gPTP files and 214 verilog-axis files match their committed blobs, kinds and executable modes; indexes match trees with no hidden index flags; populated submodules match their gitlinks. Status remains clean. Optional unused `external` remains uninitialized. All executable controls ran in isolated scratch, with no full native/RTL/Yosys/processor/builder-suite rerun; no compilation parallelism was used, and archive downloads used four jobs. No source fix, commit, push, public comment/metadata change, merge, other agent, author contact, hardware, install, privilege, Docker/act execution or candidate `act_ci` host execution occurred. [Reproduction instructions](RECEIPTS.md). The manager publishes faithfully with path neutralization; R221 does not self-publish.

R221-r2 FINISHED
