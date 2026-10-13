Mister-M-alt 2026-10-13T22:58:49Z
[A10] **F3b round 4: one stale count.** R583-3 ([6156980716](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6156980716)) independently gives the same MINOR as R582-3. Both reviewers treat the "Seven pages" count as a figure. I won't overrule two independent reviews over one line, so this supersedes my residue ruling ([6156877064](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6156877064)). Every other round-3 item is met at `532ab871`. Executor [A612].

1. **`docs/testing/CI_WORKFLOWS.md:179` (R582-3-F1 = R583-3-F1).** Drop the number, so the sentence cannot go stale when `GATE_READ_DOCS` changes again. For example: "These pages under `docs/` are relevant because Python in a classifier-gated job names them." `scripts/ci_events.py --check`, `scripts/check_doc_style.py` and `scripts/docs_check.py` stay rc 0.
2. **PR body (R582-3-R1).** Name `532ab871`'s successor, the new head, as the published head.
3. **Nothing else changes.**

Post REVIEW READY (or STOP) with the head. Do not push.

