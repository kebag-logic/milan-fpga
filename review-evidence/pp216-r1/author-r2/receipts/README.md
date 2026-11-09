# Receipts, issue #216 round 2 (head 84f6d6a)

Host paths in copied logs are replaced by placeholders (`<lanes>`, `<scratch>`, `<out>`, `<toolchain>`, `<home>`,
...); a file over 200 KB is not copied but listed with its size and sha256 in that directory's RAW-RECORDS.txt.

| Directory | What |
|---|---|
| STANDARDS.txt | the clauses read this round |
| head-84f6d6a/proc | make check, the matrix, the HDL lint, Yosys portability, the elaboration guards, the nvm_port figures (with PR #13's ref fetched), the whitespace check |
| head-84f6d6a/sweep | the full suite sweep as four shard units: each shard's spec, run record, log and suite assignment; the merged record, the merged requirement-tag evidence and its executed check |
| head-84f6d6a/camp-srp | the SRP campaign (every arm, the coverage check), the README count comparison, the per-arm change against the previous head, selected arm logs |
| head-84f6d6a/camp-pp | the two AECP campaigns |
| head-84f6d6a/camp-more | the MAAP, ADP, AECP command and elaboration-guard campaigns |
| area | the area flow at 60094a2, at the round 2 HDL and at the head; main's figures from round 1 |
| parent-84f6d6a | the scratch-parent consumer gate: the pin, the ROM digests, 40 gates |
| twin-84f6d6a | the two-placement simulation with the head pinned |
| stream-link-bounce | the report-only probe of the stream Applicants across a link bounce |
| r802-probes | the second review's probes, as published, at the head |
| self-probes | five one-edit probes of the new VID link lines |
| counts-pre-commit | the arm counts measured before the commits, from which the README tables were written |
