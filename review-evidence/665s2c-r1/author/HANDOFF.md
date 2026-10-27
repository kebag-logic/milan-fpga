# [A685b] #665 lane S2c, re-base round: the instruction cache on S2's final harness (HANDOFF)

Status: **REVIEW READY**, 2026-10-27.

- Branch `665-s2c-icache`, local, not pushed.
  - Head: `a611785f2afe5bbe587f74034d869e869a1c8d37`. That is six commits on S2's final head `f58d049beb377c3f535628067022d4d5b51e8208` (PR #792, both reviews POSITIVE): [A685]'s five, re-based, and one commit from this round.
  - The pre-rebase head `2a7b0df5` is kept as the local ref `s2c-before-r5`. [A685]'s earlier ref `s2c-before-r3` (`17922860`) is untouched.
  - Lane base: `origin/dev-soft-core` `e76a755a`, verified as the merge base. `origin/dev-soft-core` has since moved to `9220f9b3`. The PR targets `dev-soft-core`.
  - Commits: one-line subjects, no body, no trailers (`receipts/rebase/checkout_identity.txt`).
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). No git command ran inside a submodule, and the submodule pointers equal S2's final.
- Assignment: issuecomment-6431653823. TAKEN: issuecomment-6431670158 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6432403705 (`REVIEW-READY-COMMENT.md`). The PR body for the manager is `PR-BODY.md`.
- Nothing pushed. No PR, issue or comment edit. No bench, no hardware, no flashing.
- No Vivado this round, and no new measurement: every figure is a regrade of [A685]'s logs on their attested builds.
- The re-base used `git cherry-pick` of the five commits onto `f58d049b`, on the local branch only, as the round's assignment directs.

## Contents

1. Result
2. Acceptance (this round's items)
3. Changes, file:line and reason
4. Checks, planted mutants and failing words
5. Gate table
6. Run history and reproducibility
7. Findings, decisions and open questions

## 1. Result

**The re-base changes no grade, so the round does not STOP.**

- Every arm was regraded at the re-based code on its attested build, from a copy of its logs (`scripts/regrade_rebased.sh`, `receipts/regrade/summary.txt`). There are 23 arms: 12 sweep arms, B1, B8, S1, S8, three controls and four XIP arms.
- Against the pre-rebase grade (`scripts/compare_rebased.py`, `receipts/regrade/compare_pre_rebase.txt`):
  - every per-group graded JSON is byte-identical, in every arm (0 arms with a changed group grade);
  - every printed summary is the same: the paths, instances and refusals missing T_svc, and the three controls' `CONTROL ... caught` lines;
  - `results.json` changes only in `composed_maximum`, which S2's round 4 added (`null` before);
  - `table.md` changes only in S2's round-4 and round-5 composed lines: the composed-window note, `Composed maximum over ...` and `Over the windows that released their whole load only: ...`.
- The cacheless tables are byte-identical to S2's final regrade (`receipts/regrade/cacheless_vs_s2_final.txt`): `P1-none` equals A1 (sha256 `a835c98b...`) and `P8-none` equals A8 (`599f1961...`).

What S2's final rules change in the lane's report (README and design doc, commit `a611785f`):

| Figure (arm A) | 1x1, none | 1x1, 4 KiB | 8x8, none | 8x8, 4 KiB |
|---|---:|---:|---:|---:|
| Composed maximum, every backlog window (round 4) | at least 31.32 ms | **at least 19.32 ms** | at least 44.19 ms | **at least 29.12 ms** |
| Over the windows that released their whole load only (labelled, not the composed maximum) | 14.81 ms | 8.60 ms | 27.84 ms | 14.03 ms |
| Arm B, partial: 3 of 4 windows, `backlog-adp-refill` not run (round 5) | 14.81 (S2) | 8.61 ms | 27.84 (S2) | 14.07 ms |
| Paths (instances) missing T_svc | 22 of 81 (58 of 141) | 13 of 81 (34 of 141) | 60 of 129 (102 of 182) | 34 of 129 (66 of 182) |

- The bound-talker windows (`backlog-adp`, `backlog-adp-refill`) never release SRP's 32 records, at every size and without the cache. So the composed maximum is a lower bound everywhere.
- Lower bounds do not rank the sizes: at 1x1, 2 KiB's 18.82 ms is below 4 KiB's 19.32. The size choice rests on the released windows, the same two at every size (`backlog`, `backlog-owed`), and on the path counts. The choice is unchanged: 4 KiB, one way.
- Window by window (`receipts/regrade/composed_windows.txt`), the cache shortens the released windows' longest passes by 36 to 50 %, and the unreleased windows' measured passes by 34 to 39 %. It releases none of them.
- The fan-out, stated whole, over both arms and every interface (`receipts/regrade/fanout_ranges.txt`):
  - a recipient costs 7,054 to 15,334 CPU cycles with the cache (7,144 to 13,114 in arm A), against S2's 11,786 to 22,030;
  - the 16 recipients at 1x1 take 4.42 to 8.70 ms, and all fit T_svc;
  - the 32 at 8x8 take 8.25 to 18.19 ms. 5 of arm A's 13 fan-outs and 10 of arm B's 22 miss, and none is over the 24 ms ceiling.
  - The same script reproduces S2's arm-A ranges exactly on the cacheless arms: 11,818 to 20,486; 7.77 to 11.33 ms; 12.39 to 22.98 ms.
- The residual, now on the composed maximum's pass (`receipts/regrade/composed_consumers.txt`). It is `backlog-adp-refill`'s at both points, under AECP's retry:
  - `memset` and `memcpy`: 65 % at 1x1 and 43 % at 8x8;
  - AECP, ACMP and `mrp_mad`: 18 % and 39 %;
  - the mailbox driver: 7 % and 6 %;
  - software arithmetic: 3 %.
  - On the released windows' longest pass the shares are [A685]'s: 40 and 42 %; 15 and 21 %; 21 and 12 %; 7 %. The same script reproduces S2's cacheless breakdowns exactly.

## 2. Acceptance (issuecomment-6431653823)

| Item | Status | Evidence |
|---|---|---|
| Re-base the five S2c commits onto `f58d049b` | met | `receipts/rebase/range_diff.txt`: commits 2, 4 and 5 are `=`. Commit 1 differs only in the `selftest.py` conflict's resolution, and commit 3 only in README context lines that S2 changed. |
| Resolve the harness conflicts toward S2's round-4 and round-5 rules: the composed maximum over every backlog window, the partial and lower-bound labels, the fan-out ranges | met | The code conflict is `selftest.py` (section 3). `run.py`'s composed maximum, labels and `results.json` record are S2's, unmodified. The README and design doc restate every S2c figure in those terms (section 3). |
| Re-run the self-test and mutants | met | rc 0: 92 checks (S2's 87 and this lane's 5), 67 of 67 mutants caught (62 and 5), `self-test: 0 failures`. The README's mutant table matches all 67 (`receipts/regrade/mutant_table_check.txt`). |
| Docs gates and `behave` | met | 0 of 97 gates nonzero or left the tree dirty; behave 406 of 406 scenarios (section 5) |
| Regrade every arm; cacheless tables byte-identical against S2's final | met | Section 1 |
| Bare-metal scope gate | met | `baremetal-only: OK`, rc 0 (section 5). S2's round 4 reworded `scenario.py:805`, the line that failed it at [A685]'s head. |
| No new measurement unless the re-base changes a grade; if it does, STOP | no grade changed, so no STOP and no new measurement | Section 1 |
| The PR body says "Relates to #665" and states the NFR-SCOUT-01 conflict as open for the owner | met | `PR-BODY.md` |

The lane's acceptance from issuecomment-6421463860 stands as [A685] recorded it ([A685]'s HANDOFF section 2), restated in S2's final terms. The PR stays "Relates to #665": T_svc is not closed, and NFR-SCOUT-01 awaits the owner.

## 3. Changes, file:line and reason

Line numbers are at the head `a611785f`. [A685]'s changes are unchanged in substance; its HANDOFF section 3 lists them.

| File:line | What | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/selftest.py:9-20` | The module docstring names S2's round-4 and round-5 synthetic checks and this lane's cache checks | Conflict resolution: both sides' content |
| `selftest.py:767-770` | `checks()` runs `maximum_checks()` (S2) and `cache_checks()` (this lane) | Conflict resolution: both rule sets run |
| `tb/verilator/ctrl_service_budget/README.md:534-541` | The sweep table: "composed maximum, every backlog window" (at least ...) and "over the windows that released their whole load only" | S2 round 4: the composed maximum is over every backlog window, a lower bound while one is unreleased |
| `README.md:544-552` | Why every size's composed maximum is a lower bound; that it does not rank the sizes; that the released windows are the same two at every size, so the choice rests on them | S2 round 4: the released-only figure is labelled and is not the composed maximum. S2's Findings: it is no baseline when its windows differ, and here they do not. |
| `README.md:555-565` | Arm A's longest pass in each backlog window, none against 4 KiB, at both points | S2's Findings compare the baseline window by window |
| `README.md:578-579` | Arm B's figure is partial: 3 of 4 windows, `backlog-adp-refill` not run | S2 round 5: the partial label |
| `README.md:595-601` | The consumers of the composed maximum's pass (`backlog-adp-refill`), and of the released windows' longest pass, labelled | The composed maximum's pass changed under S2's rule |
| `README.md:617`, `:633-646` | The fan-out table is labelled arm A; the ranges are stated whole over both arms and every interface: the cost a recipient, the time at each point, misses and ceilings | S2 round 4: the fan-out ranges stated whole |
| `README.md:711-718`, `:725-727` | The XIP table and text: the composed maximum (at least ...) and the released-only figure, labelled | S2 round 4 |
| `README.md:758-771` | The T_svc gap and residual, on the composed maximum (a lower bound) and on the released windows' longest pass, labelled | S2 round 4 |
| `docs/design/SPLIT_CONTROL_MEMORY.md:219` | The size reason names the released windows' longest pass, and says the lower bound does not rank the sizes | S2 round 4 |

## 4. Checks, planted mutants and failing words

No check or mutant was added this round. The re-based self-test runs S2's final checks and mutants with this lane's five of each:

- `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` prints 92 `PASS` lines, 67 `MUTANT caught` and `self-test: 0 failures`, rc 0.
- This lane's five checks, their mutants and their failing words are [A685]'s HANDOFF section 4, unchanged.
- `scripts/mutant_table_check.py` (S2's, unchanged) matches all 67 rows of the README's mutant table to the self-test's output, with 0 mismatches.

## 5. Gate table

Every gate ran at the head `a611785f2afe5bbe587f74034d869e869a1c8d37`.

- The runner is `scripts/gates_s2c.py`: S2's round-5 runner, copied, with S2c's `test_soc_options.py` added beside the builder gate. Only its docstring, that gate and the environment line that serves both builder-environment gates differ (`receipts/gates/runner_diff_vs_s2_gates_r5.txt`).
- It ran the gates one at a time, each to its own log, unpiped. It refused a dirty tree before starting and checked `git status --porcelain --untracked-files=all --ignore-submodules=none` after every gate.
- It was started detached and polled with foreground waits.
- Logs are in `receipts/gates/`, each with its rc and the tree's state on its last lines. `summary.md` is the runner's table with seconds, and `serial.out` its console.
- Two logs exceed 200 KB and are kept out of the packet by digest: `bdd_conformance.log` and `ci_events_selftest.log` (`<log>.digest.txt`).
- Inherited from S2's runner: the docs workflow's `measure_fail_fast.py --selftest` and `ci_fail_fast_selftest.py` share the log name `fail_fast_selftest.log`, so only the second log is kept. Both rows of `summary.md` are rc 0.

Environments:

- The Markdown gates ran with the pinned renderer's hash-locked environment (`tools/markdown/requirements.txt`, its sha256 prefix `40cdefe08ebd` matching), with PyYAML and the docs workflow's wavedrom.
- The HDL reference ran with `tools/hdl_reference/requirements.txt`.
- The CPU option test and the end-station builder ran with the product LiteX environment and the pinned RV32 SDK first on `PATH`.

**0 of 97 gates nonzero or left the tree dirty.**

| Gate (`receipts/gates/<gate>.log`) | Command | Result |
|---|---|---|
| `harness_selftest` | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 92 `PASS`, 67 `MUTANT caught`, `self-test: 0 failures` |
| `baremetal_check`, `baremetal_selftest` | `python3 scripts/check_baremetal_only.py --check`, `--selftest` | rc 0: `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))` |
| The docs workflow's check-mode commands: 87 gates, `wire_accountability_selftest` to `ci_events_selftest` in `summary.md`, without the next row | as listed in `scripts/gates_s2c.py` | rc 0 each. `check_em_dash: 0 finding(s) over 974 added line(s) in 3 changed Markdown page(s) ... [e76a755a..HEAD]`; `docs_check: 0 finding(s) across 211 md files + 1433 scrubbed text files`; `TOC gate: OK`; `anchor check: 552 existing cross-page fragment links reproduced`; `doc path gate: OK (1062 cited paths all resolve ...)`; `documentation style: OK`; `HYGIENE RATCHET: PASS` |
| `firmware_compiler_absent` | `python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>/rv32-absent.jsonl` | rc 0: `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations` (the compiled census, hidden in this mode by design) |
| `git_diff_check` | `git diff --check e76a755a HEAD` | rc 0 |
| `bdd_conformance` | `cd tests && behave` | rc 0: 14 features, 406 scenarios, 1977 steps passed |
| `hdl_reference_selftest`, `hdl_reference` | `python3 scripts/gen_hdl_reference.py --selftest`, `--output <scratch>` | rc 0 |
| `soc_options` | `python3 sw/builder/test_soc_options.py` | rc 0: 52 constructor and 18 CLI cases, 9 killed controls; `Split placement CPU: the instruction cache on the split CPU only, 3 killed controls`; `RESULT: PASS` |
| `builder_require_rv32` | `python3 sw/builder/test_builder.py --require-rv32` | rc 0: `ALL GATES PASS EXCEPT 1 NOT RUN`. Gate 11 needs a local Arty build report, as at [A685]'s head and in S2. 1,450 s. |

Outside the runner, at the head:

| Check | Command | Result |
|---|---|---|
| Regrade of every arm | `scripts/regrade_rebased.sh <checkout> <prior-scratch>/builds <scratch>/regrade-head` | rc 0 per arm, except the two 4 KiB XIP arms at rc 1, their refused probes as the runs gave. Every graded JSON and `table.md` is byte-identical to the regrade before the restatement commit (`receipts/regrade/head_regrade.txt`), and every group grade to the pre-rebase grade (`compare_pre_rebase.txt`). |
| Cacheless tables against S2's final | `cmp` | byte-identical, A1 and A8 (`cacheless_vs_s2_final.txt`) |
| README mutant table | `scripts/mutant_table_check.py` (S2's) | 67 rows, 0 mismatches |

Not re-run, from [A685]'s receipts. Nothing they read changed between `2a7b0df5` and the head (section 6):

- the all-fabric export digest (five shipped configs, base `e76a755a` against `f3c71e42`);
- Yosys and Vivado out-of-context pricing on 11 CPU netlists;
- the PMA comparison;
- the four-shard Verilator sweep (64 of 64 suites, `f3c71e42`).

## 6. Run history and reproducibility

- **The re-base.** The branch was moved to `f58d049b` and the five commits were cherry-picked in order.
  - One conflict, in `selftest.py`'s docstring and `checks()`, was resolved by keeping both sides.
  - `run.py`, `selftest_mutants.py` and `README.md` merged without conflict. Their merged diffs against `f58d049b` add only this lane's lines.
  - The other four commits applied cleanly. The pre-rebase head is the local ref `s2c-before-r5`.
- **Build inputs unchanged.** Between `2a7b0df5` and the head, `sw/`, `build.py`, `sim_main.cpp`, `observe.vlt`, `split_soc.py` and `MARK_II_AREA_PLAN.md` are byte-identical. `scenario.py` changed only in S2's round-4 comments.
  - So [A685]'s attested builds reuse, and its export digest, Yosys and out-of-context pricing, PMA comparison and four-shard sweep still describe the head's build inputs.
  - The sweep never runs this harness, which has no Makefile.
- **The regrade.** `scripts/regrade_rebased.sh` copies each arm's results to scratch and regrades the copy with `--regrade --out`, leaving the build's own results as the run wrote them. It took 11 s for 23 arms.
- **Analysis, no measurement.** `composed_consumers.py`, `fanout_ranges.py` and `composed_windows.py` read the graded JSONs only. Each reproduces S2's published cacheless figures before giving the cached ones.

## 7. Findings, decisions and open questions

1. **Requirement conflict, open for the owner.** `docs/reference/FR_NFR.md` NFR-SCOUT-01 reads "The release architecture MUST use one cacheless RV32I control hart"; `docs/ARCHITECTURE_HW_SW_SPLIT.md` repeats it. The owner's decision gives the split hart an instruction cache. The manager asked the owner (issuecomment-6431653823). Nothing here edits the requirement; `SPLIT_CONTROL_MEMORY.md` section 7 records the conflict.
2. **The cache does not close T_svc**, and under S2's final rule the composed maximum is a lower bound at every size: at least 19.32 ms at 1x1 and at least 29.12 ms at 8x8. S2b's next round runs on the cached core, per the manager's comment.
3. **[A685]'s inherited gate finding is closed.** `check_baremetal_only.py --check` failed on S2's `scenario.py:805` at `f8876638`. S2's round 4 reworded that line, and the gate is green at this head.
4. Open as before: the integrated route (M8a-2), hardware evidence, a data-cache measurement, and the self-test not run by a CI job.
