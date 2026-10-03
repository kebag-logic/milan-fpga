[R451] NEGATIVE - exact head f4eb39d3fddbbd9e2de1947750cc1b482baff53d

Round R451-2. This is the external independent review of issue #629 / PR #644 (bench lane B7). It reviews the round-2 delta `4eee41a5..f4eb39d3`, which is docs only.

- Head `f4eb39d3fddbbd9e2de1947750cc1b482baff53d`, tree `a9e726321f3132acb6f460b886850ac95e54fc0a`.
- Two commits on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`.
- Round 2 changes only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+108/-37). Its commit message is one line with no trailers.
- The PR body says `Refs #629`, which is correct: not every #629 item is met.

**Verdict basis:** three open MINOR findings.

- F1 (Docs): a capture value that the evidence's own redaction treats as private is still public. The sample format is on the page, and the channel count is in the pinned evidence.
- F2 (Docs): the page misdescribes what `d36de704` masked.
- F3 (Conformance, Robustness, Docs): the new B0-timeout paragraph names the wrong descriptor for the command that answered next.

RTL and Tests are covered clean at this head. Every round-1 finding of R450-1 and R451-1 is resolved except R450-1 F6, which is retained in part (F1, F2). No case verdict changed between `4eee41a5` and `f4eb39d3`, and every figure added in round 2 was re-derived from the published run artifacts.

## What was examined

**Context, in this order:**
1. AGENTS.md, and CONTRIBUTING.md section 6 (wording and privacy).
2. docs/README.md.
3. The #629 body and the [A10] lane B7 assignment (issuecomment-5969106115).
4. The round-2 assignment (issuecomment-5970119417).
5. The [A519] REVIEW READY comments (5969917459 and 5970215328).
6. The design's "Switching sources" (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1035-1052`) and `docs/design/TIME_SYNC.md:385`.
7. `git diff bbf704ecc..f4eb39d3` and `4eee41a5..f4eb39d3` (`receipts/round2.diff`).
8. Issue #645.
9. PR #634's check rollup.

**Evidence:**
- Branch `629-b7-review-evidence`, fetched into a disposable repository. It holds `95448218` (first publication), `d36de704` (the masking commit, the page's pin) and the tip `2d0dc7e3` (the round-2 author packet `author-r2/`).
- The two round-1 review archives on that branch were not opened.
- The prior public review findings (R450-1 5970108899, R451-1 5970092043) were read only after the independent pass below.

## Independent checks of the round-2 claims

| Round-2 claim (page line) | Check | Result |
|---|---|---|
| A0 started 14:41:42, window 14:42:08 to 14:52:39; A1 started 14:52:53 (:760-762) | `runs/*/events.jsonl` start, window-start and window-end events (`scripts/run_times.py`, `receipts/run_times.txt`): A0 14:41:42.33 / 14:42:08.90 / 14:52:39.33; A1 14:52:53.15 | Holds. 14:50 falls inside A0's window |
| The 14:50 record is the packet's `HANDOFF.md` "Grading criteria"; the change table and :780-786 list what it fixed | `author/HANDOFF.md:66-79` read against the page's change table and paragraph | Holds. A0's beyond-2-ppm rule, the beat attribution, the B-AAF bench row, A1/A2, B0 and B-CRF all match the record |
| `b7_tables.py` applies these thresholds unchanged from the record (:786-787) | `tools/b7_tables.py:53-95` (2 ppm, 0.01 dB, 0.001 ppm, 0.5 ppm, interval holds zero, 15 s, CLOCK_DOMAIN marks 0 and 2, `SLIP_TDM`, meter restarts) | Holds |
| Bench-host file times (14:37, 14:55, 14:58, 15:40) | The packet does not carry them, and the page says so (:764-765). `author-r2/HANDOFF.md:21` gives the same stamps | Disclosed as not verifiable. Accepted as stated |
| A0's threshold basis is independent of A0's data; A0 shows the mismatch whatever the threshold (:792-800) | B6's +6.52 ppm and 10.6 ppm beat are in the base page's lane B6 Direction A. A0: 630 - 444 = 186 blocks off the floor; 470 + 291 = 761 listener events | Holds |
| Drift 0.54 to 0.93 frames/s; conservative count A2 3 in 2 clusters, B-AAF 3 in 3 (:1065-1073) | `scripts/check_figures.py` on `summary/<case>/grade.json` and `summary/checks/absorb.jsonl`: deficits 0.838, 0.543, 0.650, 0.826, 0.929 and 0.765; frames off A2 [-2, -1], B-AAF [-1, -1, -1] | Holds |
| B0: GET_COUNTERS on CLOCK_DOMAIN 0 at `window-mark-1`, 15:20:58, timed out after 1 s and was not retried; the next mark (15:25:57) answered 3/2; the only non-SUCCESS of 336 DUT AECP commands in eight runs (:938-945) | `scripts/check_dut_aecp.py` on every `runs/*/ctl.jsonl`: TIMEOUT `counters-dut-36-0`, tx 15:20:58.365, rx-tx 1.001 s, no retry; 336 DUT results, 335 SUCCESS; `window-mark-2` at 15:25:57.9 with CLOCK_DOMAIN payload LOCKED 3 / UNLOCKED 2 | Holds, **except** "the mark's next command, GET_COUNTERS on STREAM_INPUT 0". The next command is `counters-dut-6-0`, descriptor type 0x0006, which is STREAM_OUTPUT 0 (F3) |
| Simulation row: 21 executed contexts SUCCESS, "Physical gPTP (nightly and manual)" skipped (:1123) | `receipts/pr634_checks.txt`: head `2bc5adc0`, 21 SUCCESS, 1 SKIPPED (that context) | Holds |
| `SLIP_LB` 386 to 388 after lock, 6 dups between the set and the window, 2 across the lock loss; #645 (:714, :974-986, :1120) | `scripts/slip_lb_reads.py` on `runs/baaf/dut-*.txt` (0x8D4 word): 380 before the bind, 386 at window-0 (1 s in), 388 from window-1 (31 s in) to window-20, 390 after the lock loss. The B-AAF grade's `servo_window` gives [386, 388]. #645 is open, and its acceptance covers the INTERNAL-to-AAF and AAF-to-CRF switches | Holds (see S2 on the interval wording) |
| Packet location, path mapping, and the source of every hash row (:1154-1211) | `scripts/check_page_hashes.py`, run at `d36de704` and at the tip `2d0dc7e3`. Results: 19 raw rows equal their `events.jsonl` raw-file record and `RAW-ARTIFACTS.json`; 7 grade-full rows appear only in `RAW-ARTIFACTS.json`; 17 evidence rows equal the published bytes, SHA-256 and `MANIFEST.json` `published_sha256`; the 2 masked tools equal `redaction.json` `original_sha256`, and their published hash differs | 45 rows, 0 problems at both commits. Three planted mutants (a grade-full hash, a byte count, a masked tool's retained hash in place of its original) are each caught (`receipts/checker_mutants.txt`) |
| `d36de704` masked the channel count and format "in the docstrings of four tools ... the redaction pass had masked that value in their code but not there" (:1202-1206) | `receipts/d36de704_hunks.txt` and `scripts/privacy_scan.py` | Does not hold (F2) |
| R450-1 R1 and R2 applied (:845-846, :716) | Page text and PR body | Holds |
| No case verdict changed | `receipts/round2.diff`: every Result and Verdict cell of the case rows is unchanged; only evidence and judgement text was added | Holds |

**Docs gates at this head** (`receipts/gates/rc.txt`), all rc 0 in the pinned Markdown environment (requirements hash `40cdefe08ebd`):
- `docs_check.py` (0 findings, scrub self-test 23/23), `check_doc_style.py`, `check_doc_paths.py`;
- `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base bbf704ec`;
- `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`;
- `git diff --check bbf704ec f4eb39d3`.

The three Markdown gates first returned rc 2 under the system interpreter, which lacks the pinned renderer. They were then re-run in the pinned environment with rc 0. Both runs are recorded.

**Hosted contexts at the exact head** (`receipts/pr644_head_checkruns.tsv`, head_sha `f4eb39d3`):
- Executed, SUCCESS: `rtl-fast`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `elaborate`, `changes` and `full-ci-gate`.
- SKIPPED, not executed: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, both shard templates and "Physical gPTP (nightly and manual)".

## Findings

**F1 - MINOR - lens: Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1163`, and the evidence at `d36de704` and `2d0dc7e3`: the external capture's channel count and sample format, which the evidence's redaction masks as private, are still public.**
- **Authority and evidence.** The privacy rule of this lane bars capture format and channel map from the page, the PR body and the evidence. R450-1 F6 classed this value as private, and `d36de704` masked it as `<capture-channels>` and `<capture-format>`. `scripts/privacy_scan.py` recovers the two values from `d36de704`'s own diff and counts them without printing them (`receipts/privacy_scan.txt`):
  - the page at this head names the sample format at :1163 (the B7 hash table's `a0/cap-lr.raw` row);
  - the pinned evidence at `d36de704`, and the tip, still carry the channel count as the raw-file name `cap-all-<N>ch.raw`. It appears in 19 files, 25 times: `RAW-ARTIFACTS.json` (7 rows), all 7 `runs/*/events.jsonl` and all 7 `runs/*-lock.txt`, and the code of the four tools that `d36de704` edited (`run_b7.py:191`, `run_b6.py:150`, `grade_b7.py:99`, `grade_b6.py:75`).
  - The same format token is at :596, in lane B6's section, which dev already carries. That line is outside this diff.
- **Impact.** An instrument-identifying detail stays public on the page this PR adds and in the evidence it pins, after a round whose stated purpose included masking it. The PR body is clean (0 matches).
- **Required outcome.**
  - :1163 no longer names the sample format; for example, "the tone's two channels" alone.
  - The manager's evidence publication masks the channel count wherever it remains, the file-name form included, or a maintainer rules publicly that these two values are not private.
  - The handling of the already-public commit `95448218` is stated under the publication policy (R450-1 F6's second outcome).
  - Lane B6's :596 is either fixed with the manager's approval or given a public Issue.
- **Verification.** `scripts/privacy_scan.py` reports 0 matches for the page at the new head and for the republished evidence commit.

**F2 - MINOR - lens: Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1202-1206`: the page misstates what `d36de704` masked.**
- **Authority and evidence.** The page says `d36de704` masked the channel count and format "in the docstrings of four tools" and that "the redaction pass had masked that value in their code but not there". `receipts/d36de704_hunks.txt` shows otherwise:
  - `d36de704` also changed code: the capture command's format argument at `run_b6.py:457` and `run_b7.py:516`. So the first redaction pass had not masked the format in code.
  - The channel count is still in the code of all four tools (F1).
  - Only the channel-count assignment line (`NCH, ...`) was masked in code by the first pass.
- **Impact.** A cold reader is told that the published code carries no capture value, and it does. This is a statement about the redaction state, so it touches the privacy rule and is not wording only.
- **Required outcome.** The paragraph matches the evidence actually pinned after F1 is handled: which values, which files, docstring or code, and which commit masked each.
- **Verification.** The paragraph is read against `git diff d36de704^ d36de704` (or the republication commit) and a `scripts/privacy_scan.py` run.

**F3 - MINOR - lenses: Conformance, Robustness, Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:941-942`: the DUT command said to answer right after the B0 timeout is misidentified.**
- **Authority and evidence.** The page says the DUT "answered the mark's next command, GET_COUNTERS on STREAM_INPUT 0, at once". Three sources show otherwise:
  - In `runs/b0/ctl.jsonl`, the command after the TIMEOUT (`counters-dut-36-0`, seq 22912) is seq 22913, `counters-dut-6-0`, and its payload begins with descriptor type `0006`.
  - `tools/run_b7.py` builds every mark's items as `CTR_A = [("dut", 0x0024, 0), ("dut", 0x0006, 0), ...]`.
  - `tools/b7_ctl.py:46` defines `STREAM_INPUT, STREAM_OUTPUT = 0x0005, 0x0006`. IEEE 1722.1 assigns 0x0006 to STREAM_OUTPUT.
  - The next command was therefore GET_COUNTERS on the DUT's STREAM_OUTPUT 0. The mark's first DUT STREAM_INPUT 0 read is seq 22916, the fourth command after the timeout.
- **Impact.** The one record of the DUT's recovery after its only unanswered AECP command misreads a descriptor-type field. It also names a different object from the one that answered. The conclusion that the DUT answered at once still holds.
- **Required outcome.** The sentence names the command and target the log records: GET_COUNTERS on STREAM_OUTPUT 0 (seq 22913).
- **Verification.** Read the sentence against `runs/b0/ctl.jsonl` for seq 22912 to 22917 (`receipts/check_dut_aecp.txt`).

**RESIDUE-1 - lens: Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:980-982`.**
- The 32,768-tick bound is cited to "Switching sources", which does not state it. The bound is `docs/design/TIME_SYNC.md:385`, the clock-source settle row. The claim itself is true.
- Exact fix: after the Switching sources link, add "; the bound is [TIME_SYNC](../design/TIME_SYNC.md)'s clock-source settle row".

**RESIDUE-2 (R451-1 RESIDUE-2, retained) - lens: Docs - the packet's `author/HANDOFF.md:31` and `author-r2/HANDOFF.md:50`, and the round-1 REVIEW READY comment.**
- They say "all 12 live AECP descriptors". `identity/identity-verdict.txt` grades 11, plus the CLOCK_SOURCE 3 absence check. The page and the PR body are correct.
- Exact fix: "11 live AECP descriptors byte-equal, plus the CLOCK_SOURCE 3 absence check", in the next packet handoff.

**S1 - SUGGESTION - Tests, Docs - :758-759.** The page cites "the packet's `HANDOFF.md`, 'Grading criteria'" for the 14:50 record. Under the published mapping that is `author/HANDOFF.md:66`, whose heading still reads "fixed 14:50 CEST, before any case ran". The as-run `grade_b7.py` docstring says "each fixed before any graded case" too. Point instead to `author-r2/HANDOFF.md:85`, which carries the corrected heading, and note that those two as-run texts are superseded.

**S2 - SUGGESTION - Robustness, Docs - :714, :977, :1120.** "6 between the set and the window" is bracketed by the read before the bind (380) and the window's first read, 1 s into the window (386). So the interval also spans the bind, about 0.4 s before the set, and the window's first second. State the bracket as the 2-dup slip's is stated.

**S3 - SUGGESTION - Robustness, Docs - :938-945.** Add that no B0 criterion used mark 1. B0 is graded on the counted ratio alone, and B-AAF's CLOCK_DOMAIN check reads marks 0 and 2 (`tools/b7_tables.py:84`).

## Prior public findings at this head

| Item | Status at `f4eb39d3` | Evidence |
|---|---|---|
| R451-1 F1 = R450-1 F2 (grading order) | Resolved | :758-800 and the PR body give the true order, with times that equal `runs/a0/events.jsonl` and `runs/a1/events.jsonl`. The `tone.repeats` fix is placed after A0's first grade. A0's basis and #629's wording are stated. S1 is optional |
| R451-1 F2 (where the evidence lives) | Resolved | Branch, pin `d36de704`, path mapping and `MANIFEST.json` fields are on the page and in the PR body. `check_page_hashes.py` gives 45 of 45 at `d36de704` and at the tip |
| R451-1 RESIDUE-1 = R450-1 F4 (skipped context) | Resolved | :1123 against `receipts/pr634_checks.txt` |
| R451-1 RESIDUE-2 (12 vs 11) | Retained as RESIDUE-2 | The comment was not edited, as the assignment requires. The packet handoffs still say 12. The page and PR body are correct |
| R451-1 S1, S2 | Not taken (optional) | - |
| R451-1 S3 | Resolved by #645 | #645 is open, scoped to the slip, with a bench-repeat acceptance |
| R450-1 F1 (figures) | Resolved | `receipts/check_figures.txt` |
| R450-1 F3 (B0 timeout) | Resolved as asked: case, mark, command, target, no retry, next mark, cause not analysed | `receipts/check_dut_aecp.txt`. The added sentence carries a new error, F3 |
| R450-1 F5 (fabric row) | Resolved | :714, :974-986, :1120 and :1128-1131. `SLIP_LB` values in `receipts/slip_lb_reads.txt`. #645 |
| R450-1 F6 (capture value in the evidence) | Retained in part | Docstrings masked at `d36de704`. The channel count remains in the evidence's file names and tool code, the page names the format, and the handling of `95448218` is not stated publicly (F1). The page's description of the masking is inaccurate (F2) |
| R450-1 R1, R2 | Resolved, applied exactly | :845-846; :716 and the PR body's lock-loss row |
| R450-1 S1, S2 | Not taken (optional) | - |
| R450-1 S3 (peer descriptor indices in the packet) | Open, optional, for the manager's privacy pass | Unchanged in the packet |

## Reviewer ledger (R451-2)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | #629 acceptance table :1116-1131 against #629's items and #645. Fabric item against "a source switch re-locks without an undeclared discontinuity", the design's Switching sources (:1044-1052) and `TIME_SYNC.md:385`. Descriptor types in `runs/b0/ctl.jsonl` against IEEE 1722.1's descriptor-type values (F3). `Refs #629` in the PR body | R451-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| RTL | CLEAN | No HDL in `git diff --stat bbf704ecc..f4eb39d3`. The round-2 register claims were decoded from the raw dumps: `SLIP_LB` 0x8D4 [15:0] from `runs/baaf/dut-*.txt` (`receipts/slip_lb_reads.txt`), and the CLOCK_DOMAIN GET_COUNTERS payloads. The design's recentre declaration was checked against :980-986 | R451-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| Robustness | UNCLEAN (F3) | The B0 timeout: every DUT AECP result in the eight `runs/*/ctl.jsonl` (`receipts/check_dut_aecp.txt`), its retry behaviour and the following marks. The B-AAF ring slip and its #645 home. The conservative reading of the five off-signature clusters (`receipts/check_figures.txt`) | R451-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| Tests | CLEAN (S1 optional) | Grading order against `runs/*/events.jsonl` (`receipts/run_times.txt`) and the 14:50 record (`author/HANDOFF.md:66-79`). `tools/b7_tables.py:53-95` thresholds against the record. `summary/verdicts.json` unchanged in the diff. PR #634's executed and skipped contexts. PR #644's exact-head hosted contexts. Hash checker, with 3 mutants killed | R451-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |
| Docs | UNCLEAN (F1, F2, F3) | The round-2 diff of the B7 section (:691-1233) and the PR body. Docs gates rc 0 in the pinned environment (`receipts/gates/`). 45 hash rows at `d36de704` and `2d0dc7e3`. The packet pointer and mapping. Value-blind privacy scan of the page, the PR body and three evidence commits (`receipts/privacy_scan.txt`). The `d36de704` hunks | R451-2 | f4eb39d3fddbbd9e2de1947750cc1b482baff53d |

RTL and Tests are banked against `f4eb39d3`. Whether a fixing commit un-covers them is judged at that head. Conformance, Robustness and Docs need a re-review at the fixing head.

## Real limits

- The raw captures and the `grade-full.json` files are not published. So the 19 raw rows and 7 grade-full rows were checked against their records (`events.jsonl`, `RAW-ARTIFACTS.json`), not against bytes.
- The bench-host file times (14:37, 14:55, 14:58, 15:40) are not in the packet and could not be checked. The page discloses this.
- No audio was re-decoded, and no tool was re-run against raw data. This round's re-derivations start from the published grades and summaries, the console dumps and the controller logs.
- Physical calibration is NOT RUN, no hardware was touched, and skipped hosted contexts are not hardware proof.
- Where timings are quoted, they are bounded by 0.5 s console polls.

## Pending manager duties

- F1: republish the evidence with the channel count masked wherever it remains, or record a ruling that the value is public. State how `95448218` is handled. Decide lane B6's :596.
- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Hosted and act acceptance at the exact head. The Verilator/Yosys contexts at `f4eb39d3` were skipped by the docs-only scope, not executed.
- The final current-dev candidate at the merge turn (source base `bbf704ec`, live dev `bbf704ec`) is distinct from this source review.
- A positive external review at a later head. This round is NEGATIVE.

## Receipts

All paths are relative to this packet, and every file is listed in `MANIFEST.sha256`.

**Scripts:**
- `scripts/run_times.py`
- `scripts/check_page_hashes.py`
- `scripts/check_figures.py`
- `scripts/check_dut_aecp.py`
- `scripts/slip_lb_reads.py`
- `scripts/privacy_scan.py` (it prints counts and hashes, never the values)

**Raw receipts** under `receipts/`:
- `round2.diff`
- `run_times.txt`
- `check_page_hashes-d36de704.txt`, `check_page_hashes-2d0dc7e3.txt` and `checker_mutants.txt`
- `check_figures.txt`
- `check_dut_aecp.txt`
- `slip_lb_reads.txt` and `slip_lb_baaf.txt`
- `pr634_checks.txt` and `pr644_head_checkruns.tsv`
- `privacy_scan.txt` and `d36de704_hunks.txt`
- `gates/`
- `clone_integrity.txt`

**Clone state:** the clone is restored at the exact head.
- 994 of 994 tracked non-gitlink blobs and modes equal the index, and the index equals the HEAD tree (`write-tree` `a9e72632...`).
- Gitlinks: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `631eeb34`, verilog-axis `48ff7a7e`.
- The gate runs left an interpreter byte-code cache, which was removed. Afterwards `git status --porcelain --ignored` is empty.

R451-2 FINISHED
