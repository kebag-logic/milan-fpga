[A321]

## Status

The original published source `5874895eb817ed41c0f8be4eb427ad3315c29844` passed its recorded 50 static/builder commands and five native groups. [Complete historical evidence](https://github.com/kebag-logic/milan-fpga/tree/7c2f4357167e5398524f7980ab1a09690256544f/review-evidence/517-r1/corrected-source2/manager). [R245-1 is negative](https://github.com/kebag-logic/milan-fpga/pull/524#issuecomment-5783500849): F1 remains MAJOR under all five lenses pending independent re-review. The subsequent cancellation correction is retained in this rebase. The PR remains draft. The rebased local builder, static, pool and cancellation gates pass; the complete default sweep also passes: all 55 suites, 2121993 checks, zero failures and four declared skips. All four full-suite comparisons pass at `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`. R245 re-review, external R246 review, trusted local replication, hosted timing/gates and final candidate checks remain required. The earlier replica stopped while queued and supplied no invocation or pass. The original benchmark remains tied to `7ab1c8d0`; the historical host-policy correction did not change its executable artifacts.

## Rebase

Rebased the corrected source `ff7dac3257a321538a1fd1a310ab3190f646153d` onto `5c78ce2e9d831e588e759b696ed549804327e4d8` under [the assignment](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5835674224). All three original commit subjects are retained. The policy resolution keeps every base mask, every simulation mask and every self-test group. The Makefile preserves the current build recipes and passes all eleven ordinary commands through the bounded pool, including the #508 notification seam, #443 render CSR checks and CRF licence leg. Directory overrides remain effective. The five header-writing legs stay exclusive and ordered. Prerequisites, focused targets and explicit mutation campaigns keep their existing phases. The inventory documentation and actual-Makefile cancellation fixtures are reconciled with that base.

Local head: `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`. On CPUs 16-23 with eight build jobs, the complete default suite measured:

| Build state | Sequential | Pooled | Reduction |
| --- | --- | --- | --- |
| Cold | 1421.094 s | 1370.953 s | 50.140 s (3.53%) |
| Warm | 1230.269 s | 1170.273 s | 59.996 s (4.88%) |

Every run reports 10074 checks and zero failures. The eleven leg logs, ordered replay, executable hashes and recorded runtime inputs match; tracked headers are unchanged. The observed maximum is two ordinary children and one exclusive writer. The unchanged budget is 3600 s, leaving 2229.047 s cold and 2429.727 s warm for the pooled runs. These are local shared-host measurements, one pair per build state; hosted timing remains open. No workflow step or budget changed.

## Description

The eleven ordinary milan_dp executables at the rebase base ran sequentially. A suite-local
runner now allows two children while keeping the five sim_nxn header writers
exclusive and ordered. Independent legs can overlap that group. SIM_JOBS=1
reproduces sequential execution; presence of MILAN_COUNTER_FRAME_OUT preserves
the original whole-set order. Per-child logs replay in legacy order. Failures
stop the recipe. Ordered output is retained on disk, and nonblocking stdout delivery services cancellation. Owned descendants are terminated and reaped before bounded shutdown even while the consumer stays blocked; R245 F1 still requires independent re-review.
Build recipes, gPTP prerequisites and render mutation phases are unchanged.
The inaccurate sim_nxn explanatory comment is corrected; executable tokens match.

## How to reproduce

With pinned Verilator 5.050 on PATH, compare the complete suite. Each clean is followed by a cold run and then a warm run. Keep `MILAN_COUNTER_FRAME_OUT` unset and use the same available CPU set throughout:

```sh
make -C tb/verilator/milan_dp clean
taskset -c 16-23 make -C tb/verilator/milan_dp SIM_JOBS=1 VERILATOR_JOBS=8
taskset -c 16-23 make -C tb/verilator/milan_dp SIM_JOBS=1 VERILATOR_JOBS=8
make -C tb/verilator/milan_dp clean
taskset -c 16-23 make -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=8
taskset -c 16-23 make -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=8
```

## How to validate

Run `python3 tb/verilator/milan_dp/test_sim_pool.py`, `python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py`, the existing phase controls,
and the complete real suite with its unchanged render campaign. Preserve logs
and use `scripts/suite_tally.py --verdict`. Controlled cold/warm and fault-test
receipts are supplied in the author handoff for a PR evidence comment. The author also ran every requested static gate, both builder modes and the complete five-chunk default sweep. The manager retains trusted local replication, hosted timing/gates and candidate checks.

Local validation retains the declared limits: the builder utilization-report calibration arm has no hardware report, and the no-compiler mode stands down its compiler instruments. The default sweep declares four `tsn-gen` field-campaign/freshness skips because that checkout is absent; these contribute no checks.

The bare-metal checker adds only file/context-pinned workstation process references and strong positive/refusal controls; policy classes and budgets remain unchanged.

The pool unit controls pass 17/17, blocked-output cancellation controls 28/28, and phase controls 24/24. Both builder modes and every requested static/documentation/HDL/idiom gate exit 0. The policy self-test passes 700 arms; CI event checks pass 1647 contract items and 2188 self-test arms; BDD passes 344 scenarios and 1739 steps. Existing xvlog and RTL-lint ratchets are unchanged. The full default sweep has no suite failure or timeout:

| Chunk | Suites | Checks | Exit | Seconds |
| --- | --- | --- | --- | --- |
| 0/5 | 11 | 401931 | 0 | 564.104 |
| 1/5 | 21 | 173056 | 0 | 1412.828 |
| 2/5 | 10 | 1522972 | 0 | 711.309 |
| 3/5 | 12 | 13960 | 0 | 471.906 |
| 4/5 | 1 | 10074 | 0 | 1279.530 |

## DoD

Local scope and measured comparisons are recorded. R245/R246 review, manager
validation, authorized merge and post-merge containment remain open. No author
approval is claimed.

Closes #517
Relates to #270
