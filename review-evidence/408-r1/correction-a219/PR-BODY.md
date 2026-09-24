[A219] Retire gate 1b's text rules onto per-selection grading, `-E`, `-H` and the resolved store census (#408, #409)

## Contents

- **[Status](#status)** -- Tally, compiler environments and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The two issues this closes, executor and reviewers.
- **[Description](#description)** -- The rule-by-rule ledger, and what correction round 1 changed.
- **[Authoritative references](#authoritative-references)** -- Issues, prior PRs, reviews and the page this edits.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules, pinned SDK.
- **[How to validate](#how-to-validate)** -- Commands and expected results in both compiler environments.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What stays a cost, and what a runner without the compiler does not get.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN locally at `ef9034578f97ebc2951801d867b7c57f8196423d`: the first-round commit `a13b6e2e` and three correction commits on dev `759da623`. `408-409-boot-gate-retire` -> `dev`.

| Run | Pinned RV32 SDK mapped (`--require-rv32`) | Every cross compiler hidden |
|---|---|---|
| gate 1b, `sw/builder/test_firmware_compiler.py` | exit 0, 255/255 mutations, 29/29 firmware + 4/4 Makefile edits accepted, 55/55 lexer spellings re-measured, 0 NOT RUN | exit 0, 198/198 mutations, 29/29 + 4/4, 55/55 as recorded, 1 registered NOT RUN |
| dev `759da623`, same driver | 217/217, 17/17 + 4/4 | 182/182, 17/17 + 4/4 |
| whole `sw/builder/test_builder.py` | exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no Vivado report here, as on dev) | exit 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's compiler arm, gate 11) |

## Linked Issue / roles

Closes #408
Closes #409

Executor: `[A209]` (first round), `[A219]` (correction round 1)
Internal cleared-context reviewer: R272
External reviewer: R273

## Description

#504 made both hosted builder consumers require the pinned RV32 SDK, so the instruments PR #498 added beside the text refusals answer wherever a merge is graded. This retires the refusals #408 and #409 name onto those instruments, rule by rule. Where no RV32 compiler answers, a replacement is a registered `NOT RUN` and its mutations are counted as skipped, never as coverage.

**Every preprocessor conditional the pinned GCC reads is graded one arm selection at a time**: each group is resolved to each arm (and to no arm without an `#else`), and each resulting text is graded by the whole gate as a firmware of its own. Groups that ask only whether one macro is defined are graded together, as the builds that exist. The verifier's QSPI-slot group and `#error` guards are left as written; the verifier's other arm is pinned to a literal `printf` and `return 0;`.

**The readers find a conditional exactly where the pinned GCC does, and that is measured.** Correction round 1 answers R272-1 and R273-1:

| Finding | Fix | Controls (each fails with its fix removed) |
|---|---|---|
| R272 F1 BLOCKER: a form feed, vertical tab, NUL or lone CR before `#` hid a product-only arm from every reader while GCC honoured it | one lexer (`c_lexed()`), built to GCC 14.3 `-std=gnu99` as measured, under every C directive reader and every definition reader; `spliced()` rejoins a name a splice splits; trigraphs refused anywhere; a 55-spelling corpus recorded from the pinned GCC, read on every run and re-measured on the compiler | 15 entries with the SDK, 9 without, plus the corpus |
| R272 F2 MAJOR: `-E` compared only eight boot tokens, so a splice or paste rebuilding the identity local passed | the splice and `##` bans KEPT inside the six boot-path bodies and every macro they name; the `-E` retirement narrowed and stated | 13 entries in both modes; `-E` keeps a control it answers first (a boot step erased by a macro of its own name) |
| R272 F3 MINOR: every combination graded, correlated debug code refused and misnamed | groups on one macro related; the selection sentence names what was graded; the remaining cost disclosed with its remedy | two new accepted cases; a store in a related group still refused |
| R272 F4 MINOR: an open quote desynchronised the reader | an open literal ends at its line end as in GCC, and an open literal, a raw string and a trigraph are refused before any reader | 4 entries in both modes |
| R273 F1 MINOR: absent-mode statements overstated | one `#define` per name (H6, H7 refused everywhere); the NOT RUN text, the verdict's first clause and the page name what a compiler-absent runner loses | 4 entries in both modes |

Every R272-1 and R273-1 case was graded at dev, at `a13b6e2e` and at this head, with and without the compiler. With the compiler nothing dev refused is accepted here, and twelve cases dev accepted are refused: the `0 &&` arm behind a form feed, a vertical tab or lone CRs (four cases), the product-last `ADP_EID_LO` arm behind a form feed, two open-quote cases, the struct overlay in a product arm with a plain `#` and behind a form feed, a second `MILAN_ID_MAGIC` as the sample, the verifier's `#else` behind a CR and the pre-AEM clear dropped behind a CR. The four shapes R272-1 listed as pre-existing (`\f#undef`, `\f#pragma`, `\f#include`, `_Pragma` push) were refused at dev only by the compiler; here they are refused on every machine.

The ledger (page rows at 7fd04d45):

| Rule | Verdict | Replacing instrument | Accepted case |
|---|---|---|---|
| no `#if` reaching the six boot-path bodies (565) | RETIRED | per-selection grading: text rules everywhere, `-E`, census and resolver with RV32 | "an #ifdef around a debug printf INSIDE milan_init()"; "a benign statement in an arm the census tree drops, inside configure_fabric()" |
| a conditional carrying `#define`/`#include` (565) | NARROWED to the verifier group and `#error` guards | per-selection grading elsewhere | "an #ifdef/#else choosing a #define, read in a UART command handler" |
| token-joining backslash-newline (564) | NARROWED to the six boot-path bodies | the resolved census outside them | "a token-joining backslash-newline inside a macro body" |
| `##` (585) | NARROWED to the six boot-path bodies and the macros they name | the resolved census outside them | "a ## token paste building a call outside the boot path" |
| `%:` / `??` (585) | KEPT, and a trigraph refused anywhere | none | none |
| read-only `#define` accessor (584) | NARROWED: macro bodies may not name `milan_write()`/`milan_reg()` | the read rules fail closed, one definition per name | "a read-only #define accessor over milan_read()" |
| `#pragma`/`#line`/`#undef`/`#include_next`/extra `#error` (566) | KEPT, reason restated | none | none |
| directory listing pin (568) | RETIRED | `-H`: the path opened and the file it reached | a `README` and a `notes.txt` beside the firmware |
| `#include` name set (567) | KEPT (name pin), `-H` caveat at site and page | none | none |
| ordered pointer-cast, pointer-store and inline-`asm` sets; the reorder cost (563, 583) | RETIRED | resolver store census | the fifth cast, the fifth store, the exchanged pair, the fence |

New costs this round, in the page and the gate print: a second `#define` of any name; an open literal (an apostrophe in an `#if 0` block included) and a raw string; a trigraph anywhere; a continued macro body naming `milan_write()`/`milan_reg()`; a helper split across two conditionals that are not both a bare `defined` test of one macro.

## Authoritative references

- #408 and #409, their bodies and the remaining-scope comments after PR #498.
- R272-1 (https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5802602464) and R273-1 (https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5802871665), with their receipts on the review-evidence branch.
- PR #498 and its reviews; #504 / PR #521 (the pinned SDK and `--require-rv32`); PR #241 (the #153 retirement pattern).
- `docs/integration/BAREMETAL_FIRMWARE.md`: editing contract, cost table, and "Text rules retired onto instruments".

## How to get into the same state

```sh
git fetch origin 408-409-boot-gate-retire && git checkout ef9034578f97ebc2951801d867b7c57f8196423d
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination <sdk-dir> --verify-only   # the pinned SDK
```

## How to validate

```sh
python3 sw/builder/test_firmware_compiler.py --sdk-destination <sdk-dir> --audit /tmp/sdk.jsonl
python3 sw/builder/test_firmware_compiler.py --absent --audit /tmp/absent.jsonl
python3 sw/builder/test_builder.py --require-rv32        # with the SDK at the selector
python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest
python3 -B scripts/docs_check.py && python3 scripts/check_em_dash.py --base 759da623
python3 -B scripts/check_py_idiom.py
```

Expected result / pass criteria: exit 0 everywhere. Gate 1b reports 255/255 with the SDK and 198/198 without it, 29/29 and 4/4 in both, and the 55 lexer spellings read as recorded (re-measured where the compiler answers). Without the compiler the verdict reads `TEXT RULES ONLY, AND WEAKER`, with one registered NOT RUN naming the three instruments and what nothing refuses there.

## Known limitations / out of scope

- Without an RV32 compiler nothing refuses a token-joining splice or a `##` paste outside the six boot-path bodies, a file beside the firmware, a cast, store or `asm` the resolver would place in the window, or an arm only one build compiles whose defect no text rule reads (the `0 &&` choke-point arm). That is a registered `NOT RUN`; the hosted builder jobs require the compiler.
- The lexer is pinned by a fixed corpus, not by a per-firmware compiler oracle: `-fdirectives-only` does not honour NUL before `#` as normal preprocessing does, and normal `-E` is not line-aligned across a multi-line macro invocation. A spelling outside the corpus that GCC reads differently is outside the measurement.
- Pre-existing, measured by both reviews, not changed here and stated as a bound in the page: a plain function-like macro assigning the identity sample between its read and its guard is accepted, at dev and here. R273-S3 (the verifier group's `#else` deleted) is likewise pre-existing and unchanged.
- #409 acceptance 4, the two stores planted inside the address helper: pinned on the helper's return-provenance rule, which answers first on every machine; the resolver's refusal of both on its own sentence is asserted on every compiler run. Both reviews judged this satisfied.
- The `-E` caveat: a macro whose definition differs between the census stub tree and the product is outside the comparison.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (see the ledger and the round-1 table)
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

