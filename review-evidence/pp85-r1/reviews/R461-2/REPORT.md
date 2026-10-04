[R461] NEGATIVE - exact head 4298ed2595d98ec98592bea4e05c4d1744663c34

# R461-2: external independent review of issue #85 / PR #152 (GAP-16, ADP MTXW walk), round 2

- Exact head `4298ed2595d98ec98592bea4e05c4d1744663c34`, tree `7704889e1e07e546d6d155470800e7387f477e62`.
- Source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. Round-1 head `a8669732b30436c641d51829950c204defd57a30`.
- Round-2 delta (`a8669732..4298ed25`, 3 commits, 6 files):
  - `hdl/adp/KL_adp_engine.sv`: comments only;
  - `tb/adp_engine/{Makefile, README.md, mutants.py, sim_main.cpp}`;
  - the new `tb/adp_engine/mutations/arc-fresh-no-store.patch` (mode 100644).
- Verdict: **NEGATIVE**. One MINOR finding is open: R461-2-F1, Tests lens.
- Everything the round-2 assignment (issue comment 5975300666) asked for is delivered and verified. R460-1's F-1 is resolved as R460-1 specified it.
- The new follow-up step grades the fresh arc's noted index from **below only**. Two one-line RTL faults that note too high a value survive both suites that build the engine: `tb/adp_engine` 1334 of 1334 and `tb/pp_top` 10416 of 10416.

## 1. Reconstruction, in the order required

1. **Conventions.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head, so conventions come from `README.md` and `docs/README.md`. Those are: plain-text clause citations, Milan wins, single-source rules, and `make check` before commit.
2. **Frozen scope** (issue #85):
   - the body: GAP-16, acceptance 1 to 4;
   - the lane comment 5974306370: tests and the docs they cite, no RTL change, items 1 to 4, gates;
   - the round-2 assignment 5975300666. Item 1 is R460-1 F-1: a follow-up step in `V_FRESH x D_DISC` whose failure clears the cell, the same treatment for `V_GMF x D_DISC` if F04.8 notes its index, and the `arc-fresh-no-store` arm failing arc 4's check, giving 39 of 39. Item 2 takes R460-1 R-1, S-2 (`make mutants JOBS=N`) and S-1 (comment-only engine restatement, comment-stripped source identical). Item 3 leaves R461-1's suggestions open;
   - REVIEW READY `4298ed25` (5975528337).
3. **Authorities.** `docs/architecture/04_adp_engine.md` §5, F04.3 and F04.8; F04.8 row "TK_DISCOVERED to itself, fresh" has guard "`interface_index` equal, `available_index` > last" and action "note the index, restart T-ADP-NOADP" (Milan v1.2 §5.6.4.5.2 steps 1 and 3). REQ-ADP-013's restart detector. `tb/adp_engine/README.md`.
4. **Diff and history.** `git diff 5c71928a..4298ed25` (17 files) and `a8669732..4298ed25` (6 files), and the 9 commits.
5. **Public evidence:**
   - `kebag-logic/milan-fpga@4b05825f` `review-evidence/pp85-r1`, which holds the author's round-1 HANDOFF, PR bodies and adoption patches; its `PR-BODY.md` is the round-1 body;
   - the PR #152 body at this head, which carries the round-2 evidence table;
   - the manager's review-start comments.
   - No separate round-2 manager receipt was in that directory or in the issue/PR comments. Hashes are in `receipts/evidence-read.txt`.
6. **Prior public findings** were read only after my own pass and probes:
   - R460-1 (5975297523), plus its published `scripts/probes.py` and `receipts/probes/probes-summary.txt` from `pp85-review-evidence@c8dd7b8b`; both sha256 match R460-1's MANIFEST;
   - R461-1 (5975267550).
   - I did not read R460-2.

**Simulator.** Pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`; wrapper sha256 `905795b9…`; `receipts/simulator-identity.txt`), first on `PATH` for every run. The host default (5.052) was not used.

**Where things ran.** Every build and run used a `git archive` export of the exact head, or a copy of one, under the packet's `scratch/`. The review clone was never written.

## 2. What I ran (all at exact head, pinned Verilator)

| # | Run | Result | Receipt |
|---|---|---|---|
| E1 | `make -C tb/adp_engine run` | rc 0, `1334 checks: 1334 PASS, 0 FAIL`. P13: F04.2 45 cells (N 12, I 20, S 6, C 7), F04.3 33 cells (N 13, I 15, S 2, C 3), 8 arcs | `receipts/head-adp_engine-run.{log,rc}` |
| E2 | `make -C tb/adp_engine mutants JOBS=6` (Makefile forwards `--jobs 6`) | rc 0. Both controls PASS, 39 of 39 KILLED, `41 checks: 41 PASS`. **Every arm's failure count equals its README row**, the three changed rows included (`disc-fresh-checks-gm` 4, `disc-restart-not-rediscovered` 7, `arc-restart-detector-off-by-one` 13) and the new `arc-fresh-no-store` 4: both follow-ups `got 0 events`, `P13 F04.3 arc DISCOVERED -> DISCOVERED (index > last): walked and graded`, and `7 of 8`. The failing-check lists of the changed rows match their README text | `receipts/head-campaign-jobs6.{log,rc}`, `receipts/campaign-jobs6/*.log` |
| E3 | `make -n mutants` with no JOBS, `JOBS=9`, `JOBS=2 MUTANT_OUTPUT=/x`, and `JOBS=3` from the environment | `--jobs 4`, `--jobs 9`, `--jobs 2`, `--jobs 3` | `receipts/make-jobs-dryrun.txt` |
| E4 | Engine comment-only, two independent ways | `KL_adp_engine.sv` at base, round 1 and head: an independent comment stripper (`scripts/strip_compare.py`) gives identical stripped text (sha256 `0cd8c0a7…`, 1098 raw lines each). `verilator -E -P` (pkg + engine) is byte-identical at all three (sha256 `82b1fa71…`, 1045 lines). `git diff 5c71928a 4298ed25 -- hdl syn scripts` touches only `KL_adp_engine.sv`, +8/−8 | `receipts/hdl-comment-only.txt` |
| E5 | `verilator --lint-only` (`lint_hdl.sh` flags, top `KL_adp_engine`, whole tree visible) | rc 0, 0 warning or error lines | `receipts/lint-adp-engine.txt` |
| E6 | `make lint links matrix modmatrix params stale` (in a scratch local clone at the head) | all rc 0 | `receipts/make-check-subset.txt`, `receipts/make-*.log` |
| E7 | R460-1's `probes.py`, **unchanged** (sha256 `078df30e…`, equal to its MANIFEST), `--jobs 6` | control 1334 PASS. `r6-fresh-no-store` rc 2 with 4 FAIL, arc 4's check among them; at `a8669732` it was 1330 of 1330 PASS. `x1` 1338 PASS. `x2` 5 FAIL. **Every other probe** (r1 to r5, r7, r8, t1 to t3) has the same rc, failure count and byte-identical FAIL lines as R460-1's `a8669732` receipt | `receipts/r460-1-probes.txt`, `receipts/r460-1-probes/`, `receipts/r460-1-probes-compare.txt` |
| E8 | Reviewer probes `scripts/r461_probes.py` (RTL faults on the noted index, plus a TB control) | see R461-2-F1 | `receipts/r461-probes.txt`, `receipts/probes/` |
| E9 | `make -C tb/pp_top run` with probe q2 | rc 0, `10416 checks: 10416 PASS, 0 FAIL` | `receipts/pptop-q2-run.{log,rc}` |
| E10 | Feasibility of F1's required outcome, scratch only (`scripts/r461_fixcheck.py`, variants A and B) | B: head RTL 1338 of 1338 PASS; q0 to q3 each fail arc 4's check. A: misses q3 | `receipts/r461-fixcheck-{A,B}.txt`, `receipts/fixcheck/` |
| E11 | Clone integrity | HEAD and tree exact, detached, `git status --porcelain --ignored` empty, index tree = head tree. All 513 tracked entries re-hashed: 0 blob or mode mismatches. 0 gitlinks: this repository has no submodules, so there is no submodule gitlink to check | `receipts/clone-integrity.txt` |
| E12 | Hosted runs at the exact head (read-only) | push and pull_request runs: `docs-gates` success (×2) and `portability` success (×2) were executed. `suites` (×2) was **in_progress with no conclusion** when last read; no context was skipped | `receipts/hosted-check-runs.tsv` |

## 3. Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R461-2-F1 | MINOR | Tests | `tb/adp_engine/sim_main.cpp:1582-1596` (the round-2 follow-up step in `walk_discovery_cell`), and `:338-343` (`notes_fresh_index`). RTL under test: `hdl/adp/KL_adp_engine.sv:345` and `:358-360` | **Authority:** F04.8, row "TK_DISCOVERED to itself, fresh": action "note the index" (Milan v1.2 §5.6.4.5.2 step 3). REQ-ADP-013: the restart detector compares the next index with the noted one. Round-2 item 1 and R460-1 F-1: grade the noted index. **What the step checks:** an AVAILABLE repeating index 701 must give the restart pair. That only proves the noted value is **at least** 701. Its message says "index 701 noted", which the check does not establish. **Evidence** (E8 and E9, one-line edits in scratch copies): **q1** (the fresh branch notes received + 1) gives rc 0, 1334 of 1334 PASS. **q2** (the fresh branch notes `32'hFFFF_FFFF`) gives rc 0, 1334 of 1334 PASS, and `tb/pp_top run` 10416 of 10416 PASS. `KL_adp_engine` is built only by `tb/adp_engine` and `tb/pp_top`. Controls: q0 (the r6 edit) gives 4 FAIL, arc 4's check among them; q5, the walk without the follow-up, gives 1330 PASS, so the step is the only grader. q3 (noting only on a grandmaster match) gives 1 FAIL, in the `V_GMF` cell only | **Field impact:** an over-noted index makes the talker's next ordinary advert read as "index <= last". Each such advert raises a spurious EVT_TK_DEPARTED then EVT_TK_DISCOVERED, about every other advert under q1 and q2, so the ACMP listener re-probes a talker that never restarted (05 §6.5). This is the restart-detector state-update regression class R460-1 F-1 was raised for, and the suites still merge it green. The head RTL is correct: E10's control passes the stricter check, 1338 of 1338 | Bound the noted value from above as well as from below, inside each of the two fresh cells (`V_FRESH x D_DISC`, `V_GMF x D_DISC`), with a failure that clears the cell and so arc 4's check. One proven way (E10, variant B), before the repeat: (1) send an AVAILABLE at noted + 1 carrying a **foreign** grandmaster; it must give **no event**, since an over-noted value reads it as stale and foreign. (2) Repeat noted + 1 with grandmaster and domain matching; it must give the restart pair. Variant A (step 1 with a matching grandmaster) is not enough: it re-notes through the fresh arc and lets q3 through. Plant an over-noting arm (for example `arc-fresh-store-high`: the fresh branch notes received + 1) that must fail `P13 F04.3 arc DISCOVERED -> DISCOVERED (index > last)`. Update the README mutation record, the check count and the PR body's round-2 item 1 | `make -C tb/adp_engine run` passes. The campaign shows both controls PASS and 40 of 40 arms KILLED, with `arc-fresh-no-store` and the new arm each naming arc 4's check. Rerunning `scripts/r461_probes.py` turns q0 to q3 red at arc 4 (in this review's variant B: q0 4 FAIL, q1 6, q2 6, q3 4, control 1338 PASS) |
| R461-1-R1 (retained) | RESIDUE | Docs | `tb/adp_engine/README.md:100` | Unchanged at this head: "The table above gives each cell's class and Milan clause; F04.7 adds its IEEE clause." The table at `:88-98` gives a clause only for the N cells and for WAITING x ENTITY_DISCOVER (another entity_id) | Wording only: no figure, test or clause claim changes | Exact fix: "The table above gives each cell's class and, for its N cells, the Milan clause; F04.7 gives every cell's Milan clause and adds its IEEE clause." | Read `:100` against `:88-98` and F04.7 |
| R461-2-S1 | SUGGESTION | Tests, Robustness | `tb/adp_engine/sim_main.cpp:1585` (`noted = 700 + 1`), duplicating `:1475` and `:1487` | The follow-up hard-codes the index that `goto_disc` and `apply_disc` choose. If those moved to 701 or above, the repeat would give the pair whether or not anything was noted, so the step would pass vacuously. Today `arc-fresh-no-store` would then go UNPROVEN and the campaign would catch it | Maintainability only | Optional: one named constant for the discovered column's last index, used at all three sites | Read the three sites |
| R461-1-S1 (retained) | SUGGESTION | Tests, Docs | `sim_main.cpp` `check_the_mtxw_walk` citation counts | Open, not taken (assignment item 3). Still prefix-only | None today | Optional, as in R461-1 | As in R461-1 |
| R461-1-S2 (retained) | SUGGESTION | Tests | restart cell `V_STALE x D_DISC`; P9e2; P9j | Open, not taken. At this head, q4 and R460-1's `r7` (the restart branch notes nothing) still fail only `P9e2 restart stored the new index`. The walk cell stays green | None for acceptance: the suite turns red | Optional: give the restart cell the same two-sided follow-up as F1 | `receipts/probes/probe-q4-restart-no-store.log` |

No BLOCKER or MAJOR. One MINOR open (R461-2-F1).

## 4. Round-1 items at this head

| Item | Disposition | Evidence |
|---|---|---|
| R460-1 F-1 (MINOR): the fresh arc's "note the index" is graded nowhere | **Resolved as specified.** Each of its three required outcomes is met: a follow-up in both step-3 cells (F04.8's fresh guard reads no grandmaster, so `V_GMF x D_DISC` notes too, as the README says), with a failure that clears the cell and so arc 4; `arc-fresh-no-store` planted and KILLED through arc 4's own check; README record and count (1334) updated. Its verification holds: 39 of 39, R460-1's `r6` now red, `x1`/`x2` as predicted. The upper side of the same action is not graded; that is **new finding R461-2-F1**, not a retention | E1, E2, E7 |
| R460-1 R-1 (RESIDUE): PR body `--jobs` wording | **Resolved.** PR body item 3 now reads exactly as R-1's fix | PR body at review time (sha256 in `receipts/evidence-read.txt`) |
| R460-1 S-1: engine comments | **Resolved**, comments only. Banner `:33-42` and the index-manager comment `:703-707` state the adjudicated reading, which agrees with README `:163-209`. The comment-stripped source and the preprocessed source are identical to base and round 1 | E4, E5 |
| R460-1 S-2: `make mutants` jobs | **Resolved**: `JOBS ?= 4` forwarded as `--jobs $(JOBS)` | E2, E3 |
| R461-1-R1 (RESIDUE) | **Retained** as RESIDUE, with the exact fix above | `README.md:100` |
| R461-1-S1 | **Retained** (open by assignment) | — |
| R461-1-S2 | **Retained** (open by assignment); the restart arc's noted index is still caught only by P9e2 | q4, `r7` |
| R461-1-S3: `make mutants` jobs | **Resolved** by S-2's change | E3 |

Nothing worsened. All 30 earlier arms and the 8 round-1 `arc-` arms keep their verdicts, and their counts match the README. Only the three rows the README names grew.

## 5. Lens findings

- **Conformance: CLEAN.**
  - F04.8's fresh arc reads no grandmaster, so treating both index > last cells of TK_DISCOVERED as noting the index matches 04 and the cell table: `V_GMF x D_DISC` is 'N', TK_DISCOVERED, no event, arm, "5.6.4.5.2 steps 1 3".
  - Round 2 changes no citation, cell or F04.7/F04.8 row.
  - The head RTL notes exactly the received index in both cells: E10's two-sided check passes, 1338 of 1338.
  - The engine comments now agree with the adjudication: §6.2.2.15 stands, and only the live-controller DEPARTING case is open.
- **RTL: CLEAN.**
  - Comment-only, proven two ways (E4); lint clean (E5).
  - `arc-fresh-no-store.patch` removes exactly `KL_adp_engine.sv:359` and keeps the re-arm. It applies at the head; the campaign applied every RTL patch with `git apply --check`.
- **Robustness: CLEAN** (S1 is a suggestion).
  - The campaign ran at `JOBS=6` with the verdicts and counts the README records at the author's runs.
  - The `arc-fresh-no-store` expected label is a unique prefix: `(index > last)` versus `(index <= last, …)`.
  - The follow-up's events are counted from its own `e1` and attributed to the sink.
  - Clone integrity holds (E11).
- **Tests: UNCLEAN** (R461-2-F1).
  - What is delivered is verified: E1, E2, E7.
  - The follow-up bounds the noted index from below only; q1 and q2 survive every suite that builds the engine (E8, E9).
- **Docs: CLEAN** (one retained RESIDUE).
  - README `:3` check count 1334. The round-2 paragraph (`:145-160`) describes the step accurately: a repeat that must give the pair.
  - The mutation record rows and the "Re-run … second round" note match E2. The `make mutants JOBS=N` text at `:236-238` matches E3. The banner restatement at `:210-212` is accurate.
  - PR body round-2 items 1 to 4 and its evidence table agree with E1, E2 and E7.
  - Docs gates pass (E6). Privacy: the round-2 diff and commit messages add no device name, entity id or model id.
  - When F1 is fixed, the PR body's "the noted index is graded" and README `:150-153` need to describe the added upper bound. That is part of F1's required outcome, not a separate defect today.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 04 F04.3 and F04.8 (fresh-arc guard and action), the `DISC` table and `notes_fresh_index` against them, the README adjudication against the new engine comments, and E10's two-sided check on head RTL | R461-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| RTL | CLEAN | `KL_adp_engine.sv` base/r1/head comment-stripped and `-E -P` identical (E4), lint (E5), `arc-fresh-no-store.patch` against `:359` | R461-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| Robustness | CLEAN | `Makefile` JOBS forwarding (E3), campaign at `JOBS=6` (E2), label uniqueness, follow-up event attribution, clone integrity (E11), hosted runs (E12) | R461-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| Tests | UNCLEAN (R461-2-F1) | E1 (1334/1334), E2 (2 controls, 39/39, every count against README), E7 (R460-1 `probes.py` unchanged, compared byte-for-byte with its round-1 receipt), E8/E9 (q1, q2 survive `tb/adp_engine` and `tb/pp_top`), E10 (fix feasibility) | R461-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| Docs | CLEAN (1 RESIDUE retained) | `tb/adp_engine/README.md` (`:3`, `:100`, `:145-160`, `:210-212`, `:229-298`), PR #152 body round 2, engine comments, docs gates (E6), privacy sweep of the round-2 diff | R461-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |

## 7. Real limits

- **No standards text.** I had no copy of Milan v1.2 or IEEE 1722.1-2021. Clause references were checked for consistency against 04 F04.8 and the walk's tables, not against the printed text.
- **No full banks.** By instruction I ran no full processor bank (`run_suites.sh`), no full `lint_hdl.sh`, no Yosys, no builder and no parent consumer set. `wavedrom-check` was not run here: round 2 changed no WaveDrom source, and hosted `docs-gates` succeeded at this head. The author's round-2 figures for those gates (`run_suites` 1,021,455 checks, Yosys 42 tops, the parent gates re-run) are the author's record and are not reproduced here.
- **No round-2 manager receipt.** The public evidence directory `pp85-r1@4b05825f` is round-1 author material. I found no round-2 manager receipt, so every round-2 figure graded here comes from my own runs.
- **Hosted `suites` unfinished.** At the exact head it was in progress, with no conclusion, at last read. Only `docs-gates` and `portability` had executed. Hosted and act acceptance are the manager's.
- **No hardware.** Physical calibration was NOT RUN; field skips are not hardware proof. The live-controller handling of an ENTITY_DEPARTING remains the README's restated open limit.
- **No merge candidate.** The final current-dev candidate (source base `5c71928a` onto live dev `241f91845230ae410506dffb16b71937127fd175`) was not built here.

## 8. Pending manager duties

- Carry R461-2-F1 to the author lane; a new head needs re-review.
- Carry R461-1-R1 (exact fix above) to the residue checklist.
- R461-2-S1 and R461-1-S1/S2 are optional.
- Confirm the hosted `suites` conclusion at the final head, and own hosted/act acceptance.
- At the merge turn:
  - build and gate the current-dev candidate;
  - confirm the parent consumer set at dev `5fabb46e` + c8 + p2-p1 + c10, with gate 16's T30 failures attributed to parent #643;
  - merge requires two independent positive reviews.

## 9. Receipts

Every published file is listed in `MANIFEST.sha256`. Host paths in logs are redacted to `<SIM_ROOT>`, `<SCRATCH>`, `<PACKET>`, `<CLONE>` and `<SIM_WRAPPER_DIR>`. The scripts are portable and path-parameterised:

- `scripts/run_head.sh`: E1 and E2.
- `scripts/strip_compare.py`: E4.
- `scripts/r461_probes.py`: E8.
- `scripts/pptop_q2.sh`: E9.
- `scripts/r461_fixcheck.py`: E10.
- `scripts/verify_clone.sh`: E11.
- `scripts/redact.py`: the path redaction.

R461-2 FINISHED
