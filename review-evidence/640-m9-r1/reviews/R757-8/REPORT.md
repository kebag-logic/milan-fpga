[R757] POSITIVE - exact head 20933ef48a9b174e58a9d17ddd59078a072024af

# R757-8 review of issue #640 / PR #828, round 8 delta

Tree `2299420e70cea4ce2dcb0450c5ff0fbb56bbf9f0`. Delta `e7310e94..20933ef4`, documentation only: 2 commits, 3 pages, +45/-7.

Abbreviations: FR = `docs/reference/FR_NFR.md`, SE = `docs/design/MARK_II_STREAM_ENGINES.md`, AP = `docs/design/MARK_II_AREA_PLAN.md`.

## Result

- **No BLOCKER, MAJOR or MINOR is open.** All five lenses are clean at this head.
- **R757-7-F1 is resolved** by its outcome (b), as the manager ruled.
- **Two RESIDUE items** are recorded, each with an exact fix that passed the style and link gates on a disposable copy.
- **The main new fact:** the page's "that row may be low" understates what is known, and gives too narrow a cause. The 192 kHz row is low even without eight-channel streams, and the 96 kHz row is low too. Neither case exceeds 143.347 µs, so no figure on the page is false and open design item 4 already owes the answer. That makes it RESIDUE (R757-8-R1).

## The six assigned checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | NFR-LAT-03 reads as ruled and applies to every case | Holds | FR:306 and SE:230-243. Target: "SHOULD be below 65 µs". Every case is measured and reported; above 65 µs is "reported, not failed". Grading applies only where a bound is derived, the 16-reservation table, and a measurement above it is a finding. With fewer reservations no maximum is derived, and 143.347 µs is "quoted as reached, not as a limit". Both classes get a defined outcome: 16 reservations is reported and graded; fewer is reported only |
| 2 | Each reached case and witness reproduces; none is called a maximum | Holds | `receipts/probe_r8.out`. Each row's starts and stops replayed as the page words them, through my own phase rule and credit simulation and through the published model's `greedy_add`, `lindley_wait` and `cbs_sim`. All four give the page's wait and total to three decimals, with at most 16 running streams. SE:438-439 says no row is a maximum |
| 3 | Open design item 4 is verifiable | Holds | SE:1221. It names the scope (three rates, every reachable placement, every base format, with and without a CRF, eight-channel at 192 kHz), the owner (lane 6, SE:1213), how the search is stated, a failing condition in both the recursion and the simulation, and a bench case. The failing condition can fire: any result under 143.347 µs at 48 kHz fails. See S1 and S2 |
| 4 | No line presents 123.337 µs as worst, or says "published bound" for a class without one | Holds | `git grep` finds 123.337 only at the SE:416 row, an example under SE:438-439. No Mark II page says "published bound". The other hits are unrelated (`sw/firmware/ctrl`, `tb/verilator/gptp_txts`, `scripts/process_test_support.py`). "Accepted" now attaches only to 16-reservation or mixed bounds: FR:306, SE:230, SE:398, AP:60, AP:255. The PR body uses the phrase only to quote round 7's text, marked as corrected |
| 5 | R758-7-R1 applied; area plan and PR body agree | Holds | AP:276 reads "Talker latency taps on all talker streams, measured against the 65 µs target". That differs from the proposed "reported" but closes the same defect and matches FR:306. AP:60, AP:255, the live PR body (Fewer reservations line, Known limitations, Round 8 section) and FR:306 agree |
| 6 | Nothing else changed; docs gates pass | Holds | `receipts/delta_stat.txt`: 3 blobs, modes unchanged, no gitlink moved. The diff does not touch the 16-reservation table or the first fewer-reservations table. My gate re-runs all exit 0 (`receipts/gates_summary.txt`). Author's 50 rc files all read 0 |

## Checks behind check 2

| Item | Page | Mine | Model recursion and simulation |
|---|---|---|---|
| 48 kHz, six one-channel in phase 0 | 103.022 / 143.347 | 103.022, peak 16 streams | 103.022 / 103.022 |
| 48 kHz, eight in phase 0, one in phase 1 | 71.310 / 111.635 | 71.310, peak 3 | 71.310 / 71.310 |
| 96 kHz, four one-channel in phase 0 | 92.935 / 125.426 | 92.935, peak 15 | 92.935 / 92.935 |
| 192 kHz, six in phase 9, one in phase 12 | 83.941 / at least 102.034 | 83.941, peak 6 | 83.941 / 83.941 |

- **Fixed terms:** 40.325 and 32.491 µs match SE's fixed-terms table. 18.093 µs matches SE's 192 kHz line and the author's `p192.out`.
- **Page's other statements, all true:** the form `(k - 1) x 125 / k` is close for equal frames (62.259 against 62.500, 103.022 against 104.167). The published probe's output lists all four cases. Its 192 kHz searches do skip eight-channel streams. The links at SE:447-448 resolve at the pinned commit, and their blobs equal those in the evidence commit.

## Findings

### R757-8-R1 RESIDUE - Docs, Conformance - SE:450-451; PR body, Round 8 "192 kHz" row - "that row may be low" understates the fact and names too narrow a cause

- **Authority and evidence:** assigned check on this wording. `receipts/probe_r8_witness.out` gives these cases, each reached by listed starts and stops under the exact rule, with recursion and 8.6.8.2 simulation agreeing:

| Rate | Final placement | Wait, µs | Total, µs | Page's row |
|---|---|---:|---:|---:|
| 192 kHz | Six-channel in phase 0, one-channel in phase 1 (no eight-channel stream) | 94.357 | 112.450 before the packetizer term; 118.851 with the model's packetizer queue | 102.034 |
| 192 kHz | Eight-channel in phase 0, one-channel in phase 1 | 99.251 | 117.344 before; 125.664 with the queue | 102.034 |
| 192 kHz | Eight-channel in phase 3, one-channel in phase 6 (R758-7 S1) | 88.834 | 106.927 before; 115.247 with the queue | 102.034 |
| 96 kHz | Two eight-channel in phase 0, one-channel in phase 1 | 100.203 | 132.694 | 125.426 |

- **What is wrong:** "may" hedges something already known. "So" ties it to the eight-channel omission alone, but the cause is also that the search was random: phases 0 and 1 are adjacent, and those walks did not reach them. The sentence also singles out one row, though the 96 kHz row is low too.
- **What is right:** SE:438-439 already says no row is a maximum, and the row's figure is correct for its placement.
- **Why RESIDUE:** every case stays below 143.347 µs, so FR:306's "largest figure reached" stands. The maximum is out of scope by ruling, and item 4 owes it. The fix changes prose only and adds no figure.
- **Impact:** a lane reader could expect only eight-channel cases to exceed the 192 kHz row, and none to exceed the 96 kHz row.
- **Exact fix, SE:450-451:**

  ```
  Its 192 kHz search was random, without eight-channel streams.
  Higher cases exist at 96 and 192 kHz.
  [Open design item 4](#open-design-items) covers them.
  ```

  In the PR body's "192 kHz" row, after "at 192 kHz with an eight-channel stream", say that higher cases exist at 96 and 192 kHz and item 4 covers them.
- **Verification:** applied to a disposable copy: the documentation style gate and link gate both pass.

### R757-8-R2 RESIDUE - Docs, Conformance - FR:306 - "that derivation" now points at the derivation that does not exist

- **Authority and evidence:** the delta inserted "the stream-engine lane owes that derivation" shortly before "Verified by analysis (that derivation and its executable model)". The second phrase used to mean the 16-reservation derivation. The nearest match is now the owed one.
- **Impact:** a cold reader could take the analysis half of A,T as resting on work not yet done, or as covering fewer reservations.
- **Exact fix:** "Verified by analysis (the 16-reservation derivation and its executable model)".
- **Verification:** applied to a disposable copy: the documentation style gate and link gate both pass.

### Suggestions (optional)

- **S1 - Tests, Docs - SE:1221:** item 4's failing test names only the tables' cases, so a result of 130 µs at 96 kHz would pass it, against the requirement's scope. Add the published placements in `receipts/probe_r8_witness.out` and R758-7 S1 as floor cases.
- **S2 - Tests, Docs - SE:1221:** "at the largest placement" is singular over three rates. "At each rate's largest placement" would remove the doubt.
- **S3 - Tests, Docs - SE:1196, FR:306:** the evidence still owed names runs "with one format and with mixed formats per port". Only item 4 names a fewer-reservations bench case. A pointer to item 4 would join them.
- **S4 - Docs - AP:60, AP:255; PR body, lines 27 and 296:** "not met with fewer reservations" and "exceeded by" read as covering the whole class, while SE:400 says "some cases" and the first table has a Met row. "Not always met" would agree.
- **S5 - Docs - SE:246:** "So the bound applies to its AAF streams" follows a statement that separates a target from bounds. "So the target and any bound apply to its AAF streams" would be exact.

## Prior findings

Read only after my verdict and ledger were first recorded.

| Finding | State at this head | Evidence |
|---|---|---|
| R757-7-F1 MINOR | **Resolved**, outcome (b) | Rows are examples (SE:438-439). No bound is derived, and lane 6 derives it (FR:306, SE:233-234, SE:1221). The bench rule covers a case with no bound (FR:306, SE:236-240). "No connection is refused" stays. Its verification: the author's re-run of `probe_fewer_bound.py` is byte-identical to the published output, and each witness falls under the stated rule |
| R757-7 RR12, R758-7-R1 RESIDUE | **Resolved** in substance | AP:276. The relative link is kept; R758-7-R1's text carried a pinned evidence link that should not be copied into the page |
| R757-7 RR13 RESIDUE | **Retained, manager's** | The issue #640 body still says "Every talker stream meets the 65 µs target" with no superseding note |
| R757-7-S1 | Absorbed | Item 4's bench case |
| R757-7-S2 | Retained, optional | Outside the delta |
| R758-7 S1 | Covered by item 4 | 106.927 µs reproduced; see R757-8-R1 for higher cases |
| R758-7 S2 | Closed | FR:306, "contradicts the analysis and is a finding" |
| R758-7 S3 | Retained, optional | Outside the delta |
| R757-6 S14-S16, R758-6 S1-S4 | Retained, optional | Delta does not touch them |

Earlier rounds are not re-opened. The delta breaks none of them.

## Lens results

- `[R757] PASS Conformance - FR:306, SE:230-243, SE:1221, AP:60, AP:255, AP:276 against the manager's ruling and issuecomment-6558021030 - target, reported-not-failed, grading only against a derived bound, no maximum derived, 143.347 µs as reached, no connection refused. R1 and R2 are residue.`
- `[R757] PASS RTL - receipts/delta_stat.txt, SE:405-451 - no RTL, register, counter or phase-rule text changed; rule and in-phase order reimplemented from SE and agree with the model's tie order and all four rows. The RTL part of R757-7-F1 is closed by stating that no bound exists and assigning it.`
- `[R757] PASS Robustness - receipts/probe_r8.out, receipts/probe_r8_witness.out - below-16-reservation boundary searched at three rates, by walks with pruning and by constructed placements; higher 96 and 192 kHz cases recorded in R1; nothing above 143.347 µs found.`
- `[R757] PASS Tests - SE:1221, scripts/probe_r8.py, receipts/gates_summary.txt, author-r8 evidence/gates - item 4's test can fail, and the rows reproduce in two implementations. No executable test changed. S1 to S3 are optional.`
- `[R757] PASS Docs - the 3-page delta, live PR body, receipts/gate_*.log - anchors and links resolve, tables hash unchanged, em-dash, style, contents and path gates pass. R1 and R2 are residue.`

## Evidence checked

- **Author packet:** 119 `author-r8` entries in the evidence `MANIFEST.json`, none mismatched. The author's `SHA256SUMS` reports 16 mismatches. All 16 are among the 17 files the manifest marks as path-redacted, so publication explains them.
- **Author's witnesses:** `witness.out` agrees with my replay. Its statement that the owner has been told is now backed by the public record, issuecomment-6559636145.
- **My gate re-runs, disposable copy at this head:** `docs_check.py` 0 findings over 213 pages; `check_doc_style.py` and its self-test; `check_em_dash.py` 0 findings over 1,792 added lines; `check_doc_paths.py` 1,084 paths; `gen_toc.py` `--check`, `--verify-anchors` and `--selftest`; `git diff --check`. All exit 0.
- **Commits:** both subjects are one line with no trailers.
- **Source comments:** the delta has none, so the comment rule has nothing to apply to.
- **Clone state:** no probe ran in the review clone. It is clean at the exact head and tree, and its six gitlinks are unchanged.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (residue R1, R2) | FR:306, SE:230-243, SE:1221, AP:60, AP:255, AP:276, ruling and owner decision, PR body | R757-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| RTL | CLEAN | Delta file list, SE:405-451, phase rule and model agreement; no RTL in the delta | R757-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| Robustness | CLEAN | Reached cases at three rates, witness replays, walks and constructed cases | R757-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| Tests | CLEAN | Item 4's verification, two implementations against the model, author's and my gate results | R757-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |
| Docs | CLEAN (residue R1, R2) | The 3-page delta, live PR body, anchors, tables, gates | R757-8 | 20933ef48a9b174e58a9d17ddd59078a072024af |

## Real limits

- **Delta review.** Only the delta and what it depends on were judged; other artifacts keep their prior verdicts, per the assignment.
- **No ceiling is proven.** My search of "nothing above 143.347 µs" is a random walk with pruning plus constructed cases, without a CRF in the search. Supporting argument at 48 kHz: a seventh co-phased one-channel frame would need more than 16 streams. It is not a derivation, and item 4 still owes that.
- **Every figure is derived, none measured.** Fixed terms include the page's estimates. Physical calibration was NOT RUN, and no hardware proof exists.
- **Selected docs gates only.** I re-ran the gates that read the changed pages. The rest of the docs workflow, including the builder legs, is the author's receipt. No manager source bank ran at this head, and none is claimed.
- **Hosted checks are observation only.** When read, `rtl-fast`, `full-ci-gate`, `docs-check-no-git` and `wire-accountability` passed, and `docs-gates-0` to `docs-gates-2` were still pending. The Verilator and Yosys contexts skip on this documentation-only change, which is not execution evidence.

## Pending manager duties

- Carry R757-8-R1 and R757-8-R2 to the residue checklist.
- Apply RR13 on the issue #640 body.
- **Owner's answer is outstanding.** The 13:35 decision was taken on 123.337 µs. Issuecomment-6559636145 records that the owner was told of 143.347 µs and has not answered, so the decision stands and can still be revisited. The decision's text still says bounds "for fewer reservations are accepted", while the pages now say none exists, by the manager's ruling. A cold reader meets both.
- Own hosted and act acceptance at the exact head, including `docs-gates-0` to `docs-gates-2`.
- Build and validate the current-dev merge candidate at the merge turn, and publish its receipts. Source base and live dev were `1f29f189279f9fc0132f4918e47342b87d22f33a` when read.
- Obtain the other independent review at this head. Merge needs explicit maintainer authorization.

R757-8 FINISHED
