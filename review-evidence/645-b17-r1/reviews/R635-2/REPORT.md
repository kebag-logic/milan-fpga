[R635] POSITIVE - exact head b2891a8f29598fff1865f855991ad4c1505e35a3

# R635-2: external review of PR #741 (issue #645, bench lane B17), round 2

- Exact head `b2891a8f29598fff1865f855991ad4c1505e35a3`, tree `bf503993f9c6375a32d8652e810168883a4e3316`.
- Source base and live dev: `f62602531d415d6c1cae1374a3cc2938faf54049`.
- Previously reviewed head: `56d008f68f445156a9bdd81eb32f8d5353cc7a7f` (R634-1 and R635-1, both NEGATIVE, one MINOR each).
- Scope: a narrow delta review of the one commit `56d008f6..b2891a8f`, under the assignment https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187961942.

## Verdict basis

POSITIVE. All five lenses are covered clean at the exact head. No BLOCKER, MAJOR or MINOR is open.

- **Both round-1 MINORs are resolved at their cause** (R634-1-F1 and R635-1-F1).
- **Every after-slip figure names its window**, either the last poll or the capture's end. The 32 s hold is stated to give the same ranges, which is true.
- **Every figure I recomputed from the raw counter logs and the published tap data matches.**
  - I recomputed every poll figure on the page for all ten cycles, and every burst and peak figure in each window.
- **The tool's windows are explicit**, and the page states the cumulative-counter basis for "slipped nothing", with end baseline 228.

Open items: one RESIDUE (wording only) and three SUGGESTIONs, all listed under Findings.

## What the delta is

`git diff 56d008f68..b2891a8f` changes one file, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, by +98 and -29 lines (`receipts/delta_56d008f6_b2891a8f.diff`).

- All 11 hunks fall at lines 4645 to 4977, inside the section `## Dev 5603c353, 2026-10-15: lane B17`. That section starts at :4612 and is the page's last section.
- The whole PR, `f6260253..b2891a8f`, is that same single file, +370 lines (`receipts/full_f6260253_b2891a8f.diff`).
- The submodule gitlinks `external`, `gptp-processor` and `protocol-processor` are identical at the base and the head.
- No RTL, firmware, test, script or generated artifact changed. **Nothing outside the B17 section changed.**

## Checks against the assignment

**1. Every after-slip figure is bounded and says which window.**
- The priming table (:4885-4896) now carries a Window column.
  - Two rows are "To the last poll": bursts after the slip, 8 to 18, and the largest lateness after the slip, 27.1 to 30.1 us.
  - Two rows are "To the capture's end": 10 to 23, and 27.6 to 30.3 us.
  - The per-cycle burst count is given both ways: 9 to 19 to the last poll and 11 to 24 to the capture's end.
- The prose at :4898-4907 is bounded the same way: 8 to 18 bursts, up to 30.1 us, to the last poll, and 2 to 7 further bursts to the capture's end.
- `### B17: method` (:4757-4764) defines "to the last poll" as bursts that start no later than the end of the last poll. That poll ends +31.75 to +31.93 s after the bind. The section also says the 32 s hold gives the same ranges.
- The PR body's "Bind priming" bullet carries the same windows (`receipts/pr-body-live.md`, line 30).

**2. Burst counts and peak lateness, recomputed within each window from the recorded data.**
- Script: `scripts/recompute_bursts.py`. Receipt: `receipts/recompute-bursts.jsonl`.
- Method:
  - Source: the published per-cycle `summary/cNN.json` `tap.late_pdus`. It lists every post-bind peer PDU more than 10 us late. The smallest listed value is 10.001 to 10.478 us.
  - Bursts: PDUs over 20 us, grouped by gap.
  - Windows: bounded by my own raw last-poll end from `poll.jsonl`, by 32.0 s, and by the capture's end.
- Results with a 1 ms grouping gap:

| Quantity | Window | Recomputed | Page |
|---|---|---|---|
| Bursts per cycle | To the last poll | 9 to 19 | 9 to 19 |
| Bursts per cycle | To the capture's end | 11 to 24 | 11 to 24 |
| Bursts after the slip | To the last poll | 8 to 18 | 8 to 18 |
| Largest lateness after the slip | To the last poll | 27.092 to 30.071 us | 27.1 to 30.1 us |
| Bursts after the slip | To the capture's end | 10 to 23 | 10 to 23 |
| Largest lateness after the slip | To the capture's end | 27.575 to 30.260 us | 27.6 to 30.3 us |
| Largest lateness in the slip's interval | The slip's interval | 24.565 to 29.309 us | 24.6 to 29.3 us |
| Further bursts per cycle, last poll to capture's end | n/a | 2 to 7 | 2 to 7 |
| A later burst larger than the slipping one, to the last poll | n/a | 9 of 10 (not c01) | 9 of 10 |
| PDUs per burst | n/a | 3 to 12 | 3 to 12 |
| PDUs over 10 us late between the bind and the slip's interval | n/a | 0 in all ten | none |
| First burst over 20 us inside the slip's interval | n/a | all ten | all ten |

- **The 32 s hold window gives the same ranges.**
  - Per cycle, c01 and c03 each have one more burst between the last poll's end and 32 s. That does not change any range (see S3).
- **The grouping gap matters only to the capture-end counts.**
  - Gaps of 0.5 ms and 5 ms leave every last-poll figure unchanged.
  - At 0.5 ms, the capture-end counts move to 12 to 24 and 11 to 23.
  - At 5 ms they move to 11 to 23 and 10 to 22.
  - The page uses the tool's 1 ms, so its figures are consistent with its stated rule.
- **Clock domains.**
  - Burst times are on the tap's clock, from the bind command seen on the tap. The poll windows are on the host's clock, from the bind command's local instant.
  - The two agree within 0.1 ms on the unbind-to-bind interval.
  - No burst starts within 35 ms of any window edge.

**3. "Slipped nothing" states its basis.**
- The page states it at :4757-4764 and :4815-4817, and again at :4903-4904.
- Verified from the raw logs (`receipts/recompute-polls.jsonl`, `continuity_ok`):
  - c01's first `SLIP_LB` read is 208. That equals the start baseline `restore/dut-start.txt`, `0x900008d4` = `d0 00 00 00`.
  - Each later cycle's first read equals the previous cycle's last, in all nine joins.
  - c10's last read is 228. That equals the end baseline `restore/dut-end.txt`, `e4 00 00 00`. It was read at 07:57:46Z, after c10's capture ended at 07:56:07Z.
  - The skip half reads 0 throughout. `SLIP_TDM` reads 0 throughout.
- The register map says the word is never cleared and saturates only at `0xFFFF` (`docs/reference/REGISTER_MAP.md:210`, `:1878`). So equal reads at each join exclude any dup in between, and the basis is sound.

**4. The `RENDER_STAT` wording gives the bracket and the convergence start (:4821-4829).**
- Recomputed from the raw logs:
  - Prefill first read 0 by the end of a poll at +0.1227 to +0.6535 s, printed 0.12 to 0.65.
  - That poll was the first after the bind in c02, c04, c05, c07 and c08.
  - The c05 bracket is first PDU 7.854 ms to poll end 0.1376 s, printed 0.008 to 0.138.
  - Converged read 1 from the same poll in six cycles, and one poll later in c02, c04, c05 and c07, by 0.6368 to 0.6679 s, printed 0.64 to 0.67.
  - Fill read 8 to 14, and both bits held to the last poll. Rails read 11.
- All of these match the page. One sentence carries a misleading contrast; see RES-1.

**5. Every printed figure is rounded once from the raw value.**
- Script: `scripts/recompute_polls.py`. Receipt: `receipts/recompute-polls.jsonl`. It uses raw `t0`/`t1` against `bind-time.t_bind_local`.
- The c09 last poll is +31.784840, printed +31.78.
- The c08 slip's lower edge is +1.174981, printed 1.17. Round 1 printed 1.18.
- Every other table cell matches its once-rounded raw value:
  - poll coverage: first poll -8.0109 to -7.9925 s, last poll +31.7507 to +31.9268 s;
  - all ten slip intervals;
  - the polls left after the slip, 26.133 to 31.194 s, printed 26.1 to 31.2;
  - the long polls, 0.266 to 0.426 s against at most 0.138 s, starting 1.523 to 1.636 s after the unbind and 1.545 to 1.676 s after the bind;
  - the five slip intervals that contain the long poll: c02, c03, c07, c08 and c09.
- The bind UTC instants are truncated. They agree with truncation in all ten cycles.
- `summary/figures.json` lists 27 tap figures printed from the grade's 3-decimal values, each `tie: false`. For example, 24.565 printed to 1 decimal is not a tie.
- I re-ran the author's `tools/check_b17_page.py` against the page at this head and the live PR body: 84 checks, `mismatches: 0`, rc 0 (`receipts/check-page-rerun.txt`).

**6. The summary tool's windows are explicit.**
- The published `tools/summ_b17.py` matches the page's hash row: 20,088 B, `bbd9d87e…`.
- It defines `windows = dict(last_poll=last_s, hold=hold_s, capture=inf)`. Its docstring names each window and the cumulative-counter check.
- `summary/cycles.json` carries `windows`, `counter_continuity` (start 208, end 228, `joins_equal`) and the after-slip figures for each window per slip.

**Other delta claims checked.**
- The RTL citation is correct. `hdl/milan/milan_datapath.sv:6810-6812` at `f6260253`/HEAD is the `render_status_w` assignment, and at `5603c353` the same assignment is at `:6797-6799`.
- The c08 capture figures are correct:
  - 814,991 frames, against 774,651 to 776,308 for the other nine, so +38,683 to +40,340.
  - The peer AAF holds 390,321 PDUs, against about 351,636 elsewhere, so the extra frames are almost all the peer's stream.
  - The peer stream ran on for 4.8747 s after the unbind and stopped 1.1380 s before the bind, against 0.0230 to 0.1756 s in the other nine.
  - Only three streams appear in any capture.
  - The c08 unbind status is 0.
  - Between the unbind and the bind every c08 poll read prefill 1, fill 0 and `SLIP_LB` 222.
- The delta_ppm resolution claim is correct:
  - The largest |delta| is 0.0017, in c04, which gives 12,255 s.
  - With the 0.0001 resolution added it is 0.0018, which gives 11,574 s.
  - Against a bound window of about 34 s that is below 0.003 slips.
  - The stream rates are 4.9928 to 5.0161 ppm, printed +4.99 to +5.02.
- All 14 rows of the artifact-hash table match the published round-2 packet in size and SHA-256 (`receipts/evidence-verify.txt`).
- The round-1 publication locator is correct. `35cc1ae4` contains `review-evidence/645-b17-r1/author` and is an ancestor of `refs/heads/645-b17-review-evidence`, which is `5b67fa6b`.

**Evidence integrity.**
- `author-r2/MANIFEST.sha256` verifies 111 of 113 entries (`receipts/evidence-verify.txt`). The two exceptions are both accounted for:
  - `identity-resume/identity-verdict.json` differs. The top-level `MANIFEST.json` records it as `path_redacted: true` at publication (original `bc704fb3…`, published `64fae695…`).
  - A `__pycache__` entry was not published.
- `summary/counter-logs.sha256` verifies all ten raw `poll.jsonl`, and its own hash is `a1d41530…`, as the page states.

## Prior public review findings at this head

Read only after my independent pass. All of them are resolved at their cause.

| Prior finding | Status at `b2891a8f` | Evidence |
|---|---|---|
| R634-1-F1 MINOR (after-slip windows; slipped-nothing basis; `RENDER_STAT` bracket; c09 +31.78; PR body) | Resolved | Checks 1 to 5 above; `receipts/recompute-bursts.jsonl`, `receipts/recompute-polls.jsonl`, `receipts/pr-body-live.md` |
| R634-1-F2 RESIDUE (RTL citation) | Resolved | :4716-4717; RTL line check above |
| R634-1-F3 RESIDUE ("because" changed to "as expected with") | Resolved | :4904-4905 |
| R634-1-F4 SUGGESTION (packet locator) | Taken | :4645-4649 |
| R635-1-F1 MINOR (double rounding, c08 and c09) | Resolved | Check 5; `receipts/check-page-rerun.txt`; mutants 1 and 2 in `receipts/mutation-page-check.txt` |
| R635-1-RES-1 (converged one poll later) | Resolved | :4827-4829 |
| R635-1-RES-2 (citation) | Resolved | :4716-4717 |
| R635-1-S1 (long polls) | Taken, figures verified | :4831-4839 |
| R635-1-S2 (c08 extra traffic) | Taken, figures verified | :4841-4848 |
| R635-1-S3 (delta_ppm resolution) | Taken, verified | :4751-4753, :4869-4870 |
| R635-1-S4 (published packet) | Taken | :4645-4649 |

## Findings

### R635-2-RES-1: RESIDUE, Docs: the prefill lower bound reads as special to five cycles

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4824-4827`: "In c02, c04, c05, c07 and c08 that poll was the first after the bind, so only the first peer PDU bounds the exit from below".
- **Evidence:**
  - The tool computes the lower bound as the later of two instants: the start of the last poll that read prefill 1, and the first peer PDU.
  - In all ten cycles that poll started before the first peer PDU. The author's own `summary/cycles.json` has `render.lower_bound_is_first_pdu: true` for every cycle.
  - So the first peer PDU is the lower bound everywhere, not only in the five cycles listed.
  - The sentence is literally true of those five, but the contrast implies a tighter poll-based bound in the other five that does not exist.
  - The general sentence just before it is correct: the exit lies between the first peer PDU, 7.9 to 163.5 ms, and the end of that poll.
  - No figure, bracket value or claim changes.
- **Exact fix:** replace "In c02, c04, c05, c07 and c08 that poll was the first after the bind, so only the first peer PDU bounds the exit from below; in c05 the bracket is 0.008 to 0.138 s." with "In every cycle the poll before it started before the first peer PDU, so the first peer PDU is the lower bound; in c02, c04, c05, c07 and c08 that poll was the first after the bind, and in c05 the bracket is 0.008 to 0.138 s."
- **Verification:** the reworded sentence agrees with `render.lower_bound_is_first_pdu` for all ten cycles in `summary/cycles.json`.

### R635-2-S1: SUGGESTION, Tests and Docs: the page check matches prose figures by presence

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4753-4755` ("compares this section with the summary"), and `tools/check_b17_page.py` check 3.
- **Evidence:** I ran 10 disposable single-edit mutants on a copy of the page (`scripts/mutate_page.sh`, `receipts/mutation-page-check.txt`).
  - Caught: the c09 and c08 cells, the two priming-table cells, "by 0.64 to 0.67 s" and "took 0.27 to 0.43 s".
  - Not caught, each with rc 0 because the same number still appears elsewhere in the section:
    - "+31.75 to +31.93" changed to "+31.94";
    - "the end baseline, 228" changed to "229";
    - "The 2 to 7" changed to "The 2 to 8";
    - "up to 30.1 us" changed to "up to 30.2".
  - Every such prose figure is correct at this head; I recomputed each one independently.
- **Optional:** match each prose figure in its phrase, or describe check 3 as checking that each figure is present.

### R635-2-S2: SUGGESTION, Docs: point at the published round-2 packet

- **Where:** :4647-4649, "The second round's tools and summary … are in the packet the manager holds."
- **Evidence:** they are now public at `review-evidence/645-b17-r1/author-r2` on `645-b17-review-evidence`, commit `5b67fa6b`, published after this head. The page's hash rows match that tree.
- **Optional:** the manager decides when to link it.

### R635-2-S3: SUGGESTION, Docs: "the 32 s hold gives the same ranges"

- **Where:** :4759-4760, and the PR body's bullet.
- **Evidence:** the statement is true of the ranges. Per cycle, c01 and c03 each have one more burst between the last poll's end and 32 s. Their counts to the last poll are 14 and 13, against 15 and 14 to the hold.
- **Optional:** add "(per cycle, one more burst in c01 and c03)" if per-cycle readers matter.

## Lens results

| Lens | Result | path:line or artifact | What was checked and against what |
|---|---|---|---|
| Conformance | PASS | issue #645 assignment comment 6187961942, items 1 to 3; `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4745-4907`; `receipts/pr-body-live.md` | Each assignment item was met (checks 1 to 6), and both round-1 MINORs and all RESIDUE and SUGGESTION items were taken. No class, count, verdict or slip time changed. The classification (all (c)) and the #645-stays-open conclusion are unchanged. The register-map semantics cited for the counter basis are `REGISTER_MAP.md:1878` and `:2039-2045`. |
| RTL | PASS | `hdl/milan/milan_datapath.sv:6810-6812` at HEAD and `:6797-6799` at `5603c353`; `receipts/full_f6260253_b2891a8f.diff` | The delta touches no RTL. The only RTL-dependent statement, the line citation, was verified at both revisions. The `RENDER_STAT` bit decode used in my recompute matches `REGISTER_MAP.md:2039-2045`. |
| Robustness | PASS | `receipts/recompute-bursts.jsonl` (grouping gaps 0.5, 1 and 5 ms; `near_boundary_50ms`); `receipts/recompute-polls.jsonl` (continuity, long polls); c08 between-bind polls (checked in this review, see "Other delta claims checked") | Window-edge margins (at least 35 ms) and the tap/host clock alignment were checked. Grouping-gap sensitivity is confined to the capture-end counts. The counter-continuity basis was checked for monotonicity and saturation. The c08 anomaly and the long polls are bounded, and they do not affect the slip intervals. |
| Tests | PASS | `tools/check_b17_page.py` re-run: `receipts/check-page-rerun.txt` (84 checks, 0 mismatches); `receipts/mutation-page-check.txt`; `scripts/recompute_polls.py` and `scripts/recompute_bursts.py` | The checker fails on the two round-1 defects and on table cells. Its prose-presence weakness is S1, and all prose figures were independently recomputed correct. |
| Docs | PASS | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4612-4977`; gate receipts `receipts/gate-*.log` and `.rc` | All docs gates return rc 0: docs_check, doc_style, toc --check, verify-anchors, em_dash --base f6260253 (370 added lines), doc_paths and diff --check. The artifact-hash table matches the published packet. RES-1 is wording only. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6187961942; findings page B17 section; PR body (live); `summary/cycles.json` classification | R635-2 | `b2891a8f29598fff1865f855991ad4c1505e35a3` |
| RTL | CLEAN | full PR diff (docs only, gitlinks unchanged); `hdl/milan/milan_datapath.sv:6810-6812`, and `:6797-6799` at `5603c353`; `REGISTER_MAP.md` `RENDER_STAT`/`SLIP_LB` | R635-2 | `b2891a8f29598fff1865f855991ad4c1505e35a3` |
| Robustness | CLEAN | raw `cycles/cNN/poll.jsonl` and `events.jsonl` (all 10); `summary/cNN.json` `tap.late_pdus`; `restore/dut-{start,end}.txt`; `summary/peer-gap.json` | R635-2 | `b2891a8f29598fff1865f855991ad4c1505e35a3` |
| Tests | CLEAN (S1 optional) | `tools/check_b17_page.py` re-run and 10 mutants; my independent recompute scripts | R635-2 | `b2891a8f29598fff1865f855991ad4c1505e35a3` |
| Docs | CLEAN (RES-1 is RESIDUE; S2 and S3 optional) | page B17 section; docs gates; artifact-hash table against the published packet; PR body | R635-2 | `b2891a8f29598fff1865f855991ad4c1505e35a3` |

## Real limits

- **The raw captures are not published.** Burst and lateness figures were recomputed from the published `tap.late_pdus` lists, which ana_b17 grades from the captures, not from the pcaps. I did not re-grade the captures or re-derive the 20 us fit line. The c08 stream figures come from the published `summary/peer-gap.json`.
- **There is no bench access, and physical calibration was NOT RUN.** Printed precision is not calibrated accuracy. The field skips are not hardware proof.
- **No manager source bank runs at this head, and I neither claim nor infer one.** Source-head execution evidence is the author's published gate receipts (`author-r2/gates/gates-round2.txt`) plus my own docs-gate re-run.
  - Three gates needed the pinned Markdown renderer. I installed it from `tools/markdown/requirements.txt` with `--require-hashes` into a private environment under the scratch directory.
- **Hosted snapshot** at 2026-10-15T09:00:53Z (`receipts/hosted-checks-snapshot.tsv`):
  - 7 success: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `docs-check-no-git`, `full-ci-gate`, `wire-accountability`.
  - `docs-check` was still in progress.
  - 14 skipped, among them `verilator-suites`, `yosys-portability` and the firmware jobs, by path filter on a docs-only PR. Skipped contexts are not executed evidence.
- **Clone integrity:** HEAD and tree are as above, the index and worktree equal HEAD, the gitlinks are unchanged, and the one ignored cache directory created by the gates was removed (`receipts/clone-integrity.txt`).

## Pending manager duties

- Hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- The current-dev merge-candidate validation (builder and native banks) at the merge turn, from source base and live dev `f62602531d415d6c1cae1374a3cc2938faf54049`.
- Carry RES-1 to the residue checklist.
- Decide on S2, the round-2 packet locator.
- Post-merge containment.
- Merge only with explicit maintainer authorization.

## Receipts

Listed in `MANIFEST.sha256`:
- scripts: `scripts/recompute_polls.py`, `scripts/recompute_bursts.py`, `scripts/mutate_page.sh`;
- `receipts/`: the recompute outputs, the page-check re-run, the mutation results, the docs-gate logs and rc files, the live PR body, the hosted snapshot, the evidence verification, the delta and full diffs, and clone integrity.

R635-2 FINISHED
