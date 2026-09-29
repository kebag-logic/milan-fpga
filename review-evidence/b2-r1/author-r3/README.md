# [A447] PR #622 round 3 packet (bench lane B2, docs only)

Round 3 of PR #622 under the assignment on #606 (comment 5888700643), answering R404-2 (PR comment 5888547222) and R405-2 (PR comment 5888695807): F5 and R404-2 S3. One commit, `fb4a1b895e97bb808b624ea0b31c43d121723f36`, on the round-2 head `d76763733e088cd21bbdd587927c8cf2f26cc8b3`. No bench access in this round. `HANDOFF.md` gives the change with file:line, the poll count, the table-identity proof, the gates and the token scan.

Files:
- `HANDOFF.md`: state, change, derivation and results.
- `TAKEN.md`, `REVIEW-READY.md`: the two public comments on #606, as posted.
- `PR-BODY.md`: the proposed PR #622 body for round 3 (the PR itself is not edited in this round).
- `scripts/poll_count_b2r3.py` -> `receipts/poll_count_b2r3.txt`: every DUT stream-input poll in the controller transcripts, per input and per file role, with each action's `snapshot.jsonl` checked against its siblings and left out as a byte copy, and every transcript read checked against the archive manifest.
- `receipts/tables_r2_round3.txt`: R404-2's `tables_r2.py`, unmodified, from the round-2 head to the round-3 head, and the PR body's tables against the pages.
- `scripts/table_lines_diff_b2r3.sh` -> `receipts/table_lines_diff_b2r3.txt`: a literal `diff` of every table line on both pages (round-2 head against round-3 head) and in the PR body (`receipts/pr-body-round2-live.md` against `PR-BODY.md`).
- `receipts/pr-body-round2-live.md`: the PR #622 body as live at the round-2 head.
- `receipts/head_identity.txt`: head, tree, parent, subject, `git diff --raw` and gitlinks.
- `receipts/gates/`: the assigned gates at the round-3 head, one file per gate, rc in `gates.txt`.
- `scripts/token_scan_run_b2r3.py` -> `receipts/token_scan_b2r3.txt`: both reviewers' token scanners over this directory with a private deny-list built in memory and passed through a pipe.
- `MANIFEST.sha256`: every file above.

Inputs (read-only, not copied here):
- The round-1 author packet as recorded. Its redacted copy is `review-evidence/b2-r1/author/` on branch `b2-review-evidence`. `poll_count_b2r3.py` takes its directory as the first argument; all 561 transcripts it reads equal the archive's `original_sha256` (449 of them are archived as redacted copies, and the redaction does not touch the fields read).
- The archive's `review-evidence/b2-r1/MANIFEST.json` at archive commit `4fb092069a6bf9b1ecad3cc94f7cd03a400e6a01`: 554,276 bytes, sha256 `5e472758594273a11b63c6c6e83f22d54b4e0b3a697cdaab8bd997f319a65772`, git blob `f3bfbdc9e7199a564d2ab268c08a2e3d0208edb4`. Not copied (over 200 KB).
- R404-2's `tables_r2.py` (sha256 `8f02e573ba3674c0f9211bf17cb2e0a768015ad98a0765380374223264931877`) and `token_scan.py` (sha256 `7528b5b6de1779c6eee61b1cdb158b37f094833d5df4d3d3f79d86d6fa0cef14`), and R405-2's `r405_scan_tokens.py` (sha256 `3444b6c2480b36faaa4a2c3b5f58ddd2079a9e23ebaa840e58aae6518bdebdf2`), run unmodified from the review packets.

Reproduce, from this directory:
- `python3 -B scripts/poll_count_b2r3.py <round-1 author dir> <MANIFEST.json>`
- `python3 -B <R404-2 scripts>/tables_r2.py <clone> d76763733e088cd21bbdd587927c8cf2f26cc8b3 fb4a1b895e97bb808b624ea0b31c43d121723f36 PR-BODY.md`
- `bash scripts/table_lines_diff_b2r3.sh <clone> d76763733e088cd21bbdd587927c8cf2f26cc8b3 fb4a1b895e97bb808b624ea0b31c43d121723f36 receipts/pr-body-round2-live.md PR-BODY.md <scratch>`
- `SCAN_STAGE=<empty scratch> EXTRA_PRIVATE=<names> python3 -B scripts/token_scan_run_b2r3.py <clone> <round-1 author dir> <MANIFEST.json> 4fb092069a6bf9b1ecad3cc94f7cd03a400e6a01 <R404-2 scripts> <R405-2 scripts> <this directory>`
- Verify the packet: `sha256sum -c MANIFEST.sha256`.

No script here prints an identifier or a private name: the scan receipt shows masked classes, hash prefixes and counts only.
