[A761c] REVIEW READY
Commit: `d3e61e37` (branch `665-s11-aecp-reboot`; one commit on round 6's `33b0d03a`; not pushed, the manager pushes)

Round 7 is the manager's ruling on R821-6 (NEGATIVE, F1-R6) at `33b0d03a`. The commit changes Markdown, comments and whitespace only, and no firmware image changes.

Changed (4 files):
- **F1-R6:** `SPLIT_CONTROL_MEMORY.md:2238` now reads `285 (250)`. By the table's legend the parenthesis is round 22's figure, and round 22's retained figure was 250. The PR body's round 6 row says `285 (250)` too.
  - All 11 parentheses of the polls table equal round 22's figures in `git show 8684993388:docs/design/SPLIT_CONTROL_MEMORY.md`.
- **RS-R6-1, exactly, with no text changed:**
  - `test_plat_boot.cpp:187-188`: the comment's last two lines joined.
  - `poll_grade.py:72`: the short line refilled with the next.
  - `ctrl_plat.h:38-42`: the paragraph rewrapped to its neighbours' 78 columns.
  - With comment markers aside, each file's text has the same sha256 as at `33b0d03a`.
- **S-R6-1:** out of scope; the manager opens its own issue.

Validation, on a clean clone of `d3e61e37`:
- **Image identity:** the size fixture's and the platform's split images at 1x1/1if and 8x8/1if, ELF and loadable binary. All 8 files are byte-identical to `33b0d03a`'s and `d3566d44`'s by sha256.
- **The gates the touched files feed:**
  - whitespace against the merge base and `33b0d03a`, both idiom gates, `docs_check.py` and `check_doc_style.py`: rc 0;
  - `docs.yml`: 64 steps rc 0, 31 not run with a reason, 0 bad;
  - `firmware-unit`: every step rc 0. It compiles and runs `test_plat_boot.cpp` at one and two interfaces; the saved-state suites pass (526 tests) and coverage passes (39 files).
- **Carries:** round 5's legs and final pass, and round 6's gates, carry unchanged.

Acceptance criteria: items 2 to 5 met. Item 1 is met for six of the eight items and the binding, as before, so the PR still says Relates to #871.

Open risks/questions:
- Not taken, as optional: earlier rounds' suggestions.
- The #898 sync reruns the survey; the 1x1/1if margins are 0.25, 0.26 and 0.78 ms.
- The packet is `665s11-a761c/round7/` (PR body, HANDOFF-r7, receipts, INDEX).
