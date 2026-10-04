[R461] POSITIVE - exact head 4811c21d8fe29faa1e9e713a6622bb206189e74b

# R461-3: external independent review of issue #85 / PR #152 (GAP-16, ADP MTXW walk), round 3

- Exact head `4811c21d8fe29faa1e9e713a6622bb206189e74b`, tree `320166a09c124757e9f217dbb91f822690f87c34`.
- Source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. Round-2 head `4298ed2595d98ec98592bea4e05c4d1744663c34`.
- Round-3 delta (`4298ed25..4811c21d`): 4 commits, 5 files, all under `tb/adp_engine`:
  - `README.md`, `mutants.py` and `sim_main.cpp`;
  - the new `mutations/arc-fresh-store-plus-one.patch` and `mutations/arc-fresh-store-max.patch`, both mode 100644.
  - `hdl/`, `syn/`, `scripts/` and `docs/` are byte-identical to `4298ed25`. The engine blob is `97076caf…` at both heads (`receipts/round3-scope.txt`).
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR is open. Every lens is CLEAN.
- R461-2-F1 is **resolved**. The noted index is now pinned to exactly 701 in both fresh cells, and to exactly 699 in the restart cell. R461-2's q1 and q2 edits are planted as arms and fail arc 4's check. R460-1's `r7` and my `q4` now fail the restart walk cell and arc 5.
- One new SUGGESTION (R461-3-S1) and one retained SUGGESTION (R461-1-S1) are recorded.

## 1. Reconstruction, in the order required

1. **Conventions.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head, so conventions come from `README.md` and `docs/README.md`.
2. **Frozen scope** (issue #85):
   - the body: GAP-16, acceptance 1 to 4;
   - the lane comment 5974306370 and the round-2 assignment 5975300666;
   - the **round-3 assignment 5975655103**. It is tests only:
     - item 1, R461-2-F1: a two-sided follow-up, where a repeat of 701 gives the restart pair and 702 gives none, with messages stating what each side proves; q1 and q2 shipped as arms that fail arc 4's check; 41 of 41 KILLED, controls passing;
     - item 2, R461-1-S2: the restart cell `V_STALE x D_DISC` gets the same follow-up, so `r7` fails the walk cell;
     - item 3, R461-2-S1: one named constant at the three sites;
     - item 4, R461-1-R1 exactly;
     - gates, including R460-1's `probes.py` and my E8/E9 probes, unchanged;
   - REVIEW READY `4811c21d` (5975854958).
3. **Authorities.**
   - `docs/architecture/04_adp_engine.md` F04.8 `:254-255`:
     - fresh row: action "note the index, restart T-ADP-NOADP", §5.6.4.5.2 steps 1 and 3;
     - restart row: guard "`available_index` <= last, grandmaster and domain match", action "EVT_TK_DEPARTED then EVT_TK_DISCOVERED, note the index, restart T-ADP-NOADP", steps 2a, 2c and 3.
   - REQ-ADP-013's restart detector.
   - `tb/adp_engine/README.md`.
4. **Diff and history.** I read `git diff 5c71928a..4811c21d` (19 files), `4298ed25..4811c21d` (5 files) and the 13 commits.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@4b05825f` `review-evidence/pp85-r1` holds round-1 author material: HANDOFF, PR bodies and the three adoption patches. It was committed 2026-10-04T00:50Z, before this round.
   - The PR #152 body at this head carries the round-3 section and its evidence table.
   - No round-3 manager evidence comment is on the issue or PR. Hashes are in `receipts/evidence-read.txt`.
6. **Prior public findings** were read only after my own pass over the diff and runs E1 to E3, E5 and E7 to E9:
   - R460-1 (5975297523) and R460-2 (5975615786);
   - my own R461-1 (5975267550) and R461-2 (5975652786).
   - I did not read R460-3.

**Simulator.** Pinned Verilator 5.050, first on `PATH` for every run. Its identity matches round 2: wrapper sha256 `905795b9…`, `verilator_bin` sha256 `44898b22…` (`receipts/simulator-identity.txt`). The host default (5.052) was not used.

**Where things ran.** Builds and runs used a `git archive` export of the exact head, or copies of it, under the packet's `scratch/`. The docs gates used a scratch local clone. The review clone was never written.

## 2. What I ran (all at exact head, pinned Verilator)

The runs went concurrently, each with its own log and rc file, within 16 jobs.

| # | Run | Result | Receipt |
|---|---|---|---|
| E1 | `make -C tb/adp_engine run` | rc 0, `1348 checks: 1348 PASS, 0 FAIL`. P13: F04.2 45 cells (N 12, I 20, S 6, C 7), F04.3 33 cells (N 13, I 15, S 2, C 3), 8 arcs | `receipts/head-adp_engine-run.{log,rc}` |
| E2 | `make -C tb/adp_engine mutants JOBS=6` | rc 0. Both controls PASS, 41 of 41 KILLED, `43 checks: 43 PASS`. Every arm's count equals its README row (`receipts/campaign-vs-readme.txt`). Against round 2, exactly the README's stated changes and nothing else: `disc-fresh-checks-gm` 4 to 5, `disc-not-discovered-checks-index` 14 to 17, `disc-restart-not-rediscovered` 7 to 8, plus the two new arms (`receipts/campaign-vs-round2.txt`). The failing-check list of each changed or new row matches its README text (§4) | `receipts/head-campaign-jobs6.{log,rc}`, `receipts/campaign-jobs6/*.log` |
| E3 | `scripts/r461_probes.py`, **unchanged** (R461-2 E8, sha256 `6a14bf88…`, equal to its round-2 copy) | control 1348 PASS. **q1** (fresh notes received + 1) and **q2** (fresh notes `32'hFFFF_FFFF`) are now rc 2 with 4 FAIL each: both "at most 701" sides, arc 4's check and the arc count. At `4298ed25` both passed 1334 of 1334. q0: 4 FAIL, arc 4 among them. q3: 1 FAIL, the `V_GMF` cell (its fault acts only on a foreign grandmaster). q4 (restart notes nothing): 4 FAIL, namely P9e2, the restart cell's "at most 699" side, arc 5 and the arc count; in round 2 it failed P9e2 only. q5: `ANCHOR`, because the round-2 line it deletes no longer exists (E5's `c1` is its round-3 counterpart) | `receipts/r461-probes.txt`, `receipts/r461-probes-compare.txt`, `receipts/probes/` |
| E4 | `scripts/pptop_q2.sh`, **unchanged** (R461-2 E9) | rc 0, `10416 checks: 10416 PASS, 0 FAIL`, as in round 2. pp_top does not grade the noted index; `tb/adp_engine` now does (E2, E3) | `receipts/pptop-q2-run.{log,rc}` |
| E5 | Round-3 probes `scripts/r461_3_probes.py`: RTL faults on both noting branches, and TB controls showing which part of the check carries the grading | see §3. Every RTL fault is red, at the arc of its cell. Each TB control shows its design element is load-bearing | `receipts/r461-3-probes.txt`, `receipts/probes3/` |
| E6 | Order probe `scripts/r461_3_order_probe.py`: index + 1 first, then the repeat, with no second walk | head RTL 1342 PASS; q1 red; **q3 passes, 1342 of 1342**. This confirms the PR body's claim that "702, then repeat" lets q3 through | `receipts/r461-3-order-probe.{txt,rc}`, `receipts/probes-order/` |
| E7 | R460-1's `probes.py`, **unchanged** (sha256 `078df30e…`) | control 1348 PASS. **`r7`** (restart notes nothing): 4 FAIL, namely P9e2, the restart cell's "at most 699" side, `P13 F04.3 arc DISCOVERED -> DISCOVERED (index <= last, GM matches: restart pair)` and the arc count; at `4298ed25` it was P9e2 only. `r8`: 11 FAIL, its round-2 10 plus the `V_GMF` cell's "at most" side. `r6` and `x2`: same checks, with the round-3 "at least" message wording. `x1`: 1352 PASS. All other probes (r1 to r5, t1 to t3) have the same rc and FAIL lines as at `4298ed25` | `receipts/r460-1-probes.txt`, `receipts/r460-1-probes-compare.txt`, `receipts/r460-1-probes/` |
| E8 | `make lint links matrix modmatrix params stale` (scratch local clone at the head) | all rc 0: 41 mermaid and 18 wavedrom blocks, 1120 links, 115 REQ / 17 GAP, 94 rows with 0 untested, 28 parameters | `receipts/make-check-subset.txt`, `receipts/make-*.log` |
| E9 | Round-3 scope | `git diff --stat 4298ed25 4811c21d -- hdl syn scripts docs` is empty. The engine blob is identical at round 2 and head (it was proven comment-only against base in R461-2 E4). All three `arc-fresh-*` patches pass `git apply --check` at the head | `receipts/round3-scope.txt` |
| E10 | Clone integrity, after all probes | HEAD and tree exact, detached, `git status --porcelain --ignored` empty, index tree = head tree. All 515 tracked entries re-hashed: 0 blob or mode mismatches. 0 gitlinks: there is no `.gitmodules` and no submodule, so no submodule gitlink is required | `receipts/clone-integrity.txt` |
| E11 | Hosted runs at the exact head (read-only, last read 2026-10-04T02:57Z) | Executed with success, push and pull_request: `docs-gates` (×2) and `portability` (×2). `suites` (×2) was **in_progress with no conclusion**. No skipped context | `receipts/hosted-check-runs.tsv` |

## 3. The round-3 check, graded (E5, E6, and the README's own arms)

**Under test.** `check_noted_index` (`tb/adp_engine/sim_main.cpp:1599-1626`), called for `notes_index` cells (`:344-346`: `V_FRESH`, `V_GMF` and `V_STALE` x `D_DISC`). It works in three steps:

1. From the cell's end state, an AVAILABLE repeating `noted_index(row)` (`:349-351`; 701, or 699 for the restart cell) must give the pair. That proves "at least".
2. `goto_disc` and `apply_disc` walk the cell again (`:1613-1615`).
3. An AVAILABLE at the index + 1 must give no event (`:1622-1625`). That proves "at most".

A failure in either side counts against the cell through `cell_ok` (`:1663-1665`), and so against arc 4 (`V_FRESH`) or arc 5 (`V_STALE`).

| Probe | Edit | Result | What it shows |
|---|---|---|---|
| s1, s2 | restart branch notes received + 1, or the maximum | 4 FAIL each: P9e2, restart cell "at most 699", arc 5, count | restart over-noting is caught at arc 5 |
| s3 | restart notes received − 1 | 3 FAIL: restart cell "at least 699", arc 5, count | restart under-noting is caught at arc 5 |
| s4 | fresh notes received − 1 | 4 FAIL: both "at least 701" sides, arc 4, count | fresh under-noting is caught at arc 4 |
| s5 | fresh notes the right index under interface 1 | 12 FAIL, arc 4 among them | the interface half of the record is graded too |
| c1 | TB: the second walk and the "at most" side removed; RTL q1 | rc 0, 1336 PASS | the "at most" side is the only grader of over-noting |
| c2 | TB: "at most" asked straight after the repeat, with no second walk; RTL q1 | rc 0, 1342 PASS | the second walk is load-bearing. This confirms the PR body's "repeat, then 702 lets q1 through" |
| E6 o3 | TB: index + 1 first, then the repeat, with no second walk; RTL q3 | rc 0, 1342 PASS | confirms the PR body's "702, then repeat lets q3 through" |
| c3 | TB: restart cell walked at 700 (the round-2 index); RTL r7 | rc 2, P9e2 only, walk green | walking the restart cell at 699 is what makes `r7` show in the walk |
| c4, c5, c6 | TB: `DISC_LAST = 900`; head RTL, q1, r7 | 1348 PASS; q1 red at arc 4 (messages read 901/902); r7 red at arc 5 (899/900) | every site follows the constant; R461-2-S1's vacuity risk is gone |

**Exactness.** The lower side gives noted >= N and the upper side gives noted <= N, so noted = N (701 in the fresh cells, 699 in the restart cell). The over-noting and under-noting faults on both branches, and the interface fault, all fail at their arc. q3 is red in the `V_GMF` cell. That cell is not an arc's walk cell (`F043_ARCS`, `:327-336`), and the round-3 assignment requires arc 4 only for q1 and q2, so q3 at arc 4 is not required. In the match cell its fault does not act.

## 4. Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R461-3-S1 | SUGGESTION | Tests, Robustness | `tb/adp_engine/sim_main.cpp:1613-1615` (the second walk in `check_noted_index`) | The second `goto_disc` and `apply_disc` are not followed by the "reached" and end-state checks the first walk makes (`:1535-1537`, `:1550-1554`). Under `disc-not-discovered-checks-index`, the second walk of both fresh cells leaves the sink in TK_NOT_DISCOVERED (the README row at `:298` says so). Their failure is then reported as "the noted index is at most 701 … got 1 events": the one event is the EVT_TK_DISCOVERED of the 702 AVAILABLE. A second walk that ended in TK_NOT_DISCOVERED would make the "at most" side grade the discovery arc's note rather than the fresh arc's. That takes a fault that spares the first walk, and under every such single fault I ran the suite is red anyway | Diagnosis only: no fault survives (E2, E3, E5, E7) | Optional: after the second walk, check that the sink is bound and discovered before the AVAILABLE at the index + 1, so a failure names the walk. Update the count and rows if taken | Read `:1613-1625`. Under `disc-not-discovered-checks-index` the new check would fail in place of, or beside, the "at most" line |
| R461-1-S1 (retained) | SUGGESTION | Tests, Docs | `sim_main.cpp` `check_the_mtxw_walk` citation counts (`:1630-1648`) | Still prefix-only; listed open in the PR body round 3. R460-1's `t3` still gives 42 of 45 | None for acceptance | Optional, as in R461-1 | As in R461-1 |

No BLOCKER, MAJOR, MINOR or RESIDUE is open.

## 5. Earlier findings at this head

| Item | Disposition | Evidence |
|---|---|---|
| R461-2-F1 (MINOR, Tests): the noted index was bounded from below only; q1 and q2 survived | **Resolved.** Each part of its required outcome is met. Both fresh cells are bounded from both sides, each with a failure that clears the cell and so arc 4. The over-noting arms (`arc-fresh-store-plus-one`, `arc-fresh-store-max`, identical to my q1 and q2 edits) are planted, KILLED, and name arc 4's check. The README record, the count (1348) and the PR body round 3 are updated. The upper bound uses the assignment's design (the cell walked again, then index + 1 gives no event), not my variant B. E5 and E6 show it is exact and why the second walk is needed. My round-2 verification line expected q3 red at arc 4 under variant B; under the assigned design q3 is red in its own cell (§3), which the assignment accepts | E2, E3, E5, E6 |
| R461-2-S1 (SUGGESTION): the follow-up's index was a duplicated literal | **Taken.** `DISC_LAST` (`:339`) is used at the three sites (`:350`, `:1484`, `:1496`). No other 699 to 702 literal remains in `sim_main.cpp`. `c4` to `c6` move it to 900 with the grading intact | E5 |
| R461-1-S2 (SUGGESTION): the restart arc's noted index was caught by P9e2 only | **Taken.** The restart cell is walked at 699 and gets the two-sided check. `r7` and q4 now fail the cell and arc 5. `c3` shows the 699 index is what makes this work. The row, class, events, timer and clauses of the cell are unchanged (`:308-309`, F04.8 `:255`). The equality boundary is still walked: the "at least" repeat, and `V_GMS` and `V_DOMS` x DISCOVERED, send it. `arc-restart-detector-off-by-one` keeps 13 and still fails arc 5 | E2, E3, E5, E7 |
| R461-1-R1 (RESIDUE, Docs): `README.md:100` | **Resolved, exactly.** `:100-101` now read "The table above gives each cell's class and, for its N cells, the Milan clause; F04.7 gives every cell's Milan clause and adds its IEEE clause." That is my stated fix, word for word; commit `4811c21` rewraps only | README `:100-101` |
| R460-2 R2-1 (RESIDUE, Docs): "and so arc 4's check" overstated the GM-mismatch cell | **Resolved.** README `:157-158`: "A failure there fails its cell; in the fresh match cell, arc 4's walk cell, and in the restart cell, arc 5's, it also fails that arc's check." This is R2-1's fix, extended to the restart cell, and true per `F043_ARCS` and E5. PR body round 2 item 1 now reads "A failure clears that cell; in the match cell it also fails arc 4's check" | README, PR body (sha256 in `receipts/evidence-read.txt`) |
| R460-2 S2-1 (SUGGESTION): the literal index | **Taken**, as R461-2-S1 above | E5 c4 to c6 |
| R460-1 F-1, R-1, S-1, S-2; R461-1-S3 | Resolved in round 2 (R461-2 §4); unchanged by round 3, since `hdl/`, `Makefile` and the round-2 PR-body text are untouched | E9 |
| R461-1-S1 | **Retained** as SUGGESTION (above) | — |

Nothing worsened. All 39 earlier arms keep their verdicts, and every count matches its README row. Only the three rows the README names grew.

## 6. Lens findings

- **Conformance: CLEAN.**
  - F04.8's fresh and restart rows both "note the index" (`04:254-255`). The walk now grades that action exactly in the three cells that take those arcs: the two fresh cells (the fresh guard reads no grandmaster) and the restart cell.
  - The restart cell's index, 699, is inside its guard (`<= last`).
  - No citation, cell, class, F04.7 row or F04.8 row changed in round 3.
  - The head RTL notes exactly the received index on both branches: E1, and E5's control.
- **RTL: CLEAN.**
  - No RTL change in round 3 (E9).
  - The two new patches change exactly the fresh branch's write data (`KL_adp_engine.sv:359`), keep `rec_wr_en_w` and the re-arm, and apply at the head.
- **Robustness: CLEAN** (S1 is a suggestion).
  - The campaign at `JOBS=6` reproduces every README count.
  - The new arms' expected label `(index > last)` cannot match arc 5's `(index <= last, …)` (named=1 each).
  - `DISC_LAST` removes the drift risk (c4 to c6).
  - Both sides count events from their own `e1`/`e2` and check the sink.
  - Clone integrity holds (E10).
- **Tests: CLEAN.**
  - E1 to E7. Every fault class on the noted index (over and under, on both branches, and the interface) is red at its arc, as are R461-2's q1/q2 and R460-1's `r7`.
  - The TB controls show each design element is needed: the upper side (c1), the second walk (c2, o3) and the 699 index (c3).
- **Docs: CLEAN.**
  - README `:6` count 1348.
  - `:100-101` (R1 exact).
  - `:148-158` describes the check, its three cells and its arc consequences accurately.
  - `:159-167` describes the two new arms.
  - The round-3 campaign note `:264-270` and rows `:297-311` match E2 line for line.
  - PR body round 3 items 1 to 4 and its evidence table agree with E1 to E7, including the "six per graded cell" arithmetic (3 x 6 − 2 x 2 = +14) and both scratch-variant claims (c2, o3).
  - Docs gates pass (E8).
  - Privacy: the round-3 diff and commit messages contain no device name, entity id, model or tool name, mail address or host path.

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 04 F04.8 fresh and restart rows (`:254-255`) against `notes_index`/`noted_index`, the `DISC` table and `F043_ARCS`; the restart cell's 699 against its guard; head RTL notes exactly (E1, E5 control) | R461-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| RTL | CLEAN | round-3 scope empty under `hdl/` (E9); `arc-fresh-store-plus-one.patch` and `arc-fresh-store-max.patch` against `KL_adp_engine.sv:356-362`, `git apply --check` | R461-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| Robustness | CLEAN (S1 suggestion) | campaign at `JOBS=6` (E2), label uniqueness, `DISC_LAST` relocation (E5 c4 to c6), event attribution in `check_noted_index`, clone integrity (E10), hosted runs (E11) | R461-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| Tests | CLEAN | E1 (1348/1348), E2 (2 controls, 41/41, every count and changed failure list against README), E3 and E4 (my R461-2 E8/E9 unchanged), E5 and E6 (round-3 fault and TB-control probes), E7 (R460-1 `probes.py` unchanged, compared with its round-2 receipt) | R461-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| Docs | CLEAN | `tb/adp_engine/README.md` (`:6`, `:100-101`, `:148-167`, `:264-270`, `:297-311`), PR #152 body round 3 and the round-2 item-1 edit, `sim_main.cpp` comments `:338-351` and `:1594-1598`, docs gates (E8), privacy sweep of the round-3 diff and commits | R461-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |

## 8. Real limits

- **No standards text.** I had no copy of Milan v1.2 or IEEE 1722.1-2021. Clause references were checked for consistency against 04 F04.8 and the walk's tables, not against the printed text.
- **No full banks.** By instruction I ran no full processor bank (`run_suites.sh`), no full `lint_hdl.sh`, no Yosys, no builder and no parent consumer set. `wavedrom-check` was not run here: round 3 changes no WaveDrom source or doc, and hosted `docs-gates` succeeded at this head. The author's round-3 figures for those gates (`run_suites` 1,021,469 checks, and the parent gates re-run) are the author's record and are not reproduced here.
- **No round-3 manager receipt.** The brief says the manager's source static/builder and native banks passed at this head. The public evidence directory named (`pp85-r1@4b05825f`) predates round 3, and I found no round-3 manager evidence comment, so I could not inspect that receipt. Every round-3 figure graded here comes from my own runs.
- **Hosted `suites` unfinished.** At the exact head it was in progress, with no conclusion, at last read (02:57Z). Only `docs-gates` and `portability` had executed. Hosted and act acceptance are the manager's.
- **No hardware.** Physical calibration was NOT RUN; field skips are not hardware proof. The live-controller handling of an ENTITY_DEPARTING remains the README's restated open limit (issue #85 item 4).
- **No merge candidate.** The final current-dev candidate (source base `5c71928a` onto live dev `241f91845230ae410506dffb16b71937127fd175`) was not built here.

## 9. Pending manager duties

- Inspect or publish the manager's exact-head bank receipts, and confirm the hosted `suites` conclusion at the final head. Hosted/act acceptance is the manager's.
- R461-3-S1 and R461-1-S1 are optional. No residue item from this review is open; R461-1-R1 and R460-2 R2-1 are resolved and can leave the residue checklist.
- At the merge turn:
  - build and gate the current-dev candidate (source base `5c71928a`, live dev `241f9184`);
  - confirm the parent consumer set, with gate 16's T30 failures attributed to parent #643;
  - merge requires two independent positive reviews.

## 10. Receipts

Every published file is listed in `MANIFEST.sha256`. Host paths in logs are redacted to `<SIM_ROOT>`, `<SCRATCH>`, `<PACKET>`, `<CLONE>` and `<SIM_WRAPPER_DIR>`. The scripts are portable and path-parameterised:

- `scripts/run_head.sh` (unchanged from R461-2): E1 and E2.
- `scripts/r461_probes.py` (unchanged): E3.
- `scripts/pptop_q2.sh` (unchanged): E4.
- `scripts/r461_3_probes.py`: E5.
- `scripts/r461_3_order_probe.py`: E6.
- `scripts/r460-1-probes.py` (R460-1's `probes.py`, unchanged, sha256 `078df30e…`): E7.
- `scripts/verify_clone.sh`: E10.
- `scripts/redact.py`: the path redaction.
- `scripts/strip_compare.py`: carried from R461-2 and not re-run, since round 3 changes no HDL.

R461-3 FINISHED
