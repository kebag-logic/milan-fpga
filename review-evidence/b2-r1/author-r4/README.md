# [A449] PR #622 round 4 packet (bench lane B2, docs only)

Round 4 of PR #622 under the assignment on #606 (comment 5889146437), answering F6 of R404-3 (PR comment 5889116666) and R405-3 (PR comment 5889142925). One commit, `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`, on the round-3 head `fb4a1b895e97bb808b624ea0b31c43d121723f36`. No bench access in this round. `HANDOFF.md` gives the change with file:line, the census, the table-identity proof, the gates and the token scan.

Files:
- `HANDOFF.md`: state, change, derivation and results.
- `TAKEN.md`, `REVIEW-READY.md`: the two public comments on #606, as posted.
- `PR-BODY.md`: the proposed PR #622 body for round 4 (the PR itself is not edited in this round).
- `receipts/pr-body-round3-live.md`: the PR #622 body as live at the round-3 head.
- `scripts/census_b2r4.py` -> `receipts/census_b2r4.txt`: every command in the controller transcripts, by protocol, command, target entity and descriptor. It checks the four F6 statements: 0 state-changing commands to a DUT stream input; the 210 `CONNECT_RX` and `DISCONNECT_RX` all to the peer's Stream Input 8; every AECP command GET_ or READ_; the 460 commands to a DUT stream input all reads (228 GET_RX_STATE, 228 GET_COUNTERS, 4 READ_DESCRIPTOR). Every transcript read is checked against the archive manifest.
- `receipts/tables_r2_round4.txt`: the reviewers' `tables_r2.py`, unmodified, from the round-3 head to the round-4 head, and the PR body's tables against the pages.
- `scripts/table_lines_diff_b2r4.sh` -> `receipts/table_lines_diff_b2r4.txt`: a literal `diff` of every table line on the three PR pages (round-3 head against round-4 head) and in the PR body (`receipts/pr-body-round3-live.md` against `PR-BODY.md`).
- `receipts/head_identity.txt`: head, tree, parent, subject, `git diff --raw` from round 3 and from base, and gitlinks.
- `scripts/run_gates_b2r4.sh` -> `receipts/gates/`: the assigned gates at the round-4 head, one file per gate, rc in `gates.txt`.
- `scripts/token_scan_run_b2r4.py` -> `receipts/token_scan_b2r4.txt`: both reviewers' token scanners over this directory, with a private deny-list built in memory and passed through a pipe.
- `MANIFEST.sha256`: every file above.

Inputs (read-only, not copied here):
- The round-1 author packet as recorded. Its redacted copy is `review-evidence/b2-r1/author/` on branch `b2-review-evidence` (tree `fdde402a9bef91a271d7efc744194fa9afed4ffc`, unchanged at the branch tip `5d305ef68d644b14a5b345e7214876718312832c`). All 561 `*.jsonl` files `census_b2r4.py` reads equal the manifest's `original_sha256`; 449 of them are archived as redacted copies, so a rerun on the public copy checks them against `published_sha256` instead.
- The archive's `review-evidence/b2-r1/MANIFEST.json` at `5d305ef68d644b14a5b345e7214876718312832c`: 579,737 bytes, sha256 `97d7dc21e9ae6339d628c90475e6d83b85259d9a1b72c1cc73b3435302da15b4`, git blob `208980d001b691c19c8c0401b81f5b97eaec7c42`. Not copied (over 200 KB).
- The reviewers' `tables_r2.py` (sha256 `8f02e573ba3674c0f9211bf17cb2e0a768015ad98a0765380374223264931877`, the R404-3 packet's copy) and `token_scan.py` (sha256 `7528b5b6de1779c6eee61b1cdb158b37f094833d5df4d3d3f79d86d6fa0cef14`), and R405-2's `r405_scan_tokens.py` (sha256 `3444b6c2480b36faaa4a2c3b5f58ddd2079a9e23ebaa840e58aae6518bdebdf2`), run unmodified from the review packets.

Reproduce, from this directory:
- `python3 -B scripts/census_b2r4.py <round-1 author dir> <MANIFEST.json>`
- `python3 -B <R404-3 scripts>/tables_r2.py <clone> fb4a1b895e97bb808b624ea0b31c43d121723f36 5c57927413e0dae279f06a75d2a58e3fec8a2bb0 PR-BODY.md`
- `bash scripts/table_lines_diff_b2r4.sh <clone> fb4a1b895e97bb808b624ea0b31c43d121723f36 5c57927413e0dae279f06a75d2a58e3fec8a2bb0 receipts/pr-body-round3-live.md PR-BODY.md <scratch>`
- From the clone: `bash <this dir>/scripts/run_gates_b2r4.sh <pinned Markdown python> <out dir>`
- `SCAN_STAGE=<empty scratch> EXTRA_PRIVATE=<names> python3 -B scripts/token_scan_run_b2r4.py <clone> <round-1 author dir> <MANIFEST.json> 5d305ef68d644b14a5b345e7214876718312832c <R404 scripts> <R405-2 scripts> <this directory>`
- Verify the packet: `sha256sum -c MANIFEST.sha256`.

No script here prints an entity identifier or a private name. The census receipt prints role labels and counts, and the scan receipt prints masked classes, hash prefixes and counts only.
