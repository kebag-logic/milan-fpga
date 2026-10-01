[A481] REVIEW READY
Commit: `26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778` on `b6-bench-1001`, parent `e3f28f2f69343b54844ddfea368ef4cdd03facb6`. Local, not pushed. Pushing it and applying the round-3 PR body to PR #630 are the manager's.
Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only (+44 / -18), for the round-3 assignment (comment 5933253532), answering R426-2:
- Item 1: "Where the packet is" and the reproduction commands are re-pinned to `422dcf91008a09cb882dcc2b760779ce22e530cd`. Both were rerun from that commit alone, taken with `git archive` and no checkout. The tone loop hashes to `566d3dfa...5588` (48,000 unique pairs, no silent frame), and `b6_thdn.py controls` is byte-identical to the archived `controls.json` (`cmp` silent, ALL_PASS). At that commit 400 of 400 manifest files re-hash to `published_sha256`, with none unlisted or missing. All 54 page hashes resolve: 33 to `original_sha256` (12 label-masked) and 21 to `RAW-ARTIFACTS.json`. R426-2's mask check there reports RESULT CLEAN.
- Item 2, R426-2 F2(a): Method item 4 says six of the seven clusters under 98 frames have a measured rise of 0.99 to 1.00 ms. The seventh, A1's 60-frame skip after a 33 ms read stall (cluster 9), has no measurable rise and passed on the read gap alone, the gap-only branch of item 5.
- Item 2, R426-2 F2(b): the capture-path bullet separates two kinds of cluster. The gap-only clusters have an unmeasurable rise: 1 in A0, 2 in A1, 5 in A2, 3 in B INTERNAL and none in B CRF, every skip still 48 n + 12. A2's clusters 17 and 56 have a measured rise that does not match (154.5 ms for 60 frames, -155.8 ms for 1,020 frames). They passed on the read gap and size rule, item 3.
- Item 3, R426-2 S1 to S4, all taken:
  - S1: a sixth way in Method. A multi-frame listener step within 300 ms of a capture loss joins its cluster, with a tolerance of about 249 ms at A1's 12.4 s loss. Item 1's per-step sizes exclude it in A1 and B CRF, and a one-frame event never joins a cluster. Limits now says six ways.
  - S2: run the commands in a fresh clone or a disposable worktree. The page records the versions they were reproduced with (Python 3.14.7, NumPy 2.5.3) and says the original run's were not recorded.
  - S3: the round-2 packet `b6-a480` maps to `review-evidence/b6-r1/author-r2/` at the same commit, with its floor check (rerun here, identical to its receipt) and attribution checks.
  - S4: "each graded case's `events.jsonl`".
Validation (at `26dfc82f`, physical lane path, outputs to files, never piped): all rc 0.
- Markdown gates in the pinned environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base ea3fb388` and `check_doc_paths.py`.
- Repository gates: `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, and `check_feature_status.py --self-test`.
- `git diff --check`, also against `ea3fb388` and `e3f28f2f`.
- Tables: all 15 are byte-identical to `e3f28f2f` and to `b5e9242e`, with none added or removed. Every table line of the three commits (161 lines, 16,010 bytes) has sha256 `540ab528...d847`, and `diff` is empty.
- Every new statement was re-derived from the published `grade.json` and `events.csv` at `422dcf91`: RESULT PASS.
- Private-name and capture-layout scan of the diff, the page, the commit message and the round-3 packet: no private name. The only hits are known benign ones, none in the diff:
  - the round-1 page's DUT-side tone-loop channel lines;
  - the four-part clause numbers in the PR body's references, unchanged from the live body;
  - the lane path in the gate log.
Acceptance criteria: assignment items 1 to 3 met as above. No rule, verdict or measured figure changed, and every table is byte-identical.
Open risks/questions:
- R427-2 S2 (the 12.4 s loss's edge residual as up to about 1 ms) and S3 (a fourth, actionless lock window) were outside this assignment and are not taken.
- The round-3 packet (`b6-a481`) is not yet archived.
- Still pending: self-test evidence, hosted and act acceptance at the new head, and re-review.

