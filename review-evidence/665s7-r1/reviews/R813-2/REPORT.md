[R813] NEGATIVE - exact head 2131eff48066da1e3bbeb6b417ea0655fa7c7741

# R813-2: internal cleared-context delta review of PR #874 (issue #867, Mark II split S7)

Head `2131eff48066da1e3bbeb6b417ea0655fa7c7741`, tree `b61ef3ca8b8c07a89ba7fb32071eadf3550b31e3`. That is two commits on round 1's `5fb6904f`: `0d8e89bc` (F-1) and `2131eff4` (F-2). Base `dev-soft-core` `1d6bf555`. Remote branch tip re-read at review time: `2131eff4`.

**Verdict: NEGATIVE.** There is one MINOR, F-1, under Conformance, Robustness and Tests. RTL and Docs are clean. Docs carries two RESIDUE wording items.

Both round-1 findings from the prior external review are fixed at this head as the round 2 ruling asked:
- **F-1 (allowance).** Every bound and the `[608]` window come from one `SVC_MS = 20`. No 18 ms figure is left.
- **F-2 (two-sided JoinTime).** JoinTime spacing is now graded on both sides. Both short Join-timer arms are refused by their own words, and both escape with the new check switched off.

The new MINOR is in that two-sided check:
- **The defect.** It blames any frame that leaves within 100 ms of a Join-timer expiry on that timer.
- **Why it matters.** lwSRP's Join timer only gates sending. When a request arrives after the timer has run out with nothing to send, the frame goes at once. That is a conformant requested opportunity, and the check refuses it if it lands 260 to about 300 ms after the frame before.
- **Probe result.** A probe moving the licence scenario's peer LeaveAll 280 ms past a periodic frame reproduces it. lwSRP answers 1 ms after receipt, and the grade refuses that answer. The same probe at 240 ms grades clean.
- **Why the gates pass.** The shipped scenarios put every peer stimulus on the 100/200 ms grid, so `make srptx` never reaches this case.

## How the task was reconstructed

Read in order:
1. `AGENTS.md`, then `CONTRIBUTING.md` by reference.
2. Issue #867's body: acceptance items 1 to 7. Item 3 is "within IEEE 802.1Q-2018 10.7.4 and Table 10-7 plus the approved service allowance (T_svc 20 ms)".
3. The round 2 ruling (PR #874 issuecomment-6763709522) and its follow-up (issuecomment-6765717898): option (a), `SVC_MS = 20` stays a cited literal until #810.
4. The author's round 2 TAKEN and STOP comments on #867.
5. `docs/reference/FR_NFR.md` 3.4.1, whose SRP/MRP row reads: Milan v1.2 Table 4.3, JoinTime 200 ms (180 to 240); "a point-to-point requested transmit opportunity occurs within JoinTime, at most three per 1.5 x JoinTime".
6. `git diff 5fb6904f..2131eff4` and `1d6bf555..2131eff4`, and lwSRP `third_party/lwSRP/src/core/mrp_mad.c:850-855,1414-1423,1498-1541` at the pinned gitlink.
7. The author packet `review-evidence/665s7-r1/author-r2` at `75b5cb59`.

Prior review reports were read only after my own pass over the diff and my own runs. That covers the prior external review's F-1, F-2 and S-1 to S-3, and the prior internal round's S1 to S4.

## The four focus questions

**(1) F-1. One `SVC_MS = 20`, and the plant 1 ms outside it: holds.**
- `tb/verilator/milan_dp/srptx_grade.py:64` is `SVC_MS = 20`, citing #867 item 3 and the 2026-11-06 ruling.
- Every bound derives from it, at `:74-79`: rate window 280 ms, Join follow-up 220 ms, Join interval 160 to 260 ms, LeaveAll 9,780 to 15,220 ms.
- The `[608]` window at `:544` derives from it too: `deadline + SVC_MS`.
- A search of the three `srptx_*.py`, both READMEs and the Makefile finds no stale figure. It looked for `218`, `282`, `9782`, `15218`, "MRP service bound", `min(T_svc`, `MRP_CEILING` and `T_SVC_MS`. The only 18 left is the history note at `srptx_grade.py:62-63` ("no longer ... = 18 ms").
- The PR body's item 3 row (live, line 57) states 20 ms, 160 to 260, 220, and 9,780 to 15,220.
- The plants keep their own figure on purpose: `srptx_plants.py:27` `ITEM3_SVC_MS = 20`, item 3's figure, separate from the grade's. I accept that as an independent oracle; see S-2.
- `join-late-past-t-svc` sits 1 ms outside, at 221 ms, and is refused. Its control at 219 ms is clean.
- With the grade's `SVC_MS` moved by 1 ms (`receipts/plant-ablate.txt`):
  - at 21 ms, every Join plant escapes with 0 findings, refused by value;
  - at 19 ms, every Join plant escapes by its words, because the bound figure is in the words.

  So the suite pins `SVC_MS` to the millisecond.

**(2) F-2. Two-sided JoinTime, and the short-timer arms: holds as ruled.**
- `grade_time` (`srptx_grade.py:331-336`) grades every interval `join_intervals` returns (`:400-404`) against `JOIN_BOUNDS_MS`. That bound is Milan Table 4.3's 180 to 240 ms (`:71`), widened by T_svc on each side (`:78`).
- Committed arms `a Join timer of 10 centiseconds` and `... 15 centiseconds` (`srptx_mutants.py:58-63`) are refused by their own words in `make srptx-mutants`, 12 of 12 (`receipts/make-srptx-mutants.txt`).
- My own ablation (`receipts/arm-probe.txt`): each committed arm gives 3 findings, all carrying the arm's words, and 0 findings with the new check off.
- The prior external reviewer's own probe, run unchanged (`receipts/prior-external-code-probe.txt`), plants the short timer in the adapter's `mrp_port_configure`, a different place from the committed arms:
  - `join-10cs`: 15 findings, all `[TIME]` Join-interval findings;
  - `join-15cs`: 16 findings, the same;
  - `join-30cs`: refused;
  - `leaveall-5s`: refused, at 9,780 to 15,220;
  - `join-17cs` (170 ms): escapes, inside the ruled 160 to 260 (S-1);
  - `no-join-wait`: escapes (S-4).
- The new capture plants `join-early-past-t-svc` (159 ms) and `join-interval-late` (261 ms) are refused. Both escape with the check off, and their controls at 161 and 259 ms are clean (`receipts/plant-ablate.txt`).

**(3) The unplanted runs' JoinTime intervals: inside 160 to 260 ms.** From `receipts/join-gaps.txt`, using the grade's own attribution:

| Scenario | MSRP | MVRP |
|---|---|---|
| wire | N 104, 198.989 to 200.000 ms | N 104, 198.989 to 200.015 ms |
| hold | N 34, 198.989 to 200.000 ms | N 32, 198.989 to 200.000 ms |
| licence | N 8, 198.989 to 200.000 ms | N 5, 198.989 to 200.000 ms |

- These equal the author's `join-figures.txt`.
- Every gap the check does not grade that lies outside 160 to 260 is periodic or LeaveAll, or crosses a hold. So no Join-timer frame is hiding among them.
- All three reports (findings and measured block) equal the author's published report receipts (`scripts/report_compare.py`, run inline). `wire-report.json` is byte-identical, sha256 `a6ed3d88...`.

**(4) Nothing outside tb/ and docs changed: holds.**
- `git diff --name-only 5fb6904f 2131eff4` lists five files:
  - `tb/verilator/milan_dp/srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py`;
  - `tb/verilator/milan_dp/README.md`;
  - `sw/firmware/ctrl/srp/README.md`.
- Over the whole PR (`1d6bf555..`) nothing is under `hdl/` and no firmware C changed.

## Prior findings at this head

| Prior finding | State at `2131eff4` | Evidence |
|---|---|---|
| Prior external F-1 (18 ms, not 20) | RESOLVED | Question (1) above. Deriving `SVC_MS` from the budget source is deferred by ruling to #810, through the residue checklist. |
| Prior external F-2 (JoinTime graded only on the late side) | RESOLVED as ruled | Question (2). The new check's upper side has its own new defect, F-1 below. That is a new finding, not this one retained. |
| Prior external S-1 to S-3; prior internal S1 to S4 | RETAINED as SUGGESTION, to the residue checklist by the ruling | The delta touches none of them. S-1/S3 still holds: my capture hashes differ from the author's, though the reports are equal. The new Join-interval check inherits S4's positional `accepted_ms` (`queued`/`held`). |

## Findings

### [R813] F-1 MINOR: Conformance, Robustness, Tests. The two-sided Join-interval check refuses a conformant requested transmit opportunity that follows an idle Join expiry

**Where:** `tb/verilator/milan_dp/srptx_grade.py:385-397` (`causes`), `:400-404` (`join_intervals`), `:94` (`ATTRIBUTE_MS = 100`) and `:331-336` (the new refusal). All are in the reviewed delta: `causes` was measurement-only at `5fb6904f` and now gates.

**Authority and evidence:**
- **The standard.** IEEE 802.1Q-2018 10.7.4.1 has the jointimer space transmit opportunities. `FR_NFR.md` 3.4.1 (Milan v1.2 4.2.7.1.1, Table 4.3) says a point-to-point requested opportunity occurs within JoinTime, at most three per 1.5 x JoinTime.
- **lwSRP's behaviour** (`mrp_mad.c`):
  - each transmit arms the Join timer and sets `join_wait` (`:1539-1540`);
  - the timer's expiry only clears `join_wait` (`:854`);
  - a later request then transmits at the next poll (`:1421`).

  So after a quiet Join period, a request is answered at once. That frame is not "a Join timer's transmit opportunity".
- **The grade's attribution.** `causes` still pins any frame within 100 ms after a Join expiry to that expiry. `join_intervals` then grades its gap to the frame before against 160 to 260 ms.
- **Falsification** (`receipts/request-probe.txt`, `scripts/request_probe.py`). This is the licence scenario with only the peer's MSRP LeaveAll moved off the grid: `srptx.hpp` `kPeerLeaveAllMs` changed in a disposable build, then restored byte for byte.
  - At ms 16280: periodic frame at 16000.013, Join expiry 16200.001 with nothing sent, peer LeaveAll applied at 16280. lwSRP answers at 16281.044, 1 ms after the request, so within JoinTime. The grade's only finding is `[TIME] MSRP: a Join timer's transmit opportunity at ms 16281, 281.030 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms; ...)`.
  - At ms 16240: the same move grades with 0 findings.
- **Why the gates miss it.** At this head every scenario's peer stimulus is on the 100/200 ms grid (`twin.hpp:255-296`, `srptx.hpp:324-345`), so no gate reaches the window.

**Impact:**
- `[TIME]` refuses conformant egress whenever a request lands about 260 to 300 ms after the last frame, with no periodic expiry between. That is a 40 ms window in every 1 s periodic cycle.
- So item 3's evidence depends on stimulus phase, and an off-grid scenario (a later stage, or a real peer's timing) fails `make srptx` with a false item-3 violation.
- The same attribution feeds `measure_time`'s JoinTime figures, which would count such a frame as a +80 ms JoinTime error.
- No result at this head changes.

**Required outcome:**
- The Join-interval check grades only frames the Join timer actually gated, or in some other way does not refuse a requested opportunity made after the Join timer expired with nothing to send.
- It keeps refusing the committed plants (`join-early-past-t-svc`, `join-interval-late`) and arms (10 cs, 15 cs).
- A control holds the requested-after-idle case and grades clean.

**Verification:**
- `scripts/request_probe.py tb/verilator/milan_dp WORK 280 240` gives 0 findings at both offsets.
- `make srptx`, `srptx-plants` (25 of 25, every control clean) and `srptx-mutants` (12 of 12) stay rc 0.
- The prior external probe's `join-10cs` and `join-15cs` stay refused.

### [R813] R-1 RESIDUE: Docs. The PR body's Status still reads as stopped and awaiting a decision

**Where:** PR #874 body, `## Status`, lines 14-24 (live at review time): "STOPPED at the round 2 head, on one line in item 1 ..." and "... This needs a decision (below)."

**Evidence:** the follow-up ruling (issuecomment-6765717898) chose option (a) and accepted the head for delta review.

**Exact fix:** replace the STOPPED sentence with "Round 2 head, accepted for delta review (ruling of issuecomment-6765717898, option (a))". Replace "This needs a decision (below)." with "Ruled: option (a), a cited literal until #810; the switch to the budget source is on the residue checklist (#495), owned by #810."

### [R813] R-2 RESIDUE: Docs. `ATTRIBUTE_MS`'s comment says it serves "the measurement only"

**Where:** `tb/verilator/milan_dp/srptx_grade.py:93`.

**Evidence:** since `2131eff4`, `causes` also decides which frames the `[TIME]` Join-interval check refuses (`:332`).

**Exact fix:** say it serves the measurement and the `[TIME]` Join-interval check, or say whatever F-1's fix makes true.

### [R813] S-1 SUGGESTION: Conformance, Tests. A uniform 170 ms Join timer passes the ruled bound

**Evidence:** the prior external probe's `join-17cs` gives 0 findings. Every interval is 168.989 to 170.000 ms, outside Milan's 180 to 240 but inside 160 to 260. This is the bound the ruling set, so it is not a defect at this head.

**Optional:** a lower side at the configured JoinTime, `JOIN_MS - SVC_MS - RESOLUTION_MS` = 170 ms:
- it refuses that arm, whose minimum is 168.989;
- it still passes the 179.989 ms interval that follows the 219 ms control (`receipts/plant-ablate.txt`).

If not adopted, say in the README that the bound admits a uniformly short timer down to 160 ms.

### [R813] S-2 SUGGESTION: Tests, Docs. Name both `SVC_MS = 20` lines in the #810 residue entry

`srptx_plants.py:27` `ITEM3_SVC_MS = 20` is item 3's own figure, deliberately apart from the grade's `srptx_grade.py:64`.

When #810 switches the grade to the budget source, the plants' figure should stay tied to item 3. The residue entry should say so, so that it is not "derived" too and the oracle is not lost.

### [R813] S-3 SUGGESTION: Tests. The `[608]` window and the rate window have no 1 ms boundary pair

Both derive from `SVC_MS` (`srptx_grade.py:74,544`), so the Join plants pin them only through that derivation. `late-stop` is 2 s out, and its words carry no bound figure.

A `[608]` plant at deadline + 21 ms, with a control at + 19 ms, would hold the window itself.

### [R813] S-4 SUGGESTION: Tests. The rate rule still has no code mutant

The prior external probe's `no-join-wait` still gives 0 findings. At egress it is three MSRP frames in ms 1, then periodic frames. The point-to-point rule (three per 1.5 x JoinTime) allows that, so this is not a defect.

The prior external F-2's second request (a stimulus or mutant that exercises the rate rule) was not adopted by the ruling. It remains optional.

**Comment rule:** the delta's source comments name no lanes, rounds, reviewer IDs or comment IDs (diff scan). The README's `[TIME]` row cites issuecomment-6681686082. That is documentation, and it replaces an existing comment link of the same form, so it is not RESIDUE.

## Clean and unclean lenses, with evidence

```text
[R813] PASS RTL — git diff --name-only 5fb6904f 2131eff4 (5 files: 3 tb/verilator/milan_dp/srptx_*.py, 2 READMEs); git diff --stat 1d6bf555 2131eff4 (no hdl/, no firmware C) — the delta changes no RTL, CDC, interface or firmware artifact; the RTL lens result at 5fb6904f depends on nothing the delta touches, and the twin_sp build plus 3 scenarios rebuilt from these sources at this head grade 0 findings (receipts/make-srptx.txt)
[R813] PASS Docs — tb/verilator/milan_dp/README.md:111,1554,1590-1609,1618-1690; sw/firmware/ctrl/srp/README.md:380-387; PR #874 body item 3 row (line 57) and F-1/F-2 rows (67-70) — every figure checked against the code and my runs (280/220/160-260/9,780-15,220 ms; 25 plants, 3 controls, 12 mutants; 198.989-200.015 ms; the 179.99 ms figure is 179.989 in receipts/plant-ablate.txt); stale-figure search clean; docs_check, check_em_dash --base 1d6bf555 and check_doc_style rc 0 (receipts/docs-spotcheck.txt); only RESIDUE R-1, R-2
[R813] MINOR Conformance — srptx_grade.py:331-336,385-404 — F-1; acceptance items 1, 2, 4-7 and the rest of item 3 untouched by the delta and unchanged from the prior round
[R813] MINOR Robustness — srptx_grade.py:385-404 — F-1 (off-grid request timing)
[R813] MINOR Tests — srptx_grade.py:331-336; srptx_plants.py:98-115 (no control for a requested-after-idle opportunity) — F-1; otherwise plants 25/25, controls 3/3, mutants 12/12, ablations and 1 ms drift as above
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1) | `srptx_grade.py:62-79,331-336,385-404,544` against IEEE 802.1Q-2018 10.7.4.1, 10.7.11, Table 10-7; Milan v1.2 Table 4.3 via `FR_NFR.md` 3.4.1; #867 item 3; both rulings; lwSRP `mrp_mad.c:850-855,1414-1423,1498-1541`; `receipts/request-probe.txt` | R813-2 (not covered) | `2131eff48066da1e3bbeb6b417ea0655fa7c7741` |
| RTL | CLEAN | `git diff --name-only 5fb6904f 2131eff4`; `git diff --stat 1d6bf555 2131eff4`; twin_sp rebuilt from these sources at this head, 3 scenarios with 0 findings | R813-2 (RTL scope unchanged since R813-1 at `5fb6904f`) | `2131eff48066da1e3bbeb6b417ea0655fa7c7741` |
| Robustness | UNCLEAN (F-1) | `srptx_grade.py:94,385-404`; scenario stimulus `twin.hpp:255-296`, `srptx.hpp:89-92,324-345`; `receipts/request-probe.txt`, `receipts/join-gaps.txt` | R813-2 (not covered) | `2131eff48066da1e3bbeb6b417ea0655fa7c7741` |
| Tests | UNCLEAN (F-1) | `srptx_plants.py:22-115,149-185,274-311`; `srptx_mutants.py:24-67`; `receipts/make-srptx-plants.txt`, `make-srptx-mutants.txt`, `plant-ablate.txt`, `arm-probe.txt`, `prior-external-code-probe.txt`, `ratchet-diffcheck.txt` | R813-2 (not covered) | `2131eff48066da1e3bbeb6b417ea0655fa7c7741` |
| Docs | CLEAN (RESIDUE R-1, R-2 to the checklist) | `tb/verilator/milan_dp/README.md:111,1554,1590-1609,1618-1690`; `sw/firmware/ctrl/srp/README.md:380-387`; PR body (live, 12,668 bytes); `receipts/docs-spotcheck.txt` | R813-2 | `2131eff48066da1e3bbeb6b417ea0655fa7c7741` |

## Executed in this round

All runs used pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), in this clone at the exact head. Each run is in `receipts/`.

| Run | Result | Receipt |
|---|---|---|
| `make srptx` (`-j16`, 5 m 16 s) | rc 0; wire 0 findings / 1,449 MRPDUs, hold 0 / 169, licence 0 / 69 | `make-srptx.txt` |
| `make srptx-plants` (re-runs `srptx`) | rc 0: 25 of 25 refused, 3 of 3 controls clean | `make-srptx-plants.txt` |
| `make srptx-mutants` (`-j8`, 19 m 37 s) | rc 0: 12 of 12 refused, after 5 clean controls | `make-srptx-mutants.txt` |
| The prior external reviewer's `code_probe.py`, unchanged | Its sha256 matches its packet's manifest. Arms `join-10cs`, `join-15cs`, `join-17cs`, `join-30cs`, `leaveall-5s` and `no-join-wait`; results as in question (2) | `prior-external-code-probe.txt` |
| `scripts/join_gaps.py`, `scripts/plant_ablate.py`, `scripts/arm_probe.py`, `scripts/request_probe.py` | Questions (2) and (3), F-1 and S-1 | `join-gaps.txt`, `plant-ablate.txt`, `arm-probe.txt`, `request-probe.txt` |
| `measure_test_evidence.py --check`, `git diff --check` (against `1d6bf555` and `5fb6904f`) | rc 0 | `ratchet-diffcheck.txt` |
| Docs spot-checks | rc 0 | `docs-spotcheck.txt` |
| Author packet (43 `author-r2/` entries of `MANIFEST.json` rehashed) | 0 mismatches, 0 unlisted | `packet-verify.txt` |
| Tree restore | Porcelain status empty; index and work tree equal `HEAD`; every tracked blob rehashed (0 mismatches); 6 gitlinks equal `HEAD`'s; `srptx.hpp` sha256 `1c220c4f...` | `tree-restore.txt` |

The packet commit `75b5cb59` is not signed. Its integrity rests on `MANIFEST.json`, which verifies.

`receipts/make-srptx*.txt` have the toolchain's include root, which resolves under a local home directory, replaced by `<VERILATOR_ROOT>` (`receipts/REDACTION.txt`).

## Real limits

- **No manager source bank** ran at this head, and none is claimed or inferred. Source-head execution evidence beyond my own runs is the author's published receipts, spot-checked as above.
- **Not run here:**
  - the full sweep, the firmware self-test and its mutant drivers, `make split` and `split-mutants`, S2's harness, `test_builder.py` and `behave`;
  - the rtl-fast boundary jobs and the rtl/elaborate workflows;
  - any Docker or act job.

  The delta touches none of their inputs, apart from the boundary configuration's listed `srptx` files, which are unchanged.
- **Hosted checks at the exact head** (read once, read-only; `receipts/hosted-checks.txt`): 11 success, 1 skipped, 35 queued or in progress. None of them is acceptance evidence from this review.
- **The F-1 probe** is one licence-scenario variant with a moved stimulus time. It shows the check refusing conformant egress. It does not measure how often a real peer would hit the window.
- **Physical calibration NOT RUN.** There are no hardware, field or bench results. The simulated time base excludes firmware instruction time.

## Pending manager duties

- Route F-1 to the author for a fix and a delta re-review, or obtain a ruling.
- Carry R-1, R-2, S-1 to S-4, and the retained prior suggestions to the residue checklist. Add the #810 `SVC_MS` budget-source switch, naming both 20 ms lines (S-2).
- Accept the hosted exact-head contexts and the act replica.
- Build and validate the current-dev merge candidate (live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`, source base `dev-soft-core`) at the merge turn.
- Collect R814-2's independent verdict. Merging needs two independent positive reviews and the full completion bar.

R813-2 FINISHED
