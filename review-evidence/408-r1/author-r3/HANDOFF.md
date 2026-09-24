# [A248] HANDOFF — PR #535 (issues #408/#409), correction round 3

Lane: `$LANES/408-409-boot-gate-retire`, branch `408-409-boot-gate-retire`.
Base head at takeover: `8e12d31fefa7df0abb4d9474d0412ce123ac9644` (correction round 2).
Round-three head (this work): `11b1b86c11378cac414ef58f6be40d8da00980da` (local commit; NOT pushed).
Decision implemented: https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5811522505

## What round 2 left open

- R273-4 (external) NEGATIVE, BLOCKER: a header name in `__has_include(<...>)` in an
  `#if` hides a line. GCC lexes the operand as one header-name token, so `/*` opens no
  comment; the gate reads a comment hiding the line to the next `*/`. HI1-HI4 (identity
  forgery, AEM verdict, ADP enable, CSR store) were ACCEPTED at 8e12d31f **with the SDK**.
- R272-3 (internal) NEGATIVE, MAJOR: `$` after a directive name (`#if$a`). GCC keeps it
  as an unknown directive ignored in skipped code; the readers read `#if`. Nesting diverges.

Both are the same class: a hand-written reader disagreeing with GCC on a lexical feature it
does not model. Manager's direction: **stop extending the readers toward GCC's grammar; close
the grammar** — a declared lexical subset S checked first, refusing everything outside it.

## Design (implemented in `sw/builder/test_builder.py`)

- `assert_within_lexical_subset(source)` runs FIRST in `assert_boot_contract()`, before any
  reader (replaced the two prior calls). It folds in the existing literal/digraph/trigraph
  refusals and adds the new closed-grammar refusals, each with a named pin.
- `assert_subset_refuses()` runs in the pre-flight: `subset_refusal_corpus` (one firmware per
  excluded class) is refused on its own pin, plus a within-S control accepted. A removed S
  check trips this before any firmware is graded.
- The generated corpus is RESTRICTED to S: `_LEXER_HASHES=("#",)`, `_LEXER_NOT_HASHES=("##",)`,
  `_LEXER_PASTES=(" ## ",)` (digraph introducers dropped), `_LEXER_GENERATED_KEPT` re-recorded
  against the pinned GCC (4907 -> 1767). The fixed corpus (78) is kept: it validates the shared
  lexer `_c_phases()`, which is how S DETECTS the refused classes.
- New PINs: `SUBSET_DOLLAR_PIN`, `SUBSET_UCN_PIN`, `SUBSET_HAS_INCLUDE_PIN`,
  `SUBSET_HEADER_NAME_PIN`, `SUBSET_PRAGMA_PIN`, `UNTERMINATED_COMMENT_PIN`.
- `_c_phases()` gains an `unterminated_comment` finding; `assert_lexes_as_compiled()` refuses it.
- Docs (`BAREMETAL_FIRMWARE.md`) and the gate print state S and the refusal rule and DROP the
  "exact because they run GCC's phases in GCC's order" claim -> "exact on S; outside S refused".

## S table (C11 6.4 token class -> modelled or refused)

| C11 6.4 class | In S? | How the gate handles it |
|---|---|---|
| 6.4.1 keywords, 6.4.2.1 identifiers | MODELLED | `[A-Za-z_][A-Za-z0-9_]*`, the reader class |
| 6.4.3 universal character names in identifiers | REFUSED | `SUBSET_UCN_PIN` — a `\` left in code after phase 2 |
| gnu `$` in identifiers/directive names | REFUSED | `SUBSET_DOLLAR_PIN` — `$` in the phase-3 view |
| 6.4.4 constants, 6.4.5 string literals | MODELLED | raw string + open literal REFUSED (`RAW_LITERAL_PIN`, `UNTERMINATED_PIN`) |
| 6.4.6 punctuators | MODELLED | digraphs + trigraphs REFUSED (`DIGRAPH_PIN`, `TRIGRAPH_PIN`) |
| 6.4.7 header names | MODELLED only as a plain `#include` operand | `__has_include`/`__has_include_next` REFUSED (`SUBSET_HAS_INCLUDE_PIN`); comment/backslash in a `#include` operand REFUSED (`SUBSET_HEADER_NAME_PIN`) |
| 6.4.9 comments | MODELLED | block comment with no `*/` REFUSED (`UNTERMINATED_COMMENT_PIN`) |
| `_Pragma` operator | REFUSED | `SUBSET_PRAGMA_PIN` |

Shipping firmware is inside S (verified: view has no `$`, `\`, `__has_include`, `_Pragma`,
digraph, trigraph, raw string, unterminated literal/comment; includes are clean names).

## Corpus stats

| Corpus | round 2 | round 3 | notes |
|---|---|---|---|
| fixed | 78 | 78 | unchanged; validates the shared lexer / S detector |
| generated | 4907 | 1767 | restricted to S (`#`, `##` introducers; digraphs dropped) |
| total spellings | 4985 | 1845 | re-recorded against pinned GCC 14.3, re-measured where a compiler answers |
| `subset_refusal_corpus` | — | 13 | one firmware per excluded class, refused on its pin, + within-S control |

## Mutation counts (acceptance 4: no entry lost, count >= round 2's)

| | round 2 | round 3 | delta |
|---|---|---|---|
| SDK (compiler present) | 264/264 | **271/271** | +7 S refusal entries |
| absent (no compiler) | 206/206 | **213/213** | +7 (S is text-only, refuses on every machine) |
| firmware edits accepted | 30/30 | 30/30 | — |
| Makefile edits accepted | 4/4 | 4/4 | — |

No mutation-table entry removed; only the 7 subset entries added. Both counts >= 163 floor and
>= round 2. New entries: dollar, UCN, `__has_include`, `__has_include_next`, header-name,
`_Pragma`, unterminated comment.

## Probe table (every reviewer probe: refused by S or agrees with GCC)

| Round | Probe | Result at round-3 head |
|---|---|---|
| R272-1 | form feed / vtab / NUL / lone-CR before `#` | within S; readers agree with GCC (fixed corpus + mutations) |
| R272-2 | split `%:` digraph (`%\`+nl+`:ifdef`) | REFUSED by S digraph ban (r2-cases: 9 refused, 6 controls accepted) |
| R272-3 | `$` in a directive name (`dollar_skipped.c`) | REFUSED by S, `SUBSET_DOLLAR_PIN` |
| R273-1 | one `#define` per name; absent overstatement | within S; published cases unchanged |
| R273-3 | BOM at offset 0; paste-ban bound | within S / refused as before (bom: 8 refused/3 accepted; extra: 1/3) |
| R273-4 | `__has_include` header name — HI1 identity, HI2 ADP, HI3 CSR store, HI4 AEM verdict | ALL REFUSED by S, `SUBSET_HAS_INCLUDE_PIN` (were ACCEPTED with SDK at 8e12d31f) |

Reviewer case files run through the current gate (absent, 0 pin mismatches):
`hi.json` (HI1-HI4 refused; HI5 now refused too as it uses `__has_include`; HI3p accepted =
registered NOT-RUN class absent), `r2-cases.json`, `bom.json`, `extra.json`, `unread.json`,
`published.json` (49 accepted / 25 refused absent). Receipts: `probes/out/`.

## Disconnect table (removing each S refusal lets its probe through)

Two-stage: removing an S check first trips `subset_refusal_corpus` (tripwire) before any
firmware is graded; with that tripwire also bypassed, the whole-firmware probe is graded:

| S refusal | probe | tripwire | absent | SDK |
|---|---|---|---|---|
| `$` (`SUBSET_DOLLAR_PIN`) | `#if$a`-misnest store | fails on `$` entry | ACCEPTED (through) | REFUSED (arm-selection census) |
| UCN (`SUBSET_UCN_PIN`) | `id` identity forgery | fails on UCN entry | ACCEPTED (through) | REFUSED (GCC rejects basic-char UCN) |
| `__has_include` (`SUBSET_HAS_INCLUDE_PIN`) | store behind header name | fails on that entry | ACCEPTED (through) | **ACCEPTED (through — census cannot backstop; the R273-4 BLOCKER class)** |
| `#include` header-name (`SUBSET_HEADER_NAME_PIN`) | `<generated/c/*x*/sr.h>` | fails on that entry | REFUSED (include-set name pin) | — |
| `_Pragma` (`SUBSET_PRAGMA_PIN`) | `_Pragma("push_macro(...)")` | fails on that entry | ACCEPTED (through) | — |
| unterminated comment (`UNTERMINATED_COMMENT_PIN`) | trailing `/* no close` | fails on that entry | ACCEPTED (through) | REFUSED (GCC unterminated-comment error) |

Receipts: `probes/out/disc/`. Patches: `probes/disconnect/*.json` (`_full.json` = S check +
tripwire bypass).

## Gate table (all rc 0; never piped)

| Gate | mode | rc | evidence |
|---|---|---|---|
| `test_firmware_compiler.py --sdk-destination` (gate 1b) | SDK present | 0 | `receipts/sdk.log` — 271/271, 30/30+4/4, 78+1767 re-measured |
| `test_firmware_compiler.py --absent` (gate 1b) | absent | 0 | `receipts/absent.log` — 213/213, 1 registered NOT RUN |
| `test_builder.py --require-rv32` (whole suite) | present | 0 | `receipts/suite-present.log` — ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 Vivado), 85 fns |
| whole suite, cross compilers hidden (`probes/suite_absent.py`, same audit as CI absent control) | absent | 0 | `receipts/suite-absent.log` — ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b census, gate 11), 0 compiles |
| `docs_check.py` | git present | 0 | `receipts/docgates.log` |
| `docs_check.py` | no-git | 0 | `receipts/docs-check-nogit.log` |
| `check_baremetal_only.py --check` (+ `--selftest`) | — | 0 | `receipts/docgates.log` |
| `check_em_dash.py --base 759da623...` | — | 0 | `receipts/docgates.log` |
| `check_doc_style.py` (+ `--selftest`) | — | 0 | `receipts/docgates.log` |
| `gen_toc.py --check` (+ `--verify-anchors`) | — | 0 | `receipts/docgates.log` |
| `check_doc_paths.py` | — | 0 | `receipts/docgates.log` |
| `check_py_idiom.py` (+ `--selftest`) | — | 0 | `receipts/docgates.log` |
| `git diff --check` | — | 0 | `receipts/gitdiffcheck.log` |

Note on "test_builder.py in both modes": the whole suite runs present via `--require-rv32`;
the absent control is `test_firmware_compiler.py --absent` (gate 1b), which is how CI docs.yml
runs the compiler-absent path — only gate 1b consumes the RV32 compiler.

## SDK

Pinned RV32 SDK installed and verified into `sdk-home/br-milan-rv32/host` (the shared
`~/br-milan-rv32` tree lacks the provenance receipt `test_firmware_compiler.py` verifies).
Archive sha256 `d42680e9...`, `riscv32-linux-gcc` 14.3.0. Receipt: `receipts/sdk-install.log`.

## Not done / out of scope

- No push, no PR edit, no merge, no sub-agents, no other checkouts, no hardware.
- Hosted / act / Yosys / Verilator-suites not run (manager owns hosted acceptance).
- Whole builder bank beyond gate 1b: the other ~80 gates run in `suite-present.log`; they are
  untouched by this change (only gate 1b and docs changed).

## Commits

`11b1b86c` — builder, docs: close the readers' grammar to a declared subset S checked before
any reader, refuse $/UCN/__has_include/header-name/_Pragma/unterminated-comment by name,
restrict the generated corpus to S and drop the exact-because-GCC's-order claim.

One-line subject, no body, no trailers (AGENTS.md/CONTRIBUTING require no trailers; that and the
assignment override the attribution reminder's Co-Authored-By line, per the reminder's own
precedence clause). Not pushed (assignment: no push, no PR edit, no merge).
