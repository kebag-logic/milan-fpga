Relates to kebag-logic/milan-fpga#697

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

Use the build commands above with GoogleTest and GMock 1.14.0.
The [verification guide](https://github.com/kebag-logic/tsn-c-stack/blob/review-fixes/docs/VERIFICATION.md)
lists the complete contract, controls and template-regeneration command.
The manager owns hosted acceptance at this head and the two required reviews.

