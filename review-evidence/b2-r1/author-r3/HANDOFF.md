# [A447] HANDOFF: PR #622 round 3 (bench lane B2, docs only)

Status: DONE. REVIEW READY posted on #606 as 5888931713 at head `fb4a1b895e97bb808b624ea0b31c43d121723f36`. Nothing pushed, the PR not edited, no bench touched, nothing written to the NAS.

- Role: author, round 3. Branch `b2-bench-0929`.
- Start head `d76763733e088cd21bbdd587927c8cf2f26cc8b3` (round 2). New head `fb4a1b895e97bb808b624ea0b31c43d121723f36`, tree `4519e9076b2602a8a413f1793e71d5f616122601`, one commit, local only.
- Commit subject (one line, no body, no trailers): "State the stream-input polls as recorded and locate the round-1 and round-2 evidence packets".
- Assignment: #606 comment 5888700643. It answers R404-2 (PR #622, 5888547222) and R405-2 (PR #622, 5888695807): F5 and R404-2 S3. Both reviews are NEGATIVE on the same F5 only.
- Public comments on #606:
  - TAKEN: [5888718376](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5888718376) (`TAKEN.md`).
  - REVIEW READY: [5888931713](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5888931713) (`REVIEW-READY.md`).
  - Both read back equal to their files apart from the trailing newline. No other comment was posted, edited or deleted.

## The change, file:line at `fb4a1b89`

`docs/findings/606_FIRST_BIND_MEASUREMENT.md`, section Saved-state layer:
- `:267-269` (F5), replacing "The DUT's two stream inputs read connection count 0 in all 340 polls.":
  - `:267` "The DUT's Stream Input 1 read connection count 0 in 226 distinct polls: before and after every action, and at both censuses."
  - `:268` "Its Stream Input 0 was polled at the two censuses only, and read connection count 0 both times."
  - `:269` "Each action's `snapshot.jsonl` is a byte copy of its `snapshot-after.jsonl`, so it is not counted as a poll."
- `:277-281` (F5), the "no record written" conclusion now rests on the command census and the unchanged commits and slots:
  - `:277` "No command in the lane addressed a DUT stream input: every state-changing command went to the reference peer, and every AECP command was a GET_ or READ_." (new)
  - `:279` "The commit count stayed 2 / 0 and the slots stayed 229 / 230." (unchanged text, now before the conclusion)
  - `:281` "So none of the lane's binds, unbinds or cycles wrote a record, and no commit ran." (unchanged text, now after both grounds)
  - The indexing lines `:271-275` (record writer, indexed by sink, no record holds a stream output's connections) are unchanged.
- `:257` (S3): "That packet is `review-evidence/b2-r1/author-r2/` on branch `b2-review-evidence`." It follows the sentence citing the round-2 packet's `saved_state_b2.py`.
- `:295` (S3), section Artifact hashes: "Its redacted copy is `review-evidence/b2-r1/author/` on branch `b2-review-evidence`; the round-2 packet is `author-r2/` beside it."

`docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:450` (S3): the same line as the #606 page's `:295`. That page's Artifact hashes section described the same round-1 packet without a location. This is one line beyond the page S3 cites; it is raised as open question 1 in REVIEW READY.

No other file changed, and the gitlinks equal the base (`receipts/head_identity.txt`). R405-2 S4 is not in the assignment and was not taken.

`PR-BODY.md` (proposed; the PR is not edited):
- The first line `[A440] ...` and the three "Relates to" lines are unchanged.
- The Round 2 F2 bullet now reads: "... 226 console samples, 210 ACMP commands all to the peer's input, and no AECP write. The DUT's Stream Input 1 read unbound in 226 distinct polls (before and after every action, and at both censuses), and its Stream Input 0 at the two censuses only. It also gives the cause: binding records are indexed by the DUT's stream inputs, and no command addressed one. With that command census and the commits (2 / 0) and slots (229 / 230) unchanged, no record was written and no commit ran. ..."
- A new "Round 3" section covers F5, S3 and the unchanged tables.
- No absolute path, no tool or model name, no attribution footer.

## F5: the stream-input polls as recorded

`scripts/poll_count_b2r3.py` -> `receipts/poll_count_b2r3.txt` (FAILURES 0, rc 0), over the round-1 author packet's 561 controller transcripts:

| Measure | Value |
|---|---|
| Action directories; `snapshot.jsonl` byte-identical to `snapshot-after.jsonl` | 112; 112 |
| DUT GET_RX_STATE records, every `*.jsonl` | 340 (input 1: 338; input 0: 2) |
| Of which in the `snapshot.jsonl` copies | 112, all input 1 |
| Distinct polls, copies left out | 228 |
| Stream Input 1 | 226: 112 `snapshot-before`, 112 `snapshot-after` (one each per action directory), 1 `census-start`, 1 `census-end` |
| Stream Input 0 | 2: 1 `census-start`, 1 `census-end`, none elsewhere |
| Other DUT stream inputs polled | none |
| Values | status 0 and connection count 0 in all 228 |
| Transcripts against the archive `MANIFEST.json` (`original_sha256`) | 561 of 561 equal; 449 archived as redacted copies |

The same split appears in R404-2's `receipts/saved_state_r2.txt` ("duplicates excluded: state-5-1 226, state-5-0 2, total 228") and in R405-2's `receipts/poll_count_r405.txt` ("distinct (input, timestamp) polls: 228"). The 112 action directories are 100 cycles, 5 binds, 4 unbinds, the restore unbind, the baseline and the final capture. These are the same actions whose 224 console samples the page counts.

## Measurement tables byte-identical

- `receipts/tables_r2_round3.txt`: R404-2's `tables_r2.py`, run unmodified (sha256 `8f02e573ba3674c0f9211bf17cb2e0a768015ad98a0765380374223264931877`), from `d7676373` to `fb4a1b89`, with `PR-BODY.md`. rc 0.
  - #606 page: 10 tables at old, 10 at new, all IDENTICAL. That covers the verdict, identity, binding, per-bind, unbind, comparison, saved-state, image, tool and capture tables. Table lines at old absent at new: 0.
  - #608 page: 11 tables at old, 11 at new, all IDENTICAL, including the 102-line per-cycle table and the 102-line capture-hash table. Table lines at old absent at new: 0.
  - PR body: the per-bind table is identical to the #606 page's. The verdict table has no page counterpart, as in round 2.
- `receipts/table_lines_diff_b2r3.txt` (`scripts/table_lines_diff_b2r3.sh`, rc 0), a literal `diff` of every line starting with `|`:

| Compared | Table lines old / new | sha256 (old = new) | `diff` |
|---|---|---|---|
| #606 page, `d7676373` / `fb4a1b89` | 86 / 86 | `138630b6689bf18d9f4df426ef26760e7b48a9d94f17b105c4c200d1b90bc450` | empty, rc 0 |
| #608 page, `d7676373` / `fb4a1b89` | 272 / 272 | `5f2f8eec875f2fff9e552909104bcb58dbec7933ee684f2b4b2d1ab07f6b5ce4` | empty, rc 0 |
| PR body, round-2 live / proposed | 17 / 17 | `a287bf7051aef9b459e59c005962ebf33d95b73e57cf750752a001e3e41e90d2` | empty, rc 0 |

`git diff -U0 d7676373 fb4a1b89` changes no line starting with `|` on either page (10 added and 2 removed on the #606 page, 2 added on the #608 page).

## Gates at `fb4a1b89`

`receipts/gates/gates.txt`. Every gate ran in the foreground, not piped, output redirected to one file per gate, from the physical `/data` worktree, with 0 uncommitted entries before and after:

| Gate | rc |
|---|---|
| `docs_check.py` (pinned env) | 0: 0 findings, 176 md + 938 scrubbed files |
| `check_doc_style.py` (pinned env) | 0 |
| `gen_toc.py --check` (pinned env) | 0 |
| `check_em_dash.py --base 13eda870` (pinned env) | 0: 0 findings over 912 added lines in 3 pages |
| `check_doc_paths.py` (pinned env) | 0: 854 cited paths resolve |
| `ci_scope.py --selftest` | 0 |
| `check_baremetal_only.py --check` | 0 |
| `check_feature_status.py --self-test` | 0: 46/46 |
| `git diff --check` (worktree; `13eda870..HEAD`; `d7676373..HEAD`) | 0, 0, 0 |

The commit adds no link, heading or anchor. The archive paths it names begin with `review-evidence/`, which is not a prefix `check_doc_paths.py` claims for the tree.

## Token scan

`scripts/token_scan_run_b2r3.py` -> `receipts/token_scan_b2r3.txt`. It runs R404-2's `token_scan.py` and R405-2's `r405_scan_tokens.py`, both unmodified, over every file of this directory except the receipt itself, and over both pages at `fb4a1b89`. Result: **CLEAN**, rc 0. It ran before REVIEW READY and again after this file's final edit.

- **Private deny-list.** Built in memory at run time and handed to each scanner through a pipe. It is never written to disk and never printed. It holds:
  - the controller-host identity, recovered by aligning three redacted archive transcripts with their originals, in every spelling (EUI-64 and derived MAC, plain, `:`, `-` and dotted);
  - this host's name, account name and home directory, and the absolute paths of the clone, the author packet and this directory, with their first two components;
  - every network interface name and hardware address, also as an EUI-64;
  - tool and model names, supplied on the command line.
- **Positive control.** The controller class hits 46 of the 58 unredacted round-1 `bind/` transcripts. The account and home patterns match their own sources.
- **Result.** 0 private-pattern hits in the packet and on the pages. The generic classes find only the DUT's locally administered entity ID and one MAAP multicast destination, on the #606 page, both unchanged since round 1.
- **A trial scan and two fixes.**
  - The trial deny-list also carried two public GitHub identities. One of them hit only the processor repository's owner in pre-existing processor URLs on both pages, lines round 3 does not touch, and it also appears across the tree at `13eda870`. Neither identity is private, so the final scan leaves both out.
  - The trial also flagged two literals in the scan script itself, an all-zero MAC and a method name matching the host-name shape. The script now avoids both.

## Packet

`README.md` lists every file. No toolchain, virtualenv, tree export or file over 200 KB is here. The archive `MANIFEST.json` (554,276 bytes) is recorded by sha256 and size only. `MANIFEST.sha256` covers every file.

## Open items for the manager

1. Push `fb4a1b89`, apply `PR-BODY.md` to PR #622, and archive this packet. The author may not do these in this round. Hosted checks and act at the new head follow the push.
2. Delta reviews by [R404] and [R405], per the assignment. Conformance and Docs are the lenses F5 left unclean. The commit touches both pages' prose only.
3. Carried from the round-2 reviews, unchanged here:
   - the "67 of 112 captures" wording in the #608 correction;
   - the GitHub-side removal of the pre-redaction commits;
   - the `docs/findings/README.md` conflict with live dev at the merge turn.
