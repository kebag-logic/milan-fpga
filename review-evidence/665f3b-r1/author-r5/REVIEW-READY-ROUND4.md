[A612] REVIEW READY - F3b round 4

Commit: `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` (one new local commit after `532ab871`; no push).

Changed: `docs/testing/CI_WORKFLOWS.md:179` now opens "These pages under `docs/`" instead of "Seven pages", answering R582-3-F1 / R583-3-F1. The sentence states no count, so it cannot go stale when `GATE_READ_DOCS` changes. The prepared PR body names `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` as the published head (R582-3-R1 / R583-3-R1). Nothing else changes: one line in one file.

Validation, at the committed head with CPython 3.12.3, all rc 0:
- `python3 scripts/ci_events.py --check`: 2169 contract items. `--selftest`: 3064 arms.
- `python3 scripts/check_doc_style.py` and `--selftest`.
- `python3 scripts/docs_check.py` and `--selftest`: 23 scrub and 4 routing arms.
- `python3 scripts/ci_scope.py --selftest`: 109 checks, eight gate-read pages. `ci_scope.py docs/testing/CI_WORKFLOWS.md` prints `false`.
- Added-line em-dash, doc paths, contents/anchors, bare-metal, hygiene and documentation map checks, each with its self-test.
- Packet check `round4/gate_read_paragraph.py`: the paragraph links eight pages and `GATE_READ_DOCS` registers eight. Six planted controls are refused, including restored "Seven", stated "Eight" and a dropped link. On the `532ab871` page it returns 1.

Acceptance: both round 4 items are met. The integrity audit confirms one changed path, unchanged gitlinks and pin `70936b77`, raw blobs and modes for 1311 parent and 1043 dependency files, and a clean checkout. Firmware and image inputs are unchanged, and all 30 retained ELF digests still match. HANDOFF.md, PR-BODY.md and the round4 receipts are in the evidence packet.

Open risks/questions: none. The manager owns the push, the workflow replica, exact-head hosted acceptance, independent new-head review and the rest of the merge bar. No hosted or review verdict is claimed.
