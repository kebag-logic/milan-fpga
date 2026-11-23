# Receipt indexes against the published blobs (#584, R894-2 F5-R2, R893-2 F7)

Each index's rows are checked against the Git blobs of evidence commit `e3127c91` (`auditidx.py`: size and sha256 of every indexed file, read from the commit).

| Index | Rows that match their published blob |
|---|---|
| `author-r1/receipts/INDEX.md`, the original round-1 index | 77/80 |
| `author-r2/receipts/f5/round1-INDEX-corrected.md`, its replacement, published in round 2 | 80/80 |
| `author-r2/receipts/INDEX.md`, the original round-2 index | 14/16 |
| `f5/round2-INDEX-corrected.md`, its replacement, in this round | 16/16 |

Cause of the mismatches: publication redacted private home-path prefixes in three round-1 receipts, and in two round-2 receipts that quoted them, after their indexes were written. No measurement, result or return code changed.

This round's receipts contain no host path. `pubcheck.py` passes every one of them, and the index, through the manager's publication rewrite: `privacy.scrub_redact` and the host-prefix rewrites. Each comes through byte-identical, so the sizes and sha256 in this round's `INDEX.md` are those of the files as they will be published.
