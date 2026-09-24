[A254] Retire gate 1b's text rules onto per-selection grading, `-E`, `-H` and the resolved store census, behind a closed lexical subset S that starts with a character allowlist (#408, #409)

## Contents

- **[Status](#status)**: tally, compiler environments and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)**: the two issues this closes, the executors and the reviewers.
- **[Description](#description)**: the rule-by-rule ledger, and what correction rounds 1 to 4 changed.
- **[Authoritative references](#authoritative-references)**: issues, prior PRs, reviews and the page this edits.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: checkout, submodules and the pinned SDK.
- **[How to validate](#how-to-validate)**: commands and expected results in both compiler environments.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what stays a cost, and what a runner without the compiler does not get.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

GREEN locally at the round-four head `4a56ef08`, on dev `759da623`. The branch holds:

- the first-round commit;
- three commits from correction round 1;
- three from correction round 2;
- one from correction round 3;
- one from correction round 4.

`408-409-boot-gate-retire` -> `dev`.

| Run | Pinned RV32 SDK mapped (`--require-rv32`) | Every cross compiler hidden |
|---|---|---|
| gate 1b, `sw/builder/test_firmware_compiler.py` | exit 0, 280/280 mutations, 29/29 firmware + 4/4 Makefile edits accepted, 1845 directive spellings (78 fixed, 1767 generated) and 2520 character-closure cells re-measured, 0 NOT RUN | exit 0, 222/222 mutations, 29/29 + 4/4, 1845 spellings and 2520 cells as recorded, 1 registered NOT RUN |
| round-three head `11b1b86c`, same driver | 271/271, 30/30 + 4/4, 1845/1845 | 213/213, 30/30 + 4/4, 1845/1845 |
| dev `759da623`, same driver | 217/217, 17/17 + 4/4 | 182/182, 17/17 + 4/4 |
| whole `sw/builder/test_builder.py` | exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no Vivado report here, as on dev) | exit 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's registered instruments, gate 11), 0 firmware compiles |

## Linked Issue / roles

Closes #408
Closes #409

Executor: `[A209]` (first round), `[A219]` (correction round 1), `[A234]` (correction round 2), `[A248]` (correction round 3), `[A254]` (correction round 4)
Internal cleared-context reviewer: R272
External reviewer: R273

## Description

#504 made both hosted builder consumers require the pinned RV32 SDK. The instruments PR #498 added beside the text refusals therefore answer wherever a merge is graded. This PR retires the refusals #408 and #409 name onto those instruments, rule by rule. Where no RV32 compiler answers, a replacement is a registered `NOT RUN`, and its mutations are counted as skipped, never as coverage.

**Every preprocessor conditional the pinned GCC reads is graded one arm selection at a time.**

- Each group is resolved to each arm, and to no arm when it has no `#else`. Each resulting text is graded by the whole gate as a firmware of its own.
- Groups that ask only whether one macro is defined are graded together, as the builds that exist.
- The verifier's QSPI-slot group and the `#error` guards are left as written. The verifier's other arm is pinned to a literal `printf` and `return 0;`.

**The gate reads a directive exactly where the pinned GCC does, on a declared lexical subset S, and refuses everything outside it. Since correction round 4, S starts at the character.**

Correction round 4 answers R272-4 and R273-5. Their finding was one MAJOR, and the same one: GCC 14.3 at `-std=gnu99` reads U+00B7, U+0301, U+0387 and U+203F as identifier characters. So `#if`, U+00B7, `x` is one unknown directive that GCC ignores in skipped code, while the readers, stopping a name at `\b`, read `#if`. Round three's S refused `$` and a universal character name and admitted every other character.

The manager's direction was to close S by an allowlist at the character level, not by more denylist entries:

- **The character allowlist, checked first in `assert_within_lexical_subset()`, before any reader, on every machine.**
  - Outside a comment and a string or character literal, a firmware spells printable ASCII (U+0020 to U+007E) and the six characters the readers model as whitespace or a line end: tab, line feed, vertical tab, form feed, carriage return and NUL. Nothing else is admitted.
  - Every other character is refused by name with its code point and line: every non-ASCII character, every other control, and a UTF-8 byte-order mark at offset 0.
  - Inside a comment or a literal, any UTF-8 character is allowed. No reader sees one: the lexer blanks each comment and literal body in the phase-3 view every directive and macro reader reads, and in the code text every other rule reads. The two checks that read raw text, the trigraph ban and the `#include` operand check, match ASCII spellings only.
  - A byte that is not UTF-8 is refused wherever it sits. The firmware read keeps such a byte as an escape so that S names it.
  - The lexer's raw-prefix test now keys on an ASCII set. Every raw literal GCC lexes is therefore one the lexer finds, and no character outside the set moves a comment or literal boundary.
  - The shipping firmware is inside S: printable ASCII, tabs and line feeds only.
- **Readers in ASCII mode.** The shared directive anchor carries `(?a)`, and every other C text reader passes `re.ASCII` or spells explicit ASCII classes. This is defence in depth, measured as such: without the allowlist, the readers disagree with GCC on every extended identifier character tried, where Unicode mode agreed on some by accident. The allowlist is the closure.
- **A generated closure proof.** `_closure_corpus()` builds 2520 cells: every byte value 0 to 255 alone, 20 multi-byte UTF-8 sequences and 4 byte strings that are not UTF-8, each in 9 positions.
  - The positions are: at offset 0 before `#`, in a line's lead before `#`, between `#` and a directive name, inside a directive name, after one, inside an identifier in code, and inside a block comment, a string literal and a character literal.
  - `_CLOSURE_KEPT` records the pinned GCC's answer for every cell.
  - Gate 1b shows each cell refused by S or read as GCC reads it, and re-measures every cell wherever the compiler answers.
  - It also checks that every cell outside the allowlist is refused by the allowlist itself, and that no cell inside it is.
  - Result: 1470 cells are refused by the allowlist; on 43 of those the readers would read differently from GCC. 32 are refused by another rule of S, 1018 are read as GCC reads them, and there are 0 holes. U+00B7 inside a directive name must stay among the cells the allowlist closes: that is the table's negative control.

| Finding | Fix | Controls (each fails with its fix removed) |
|---|---|---|
| R272-4-F1 / R273-5 F1 MAJOR: an extended identifier character in a directive name is inside S, and the readers disagree with GCC on it (`mid.c`, `comb.c`; U+00B7, U+0387, U+203F and U+00A0 in the misnest shape; a store in the CSR window hidden between two such directive names compiles live) | The character allowlist, checked first in S. `re.ASCII` on every C text reader. The generated closure table | 9 allowlist entries in `subset_refusal_corpus` and 9 in the mutation table, 3 byte-order-mark entries re-pinned, and the 2520-cell closure table. Removing the allowlist trips `subset_refusal_corpus` first, on U+00B7 after `#if`. With that bypassed, the closure table trips. With both bypassed, the external review's U+00B7, U+0387 and U+203F stores pass the whole gate without a compiler, and so do 5 more allowlist entries. `mid.c`, `comb.c` and the external review's misnest spellings then pass S and disagree with GCC (22 of the reviews' 89 reader-level spellings) |

**Every reviewer probe of rounds one to four was run again at this head.**

- The 89 reader-level spellings, taken from the reviewers' own files: S refuses 62, and the readers read the other 27 as GCC does.
- The external review's subset probe, run unchanged, reports 0 holes. Its lexer oracle, unchanged, matches its round-three receipt.
- The 233 whole-firmware cases were graded in both modes, and the round-two split-digraph probe with the compiler. Against the round-three head, every verdict that changed went from accepted to refused: the U+00B7, U+0387 and U+203F stores without a compiler, and the byte-order-mark and U+00B7 controls in both modes.

**Correction round 3 (unchanged here) closed the grammar.** It answered R273-4 (a header name in `__has_include(<...>)` hid a line) and R272-3 (a `$` in a directive name). Before any reader, S refuses:

- `$` and universal character names;
- `__has_include`/`__has_include_next`, and a `#include` operand hiding a comment or a backslash;
- digraphs and trigraphs, raw strings, open literals, a block comment no `*/` closes, and the `_Pragma` operator.

The generated lexer corpus is restricted to S. **Correction round 2 (unchanged)** answered R272-2 (a split `%:` digraph) and R273-3 (the byte-order mark and the paste-ban bound) by running translation phases 1 to 3. **Correction round 1 (unchanged)** answered R272-1 F1-F4 and R273-1 F1.

Refusing is never a reduction (acceptance 4). No mutation-table entry is lost, the counts rise to 280 and 222, and the allowlist has its own entries.

The byte-order mark at offset 0, which round two accepted, is a non-ASCII character outside a comment. It is refused now: it moved from the accepted set into the mutation table. The three entries that measured a directive behind it are re-pinned on the allowlist, which refuses the mark first, and the rules they measured keep their other entries.

The ledger (rows in the page's cost table):

| Rule | Verdict | Replacing instrument | Accepted case |
|---|---|---|---|
| no `#if` reaching the six boot-path bodies | RETIRED | per-selection grading: text rules everywhere, `-E`, census and resolver with RV32 | "an #ifdef around a debug printf INSIDE milan_init()"; "a benign statement in an arm the census tree drops, inside configure_fabric()" |
| a conditional carrying `#define`/`#include` | NARROWED to the verifier group and `#error` guards | per-selection grading elsewhere | "an #ifdef/#else choosing a #define, read in a UART command handler" |
| token-joining backslash-newline | NARROWED to the six boot-path bodies | the resolved census outside them | "a token-joining backslash-newline inside a macro body" |
| `##` | NARROWED to the six boot-path bodies and the macros this file defines that they name | the resolved census outside them | "a ## token paste building a call outside the boot path" |
| `%:` / `??`, and the whole closed grammar S, its character allowlist first | KEPT / NEW, read on the whole firmware before any reader and no narrower than dev's | none | none |
| read-only `#define` accessor | NARROWED: macro bodies may not name `milan_write()`/`milan_reg()` | the read rules fail closed, one definition per name | "a read-only #define accessor over milan_read()" |
| `#pragma`/`#line`/`#undef`/`#include_next`/extra `#error`; (round 3) `$`, universal character names, `__has_include`, a `#include` header name hiding a comment, `_Pragma`, an unterminated block comment; (round 4) any character outside the allowlist in code, a byte that is not UTF-8 anywhere | KEPT / NEW, reason restated | none | none |
| directory listing pin | RETIRED | `-H`: the path opened and the file it reached | a `README` and a `notes.txt` beside the firmware |
| `#include` name set | KEPT (name pin), `-H` caveat at site and page | none | none |
| ordered pointer-cast, pointer-store and inline-`asm` sets; the reorder cost | RETIRED | resolver store census | the fifth cast, the fifth store, the exchanged pair, the fence |

Costs, stated in the page and the gate print. None of the closed-grammar and allowlist refusals is spelled by the shipping firmware:

- a second `#define` of any name;
- an open literal (an apostrophe in an `#if 0` block included) and a raw string;
- a trigraph or a digraph anywhere;
- a `$` or a universal character name in an identifier, `__has_include`/`__has_include_next`, a `#include` header name hiding a comment or a backslash, a block comment no `*/` closes, or the `_Pragma` operator;
- (round 4) outside a comment or a literal, any character but printable ASCII and tab, line feed, vertical tab, form feed, carriage return and NUL: an accented letter, U+00B7 or a no-break space in code, a control such as FS, a byte-order mark at offset 0; and a byte that is not UTF-8 anywhere, a comment included;
- a continued macro body naming `milan_write()`/`milan_reg()`;
- a helper split across two conditionals that are not both a bare `defined` test of one macro.

## Authoritative references

- #408 and #409: their bodies and the remaining-scope comments after PR #498. Acceptance 4 (no reduction) governs.
- Round one: R272-1, R273-1. Round two: R272-2, R273-3. Round three: R272-3, R273-4. The reviews are linked on the PR and archived on the review-evidence branch.
- Round four: R272-4 (https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5813156856) and R273-5 (https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5813524739).
- Correction round 4 decision / assignment: https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5813535416. Correction round 3: https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5811522505
- C11 5.1.1.2 (translation phases), 5.2.1 (character sets), 6.4 (lexical elements) and Annex D; GCC 14 gnu99 lexing.
- PR #498 and its reviews; #504 / PR #521 (the pinned SDK and `--require-rv32`); PR #241 (the #153 retirement pattern).
- `docs/integration/BAREMETAL_FIRMWARE.md`: the editing contract, the subset table and the closure table, the cost table, and "Text rules retired onto instruments".

## How to get into the same state

```sh
git fetch origin 408-409-boot-gate-retire && git checkout 408-409-boot-gate-retire
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination <sdk-dir>   # the pinned SDK, with its provenance receipt
```

## How to validate

```sh
python3 sw/builder/test_firmware_compiler.py --sdk-destination <sdk-dir> --audit /tmp/sdk.jsonl
python3 sw/builder/test_firmware_compiler.py --absent --audit /tmp/absent.jsonl
python3 sw/builder/test_builder.py --require-rv32        # with the SDK at the selector
python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest
python3 -B scripts/docs_check.py && python3 scripts/check_em_dash.py --base 759da623
python3 scripts/check_doc_style.py && python3 scripts/gen_toc.py --check && python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py && git diff --check
```

Expected result, the pass criteria:

- Exit 0 everywhere.
- Gate 1b reports 280/280 with the SDK and 222/222 without it, and 29/29 and 4/4 in both.
- The 1845 directive spellings (78 fixed, 1767 generated) and the 2520 character-closure cells read as recorded, and are re-measured where the compiler answers.
- The closure line reports 1470 cells refused by the allowlist (43 of them read differently by the readers and GCC), 32 refused by another rule of S, and 1018 read as GCC reads them.
- Every firmware outside S is refused by name before any reader (`subset_refusal_corpus`: 22 refused, 3 within-S controls accepted), on every machine.
- Without the compiler, the verdict reads `TEXT RULES ONLY, AND WEAKER`, and one registered NOT RUN names the three instruments and what nothing refuses there.

## Known limitations / out of scope

- Without an RV32 compiler, nothing refuses:
  - a token-joining splice or a `##` paste outside the six boot-path bodies;
  - a file beside the firmware;
  - a cast, store or `asm` the resolver would place in the window;
  - an arm only one build compiles whose defect no text rule reads (the `0 &&` choke-point arm).

  That is a registered `NOT RUN`, and the hosted builder jobs require the compiler. The closed grammar S, the character allowlist included, is a text rule and refuses on every machine.
- The readers are exact ON THE SUBSET S, pinned by the two lexer corpora and, at the character level, by the generated closure table, not by a per-firmware compiler oracle. A token-level spelling in neither corpus that GCC reads differently is either outside S (refused) or outside the measurement, and the page and the site say so. At the character level the table covers every byte in every position it names.
- ASCII mode is defence in depth, not a second closure. Without the allowlist, the readers disagree with GCC on extended identifier characters in either mode. That was measured, and the page says so.
- New costs this round: a byte-order mark at offset 0, which GCC drops and round two accepted, is refused now. A byte that is not UTF-8 inside a comment, which GCC accepts, is refused too.
- Pre-existing, stated as a bound in the page, and not changed here (#544): a plain function-like macro, or a paste through a header's macro such as `__CONCAT`, can assign the identity sample between its read and its guard and is accepted, at dev and here. R273-S3 (the verifier group's `#else` deleted) is likewise pre-existing and unchanged.
- #409 acceptance 4, the two stores planted inside the address helper: pinned on the helper's return-provenance rule, which answers first on every machine.
- The `-E` caveat: a macro whose definition differs between the census stub tree and the product is outside the comparison.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (see the ledger and the correction tables)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
