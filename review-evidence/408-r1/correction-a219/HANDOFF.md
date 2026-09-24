# [A219] handoff: PR #535 correction round 1 (#408, #409)

State: REVIEW READY. Not pushed; the PR was not edited (outside this lane's authority).

- Lane: `$LANES/408-409-boot-gate-retire`, branch `408-409-boot-gate-retire`
- Reviewed head: `a13b6e2e461695cdb8d978444ae499a5a6745429`; base dev `759da623`
- New head: `ef9034578f97ebc2951801d867b7c57f8196423d`, three commits, one-line subjects, no trailers:
  - `75066c16` builder: read every gate 1b C directive where the pinned GCC does, keep the splice and ## bans in the six boot bodies, and relate groups on one macro
  - `d8abee3e` builder, docs: bound gate 1b's per-selection grading to the measured lexer, state the narrowed splice and ## bans, the new costs and what a compiler-absent runner loses
  - `ef903457` builder, docs: pin the directive-set closure, include pin, #error count and definition reader behind the spellings the lexer now reads
- Files: `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` (`docs/testing/CI_WORKFLOWS.md` unchanged this round).
- `PR-BODY.md` beside this file replaces the PR body (starts `[A219]`, carries `Closes #408` and `Closes #409`).
- Public: `[A219] REVIEW READY` on #408, https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5805303297 (the only A219 comment; the takeover details are in it).

## Per finding

| Finding | Fix | Controls, each failing when its fix is removed |
|---|---|---|
| R272 F1 BLOCKER (Conformance, Robustness, Tests, Docs) | One lexer, `c_lexed()`, built to the pinned GCC 14.3 at `-std=gnu99` as measured: LF/CRLF/lone-CR line ends; form feed, vertical tab and NUL are whitespace everywhere; comments before `#` on one or several lines; splices in comments, literals and directive names. Every C directive reader reads its view through one anchor, `cpp_hash`: the conditional readers, `#error`, the directive-set closure, the include pin, `#undef`, the keyed-condition reader, the surviving-directive check; and every definition reader goes through `macro_definitions()` (phase-3 text), the macro-body rule included. `spliced()` rejoins a name a splice splits. Trigraphs are not translated (as gnu99) and are refused anywhere. A 55-spelling corpus, recorded from the pinned GCC, is read by the readers on every run and re-measured on the compiler wherever it answers. | 15 table entries with the SDK, 9 without (FF/VT/NUL/CR product arms, `lui`, `0 &&`, dropped pre-AEM clears, verifier `#else` behind CR, `#undef`/`#include`/`#error`/`#define` behind those spellings); the corpus, which fails on its own sentence; the spliced-`#else` arm for the name rejoin |
| R272 F2 MAJOR | The token-joining splice ban and the `##` ban are KEPT inside the six boot-path bodies and every macro they name at any depth (`assert_boot_path_is_spelled()`); the retirement onto `-E` is narrowed and said so at the site, in the page and in the gate print; outside the six bodies both stay retired onto the resolver | 13 entries in both modes (the 10 old splice/paste entries re-pinned onto the kept bans, the identity sample forged by a splice, a paste and a nested paste); `-E` keeps one entry it answers first (a boot step erased by a macro of its own name) |
| R272 F3 MINOR | Groups that ask only whether one macro is defined are graded together as the builds that exist; the selection sentence is `graded as a firmware of its own` and no longer claims the product builds that combination; the remaining cost is a row in the page and in the gate print's COSTS with its remedy | the two correlated debug edits are accepted cases (GREEN both modes) and are refused with the relating removed; a store in the second of two groups on `CSR_UART_BASE` is still refused |
| R272 F4 MINOR | `c_lexed()` ends an open literal at its line end as GCC does, and an open literal, a raw string and a trigraph are refused before any reader runs; the page and the site bound the "every conditional is graded" claim to the measured lexer | 4 entries in both modes (open quotes around a product-only store, a raw string, `??/` ending a comment, the `??=` include re-pinned) |
| R273 F1 MINOR | (a) one `#define` per name, on every machine, which is what refuses H6 and H7; the macro-body rule's reason restated; (b) the registered NOT RUN text, the verdict's first clause and the page's compiler-absent section name the splice and `##` outside the six bodies and the reach ban's compiler half (`0 &&`) | 4 entries in both modes (H6, H7, the spliced `PP_CTRL` redefinition, a second `ADP_CTRL` definition behind a NUL) |

## Evidence

See `receipts/README.md`. Gate 1b at `ef903457`: SDK 255/255, no compiler 198/198 (dev: 217 / 182); 29/29 + 4/4 accepted in both (dev: 17 + 4). Whole builder exit 0 in both modes. 38 static and ratchet commands exit 0. Every R272-1 and R273-1 case graded at base, `a13b6e2e` and this head in both modes (`receipts/probes/SUMMARY.md`): with the SDK, nothing base refused is accepted here, and 12 cases base accepted are refused. Without a compiler, 21 cases base refused are accepted here, each a shape whose replacement needs the compiler; that is the registered NOT RUN, and it is now named where the reviewers asked.

## Decisions a reviewer may want to question

- **Why a corpus, not a per-firmware compiler oracle.** Two oracles were tried and rejected. `-fdirectives-only` is line-aligned and blanks exactly what it reads as a directive, but its scanner does NOT honour NUL before `#`, which normal preprocessing does. Normal `-E` folds a multi-line macro invocation onto its first line, so line alignment gives false refusals. The corpus pins every byte GCC's lexer skips as whitespace and every line end, and is re-measured wherever the compiler answers. A spelling outside it that GCC reads differently would not be caught by the corpus: that is the stated bound.
- **The macro-body rule now reads a continued body whole.** Two old resolver-pinned entries now answer on it on every machine. The cost is disclosed: a continued macro body naming `milan_write()` or `milan_reg()` is newly refused.
- **One definition per name refuses an identical redefinition too.** C allows one; the cost is in the page with its remedy.
- **The spliced `#else` arm.** Without a compiler it is now graded instead of refused by the closed directive set, so it is accepted there, like every other product-only store; with the compiler it is refused.

## Not done, for the manager

- R272-1 and R273-1 both ask for a public Issue for the pre-existing plain function-like macro forging the identity sample (R272 r3, R273 V2c): ACCEPTED at dev and here. It is stated as a bound in the page row; it is not fixed.
- R273-S3 (H8, the verifier group's `#else` deleted) is a SUGGESTION, pre-existing, and not addressed.
- No push, no PR edit, no merge, no act/Docker, no hosted runs, no hardware. Candidate-merge validation against live dev is the manager's.
