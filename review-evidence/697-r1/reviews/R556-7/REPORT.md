[R556] NEGATIVE - exact head 68070cb5723682586c07a6de80a49886732b5dc2

# R556-7 internal independent review: tsn-c-stack PR #16, round 8 (relates kebag-logic/milan-fpga#697)

- Head `68070cb5723682586c07a6de80a49886732b5dc2`, tree `f42024aec0fddde6cf6d552e85e50109a8e6cbb4`, base `main` `ae982af85ec97286bd35b39403926d8f0eaec81d`.
- Delta reviewed: `6bb706e2..68070cb5`, five one-line commits with no bodies (`1fb40ab`, `71640ce`, `c0d1e61`, `97971e2`, `68070cb`). `6bb706e2` is an ancestor, so there was no rebase. The commits touch 11 files in `scripts/`, `docs/` and `CMakeLists.txt`. No file under `src/`, `include/`, `tests/`, `examples/` or `.github/` changed (`receipts/round8_delta.txt`).
- Review start: [6079422056](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6079422056). Assignment: [6079166369](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079166369). REVIEW READY: [6079409858](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079409858).

## Summary

Verdict: NEGATIVE. Two MINOR findings are open.

- **F1 (rule 6, regression):** the assertion gate no longer refuses the public GoogleTest assertions in `gtest/gtest-spi.h`. These are `EXPECT_NONFATAL_FAILURE`, `EXPECT_FATAL_FAILURE` and their `_ON_ALL_THREADS` forms.
  - The previous round head refused them, because it refused every `EXPECT_*` name outside the 14 allowed forms.
  - At this head the gate refuses only the generated list, and that list is built from `gtest.h` and `gmock.h` alone.
  - An honest in-test use compiles with 1.14.0 and passes every source gate. The test also passes while the assertion it wraps fails.
- **F2 (robustness of the new pin):** with GoogleTest 1.14.0 installed in a non-system prefix, the new dependency gate cannot pass, and the mutation gate fails too.
  - `pkg-config` then supplies `-I`, so gtest.h is no longer a system header.
  - One mixed-sign comparison in a test (`tests/test_adp.cpp:116`) then fails `-Werror`.
  - Hosted CI is unaffected, because Ubuntu installs to `/usr`.

All other round-8 items work as assigned, each with a compiling or linking control:

- `.include`, `.incbin` and `.end` are refused in `.S` files.
- `\`, `#` and `VERSION` are refused in `.ld` files.
- `#include` of `.c` and `.cpp` files is refused in the gated directories.
- The `GTEST_*` aliases and `##` are refused in tests.
- CMake enforces the exact pin, and the mutation driver uses the checked package flags.

All 11 R556-6 probe rows and the R557-6 probes now report CAUGHT. The fresh campaign catches 311/311 plants by name, and my per-arm XML regrade confirms 329/329 killers. Both targets pass locally and in hosted CI at the exact head.

## 1. Scope reconstructed

- **Contributing rules:** there is no `AGENTS.md`. `CONTRIBUTING.md` requires one-line commits, neutral labels and two independent reviews. `README.md`, `docs/VERIFICATION.md` and `docs/CODING_STANDARD.md` were read before the diff.
- **Issue #697:** the frozen acceptance (body) and owner decisions [6074086970](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074086970), [6074093506](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506), [6074191062](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062), [6074245112](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112) (assignment), [6074811248](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) (comment rule) and [6074877336](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336) (both targets on every change).
- **Round 8 decision ([6079166369](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6079166369)):**
  - The threat model: the comment gate keeps honest contributors to the six rules plus the round-8 refusals. A deliberately obfuscated form outside those rules is a SUGGESTION unless it is shipped.
  - Items 1-5, each with a compiling planted control.
  - Unchanged replay of the earlier probes, and a fresh 311/311 campaign.
- **Prior findings** were read only after my independent pass over the diff, probes and runs:
  - [R556-6](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6079158227): F1-F5, S1, S2.
  - [R557-6](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6078915470): F1 and RS1.
- **Public evidence:** the [697-r1 packet](https://github.com/kebag-logic/milan-fpga/tree/2ae0b85299a979413a5ba4b7fe3e3de175967a19/review-evidence/697-r1) holds the round-1 import provenance (head `b9b9c20a`, host GoogleTest 1.18.0). It is not exact-head execution evidence. Source-head execution evidence at this head is the hosted CI runs plus this review's own runs. No manager source bank ran at this head, and none is claimed.

## 2. Findings

### R556-7-F1 - MINOR - Conformance, Robustness, Tests, Docs - `gtest-spi.h` assertions pass the assertion gate (regression)

- **Where:**
  - `scripts/assertion_forms.py:16-24`: `errors()` now refuses a raw identifier only if it is in `refused_macros`.
  - `scripts/assertion_forms.py:32-44`: `refused_macros()` takes names from `-dM -E` of `<gtest/gtest.h>` and `<gmock/gmock.h>` only.
  - At `6bb706e2`, `errors()` refused every identifier that starts with `EXPECT_` or `ASSERT_` and is outside the 14.
  - The GoogleTest 1.14.0 public header `gtest/gtest-spi.h` defines `EXPECT_FATAL_FAILURE`, `EXPECT_NONFATAL_FAILURE`, `EXPECT_FATAL_FAILURE_ON_ALL_THREADS` and `EXPECT_NONFATAL_FAILURE_ON_ALL_THREADS`. `gtest.h` does not include that header.
- **Authority:**
  - Rule 6 at `docs/CODING_STANDARD.md:27-31`: "Tests use only [the 14 forms] ... The assertion gate refuses other forms".
  - `docs/VERIFICATION.md:27`: "Other assertion forms are refused."
  - Round 8 item 1: "Refuse any outside the 14 allowed forms".
  - R556-6-F4 required outcome: "refuse every GoogleTest and GMock assertion or result macro outside the 14".
  - Testing an assertion helper with `EXPECT_NONFATAL_FAILURE` is the documented GoogleTest idiom. An honest contributor could plausibly write it, and rule 6 lists it as refused.
- **Evidence:**
  - `receipts/probes/probe_assertions.json` and `.log`: the four `gtest-spi` controls compile with 1.14.0 under `-Wall -Wextra -Werror` and run with rc 0, so the wrapped failure is absorbed.
    - Head gate: `[]`.
    - Gate at `6bb706e2`: `unsupported assertion form: EXPECT_NONFATAL_FAILURE` and the others.
  - `receipts/probes/probe_spi_tree.log` and `spi-plant.diff`:
    - The plant adds `#include <gtest/gtest-spi.h>` and `EXPECT_NONFATAL_FAILURE(EXPECT_EQ(1, 2) << "planted inner failure", "planted inner failure");` to the existing traced `ExamplePort` test.
    - The documented `--write` regeneration of TRACEABILITY and TESTS follows.
    - Then comments, needles, test-inventory, traceability, conditionals, boundary, licence and port-contracts all return 0. `port_tests` builds and passes.
  - `receipts/probes/header_macro_survey.txt`: these four are the only public function-like assertion macros in the pinned include tree that are neither allowed nor refused. The four `*_HRESULT_*` macros are Windows-only and do not compile on Linux.
- **Impact:** the rule-6 claim of a closed vocabulary is false at this head. This round regressed it from the previous head. These forms invert a contained assertion: a test can pass while its inner check fails. They also produce failure text outside the generated templates. No false mutation catch is shown; the 311/311 campaign is unaffected.
- **Required outcome:** refuse every `EXPECT_*` and `ASSERT_*` identifier outside the 14 again, beside the generated list. Alternatively, generate from every public header of the pinned tree, `gtest/gtest-spi.h` included. Add a compiling control for `EXPECT_NONFATAL_FAILURE`.
- **Verification:**
  - The four `spi` rows of `probe_assertions.py` report refused.
  - `probe_spi_tree.sh` makes `needle_audit.py` return 1.
  - The allowed forms, the shipped tests, `--check` and 311/311 still pass.

### R556-7-F2 - MINOR - Robustness, Tests - the pinned GoogleTest in a non-system prefix fails the dependency and mutation gates

- **Where:**
  - `scripts/assertion_forms.py:27-29` (`package_flags`) and `scripts/mutation.py:111-112, 126, 137-138, 185, 189` now compile tests with `pkg-config --cflags gmock gtest`.
  - For a prefix outside the compiler's system directories, that output is `-I<prefix>/include`. The pinned headers are then not system headers.
  - `tests/test_adp.cpp:116` has `EXPECT_EQ(fk.starts, 0)`, an unsigned/int comparison. It instantiates `CmpHelperEQ` with `-Wsign-compare` under `-Werror`.
  - `scripts/dependency_selftest.py:55` removes `CPLUS_INCLUDE_PATH`, `C_INCLUDE_PATH` and `LIBRARY_PATH`.
- **Authority:**
  - Round 8 item 2 and R556-6-F5 aim to build with "the version it checked" when another version is installed.
  - `docs/VERIFICATION.md:42` tells testers to install 1.14.0 from the pinned commit.
  - The VERIFICATION Dependency pin row: "Compile and catch a header plant using the checked package flags ... without ambient include or library paths."
- **Evidence:**
  - `receipts/local-validation-plain/dependencies.log`: the full runner with the upstream `gtest.pc` (`-I` prefix) fails the dependencies gate with `gtest.h:1379 ... [-Werror=sign-compare]`, "required from" `test_adp.cpp:116`. The runner then stops before the builds (`gates.json`).
  - `receipts/probes/probe_dependency.log`:
    - The unmodified head passes the dependency gate (rc 0) when the identical install's package flags use `-isystem`.
    - It fails (rc 1) with the upstream `-I` flags.
    - Only `test_adp.cpp` trips, with exactly one instantiation.
  - `receipts/probes/probe_prefix.log`: adding `CPLUS_INCLUDE_PATH` lets `mutation.py` pass. The dependency gate still fails, because `pkg-config` then drops the `-I` and the gate strips the variable.
- **Impact:**
  - A tester whose distribution ships another GoogleTest version, and who installs 1.14.0 under a user prefix, cannot pass the documented Linux validation command. That is the case the pin exists for.
  - The error points into gtest.h and hides its cause, a test-side mixed-sign comparison that system-header suppression masks in every passing build.
  - Fail-closed only: there is no false pass. Hosted CI and `/usr` or `/usr/local` installs are unaffected.
- **Required outcome:** do one of the following, and add a control that runs the dependency gate against 1.14.0 in a non-default prefix:
  - pass package include directories as system includes, for example by translating `pkg-config` `-I` to `-isystem` as CMake imported targets do;
  - make `tests/test_adp.cpp:116` sign-consistent (`0u`) and keep tests warning-free without system-header suppression.
- **Verification:** the "upstream -I package flags" row of `probe_dependency.sh` returns 0. The campaign stays 311/311.

### SUGGESTION (no verdict effect)

- **R556-7-S1 - Robustness, Tests:** internal trailing-underscore macros are excluded by design (`assertion_forms.py:39`). An example is `GTEST_NONFATAL_FAILURE_("...")`. It compiles, fails at runtime and passes the gate (`receipts/probes/probe_internal_macro.txt`). These are reserved implementation names, outside the threat model. A prefix rule on `EXPECT_`, `ASSERT_` and `GTEST_` would close this together with F1.
- **R556-6-S2 - RETAINED as SUGGESTION:** headers outside the four directories, and directory symlinks, are not lexed. The PR body declares this outside the scan scope. A linker-script `INCLUDE` of a file outside the gated directories is in the same class. In-scope `.ld` files are checked themselves (`probe_comment_gate.json` row `ld-include-other`).

### RESIDUE (no verdict effect; manager checklist)

- **R556-7-RS1 - Docs:** at `docs/VERIFICATION.md:71`, the sentence "The six contributor rules are the gate's complete comment and assertion contract:" ends in a colon. The colon now introduces the two threat-model sentences (`:72-73`), not the rule table. Exact fix: end line 71 with a full stop, and put the two threat-model sentences after the rule table.
- **R556-1-R3 - Docs - RETAINED:** the closed PR #1 body still says "Hosted execution awaits publication of this branch." The exact fix carried by the manager is unchanged.

## 3. Round 8 items at this head

| Item | Implementation | My controls | Result |
|---|---|---|---|
| 1 Assertion vocabulary | `refused_macros()` produces 81 names from `-dM -E` (`assertion-defaults.json`). `--check` regenerates them. `hashhash` tokens are refused in every C and C++ file below `tests/`. | The list regenerates identically with g++ and clang++ (`refused_list_regen.txt`). `GTEST_ASSERT_LT`, `GTEST_FAIL`, `EXPECT_THAT`, `EXPECT_GT`, `EXPECT_PRED2`, `FAIL`, `ADD_FAILURE`, `SUCCEED`, `GTEST_SKIP`, `EXPECT_NO_FATAL_FAILURE`, `##` and the `%:%:` digraph paste all compile and are refused. Allowed forms and literal `##` text pass. | Holds for `gtest.h` and `gmock.h`. `gtest-spi.h` regressed (F1). |
| 2 GoogleTest pin | `find_package(GTest 1.14.0 EXACT CONFIG REQUIRED)`. `mutation.py` uses `pkg-config --cflags/--libs` for `main.o`, test objects and links. New `dependency_selftest.py` gate. | With only host 1.18.0 visible, configure fails and names both versions, and `mutation.py` refuses (`f5_only_other_version.txt`). Reverting to module mode, dropping the package cflags, or restoring `-lgmock -lgtest -pthread` each makes `dependency_selftest.py` fail (`probe_dependency.log`). | Holds. Non-system prefix fails closed (F2). |
| 3 Assembly | The `.` + word check covers `include`, `incbin` and `end` (`check_comments.py:80-83`). | Each of these assembles and links with `--fatal-warnings` and is refused: `.include`, `.INCLUDE`, after a label, after `;`, `.incbin`, `.incbin` with a range, `.end`, and `nop; .end`. Direct tracing and `.func/.endfunc` pass. | Holds. |
| 4 Linker script | `'`, `\` and `#` are refused anywhere. A raw `VERSION` identifier is refused (`:70-72`, `:89-90`). | Backslash string, VERSION `#` comment and VERSION block each link with fatal warnings and are refused. The quote is refused and fails fatal linking. Tracing passes. | Holds. |
| 5 Source includes | `#include` rows whose quoted or angled target ends `.c` or `.cpp` are refused, in every mode (`:65-68`). | Quoted, angled, spaced, subdirectory, comment-in-directive and spliced forms in `.cpp`, `.c` and `.h` all compile and are refused. `#include_next` is refused as an unknown directive. | Holds. |
| Threat model | `docs/CODING_STANDARD.md:7-8` and `docs/VERIFICATION.md:72-73` | Wording matches the decision. Both guides claim exactly the six rules and the round-8 refusals. | Holds, except the rule-6 claim (F1). RS1 is wording only. |

## 4. Prior findings at this head

| Finding | Severity | Status | Evidence |
|---|---|---|---|
| R556-6-F1 ld escape and VERSION `#` | MINOR | RESOLVED | Replayed `ld-backslash-quote` and `ld-version-hash` are CAUGHT by comments after an RV32 build, link and smoke. My `ld-*` rows are refused. |
| R556-6-F2 assembler `.include` | MINOR | RESOLVED | Replayed `asm-include-ld` and `asm-include-h` are CAUGHT. My `asm-include*` and `asm-incbin*` rows are refused. |
| R556-6-F3 `.c` in a C++ unit | MINOR | RESOLVED | Replayed `c-file-in-cpp-unit` is CAUGHT. My eight include rows are refused. |
| R556-6-F4 `GTEST_` aliases and `##` | MINOR | RESOLVED for the reported forms. The class WORSENED for `gtest-spi.h`, tracked as R556-7-F1. | Replayed `gtest-alias-forms` and `token-pasted-near` are CAUGHT by needles and test-inventory. |
| R556-6-F5 pin not enforced | MINOR | RESOLVED | `f5_only_other_version.txt` and the `probe_dependency.log` variants. The fix introduces F2. |
| R556-6-S1 `.end` | SUGGESTION | ADOPTED | Replayed `asm-end-trailer` is CAUGHT. |
| R556-6-S2 directory scope | SUGGESTION | NOT ADOPTED (declared scope) | Retained above. |
| R557-6-F1 `GTEST_ASSERT_LT`, `GTEST_FAIL` | MINOR | RESOLVED | Replayed `independent_probes.py`: both rows `source_gate: refused`, compile rc 0, run rc 1. Replayed `full_assertion_probe.py`: needles rc 1 (`unsupported assertion form: GTEST_ASSERT_LT`). The script's rc 1 is its own "bypass closed" assertion. |
| R557-6-RS1 PR body sentence | RESIDUE | RESOLVED | The current PR body no longer contains it. |
| R556-1-R3 closed PR #1 body | RESIDUE | RETAINED | Still present. Manager duty. |
| Earlier rounds (R556-1 to R556-5, R557-1 to R557-5) | as recorded | RESOLVED, no regression | Replayed byte-unchanged (`receipts/replay/provenance.sha256`). See the list below. |

Replay detail for the earlier rounds:

- `comment_probes.py`: `gaps: 0`.
- `needle_probes.py`: all refused.
- `comment_bypass_probe.py`: `gaps: 0 of 11`. The C23 `0wb` row still does not compile.
- `needle_default_fragments.py`: 0 of 955 fragments accepted per kill.
- `needle_specificity.py`: 329 CAUGHT-BY-MESSAGE, 0 SHARED, 0 MISSING.
- `hidden_text_probe.py`: `gaps: 0`.
- `plant_tree_probe.sh`: A-comments, B-comments, B-rv32 and C-comments are each rc 1. Its pinned checkout was retargeted to the head (`plant_tree_probe.adapt.diff`).
- `full_comment_bypass.py`: `bypass: false`. Its rc 1 means "not reproduced".
- R557-5 `independent_probes.py` and `preservation_and_probe.py`: rc 0. Their packet `receipts/` directory had to be created; that is an invocation-only change.

## 5. Executed evidence

| Area | Result | Receipt |
|---|---|---|
| Linux full runner | `validate.py --jobs 16 --graphs`: all 24 gates rc 0. Uses GoogleTest 1.14.0 with `-isystem` package flags and the Clang 18.1.3 lexer. | `receipts/local-validation/gates.json`, `*.rc`, `*.log` |
| Same, upstream `-I` package flags | `dependencies` rc 1 (F2). The runner stops after the source gates. | `receipts/local-validation-plain/` |
| Test instances | 369 for GCC with coverage and 369 for Clang with ASan and UBSan; 7/7 CTest each. | `receipts/test_instances.txt` |
| Coverage | 100% adjusted lines and branches. ADP raw is 203/205 and 93/100, with the registered exclusions. | `local-validation/coverage.log` |
| Mutation (fresh) | 311 CAUGHT, 0 ESCAPED, 0 ERROR. Names equal the table. My per-arm XML regrade confirms 329/329 killers inside the streamed-message markers. | `local-validation/mutation-results.json`, `receipts/regrade.txt`, `scripts/regrade_xml.py` |
| Templates and controls | `--check --selftest` passes: 14 forms, the `GTEST_ASSERT_LT`, `GTEST_FAIL` and pasted controls, and a current list of 81 names. Comment controls pass, the new assembly, linker and include controls included. | `local-validation/assertion-templates.log`, `comments.log`, `dependencies.log` |
| RV32 | Debug and Release link with `-Wl,--fatal-warnings`. There are no unresolved final symbols, imports stay within the allowlist, and the QEMU smoke passes. | `receipts/rv32/results.json`, `release-link-command.txt`, `receipts/baremetal.log` |
| Hosted | PR run 37920179036 and push run 37920173994 both pass quality and bare-metal at the exact sha, with every step executed. The PR artifact has 24 gates at rc 0 and 311 CAUGHT; my regrade of the hosted XML gives 329/329, and RV32 Debug and Release pass. | `receipts/hosted/` |
| Round-8 probes | See section 3 | `receipts/probes/` |
| Prior replay | See section 4 | `receipts/replay/` |
| Documents | 69 relative links in the changed and entry documents resolve. | `receipts/doc_links.txt` |
| Clone integrity | Head and tree are exact; the index tree equals HEAD. Status is clean, including ignored and untracked files. All 74 tracked files match their blob bytes and modes. There are zero gitlinks at base and head and no `.gitmodules`. | `receipts/clone_integrity.txt` |

The environment is listed in `receipts/toolchain_versions.txt` and `scripts/setup_toolchain.sh`.

- The host has neither Clang 18 nor GoogleTest 1.14.0.
- GoogleTest was built from `f8d7d77c` (v1.14.0).
- The lexer is the Ubuntu 24.04 `clang-18` 18.1.3-1ubuntu1 package and its runtime libraries, extracted under `scratch/` (SHA256 recorded).
- The host compilers are GCC 16.2 and Clang 23.1. RV32 uses GCC 16.2 with binutils 2.47, and QEMU 11.1.
- The hosted runner uses GCC 13 and binutils 2.42.
- The bank uses an `-isystem` copy of the package files. This matches how a `/usr` install behaves; F2 records why that copy is needed.
- Host location prefixes in receipts are replaced by placeholders (`receipts/location-redactions.json`).

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-8 items 1-5 and the threat model against `assertion_forms.py`, `assertion_templates.py`, `assertion-defaults.json`, `check_comments.py`, `comment_selftest.py`, `CMakeLists.txt`, `mutation.py` and `dependency_selftest.py`. Also the owner comment rule, issue acceptance and the two-target rule. | R556-7 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| RTL | CLEAN | No HDL and no gitlinks in the tree or the delta. The RV32 freestanding build, `start.S`, `link.ld` and the minimal port are unchanged in round 8. Both RV32 configurations link with fatal warnings and pass the smoke, locally and hosted. | R556-7 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| Robustness | UNCLEAN (F1, F2) | Lexer agreement for `.S`, `.ld` and source includes; generated vocabulary scope; token pasting; version pinning and package flags in custom and system prefixes; internal macros (S1); directory scope (S2). | R556-7 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| Tests | UNCLEAN (F1, F2) | 24 local gates; 45 round-8 probe rows; 3 dependency-control reversals; 13 prior probe scripts replayed unchanged; fresh 311-plant campaign with local and hosted regrade; 369 instances per compiler; coverage; hosted jobs. | R556-7 | 68070cb5723682586c07a6de80a49886732b5dc2 |
| Docs | UNCLEAN (F1) | `CODING_STANDARD.md`, `VERIFICATION.md` (threat model, rule table, pin and generator claims), `CONTRIBUTING.md`, `README.md` links, the PR body Round 8 section, the closed PR #1 body. | R556-7 | 68070cb5723682586c07a6de80a49886732b5dc2 |

## 7. Real limits

- The probes are short compiling forms. I did not search exhaustively. Deliberately obfuscated forms outside the listed rules were not pursued, as the threat model directs.
- Local runs used newer host compilers and binutils than the hosted runner. Hosted runs cover only the unmodified head. I did not run F2 on Ubuntu, but the `-I` versus system-header behaviour and `-Wsign-compare` under `-Wall` are long-standing GCC behaviour.
- No manager source bank exists at this head. Source-head execution evidence is the hosted CI plus this review's runs. I make no claim about the current-dev merge candidate.
- The RV32 evidence is simulator smoke only. Physical calibration NOT RUN. Field skips are not hardware proof.
- I ran no RTL simulation or synthesis, no parent, PP, gPTP, Yosys or builder bank, no container or act, and no hosted replica. Branch `dev-linux` was out of scope.
- The cited standards' full texts were not re-audited. Round 8 changes no requirement or clause claim.

## 8. Pending manager duties

- Return R556-7-F1 and F2 to the author lane. Carry R556-7-RS1 and R556-1-R3 on the residue checklist.
- Own hosted and act acceptance at this head. All four contexts are green: runs 37920179036 and 37920173994.
- Obtain two independent positive reviews.
- At the merge turn, validate the current-dev merge candidate with the builder and native banks, and link their receipts on the PR. The candidate is source base `ae982af85ec97286bd35b39403926d8f0eaec81d` with live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
- Consumer integration, submodule pins and firmware-image identity remain later acceptance. Repository publication is an owner action.

## 9. Packet

- `scripts/setup_toolchain.sh` and `scripts/env.sh`: the reviewer toolchain and environment. `PACKET` must name this directory; set `TSN_REVIEW_PC=isystem` for the bank variant.
- `scripts/launch.sh` and `scripts/wait.sh`: start a long run with its own log and rc file, then wait in the foreground.
- `scripts/probe_assertions.py HEAD_TREE PREV_TREE WORK`: the assertion controls, compiled, run and gated at both heads.
- `scripts/probe_spi_tree.sh HEAD_CLONE SHA WORK`: the in-tree F1 plant with the documented regeneration.
- `scripts/probe_comment_gate.py HEAD_TREE PREV_TREE WORK`: the assembly, linker and include controls.
- `scripts/probe_dependency.sh HEAD_TREE WORK`: the pin-control reversals and the F2 prefix rows.
- `scripts/regrade_xml.py MUTATIONS_JSON CAMPAIGN_DIR`: the per-arm regrade.
- `scripts/replay_prior.sh REVIEWS_DIR HEAD_CLONE SHA REPLAY_DIR CAMPAIGN_DIR`: the byte-unchanged prior replay.
- `scripts/redact_receipts.py`: the location placeholders.
- `receipts/`: raw outputs. Only `REPORT.md` and the files in `MANIFEST.sha256` are published. `scratch/` is not.
- Long runs had their own log and rc files and were awaited in the foreground. There were no source fixes, commits, pushes, GitHub writes, shared installs or edits to other checkouts. The review clone was verified at the exact head after all probes.

R556-7 FINISHED
