[A720g] TAKEN
Branch: 640-mark2-charter (round 7 on PR #828, from head 3f5fea24; local, not pushed by this lane)
Authoritative references: the owner decisions of 2026-11-01 13:35 on #640 (issuecomment-6558021030); R757-6 RR11 and R758-6-R1 on PR #828
Interpreted scope: docs only. Restate NFR-LAT-03 as a target (SHOULD be below 65 us, as short as possible; derived bounds accepted and published; no connection refused because of them; the bench reports each case against the target). Remove open question 1 of the stream-engine design and state the decision once on that page, keeping the bounds tables. Align the area plan's D14 and target rows. Apply the two round-6 residue items to the lapse sentence. The other open owner decisions stay open; no figure changes.
Validation plan: every step of the docs workflow on the committed head, each rc recorded; git diff --check against the merge base.
Blockers: none
