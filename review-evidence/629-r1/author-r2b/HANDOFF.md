# [A484] round-2b handoff, issue #629, PR #631 (lane M1)

Status: DONE. One commit, not pushed. REVIEW READY posted on #629
(issuecomment-5936429406).

Assignment: the newest [A10] comment on #629, "Round 2b"
(issuecomment-5936355573). It asks for one gate fix and nothing else.

- Base head: `49899572741b732563bdca0bff03cefb69aea867`
- New head: `c554ae51b1dcc2285863f0f0117cb025971a594c` (one commit on top, no amend)
- Subject: "Name the five tracked shape-header copies in the #629 design's
  Generated row instead of a glob that check_entity_shape.py arm I cannot
  resolve". One line, no body, no trailers.

## The failure and its cause

`scripts/check_entity_shape.py` arm I ("every shape-header consumer
resolves", `scripts/check_entity_shape.py:258-302`) scans every tracked file
with `CONSUMER_RE` (`scripts/shape_consumer_inventory.py:46`,
`[\w$(){}./\\-]*gen/adp_shape_defaults\.svh`). `*` is not in that character
class, so the glob `configs/generated/*/gen/adp_shape_defaults.svh` in the
"Generated" row of the page's "Parent-visible changes" table
(`docs/design/MEDIA_CLOCK_FOLLOWING.md:755` at `49899572`) was extracted as
`/gen/adp_shape_defaults.svh`. That is neither a bare `gen/...` include
(skipped at `shape_consumer_inventory.py:313`) nor a classified consumer,
and it resolves outside the tracked tree, so the gate fails.

Reproduced at `49899572`: rc 1, `checks: 166 failures: 1`, the one
failure being that line. The same reference is in the round-1 page at
`78d4fef2` (line 471 there; read with `git show`, no checkout), which matches
the assignment's "at both the round-1 head and this head".

## The fix

The "Where" cell of that one row now names the five tracked per-config
copies (`git ls-files 'configs/generated/*/gen/adp_shape_defaults.svh'`
lists exactly these five):

- `configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh`
- `configs/generated/endstation_arty_8ch/gen/adp_shape_defaults.svh`
- `configs/generated/endstation_arty_current/gen/adp_shape_defaults.svh`
- `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh`
- `configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh`

The meaning is unchanged. The glob meant one per shipping configuration,
and there are five `configs/endstation_*.yaml`. The row's "Change" cell is
untouched. It still names the tracked `hdl/common/gen` copy in prose, as
before. That copy was never in the "Where" cell, so it is not added.
Diff: 1 file, 1 insertion, 1 deletion. No other line, page or index row
changed.

After the fix, `CONSUMER_RE` finds only tracked paths in the page: the five
above plus the existing `:239` reference.

## Gates at `c554ae51`

Each command ran unpiped with its output in a file. Logs and rc files are
in `gates/`, and `gates/HEAD` holds the head.

| Gate | rc | Result |
|---|---|---|
| `python3 scripts/check_entity_shape.py` | 0 | checks: 166, failures: 0, RESULT: PASS |
| `scripts/docs_check.py` | 0 | 0 findings across 184 md files and 955 scrubbed text files |
| `scripts/check_doc_style.py` | 0 | OK, 22 current documents |
| `scripts/gen_toc.py --check` | 0 | OK, 126 pages |
| `scripts/gen_toc.py --verify-anchors` | 0 | 292 cross-page fragment links reproduced |
| `scripts/check_em_dash.py --base d4dd7426` | 0 | 0 findings over 885 added lines in 2 pages |
| `scripts/check_doc_paths.py` | 0 | 874 cited paths resolve |
| `git diff --check` (tree) and `git diff --check d4dd7426 HEAD` | 0 | clean |

The Markdown gates ran with the pinned Markdown venv's python, from the
physical `/data` lane path. The area run under "How to validate" in the PR
body was not re-run. This commit touches no RTL, and its figure is
unchanged.

## PR body

`PR-BODY.md` is the round-2 body from `../629-a483/PR-BODY.md` with one
line added at the end of its "Round 2" section, plus a blank separator line.
That line states the round-2b head, the fix and the gate result. Nothing else
changed, so the Status section and the "Results at" paragraph still name
`49899572`. A later round should move them to the current head.

## Unchanged from round 2

The page's clause findings, code map, design options and recommendation,
parent-visible and processor-visible change lists, and test plan are exactly
as round 2 left them. See `../629-a483/HANDOFF.md` and
`docs/design/MEDIA_CLOCK_FOLLOWING.md`. D1 and D5 are still re-opened for
decision, and D4 is still with the owner.

## Not done, by the assignment

No push, no PR edit, no other comment. No RTL, builder, generator, config
or processor change, and no bench access.
