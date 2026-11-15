# HANDOFF — lane 895 ([A775]), round 10

**Status (22:2x CET 2026-11-15): REVIEW READY at `1215bd82` (local, not pushed), posted once on #895 as issuecomment-6901464046 (REVIEW-READY-COMMENT.md; the posted body checked).** Every finding of R835-4 and R836-4 answered; no statement moved; no image changed after `056d619d`.

Assignment: the manager's round-10 relay. The two NEGATIVE delta reviews of `056d619d` from `62298ab5`: R835-4 (PR #901
issuecomment-6900107977; `review-evidence/895-r1/reviews/R835-4/REPORT.md`, archive `f32a9de6`) and R836-4
(issuecomment-6899966960; `reviews/R836-4/REPORT.md`, archive `c43b8cd0`), each read in full (round10/reviews/).
Start: `056d619d` (pushed, the PR's head), clean.

## Findings

| Finding | Answer | Commit | Receipt |
|---|---|---|---|
| R836-4-F2 MAJOR | the survey's two defects fixed (round10/scripts/costs_vs_stated.py:145 `held(..., r.command)`, :185 `classes.paced`; `record.aecp` counted); the head's record_classes.py over every preserved leg at both points: RESULT PASS; the class maxima (1x1/1if paced 28,288 = 300 of 300, ordinary 21,187 = 225 of 235, long 86,698 = 915 of 975; 8x8/2if 55,365 = 585 of 595, 18,904 = 200 of 265, 126,152 = 1,325 of 1,650); SET_STREAM_INFO 20,363 (215 of 235) and 17,511 (185 of 265), held with the command only; no restatement; the four plants refused by the grader and the corrected survey, passed by round 8's; coverage 63 a point, 57 measured, 6 derived; section 13 "The record classes graded (#895)" | `1215bd82` | classes/ |
| R835-4-F1 MINOR | `Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriodsAfterTheLatestLeave` (the Leave at request + 10 JoinTime cs + CTRL_LOOP_TX_MS; 20,005 / 20,006 ms after it); three plants (drops the TX term, rounds it down, drops both), each caught by name at both counts | `a97a3c3e` | talker/, gates/ |
| R836-4-F1 MINOR | every listed passage restated or attributed; sections 5 and 13 provenance leads; section 5's head table | `1215bd82` | docs/ |
| R835-4-F2 MINOR | the four, and every other instance (inventory: 178 hits, none a superseded figure stated as this head's) | `1215bd82` | docs/superseded-inventory.md |
| RS1 (both) | PR roles: R835-4 / R836-4 with starts and verdicts; R835-5 / R836-5 next | PR-BODY.md | |
| R835-4-S1, S2 | taken (section 13); S1 reproduced (flip refuses at a 226 us base, tx 34.02) | `1215bd82` | flip-226.log |
| R835-4-S3 | retained, optional | | |

8x8/1if: record_classes.py reports it by class and never holds it; this lane has no 8x8/1if leg (lane 894b's point) and
ran none. The manager's note said "1x1/1if and 8x8/1if (and 8x8/2if reported)"; the grader holds 1x1/1if and 8x8/2if,
so both were graded on the preserved legs. A new 8x8/1if bank (every arm) is the only way to report that point.

## Commits (on `056d619d`)

| Commit | What |
|---|---|
| `a97a3c3e` | srp_talker.cpp's latest-Leave test; srp_talker_mutants.py's three hold-off plants. Test-side only. |
| `1215bd82` | docs: SPLIT_CONTROL_MEMORY.md (sections 5 and 13), FR_NFR 3.4.1, aecp/plat/harness READMEs. Markdown only. |

Changed after `056d619d`: docs/design/SPLIT_CONTROL_MEMORY.md, docs/reference/FR_NFR.md, sw/firmware/ctrl/aecp/README.md,
sw/firmware/ctrl/plat/README.md, tb/verilator/ctrl_service_budget/README.md (markdown); sw/firmware/ctrl/test/srp_talker.cpp,
sw/firmware/ctrl/test/srp_talker_mutants.py (non-markdown, test-side; no image input). Images: 552 of 552 identical to
`056d619d`'s (identity/compare-056d619d-1215bd82.txt); plat_ledger.py rc 0 (ledger-final/).

## Gates at `1215bd82` (each on its own fresh clean clone)

| Gate | Result | Receipt |
|---|---|---|
| docs.yml: wire-accountability, docs-check-no-git, docs-gates-0/1/2, docs-check | every job failed 0 (no-git's 3 steps rc 0, the driver's after-run git status the known artifact) | gates/workflows |
| rtl-fast: changes, bdd-conformance, firmware-unit, firmware-{control,aecp,srp}-mutants; rtl: full-ci-gate | every job failed 0; campaigns 716/716, AECP 299, SRP 421 (76 talker-), 0 escaped; fw_coverage PASS; srp_talker.cpp 12 tests at each count | gates/workflows, gates/campaigns.txt |
| verify (verify_wf.py, then verify_r10.py against round 9's table) | 86 ran, 53 carried (rc 0 at 056d619d, jobs reading no changed path), 226 reasoned, 0 bad | gates/verify-table.md |
| lane gates a | all rc 0 but flip_check / flip_check_8x8 (by design); harness_selftest 0 failures | gates/lane |
| the 27 workflow check scripts (worktree) | rc 0 | |
| record_classes.py, corrected survey, plants | PASS; UNDER 0 both points; the four plants refused | classes/ |
| ledger, identity | plat_ledger rc 0; 552/552 identical to 056d619d | ledger-final/, identity/ |

Carried from round 9's full pass at `056d619d` (their inputs unchanged, the images identical by sha256): rtl-fast's
verilator-lint, yosys-tool, yosys-elaboration, publication-census, split-cdc, firmware-boundary, firmware-verilator and
rtl-fast; rtl.yml's yosys-tool and yosys-shards; elaborate.yml; lane gates b and c; the four-shard sweep.

## Run history

- 20:37 relay read; both reports fetched from the evidence branch (FETCH_HEAD f32a9de6) and read in full. HEAD 056d619d,
  clean, no units; origin/895-talker-redeclare at 056d619d.
- 20:4x classes-real unit (8-15): record_classes.py over every preserved leg, PASS; the corrected survey (still with the
  record.aecp exemption) UNDER 0 at both points.
- 20:5x class-evidence unit (8-15): arm B's records by class; the four plants and two controls on the grader, the
  corrected survey (the exemption removed) and round 8's survey.
- 20:5x the latest-Leave test on the worktree: Talker arms PASS (12 tests at each count); plants.py talker-hold-off:
  the five then six hold-off plants caught at both counts. `a97a3c3e`.
- 21:0x the inventory of superseded figures (r10/superseded-hits.txt, before; receipts/docs/superseded-inventory.md,
  after); docs_r10.py and docs_r10b.py; doc gates rc 0; `1215bd82`. The 226 us flip probe on an export.
- 21:0x the corrected survey on the real legs (survey-final): UNDER 0 at both points, every class measured.
- 21:1x the 27 workflow check scripts on the worktree: rc 0. Clean clone r10/H at 1215bd82; ledger-final (40-47):
  plat_ledger rc 0; 552 of 552 image files identical to 056d619d's.
- 21:11 the gate queue (10 units) on pick8 ranges and the session pool (at most two there).
- 21:1x-22:1x the gate queue: every unit done, all green; verify_r10.py: 86 ran, 53 carried, 0 bad.
- 22:2x receipts INDEX.md (226 files, scrub idempotent, no host path, none over 200 KB); REVIEW READY posted once
  (#895 issuecomment-6901464046).

## For the manager

- Push `895-talker-redeclare` at `1215bd82` (two commits on `056d619d`); replace PR #901's body with round10/PR-BODY.md
  (the whole PR; its Round 10 section answers each finding; roles R835-5 / R836-5).
- For the running merge candidate of `056d619d`: no image input changed (552/552 by sha256); two non-markdown paths
  changed, both test-side (sw/firmware/ctrl/test/srp_talker.cpp, srp_talker_mutants.py), plus five markdown files.
  A native bank of `056d619d` covers this head's images; the firmware unit and the SRP campaign read the two
  test-side files, and they ran again at the head here.
- 8x8/1if: record_classes.py holds nothing there and this lane has no leg; reporting that point by class needs a new
  bank of every arm at 8x8-1if.
- The survey script is the author's evidence tool (round10/scripts/costs_vs_stated.py), not in the tree; the tree's own
  class grader (record_classes.py) is the authority and passes.
- Scratch: r10/H (the head's clone), r10/class-evidence (the planted leg copies, about 40 MB), r10/gates; the R8-* and
  R9-W8 builds the legs carry from. No unit of this lane runs.
- 22:3x removed r9/gates (round 9's job clones, its receipts kept), r9/H, and r10's probe export and worktree arm builds: the lane's scratch 18 GB -> 13 GB.
