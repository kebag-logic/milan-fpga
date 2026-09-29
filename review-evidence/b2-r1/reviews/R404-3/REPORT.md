[R404] NEGATIVE - exact head fb4a1b895e97bb808b624ea0b31c43d121723f36

# R404-3: internal independent delta review of PR #622 (issue #606, with #608 and #75)

- Round: R404-3, internal independent reviewer, cleared context, under the round-3 assignment on #606 ([5888700643](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5888700643)).
- Exact head: `fb4a1b895e97bb808b624ea0b31c43d121723f36`, tree `4519e9076b2602a8a413f1793e71d5f616122601`.
- Delta judged: `d7676373..fb4a1b89`, one docs commit by [A447]. Whole PR: `13eda870..fb4a1b89`.
- Changed in the delta, both mode 100644, no gitlink (`receipts/clone_integrity_r3.txt`):
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md` (blob `dc12b5f2` to `a6b23e26`);
  - `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md` (blob `b0b60726` to `c69870c5`).
- PR body: the round-2 body (edit of 09:59:34Z) against the live body (edit of 11:04:14Z, read 11:07Z): `receipts/pr_body_diff_r2_to_r3.txt`.
- Evidence judged: the redacted archive `b2-review-evidence` at `9c992d5c`.
  - `author/` has the same tree id (`fdde402a`) at `666d8897`, `dab86d7b` and `9c992d5c`. `author-r2/` has the same tree id (`ba787bec`) at `dab86d7b` and `9c992d5c`.
  - `MANIFEST.json` at `9c992d5c` verifies every author entry, 0 mismatched (`receipts/archive_r3.txt`). Reviewer trees under `reviews/` were skipped and not read.
  - The round-3 author packet `author-r3/` was read as public author evidence.

Authorities, read in this order:
1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #606: the round-3 assignment (5888700643), the [A447] TAKEN (5888718376) and REVIEW READY (5888931713) comments.
3. PR #622: the live body, and my own R404-2 report (F5, S3) as the finding this round answers.
4. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11 and `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2 (unchanged; the page cites both).
5. IEEE 1722.1 AEM descriptor type 5 (STREAM_INPUT) and the ACMP GET_RX_STATE command, as labelled in the archived transcripts (`what` = `state-5-<n>`, `counter-5-<n>`, `desc-5-<n>`).

The other reviewer's round-2 report (R405-2) was read only after this round's verdict and ledger were written; see "Prior public findings".

## Verdict summary

The round does what the assignment asked on items (1) to (4), with one exception:

- The three new poll sentences are exact against the archive.
- Both packets are located, on both pages.
- Every table is byte-identical.
- All Markdown gates pass in the pinned environment.
- Nothing else changed.

The exception is the new sentence that carries the conclusion. It restates the command census as "No command in the lane addressed a DUT stream input". The census says the opposite:
- the lane sent 460 read commands to the DUT's stream inputs, 228 of them the very GET_RX_STATE polls counted two paragraphs earlier;
- what it did not send is a state-changing command to one.

The PR body repeats the claim. This is filed as F6, MINOR, under Conformance and Docs, so the verdict is NEGATIVE. The conclusion itself, no record written and no commit run, still holds. It rests correctly on the state-changing census and the unchanged commits and slots.

## Assigned checks

1. **Poll sentences and the conclusion: the polls pass, the census sentence does not (F6).**
   - Checked against `606…:267-269` and `receipts/poll_census_r3.txt`, which reproduces my `saved_state_r2.txt` byte for byte (`receipts/saved_state_r3_rerun.txt`):
     - `:267` "Stream Input 1 read connection count 0 in 226 distinct polls: before and after every action, and at both censuses." All 112 action directories hold exactly one Stream Input 1 poll in `snapshot-before.jsonl` and one in `snapshot-after.jsonl`, and each census file holds one: 224 + 2 = 226. All 226 read status 0 and connection count 0.
     - `:268` "Its Stream Input 0 was polled at the two censuses only, and read connection count 0 both times." Stream Input 0 appears only in `census-start.jsonl` and `census-end.jsonl`, once each, connection count 0.
     - `:269`: all 112 `snapshot.jsonl` files are byte copies of their `snapshot-after.jsonl`, and none is counted. 340 = 228 + 112.
   - The PR body's Round 2 F2 bullet states the same split, and its Round 3 bullet says "round 2's 340 was 228 polls plus 112 copies". Both are correct.
   - The conclusion now rests on `:277` (the command census), `:279` (commits 2 / 0, slots 229 / 230) and `:281` ("So none of the lane's binds, unbinds or cycles wrote a record, and no commit ran"). That is the order the assignment asked for.
   - `:277`'s first clause misstates the census; see F6.
   - The unchanged derivation lines are still exact against the archive (`receipts/saved_state_r3_rerun.txt`):
     - `:264`: 105 `CONNECT_RX` and 105 `DISCONNECT_RX`;
     - `:265`: all to the peer's Stream Input 8;
     - `:266`: AECP commands GET_ and READ_ only.
2. **Packet locations: pass.**
   - `606…:257` names `review-evidence/b2-r1/author-r2/` on branch `b2-review-evidence` for the `saved_state_b2.py` it cites. `saved_state_b2.py` is in `author-r2/scripts/`.
   - `606…:295` and `608…:450` name `review-evidence/b2-r1/author/`, with `author-r2/` beside it.
   - `RAW-ARTIFACTS.json`, which the next sentence says is "there", is at `author/RAW-ARTIFACTS.json`.
   - The `608` line goes one page beyond R404-2 S3. It sits in the same undescribed-location sentence of that page's Artifact hashes section, and the author disclosed it (REVIEW READY risk 1). It is correct and in the spirit of the suggestion. I do not count it as scope creep.
3. **Tables and gates: pass.**
   - `receipts/tables_r3.txt` runs my unmodified `tables_r2.py`:
     - `d7676373` to `fb4a1b89`: #606 page 10 of 10 tables IDENTICAL, #608 page 11 of 11 IDENTICAL, 0 table lines lost.
     - The live PR body's per-bind table is identical to the page's.
     - The PR body's 17 table lines are identical between the round-2 and live bodies.
     - No changed line in the commit starts with `|`.
   - From `c37f1d04` the report is unchanged from round 2: only the ruled verdict rows and the added saved-state tables differ.
   - Gates, pinned environment (cmarkgfm 2025.10.22, html5lib 1.1, installed with `--require-hashes` from `tools/markdown/requirements.txt`), all rc 0 (`receipts/gates/summary.txt`):
     - `docs_check.py`: 0 findings, 176 md and 938 scrubbed files;
     - `check_doc_style.py` and `gen_toc.py --check`;
     - `check_em_dash.py`: 0 findings over 912 lines from `13eda870` and over 12 lines from `d7676373`, arms 339/339;
     - `check_doc_paths.py`: 854 cited paths;
     - `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `check_feature_status.py --self-test`;
     - `git diff --check`, from base and from round 2.
   - 53 of 53 relative links and fragments on the three pages resolve (`receipts/links_r3.txt`). The delta adds no link.
4. **Nothing else changed: pass.**
   - `git diff --raw d7676373..fb4a1b89` lists only the two pages. Their hunks are exactly:
     - `606…:257`, `:267-269`, `:277`, `:281` and `:295`;
     - `608…:450`.
     - One sentence was removed: the old `:265` "340 polls" line. The conclusion sentence moved from before the commits line to after it.
   - The PR body changed only in its Round 2 F2 bullet and a new Round 3 section (`receipts/pr_body_diff_r2_to_r3.txt`). The live body equals the author's proposed `author-r3/PR-BODY.md`, and the author's `pr-body-round2-live.md` equals the 09:59Z edit (`receipts/pr_body_identity_r3.txt`).
   - The four gitlinks equal base, and README.md is untouched since round 2.
   - The added lines on both pages and in the PR body carry no identifier-class token: no 16-hex, EUI-48, fffe-form, host path, e-mail or interface name (`receipts/token_scan_r3.txt`).

## Findings

### F6 MINOR: the new census sentence says no command addressed a DUT stream input

- **ID:** F6 (numbering continues from R404-2).
- **Severity:** MINOR.
- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:277`: "No command in the lane addressed a DUT stream input: every state-changing command went to the reference peer, and every AECP command was a GET_ or READ_."
  - The PR #622 body, Round 2 F2 bullet: "binding records are indexed by the DUT's stream inputs, and no command addressed one."
- **Authority/evidence:**
  - The round-3 assignment (5888700643) item 1: "rest the 'no record written' conclusion on the command census". R404-2 F5's required outcome: state the evidence as recorded.
  - AGENTS section 6, `Docs`: the page must give a cold reviewer accurate evidence.
  - `receipts/poll_census_r3.txt`: distinct records addressed to the DUT that name a STREAM_INPUT descriptor (type 5) total 460:
    - 228 ACMP GET_RX_STATE, the polls the page counts at `:267-268`;
    - 228 AECP GET_COUNTERS;
    - 4 AECP READ_DESCRIPTOR.
    - Of these, 0 are state-changing.
  - The page's own `:267` records 226 polls of Stream Input 1 ten lines above the sentence that says nothing addressed it.
- **Impact:**
  - The one sentence the assignment asked to carry the conclusion states a census that did not happen, and it contradicts the poll count just above it.
  - A cold reader must guess that "command" means "state-changing command". That is the kind of loose evidence statement F5 was raised against.
  - The conclusion is unaffected. The true census is that no state-changing command addressed a DUT stream input, and read commands write no record. With the unchanged commits and slots, that supports `:281` exactly as before. No number, table or verdict changes.
- **Required outcome:** On the page and in the PR body, state the census as recorded: no *state-changing* command addressed a DUT stream input (the 210 `CONNECT_RX` and `DISCONNECT_RX` went to the peer, and every AECP command was a GET_ or READ_). The reads that did address the DUT's inputs may be named or left implicit. Tables stay byte-identical.
- **Verification:**
  - The sentence agrees with `receipts/poll_census_r3.txt` (0 state-changing of 460).
  - `scripts/tables_r2.py` still reports every table identical.
  - The Markdown gates stay at rc 0.

## Per-lens results

- `[R404] PASS RTL - receipts/clone_integrity_r3.txt (git diff --raw 13eda870..fb4a1b89 and d7676373..fb4a1b89; four gitlinks) - only two .md files at mode 100644 changed in the delta, and three .md files across the PR; every gitlink equals base (external efeb541a, gptp-processor 5dce647a, protocol-processor c951a9ff, third_party/verilog-axis 48ff7a7e). No RTL, tooling, constraint or interface is in scope, so there is no clock, reset, CDC, FSM or width to check.`
- `[R404] PASS Robustness - receipts/poll_census_r3.txt, saved_state_r3_rerun.txt, archive_r3.txt - checked the new poll claims at their edges: every one of 112 actions has exactly one before and one after Stream Input 1 poll (no action missing one, none with two); Stream Input 0 appears nowhere outside the two census files; all 112 snapshot.jsonl are byte copies (none partially differs); the identity transcript carries no DUT stream-input poll; 0 of 228 distinct polls read non-zero status or connection count; and the archive author trees are unchanged since 666d8897 / dab86d7b with 0 manifest mismatches.` The census miscount is filed under F6's lenses.
- `[R404] PASS Tests - receipts/mutate_r3.txt - this PR adds no executable test. This round's evidence chain was proved able to fail: 6 of 6 planted mutants were killed, and the unmutated control reproduces the receipt.` The mutants are:
  - one action's before-poll removed;
  - one `snapshot.jsonl` made distinct;
  - a Stream Input 0 poll inside an action;
  - one poll reading connection count 1;
  - a SET_ command to DUT Stream Input 1, which moves the state-changing count off 0;
  - one per-bind table cell, which `tables_r2.py` reports CHANGED and no longer identical to the PR body.

  All ran on scratch copies, since removed.
- **Conformance: UNCLEAN (F6).**
  - Applied: the round-3 assignment items 1 and 2, R404-2 F5's required outcome and S3, snapshot-ownership section 11 and FASTCONNECT 4.2 for the cause.
  - Items 1 (the polls), 2, 3 and 4 conform. F6 is the one departure.
- **Docs: UNCLEAN (F6).**
  - Both changed pages were read at head around every hunk, and the live PR body was read in full.
  - Gates, links, table identity and the token scan all pass.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F6) | `606…:243-299`, `608…:446-456` at head; live PR body; #606 5888700643, 5888718376, 5888931713; R404-2 F5/S3; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §11; `SAVED_STATE_FASTCONNECT.md` §4.2; `receipts/poll_census_r3.txt`, `saved_state_r3_rerun.txt` | R404-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| RTL | CLEAN | `receipts/clone_integrity_r3.txt` (diff --raw from base and from round 2, modes, four gitlinks) | R404-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| Robustness | CLEAN | `receipts/poll_census_r3.txt` (per-action poll shape, census files, duplicates), `saved_state_r3_rerun.txt`, `archive_r3.txt` | R404-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| Tests | CLEAN | `receipts/mutate_r3.txt` (6/6 killed, control reproduces), `tables_r3.txt` | R404-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| Docs | UNCLEAN (F6) | Both changed pages at head; live PR body and its round-2 predecessor; `receipts/gates/*`, `links_r3.txt`, `tables_r3.txt`, `pr_body_diff_r2_to_r3.txt`, `pr_body_identity_r3.txt`, `token_scan_r3.txt` | R404-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |

RTL, Robustness and Tests were also CLEAN in R404-2 at `d7676373`. The delta touches only Markdown text in no artifact within their scope, and this round re-applied all three at `fb4a1b89` in any case.

### Suggestion (non-blocking)

- **R404-3 S4 (Docs).** Name the derivation for the poll count. `606…:255` still names `author-r2/scripts/saved_state_b2.py` as the derivation of the saved-state list, and the list now includes the new poll bullets.
  - That script globs every `*.jsonl`, and its receipt (`author-r2/receipts/saved_state_b2.txt:55`) prints `'state-5-1': 338, 'state-5-0': 2`, not 226 and 2.
  - The count the page states is produced by `author-r3/scripts/poll_count_b2r3.py`, whose receipt passes every check and matches `receipts/poll_census_r3.txt`. The page does not name it.
  - `:269` states the copy rule, so a cold reader can reach 226 from 338 - 112. Naming the round-3 script, or saying that the round-2 receipt includes the copies, would close the trail.
  - This could ride with the F6 edit. It does not affect coverage.

## Prior public findings on this PR

Read after the verdict and ledger above were written.

| Finding | State at `fb4a1b89` |
|---|---|
| R404-1 F1-F4, R405-1 F1-F4 (all MINOR, Conformance and Docs) | **Resolved** at `d7676373` (R404-2 and R405-2 agree). This delta touches none of that text, apart from the saved-state derivation sentences covered below. |
| R404-1 S1, S2; R405-1 S1-S3 | Taken at `d7676373`; unchanged here. |
| R404-2 F5 MINOR (Conformance, Docs): "two stream inputs … all 340 polls" | **Resolved.** `606…:267-269` and the PR body's Round 2 F2 bullet state 226 distinct polls of Stream Input 1 (before and after every action and at both censuses), and 2 of Stream Input 0 (censuses only), with the copies excluded. That is exact against `receipts/poll_census_r3.txt`. The replacement conclusion sentence introduced a new, narrower defect, filed as F6, not retained as F5. |
| R404-2 S3 (Docs): locate the packets | **Taken** (check 2), on both pages. |
| R405-2 F5 MINOR (Docs, Tests, Robustness): the same 340-poll count | **Resolved** as for R404-2 F5. Its required outcome has two parts. The first, the distinct per-input count on the page and in the PR body, is met. The second, "any derivation cited for it excludes the duplicate copies", was not carried into the round-3 assignment, which asked only that the copies be left out of the count. The cited `saved_state_b2.py` still counts them, while the page states the copy rule at `:269`. I record this as S4 above, not as an open MINOR. R405 owns the disposition of its own clause. |
| R405-2 S4 (Docs): processor PR #133 described as implementing the restart while open | **Not taken, still applicable.** `608…:32` ("implements") and `:229` ("adds") are unchanged. The author declined it as outside the round-3 assignment (REVIEW READY risk 2). It is optional. |

## Limits

- **Docs-only delta.** No bench access, and no raw capture was re-parsed. The poll and command census comes from the archived controller transcripts, and the saved-state values from the archived console captures.
- **Physical calibration NOT RUN.** Printed precision is not calibrated accuracy, and field skips are not hardware proof.
- **Not run here:** the builder, parent, processor, gPTP and Yosys banks, and act. The pinned Verilator was not needed and not used: no RTL is in scope. The manager's source banks at this head are theirs.
- **Hosted checks.** At read time (11:11Z) the exact head had 0 check runs, 0 status contexts and 0 workflow runs (`receipts/hosted_checks_r3.txt`). There is no hosted verdict at this head to cite.
- **Clone untouched.** At the end (`receipts/clone_integrity_r3.txt`):
  - HEAD, tree, index records (mode, blob, path), worktree bytes and the four gitlinks equal the exact head;
  - no assume-unchanged or skip-worktree flag is set;
  - status, including ignored files, is empty.

  A `scripts/__pycache__/` left by the gate run was removed before that check.
- **Scratch only.** Mutants ran on scratch copies under the packet's scratch area, since removed. The evidence-branch clone and the gate venv stay in scratch and are not published.
- **Reviewer trees in the archive were not read before the verdict.** R405-2 was read from its public PR comment after the ledger was written.

## Pending manager duties

- Publish this report.
- Route F6 to an author round. It is a one-phrase edit on `606…:277` and in the PR body's Round 2 F2 bullet ("no state-changing command"). S4 and R405-2 S4 can ride with it.
- Re-cover Conformance and Docs at the head that answers F6. Re-cover any CLEAN lens whose scope a later commit touches.
- Own hosted and act acceptance at the exact head; none existed at read time.
- Build and validate the final current-dev candidate at the merge turn (source base `13eda870`, live dev `79c36963`).
  - The `docs/findings/README.md` trial-merge conflict against live dev recorded in R404-2 still applies: README.md is unchanged since round 2.
  - Resolving it keeps both rows.
- Carried from earlier rounds:
  - the "67 of 112 captures" wording in the #608 correction record;
  - the GitHub-side removal of the pre-redaction commits `2c9f3df2` and `51bfa948`;
  - the external review.

R404-3 FINISHED
