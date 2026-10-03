[R450] NEGATIVE - exact head f4eb39d3fddbbd9e2de1947750cc1b482baff53d

# R450-2: internal re-review of PR #644 (issue #629, bench lane B7), round 2

- **Head:** `f4eb39d3fddbbd9e2de1947750cc1b482baff53d`, tree `a9e726321f3132acb6f460b886850ac95e54fc0a`. That is two commits on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`: round 1 `4eee41a5` and round 2 `f4eb39d3`.
- **Round-2 delta (`4eee41a5..f4eb39d3`):** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only, +108 / -37 (`receipts/delta-round2.diff`). It is docs only, with no code, RTL, test or generated file. `docs/findings/README.md` is unchanged since round 1.
- **Evidence examined:** branch `629-b7-review-evidence`:
  - at the page's pin `d36de704456713fb89b39a59151b72015fa00c6d`, path `review-evidence/629-b7-r1/author/`;
  - its first publication `95448218`;
  - the branch tip when read, `2d0dc7e3`, which adds only `author-r2/HANDOFF.md`, `author-r2/PR-BODY.md` and the manifest. `author/` is byte-unchanged since `d36de704` (`receipts/evidence_branch_state.txt`).
- **Context, in this order:**
  1. AGENTS.md and CONTRIBUTING.md (sections 2, 3 and 6);
  2. docs/README.md;
  3. #629's body;
  4. the lane B6 assignment (5929778646), the lane B7 assignment (5969106115), [A519] TAKEN and REVIEW READY, and the round-2 assignment (5970119417);
  5. the design and reference authorities the page cites: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Switching sources :1035-1052), `docs/design/TIME_SYNC.md:385`, and `docs/reference/REGISTER_MAP.md` (0x8D4 :1867, 0x8E4 :2074, 0x8F8 :2136);
  6. the diff and history;
  7. the evidence packet;
  8. the hosted check runs;
  9. #645.
- **Prior findings:** R450-1 and R451-1 were read only after this round's own pass over the diff and evidence. Their status is given in "Prior public findings" below.

## Independent checks at this head

Each check below was run against the published run artifacts, not the page's prose. The receipts are listed in `MANIFEST.sha256`.

| Round-2 claim | Check | Result |
|---|---|---|
| Criteria written down at 14:50, during A0's window; A0 started 14:41:42, window 14:42:08 to 14:52:39; A1 started 14:52:53 | `scripts/run_times.py` over every `runs/*/events.jsonl` (epoch to CEST, UTC+2) | Holds. A0 start 14:41:42.336, window 14:42:08.907 to 14:52:39.336, A1 start 14:52:53.150. Every window start equals the page's tables (`receipts/run_times.txt`). The packet's `HANDOFF.md:66` heading still reads "fixed 14:50 CEST, before any case ran". The page no longer repeats that, and states the true order |
| Thresholds listed as fixed in the 14:50 record are those `b7_tables.py` applies | Read `tools/b7_tables.py:56-83` against `HANDOFF.md:68-77` and page :782-786 | Holds: 2 ppm, 0.01 dB, 0.001 ppm, 0.5 ppm and 15 s |
| A0's threshold basis is independent of A0's data | Page :792-800 against lane B6's text on dev (:396-400) | Holds. B6 counted +6.52 ppm net and a 10.6 ppm beat; 186 = 630 - 444 blocks off the floor |
| Hash tables: 19 rows recorded in each run's `events.jsonl`, 7 full-grade rows only in `RAW-ARTIFACTS.json`, evidence rows equal to `published_sha256` at `d36de704`, and the two masked tools equal to `redaction.json` `original_sha256` | `scripts/check_page_hashes.py` (all 45 rows: hash and bytes) | PASS, 0 problems (`receipts/check_page_hashes.txt`). A planted fault probe (two hashes and one byte count altered) fails 4 checks (`receipts/check_page_hashes_mutant.txt`) |
| Packet published at `d36de704`, mapping `629-b7-a519` to `review-evidence/629-b7-r1/author/` | The pin is an ancestor of the branch tip; `author/summary/a1/grade.json` exists there; `MANIFEST.json` carries `original_sha256` and `published_sha256` | Holds |
| Drift 0.54 to 0.93 frames/s over the six windows | `frame_rate_ratio.external_capture.rate` in the six `summary/<case>/grade.json` | Holds: deficits 0.838, 0.543, 0.650, 0.826, 0.929 and 0.765 |
| Conservative count: A2 3 frames in 2 clusters, B-AAF 3 in 3 | `summary/checks/absorb.jsonl`, `item1_clusters_net_off` | Holds. A2 is -2 (100,810 frames) and -1 (215 frames); B-AAF is -1 three times (57,395, 155 and 4,331). Item 4 also holds: 47 clusters, rise 0.973 to 2.006 ms, gap 10.678 ms or more |
| B0 timeout: CLOCK_DOMAIN 0 GET_COUNTERS at `window-mark-1`, 15:20:58, 1 s, not retried; next mark 15:25:57 answered 3/2; the only non-SUCCESS of 336 DUT commands | `scripts/b0_timeout_record.py` over `runs/b0/ctl.jsonl` and every run's `ctl.jsonl`; `runs/b0/events.jsonl` marks | Holds, except the name of the next command (RES-1): it was GET_COUNTERS on STREAM_OUTPUT 0, descriptor type 0x0006 (`receipts/b0_timeout_record.txt`) |
| PR #634 head `2bc5adc0`: 21 executed contexts SUCCESS, "Physical gPTP (nightly and manual)" skipped | Check runs of `2bc5adc0` | Holds: 21 success, 1 skipped (`receipts/checkruns_2bc5adc0.tsv`) |
| B-AAF listener ring: `SLIP_LB` 386 to 388 between window reads 0 and 1, 14 to 45 s after LOCKED, then 570 s static; 6 dups between the set and the window; 2 across the lock loss | `scripts/slip_lb.py` decoding 0x8D4 from every `runs/baaf/dut-*.txt`; the set and LOCKED times from `events.jsonl` | Holds. 380 before the bind (the set followed it within 1 ms), 386 at +1 s, 388 from +31 s to +601 s, 390 after the lock loss. B0's 20 to 362 gives 342 (`receipts/slip_lb_baaf_b0.txt`) |
| #645 takes the slip | `gh issue view 645` | Open. Its scope and acceptance cover the slip, cause and a bench repeat of the switches (`receipts/issue645.json`) |
| Lock loss, "LOCKED 5.6 to 6.1 s after the return" | The 0x8F8 state in `runs/baaf/poll-ll-return.jsonl` against the `ll-rebind` event | Holds: 3 -> 4 between 5.55 and 6.05 s by host stamps, so 5.6 to 6.1 rounds both bases |
| No case verdict changed | `scripts/verdict_cells.py`: every Verdict, Result and Judgement cell of the B7 section at `4eee41a5` against `f4eb39d3` | Holds. Every case verdict and Result cell is identical. Only the Fabric acceptance judgement changed, and it is narrower ("not shown free of undeclared discontinuity", #645) (`receipts/verdict_cells_r1_r2.txt`) |
| Controls and tone unchanged from lane B6 | Re-ran the published `b6_tone.py` and `b6_thdn.py controls` (hashes `d188a1a9...` and `d4673f55...`, equal to lane B6's on dev :680-681) | Tone loop `566d3dfa...` reproduced. `controls.json` is byte-equal to `7bbefc71...`, ALL_PASS True |
| Docs gates at this head | `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py` with the shared Markdown venv; `gen_toc.py --check`, `gen_toc.py --verify-anchors` and `check_em_dash.py --base bbf704ec` in a disposable venv built from `tools/markdown/requirements.txt` with `--require-hashes`; `git diff --check bbf704ec HEAD` | All rc 0 (`receipts/gates/`). The shared venv lacks one pinned package, so the three renderer gates refused there (rc 2) before the disposable venv |
| Hosted contexts at this head | Check runs of `f4eb39d3` | 8 executed, all SUCCESS: `rtl-fast`, `docs-check`, `docs-check-no-git`, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `elaborate` and `changes`. 7 SKIPPED, not executed: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, both shard matrices and "Physical gPTP" (`receipts/checkruns_f4eb39d3.tsv`) |
| Privacy of page, PR body and evidence | `scripts/privacy_capture_scan.py`. It reads the format token at run time from an unpublished file, and prints paths and counts, never values | F-R450-2-1 |

## Findings

### F-R450-2-1. MINOR (Docs, Conformance): capture values that the evidence's own redaction classes as private stay public, and the page and PR body describe the masking as complete

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1163`: the B7 raw-hash row prints the external capture's sample format as the format of `a0/cap-lr.raw`.
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1203-1206` and the PR body's "Evidence" paragraph: "`d36de704` masked the external capture's channel count and format in the docstrings of four tools ... the redaction pass had masked that value in their code but not there".
  - The published packet at `d36de704`, and unchanged at the branch tip `2d0dc7e3`: 19 files still carry the capture's channel count, in the capture-file name. They are:
    - `author/RAW-ARTIFACTS.json` (7 occurrences);
    - `author/runs/<case>/events.jsonl` for all seven runs;
    - `author/runs/<case>-lock.txt` for the same seven;
    - the code of the four tools that `d36de704` masked: `tools/run_b7.py`, `run_b6.py`, `grade_b7.py` and `grade_b6.py`.
- **Authority/evidence:**
  - The packet's redaction treats both values as private. `run_b7.py:87` masks the channel count as `<capture-channels>`, and `d36de704` masks the format as `<capture-format>`. The round-2 assignment (item 2) and the PR body both say they were masked.
  - The lane assignments bar instrument detail from public text: B6's 5929778646 constraints, which B7 carries ("B6's method ... unchanged"). CONTRIBUTING.md section 6 names bench equipment by role and bars bench-identifying information.
  - `receipts/privacy_capture_scan_d36de704.txt`: at `d36de704` the channel-count file name is in 19 files, and the page carries the format at :1163 (and at :596, lane B6's row on dev, outside this diff).
  - The same receipt, at `95448218`: the format was not only in docstrings. It was the literal capture-command argument in the code of `run_b6.py` and `run_b7.py` (2 occurrences each), and `d36de704` masked it there too (`run_b6.py:457`, `run_b7.py:516` at `d36de704`). So "the redaction pass had masked that value in their code" is not what the record shows. The channel count is also still in those tools' code, as the output file name.
  - This report does not repeat either value.
- **Impact:** an instrument-identifying detail stays public in the evidence the page pins, and in the page itself. Meanwhile the page and PR body tell a cold reader that it was masked. The verdicts and measurements are unaffected.
- **Required outcome:**
  - **(a) One consistent position.** Either:
    - a recorded manager or owner ruling that the capture's channel count and sample format are not private, with the masking claims reconciled to it; or
    - consistent masking: the B7 row at :1163 no longer states the format, and the published evidence masks the channel count in the capture-file name everywhere it occurs, with the handling of the already-public commits stated. The identical lane B6 row at :596 is on dev and outside this diff; it is the manager's call, for example a follow-up.

    The page's hash rows are unaffected either way. No row cites a file that the masking would change: the raw rows are the hashes recorded inside `events.jsonl`, and `run_b7.py`/`grade_b7.py` cite `original_sha256`.
  - **(b) An accurate description of `d36de704`.** The page and the PR body describe what it changed: the four tools' docstrings, plus the capture command's format argument in `run_b6.py` and `run_b7.py`. They do not state that the code was masked where it was not.
- **Verification:**
  - `scripts/privacy_capture_scan.py` over the republished packet and the page reports 0 files and 0 page lines in this diff, or the ruling is linked;
  - the page's sentence is compared with `git diff 95448218 <new pin> -- review-evidence/629-b7-r1/author/tools`.

No other open BLOCKER, MAJOR or MINOR.

## RESIDUE

Each item is wording only. It changes no measurement, figure, verdict, test, code, generated artifact or conformance claim, and touches no privacy rule. Each goes to the residue checklist with its exact fix.

- **RES-1:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:941-942`.
  - The sentence reads "the DUT answered the mark's next command, GET_COUNTERS on STREAM_INPUT 0, at once".
  - The record shows the mark's next DUT command was GET_COUNTERS on STREAM_OUTPUT 0, descriptor type 0x0006 (`counters-dut-6-0`). STREAM_INPUT 0 was the DUT's third command after it, also answered at once (`receipts/b0_timeout_record.txt`).
  - Exact fix: "the DUT answered the mark's next command, GET_COUNTERS on STREAM_OUTPUT 0, and its other three, at once."
- **RES-2:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1155-1156`.
  - The sentence reads "Each run's `events.jsonl` records the size and SHA-256 of its three raw files and of the tone loop".
  - Each records seven raw-file entries, of which the page tabulates three plus the tone loop. The hash claim itself holds.
  - Exact fix: "Each run's `events.jsonl` records the size and SHA-256 of every raw file of its run, among them the three per case below and the tone loop: the first 19 rows below."
- **RES-3:** the PR body's "Round 2" table numbers two rows "7" (R450-1 R1/R2, and R451-1 RESIDUE-2).
  - Exact fix: renumber the second "7" as "8" and "8" as "9".

## SUGGESTIONS

- **S1.** Extend the README row's last cell (`docs/findings/README.md`, unchanged since round 1). It names only Direction B's THD+N as open, while the page's acceptance section now also leaves the fabric switch open. Append: "; the one INTERNAL-to-AAF switch left an undeclared one-frame slip on the DUT's listener ring (#645)".
- **S2.** Name the source of the byte counts at :1223-1224 (32,321 and 27,057, the masked tools as run). `redaction.json` records only hashes, so the as-run byte counts have no public record.
- **S3.** Give B0's one unanswered AECP command a public home, as #645 does for the slip: a new Issue, or a ruling that it needs none. One timeout in 336 commands is weak evidence, but "not analysed" leaves no owner.
- **S4.** For the manager's privacy pass: `author-r2/HANDOFF.md:47`, at the branch tip, names the external capture's USB audio class. The class is not a product name, but it narrows the instrument together with the values in F-R450-2-1.

## Prior public findings

Each was read only after the pass above. Status at `f4eb39d3`:

| Item | Status | Evidence |
|---|---|---|
| R450-1 F1 (MINOR): drift range and one-basis conservative count | Resolved | :1065-1073 read 0.54 to 0.93 and "3 in its 2 clusters / 3 in its 3 clusters"; both re-derived above |
| R450-1 F2 = R451-1 F1 (MINOR): the grading order | Resolved | :758-800 give the true order, the evidence path, a "Fixed" column, the 14:55 summary fix and the A0 basis apart from A0's data; the PR body's sentence is corrected. The 14:37, 14:58 and 15:40 times are bench-host file times, which the page says the packet does not carry |
| R450-1 F3 (MINOR): the B0 timeout | Resolved | :938-945 record case, mark, command and target, no retry, the next mark, and "not analysed"; one wording slip remains (RES-1) |
| R450-1 F4 = R451-1 RESIDUE-1: the skipped context | Resolved | :1123 checked against the PR #634 check runs |
| R450-1 F5 (MINOR): the Fabric judgement | Resolved | The Fabric row :1120, the B-AAF summary row :714, :974-986, the closing sentence :1128-1131 and the limits :1146-1147 state it and cite `SLIP_LB` 386 to 388 and the 6 dups. #645 is open with matching scope. No case verdict changed |
| R450-1 F6 (MINOR): capture value in four tool docstrings | Resolved as scoped (the docstrings are masked at `d36de704`); the underlying defect is retained elsewhere | The same values stay in the capture-file name in 19 evidence files and in the page at :1163, and the page's description of the masking is inaccurate: F-R450-2-1 |
| R450-1 R1 | Resolved | :845-846, text as specified. Values are equal to `summary/tables.md`; only the number format differs, for example `2.7e-7` for `2.7e-07` |
| R450-1 R2 | Resolved | :716 and the PR body read "LOCKED 5.6 to 6.1 s after the return" |
| R450-1 S1 to S3 | Not taken (optional) | Round-2 assignment item 8 |
| R451-1 F2 (MINOR): packet location and row sources | Resolved | :1154-1211; `check_page_hashes.py` 0 problems over 45 rows. Wording residue RES-2 |
| R451-1 RESIDUE-2: "12 live descriptors" in a comment | Retained as a note | Outside the diff, and comments may not be edited. The page says 11 and the PR body notes it. It stays on the residue checklist |
| R451-1 S1, S2 | Not taken (optional) | |
| R451-1 S3 | Covered | #645 |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-R450-2-1) | Every row of the acceptance table at :1116-1131 against #629's items and the evidence; "Refs #629" in the PR body; #645's scope against #629's Fabric item and `MEDIA_CLOCK_FOLLOWING.md:1044-1052`; verdict cells at `4eee41a5` against `f4eb39d3` (`receipts/verdict_cells_r1_r2.txt`); the lane assignments' public-text constraint against the page, PR body and packet (`receipts/privacy_capture_scan_d36de704.txt`) | R450-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| RTL | CLEAN | No HDL in the diff (`receipts/delta-round2.diff`). The page's register claims against `REGISTER_MAP.md:1867` (0x8D4 `SLIP_LB`, one dup per fed pair), `:2136` (0x8F8 states and trim units; poll word `0xffa10035` = HOLDOVER, DRP mismatch, -5.94 ppm) and `:2074`; the switch and recentre contract at `MEDIA_CLOCK_FOLLOWING.md:1035-1052` and `TIME_SYNC.md:385` against :978-986 and the decoded `runs/baaf/dut-*.txt` (`receipts/slip_lb_baaf_b0.txt`) | R450-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| Robustness | CLEAN | The B0 unanswered command against `runs/b0/ctl.jsonl` and all eight runs' AECP statuses (`receipts/b0_timeout_record.txt`); the lock-loss return time from `runs/baaf/poll-ll-return.jsonl`; the B-AAF ring slip timeline (`receipts/run_times.txt`, `receipts/slip_lb_baaf_b0.txt`); the conservative-reading text :1062-1073 against `absorb.jsonl`. Wording slip RES-1 only | R450-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| Tests | CLEAN | Controls and tone loop re-run byte-equal from the published tools; the thresholds in `tools/b7_tables.py:56-83` against the 14:50 record and the page; drift and off-signature figures re-derived from the six `grade.json` and `absorb.jsonl`; all 45 hash rows checked, with a planted fault probe failing 4 checks; PR #634 check runs (21 success, 1 skipped) | R450-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| Docs | UNCLEAN (F-R450-2-1) | The whole round-2 delta, and the B7 section :691-1233 with its intro (:8-9) and Contents line (:51); the README row; the PR body; docs gates rc 0 (`receipts/gates/`); the privacy scan of the page, PR body and packet at `95448218`, `d36de704` and `2d0dc7e3` | R450-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |

Three lenses are covered clean at this exact head: RTL, Robustness and Tests. Conformance and Docs remain unclean while F-R450-2-1 is open.

## Real limits

- **Raw files:** the captures, timing samples and full grades are not published. The audio was not re-decoded, and the raw-file hashes were checked against the packet's records (`events.jsonl`, `RAW-ARTIFACTS.json`), not against bytes.
- **Masked tools:** `run_b7.py` and `grade_b7.py` cannot be run as published. Their as-run hashes are checked against `redaction.json`; their as-run byte counts have no public record (S2).
- **Bench-host times:** the 14:37, 14:58 and 15:40 file times have no record in the packet. Only the 14:50 record and the run logs were checkable. The 14:50 time itself is the operator's record.
- **Hardware and calibration:** physical calibration NOT RUN, and no hardware was touched. The field skips are not hardware proof. Each case is one run on one DUT against one peer.
- **Builds and banks:** no simulation, builder, Verilator or Yosys bank was run. The Simulation row rests on PR #634's merged hosted evidence.
- **Hosted contexts at this head:** the 7 skipped contexts are docs-only scoping, not execution evidence.

## Pending manager duties

- F-R450-2-1: the privacy ruling or the consistent masking and republication, plus the corrected description of `d36de704`, then a re-review of Conformance and Docs at the new head.
- Carry RES-1 to RES-3, and R451-1 RESIDUE-2, to the residue checklist.
- Hosted and local-replica acceptance at the exact head.
- At the merge turn, the final current-dev candidate validation (source base `bbf704ec`; live dev was `bbf704ec` at review start). This is distinct from this source review.
- The second positive review: this round is NEGATIVE.

## Receipts

Paths are relative to this packet and listed in `MANIFEST.sha256`.

- **Scripts:** `scripts/check_page_hashes.py`, `scripts/run_times.py`, `scripts/b0_timeout_record.py`, `scripts/slip_lb.py`, `scripts/verdict_cells.py` and `scripts/privacy_capture_scan.py`.
- **Receipts:**
  - `receipts/check_page_hashes.txt` and `check_page_hashes_mutant.txt`;
  - `run_times.txt`, `b0_timeout_record.txt` and `slip_lb_baaf_b0.txt`;
  - `verdict_cells_r1_r2.txt` and `privacy_capture_scan_d36de704.txt`;
  - `evidence_branch_state.txt`;
  - `checkruns_2bc5adc0.tsv`, `checkruns_f4eb39d3.tsv` and `status_*.tsv`;
  - `issue629.json`, `issue629_comments.json`, `issue645.json`, `pr644.json` and `pr644_comments.json`;
  - `delta-round2.diff` and `delta-round2.worddiff.txt`;
  - `gates/` and `clone-integrity.txt`.
- **Clone state:** the clone is left at exact head bytes (`receipts/clone-integrity.txt`):
  - write-tree `a9e72632...` equals the HEAD tree;
  - the worktree equals the index, which equals HEAD;
  - 998 entries, with 0 blob or mode mismatches;
  - the ignored `scripts/__pycache__/` created by this round's gate runs was removed, leaving 0 untracked or ignored entries;
  - gitlinks: verilog-axis `48ff7a7e`, protocol-processor `631eeb34`, gptp-processor `5dce647a`, external `efeb541a` (uninitialised).

R450-2 FINISHED
