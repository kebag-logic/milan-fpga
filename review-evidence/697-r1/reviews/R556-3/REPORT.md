[R556] NEGATIVE - exact head 3c350014de990171681b6b3113c70bdc6ace18c6

# R556-3 internal independent review: tsn-c-stack PR #16, round 4 (relates kebag-logic/milan-fpga#697)

- Repository: kebag-logic/tsn-c-stack (private), PR #16, branch `review-fixes` into `main`.
- Exact head `3c350014de990171681b6b3113c70bdc6ace18c6`, tree `16cb118bdd7f71afdb94442c28f38df7316ff4f9`.
- Delta under review: `ccb4ac3..3c35001`, two commits, `a2736b3` (contracts and gate fixes) and `3c35001` (porting links). Base `ae982af`.
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075556732
- Reviewer: R556, internal role, cleared context, own detached clone. No source edits, commits, pushes or GitHub writes.

Verdict: NEGATIVE. Two new MINOR findings are open (R556-3-F1, R556-3-F2).
All five round-2 findings (R556-2-F1/F2/F3, R557-2-F1/F2) are RESOLVED at this head under their original MINOR severity.
The adopted suggestions S2, S3 and S4 are in place. The residue RS1 and RS2 is applied.
The port contracts are restored in full, and a CI check keeps their names in the guide.
Production sources are unchanged. Fresh and reused campaigns catch 311/311 plants by name. Both targets pass locally and on hosted runners.
The open items are new compiling bypasses of the two strengthened gates.
The comment gate misses four comment forms that compile and are not checked.
The needle audit refuses whole gtest default lines but accepts fragments of them, which the grader treats the same way.

## 1. Scope reconstructed

There is no AGENTS.md. I read CONTRIBUTING.md, README.md, CHANGELOG.md, and the changed documents under `docs/`.
On #697 I read the issue body and every manager and owner comment: MIT 6074086970, repository 6074093506, name 6074191062, creation 6074219579, assignment 6074245112, round 2 6074721212, follow-up 6074811248, dual target 6074877336, round 4 assignment 6075324408 and REVIEW READY 6075545653.
I also read the PR #16 body, including its Round 4 section.
I read the full diff `ccb4ac3..3c35001` and both commits. Both commit messages are one line with no body.
`src/`, `include/`, `examples/`, `cmake/` and `CMakeLists.txt` have the same tree IDs at `ccb4ac3` and at the head (`receipts/production_tree_ids.txt`).
The only test change is `tests/test_maap.cpp:375`. The only table change is the needle of `maap-stall-unqueued`.
The milan-fpga evidence tree `2ae0b85/review-evidence/697-r1` holds round-1 material only. It has no receipts for this head.
I read the R556-2 and R557-2 reports only after my own pass over the delta. I then re-ran my round-2 probes and the R557-2 comment probe unchanged.
Branch `dev-linux` was not examined.

## 2. Findings

### R556-3-F1 - MINOR - Conformance, Robustness, Tests, Docs - the comment gate still misses four compiling comment forms

- Where: `scripts/check_comments.py:10` (the token pattern treats any `'` as the start of a character literal, and the literal can span lines), `scripts/check_comments.py:50-54` (only a `#if` directive is tested, and only for a leading `0` followed by a word boundary or by `x0`), and `scripts/check_comments.py:55-57` (every recognised directive line in a `.S` file is skipped whole).
  The claims are `docs/CODING_STANDARD.md:31-32` ("checks every logical comment line, including assembly `#` comments"; "Disabled `#if 0` regions are refused") and `docs/VERIFICATION.md:28` ("Every comment line is checked after line splicing").
- Authority: round 4 item 2 ([6075324408](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6075324408)): "Validate every comment line", "treat `#` lines that are not preprocessor directives as comments", "Refuse `#if 0` in the gated directories". Owner comment rule in [6074811248](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) item B.
- Evidence: `scripts/comment_probes.py`, `receipts/comment_probes.txt`, `receipts/comment_gate_inplace_bypass.txt`, `receipts/asm_define_prose_probe.txt`.
  - A C++14 digit separator masks later comments. `static const unsigned probe_digits = 1'000; // this prose is hidden from the gate`, followed by `static_assert(probe_digits == 1'000);`, passes the gate. The pattern reads `'000; // ... 1'` as one character literal. The tests are C++20, so this compiles.
  - `#elif 0` disables a region and is not refused. `#if 00` (octal zero) and `#if false` (C++) are not refused either.
  - In a `.S` file, an unbalanced assembler character constant (`li a0, 'A`) masks every following `#` prose line up to the next `'`.
  - In a `.S` file, `#define STACK_WORDS 4 # narrative prose about the stack size` is skipped as a directive line. When `STACK_WORDS` expands, the text after `#` is an assembler comment. The RV32 compiler assembles it with `-Wall -Werror` (rc 0).
  - I placed the first three plants in `tests/test_maap.cpp`, `src/adp.c` and `examples/rv32/start.S` of a disposable copy of the head. The gate printed "comments: 23 code files and all mutation fragments pass" (rc 0). The hosted-configuration gcc Debug build and `scripts/baremetal.py` both passed on that copy (rc 0).
  - The shipped tree is clean. All 15 refusal and 11 pass controls of `--selftest` behave as documented, and every round-2 comment probe is now refused (section 3).
- Impact: the gate reports that every comment line passes, but prose comments and a disabled region remain in compiled sources. The claims in CODING_STANDARD and VERIFICATION are false for these forms. Code behaviour is unaffected.
- Required outcome:
  - Tokenise character literals on one line only, and accept C++14 digit separators, so that a `'` cannot mask a later comment. In `.S` files, do not treat `'` as a literal delimiter.
  - Refuse `#elif` with a zero constant as well as `#if`. Treat any zero integer literal (`00`, `0x0`, `0u`) and the C++ `false` the same as `0`.
  - In `.S` files, check any `#` text that follows a directive's operands under the same allowlist. At least check `#define` bodies.
  - Add one planted `--selftest` control for each of these forms. Keep the existing pass controls passing.
- Verification: `python3 scripts/comment_probes.py <tree>` reports `gaps: 0`. The three in-place plants make `scripts/check_comments.py` return 1. The real tree and every existing control still pass.

### R556-3-F2 - MINOR - Robustness, Tests, Docs - the needle audit accepts fragments of gtest default lines

- Where: `scripts/needle_audit.py:20-22`. This is a full-match deny-list on the whole stripped needle. The grader, `scripts/mutation.py:79-82`, matches a needle as a substring of the failure message. The claim is `docs/VERIFICATION.md:27` ("No empty or generic needles, including default GoogleTest value lines").
- Authority: R556-2-F3 and round 4 item 3 ([6075324408](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6075324408)): "The needle audit refuses gtest default lines (`Which is:`, `Expected equality of these values:`, `Actual:`)". Round 2 item 2 ([6074721212](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074721212)): "refuse an empty or generic needle".
- Evidence: `scripts/needle_probes.py`, `receipts/needle_probes.txt`.
  - The audit refuses `'    Which is: 5'`, `'Which is:'`, `'Actual: 4'` and `'Expected equality of these values:'`.
  - It accepts `'is: 5'`, `'5u'`, `'r.frames.size()'`, `'Expected equality'` and `'equality of these values'`. Each is part of the gtest default message for `tests/test_maap.cpp:375` (`receipts/maap_375_kill.txt`).
  - Because the grader matches substrings, `is: 5` grades exactly as the refused `    Which is: 5` did.
  - The current table is clean. All 329 required killers use an assertion's own streamed message. 305 occur in one string literal, and 24 are composed from a literal and a streamed value (`receipts/needle_literal_audit.txt`).
- Impact: removing one word bypasses the regression control that R556-2-F3 asked for. A future table entry could again rest on a value printout or an expression echo. The VERIFICATION claim overstates the control.
- Required outcome: replace the deny-list with a positive rule, or add one beside it. For example, require each needle to occur in a string literal that an assertion in the named test streams. Alternatively, refuse any needle that is a substring of a gtest default-message line. Add planted table controls for `is: 5`, `5u` and an expression echo such as `r.frames.size()`.
- Verification: `python3 scripts/needle_audit.py --selftest` refuses the new controls and passes the real table. `scripts/needle_probes.py` reports every default-line fragment as refused. A fresh campaign still gives 311/311 CAUGHT.

### RESIDUE (wording only; no verdict effect; for the residue checklist)

- R556-3-RS1 - `docs/PORTING.md:40` and `:43` say "Debug builds" and "Release builds". The removed header text named the selector, `NDEBUG`. A bare-metal build without CMake cannot tell which mode it gets.
  Fix line 40: "Builds without `NDEBUG` assert on re-entry. Builds with `NDEBUG` ignore it and increment the lifetime `adp_reentry_count` modulo 2^32."
  Fix line 43: "MAAP guards its instance and counts refused re-entry. Builds without `NDEBUG` also assert."

### SUGGESTION (no verdict effect)

- R556-3-S1 - `tests/test_maap.cpp:375` is the only tab-indented line in a file that indents with four spaces. Re-indent it with spaces when this file is next touched.
- R556-3-S2 - `scripts/check_port_contracts.py` checks only that each name appears in backticks in its section. Only review checks the meanings, such as the NULL case of `env->srp`. A short required phrase per critical contract, such as "NULL stops", would keep the meaning as well as the name.
- R556-3-S3 - `docs/PORTING.md:281` links `https://standards.ieee.org/ieee/1722/5979/`. The other IEEE 1722-2016 references link the working-group page. I could not fetch either IEEE page (challenge page). Use one form throughout.

## 3. Prior findings at this head

| Finding | Original severity | State at 3c35001 | Evidence |
|---|---|---|---|
| R556-2-F1 lost port contracts | MINOR | RESOLVED | `docs/PORTING.md:158-301`. `env->srp`: a non-NULL stream starts reservation and listening, and NULL stops and clears (line 181). This traces to Milan v1.2 5.5.3.5.18 step 4 and 5.5.3.5.36 step 1 (line 185). `ports->admit`, `bound=false` and when the core calls it (bind, unbind, rebind, and `acmp_open` per restored binding) are at lines 170-175. `dest_mac_valid` and `asking_failed` are at 187-188. The `failed` argument of `acmp_tk_registered` is at 192-193. Counter tables exist for ADP (143-156), ACMP (248-266) and MAAP (290-301). I compared every comment that `ccb4ac3` removed from `include/*.h` with PORTING and ARCHITECTURE. Each callback, public-field and precondition statement has a counterpart. The one imprecision is R556-3-RS1. `check_port_contracts.py` runs in `validate.py` and in CI. Its self-test refuses the removal of every listed name (`receipts/validate_gates.txt`, gate `port-contracts` rc 0). |
| R557-2-F1 null-stream SRP obligation | MINOR | RESOLVED | As above, `docs/PORTING.md:181`. The remaining deleted callback obligations were audited (row above). |
| R556-2-F2 assembly `#` prose | MINOR | RESOLVED | My round-2 `gate_probes.sh`, run unchanged: `comment-asm-hash-prose` rc 1 (was 0), and the planted file still assembles. `comment-if0-prose-block` rc 1 (was 0). Five other comment probes rc 1. Eight Linux boundary probes and five RV32 probes rc 1 (`receipts/round2_gate_probes.txt`). Other bypasses of the same requirement are new finding R556-3-F1. |
| R557-2-F2 SPDX-block prose and splicing | MINOR | RESOLVED | The R557-2 `probe_comments.py`, run unchanged: `spdx-block-prose` and `spliced-spdx-prose` give gate rc 1 with compile rc 0. Baseline rc 0, plain prose rc 1. The script's last assertion expected the bypass, and it now fails (`receipts/r557_round2_comment_probe.txt`). The self-test has SPDX-block, decorated-block, splice, delimiter-splice and trigraph-splice controls. |
| R556-2-F3 generic MAAP needle | MINOR | RESOLVED as scoped | `tests/test_maap.cpp:375` carries `<< "both owed frames and ANNOUNCE leave once room returns"`. That text is the needle of `maap-stall-unqueued` (`tests/mutations.json:4409`), and it occurs only on that line. In the campaign XML the plant fails line 375 with that message (`receipts/maap_375_kill.txt`). The audit refuses ten table controls, including `Which is:`, `Expected equality of these values:` and `Actual:`. Fragment bypasses are new finding R556-3-F2. |
| R556-2-S2 unknown test, stale summary | SUGGESTION | ADOPTED | `scripts/mutation.py:46-49` raises for an unknown test inside the per-plant `try`, so the plant records ERROR. Line 94 deletes `results.json` before any other check. The `mutation-controls` gate shows unknown-test ERROR, alone and mixed, and summary removal after a baseline failure. My round-2 `driver_probes.sh`, run unchanged: the genuine plant is CAUGHT; the unrelated-needle, crash and `exit(0)` plants ESCAPE; and the planted stale XML is deleted (`receipts/round2_driver_probes.txt`). |
| R556-2-S3 `assert` gate decisions | SUGGESTION | ADOPTED | No `assert` statement remains under `scripts/`. All 21 gates and `baremetal.py` return 0 under `python3 -O`. |
| R556-2-S4 workflow refs | SUGGESTION | ADOPTED | Both jobs in `.github/workflows/quality.yml` check out `${{ github.event.pull_request.head.sha \|\| github.sha }}`. |
| R556-2-S5 `#if 0` | SUGGESTION | ADOPTED, incomplete | `#if 0`, spliced, digraph and comment-separated forms are refused. `#elif 0`, `#if 00` and `#if false` are not (R556-3-F1). |
| R556-2-S1 header blank runs | SUGGESTION | DEFERRED by the manager | Not assessed. |
| R556-2-RS1 CHANGELOG | RESIDUE | RESOLVED | `CHANGELOG.md:3-11`: one `## Unreleased` section with the bullets. No double blank line. |
| R556-2-RS2 VERIFICATION wording | RESIDUE | RESOLVED | `docs/VERIFICATION.md:60` reads "must stay within the explicit port, memory and integer-helper allowlist". |
| R556-2-RS3 PR body | RESIDUE | RESOLVED (manager) | The PR body names runs 37889967433 and 37889963458 at `ccb4ac3`. |

## 4. Assigned checks

### (1) Contracts and unchanged production

- See R556-2-F1 in section 3. The name check is in `validate.py` (gate `port-contracts`) and in CI.
- `src`, `include`, `examples`, `cmake` and `CMakeLists.txt` have identical tree IDs at `ccb4ac3` and `3c35001`. All 22 core objects are therefore built from identical inputs. R556-2 proved them identical to `086e5d3` under `-g0`.

### (2) Comment gate

- `--selftest`: 15 refusal controls are refused and 11 pass controls pass. The real tree passes (23 code files and all mutation fragments).
- Round-2 probes, re-run unchanged: all are now refused (section 3).
- Independent probes: 15 of 20 behave as required. Five forms are gaps (R556-3-F1).

### (3) Needle and campaign

- Fresh campaign (`python3 -O scripts/validate.py --jobs 16`): `{"CAUGHT": 311, "ESCAPED": 0, "ERROR": 0}`.
- Reused campaign in the same work directory: the same result.
- My XML regrade of both campaigns matches 311/311 plants and all 329 killers by test name and needle (`receipts/regrade_fresh.txt`, `receipts/regrade_reused.txt`, `scripts/regrade.py`).
- Needle audit: R556-3-F2.

### (4) Adopted suggestions

- See S2, S3 and S4 in section 3.

### (5) Residue

- RS1 and RS2 are applied. The manager applied RS3.

### (6) Both targets and hosted CI

- Linux, local: `python3 -O scripts/validate.py --work <scratch> --jobs 16 --graphs` returns 0. All 21 gates are rc 0 (`receipts/validate_gates.txt`, `receipts/validate_gates.json`).
  GCC with coverage, and Clang with ASan, UBSan and leak detection, each run 7 binaries with 369 test instances (`receipts/local_test_instances.txt`).
  Adjusted coverage is 100% lines and branches. Raw ADP is 203/205 lines and 93/100 branches, with the listed exclusions (`receipts/coverage.txt`). Static analysis and three diagram renders pass.
- RV32, local: `python3 -O scripts/baremetal.py --jobs 16` returns 0 (`receipts/baremetal_results.json`). Debug and Release link with `-march=rv32i -mabi=ilp32 -ffreestanding -nostdinc` and have no unresolved symbols.
  Debug imports `__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset` and `port_assert_failed`. Release imports a subset of these. QEMU smoke checks pass in both.
  The round-2 RV32 refusal probes all return 1: `unistd.h`, a heap symbol, an OS symbol, a failing smoke check and a core period defect.
- Hosted, exact head: `gh pr checks 16` shows quality and bare-metal passing in both runs, 37893062871 (pull_request) and 37893059240 (push).
  Every step of both jobs executed and succeeded. None was skipped (`receipts/gh_pr_checks.txt`, `receipts/gh_run_jobs.txt`).
  The quality-evidence artifact of 37893062871 shows 21 gates at rc 0 and 311/311 CAUGHT. Its rv32-evidence artifact shows Debug and Release at rc 0 with empty `unresolved_final` (`receipts/hosted_artifact_summary.txt`).
  I only inspected this evidence. Hosted and act acceptance stay with the manager.

### Documents

- In PORTING, VERIFICATION, CODING_STANDARD, CHANGELOG, ARCHITECTURE and README, no sentence outside tables and code exceeds 25 words. Every relative link resolves (`receipts/doc_lint.txt`). The in-page anchors that PORTING uses exist.
- Claims checked against code: ten needle controls, the port-contract gate, the comment controls, the stale-summary and unknown-test behaviour, and both workflow refs. The comment and needle claims are overstated (F1, F2).
- The PR body Round 4 section matches the local and hosted results. It names no hosted run at this head. Linking runs belongs to the manager.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R556-3-F1) | Round 4 assignment items 1-5; owner rule B and the dual-target rule; PORTING contracts against every comment removed from `include/*.h` in `ccb4ac3`, with the Milan v1.2 5.5.3.5.36, 5.5.4.1 and Table 5.47 references; production tree IDs | R556-3 | 3c350014de990171681b6b3113c70bdc6ace18c6 |
| RTL (C implementation) | CLEAN | `src/`, `include/`, `examples/rv32/` and the CMake targets, unchanged since `ccb4ac3` (same tree IDs); local and hosted RV32 Debug and Release builds, symbol audits and QEMU smoke runs; 369 test instances under GCC and under Clang sanitizers | R556-3 | 3c350014de990171681b6b3113c70bdc6ace18c6 |
| Robustness | UNCLEAN (R556-3-F1, R556-3-F2) | `check_comments.py`, `needle_audit.py`, `mutation.py`, `mutation_selftest.py`, `check_port_contracts.py`, `baremetal.py`, `validate.py`, the workflow; independent and round-2 probes; `python3 -O` runs | R556-3 | 3c350014de990171681b6b3113c70bdc6ace18c6 |
| Tests | UNCLEAN (R556-3-F1, R556-3-F2) | `tests/test_maap.cpp:375`; `tests/mutations.json` (311 plants, 329 killers); fresh and reused campaigns with XML regrade; literal needle audit; self-test controls of all gates; coverage | R556-3 | 3c350014de990171681b6b3113c70bdc6ace18c6 |
| Docs | UNCLEAN (R556-3-F1, R556-3-F2; RS1 residue) | PORTING, VERIFICATION, CODING_STANDARD, CHANGELOG, ARCHITECTURE, README; the PR body Round 4 section; sentence and link lint; claims checked against code | R556-3 | 3c350014de990171681b6b3113c70bdc6ace18c6 |

## 6. Real limits

- I hold no standard texts. I checked the clause references in PORTING against the removed header comments, not against Milan v1.2 or IEEE 1722-2016. The IEEE standard pages could not be fetched (challenge page).
- Object identity at this head rests on identical source tree IDs plus the R556-2 `-g0` proof. I did not recompile `ccb4ac3`.
- Local tools: GCC 16.2.1, Clang 23.1.1, RISC-V GCC 16.2.0, QEMU 11.1.2, CMake 4.4.4, cppcheck 2.22.0, GoogleTest 1.18.0, Python 3.14.7 and Mermaid CLI 11.16.0 (`receipts/tool_versions.txt`). Hosted runners use Ubuntu packages.
- I did not re-judge graph readability. I checked only that the graphs render.
- QEMU smoke checks are simulator evidence. Physical calibration NOT RUN. Host unit tests and field skips are not hardware proof.
- No manager source bank ran at this head, and I claim none. The exact-head execution evidence here is my local runs, the hosted runs I inspected, and the author's published claims.

## 7. Pending manager duties

- Hosted and act acceptance at the head. If wanted, link the exact-head runs 37893062871 and 37893059240 in the PR body.
- The merge-turn current-dev candidate (source base ae982af85ec97286bd35b39403926d8f0eaec81d, live dev 6aa25dec977c6ad78bf4ff6275de47fb81d0c246), with its builder and native banks.
- Carry R556-3-RS1 to the residue checklist.
- Two independent positive reviews are still required. Publication stays an owner action.

## 8. Packet

- Scripts: `scripts/comment_probes.py`, `scripts/needle_probes.py`, `scripts/needle_literal_audit.py`, `scripts/regrade.py`, `scripts/doc_lint.py`, and `scripts/round2-unchanged/` (my round-2 gate and driver probes and the R557-2 comment probe, byte for byte as published).
- Receipts are under `receipts/`. Host paths are removed.
- I never modified the clone. After the probes I verified the head, the tree, the index, and the hashes and modes of all 65 tracked blobs. The repository has no submodule gitlinks (`receipts/clone_integrity_pre_report.txt`).
- `MANIFEST.sha256` lists every published file.

R556-3 FINISHED
