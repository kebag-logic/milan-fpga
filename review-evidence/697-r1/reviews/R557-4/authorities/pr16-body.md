https://github.com/kebag-logic/tsn-c-stack/pull/16

Relates to kebag-logic/milan-fpga#697

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
