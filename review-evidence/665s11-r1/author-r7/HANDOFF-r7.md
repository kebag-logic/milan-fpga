# HANDOFF: #871 (#665 S11), AECP REBOOT, round 7 ([A761c])

Status: REVIEW READY at `d3e61e37` (#871 issuecomment-6902228089), one commit on round 6's `33b0d03a`; nothing pushed by this lane. Next: one delta
review (R821-7) from `33b0d03a`; the sync onto #898's head when the manager relays it.

## The ruling

R821-6 NEGATIVE at `33b0d03a` (PR #881 issuecomment-6901483802; `review-evidence/665s11-r1/reviews/R821-6/REPORT.md`,
archive `cd3cb244`) on one MINOR, F1-R6, whose origin was the round 6 prescription `285 (280)`: the polls table's
parenthesis is round 22's figure by its legend, so the retained row reads `285 (250)`. The manager's ruling: that cell
and the PR body's round 6 row; every other parenthesis of the table checked against round 22's (`8684993388`); RS-R6-1's
three layout-only rewraps exactly; Markdown, comments and whitespace only, no firmware image change proved by sha256;
rerun docs_check, check_doc_style, the docs.yml steps, both idiom gates, whitespace and the firmware-unit build on a clean
clone of the final head. S-R6-1 is out of scope.

## The commit `d3e61e37` (4 files)

| File | Change |
|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:2238` | `285 (250)` for `285 (280)` |
| `sw/firmware/ctrl/test/test_plat_boot.cpp:187-188` | the comment's last two lines joined |
| `tb/verilator/ctrl_service_budget/poll_grade.py:72-73` | the short line refilled with the next |
| `sw/firmware/ctrl/plat/ctrl_plat.h:38-42` | the paragraph's tail rewrapped to its neighbours' 78 columns |

## Results

- The polls table's 11 parentheses each equal round 22's (`receipts/round22-parentheses.txt`).
- The three rewrapped files' text, comment markers aside, is identical to `33b0d03a`'s (`receipts/text-identity.txt`).
- The 8 split image files (fixture and platform, ELF and loadable binary, 1x1/1if and 8x8/1if) are byte-identical to
  `33b0d03a`'s and `d3566d44`'s (`receipts/identity/`).
- The reruns at `d3e61e37`: the PR body's round 7 table.
