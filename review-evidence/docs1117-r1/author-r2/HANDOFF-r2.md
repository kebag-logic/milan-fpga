# HANDOFF r2: docs1117, issue #940 (author [A795])

Status: REVIEW READY (all five docs jobs green on clean clones of ee5c6f92)

- Repository: milan-fpga, branch `docs-batch-merge`, base dev `6b66f66d` (live dev unchanged, checked with `git ls-remote`).
- Head: `ee5c6f92`, two commits on dev:
  - `490d54ee` (round 1): draft pieces (a) to (h), verbatim.
  - `ee5c6f92` (round 2): splits the paragraphs over 30 words. It adds 5 blank lines and changes no word or order.
- Not pushed and no PR opened: the manager pushes and opens the PR.
- Scope point: the owner asked for standing process. The draft wording is kept, and the PR body no longer lists the scope as an open risk.

## Round 2 change (file:line at ee5c6f92, and reason)

| Location | Before (round 1) | After | Reason |
|---|---|---|---|
| AGENTS.md:302-306 (section 6) | one 40-word paragraph | 19 + 21 words, split after "...the composed measurements." | owner rule: paragraphs of at most 20-30 words |
| AGENTS.md:401-408 (section 7, inside the "every lens" bullet, 2-space indent kept) | one 63-word paragraph | 23 + 21 + 19 words | same |
| docs/testing/CI_WORKFLOWS.md:273-281 ("Fast feedback") | one 70-word block (the draft's 4 lines + 3 existing lines) | 24 + 19 + 27 words | same; "Those banks" in the third paragraph still refers to the first paragraph's builder and native banks, the only banks in the passage |

`git diff --ignore-all-space --ignore-blank-lines 490d54ee ee5c6f92` is empty (`receipts/paragraph-counts.txt`, `receipts/draft-lines.txt`).

## Paragraph counts (every new or changed prose block; words counted with check_doc_style's own normalisation)

| Block | Words |
|---|---|
| CONTRIBUTING.md:189-190 step 7 batch note (c) | 22 |
| CONTRIBUTING.md:425-427 2.3 decision links (a) | 16 |
| CONTRIBUTING.md:429-430 2.3 scope (a) | 24 |
| CONTRIBUTING.md 2.3 lead-ins (Freeze., Batch., ...) | 1-3 each |
| CONTRIBUTING.md 2.3 bullets (a) | at most 14 each |
| AGENTS.md:298-300 frozen PR (d) | 29 |
| AGENTS.md:302-303 composition review (d) | 19 |
| AGENTS.md:305-306 lens coverage (d) | 21 |
| AGENTS.md:401-402 composed batch (e) | 23 |
| AGENTS.md:404-405 new change (e) | 21 |
| AGENTS.md:407-408 conflict-free interactions (e) | 19 |
| AGENTS.md:430-431 completion bullet (f) | 20 |
| AGENTS.md:469, 470 never-rules (g) | 17, 17 |
| CI_WORKFLOWS.md:273-274 (h) | 24 |
| CI_WORKFLOWS.md:276-277 (h) | 19 |
| CI_WORKFLOWS.md:279-281 existing lines, now their own paragraph | 27 |

Blocks over 30 words: 0. The full per-block listing is `receipts/paragraph-counts.txt`, from `receipts/tools/para_counts.py`, which exits 1 if any block is over the limit.

## Checks and planted mutants at ee5c6f92 (clean clone)

| Check | Result | Receipt |
|---|---|---|
| draft lines (blank lines ignored) equal the draft's, file by file | True for all three files; (d), (e) and (h) are no longer byte-verbatim, as intended | `receipts/draft-lines.txt` |
| whitespace-insensitive diff vs round 1 | 0 lines | `receipts/draft-lines.txt` |
| gen_toc --verify-anchors | 620 (617 on dev) | `receipts/anchors-and-em-dash.txt` |
| check_em_dash on 122 added lines | 0 findings, rc 0 | `receipts/anchors-and-em-dash.txt` |
| M1 AGENTS.md fragment -> mergez | gen_toc rc 1 `MISS AGENTS.md -> CONTRIBUTING.md#23-batched-mergez` | `receipts/mutants.txt` |
| M2 CONTRIBUTING.md same-page fragment -> mergez | no repo gate fails (known gap); scratch check rc 1 `MISSING` | `receipts/mutants.txt` |
| M3 CI_WORKFLOWS.md path ../CONTRIBUTING.md | docs_check rc 1 `broken link -> ../CONTRIBUTING.md` | `receipts/mutants.txt` |
| M4 CI_WORKFLOWS.md fragment -> mergez | gen_toc rc 1 `MISS docs/testing/CI_WORKFLOWS.md -> ../../CONTRIBUTING.md#23-batched-mergez` | `receipts/mutants.txt` |
| mermaid | CONTRIBUTING.md blob `2ff614ba` is identical to round 1, so round 1's render (both rc 0) applies | `receipts/anchors-and-em-dash.txt` |

## Gates (docs workflow replay, clean clone per job at ee5c6f92)

Same method as round 1, using `receipts/tools/replay_docs.py`:
- a fresh `--no-local` clone per job, detached at the head, origin set to the public repository;
- a fresh CPython 3.12 venv and a fresh scratch HOME (the RV32 SDK installs from its pinned archive);
- every `run:` body executed verbatim under `bash --noprofile --norc -eo pipefail`.

| Job | Where it ran | Run steps | Result |
|---|---|---|---|
| wire-accountability | session (before the shutdown) | 3 | success |
| docs-check-no-git | session (before the shutdown) | 2 | success |
| docs-gates-0 | unit milan-a795-docs1117-g0, CPUs 56-63 | 48 | success |
| docs-gates-1 | unit milan-a795-docs1117-g1, CPUs 48-55 | 8 | success |
| docs-gates-2 | unit milan-a795-docs1117-g2, CPUs 16-23 | 10 | success |

- 71 run steps in all, every rc 0. The per-step table is `receipts/gate-table.md`, and the logs are in `receipts/logs/<job>/`. The one log over 150 KB is recorded by sha256 and size only.
- Not run (hosted-only): action steps (checkout, cache, upload), evidence recording, apt package resolution, and the `docs-check` receipt-union job.
- Substituted, as in round 1: the sv2v install uses the same pinned archive and sha256, installed into a scratch bin.
- Every clone was still clean after its job. protocol-processor in the gates clones has the processor repository as origin.
- Peak MemAvailable stayed above 70 GB. All three units have exited, and no process of this lane is running.

## Restart record

- 07:25 host shutdown. The round-2 replays of docs-gates-0/1/2 were killed with no summary, so they count as cut, not passed. Their output was removed and they were re-run.
- docs-check-no-git and wire-accountability had already recorded `RESULT success` with a summary, so they stand.
- After the restart the host has 96 CPUs. The re-runs are units `milan-a795-docs1117-g0/1/2` (MemoryMax 10G), each on a range from `cpu_ranges.py pick`.

## Comments on #940

- Round 1: `[A795] TAKEN` issuecomment-6939809424, `[A795] REVIEW READY` issuecomment-6940360656.
- Round 2: `[A795] REVIEW READY` issuecomment-6941601004 (text in `REVIEW-READY.md`). It replaces round 1's for review.
- No other comment was posted, edited or deleted.

## For the manager

- Push `docs-batch-merge` at `ee5c6f92`, then open the PR against `dev` with `round2/PR-BODY.md` (first line `[A795]`, `Closes #940`, `Relates to #665`).
- Reviewers are still unnamed (`[R<n>]` placeholders).
- Scratch (clones, venvs, the SDK) is outside the output directory.
