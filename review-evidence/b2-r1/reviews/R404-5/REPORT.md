[R404] POSITIVE - exact head 5c57927413e0dae279f06a75d2a58e3fec8a2bb0

Round R404-5 is a cleared-context internal confirmation round for PR #622 (bench lane B2, issue #606, with #608 and #75). It is taken at the same exact head as R404-4, and it judges only my round-4 finding F7, which a PR-body edit answers.

- Exact head: `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`, tree `5613d2b3b7b0f0b8b8d710216647631401bf1265`. The remote branch and `refs/pull/622/head` both point at it (`receipts/clone_integrity_r5.txt`).
- PR body: the manager's edit of 11:38:44Z, read at 11:41:16Z and re-read byte-identical at 11:43:48Z (`receipts/pr_body_at_read_r5.md`, `receipts/archive_and_body_reread_r5.txt`).
- Archive: branch `b2-review-evidence` at `32d9cc79`. Its `author/` tree is `fdde402a`, the same tree id as in round 4. Only `author/` was read, and the reviewer trees under `reviews/` were not opened.

## Verdict summary

- **F7 is resolved.** The Round 2 F2 bullet now opens its derivation with "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input". That is the census as recorded:
  - the archive holds 105 transactions of message type 6 and 105 of type 8, 210 in all, and every one of them names listener unique id 8;
  - the count agrees with the bullet's later sentence "The 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer";
  - it no longer contradicts the bullet's named reads (228 GET_RX_STATE, 228 GET_COUNTERS, 4 READ_DESCRIPTOR);
  - the figure it attributes to the #606 page is the page's own (`606…:264-265`: "The lane's only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`. All went to the reference peer's Stream Input 8").
- **The tables are unchanged.** The body's 17 table lines are identical to the round-4 body, in order. The per-bind table is still identical to the page's. All 21 page tables are IDENTICAL (`receipts/tables_r5.txt`).
- **The body has no closing reference.** `closingIssuesReferences` is empty, and no closing keyword precedes an issue number anywhere in the body. The body says "Relates to #606", "Relates to #608" and "Relates to #75", and "No issue closes here".
- **Nothing else changed.**
  - The head is unchanged. The tree, the four gitlinks and the page blob `19dadb8b` are the same as in round 4.
  - Round 4 to round 5, the body differs in two places only: the F2 bullet (one clause replaced), and one trailing empty line appended after the Validation section, which renders nothing.
  - The PR has no new commit, and its last body edit is 11:38:44Z (`receipts/pr_edit_history_r5.txt`).
- **No new finding.** An open MINOR or above is absent under every lens, so the verdict is POSITIVE.

## Authorities, in the order read

1. AGENTS.md sections 3 and 5 to 8. The verdict line, lens coverage per head, and the rule that a moved finding is not resolved.
2. CONTRIBUTING.md, through my round-4 report, which this round builds on (commits are one line with no trailers; the docs gates).
3. The round-4 assignment (issue 606 comment 5889146437): the PR body's Round 2 F2 bullet must "state the census as recorded".
4. My R404-4 F7 (PR comment 5889481776). Its required outcome is a PR-body edit stating the ACMP census as recorded. Its verification is `census_sentence_r4.py` rc 0 on the edited body, with the body's table lines unchanged.
5. `docs/findings/606_FIRST_BIND_MEASUREMENT.md:262-283` at the head, as the source the bullet cites.
6. The live PR body, its edit history and its metadata. Then the archived transcripts.
7. Prior public review findings, read only after the verdict below and the ledger were drafted.

## Checks

1. **`census_sentence_r4.py`, unmodified (sha256 `d30e255e…`): rc 0** (`receipts/census_sentence_r4_on_r5_body.txt`).
   - All ten page and body checks are OK. The archive recount is identical to round 4: 210 state-changing, all to uid 8; 809 ACMP in all, 232 to the DUT; 460 commands to DUT stream inputs, all reads.
   - **This rc 0 alone is not proof.** The script's F7 check runs only when the old wording "`<n>` ACMP commands all to the peer's input" is present. The edit removed that wording, so the check is skipped, not passed. That is a limit of my round-4 verification method, disclosed here. It is not a defect in the PR.
2. **`census_sentence_r5.py`, new: rc 0 on the live body, rc 1 on the round-4 body** (`receipts/census_sentence_r5.txt`). The script requires the reworded census to be present, and it checks it positively:
   - the opening phrase "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input" matches the archive. The counts are type 6 = 105 and type 8 = 105, the total is 210, the only listener uid is 8, and no other transaction type exists;
   - no unqualified "`<n>` ACMP commands" count remains in the bullet;
   - the opening count equals the later "The 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer";
   - the later sentences are intact: "no state-changing command addressed one", and the reads name GET_RX_STATE.
   - On the round-4 body, the control fails 3 of 4 checks, which reproduces F7.
3. **The check can fail: 9 of 9 mutants killed, control passes** (`receipts/mutate_r5.txt`, `scripts/mutate_r5.sh`, scratch copies only).
   - Body mutants:
     - B1: 105 `CONNECT_RX` changed to 104.
     - B2: 210 state-changing changed to 211.
     - B3: "state-changing" dropped.
     - B4: "the peer's input" changed to "the DUT's input".
     - B5: the later sentence's 210 changed to 200.
     - B6: "no state-changing command addressed one" deleted.
     - B7: an unqualified "214 ACMP commands" count re-added.
   - Archive mutants:
     - A1: one transaction's listener uid changed from 8 to 1.
     - A2: one extra type-6 transaction added.
   - The first draft of A1 hit a peer state record's ACMPDU rather than a transaction, and it survived. I retargeted it to the first transaction record, and it was killed. The receipt records this. It was a defect in the probe, not in the checker.
4. **Tables: pass** (`receipts/tables_r5.txt`, `tables_r2.py` unmodified, sha256 `8f02e573…`).
   - `fb4a1b89..5c579274`: the #606 page has 10 of 10 tables IDENTICAL, and the #608 page 11 of 11. 0 table lines were lost.
   - The body's per-bind table is identical to the #606 page's. The Verdicts table has no page counterpart, as in rounds 2 to 4.
   - The body's table lines: 17 in the round-4 body and 17 in the round-5 body, identical and in order.
5. **No closing reference: pass** (`receipts/pr_meta_r5.json`).
   - `closingIssuesReferences: []`.
   - A case-insensitive search of the body for close/fix/resolve keywords before `#N` finds nothing.
   - Lines 3 to 5 read "Relates to #606", "Relates to #608" and "Relates to #75".
6. **Nothing else changed at the head: pass** (`receipts/clone_integrity_r5.txt`).
   - `13eda870..HEAD` has the same 4 commits.
   - `git diff --raw` shows the same three docs entries, all 100644. The #606 page blob is `19dadb8b`, as in round 4.
   - The gitlinks are identical to `13eda870`: `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor c951a9ff`, `third_party/verilog-axis 48ff7a7e`.
   - Live dev is `79c36963`.

## Findings

None at this head.

### Suggestions (non-blocking, no lens effect)

- **R404-3 S4 / R405-3 S1 / R405-4 S1 (Docs).** Still applicable and still optional. `606…:255` names the round-2 derivation script, which does not print the page's `:277-279` counts.
- **R405-3 S2 / R405-4 S2 (Docs).** Untouched. R405 owns it.

## Prior public findings on this PR

Read after the independent pass above.

| Finding | State at `5c579274` with the 11:38:44Z body |
|---|---|
| R404-4 F7 MINOR (Conformance, Docs): "210 ACMP commands all to the peer's input" | **Resolved** (checks 1 to 3). Its first alternative outcome is met verbatim. |
| R405-4 F7 MINOR (Conformance, Docs): the same phrase, and its attribution to the page | **Resolved on the same evidence.** Its first alternative asks for "…all to the peer's Stream Input 8". The body says "the peer's input", and the next sentence of the bullet names the reference peer. The page's `:265` names Stream Input 8, and the page is the source the bullet cites. The attribution is now to text the page carries (`receipts/page_attribution_r5.txt`). R405 owns its final disposition. |
| R404-3 F6, R405-3 F6 MINOR | Resolved at `5c579274` (R404-4, R405-4). The census sentences they required are unchanged in this body and are re-checked OK in check 1. |
| R404-2 F5, R405-2 F5; R404-1 F1-F4, R405-1 F1-F4 MINOR | Resolved at earlier heads. No commit since, so they remain resolved. |
| R404-3 S4, R405-3 S1/S2, R405-4 S1/S2 | Not taken. Optional. |
| R405-2 F4 residual: pre-redaction commits `2c9f3df2`, `51bfa948` served by SHA | GitHub-side removal, owned by the manager. It is not a head finding. |

## Per-lens results

- `[R404] PASS Conformance - PR #622 body :78 (receipts/pr_body_at_read_r5.md), receipts/census_sentence_r5.txt, receipts/census_sentence_r4_on_r5_body.txt, 606_FIRST_BIND_MEASUREMENT.md:262-283 - the F2 bullet states the ACMP census as recorded (210 = 105 CONNECT_RX + 105 DISCONNECT_RX, all to listener uid 8), agrees with its own later census sentences, and cites figures the page carries; this meets the round-4 assignment and F7's required outcome; no closing reference (receipts/pr_meta_r5.json).`
- `[R404] PASS RTL - receipts/clone_integrity_r5.txt - same head, tree, git diff --raw 13eda870..HEAD (three docs files, 100644) and four gitlinks as round 4; no HDL, constraint, script or submodule is in the PR, and a PR-body edit cannot change one; the round-4 authority check (SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1285, SAVED_STATE_FASTCONNECT.md:275) stands at this unchanged tree.`
- `[R404] PASS Robustness - receipts/census_sentence_r5.txt, receipts/mutate_r5.txt - the reworded census was checked at its edges: the per-type split, not just the total; listener set exactly {8}; no transaction type other than 6 and 8; any unqualified ACMP count rejected; the round-4 body rejected; an off-by-one in either type count, a non-peer listener, or an extra transaction each detected.`
- `[R404] PASS Tests - receipts/mutate_r5.txt, receipts/census_sentence_r4_on_r5_body.txt - the PR adds no executable test; this round's evidence chain was shown able to fail: 9 of 9 mutants killed, control passes; the vacuous pass of the round-4 script on reworded text was identified and replaced by a positive check.`
- `[R404] PASS Docs - PR #622 body in full (receipts/pr_body_at_read_r5.md), receipts/tables_r5.txt, receipts/pr_edit_history_r5.txt - the body is accurate against the archive; the only other body change is one trailing empty line; 17 body table lines and 21 page tables identical; the tree docs are unchanged since the round-4 gate run (rc 0) at this same tree.`

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PR body `:78` (11:38:44Z edit), `606…:262-283`, the round-4 assignment, `author/` tree `fdde402a`, `census_sentence_r4/r5` receipts, `pr_meta_r5.json` | R404-5 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| RTL | CLEAN | `clone_integrity_r5.txt`: diff --raw, the gitlinks, the tree; the round-4 authority rows, at the unchanged tree | R404-5 (also R404-4) | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Robustness | CLEAN | `census_sentence_r5.txt`, `mutate_r5.txt` A1/A2 | R404-5 (also R404-4) | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Tests | CLEAN | `mutate_r5.txt` (9/9 killed, C0 passes); round-4 `mutate_r4.txt` and gates at the same tree | R404-5 (also R404-4) | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |
| Docs | CLEAN | the full live PR body, `tables_r5.txt`, `pr_edit_history_r5.txt`; the page delta and gates from R404-4 at the same tree | R404-5 | `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` |

Any new commit, or any later PR-body edit to the F2 bullet or to a table, re-opens the lenses whose scope it touches.

## Real limits

- **Confirmation round only.** I judged F7 and whether anything else changed. I did not re-derive the round-2-covered measurement values inside the tables. Those rest on the earlier rounds and on table identity.
- **Gates not re-run.** The head and tree are byte-identical to round 4, where every docs gate returned rc 0 in the pinned environment. No bank was run: no builder, parent, processor, gPTP or Yosys bank, no act and no hardware. The pinned Verilator was not used, because no RTL is in scope.
- **No hardware proof.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Redacted archive.** The transcripts are the redacted copies. Message types, listener ids, command names and counts are not affected by the redaction. Message types 6 and 8 are CONNECT_RX_COMMAND and DISCONNECT_RX_COMMAND in the ACMP message-type table. That reading is the same as the page's and the earlier rounds', and I did not re-read the standard's text.
- **Hosted evidence.** At 11:43:16Z the exact head had no check runs, no commit statuses and no workflow runs (`receipts/hosted_checks_r5.txt`). No hosted evidence was judged.
- **The body can still be edited.** The body judged is the 11:38:44Z edit, byte-identical at both reads.
- **Clone untouched.** No tracked file in the review clone was modified, and all probes ran on scratch copies. At the end: HEAD `5c579274`, tree `5613d2b3`, 0 status lines including ignored files, index modes and blobs equal to `HEAD` for 966 entries, and the gitlinks unchanged.

## Pending manager duties

- **Hosted and act acceptance** at the final head. None exists at `5c579274`.
- **The candidate merge** against live dev `79c36963`, where a `docs/findings/README.md` conflict was reported in round 3. It must be built and validated at the merge turn. Source validation at `13eda870` is not that candidate.
- **The second independent positive review** (R405) and the full completion bar before any authorized merge.
- **The pre-redaction commits** `2c9f3df2` and `51bfa948` need GitHub-side removal.

R404-5 FINISHED
