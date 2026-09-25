[A293] REVIEW READY

Head: `490e4309749c83f92d794a8ff10d3043e0f5f080` on `510-mvu-waiver` (PR #118, round 2).

Items 1–3 are complete: merged-head counts re-measured and commit-qualified;
full Milan recommendation note and revision trigger recorded; phantom P-ID
replaced; M4L pins both waived SET responses under another controller's lock.
No RTL changes.

All required local processor gates returned 0, including every workflow gate,
`make check`, lint and the full bank: 33 suites, 1,014,637 checks, zero failing.
The top-level suite passes 7,666 checks. Both ROM mutations are rejected;
results and denominators are recorded for both the merged baseline and round 2.

Local parent consumer commit: `d1d1fbba98563524a46cc825e4cf9936603ef1bb`, based on
`35f0695815c202392b6b4806bb9f59dd110687ed`, with only the processor gitlink
changed. All ten gates returned 0; integration: 371 checks, zero failures.

HANDOFF.md and the full updated PR-BODY.md are in the assigned output packet.
Processor and parent tracked trees are clean. No push, PR edit, merge or hardware
operation was performed. REQ-MVU-005 timing remains in #57.
