# [A449] HANDOFF: PR #622 round 4 (bench lane B2, docs only)

Status: DONE. REVIEW READY posted on #606 as 5889299853 at head `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`. Nothing pushed, the PR not edited, no bench touched, nothing written to the NAS.

- Role: author, round 4. Branch `b2-bench-0929`.
- Start head `fb4a1b895e97bb808b624ea0b31c43d121723f36` (round 3). New head `5c57927413e0dae279f06a75d2a58e3fec8a2bb0`, tree `5613d2b3b7b0f0b8b8d710216647631401bf1265`, one commit, local only.
- Commit subject (one line, no body, no trailers): "State that no state-changing command addressed a DUT stream input and name the reads that did".
- Assignment: #606 comment 5889146437. It answers F6 of R404-3 (PR #622, 5889116666) and R405-3 (PR #622, 5889142925). Both reviews are NEGATIVE on the same F6 only.
- Public comments on #606:
  - TAKEN: [5889170170](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5889170170) (`TAKEN.md`).
  - REVIEW READY: [5889299853](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5889299853) (`REVIEW-READY.md`).
  - Both read back equal to their files apart from the trailing newline. No other comment was posted, edited or deleted.

## The change, file:line at `5c579274`

`docs/findings/606_FIRST_BIND_MEASUREMENT.md`, section Saved-state layer. One line replaced by two one-sentence paragraphs (`git diff --numstat`: 3 added, 1 removed):

- Removed (was `:277`): "No command in the lane addressed a DUT stream input: every state-changing command went to the reference peer, and every AECP command was a GET_ or READ_."
- `:277`: "No state-changing command addressed a DUT stream input: the 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer, and every AECP command was a GET_ or READ_."
- `:279`: "The commands that did address the DUT's stream inputs were reads, which write no record: 228 GET_RX_STATE (the polls above), 228 GET_COUNTERS and 4 READ_DESCRIPTOR."
- The two unchanged sentences after them move down by two lines: the commits and slots line is now `:281`, and the conclusion ("So none of the lane's binds, unbinds or cycles wrote a record, and no commit ran.") is now `:283`.

The assignment's four points map to the text as follows:

| Assignment point | Where |
|---|---|
| No *state-changing* command addressed a DUT stream input | `:277`, first clause |
| The 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer | `:277`, second clause |
| Every AECP command was a GET_ or READ_ | `:277`, third clause |
| The reads that did address the DUT's inputs (228 GET_RX_STATE, 228 GET_COUNTERS, 4 READ_DESCRIPTOR) are named as reads, which write no record | `:279` |

"The polls above" points at `:267-268`: 226 polls of Stream Input 1 plus 2 of Stream Input 0 are the 228 GET_RX_STATE.

No other file changed. The whole-PR scope is still the two findings pages and `docs/findings/README.md`, and the four gitlinks equal base (`receipts/head_identity.txt`).

## PR body

`PR-BODY.md` is the proposed PR #622 body; the PR itself is not edited. `receipts/pr-body-round3-live.md` is the live body as read at the start of this round, byte-equal to the file the manager placed here.

- The first line `[A440] ...` and the three "Relates to" lines are unchanged.
- Round 2 F2 bullet (`PR-BODY.md:78`), F6: "... and no command addressed one." now reads "... and no state-changing command addressed one. The 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer, and every AECP command was a GET_ or READ_. The commands that did address the DUT's stream inputs were reads, which write no record: 228 GET_RX_STATE (the polls above), 228 GET_COUNTERS and 4 READ_DESCRIPTOR." The rest of the bullet is unchanged.
- A "Round 4" section (`PR-BODY.md:91-93`): a heading and one line naming the assignment, F6 of both reviews, the change and the unchanged tables.
- No absolute path, no tool or model name, no attribution footer.

## Census re-derivation

`scripts/census_b2r4.py` -> `receipts/census_b2r4.txt` (FAILURES 0, rc 0), over the round-1 author packet as recorded (561 `*.jsonl`, each equal to the archive manifest's `original_sha256`):

| Measure | Value |
|---|---|
| Controller transcripts counted | 337: 112 `snapshot-before`, 112 `snapshot-after`, 100 `cycle`, 5 `bind`, 5 `unbind`, 1 `identity-aecp`, 2 census. The 112 `snapshot.jsonl` byte copies and the 112 `events.jsonl` (no commands) are left out |
| Commands | 3,165. Each ACMP wire record is paired with its command record and not counted twice |
| State-changing commands | 210: 105 `CONNECT_RX` and 105 `DISCONNECT_RX`, all to the peer's Stream Input 8, all status 0; every `CONNECT_RX` names DUT Stream Output 1 as talker |
| State-changing commands to the DUT | 0; to a DUT stream input: 0 |
| AECP commands, both entities | 2,356, all GET_ or READ_ |
| Commands addressed to a DUT stream input (descriptor type 5) | 460, all reads: 228 ACMP GET_RX_STATE (226 on input 1, 2 on input 0), 228 AECP GET_COUNTERS (226 and 2), 4 AECP READ_DESCRIPTOR (2 and 2) |

These equal R404-3's `receipts/poll_census_r3.txt` ("DUT-addressed commands naming a STREAM_INPUT (type 5): 460, of which state-changing: 0") and R405-3's `receipts/command_census_r405_3.txt` (DUT `counter` 908, `desc` 14 plus the 2 identity reads, peer `acmp` 210 to input 8).

## Table byte-identity proof

- `receipts/tables_r2_round4.txt`: the reviewers' `tables_r2.py`, run unmodified (sha256 `8f02e573ba3674c0f9211bf17cb2e0a768015ad98a0765380374223264931877`), from `fb4a1b89` to `5c579274`, with `PR-BODY.md`. rc 0.
  - #606 page: 10 tables at old, 10 at new, all IDENTICAL; table lines at old absent at new: 0.
  - #608 page: 11 tables at old, 11 at new, all IDENTICAL; table lines at old absent at new: 0.
  - PR body: the per-bind table is identical to the #606 page's; the verdict table has no page counterpart, as in rounds 2 and 3.
- `receipts/table_lines_diff_b2r4.txt` (`scripts/table_lines_diff_b2r4.sh`, rc 0), a literal `diff` of every line starting with `|`:

| Compared | Table lines old / new | sha256 (old = new) | `diff` |
|---|---|---|---|
| #606 page, `fb4a1b89` / `5c579274` | 86 / 86 | `138630b6689bf18d9f4df426ef26760e7b48a9d94f17b105c4c200d1b90bc450` | empty, rc 0 |
| #608 page, `fb4a1b89` / `5c579274` | 272 / 272 | `5f2f8eec875f2fff9e552909104bcb58dbec7933ee684f2b4b2d1ab07f6b5ce4` | empty, rc 0 |
| `docs/findings/README.md`, `fb4a1b89` / `5c579274` | 13 / 13 | `2c6df4f898de8154716bc4115373c5f882d783a52a5f09e1f13bfb2cdfe6bbdb` | empty, rc 0 |
| PR body, round-3 live / proposed | 17 / 17 | `a287bf7051aef9b459e59c005962ebf33d95b73e57cf750752a001e3e41e90d2` | empty, rc 0 |

The page and PR body hashes equal the round-3 packet's. `git diff -U0 fb4a1b89 5c579274` changes no line starting with `|`.

## Gates at `5c579274`

`scripts/run_gates_b2r4.sh` -> `receipts/gates/gates.txt`. Every gate ran in the foreground, not piped, with its output redirected to one file, from the physical path of the lane worktree. The pinned Markdown environment is Python 3.14.7 with `cmarkgfm==2025.10.22` and `html5lib==1.1`.

| Gate | rc |
|---|---|
| `docs_check.py` (pinned env) | 0: 0 findings, 176 md + 938 scrubbed files |
| `check_doc_style.py` (pinned env) | 0 |
| `gen_toc.py --check` (pinned env) | 0 |
| `check_em_dash.py --base 13eda870` (pinned env) | 0: 0 findings over 914 added lines in 3 pages |
| `check_em_dash.py --base fb4a1b89` (pinned env) | 0: 0 findings over 3 added lines |
| `check_doc_paths.py` (pinned env) | 0: 854 cited paths resolve |
| `ci_scope.py --selftest` | 0 |
| `check_baremetal_only.py --check` | 0 |
| `check_feature_status.py --self-test` | 0 |
| `git diff --check` (worktree; `13eda870..HEAD`; `fb4a1b89..HEAD`) | 0, 0, 0 |

The commit adds no link, heading or anchor. `gates.txt` shows one uncommitted entry before and after the gates. It is the ignored `scripts/__pycache__/`, whose files date from 09:29-09:30 local time. That is before this round started, so it was left as found.

## Token scan

`scripts/token_scan_run_b2r4.py` -> `receipts/token_scan_b2r4.txt`. It is the round-3 runner with only its header and receipt name changed. It runs the reviewers' `token_scan.py` (sha256 `7528b5b6…`) and R405-2's `r405_scan_tokens.py` (sha256 `3444b6c2…`), both unmodified. They scan every file of this directory except the receipt itself, and both pages at `5c579274`. Result: **CLEAN**, rc 0. It ran before REVIEW READY and again after this file's final edit.

- **Private deny-list, 61 patterns.** Built in memory at run time and handed to each scanner through a pipe; never written to disk and never printed. It holds three classes:
  - the controller-host identity, recovered by aligning three redacted archive transcripts (at `5d305ef6`) with their originals, in every spelling (7 patterns);
  - this host's name, account name and home directory, the absolute paths of the clone, the author packet and this directory with their first two components, and every network interface name and hardware address, also as an EUI-64 (39 patterns);
  - tool and model names, supplied on the command line (15 patterns).
- **Positive control.** The controller class hits 46 of the 58 unredacted round-1 `bind/` transcripts. The account and home patterns match their own sources.
- **Result.** 0 private-pattern hits in the packet (28 files, every file but the receipt) and on the pages. The reviewers' `token_scan.py` reports no hit in any class on the pages, and none in the packet. R405-2's generic classes find only the DUT's locally administered entity ID and one MAAP multicast destination, both on the #606 page, both unchanged since round 1 and outside this commit.

## Not taken

The assignment says "Nothing else changes", so these optional suggestions are recorded, not taken:
- R404-3 S4 and R405-3 S1 (Docs): name the round-3 poll-count script as the derivation at `606…:255`.
- R405-3 S2 (Docs), carried from R405-2 S4: `608…:32` and `:229` describe processor PR #133 as landed while it is open.

## Open items for the manager

1. Push `5c579274`, apply `PR-BODY.md` to PR #622, and archive this packet. The author may not do these in this round. Hosted checks and act at the new head follow the push.
2. Delta reviews by [R404] and [R405], per the assignment. F6 left Conformance and Docs unclean. The commit touches one prose paragraph on the #606 page, no table, script or evidence file.
3. Carried from earlier rounds, unchanged here:
   - the "67 of 112 captures" wording in the #608 correction;
   - the GitHub-side removal of the pre-redaction commits;
   - the `docs/findings/README.md` conflict with live dev at the merge turn.
