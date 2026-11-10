# [A757] #867 (S7 of #665), round 2: the 20 ms egress allowance and two-sided Join spacing

Status: **STOP** at head `2131eff48066da1e3bbeb6b417ea0655fa7c7741`, on one line of the round 2 ruling's item 1 (below). Every gate run at that head is rc 0; the gate table is at the end. TAKEN: issue 867 comment 6763788175 (`TAKEN-COMMENT.md`). STOP: issue 867 comment 6765682668 (`STOP-COMMENT.md`).

Authority:
- the round 2 ruling (PR #874 issuecomment-6763709522), items 1 and 2;
- R814-1 (PR #874 issuecomment-6763695560), F-1 and F-2;
- #867 acceptance item 3;
- #665 issuecomment-6681686082, item 3.

Lane: `$LANES/665-s7-srp-tx`, branch `665-s7-srp-tx`, base `dev-soft-core` `1d6bf555`. Two commits were added on round 1's `5fb6904f`, with no merge, rebase, force or amend. Nothing is pushed.

| Commit | Subject |
|---|---|
| `0d8e89bc` | Grade the split's MRP spacing and the #608 stop at the approved T_svc of 20 ms, with the Join follow-up planted 1 ms past it and a control 1 ms inside, both at item 3's figure (#867) |
| `2131eff4` | Grade each Join timer's transmit opportunity on both sides of JoinTime's range widened by T_svc, with a short and a long timer planted 1 ms past it, their controls, and lwSRP Join timers of 10 and 15 centiseconds (#867) |

Only `tb/verilator/milan_dp/srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py`, `tb/verilator/milan_dp/README.md` and `sw/firmware/ctrl/srp/README.md` change. There is no RTL, firmware, lwSRP, fixture, Makefile, shape or generated-file change. The fixture (`srptx.hpp`) is untouched, and item 5 stays owed.

## The STOP line (ruling item 1, "derive `SVC_MS` from the one source the firmware budget uses, not from a literal")

At this base no source the firmware budget uses holds 20 ms for SRP:

| Source | At `1d6bf555` | SRP bound it gives |
|---|---|---|
| `tb/verilator/ctrl_service_budget/scenario.py:91`, `:99` (the CPU budget harness; `nvm_split_target/target_grade.py` imports it) | `T_SVC_MS = 10.0` ("proposed"), `CEILING_MS['srp'] = 18.0` | 10 ms (T_svc) or 18 ms (ceiling) |
| `tb/verilator/ctrl_service_hooks/hooks.py:44`, `:84` | `T_SVC_MS = 20.0`, `bound_ms = min(T_svc, ceiling)` | 18 ms. Its docstring (`:9-12`) says the 2026-11-06 bounds "grade nothing, until #810 brings them" |
| `tb/verilator/ctrl_split_boot/run.py:74` | `T_SVC_MS = 10.0` | 10 ms |
| `docs/reference/FR_NFR.md:333` | "Proposed project budget: T_svc = 10 ms" | 10 ms |

The 20 ms values exist only on S2b's branch (`origin/665-s2b-cycles` `scenario.py:86`, `:94`).

Deriving `SVC_MS` from that source here gives 10 or 18 ms. Both are tighter than item 3's 20 ms; the 18 ms figure is the one F-1 refused. Editing that source is S2b's change (#810), and would change S2's harness, the hooks and the NVM split target's bounds, all outside this lane.

So `srptx_grade.py:64` holds `SVC_MS = 20` with its authority cited. Every bound is derived from it: `:74`, `:75`, `:78`, `:79`, and the `[608]` window at `:544`.

The decision needed is one of:
- (a) accept the literal until #810 lands, with switching to the budget source as a residue;
- (b) derive from `scenario.py` now, at 10 ms, which fails item 3's controls by design;
- (c) take S2b's bound change into this lane.

I recommend (a). The plants hold item 3's figure apart from the grade's, so the literal cannot drift unrefused (`plant-probe.txt`).

The other exit does not apply: every Join timer interval of the unplanted runs lies inside the two-sided bound.

| Scenario | MSRP N, min to max | MVRP N, min to max | Outside 160 to 260 ms |
|---|---|---|---|
| wire | 104, 198.989 to 200.000 ms | 104, 198.989 to 200.015 ms | 0 |
| hold | 34, 198.989 to 200.000 ms | 32, 198.989 to 200.000 ms | 0 |
| licence | 8, 198.989 to 200.000 ms | 5, 198.989 to 200.000 ms | 0 |

(`receipts/srptx/join-figures.txt`)

## Changes (file:line at `2131eff4`, reason)

F-1 (`0d8e89bc`):
- `tb/verilator/milan_dp/srptx_grade.py:61-64`: `SVC_MS = 20`, the approved T_svc (#867 item 3; the 2026-11-06 ruling). It replaces `min(T_SVC_MS 20, MRP_CEILING_MS 18)`, the superseded per-family rule. Reason: F-1.
- `srptx_grade.py:18-25`: the docstring states the allowance and its authority. `:319-320`, `:328-330`, `:355-356`, `:369-371`, `:546`: the finding words say "T_svc", no longer "the MRP service bound".
- `srptx_grade.py:633-635`: `--plant` grades a control, which must be clean.
- `srptx_plants.py:25-31`: `ITEM3_SVC_MS = 20`, item 3's figure, held apart from the grade's. `FOLLOW_MS` and `LEAVE_ALL_BOUNDS_MS` are derived from it. Reason: a plant derived from the grade follows any drift of the grade, so it could not have caught F-1. A plant at item 3's own figure does.
- `srptx_plants.py:54-56`: the plant `join-late-in-t-svc` becomes `join-late-past-t-svc`. It moves the second MSRP frame and the adapter's record of it to 221 ms after the first, 1 ms past 220 ms. The old name said "inside T_svc", so it was renamed.
- `srptx_plants.py:97-99` (`WITHIN`) adds `join-late-within-t-svc` at 219 ms, which must grade clean. `:105-110` (`TIMING`), `:149-178` (`leave_all`, `move`, `plant_timing`), `:274-310` (`planted_findings`, and the controls in `main`).
- `move` also moves the adapter's record, so `[TX]` stays clean and a control can be required to have no finding at all.
- `srptx_plants.py:52-53`, `:69-71`: the `join-late` and `leave-all-missing` words carry item 3's 220 ms and 9,780 to 15,220 ms.
- `srptx_mutants.py:24`, `:55-57`, `:64-67`: the 23-centisecond and LeaveAll arms take their words from the grade (`g.JOIN_FOLLOW_MS`, `g.LEAVE_ALL_BOUNDS_MS`). Reason: one statement of each bound.
- `tb/verilator/milan_dp/README.md:1554` (`[TIME]` row, citing item 3 and issuecomment-6681686082), `:1556` (`[608]`), `:1602-1603`, `:1620-1623` (the plants intro), `:1633-1634`, `:1638`, `:1653-1659` (the controls), `:1679`, `:1682`, `:111` (contents description); `sw/firmware/ctrl/srp/README.md:384`.

F-2 (`2131eff4`):
- `srptx_grade.py:70-71`: `JOIN_RANGE_MS = (180, 240)`, Milan v1.2 Table 4.3 (`FR_NFR.md` 3.4.1). `:76-78`: `JOIN_BOUNDS_MS`, that range widened by T_svc on each side (160 to 260 ms), as LeaveAll's is (the ruling's item 2).
- `srptx_grade.py:385-404`: `causes` and `join_intervals`, factored out of `measure_time`. `:407-424`: `measure_time` uses them. Its measured block is identical to round 1's in every scenario (`receipts/srptx/measured-identical.txt`).
- `srptx_grade.py:323`, `:331-336`: `grade_time` grades each Join timer interval two-sided, citing IEEE 802.1Q-2018 10.7.4.1, 10.7.11, Table 10-7 and Milan v1.2 Table 4.3.
- **Why the range, not 200 ms ± T_svc.** A frame delayed within T_svc shortens the interval after it. A frame 219 ms after its predecessor leaves the next 179.99 ms later (the 200 ms timer grid less the 1.01 ms first arm). A bound of 180 ms would refuse that frame, which item 3 allows.
- `srptx_plants.py:57-66`: two plants.
  - `join-early-past-t-svc`: a short Join timer. The second and third MSRP frames, their records and their Join expiries and re-arms move earlier, so the second leaves 159 ms after the first.
  - `join-interval-late`: a long Join timer. The second and third Join frames after the first MSRP LeaveAll move later, the second at 261 ms. No New is followed there, so only the new check sees it.
- `srptx_plants.py:100-103`, `:111-114`: their controls at 161 and 259 ms.
- `srptx_mutants.py:31-34`: `JOIN_ARM`, the shared anchor, and `JOIN_SPACING`, the grade's words. `:58-63`: lwSRP Join timers of 10 and 15 centiseconds (`ps->join_cs - 10u`, `- 5u`), the ruling's arms.
- `README.md:1554` (the range clause and 10.7.11), `:1603-1609`, `:1635-1636`, `:1660-1661`, `:1680-1681`, `:111`; `sw/firmware/ctrl/srp/README.md:384` ("on each side").

## Checks, planted mutants and failing words

| Check | Plant or mutant | Refused by | Without the new check |
|---|---|---|---|
| `[TIME]` follow-up, at 20 ms (F-1) | `join-late-past-t-svc`, 221 ms | `followed at ms 222, past JoinTime + T_svc (220 ms` | not applicable (the existing check, re-bound) |
| the same, inside | control `join-late-within-t-svc`, 219 ms | none: graded clean | |
| `[TIME]` Join interval, low side (F-2) | `join-early-past-t-svc`, 159 ms | `a Join timer's transmit opportunity at ms 160, 159.000 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` | 0 findings (`plant-probe.txt`) |
| the same, inside | control `join-early-within-t-svc`, 161 ms | none: graded clean | |
| `[TIME]` Join interval, high side (F-2) | `join-interval-late`, 261 ms | `a Join timer's transmit opportunity at ms 15021, 261.000 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` | 0 findings |
| the same, inside | control `join-interval-late-within`, 259 ms | none: graded clean | |
| `[TIME]` Join interval, code (F-2) | lwSRP Join timer of 10 cs: MSRP at ms 1, 100, 200 | `ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms`, three times (98.989, 100.000 ms MSRP; 98.989 ms MVRP) | 0 findings (`mutant-probe.txt`) |
| the same | lwSRP Join timer of 15 cs: MSRP at ms 1, 150, 300 | the same words, three times (148.989, 150.000; 148.989 ms) | 0 findings |

R814-1's third arm, a 17-centisecond timer (MSRP at ms 1, 170, 340), is not refused, because 170 ms lies inside 160 to 260 ms. It is not a committed arm. The ruling names the 10 and 15 cs arms, and the probe records the 17 cs result (`mutant-probe.txt`).

**The plants pin the allowance** (`plant-probe.txt`, the grade's constants re-derived in-process):

| Allowance | Plants refused | Controls clean | What fails |
|---|---|---|---|
| 18 ms | 20 of 25 | 0 of 3 | the 18 ms figure F-1 refused: every control refused, including `join-late-within-t-svc` at 219 ms |
| 22 ms | 20 of 25 | 3 of 3 | the five plants at item 3's bounds escape |
| 20 ms | 25 of 25 | 3 of 3 | nothing |

## Gates (clean clones of `2131eff4`; receipts under `receipts/`, index `receipts/INDEX.md`)

| Gate | Head | rc | Result | Receipt |
|---|---|---|---|---|
| `make srptx` | `2131eff4` | 0 | wire, hold, licence: 0 findings each. Every Join timer interval is 198.989 to 200.015 ms. Each report's measured block equals round 1's | `srptx/make-srptx.txt`, `srptx/*-report.json.txt`, `srptx/join-figures.txt`, `srptx/measured-identical.txt`, `srptx/captures-sha256.txt` |
| `make srptx-plants` | `2131eff4` | 0 | `srptx plants: 25 of 25 refused; 3 of 3 controls inside their bound clean` | `srptx/make-srptx-plants.txt` |
| `make srptx-mutants` | `2131eff4` | 0 | five clean controls, then `srptx mutants: 12 of 12 refused` | `srptx/make-srptx-mutants.txt` |
| the gate clone after those three | `2131eff4` | 0 | `git status --porcelain` empty | `srptx/gate-clone-clean.txt` |
| the plant probe | `2131eff4` | 0 | with the new check off, the two new plants grade with 0 findings. At 18 ms, 0 of 3 controls are clean; at 22 ms, 20 of 25 plants are refused; at 20 ms, 25 of 25 and 3 of 3 | `srptx/plant-probe.txt` |
| the mutant probe | `2131eff4` | 0 | 10 cs and 15 cs: 3 findings each with the arm's words, and 0 with the new check off. 17 cs (R814-1's, not committed): 0 | `srptx/mutant-probe.txt` |
| every `run:` step of every docs.yml job a pull request to dev-soft-core runs (9 instances), and rtl-fast `changes`, `firmware-boundary` (LiteX venv) and `firmware-verilator`, each job on its own clean clone (`tools/ci_replay.py`) | `2131eff4` | 0 | 120 steps ran, all rc 0; 11 cannot run here, each with its reason (APT resolution, a Verilator source build already pinned here, hosted-only GitHub API steps). Both boundary jobs: `ctrl_boundary: PASS`, 0 findings, 183 pin controls | `ci/ci-replay-table.md`, `ci/not_run.json`, `ci/key-verdicts.txt`, `ci/attempts.txt` |
| `git diff --check 1d6bf555 2131eff4` | `2131eff4` | 0 | clean | `gates/diff-check.txt` |

Earlier attempts and their causes are in `receipts/ci/attempts.txt`; none is a defect of the change. `docs-check` first ran before the docs-gates jobs, because the first driver misnamed them; it was set aside and re-run after them.

Before committing, the working tree also passed `check_py_idiom.py` (after two over-long lines were wrapped), `gen_toc.py --check`/`--verify-anchors`, `check_doc_style.py`, `check_doc_paths.py`, `check_em_dash.py --base 1d6bf555`, `check_hygiene.py --check`, `check_todo_ownership.py`, and `measure_test_evidence.py`/`measure_naming.py`/`measure_fail_fast.py --check`. The docs jobs above re-ran them on clean clones.

No hardware, bench, Vivado, flashing, push or PR edit.

## Not run at this head, and why

The full sweep (4 shards), the firmware self-test, `fw_coverage.py --check`, the firmware mutant drivers, S2's harness at 1x1/1if and 8x8/2if, `test_builder.py --require-rv32`, `cd tests && behave`, the rtl and elaborate workflows, and the other rtl-fast jobs are not run here. The ruling's done-means asks for them at the final head, and this head stops on a decision that may add a commit. The efficiency rule runs the full clean-clone pass once, on the final head. The round 2 commits change only the three `srptx_*.py` scripts and two READMEs, and none of those gates reads them: no workflow and no sweep suite runs `srptx` (`make run` in `milan_dp` has no srptx case). Round 1's full pass at `5fb6904f` is in `665s7-a757/receipts/`.

The lane tree is clean at `2131eff4`. Its gitignored build outputs under `tb/verilator/milan_dp` (`obj_twin_fw/`, `obj_twin_sp/`, `gen_divergent/`, the three `.hex` files) date from round 1 (2026-11-09) and were left in place.

Scratch: `/data-2/milan/tmp/665s7-a757b` (the gate clones, the replay's job clones, the docs venv, the probes' builds). Its `sdk` is a link to round 1's verified RV32 SDK.
