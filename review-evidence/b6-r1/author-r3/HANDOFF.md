# B6 round 3 ([A481]) handoff

Refs #629, PR #630 (bench lane B6, the dev `ec0cc0c1` image). Round 3: docs only, no bench access.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5933253532
- Round-2 reviews answered: PR #630 comments 5933241034 (R426-2, NEGATIVE, two MINOR, four SUGGESTION) and 5933242529 (R427-2, POSITIVE, four SUGGESTION).
- Manager's PR #630 comments read: 5933253119 (R426-2 F1 resolved at archive tip `422dcf91`; owner decision 2026-10-01: evidence redaction is top-only, with no branch history rewrite) and 5932531424 (round-1 self-test evidence).
- Read-only inputs: the round-1 and round-2 packets (`b6-a477`, `b6-a480`), the round-1 private redaction map (local, never copied), the review packets of R426-2 and R427-2 (R426-2's `scripts/mask_check.py` was run here), and the evidence archive at `422dcf91008a09cb882dcc2b760779ce22e530cd`, read with `git show` and `git archive` only. No checkout, no clone.

## State

**DONE, REVIEW READY.**

- Commit `26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778` on `b6-bench-1001`, parent `e3f28f2f69343b54844ddfea368ef4cdd03facb6`. One-line subject, no body, no trailers. It changes one file, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, +44 / -18 lines. The worktree is clean (`gates/status-after.txt` is empty).
- An earlier local commit of this round, `5a321d9f`, was amended into `26dfc82f` before any posting. It narrowed one sentence ("the checks of items 1 to 5"). `5a321d9f` was never pushed or cited.
- **Not pushed.** No PR edit, no merge. The live PR #630 head is still `e3f28f2f`. The manager pushes `26dfc82f` and applies `PR-BODY.md`.
- Every measurement table is byte-identical to `e3f28f2f` and to `b5e9242e` (15 of 15). No rule, verdict or measured figure changed.
- Gates at `26dfc82f`: every invocation rc 0 (`gates/gates.txt`).
- Token scan: no private name (see "Token scan").
- Posted on #629: `[A481] TAKEN` (https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5933276686). `[A481] REVIEW READY` (https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5933514818). Each readback equals the posted text except for one trailing newline. No existing comment was edited or deleted, and nothing else was posted.

## The change, by assignment item (page lines at `26dfc82f`)

| Item | Finding | Page lines | What changed |
|---|---|---|---|
| 1 | Re-pin (R426-2 F1, resolved in the archive by the manager) | `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:617-618`, `:642` | "Where the packet is" and the reproduction command's checkout pinned to `422dcf91008a09cb882dcc2b760779ce22e530cd`. The earlier pin is not named |
| 2 | R426-2 F2(a) | `:255-261` (Method, item 4) | Six of the seven clusters under 98 frames have a measured rise of 0.99 to 1.00 ms. The seventh, A1's skip after a 33 ms read stall (cluster 9 in its `grade.json`), has no measurable rise and passed on the read gap alone, the gap-only branch of item 5 |
| 2 | R426-2 F2(b) | `:497-505` (The capture path, first bullet) | Two kinds of cluster without a matching rise. Gap-only, rise unmeasurable: 1 in A0, 2 in A1, 5 in A2, 3 in B INTERNAL and none in B CRF. Every skip in these eleven is still 48 n + 12. A2's clusters 17 and 56 have a measured, non-matching rise (154.5 ms for 60 frames, -155.8 ms for 1,020 frames just after the 13.3 s stall) and passed on the read gap and size rule, item 3 |
| 3 | R426-2 S1 | `:221`, `:267-273` (Method, new item 6), `:569` (Limits) | "six ways". Item 6: a multi-frame listener step within 300 ms of a capture loss joins its cluster, and the rise test applies to the net step, within 1 ms + 2 %, about 249 ms at A1's 12.4 s loss. A one-frame event never joins a cluster. In A1 and B CRF item 1's per-step sizes exclude it: every member step is 48 n + 12 or an exact stale-replay edge, or it is the 12.4 s loss's own 18,626 frames, the only step in its cluster |
| 3 | R426-2 S2 | `:636-638`, `:648-650` | Run the commands in a fresh clone or a disposable worktree, because the checkout writes the archive into the working tree and stages it. Reproduced at this pin with Python 3.14.7 and NumPy 2.5.3. The original run's versions were not recorded (the round-1 packet holds no version record) |
| 3 | R426-2 S3 | `:628-634` | The round-2 packet `b6-a480` is `review-evidence/b6-r1/author-r2/` at the same commit. Its `floor_check.py` repeats the floor check from the archive alone (rerun here, output identical to its receipt, `receipts/floor-check.txt`). Its `attribution_checks.py` and receipt hold the checks of items 1 to 5, including item 5's gap share. That tool reads the raw files, and its receipt records their hashes |
| 3 | R426-2 S4 | `:621-623` | "each graded case's `events.jsonl`", which matches the twelve label-masked files |
| - | Contents | `:48` | "where the packets are published" |

Notes for review:

- **R427-2's suggestions** were not in this round's assignment. S1 is R426-2 F2(a), done. S4 is answered by R426-2 S3 on the page and in the PR body's Round 3 section, which maps `b6-a480` to `author-r2/`. S2 (the residual at the 12.4 s loss's edge as up to about 1 ms, not one frame) and S3 (a fourth, actionless lock window) are not taken and are recorded in the PR body as retained, outside this assignment. Item 6 covers S2's related note on steps grouped into a cluster.
- **Item 6 and the 12.4 s loss.** That loss's cluster holds one step, the 18,626. So no separate step joined it. A listener event merged at that very step is item 1's stated residual, and the page's wording of that residual is unchanged.
- **Cluster numbers** are the `skip_clusters[].cluster` indices in each case's published `summary/<case>/grade.json`, so a reader can find them.
- **The archive at the pin.** R426-2's `mask_check.py` reports RESULT CLEAN at `422dcf91`. Its "own diff" line counts one removed line carrying a layout literal. That is the masking commit's own diff, which the owner decided to keep (top-only redaction). The page names neither the earlier pin nor that diff. A capture-layout scan of the whole `review-evidence/b6-r1` tree at `422dcf91` finds no count, index, index-spelling key or frame byte size. Its 26 hits are the raw file name with the count already masked as `<n>` (23) and the AES17 measurement standard (3) (`receipts/mask-check.txt`).

## Byte-identical table proof

- `receipts/table-identity.txt`: `tools/table_identity.py` splits both commits' page into tables (maximal runs of lines starting with `|`). All 15 tables at `e3f28f2f` equal the 15 at `26dfc82f`, byte for byte and in order, with none added or removed. RESULT PASS, rc 0. `receipts/table-identity-r1.txt` gives the same result against `b5e9242e`.
- `receipts/table-diff.txt`: every table line of `b5e9242e`, `e3f28f2f` and `26dfc82f` (161 lines, 16,010 bytes each) has the same sha256, `540ab528a6ad30ff45d173509d2f4de5dac94876ce406de47adf008e4e95d847`. `diff e3f28f2f -> 26dfc82f` gives rc 0 with empty output, and both `cmp` runs give rc 0.
- The PR body's How to validate step 2 repeats the check with `git show`, `grep` and `cmp` across all three rounds.

## Token scan

- `tools/token_scan.py` (round 2's tool, unchanged) loads three token sources: the round-1 private redaction map (27 literal and 5 regex entries) and this round's two token lists, 37 patterns and 7 literal names (76 tokens in all). The lists cover tool and model names, account names, home and data paths, and capture-layout tokens: the channel count, the indices, the index-spelling key, the frame byte size and the raw file name. They also cover interface names, serial devices, MAC and IPv4 patterns, USB bus positions, IDs and product strings, and instrument, switch and board brands. All three sources stay outside this packet and are never printed. A hit is reported as file:line and a label, never the matched text.
- Scanned: the round-3 diff `e3f28f2f..26dfc82f`, the page at `26dfc82f`, the commit message, and every file in this packet, including `PR-BODY.md`, this file and `REVIEW-READY.md`. Result and disposition: `receipts/token-scan.txt`.
- A planted-token self-test hits as expected (`receipts/token-scan.txt`).
- A read of the diff by hand finds no host, peer, switch or instrument name. It also finds no wiring, channel map, stream count, capture layout or clock topology. The new text names roles only: "the reference peer", "the bench host" and "the capture read times".

## Reproduction and archive (receipts/)

- `repro.txt`: `review-evidence/b6-r1` was taken from `422dcf91` with `git archive` into a scratch directory, with no checkout. The two page commands ran from `author/tools` with outputs in the scratch area. `b6_tone.py` gives rc 0 and the loop `566d3dfa...5588` (48,000 unique pairs, 0 silent frames). `b6_thdn.py controls` gives rc 0, `cmp` against `controls/controls.json` is silent, and ALL_PASS is True. The three input files hash to the page's values.
- `archive-check.txt`: at `422dcf91`, 400 of 400 manifest files re-hash to `published_sha256`. The tree holds 401 files, the manifest plus the 400 it lists, so none is unlisted and none missing. The page's 54 hashes resolve: 33 to `original_sha256`, 12 of them label-masked, and 21 to `RAW-ARTIFACTS.json`. The grade tool's entry keeps `original_sha256` `386ac2a6...`, the page's value, with a new `published_sha256` and `path_redacted`.
- `floor-check.txt`: round 2's `floor_check.py`, taken from `author-r2/tools` at `422dcf91`, run on that commit's `author/tools` and `controls.json`. rc 0, and the output is byte-identical to round 2's receipt.
- `round3-checks.txt`: `tools/round3_checks.py` re-derives every new statement from the published `grade.json` and `events.csv` at `422dcf91`: item 4's seven clusters, item 6's member steps and the 248.76 ms tolerance, that no one-frame event carries a cluster, and the capture-path bullet's counts and A2's clusters 17 and 56. RESULT PASS.
- `mask-check.txt`: R426-2's mask check and this round's capture-layout scan, as above.

## Gates (gates/)

Run at `26dfc82f` from the physical lane worktree path. Each output went to its own file, never piped. The Markdown gates used the pinned environment (md-venv `40cdefe08ebd`).

| Gate | rc |
|---|---|
| `docs_check.py` (0 findings, 183 md files) | 0 |
| `check_doc_style.py` | 0 |
| `gen_toc.py --check` | 0 |
| `check_em_dash.py --base ea3fb388` (0 findings, 687 added lines) | 0 |
| `check_doc_paths.py` (862 cited paths) | 0 |
| `ci_scope.py --selftest` | 0 |
| `check_baremetal_only.py --check`, `--selftest` | 0, 0 |
| `check_feature_status.py --self-test` | 0 |
| `git diff --check`; `ea3fb388 HEAD`; `e3f28f2f HEAD` | 0, 0, 0 |
| `gen_toc.py --verify-anchors` (285 links) | 0 |

## Reproduce (placeholders, not host paths)

```sh
python3 tools/round3_checks.py <evidence clone> 422dcf91008a09cb882dcc2b760779ce22e530cd
python3 tools/archive_check.py <evidence clone> 422dcf91008a09cb882dcc2b760779ce22e530cd <page at 26dfc82f>
python3 tools/table_identity.py <lane clone> e3f28f2f69343b54844ddfea368ef4cdd03facb6 26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778 docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
python3 tools/token_scan.py <private map> <regex tokens> <name tokens> <files...>
```

## Open for the manager

- Push `26dfc82f` to `b6-bench-1001` and apply `PR-BODY.md` to PR #630. The body keeps the `[A477]` first line, the template sections and "Relates to #629", with no closing keyword. It adds the Round 3 section and updates Status, roles, the two command blocks, Known limitations ("six ways") and the self-test DoD note.
- Self-test evidence at `26dfc82f` (the DoD item stays unchecked), hosted and act acceptance at the new head, and re-review of R426-2 F1 and F2.
- Archive this packet if reviewers are to re-run the round-3 receipts.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| PR-BODY.md | The PR #630 body for the manager to apply |
| TAKEN.md, TAKEN.readback.md, taken-url.txt | The #629 TAKEN post, read back, and its URL |
| REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt | The #629 REVIEW READY post, read back, and its URL |
| tools/ | `round3_checks.py` (new), plus `archive_check.py`, `table_identity.py` and `token_scan.py`, carried from round 2 unchanged |
| receipts/ | `round3-checks.txt`, `archive-check.txt`, `repro.txt`, `floor-check.txt`, `mask-check.txt`, `table-identity.txt`, `table-identity-r1.txt`, `table-diff.txt`, `token-scan.txt` |
| gates/ | `gates.txt` and each gate's output at `26dfc82f` |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
