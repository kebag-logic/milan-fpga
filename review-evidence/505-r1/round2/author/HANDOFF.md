[A159] COMMITTED HANDOFF

Revision head: `ad62493186576144f9fa1568babad012bc9ad8ca`
Parent: `6af65a151663e1301f1983a6c9d22650a0b35da9`
Live base verified: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`
Branch: `407-carrier-script-pins`
Worktree: `$CANDIDATE`
Commit: `Add per-line carrier script regression controls`

The checkout is clean. The revision changes only `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md` (48 insertions, 20 deletions). No rebase or public head push occurred. Remote PR head remains the starting head. The normal three initialized submodules retain their gitlinks; external remains uninitialized as at entry.

Launch authority: manager assignment [5771751574](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5771751574) confirms A158 finished and assigns this sole author slot. Own TAKEN: [5771766429](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5771766429). R219/R220 remain the manager-assigned cold reviewers.

Implemented findings: duplicated F1 (MINOR Docs) and F2 (MINOR Tests, Conformance), with the accepted append/reorder, population, comments and maintenance suggestions. See RESPONSE.md for individual mappings. No finding is deferred or relabeled; reviewer acceptance remains pending.

Measured committed-head results:

- Actual pristine `ci_events.py --check`: exit 0, 1,505 contract items.
- Actual full `--selftest`: exit 0, 1,144 arms. There are 1,046 workflow mutations, including 456 carrier mutations; 213 new reason-pinned arms comprise 117 non-last swallowing, 56 append and 40 reorder controls.
- M5b passed all 931 arms before revision and accepted the exact AC5 edit. At this head it fails 117 arms, including Python idiom step 34 line 1. Prefix-only fails 56; order-insensitive fails 40; removed comparison fails 400; removed record enforcement fails 56. Every mutant still passes pristine `--check`.
- All 833 pre-revision mutation names, expected fragments and edits are unchanged. All 590 specialized refusals work with the new carrier helper disabled. AST comparison changes only `_carrier_script_edits` and `_carrier_script_arms`; the production comparator, records, normalization and other functions are unchanged.
- All 173 normalized carrier lines have swallowing controls, including all 14 `--check` lines and bounded ratchets at docs-check steps 26/28/30/31. The exact AC5 Python call is covered at step 34 line 1.
- Whitespace and record-update positives pass. A scratch workflow-only appended command is refused at step 34 line 3; an explicit matching canonical update passes the actual check and full self-test, automatically deriving 1,145 arms.
- Docs, TOC, paths, em-dash, doc style, Python idiom/check+selftest, hygiene, TODO ownership, fail-fast, feature-status, lint and diff checks passed. Lint: 90 <= 90, 17 waived. Committed-head em-dash: 47 added lines, zero findings, 34/34 controls.

Files for publication/review:

- `REVIEW-READY.md`: factual author evidence comment, no verdict.
- `PR-BODY.md`: replacement description for the final implementation, using the PR template.
- `RESPONSE.md`: every finding and accepted suggestion mapped to code and receipts.
- `COMMANDS.md`, `MUTATIONS.md`: commands, definitions, controls, measured results.
- `before/`, `after/`, `controls/`, `gates/`, `committed-gates/`: exact source variants/input snapshots, JSON commands/results and raw logs.
- `public-state/`, `archive-probes/`: exact public reports/decisions and immutable reviewer instruments read.
- `integrity.json`, `revision.patch`, `SHA256SUMS`: source state, patch and receipt hashes.

Manager-owned remaining work: publish the final head/evidence, trusted act-first replica, full mandatory native/hosted gates, AC5 remeasurement if the manager judges it affected, independent R219/R220 re-review and reviewer-owned lens ledger, candidate merge and containment. This author ran no Docker/act, candidate orchestrator, full parent sweep, builder, hardware, subagent, merge or PR-state mutation. The checker-only AC5 analogue is not a new act receipt. Historical review/CI results are not asserted for this new head. No author verdict is provided.
