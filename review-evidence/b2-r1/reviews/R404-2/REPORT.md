[R404] NEGATIVE - exact head d76763733e088cd21bbdd587927c8cf2f26cc8b3

# R404-2: internal independent delta review of PR #622 (issue #606, with #608 and #75)

- Round: R404-2, internal independent reviewer, cleared context, under the round-2 assignment on #606 ([5886531640](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5886531640)).
- Exact head: `d76763733e088cd21bbdd587927c8cf2f26cc8b3`, tree `2e2dcd08dd16575aee614c8ff694a2c6c964b95c`.
- Delta judged: `c37f1d04..d7676373`, one docs commit by [A444]. Whole PR: `13eda870..d7676373`.
- Changed at this head, all mode 100644, no gitlink (`receipts/clone_integrity_r2.txt`):
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md` (blob `dc12b5f2`);
  - `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md` (blob `b0b60726`);
  - `docs/findings/README.md` (blob `01b2ecb1`).
- Evidence judged:
  - the redacted archive `b2-review-evidence` at `666d8897` (author packet and the R404-1 packet), and its current head `dab86d7b` (adds R405-1 and the round-2 author packet `author-r2/`);
  - `MANIFEST.json` at `dab86d7b` verifies all 1,951 entries, 456 of them redacted copies (`receipts/token_scan_r2_r405dir.txt`);
  - the `author/` and `reviews/R404-1/` trees are unchanged from `666d8897` to `dab86d7b`.

Authorities, read in this order:
1. AGENTS.md, CONTRIBUTING.md (sections 3 and 6, and the docs gates) and docs/README.md.
2. Issue #606: body, the lane B2 assignment (5885087413), the round-2 assignment (5886531640), and the [A444] TAKEN and REVIEW READY comments.
3. Issue #608: the ruling (5885808887) and its correction (5886425487). Issue #75: body and acceptance criteria.
4. PR #622: body at this head, my R404-1 report (5886414299) and the F4 disposition (5886425159).
5. `docs/reference/REGISTER_MAP.md` (`0x924` `PP_STAT`, `0x93C` `PP_NVM_STAT`).
6. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11 and `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2.
7. Lane B1's page `599_394_E1_LINK_CYCLES.md` at `931c3edf`. It is byte-identical on live dev `79c36963` (`receipts/b1_page_identity.txt`).
8. Processor docs at pin `c951a9ff`: `10_srp_engine.md` section 6.5 (the leavealltimer deviation) and `08_timing.md` (T-MRP-LEAVEALL, Milan Table 4.3). Processor #108, PR #133 and #134 (read-only).

The other reviewer's round-1 report (R405-1) was read only after this round's verdict and ledger were drafted.

## Verdict summary

The round answers all four round-1 findings as ruled:
- the #608 reading is presented as decided under the corrected ruling;
- the cycle-22 attribution records the 0.401 s gap, the #108 deviation and the session count;
- both restore sections carry a correct saved-state table with its cause;
- the controller-host identity is gone from the archive.

Every saved-state value, the LeaveAll counts, the MSRP spacing wording and the byte identity of every measurement table re-derive independently. All Markdown gates pass in the pinned environment.

One new MINOR is open, so the verdict is NEGATIVE:
- **F5:** one sentence of the new saved-state derivation, repeated in the PR body, misstates its own evidence. It says both DUT stream inputs read connection count 0 "in all 340 polls". Stream Input 0 was polled twice, and 112 of the 340 records are byte copies.

No measured number, verdict or conclusion depends on that sentence.

## Assigned checks

1. **F1, the #608 reading: resolved.**
   - `608_75_WITHDRAWAL_AND_RESTART.md:17` grades #608 item 3 as "99 of 99 withdrawals that reached an IN registrar stopped; qualified" and links the correction.
   - `:27-35` say:
     - the reading is decided;
     - 99 of 99 IN-registrar withdrawals stopped within one PDU;
     - cycle 22 is attributed to the processor #108 deviation, "not accepted as standard behavior";
     - #608 item 3 is met without qualification only after the pin adoption of processor PR #133 and a 100-cycle re-run;
     - processor #134 still grades the LV-registrar stop.
   - `:37` keeps the literal 99-of-100 reading as history only.
   - The PR body's verdict row and its "The reading of #608 item 3 is decided" list say the same.
   - The #75 row now quotes #75's own proof line ("At least 100 physical disconnect/reconnect cycles resume the stream in under one second"). It reads "Met under the ruling", which matches the ruling's "No additional cycle is required". The correction leaves #75 unchanged.
   - Processor #108, PR #133 and #134 exist and are open, with titles that match the page (`receipts/ext_links_r2.txt`).
2. **F3, the cycle-22 attribution: resolved** (`:209-229`).
   - Gap: the bridge LeaveAll at -0.391721 s and the DUT's own at +0.009401 s give the recorded 0.401121 s.
   - Authorities: 802.1Q-2014 Table 10-5 (10.7.9) and clause 10.6 are cited. Milan v1.2 Table 4.3 is cited as "10-15 s, ± 0.5 s", matching `10_srp_engine.md` section 6.5 at `c951a9ff`, which the page links at the pinned blob. The 9.5 s inference follows from it.
   - Session count: `receipts/leaveall_r2.txt` gives 67 DUT LeaveAll PDUs less than 10 s after a received bridge LeaveAll, in 64 distinct captures of 112. The gaps are 0.199564 / 1.997469 / 4.807277 s (min / median / max), 14 of them under 1 s. All 67 are also under 9.5 s, so the threshold choice does not move the count.
   - "Only pairs inside one capture are seen, so these counts are lower bounds" is correct.
   - "Genuine LeaveAll cycle" is qualified at `:41-45`.
   - **A correction to my own round 1.** R404-1 F3 wrote "67 of 112 captures". My script counted PDUs, not captures (`leaveall_damping.py` appends one hit per PDU), and the corrected ruling inherited the wording. The page's "67 DUT LeaveAlls, in 64 of the 112 captures" is the accurate statement. It answers the author's open question 1.
3. **F2, the saved-state layer: resolved, apart from F5.** `receipts/saved_state_r2.txt` is an independent parse of all 226 archived console files and every controller transcript. It reproduces every value in both tables (`606…:247-253`, `608…:420-426`):
   - slots 229 / 230, image 230;
   - 53 records, 3,264 B, writer live;
   - commits 2 / 0;
   - `PP_STAT` `0x5b000c44` in all 226 samples: backed 1, img_valid 1, pend 1, dirty 0, stale 0, alarm 0, verdict 0 per `REGISTER_MAP.md` `0x924`;
   - `PP_NVM_STAT` `0xc34000e4`: tag C3, pend 1, unres 0, per `0x93C`.

   The start and end reads are identical in every field.

   The rest of the derivation also checks out:
   - Only the two `milan_nvm` reads carry the slot and commit fields. The 224 action samples run 06:53:46Z-07:20:32Z.
   - The 210 ACMP transactions are 105 of message type 6 and 105 of type 8, all to listener unique ID 8, all status 0.
   - The AECP commands are GET_ and READ_ only.

   The cause is correct against the design:
   - section 11 of the snapshot-ownership page gives `KL_acmp_nvm_shadow` as the only record writer (ids `0x20`-`0x2F`);
   - FASTCONNECT 4.2 indexes that block by sink;
   - so talker-side binds write no record.

   Lane B1's final column at `931c3edf` (and on live dev) equals B2's start column. That page attributes `nvm_pend` to the sticky SET_CLOCK_SOURCE level. "The persisted records were not read back or compared with the found state" is stated on both pages.

   The exception is `606…:265`, the poll-count sentence: see F5.
4. **F4, privacy: resolved** (`receipts/token_scan_r2.txt`, `receipts/token_scan_r2_r405dir.txt`, `receipts/stream_id_class.txt`).
   - Round 1's `token_scan.py` classes were re-run through `token_scan_r2.py` over:
     - the three pages at this head;
     - the complete `review-evidence/b2-r1` tree at branch head `dab86d7b`, all 1,951 files.
   - A private set of 10 controller-host identity patterns (the EUI-64 and its MAC in every spelling) was used. It was derived in scratch from the pre-redaction commit, never printed and not published.
     - The positive control on the pre-redaction tree hits (14 file-hits).
     - The pages and the whole archive head give 0 hits.
   - The fffe-form class now holds one identifier, under JSON field `gm`: the switch clock identity, found in 2 tracked files at head.
   - The vendor-prefix class holds three identifiers:
     - the peer entity ID (fields `listener`/`talker`/`stream_id`, 5 tracked files);
     - the DUT model ID (2 tracked files);
     - one stream ID found in no tracked file. It shares the peer entity-ID prefix and is declared only in the DUT's Listener MSRP events, so it is a reference-peer stream ID.
   - All four are in the maintainer's disposition 5886425159. The remaining generic hits are the scanners' own pattern text, bench-lane `/tmp` script names and one dotted clause number: no host, account, interface or serial identity.
   - The pre-redaction commits `2c9f3df2` and `51bfa948` are still served by SHA. That is recorded in the disposition as a GitHub-side request: see the pending duties.
5. **Index rows, the S2 wording, table identity and gates: pass.**
   - `README.md:11-13`:
     - both pages are indexed;
     - the #75 row no longer claims "three non-restarts tracked by #608; initial-bind exception tracked by #606";
     - the row points at the new pages and names its own image `9e9954e9`.
   - The S2 wording "1.000 s periodic spacing, 0.2 s after a LeaveAll" (`606…:19`, `:198`) and the new off-grid sentence (`:199`) re-derive in `receipts/msrp_spacing_r2.txt`:
     - spacing is 0.199998-1.000003 s;
     - every off-grid DUT PDU is a reply to the bridge LeaveAll, the DUT's own LeaveAll, or the join 0.2 s after it;
     - 0 are unexplained.
   - `receipts/tables_r2.txt` compares every table at `c37f1d04` and at this head:
     - #606 page: 8 of 8 measurement tables byte-identical;
     - #608 page: 9 of 9 byte-identical;
     - only the two verdict tables changed (1 and 2 rows, exactly the ruled rows);
     - the only additions are the two saved-state tables;
     - the PR body's per-bind table is byte-identical to the page's.
   - "2.742 s" (`608…:140`) is the truncated minimum 2.742934 s. That is a correct lower bound, where the old 2.743 overstated it.
   - Gates, pinned environment (cmarkgfm 2025.10.22, html5lib 1.1, installed with `--require-hashes` from `tools/markdown/requirements.txt`), all rc 0 (`receipts/gates/`):
     - `docs_check.py`: 0 findings, 176 md and 938 scrubbed files;
     - `check_doc_style.py`;
     - `gen_toc.py --check`;
     - `check_em_dash.py`: 0 findings over 902 lines from `13eda870` and over 113 lines from `c37f1d04`, arms 339/339;
     - `check_doc_paths.py`;
     - `ci_scope.py --selftest`;
     - `check_baremetal_only.py --check`;
     - `check_feature_status.py --self-test`;
     - `git diff --check`, from base and from round 1.
   - Links:
     - 53 of 53 relative links and fragments on the three pages resolve through the repository's own heading reader (`receipts/links_r2.txt`);
     - 13 of 13 external GitHub links resolve (`receipts/ext_links_r2.txt`).
   - The PR body says "Relates to #606 / #608 / #75", has no closing keyword and describes only these three files.

## Findings

### F5 MINOR: the saved-state derivation overstates its stream-input polls

- **ID:** F5 (numbering continues from R404-1).
- **Severity:** MINOR.
- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:265`: "The DUT's two stream inputs read connection count 0 in all 340 polls."
  - The PR #622 body, "Round 2", F2 bullet: "the DUT's stream inputs unbound in all 340 polls".
- **Authority/evidence:**
  - Round-2 ruling 3 (5886531640): "Derive them from the archived console captures. Give the cause … If the captures do not carry the values, say so."
  - AGENTS section 6, `Docs`: the page must give a cold reviewer accurate evidence.
  - `receipts/saved_state_r2.txt`: the 340 DUT GET_RX_STATE records are 338 of Stream Input 1 and 2 of Stream Input 0.
    - Stream Input 0 was read only in the two censuses, at 06:50:41Z and 07:20:45Z.
    - All 112 `snapshot.jsonl` files are byte-identical copies of the same action's `snapshot-after.jsonl`. So Stream Input 1 has 226 distinct polls, and the transcripts hold 228 distinct polls in all.
  - The author's own receipt (`author-r2/receipts/saved_state_b2.txt`) prints the same split (`'state-5-1': 338, 'state-5-0': 2`), and the sentence merges it.
- **Impact:**
  - A durable restore record claims about 338 observations of Stream Input 0 that do not exist, and counts duplicate files as observations. It is the one derivation the round was asked to get right.
  - The conclusion itself is unaffected. No record was written and no commit ran, and that rests on the command census (no command addressed a DUT stream input) and on the unchanged commits and slots. No table, number or verdict changes.
- **Required outcome:** On the page and in the PR body, state the polls as recorded, or drop the count and rest the sentence on the command census. As recorded: Stream Input 1 in 226 distinct polls (before and after every action and at both censuses), and Stream Input 0 at the two censuses only. Measurement tables stay byte-identical.
- **Verification:**
  - The sentence agrees with `receipts/saved_state_r2.txt`.
  - `scripts/tables_r2.py` still reports every measurement table identical.
  - The Markdown gates stay at rc 0.

### Suggestion (non-blocking)

- **S3 (Docs).** `606_FIRST_BIND_MEASUREMENT.md:255` cites "the round-2 packet's `saved_state_b2.py`", but nothing on the page says where that packet lives. It is `review-evidence/b2-r1/author-r2/` on `b2-review-evidence`. The round-1 packet is also only described, not located. Naming the archive path, or leaving it to the PR, is the author's choice. A cold reader can reach it through PR #622 today.

## Prior public findings on this PR

| Finding | State at `d7676373` |
|---|---|
| R404-1 F1 MINOR (Conformance, Docs) | **Resolved.** See check 1. |
| R404-1 F2 MINOR (Conformance, Docs) | **Resolved.** Table, cause, the not-compared statement and the B1 inheritance are all present and correct (check 3). A narrower defect in one derivation sentence is filed as F5, not retained as F2. |
| R404-1 F3 MINOR (Conformance, Docs) | **Resolved** (check 2). The page's 67 PDUs in 64 captures corrects R404-1's "67 of 112 captures". A maintainer disposition exists (the correction 5886425487). |
| R404-1 F4 MINOR (Conformance, Docs) | **Resolved** by the redacted archive and disposition 5886425159. The controller identity is absent from the whole archive head (check 4). |
| R404-1 S1, S2 | Taken (check 5). |
| R405-1 F1 MINOR (Conformance, Docs) | **Resolved.** Same as R404-1 F1; the LV simulation arm, processor #134, is named at `608…:34`. |
| R405-1 F2 MINOR (Conformance, Docs) | **Resolved**, as R404-1 F2. F5 applies. |
| R405-1 F3 MINOR (Conformance, Docs) | **Resolved.** Its 64 of 112 captures is on the page beside the 67 PDUs. |
| R405-1 F4 MINOR (Conformance, Docs) | **Resolved.** Its narrowed class, the controller entity ID, is empty at the archive head. |
| R405-1 S1, S2, S3 | Taken. S1 at `608…:140`. S2 in different words that say the same (`606…:19`, `:198-199`). S3 at `README.md:11-13`. |

## Per-lens results

- `[R404] PASS RTL - clone_integrity_r2.txt (git diff --raw 13eda870..d7676373 and c37f1d04..d7676373; four gitlinks) and protocol-processor docs/architecture/10_srp_engine.md section 6.5 at c951a9ff - only three .md files at mode 100644 changed, and every gitlink equals base. No RTL, tooling or interface is in scope. The processor leavealltimer behavior the page now attributes cycle 22 to is quoted accurately from the pinned design text; it is pre-existing processor behavior tracked by processor #108, not a change of this PR.`
- `[R404] PASS Robustness - receipts/leaveall_r2.txt, msrp_spacing_r2.txt, saved_state_r2.txt, archive_manifest_r2.txt, token_scan_r2_r405dir.txt - checked the new claims at their edges against the archive:`
  - the LeaveAll predicate, where the 10 s and 9.5 s thresholds give the same 67 and the page's lower-bound caveat is correct;
  - multi-hit captures (bind-4, unbind-2, unbind-3) explain 67 versus 64;
  - `PP_STAT` holds constant over all 226 samples, and both `milan_nvm` reads bracket every action and every ACMP command;
  - every off-grid MSRP PDU is classified;
  - the archive manifest has 0 mismatches over 1,951 entries.

  The duplicate-record miscount is filed under F5's lenses.
- `[R404] PASS Tests - receipts/mutate_r2.txt - this PR adds no executable test. The round's evidence chain was proved able to fail: 8 of 8 planted mutants were killed, and the unmutated control reproduces the receipt.` The mutants are:
  - a dirty bit in one console sample;
  - final commits 3/0;
  - a SET_CLOCK_SOURCE in one transcript;
  - a DUT input bound in one poll;
  - cycle 22's own LeaveAll moved +10 s;
  - an unexplained off-grid DUT PDU;
  - one per-cycle table cell;
  - one per-bind cell against the PR body.

  All ran on scratch copies.
- **Conformance: UNCLEAN (F5).**
  - Applied: the corrected ruling, the round-2 rulings 1-5, #75's criteria, `REGISTER_MAP.md` `0x924` and `0x93C`, snapshot-ownership section 11, FASTCONNECT 4.2, B1's page, and processor section 6.5.
  - Everything else conforms (checks 1-5).
- **Docs: UNCLEAN (F5).**
  - All three pages were read at this head.
  - Gates, links, index rows and table identity all pass.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F5) | Both pages and README at head; PR body; #606 5885087413 and 5886531640; #608 5885808887 and 5886425487; #75 criteria; `REGISTER_MAP.md` `0x924`/`0x93C`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §11; `SAVED_STATE_FASTCONNECT.md` §4.2; B1 page `931c3edf`; processor `10_srp_engine.md` §6.5 and `08_timing.md` at `c951a9ff`; `receipts/saved_state_r2.txt`, `leaveall_r2.txt` | R404-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| RTL | CLEAN | `receipts/clone_integrity_r2.txt` (diff --raw, modes, gitlinks); processor §6.5 at `c951a9ff` | R404-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| Robustness | CLEAN | `receipts/leaveall_r2.txt`, `msrp_spacing_r2.txt`, `saved_state_r2.txt`, `archive_manifest_r2.txt`, `token_scan_r2*.txt` | R404-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| Tests | CLEAN | `receipts/mutate_r2.txt` (8/8 killed, control reproduces), `tables_r2.txt` | R404-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| Docs | UNCLEAN (F5) | Three pages in full at head; PR body; `receipts/gates/*`, `links_r2.txt`, `ext_links_r2.txt`, `tables_r2.txt`, `token_scan_r2*.txt` | R404-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |

## Limits

- **Docs-only delta.** No bench access, and no raw capture was re-parsed; the raw captures stay outside the public archive.
  - The unchanged measurement tables rest on R404-1's re-derivation at `c37f1d04`, and are proven byte-identical here.
  - Round-2 values were re-derived from the archived console files, transcripts and `msrp.tsv`.
- **Physical calibration NOT RUN.** Printed precision is not calibrated accuracy.
- **Not re-run here:** the builder, parent, processor, gPTP and Yosys banks. The pinned Verilator was not needed and not used: no RTL is in scope.
- **Hosted checks.** At read time (10:35Z) the exact head had 0 check runs, 0 status contexts and 0 workflow runs (`receipts/hosted_checks_r2.txt`). No hosted verdict at this head exists to cite, and skipped contexts would not be proof in any case.
- **Clone untouched.** The clone was never modified:
  - HEAD, tree, index records (mode, blob, path), worktree bytes and the four gitlinks equal the exact head;
  - no assume-unchanged or skip-worktree flag is set;
  - status is clean (`receipts/clone_integrity_r2.txt`).
- **Scratch only.** Mutants ran on scratch copies and a scratch shared clone, both removed. The private identity patterns and the pre-redaction tree stay in scratch and are not published.

## Pending manager duties

- Publish this report.
- Route F5 to an author round. It is a one-sentence edit on the #606 page and in the PR body.
- Correct the count wording in the #608 correction record if wanted: "67 of 112 captures" should read 67 DUT LeaveAll PDUs in 64 captures. The error came from R404-1.
- Pursue the GitHub-side removal of the pre-redaction commits `2c9f3df2` and `51bfa948`, as the disposition records.
- Own hosted and act acceptance at the exact head; none was recorded at read time.
- Build and validate the final current-dev candidate at the merge turn (source base `13eda870`, live dev `79c36963`).
  - A trial three-way merge of `docs/findings/README.md` against live dev conflicts (`receipts/readme_merge_probe.txt`). Live dev inserted the `451_TDM8_FIRST_LIGHT.md` row next to the #75 row this PR edits.
  - Resolving it keeps both rows.
- Obtain the external review.
- Re-cover Conformance and Docs at the head that answers F5, and re-cover any CLEAN lens whose scope a later commit touches.

R404-2 FINISHED
