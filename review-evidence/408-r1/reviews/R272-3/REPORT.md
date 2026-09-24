[R272] NEGATIVE - exact head 8e12d31fefa7df0abb4d9474d0412ce123ac9644

Round R272-3, internal cleared-context review of PR #535 (issues #408 and #409) at tree `73a2836b0fffdedb294675d75c61167eb446ceb8`. The review covers correction round 2 (commits 8fd74a99, 479a2175 and 8e12d31f on ef903457), with the full diff from 759da623.

## Verdict

The correction fixes what it was asked to fix:
- **R272-2 F1 BLOCKER (split digraph):** resolved. The prior round's probe is refused in all four spellings, in both modes.
- **R273-3 F1 (BOM):** resolved.
- **R273-3 F2 (paste-ban bound):** resolved.

Gate 1b reproduces the author's counts in both modes. The directive readers now read one phase-1-to-3 view (`_c_phases()`, `sw/builder/test_builder.py:2420-2525`). The old approximations are gone: `c_lexed`, `spliced` and `closed_splices` were removed, and `line_spliced` is kept only for make. The digraph ban reads the phase-3 tokens and also refuses any unread `%:` pair, so it is no narrower than dev.

One new finding keeps the verdict NEGATIVE. The readers still disagree with GCC on which directives exist. They match a directive NAME with a regex word boundary, not with GCC's identifier lexing, so `#if$a` and `#endif$b` are read as `#if` and `#endif`. GCC reads them as unknown directives and ignores them in skipped code. The two therefore disagree on conditional nesting. This is the class the manager's direction named: a directive reader disagreeing with GCC.

## Findings

### R272-3-F1 - MAJOR - Conformance, Robustness, Tests, Docs

**Artifact.**
- `sw/builder/test_builder.py:2967`: `cpp_hash`.
- `:2974-2975`: `cpp_directive_re`, ending in `(if|...|endif)\b`.
- `:4073`: `directive_re`, `([A-Za-z_]\w*)?`.
- `:3161-3164`: `keyed_condition_re`.
- `:3052`: `error_line_re`.
- `:4811-4812`: `macro_definition_re`.

**Authority and evidence.**
- #408/#409 acceptance 4 ("no reduction").
- The manager's round-2 direction on #408: fix the class, where a directive reader disagrees with GCC, not one spelling.
- The site comment at `:3030-3036` and the page at `docs/integration/BAREMETAL_FIRMWARE.md:325-328` say the readers "find one exactly where the pinned GCC does" and are exact "because they run GCC's phases in GCC's order".

GCC 14.3 at `-std=gnu99` lexes a directive name as an identifier, and `$` is an identifier character. So `if$a` is an unknown directive, which GCC ignores inside a skipped group. The readers stop the name at `\b` before `$`. Every reader built on `cpp_hash` + name + `\b`, or on `[A-Za-z_]\w*`, therefore reads `#if$a` as `#if`, `#endif$b` as `#endif`, and likewise `#else$`, `#ifdef$` and `#error$`.

Measured by `probes/reader_vs_gcc.py` on `probes/dollar_skipped.c`, with the pinned SDK compiler (receipt `receipts/probes/reader_vs_gcc.txt`):
- The readers find `['ifdef','if','endif','if','endif','endif']`.
- The directive-set closure reads `['ifdef','error','if','endif','if','endif','endif']`, every name admitted.
- GCC exits 0 with no diagnostics and keeps `evil` and `z`. So GCC compiles unconditionally a line that the readers place inside an `#ifdef` arm which holds an `#error`.

`arm_selections()` skips an arm whose own text holds an `#error` (`:3248-3250`). So the readers' nesting and GCC's nesting diverge on a text the directive-set closure admits. Neither corpus covers an identifier character after a directive name.

On dev (759da623) `cpp_directive_re` had the same `\b` (dev line 2560). However, dev refused a conditional reaching the six boot-path bodies on its own. This PR retires that refusal onto per-selection grading, which is only as sound as the readers' nesting.

**Not measured.** I measured this at the reader level with the compiler as oracle. I did not construct or grade a whole-firmware case. I have not shown that a store or a boot-path change passes the whole gate through it, and it is not claimed here.

**Impact.** The per-selection grading that replaces the retired conditional-reach ban can grade an arm structure that GCC does not build. Where it does, code GCC compiles unconditionally is attributed to an arm the gate drops or grades apart. That reproduces the reduction class of R272-1 F1 and R272-2 F1 by a different spelling. The page and the site overstate what the readers match.

**Required outcome.** The readers must lex a directive name as GCC does, as a whole identifier with `$` included. Alternatively, a directive whose name is not exactly one the gate has a rule for must be refused wherever it sits, skipped groups included, on every machine. Add corpus entries recorded from the pinned GCC for a `$` (and any other identifier character GCC admits) after `if`, `ifdef`, `ifndef`, `elif`, `else`, `endif`, `define`, `undef` and `error`. Bound or correct the "exactly where the pinned GCC does" claims at the site and on the page.

**Verification.** `probes/reader_vs_gcc.py <clone> <sdk-gcc> probes/dollar_skipped.c`: the readers either find exactly the directives GCC honours, or the firmware carrying those lines is refused by gate 1b in both modes. The new corpus entries must be re-measured on GCC 14.3. A disconnect of the fix must fail them.

## Prior public findings at this head

| Finding | Status at 8e12d31f | Evidence |
|---|---|---|
| R272-2 F1 BLOCKER (`%\`, a line end, then `:ifdef`) | RESOLVED | The prior round's `probe_split_digraph.py` was run with only the repository path changed (`receipts/probes/r272-2-probe-sdk.diff`). Every spelling (control_hash, formfeed, plain_digraph, split_digraph) is REFUSED with the pinned SDK. A no-compiler variant also refuses all four; its only extra change is the compiler mapped to a missing path without `--require-rv32` (`r272-2-probe-absent.diff`). The split and plain digraphs are refused by the digraph ban, and the other two by the per-selection grading. Receipts: `receipts/probes/r272-2-*.txt`. |
| R273-3 F1 MINOR (BOM) | RESOLVED | `_c_phases_12` drops U+FEFF at offset 0 (`test_builder.py:2429-2432`). The fixed corpus carries the BOM entries (`:5186-5255`), and they are re-measured on GCC 14.3 in my SDK run (4985/4985). |
| R273-3 F2 MINOR (paste-ban bound) | RESOLVED | `BAREMETAL_FIRMWARE.md:360-365` and the site docstring (`test_builder.py:4944-4953`) state the bound: this file's own `#define`s only, `__CONCAT` via headers outside, the same bound as #544. |
| Round-1 findings (R272-1 F1-F4, R273-1 F1) | Not re-derived one by one this round | R272-1 F1's form-feed, vertical-tab, NUL and lone-CR spellings are fixed-corpus entries (`:5147-5164`) re-measured on GCC. The prior round's formfeed spelling is REFUSED. |

## Lens results

| Lens | Result | Artifact at 8e12d31f | Checked against |
|---|---|---|---|
| Conformance | UNCLEAN (F1) | `test_builder.py:2312-2736`, `:2960-3300`, `:4071-4155`, `:4808-4981`, `:5365-5408`; `receipts/gate1b/*.log`; `receipts/probes/*` | #408/#409 acceptance 1-5. The C11 5.1.1.2 phase order: BOM, line ends, splice deletion, `%:`/`%:%:` by maximal munch. |
| RTL | CLEAN | `git diff 759da623..8e12d31f --stat`: only `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/testing/CI_WORKFLOWS.md` change. No file under `hdl/` or any processor submodule. | Gate 1b's RTL mutation variants elaborated under Verilator 5.050 in both gate runs, exit 0 (`receipts/gate1b/sdk.log`, `absent.log`). |
| Robustness | UNCLEAN (F1) | The same reader sites; `probes/dollar_skipped.c` | Malformed and skipped-group directive spellings against GCC 14.3. |
| Tests | UNCLEAN (F1) | `_LEXER_TEMPLATES`/`_LEXER_GENERATED_KEPT` (`:2546-2736`) and `lexer_corpus` (`:5013-5256`). Gate 1b with the SDK: exit 0, 264/264, 30/30+4/4, 4985/4985 re-measured, 0 NOT RUN. Absent: exit 0, 206/206, 4985/4985 as recorded, 1 registered NOT RUN. `--absent --require-rv32`: exit 1. | The corpora do not cover identifier characters after a directive name. |
| Docs | UNCLEAN (F1) | `BAREMETAL_FIRMWARE.md:296-368`. `docs_check.py` 0, `check_baremetal_only.py --check` 0, `check_em_dash.py --base 759da623` 0, `git diff --check` 0 (`receipts/static.txt`). The PR body was updated for this round. | The claim at `:325-328` and the site comment `:3030-3036`. |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | reader sites above, gate logs, probes | R272-3 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| RTL | CLEAN | diff stat (no RTL touched); Verilator 5.050 elaboration in both gate runs | R272-3 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| Robustness | UNCLEAN | reader sites; `dollar_skipped.c` | R272-3 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| Tests | UNCLEAN | both corpora; gate 1b both modes; prior probes | R272-3 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| Docs | UNCLEAN | `BAREMETAL_FIRMWARE.md:296-368`; static doc gates; PR body | R272-3 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |

## Real limits

- **Not re-run independently:**
  - The author's disconnect matrix (53/41 controls). I attempted my own disconnects (the unread-pair check and the BOM drop), but the disposable copy step was not permitted in this session, so that claim remains the author's.
  - The author's 103-case reviewer grading.
  - The "only the 14 legitimate edits" claim.
  - The full builder bank, which is outside this round's allowance.
- **Generated corpus:** checked through gate 1b's own re-measurement on the pinned GCC 14.3 (4985/4985 in my SDK run), not by a separate oracle script.
- **No-compiler probe mode:** approximated by mapping the RV32 selector to a missing path, with the host `cc` still present.
- **F1:** measured at the reader level only (see "Not measured" under F1).
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted evidence:** not inspected. The A234 receipts are not in the public evidence tree at 470f959a, whose newest packet is A219. Evidence tip 8e901270 holds the reviews only.

## Pending manager duties

- Publish the A234 receipts packet.
- Hosted and act acceptance at the exact head.
- Candidate-merge validation against live dev 3d2f3e31 (source base 759da623).
- The re-review of F1's fix.

R272-3 FINISHED
