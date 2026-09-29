# [A444] HANDOFF: PR #622 round 2 (bench lane B2, docs only)

Status: DONE. REVIEW READY posted on #606 as 5886852822 at head `d76763733e088cd21bbdd587927c8cf2f26cc8b3`. Nothing pushed, the PR not edited, no bench touched, nothing written to the NAS.

- Role: author, round 2. Branch `b2-bench-0929`.
- Start head `c37f1d04e39be0344dfde77e793cdfa441bd4869` (round 1). New head `d76763733e088cd21bbdd587927c8cf2f26cc8b3`, tree `2e2dcd08dd16575aee614c8ff694a2c6c964b95c`, one commit, local only.
- Commit subject (one line, no body, no trailers): "Apply the corrected #608 ruling, attribute cycle 22 to processor #108, record the saved-state layer and index both pages".
- Assignment: #606 comment 5886531640. Inputs read: R404-1 (PR #622, 5886414299), R405-1 (PR #622, 5886527108), the corrected #608 ruling 5886425487, the original ruling 5885808887, the F4 disposition 5886425159 (on PR #622), PR #620's pages at `931c3edf`, processor `10_srp_engine.md` at `c951a9ff`, processor issue #108, PR #133 and issue #134 (all open), #75's "How we prove it".
- Public comments on #606: TAKEN [5886549830](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5886549830) (`TAKEN.md`) and REVIEW READY [5886852822](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5886852822) (`REVIEW-READY.md`). Both read back equal to their files apart from the trailing newline. No other comment was posted, edited or deleted.

## Timeline

- 10:28 CEST: TAKEN posted.
- Saved-state sources located: the two `milan_nvm` reads (identity gate, final restore) and `PP_STAT` in every console sample. `PP_NVM_STAT` (`0x93C`) is not read by the per-action samples, which read `PP_STAT`, `PP_DIAG`, `RST_EPOCH`, `CRFT_CTRL`, `CRFT_COUNT`, `LINKG_STAT` and `MAC_STATUS`.
- Scripts written and run; page edits; commit `d7676373`; gates at that head all rc 0; table identity proved; packet README, manifest and token scan; REVIEW READY.

## The change, file:line at `d7676373`

`docs/findings/608_75_WITHDRAWAL_AND_RESTART.md`:
- `:17`: #608 item 3 row, graded under the corrected ruling: "99 of 99 withdrawals that reached an IN registrar stopped; qualified". Cycle 22 is attributed to processor #108. Met without qualification only after the pin adoption of processor PR #133 and a re-run (F1).
- `:23`: #75 cycle-count row, now "at least 100 physical cycles resume within 1 s": "Met under the ruling: 100 cycles, 99 of 99 demonstrated restarts", citing 5885808887's "no additional cycle" (F1).
- `:27-45`: "The reading of #608 item 3 is decided" (F1, F3). It replaces "The two readings ... need a decision; this page does not choose":
  - the ruling and its correction;
  - #108, #133 and #134 with links;
  - the literal count kept as history, and the earlier decision 5860869482 cited as history;
  - "genuine LeaveAll cycle" qualified: cycle 22 is a LeaveAll cycle, but not a genuine one in that sense.
- `:54`, `:57`: Contents descriptions for Cycle 22 and Counters and restore (human-owned text; the TOC gate passes).
- `:140`: "at least 2.742 s" (was 2.743; R405-1 S1; the exact minimum is 2.742934 s, cycle 4).
- `:209-229`: Cycle 22, "Why the registrar was LV" (F3):
  - the 0.401121 s gap;
  - 802.1Q-2014 Table 10-5 (10.7.9) and clause 10.6;
  - Milan v1.2 Table 4.3 (10-15 s, ± 0.5 s);
  - the processor's section 6.5 "Timer on receipt: an open deviation" at `c951a9ff` and #108;
  - the counterfactual (IN registrar, Δ13 stop);
  - the session count: 67 DUT LeaveAlls in 64 of 112 captures, gaps 0.199564-4.807277 s, median 1.997469 s, 14 under 1 s, lower bounds;
  - #133 and #134.
- `:414-434`: restore bullet and "### Saved-state layer": the table, the cause in brief, "not compared", and a link to the #606 page's derivation (F2).

`docs/findings/606_FIRST_BIND_MEASUREMENT.md`:
- `:19`: "DUT MSRP kept 1.000 s periodic spacing, 0.2 s after a LeaveAll" (R404-1 S2, R405-1 S2).
- `:35`: Contents description for Restore.
- `:198-199`: the same spacing wording, plus "Each off-grid DUT PDU there was a reply to the bridge's LeaveAll, its own LeaveAll, or the PDU 0.2 s after it" (R405-1 S2's fact, `receipts/msrp_spacing_b2.txt`).
- `:239`, `:243-283`: restore bullet and "### Saved-state layer": the table, the derivation, the cause, B1 inheritance and "not compared" (F2).

`docs/findings/README.md:11-13`: #75 row corrected (image `9e9954e9`; the non-restarts and the initial bind now point at the two pages), plus index rows for both pages (R404-1 S1, R405-1 S3).

No other file changed; the gitlinks equal the base (`receipts/head_identity.txt`).

## F2: the saved-state layer and its derivation

| Saved-state field | Identity gate, 06:49:58Z | Final restore, 07:20:45Z |
|---|---|---|
| NVM slots A / B, image sequence | 229 / 230, image 230 | 229 / 230, image 230 |
| Records, writer | 53 records, 3,264 B, writer live | 53 records, 3,264 B, writer live |
| Commits ok / failed | 2 / 0 | 2 / 0 |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000c44`, 1 | `0x5b000c44`, 1 |
| `PP_NVM_STAT` | `0xc34000e4`, pend 1 | `0xc34000e4`, pend 1 |

Derivation, `scripts/saved_state_b2.py` -> `receipts/saved_state_b2.txt` (FAILURES 0, rc 0):
- **Sources.** `identity/console-identity.txt` and `restore/console-final.txt` in the round-1 author packet: their `milan_nvm` blocks and `PP_STAT`.
  - All other fields are identical between the two reads (slot verdicts `VD_OK`/`VD_OK`, authoritative B, refusals 0, last `VD_OK`).
  - `PP_NVM_STAT` decoded: tag `c3`, unres 0, pend 1, commit_busy 0, stale 0, dirty 0, img_valid 1, backed 1, dev_busy 0.
- **Bracket.** The two reads bracket every action: the 224 action console samples run 06:53:46Z-07:20:32Z, and all 210 ACMP commands fall 06:56:18Z-07:19:56Z.
- **Samples.** `PP_STAT` = `0x5b000c44` in all 226 console samples. Decoded per `REGISTER_MAP.md` `0x924`: alarm 0, backed 1, dirty 0, stale 0, img_valid 1, pend 1, verdict 0 (`VD_OK`).
- **Commands.** The only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`, all to the peer (listener uid 8) and all SUCCESS; every `CONNECT_RX` response names the DUT talker, uid 1. Every AECP command to either entity was GET_ or READ_.
- **DUT sinks.** The DUT's stream inputs were polled 340 times (input 1 338, input 0 2): connection count 0, no talker and no stream in every poll.
- **Cause.** The binding records `0x20`-`0x2F` are the only records with a writer (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11), and they are indexed by sink (`SAVED_STATE_FASTCONNECT.md` section 4.2). No record group holds a stream output's connections. So the lane's binds, unbinds and cycles of DUT Stream Output 1 wrote no record, and no commit ran: commits 2 / 0 and slots 229 / 230 at both ends.
- **Inheritance.** `nvm_pend` 1 is inherited: the B2 identity-gate read equals lane B1's final-restore column (PR #620 page at `931c3edf`) in all four of its rows. That page attributes it to the SET_CLOCK_SOURCE sticky level, which only a reset clears.
- **Coverage.** Between the two reads the captures carry `PP_STAT` only; `PP_NVM_STAT`, the slot sequences and the commit counts are read at the start and end alone. The pages say so.
- **Not compared.** The persisted records were not read back or compared with the found state. The pages say so.
- **Archive match.** Inputs match the archive `666d8897` (`receipts/archive_blob_match.txt`). All 787 files read match the archive MANIFEST's `original_sha256`. All 226 console files and 112 `msrp.tsv` are git-blob-equal to the archive tree. 449 controller transcripts are archived as redacted copies, and the fields read (command type, listener uid, status, DUT sink state) do not depend on the redaction.

## F3: cycle 22 and the session count

`scripts/leaveall_gap_b2.py` -> `receipts/leaveall_gap_b2.txt` (rc 0):

| Measure | Value |
|---|---|
| Cycle 22: bridge LeaveAll, DUT own LeaveAll, bridge `Lv` (s after the disconnect response) | -0.391721, +0.009401, +0.010791 |
| Own LeaveAll minus bridge LeaveAll | 0.401121 s |
| DUT LeaveAll MRPDUs less than 10 s after a received bridge LeaveAll | 67 |
| Captures holding at least one | 64 of 112 (bind-4, unbind-2 and unbind-3 hold two) |
| Gap min / median / max | 0.199564 / 1.997469 / 4.807277 s; 14 under 1 s |

R404-1's `leaveall_damping.py` counts PDUs (67) and R405-1's counts captures (64). Both reproduce on the round-1 packet. The corrected ruling's "67 of 112 captures" mixes the two; the page states "67 DUT LeaveAlls, in 64 of the 112 captures". Raised as open question 1 in REVIEW READY.

## Suggestions

- R404-1 S1 / R405-1 S3: index rows and the #75 row. Taken.
- R404-1 S2 / R405-1 S2: the MSRP spacing wording as ruled. R405-1's grid fact was added as one bullet, verified by `receipts/msrp_spacing_b2.txt`: 16 of 19 and 17 of 19 DUT MRPDUs on the 1.000 s grid, and every off-grid one in a LeaveAll round. Taken.
- R405-1 S1: 2.742 s. Taken.

## Byte-identical measurement tables

`scripts/tables_identity.py` -> `receipts/tables_identity.txt` (RESULT PASS, rc 0), and `receipts/table_lines_diff.txt`:
- #606 page: 8 of 8 measurement tables byte-identical, and the measurement-table diff is empty. Only at head: `### Saved-state layer / table 1`.
- #608 page: 9 of 9 byte-identical, including the 102-line per-cycle table and the 102-line capture-hash table, and the diff is empty. Only at head: `### Saved-state layer / table 1`.
- PR body: the per-bind table is byte-identical.
- `git diff -U0 c37f1d04 d7676373` removes exactly three table lines, all verdict rows: 606 `:19`, 608 `:17` and `:23`. It adds 17: three replacement verdict rows and two 7-line saved-state tables.
- Literal `diff` of all table lines with the verdict and saved-state tables set aside: rc 0 on both pages (72 and 254 lines).

## Gates at `d7676373`

`receipts/gates/gates.txt`. Every gate ran in the foreground, not piped, output redirected to a file, from the physical `/data` worktree:

| Gate | rc |
|---|---|
| `docs_check.py` (pinned env) | 0: 0 findings, 176 md + 938 scrubbed files |
| `check_doc_style.py` (pinned env) | 0 |
| `gen_toc.py --check` (pinned env) | 0 |
| `check_em_dash.py --base 13eda870` (pinned env) | 0: 902 added lines in 3 pages, 0 findings |
| `check_doc_paths.py` (pinned env) | 0 |
| `ci_scope.py --selftest` | 0 |
| `check_baremetal_only.py --check` | 0 |
| `check_feature_status.py --self-test` | 0 |
| `git diff --check` (worktree; 13eda870..HEAD; c37f1d04..HEAD) | 0, 0, 0 |

Also rc 0: `receipts/links.txt` (53 of 53 links and anchors in the three pages resolve with R405-1's `check_links.py`, and `gen_toc.py --verify-anchors` reproduces 249 cross-page fragments).

## Token scan

`receipts/token_scan.txt`: both reviewers' scanners, run unmodified from their round-1 packets at `d7676373`. They cover every file in this output directory except the receipt itself (the manifest included), and the three pages. Result: **clean**.

- **Private patterns.** 19, held outside the packet and never printed: the controller host's identity in every spelling, account and host names, the tap instrument, home and data paths, and tool and model names.
- **R404-1 `token_scan.py`.** Also applies the repository's `SCRUB_RULES` and its generic classes: IPv4, colon MAC, interface, home path, tty, e-mail, host name, tmp path, EUI-64 and vendor 16-hex. No hit in any class, in the packet or the two pages.
- **R405-1 `scan_tokens.py`.** Public ref `13eda870`. 0 hits in its `ipv4`, `abs-path`, `hostname`, `iface` and `serial` classes and in all 19 private classes.
  - Its only identifier hits are on the #606 page, unchanged since round 1: the DUT's locally administered entity ID (public at `13eda870`) and one MAAP multicast destination.
- **One fix before the final scan.** The first scan flagged sha256 and commit-SHA prefixes in `receipts/tables_identity.txt` as 16-hex and 12-hex identifier shapes. The receipt now prints full hashes and SHAs, and the final scan is clean. The scan receipt is excluded from its own scan because it holds the scanner's `sha256:` prefixes. `MANIFEST.sha256` is regenerated after the scan to add the receipt's hash.

## Packet

`README.md` lists every file. No toolchain, virtualenv, tree export or file over 200 KB is here. The archive `MANIFEST.json` (516,713 bytes) and the archive tree listing are recorded by sha256 and size only. `MANIFEST.sha256` covers every file.

## Open items for the manager

1. Confirm or correct the "67 of 112 captures" wording (see F3 above).
2. Push `d7676373`, apply `PR-BODY.md` to PR #622, and archive this packet. The author may not do these in this round. Hosted checks and act at the new head follow the push.
3. Delta reviews by [R404] and [R405], per the assignment.
