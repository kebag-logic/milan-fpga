[R624] NEGATIVE - exact head e20fd2820a9c6b9effabc529a742e732263fafa8

Round R624-1, internal independent review of PR #725 for issue #629 (bench lanes B16, B16b and B16c, docs and findings only), in a cleared context with its own detached clone.

- Head `e20fd2820a9c6b9effabc529a742e732263fafa8`, tree `6299ec05fc1085b62defe945c9dc5c426e54d055`.
- Source base `c20c85bd`. The diff is `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+1021) and `docs/findings/README.md` (one row), in three one-line commits with no trailers.
- Read in order: AGENTS.md, CONTRIBUTING.md, docs/README.md; the #629 body; the B16 assignment (6117305187); the rulings 6117672835 and 6118365090; the author's TAKEN, STOP, STOP (B16b) and REVIEW READY (B16c) comments; `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Bench); `docs/reference/REGISTER_MAP.md` (`MCSRV_STAT`, `AAFM_STAT`, `SLIP_LB`, `SLIP_TDM`, `CRF_RATE`); the diff and its history; and the published packet `review-evidence/629-b16-r1` at `724b0974304beddc80fcf5512061c8a588a76cfd`.

**Verdict.** Two MINOR findings are open, both in Conformance and Docs, so the verdict is NEGATIVE. Neither finding changes a bench result:

- the tone reaches the DUT's TDM output sample-exact;
- B0 is graded at THD+N -123.95 / -122.80 dB median;
- B-CRF and B-AAF are graded at the path's floor, LOCKED, with 0 discontinuities;
- the clock-source sets and the full restore are read back.

Each of these was re-derived from the published receipts. The open defects are figures in B16b that do not match their receipts, and a misquoted pass criterion attached to the B-CRF "met" judgement.

## Findings

### F1 MINOR (Conformance, Docs): three B16b figures do not match their receipts

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2735`, `:2765-2766`, `:2625` and `:2650-2651`.
- **Authority:** the assignment's acceptance requires every figure in the findings section to match a receipt. The receipts are in packet `724b0974`, `review-evidence/629-b16-r1/author-r1/`.
  - (a) `:2735` gives the event-free-block THD+N at (c) as "-123.98 dB on both tones, `pts3` and `b0-2`". For `b0-2`, `summary/b0-2/c-b9-grade.stdout` `ch1_floor.thdn_db_median` is **-123.95** at 9,973 Hz. The page's own B0 table, at `:2762` and `:3068`, also says -123.95. Only `pts3` reads -123.98 on both tones.
  - (b) `:2766` gives the degraded runs as "0 to 18, 28 to 31, 43 to 54 and later runs". The receipt's `degraded_event_free_blocks` holds 43, 44 and 46 to 54. Block 45 is at the floor, so the third run is two runs.
  - (c) `:2625` says "McASP0 300 s from 06:38:03", and `:2650` says the B0 window "starts 24 s after the last bind".
    - 06:38:03.2 is when the capture command was launched (`runs/b0-2/events.jsonl` `captures-started`).
    - In this mode the board plays the loop for 2 s before it records: `tools/run_b16.py:277-281` has `sleep 2`, and `runs/b0-2/soc-record.log` shows the playback status lines before `arecord`.
    - The alignment confirms this. It covers 34.1 s of the 40 s tap, which started at 06:37:59.2, so the recording starts about 26 s after the 06:37:39.2 binds.
    - B16c applies the 2 s and states its windows as "from 26 s after the set" (`tools/run_b16c.py:687`, page `:2983-2984`).
- **Impact:** a cold reader checking B16b against the packet finds three figures that disagree with it. Two of the three also disagree with the page itself. The conclusions do not change: the B0 floor, the attribution, and "past lane B7's 20 s" all stand.
- **Required outcome:** each figure equals its receipt. Use -123.98 / -123.95 dB for `b0-2` (or name the tones per run), the runs 43 to 44 and 46 to 54, and the B0 recording's start as the capture start plus the 2 s playback lead, which is about 26 s after the binds.
- **Verification:** compare `:2735`, `:2766`, `:2625` and `:2650` with `summary/b0-2/c-b9-grade.stdout`, `runs/b0-2/events.jsonl` and `tools/run_b16.py:277-281` (`scripts/dump_figures.py` prints the first two).

### F2 MINOR (Conformance, Docs): B-CRF is judged "met" against a three-term restatement of lane B6's four-term criterion

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3112-3115`.
- **Authority:**
  - The design's bench row for B CRF reads "As B6" (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1671`).
  - Lane B6's pass rule (`629_MEDIA_CLOCK_FOLLOWING_BENCH.md:324-326`, repeated for B7 at `:811-813`) has four terms: the servo LOCKED, the counted ratio within 0.5 ppm of zero, **the timed ratio's interval holds zero**, and 0 listener discontinuities on the tone path.
  - The page restates "lane B6's terms" as three terms and concludes "All three are met here". The timed ratio was not measured in this mode (`:3114-3115`, and the limit at `:3227-3228`).
- **Impact:** the B-CRF judgement against the design row reads as fully met, but one of the row's four terms was not run. The substitution is disclosed only as a limit, not where the criterion is stated. The measurements themselves are strong: 0 net steps in 14,583,391 frames bounds the counted ratio below 0.07 ppm.
- **Required outcome:** the page states all four of B6's terms. It records the timed-ratio term as NOT RUN, and B-CRF as meeting the other three with the counted ratio standing in. Alternatively, it cites a recorded decision that the counted ratio replaces the timed ratio for this mode.
- **Verification:** read `:3112-3115` against `:324-326`.

### R1 RESIDUE (Docs): the PR #725 title calls B0 "following" and says it was at the floor

- **Where:** the PR #725 title.
- **Evidence:** the title says "Direction B graded at the path's floor for INTERNAL, CRF and AAF following". B0 (INTERNAL) is not a following case, and 131 of its 300 blocks are off the floor (`summary/b0-2/c-b9-grade.stdout`). The page itself is correct here.
- **Exact fix:** "Record bench lanes B16, B16b and B16c: Direction B's B0 graded, and B-CRF and B-AAF graded at the path's floor (#629)".

### R2 RESIDUE (Docs): B16c says the first counter mark is "at the window's start"

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2971-2972`, and the column header at `:3096`.
- **Evidence:** `window-mark-0` is taken 20 s after the DUT's set (`tools/run_b16c.py:680-682`), about 6 s before the window starts at 26 s (`:687`). The counters did not move between the marks, so no value changes.
- **Exact fix:**
  - `:2971-2972`: "Read GET_COUNTERS and GET_CLOCK_SOURCE of both entities 20 s after the DUT's set, about 6 s before the window, then at its middle and 15 s before its end, and after it."
  - `:3096` header: "DUT CLOCK_DOMAIN LOCKED / UNLOCKED, before the window and near its end".

### S1 SUGGESTION (Docs): the census counts its header record as an entry

- **Where:** `restore/census-*.jsonl` and `tools/census_cmp.py`.
- **Evidence:** "45 of 46 entries equal" counts the file's `{"type":"start",...}` record. The comparison therefore covers 45 reads, of which 44 are equal. This convention dates from lane B15, and the statement is true under the tool's definition.
- **Suggestion:** "44 of 45 reads equal".

### S2 SUGGESTION (Tests): publish the console poll's extremes

- **Where:** B16c's following record, `:3098-3129`.
- **Evidence:** several figures rest on `poll-run.jsonl`, which is hashed but not published:
  - the trim range -6.000 to -6.125 ppm;
  - the rate ranges +10.60 to +10.65 ppm and +10.60 to +10.63 ppm;
  - the `SLIP_LB` step times 2.66 s, 2.65 s and 5.68 s;
  - the "five steps in the 12 s between the binds and the set";
  - `0x...0074`.

  The published `poll-summary` gives only the first value, the last value and a distinct count per span. Its `peer-set..dut-set` span also includes the 5 s before the binds. Everything the published summary does carry agrees with the page: `SLIP_LB` 0xa2 to 0xae to 0xbc, `AAFM_STAT` `0x001e0007`, the 596 LOCKED polls, and `SLIP_TDM` 0.
- **Suggestion:** add per-span minimum and maximum values, and the step times, to the published summary.

**Prior public review findings on PR #725:** none. At the start of this round the PR had only the two review-start comments (6119031065 and 6119036339), so there is nothing to resolve or retain.

## Per-lens results

- [R624] UNCLEAN Conformance — artifacts below — F1 and F2 are open. Checked against the two rulings and the issue's acceptance:
  - **Peer set and restore:** the ruling's exception was used for B-CRF and B-AAF only. In each case the peer was set to 0 and read back 0, then restored to 1 and read back 1, after the DUT's unbinds (`runs/bcrf/events.jsonl` and `runs/baaf/events.jsonl` `set-clock`).
  - **DUT sets:** 1 or 2, then back to 0, each read back.
  - **Binding rule:** every listener format equalled its talker's, so none was set (`format-check`). In B16 the peer listener's format was set and restored (`runs/loop1/events.jsonl` and `runs/loop2/events.jsonl`).
  - **Full restore:** the B16 start census equals the B16c end census in every read except the DUT's propagation delay (`receipts/census.txt`). That includes the peer's STREAM_INPUT 0 and 8 bindings and both clock sources.
  - **B16's unreflected PROBE_TX:** `summary/loop2/acmp-peer-tap.json` shows CONNECT_RX_RESPONSE and CONNECT_TX_COMMAND at +99.6 ms and nothing returned. There were 14 listener polls per run, all with flags `0x0002` and stream ID 0, and the (d) channels are all zero over 1,056,000 and 768,000 frames.
  - **INTERNAL mismatch control:** stated as NOT run at `:3213`, `:3218-3220` and `:3231-3232`.
  - **Attribution:** the tone-source route and clock changes are attributed outside the lane at `:2466-2476` and `:2717-2741`, not to the DUT.
- [R624] PASS RTL — `git diff --stat c20c85bd..e20fd282` (two Markdown files, no HDL, firmware or tooling) and `docs/reference/REGISTER_MAP.md:1870-1871`, `:2076-2097` and `:2139` — the page's register decodes match the map:
  - `MCSRV_STAT` `0x...0034` is LOCKED and `0x...0074` adds the fine-PS busy bit; the trim is in 1/16 ppm (ffa0 = -6.000, ff9f = -6.0625).
  - `AAFM_STAT` `0x001e0007` reads locked, rate valid, enabled, listener 0, 0 restarts and 30 ns.
  - `SLIP_LB` counts two dups per slipped frame on the 4-channel stream, as lanes B7 and B8 used it.
- [R624] PASS Robustness — `tools/run_b16c.py:680-760` and `tools/dryrun_b16c/` — the abort, refusal and restore paths were re-executed offline in scratch, against stand-ins only:
  - All 8 dry-run scenarios PASS, matching `controls/b16c-dryrun-summary.json` (`receipts/dryrun/*.json`). They cover the DUT's set refused, a deadline signal mid-window, music found before the binds, no lock, the peer not found as recorded, and the agent ending at a bind.
  - Planted mutant R1 (the peer never restored) FAILS end-state, order and read-back.
  - Planted mutant R2 (restore order inverted) FAILS order.
  - The incidents are disclosed and placed outside the graded windows: `b0`'s busy device (`runs/b0/soc-record.log`), and the five underruns between 06:45 and 06:46, after `b0-2` ended at 06:43:09.4 and before `pts3`'s taps at 06:49:14.6.
- [R624] PASS Tests — `controls/` and `tools/` at `724b0974` — the grading tools' published controls were re-run offline and reproduce byte-equal (`receipts/controls-repro/SHA256.txt`):
  - `b6_thdn.py` `7bbefc71`, `b9_thdn.py` `728a4f0e`, `tone_points_b16.py` `77a5995f`, `align_b16.py` `20ca766e` and `dloop_b16.py` `fbce8878`.
  - The alignment controls can fail. Mutant M1, with the key and equality on the low byte only (lane B15's weakness), FAILS the +256 LSB control. Mutant M2, slip-blind, FAILS the drop and repeat controls (`receipts/align_mutants.txt`).
  - S2 is a suggestion only.
- [R624] UNCLEAN Docs — `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, `docs/findings/README.md` and the PR #725 body — F1 and F2 are open, and R1 and R2 are residue. The docs gates are rc 0 at the head (`receipts/gates/rc.txt`): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py` with base `c20c85bd` and with base `e8454e27`, `check_doc_paths.py`, and both `git diff --check`. The rest was checked as follows:
  - **Fragment links:** all 42 on the added lines resolve (`receipts/anchors.txt`).
  - **Hash rows:** every evidence row (52) and raw row (40) in the B16, B16b and B16c sections equals the packet's `MANIFEST.json` and `RAW-ARTIFACTS.json`. All 471 published files hash to their `published_sha256` (`receipts/check_hashes.txt`).
  - **Privacy:** the added lines name the reference peer and the external capture only by role. They carry no host path, host name, interface or vendor token. The DUT serial and McASP0 already appear in the tree at the base.
  - **Figures matched to receipts:** apart from F1, the following all match:
    - B16b's four-point table (pts1, pts2, pts3, b0-2), and the B0 grade with its 169 floor blocks;
    - the totals 3,077,452 / 3,077,980 and 3,289,015 / 3,290,863;
    - B16c's tables, matching `summary/b16c-tables.md` and the per-point stdouts;
    - (d): 13 of 16, 305 of 306, net -4 and 0 net steps;
    - the times in the B16c run table;
    - LOCKED at 2.657 to 3.161 s and 6.68 to 7.18 s;
    - the counters 22/21 to 24/23 (DUT) and 6/5 to 8/7 (peer);
    - MEDIA_RESET 0 to 4 on both DUT talkers (`restore/counters-startc.jsonl` and `restore/counters-endc.jsonl`).

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #629 acceptance; rulings 6117672835 and 6118365090; findings `:2276-3283`; `runs/*/events.jsonl`; `restore/census-*.jsonl`; `summary/loop2/acmp-peer-tap.json` | R624-1 | `e20fd2820a9c6b9effabc529a742e732263fafa8` |
| RTL | CLEAN | diff stat (docs only); `REGISTER_MAP.md:1870-1871, 2076-2097, 2139` against the page's decodes | R624-1 | `e20fd2820a9c6b9effabc529a742e732263fafa8` |
| Robustness | CLEAN | `tools/run_b16c.py` teardown and refusals; 8 dry-run scenarios re-run; mutants R1 and R2; incident placement | R624-1 | `e20fd2820a9c6b9effabc529a742e732263fafa8` |
| Tests | CLEAN | five tool controls reproduced byte-equal; alignment mutants M1 and M2 killed | R624-1 | `e20fd2820a9c6b9effabc529a742e732263fafa8` |
| Docs | UNCLEAN (F1, F2) | findings page; README row; PR body; docs gates; anchors; hash rows; privacy scan | R624-1 | `e20fd2820a9c6b9effabc529a742e732263fafa8` |

## Real limits

- No hardware or bench access. Every bench figure is checked against published receipts, not re-measured. The raw captures (pcap, McASP and external capture) and `poll-run.jsonl` stay on the bench host, so the per-point analyses were not re-run from raw data; only their hashes were checked against `RAW-ARTIFACTS.json`.
- The tool controls and the dry run were re-executed on this host's interpreter and numeric library. Byte-equality with the bench host's outputs is the evidence. No grading tool was run on a real capture.
- Physical calibration was NOT RUN, and printed precision is not accuracy, as the page states. No manager source bank runs at this head, and none is claimed or inferred. No RTL build, Verilator, Yosys or builder bank was run: the diff carries no HDL or tooling.
- Hosted contexts at the exact head, read once (`receipts/hosted-check-runs.tsv`):
  - success: `rtl-fast`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, `changes` and `bdd-conformance`;
  - skipped: `verilator-suites`, `yosys-portability` and their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit`, `publication-census` and physical gPTP;
  - still in progress when read: `docs-check`.

  The hosted contexts and the act acceptance are the manager's to judge.
- After every probe, the clone is unchanged: HEAD and tree are as above, the worktree and index are clean, the index equals the HEAD tree (blob, mode and stage hashes equal), and the submodule gitlinks are as pinned (`receipts/clone-integrity.txt`).

## Pending manager duties

- Carry R1 and R2 to the residue checklist.
- Publish this packet.
- After F1 and F2 are fixed, re-review the corrected head for Conformance and Docs.
- Judge `docs-check` and the other hosted contexts on the final head.
- Build and validate the current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6`) at the merge turn, and link its receipts.
- The external review is separate. A merge needs two independent positives and the full completion bar. #629 stays open: `Refs #629`, the INTERNAL mismatch control and #645.

R624-1 FINISHED
