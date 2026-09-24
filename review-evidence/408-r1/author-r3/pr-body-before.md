Retire gate 1b's text rules onto per-selection grading, -E, -H and the resolved store census
8e12d31fefa7df0abb4d9474d0412ce123ac9644 draft=false
[A234] Retire gate 1b's text rules onto per-selection grading, `-E`, `-H` and the resolved store census (#408, #409)

## Contents

- **[Status](#status)**: tally, compiler environments and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)**: the two issues this closes, the executors and the reviewers.
- **[Description](#description)**: the rule-by-rule ledger, and what correction rounds 1 and 2 changed.
- **[Authoritative references](#authoritative-references)**: issues, prior PRs, reviews and the page this edits.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: checkout, submodules and the pinned SDK.
- **[How to validate](#how-to-validate)**: commands and expected results in both compiler environments.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what stays a cost, and what a runner without the compiler does not get.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

GREEN locally at `8e12d31fefa7df0abb4d9474d0412ce123ac9644`. That is the first-round commit `a13b6e2e`, three commits from correction round 1 (to `ef903457`) and three from correction round 2, on dev `759da623`. `408-409-boot-gate-retire` -> `dev`.

| Run | Pinned RV32 SDK mapped (`--require-rv32`) | Every cross compiler hidden |
|---|---|---|
| gate 1b, `sw/builder/test_firmware_compiler.py` | exit 0, 264/264 mutations, 30/30 firmware + 4/4 Makefile edits accepted, 4985/4985 directive spellings (78 fixed, 4907 generated) re-measured, 0 NOT RUN | exit 0, 206/206 mutations, 30/30 + 4/4, 4985/4985 as recorded, 1 registered NOT RUN |
| round-two head `ef903457`, same driver | 255/255, 29/29 + 4/4, 55/55 | 198/198, 29/29 + 4/4, 55/55 |
| dev `759da623`, same driver | 217/217, 17/17 + 4/4 | 182/182, 17/17 + 4/4 |
| whole `sw/builder/test_builder.py` | exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no Vivado report here, as on dev) | exit 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's compiler arm, gate 11) |

## Linked Issue / roles

Closes #408
Closes #409

Executor: `[A209]` (first round), `[A219]` (correction round 1), `[A234]` (correction round 2)
Internal cleared-context reviewer: R272
External reviewer: R273

## Description

#504 made both hosted builder consumers require the pinned RV32 SDK, so the instruments PR #498 added beside the text refusals answer wherever a merge is graded. This PR retires the refusals #408 and #409 name onto those instruments, rule by rule. Where no RV32 compiler answers, a replacement is a registered `NOT RUN` and its mutations are counted as skipped, never as coverage.

**Every preprocessor conditional the pinned GCC reads is graded one arm selection at a time.** Each group is resolved to each arm (and to no arm without an `#else`), and each resulting text is graded by the whole gate as a firmware of its own. Groups that ask only whether one macro is defined are graded together, as the builds that exist. The verifier's QSPI-slot group and the `#error` guards are left as written, and the verifier's other arm is pinned to a literal `printf` and `return 0;`.

**The readers find a conditional exactly where the pinned GCC does, because they read the text GCC's translation phases build, in GCC's order.** Correction round 2 answers R272-2 and R273-3. The two BLOCKERs of rounds one and two were one class: a directive reader disagreeing with GCC's translation phases. So the phases are now run, not approximated. `_c_phases()` runs phases 1 to 3 as GCC 14.3 runs them at `-std=gnu99`:

1. Phase 1 drops a byte-order mark at offset 0 and ends a line at LF, CRLF or a lone CR. It does not replace trigraphs.
2. Phase 2 deletes every splice.
3. Phase 3 lexes the result, with `%:` and `%:%:` read as `#` and `##` by maximal munch.

Every C directive reader reads that one view through one anchor and maps back to the source for its messages: the conditional readers, `#error`, the directive-set closure and include pin, `#undef`, the keyed-condition reader, the definition reader, and the `-E` comparison's second row.

| Finding | Fix | Controls (each fails with its fix removed) |
|---|---|---|
| R272-2 F1 BLOCKER: `%\`, a line end, then `:ifdef` hid a product-only arm from every reader and from the kept `%:` ban | the phases above under every reader. The digraph ban reads the whole firmware before any reader, on the phase-3 tokens, and also refuses a `%:` pair phase 3 reads as other tokens (`<%:`), so it is no narrower than dev's. A generated corpus of 4907 firmwares crosses every splice position (inside `%:`, the directive name and the macro name included) with every introducer (`#`, `%:`, and each after a form feed, a vertical tab, a NUL or blanks, plus six non-introducers), recorded from GCC 14.3 and re-measured wherever it answers | 4 table entries (split-digraph arm, plain-digraph arm, split `%:%:` paste, `<%:`). A census entry grading the product's selection of the split-digraph arm, and an in-code assertion that the readers find it. The generated corpus. Reverting the phase order stops the gate on the assertion and on the generated corpus; the fixed corpus alone passes. With the unread-pair check also removed, the split-digraph arm passes the whole gate on every machine |
| R273-3 F1 MINOR: a BOM at offset 0 hid a `#define` (and, pre-existing, an `#include` and a `#line`) | phase 1 drops the mark as GCC does. The fixed corpus gains R273-3's 20 extra spellings and three more behind a BOM (78 in all) | 3 table entries (identity forged behind a BOM, `#include` and `#line` behind one). The fixed corpus. An accepted case: a BOM alone. With the mark kept, the forgery passes the whole gate on every machine |
| R273-3 F2 MINOR: the page claimed the paste ban reads every macro the six bodies name | the rows, the site and the gate print say it reads this file's own `#define`s. A paste through a header's macro (`__CONCAT`) is outside it, the bound of #544. The sentence is a required page claim | a doc mutation claiming the ban reads a header's macro |

The reviewers' cases were graded in both modes: R272-2's split-digraph probe, R273-3's BOM and extra cases, and the 74 published round-one and round-two cases. All four R272-2 spellings are refused with the SDK. Nothing round two refused is accepted here, in either mode. With the compiler, nothing dev refused is accepted except the 14 legitimate edits this PR retires rules for.

Correction round 1 (unchanged by round 2):

| Finding | Fix |
|---|---|
| R272-1 F1 BLOCKER: a form feed, vertical tab, NUL or lone CR before `#` | now subsumed by the phases above; the corpus pins each spelling |
| R272-1 F2 MAJOR: `-E` compared only eight boot tokens | the splice and `##` bans KEPT inside the six boot-path bodies and every macro this file defines that they name |
| R272-1 F3 MINOR: every combination graded | groups on one macro related; the selection sentence names what was graded |
| R272-1 F4 MINOR: an open quote desynchronised the reader | an open literal ends at its line end; an open literal, a raw string and a trigraph are refused before any reader |
| R273-1 F1 MINOR: absent-mode statements overstated | one `#define` per name; the NOT RUN text, the verdict and the page name what a compiler-absent runner loses |

The ledger (rows in the page's cost table):

| Rule | Verdict | Replacing instrument | Accepted case |
|---|---|---|---|
| no `#if` reaching the six boot-path bodies | RETIRED | per-selection grading: text rules everywhere, `-E`, census and resolver with RV32 | "an #ifdef around a debug printf INSIDE milan_init()"; "a benign statement in an arm the census tree drops, inside configure_fabric()" |
| a conditional carrying `#define`/`#include` | NARROWED to the verifier group and `#error` guards | per-selection grading elsewhere | "an #ifdef/#else choosing a #define, read in a UART command handler" |
| token-joining backslash-newline | NARROWED to the six boot-path bodies | the resolved census outside them | "a token-joining backslash-newline inside a macro body" |
| `##` | NARROWED to the six boot-path bodies and the macros this file defines that they name | the resolved census outside them | "a ## token paste building a call outside the boot path" |
| `%:` / `??` | KEPT, read on the whole firmware after phase 2 and no narrower than dev's; a trigraph refused anywhere | none | none |
| read-only `#define` accessor | NARROWED: macro bodies may not name `milan_write()`/`milan_reg()` | the read rules fail closed, one definition per name | "a read-only #define accessor over milan_read()" |
| `#pragma`/`#line`/`#undef`/`#include_next`/extra `#error` | KEPT, reason restated | none | none |
| directory listing pin | RETIRED | `-H`: the path opened and the file it reached | a `README` and a `notes.txt` beside the firmware |
| `#include` name set | KEPT (name pin), `-H` caveat at site and page | none | none |
| ordered pointer-cast, pointer-store and inline-`asm` sets; the reorder cost | RETIRED | resolver store census | the fifth cast, the fifth store, the exchanged pair, the fence |

Costs, in the page and the gate print:

- a second `#define` of any name;
- an open literal (an apostrophe in an `#if 0` block included) and a raw string;
- a trigraph anywhere;
- a continued macro body naming `milan_write()`/`milan_reg()`;
- a helper split across two conditionals that are not both a bare `defined` test of one macro.

Correction round 2 adds no cost. A byte-order mark at offset 0 is accepted.

## Authoritative references

- #408 and #409: their bodies and the remaining-scope comments after PR #498. Acceptance 4 (no reduction) governs.
- Round one:
  - R272-1: https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5802602464
  - R273-1: https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5802871665
- Round two:
  - R272-2: https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5807262250
  - R273-3: https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5807558369
- The receipts for every review are on the review-evidence branch.
- Correction round 2 assignment: https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5807562819
- C11 5.1.1.2, the translation phases.
- PR #498 and its reviews; #504 / PR #521 (the pinned SDK and `--require-rv32`); PR #241 (the #153 retirement pattern).
- `docs/integration/BAREMETAL_FIRMWARE.md`: the editing contract, the cost table, and "Text rules retired onto instruments".

## How to get into the same state

```sh
git fetch origin 408-409-boot-gate-retire && git checkout 8e12d31fefa7df0abb4d9474d0412ce123ac9644
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

Expected result, the pass criteria:

- Exit 0 everywhere.
- Gate 1b reports 264/264 with the SDK and 206/206 without it, 30/30 and 4/4 in both.
- The 4985 directive spellings (78 fixed, 4907 generated) read as recorded, and are re-measured where the compiler answers.
- Without the compiler, the verdict reads `TEXT RULES ONLY, AND WEAKER`. One registered NOT RUN names the three instruments and what nothing refuses there.

## Known limitations / out of scope

- Without an RV32 compiler nothing refuses a token-joining splice or a `##` paste outside the six boot-path bodies, a file beside the firmware, a cast, store or `asm` the resolver would place in the window, or an arm only one build compiles whose defect no text rule reads (the `0 &&` choke-point arm). That is a registered `NOT RUN`, and the hosted builder jobs require the compiler.
- The readers are pinned by two corpora, not by a per-firmware compiler oracle. `-fdirectives-only` does not honour NUL before `#` as normal preprocessing does, and normal `-E` is not line-aligned across a multi-line macro invocation. The generated corpus enumerates every splice position against every introducer rather than listing spellings. Still, a spelling in neither corpus that GCC reads differently is outside the measurement, and the page and the site say so.
- Pre-existing, stated as a bound in the page, and not changed here (#544): a plain function-like macro, or a paste through a header's macro such as `__CONCAT`, assigning the identity sample between its read and its guard is accepted, at dev and here. R273-S3 (the verifier group's `#else` deleted) is likewise pre-existing and unchanged.
- #409 acceptance 4, the two stores planted inside the address helper: pinned on the helper's return-provenance rule, which answers first on every machine. The resolver's refusal of both on its own sentence is asserted on every compiler run.
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

