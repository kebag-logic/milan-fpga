[A359] TAKEN
Branch: `396-release-gates`, starting head `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`.
Authoritative references: round-2 decision 5854930205; round-1 assignment 5854692245; REQ-VER-06; TESTING 6d; the cited Milan and IEEE clauses, extracted directly for this round.
Interpreted scope: desk acceptance items 1, 2 and 5, addressing both round-1 reports. Post-cut timing follows the recorded T0 decision; the additional controller reconnect check retains its separate origin. The stated sampling ceiling will be 60 seconds, matching the existing default cadence. The boot observation margin defaults to 5 seconds and remains a named parameter; it cannot relax restoration or advertisement deadlines. Explicit topology requires both descriptor-derived device specifications. The release boot assertion will reject a repeated BIOS pass, including the #366 negative control; the existing per-flash smoke check has a narrower scope.
Validation plan: all round-1 gates, both unchanged public mutation scripts, both public omission/audit probes, and the corrected contract controls. Public review scripts were fetched from `396-review-evidence` and extracted into temporary storage.
Reviewers: internal and external reviewers assigned in the round-2 decision.
Blockers: none. Physical campaigns and the hardware negative control remain open. No push or PR modification will be performed.
