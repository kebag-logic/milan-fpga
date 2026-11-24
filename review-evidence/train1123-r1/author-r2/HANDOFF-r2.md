# HANDOFF r2: [A828], the post-flip composition lane (pf-train-1123 -> dev-soft-core), round 2

**Status: REVIEW READY (01:15 CET, 2026-11-24). No work remains in this lane, so there is no ETA.** The manager's
ruling on round 1's STOP ([#969 issuecomment-7116192252](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252))
is implemented in `kept_grade.py`. Round 1's formal legs were re-graded without re-simulating, since the image hashes
are unchanged. `kept_grade` passes at both points and in both arms with 0 findings. Every final-head gate passes.

- Final head **`43076d0f8c87b5118f6f4317d000a7eebdefc967`**, branch `pf-train-1123`, committed locally and **not
  pushed** (the manager pushes).
- One `[A828] REVIEW READY` is posted on #665:
  [issuecomment-7117784930](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7117784930). Its text
  is [REVIEW-READY.md](REVIEW-READY.md), the delta from `f5a1585e`.
- Outputs: [PR-BODY.md](PR-BODY.md) (one PR, `pf-train-1123` -> `dev-soft-core`, the seven PRs and their issues, the
  statement changes with figures, the ruling's link, no footer) and [ISSUE-output-map.md](ISSUE-output-map.md) (for
  the manager to file).

## Commits (f5a1585e..43076d0f)

| Commit | What |
|---|---|
| `93c5ad84` | Merge PR #959's reviewed head `8aeb2f0b` (#948; README only, its pin count 192). The tree is identical to `f5a1585e`'s, `db8dd481`: the composed README already said 192, so the count is kept as is |
| `4df6751e` | Merge live `dev-soft-core` `aa30d77f` (PR #961's merge). Its parents `854bd723` and `287ca1ee` are both ancestors of `f5a1585e`, and the tree is again `db8dd481`: **verified, it adds nothing** |
| `ce8454cb` | `kept_grade.py`: the ruling (below) |
| `43076d0f` | The harness README, `kept_window.py`'s docstring and the design page's train section record the amended conditions and the re-grade. **Final head** |

Both branches were fetched from `https://github.com/kebag-logic/milan-fpga.git`, and `ls-remote` gave the manager's
SHAs (`948-rx-fanout` `8aeb2f0b`, `dev-soft-core` `aa30d77f`). Receipt: `receipts/merge/merges-r2.txt`.

## The ruling in kept_grade.py (`ce8454cb`)

- **kept <= bound within the measurement rule.** The check is `kept * 100 <= bound * 105`, from
  `KEPT_MARGIN_PERCENT = 5`, which cites `record_classes.rule` and #665's ruling item 4. The KEPT <= BOUND line
  prints both figures, the signed difference and percentage, the allowance and the margin.
- **The bound path's build of one is OWED #977.** The line names the pass, its cost and the constant
  (`CTRL_LOOP_BUILD_ONE_PASS_US, not restated`). `run.py`'s STATED lines for that pass are owed through `OWED_KINDS`
  too: `a build-one pass of` and `a tier-2 slice of THE TRANSMIT's build of`. The bound path's passes over THE SHARE
  stay OWED, as before.
- **These stay findings:** the kept path's builds (whole and build of one) and its passes over THE SHARE, idle runs
  over THE SHARE in either group, and either group's pass given whole to THE TRANSMIT's build (two MRPDUs).
- **The comments cite #969 and #977**, and the amendment's URL is `AMENDED`. They carry no lane or review labels.
  Nothing restates `CTRL_LOOP_BUILD_ONE_PASS_US`, `CTRL_LOOP_SRP_UNIT_US` or any owner bound.
- **The self-test** has 19 checks before and 24 after. Kept 4 % over bound PASSES and 6 % FAILS; bound + 5 % holds
  and one cycle more fails. A kept pass over THE SHARE FAILS, and so does a kept build of one over its slice. A bound
  pass over THE SHARE alone, and a bound build of one, are OWED with no finding. A whole build over its cost fails in
  either group. Through `Disposition`, the bound build-one and build-slice lines are owed while the kept ones stay
  failures.
- **Ten planted defects** (scratch monkeypatches, not committed) are each caught by a named check
  (`receipts/budget/kept-grade-planted-r2.txt`).

**One interpretation, published in Open risks item 1.** `run.py`'s THE TRANSMIT slice line for `srp-bound` is owed
together with its build of one, because at 8x8/1if it is the same 171,645-cycle pass against the same 147,500 slice.
A bound whole-build pass stays a finding, because the ruling names the build of one only.

## The re-grade (no re-simulation)

`plat_ledger` at `43076d0f` passes with 0 findings and the same figures as round 1. All **24 image hashes are
identical to `f5a1585e`'s** (`receipts/ledger/plat-ledger-43076d0f.txt`). Since `f5a1585e`, only these four files
changed: `kept_grade.py`, `kept_window.py`, the harness README and the design page. So no budget leg was re-run.

| Point / arm | kept Failed vs bound (CPU cycles) | margin to bound + 5 % | srp-bound build of one | kept_grade |
|---|---|---:|---|---|
| 1x1/1if arm A | 36,631 vs 38,739 (-5.44 %) | +4,044 | 53,182 of 73,500 | PASS, 0 findings, 4 owed |
| 1x1/1if answering-ports | 35,435 vs 38,746 (-8.55 %) | +5,248 | 53,605 of 73,500 | PASS, 0 findings, 4 owed |
| 8x8/1if arm A | 142,582 vs 142,137 (+0.31 %) | +6,661 (to 149,243) | 103,782 of 147,500 | PASS, 0 findings, 5 owed |
| 8x8/1if answering-ports | 134,143 vs 138,016 (-2.81 %) | +10,773 | 171,645 of 147,500, OWED #977 | PASS, 0 findings, 6 owed |

- **`kept_grade` standalone** was run at the final head on round 1's views of each leg's `srp-kept` and `srp-bound`
  logs (`receipts/budget/kept-grade-*-r2.txt`, each with the logs' sha256).
- **`run.py --regrade` of the pair**, with `--record-budget-findings --record-share-findings`, exits rc 0 at all four
  legs with 0 refusals and 0 budget misses (`receipts/budget/run-regrade-*-r2.txt`).
  - The reuse check refuses a build whose firmware tree digest changed. The digest covers `sw/firmware/ctrl` and
    `sw/litex/ctrl_memory.py`, where round 1 changed only text after `c2b2ba1a`. It also refuses a build run from
    another path.
  - So the re-grade ran from round 1's measurement clone at `c2b2ba1a`, with only `tb/verilator/ctrl_service_budget/`
    checked out from `ce8454cb`, on copies of the logs. The clone was restored clean afterwards (porcelain 0).
  - Round 1's in-leg output at 8x8/1if `answering-ports` had "graded alone" findings because the scratch leg splitter
    put `srp-kept` and `srp-bound` in different parts. The pair re-grade grades them together, as the ruling requires.
  - The other groups' grades are unchanged, because `Disposition` touches only the `srp-kept`/`srp-bound` lines.
- **The kept path:** 0 passes over THE SHARE at both points. Its heaviest build of one is 86,018 at 8x8/1if and
  37,898 at 1x1/1if.

## Gate table (final head 43076d0f)

| Gate | Result | Receipt |
|---|---|---|
| kept_grade --selftest | **PASS**, 24 checks | `budget/kept-grade-selftest-r2.txt` |
| kept_grade planted defects | **10 of 10 caught**; unpatched PASS | `budget/kept-grade-planted-r2.txt` |
| Harness tree checks: load_grade, flip_grade (1x1/1if, 8x8/1if) and shape_costs `--check`; the five `--selftest`s; run.py --self-test; test_ctrl_memory | **PASS**, every rc 0. Load 0.512 / 0.744. run.py --self-test 0 failures, 295 MUTANT caught lines as at f5a1585e. test_ctrl_memory 0 failures. Porcelain 0 before and after | `gates/tree-checks-43076d0f.txt` |
| ctrl_boundary --require-rv32 --selftest | **PASS**: 0 findings, 117 boundary, 192 pin, 4 figure controls, 0 misbehaved | `gates/ctrl-boundary-43076d0f.txt` |
| Firmware gate, 4 shards | **Not re-run**: no firmware or test input changed since f5a1585e. The diff limited to `sw/`, `third_party/`, `configs/` and `hdl/` is empty, and nothing under `sw/` reads kept_grade or kept_window. It passed all four at f5a1585e | `gates/firmware-gate-inputs-unchanged.txt` |
| plat_ledger | **PASS**, 0 findings; 24 hashes identical to f5a1585e's | `ledger/plat-ledger-43076d0f.txt` |
| Docs workflow steps (5 jobs, fresh clone, em-dash base aa30d77f) | 56 steps rc 0 and 24 SKIP. docs_check 0 findings (223 pages), em-dash 0 over 762 added lines, the SV, C/C++, Python and Shell idiom gates PASS. The 3 RV32 SDK install-verify steps refuse, as in round 1 and on the bases (environment). Tree clean after | `docs/docs-workflow-steps-43076d0f.txt` |
| Routes | Not run: no RTL changed. Round 1's routes on identical images meet #818's floor | round 1 |

## Notes

- **CPUs.** The tree checks, ctrl_boundary, plat_ledger and docs steps ran as systemd user units
  `milan-train1123-a828-{tree,cb,ledger,docs}-r2`, on 16-CPU ranges booked through `cpu_ranges.py`. The four re-grades
  and the self-tests are pure-Python log reads and ran on the session pool. No Vivado.
- **Scratch.** `$VALIDATION_STORAGE/train1123-a828`: `regrade-r2/` (the log copies and run.py outputs), `clones/{tc,cb,lg}`
  at the final head, `ledger/43076d0f/`, `docs-43076d0f/`, `bin/docs_steps_r2.py` and `bin/kept_mutants_r2.py`.
- **A clone I removed.** I created `clones/rg` this session and removed it after a failed abbreviated-SHA fetch. I
  then recreated it at the full SHA and kept it; it is unused, since the reuse check needs the build's own clone path.
- **Receipts** are under `receipts/`, with `INDEX.md` generated from the files present. Host paths are replaced, and
  no file is over 200 KB.

REVIEW READY 43076d0f8c87b5118f6f4317d000a7eebdefc967
