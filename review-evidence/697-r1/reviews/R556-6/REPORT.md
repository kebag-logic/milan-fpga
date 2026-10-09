[R556] NEGATIVE - exact head 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5

# R556-6 internal independent review: tsn-c-stack PR #16, round 7 (relates kebag-logic/milan-fpga#697)

- Head `6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5`, tree `74f57eca0b0f93e6ed8681c9385635914c25701c`, base `main` `ae982af85ec97286bd35b39403926d8f0eaec81d`.
- Delta reviewed: `60c911b9..6bb706e2`, nine one-line commits (`42fa54e` to `6bb706e`). They touch 15 files, all in `scripts/`, `docs/`, the workflow, `CMakeLists.txt`, `README.md` and `CHANGELOG.md`. No file in `src/`, `include/`, `tests/` or `examples/` changed (`receipts/round7_delta.txt`).
- Review start: [6078602341](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078602341). Assignment: [6078263180](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6078263180). REVIEW READY: [6078586685](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6078586685).

## Summary

Verdict: NEGATIVE. Five MINOR findings are open. Four are compiling forms that bypass a listed contributor rule while every gate and both targets pass. The fifth is a version-pin claim that the build does not enforce.

- **F1 (rule 4)**: GNU ld and the C11 lexer still disagree on linker-script text. A backslash before `"`, or a `#` comment inside a `VERSION` node, hides a linker comment from the gate. The link succeeds with fatal warnings.
- **F2 (rule 5)**: the assembler directive `.include` reads a scanned non-assembly file (`.ld` or `.h`). Its `#` comments reach the assembler unchecked.
- **F3 (rule 3)**: a `.c` file included only by a C++ test unit is lexed as C11 only. A digit separator hides a `//` comment from the gate, and C++20 compiles it.
- **F4 (rule 6)**: GoogleTest's `GTEST_EXPECT_TRUE`, `GTEST_ASSERT_EQ` and `GTEST_SUCCEED`, and an `EXPECT_NEAR` spelled through `##`, compile in `tests/` and pass the assertion-form gate.
- **F5 (docs and tests)**: VERIFICATION says "CMake requires the same version". In fact `find_package(GTest 1.14.0 EXACT REQUIRED)` configures, builds and passes against GoogleTest 1.18.0.

The rest of the round-7 contract holds:
- VERIFICATION and CODING_STANDARD list exactly the six rules, and each rule has a compiling planted control (46 comment controls and the `EXPECT_NEAR` assertion control).
- `assertion_templates.py --check` regenerates the 14-form list byte-identically with GoogleTest 1.14.0.
- Every earlier reviewer probe, replayed unchanged, reports zero gaps.
- A fresh campaign catches 311/311 plants by name. An independent per-arm XML regrade confirms 329/329 killers, both locally and from the hosted artifact.
- All 23 Linux gates return 0 locally and in hosted run 37914316490. Each compiler runs 369 instances. RV32 Debug and Release link with `--fatal-warnings` and pass the QEMU smoke checks.
- All four hosted contexts at the exact head are green (pull_request and push runs, quality and bare-metal).

R556-5-F1/F2/F3 and R557-5-F1/F2 are resolved as demonstrated. F1-F4 continue their classes through forms that the round-7 rules do not close.

## 1. Scope reconstructed

- CONTRIBUTING.md and README.md (the repository has no AGENTS.md). Two independent positive reviews are required, with one-line commits, MIT SPDX, and Linux plus RV32 on every change.
- docs/CODING_STANDARD.md, docs/VERIFICATION.md, and the CHANGELOG.
- The issue #697 body and the owner decisions: 6074086970 and 6074093506 (MIT, own repository), 6074191062 (name), 6074245112 (assignment), 6074811248 (comment reduction) and 6074877336 (both targets on every change).
- Round 6 design: 6076983832. Round 7 contract: 6078263180, which defines the six-rule closed contract, the control obligation, the probe replays and the campaign.
- PR body, Round 7 section.
- Full diff `ae982af..6bb706e` and history (16 commits), then the round-7 delta.
- Public evidence:
  - the milan-fpga tree `2ae0b85` `review-evidence/697-r1` (round-1 author packet);
  - the earlier reviewer probes from the evidence branch at `fc3d8ef` (blob IDs in `receipts/prior-replay/prior_probe_blobs.txt`);
  - the manager's issue comments;
  - hosted runs 37914316490 (pull_request) and 37914311694 (push).
- I wrote my candidate list (`scratch`, unpublished) before reading any prior review finding. I read no other current-round report.

## 2. Findings

Each finding was probed by `scripts/r556_6_probes.py HEAD_CLONE WORK` in a disposable clone of the exact head. Every probe is a short compiling line. Each probe is first built: an RV32 probe runs `baremetal.py` (Debug and Release link with `--fatal-warnings`, the ELF checks and the QEMU smoke), and a host probe runs a CMake build plus ctest against GoogleTest 1.14.0. The head's own gates then run: comments, needles, conditionals, boundary, traceability, test-inventory, licence and port-contracts. A probe is GAP when it builds and every gate returns 0. All three positive controls are refused (`receipts/probes/probes.json`, per-probe logs with the applied diff).

| Probe | Rule | Build | Gates refusing | Result |
|---|---|---|---|---|
| `ld-backslash-quote` | 4 | rc 0 (link, fatal warnings, smoke) | none | GAP |
| `ld-version-hash` | 4 | rc 0 | none | GAP |
| `asm-include-ld` | 5 | rc 0 | none | GAP |
| `asm-include-h` | 5 | rc 0 | none | GAP |
| `asm-end-trailer` | 5 | rc 0 | none | GAP (outside the rules, see S1) |
| `c-file-in-cpp-unit` | 3 | rc 0 (7/7 ctest) | none | GAP |
| `gtest-alias-forms` | 6 | rc 0 (7/7 ctest) | none | GAP |
| `token-pasted-near` | 6 | rc 0 (7/7 ctest) | none | GAP |
| `control-expect-near` | 6 | rc 0 | needles, test-inventory | CAUGHT |
| `control-asm-hash` | 5 | rc 0 | comments | CAUGHT |
| `control-ld-comment` | 4 | rc 0 | comments | CAUGHT |

### R556-6-F1 - MINOR - Conformance, Robustness, Tests, Docs - the linker-script lexers still disagree

- Where: `scripts/check_comments.py:80-85` refuses only `'` in `.ld` and then lexes the file as C11 raw tokens. Two other ld forms make the C11 lexer and GNU ld disagree:
  - **Escaped quote.** GNU ld quoted names have no escapes. C11 treats `\"` as an escape. In `examples/rv32/link.ld` line 7, `*(.rodata .rodata.*) *("x\" /* prose words */ "y")` is read by ld as the names `x\` and `y` around a comment. C11 sees one string `"x\" /* prose words */ "`, an identifier, and an unterminated literal to the end of the line.
  - **VERSION node.** GNU ld accepts `#` comments inside a `VERSION { ... }` node. Appending `VERSION { PROBE { local: *; # prose words` plus `}; }` gives C11 a mid-line hash token, which is neither a comment nor a directive row.
  - Negative check (`scratch` only): replacing the comment delimiters with plain text makes ld report a syntax error. So ld really does parse `/* ... */` and `# ...` as comments here.
- Authority: Round 7 rule 4 ("Linker script ... Refuse `'` in `.ld`, and link RV32 with `-Wl,--fatal-warnings`"), which closes R556-5-F2's linker class. The rule's purpose is that the C11 lexer sees the comments the linker reads. `docs/CODING_STANDARD.md:6`: "It checks every comment under these rules". `docs/CODING_STANDARD.md:17` and `docs/VERIFICATION.md:58` and `:73`: linker-script comments use C11 raw tokens. `docs/VERIFICATION.md:29`: "Every comment under the closed contributor rules is checked".
- Evidence: `receipts/probes/ld-backslash-quote.log` and `ld-version-hash.log`. Both link in Debug and Release with `-Wl,--no-undefined -Wl,--fatal-warnings`, pass the ELF, import and unresolved-symbol checks and the QEMU smoke, and `check_comments.py` returns 0. The direct `/* prose words */` control is refused (`control-ld-comment.log`).
- Impact: a prose comment in the linker script passes the mandatory gate. The stated rule 4 guarantee does not hold.
- Required outcome: close the remaining ld/C11 disagreements by construction. For example:
  - refuse `\` and `#` in `.ld` files, as `'` is refused (neither appears in today's script);
  - or refuse `VERSION`, and treat ld strings and comments with ld's own rules.
  Add a compiling and linking `--selftest` control for each form, and keep `linker-tracing` passing.
- Verification: both probe rows make `check_comments.py` return nonzero, or fail the RV32 link. `scripts/r556_6_probes.py` reports CAUGHT for both. The real tree and existing controls pass, and both target jobs pass.

### R556-6-F2 - MINOR - Conformance, Robustness, Tests, Docs - assembler `.include` brings unchecked `#` comments from scanned non-assembly files

- Where: `scripts/check_comments.py:47-75`. The assembly rules refuse `'`, preprocessor directives, `.if*`, `.macro`, `.rept`, `.irp` and `.irpc`, but not `.include`. The included file is lexed under its own suffix's rule, where a mid-line `#` is neither a comment nor a directive:
  - `examples/rv32/include/probe.ld` holding `nop # prose words` passes rule 4;
  - `examples/rv32/include/probe.h` holding `#define PROBE_VALUE 1 # prose words` passes rule 3 in C11 and C++20, and the conditional matrix compiles it as C.
  The RV32 assembler reads either file through `.include "probe.ld"` or `.include "probe.h"` appended to `start.S`. The include path is the target's `examples/rv32/include`, which gcc passes to the assembler as `-I`. The assembler treats `# prose words` (and the whole `#define` line) as comments.
- Authority: Round 7 rule 5 ("Refuse every preprocessor directive in `.S` files ... Every `#` there is then an assembler comment, checked under the allowlist"). `docs/CODING_STANDARD.md:19-22`, `docs/VERIFICATION.md:60-61` ("Every `#` starts a comment checked against the tracing allowlist") and `:74` ("every hash starts a checked comment"). R556-5-F3 named "an assembler `.include`" as part of its class. Round 7 closed that class only for unscanned suffixes.
- Evidence: `receipts/probes/asm-include-ld.log` and `asm-include-h.log`. `baremetal.py` links both configurations with fatal warnings and passes the smoke. All eight gates return 0, including the licence gate (the planted files carry MIT SPDX). The direct `nop # prose words` control in `start.S` is refused (`control-asm-hash.log`).
- Impact: prose reaches the assembler as `#` comments while the gate reports success. The stated rule 5 guarantee does not hold.
- Required outcome: refuse `.include` (and `.incbin`, which can only carry data) in `.S` files, or lex every `.include` target as assembly under rule 5. Add a compiling and linking `--selftest` control.
- Verification: both rows make the gate fail. `start.S` still passes (it has no `.include`). Both target jobs pass.

### R556-6-F3 - MINOR - Conformance, Robustness, Tests, Docs - a `.c` file consumed by a C++ unit is lexed only as C11

- Where: `scripts/check_comments.py:83` and `:97-98` choose the modes by suffix, and only `.h` and `.hpp` get both. A test can include any scanned file. Probe:
  - `tests/probe_value.c` holds `#define TSN_PROBE_IGNORE(a) 0` and `enum { probe_value = TSN_PROBE_IGNORE(1'2 // prose words '` followed by `) };`;
  - `tests/test_port.cpp` ends with `#include "probe_value.c"`.
  In C11, `'2 // prose words '` is a discarded character constant, so there is no comment. In C++20, `1'2` is a number, and `// prose words '` is a comment that the compiler of `port_tests` reads. The conditional matrix compiles the `.c` file as C11 without a warning.
- Authority: Round 7 rule 3 ("Lex every `.h` and `.hpp` that a C++ unit includes in both C11 and C++20"), which answers R556-5-F2: a file must be lexed in each language that compiles it. `docs/VERIFICATION.md:50`: "This includes every header consumed by a C++ test unit". `docs/CODING_STANDARD.md:6`. Including a `.c` file from a test is a common unit-test idiom. Here the `.c` file is a header in all but suffix.
- Evidence: `receipts/probes/c-file-in-cpp-unit.log`. The CMake build passes with 7/7 ctest, and all eight gates return 0. The same text in a `.h` file is refused by the shipped header control (`receipts/local-validation/comments.log`, `header.h`).
- Impact: a comment that reaches the C++ compiler is unchecked. Rule 3's guarantee depends on the file's suffix, not on its consumer.
- Required outcome: one of:
  - lex every scanned file that a C++ unit includes in C++20 as well (for example from the CI builds' dependency output);
  - or refuse `#include` of `.c` and `.cpp` files in the gated directories.
  Add a compiling control.
- Verification: the probe row makes the gate fail, and the real tree passes.

### R556-6-F4 - MINOR - Conformance, Robustness, Tests, Docs - other GoogleTest assertion macros pass the assertion-form gate

- Where: `scripts/assertion_forms.py:11-17` refuses a raw identifier only if it starts with `EXPECT_` or `ASSERT_`, or equals `FAIL`, `ADD_FAILURE`, `ADD_FAILURE_AT`, `SUCCEED` or `GTEST_SKIP`.
  - GoogleTest 1.14.0 also defines `GTEST_EXPECT_TRUE`, `GTEST_EXPECT_FALSE`, `GTEST_ASSERT_TRUE`, `GTEST_ASSERT_EQ` (and the other `GTEST_ASSERT_*` aliases), `GTEST_FAIL`, `GTEST_FAIL_AT` and `GTEST_SUCCEED` (`gtest/gtest.h`).
  - A token-pasted spelling, `#define TSN_PROBE_PASTE(a, b) a##b` with `TSN_PROBE_PASTE(EXPE, CT_NEAR)(1.0, 1.0, 0.1);`, has no raw identifier that names the form.
- Authority: Round 7 rule 6 ("`tests/` may use only the assertion macros it uses today ... A gate refuses any other"). `docs/CODING_STANDARD.md:23-26` ("Tests use only ... The assertion gate refuses other forms, including `EXPECT_NEAR`"). `docs/VERIFICATION.md:27` ("Other assertion forms are refused"), `:77` and `:150` ("Unsupported forms fail the source gate").
- Evidence: `receipts/probes/gtest-alias-forms.log` and `token-pasted-near.log`. The probes insert `GTEST_EXPECT_TRUE(true); GTEST_ASSERT_EQ(1, 1); GTEST_SUCCEED();` or the pasted `EXPECT_NEAR` into the existing `ExamplePort` test body. Both build with GoogleTest 1.14.0, `port_tests` passes, and `needle_audit.py`, `test_inventory.py` and the other gates return 0. The literal `EXPECT_NEAR` control is refused (`control-expect-near.log`).
- Impact: the assertion vocabulary is not closed as stated. This does not create a false catch. Unlisted forms are neither instrumented nor inventoried, so they cannot supply a needle. But the rule-6 claim, and the premise that the generated templates cover every form in `tests/`, do not hold.
- Required outcome:
  - refuse every GoogleTest and GMock assertion or result macro outside the 14, including the `GTEST_` aliases, for example by listing the public macro names that the pinned headers define;
  - refuse `##` in test sources, or check the preprocessed test units for the expanded assertion helpers.
  Add a compiling control for an alias and for a pasted form.
- Verification: both probe rows make `needle_audit.py` fail. The 14 allowed forms and the shipped tests still pass.

### R556-6-F5 - MINOR - Docs, Tests, Robustness - the GoogleTest 1.14.0 pin is not enforced where VERIFICATION says it is

- Where:
  - `CMakeLists.txt:41` calls `find_package(GTest 1.14.0 EXACT REQUIRED)`. CMake's FindGTest module tries the package config first. If that is rejected, it falls back to a library and header search that checks no version.
  - `scripts/mutation.py:110` checks `pkg-config --modversion`, but its compiles use the default include path and link `-lgmock -lgtest` (`:136`, `:187`). So the version it checks need not be the version it builds against.
  - `docs/VERIFICATION.md:79` states "CMake requires the same version; the mutation driver checks it too."
- Evidence: `receipts/gtest_version_pin.txt`. On a host whose only GoogleTest is 1.18.0, CMake prints `Found GTest: /usr/lib/libgtest.so (Required is exact version "1.14.0")`, configures with rc 0, builds, and passes 7/7 tests. During this review a mixed environment (pkg-config metadata for 1.14.0, host 1.18.0 headers and libraries) let the mutation driver's version check pass while it compiled and linked 1.18.0. That run was discarded, and the environment was corrected before the recorded runs. `assertion_forms.require_version` correctly refuses on a single-install 1.18.0 host.
- Impact: the hosted job (Ubuntu 1.14.0 only) is unaffected. The documented reproduction claim is not true: a contributor's plain CMake build and ctest can silently use another GoogleTest version, whose default diagnostics differ from the generated list.
- Required outcome: make CMake enforce the pin (for example `find_package(GTest 1.14.0 EXACT CONFIG REQUIRED)`, or compare `GTest_VERSION` after the search). Have the campaign build with the flags whose version it checked (`pkg-config --cflags --libs`). If either is not wanted, state exactly what is checked.
- Verification: configuring with only GoogleTest 1.18.0 installed fails. The hosted job still configures. The campaign still gives 311/311.

### SUGGESTION (no verdict effect)

- **R556-6-S1 - Robustness.** `asm-end-trailer` appends `.end` and then a line of prose to `start.S`. The assembler ignores everything after `.end`, the build and smoke pass, and every gate returns 0 (`receipts/probes/asm-end-trailer.log`). The text is neither a `#` comment nor an assembler conditional, macro or repeat. So it is outside every listed rule, like unused `#define` bodies. Consider refusing `.end` in `.S` files beside `.if*`.
- **R556-6-S2 - Robustness.** The gate scans only `src/`, `include/`, `tests/` and `examples/` (`scripts/check_comments.py:112`). A test unit can still `#include` a header from another directory, or through a tracked directory symlink, and that file is never lexed. This is outside the contract's directory scope. Taking the scanned set from the CI builds' dependency output (R556-5-F3's second option) would also close F2 and F3.

## 3. Round 7 contract at this head

| Rule | Implementation | Control | Result |
|---|---|---|---|
| 1 Character set | `check_file` reads bytes and refuses anything but printable ASCII, tab and LF, data files included. `check_mode` applies the same rule to plant fragments. | `carriage-return`, `control-byte`, `non-ascii`, `assembly-formfeed`, `assembly-formfeed-define`, `assembly-verticaltab`, all compiling | Holds. R556-5-F1 rows are refused. |
| 2 Suffixes | `SUFFIXES` plus `DATA_FILES`. Every file below the four directories, tracked or untracked, is checked. | `included-suffix` (`.inc` compiled into a C++ unit) | Holds for files in the four directories (S2 concerns others). |
| 3 Header modes | `.h` and `.hpp` sources and header plants are lexed in C11 and C++20. | `header.h` and `header.hpp`, compiled in both languages, source and fragment refused, tracing passes | Holds for `.h` and `.hpp`. A `.c` consumed by C++ is open (F3). |
| 4 Linker script | `'` refused, C11 raw comments, `-Wl,--fatal-warnings` in `CMakeLists.txt:33` | `linker-quote` (links, then fails policy and fatal link), `linker-tracing` | The quote form is closed. Escaped quote and VERSION `#` are open (F1). |
| 5 Assembly | Directives refused (line check plus Clang directive rows), every `#` tail checked, `'`, `.if*`, `.macro`, `.rept`, `.irp` and `.irpc` refused | plain, spliced, macro-produced prose and tracing; quote, conditional, macro, repeat, pragma | R557-5-F1 is closed. `.include` is open (F2). `.end` is outside the rules (S1). |
| 6 Assertions | `ALLOWED` = 14 forms. `errors()` checks every C and C++ file in `tests/`. The inventory accepts only `ALLOWED`. Templates are generated from 1.14.0. | `EXPECT_NEAR` compiles and is refused. All 14 generated defaults are refused as needles. | `--check` regenerates identically. `GTEST_` aliases and pasted forms are open (F4). |

- Docs: `docs/CODING_STANDARD.md:5-31` and the `docs/VERIFICATION.md:66-75` table list exactly these six rules. The claims ("every comment under these rules") are scoped as the decision asked. F1-F5 are claims the behaviour contradicts.
- Adopted suggestions:
  - R556-5-S1: the bare-metal timeout is 20 minutes, with apt retries. The push-event bare-metal job passed at this head.
  - R556-5-S2: the per-arm mutation XML is uploaded. My regrade of the hosted artifact confirms 329/329 killers from per-arm XML.

## 4. Prior findings at this head

Prior probes ran byte-unchanged against a clean clone of the head (`receipts/prior-replay/`). The blob IDs match the published evidence branch (`prior_probe_blobs.txt`). One adaptation was needed: R556-5's `plant_tree_probe.sh` pins the commit it checks out. A copy with only that commit ID substituted was run (`plant_tree_probe.substitution.diff`). R557-5's scripts were placed so that their fixed relative Clang 18 location resolves to the same package extraction.

| Prior ID | Severity | Disposition | Exact-head evidence |
|---|---|---|---|
| R556-5-F1 assembly line model (form feed, vertical tab) | MINOR | RESOLVED | Rule 1 refuses the bytes. `hidden_text_probe.py`: all three assembly rows REFUSED, `gaps: 0`. `plant_tree_probe` row A: `A-comments rc=1`. |
| R556-5-F2 headers lexed only as C; `.ld` quote | MINOR | RESOLVED as demonstrated; the class continues as R556-6-F1 and F3 | `header-cxx-digit-separator` REFUSED. Row A comments rc 1. Row B: `B-comments rc=1`, `B-rv32 rc=1` (fatal warning). |
| R556-5-F3 unscanned suffix | MINOR | RESOLVED as specified; the assembler `.include` path named in its impact continues as R556-6-F2 | Row C: `C-comments rc=1`. `included-suffix` control. |
| R556-5-RS1 CHANGELOG paragraph | RESIDUE | RESOLVED | `CHANGELOG.md:6` is the requested bullet. |
| R556-5-S1, S2 | SUGGESTION | ADOPTED | Section 3. |
| R557-5-F1 macro-produced assembler comment | MINOR | RESOLVED | `independent_probes.py`: `assembly-macro-hash` and `-trace` refused. `preservation_and_probe.py`: full-tree comment gate rc 1, and the macro-produced `.if` is refused. |
| R557-5-F2 `EXPECT_NEAR` default fragment | MINOR | RESOLVED as demonstrated; the class continues as R556-6-F4 | `default-near-template`: the audit refuses (no owned literal). The unrelated default match stays false. |
| R556-4-F1, R557-4-F1, R556-3-F1 comment forms | MINOR | RESOLVED, no regression | `comment_bypass_probe.py`: `gaps: 0 of 11` (one exploratory C23 row does not compile, as before). `full_comment_bypass.py`: `bypass: false`, object bytes equal (its rc 1 means "not reproduced"). `comment_probes.py`: `gaps: 0`. |
| R556-4-F2, R556-3-F2 generic and default needles | MINOR | RESOLVED, no regression | `needle_probes.py`: all 11 refused. `needle_default_fragments.py`: 955 fragments per killer, 0 accepted. `needle_specificity.py`: 329 CAUGHT-BY-MESSAGE, 0 SHARED, 0 MISSING. |
| R556-2-F1 to F3, R557-2-F1 and F2, R556-1-F1 to F3, R557-1-F1 (MAJOR) to F4 | as recorded | RESOLVED, no regression | Their gates (port-contracts, boundary, registration-controls, mutation-controls, traceability, test-inventory, coverage) return 0 locally and in hosted run 37914316490. No production, test, port-contract or requirement file changed in round 7. |
| R556-1-R3 closed PR #1 body | RESIDUE | RETAINED (manager carries it) | The sentence "Hosted execution awaits publication of this branch." is still in PR #1's body. It is not part of this PR. |
| R556-2-S1 header blank runs | SUGGESTION | DEFERRED by the manager | Not assessed. |

## 5. Executed evidence

| Area | Result | Receipt |
|---|---|---|
| Linux full runner | `validate.py --jobs 16 --graphs`: rc 0, all 23 gates rc 0, with GoogleTest 1.14.0 headers and libraries and the Clang 18.1.3 lexer | `receipts/local-validation/gates.json`, `*.rc`, `*.log` |
| Test instances | 369 GCC (coverage) and 369 Clang (ASan, UBSan), 7/7 CTest each | `receipts/local-validation/traceability.log`; `--gtest_list_tests` counts |
| Coverage | 100% adjusted lines and branches. Raw ADP is 203/205 and 93/100, with the registered exclusions. | `receipts/local-validation/coverage.log` |
| Mutation (fresh) | 311 CAUGHT, 0 ESCAPED, 0 ERROR, names equal to the table. Independent per-arm XML regrade: 329/329 killers by streamed message. | `mutation-summary.txt`, `mutation-results.json`, `receipts/regrade-local.txt` |
| Assertion templates | `--check --selftest`: "14 compiled failing forms; current". `EXPECT_NEAR` compiles and is refused. | `receipts/local-validation/assertion-templates.log` |
| Comment controls | 46 compiling controls (38 refused, 8 pass) | `receipts/local-validation/comments.log` |
| RV32 | Debug and Release link with fatal warnings and no unresolved final symbols. Imports are within the allowlist, and the QEMU smoke passes. | `receipts/baremetal.log`, `receipts/rv32-results.json` |
| Hosted | PR run 37914316490: quality and bare-metal success, 23 gates rc 0, lexer `/usr/bin/clang-18`, my per-arm regrade 329/329, RV32 rc 0. Push run 37914311694: both jobs success. No step skipped. | `receipts/hosted/` |
| Contract probes | 8 GAP rows, 3 controls caught | `receipts/probes/` |
| Prior probes | All zero gaps | `receipts/prior-replay/` |
| Clone integrity | Head and tree exact. Clean status with no untracked or ignored files. 73 index entries match blob bytes and modes. Index equals HEAD. Zero gitlinks at base and head. | `receipts/clone_integrity.txt` |

Environment: the host has neither Clang 18 nor GoogleTest 1.14.0. I extracted the Ubuntu 24.04 packages that the hosted runner installs (`clang-18` 1:18.1.3-1ubuntu1, `googletest`/`libgtest-dev`/`libgmock-dev` 1.14.0-1, plus clang's runtime libraries) into `scratch`. The SHA256 values are in `receipts/toolchain_versions.txt`. `scripts/setup_sdk.sh` and `scripts/env.sh` reproduce the extraction. Compilers were host GCC 16.2 and Clang 23.1, RV32 GCC 16.2 with binutils 2.47, and QEMU 11.1. The hosted job uses GCC 13 and binutils 2.42. Host locations in receipts are replaced by placeholders (`receipts/location-redactions.json`).

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | Round 7 six-rule contract against `check_comments.py`, `comment_selftest.py`, `compiler_tokens.py`, `conditional_policy.py`, `assertion_forms.py`, `assertion_templates.py`, `assertion_messages.py`, `needle_audit.py`, `mutation.py`; owner comment rule; issue acceptance; dual-target rule | R556-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| RTL (production code and targets) | CLEAN | `src/`, `include/`, `examples/`, `tests/` unchanged since `60c911b9`; R557-5 preservation replay (7 files equal, non-comment tokens equal to base); GCC and Clang Linux builds; RV32 Debug and Release with `--fatal-warnings`, imports, ELF checks and smoke; hosted bare-metal on both events | R556-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| Robustness | UNCLEAN (F1, F2, F3, F4, F5) | Byte and suffix selection, mode selection, ld/assembler/C lexer agreement, `.include`, token pasting, version pinning, raw-dump parser, marker grading per arm | R556-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| Tests | UNCLEAN (F1, F2, F3, F4, F5) | 46 comment controls, assertion-template check and control, needle controls; 11 contract probes; 10 prior probe replays; fresh 311-plant campaign and per-arm regrade (local and hosted); 369 instances per compiler; coverage; hosted jobs | R556-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |
| Docs | UNCLEAN (F1, F2, F3, F4, F5) | CODING_STANDARD.md, VERIFICATION.md (six-rule table and claims), README.md, CHANGELOG.md, PR body Round 7, workflow | R556-6 | 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5 |

## 7. Real limits

- The probes are short compiling lines in disposable clones. I did not search exhaustively for further forms.
- Text that is not a comment (unused `#define` bodies, string literals, text after `.end`) is outside the owner's comment rule. I recorded `.end` only as S1.
- Local runs used newer host compilers and binutils than the hosted runner. The ld and assembler behaviours in F1 and F2 are long-standing GNU features, but I did not run the probes on binutils 2.42 or GCC 13. The hosted job ran only the unmodified head.
- No manager source bank exists at this head. Source-head execution evidence is the author's gate receipts plus this review's own runs. I make no claim about the current-dev merge candidate.
- RV32 evidence is simulator smoke only. Physical calibration NOT RUN. Field skips are not hardware proof.
- I ran no RTL simulation, synthesis, parent, PP, gPTP or builder bank, Docker or act, or hosted replica. Branch `dev-linux` was out of scope.
- The cited standards' full texts were not re-audited. Round 7 changes no requirement or clause claim.

## 8. Pending manager duties

- Return R556-6-F1 to F5 to the author lane. Carry R556-1-R3 on the residue checklist.
- Own hosted acceptance at this head (all four contexts are green: runs 37914316490 and 37914311694).
- Obtain two independent positive reviews.
- At the merge turn, validate the current-dev merge candidate (source base `ae982af85ec97286bd35b39403926d8f0eaec81d`, live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`) with the builder and native banks, and link their receipts on the PR.
- Consumer integration, submodule pins and firmware-image identity remain later acceptance. Repository publication is an owner action.

## 9. Packet

- `scripts/setup_sdk.sh` and `scripts/env.sh`: the reviewer toolchain extraction and environment (`PACKET` must name this directory).
- `scripts/r556_6_probes.py HEAD_CLONE WORK [probe ...]`: the contract probes and controls above.
- `scripts/regrade.py MUTATIONS_JSON CAMPAIGN_DIR`: per-arm XML regrade by streamed message.
- `scripts/replay_prior.sh PRIOR_DIR REPLAY_DIR CAMPAIGN_DIR`: the prior-probe replay.
- `scripts/run_bg.sh`: the background runner with per-job log and rc files.
- `receipts/`: raw outputs. Only files listed in `MANIFEST.sha256` and this report are published. `scratch/` is not.
- Long runs were started with their own log and rc files and awaited in the foreground. There were no source fixes, commits, pushes, GitHub writes, shared installs or edits to other checkouts. The review clone was verified at the exact head after all probes.

R556-6 FINISHED
