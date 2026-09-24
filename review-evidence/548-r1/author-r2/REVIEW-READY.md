[A285] REVIEW READY

Head: `8544472a19a4b4d3853d64b15dea22f999372a32` (local commit, not pushed).
Parent: `e41703b2948ef53e5cb0dd01a1e13c5632637615`.

Changed: the two remaining `CTLR_DIAG` address-table/read-mux comments now state STRUCTURAL ZERO, the deleted source, processor ownership and ABI retention. The reserved-word note is preserved. This implements R308-1 F1 and R309-1 F1; delta reviews remain pending.

Validation: all assigned commands returned 0, without pipelines:

- `python3 scripts/xvlog_gate.py --check` (4 existing findings match the ratchet).
- `python3 scripts/check_rtl_source_lists.py`.
- `python3 scripts/check_sv_idiom.py`.
- `python3 scripts/lint_rtl.py --check` (90 existing violations match the ratchet).
- `python3 scripts/docs_check.py`, both Git and filesystem inventory modes; the latter used `GIT_DIR=/dev/null`.
- `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55`.
- `git diff --check`, also across the complete base-to-head range.

The tracked-tree search found no remaining current live-count claim for `CTLR_DIAG`/`0x6F4`; frozen history is unchanged. HANDOFF.md records its exact command and complete output. All 137 tracked RTL files are comment-free identical to `573f0052a0e4412e81f0845438fcec2086ce5d55`; the in-memory nonzero-tie control is detected. Every added/removed RTL line is a comment. All gitlinks are unchanged.

Acceptance for assigned items 1-3: met with the above evidence. The worktree is clean. HANDOFF.md and the full updated PR-BODY.md are prepared. Open implementation questions: none. Independent delta reviews by [R308] and [R309] remain required.
