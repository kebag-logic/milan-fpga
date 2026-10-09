Relates to kebag-logic/milan-fpga#697

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

