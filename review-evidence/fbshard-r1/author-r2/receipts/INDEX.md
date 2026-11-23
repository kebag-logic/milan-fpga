# Receipts: #980 firmware-boundary shards, round 2 ([A827])

Lane `pf-fbshard-1`. Round-1 head `b7b351935f65416c8632c21dd13e08fb2e9c1d9c`, reviewed NEGATIVE by R897-1.
Round-2 head `5392adf989349b68cfbb54d91fd0413c5b745521`, tree `766ccefea747fa53f340cb99578f943b5279893c`. Local only, not pushed.
Every log below starts with the `git rev-parse HEAD` it ran at, and all ran at `5392adf9`.

| Receipt | What | Result |
|---|---|---|
| `head-ci-and-docs-gates.log` | The 28 CI and docs gates of round 1, in order (`tools/run_gates.sh`). Includes the generator check, `ci_events --check`, every CI scheduling self-test, wire-accountability, the docs, doc-path, doc-style, em-dash, hygiene, TODO, sh and py idiom gates, docs inventory and `act_ci.py --selftest`. | 28 of 28 rc 0 |
| `head-ci_events-selftest.log` | `ci_events.py --selftest` | PASS, 2369 items, 5881 arms, 252 s |
| `head-ci_fail_fast_selftest.log` | `ci_fail_fast_selftest.py`, full output. The new watcher runtime control runs on each committed workflow, then on the plant. | rc 0. `rtl` and `rtl-fast`: plant caught (`watcher stopped observing: observer_error after 1 read(s), rc=0`). `docs` and `elaborate`: no matrix, so no plant applies. |
| `skipped-matrix-receipts.log` | `tools/skipped_matrix_receipts.py`. (1) The committed control run on the round-1 committed workflows. (2) A scan of every job without a matrix, in all four workflows at both heads, for `${{ matrix.` and for expressions in the watcher's two job lists. (3) A generator plant where an unexpanded matrix name equals another job's name. | (1) `rtl` and `rtl-fast` at `b7b35193`: CAUGHT. (2) Round 1: `rtl` has 4 and `rtl-fast` has 2 matrix expressions in `SKIPPED_MATRICES`, and nothing else. Head: 0 everywhere. (3) Unplanted control generates; the plant is REFUSED. |
| `reviewer-probe-at-head.log` | R897-1's `probe_skipped_matrix.py`, unmodified (sha256 `5d2bb387...202c13`), run from its packet against this head | The runtime key is now the raw name `firmware-boundary shard ${{ matrix.shard }}/${{ matrix.total }}`. So the probe's own `probe no longer reproduces` assertion fires (rc 1). That is the expected result after the fix. |
| `issue-comment-review-ready.md`, `issue-comment-readback.md` | The `[A827] REVIEW READY` posted on #980 (issuecomment-7097237511), and its API readback after one edit. The edit restored a literal backslash escape that a file write had decoded. | identical apart from the trailing newline |
| `commits.txt`, `diffstat.txt`, `delta-from-b7b35193.diff` | The two round-2 commits and their full delta | 7 files, +144/-14 |

## Not run

- **Act replica: not run.** `act_ci.py --pr 982` refuses a candidate that is not the exact remote PR head. Remote `pf-fbshard-1` is still `b7b35193`, and this round may not push. Replaying `b7b35193` would not be evidence for this delta. The replica is owed once `5392adf9` is pushed.
- **No firmware builds.** This delta changes no builder, shard table or judging code. The round-1 shard and judging measurements stand at their named commits.

## Tools (receipt only, not committed)

- `tools/run_gates.sh CHECKOUT BASE MARKDOWN_PYTHON`: the 28 gates.
- `tools/skipped_matrix_receipts.py CHECKOUT ROUND1_COMMIT`: parts (1) to (3) above.
