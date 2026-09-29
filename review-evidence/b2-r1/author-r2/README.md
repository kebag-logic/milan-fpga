# [A444] PR #622 round 2 packet (bench lane B2, docs only)

Round 2 of PR #622 under the assignment on #606 (comment 5886531640). One commit, `d76763733e088cd21bbdd587927c8cf2f26cc8b3`, on the round-1 head `c37f1d04e39be0344dfde77e793cdfa441bd4869`. No bench access in this round. HANDOFF.md gives the change with file:line, the saved-state table and its derivation, the table-identity proof and the token scan.

Files:
- `HANDOFF.md`: state, changes, derivations and results.
- `TAKEN.md`, `REVIEW-READY.md`: the two public comments on #606, as posted.
- `PR-BODY.md`: the proposed PR #622 body for round 2 (the PR itself is not edited in this round).
- `scripts/saved_state_b2.py` -> `receipts/saved_state_b2.txt`: the saved-state layer at start and end, every console sample's `PP_STAT`, every state-changing controller command, every DUT stream-input poll, and each input file checked against the archive manifest.
- `scripts/leaveall_gap_b2.py` -> `receipts/leaveall_gap_b2.txt`: DUT LeaveAlls less than 10 s after a received bridge LeaveAll, counted per PDU and per capture, and cycle 22's gap.
- `scripts/msrp_spacing_b2.py` -> `receipts/msrp_spacing_b2.txt`: DUT MSRP spacing in the baseline and final captures.
- `scripts/tables_identity.py` -> `receipts/tables_identity.txt`, and `receipts/table_lines_diff.txt`: every measurement table byte-identical to round 1, on both pages and in the PR body.
- `scripts/archive_blob_match.py` -> `receipts/archive_blob_match.txt`: the 226 console files and 112 `msrp.tsv` read are git-blob-equal to archive commit `666d8897`.
- `receipts/gates/`: the assigned gates at the round-2 head, one file per gate, rc in `gates.txt`.
- `receipts/links.txt`, `receipts/head_identity.txt`, `receipts/token_scan.txt`.
- `MANIFEST.sha256`: every file above.

Inputs (read-only, not copied here):
- The round-1 author packet, the `author/` tree of `review-evidence/b2-r1` at archive commit `666d8897bc0659b7d2d29ef222437da5087d586e` on `b2-review-evidence`. The scripts take its directory as the first argument. Every file they read matches the archive's `original_sha256`; the 226 console files are byte-identical to the archived copies, and 449 controller transcripts are archived as redacted copies whose redaction does not touch the fields read.
- The archive's `review-evidence/b2-r1/MANIFEST.json`: 516,713 bytes, sha256 `45a986ea6e34f40c7ffb9d83fe710159628055b372b6373e97b5d9f218259b2e`, git blob `7b53a10ade024e74bc237767a1942cbc0fee91b9` (equal to the archive tree entry at `666d8897`). Not copied (over 200 KB).
- PR #620's `docs/findings/599_394_E1_LINK_CYCLES.md` at `931c3edfced972e01356cd989b5092a1672de5a3`, 25,179 bytes, sha256 `3ac7cea8796b94842decf499c1afb7317908e8632026e94ecc72b4d3d0f6f28e`, for lane B1's final saved-state column.

Reproduce, from this directory: `python3 -B scripts/saved_state_b2.py <author dir> <MANIFEST.json> <B1 page>`, `python3 -B scripts/leaveall_gap_b2.py <author dir> <MANIFEST.json>`, `python3 -B scripts/msrp_spacing_b2.py <author dir>`, `python3 -B scripts/tables_identity.py <clone> c37f1d04e39be0344dfde77e793cdfa441bd4869 d76763733e088cd21bbdd587927c8cf2f26cc8b3 <round-1 PR body> PR-BODY.md`. Verify the packet: `sha256sum -c MANIFEST.sha256`.

No identifier other than the DUT's own is printed by any script here.
