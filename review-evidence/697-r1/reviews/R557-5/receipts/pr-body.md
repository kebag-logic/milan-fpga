Relates to kebag-logic/milan-fpga#697

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

