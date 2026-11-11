[R813] POSITIVE - exact head 2128daad26b932feeed1ef2bde8f2774e8a51a31

# R813-3: internal cleared-context delta review of PR #874 (issue #867, Mark II split S7), round 3

- Head `2128daad26b932feeed1ef2bde8f2774e8a51a31`, tree `9b067a62ffa66e2cb51303206cac6c7f85ba61c6`, on `dev-soft-core` `1d6bf5556a`. The round-3 delta is one commit on `2131eff48066da1e3bbeb6b417ea0655fa7c7741`, touching 7 files (`receipts/delta-files.txt`).
- Base for this review: the issue's frozen acceptance 1 to 7; the item-5 ruling (issuecomment-6760813135); the round-2 rulings (PR issuecomment-6763709522 and -6765717898, option (a)); the round-3 ruling (PR issuecomment-6766550989, items 1 to 4); `docs/reference/FR_NFR.md` 3.4.1; IEEE 802.1Q-2018 10.7.4.1, 10.7.11, Table 10-7; lwSRP `mrp_mad.c` at the pinned gitlink `08ee86e8`.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open, and all five lenses are clean at this head. The round-3 ruling's items 1 to 4 are met. R813-2's F-1 is resolved at its cause, and so are both round-2 reviews' RESIDUE items. Recorded below: one RESIDUE, three new SUGGESTIONs and the retained prior SUGGESTIONs. None affects coverage. As ruled, item 5 (#608 in the production composition) stays owed and keeps #867 open. The PR says "Relates to #867" and does not close it.

## How the task was reconstructed

Sources, in this order: AGENTS.md and CONTRIBUTING.md, then the issue body, the author's TAKEN, STOP and REVIEW READY comments and the manager's rulings, then `FR_NFR.md` 3.4.1 (the SRP/MRP row) and lwSRP's `mrp_transmit` and `on_join_timer`. After that came the raw diff `2131eff4..2128daad` and its history, and then my own runs. I read the prior reviews' findings only after my own pass over the diff.

Round 3 asked for four things, under the scope the ruling sets:
1. Attribute a Join-timer transmit opportunity by what lwSRP did at its boundary, not by a time window, and grade a requested opportunity after an idle Join expiry by the "within JoinTime" rule.
2. Keep the committed refusals: `join-early-past-t-svc`, `join-interval-late`, and the 10 cs and 15 cs arms.
3. Commit the off-grid case (peer LeaveAll at 16,280 and 16,240 ms) as controls, and have `measure_time` use the same attribution.
4. Fix the five round-2 wording items.

## What I checked, and how

**The attribution (`srptx.hpp:501-525`, `:536-542`, `:608-613`).**
- lwSRP behaves as the bench says. `mrp_transmit` returns 0 while `join_wait` is set, unless a PDU is prepared (`mrp_mad.c:1419-1421`). Each send sets `join_wait` and arms the Join timer (`:1539-1540`). The expiry only clears `join_wait` (`:850-854`).
- The wrapper reads `join_stopped` from the Join timer's public `cs` before the real call, then marks the records that call produced.
  - `after_join` is set on the first poll after an expiry the tick wrapper saw.
  - `idle_us` is set only when the Join timer is stopped and the poll is not that first poll.
  - `idle_us` is cleared by any send.
- The bench edits nothing in lwSRP or the adapter: the `--wrap` link only.
- I classed every accepted MRPDU of the head runs by this record (`receipts/attribution-census*.txt`, `receipts/probe-full-clean.txt`). In the clean tree, only the two first frames after reset fall outside the Join-gated and requested classes. In `hold`, so does the frame the hold queued, at 25,000 ms, which `held()` excludes.

**The grade (`srptx_grade.py:329-360`, `:408-428`, `:444`).**
- `join_intervals` takes exactly the `after_join` frames, with no window.
- The requested rule grades frames with `idle_us` against `JOIN_FOLLOW_MS` (220 ms), outside holds.
- `causes` keeps `ATTRIBUTE_MS` only for periodic and LeaveAll frames, and only `measure_time` calls it (`:438`). So the comment at `:97-98` and the PR's "No check reads it" are true.
- `measure_time`'s JoinTime figures use the new `join_intervals` (`:444`).

**Reproduced at this head** (pinned Verilator 5.050, identity checked; `receipts/head-make-srptx-plants.txt`, `receipts/head-srptx-mutants.txt`):

| Gate | Result |
|---|---|
| `make srptx` | 0 findings in `wire` (1,449 MRPDUs), `hold` (169), `licence`, `licence-16280` and `licence-16240` (69 each) |
| `make srptx-plants` | `26 of 26 refused; 4 of 4 controls inside their bound clean; 2 of 2 off-grid controls clean with their requested transmit opportunity`. The new plant `requested-late` is refused at 221.000 ms, by its own words, and `requested-within` (219 ms) is clean |
| `srptx_mutants.py` | `12 of 12 refused`. The 10 cs and 15 cs arms are refused by the Join-spacing words, at 98.989 and 148.989 ms |

**Other checks.**
- The ablation is as the author claims. The round-2 grade refuses the committed 16,280 ms capture with `a Join timer's transmit opportunity at ms 16281, 281.030 ms after the one before`. It passes 16,240 ms, at 241.030 ms, inside 260 (`receipts/ablation-round2-grade.txt`).
- The figures match. Over all five head captures, the Join intervals are 198.958 to 200.024 ms, and the largest requested latency is 1.025 ms (`receipts/join-range.txt`). The `wire` table's N values (116/524 MSRP, 111/520 MVRP) and the 105/106 after-the-tick counts equal my `wire-report.json`. The README's "six LeaveAll frames" a time window would refuse is 6 by my count (`receipts/window-counterfactual.txt`).

**Falsification probes** (`scripts/joinwait_probe.py`, `receipts/joinwait-probe.txt`, `receipts/probe-full-*.txt`). I wanted to know whether the new attribution leaves a class of frame ungraded, so I planted two lwSRP mutants in a scratch copy, built them through the bench's own `twin_fw.py --replace` recipe, and graded each with the head grade and the round-2 grade.
- **`join_wait` dropped from `mrp_transmit`'s hold.**
  - Wire runs of 3 or 16 s: neither grade refuses it.
  - `wire` at 60 s and 600 s, `hold` and `licence`: the rate rule refuses it at both heads (51/104/1 head findings, 75/160/3 round-2 findings). The round-2 grade's extra findings are Join-spacing findings such as `0.011 ms after the one before`, which the head no longer raises for frames sent while the Join timer runs.
- **Only a pending LeaveAll skips the hold.** No finding at either head, in any full scenario. The census shows 14 LeaveAll frames 10 to 180 ms after the frame before, with the Join timer running.
- **Why neither is a defect.** `FR_NFR.md` 3.4.1 (Milan v1.2 4.2.7.1.1) allows a point-to-point requested transmit opportunity within JoinTime, at most three per 1.5 x JoinTime. So a frame sent while the Join timer runs is answerable to the rate rule, which the grade applies (`:337-342`). It is not answerable to the Join-interval rule. The head grade is consistent with the clause. The round-2 grade's extra refusals were the time window over-attributing, the defect R813-2 F-1 named. This is recorded as S-1, not as a finding.

**Remaining checks.**
- Comment rule: I scanned the delta's added source comments and docstrings for lane labels, lane names, round names, reviewer or author IDs and issue-comment IDs, and found none. They carry issue and clause IDs only. The only issue-comment link in the delta is in the README's `[TIME]` row, a documentation page. It replaces a link of the same form there, so it is not RESIDUE.
- `docs_check.py` (0 findings), `check_doc_style.py` (OK) and `check_doc_paths.py` (OK) are rc 0. `git diff --check` is clean against `2131eff4` and against `1d6bf555`. `check_em_dash.py` cannot judge on this host, because its pinned renderer is not installed and I installed nothing. A scan of the delta's 248 added lines finds no em dash (`receipts/docs-gates.txt`).
- The PR body at review time (`receipts/pr874-body-snapshot.md`) is ready, not draft, and its Status reads "Round 3 at `2128daad`, ready for delta review". Its item rows match my runs.

## Prior findings at this head

| Prior finding | Status | Evidence at this head |
|---|---|---|
| R813-2 F-1 MINOR (Conformance, Robustness, Tests): the time window counts a requested opportunity after an idle expiry as the Join timer's | **RESOLVED** at its cause | `join_intervals` keys on the bench's `after_join` (`srptx_grade.py:424-428`), with no window. The off-grid case is committed and graded clean in `make srptx`, and `srptx-plants` requires it to hold the case. The round-2 grade still refuses 16,280 (ablation). The Join plants and the 10 cs and 15 cs arms are still refused. `measure_time` uses the same attribution. I did not run R813-2's `request_probe.py` myself: the committed `--peer-leave-all-ms` controls are the same stimulus without the source edit, and the author's receipt reports 0 findings at 280 and 240 |
| R813-2 R-1, R814-2 R-1 (PR body read as a STOP) | RESOLVED | The PR body's Status at review time |
| R813-2 R-2 (`ATTRIBUTE_MS` comment) | RESOLVED | `srptx_grade.py:97-98`. Its claim is true: `causes` is called only from `measure_time` (`:438`) |
| R814-2 R-2 (garbled grade prose) | RESOLVED | `srptx_grade.py:18-27` docstring and the `grade_time` comment, as R814-2's exact fix |
| R814-2 R-3 (rate window missing its T_svc term) | RESOLVED | `README.md:1557` reads "1.5 x JoinTime less T_svc (280 ms)" |
| R814-2 S-1 (the Join upper bound assumes the frame before armed the timer) | RESOLVED | It was the same over-attribution, now gone. The 16,280 control is the case |
| R813-2 S-1 (a uniform 170 ms timer passes), S-2 (keep `ITEM3_SVC_MS` on item 3 at #810), S-3 (no 1 ms pair for `[608]` or rate); R814-2 S-3 (controls on a bound 1 ms tighter), S-4 (as R813-2 S-2) | RETAINED, SUGGESTION | The delta does not change them. For R813-2 S-3, the new `requested-late`/`requested-within` pair sits at 221/219 ms, but the `[608]` and rate windows still have no pair |
| R813-2 S-4, R814-2 S-2 (the rate rule has no code mutant) | RETAINED, SUGGESTION, with new evidence | `join_wait` dropped from the hold is refused by the rate rule alone at this head, in `licence` (`four transmit opportunities in 229.997 ms from ms 21000`), and in `wire` at 60 s and over. So a committed arm on `licence` would close it (see S-1) |
| R814-1 S-1 to S-3; R813-1's four SUGGESTIONs | RETAINED, SUGGESTION | Carried by the round-2 reviews and the ruling to the residue checklist. The delta touches none of their artifacts. Not re-examined |

## Findings

### [R813] R-1 RESIDUE: Docs. `Lib::idle_us`'s comment reads as "a transmit that sent nothing"

- **Where:** `tb/verilator/milan_dp/srptx.hpp:178`, `// its Join timer stopped: its last poll since its last transmit that sent nothing`.
- **Evidence:** `poll()` (`:516-525`) records the last poll that sent nothing since the last transmit. The comment's "its last transmit that sent nothing" can be read as a property of the transmit. Wording only: no figure, check or output changes.
- **Exact fix:** `// with its Join timer stopped: its last poll that sent nothing since its last transmit, or -1`.

### [R813] S-1 SUGGESTION: Docs, Tests. Name the third class: frames lwSRP sends while its Join timer runs, graded by the rate rule alone

- **Where:** `srptx_grade.py:329-360`; `README.md:1557` and `:1563-1585`; `srptx_mutants.py` `ARMS`.
- **Evidence:** the bench's record splits each MRPDU three ways: Join-gated (`after_join`), requested after an idle poll (`idle_us`), or neither. In the clean runs the third class is only each protocol's first frame after reset, plus the queued frame in `hold`. A frame lwSRP sends while its Join timer runs falls in that third class. It is a point-to-point requested opportunity, which `FR_NFR.md` 3.4.1 limits only by "at most three per 1.5 x JoinTime". So only the rate rule grades it. That is correct, but neither the README nor the grade says so. Both probe arms show the effect: `join_wait` dropped (refused only by the rate rule, and only from 60 s of `wire`, or in `licence` and `hold`), and LeaveAll skipping the hold (no finding, which is conformant).
- **Suggested outcome:** one README sentence in the `[TIME]` notes: a frame sent while the Join timer runs is a requested opportunity whose request the boundary cannot time, graded by the rate rule. Optionally, commit the `join_wait` arm on `licence` as the rate rule's code mutant, which would close R813-2 S-4 and R814-2 S-2.

### [R813] S-2 SUGGESTION: Robustness, Tests. `--peer-leave-all-ms` accepts any value, and a non-numeric one aborts the bench

- **Where:** `twin_split.cpp:511-523` (`srptx_args`, `std::stoul`), and `:467-471`.
- **Evidence** (`receipts/arg-probe.txt`):
  - `--peer-leave-all-ms abc` throws an uncaught `std::invalid_argument`, rc 134 with a core dump, not a usage error.
  - `-5` is accepted and wraps to a uint32.
  - `18500` is accepted. That puts the peer's LeaveAll after the 18,000 ms withdrawal, which changes the `[608]` premise silently.
  - No committed run is affected: the Makefile passes 16280 and 16240 only.
- **Suggested outcome:** parse with a range check, kPeerLeaveAllMs ≤ N < kWithdrawMs or whatever bound the scenario's premise needs, and print the usage on failure.

### [R813] S-3 SUGGESTION: Tests. The off-grid offsets are listed twice

- **Where:** `Makefile:1004` (`SRPTX_OFF_GRID = 16280 16240`) and `srptx_plants.py:117` (`OFF_GRID = (16280, 16240)`).
- **Evidence:** removing an offset from the Makefile alone fails loudly, because the capture is missing. An offset added to the Makefile alone is graded but never case-checked, so a hollow control could pass.
- **Suggested outcome:** have `srptx_plants.py` take the offsets from the `licence-*.json` captures it finds, or pass `SRPTX_OFF_GRID` to it.

## Clean lenses, with evidence

```text
[R813] PASS Conformance — srptx_grade.py:329-360,424-428,444; srptx.hpp:501-542,608-613; lwSRP mrp_mad.c:850-854,1419-1421,1539-1540 at 08ee86e8; FR_NFR.md 3.4.1 SRP/MRP row — ruling items 1-3 checked against 10.7.4.1 and the point-to-point requested rule: Join interval only for Join-gated frames, requested opportunities within JoinTime + T_svc, frames sent while the Join timer runs left to the rate rule as the clause allows; acceptance 1, 2, 4, 6, 7 untouched by the delta and unchanged (5 runs 0 findings, 26/26 plants, 12/12 mutants at this head); item 5 owed by ruling
[R813] PASS RTL — receipts/delta-files.txt (round-3 delta: no hdl/, .sv, firmware C or gitlink); tb_split_top.sv unchanged since 2131eff4; twin_sp rebuilt from these sources with pinned Verilator 5.050 and run on 5 scenarios — the delta changes no RTL, CDC, interface, firmware or lwSRP artifact; the bench reads lwSRP's public timer cs at the --wrap boundary only
[R813] PASS Robustness — srptx.hpp:516-525 (poll() on result <0, 0 and >0; join_stopped read before the call); srptx_grade.py:349-360 (requested rule outside holds); twin_split.cpp:467-523 — the boot, hold-retry and refused-send paths classed by receipts/attribution-census*.txt; off-grid stimuli at 16,280 and 16,240 ms clean; bad CLI values recorded as S-2 (bench-only, no committed run affected)
[R813] PASS Tests — receipts/head-make-srptx-plants.txt, receipts/head-srptx-mutants.txt, receipts/ablation-round2-grade.txt, receipts/joinwait-probe.txt, receipts/probe-full-*.txt — new plant requested-late refused by its own words and its control clean; off-grid controls clean and case-checked; the round-2 grade refuses the 16,280 control (the control can fail for F-1's defect); the 10/15 cs arms and Join plants still refused; two disposable lwSRP mutants classed as above
[R813] PASS Docs — tb/verilator/milan_dp/README.md:111,1491,1503-1505,1539,1557,1563-1585,1599-1637,1670,1696-1702; sw/firmware/ctrl/srp/README.md:381-387; srptx_grade.py:18-27,97-98,408-428 docstrings; PR #874 body (receipts/pr874-body-snapshot.md) — figures checked against my runs (26/4/2/12; 198.958-200.024 ms; ≤1.03 ms; N 116/524/111/520; 105/106; 6 window refusals; 16,281.044/281.030 and 16,241.044/241.030 ms); docs_check, check_doc_style and check_doc_paths rc 0; comment rule clean; RESIDUE R-1 only
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srptx_grade.py:329-360,408-428,444`; `srptx.hpp:501-542,608-613`; lwSRP `mrp_mad.c:850-854,1419-1421,1539-1540`; `FR_NFR.md` 3.4.1; the five head runs | R813-3 | `2128daad26b932feeed1ef2bde8f2774e8a51a31` |
| RTL | CLEAN | `receipts/delta-files.txt`; `tb_split_top.sv` unchanged since `2131eff4`; the twin_sp build at the head | R813-3 | `2128daad26b932feeed1ef2bde8f2774e8a51a31` |
| Robustness | CLEAN (S-2) | `srptx.hpp:516-542`; `srptx_grade.py:349-360`; `twin_split.cpp:467-523`; `receipts/attribution-census*.txt`; `receipts/arg-probe.txt` | R813-3 | `2128daad26b932feeed1ef2bde8f2774e8a51a31` |
| Tests | CLEAN (S-1, S-3) | `srptx_plants.py:68,110-117,194-224,352-371`; `srptx_mutants.py`; `Makefile:997-1025`; head plants and mutants; round-2 grade ablation; two lwSRP probe mutants | R813-3 | `2128daad26b932feeed1ef2bde8f2774e8a51a31` |
| Docs | CLEAN (RESIDUE R-1) | `tb/verilator/milan_dp/README.md` (rows and sections above); `sw/firmware/ctrl/srp/README.md:381-387`; grade docstrings; PR body snapshot; `receipts/docs-gates.txt` | R813-3 | `2128daad26b932feeed1ef2bde8f2774e8a51a31` |

## Executed in this round (all in this clone or under this packet's scratch)

- `make -C tb/verilator/milan_dp srptx srptx-plants` with `SRPTX_OUT` in scratch: rc 0.
- `python3 -B tb/verilator/milan_dp/srptx_mutants.py`: rc 0, 12 of 12 refused, 4 min 4 s.
- `scripts/joinwait_probe.py`: clean, `join_wait_ignored` and `leaveall_skips_join_wait`, on `wire` (3, 16, 60 and 600 s), `hold` and `licence`, each graded by the head grade and the `2131eff4` grade.
- `scripts/attribution_census.py`, `scripts/join_range.py` and `scripts/window_counterfactual.py` on the head captures.
- The bench's option parsing with three bad values.
- `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `git diff --check` (×2), and an em-dash scan of the added lines.
- Hosted check runs at the exact head, read only (`receipts/hosted-check-runs.txt`).
- Restore check (`receipts/restore-check.txt`): `HEAD` and `write-tree` equal tree `9b067a62`, no tracked change, no untracked file outside ignored build products, and all six gitlinks as committed. lwSRP's worktree is clean at `08ee86e8`. Every mutant copy lived in scratch.
- One host path in a build log is redacted, marked in that file's first line.

## Real limits

- I did not run the workflow `run:` banks, the full sweep, the firmware self-test or mutant campaigns, `make twin`/`twin-plants`, `test_builder.py`, `behave`, S2's harness, `split-mutants` or the Yosys gates. For these I rely on the author's REVIEW READY receipt. The delta touches only `tb/verilator/milan_dp` srptx files and two READMEs.
- `check_em_dash.py` could not run on this host. I replaced it with the added-line scan.
- I did not re-run R813-2's `request_probe.py`. The committed off-grid controls cover the same stimulus.
- Hosted contexts at this head were mostly queued or in progress when read: 9 success, 1 skipped, 39 pending. They are not evidence here.
- My capture bytes are not compared with the author's. Reports and figures are compared, as earlier rounds note.
- No physical calibration, hardware or bench run was made, so this is not hardware proof. Item 5 holds only under the test-only fixture.

## Pending manager duties

- Hosted and act acceptance at the exact head, and the current-dev merge-candidate validation (builder and native banks) against live `dev` `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`, with receipts linked on the PR.
- Carry RESIDUE R-1 and every retained SUGGESTION to the residue checklist (#495). That includes the `SVC_MS` switch to the budget source after #810, with the plants' `ITEM3_SVC_MS` kept on item 3.
- Keep #867 open for item 5 in the production composition. After #810 merges, re-run the #608 check without the fixture.
- Merge needs explicit maintainer authorization, a second independent positive review at this head (the external round R814-3) and the full completion bar.

R813-3 FINISHED
