[R405] NEGATIVE - exact head fb4a1b895e97bb808b624ea0b31c43d121723f36

# R405-3: external delta review of PR #622 (issue #606, with #608 and #75)

- Round R405-3, external independent reviewer, cleared context, under the round-3 assignment (606 comment 5888700643).
- Exact head `fb4a1b895e97bb808b624ea0b31c43d121723f36`, tree `4519e9076b2602a8a413f1793e71d5f616122601`.
- Delta judged: `d7676373..fb4a1b89`, one docs commit by [A447]. Whole PR: `13eda870..fb4a1b89`.

The round does what F5 asked for the polls. The per-input counts, their positions and the exclusion of the duplicate copies all re-derive exactly. The packets are named where they actually are. Every measurement table is byte-identical, and every Markdown gate passes in the pinned environment.

The verdict is NEGATIVE because of one new MINOR finding, **F6**. The replacement premise says "No command in the lane addressed a DUT stream input". The archive shows that 460 commands addressed one, all of them reads. The conclusion itself still holds. The fix is one sentence on the #606 page and one clause in the PR body.

## Authorities, in the order read

1. `AGENTS.md`, `CONTRIBUTING.md` (the documentation gates and the pinned Markdown lock, `tools/markdown/requirements.txt`), and `docs/README.md` at the head.
2. Issue #606: the body and the round-3 assignment (5888700643). The assignment takes the round-2 findings R404-2 F5 and R405-2 F5 as one item, plus R404-2 S3. It requires byte-identical tables, gates in the pinned environment, and no bench.
3. The interface authority for the conclusion: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11, row `0x20 to 0x2F`. `KL_acmp_nvm_shadow` is the only record writer, driven by the manager's per-sink dirty on binding, parameters and started state.
4. `git diff 13eda870..fb4a1b89` and the round-3 delta `d7676373..fb4a1b89` (`receipts/delta_d7676373_fb4a1b89.diff`, `receipts/delta_scope_r405_3.txt`).
5. Public evidence: `b2-review-evidence` at its live tip `9c992d5c`, of which I read only `author/`, `author-r2/` and `author-r3/`, plus `MANIFEST.json` at `4fb09206`. The live PR body at the head, and hosted state at the exact head.

The round-2 review findings (R404-2 and R405-2) were read only after the independent pass below was complete and F6 was written down. No review report for round 3 was read.

## Independent pass over the round-3 delta

**Scope.** The delta changes two files: `docs/findings/606_FIRST_BIND_MEASUREMENT.md` (blob `a6b23e26`) and `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md` (blob `c69870c5`).
- Both are mode 100644. The change is 12 lines added and 2 removed, and no removed or added line starts with `|`.
- The four gitlinks are unchanged (`efeb541a`, `5dce647a`, `c951a9ff`, `48ff7a7e`), and `git diff --check` is clean (`receipts/delta_scope_r405_3.txt`).
- Whole-PR scope is still those two pages plus `docs/findings/README.md`.
- The live PR body equals the archived `author-r3/PR-BODY.md`. Against my round-2 snapshot of the body, it changes only the Round 2 F2 bullet and adds a Round 3 section (`receipts/pr_body_diff_r2_r3.txt`).

### Check 1: the stream-input polls (`606…:267-269`, PR body `:78`)

I re-derived these from the 561 archived controller transcripts (`scripts/r405_3_polls.py`, `receipts/polls_located_r405_3.txt`). All 561 match `MANIFEST.json`'s `published_sha256` (`receipts/archive_integrity_r405_3.txt`). The redaction only touches the `controller` field, which none of these checks read.
- **Stream Input 1:** 226 distinct polls, all status 0 and connection count 0.
  - It was polled exactly once in `snapshot-before.jsonl` and once in `snapshot-after.jsonl` in each of the 112 action directories: 100 cycles, plus `bind/` baseline, bind-1..5, unbind-1..4, unbind-restore and final.
  - It was polled once at each census.
  - That is 112 × 2 + 2 = 226.
  - The page's "224 action console samples" (`:261`) counts the same 112 directories, so "every action" is used consistently on the page.
- **Stream Input 0:** polled only in `restore/census-start.jsonl` and `restore/census-end.jsonl`, reading 0 both times. It is polled nowhere else.
- **Duplicates:** in 112 of 112 action directories, `snapshot.jsonl` is byte-identical to `snapshot-after.jsonl`. Counting every file gives 340, which is 228 distinct polls plus 112 copies, as the PR body's Round 3 bullet says.
- **Against my round-2 receipts:** `scripts/r405_saved_state.py` and `scripts/r405_poll_count.py` rerun unmodified. Their output is byte-identical to my round-2 `saved_state_r405.txt` and `poll_count_r405.txt` (`receipts/saved_state_r405_3.txt`, `receipts/poll_count_r405_3.txt`). That includes the 338 + 2 raw and 226 + 2 de-duplicated split.

The poll statement is correct as recorded. The premise sentence that follows it is not; see F6.

### Check 2: the packets located (`606…:257`, `606…:295`, `608…:450`, PR body Round 3)

On the live branch `b2-review-evidence` (`9c992d5c`), `review-evidence/b2-r1/` holds `author/`, `author-r2/`, `author-r3/`, `reviews/` and `MANIFEST.json` (`receipts/packet_locations_r405_3.txt`).
- `author/` is tree `fdde402a`, unchanged since `666d8897`.
- `author-r2/` is tree `ba787bec`, unchanged since `dab86d7b`. It holds `scripts/saved_state_b2.py`, which is the script `:255` names.
- `author/` holds `RAW-ARTIFACTS.json` and `MANIFEST.sha256`, which is what `:297` and `608…:452` say "there" holds.

The `608…:450` line goes beyond the page R404-2 S3 cited. It locates the same packet that page's Artifact hashes section describes, and it is accurate. I judge it within item 2 of the assignment.

### Check 3: tables and gates

- **Tables.** `scripts/r405_tables.py`, unmodified from round 2, keys tables by header (`receipts/tables_identity_r405_3.txt`):
  - #606 page: 10 of 10 tables SAME;
  - #608 page: 11 of 11 SAME;
  - `docs/findings/README.md`: 1 of 1 SAME.
- A header-independent positional diff of every `|` line agrees:
  - #606: 86 = 86 lines;
  - #608: 272 = 272;
  - README: 13 = 13.
  - All three diffs are empty, with equal sha256.
- In the PR body, the 7-line per-bind table appears verbatim on the #606 page. The 10-line verdict table is PR-body-only and is identical to my round-2 snapshot.
- **Gates.** Pinned environment: a fresh venv installed with `--require-hashes` from `tools/markdown/requirements.txt`, giving `cmarkgfm==2025.10.22` and `html5lib==1.1` (`receipts/gates_r405_3.txt`). All rc 0:
  - `docs_check.py`: 0 findings, 176 md and 938 scrubbed files;
  - `check_doc_style.py`;
  - `gen_toc.py --check`;
  - `gen_toc.py --verify-anchors`: 249 links;
  - `check_em_dash.py --base 13eda870`: 912 added lines;
  - `check_em_dash.py --base d7676373`: 12 added lines;
  - `check_doc_paths.py`: 854 paths;
  - `git diff --check 13eda870..fb4a1b89`.

### Check 4: nothing else changed

- The diff touches only the lines listed in check 1 and check 2. The old `:265` sentence was replaced. The conclusion sentence moved two lines down unchanged, and the new premise `:277` was inserted before it.
- No table, number, verdict, link or other section changed.
- The round-1 findings' text (the #608 reading, the cycle-22 attribution, the saved-state tables and the redaction) is untouched.

### Fault probes on the poll claims

`scripts/r405_3_probes.sh` ran on disposable copies of `author/` under scratch (`receipts/probes_r405_3.txt`). The control passes both checkers. Each of the four mutants is reported by my `r405_3_polls.py`, and makes the author's round-3 `poll_count_b2r3.py` exit 1 on the matching check:
1. one before-poll removed;
2. one after-poll set to connection count 1;
3. a Stream Input 0 poll added in a cycle;
4. one `snapshot.jsonl` no longer a byte copy.

A note on reproducing the author's manifest check from the public copy: `poll_count_b2r3.py` with the archive manifest reports 112 of 561 transcripts equal to `original_sha256` (`receipts/author_poll_count_rerun_r405_3.txt`). That is expected, because the other 449 are redacted copies, and all 561 equal `published_sha256`. The author's receipt shows 561 because it ran on the unredacted originals.

## Findings

### F6 MINOR: the new command-census premise says no command addressed a DUT stream input, but 460 read commands did

- **ID:** F6 (numbering continues from round 2).
- **Severity:** MINOR.
- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:277`: "No command in the lane addressed a DUT stream input: every state-changing command went to the reference peer, and every AECP command was a GET_ or READ_."
  - The live PR #622 body, Round 2 F2 bullet (`:78`): "binding records are indexed by the DUT's stream inputs, and no command addressed one."
- **Authority/evidence:**
  - The round-3 assignment, item 1, asks that the "no record written" conclusion rest on the command census, so the census statement is the premise the round was asked to write.
  - IEEE 1722.1 ACMP `GET_RX_STATE_COMMAND` (message type 10) is addressed to a listener's stream input, which it names by `listener_entity_id` and `listener_unique_id`. The 226 + 2 polls that `:267-268` count are exactly such commands.
    - `author/tools/b2_controller.py:19` and `:32` send `a.acmp(10, Z, 0, <listener>, <unique id>)`.
    - The archived responses name listener `020000fffe000001` (the DUT) with `listener_uid` 1, or 0 at the censuses (`receipts/polls_located_r405_3.txt`).
  - The controller transcripts, with copies excluded, also carry AECP reads of the DUT's STREAM_INPUT descriptors, descriptor type 5 (`receipts/command_census_r405_3.txt`):
    - `GET_COUNTERS` on input 1, 226 times, and on input 0, twice;
    - `READ_DESCRIPTOR` on inputs 0 and 1, twice each.
  - In all, 460 commands addressed a DUT stream input: 228 ACMP GET_RX_STATE, 228 AECP GET_COUNTERS and 4 AECP READ_DESCRIPTOR. All were reads.
  - The derivation the page cites labels them the same way. `author-r2/receipts/saved_state_b2.txt:55` prints "DUT stream input polls (GET_RX_STATE)", and the round-3 receipt `author-r3/receipts/poll_count_b2r3.txt` heads them "DUT GET_RX_STATE records".
- **Impact:**
  - The page's premise contradicts the poll count two lines above it on the same page, and it misdescribes the command census it rests the conclusion on.
  - A cold reader checking the census against the transcripts finds 460 commands to the DUT's inputs where the page says none.
  - The conclusion is unaffected. By `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11, a binding record is written only on a sink's binding, parameters or started-state change. None of these reads makes such a change, the state-changing commands all went to the peer's Stream Input 8, and the commits (2 / 0) and slots (229 / 230) are unchanged.
  - No table, number or verdict changes.
- **Required outcome:**
  - On the page and in the PR body, the premise says what the census shows: no **state-changing** command addressed a DUT stream input. The commands that addressed one were reads (GET_RX_STATE, GET_COUNTERS, READ_DESCRIPTOR), which change no binding, parameter or started state.
  - Alternatively, drop the universal claim and keep the two facts already given: state-changing commands to the peer only, and AECP GET_/READ_ only.
  - The measurement tables stay byte-identical.
- **Verification:**
  - The sentence agrees with `receipts/command_census_r405_3.txt` and `receipts/polls_located_r405_3.txt`.
  - `scripts/r405_tables.py` and the positional diff still show every table unchanged.
  - The pinned Markdown gates stay at rc 0.

### Suggestions (optional, no lens effect)

- **S1 (Docs).** `606…:255` still names the round-2 `saved_state_b2.py` as the derivation. That script prints the raw 338 + 2, because it globs every `*.jsonl` (`author-r2/scripts/saved_state_b2.py:137`). `:269` explains the copies, so a reader can reconcile the two.
  - Naming the round-3 `author-r3/scripts/poll_count_b2r3.py`, which prints the 226 / 2 split and checks it, would let the cited derivation print the page's own number.
  - This is the one part of my round-2 F5 required outcome ("any derivation cited for it excludes the duplicate copies") that the round-3 assignment did not carry. I accept that narrowing, and I am not retaining it as a finding.
- **S2 (Docs, carried from R405-2 S4, not in this round's assignment).** `608…:32` and `:229` still say processor PR #133 "implements" / "adds" the leavealltimer restart. PR #133 is still open and unmerged, and processor #108 and #134 are open (`receipts/hosted_and_external_r405_3.txt`).

## Prior public findings on this PR

| Item | Disposition at `fb4a1b89` |
|---|---|
| R404-2 F5 MINOR (Conformance, Docs): polls overstated | **Resolved.** `:267-269` and the PR body state Stream Input 1 in 226 distinct polls before and after every action and at both censuses, and Stream Input 0 at the censuses only, with the copies excluded. All of it re-derives exactly (check 1). The new premise sentence's defect is filed as F6, not retained as F5. |
| R405-2 F5 MINOR (Docs, Tests, Robustness): duplicate copies counted | **Resolved.** The distinct per-input counts are stated, and the copies are named and excluded (`:269`). The author's round-3 checker detects each fault I seeded (probes). The cited-derivation residual is S1. |
| R404-2 S3 (Docs): packets not located | **Taken.** `:257`, `:295` and `608…:450` name `review-evidence/b2-r1/author/` and `author-r2/` on `b2-review-evidence`, and both exist there (check 2). |
| R405-2 S4 (Docs): PR #133 described as landed | **Not taken** (outside the round-3 assignment). Still applicable; optional, see S2. |
| R405-2 F4 residual: pre-redaction commits served by SHA | Still served: `2c9f3df2` and `51bfa948` resolve through the API. This is not a head finding; it is a GitHub-side removal the manager owns. |
| R404-1 F1-F4, R405-1 F1-F4 (all MINOR, Conformance, Docs) | Resolved at `d7676373` by both round-2 reviews. The round-3 delta touches none of their text (check 4), so they remain resolved. |

## Lens results

- `[R405] UNCLEAN Conformance — 606_FIRST_BIND_MEASUREMENT.md:277, PR body :78 — F6`: the command census, the premise the assignment asks the conclusion to rest on, misstates the ACMP GET_RX_STATE and AECP GET_COUNTERS/READ_DESCRIPTOR traffic to the DUT's stream inputs. Assignment items 1 (the poll statement) and 2 are otherwise met.
- `[R405] PASS RTL — git diff --raw 13eda870..fb4a1b89 (receipts/delta_scope_r405_3.txt); SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 11 row 0x20-0x2F at the head`:
  - no HDL, constraint, script or gitlink is in the PR (three `docs/findings/*.md`, mode 100644, four gitlinks unchanged);
  - the page's RTL-contract claim, that the binding records' only writer is `KL_acmp_nvm_shadow` through `KL_pp_nvm_port`, triggered by per-sink binding, parameter or started-state change, matches the authority.
- `[R405] PASS Robustness — receipts/polls_located_r405_3.txt, receipts/probes_r405_3.txt`: the boundary cases of the poll claim hold:
  - Stream Input 0 appears only at the censuses;
  - no non-zero connection count anywhere;
  - each of 112 directories has exactly one before-poll and one after-poll;
  - 112 of 112 copies are byte-identical.
  - Four seeded faults are each caught by both checkers.
- `[R405] PASS Tests — receipts/probes_r405_3.txt, receipts/tables_identity_r405_3.txt, receipts/gates_r405_3.txt`:
  - the author's round-3 `poll_count_b2r3.py` and my `r405_3_polls.py` each fail on the fault they claim to detect and pass on the control;
  - the table-identity checks (keyed and positional) and all pinned Markdown gates are rc 0 at the head.
- `[R405] UNCLEAN Docs — 606_FIRST_BIND_MEASUREMENT.md:277, PR body :78 — F6`: the rest of the delta (`:257`, `:267-269`, `:279-281`, `:295`, `608…:450`, and the PR body Round 3 section) is accurate against the archive and the branch.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F6 open) | `606…:255-285`; PR body `:78`, `:83-90`; round-3 assignment 5888700643; `author/` transcripts and `tools/b2_controller.py` | R405-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| RTL | CLEAN | `git diff --raw 13eda870..fb4a1b89`, gitlinks, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11 | R405-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| Robustness | CLEAN | `receipts/polls_located_r405_3.txt`, `receipts/probes_r405_3.txt`, `receipts/archive_integrity_r405_3.txt` | R405-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| Tests | CLEAN | `receipts/probes_r405_3.txt`, `receipts/tables_identity_r405_3.txt`, `receipts/gates_r405_3.txt`, `author-r3/scripts/poll_count_b2r3.py` | R405-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |
| Docs | UNCLEAN (F6 open) | both pages' delta lines, `docs/findings/README.md`, PR body, `b2-review-evidence` at `9c992d5c` | R405-3 | `fb4a1b895e97bb808b624ea0b31c43d121723f36` |

A fix for F6 touches Docs-scope and Conformance-scope text. Both lenses need re-covering at the fix head. RTL, Robustness and Tests stay banked at `fb4a1b89` only as long as the fix changes no table, no evidence script and nothing outside those two sentences.

## Real limits

- This was a delta review. I re-derived the round-3 claims, and checked identity for every table. I did not recompute the round-2-covered measurement values in those tables.
- I ran no builder, parent, processor, gPTP or Yosys bank, no Verilator (none is relevant to a docs-only delta), no act and no hardware.
- Physical calibration was NOT RUN, and nothing here is hardware proof.
- The archived transcripts are redacted copies. I verified them against `published_sha256`, not `original_sha256`. The `original_sha256` equality in the author's receipt is not reproducible from public state, and only 112 of the 561 files are unredacted.
- The IEEE 1722.1 reading in F6, that GET_RX_STATE is addressed to a listener stream input, is taken from the controller's own call and the archived response fields, not from a re-read of the standard's text.
- The clone was never modified. At the end, HEAD, index and tree are `4519e907`, the worktree is clean with nothing untracked or ignored, all tracked modes and blobs equal `HEAD`, and the four gitlinks are unchanged (`receipts/clone_integrity_r405_3.txt`).

## Pending manager duties

- **Hosted evidence.** At review time, the exact head has no check runs, no commit statuses and no workflow runs (`receipts/hosted_and_external_r405_3.txt`). Hosted and act acceptance at the final head belongs to the manager.
- **Candidate merge.** GitHub reports `mergeable_state=dirty`. A scratch `git merge-tree` of `fb4a1b89` into live dev `79c36963` (merge base `13eda870`) has a content conflict in `docs/findings/README.md` (`receipts/merge_probe_r405_3.txt`). The conflict must be resolved and validated in the merge-turn candidate. That file is not in the round-3 delta.
- **PR body.** F6's fix includes the PR body's Round 2 F2 bullet.
- **Pre-redaction commits.** `2c9f3df2` and `51bfa948` are still served by SHA and need GitHub-side removal.

R405-3 FINISHED
