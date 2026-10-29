# [A683k] #665 lane S2b round 9: T_svc = 20 ms approved, each family graded against min(T_svc, its ceiling) (HANDOFF)

**Status: REVIEW READY** (2026-10-29) at `bf1773c0eabf0ba7fa1b1268c2a714e6b636e6eb`. Every composed row the CPU decides fits its own bound at both points (1x1/1if, 8x8/2if), on both arms, with both drafts staged and without them. The STOP condition does not hold. The only rows over their bound are the three egress-held ones (tsn-c-stack #26). No RTL changed.

- Branch `665-s2b-cycles`, local, not pushed. Head `bf1773c0eabf0ba7fa1b1268c2a714e6b636e6eb`: five commits on round 8's final head `59038a1d7c8ec65417fc74d7fb64804d7075e3fe`, whose commits stay.
  - Lane base `origin/dev-soft-core` `e76a755a`, checked as an ancestor (not dev). The PR targets `dev-soft-core`, which is now `f4c9ad4f` with S1's PR #795 merged (section 7: the merge conflicts).
- Remote `https://github.com/kebag-logic/milan-fpga.git` (checked). No git command changed a submodule of the lane. Each submodule was checked to be its own top level with its own origin before use. The drafts were staged in scratch clones only.
- Assignment: issuecomment-6495692075 (`ASSIGNMENT-A10-6495692075.md`). TAKEN: issuecomment-6495860708 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6497614101 (`REVIEW-READY-COMMENT.md`).
- CPU and memory:
  - every heavy job ran as its own transient unit (MemoryMax 6 to 8 GB), on this session's 112-127 and on 0-15 while `cpu_ranges.py` showed it free;
  - no full sweep (no RTL change);
  - MemAvailable stayed above 22 GB; the other lanes' units held most of what moved.
- Vivado: only the xvlog front-end gate, under `$VIVADO_LOCK`, exclusive, started in the background at 34.7 GB MemAvailable with no other Vivado run. No route ran.

## Contents

1. Outcome against the assignment
2. Changes (file:line, reason)
3. New checks, planted defects and failing words
4. Method
5. Measurement
6. Gates
7. Findings, conflicts, decisions needed
8. Run history

## 1. Outcome against the assignment

| Item | Outcome |
|---|---|
| 1. FR_NFR 3.4.1: approved `T_svc = 20 ms`, owner and date | `01879189`: `docs/reference/FR_NFR.md:334-335`, with the decision linked |
| The per-family rule `min(T_svc, ceiling)` and its table | `FR_NFR.md:338-348` (the owner's table, with each ceiling's source), `:361` (`elapsed <= W + min(T_svc, C)`) |
| Rewrite "Choosing 10 ms remains below each listed ceiling", the MRP 200 ms slack, MAAP draws near 600 ms | `FR_NFR.md:385-389`, `:393`, `:394` |
| Show `T_ingress + T_svc + T_egress + T_network < timeout`, with the margin, for each numeric response deadline | `FR_NFR.md:400-424`: ACMP 200 ms leaves 178 ms (188 at 10 ms); AECP 240 ms leaves 218 (228); the controller's 250 ms transaction timeout leaves 228 (238); MVU 240 ms leaves 218 (228). The two fabric allowances are derived there and marked as not yet measured (section 7) |
| Update the NFR-SCOUT-03 row; `docs/history` untouched | `FR_NFR.md:324`; `git diff 59038a1d bf1773c0 -- docs/history` is empty |
| 2. `scenario.py`: `T_SVC_MS = 20.0` | `2a079d5d`: `tb/verilator/ctrl_service_budget/scenario.py:90-92` |
| The grader decides "within" by `min(T_SVC_MS, CEILING_MS[family])` | `grade.py:431-440`: `budget_ms()` and `verdicts()` |
| `selftest.py` pins both values | `selftest.py:61-65` (`T_SVC`, `CEILINGS`, and the resulting `BUDGETS`), checked at `:234` and `:292` |
| Planted defects: SRP graded against T_svc alone (fails on an 18 to 20 ms SRP instance); a stale 10 ms pin | `selftest_mutants.py:439-443`, with a third, each family against its ceiling alone. They are caught by `an SRP instance one cycle over 18 ms misses, under T_svc`, `fixture row fixture.service.srp.first.if0` and `an AECP instance at 22 ms misses T_svc, within its ceiling` (section 3) |
| 3. Re-measure every composed row at 100 MHz, both points, both arms, with and without the two drafts; bold over its own bound | Section 5: 8 legs at `2a079d5d`, 0 refusals. Every group log and every image is byte-identical to round 8's legs, and the final head's images are byte-identical to the legs' |
| `SPLIT_CONTROL_MEMORY.md` section 13 and `MAILBOX_SPLIT.md` to the approved budget | `bf1773c0` (section 13, its tables bolded against each bound and a new "At the approved budget"), `01879189` (MAILBOX_SPLIT and its checker) |
| 4. Round 8's full gate set, all rc 0; no full sweep (no RTL change) | Section 6. rc 0 everywhere but rtl-fast's `firmware-boundary` at the head, which is the existing refusal of S2's harness files. It passes with S2's `e0e1b464`, which `dev-soft-core` has |
| 5. Not in this round: the block-RAM ledger, the egress-held rows, the drafts' reviews | Not touched |
| 6. Exit: REVIEW READY with the head; PR-BODY "Relates to #665" | Yes |

## 2. Changes

`2a079d5d` Grade each split service path against min(T_svc, its family's ceiling) at the approved T_svc = 20 ms, and plant the controls past it:

| file:line | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/scenario.py:90-92` | `T_SVC_MS = 20.0`; the comment names the owner's approval and the min rule | Item 2 |
| `scenario.py:112` | `wait_ms`'s comment: W plus its budget | The rule changed |
| `grade.py:431-433` | `budget_ms(probe)`: `min(T_SVC_MS, CEILING_MS[family]) + wait_ms` | The one place the rule lives, so a mutant can replace it |
| `grade.py:436-440` | `verdicts()` returns `budget_ms`, `within_budget`, `ceiling_ms`, `within_ceiling` | A field named `within_t_svc` would read False for a 19 ms SRP instance under T_svc = 20; the field says what it grades |
| `grade.py:3`, `:27`, `:454`, `:460`, `:538`, `:716`, `:747` | The same names in the docstrings, `never_answered`, the pass bound's `bound_within_budget`, `service` | Same |
| `run.py:10-11`, `:46-54`, `:105`, `:112`, `:123`, `:150`, `:160`, `:246`, `:262-264`, `:278-280`, `:343` | The budget in the run's docstring, the verdict word, the tallies, the table's `Budget (+W) ms` column, the miss lines (`over its budget 18 ms`), the control verdict and the summary line | The verdict words stay exact: `MISS T_svc` is over T_svc within a looser ceiling, and `MISS ceiling` is over a ceiling, which is the budget where it is the tighter |
| `selftest.py:58-65` | `PINNED` with the new field names; `T_SVC = 20.0`, `CEILINGS`, `BUDGETS` restated | Item 2: both values pinned |
| `selftest.py:172-178` | The planted over-budget BIND_RX moved 20 ms + 1 cycle | At 10 ms + 1 it now fits its 20 ms budget |
| `selftest.py:234-241` | `T_svc and the ceilings pinned`; the exact-budget checks at 2,000,000 bus cycles | Same |
| `selftest.py:275-293` | `budget_checks()`, the new checks of section 3 | Item 2's SRP defect needs an 18 to 20 ms instance to fail on |
| `selftest.py:315-327` | The normative-wait checks: an AECP path (budget W + 20 under its ceiling W + 24) for the three tiers, and SRP (budget = ceiling = W + 18) | With SRP's budget equal to its ceiling the old SRP tiers collapsed |
| `selftest.py:359-360`, `:606`, `:677` | The late recipient at 22 ms; the shutdown tally at 20; the run-exit check's name | Calibrated to 10 ms |
| `selftest_mutants.py:294`, `:436` | The field names | Same |
| `selftest_mutants.py:439-447` | `deadline: T_svc 20 ms` (now the value itself) replaced by the stale 10 ms pin; two new budget mutants; the wait mutant restated with the min | Section 3 |
| `selftest_mutants.py:451` | `run: a budget miss never fails the run` | Name |
| `oracle.json` | Regenerated by its generator (`selftest.py --write-fixture`) from the committed `fixture.log`, which is unchanged (sha256 `8137bb36...` before and after), with a fresh 1x1 cacheless build's `build.json` (same clocks, 100 / 50 MHz). The diff is the field names and the two `fixture.service.srp.*` rows, 11.72 ms, now within their 18 ms budget | The oracle pins the grader's verdicts; `f8876638` regenerated it the same way |
| `build.py:46-55` | The planted spin of both controls from 16,000 to 32,000 turns; the comment says why | On the cacheless core it measured 24.6 ms, 4.6 ms over the new 20 ms budget; 32,000 turns measure 48.7 ms |

`e037f7ea` State the harness's budget, its verdicts and its new checks and planted defects in its README:

| file:line | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/README.md:8-11` | The budget, the approval, and that Results and The instruction cache were graded at the 10 ms then proposed | Their figures and misses are S2's and S2c's at 10 ms |
| `README.md:47`, `:181`, `:189-192`, `:196`, `:554` | Over its budget; the budget per family (`grade.budget_ms`); the verdict words; the two sections marked as graded at 10 ms | Same |
| `README.md:825-829` | The self-test's checks | Section 3 |
| `README.md:902-905`, `:909`, `:911`, `:928` | The mutant table: the three deadline mutants, the renamed checks, and `xip: the hot code and the rest stay in rom`, a mutant the table had left out | The table restates the self-test's output |

`01879189` Approve T_svc = 20 ms in FR_NFR 3.4.1 and NFR-SCOUT-03, grade each family against min(T_svc, its ceiling), show each response deadline's margin, and restate the mailbox bounds and their checker at 20 ms:

| file:line | Change | Reason |
|---|---|---|
| `docs/reference/FR_NFR.md:324` | NFR-SCOUT-03: T_svc = 20 ms approved, the bound min(T_svc, ceiling) | Item 1 |
| `FR_NFR.md:334-348` | The approval, the rule, and the owner's table with each ceiling's source | Item 1 |
| `FR_NFR.md:361-362` | `elapsed <= W + min(T_svc, C)`; overhead shares that bound | The rule with a normative wait |
| `FR_NFR.md:371-383` | Each derivation row's "service <= 10 ms" restated: T_svc = 20 ms where the ceiling is looser, equal for ACMP, 18 ms for SRP, 15 ms for identification while enabled, 12 ms for a future IN_PROGRESS cadence | Item 1 |
| `FR_NFR.md:385-389` | "Choosing 10 ms remains below each listed ceiling" rewritten: MRP's 18 ms is the bound, ACMP's equals T_svc, the rest are above it | Item 1 |
| `FR_NFR.md:392-394` | The MRP slack: 18 ms and the 1 ms egress allowance take 19 of the 40 ms; MAAP draws within 20 ms of 600 ms | Item 1 |
| `FR_NFR.md:400-424` | The inequality with `T_svc` as the path's bound, then the table for each numeric response deadline, the derivation of `T_ingress` and `T_egress`, and what `T_network` is left | Item 1 |
| `FR_NFR.md:465` | H-DISC: total service within the path's bound, 20 ms | Was 10 |
| `docs/design/MAILBOX_SPLIT.md:441`, `:461-462` | H-DISC within its 20 ms bound; NFR-SCOUT-03's approved budget | Item 3 |
| `MAILBOX_SPLIT.md:690-715` | The ACMP backlog table: one access-time column for the 20 ms bound (T_svc and the ceiling are equal), and the conclusions at that bound: the event, acmp-ring and owed-frame bounds fit at 1 us an access, the adp-ring one does not | Item 3 |
| `MAILBOX_SPLIT.md:727-740` | The same for the bounds with MAAP | Item 3 |
| `MAILBOX_SPLIT.md:769-778` | The four-module table and its conclusion at 20 ms | Item 3; pinned by the checker below |
| `MAILBOX_SPLIT.md:1100-1102`, `:1362-1366` | F5's 10 ms target inside the 20 ms bound; the open item's access times at 20 ms | Item 3 |
| `sw/firmware/ctrl/test/ctrl_service_bounds.py:26-30`, `:51-54` | The firmware gate that requires the page's table and conclusions now computes the threshold at 20 ms, refuses unless the events fit 20 ms and the others exceed it, and states the conclusion at 20 ms | It regenerates and pins that table; the page and the checker move together. Its planted controls are derived from the lines (37 of 37 caught; 46 checks, 0 failures in shard 0) |
| `docs/design/MARK_II_AREA_PLAN.md:447`, `:1290` | "Prove 10 ms project service", "The 10 ms project budget" | They stated the old value as current |
| `sw/firmware/ctrl/loop/ctrl_loop.h:55-62`, `:110`; `acmp/acmp_mbx.h:108-111`; `aecp/aecp.h:22-23`; `srp/srp_mbx.c:20`; `srp/README.md:165`, `:320-322` | Comments only: each statement of "T_svc = 10 ms" as the requirement now names the approved bound, and where a figure was sized against 10 ms (the pass share, the event count, the SRP host desk test's allowance) it says so | A comment citing FR_NFR 3.4.1 for 10 ms would now be false. No code changed: the images are byte-identical (section 5) |

`1c601479` State that the planted controls are the cacheless core's, where they miss the 20 ms budget by 29 ms, and that the split CPU's caches bring the spin under it:

| file:line | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/build.py:47-48` | The comment: the cacheless CPU the controls run on | My first comment also claimed the split's fetch L1; measured, it does not hold (section 7) |
| `README.md:811-812` | "Controls with the cache" is S2c's run, 16,000 turns, against 10 ms | Historical |
| `README.md:954-962` | The controls' figures at the head (48.697 ms and 48.932 ms; unplanted 0.057 ms and 0.291 ms); why 32,000 turns; that they are the cacheless core's, and why no count serves both cores | Measured (`receipts/controls/`) |

`bf1773c0` Grade section 13's composed rows against each family's approved bound, and record every row again at the head at T_svc = 20 ms with and without both drafts:

| file:line | Change | Reason |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:26` | The contents entry names the new subsection | Navigation |
| `SPLIT_CONTROL_MEMORY.md:776` | Section 12's model: "within the 10 ms T_svc then proposed" | Historical |
| `SPLIT_CONTROL_MEMORY.md:846-847`, `:852-878` | The tables' bold is now over each row's own bound (18 ms SRP, 20 ms the rest), and the figures are named as round 8's | Item 3 |
| `SPLIT_CONTROL_MEMORY.md:880-883` | The conclusion at the approved budget | Item 3 |
| `SPLIT_CONTROL_MEMORY.md:890-914` | "At the approved budget": the decision, the rule, the re-measurement, the table with each row's bound at both points with and without the drafts, the margins | Item 3 |
| `SPLIT_CONTROL_MEMORY.md:936`, `:944-949` | "What holds the 8x8 rows" and "What is left" at the approved budget; #26 and the ledger named | Item 3 |

## 3. New checks, planted defects and failing words

All in `tb/verilator/ctrl_service_budget/selftest.py`, run by `run.py --self-test` (`self-test: 0 failures`, 105 checks, 74 mutants caught):

| Check | Planted defect (`selftest_mutants.py`) | Failing words |
|---|---|---|
| `an SRP instance at its 18 ms ceiling fits`; `an SRP instance one cycle over 18 ms misses, under T_svc`; `an SRP instance at 19 ms misses its 18 ms budget` | `deadline: SRP graded against T_svc alone, not its 18 ms ceiling` (`budget_ms` = T_svc + W) | `MUTANT caught: deadline: SRP graded against T_svc alone, not its 18 ms ceiling: an SRP instance one cycle over 18 ms misses, under T_svc ({'ms': 18.00001, 'budget_ms': 20.0, 'within_budget': True, 'within_ceiling': False})` |
| `T_svc and the ceilings pinned` (T_svc = 20.0 and the ceilings, restated); the fixture's SRP service rows pinned within their 18 ms budget | `deadline: T_svc pinned at the 10 ms proposal (earlier rule)` (`T_SVC_MS = 10.0`) | `MUTANT caught: deadline: T_svc pinned at the 10 ms proposal (earlier rule): fixture row fixture.service.srp.first.if0 (within_budget False (pinned True))` |
| `an AECP instance at 22 ms misses T_svc, within its ceiling`; `a MAAP instance at 30 ms misses T_svc, within its ceiling` | `deadline: each family graded against its ceiling alone, not T_svc` (`budget_ms` = ceiling + W) | `MUTANT caught: deadline: each family graded against its ceiling alone, not T_svc: an AECP instance at 22 ms misses T_svc, within its ceiling ({'ms': 22.0, 'budget_ms': 24.0, 'within_budget': True, 'within_ceiling': True})` |
| `each family's budget is min(T_svc, its ceiling)` (the owner's table, `BUDGETS`, against `grade.budget_ms`) | each of the two above (a second catch) | listed after the first catch |
| `W + T_svc passes` (AECP, W = 200 ms: 220 ms), `... + 1 misses, within W + ceiling`, `W + ceiling + 1 is over the ceiling`; `W + SRP's ceiling passes, its budget` (218 ms), `... + 1 misses its budget and its ceiling` | `deadline: the normative wait is not added` (restated with the min); `deadline: the ceiling drops the normative wait` | `... the normative wait is not added: W + T_svc passes`; `... the ceiling drops the normative wait: W + T_svc passes` |
| `exact budget passes` (an ACMP path at exactly 20 ms), `one cycle over misses` | `deadline: strictly below the budget` | `... strictly below the budget: exact budget passes` |
| `planted over-budget path is caught` (BIND_RX moved past 20 ms), `a late recipient misses its budget` (22 ms) | (recalibrated, existing) | |

The whole mutant table, as the self-test prints it, is in `README.md:853-928` and `receipts/gates/harness_selftest.log`.

The harness's controls (planted firmware defects, `run.py --mutation`), at the head's harness code (`receipts/controls/`):

| Control | Planted defect | Failing words |
|---|---|---|
| `slow-adp-rx`, cacheless core | ADP's receive handler spins 32,000 turns before it hands the record on | `BUDGET control.discover.if0: 48.697 ms over its budget 20 ms`, `CONTROL slow-adp-rx caught: every control path missed its budget` |
| `slow-adp-shutdown`, cacheless core, `shutdown-entry` arm | Disabling ADP spins 32,000 turns before its ENTITY_DEPARTINGs | `BUDGET control.shutdown.if0: 48.932 ms over its budget 20 ms`, `CONTROL slow-adp-shutdown caught` |
| `as-built`, cacheless core | The generator handed the SoC's regions unchanged | `CONTROL as-built caught: an instruction access fault (cause 1)` |

## 4. Method

- **The harness:** S2's, the four backlog groups (`backlog`, `backlog-adp`, `backlog-adp-refill`, `backlog-owed`), at 1x1/1if and 8x8/2if, arms A and B (`--variant answering-ports`), `--record-budget-findings`, each leg from a clean clone at `2a079d5d` with round 6's labelled profiling variant (round 8's `receipts/variants/harness-profile-cumulative.patch`, which carries `CSB_CPU_HZ`), `CSB_CPU_HZ=100000000`; the bus stays 100 MHz.
- **The legs** (`receipts/measure/`, each `label.txt`): `N9-<arm><point>` the branch; `D9-<arm><point>` with both drafts staged as round 8 staged them: lwSRP `fc06e7c0` and tsn-c-stack `6532c3b0` by gitlink, `ctrl_arms.LWSRP_REV` moved, the runtime's `__lshrdi3` hot-list entry removed (round 8's `receipts/variants/parent-with-*.patch`). The drafts came from round 8's and round 7's scratch clones, each checked to be its own top level.
- **`2a079d5d` against the head:** since then the harness's code changed only in a `build.py` comment, and the firmware only in comments; the rest is Markdown and `ctrl_service_bounds.py`. The head's linked images at both points, with and without the drafts, are byte-identical to the legs' (`receipts/images/images-at-head.md`). The legs' 32 group logs and 8 images are byte-identical to round 8's `M100` and `D100` (`receipts/behaviour/legs-vs-round8.md`). A fresh build at the head reproduces the 1x1 arm A `backlog` group (section 6).
- **The analysis** (`scripts/rows9.py`): each composed row's worst instance over the four groups, graded against min(T_svc, the family's ceiling) + W taken from the lane's `scenario.py`. So round 8's legs, which were graded at 10 ms, are regraded at the approved budget too. The grader's own verdicts in the legs' `results.json` agree with it on all 392 measured rows.

## 5. Measurement

Every composed row, worst instance over the four groups, ms, arm A / arm B, bold over its own bound (`receipts/rows/rows-1x1.md`, `rows-8x8.md`; SPLIT_CONTROL_MEMORY section 13, "At the approved budget"):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.09 / 5.02 | 4.41 / 4.55 | 8.51 / 8.94 | 8.62 / 8.28 |
| ADP record, last | 20 | 3.77 / 3.56 | 3.22 / 3.24 | 6.68 / 6.86 | 6.64 / 6.52 |
| MAAP record, last | 20 | 3.81 / 3.60 | 3.25 / 3.27 | 6.66 / 6.84 | 6.63 / 6.50 |
| AECP record, last | 20 | 9.56 / 9.93 | 8.64 / 9.00 | 14.92 / 15.89 | 14.47 / 15.22 |
| SRP record, last | 18 | 10.41 / 9.91 | 9.11 / 9.26 | 16.30 / 16.39 | 15.81 / 15.19 |
| An ACMP command behind a full ACMP ring | 20 | 3.91 / 3.69 | 3.44 / 3.44 | 7.87 / 8.29 | 7.98 / 7.63 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.88 / 2.72 | 2.46 / 2.48 | 4.23 / 4.32 | 4.24 / 4.38 |
| An event behind 15 others | 20 | 1.22 / 1.17 | 1.10 / 1.10 | 2.15 / 2.20 | 2.15 / 2.12 |
| AECP record, last, in the owed window | 20 | **62.40** / **62.32** | **62.25** / **62.36** | **64.66** / **64.79** | **64.79** / **64.68** |
| A response with 7 frames owed ahead of it | 20 | **61.70** / **61.64** | **61.60** / **61.68** | **63.44** / **63.51** | **63.78** / **63.42** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

The first records (1.0 to 4.5 ms) and the refilling bucket's row fit everywhere (the receipts list them).

- Every row the CPU decides fits its bound at both points, on both arms, with the drafts staged or not. The STOP condition does not hold.
- The least margin is the 8x8 last SRP record's: 1.61 ms under 18 ms without the drafts (arm B, 16.39), 2.19 ms with them (arm A, 15.81). The 8x8 last AECP record keeps 4.11 ms without them and 4.78 ms with them.
- At 1x1 every such row keeps at least 7.59 ms (the last SRP record, 10.41 ms).
- The owner's figures for round 8's head (14.47 / 15.22 ms AECP and 15.81 / 15.19 ms SRP at 8x8 with both drafts) are reproduced exactly.
- Each leg's run: `4 groups graded, 0 refusals, 6 budget misses`. The six are exactly the egress-held rows: `backlog.owed`, the four `backlog.owed_behind*` (never answered), and `backlog-owed.service.aecp.last` (each `run.log`).

## 6. Gates

Each gate ran on a clean clone of its head (`scripts/clone.sh`). Its log is in `receipts/gates/` with host paths replaced; `receipts/gates/stale/` keeps superseded runs. "Since" says what changed after a gate's head.

| Gate | Command | Where | Result | Receipt |
|---|---|---|---|---|
| Firmware self-test, all four shards (every firmware mutant driver; the service-bounds arm that pins MAILBOX_SPLIT's table) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard k/4 --jobs 4` | `bf1773c0` | rc 0, `test_ctrl_firmware: PASS` each; shard 0 `[ok] arm hot`, `named plants not caught: none`, `== ctrl service bounds: checks: 46   failures: 0 ==`; shard 1 `mutants: 546 of 546 caught`; no `ESCAPED` in any shard | `selftest-shard0.log` to `selftest-shard3.log` (shard 1 also at `01879189`, the same result: `stale/`) |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check` | `bf1773c0` | rc 0, `firmware coverage: PASS (32 files)` | `fw_coverage_check.log` |
| RV32 self-test | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | `bf1773c0` | rc 0, `RV32 build self-test: 25 checks PASS` | `fw_rv32_selftest.log` |
| Mailbox generator | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | `bf1773c0` | rc 0, `selftest: 0 arm(s) failed` | `gen_mailbox.log` |
| rtl-fast `publication-census` | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 4`, with the pinned sv2v v0.0.12 and Yosys 0.66 named by `SV2V` / `YOSYS` | `01879189` (since: Markdown and a comment in the harness's `build.py`) | rc 0, `RESULT: PASS`; `mutations: 0 of 31 rule(s) no arm proves` | `publication_census.log` |
| RTL lint ratchet | `python3 scripts/lint_rtl.py --check` | `bf1773c0` | rc 0, `LINT GATE: PASS (89 violation(s) <= ratchet 89; ...)` | `lint_rtl.log` |
| Vivado front-end, under the lock | `python3 scripts/xvlog_gate.py --check` | `bf1773c0` | rc 0, `xvlog gate: PASS (0 finding(s) == ratchet; 0 hdl/, 0 pinned processors)` | `xvlog_check.log` |
| Yosys, the mover's and the adapter's rows | `syn/yosys/run.sh --top KL_mbx_dma --top KL_mbx_wb` | `bf1773c0` | rc 0, `[PASS] KL_mbx_dma cells=2302`, `[PASS] KL_mbx_wb cells=5`, `TAP-PURITY RESULT: PASS` | `yosys-KL_mbx_dma-KL_mbx_wb.log` |
| CPU option test | `python3 sw/builder/test_soc_options.py` | `bf1773c0` (and in the docs runner) | rc 0, `RESULT: PASS` | `soc_options.log` |
| End-station builder | `python3 sw/builder/test_builder.py --require-rv32` | `01879189` (since: Markdown and a harness comment) | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11, the historical Arty report not on disk, as in rounds 3 to 8 (1,994 s) | `builder_require_rv32.log` |
| rtl-fast `firmware-boundary` | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `bf1773c0` | **rc 2**: it refuses S2's harness files; the `REFUSED` line is byte-identical to rounds 5 to 8 (md5 `079f75e5...`) | `ctrl_boundary_without_verilator.log` |
| same | same | `bf1773c0` + S2's `e0e1b464` (in `dev-soft-core`), cherry-picked uncommitted in a scratch clone | rc 0, `ctrl_boundary: PASS` | `ctrl_boundary_without_verilator_with_S2_e0e1b464.log` |
| rtl-fast `firmware-verilator` (the mailbox suite among its builders) | `... --only verilator` | `bf1773c0` | rc 0, `ctrl_boundary: PASS`; `make -C tb/verilator/mbx: exit 0` | `ctrl_boundary_only_verilator.log` |
| The split link script's test | `python3 sw/litex/test_ctrl_memory.py` | `bf1773c0` | rc 0 | `test_ctrl_memory.log` |
| Linked images at four points | `scripts/images.py` (`ctrl_srp_image.py --with-aecp --layout split`), round 8's head against this head | `bf1773c0` | rc 0; every point byte for byte the same size, planned tiles 35.0 / 38.5 / 48.5 / 55.0, 0 over a cap | `images-four-points.log`, `receipts/images/` |
| Docs workflow, bare-metal scope, idiom gates, `ci_events`, harness self-test, CPU option test, `behave` (96 gates) | `scripts/docs_gates.sh` (`gates_s2b3.py`) | `bf1773c0` | `0 of 96 gates nonzero or left the tree dirty`: `docs_check: 0 finding(s)`, `check_em_dash: 0 finding(s) over 1954 added line(s)`, `TOC gate: OK`, the anchors reproduced, `baremetal-only: OK`, `NAMING RATCHET: PASS`, the C++ and Python idioms within their ratchets, the harness `self-test: 0 failures`; `cd tests && behave`: 14 features, 406 scenarios, 1,977 steps passed | `docs/` (two logs trimmed, `TRIMMED.md`) |
| The harness's self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | `bf1773c0` | rc 0, `self-test: 0 failures`; 105 checks, 74 mutants caught | `harness_selftest.log` |
| S2's harness, both points, both arms, with and without both drafts | `run.py --point 1x1/8x8 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings`, arm B `--variant answering-ports` | `2a079d5d` + the profiling variant, 8 legs | rc 0 each, `4 groups graded, 0 refusals, 6 budget misses`, the six the egress-held rows | `receipts/measure/` |
| same, a fresh build at the head | `--groups backlog`, 1x1 arm A | `bf1773c0` + the profiling variant | rc 0, `0 budget misses`; its log and image byte-identical to leg N9-A1's | `receipts/measure/final-head-check/` |
| The harness's controls | `run.py --point 1x1 --fetch-l1 none --mutation slow-adp-rx`; `... --variant shutdown-entry --mutation slow-adp-shutdown`; `... --cpu-regions as-built` | `01879189` (the harness code since: a comment) | rc 0 each: `CONTROL slow-adp-rx caught` (48.697 ms), `CONTROL slow-adp-shutdown caught` (48.932 ms), `CONTROL as-built caught: an instruction access fault (cause 1)` | `receipts/controls/` |
| lwSRP's draft | its suite (`cmake`, `ctest`, `unit_tests`), `behave`, `scripts/lwsrp_plants.py` | the draft `fc06e7c0`, unchanged since round 8 | `Completed "main": 26690 passes`, rc 0; 3 scenarios passed; `lwSRP donor plants: 6 of 6 caught` | `receipts/donor/` |

Not run:
- the full sweep: no RTL changed (`git diff 59038a1d bf1773c0 -- hdl syn` is empty);
- the CI command table's checker (`scripts/ci_tool_inventory.py --check`), which needs the CI image's checksum-pinned shell parser (as in round 8). This round changes no CI command.

## 7. Findings, conflicts, decisions needed

- **No STOP.** Every row the CPU decides fits its own bound at both points, on both arms, with both drafts staged and without them. The least margin is the 8x8 last SRP record's: 1.61 ms under 18 ms without the drafts (16.39 ms, arm B) and 2.19 ms with them (15.81 ms, arm A). The owner's figures for round 8's head are reproduced exactly.
- **Assumption, for review: the fabric allowances.** FR_NFR's response-deadline table allots 1 ms to `T_ingress` and 1 ms to `T_egress`. Neither is measured; both are bounds from the design:
  - `T_ingress`: `KL_mbx_rx`'s commit within 64 mailbox cycles of a frame's last byte, which the harness requires of every commit, behind the 656 ns receive chain in the board's configuration;
  - `T_egress`: `KL_mbx_tx`'s commit-order merge behind at most the five TX rings' 6,144 bytes (21,504 bytes on the wire as 256 minimum frames). That is under 0.7 ms at the quarter of 1000BASE-T that IEEE 802.1Q-2018 34.3's default 75 % `deltaBandwidth` leaves unreserved.

  The datapath tap and the wire round trip (H-ACMP, H-AECP) are open, and an egress held longer (the 60 ms hold) stays with #26. If the owner wants other allowances, only the table's margins move: the inequality holds while the network's round trip stays under 178 ms (ACMP) or 218 ms (AECP).
- **Finding: the controls are the cacheless core's.** My first change's comment claimed the doubled spin also misses behind the split's fetch L1. Measured, it does not: behind the split CPU's own caches (the 16 KiB fetch L1 and the data cache) at 50 MHz, `slow-adp-rx` and `slow-adp-shutdown` take 17.324 and 17.406 ms, fit the 20 ms budget, and escape (`receipts/controls/rx-split`, `sd-split`, rc 1).
  - The README's controls already run on the cacheless core, as S2 designed them. There they are caught at 48.7 ms, where the old 16,000-turn spin left 4.6 ms over the new budget.
  - No count serves both cores within the `control-shutdown` group's window (50 ms past the SHUTDOWN, then at most 20 ms to settle).
  - So `1c601479` scopes the comment and the README to the cacheless core. Controls on the cached CPU would need that group's wait lengthened, a scenario change to the shutdown groups this round did not make.
- **Finding: the firmware's host suites still hold 10 ms.** `sw/firmware/ctrl/test/aecp_latency_policy.hpp` and `srp_latency_policy.hpp` (`*_service_limit_ns = 10000000`) and `test_maap_mbx.cpp` (`within 10 ms`) grade the host model's paths against 10 ms. Each has a planted "relaxed budget" defect at 10 to 20 ms (`aecp_mutants.py` `latency-budget-relaxed`, `srp_mutants.py` `latency-relaxed-budget`).
  - That is tighter than the approved bounds, so the suites stay valid and pass.
  - Moving them to min(20 ms, the ceiling) would change those tests and their plants, so it is not done here. It is a decision for the next firmware round.
  - Only the comments and the SRP README that cited 10 ms as FR_NFR's requirement were corrected (`01879189`).
- **Lane conflict: S1 (PR #795) is now in `dev-soft-core` (`f4c9ad4f`).** A trial merge of this head into it, in a scratch clone, conflicts in eleven files:
  - docs: `docs/reference/FR_NFR.md`;
  - firmware: `sw/firmware/ctrl/aecp/aecp.c`, `aecp_commands.c`, `aecp_internal.h`, `test/aecp_mutants.py`, `test/test_aecp.cpp`, `sw/firmware/gtest/coverage.ratchet`;
  - SoC: `sw/litex/milan_soc.py`;
  - harness: `tb/verilator/ctrl_service_budget/README.md`, `build.py`, `split_soc.py`.

  One of FR_NFR's conflicts carries a rule. S1 adopts AECP IN_PROGRESS for a face-state change, and its row says the 120 ms cadence's "12 ms ceiling is still above T_svc". Under the approved rule that path's bound is 12 ms, min(20, 12), and the merge must state that. A path answered with IN_PROGRESS would also need its own family in the harness, since `aecp` grades at 20 ms. Whoever merges second rebases (round 8's note); this lane may not rebase.
- **The firmware-boundary step's refusal** is S2's existing one: this lane's base lacks `e0e1b464`, which `dev-soft-core` has. Its `REFUSED` line is byte-identical to rounds 5 to 8, and with that commit applied the step passes (section 6).
- **The harness's result fields were renamed:** `t_svc_ms` to `budget_ms`, `within_t_svc` to `within_budget`, `bound_within_t_svc` to `bound_within_budget`. No reader outside the harness uses them (`grep` over the tree). Round 8's scratch analysis scripts read the old names; this round's `scripts/rows9.py` regrades from `ms`, `family` and `wait_ms`, and agrees with the grader on all 392 rows.
- **Not in this round, as assigned:** the block-RAM ledger (124 against 121.5), the egress-held rows (#26), the drafts' repository reviews.

## 8. Run history

- 2026-10-29 12:47 CET start; 12:5x TAKEN (issuecomment-6495860708).
- 12:5x the harness change; the oracle regenerated from the committed trace with a fresh cacheless fixture build's spec.
- 12:58 the eight legs as units at `2a079d5d` (4 on 0-15, 4 on 112-127); 13:24 all rc 0.
- 13:0x-13:1x FR_NFR, MAILBOX_SPLIT and its checker, the area plan's two lines, the firmware's comments; the builder, shard 1 and the census at `01879189`.
- 13:2x the seven control runs (two on the split's caches, to test the claim in my first comment: they escape, section 7).
- 13:3x section 13 and the controls' text; head `bf1773c0`. Shards 0, 2, 3, the quick gates, xvlog under the lock (13:4x, 159 s), coverage, the images, the boundary steps, the docs runner, the lwSRP draft, a fresh build at the head for the `backlog` group, and shard 1 again at the head.
- 14:09 the last gate (the docs runner, 96 of 96 rc 0). REVIEW READY posted: issuecomment-6497614101.
