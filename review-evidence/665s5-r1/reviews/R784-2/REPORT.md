[R784] NEGATIVE - exact head 26ba56e1d5749a71668f9e4436f28e8635f03f95

# R784-2: external review of #665 lane S5 (PR #844), round 2

Head `26ba56e1d5749a71668f9e4436f28e8635f03f95`, tree `47d25f3f8b51c5917f2575950612e5977562b730`. Delta reviewed: `eef3d97a..26ba56e1`, four commits, on the ruling in issuecomment-6677495623 and the grading answer in issuecomment-6682851386.

The measurements are sound. Every round 2 item is delivered, and all four prior MINOR findings are resolved. The verdict is NEGATIVE on two open MINOR findings:

- **F-1:** the audit claim the brief asked me to check does not hold. Two mutants never reach the rule they name, and one of those rules is "the column grades nothing".
- **F-2:** "the amended bounds change no verdict" is not true of the per-descriptor rows this round added.

Both are small to fix, and neither changes a measured figure.

## Focus checks

| Asked | Result | Evidence |
|---|---|---|
| Verdicts stay on the bounds at the base; no verdict reads the amended column | **Confirmed** | All 756 published rows recompute from the base bounds, 0 differ. `run.summary` with the amended functions set to raise reproduces every published summary. The only readers are `run.py:192,206,215`, all in `table()` (`receipts/verdict_independence.txt`, `receipts/amended_readers.txt`). |
| Per-descriptor rows beside the ALL-push row | **Confirmed** | 5 rows at 1x1 and 19 at 8x8, with `counters.all` kept. My own build and run of `hooks-counters` at both points gives all 30 rows identical in every field to the published run, from a different executable (`receipts/compare_repro.txt`). |
| All 732 round 1 paths reproduce to the cycle | **Confirmed** | 732 of 732 rows identical in every field, not only cycles. The only new rows are the 24 per-descriptor ones. Findings, refusals and ordering checks are unchanged apart from those rows (`receipts/compare_runs.txt`). |
| Each of the 79 mutants fails on its own rule | **Not confirmed** | 79 of 79 fail through an assertion and none through a crash, but 2 fail on a different rule (F-1). |
| The queued ceiling applies only to the ALL-push rows | **Confirmed** | The column differs from the bound on two kinds of row only: H-SRP (+2 ms, all 72 rows) and `counters.all*` at 8x8 (+40 ms, 20 rows). `counters.first`, `.held`, `.loaded` and both fan-outs keep their bound (`receipts/amended_table.txt`). |

"Each hook within its bound" stays open as ruled, and is not reported here.

## Findings

### F-1 [R784] MINOR Tests, Docs - `tb/verilator/ctrl_service_hooks/hooks_selftest.py:753-757,700-704,843` and the PR body's Round 2 table, item 2 - two mutants never reach the rule they name

- **Authority/evidence.** AGENTS section 6 (Tests): each test can fail for the defect it claims to detect. The PR says: "An audit of all 79 mutants finds each fails on its own rule, none on an incidental exception." `receipts/assert_sites.txt` records the assertion line each mutant actually fires.
  - **`aging: the window opens before the arm (the earlier rule)`.** Its stand-in group has no `reply` steps, so it fails at `:589`, "the PROBE_TX answers []". It never reaches the rule it names, `:599` `armed < mark`.
  - **`amended: the column grades a path`.** It rewrites `bound_ms`, and `amended_ms` derives from `bound_ms`, so it fails at `:544` with `SRP 22.0`. That is a side effect on the column's arithmetic. It never reaches `:553` or `:556`, the two assertions that say nothing was graded by the column.
  - **Deleting the rules proves it** (`receipts/rule_probes.txt`). With `:599` deleted the self-test still reports 28 of 28 and 79 of 79. With `:553-554` and `:556` deleted it reports the same.
  - The published audit shows both messages (`probes/mutant_audit.txt:26,78`) but marks them `ok`. These are the same class as the two hollow mutants the author fixed this round: the mutant stops at something other than its rule. Here the stop is a failed assertion rather than a setup crash, so a search for exceptions would not find them.
- **Impact.** Nothing measured is wrong: the assertions themselves work, and sharper mutants fail on them (probes D1, D2, D3). The gap is in the gate. `the column grades nothing` is the property the grading answer depends on, and no mutant holds it in place, so that check could lose those assertions with the self-test still green.
- **Required outcome.** Each named mutant fails on its own rule, and the PR's audit sentence is true of all 79.
- **Verification.** The aging mutant keeps the real group and moves only the marks, so it fires `:599` (D1 in `scripts/rule_probes.py` is one shape). The grading mutant leaves `bound_ms` alone, so it fires `:553` (D2), and a finding-level mutant fires `:556` (D3). Then repeat probes B and C: each deletion must now make its mutant escape.

### F-2 [R784] MINOR Docs - `tb/verilator/ctrl_service_hooks/README.md:444` and the PR body's Round 2 table, row "Grading" - the amended bounds do change four path verdicts

- **Authority/evidence.** AGENTS section 6 (Docs). The PR says: "the amended bounds change no verdict: no H-SRP path lies between 18 and 20 ms, and the ALL push stays over its ceiling". README:444 says they "would change none of them", with the same two reasons.
  - Those reasons leave out the per-descriptor rows, which the same column raises to 60 ms at 8x8.
  - Four rows are over 20 ms and within 60 ms: `counters.all.t5.i1` 21.70, `.t5.i2` 33.43, `.t5.i3` 44.89 and `.t5.i4` 57.15 (`receipts/amended_table.txt`).
  - README:454 has the true count, 14 of 19 over the ceiling against 18 of 19 over 20 ms, so the README disagrees with itself.
  - The claim does hold at hook level: H-COUNTERS still misses either way, and no H-SRP path changes.
- **Why MINOR and not RESIDUE.** The fix is wording, but the sentence is itself a claim about verdicts, and it concerns the rows the round added and the question the owner still has open (one path or per descriptor). The owner rule sends doubt to MINOR. No figure changes.
- **Impact.** A reader of the PR would take it that the amended column moves nothing, on exactly the row kind whose reading is undecided.
- **Required outcome.** Replace README:444's second sentence, and say the same in the PR's Grading row: "For information, the amended bounds would change no hook's verdict: no H-SRP path lies between 18 and 20 ms, and the ALL push as one path stays over its ceiling at both points. Per descriptor, four rows at 8x8 (`counters.all.t5.i1` to `t5.i4`, 21.70 to 57.15 ms) are over 20 ms and within the 60 ms ceiling."
- **Verification.** Read the two sentences against `receipts/amended_table.txt`.

### RESIDUE-1 [R784] RESIDUE Docs - `tb/verilator/ctrl_service_hooks/README.md:454` - "leaves" for a commit

- **Evidence.** "Its first notice leaves after 2.76 and 4.68 ms." The figure is a mailbox commit, and README:492 says wire departure is not measured.
- **Exact fix.** "Its first notice is committed after 2.76 and 4.68 ms."

### SUGGESTION (optional)

- **S-1 (Tests) - `hooks_selftest.py:529-564`.** A `NARROW` slack computed from the amended bound escapes all 28 checks (probe D5), and a hook's over-its-bound count read from it is caught only by another check, and only by chance (D4). The head reads neither, but `check_amended` could pin both while F-1 is open.
- **S-2 (Robustness) - `hooks.py:78,96`.** `startswith('counters.all')` has no dot boundary, so a future `counters.allowed` would take the ceiling. `path == QUEUED_PATH or path.startswith(QUEUED_PATH + '.')` is exact.
- **S-3 (Conformance, for #810's re-grade) - README:168.** Ruling 6682851386 gives the first notice 20 ms and queued notices the ceiling. The column gives each row the ceiling, including the first descriptor's. The first-notice half is met today (2.76 and 4.68 ms), and one sentence saying so would help the re-grade.
- **S-4 (Tests) - `receipts/assert_sites.txt`.** 52 `expect` lines are fired by no mutant, including every ordering check's defective-log branch (`:188,:208,:232,:254,:269,:314,:329`). This does not show those lines cannot fail, and the PR makes no claim about them; it lists where mutants could be added.

## Prior findings, resolved or retained at this head

These were read after my verdict and ledger were recorded (`receipts/verdict_before_prior_findings.txt`).

| Finding | Status | Evidence at this head |
|---|---|---|
| R784-1 F-1 = R783-1 F1, `counters-late` caught with no plant | **Resolved** | Round 1's vacuity probe now prints `ESCAPED`, rc 1 (`receipts/plant_vacuity_probe.txt`). My real unplanted run's 3 LATE findings match no catch rule (`receipts/prior_resolution.txt`). On the published unplanted runs 0 of 16 rules match (`receipts/doc_figures.txt`). The published real plant is caught on `counters.first.if0`, 81.819 ms, and the published no-op ends `ESCAPED`, rc 1. |
| R784-1 F-2, grading rules unchecked | **Resolved** | Its three extra mutants each fail a named check (`receipts/extra_mutants.txt`). |
| R783-1 F2, `ctrl_configs.py` | **Resolved** | The file equals its base. No file outside `tb/verilator/ctrl_service_hooks/` differs. The harness no longer names the firmware tree by text. Published boundary receipts at this head: `ctrl_boundary: PASS`, rc 0, in both modes. |
| R784-1 RESIDUE-1 = R783-1 R1; R783-1 R2 | **Resolved** | Neither wording remains in any `.py` of the harness. |
| R784-1 RESIDUE-2, RESIDUE-3 = R783-1 S4 | **Resolved** | README:15, :440-441 and the PR's Status bullets. |
| R784-1 S-2, direct run of the self-test | **Resolved** | `hooks_selftest.py` run directly gives 28 of 28 and 79 of 79, rc 0 (`receipts/selftest_standalone.txt`). |
| R783-1 S1 P1, P12 | **Resolved** | Pinned by `summary:` and `ALL:` mutants. |
| R783-1 S1 P2, P3, P4, P9; S2; S3 = R784-1 S-1; S5; S6; R784-1 S-3 | **Retained, optional** | Declined in the PR as outside the four assigned items. |

## Lens results

```text
[R784] PASS Conformance - hooks.py:71-103, run.py:190-215, four published table.md and results.json, receipts/verdict_independence.txt, amended_table.txt, compare_repro.txt - verdicts against the base bounds, SRP 18, per ruling 6682851386; both H-COUNTERS row kinds present per ruling 6677495623; column at SRP 20 plus W and the ceiling 20/60 on counters.all* only; recipients 16 and 32 per Milan v1.2 5.3.4.2 as ruled
[R784] PASS RTL - git diff 5b5f4336..26ba56e1 (six files, all under tb/verilator/ctrl_service_hooks/) and git diff eef3d97a..26ba56e1 (hooks_soc.py absent) - no RTL or firmware in the delta, test gateware unchanged since round 1, so its round 1 result stands
[R784] PASS Robustness - run.py:251-259, hooks.py:349-356, hooks_build.py:93-96, run.py:304-308 - a late plant needs its exact path up to the colon, so control.discover.if01 does not match; an unmeasured per-descriptor row is a refusal and fails the run; a changed group script refuses a stale regrade; the moved FIRMWARE path built and ran here at both points
[R784] MINOR Tests - hooks_selftest.py:753-757,843 - two mutants do not reach their rule (F-1)
[R784] MINOR Docs - PR body item 2 - the audit claim (F-1)
[R784] MINOR Docs - README.md:444, PR body row Grading - four path verdicts do change (F-2)
```

Docs otherwise checks out. All 64 hook-table cells match the results, all 24 per-descriptor rows match my own runs, and README lists all 79 mutants by exact name. The LATE counts 28, 31, 38 and 60 match. Later-commit scope is as stated: after `d5add6f9` only `run.py`'s printed line, one self-test line and the README change. Comment rule: no new lane label, reviewer ID, round or comment ID in any added `.py` line; the only grep hits are the word `round` in Python code.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `hooks.py:71-103`, `run.py:190-215`, published tables and results, rulings 6677495623, 6681686082, 6682851386 | R784-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| RTL | CLEAN | Delta file list; no file under `hdl/`; `hooks_soc.py` unchanged | R784-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| Robustness | CLEAN | `run.py:251-259,310-316`, `hooks.py:349-356`, `hooks_build.py:93-96`, own builds at both points | R784-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| Tests | UNCLEAN (F-1) | `hooks_selftest.py` whole; `receipts/assert_sites.txt`, `rule_probes.txt`, `mutant_audit.txt`, `extra_mutants.txt` | R784-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| Docs | UNCLEAN (F-1, F-2) | README lines 160-209 and 295-504, PR body, `receipts/doc_figures.txt`, `amended_table.txt` | R784-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |

## What I ran

All at the exact head, under the scoped Verilator 5.050 (identity verified):

- `run.py --self-test` and `hooks_selftest.py` directly: 28 of 28, 79 of 79, rc 0.
- `run.py --point 1x1|8x8 --arm answering --groups hooks-counters --record-findings`: rc 0, 8 and 22 rows.
- In-memory probes of the self-test source (`scripts/rule_probes.py`, `assert_sites.py`, `mutant_audit.py`). Nothing was written to the tree.
- Recomputation over published receipts (`scripts/compare_runs.py`, `amended_table.py`, `verdict_independence.py`, `doc_figures.py`), which also regenerated all four `table.md` files byte for byte at this head.
- 58 fetched evidence files checked against the evidence `MANIFEST.json` (432 entries), 0 mismatches.
- Round 1's `plant_vacuity_probe.py` and `extra_mutants.py`, read first, then run.

After the probes the tree is at exact head: 0 changed paths, index blobs and modes equal the tree, and the six gitlinks are unchanged (`receipts/head_integrity.txt`). `external` was already uninitialised. Two ignored `__pycache__` directories my session created were removed.

## Real limits

- I ran only `hooks-counters`, on the answering arm. That re-simulated 6 of the 732 round 1 rows (`counters.first`, `.all` and `.held` at each point) and the 24 new rows. The other 726 rest on the published receipts.
- I did not re-run the 16 plants, the no-op control, the firmware self-test, the builder, the boundary gate or the docs gates. Those rest on the author's published receipts, some at `78415f7a` and `d5add6f9`; only the README or printed-line changes above separate those commits from this head.
- The amended column carries the ceiling, not the derived bound, which is #810's. Nothing here tests the amended bounds themselves.
- Hosted snapshot at review time: 48 contexts, 43 pending, 4 passed, 1 skipped (`Physical gPTP`), so this is no evidence of hosted success (`receipts/hosted_checks_snapshot.txt`).
- Physical calibration was not run, and field skips are not hardware proof. No manager source bank exists at this head, and none is claimed.

## Pending manager duties

- Carry F-1 and F-2 to the author, and RESIDUE-1 to the residue checklist.
- Rule on the column's assumption if wanted: the queued ceiling on the ALL-push rows only, which the code does as the author states.
- Own hosted and act acceptance at the exact head.
- Build and validate the current-dev merge candidate at the merge turn (source base `5b5f4336`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`), and link its receipts on the PR.
- Merge needs the full bar: two independent positive reviews, all five lenses covered clean at the merge head, and maintainer authorisation.

R784-2 FINISHED
