[A262] REVIEW READY

Head: `a024ab51b926690be5ade8ec35ec1fa7dd23981b` on `43-49-gsi-internal` (local commit, not pushed).

Round 2b for PR #111 / issues #43 and #49: split the SRP stream failure-change test at its existing reset boundaries. The three scenarios are 79, 20 and 24 lines; the file maximum is 90 against the 100-line limit. The unchanged parent measurement and zero budget pass; temporary scratch copies were deleted.

Before/after stream output is identical: `1087 checks: 1087 PASS, 0 FAIL`. All four SRP suites pass. Full bank before/after output is identical: 32 suites, 16416 checks, 0 failing. Full bank and lint both return 0, run in the foreground without output pipelines.

Handoff and evidence: `$MANAGEMENT/2026-09-23/pp43-a262/HANDOFF.md`.
