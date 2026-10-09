Relates to kebag-logic/milan-fpga#697

## Round 9

Addresses the [Round 9 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079940414)
and the [internal](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6079935853)
and [external](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6079752012) findings.
Head: `abe2476c4771bedc84531cf8d05fd12ef947c0cf`. Three commits follow `68070cb5`.

- Generate refused assertion names from all 21 public headers in the pinned install, including the failure-capturing header. Both compilers produce the same 85 refused names.
- Also refuse every identifier beginning `EXPECT_`, `ASSERT_` or `GTEST_` outside the fourteen-form allowlist, including trailing-underscore internals.
- Convert package `-I` paths to `-isystem`. Preserve all other compile and link flags and project signedness warnings. The dependency control uses real pinned headers in a scratch prefix.
- End the rule-table introduction with a full stop and place the threat model after the table.

Each item passed Linux and RV32 before its commit. All 24 Linux gates pass with a real GoogleTest 1.14.0 prefix install and no ambient include or library paths.
GCC and Clang each pass 369 tests. The fresh campaign catches 311/311 plants; independent XML grading confirms all 329 streamed-message killers.
Adjusted coverage remains 1164/1164 lines and 583/583 branches. Sanitizers, static analysis and all three diagram renders pass.
RV32 Debug and Release link with zero unresolved symbols and pass their minimal-port smoke checks.
All 25 production, test and data files and all 22 core object variants retain their bytes.

The four failure-capturing assertion controls compile and pass at runtime, then fail the source gate.
The internal failure control compiles, fails at runtime and is refused by the gate.
All six isolated-prefix reviewer steps pass. Removing the version check, compile flags or link flags still fails the dependency gate.
The incompatible 1.18.0 package is refused. Project signedness errors still fail with both compilers.

Every earlier reviewer probe was replayed unchanged. Replay audits validate the intended outcomes:

- All eleven prior full-tree probes report CAUGHT. Default-output fragments remain refused.
- Allowed assertion, tracing, literal-text and conditional controls pass.
- The exploratory C23 constant, the include-next probe and the header control containing assembler text retain their compile failures. None is counted as a compiling policy control.
- The out-of-scope linker include remains accepted in isolation. The declared directory scope is unchanged.
- The inherited ADP input probe accepts the same three documented inputs. The literal-label audit retains two conceptual labels with correct targets.
- Historical bypass scripts retain expected nonzero statuses after closure; their replay audits pass.

Follow the [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md)
for the build commands and separate-prefix setup. The [coding standard](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/CODING_STANDARD.md)
states the assertion contract. The earlier quality-document links remain applicable.
The manager owns hosted acceptance at this head and the two independent reviews.


## Round 5

Address [R556-3](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075697881)
under the [round 5 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076492549).
Head: `625b001173fda5f6401af1dceaef8d8ab86f5ae9`.

- Recognize single-line character literals and digit separators. Check assembly character constants and directive-body comments.
- Refuse zero and false conditions in both `#if` and `#elif`. Keep the existing valid tracing controls.
- Require each mutation needle to occur in an assertion message literal for its named test or referenced helper.
- Use literal message fragments for 24 needles. Preserve all 311 plant substitutions and all 329 named killers.
- Check critical contract phrases, name `NDEBUG`, use spaces in the MAAP assertion and unify IEEE 1722-2016 links.

All 21 Linux gates pass with optimized Python. GCC and Clang each pass 369 test instances.
The fresh campaign catches 311/311 plants. Independent XML grading confirms 329/329 killer entries.
Adjusted line and branch coverage remain 100%. Sanitizers, static analysis and three diagram renders pass.
RV32 Debug and Release link without unresolved symbols and pass the minimal-port smoke checks.
All seven production files remain unchanged, and all 22 core objects are byte-identical to the starting head.
The reviewer comment probes report zero gaps. Every default-output fragment in the needle probes is refused.
Thirteen compiling comment controls preserve object bytes and fail the gate. All valid controls still pass.

The build commands and quality documents below apply to this head. Hosted-run acceptance remains with the manager.

## Round 4

Address the [round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6075324408) in new commits after `ccb4ac3`.

- Restore callback semantics, public field meanings, preconditions and per-core counter tables in the porting guide. Check the documented names in CI.
- Check every comment line after splicing. Refuse prose inside SPDX blocks, assembly comments and disabled `#if 0` regions.
- Give the remaining MAAP killer its own assertion message. Refuse default GoogleTest value lines as needles.
- Record unknown mutation tests as ERROR. Clear the previous campaign summary before any new run.
- Keep every gate decision active under optimized Python. Both workflow jobs check out the same source revision.
- Keep the change log under Unreleased and describe the RV32 symbol allowlist accurately.

Production sources and headers are unchanged. All 22 core object hashes match the starting head under the CI flags and `-g0`.
Round 4 head: `3c350014de990171681b6b3113c70bdc6ace18c6`.
All 21 Linux gates pass under optimized Python. Both RV32 configurations link without unresolved symbols and pass their smoke checks.
Each hosted configuration passes 369 test instances. Fresh and reused campaigns catch all 311 plants; an independent XML audit matches all 329 required killers.
Adjusted line and branch coverage remain 100%. Sanitizers, static analysis and all three diagram renders pass.
The reviewer probes reject all reported bypasses. Their compiled comment variants retain identical objects.

## Round 3

Resolve the import reviews under the [follow-up assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) and [dual-target decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336).

- Require fresh, complete mutation reports. Refuse stale XML, partial results, skipped tests and mismatched registration.
- Give every killer an assertion-specific message. Reconcile traceability and sensitivity against executable GoogleTest registration.
- Check compiler dependencies and object symbols. Refuse digraph/trigraph outside includes, hidden heap use and OS calls.
- Link each standard separately. Preserve inherited ADP behavior with four input controls and explicit caller obligations.
- Keep only SPDX, requirement IDs and short standard references in code comments. Move integration contracts to the porting guide.
- Require Linux and freestanding RV32 CI jobs. Link every core against a minimal port and run RV32 smoke checks in Debug and Release.

The review fixes and RV32 support form the first commit. Comment reduction and its enforcement form the second.
All 311 planted programs retain identical code tokens and killer mappings after re-anchoring.
All 22 core objects match before and after comment reduction with CI flags, `-g0` and a fixed compiler seed.

## Build and validate

Linux needs GCC, Clang, CMake, GoogleTest, GMock, cppcheck, clang-tidy, Python and Mermaid CLI.
RV32 needs a RISC-V cross compiler, binutils and QEMU. The [workflow](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/.github/workflows/quality.yml) installs both sets.

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j16
ctest --test-dir build --output-on-failure -j16
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
python3 scripts/mutation.py --work build-validation/mutations --jobs 16
```

Use the commands in the linked [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md) with GoogleTest and GMock 1.14.0.

Round 3 validation: 369 hosted test instances; all 20 Linux gates pass; all 311 plants caught in fresh and repeated campaigns.
Adjusted coverage is 100% lines and branches, with the same five inherited exclusion rows.
AddressSanitizer, UBSan and static analysis pass with documented suppressions. All three Mermaid diagrams render.
RV32 Debug and Release pass dependency, symbol, full-link and runtime smoke checks. Both final images have zero unresolved symbols.
RV32 smoke checks cover all three cores; the full GoogleTest and coverage campaigns run on Linux.

Original import evidence: hosted runs [37885778682](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778682) (pull_request)
and [37885778700](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778700) (push) pass all 16 gates at `b9b9c20`.
Those runs describe the original import.
Hosted runs [37889967433](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37889967433) (pull_request)
and [37889963458](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37889963458) (push) pass the quality and bare-metal jobs at `ccb4ac3`.

## Quality documents

See the [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md),
[port contract](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/PORTING.md),
[requirements](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/REQUIREMENTS.md),
[traceability](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/TRACEABILITY.md),
[test defects](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/TESTS.md),
[coverage exclusions](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/COVERAGE.md),
[analysis suppressions](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/STATIC_ANALYSIS.md),
and [import provenance](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/IMPORT.md).
The [ADP correction](https://github.com/kebag-logic/tsn-c-stack/issues/3) remains a separate behavior change.

## Round 6

Addresses the [Round 6 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076983832)
and the [internal](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6076927671)
and [external](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6076974636) findings.

The comment gate reads Clang 18 raw tokens in C11 or C++20 mode.
Only documented conditional macros and file guards are allowed.
A compilation matrix reaches both sides of every non-guard region, including nested regions.
Assembly rejects single quotes, assembler conditionals, macros and repeats.
Hash comments in directive bodies follow the same allowlist.

Mutation grading uses only the assertion's streamed message.
Each needle has at least eight characters and occurs in exactly one message literal of its named test.
Default diagnostic fragments are refused. Twenty-five needles and five assertion messages are made unique.
All 311 plant substitutions and their killer mappings remain unchanged.
The production sources and all 22 core object variants retain their bytes.

Validation at `60c911b92825a720044e78bed540752c7dd0368e` follows the host-reset recovery:

- All 22 Linux gates pass. GCC and Clang each pass 369 test instances without skips.
- Fresh and repeated campaigns catch 311/311 plants. Independent XML grading confirms all 329 killers depend only on streamed messages.
- Adjusted coverage remains 1164/1164 lines and 583/583 branches with the same inherited exclusions.
- Sanitizers and static analysis pass with the documented suppressions. Three diagrams render.
- The conditional matrix compiles 38 branch sides across 22 files. All 32 comment controls compile and reach their expected policy result.
- The unchanged reviewer comment probes report zero gaps. All tested default-output fragments and single-letter needles are refused.
- RV32 Debug and Release link with zero unresolved symbols and pass the minimal-port smoke checks.

Both required jobs remain in the [workflow](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/.github/workflows/quality.yml).
Hosted execution at this head remains the manager's acceptance step.
The [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md)
and [coding standard](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/CODING_STANDARD.md)
describe the compiler version, controls, conditional allowlist and grading rules.

## Round 7

Addresses the [Round 7 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6078263180)
and the [internal](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078253855)
and [external](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078194538) findings.
Head: `6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5`.

- Restrict checked files to printable ASCII, tab and LF, scanned suffixes and two data exceptions.
- Lex every header and header plant in C11 and C++20. Refuse linker quotes and make RV32 link warnings fatal.
- Refuse assembly preprocessing. Keep the single-quote and assembler-conditional restrictions.
- Permit 14 assertion forms. Generate their default diagnostics from GoogleTest and GMock 1.14.0, blank streamed messages and compare regeneration in CI.
- State all six contributor rules in both quality guides. Raise the bare-metal timeout to 20 minutes, retry package downloads and retain per-arm mutation XML.

All 23 Linux gates pass. GCC and Clang each pass 369 instances.
The fresh campaign catches 311/311 plants; independent XML grading confirms all 329 killers.
Adjusted coverage remains 1164/1164 lines and 583/583 branches.
Sanitizers, static analysis and three diagram renders pass.
All 46 compiling comment controls and 14 generated assertion diagnostics pass their expected checks.
The unchanged reviewer probes report zero remaining gaps under the new rules.
RV32 Debug and Release link without unresolved symbols and pass the minimal-port smoke checks.
All 13 core and port files, all 22 core object variants and the entire mutation table retain their bytes.

The [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md)
lists the complete contract, controls and template-regeneration command.
The manager owns hosted acceptance at this head and the two required reviews.

## Round 8

Addresses the [Round 8 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079166369)
and the [internal](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6079158227)
and [external](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078915470) findings.
Head: `68070cb5723682586c07a6de80a49886732b5dc2`. Five commits follow `6bb706e2`.

- Generate 81 refused public assertion and result macros from the pinned headers. Check regeneration and refuse token pasting in tests.
- Require the exact GoogleTest config package. Compile and link mutations with the checked package flags.
- Refuse assembly source and binary includes and `.end`.
- Refuse linker backslashes, hashes and `VERSION`.
- Refuse includes of `.c` and `.cpp` sources in the checked directories.

Each item has compiling controls and passed both targets before its commit.
All 24 Linux gates pass. GCC and Clang each pass 369 test instances.
The fresh campaign catches 311/311 plants. Independent XML grading confirms all 329 streamed-message killers.
Adjusted coverage remains 1164/1164 lines and 583/583 branches.
Sanitizers, static analysis and three diagram renders pass.
RV32 Debug and Release link with zero unresolved symbols and pass the minimal-port smoke checks.
All 25 production, test and data files and all 22 core object variants retain their bytes.

All eleven current internal probe rows report CAUGHT after compiling or running.
The independent assertion controls refuse both aliases and preserve the allowed form.
Every earlier reviewer probe was replayed unchanged. Unchanged outcomes remain explicit:

- Allowed assertion, tracing, literal-text and conditional controls pass.
- The exploratory C23 bit-precise constant still does not compile.
- The inherited ADP input probe still accepts the three documented inputs, as the owner decided.
- The literal-label audit still flags two conceptual labels with correct target lines.
- Historical bypass scripts retain expected nonzero statuses when a bypass is closed; replay audits pass.

The [coding standard](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/CODING_STANDARD.md)
and [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md)
state the contributor threat model beside the six rules.
Deliberately obfuscated forms outside those rules remain suggestions unless shipped.
External-directory headers and directory symlinks remain outside the declared scan scope.
The manager owns hosted acceptance at this head, the wording update and two independent reviews.
