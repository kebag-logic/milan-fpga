[R405] NEGATIVE - exact head d76763733e088cd21bbdd587927c8cf2f26cc8b3

# R405-2: external delta review of PR #622 (issue #606, with #608 and #75)

Round R405-2, external independent reviewer, cleared context. Exact head `d76763733e088cd21bbdd587927c8cf2f26cc8b3`, tree `2e2dcd08dd16575aee614c8ff694a2c6c964b95c`, one docs commit ([A444]) on the round-1 head `c37f1d04e39be0344dfde77e793cdfa441bd4869`, source base `13eda870d1a6cf3f946fc228a98862366b08d102`. The PR relates to #606, #608 and #75 and closes none (`closingIssuesReferences` is empty).

All four round-1 findings are resolved at this head, and all three round-1 suggestions are taken. One new MINOR (F5) is in the round-2 saved-state derivation text: a poll count that includes a duplicated transcript file. It leaves Docs, Tests and Robustness unclean, so the verdict is NEGATIVE. The fix is one sentence on the #606 page and one in the PR body.

## Authorities, in the order read

1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md` at the head.
2. Issue #606 body, the B2 assignment (606 comment 5885087413) and the round-2 assignment (606 comment 5886531640). Issues #608 and #75 bodies.
3. The #608 ruling (5885808887), its correction (5886425487) and the earlier [A10] decision (5860869482). The F4 disposition (PR comment 5886425159).
4. Interface authorities: `docs/reference/REGISTER_MAP.md` (`PP_STAT` at `0x924`, `PP_NVM_STAT` at `0x93C`), `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11, `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2, and the processor at the pin `c951a9ff` (`10_srp_engine.md` section 6.5, `08_timing.md`, `05_acmp_engine.md` section 6bis).
5. `git diff 13eda870..d7676373` and the round-2 delta `c37f1d04..d7676373` (`receipts/delta_c37f1d04_d7676373.diff`).
6. Public evidence: `b2-review-evidence` at `dab86d7` (its parent chain holds the redacted `666d8897`). I read `author/` and `author-r2/` and `MANIFEST.json`. I did not read `reviews/R404-1`. PR #620's merged pages at live dev `79c36963`. Hosted checks at the exact head.

My own round-1 report (R405-1) was read only after the independent pass below was complete and F5 was written down.

## Independent pass over the round-2 delta

The delta changes three Markdown files, all mode 100644, and no gitlink (`receipts/clone_integrity_r405.txt`).

### F1: the #608 reading as decided

- The #608 page (`608_75_WITHDRAWAL_AND_RESTART.md:17`, `:27-45`) and the live PR body now present the reading as decided under the correction 5886425487:
  - 99 of 99 withdrawals that reached an IN registrar stopped within one PDU;
  - cycle 22 is attributed to the processor #108 deviation, "not accepted as standard behavior";
  - #608 item 3 is met without qualification only after the pin adoption of processor PR #133 and a 100-cycle re-run;
  - processor #134 owns the LV-registrar stop in simulation.
- The literal count (99 of 100) stays as history only (`:37`). The #75 cycle-count row (`:23`) cites the original ruling's "no additional cycle", which the correction did not withdraw.
- The external targets exist: processor #108 and #134 are open, PR #133 is open, PR #130 is merged (`97bd3786`). The issue-comment anchors match the fetched comment lists (`receipts/issue608_comments.json`, `receipts/issue606_comments.json`).

### F3: cycle 22's attribution

- The gap reproduces from the archived `cycles/cycle-022/msrp.tsv` and `acmp.tsv` (`receipts/leaveall_r405.txt`):
  - the bridge's LeaveAll at -0.391721 s after the tapped `DISCONNECT_RX` response;
  - the DUT's own LeaveAll at +0.009401 s;
  - a gap of 0.401121 s, and the bridge's `Lv` at +0.010791 s.
- The deviation is documented at the pin, `protocol-processor/docs/architecture/10_srp_engine.md:559-570` ("Timer on receipt: an open deviation", tracked as #108). The same lines carry the page's other citations: Table 10-5 (10.7.9), clause 10.6, and Milan v1.2 Table 4.3's "10-15 s, ± 0.5 s".
- The session count reproduces exactly under the page's stated rule (a DUT LeaveAll PDU less than 10 s after the last bridge LeaveAll in the same capture):
  - 67 PDUs, in 64 of the 112 captures;
  - gaps 0.199564-4.807277 s, median 1.997469 s, 14 under 1 s.
- The page states both numbers correctly. The correction's wording, "67 of 112 captures", counts PDUs as captures (see Pending manager duties).
- "Genuine LeaveAll cycle" is qualified (`:41-45`).

### F2: the saved-state layer

Re-derived from the 226 archived console captures, the tap ACMP tables and the controller transcripts (`scripts/r405_saved_state.py`, `receipts/saved_state_r405.txt`). All 226 console files, 112 `msrp.tsv` and 112 `acmp.tsv` are unredacted originals (`original_sha256` equals `published_sha256`), and all 1,889 extracted files match `MANIFEST.json` (`receipts/archive_integrity_r405.txt`).

| Field | Page | Re-derived |
|---|---|---|
| Start and end `milan_nvm` reads | 06:49:58Z, 07:20:45Z | 06:49:58.397Z (`identity/console-identity.txt`), 07:20:45.541Z (`restore/console-final.txt`) |
| Slots A / B, image, records | 229 / 230, image 230, 53 records, 3,264 B, writer live | same at both reads |
| Commits ok / failed | 2 / 0 | 2 / 0 at both reads |
| `PP_STAT` | `0x5b000c44` in all 226 samples | 226 of 226. By the register map: pend `[11]` 1, backed `[6]` 1, alarm `[4]`, dirty `[8]` and stale `[9]` 0 |
| `PP_NVM_STAT` | `0xc34000e4`, pend 1, at the two reads only | `[22]` pend 1. No action sample reads `0x9000093C` (the `0x930` word is `PP_DIAG`) |
| Action samples | 224, 06:53:46Z to 07:20:32Z | 224 files; first and last section 06:53:46.586Z and 07:20:32.155Z |
| State-changing commands | 105 `CONNECT_RX`, 105 `DISCONNECT_RX`, all to peer input 8 naming DUT output 1 | same, from the tap ACMP tables |
| AECP commands | GET_ or READ_ only | GET_AVB_INFO, GET_COUNTERS, GET_CLOCK_SOURCE, GET_CONFIGURATION, GET_SAMPLING_RATE, READ_DESCRIPTOR only |
| DUT stream-input polls | "two stream inputs ... all 340 polls" | **228 distinct polls**: input 1 in 226, input 0 in 2 (the censuses). All read 0. See F5 |

The cause holds against the authorities:

- Only records `0x20`-`0x2F` have a record writer (snapshot ownership, section 11).
- They are indexed by sink (FASTCONNECT section 4.2), and this lane bound only the DUT's Stream Output 1.
- PR #620's merged pages (`599_394_E1_LINK_CYCLES.md:293-296,321` at `79c36963`) end at the same slots, commits, `PP_STAT` and `PP_NVM_STAT`, and attribute the pending bit to SET_CLOCK_SOURCE writes.

Both pages say plainly that the persisted records were not read back or compared.

### S1-S3 and the tables

- **S1:** the inference bound's exact minimum is 2.742934 s (cycle 4), so "at least 2.742 s" is a true bound.
- **S2:** in the baseline and final captures every off-grid DUT MRPDU is a reply to the bridge's LeaveAll, the DUT's own LeaveAll, or the PDU one join period after it. The rest sit on a 1.000 s grid.
- **S3:** both pages are indexed in `docs/findings/README.md:12-13`. The #75 row (`:11`) now names image `9e9954e9` and points at the two new pages.
- **Measurement tables are byte-identical** (`scripts/r405_tables.py`, `receipts/tables_identity_r405.txt`):
  - #606 page: 8 of 9 tables identical; the 9th is the verdict table (the S2 row).
  - #608 page: 9 of 10 identical; the 10th is the verdict table (the #608 and #75 rows).
  - Each page adds one saved-state table.
  - The PR body's per-bind table is identical to the round-1 body.
  - The comparator detects a one-digit edit in a per-cycle row (`receipts/probes_r405.txt`, probe 1).

### F4 and the token scan

- I ran my own scanner (`scripts/r405_scan_tokens.py`, identifiers printed only as sha256 prefixes) with a private deny-list covering the controller host's EUI-64 and its derived MAC in every separator form. The deny-list was built from the pre-redaction public commit, held outside the packet and discarded after the scan.
- **Head pages and live PR body** (`receipts/token_scan_head_pages_r405.txt`): all four controller-host classes are empty. The only identifier-shaped tokens are the DUT's own locally administered entity ID (public at `13eda870`) and one DUT MAAP destination.
- **Archive tip `dab86d7`, whole `review-evidence/b2-r1`, 1,956 files with the pages** (`receipts/token_scan_r405.txt`):
  - The controller-host classes are empty.
  - The remaining vendor-OUI identifiers are the dispositioned public ones: the switch's gPTP clock identity, the peer's entity ID, MAC and stream ID.
  - The other 12-hex tokens all sit in hash or commit-prefix contexts inside scanner receipts and reports, 0 in any other context (`receipts/token_scan_fp_context_r405.txt`).
  - The `abs-path`, `iface` and `serial` hits are regex literals in the reviewers' own scanner sources and one prose word in the R405-1 report.

### Gates

In a disposable venv built from `tools/markdown/requirements.txt` with `--require-hashes` (cmarkgfm 2025.10.22, html5lib 1.1), every gate returned rc 0 at the head (`receipts/gates_r405.txt`):

- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base 13eda870` and `check_doc_paths.py`;
- `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `check_feature_status.py --self-test`;
- `git diff --check` over `13eda870..d7676373` and `c37f1d04..d7676373`.

All 53 relative links and anchors in the three pages resolve (`receipts/links_r405.txt`). All 13 external targets exist (`receipts/external_links_r405.txt`).

## Findings

### F5 MINOR: the saved-state derivation overcounts the DUT stream-input polls by a duplicated transcript

- **Lenses:** Docs, Tests, Robustness.
- **Where:**
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:265`: "The DUT's two stream inputs read connection count 0 in all 340 polls."
  - The live PR body, round-2 F2 bullet: "the DUT's stream inputs unbound in all 340 polls".
- **Authority/evidence:**
  - The round-2 ruling (606 comment 5886531640, item 3) requires the layer and its cause to be derived from the archived captures.
  - In all 112 action directories `snapshot.jsonl` is byte-identical to `snapshot-after.jsonl`, timestamps included. It is one poll stored twice (`receipts/poll_count_r405.txt`).
  - Counting every `*.jsonl` gives 340 (338 of input 1, 2 of input 0). Without the copies there are 228 distinct (input, timestamp) polls: input 1 in 226, input 0 in only 2, the start and end censuses.
  - The author's `author-r2/scripts/saved_state_b2.py` globs every `*.jsonl` (`A.rglob("*.jsonl")`, line 137), and its receipt shows the same 338 + 2.
- **Impact:**
  - A durable evidence page states a measurement count that the archive does not support, and implies that both inputs were polled throughout the session.
  - The zero-connection conclusion and the cause are unaffected.
  - The derivation the page names cannot tell a repeated file from a repeated read. A later count built the same way can silently inflate its evidence.
- **Required outcome:**
  - The page and the PR body state the distinct count, attributed per input: input 1 in 226 polls, input 0 at the two censuses, all 0. Alternatively, drop the count and keep the fact.
  - Any derivation cited for it excludes the duplicate copies.
  - The measurement tables stay byte-identical.
- **Verification:**
  - `scripts/r405_poll_count.py` over the archive gives 228 distinct polls, and the page and PR body agree with it.
  - `scripts/r405_tables.py` shows every measurement table unchanged.
  - The Markdown gates stay rc 0.

### Suggestion (non-blocking)

- **S4 (Docs).** `608_75_WITHDRAWAL_AND_RESTART.md:32` and `:229` say processor PR #133 "implements" / "adds" the leavealltimer restart. At review time #133 is open, in review.
  - Suggest saying so, so that a cold reader does not take the pending pin adoption for a merged fix.

## Prior public findings on this PR

| Item | Disposition at this head |
|---|---|
| R405-1 F1 MINOR (Conformance, Docs): decided reading shown as undecided | **Resolved.** The page and the PR body grade #608 item 3 and the #75 cycle count under 5885808887 and 5886425487, and name #134 as the LV-arm owner. |
| R405-1 F2 MINOR (Conformance, Docs): restore omits the saved-state layer | **Resolved.** Both restore sections carry the start and end table, with the cause and the "not compared" statement. The values equal my round-1 table and this round's re-derivation. The new poll-count error in the derivation text is F5, not a reopening of F2. |
| R405-1 F3 MINOR (Conformance, Docs; from R404-1): cycle-22 attribution | **Resolved.** The gap, the #108 deviation and the session count are recorded, and "genuine" is qualified. The correction 5886425487 is the maintainer disposition my F3 asked for. The page's 67 PDUs in 64 captures reconciles R404-1's 67 with my 64. |
| R405-1 F4 MINOR (Conformance, Docs; from R404-1, narrowed): controller host identity in the archive | **Resolved on the branch and archive tip.** The class is empty in the head pages, the live PR body and all of `b2-review-evidence` at `dab86d7`, per disposition 5886425159. The residual is below under Limits. |
| R405-1 S1, S2, S3 | Taken, and verified above. |
| R404-1 findings | Not read before this verdict. Its F1-F4 are the same four items per the round-2 assignment, and they are covered by the rows above. |

## Per-lens results

- **Conformance: CLEAN.**
  - The round-2 ruling's items 1-3 are met on both pages and in the PR body (F1, F3, F2 content).
  - The processor and 802.1Q claims match the pinned documents, including the Milan Table 4.3 range quoted at `10_srp_engine.md:565-566`.
  - Register decodes match `REGISTER_MAP.md`. The record-writer cause matches snapshot ownership section 11 and FASTCONNECT section 4.2.
- [R405] PASS RTL - `receipts/clone_integrity_r405.txt` (`git diff --raw 13eda870..d7676373`: three `.md`, 100644; four gitlinks equal to base); `protocol-processor` at `c951a9ff` `docs/architecture/10_srp_engine.md:423-571` (section 6.5, deviation at `:559-570`) and `08_timing.md:39-41` - No RTL, constraint, gitlink or tooling change. The rLA!/leavealltimer behaviour the page attributes to the pin is exactly what the pinned design documents as its open deviation #108.
- **Robustness: UNCLEAN (F5).**
  - Applied to the round-2 derivations: repeated input files (F5), the 10 s rule boundary (probe 3: moving one PDU past 10 s gives 66 PDUs in 63 captures), a one-sample `PP_STAT` change (probe 2: detected), and redacted-versus-original inputs (the consoles, `msrp.tsv` and `acmp.tsv` are originals).
- **Tests: UNCLEAN (F5).**
  - My re-derivations (`r405_saved_state.py`, `r405_leaveall.py`, `r405_tables.py`, `r405_poll_count.py`) each fail on a planted defect (`receipts/probes_r405.txt`, 3 of 3).
  - The page's own cited derivation counts a duplicated transcript (F5).
- **Docs: UNCLEAN (F5).**
  - The three pages were read in full at the head. All gates are rc 0, and links and anchors resolve.
  - The index rows and the #75 row are correct. S4 is a suggestion.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `608_75_WITHDRAWAL_AND_RESTART.md:13-47,209-229,414-434`; `606_FIRST_BIND_MEASUREMENT.md:13-25,239-283`; live PR body; 606 comments 5885087413 and 5886531640; 608 comments 5885808887, 5886425487 and 5860869482; `REGISTER_MAP.md` `0x924`/`0x93C`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11; `SAVED_STATE_FASTCONNECT.md` section 4.2; processor `10_srp_engine.md:559-570` and `08_timing.md:39-41` at `c951a9ff`; PR #620 pages at `79c36963` | R405-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| RTL | CLEAN | `git diff --raw` base..head and round-1..head; gitlinks; processor section 6.5 at `c951a9ff` (`receipts/clone_integrity_r405.txt`) | R405-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| Robustness | UNCLEAN (F5) | Archive `dab86d7` `author/**/{console*.txt,msrp.tsv,acmp.tsv,*.jsonl}`; `receipts/saved_state_r405.txt`, `leaveall_r405.txt`, `poll_count_r405.txt`, `probes_r405.txt`, `archive_integrity_r405.txt` | R405-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| Tests | UNCLEAN (F5) | `scripts/r405_*.py`; `author-r2/scripts/saved_state_b2.py` and its receipt; `receipts/probes_r405.txt`, `tables_identity_r405.txt` | R405-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |
| Docs | UNCLEAN (F5) | The three pages in full; live PR body; `receipts/gates_r405.txt`, `links_r405.txt`, `external_links_r405.txt`, `token_scan_head_pages_r405.txt`, `token_scan_r405.txt`, `token_scan_fp_context_r405.txt` | R405-2 | `d76763733e088cd21bbdd587927c8cf2f26cc8b3` |

## Limits

- **Hosted checks at this head:** none exist. Check-runs total 0, and the workflow-run list for `d7676373` is empty. The last runs on the branch are docs, elaborate, rtl-full and rtl-fast at `c37f1d04`, all successful (`receipts/hosted_checks_r405.txt`, read 10:44Z). This round records no hosted evidence at the exact head.
- **F4 residual:** the pre-redaction commits `2c9f3df2` and `51bfa948` are off every branch but still served by SHA. I fetched `2c9f3df2` by SHA to build the deny-list. Removal needs the GitHub-side request the disposition describes.
- **Raw captures not re-parsed.** They are outside the public packet. AVTP timing is consumed from `analysis.json` as in round 1, and the measurement tables are unchanged since round 1.
- **Standards consulted only through citations.** Milan v1.2 Table 4.3 and 802.1Q-2014 were checked through the pinned processor documents and in-repo citations, not the standards text.
- **Not run:** the full parent, processor, gPTP, Yosys and builder banks, as instructed. The manager's source banks at this head are theirs. The scoped Verilator was not used: no RTL is in scope. No hardware, bench, Docker, act or GitHub write. Physical calibration NOT RUN; field skips are not hardware proof.
- **Clone untouched.** At the end the worktree and index equal HEAD, the three page blobs and modes equal the tree, and the gitlinks and submodule checkouts sit at their pins with no local changes (`receipts/clone_integrity_r405.txt`). All probes ran on copies under the packet's scratch area.

## Pending manager duties

- Publish this report and its manifest.
- Route F5 to an author round: a one-line edit on the #606 page and in the PR body. S4 is optional.
- Hosted required contexts at the exact head: none exist yet. Start them, or record act and hosted acceptance at the head that merges.
- Confirm or correct the correction's "67 of 112 captures" wording (5886425487). The archive gives 67 PDUs in 64 captures, as the page says.
- The F4 residual: GitHub-side removal of `2c9f3df2` and `51bfa948`, and the PR #604 archive scrub named in 5886425159.
- Build and gate the final current-dev candidate at the merge turn (source base `13eda870`, live dev `79c36963`).

R405-2 FINISHED
