[R557] NEGATIVE - exact head 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5

One MINOR remains: the assertion-form gate accepts compiling GoogleTest macros outside the closed list. The five preceding-round findings are resolved at this head. Current production behavior, both required targets, all 311 plants and all 329 required killers pass the checks below. The finding does not invalidate those mutation grades.

Tree: `74f57eca0b0f93e6ed8681c9385635914c25701c`. Full PR base: `ae982af85ec97286bd35b39403926d8f0eaec81d`. Focused delta: `60c911b92825a720044e78bed540752c7dd0368e..6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5`. The actual history contains **nine commits**, matching REVIEW READY, rather than the six stated in the review request. [Public review start](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078602980).

Reconstruction followed the supplied contribution instructions, CONTRIBUTING and README/docs; [frozen issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/697) and public scope decisions; requirement and port authorities; cumulative diff and history; then published executable evidence. No repository AGENTS.md exists. The [independent verdict and five-lens ledger](receipts/independent-pass.md) were written before reading earlier finding bodies or reports. No other current-round report was used.

The [standalone assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112), [comment decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248), [dual-target decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336), [round-6 design](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076983832) and [round-7 closed contract](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6078263180) govern this review. FPGA consumer integration and byte-identical firmware images are later work. Branch `dev-linux` was outside scope.

**R557-6-F1 — MINOR — Conformance, Robustness, Tests, Docs — OPEN**

Artifact: [scripts/assertion_forms.py:11](https://github.com/kebag-logic/tsn-c-stack/blob/6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5/scripts/assertion_forms.py#L11), especially lines 15–16; [needle_audit.py:19](https://github.com/kebag-logic/tsn-c-stack/blob/6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5/scripts/needle_audit.py#L19). The scanner recognizes identifiers beginning `EXPECT_` or `ASSERT_` and five additional names. It does not recognize the pinned library’s `GTEST_ASSERT_LT` or `GTEST_FAIL` assertion macros, so neither is refused as an unlisted form.

A single added line in the existing `ExamplePort.DefersExpiryAndRetainsBlockedOutput` test demonstrates the bypass:

```cpp
GTEST_ASSERT_LT(1, 2);
```

In a disposable exact-head copy, the full comment gate, `needle_audit.py --selftest`, CMake configuration, compilation of `port_tests`, and execution of that test all return zero. No test declaration, existing assertion, needle or mutation mapping is removed. [Full-tree receipt](receipts/full-assertion-probe.json), [gate output](receipts/full-assertion-probe/needles.log), [test XML](receipts/full-assertion-probe/port.xml), [portable reproduction](scripts/full_assertion_probe.py).

Companion short controls `GTEST_ASSERT_LT(2, 1)` and `GTEST_FAIL()` compile with C++20, `-Wall -Wextra -Werror`, and pinned GoogleTest 1.14.0. Each executes a real failing assertion, yet `assertion_forms.errors()` returns no errors and the source inventory accepts the file. The allowed `EXPECT_TRUE` control passes the source gate; the unlisted `EXPECT_NEAR` control is refused. [Control receipt](receipts/independent-probes.log), [sources and execution XML](receipts/independent-probes/), [portable controls](scripts/independent_probes.py).

Authority: round 7 rule 6 permits only the fourteen named forms and says a gate refuses any other. [CODING_STANDARD.md:23–26](https://github.com/kebag-logic/tsn-c-stack/blob/6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5/docs/CODING_STANDARD.md#L23) makes the same enforcement claim; [VERIFICATION.md:75](https://github.com/kebag-logic/tsn-c-stack/blob/6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5/docs/VERIFICATION.md#L75) records the closed assertion subset. This directly bypasses a listed rule and contradicts a stated claim; it is not an extension requested outside the contract.

Impact: contributors can introduce assertion forms outside the documented subset without the mandatory source gate rejecting them. Their diagnostics are outside the generated fourteen-form list, and the message inventory silently omits them. This is an enforcement defect, not wording-only residue. No false runtime mutation catch is alleged: default-only text remains excluded from grading, and the current campaign is independently confirmed.

Required outcome: refuse these unlisted GoogleTest assertion spellings under the existing closed contract, with compiling regression controls, while preserving the allowed forms. Verification: both short failing controls must compile and then fail the source gate; the passing in-tree `GTEST_ASSERT_LT` addition must also fail that gate. Keep the positive control, `EXPECT_NEAR` refusal, template `--check`, all earlier probes, 311/311 named catches and both target jobs passing.

**Closed-contract examination**

Both quality guides enumerate all six rules and expressly avoid a broader text-classification claim. The template guide correctly limits generation to one failing instance per allowed form, without claiming every value-dependent diagnostic variation. The rule-6 enforcement promise is contradicted by F1; no broader semantic-text requirement was imposed.

| Rule | Artifact-specific examination and execution |
|---|---|
| Printable ASCII, tab, LF | `check_file()` reads bytes before decoding; `check_mode()` checks fragment characters. Compiling CR, CRLF, form-feed, vertical-tab, control-byte and non-ASCII controls are refused. Data exceptions still receive the byte check. |
| Closed suffixes | All four source directories are walked, including untracked files. Only six suffixes and the two exact data paths pass. Included `.inc` selftest and earlier full-tree row C compile but fail the gate. |
| Both header modes | Every `.h` and `.hpp`, including header mutation fragments, is lexed in C11 and C++20. Both header selftests compile in both languages; hidden-comment source/fragment controls fail and tracing passes. |
| Linker scripts | Single quotes fail policy. The quote control links without fatal warnings, then fails with fatal warnings. CMake applies `-Wl,--fatal-warnings` to the real RV32 whole-archive link. Earlier row B fails both gate and RV32 link. |
| Assembly | Directives, single quotes, conditionals, macros and repeats are refused. Every hash tail is checked; plain/spliced definitions and macro-produced prose/tracing controls are refused. Direct tracing passes. Earlier assembly bypasses are closed. |
| Assertion forms/templates | All fourteen failing forms are generated from GoogleTest/GMock 1.14.0; streams are removed and regeneration matches. Every generated default control and compiling `EXPECT_NEAR` control is refused. **F1** demonstrates unlisted assertion spellings accepted by the form scanner. |

[Local comment controls](receipts/local-linux/comments.log) record all **46** compiling controls reaching their expected result. [Template controls](receipts/local-linux/assertion-templates.log) confirm fourteen generated diagnostics and current `--check`. [Conditional matrix](receipts/local-linux/conditionals/results.json) covers 22 files and 38 non-guard sides, including nested-unreachable refusal. Guard placement, macro redefinition restrictions, raw-token parsing and streamed-message grading were inspected independently.

**Earlier public findings, explicitly reconciled at this head**

Original severities are preserved. Authorities are the [prior external findings](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078194538), [prior internal findings](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078253855) and their linked earlier public reports.

| ID | Severity | Disposition and exact-head evidence |
|---|---|---|
| R556-5-F1 | MINOR | **RESOLVED.** All three assembly control-character probes compile and are refused before lexing. `hidden_text_probe.py`: zero gaps; full-tree row A comment gate rc 1. |
| R556-5-F2 | MINOR | **RESOLVED.** Dual header lexing and header-fragment controls pass. The unchanged C++ digit-separator probe is refused. Linker quote row B gives comment rc 1 and fatal-link rc 1. |
| R556-5-F3 | MINOR | **RESOLVED.** Included `.inc` selftest and unchanged row C give comment rc 1 while the GCC suite builds and passes. |
| R557-5-F1 | MINOR | **RESOLVED.** Macro-created assembly prose and tracing are now refused because preprocessing directives are forbidden. Unchanged full-tree probe: comment rc 1; RV32 smoke still passes. Macro-produced conditional is refused too. |
| R557-5-F2 | MINOR | **RESOLVED for the reported form and required outcome.** `EXPECT_NEAR` is refused; its message is excluded from inventory. Pinned generation covers all fourteen allowed forms, and default-only runtime matching remains false. F1 above is a separate bypass of the newly required form gate. |
| R556-2-F1; R557-2-F1 | MINOR each | **RESOLVED.** Relocated SRP start/NULL stop, admission withdrawal/timing, source flags, Talker Failed meaning, public fields, preconditions and counters remain in PORTING. Name-removal and fourteen meaning-removal controls pass. |
| R556-2-F2; R557-2-F2; R556-3-F1; R556-4-F1; R557-4-F1 | MINOR each | **RESOLVED.** SPDX tails, splices, C/C++ token forms, conditional hiding and the assembly quote/macro/control-character forms are refused. Earlier comment probe suites report zero bypass gaps. |
| R556-2-F3; R556-3-F2; R556-4-F2 | MINOR each | **RESOLVED.** Specific MAAP message retained; original generic/default fragments refused. Unchanged specificity audit reports 329 CAUGHT-BY-MESSAGE, zero SHARED/MISSING. Runtime grading uses delimited streams only. |
| R557-1-F1 | MAJOR | **RESOLVED.** Fresh complete reports are required. Built-in stale/partial/early-exit controls pass. Unchanged early driver probe catches the genuine plant; unrelated-needle, crash and exit-zero plants escape, and stale XML is removed. |
| R556-1-F1 | MINOR | **RESOLVED.** Fourteen weak killers remain corrected; all 329 current killer entries are independently confirmed. |
| R556-1-F2; R557-1-F2 | MINOR each | **RESOLVED.** Compiler dependencies/object symbols enforce the boundary. Built-in and unchanged early include, heap and OS controls are refused. |
| R556-1-F3; R557-1-F3 | MINOR each | **RESOLVED.** Per-standard links remain separate; generated traceability and executable registration reconciliation pass. Indented/multiline/wrapper, unknown-ID and missing-plant controls pass. |
| R557-1-F4 | MINOR | **RESOLVED under the owner decision.** ADP-01, PORTING and DEV-08 preserve and disclose the inherited three malformed-input cases. Hosted and RV32 controls pass; correction remains issue 3. |

[Unchanged script provenance](receipts/prior-provenance.json), [replay results](receipts/prior-replay.json) and [raw replay receipts](receipts/prior/) preserve the evidence. This replay includes the named round-3/4 probes, round-5 hidden-text and planted-tree probes, the prior external controls/full-tree probes, ownership checks and early boundary/driver/comment probes. No forbidden-form gap remains among those probes. The historical `plant_tree_probe.sh` hard-codes `60c911b9`; a documented invocation adapter retargeted only that checkout to the published head. Its source bytes, probe lines and gate calls remain unchanged, and the resulting clone head was verified. The older scripts that intentionally return nonzero when an old bypass disappears do so here: the full quote probe reports `bypass: false`, and the early SPDX probe fails its obsolete expectation that forbidden prose should pass. Neither is counted as a new failure.

R556-5-RS1 is resolved: CHANGELOG uses bullets. R556-5-S1 and S2 are adopted: the RV32 job allows twenty minutes and retries package downloads; hosted evidence now includes per-arm mutation XML, permitting all 329 killers to be regraded. Earlier R556-2-S2/S3/S4/S5 and R556-3-S1/S2/S3 remain adopted through explicit errors, fresh summaries/unknown-test refusal, shared checkout refs, strengthened port phrases and corrected links/spacing. R556-2-RS1/RS2/RS3 and R556-1-R1/R2/R4 remain resolved. Earlier action pins, retained import map and ratchet header remain present. R556-1-S4 has the published clause-check confirmation, with the independent-standard limitation below. R556-2-S1, header blank runs, remains deferred by the manager.

**Executed evidence**

| Area | Result and receipt |
|---|---|
| Linux | [All 22 local gates rc 0](receipts/local-linux/gates.json), omitting only local diagram rendering. GCC coverage and Clang ASan/UBSan each pass 369 instances in seven binaries, no skips; leak detection and halt-on-error enabled. [GCC instances](receipts/local-linux/gcc-instances.log), [sanitizer instances](receipts/local-linux/clang-sanitizers-instances.log). |
| Coverage | [Adjusted 1164/1164 lines and 583/583 branches](receipts/local-linux/coverage.log). ADP raw is 203/205 lines and 93/100 branches; the same two statements and seven unreachable arcs are excluded. Ratchet and exclusion controls pass. |
| Mutation | Fresh 311/311 CAUGHT by name. Independent per-arm XML audit confirms all 329 required killers inside streamed-message delimiters, for both local and hosted campaigns. [Local audit](receipts/local-killer-audit.json), [hosted audit](receipts/hosted-killer-audit.json), [local XML archive](receipts/local-linux-mutation-xml.tar.gz), [hosted XML archive](receipts/hosted-mutation-xml.tar.gz). |
| RV32 | [Debug and Release](receipts/local-rv32/results.json) build every core with RV32I/ILP32/freestanding flags and restricted headers, link the whole archive with fatal warnings, have no unresolved final symbols, and pass minimal-port smoke checks. Startup, BSS/stack layout, memory subset, imports, ELF ABI and completion path were inspected. |
| Preservation | [All 15 source/header/example files](receipts/preservation.json) and the entire mutation table are byte-identical across round 7. Seven production code-token streams equal the full PR base. [All 22 core object variants](receipts/object-comparison.json) equal that base byte for byte under current GCC, sanitizer and RV32 compile commands with `-g0 -frandom-seed=0`. |
| Documents and other gates | [427 relative links and 251 line links](receipts/document-links.json) pass. Traceability and test inventory regenerate without changes; 108 declarations reconcile with 369 instances. Boundary, static analysis, licence, privacy, registration, port-contract, report and coverage controls pass. |
| Integrity | [73 tracked files](receipts/checkout-integrity.json) match exact blob bytes and modes; index tree and HEAD match the assigned values. No untracked/ignored files. No required gitlinks exist at either source base or head. |

The [exact-head pull-request run](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37914316490) and [exact-head push run](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37914311694) both have successful quality and bare-metal jobs. Each run records fourteen successful steps and zero skipped steps. [PR checks](receipts/pr-checks.json), [run/head metadata](receipts/hosted-runs.json), [PR jobs](receipts/hosted-jobs.json), [push jobs](receipts/hosted-push-jobs.json). Downloaded PR artifacts contain 23 zero-return Linux gates, passing RV32 results, all per-arm XML and three rendered diagrams. [Independent evidence audit](receipts/evidence-audit.json). This is inspection of executed hosted evidence; the manager still owns hosted/act acceptance.

The specified [original public packet](https://github.com/kebag-logic/milan-fpga/tree/2ae0b85299a979413a5ba4b7fe3e3de175967a19/review-evidence/697-r1) has eight manifest entries, all verified. It records original-import author execution and production provenance, not current-head manager execution. The current [author REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6078586685), source-head hosted receipts and this review’s executions are distinguished throughout. No manager source bank ran at this head; none is claimed or inferred.

Local dependencies were isolated under scratch. Clang 18.1.3 package hashes were verified; GoogleTest/GMock was built from `f8d7d77c06936315286eb55f8de22cd23c188571` and reports exactly 1.14.0. Host builds used GCC 16 and Clang 23; comment/assertion lexing used Clang 18. [Versions](receipts/versions.txt), [dependency provenance](receipts/dependencies.json). Independent suites ran concurrently under a foreground coordinator; compilation was limited to eight simultaneous compiler processes. No detached background work remains.

**Wording residue**

- **R557-6-RS1 — RESIDUE — Docs.** Artifact: [PR #16 body](receipts/pr-body.md), sentence “Use the build commands above with GoogleTest and GMock 1.14.0.” No build commands precede it in the current body. Impact: a dangling prose direction only; no measurement, test, generated artifact or conformance claim changes. Exact fix: “Use the commands in the linked verification guide with GoogleTest and GMock 1.14.0.” Verification: reread the body and confirm the direction reaches the guide. The manager carries this wording fix.
- **R556-1-R3 — RESIDUE — Docs — RETAINED as previously classified.** The [closed PR #1 body](receipts/closed-pr1-body.md) still says “Hosted execution awaits publication of this branch.” Historical prose only; existing execution measurements and acceptance are unchanged. Exact carried fix: “Hosted runs [37885778682](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778682) (pull_request) and [37885778700](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778700) (push) pass all 16 gates at `b9b9c20`.” Verification: reread that body and confirm the stale sentence is absent. This lies outside the current source delta and remains a manager duty.

Neither residue changes the verdict or leaves a lens unclean.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | Frozen issue scope; six rules against byte/suffix/header/linker/assembly/assertion implementation; requirements/port authorities; compiling unlisted assertion probes | R557-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| RTL | CLEAN | No HDL or gitlinks in source tree/delta; core token and 22-object identity; RV32 startup/link/runtime and minimal port; restricted imports, final ELF and both smoke runs | R557-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| Robustness | UNCLEAN — F1 | Raw-token/conditional/assembly handling; assertion inventory and streamed grading; report freshness; boundary, re-entry, bounds, backpressure and sanitizer evidence | R557-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| Tests | UNCLEAN — F1 | 46 compiling comment controls, 14 generated templates, conditional matrix, prior probes, new full-tree bypass, 311 plants/329 killers, 369 instances per host compiler, coverage, hosted execution | R557-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| Docs | UNCLEAN — F1 | CODING_STANDARD/VERIFICATION enforcement claim; README, PORTING, requirements, deviations, import/provenance, generated links, PR body and residue | R557-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |

**Real limits and pending manager duties**

This is a delta review of a portable C stack, not complete device certification. The public [IEEE 1722.1-2021](https://standards.ieee.org/ieee/1722.1/6670/), [IEEE 1722-2016](https://standards.ieee.org/ieee/1722/5979/) and [Milan specification](https://avnu.org/resource/milan-specification/) authority pages were checked. Full normative clause texts were not independently re-audited; this delta changes no protocol requirement or clause claim. Local graph rendering was not rerun; three renders and their successful gate were inspected in exact-head hosted artifacts. The short probes do not prove absence of every possible form beyond the examined closed rules.

RV32 results establish simulator smoke behavior only. **Physical calibration NOT RUN. Field skips are not hardware proof.** No RTL simulation or synthesis, full parent/PP/gPTP/builder bank, hardware, privileged install, container execution, act or hosted replica was run. No private author material, lane scratchpad or management checkout was read. No source fix, commit, push, GitHub write, merge, author contact or other-checkout edit was performed.

The manager must return F1 for correction, carry the two wording residues, own hosted/act acceptance and obtain two independent positive reviews. At the merge turn, the manager validates the final current-dev candidate with builder and native banks and links those receipts on the PR. Source base remains `ae982af85ec97286bd35b39403926d8f0eaec81d`; the stated live dev is `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Those future candidate results are distinct from this source-head review. Consumer pins, submodule admission and firmware-image identity remain later acceptance; repository publication is an owner action.

Portable reproduction starts with `scripts/prepare_dependencies.py PACKET`, then sourcing `scripts/environment.sh`. The review scripts accept the reviewed clone and packet as arguments; the focused independent probe additionally accepts its work directory. `scripts/run_suites.py` runs local suites concurrently and waits for completion. `scripts/replay_prior.py` and `scripts/replay_early.py` preserve published probe bytes and record invocation details. Disposable SDKs, builds and probe trees remain under `scratch/`, which is excluded from publication. Receipts contain only documented path-prefix replacements; [redaction provenance](receipts/path-redactions.json) records affected hashes. Only REPORT.md and files listed in MANIFEST.sha256 are publishable.

R557-6 FINISHED
