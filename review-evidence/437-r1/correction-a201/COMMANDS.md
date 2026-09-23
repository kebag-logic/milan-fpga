# A201 commands for #437 / PR #515

Head `34f124f9b0dabeb74c655052f0a0858620a09037`, tree `bb9b3dbc70a81af453f47c4c72aeb8433d927d91`.
`CLONE` is a clean checkout of that head holding `574c29fa`, `e4906bfc` and `ede8d48e`.
Every script reads `CLONE` from the environment (default: the lane worktree).

## Integration of live dev

    git merge-tree --write-tree e4906bfc ede8d48e           # exit 0: conflict-free
    git merge --no-ff origin/dev                             # 070ef51e
    git diff 574c29fa e4906bfc | git patch-id --stable       # a71c48c9...
    git diff ede8d48e 070ef51e | git patch-id --stable       # a71c48c9... (identical)

Receipt: `receipts/merge-dev.txt`.

## Gates at the head (receipts/gates/, all exit 0)

    python3 -B scripts/gen_toc.py --selftest                 # 1269/1269
    python3 -B scripts/gen_toc.py --check                    # 106 pages
    python3 -B scripts/gen_toc.py --verify-anchors           # 144 links
    python3 -B scripts/gen_toc.py --sites                    # 29 single-source sites
    python3 -B scripts/check_em_dash.py --selftest           # 429 arms
    python3 -B scripts/check_em_dash.py --base ede8d48e...   # 0 findings over 39 added lines
    python3 -B scripts/docs_check.py
    python3 -B scripts/docs_check.py --selftest
    python3 -B scripts/check_doc_style.py
    python3 -B scripts/check_doc_style.py --selftest
    python3 -B scripts/check_py_idiom.py                     # long module 10<=10, long function 9<=9
    python3 -B scripts/check_py_idiom.py --selftest
    git diff --check ede8d48e HEAD

`receipts/gates/SUMMARY.txt` lists the thirteen exits; `identity.txt` the head, tree and merge base.

## Evidence scripts (scripts/)

| Script | What it does | Receipt |
|---|---|---|
| `walks.py` | runs `headings()` and `blocks()` of a revision (`git archive` of scripts/) or the worktree | - |
| `render.py` | GitHub `POST /markdown`, mode `gfm`, request bytes built as the fixtures record them; cached | `receipts/renders/` (269 fresh renders, request and response bytes, both SHA-256) |
| `fixture_compare.py` | every fixture shape under base, reviewed head and this head | `receipts/fixture-compare.json` |
| `edit_fixtures.py` | the fixture rewrite: 10 shapes removed, limitation marks, 23 shapes added | `receipts/removed-shapes.json` |
| `ac4.py` | acceptance 4 on the base, dev and head trees | `receipts/ac4.json` |
| `mutate.py` | 14 named mutations, both self-tests | `receipts/mutations.json` |
| `replay_public.py` | every public rendered page of R237-3 and R238-2, and the prior findings R237-3 collected | `receipts/replay-public.json` |
| `gen_pages_r237_3.py` | R237-3's public page generator, unchanged | - |
| `sweep.py`, `render_diffs.py` | 30,000 pages each at seeds 201 (full) and 2011 (core); every page where this head differs from the base is rendered | `receipts/sweep201-rendered.json`, `receipts/sweep2011-rendered.json` |

`receipts/regressions-vs-base.json` classifies every page that agreed at the base and disagrees here.

Reproduce, from this directory:

    python3 scripts/fixture_compare.py "$CLONE/scripts" > receipts/fixture-compare.json
    python3 scripts/ac4.py receipts/ac4.json
    python3 scripts/mutate.py receipts/mutations.json
    python3 scripts/replay_public.py receipts/replay-public.json
    python3 scripts/gen_pages_r237_3.py 201 30000 scratch/sweep201.json
    python3 scripts/gen_pages_r237_3.py 2011 30000 scratch/sweep2011.json core
    python3 scripts/sweep.py scratch/sweep201.json scratch/sweep201.diff.json
    python3 scripts/sweep.py scratch/sweep2011.json scratch/sweep2011.diff.json
    python3 scripts/render_diffs.py scratch/sweep201.diff.json receipts/sweep201-rendered.json
    python3 scripts/render_diffs.py scratch/sweep2011.diff.json receipts/sweep2011-rendered.json

`replay_public.py` reads the public packets under `scratch/public/`. They were fetched read-only from
evidence commits `a75d3b91` (R237-3) and `1f4b0af7` (R238-2), paths `review-evidence/437-r1/reviews/`.
With the render cache present, no page is sent again.
