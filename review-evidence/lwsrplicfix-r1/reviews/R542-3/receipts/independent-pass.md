# R542-3 independent pass (written before reading any prior review report or finding)

Recorded 2026-10-07 after the reviewer's own runs, before opening R542-1, R542-2 or R543-1 material.

- Diff a4cbe41..f800a2b: one path, `LICENSE`, two lines removed (SPDX line and blank line); 0 additions.
- Head `LICENSE` is byte-identical to the canonical Apache-2.0 text fetched from apache.org (cmp rc 0; sha256 cfc7749b...d30; blob d6456956...cd7).
- Base `LICENSE` minus its first two lines equals the canonical text, so nothing else in the file changed.
- GitHub licence API: base/main ref NOASSERTION; head ref Apache-2.0 (repository-level value updates only after merge to main).
- SPDX sweep: 60 tracked files at base all carry the header; at head 59 do, the only exception being LICENSE. Only LICENSE changed.
- Removing LICENSE in a disposable copy makes the link checker fail with 4 missing-target links, so the required-licence-link rule still guards the file.
- Every documented check at head ran with rc 0: sentences 975/0, references 0 unlinked, self-test 79/0, links 354 local + 20 external/0 failures, render 27 graphs/0 failures, both profiles configure/build/ctest/unit/behave/dry-run rc 0 (86 tests; 19885 OFF, 19873 ON), isolated codec 1690, freestanding x2, embedded, reversals 93/0 in both profiles.
- The live PR body equals the published validation2/PR-BODY.md apart from one trailing newline the API adds. Every row in its Validation table matches the reviewer's runs.
- The commit subject is one line with no body or trailers, as CONTRIBUTING requires.
- Provisional own findings: none at MINOR or above. Possible wording-only observation: Validation-table tool names other than the link checker are not links (the CONTRIBUTING link rule targets repository documentation, so at most RESIDUE).
- Provisional verdict: POSITIVE, subject to resolving prior findings.
