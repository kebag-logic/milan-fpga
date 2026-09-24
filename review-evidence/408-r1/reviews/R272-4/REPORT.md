[R272] NEGATIVE - exact head 11b1b86c11378cac414ef58f6be40d8da00980da

Round R272-4 is the internal, cleared-context independent review of issue #[408, 409] / PR #535 at exact head `11b1b86c11378cac414ef58f6be40d8da00980da` (tree `0f40b320501b88a9a88342d69a15552ddfd946e7`). It covers correction round 3, commit 11b1b86c on 8e12d31f, and the full diff from source base `759da623072358afdb0e9d570a7b4b6a788492c9`.

## Reconstruction

- AGENTS.md sections 3, 6 and 7, and the docs/README authority order.
- The #408 and #409 bodies and their frozen acceptance.
- The manager's scope comments and assignments on #408. This round is governed by the round-3 DECISION (issue comment 5811522505). Gate 1b must first enumerate the C11 6.4 token classes plus the gnu99 extensions that can appear in the firmware, and mark each one as modelled exactly or refused. "Every other class the readers do not model exactly is refused too." A firmware outside S is refused by name before any reader runs. The corpus is restricted to S. The docs must say "exact on S; outside S refused". Acceptance 4 still governs.
- The author's REVIEW READY (issue comment 5812903766).
- The diff 759da623..11b1b86c: `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/testing/CI_WORKFLOWS.md`. The round-3 commit alone is `git diff 8e12d31f..11b1b86c`.

I wrote my own pass and verdict before reading any prior review finding. Receipt `receipts/verdict-before-prior-findings.txt` records it with a timestamp.

## Verdict summary

S closes the two constructs this round was asked to close. `$` and `__has_include`/`__has_include_next` are refused by name before any reader, and so are UCNs, `#include` operands hiding a comment or backslash, `_Pragma`, digraphs, trigraphs, raw strings, open literals and unterminated block comments. Each has a subset-corpus entry and a mutation-table entry, and both pass in both modes. Gate 1b reproduces the author's counts. The shipping firmware is inside S. Acceptance 4 holds: 271/271 with the SDK, 213/213 absent, and the round-3 diff removes no mutation tuple.

S is not closed, however. The pinned GCC 14.3 at `-std=gnu99` accepts extended characters written directly as UTF-8 in identifiers, and therefore in directive names. S neither models nor refuses them. The readers stop a directive name at Python's Unicode `\b`, so for some of these characters they find `#if` where GCC reads one identifier and an unknown directive. This is the same divergence as R272-3-F1 (`$`) through a different identifier character. It contradicts the decision's closure requirement and the page's claim. One MAJOR finding, so the verdict is NEGATIVE.

## Findings

### R272-4-F1 - MAJOR - Conformance, Robustness, Tests, Docs

**Artifact.**
- `sw/builder/test_builder.py:4893-4981`, `assert_within_lexical_subset()`. It checks `$` (`:4940`), a backslash (UCN), `__has_include` (`:4954`), `#include` operands and `_Pragma`, and nothing that detects a non-ASCII identifier character.
- Its docstring at `:4911-4912` says identifiers are "MODELLED, as the `[A-Za-z_][A-Za-z0-9_]*` class every reader keys on". At `:4932` it says "Every other class the readers do not model exactly is refused by one of the rules above".
- The readers that stop a name at `\b` or `\w`, all run on a Python `str`, where `\b` and `\w` are Unicode-aware:
  - `cpp_hash` / `cpp_directive_re` (`:2929`, `:2936`);
  - `directive_re` (`:4039`);
  - `keyed_condition_re` (`:3127`);
  - `macro_definition_re` (`:4794`).
- `subset_refusal_corpus` (`:4988`) has no extended-character entry.
- Docs: `docs/integration/BAREMETAL_FIRMWARE.md:304` (identifiers "modelled" as `[A-Za-z_][A-Za-z0-9_]*`) and `:350-352`: "a spelling they would lex differently is one S refuses before they see it".
- Gate print: `sw/builder/test_builder.py:15187` ("a construct GCC lexes and the readers do not ... is refused by name before any reader").

**Authority and evidence.**
- The manager DECISION on #408 (comment 5811522505), item 1: "Every other class the readers do not model exactly is refused too", and the firmware is refused before any reader.
- Acceptance 4 (no reduction).
- R272-3-F1, the same divergence for `$`.

Measured with the pinned SDK compiler (`riscv32-linux-gcc` 14.3.0, `-std=gnu99 -E -P`) as the oracle and the head's own `_c_phases()` view with the readers' regex. Script `scripts/r3/reader_vs_gcc.py` (round-3 probe, unchanged). Inputs `receipts/probes/{mid,comb,sup2,eacute}.c`. Result `receipts/probes/reader_vs_gcc.txt`. Each input is `#ifdef NEVER / #if<X> / #endif / int evil; / #endif / int z;`:

| `<X>` after `#if` | readers' conditionals | GCC |
|---|---|---|
| U+00B7 MIDDLE DOT + `a` (`mid.c`) | `ifdef, if, endif, endif`: the readers find an `#if` | one identifier `if·a`, an unknown directive ignored in the skipped group; the `#ifdef` closes at line 3 and `evil` is kept (then `#endif without #if`) |
| U+0301 COMBINING ACUTE + `a` (`comb.c`) | `ifdef, if, endif, endif` | same as U+00B7: an identifier character to GCC, not a `\w` to Python |
| U+00B2 (`sup2.c`), U+00E9 (`eacute.c`), controls | `ifdef, endif, endif`: agree with GCC | identifier characters to both |

So on U+00B7 and U+0301 the readers' conditional nesting and GCC's nesting diverge, on text S admits. This is the reader-level shape of R272-3-F1, whose `$` form S now refuses. The directive-set closure also admits the extended names as directives (`if²`, `ifé`).

**Not measured.** I measured this at the reader level with the compiler as the oracle. I did not construct or grade a whole-firmware case, and I do not claim that a store or boot-path change passes the whole gate through it. The finding rests on the stated contract, not on an end-to-end escape: S is declared closed, the readers are declared exact on S, and on these spellings they are not.

**Impact.** Per-selection grading replaces the retired conditional-reach ban and the cast, store and asm sets on the arms without an RV32 compiler, and it is only as sound as the readers' nesting. A construct GCC lexes and the readers do not reaches the readers. That is the class the round-3 decision was written to close, after three rounds of such findings (form feed, split digraph, `$`, `__has_include`). The page and the gate print assert a closure that does not hold.

**Required outcome.** Any identifier character GCC 14.3 accepts at `-std=gnu99` beyond `[A-Za-z0-9_]` is either refused by S by name before any reader, or modelled exactly by every reader. Refusing any non-ASCII character in code outside comments and literals would be the simplest closure; the shipping firmware is expected to spell none, and that should be measured. The subset corpus and the mutation table each carry an entry for it. The docstring, the page (`:304`, `:350-352`) and the gate print state the rule as it runs. The author should also state which other characters S leaves to Python's Unicode `\b`/`\w`, since the readers' regexes are not ASCII-restricted (`re.ASCII` is not set).

**Verification.** Rerun `scripts/r3/reader_vs_gcc.py` on `mid.c` and `comb.c`: either the S check refuses them by its new message, or the readers' conditionals equal GCC's. The new corpus and mutation entries pass in both modes, and gate 1b stays at or above 271/271 SDK and 213/213 absent.

## Prior public findings at this head

These were read after the verdict above was recorded.

| Finding | Status at 11b1b86c | Evidence |
|---|---|---|
| R272-1 F1 BLOCKER (form feed, VT or NUL before `#`) | Resolved (resolved at R272-3; still covered) | The generated corpus crosses these leads (`_LEXER_LEADS`, `:2561`). 1845/1845 match on the SDK (`receipts/gate1b/head-gate1b-sdk.log`) |
| R272-1 F2 MAJOR, F3 and F4 MINOR; R273-1 F1 MINOR | Resolved at R272-2/R272-3. The round-3 commit does not touch their sites apart from F4's literal refusal, which S now calls first (`:4936`) | Round-3 diff; gate passes in both modes |
| R272-2 F1 BLOCKER (split `%:` digraph) | Resolved. Every `%:` is refused by S's digraph refusal before any reader | The subset-corpus entry "the %: digraph of a directive" passes, and so does the gate in both modes. The round-2 whole-gate probe was not re-run this round (see Limits) |
| R273-3 F1 (BOM) and F2 (paste bound) MINOR | Resolved at R272-3. Unchanged | Fixed corpus BOM entry, 1845/1845 |
| R272-3-F1 MAJOR (`$` after a directive name) | Resolved for `$`: `dollar_misnest_store` in the mutation table, SUBSET_DOLLAR_PIN, and my round-3 `dollar_skipped.c` probe, which S refuses via `:4940`. **The class is RETAINED as R272-4-F1** through extended identifier characters | `receipts/probes/reader_vs_gcc.txt` |
| R273-4-F1 BLOCKER (`__has_include` header name) | Resolved on the named construct. `:4954` matches `__has_include(_next)?` in the phase-3 view, where splices are already deleted. Mutation entries `has_include_hidden_store` and `has_include_next_hidden_store` pass in both modes | Gate logs, both modes |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R272-4-F1) | Round-3 DECISION items 1-3 against `assert_within_lexical_subset()` `:4893-4981` and its call at `:9676`. Acceptance 1-5 of #408 and #409 against the gate logs (271/271 SDK, 213/213 absent, 30/30 + 4/4 accepted edits, 1845/1845 spellings, 1 NOT RUN absent). The round-3 diff removes no mutation tuple | R272-4 | 11b1b86c11378cac414ef58f6be40d8da00980da |
| RTL | CLEAN | `git diff --stat 759da623..11b1b86c`: only `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/testing/CI_WORKFLOWS.md`, with no HDL, clocking, CDC or interface file. The gate's RTL-mutant elaborations ran under the verified scoped Verilator 5.050 (`receipts/gate1b/head-verilator-path.txt`) and passed in both modes | R272-4 | 11b1b86c11378cac414ef58f6be40d8da00980da |
| Robustness | UNCLEAN (R272-4-F1) | Malformed or unusual lexical input against S: `_c_phases()` `:2451-2530` (unterminated-comment finding), S checks `:4936-4981`, extended identifier characters measured against GCC | R272-4 | 11b1b86c11378cac414ef58f6be40d8da00980da |
| Tests | UNCLEAN (R272-4-F1) | `subset_refusal_corpus` `:4988-5016` and `assert_subset_refuses()` `:5018` (13 refusals plus one within-S negative control). The generated corpus restricted to `#`/`##` (`:2564-2565`). The new mutation entries. No extended-character case anywhere | R272-4 | 11b1b86c11378cac414ef58f6be40d8da00980da |
| Docs | UNCLEAN (R272-4-F1) | `docs/integration/BAREMETAL_FIRMWARE.md:292-352` (S table and closure claim) and the gate print `:15187`, `:15351`. `docs_check.py`, `check_baremetal_only.py --check`, `check_em_dash.py --base 759da623` and `git diff --check` all exit 0 (`receipts/static.txt`) | R272-4 | 11b1b86c11378cac414ef58f6be40d8da00980da |

## Executed evidence

- SDK installed fresh from the pinned archive and verified: `receipts/sdk-install.txt`, riscv32-linux-gcc 14.3.0.
- Scoped Verilator identity: 5.050 rev v5.050 (`receipts/gate1b/head-verilator-path.txt`).
- Gate 1b at the exact head, run with `scripts/r1/run_gate1b.sh` (round-1 runner, unchanged):
  - with the SDK: `GATE 1b PASS; 0 NOT RUN; 368 actual firmware compiler invocations`, 271/271, 1845/1845 re-measured;
  - absent: `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`, 213/213.
  - Logs and audits are in `receipts/gate1b/`, with the home prefix redacted (`receipts/95-redaction.txt`).
- Reader-versus-GCC probe: `receipts/probes/reader_vs_gcc.txt`.
- Static gates: `receipts/static.txt`.
- Restore check: `receipts/restore-check.txt`. HEAD and tree are exact, the status is empty, there is no diff against the index, and the four submodule gitlinks match HEAD.

## Real limits

- Of my earlier rounds' probes, only these were re-run this round:
  - the round-3 reader probe on `dollar_skipped.c`, now refused by S by code path; its reader/GCC comparison is unchanged in the receipt;
  - the round-1 gate runner in both modes.
- These were not re-run: round 1's `probe_gate1b.py` case files (`cases_r1` to `cases_r4`, `cases_accepted`), its disconnect patches, and round 2/3's whole-gate split-digraph probe (four spellings, two modes). Their scripts are copied unchanged under `scripts/r1`, `scripts/r2` and `scripts/r3` for the next round. Their constructs are covered at this head only by S's own refusal entries and the gate's mutation table, which passed in both modes.
- R272-4-F1 is measured at the reader level only. No whole-firmware case was built or graded.
- No base-tree comparison was run this round. Base 759da623 is unchanged since round 1.
- Not run: full parent/PP/gPTP/Yosys/builder banks, act, hosted jobs, the candidate merge and hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head (the manager's), distinguishing executed jobs from skipped contexts.
- Candidate-merge validation against live dev `eaf0e6c402027112cb0658a4f92016bd9bf9aa9b` at the merge turn.
- A correction round for R272-4-F1, then a re-review of all five lenses at the new head, since a change to S un-covers Conformance, Robustness, Tests and Docs.

R272-4 FINISHED
