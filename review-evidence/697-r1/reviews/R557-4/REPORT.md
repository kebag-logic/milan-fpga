[R557] NEGATIVE - exact head 625b001173fda5f6401af1dceaef8d8ab86f5ae9

One MINOR remains: the assembly comment scanner can still hide prohibited prose behind a double-quote character operand. R556-3-F1 is retained at its original severity. R556-3-F2 is resolved. All earlier verdict-bearing findings are resolved as scoped; none is worsened. One historical RESIDUE remains in the closed import PR body.

Reviewed tree: `ac1ad256022bde4758d180a1f938da81ed7cbed6`. Full comparison: `ae982af85ec97286bd35b39403926d8f0eaec81d..625b001173fda5f6401af1dceaef8d8ab86f5ae9`. The six-commit follow-up includes the two assigned Round 5 commits, `e5c9c84` and `625b0011`, after `3c350014`. The [review start](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6076735578), [Round 5 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076492549), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076714170) and [PR body snapshot](authorities/pr16-body.md) identify this head.

I read the session instructions, CONTRIBUTING, README and documentation, then reconstructed the issue acceptance and public scope decisions, linked requirements and interface contracts, and the full diff/history. I examined the implementation and executed independent checks before reading earlier review findings. The [independent verdict and five-lens ledger](receipts/independent-verdict.md) were written first. Public prior-review reconciliation followed. No private author material, management checkout, other reviewer workspace or current parallel review was read.

The [standalone assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112), [comment-reduction decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248), and [dual-target rule](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336) govern acceptance. Parent integration, consumer pins and byte-identical firmware images remain later work. The separate Linux development branch was not examined or modified.

**R557-4-F1 / R556-3-F1 retained | MINOR | Conformance, Robustness, Tests, Docs | OPEN**

Artifact: [scripts/check_comments.py:17](https://github.com/kebag-logic/tsn-c-stack/blob/625b001173fda5f6401af1dceaef8d8ab86f5ae9/scripts/check_comments.py#L17), with token masking at line 44. Related claims are [CODING_STANDARD.md:33](https://github.com/kebag-logic/tsn-c-stack/blob/625b001173fda5f6401af1dceaef8d8ab86f5ae9/docs/CODING_STANDARD.md#L33) and the comment-gate row in [VERIFICATION.md](https://github.com/kebag-logic/tsn-c-stack/blob/625b001173fda5f6401af1dceaef8d8ab86f5ae9/docs/VERIFICATION.md).

Authority: owner decision B permits only SPDX, requirement tags and short standard references in the gated source directories. Round 5 item 1 expressly requires assembly character constants and directive bodies to remain subject to that allowlist.

The assembly lexer omits single-quoted literals, but still recognizes a double quote following the assembler's character introducer as a string opener. The following valid assembly therefore hides the prose from the scanner:

```asm
.equ reviewer_quote, '" # narrative "
```

The assembler reads `'"` as character value 34, then treats the rest as a comment. The scanner masks `" # narrative "` as a string. The same problem occurs in an instruction operand and a `#define` replacement body:

```asm
li a0, '" # narrative "
#define VALUE '" # narrative "
```

Evidence: [portable full-gate reproduction](scripts/full_comment_bypass.py), [full receipt](receipts/full-comment-bypass-final.json), and [independent compiling probes](receipts/independent-comment-probes.json). Appending the `.equ` plant to `examples/rv32/start.S` in a disposable copy gives compilation rc 0 with RV32I/ILP32 and `-Wall -Wextra -Werror`. The complete `check_comments.py --selftest` also returns 0 and reports all 23 code files and mutation fragments passing. Its object is byte-identical to the clean `.equ reviewer_quote, 34` control. Both standalone instruction and macro-body examples compile and return no scanner errors.

The original R556-3 examples are fixed: unchanged [comment_probes.py](scripts/prior-unchanged/comment_probes.py) reports [gaps: 0](receipts/prior-comment-probes.log). All 60 current selftest controls behave as their table requests, including carriage-return, digit-separator, zero/false directive and legitimate SPDX/tracing controls. This new compiling form nevertheless leaves the assigned gate obligation incomplete. The shipped source comments themselves are clean.

Impact: prohibited prose can enter an assembly source or macro body while the mandatory gate reports success. This affects executable validation and its documentation claim; it is not wording-only RESIDUE. No production protocol regression is alleged.

Required outcome: recognize assembler character operands before applying double-quoted string masking, including operands inside `#define` bodies. Preserve genuine assembly strings. Add compiling negative controls for the double-quote character followed by prose, and positive controls for legitimate character constants, strings containing `#`, SPDX and tracing.

Verification: each demonstrated prose plant must compile but make the full gate return nonzero; clean source and legitimate controls must pass. Rerun the unchanged prior probes and the two required target jobs. Signed `+0` and `-0` expressions also appear in the exploratory receipt; they are not needed for this finding or treated as part of the required integer-literal family.

**Prior findings and adopted items at this exact head**

Sources: [R556-1](https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074692175), [R557-1](https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074712341), [R556-2](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075317932), [R557-2](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075281257), and [R556-3](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075697881). R557-3 produced no verdict. Original severities are retained.

| Prior ID | Severity | Disposition | Exact-head evidence |
|---|---|---|---|
| R556-3-F1 | MINOR | RETAINED | Original probes pass, but the compiling quote-character bypass above remains. |
| R556-3-F2 | MINOR | RESOLVED | Positive named-assertion literal inventory plus retained deny-list. [Unchanged probes](receipts/prior-needle-probes.log) refuse every default-output fragment. [13 independent ownership controls](receipts/needle-ownership-probes.json) pass, including the correct MAAP message accepted in its own test and rejected under another test. All 329 current killers pass the positive rule. |
| R556-2-F1; R557-2-F1 | MINOR each | RESOLVED | PORTING restores SRP start/NULL stop, admission/withdrawal and call timing, source-state flags, Talker Failed meaning, storage fields, preconditions and per-core counters. Compared against the deleted public-header contracts. [Gate](receipts/checks/check_port_contracts.log) refuses name removal and all 14 critical meaning removals. |
| R556-2-F2; R557-2-F2 | MINOR each | RESOLVED as originally demonstrated | Ordinary assembly prose, SPDX-block tails and spliced prose are refused by the [unchanged probes](receipts/prior-comment-probes.log) and current selftests. The remaining assembly lexical gap is retained above under R556-3-F1. |
| R556-2-F3 | MINOR | RESOLVED | `tests/test_maap.cpp:375` streams its own message; `maap-stall-unqueued` requires it. Whole default-message lines and fragments are refused. [Campaign XML](receipts/mutation-xml/maap-stall-unqueued/maap.xml) records the intended assertion message. |
| R556-1-F1 | MINOR | RESOLVED | The 14 export-introduced weak killers and inherited weak entries now have assertion messages. No inherited exceptions remain. Literal audit and fresh/reused XML regrading cover all 329 killers. |
| R556-1-F2; R557-1-F2 | MINOR each | RESOLVED | Dependency output under real compiler flags and undefined-object symbols enforce the boundary. [Both-compiler controls](receipts/checks/boundary.log) compile and refuse all ten outside/heap/OS forms; both allowed controls pass. |
| R556-1-F3 | MINOR | RESOLVED | Requirements and generated traceability render separate links per cited standard. Regeneration passes; [link audit](receipts/doc-links.json) finds one consistent IEEE 1722-2016 URL. |
| R557-1-F1 | MAJOR | RESOLVED | Reports are deleted before each execution and checked for completeness, registration, uniqueness and completed status. [Controls](receipts/checks/mutation-controls.log) reject stale/partial/mismatched/skipped/error reports; genuine catch followed by early exit ESCAPES and removes old XML. Fresh and reused campaigns both catch 311/311. |
| R557-1-F3 | MINOR | RESOLVED | [Registration controls](receipts/checks/registration-controls.log) compile and execute indented, multiline and wrapper declarations. Unknown requirements, missing plants and unsupported registration mismatches are refused. Inventory reconciles 108 declarations with 369 instances. |
| R557-1-F4 | MINOR | RESOLVED under owner decision | ADP-01, PORTING and DEV-08 state the inherited version/length/control-length limits and caller obligations. Four input controls and RV32 counterparts pass. Core behavior remains unchanged; correction stays in [issue 3](https://github.com/kebag-logic/tsn-c-stack/issues/3). |

| Prior residue or suggestion | Disposition and evidence |
|---|---|
| R556-3-RS1 (RESIDUE) | Resolved: PORTING names `NDEBUG` for ADP and MAAP. |
| R556-3-S1 (SUGGESTION) | Resolved: line 375 uses four spaces. |
| R556-3-S2 (SUGGESTION) | Adopted: critical phrases, including NULL stops listening, are checked beside contract names; 14 removal controls pass. |
| R556-3-S3 (SUGGESTION) | Resolved: IEEE 1722-2016 links consistently use the edition page. |
| R556-2-S1 (SUGGESTION) | Deferred by the manager: header blank runs remain. No verdict effect. |
| R556-2-S2 (SUGGESTION) | Adopted: unknown test selections record ERROR; old summaries are removed before baseline work. Alone/mixed unknown tests and failed-baseline controls pass. |
| R556-2-S3 (SUGGESTION) | Adopted: no Python `assert` gate decisions remain. [Optimized controls](receipts/optimized-gates.json) and the optimized reused campaign pass. |
| R556-2-S4 (SUGGESTION) | Adopted: both workflow jobs use the source-head ref; hosted job metadata confirms the exact head. |
| R556-2-S5 (SUGGESTION) | Assigned zero/false literal forms are now refused, including `#elif`, octal, hex, suffixes and digit separators. |
| R556-2-RS1, RS2, RS3 (RESIDUE) | Resolved: Unreleased layout, subset wording and historical hosted-run links in PR #16 are present. |
| R556-1-R1, R2, R4 (RESIDUE) | Resolved: COVERAGE links, edition links and the seven added-case provenance are present. |
| R556-1-R3 (RESIDUE) | Retained in the closed PR #1 body, as detailed below. |
| R556-1-S1, S2, S3 (SUGGESTION) | Adopted: action SHA pins, 26-pair import map and generated ratchet header are present. |
| R556-1-S4 (SUGGESTION) | Published confirmation present in REQUIREMENTS. Independent full-standard corroboration remains limited, as stated below. |

The unchanged needle probe assigns even its final MAAP message to the table's first, unrelated test. Its rejection is therefore expected under the new ownership rule; the independent positive control assigns that message to the proper MAAP test and passes.

**R556-1-R3 | RESIDUE | Docs | RETAINED**

Artifact: [closed PR #1 body snapshot](authorities/pr1-body.md). Authority: the original residue and the [manager's Round 2 disposition](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074721212). Impact: a stale historical sentence says hosted execution awaits branch publication. The existing execution evidence and this verdict do not change.

Exact fix: replace that sentence with: “Hosted runs [37885778682](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778682) (pull_request) and [37885778700](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778700) (push) pass all 16 gates at `b9b9c20`.” Verification: reread the body and confirm the obsolete sentence is absent. Retained under its original RESIDUE classification for the manager's checklist; it does not affect lens cleanliness.

**Executed evidence and acceptance**

| Area | Independent exact-head result |
|---|---|
| Full change and behavior preservation | [Seven production token streams](receipts/source-audit.json) equal main; core line counts are preserved. All 311 applied mutant programs retain their token streams. Round 5 changes 24 needles and no other plant or killer-mapping data. [All 22 CI core object variants](receipts/object-comparison.json), compiled at stable paths with `-g0 -frandom-seed=0`, are byte-identical between main and this head. |
| Linux | GCC and Clang each run seven binaries and 369 instances, with no skipped instances. Clang enables address/undefined-behavior sanitizers, leak detection and halt-on-error. [Counts](receipts/native-instance-counts.json), [GCC output](receipts/gcc-instances.log), [Clang output](receipts/clang-instances.log). |
| Coverage | [Raw receipt](receipts/checks/coverage.log): ADP 203/205 lines and 93/100 branches; ACMP 742/742 and 348/348; MAAP 209/209 and 140/140; wire 10/10 and 2/2. Five inherited exclusion rows remove two unreachable ADP statements and seven arcs, yielding 1164/1164 lines and 583/583 branches. Exact-exclusion controls pass. |
| Mutation | Fresh and reused campaigns: 311 CAUGHT, zero ESCAPED/ERROR. Independent XML regrading matches 329/329 killer entries in each. [Fresh results](receipts/mutation-results-fresh.json), [fresh regrade](receipts/prior-regrade.log), [reused results](receipts/mutation-results-reused.json), [reused regrade](receipts/mutation-reused-regrade.log); reused per-plant XML is included. |
| RV32 | [Debug and Release](receipts/rv32-results.json) compile all cores using RV32I, ILP32, freestanding C11 and restricted headers. Both whole-archive links have zero unresolved final symbols, correct ELF32 machine/ABI, and passing ADP/ACMP/MAAP smoke checks. Startup, stack/BSS layout, the memory subset, integer-helper allowance and simulator completion path were inspected. |
| Boundary, analysis and controls | [Gate summary](receipts/checks/summary.json): all executed entries return zero. Compiler-based boundary controls, static analysis with registered suppressions, report/registration controls, licence and privacy scans pass. The independent comment bypass is additional evidence outside those passing selftests. |
| Documents | Compared removed header contracts with PORTING/ARCHITECTURE; checked requirement/deviation scope, clause links, generated matrices, example and validation instructions. [400 relative links and 251 line links](receipts/doc-links.json) pass; generated test links point to declarations. Three diagrams render. Required NDEBUG wording, spaces, critical phrases and IEEE link form are present. |
| Hosted evidence | [PR run 37900893378](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37900893378) and [push run 37900889048](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37900889048) both pass quality and bare-metal at the exact head. Every recorded step executed and succeeded; none was skipped. [PR checks](authorities/hosted-checks.json), [PR steps](authorities/hosted-jobs-37900893378.json), [push steps](authorities/hosted-jobs-37900889048.json). The downloaded PR artifacts contain 21 zero-return Linux gates, 311 caught plants, and two successful RV32 configurations with empty unresolved-symbol lists. [Artifact summary](receipts/hosted-artifact-summary.json). This is inspection of hosted evidence, not manager acceptance. |

The [specified public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/2ae0b85299a979413a5ba4b7fe3e3de175967a19/review-evidence/697-r1) contains original-import author material, not Round 5 source-bank receipts. Its [manifest audit](receipts/published-round1-audit.json) verifies the eight published files. Exact-head evidence here is the public Round 5 author statement, the inspected hosted artifacts and this review's independent execution. No manager source bank ran at this head and none is claimed or inferred. The PR snapshot contains no submitted reviews or inline review comments; the earlier findings are the public issue comments reconciled above.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen scope/decisions; requirements/deviations; unchanged source and mutant programs; relocated interface contracts; compiler boundary; remaining comment-allowlist breach F1 | R557-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| RTL | CLEAN | Full delta contains no RTL; C core/header identity; 22 core objects; CMake targets; RV32 startup/link/runtime and minimal port; dependency/symbol/ABI checks and both smoke runs | R557-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| Robustness | UNCLEAN | Re-entry/backpressure/wrap/input/capacity suites; sanitizers; fresh-report and unknown-test controls; assertion ownership; compiling assembly scanner bypass F1 | R557-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| Tests | UNCLEAN | 369 instances per compiler; 311 plants/329 killers; coverage/exclusion controls; original and new gate probes; hosted executed steps; missing refusal exposed by F1 | R557-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| Docs | UNCLEAN | README/personas; PORTING/ARCHITECTURE; requirements/traceability; verification/coding claims; import/coverage/analysis registers; PR claims and public receipts; F1 | R557-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |

**Limits and pending manager duties**

The [IEEE 1722.1 edition page](https://standards.ieee.org/ieee/1722.1/6670/) and [IEEE 1722 edition page](https://standards.ieee.org/ieee/1722/5979/) identify the cited standards; they do not supply the licensed full texts. The [Milan landing page](https://avnu.org/resource/milan-specification/) currently offers v1.3 through a form. Full v1.2 clause text and later amendments were not independently re-audited. This review checks the frozen requirements, imported behavior, documented limits and validation claims; it does not establish complete device certification. The original full-history export was not rerun.

RV32 execution is simulator evidence. Physical calibration NOT RUN. Field skips are not hardware proof. Linux coverage excludes test/example code and debug assertion instructions; RV32 smoke coverage is not the Linux denominator. No RTL simulator, synthesis, full parent/PP/gPTP/builder bank, hardware or hosted-replica run was performed.

The manager must resolve the MINOR, obtain both independent positive reviews, own hosted/replica acceptance, and carry the retained residue. At merge, the manager validates the final current-dev candidate with builder and native banks and publishes the receipts. Source base is `ae982af85ec97286bd35b39403926d8f0eaec81d`; the supplied live dev is `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Those future candidate checks are distinct from this source review. Consumer integration, exact pins and linked firmware-image identity remain later acceptance. Repository publication remains an owner action.

All commands were foreground operations; independent work used an awaited supervisor and separate logs. Disposable trees stayed beneath the packet's scratch directory. No source fixes, commits, pushes, GitHub writes, shared installations or other-checkout edits occurred. [Final integrity](receipts/checkout-final.json) verifies all 66 tracked blob bytes and modes, the index, head and tree. Base and head contain zero gitlinks; no lwSRP or consumer pin changed.

[Replay instructions](REPLAY.md) identify portable scripts and expected results. Publish REPORT.md and only the files listed in MANIFEST.sha256. Scratch is excluded. Published receipts preserve execution results while replacing host-specific locations with neutral placeholders; [the redaction record](receipts/location-redactions.json) records original and published hashes.

R557-4 FINISHED
