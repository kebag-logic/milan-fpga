[R624] NEGATIVE - exact head 35e332b6be3de2b36c4aec0f1d0bc9f390447b74

Round R624-2: internal, independent review of PR #725 for issue #629 (bench lanes B16, B16b and B16c, docs and findings only). This round covers documents only, under the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763). It ran in a cleared context against a detached clone.

- Head `35e332b6be3de2b36c4aec0f1d0bc9f390447b74`, tree `870785667820e5cae10f060bbd48d0b524db4aeb`, source base `c20c85bd`.
- Diff: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+1185) and one row of `docs/findings/README.md`, in four one-line commits with no trailers.
- Read in this order:
  - AGENTS.md, CONTRIBUTING.md (sections 2, 6 and 6.1) and docs/README.md;
  - the #629 body;
  - the B16 assignment (6117305187), the rulings 6117672835 and 6118365090, and the round 2 assignment 6119316763;
  - the author's TAKEN, STOP, STOP (B16b), REVIEW READY (B16c) and REVIEW READY (round 2) comments;
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Bench) and `docs/reference/REGISTER_MAP.md` (`0x738`, `0x8D4`, `0x8E0`, `0x8F8`);
  - the diff and its history;
  - the published packet [`review-evidence/629-b16-r1` at `7affd601`](https://github.com/kebag-logic/milan-fpga/tree/7affd6015fd3bb56ef0fbd37499be3c6f188d9b3/review-evidence/629-b16-r1), `author-r2/`;
  - the PR #725 body and title.
- The prior reviews R624-1 and R625-1 were read only after this round's own pass over the diff and the receipts.

## Verdict

Two MINOR findings are open, so the verdict is NEGATIVE. F1 is under Robustness, Tests and Docs; F2 is under Tests and Docs. Neither alleges a DUT defect, and neither reverses a bench verdict.

Every round-1 finding is resolved at this head (see the reconciliation table). Re-derived from the published receipts:

- B0's floor medians, degraded runs, overlap split and recording start;
- all four of lane B6's terms, with the timed ratio NOT RUN;
- the attribution inside and beyond the taps' overlap;
- the reduced receipts.

Both open findings are figures that do not match what their receipts show:

- F1: the positive control's "blocks at the loop's floor" count includes two pre-playback blocks that are digital silence;
- F2: B16c's LOCKED bracket starts later than the poll data supports.

## Findings

### F1 MINOR (Robustness, Tests, Docs): the positive control's floor counts include two silent blocks before the playback

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2705` (`pts2`, "the loop's floor, in 13 of 16 blocks"), `:2706` (`b0-2`, "305 of 306"), `:2801`, `:3111`, `:3112` and `:3192` ("305 of 306").
- **Authority:** the assignment requires every figure to match a receipt. Lane B15's same control, at the same point (`:2113-2121`), counts only blocks that hold the playback: "The other blocks hold no playback, or its start or end."
- **Evidence:** `summary/{bcrf,baaf,b0-2,pts2}/d-extcap-pair.json`, `rows[*].tone_*.per_block`.
  - Blocks 0 and 1 of every one of these captures have level -475.38 dBFS and the THD+N sentinel -400.0 dB. They are digital zero, captured before the loop starts.
  - The decode agrees: `d-loop-decode.json` gives `invalid` 104,609, 102,076 and 104,714 frames before the loop, about 2.2 s.
  - A sentinel of -400 dB sits "within 3 dB of the median" only numerically. A silent block has no THD+N to be at a floor.
  - The correct counts are 303 of 306 for `bcrf`, `baaf` and `b0-2` (blocks 0 and 1 precede the playback, block 2 holds its start), and 11 of 16 for `pts2` (blocks 0 and 1 precede it, block 2 holds its start, blocks 6 and 12 hold the repeats). Receipt: `receipts/d-floor-blocks.txt`, from `scripts/d_floor_blocks.py`.
  - No tool in the packet emits these counts. `tools/tables_b16c.py` prints only `blocks` 306, so the page's figure has no receipt of its own.
- **Impact:**
  - The control's reported coverage overstates by two blocks per run. Two of the blocks credited "at the floor" could not fail by construction.
  - `pts2`'s "13 of 16" equals lane B15's "13 of 16" at the same point, but counts something different.
  - No verdict changes: 0 discontinuities, 0 net steps and PRESENT stand, and so does the design row's "tone blocks at the floor outside capture-path losses".
- **Required outcome:** each count states only blocks that hold the tone. Either give 303 of 306 and 11 of 16 with the silent blocks named, or define the count over blocks wholly inside the playback (303 of 303; `pts2` 11 of 13), as lane B15 did. Apply this at every location listed above.
- **Verification:** run `python3 -I scripts/d_floor_blocks.py summary/{bcrf,baaf,b0-2,pts2}/d-extcap-pair.json` in the packet and compare with the revised text.

### F2 MINOR (Tests, Docs): B16c's LOCKED bracket starts at the end of the last ACQUIRE poll, after that poll's state read

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2962` ("LOCKED 2.7 to 3.2 s") and `:2963` ("6.7 to 7.2 s");
  - `:3126` and `:3127` ("2.66 to 3.16 s", "6.68 to 7.18 s");
  - `:3146` and `:3379-3380`;
  - the `docs/findings/README.md:15` row ("2.7 to 3.2 s and 6.7 to 7.2 s");
  - the PR body's B16c result.
- **Authority:** every figure must be supported by its receipt. The lock-time bracket is part of the B16c focus ("LOCKED").
- **Evidence:** `receipts/locked-bracket.txt`, from the published `r2/*-poll-trace.tsv`.
  - In `bcrf`, poll 44 runs from 2.585 to 2.656 s and reads `MCSRV_STAT` `0xffab0033` (ACQUIRE). Poll 45 runs from 3.090 to 3.161 s and reads `0xffa60034` (LOCKED).
  - In `baaf`, poll 52 runs from 6.602 to 6.679 s (ACQUIRE) and poll 53 from 7.103 to 7.180 s (LOCKED).
  - `tools/console_poll_b8.py` issues `MCSRV_STAT` as the second of five console reads in each poll, so the ACQUIRE value was read before that poll ended.
  - `tools/run_b16c.py` `wait_state` nevertheless takes the bracket's lower edge as the earlier poll's end (`prev["raw1"]`). That gives 2.657 and 6.68 s, so the lock could have come up to about 70 ms before the stated bracket opens.
  - The same section brackets each `SLIP_LB` step from the earlier poll's start (`:3164-3166`, "2.08 to 2.66 s"), so the page uses two conventions side by side.
- **Impact:** the published lock-time interval can exclude the true lock instant. No verdict changes: "LOCKED within 15 s", LOCKED at 596 of 596 window polls, and lane B6's LOCKED term all stand.
- **Required outcome:** the bracket runs from the start of the last poll that read ACQUIRE to the end of the first poll that read LOCKED, which gives 2.59 to 3.16 s and 6.60 to 7.18 s. Alternatively, the text states exactly what the figures are ("the poll ending 2.66 s read ACQUIRE; the poll ending 3.16 s read LOCKED"). Apply this at every location listed above.
- **Verification:** compare the revised figures with `receipts/locked-bracket.txt`, or with `r2/bcrf-poll-trace.tsv` rows 44 and 45 and `r2/baaf-poll-trace.tsv` rows 52 and 53.

### R1 RESIDUE (Docs): two source-state statements read wider than the partial comparisons that support them

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2744` and `:3206-3207`.
- **Evidence:** `r2/source-receipt.json` `compare`.
  - B16b's later read caught 1,255 of the first read's 2,262 entries.
  - B16b's last read and B16c's first share 618 entries; the two B16c reads share 668.
  - The page states those counts, but then writes "So two settings changed" and "As read, the tone source's state was the same for B0 and for both cases here".
- **Exact fix:**
  - `:2744`: "So, among the 1,255 entries both reads hold, two settings changed: the clock setting and that output's level. The later read did not catch the other 1,007."
  - `:3206-3207`: "In the entries the reads around them both hold (618 between lane B16b's last read and B16c's first, 668 within B16c), the tone source's state read the same for B0 and for both cases here."

### R2 RESIDUE (Docs): B16c attributes all five pre-set `SLIP_LB` steps to the clock difference

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3159-3161`.
- **Evidence:**
  - B16b counted one slip per bind with the peer following the DUT, so with no clock difference (`:2862-2865`; `runs/b0/dut-*.txt` and `runs/b0-2/dut-*.txt`, `SLIP_LB` 156 to 158 and 158 to 160).
  - In each B16c case the first step falls 0.14 to 0.15 s after the binds (`receipts/poll-decode-*.json`).
  - The sentence's "so" states a cause that the receipts do not separate. No figure or verdict depends on it.
- **Exact fix:** "Then the DUT was on INTERNAL and the peer on its own clock. The steps are consistent with the ring absorbing the two clocks' difference and, for the first, with the one slip per bind that lane B16b counted; the receipts do not separate the two."

### R3 RESIDUE (Docs): the PR body's "Its INTERNAL mismatch control" has the wrong antecedent

- **Where:** the PR #725 body, section "#629".
- **Evidence:** the sentence follows "Lane B6's timed ratio for B-CRF and B-AAF was not run.", so "Its" reads as lane B6's. The control is Direction B's. The page has it right (`:3264`, `:3284-3285`).
- **Exact fix:** "Direction B's INTERNAL mismatch control did not run: B0 had the peer following the DUT, and the exception covers B-CRF and B-AAF only."

### S1 SUGGESTION (Docs): B16c's limits could carry the servo status bit 4 that lanes B6 and B7 recorded

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3129-3131` and the limits at `:3274-3289`.
- **Evidence:** `0x...0034` and `0x...0074` carry `MCSRV_STAT[4]`, DRP config mismatch (`docs/reference/REGISTER_MAP.md`, `0x8F8`). Lanes B6 and B7 recorded it as "recorded, not analysed" (`:505-506`, `:1181-1182`). B16c refers to it only as "as lane B7 read it".
- **Suggestion:** add the same one-line limit.

### S2 SUGGESTION (Docs), retained from R624-1 S1: "44 of 45 reads" would exclude the census header

The census header is counted as an entry. Optional; this round's author declined it, and the existing count is true under the tool's definition.

## Prior public findings, reconciled at this head

| Item | Disposition at `35e332b6` | Evidence |
|---|---|---|
| R624-1 F1 = R625-1 F3 (figures) | RESOLVED | `:2752` gives `b0-2` -123.98 / -123.95 dB and `pts3` -123.98 on both. `:2783-2784` gives the runs 0 to 18, 28 to 31, 43 to 44 and 46 to 54. `:2635` and `:2660-2664` give the recording start about 06:38:05.2, 26 s after the 06:37:39.2 binds. `pts2`'s start is corrected at `:2633`. Each reproduces: `receipts/b0-recompute.json`; the published `r2_b0_receipt.py` re-run is byte-equal to `r2/b0-2-receipt.json`; `runs/b0-2/events.jsonl` `captures-started` and `bind` |
| R624-1 F2 = R625-1 F4 (lane B6's four terms) | RESOLVED | `:3141-3153` states all four terms, matching lane B6's pass rule (`:328-330`). The timed ratio is NOT RUN, and no decision replaces it. This is repeated in the acceptance row (`:3264`), the limits (`:3279-3281`), the index and the PR body |
| R625-1 F1 (attribution) | RESOLVED | 131 is kept as the count at (c). 23 lie inside the whole blocks 0 to 33 of the 34.1136 s overlap and 108 beyond it, worst at block 224. The beyond-overlap part is labelled inference at `:2614`, `:2785-2801`, `:2886-2889`, `:3200-3209` and `:3286-3288`, in the index row and in the PR body. Recomputed independently in `receipts/b0-recompute.json` |
| R625-1 F2 (reduced receipts) | RESOLVED | `r2/` is published and bound to the raw hashes: the poll receipts carry `9cfc79bb...` and `476a0077...`, and the source receipt carries the twelve read hashes and the class map's hash. The extraction commands are at `:3404-3409`, with 6 of 6 controls. No identity, address or host path appears (scan below). My decode of the traces by `REGISTER_MAP.md` reproduces every poll figure on the page (`receipts/poll-decode-*.json`). The traces also equal the round-1 `poll-summary` published in `runs/*/events.jsonl`, in first, last and distinct values for every span and word (`receipts/trace-vs-r1-summary.txt`; the check fails on a mutated trace, `receipts/probe-trace-vs-summary.txt`). The narrowing is partial; see R1 |
| R624-1 R1 = R625-1 R1 (title) | RESOLVED | The PR title now equals the exact fix |
| R624-1 R2 = R625-1 R2 (counter mark) | RESOLVED | `:2994-2996` and the header at `:3124` read as the exact fix. The marks fall at 20.0 s after the set, at the window's middle, at 15 s before its end, and after it (`runs/{bcrf,baaf}/events.jsonl`) |
| R624-1 S1 = R625-1 S1 (census wording) | RETAINED as optional S2 | Declined by the author |
| R624-1 S2 (poll extremes) | Superseded by R625-1 F2, RESOLVED | as above |

The round-1 reviews matched "13 of 16" and "305 of 306" against the rule's count. F1 is new in this round, and so is F2, which concerns the bracket rule rather than its equality with the run's record.

## Per-lens results

- [R624] PASS Conformance — `runs/{loop1,loop2,pts1,pts2,pts3,b0,b0-2,bcrf,baaf}/events.jsonl`, `summary/loop2/acmp-peer-tap.json`, `restore/census-*.jsonl`, `restore/counters-{startc,endc}.jsonl`, and findings `:2279-3447` against the B16 assignment, both rulings and the round 2 assignment. Checked:
  - **B16's loopback:**
    - the BIND_RX response and the peer's first PROBE_TX (CONNECT_TX_COMMAND) both come 99.6 ms after the UNBIND_RX command, and the second probe at 299.6 ms;
    - no CONNECT_TX response appears among the 38 ACMP messages, and no further probe in the tap's remaining 49 s (tap 52.5 s from 05:59:19);
    - all 14 listener reads per run show flags `0x0002` and stream ID 0;
    - (d) is all zero over 1,056,000 and 768,000 frames.
  - **The ruling's exception:**
    - `set-clock` events: in each case the peer is set to 0 and reads back 0, the DUT is set to 1 or 2 and reads back, the DUT goes back to 0 and reads back 0, and the peer, after the DUT's unbinds, goes back to 1 and reads back 1;
    - the censuses read the peer's GET_CLOCK_SOURCE as 1 at the B16c start and end;
    - B16 and B16b set no clock source, and the DUT reads 0 before and after each B0 window.
  - **Bindings:** every format equalled its talker's, so none was set. `final.equal_to_found` is true in each B16c run, and every census is 45 of 46 equal, the other entry the DUT's propagation delay (0x183 to 0x179 in B16).
  - **Residual counters:** MEDIA_RESET 0 to 4 on both DUT talkers and both peer listeners; CLOCK_DOMAIN 22/21 to 24/23 on the DUT and 6/5 to 8/7 on the peer; MEDIA_RESET timed at the marks as stated.
  - **Attribution:** the source routing and clock changes are attributed outside the lane, not to the DUT (`:2471-2481`, `:2729-2763`). The (a) level steps from -14.1353 to -14.1035 dBFS between 06:28:50 and `b0`'s first (a) frame at 06:31:51.6 (`summary/b0/a-peer-tap.json`), and `pts3` without the CRF bind reads as B0.
  - **INTERNAL mismatch control:** stated NOT RUN at `:3264`, `:3269-3271` and `:3284-3285`, in the index and in the PR body.
  - **Lane B6's four terms:** see the reconciliation table.
  - **Names:** the reference peer and the external capture are named only by role.
- [R624] PASS RTL — `git diff --stat c20c85bd..35e332b6` (two Markdown files, no HDL, firmware, tooling or gitlink) and `docs/reference/REGISTER_MAP.md` `0x738`, `0x8D4`, `0x8E0`, `0x8F8`. The page's decodes agree with the map, as reproduced by `scripts/decode_poll_trace.py`:
  - state 4 is LOCKED and `0x74` adds `[6]` fine-PS busy (580/16 and 584/12 in the window);
  - the trim in 1/16 ppm spans -6.125 to -6.000;
  - `CRF_RATE` and `AAFM_RATE` at 512 per ppm give +10.600 to +10.652 and +10.600 to +10.631 (CRF in B-AAF +10.586 to +10.646);
  - `AAFM_STAT` `0x001e0007` reads locked, rate valid, enabled, listener 0, 0 restarts and 30 ns;
  - `SLIP_LB` steps by 2 per slipped frame on the 4-channel stream, and `SLIP_TDM` is 0 throughout.
- [R624] UNCLEAN Robustness — F1 is open (a silent, minimum-level block credited as at the floor). Also applied, and clean outside F1:
  - `runs/b0/soc-record.log` and `runs/b0/events.jsonl`: the incident is excluded from grading, and its (a) and (d) serve only to place the source change;
  - the five underruns at 06:45 to 06:46 lie outside every capture window;
  - `controls/b16c-dryrun-summary.json`: 8 of 8, including refusal, deadline, no lock, peer not as found, and the agent ending;
  - the lock windows in `runs/{bcrf,baaf}-lock.txt` are 07:50:00 to 07:56:15 and 07:56:52 to 08:03:07;
  - in both cases the window holds no straddling poll or `SLIP_LB` step, and the last 12 polls after the restore read IDLE.
- [R624] UNCLEAN Tests — F1 and F2 are open. Also applied, and clean outside them:
  - `scripts/check_point_tables.py` rebuilds all 20 point-table rows from the per-point JSON. Every cell matches, except `pts3` (a)'s 9,973 Hz SNR, which is 122.475 printed half-up as 122.48: a rounding boundary, not a defect.
  - The B16c grade rows, the alignments (34.33, 34.30, 34.19 and 34.26 s, 0 differing) and the frame totals 3,077,452 / 3,077,980 and 3,289,015 / 3,290,863 match.
  - The (d) decodes match: 14,583,391, 14,585,924, 14,583,286 and 14,583,189 frames; 0 net steps; `pts2` -4 net at 6.131 and 12.113 s.
  - The published `r2_b0_receipt.py` reproduces byte-equal on a copy. It fails when the run tool's 2 s lead is altered, and moves its counts when a degraded block is planted. My recompute flags the same plant.
  - My trace decoder finds a `SLIP_LB` step and an ACQUIRE poll planted after LOCKED (`receipts/probe-poll-decoder.txt`).
- [R624] UNCLEAN Docs — F1 and F2 are open; R1 to R3 are residue. Also applied, and clean outside them:
  - **Gates at the head**, all rc 0 (`receipts/gates/rc.txt`) in the pinned Markdown environment: `docs_check.py`; `check_doc_style.py`; `gen_toc.py --check` and `--verify-anchors`; `check_em_dash.py` with base `c20c85bd` (0 findings over 1,186 added lines) and with base `e8454e27`; `check_doc_paths.py`; `ci_scope.py --selftest`; `check_baremetal_only.py --check`; `check_feature_status.py --self-test`; and `git diff --check c20c85bd HEAD`.
  - **Hash rows:** all 62 evidence-file rows in the B16, B16b, B16c and round 2 sections equal the packet, with manager path redaction accounted for through `MANIFEST.json` `original_sha256` (`receipts/doc-hash-check.txt`). All 52 raw rows, including the twelve tone-source reads, equal `RAW-ARTIFACTS.json` (`receipts/raw-row-check.txt`). `author-r2/MANIFEST.sha256` verifies except 9 files, each marked `path_redacted` with its original hash equal.
  - **Privacy:** a scan of the added lines and the PR body finds no host path, address, interface or vendor token. The `r2/` files and tools carry only hashes.
  - **The PR body** equals `author-r2/PR-BODY.md`.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment, rulings and round 2 assignment; findings `:2279-3447`; `runs/*/events.jsonl` `set-clock`, `bind` and `final`; `summary/loop2/acmp-peer-tap.json`; `restore/census-*.jsonl` and `counters-*c.jsonl`; README row; PR body | R624-2 | `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` |
| RTL | CLEAN | Diff stat (docs only); `REGISTER_MAP.md` `0x738`, `0x8D4`, `0x8E0` and `0x8F8` against the page's decodes and both `r2/*-poll-trace.tsv` | R624-2 | `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` |
| Robustness | UNCLEAN (F1) | `summary/*/d-extcap-pair.json` per-block; incident and underrun placement; dry-run summary; lock windows; post-restore polls | R624-2 applied; not clean | `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` |
| Tests | UNCLEAN (F1, F2) | Point tables (20 rows); grades; alignments; (d) decodes; `r2/` receipts re-derived; trace against the round-1 summary; `console_poll_b8.py` and `run_b16c.py` `wait_state`; fault probes | R624-2 applied; not clean | `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` |
| Docs | UNCLEAN (F1, F2) | Findings page; README row; PR title and body; 14 gate runs; 114 hash rows; privacy scan | R624-2 applied; not clean | `35e332b6be3de2b36c4aec0f1d0bc9f390447b74` |

## Real limits

- **No bench access.** The raw captures, the raw polls and the tone source's reads are private, and only their hashes were checked against `RAW-ARTIFACTS.json`. Every figure was checked against published reduced data, not re-measured.
  - The poll traces are bound to the raw polls by the author's tool. Independently, they are bound to the round-1 `poll-summary` already published.
  - The source receipt cannot be re-extracted without the private reads and class map.
- **Interpreter.** The published `r2_b0_receipt.py` and my scripts ran on this host's interpreter, offline, on copies.
- **Not run.** Physical calibration was NOT RUN; printed precision is not accuracy. No manager source bank runs at this head, and none is claimed or inferred. No RTL, Verilator, Yosys or builder bank was run: the diff carries no HDL or tooling.
- **Hosted contexts at the exact head**, read at 07:34Z (`receipts/hosted-check-runs-final.tsv`):
  - executed and successful: `rtl-fast`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`, `elaborate`, `bdd-conformance` and `changes`;
  - skipped: `verilator-suites`, `yosys-portability` and their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit`, `publication-census` and physical gPTP;
  - `docs-check` was still in progress (started 07:20:31Z).
- **Clone integrity.** After every probe the clone is unchanged: HEAD and tree are as above; the index tree equals the HEAD tree; the worktree and index are clean with no untracked file; 1,291 tracked blobs re-hash with their modes; the gitlinks equal their pins, and the required submodules are initialised at them (`receipts/clone-integrity.txt`).

## Pending manager duties

- Carry R1, R2 and R3 to the residue checklist. S1 and S2 are optional.
- Publish this packet.
- After F1 and F2 are corrected, arrange re-review of Robustness, Tests and Docs at the corrected head. Conformance and RTL are covered clean here; they need re-coverage only if a later commit touches their scope.
- Judge whether the published entry counts of the tone source's state reads (2,262, 1,255, 1,351 and 1,248) state its control layout. This round raises no finding on it, because the author withheld byte sizes on that ground and the redaction is the manager's.
- Judge `docs-check` and the other hosted contexts on the final head, and own the hosted and act acceptance.
- At the merge turn, build and validate the current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`) and link its receipts.
- Two independent positives and the full completion bar are required; this report authorises no merge. #629 stays open (`Refs #629`), with the INTERNAL mismatch control, lane B6's timed ratio and #645.

R624-2 FINISHED
