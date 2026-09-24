[A248] Retire gate 1b's text rules onto per-selection grading, `-E`, `-H` and the resolved store census, behind a closed lexical subset (#408, #409)

## Contents

- **[Status](#status)**: tally, compiler environments and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)**: the two issues this closes, the executors and the reviewers.
- **[Description](#description)**: the rule-by-rule ledger, and what correction rounds 1 to 3 changed.
- **[Authoritative references](#authoritative-references)**: issues, prior PRs, reviews and the page this edits.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: checkout, submodules and the pinned SDK.
- **[How to validate](#how-to-validate)**: commands and expected results in both compiler environments.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what stays a cost, and what a runner without the compiler does not get.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

GREEN locally at the round-three head. That is the first-round commit, three commits from correction round 1, three from correction round 2, and correction round 3, on dev `759da623`. `408-409-boot-gate-retire` -> `dev`.

| Run | Pinned RV32 SDK mapped (`--require-rv32`) | Every cross compiler hidden |
|---|---|---|
| gate 1b, `sw/builder/test_firmware_compiler.py` | exit 0, 271/271 mutations, 30/30 firmware + 4/4 Makefile edits accepted, 1845 directive spellings (78 fixed, 1767 generated) re-measured, 0 NOT RUN | exit 0, 213/213 mutations, 30/30 + 4/4, 1845 as recorded, 1 registered NOT RUN |
| round-two head `8e12d31f`, same driver | 264/264, 30/30 + 4/4, 4985/4985 | 206/206, 30/30 + 4/4, 4985/4985 |
| dev `759da623`, same driver | 217/217, 17/17 + 4/4 | 182/182, 17/17 + 4/4 |
| whole `sw/builder/test_builder.py --require-rv32` | exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no Vivado report here, as on dev) | — |

## Linked Issue / roles

Closes #408
Closes #409

Executor: `[A209]` (first round), `[A219]` (correction round 1), `[A234]` (correction round 2), `[A248]` (correction round 3)
Internal cleared-context reviewer: R272
External reviewer: R273

## Description

#504 made both hosted builder consumers require the pinned RV32 SDK, so the instruments PR #498 added beside the text refusals answer wherever a merge is graded. This PR retires the refusals #408 and #409 name onto those instruments, rule by rule. Where no RV32 compiler answers, a replacement is a registered `NOT RUN` and its mutations are counted as skipped, never as coverage.

**Every preprocessor conditional the pinned GCC reads is graded one arm selection at a time.** Each group is resolved to each arm (and to no arm without an `#else`), and each resulting text is graded by the whole gate as a firmware of its own. Groups that ask only whether one macro is defined are graded together, as the builds that exist. The verifier's QSPI-slot group and the `#error` guards are left as written, and the verifier's other arm is pinned to a literal `printf` and `return 0;`.

**The gate reads a directive exactly where the pinned GCC does, on a declared lexical subset S, and refuses everything outside it.** Correction round 3 answers R273-4 and R272-3. Their two findings were one class, the same as rounds one and two: a hand-written reader disagreeing with GCC on a lexical feature it does not model (a header name in `__has_include(<...>)`, and a `$` in a directive name). Rather than extend the readers toward GCC's whole grammar again, the grammar is CLOSED. `assert_within_lexical_subset()` runs before any reader, on every machine, and enumerates the C11 6.4 token classes plus the gnu99 extensions reachable in the firmware, each modelled exactly by the readers or refused by name:

- 6.4.3 universal character names and the gnu `$` in identifiers: REFUSED (a `$` or a `\` in the phase-3 view).
- 6.4.7 header names: modelled only as a plain `#include` operand; `__has_include`/`__has_include_next` and a comment- or backslash-bearing `#include` operand are REFUSED.
- 6.4.6 punctuators: digraphs and trigraphs REFUSED; 6.4.5 raw strings and open literals REFUSED; 6.4.9 a block comment with no `*/` REFUSED; the `_Pragma` operator REFUSED.

A firmware carrying anything outside S is refused, naming the construct, before a reader runs, so no reader ever reads a spelling it would misread. Refusing is never a reduction (acceptance 4): S admits every spelling the shipping firmware uses, and the shipping firmware is inside S. The page and the gate print drop the claim that the readers are exact "because they run GCC's phases in GCC's order"; the claim is now "exact on S; outside S refused".

| Finding | Fix | Controls (each fails with its fix removed) |
|---|---|---|
| R273-4 F1 BLOCKER: a header name in `__has_include(<x/*y>)` in an `#if` hides a line GCC compiles; HI1-HI4 (identity, AEM verdict, ADP enable, CSR store) passed the whole gate with the SDK | `__has_include`/`__has_include_next` refused by S before any reader, on every machine. HI1-HI4 are now refused by S | the 7 `subset_refusal_corpus` entries + 7 mutation entries. Removing the `__has_include` check trips the subset corpus first; with that bypassed the hidden store passes the whole gate on EVERY machine, the SDK included, because the census builds each selection from the gate's own reading |
| R272-3 F1 MAJOR: `$` after a directive name (`#if$a`) is an unknown directive GCC ignores in skipped code while the readers read `#if` | `$` in code refused by S. `dollar_skipped.c` is refused on the subset pin | the `$` subset entry. Removing the `$` check trips the corpus; with it bypassed the misnest store passes without a compiler |

Correction round 2 (unchanged by round 3) answered R272-2 (split `%:` digraph) and R273-3 (byte-order mark, paste-ban bound) by running translation phases 1 to 3. Round 3 keeps those phases and folds the digraph, trigraph, literal and raw-string refusals into the subset check S; the generated corpus is restricted to S (`#` and `##` introducers, the digraph introducers dropped and measured refused in `subset_refusal_corpus` instead), re-recorded against the pinned GCC (4907 -> 1767 spellings). Every reviewer probe of every round is now either refused by S or agrees with GCC.

The reviewers' cases were graded in both modes at the round-three head: R273-4's HI1-HI4 are refused by S, R272-3's `dollar_skipped.c` is refused by S, R272-2's split-digraph probe stays refused, and R273-3's BOM and paste-ban cases are unchanged. With the compiler, nothing dev refused is accepted except the 14 legitimate edits this PR retires rules for.

Correction round 1 (unchanged): R272-1 F1-F4 and R273-1 F1, as in the round-two body.

The ledger (rows in the page's cost table):

| Rule | Verdict | Replacing instrument | Accepted case |
|---|---|---|---|
| no `#if` reaching the six boot-path bodies | RETIRED | per-selection grading: text rules everywhere, `-E`, census and resolver with RV32 | "an #ifdef around a debug printf INSIDE milan_init()"; "a benign statement in an arm the census tree drops, inside configure_fabric()" |
| a conditional carrying `#define`/`#include` | NARROWED to the verifier group and `#error` guards | per-selection grading elsewhere | "an #ifdef/#else choosing a #define, read in a UART command handler" |
| token-joining backslash-newline | NARROWED to the six boot-path bodies | the resolved census outside them | "a token-joining backslash-newline inside a macro body" |
| `##` | NARROWED to the six boot-path bodies and the macros this file defines that they name | the resolved census outside them | "a ## token paste building a call outside the boot path" |
| `%:` / `??`, and the whole closed grammar S | KEPT / NEW, read on the whole firmware before any reader and no narrower than dev's | none | none |
| read-only `#define` accessor | NARROWED: macro bodies may not name `milan_write()`/`milan_reg()` | the read rules fail closed, one definition per name | "a read-only #define accessor over milan_read()" |
| `#pragma`/`#line`/`#undef`/`#include_next`/extra `#error`, and (round 3) `$`, universal character names, `__has_include`, a `#include` header name hiding a comment, `_Pragma`, an unterminated block comment | KEPT / NEW, reason restated | none | none |
| directory listing pin | RETIRED | `-H`: the path opened and the file it reached | a `README` and a `notes.txt` beside the firmware |
| `#include` name set | KEPT (name pin), `-H` caveat at site and page | none | none |
| ordered pointer-cast, pointer-store and inline-`asm` sets; the reorder cost | RETIRED | resolver store census | the fifth cast, the fifth store, the exchanged pair, the fence |

Costs, in the page and the gate print (round 3 adds the closed-grammar refusals, none of which the shipping firmware spells):

- a second `#define` of any name;
- an open literal (an apostrophe in an `#if 0` block included) and a raw string;
- a trigraph or a digraph anywhere;
- a `$` or a universal character name in an identifier, `__has_include`/`__has_include_next`, a `#include` header name hiding a comment or a backslash, a block comment no `*/` closes, or the `_Pragma` operator;
- a continued macro body naming `milan_write()`/`milan_reg()`;
- a helper split across two conditionals that are not both a bare `defined` test of one macro.

## Authoritative references

- #408 and #409: their bodies and the remaining-scope comments after PR #498. Acceptance 4 (no reduction) governs.
- Round one: R272-1, R273-1; round two: R272-2, R273-3; the reviews are linked on the PR and archived on the review-evidence branch.
- Round three: R272-3 (https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5811500607) and R273-4 (https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5811503313).
- Correction round 3 decision / assignment: https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5811522505
- C11 5.1.1.2 (translation phases) and 6.4 (lexical elements); GCC 14 gnu99 lexing.
- PR #498 and its reviews; #504 / PR #521 (the pinned SDK and `--require-rv32`); PR #241 (the #153 retirement pattern).
- `docs/integration/BAREMETAL_FIRMWARE.md`: the editing contract, the subset table, the cost table, and "Text rules retired onto instruments".

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
- Gate 1b reports 271/271 with the SDK and 213/213 without it, 30/30 and 4/4 in both.
- The 1845 directive spellings (78 fixed, 1767 generated) read as recorded, and are re-measured where the compiler answers.
- Every firmware outside the subset S is refused by name before any reader (`subset_refusal_corpus`), on every machine.
- Without the compiler, the verdict reads `TEXT RULES ONLY, AND WEAKER`. One registered NOT RUN names the three instruments and what nothing refuses there.

## Known limitations / out of scope

- Without an RV32 compiler nothing refuses a token-joining splice or a `##` paste outside the six boot-path bodies, a file beside the firmware, a cast, store or `asm` the resolver would place in the window, or an arm only one build compiles whose defect no text rule reads (the `0 &&` choke-point arm). That is a registered `NOT RUN`, and the hosted builder jobs require the compiler. The closed grammar S is a text rule and refuses on every machine.
- The readers are exact ON THE SUBSET S, pinned by two corpora, not by a per-firmware compiler oracle. A spelling in neither corpus that GCC reads differently is either outside S (refused) or outside the measurement, and the page and the site say so.
- Pre-existing, stated as a bound in the page, and not changed here (#544): a plain function-like macro, or a paste through a header's macro such as `__CONCAT`, assigning the identity sample between its read and its guard is accepted, at dev and here. R273-S3 (the verifier group's `#else` deleted) is likewise pre-existing and unchanged.
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
