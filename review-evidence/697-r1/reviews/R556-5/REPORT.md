[R556] NEGATIVE - exact head 60c911b92825a720044e78bed540752c7dd0368e

# R556-5 internal independent review: tsn-c-stack PR #16, round 6 (relates kebag-logic/milan-fpga#697)

- Head `60c911b92825a720044e78bed540752c7dd0368e`, tree `356130401dbcb3a47184742b9f4973508f2b72eb`, base `main` `ae982af85ec97286bd35b39403926d8f0eaec81d`.
- Delta reviewed: `625b0011..60c911b9`, one commit (`60c911b`). The whole PR against `ae982af` was re-checked for regressions.
- Review start: [6077901124](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6077901124). Assignment: [6076983832](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076983832). REVIEW READY: [6077884025](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6077884025).

## Summary

Verdict: NEGATIVE. Three MINOR findings are open. Each is a compiling form that hides prose from the comment gate while the full gate set and both targets pass.

- **F1**: assembly line splitting differs from the preprocessor and assembler. A form feed before `#` turns an assembler comment into an unchecked "directive".
- **F2**: headers are lexed only as C11, but every test compiles them as C++20. A C++ digit separator hides a `//` comment in `include/wire.h`. The linker script is also lexed as C, so a `'` hides a block comment that the linker reads.
- **F3**: files are chosen by suffix. A `tests/probe.inc` included by a test compiles into `port_tests` and is never scanned.

Everything else in round 6 holds:
- Needle grading is assertion-specific by construction.
- The conditional-region gate compiles both sides of every permitted region.
- Every earlier reviewer probe, run unchanged, reports zero gaps.
- A fresh campaign catches 311/311 plants by name. An independent per-arm XML regrade confirms all 329 killers by streamed message at the owning assertion.
- All 22 Linux gates return 0. GCC and Clang each pass 369 test instances. RV32 Debug and Release link and pass their smoke checks.
- Production sources are byte-identical to `625b0011`.
- Hosted run 37909284956 (pull_request) is green on both jobs. The push-event bare-metal job was cancelled at its 10-minute limit while apt was still downloading packages, before the gate step ran.

Every earlier MINOR is resolved as demonstrated. The three new forms continue the comment-gate class of R556-3-F1 under new IDs.

## 1. Scope reconstructed

- CONTRIBUTING.md and README.md (the repository has no AGENTS.md). Two independent positive reviews are required, plus one-line commits and MIT SPDX. Linux and RV32 are required targets for every change.
- docs/VERIFICATION.md, docs/CODING_STANDARD.md and the other docs.
- Issue #697 body, owner decisions 6074086970, 6074093506, 6074191062, 6074811248 (comment reduction) and 6074877336 (both targets on every change).
- Round 6 assignment 6076983832: close each class by construction.
  1. Clang raw tokens in the file's language mode.
  2. A conditional allowlist with a both-sides compile gate.
  3. Assembly rules: no `'`, every non-directive `#` checked, no `.if*`, `.macro` or `.rept`.
  4. Streamed-message grading, plus needles of at least 8 characters, unique, and not default-template fragments.
  5. Unchanged prior probes report zero gaps, and the campaign gives 311/311.
- Full diff `ae982af..60c911b` and history (7 commits). Round 6 changes 17 files and touches no file in `src/`, `include/` or `examples/`.
- Public evidence: the tree at milan-fpga `2ae0b85` `review-evidence/697-r1/author/` holds the round-6 author gates.json, versions.txt, production-proof.json and PR-BODY.md. Prior reviewer probes come from milan-fpga `00d993b` (provenance below).
- My verdict and ledger were written before I read any prior review finding. The verdict did not change after reconciliation.

## 2. Findings

### R556-5-F1 - MINOR - Conformance, Robustness, Tests, Docs - assembly line model lets a form feed hide a `#` comment

- Where: `scripts/check_comments.py:47-56`. `logical(text).splitlines(keepends=True)` splits on `\f`, `\v`, `\x1c`-`\x1e`, U+0085, U+2028 and U+2029. The C preprocessor and the RV32 assembler treat `\f` and `\v` as in-line whitespace.
  - After `nop \f`, the gate sees a new line starting `#define ...`, classifies it as a directive and checks nothing after the first `#`.
  - The preprocessor passes the whole line through unchanged, and the assembler reads everything after `#` as a comment.
  - The same happens inside a `#define` body: `#define V 4 \f#define words` followed by `.word V`.
- Authority: Round 6 item 3 ("every `#` that does not start a preprocessor directive line, including inside `#define` bodies, begins a comment checked under the allowlist"). `docs/CODING_STANDARD.md:34` ("Every assembly `#` after a preprocessor directive marker starts a checked comment") and the comment row at `docs/VERIFICATION.md:28`.
- Evidence:
  - `probes/hidden_text_probe.py` gives `receipts/hidden_text_probe.txt` and `.json`:
    - rows `asm-formfeed-before-hash`, `asm-define-body-formfeed` and `asm-verticaltab-before-hash` compile with RV32I/ILP32 and `-Wall -Wextra -Werror`;
    - the preprocessed text keeps `# hidden probe words` for the assembler;
    - `check()` returns no error for all three;
    - the control `nop # hidden probe words` is refused.
  - `probes/plant_tree_probe.sh` gives `receipts/plant_tree_probe.txt` (row A). With `nop \f#define hidden probe words` in `examples/rv32/start.S`, `check_comments.py`, `check_conditionals.py`, the GCC and Clang builds with ctest, and `baremetal.py` (Debug and Release link plus QEMU smoke) all return 0.
- Impact: prohibited prose can enter an assembly source while the mandatory gate reports success. The documented assembly rule is not enforced. The shipped tree contains none of these characters (`receipts/shipped_tree_form_scan.txt`).
- Required outcome: the assembly line model must match the preprocessor's. Split only on `\n`, `\r\n` and `\r` after splicing, and treat the other separators as in-line characters (or refuse them in `.S`). Add a compiling `--selftest` control for `nop \f#define words` and one for the `#define` body form.
- Verification: both controls compile and make `check_comments.py --selftest` fail. `probes/hidden_text_probe.py` reports no assembly GAP row. The unchanged prior probes still report zero gaps. Both target jobs pass.

### R556-5-F2 - MINOR - Conformance, Robustness, Tests, Docs - headers and the linker script are lexed in a mode their consumers do not use

- Where:
  - `scripts/check_comments.py:89-91` picks one mode by suffix. `.h` is lexed only as `-x c -std=c11`. `.ld` is lexed as C.
  - `scripts/check_comments.py:95` lexes every mutation fragment as C, including header plants that the campaign compiles into C++ test units.
  - `docs/VERIFICATION.md:47` documents C11 for `.h`.
- What happens:
  - `include/*.h` and `examples/adp_port.h` are compiled as C++20 by every test translation unit, and as C++ by the conditional gate where they test `__cplusplus`.
  - In C11, `'` after a digit opens a character constant. In C++20 it is a digit separator. So `TSN_PROBE_IGNORE(1'2 // words '` followed by `)` holds no comment in C, but `// words '` is a comment in C++. The probe lines build with GCC and Clang in both languages.
  - GNU ld has no character constants. It ignores `'` with a warning, which is not fatal in this build, and reads `/* ... */` as a comment. The C lexer instead reads `' = 1); /* ... */ PROVIDE(x'` as one character constant.
- Authority: Round 6 item 1 ("Take every comment from `clang -cc1 -dump-raw-tokens` in the file's language mode. Check each `comment` token"). `docs/CODING_STANDARD.md:3`: "Public headers also compile as C++20". `docs/CODING_STANDARD.md:32` and `docs/VERIFICATION.md:28`: "Clang 18 raw tokens supply every C11 and C++20 comment". The assignment named C11 for `.h`. Its stated goal, that every comment token reaching a compiler is checked, needs headers lexed in both of their compiled languages.
- Evidence:
  - `receipts/hidden_text_probe.txt`, row `header-cxx-digit-separator`:
    - GCC and Clang compile it as C11 and as C++20;
    - Clang 18's C++20 raw tokens contain the comment and its C11 raw tokens do not;
    - `check()` returns no error;
    - the plain `//` control is refused.
  - `receipts/plant_tree_probe.txt` row A: with the two probe lines in `include/wire.h`, all five checks return 0, and 7/7 CTest binaries pass under GCC and under Clang.
  - Row B: with `PROVIDE(tsn_probe' = 1); /* hidden probe words */ PROVIDE(tsn_probe_end' = 2);` in `examples/rv32/link.ld`, `check_comments.py` and `baremetal.py` return 0. The linker only warns "ignoring invalid character".
- Impact: comments that reach the C++ compiler or the linker are never checked. The documentation claim that every C11 and C++20 comment is supplied by the compiler lexer is not met for headers.
- Required outcome:
  - Lex each header in every language that compiles it (C11 and C++20 for `include/` and `examples/adp_port.h`), and check comment tokens from each mode. Fragments of header plants follow the same rule.
  - For `.ld`, refuse `'` as `.S` does, or make linker warnings fatal (`-Wl,--fatal-warnings`) so the form cannot link.
  - Add one compiling control per form.
  - Update VERIFICATION.md:47 to state the modes used.
- Verification: the header and linker-script controls fail the gate or the build. Rows A and B of `plant_tree_probe.sh` no longer return 0 for the gate or the RV32 build. Existing pass controls still pass.

### R556-5-F3 - MINOR - Conformance, Robustness, Tests, Docs - compiled files outside the suffix list are never scanned

- Where: `scripts/check_comments.py:84-86` scans only `.c .h .cpp .hpp .S .ld` beneath `src`, `include`, `tests` and `examples`. Test sources can include any file, because the boundary gate covers core translation units only. No gate refuses another suffix in these directories.
- Authority: `docs/CODING_STANDARD.md:5` ("The comment gate checks sources, headers, tests, examples and mutation fragments"). Round 6 item 1 ("Check each `comment` token") and the owner comment rule (6074811248).
- Evidence: `receipts/plant_tree_probe.txt` row C. `tests/probe.inc` holds `// hidden probe words`, and `tests/test_port.cpp` includes it. `check_comments.py` returns 0 and reports the same 23 files. The GCC build compiles the file into `port_tests`, and 7/7 binaries pass. The licence and privacy gates also pass.
- Impact: any included text file, or an assembler `.include`, carries unchecked prose into a compiled unit. Today the gated directories contain only scanned suffixes plus `tests/mutations.json` and `tests/coverage.ratchet`, so a closed rule costs nothing now.
- Required outcome: one of the following, with a compiling control for an included `.inc` file:
  - refuse every tracked file in the gated directories whose suffix is neither scanned nor on an explicit data allowlist (`mutations.json`, `coverage.ratchet`);
  - or take the scanned set from the dependency output of every CI build (C, C++ and RV32), so that every file a compiler reads is scanned.
- Verification: row C makes `check_comments.py` fail, and the real tree still passes.

### RESIDUE

- **R556-5-RS1 - Docs - CHANGELOG.md:5-7.** The round 6 entry is an unbulleted paragraph above the bullet list of the same `## Unreleased` section. Exact fix: replace lines 5-8 with one bullet, `- Use compiler comment tokens and compile both sides of permitted conditional regions. Refuse assembly hiding mechanisms. Grade mutations only from delimited assertion messages. Require unique message needles with at least eight characters.`, directly above the existing bullets.

### SUGGESTION (no verdict effect)

- **R556-5-S1 - Tests (hosted).** `.github/workflows/quality.yml:40` gives `bare-metal` 10 minutes. In push run 37909279678, apt was still downloading `qemu-system-misc` (57.7 MB from a slow mirror) when the job was cancelled at 10m17s. The gate step never ran (`receipts/hosted/push_baremetal_cancel.txt`, `run_37909279678.json`). The pull_request run passed the same job in 38 s. Raise the limit or cache the packages, so that a mirror stall does not show as a red required context.
- **R556-5-S2 - Tests (evidence).** `scripts/mutation.py:170-191` grades each arm separately, which is correct. But `failures_all.update()` merges arms by test name into the summary. For `reentry-guard-removed`, the `adp_release` failures overwrite the `adp_debug` ones. The hosted artifact uploads only `results.json`, not the per-arm XML, so 2 of the 329 killers cannot be regraded from hosted evidence (`receipts/hosted_streamed_regrade.txt`). The local per-arm XML confirms both. This has been there since `ae982af`. Key the summary failures by arm, or upload the per-arm XML.

## 3. Round 6 design items at this head

| Item | Result |
|---|---|
| 1. Clang raw tokens | `compiler_tokens.py` runs `-cc1 -dump-raw-tokens` and refuses a non-18 Clang. The regex tokenizer is gone for C and C++, and `assertion_messages.py` uses the same lexer. The dump parser fails closed: a forged location inside a token always ends with the token's real, smaller location, so contiguity fails. The workflow installs `clang-18`; the hosted log shows `comment lexer: /usr/bin/clang-18`. Gaps: F2 (header and linker modes), F3 (file selection). |
| 2. Conditional directives | `conditional_policy.py` refuses `#if`, `#elif`, `#elifdef`, `#elifndef`, `#pragma`, `#line`, unknown directives, unlisted macros, operands on `#else` and `#endif`, redefinition of listed macros, and guard spoofing. Guards must be first, enclose the file, define on the next line and have no `#else`. `check_conditionals.py` compiles every macro combination per file: 38 sides in 22 files, nested-unreachable control refused, assembly sides found as object symbols. Its CI matrix replaces "the CI builds" with a dedicated build set inside the CI job; I accept this as meeting the goal. Clean. |
| 3. Assembly | `'`, `.if*`, `.macro`, `.rept`, `.irp`, `.irpc` and `#pragma` are refused, and `#` text in directive bodies is checked. R557-4's quote form is refused. Gap: F1 (line model). |
| 4. Needles | Markers with fresh 128-bit suffixes delimit each assertion stream in disposable test copies. The grader blanks everything outside them; the default-value control is not counted. The audit requires at least 8 characters, no default-template substring, and exactly one owning literal; `e`, `Failed`, `hich is`, ` equal` and duplicate-message controls are refused. 25 needles and 5 test messages changed; no plant text, path or killer mapping changed. Clean. |
| 5. Controls and campaign | 32 comment controls (25 refused, 7 pass) compile. Prior probes report zero gaps (section 4). Fresh campaign: 311/311 CAUGHT by name. My independent per-arm XML regrade confirms 329/329 killers by streamed text at the owning assertion statement (`receipts/regrade_kills.json`). Hosted campaign: 311 CAUGHT, 327/329 regradable from its summary (S2). Clean apart from F1-F3, which no listed probe exercises. |

## 4. Prior findings at this head

Prior probes ran unchanged against an export of the head. Provenance: `prior-probes/provenance.txt`, with git blob IDs equal to milan-fpga `00d993b` `review-evidence/697-r1/reviews/...`.

| Prior ID | Severity | Disposition | Exact-head evidence |
|---|---|---|---|
| R556-4-F1 (retained R556-3-F1) comment forms | MINOR | RESOLVED as demonstrated; class continues as R556-5-F1 to F3 | `comment_bypass_probe.py`: `gaps: 0 of 11` (`receipts/prior/R556-4_comment_bypass_probe.txt`). Every row is refused with the gate's error. |
| R557-4-F1 (retained R556-3-F1) assembly `'"` operand | MINOR | RESOLVED as demonstrated; class continues as R556-5-F1 | `full_comment_bypass.py`: `bypass: false`, gate refuses, object bytes equal (`receipts/prior/R557-4_full_comment_bypass.json`). Its exit status 1 means "bypass not reproduced". |
| R556-3-F1 original forms | MINOR | RESOLVED | `comment_probes.py`: `gaps: 0`. |
| R556-4-F2 (retained R556-3-F2) generic and default needles | MINOR | RESOLVED | `needle_default_fragments.py`: `accepted default fragments: 0`, single letters refused. `needle_specificity.py`: 329 CAUGHT-BY-MESSAGE, 0 SHARED, 0 MISSING. `needle_probes.py` refuses all 11 values. Grading is now from streamed text only (section 3). |
| R556-4-S1 forms outside the enumerated list | SUGGESTION | ADOPTED | Undefined-macro region, `#if !1`, assembly `#pragma` and `.if 0` are all refused (`R556-4_comment_bypass_probe.txt`, last four rows). |
| R557-4: R556-1-R3 (closed PR #1 body) | RESIDUE | RETAINED as recorded by R557-4 | Not part of this PR. The manager carries it. |
| R556-2-F1 to F3, R557-2-F1 to F2, R556-1-F1 to F3, R557-1-F1 (MAJOR) to F4, and their residue and suggestions | as recorded | RESOLVED, no regression | Their gates (`port-contracts`, `boundary`, `registration-controls`, `mutation-controls`, `traceability`, `test-inventory`) return 0 locally and in hosted run 37909284956. No production, port-contract or requirement file changed in round 6. |
| R556-2-S1 header blank runs | SUGGESTION | DEFERRED by the manager | Not assessed. |

## 5. Executed evidence

| Area | Result | Receipt |
|---|---|---|
| Linux full runner | `validate.py --jobs 12 --graphs` under optimized Python. rc 0, all 22 gates rc 0, 1 min 30 s wall. | `receipts/local-validation/gates.json`, `validate_time.txt` |
| Test instances | 369 GCC (coverage) and 369 Clang (ASan, UBSan), 7/7 CTest each. | `instance_counts.txt`, `gcc-test.log`, `clang-sanitizers-test.log` |
| Coverage | 100% adjusted lines and branches. Per file: ADP 203/205 and 93/100 raw, with the registered exclusions. | `coverage.log` |
| Mutation | 311 CAUGHT, 0 ESCAPED, 0 ERROR, by name. Independent per-arm regrade 329/329. | `mutation_by_name.json`, `regrade_kills.json` |
| Gate controls | 32 comment controls; conditional, needle, report, grading and registration controls. | `comments.log`, `conditionals.log`, `needles.log`, `mutation-controls.log` |
| RV32 | Debug and Release link with no unresolved final symbols; QEMU smoke passes. Core imports are within the documented subset. | `receipts/rv32_results.json`, `rv32_smoke.log` |
| Production identity | All 13 production and port blobs equal `625b0011`. | `receipts/production_blobs.txt` |
| Hosted | Run 37909284956 (pull_request, exact head): quality success with 22 gate rcs 0 and clang-18 lexer, bare-metal success. Run 37909279678 (push): quality success; bare-metal cancelled during apt (S1). | `receipts/hosted/` |
| New probes | 4 GAP rows plus controls refused; in-tree rows A, B and C reproduce. | `receipts/hidden_text_probe.*`, `plant_tree_probe.txt` |
| Clone integrity | Head and tree exact; no untracked or ignored files; 70 tracked blobs match bytes and modes; index matches; 0 gitlinks at base and head. | `receipts/clone_integrity.txt` |

Lexer environment: the host has no Clang 18. I extracted the Ubuntu 24.04 `clang-18` 1:18.1.3-1ubuntu1 packages, the build the hosted runner installs, into scratch, verified them against the archive SHA256 values (`receipts/clang18_packages.sha256`), and passed them through `TSN_CLANG`. Other compilers were host GCC 16 and Clang 23 (`receipts/toolchain_versions.txt`).

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | Round 6 items 1-5 against `compiler_tokens.py`, `check_comments.py`, `conditional_policy.py`, `check_conditionals.py`, `assertion_messages.py`, `mutation.py`, `needle_audit.py`; owner comment rule; issue acceptance; dual-target rule | R556-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| RTL (production code and targets) | CLEAN | `src/`, `include/`, `examples/` blobs unchanged since `625b0011`; GCC and Clang Linux builds; RV32 Debug and Release link, imports, ELF checks and smoke; hosted bare-metal (pull_request) | R556-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| Robustness | UNCLEAN (F1, F2, F3) | Raw-dump parser fail-closed behaviour; assembly line model; language-mode selection; file selection; conditional matrix markers; marker grading and arm handling | R556-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| Tests | UNCLEAN (F1, F2, F3) | 32 comment controls, conditional selftest, grading and report controls, needle controls; fresh 311-plant campaign and independent regrade; 369 instances per compiler; coverage; prior probes; hosted runs | R556-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| Docs | UNCLEAN (F1, F2, F3); RS1 RESIDUE | CODING_STANDARD.md, VERIFICATION.md, CHANGELOG.md, README.md, PR body Round 6, author evidence at `2ae0b85` | R556-5 | 60c911b92825a720044e78bed540752c7dd0368e |

## 7. Real limits

- The probes are short compiling lines in disposable copies. I did not search exhaustively for further forms.
- Unused `#define` bodies and string literals can carry text, but neither is a comment, and the owner rule names comments. I did not treat them as findings.
- No manager source bank exists at this head. Source-head execution evidence is the author's published gate receipts plus this review's own runs. I make no claim about the current-dev merge candidate.
- RV32 evidence is simulator smoke only. Physical calibration NOT RUN. Field skips are not hardware proof.
- I ran no RTL simulation, synthesis, parent, PP, gPTP or builder bank, Docker or act, or hosted replica.
- The author's `versions.txt` at `2ae0b85` does not record the Clang 18 build used for lexing. The hosted log shows `/usr/bin/clang-18`.
- The cited standards' full texts were not re-audited. Round 6 changes no requirement or clause claim.

## 8. Pending manager duties

- Return R556-5-F1 to F3 to the author lane, and carry R556-5-RS1 and R556-1-R3 to the residue checklist.
- Own hosted acceptance. Re-run or accept the cancelled push-event `bare-metal` job of run 37909279678 (S1).
- Obtain two independent positive reviews.
- At the merge turn, validate the current-dev merge candidate (source base `ae982af85ec97286bd35b39403926d8f0eaec81d`; live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`), run the builder and native banks, and link their receipts.
- Consumer integration, pins and firmware-image identity remain later acceptance. Repository publication is an owner action.

## 9. Packet

- `probes/hidden_text_probe.py TREE WORK`: standalone compile-and-gate rows with controls.
- `probes/plant_tree_probe.sh CLONE WORK`: in-tree rows A, B and C against the head's own gates and builds.
- `probes/regrade_kills.py TREE CAMPAIGN_WORK`: per-arm XML regrade by streamed message and assertion location.
- `TSN_CLANG` must name Clang 18.
- `prior-probes/`: unchanged prior scripts with provenance. `receipts/`: raw outputs. Host locations are replaced by placeholders (`receipts/location-redactions.json`).
- All commands ran in the foreground or were awaited. Disposable trees stayed under `scratch/`, which is not published.
- No source fixes, commits, pushes, GitHub writes, shared installs or edits to other checkouts. The clone was verified at the exact head after the probes.

R556-5 FINISHED
