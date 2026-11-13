# [A683zp] HANDOFF: #665 S2b round 31 (docs only)

- **Base:** round 30's head `325514224bcc356a6b43843f1003c2323f09de25` (the manager's sync merge of `dev-soft-core` `e5f88a8e`; tree `a3ca67b9`, `5bea2597`'s).
- **Head:** `084cf7a8455e9fa8e24a0e5bcf57c9557816c819`, branch `665-s2b-cycles`, three one-line commits, nothing pushed.
- **Status:** REVIEW READY, posted as #665 issuecomment-6850895861. No STOP condition met.
- **Ruling:** the manager's round 31 ruling on R711-9 (#810 issuecomment-6850590935, POSITIVE) and R712-9 (#810 issuecomment-6850656712, NEGATIVE on two MINOR Docs findings).

## Changes

| Item | Commit | File:line at the head | What it says | The receipt line it cites |
|---|---|---|---|---|
| 1. R712-9-F1 | `f150b8cb` | `docs/design/SPLIT_CONTROL_MEMORY.md:442` | `0fb66211` carries #874, #880 (with KLJ3, #823), #889 and #888, as `dev-soft-core` `6eacd76d` names them | `receipts/gates/diff_vs_dev_soft_core-excerpt.log`: the `+` line beside the `-` line from `e5f88a8e` is the same text |
| 1. R712-9-F1 | `f150b8cb` | `docs/design/SPLIT_CONTROL_MEMORY.md:455-456` | at the pin move's merge, the smallest margins: 288 B of `rom` at the platform's 1x1/2if, 16 B of `sram` at the platform's 8x8/2if, whose next granule would plan 59.5 against the 59.0 its override held there | The doc's own table, `:448` (112,352 B of `rom`) and `:450` (114,672 B of `sram`), with `GRANULE_BYTES` 2,048 (`sw/litex/ctrl_memory.py:51`): 112,640 − 112,352 = 288 and 114,688 − 114,672 = 16. `receipts/gates/diff_vs_dev_soft_core-excerpt.log` keeps `6eacd76d`'s sentence, with "that merge" for "the merge" and "held there" for "holds", the paragraph's framing on the pin move's branch |
| 2. R712-9-F2 | `47e44d73` | `docs/design/SPLIT_CONTROL_MEMORY.md:2323` | arm A's least margin at this head, from round 30's legs: at most 8.162 ms at 8x8/2if (11.838 ms, group `backlog-adp@program-aged2-7`, instance `service.aecp.last.if1`) and at most 9.992 ms at 1x1/1if (10.008 ms, group `backlog-adp@verify-aged2-5`, instance `service.aecp.last.if0`), each the least of the aged windows; round 30 did not re-derive arm A's least over all rows, nor the `answering-every-port` arm's; round 29's figures given as round 29's | Round 30's `receipts/final-5bea2597/harness/X-GA8-regrade.log:10`: `AGED 48 windows ... the least margin 8.162 ms, backlog-adp@program-aged2-7.service.aecp.last.if1 at 11.838 ms`; `X-GA1-regrade.log:10`: `AGED 48 windows ... the least margin 9.992 ms, backlog-adp@verify-aged2-5.service.aecp.last.if0 at 10.008 ms`. `X-GN8-regrade.log` and `X-GN1-regrade.log` hold only `CLOCK`, `STEPS`, `NOTICE` and summary lines, so no row margin of that arm. Round 29's are round 29's `receipts/legs/least-margins.txt:1-4` |
| 2. R712-9-F2 | `47e44d73` | `docs/design/SPLIT_CONTROL_MEMORY.md:2331` | "arm A's least AECP-record margins in its windows opened at the age limit above, 8.162 ms at 8x8/2if and 9.992 ms at 1x1/1if", in place of "the rows' least above" | the same two `AGED` lines |
| 3. R711-9 RES-2 | `084cf7a8` | `sw/litex/ctrl_memory.py:257`, `:265` | "ROM debt owed to the hybrid XIP work (#665 decision D3)" in place of "ROM debt owed to S14"; at `:265` the trailing "(#665)" is dropped, since the new text carries #665. Reason strings only | `receipts/gates/s14_reason_grep.log` (no match, rc 0); `receipts/gates/test_ctrl_memory.log`: `RESULT: PASS` |

No code, cost, bound, ledger figure or gate changed (`receipts/gates/diff_round.log`: 2 files, 10 insertions, 7 deletions).

## Gates at the head

All in `receipts/gates/`, one log and one rc each, never piped (`summary.txt`), run by `scripts/gates31.sh`:

| Gate | Result |
|---|---|
| `git status --short --untracked-files=all` | empty |
| `git diff --check 32551422 HEAD` | rc 0, no output |
| `scripts/docs_check.py` | rc 0, 0 findings |
| `scripts/check_doc_style.py` | rc 0, OK |
| `scripts/check_em_dash.py --base 32551422` | rc 0, 0 findings over 5 added lines in 1 page |
| `scripts/check_em_dash.py --selftest` | rc 0 |
| `scripts/check_py_idiom.py` | rc 0, every count within its budget |
| `sw/litex/test_ctrl_memory.py` | rc 0, `RESULT: PASS`, 0 failures |

The em-dash gate needs the pinned renderer, installed in a scratch venv outside the tree and this directory from `tools/markdown/requirements.txt` with `--require-hashes`. `test_ctrl_memory.py` ran in the product LiteX tree's venv. Host paths in the logs are redacted (`receipts/INDEX.md` names the placeholders).

## Open risks

- Section 13 now says arm A's least is "at most" each aged-window figure: round 30's re-grades print no table of rows, so arm A's least over all its rows and the `answering-every-port` arm's least are not re-derived at this head. Re-deriving them means re-grading each leg's group logs with a table, which this round's ruling excludes.
- `:2331`'s heaviest work pass at 8x8/2if, 183,244 cycles (`notice-burst-2`), is round 30's figure, unchanged here; it is not in round 30's published verdict lines (`X-GN8-regrade.log:2` gives the longest pass carrying the store's step, 88,448). 1x1/1if's 166,127 is `X-GN1-regrade.log:2`. Disclosed in the PR body's Known limitations.
- `SPLIT_CONTROL_MEMORY.md:141` still says "ROM debt of 4.0 RAMB36 owed to S14" in prose; the ruling's item 3 covers the reason strings only.
- The Docs lens must be covered again at this head.

## Files

- `PR-BODY.md`: round 30's body with round 31's three items, first line `[A683zp]`.
- `REVIEW-READY-COMMENT.md`: the comment posted on #665.
- `scripts/gates31.sh`, `scripts/redact_index.py`: the gate runner and the receipt redaction and index.
- `receipts/INDEX.md`: generated from the files present.
