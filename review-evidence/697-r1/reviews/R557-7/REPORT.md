[R557] NEGATIVE - exact head 68070cb5723682586c07a6de80a49886732b5dc2

One new MINOR remains: the mutation build fails with the pinned dependency installed in a non-default prefix. The five assigned Round 8 fixes and the prior assertion-alias finding are resolved as specified. Both exact-head hosted jobs are green; F1 concerns a different, reproducible dependency configuration.

Tree: `f42024aec0fddde6cf6d552e85e50109a8e6cbb4`. Full comparison: `ae982af85ec97286bd35b39403926d8f0eaec81d..68070cb5723682586c07a6de80a49886732b5dc2`. Focus: five commits after `6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5`, assignment round 8, review R557-7. [History](receipts/round8-history.txt), [delta summary](receipts/round8-diff-stat.txt), [review start](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6079422627).

Scope follows the [issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/697), [standalone assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112), [comment reduction](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248), [dual-target rule](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336), [six-rule contract](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6078263180), and [Round 8 decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079166369). The gate is judged against the honest-contributor threat model and listed refusals. No new obfuscated payload was authored. F1 uses the shipped tests and pinned upstream dependency unchanged.

**R557-7-F1 — MINOR — Robustness, Tests, Docs — OPEN**

Artifacts: [scripts/mutation.py:111](https://github.com/kebag-logic/tsn-c-stack/blob/68070cb5723682586c07a6de80a49886732b5dc2/scripts/mutation.py#L111), C++ compile commands at lines 126, 137 and 185; [dependency_selftest.py:37](https://github.com/kebag-logic/tsn-c-stack/blob/68070cb5723682586c07a6de80a49886732b5dc2/scripts/dependency_selftest.py#L37); [VERIFICATION.md:29](https://github.com/kebag-logic/tsn-c-stack/blob/68070cb5723682586c07a6de80a49886732b5dc2/docs/VERIFICATION.md#L29). The triggering existing assertion is `tests/test_adp.cpp:116`.

Authority: Round 8 item 2 requires using the checked package flags, with a compiling control. VERIFICATION says its dependency control compiles and catches a header plant without ambient include/library paths, and its mutation command catches all 311 plants.

Reproduction: install the documented GoogleTest/GMock commit `f8d7d77c06936315286eb55f8de22cd23c188571` (1.14.0) in an isolated prefix. Select its CMake config and pkg-config files; clear ambient include/library paths. Its unmodified `.pc` files supply `-I<prefix>/include` and `-L<prefix>/lib`. Version checks pass. A fresh exact-head CMake build and all seven test binaries pass against that installation, classifying its headers with `-isystem`. The mutation command and dependency selftest both fail during baseline compilation: `gtest/gtest.h:1379` compares unsigned and signed values, and `-Werror=sign-compare` makes that third-party warning fatal. Direct compilation of the unchanged ADP test reproduces this with GCC 16.2 and Clang 23.1.

Evidence: [flags](receipts/package-prefix/flags.txt), [mutation failure](receipts/package-prefix/mutation.log), [dependency-control failure](receipts/package-prefix/dependencies.log), [GCC diagnostic](receipts/package-prefix/g++-direct.log), [Clang diagnostic](receipts/package-prefix/clang++-direct.log), [passing CMake command](receipts/package-prefix/fresh-cmake-command.json), [CMake tests](receipts/package-prefix/cmake-test.log). A diagnostic control changes only the dependency include classification from `-I` to `-isystem`; the baseline compiles and the selected header plant is CAUGHT. [Control output](receipts/package-prefix/control/system-header-control.log), [control result](receipts/package-prefix/control/results.json). This modified-metadata control is not a source-head pass claim.

Impact: an honest contributor installing the pinned release alongside a newer system release can build/test through CMake, but cannot execute the documented mutation campaign or dependency gate through normal package metadata. Failure occurs before mutation grading; no false catch or production behavior change is alleged. The hosted system installation of 1.14.0 does not expose this case.

Required outcome: handle dependency headers consistently with CMake while preserving project warnings and the checked compile/link flags. Add a control with a real pinned installation in a non-default prefix and no ambient paths. Do not globally disable project signedness warnings.

Verification: the isolated configuration must build and pass the suite; the dependency control must catch its header plant; a fresh campaign must catch 311 named plants and all 329 required streamed-message killers. Keep the wrong-version refusal and both targets green. [Portable reproducer](scripts/probe_package_prefix.py), [dependency preparation](scripts/setup_sdk.py).

The initial local dependency-selftest pass is not credited for this case: the local package resolver suppressed flags already supplied by ambient variables, which the selftest subsequently removed. The explicit-path rerun exposes F1. The initial full mutation campaign itself retained the selected 1.14.0 ambient paths and remains valid. Its successful result and the separately failing isolated campaign are both preserved.

**Round 8 dispositions**

| Prior ID | Severity; attributable lenses | Disposition | Exact-head evidence |
|---|---|---|---|
| R556-6-F1 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED | `check_comments.py:70,89` refuses `VERSION`, backslashes and hashes. Linked controls pass fatal linking and fail policy. Both unchanged linker probes are CAUGHT. |
| R556-6-F2 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED | `check_comments.py:82` refuses `.include`/`.incbin`. Both assembly-include probes build/link/run and are CAUGHT; the `.incbin` control also compiles, links and is refused. |
| R556-6-F3 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED | `check_comments.py:65` refuses direct `.c`/`.cpp` includes. Quoted/angled controls compile and are refused. The unchanged C-file-in-C++ probe is CAUGHT. |
| R556-6-F4; R557-6-F1 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED | `assertion_forms.py:32` derives 81 refused names, including GTEST aliases, from pinned preprocessor output; line 20 refuses token pasting. `--check` regenerates names and 14 templates. Alias, failure and pasted controls compile, execute failing assertions and are refused. Both internal rows are CAUGHT; external aliases are refused while the allowed form passes. |
| R556-6-F5 | MINOR; Robustness, Tests, Docs | RESOLVED as originally specified; new F1 concerns the replacement build path | CMake uses `EXACT CONFIG REQUIRED`; an actual 1.18.0-only configure fails. Mutation commands use the checked flags. F1 is distinct from the former unversioned fallback and ignored flags. |
| R556-6-S1 | SUGGESTION; Robustness | RESOLVED | `.end` control and unchanged trailer probe compile and are refused. |
| R557-6-RS1 | RESIDUE; Docs | RESOLVED | The current PR body removes the dangling “build commands above” direction and links the verification guide. |

Receipts: [54 comment-control labels](receipts/local/comments.log), [assertion controls](receipts/local/assertion-templates.log), [wrong-version refusal](receipts/native-wrong-version.log), [eleven internal rows](receipts/prior/r5566/probes.json), [external controls](receipts/prior/r5576-controls/results.json), [PR body](receipts/pr-body.md). Every internal row builds successfully before a gate catches it.

**Earlier public findings**

[Provenance](receipts/prior-script-sources.json) pins the replayed scripts. [Results](receipts/prior/results.json) preserve their exit statuses. Historical scripts asserting that a bypass exists return nonzero after closure; their detailed rows determine the disposition.

| Prior items | Disposition | Verification at this head |
|---|---|---|
| R556-2-F1; R557-2-F1, lost contracts | RESOLVED | PORTING contains null-stream stop/clear, admission withdrawal, source fields, failed feedback and counter tables. Contract selftests and production preservation pass. |
| R556-2-F2; R557-2-F2; R556-3-F1; R556-4-F1; R557-4-F1 | RESOLVED | Unchanged comment probes report zero gaps. SPDX block/splice and assembly controls compile and are refused. R556-4 reports 0 gaps of 11; its exploratory C23 row still does not compile. |
| R556-2-F3; R556-3-F2; R556-4-F2; R557-5-F2 | RESOLVED | Eleven old needle controls are refused. 955 default fragments per killer yield zero accepted fragments. Specificity replay: 329 CAUGHT-BY-MESSAGE, zero SHARED/MISSING. |
| R556-5-F1/F2/F3; R557-5-F1 | RESOLVED | Byte/suffix/header/assembly refusals hold. Tree rows A/B/C refuse comments; B also fails fatal linking. Macro-produced prose and tracing are refused. |
| R556-1-F1/F2/F3; R557-1-F1/F2/F3 | RESOLVED, no regression | Fresh named grading; stale/partial/skipped/mismatched reports; compiling boundary controls; executable registration and 17-requirement traceability. Genuine/crash/early-exit/unrelated-needle replays retain expected outcomes. |
| R557-1-F4, ADP limits | RESOLVED under scope decision | Unchanged probe accepts the three documented inputs, matching DEV-08 and hosted controls. Its nonzero exit reports inherited behavior. Correction remains issue 3. |
| R556-2-S2/S3/S4/S5; R556-3-S1/S2/S3; R556-4-S1; R556-5-S1/S2 | RESOLVED/adopted | Unknown-killer/report controls, explicit errors, common checkout ref, conditional policy, contract phrases, standard links, RV32 timeout/retries and per-arm hosted XML remain present. |
| R556-2-RS1/RS2/RS3; R556-3-RS1; R556-5-RS1 | RESOLVED | Current CHANGELOG, VERIFICATION, PORTING and rewritten PR body retain the corrections. |
| R556-1-R1/R2/R4; R556-1-S1/S2/S3 | RESOLVED/adopted | Linked coverage/editions, import inventory/commit map, pinned actions and ratchet provenance remain present. |
| R556-1-S4 | Retained published clause-check confirmation | REQUIREMENTS records the checks; full normative text was not independently re-audited in this delta. |

**Carried non-blocking items**

- **R556-1-R3 — RESIDUE — Docs — RETAINED.** [Closed PR #1 body](receipts/closed-pr1-body.md) still says “Hosted execution awaits publication of this branch.” This retains its historical wording-only classification; measurements and acceptance are unchanged. Exact fix: “Hosted runs [37885778682](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778682) (pull_request) and [37885778700](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778700) (push) pass all 16 gates at `b9b9c20`.” Verify replacement of the stale sentence. The manager carries it.
- **R556-6-S2 — SUGGESTION — Robustness — RETAINED.** `check_comments.py:120` scans four declared directories. External-directory headers and directory symlinks remain outside the stated contract; the PR body acknowledges this and no such hiding construction is shipped. Optional outcome: extend the scan from build dependencies and verify compiling controls. No lens is unclean from this suggestion.
- **R556-2-S1 — SUGGESTION — Docs — DEFERRED by the manager.** Long blank runs remain in the public headers after comment reduction. Optional cleanup must retain token/object identity and regenerate line links. No code or contract defect is alleged.

**Executed evidence**

| Area | Result |
|---|---|
| Linux | GCC coverage and Clang address/undefined-behavior sanitizer suites pass seven binaries, 369 registered instances. Leak detection/halt-on-error enabled. [GCC](receipts/local/gcc-test.log), [Clang](receipts/local/clang-test.log), [registration](receipts/local/traceability.log). The isolated-prefix exceptions are F1. |
| Coverage | Adjusted 1164/1164 lines and 583/583 branches. Raw ADP 203/205 and 93/100, with unchanged exact exclusions. [Receipt](receipts/local/coverage.log). |
| Mutation | Fresh selected-version run catches 311/311 names; independent per-arm regrade confirms 329/329 streamed-message killers. [Audit](receipts/mutation-audit.json), [results/raw XML](receipts/local/mutations/results.json). The separate non-ambient run fails baseline compilation and is not counted as passing. |
| Controls | 54 comment-control labels pass expected outcomes; 14 templates and 81 refused names regenerate; 38 conditional region sides compile in 22 files. Boundary, port, registration, report, coverage, licence and privacy controls pass. [Gates](receipts/local/gates.json), [comments](receipts/local/comments.log), [templates](receipts/local/assertion-templates.log). Initial dependency-control qualification is stated under F1. |
| Static/docs | Static analysis passes with documented suppressions; three graphs render. 427 relative links, including 251 line links, have valid targets. [Analysis](receipts/local/static-analysis.log), [graphs](receipts/local/graphs.log), [links](receipts/document-links.json). |
| RV32 | Debug/Release compile all cores with RV32I/ILP32, freestanding flags and restricted headers. Whole-archive links use fatal warnings and have no unresolved symbols; both smoke runs pass. [Results](receipts/local/rv32/results.json), [log](receipts/local/rv32.log). Simulator evidence only. |
| Preservation | All 25 production/test/port/data files retain bytes across Round 8. Seven production token streams equal the source base. All 22 core object pairs equal the pre-reduction commit with CI flags plus `-g0 -frandom-seed=0`. [Comparison](receipts/preservation.json). |
| Hosted | [PR run 37920179036](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37920179036) and [push run 37920173994](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37920173994): quality/bare-metal SUCCESS; every step executed, none skipped. Each quality artifact has 24 gates at rc 0. Independent regrades confirm 311 plants/329 killers each. [Checks](receipts/hosted-checks.txt), [audit](receipts/hosted-audit.json), [PR regrade](receipts/hosted-pr-mutation-audit.json), [push regrade](receipts/hosted-push-mutation-audit.json). |
| Original public packet | Eight manifest entries at `2ae0b85299a979413a5ba4b7fe3e3de175967a19` verify. This establishes original-import provenance, not current-head execution. [Audit](receipts/original-packet-audit.json). The [Round 8 author statement](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079409858), hosted source evidence and this review's execution are distinguished. |

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue decisions; six rules/threat model; requirements, deviations and port authorities; listed refusal implementations and compiling controls | R557-7 / assignment round 8 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| RTL | CLEAN | No RTL or stack gitlink change; production token identity; 22 object pairs; RV32 startup/linker/runtime/import allowlist/smoke; both hosted targets | R557-7 / assignment round 8 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| Robustness | UNCLEAN (F1) | Token/comment/conditional gates; generated vocabulary; report validation and streamed grading; CMake version refusal; non-ambient package-path reproduction | R557-7 / assignment round 8 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| Tests | UNCLEAN (F1) | Suites, coverage, 311-plant/329-killer regrades, 54 comment controls, assertion controls, unchanged probes, failing isolated-prefix campaign/control | R557-7 / assignment round 8 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| Docs | UNCLEAN (F1) | CONTRIBUTING, README, CODING_STANDARD, VERIFICATION, PORTING, IMPORT, REQUIREMENTS/TRACEABILITY/DEVIATIONS, CHANGELOG and PR body; claims/links/graphs | R557-7 / assignment round 8 | 68070cb5723682586c07a6de80a49886732b5dc2 |

**Limits and pending manager duties**

- No manager source bank ran at this head, and none is claimed or inferred. The manager validates the final current-dev merge candidate with builder/native banks at the merge turn and links receipts on the PR. Source base: `ae982af85ec97286bd35b39403926d8f0eaec81d`; live dev: `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
- Physical calibration NOT RUN. Field skips are not hardware proof. No RTL simulation, synthesis, parent/PP/gPTP/builder bank, hosted replica, container run or hardware test was performed. The separate Linux development branch was not examined or changed. Full normative text was not re-audited; Round 8 changes no protocol or clause claim.
- Local compilers differ from hosted versions. [Versions](receipts/versions.json) and [download hashes](receipts/sdk-downloads.json) identify the scoped environment. F1 is demonstrated on the recorded GCC/Clang versions; behavior on other versions is not inferred.
- Independent diff notes preceded reading prior findings. The public-comment extraction also exposed broader prior-report text before the final verdict and ledger. This did not meet the requested strict report-reading sequence; the manager should retain that procedural limitation. No private author material or private reviewer report files were used.
- Return F1 for correction and verify its controls plus required source gates. Obtain two independent positive reviews. Carry the historical residue. The manager owns hosted acceptance, final candidate execution, later consumer/submodule and firmware-image identity acceptance, and any visibility change.
- Exact-head tracked bytes, modes and index are verified; the stack has zero gitlinks at base and head. [Integrity](receipts/checkout-integrity.json). No source fixes, commits, pushes, GitHub writes, author contact or shared installs were performed.

Portable scripts and text receipts are enumerated in `MANIFEST.sha256`; only listed files and this report are publishable. Only location prefixes are replaced in receipts, as described in [receipt-format.json](receipts/receipt-format.json). Originals, dependencies, disposable trees and builds remain in unpublished `scratch/`. Coordinated commands were awaited in the foreground; the execution group stayed below its 12 GiB cap.

R557-7 FINISHED
