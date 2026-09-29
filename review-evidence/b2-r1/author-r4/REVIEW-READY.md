[A449] REVIEW READY
Commit: `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` on `b2-bench-0929`, one commit on the round-3 head `fb4a1b895e97bb808b624ea0b31c43d121723f36`, local and not pushed. Tree `5613d2b3b7b0f0b8b8d710216647631401bf1265`. Docs only, no bench access, under the [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5889146437), answering F6 of [R404-3](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5889116666) and [R405-3](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5889142925).

Changed: one Markdown page, mode 100644, no gitlink (`git diff --raw fb4a1b89..5c579274`), 3 lines added and 1 removed:
- `docs/findings/606_FIRST_BIND_MEASUREMENT.md`, Saved-state layer. The old `:277` ("No command in the lane addressed a DUT stream input: ...") is replaced by two sentences:
  - `:277` "No state-changing command addressed a DUT stream input: the 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer, and every AECP command was a GET_ or READ_."
  - `:279` "The commands that did address the DUT's stream inputs were reads, which write no record: 228 GET_RX_STATE (the polls above), 228 GET_COUNTERS and 4 READ_DESCRIPTOR."
  - The commits and slots line and the conclusion are unchanged and move to `:281` and `:283`.
- Proposed PR body (the PR is not edited). The Round 2 F2 bullet's "and no command addressed one" now says "no state-changing command addressed one", followed by the same two facts and the named reads. A one-line Round 4 section is added. The first line and the three "Relates to" lines are unchanged.

Validation, all at `5c579274`, foreground, not piped:
- **Census.** Every command in the 337 controller transcripts of the round-1 packet; the 112 `snapshot.jsonl` byte copies are left out, and all 561 `*.jsonl` equal the archive manifest's `original_sha256`. FAILURES 0:
  - 210 state-changing commands: 105 `CONNECT_RX` and 105 `DISCONNECT_RX`, all to the peer's Stream Input 8. None went to the DUT.
  - 2,356 AECP commands, all GET_ or READ_.
  - 460 commands to a DUT stream input, all reads: 228 GET_RX_STATE (226 on input 1, 2 on input 0), 228 GET_COUNTERS, 4 READ_DESCRIPTOR.
  - This matches R404-3's `poll_census_r3.txt` and R405-3's `command_census_r405_3.txt`.
- **Tables byte-identical.**
  - The reviewers' `tables_r2.py`, unmodified, `fb4a1b89` to `5c579274`: #606 page 10 of 10 IDENTICAL, #608 page 11 of 11 IDENTICAL, 0 table lines lost. The PR body's per-bind table is identical to the page's.
  - Literal `diff` of every table line: #606 86 = 86, #608 272 = 272, `docs/findings/README.md` 13 = 13, PR body (round-3 live against proposed) 17 = 17. All four diffs are empty, rc 0, with equal sha256, the same hashes as round 3. No changed line starts with `|`.
- **Gates, all rc 0.**
  - Pinned Markdown environment (`cmarkgfm==2025.10.22`, `html5lib==1.1`): `docs_check.py` (0 findings, 176 md + 938 scrubbed files), `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870` (0 findings over 914 added lines) and `--base fb4a1b89` (0 over 3), `check_doc_paths.py` (854 paths).
  - Also `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, and `git diff --check` (worktree, `13eda870..HEAD`, `fb4a1b89..HEAD`).
- **Token scan: clean.** The reviewers' `token_scan.py` and R405-2's `r405_scan_tokens.py` ran unmodified over the round-4 packet and both pages. They used a private deny-list of 61 patterns built in memory, never written or printed: the controller-host identity recovered from the archive's redaction, the local host, account, paths, interfaces and hardware addresses, and tool and model names.
  - The deny-list gives 0 hits in the packet and on the pages; its controller class hits 46 of 58 unredacted round-1 bind transcripts as a positive control.
  - The generic classes find only the DUT's own entity ID and one MAAP destination on the #606 page, both unchanged since round 1.

Acceptance (the assignment's F6 points), all met on the page (`:277`, `:279`) and in the proposed PR body:
- no state-changing command addressed a DUT stream input;
- the 210 `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer;
- every AECP command was a GET_ or READ_;
- the 228 GET_RX_STATE, 228 GET_COUNTERS and 4 READ_DESCRIPTOR are named as reads, which write no record.

Tables are byte-identical, the Markdown gates are rc 0 in the pinned environment, and no bench was used. Nothing else changed.

Open risks/questions:
1. Not taken, because the assignment says nothing else changes: R404-3 S4 / R405-3 S1 (name the round-3 poll-count script at `606…:255`) and R405-3 S2 (processor PR #133 described as landed on the #608 page).
2. For the manager: push `5c579274`, apply the proposed PR body, archive the round-4 packet, and start hosted checks and act at the new head. The author may do none of these in this round.
