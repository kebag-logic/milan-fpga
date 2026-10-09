[R556] NEGATIVE - exact head 625b001173fda5f6401af1dceaef8d8ab86f5ae9

# R556-4 internal independent review: tsn-c-stack PR #16, round 5 (relates kebag-logic/milan-fpga#697)

- Head `625b001173fda5f6401af1dceaef8d8ab86f5ae9`, tree `ac1ad256022bde4758d180a1f938da81ed7cbed6`, base `main` `ae982af85ec97286bd35b39403926d8f0eaec81d`.
- Delta reviewed: `3c350014..625b0011` (commits `e5c9c84`, `625b001`). The whole PR against `ae982af` was re-checked for regressions of every earlier finding.
- Review start: [6076734998](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6076734998). Assignment: [6076492549](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076492549). REVIEW READY: [6076714170](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076714170).

Verdict: NEGATIVE. Two MINOR findings are open. Both retain part of a round-4 finding.
- R556-4-F1 retains R556-3-F1: the comment gate still passes six compiling forms that hide prose in a real comment or a zero-constant disabled region.
- R556-4-F2 retains R556-3-F2: the needle audit still accepts one-letter needles and fragments of GoogleTest default output. A planted needle `e` passes the audit, and its plant is graded CAUGHT.

Everything else assigned for this round is in place:
- RS1, S1, S2 and S3 are done.
- R556-3's probes run unchanged: comment `gaps: 0`, and every default-line fragment in its list is refused.
- A fresh campaign catches 311/311 plants by name, with 329/329 killers regraded independently.
- All 21 Linux gates return 0. RV32 Debug and Release link and pass the smoke checks.
- Both hosted jobs are green at the head.
- Production sources are unchanged, and all 24 core object variants match `main`.

## 1. Scope reconstructed

- CONTRIBUTING.md and README.md (the repository has no AGENTS.md): two independent positive reviews, one-line commits, MIT SPDX, and the Linux and RV32 targets on every change.
- Issue #697: the body, the owner decisions (MIT, own repository, the `tsn-c-stack` name, the comment rule [6074811248](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) item B, and the dual-target rule [6074877336](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336)), and rounds 2 to 5.
- Round 5 acceptance:
  - item 1: comment gate forms, one `--selftest` control per form, and `comment_probes.py` reporting `gaps: 0`;
  - item 2: the positive needle rule plus the deny-list, controls for `is: 5`, `5u` and `r.frames.size()`, `needle_probes.py`, and 311/311 by name;
  - item 3: RS1, S1, S2 and S3.
- PR body, Round 5 section.
- Commit identities: all six PR commits are authored and committed by the holder identity, and each has a one-line subject with no body.
- I made my own pass over the diff before reading any prior review. I then read R556-3 ([6075697881](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075697881)) and the R556-2 and R557-2 finding tables to settle the prior findings (section 3).
- Branch `dev-linux` was not examined.

## 2. Findings

### R556-4-F1 - MINOR - Conformance, Robustness, Tests, Docs - the comment gate still passes compiling forms that hide prose (retains R556-3-F1)

- Where:
  - `scripts/check_comments.py:14`: `PP_NUMBER` starts at any digit, including a digit inside an identifier. It then consumes `'x` as a digit separator, so in `x1'a' /* prose */ 'b'` the gate reads `' /* prose */ '` as a character literal. In C11 there are no digit separators at all.
  - `scripts/check_comments.py:10`: `RAW_STRING` matches `R"` after any identifier character, and in C files too. In `XR"(" /* prose */ ")"` the compiler sees the identifier `XR`, a string, a comment and a string.
  - `scripts/check_comments.py:62`: the zero pattern does not cover zero character constants: `#if '\0'`, `#elif L'\0'`.
- Claims made false by these forms:
  - `docs/CODING_STANDARD.md:32`: "digit separators cannot hide prose. Zero or false `#if` and `#elif` conditions are refused".
  - `docs/VERIFICATION.md:28`: "Digit separators cannot hide comments. Zero or false `#if` and `#elif` conditions ... are refused".
  - `CHANGELOG.md:5`.
- Authority:
  - Round 5 item 1 ([6076492549](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076492549)): "character literals are single-line, and C++14 digit separators (`1'000`) do not open one"; "refuse `#if` and `#elif` with any zero constant".
  - R556-3-F1 required outcome: "so that a `'` cannot mask a later comment".
  - Owner comment rule, [6074811248](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248) item B.
- Evidence: `scripts/comment_bypass_probe.py` and `receipts/comment_bypass_probe.txt`.
  - Each form is appended to a disposable copy of the exact head.
  - It compiles under the project flags: gcc and clang, `-std=c11` or `-std=c++20`, `-Wall -Wextra -Werror`.
  - The planted word does not survive preprocessing, so the compiler treats it as a comment or a disabled region.
  - The repository gate then prints "comments: 23 code files and all mutation fragments pass" (rc 0).

  | Form | File | Compiles (gcc, clang) | Gate |
  |---|---|---|---|
  | `#define V x1'a' /* prose */ 'b'` | `src/adp.c` | yes | pass |
  | same | `tests/test_port.cpp` | yes | pass |
  | `#define TSN_PROBE_R` then `#define S TSN_PROBE_R"(" /* prose */ ")"` (identifier ending in R) | `src/maap.c` | yes | pass |
  | same, as a variable initializer | `tests/test_port.cpp` | yes | pass |
  | `#if '\0'` / prose / `#endif` | `src/acmp.c` | yes | pass |
  | `#if 0x1` / `#elif L'\0'` / prose / `#endif` | `tests/test_port.cpp` | yes | pass |

  - The C-core plants change no object bytes (path-mapped, `-g0`).
  - `receipts/combined_plant_rv32.txt`: with the three core plants and an assembly plant in one copy, the gate returns 0 and `scripts/baremetal.py` returns 0. Debug and Release link with no unresolved symbols, and Release core objects are identical to the unplanted head.
  - What is fixed: R556-3's `comment_probes.py`, run unchanged, reports `gaps: 0` (`receipts/r556-3_comment_probes_rerun.txt`). All 43 refusal and 17 pass self-test controls behave as documented (`receipts/local-comments.log`). The shipped tree is clean.
- Impact: the gate and two documents state that these forms cannot hide prose, but prose can still sit in compiled sources, including the production cores. Code behaviour is unaffected.
- Required outcome:
  - A `'` is a digit separator only inside a pp-number that begins a token (a digit or `.digit` not preceded by an identifier or pp-number character), and only in C++ files. C11 files never treat `'` as a separator.
  - Recognize raw strings only when `R`, `LR`, `uR`, `UR` or `u8R` begins a token, and only in C++ files.
  - Refuse `#if` and `#elif` whose expression is a zero character constant, with or without an encoding prefix.
  - Add one planted `--selftest` control for each of the four forms.
  - An alternative that closes the class is to derive comments from the compiler's own lexer, for example comment-preserving preprocessing of each file in its language mode, instead of a regex tokenizer.
- Verification:
  - `python3 scripts/comment_bypass_probe.py <exported head> <empty dir>` reports no GAP for the six rows above. The three rows marked "outside enumerated forms" fall under S1.
  - R556-3's `comment_probes.py` still reports `gaps: 0`. The real tree and every existing control still pass.

### R556-4-F2 - MINOR - Robustness, Tests - the needle audit still accepts generic needles and default-output fragments (retains R556-3-F2)

- Where: `scripts/needle_audit.py:34-43`.
  - The deny-list is a full match on a few whole lines.
  - The positive rule only requires the needle to be a substring of some message literal of the named test, so any short or common text passes.
  - The grader `scripts/mutation.py:79-82` counts a kill when the needle is a substring of any failure text of that test, default output included.
- Authority:
  - Round 2 item 2 ([6074721212](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074721212)): "must refuse an empty or generic needle, with a planted table entry".
  - R556-3-F2 ("the needle audit accepts fragments of gtest default lines"; impact: "a future table entry could again rest on a value printout"), carried by round 5 item 2.
  - The script's own purpose (line 3): "Refuse missing or generic assertion identifiers".
- Evidence:
  - `receipts/needle_short_fragment_probe.txt`: the audit accepts the one-letter needles `e`, `a` and `s` for the first killer.
  - `scripts/needle_default_fragments.py` and `receipts/needle_default_fragments.txt` try every 3-or-more-character substring of the default GoogleTest failure templates as each of the 329 needles. The audit accepts 130 distinct fragments. Examples: `Failed` (the whole default message of `FAIL()`) for 5 killers, `hich is` and ` equal` for 3, `the` for 242, `ed ` for 291.
  - `receipts/needle_single_letter_campaign.txt`, end to end on a disposable copy: the needle of `reentry-guard-removed` is replaced by `e`. `needle_audit.py --selftest` and the plain audit both return 0. `mutation.py --select` grades the plant CAUGHT, and the first `e` in the failure text is in the default line "Expected equality of these values:".
  - What is fixed: the positive rule exists. The 15 table controls, including `is: 5`, `5u` and `r.frames.size()`, are refused. R556-3's `needle_probes.py`, run unchanged, refuses all 11 values (`receipts/r556-3_needle_probes_rerun.txt`).
  - The current table is clean. `scripts/needle_specificity.py` (`receipts/needle_specificity.txt`) removes every streamed message literal from the campaign's own failure text. No needle still matches, so all 329 killers are matched by message text only.
- Impact: a future table entry can rest on a one-letter or default-output needle, and the campaign will grade any failure of the named test as the required killer. This is the bypass that R556-3-F2 asked to close.
- Required outcome: keep the positive rule, and add one of the following:
  - refuse any needle that is a substring of a default GoogleTest failure template (`Expected equality of these values:`, `Which is: `, `Value of: `, `Actual: `, `Expected: `, `Failed`, `Google Test trace:`);
  - or have `mutation.py` grade a kill only when the needle still occurs after the test's streamed message literals are blanked out of the default text, as `needle_specificity.py` does.

  Add planted table controls for `e`, `Failed`, `hich is` and ` equal`.
- Verification:
  - `needle_default_fragments.py <tree>` reports `accepted default fragments: 0` and refuses the single letters.
  - The single-letter campaign records the plant as ERROR, or the audit returns 1.
  - A fresh campaign still gives 311/311 CAUGHT by name.

### RESIDUE

None.

### SUGGESTION (no verdict effect)

- R556-4-S1 - Forms outside the enumerated round-5 list also pass the comment gate and compile (`receipts/comment_bypass_probe.txt`, rows "outside enumerated forms"):
  - a disabled region guarded by an undefined macro (`#ifdef TSN_PROBE_NEVER`);
  - a non-constant false condition (`#if !1`);
  - `#pragma` prose in `examples/rv32/start.S`, which assembles with `-Wall -Werror`;
  - an assembler `.if 0` region (not counted as a gap by the probe, because the assembler, not the preprocessor, drops it).

  Decide whether disabled regions and inert directives fall under the comment rule. If they do, refuse non-directive text in regions whose condition is not provably taken, and refuse `#pragma` operands outside an allowlist. Deriving comments from the compiler (F1) does not close these forms.

## 3. Prior findings at this head

| Finding | Original severity | State at 625b001 | Evidence |
|---|---|---|---|
| R556-3-F1 comment gate forms | MINOR | RETAINED in part as R556-4-F1 | Enumerated controls landed: digit separators, multiline and CR characters, assembly `'`, `#elif` and `#if` zero and `false`, and `#define` bodies. R556-3 `comment_probes.py` reports `gaps: 0`. Literal-recognition and zero-character forms remain (F1). |
| R556-3-F2 needle fragments | MINOR | RETAINED in part as R556-4-F2 | The positive rule and the `is: 5`, `5u` and `r.frames.size()` controls landed. `needle_probes.py` refuses all 11 values. One-letter and default-output fragments remain accepted (F2). |
| R556-3-RS1 NDEBUG wording | RESIDUE | RESOLVED | `docs/PORTING.md:40` and `:43` name `NDEBUG`. `check_port_contracts.py` requires both phrases. |
| R556-3-S1 tab at test_maap.cpp:375 | SUGGESTION | ADOPTED | `tests/test_maap.cpp:375` uses spaces. No tab remains in `tests/`. |
| R556-3-S2 critical contract phrases | SUGGESTION | ADOPTED | `scripts/check_port_contracts.py:254-266` and `:276-281` require 14 phrases, including "NULL stops listening" beside `env->srp`. 14 meaning-removal controls are refused (`receipts/local-port-contracts.log`). |
| R556-3-S3 one IEEE 1722-2016 link form | SUGGESTION | ADOPTED | All 19 IEEE 1722-2016 links in Markdown and JSON use `https://standards.ieee.org/ieee/1722/5979/`. No other form remains. |
| R556-2-F1 / R557-2-F1 port contracts, NULL SRP | MINOR | RESOLVED, no regression | `docs/PORTING.md:173`, `:181`, `:187-188`, `:192`. The gate requires the names and the critical meanings. |
| R556-2-F2 assembly `#` prose | MINOR | RESOLVED, no regression | Self-test controls and R556-3 probes refuse the plants. |
| R557-2-F2 SPDX-block prose, splicing | MINOR | RESOLVED, no regression | R556-3 `comment_probes.py`: SPDX-block and splice probes are refused. |
| R556-2-F3 generic MAAP needle | MINOR | RESOLVED, no regression | Line 375 carries its own message, and the plant is caught by it. |
| R556-2-S2 to S4, RS1 to RS3 | SUGGESTION / RESIDUE | Adopted or resolved | `mutation-controls` gate rc 0. Optimized-Python self-tests rc 0 (`receipts/optimized_python_selftests.txt`). Both workflow jobs check out the same ref. |
| R556-2-S5 `#if 0` | SUGGESTION | Superseded by R556-3-F1 and R556-4-F1 | |
| R556-2-S1 header blank runs | SUGGESTION | DEFERRED by the manager | Not assessed. |
| R557-1-F1 stale XML (MAJOR), R557-1-F2 to F4, R556-1-F1 to F3 | MAJOR / MINOR | RESOLVED, no regression | Gates `mutation-controls`, `boundary`, `registration-controls`, `traceability` and `test-inventory` return rc 0 with their controls. DEV-08 and PORTING "ADP input validation" are present, and the per-standard links are present. |
| R556-1-R1 to R4, S1 to S4 | RESIDUE / SUGGESTION | As recorded by R556-2, no regression | |

## 4. Assigned checks

1. **Comment gate.**
   - Single-line characters, separators, CR handling, assembly `'`, `#if` and `#elif` zero and `false`, and `#define` and `#pragma` trailing `#` text: each has a control, and all pass.
   - The real tree and the SPDX and tracing pass controls pass.
   - Remaining forms: F1 and S1.
2. **Needle audit.**
   - The positive rule, the deny-list and the 15 controls are in place, and `needle_probes.py` refuses everything in its list.
   - The `validate.py` campaign is fresh: 311/311 CAUGHT, names equal to the table (`receipts/campaign_by_name.txt`).
   - The independent regrade gives 311 caught with 329 killers (`receipts/regrade_fresh_campaign.txt`), and R556-3's literal audit finds 329/329 in one literal.
   - Remaining gap: F2.
3. **RS1 and S1 to S3:** all done (section 3).
4. **Both targets.**
   - Linux: `scripts/validate.py --jobs 16 --graphs` returns 0 for all 21 gates (`receipts/validate_gates.json`).
     - GCC with coverage and Clang with ASan and UBSan each pass 7/7 CTest binaries, 369 registered instances.
     - Adjusted coverage is 100% lines and branches.
     - Static analysis and three diagram renders pass.
     - The largest single process stayed at 0.45 GB resident.
   - RV32: `scripts/baremetal.py` builds Debug and Release, links with no unresolved symbols, and passes the QEMU smoke checks (`receipts/baremetal_results.json`).
   - Production:
     - The `src/`, `include/` and `examples/` trees at the head equal those at `ccb4ac3`, `a2736b3` and `3c35001`.
     - Core objects equal `main` `ae982af` in 24 of 24 variants: gcc and clang, `-O0` and `-O2`, with and without `NDEBUG`, `-g0`, path-mapped (`receipts/core_objects_vs_main.txt`).
   - Docs: 249 of 251 Markdown line links name the declared test or line text. The other two are free-text links in STATIC_ANALYSIS.md, checked by hand: `src/maap.c:262` (`decode`) and `examples/rv32/smoke.c:137` (`p.room = true`).
   - Hosted at the head: `gh pr checks` shows 4 passed and 0 failed.
     - Runs 37900893378 (pull_request) and 37900889048 (push) have `head_sha` `625b001`. In both, the `quality` and `bare-metal` jobs executed every step with success.
     - The pull_request artifacts show 21 gates at rc 0, 311/311 CAUGHT, and RV32 Debug and Release at rc 0 with nothing unresolved (`receipts/hosted_artifact_summary.txt`).
     - Hosted acceptance remains the manager's.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Owner comment rule against `scripts/check_comments.py` and compiled plants. Clause links in REQUIREMENTS, TRACEABILITY, DEVIATIONS, PORTING and `requirements.json` (one form per standard). DEV-08 and the ADP limits. | R556-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| RTL (production code and targets) | CLEAN | `src/`, `include/` and `examples/` tree IDs unchanged since `ccb4ac3`. 24/24 core objects equal `main`. RV32 Debug and Release link and smoke. Hosted `bare-metal` job. | R556-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| Robustness | UNCLEAN (F1, F2) | Comment tokenizer and directive checks. Needle audit and grader. `assertion_messages.py` inventory. Per-plant needle ERROR path in `mutation.py`. Optimized-Python behaviour. | R556-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| Tests | UNCLEAN (F1, F2) | Self-tests of the comment, needle and port-contract gates. Fresh 311-plant campaign with independent regrade and specificity grading. 369 instances under GCC and Clang with sanitizers. Coverage. Mutation and registration controls. | R556-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |
| Docs | UNCLEAN (F1) | CODING_STANDARD, VERIFICATION, PORTING, REQUIREMENTS, TRACEABILITY, DEVIATIONS, CHANGELOG and the PR body Round 5 section. 251 line links. | R556-4 | 625b001173fda5f6401af1dceaef8d8ab86f5ae9 |

## 6. Real limits

- No manager source bank runs at this head. Source-head execution evidence is the author's published gate receipts, plus my local runs and the hosted runs listed above. I claim no manager bank.
- My local toolchain is newer than the hosted Ubuntu 24.04 runner (`receipts/tool_versions.txt`). Hosted parity rests on the two hosted runs.
- The RV32 smoke checks run on QEMU only. No hardware or physical calibration was run, and none applies to this repository.
- I hold no standard text. Clause and link checks are of form and consistency, not of standard content.
- The R557-4 review runs independently. I did not read it.

## 7. Pending manager duties

- Return R556-4-F1 and R556-4-F2 to the author lane.
- Own hosted acceptance at this head.
- At the merge turn, validate the current-dev merge candidate (source base `ae982af`; live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246` on milan-fpga), run the builder and native banks, and link their receipts.
- Obtain the second independent review.
- No residue items to carry.

## 8. Packet

- `scripts/`: `comment_bypass_probe.py`, `needle_default_fragments.py`, `needle_specificity.py` and `line_links.py`. Each takes the tree root, and `comment_bypass_probe.py` also takes an empty work directory.
- `receipts/`: raw outputs, including the unchanged re-runs of R556-3's probe scripts. Their provenance and hashes are in `receipts/r556-3_scripts_provenance.txt`.
- `MANIFEST.sha256` lists every published file.
- Clone integrity after probes (`receipts/clone_integrity_final.txt`): the clone is at the exact head with no untracked or ignored files. The worktree and index match HEAD bytes and modes. There are no submodule gitlinks.

R556-4 FINISHED
