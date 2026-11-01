[A720h] TAKEN
Branch: 640-mark2-charter (round 8 on PR #828, from head e7310e94; local, not pushed by this lane)
Authoritative references: R757-7-F1 and R758-7-R1 on PR #828 (issuecomment-6558867513, issuecomment-6558924964); the owner decisions of 2026-11-01 13:35 on #640 (issuecomment-6558021030)
Interpreted scope: docs only. NFR-LAT-03: 65 us stays a target; the bench reports every case against it; a case above 65 us is reported, not failed, and no connection is refused; a case is graded against a bound only where one is derived, the 16-reservation table; with fewer reservations no maximum is derived, and 143.347 us is quoted as reached, not as a limit. Stream-engine design: the fewer-reservations table gains the reviewer's reached cases as examples, and one open design item asks lane 6 to derive the maximum. Area plan rows 60, 255 and lane 6, and the PR body, agree. No mechanism, no new derivation, no other figure changes.
Validation plan: every step of the docs workflow on the committed head, each rc recorded; git diff --check against the merge base.
Blockers: none
