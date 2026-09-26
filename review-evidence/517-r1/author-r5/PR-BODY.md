[A324]

## Round 5

Local head: `1d694677c8f376ec44e3b59b1d7fa7abccda106b`. Implements items 1-3 of [the assignment](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5843777653):

- Audited all eleven ordinary legs with tree/private nanosecond timestamps and file-operation traces, including a same-byte-write positive control. Five legs each write fourteen files in distinct private directories; the other six write no data files. A common-TMPDIR run confirms seventy distinct private paths with no intersection. Both unchanged reviewer builder probes confirm no suite-directory tracked-header write; the repository-root positive control detects one. Removed all five unsupported exclusivity marks, restored the accurate base comment and documented the measured writes.
- Made the backpressure fixture establish default signal dispositions and an empty mask, and read the ledger while both writers are held. Twenty default-SIGINT and twenty inherited-ignored runs all pass 28/28. Both reviewers' selected exclusivity, overlap, inventory and backpressure mutations reject their defects. The old runner blob `761ec858` fails 28/28. One overlap mutation is rejected by a guard timeout rather than an assertion; that existing fixture limitation remains under #495.
- Corrected the runner contract to eleven legs and included `obj_crflic` in the no-handler rationale. Runtime runner code is unchanged in this round.

The full default pooled cold command used pinned Verilator 5.050, CPUs 16-23 and eight build jobs, after `make clean` each time:

| State | Seconds | Exit | Checks / failures |
|---|---:|---:|---|
| Before, `f36b40dd` | 1356.114 | 0 | 10074 / 0 |
| After, final runtime artifacts | 1361.378 | 0 | 10074 / 0 |

The after sample is 5.264 s (0.388%) slower: this pair shows no incremental speed gain. Both are single shared-host samples; test activity used separate CPUs and static checks also overlapped the after run. All executable hashes, eleven captures and replay bytes match; tracked header bytes and nanosecond mtimes remain unchanged. The final amendment changes only the cancellation fixture's PID packaging, leaving timed artifacts identical. Final-head sequential/warm and hosted timing were not measured in this round.

All requested normal gates exit 0, including both builder modes, pool controls, every static/documentation/HDL/idiom gate and BDD. The unmodified complete builder test ran with a selector adapter for the supplied read-only SDK, and separately with RV32 candidates unavailable. Compiler argv receipts are retained; this is local compatibility evidence. The declared unavailable builder arms remain listed below. Real-leg blocked-output cancellation passes INT/TERM/HUP through the actual Makefile, plus TERM with file output and TERM while a real generator descendant is live; no owned process survives.

## Status

Round 5 local head: `1d694677c8f376ec44e3b59b1d7fa7abccda106b`. The [Round 5 assignment](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5843777653) corrects the shared-header premise and authorizes dropping unsupported exclusivity. This round implements only its three items. Both [internal](https://github.com/kebag-logic/milan-fpga/pull/524#issuecomment-5843776016) and [external](https://github.com/kebag-logic/milan-fpga/pull/524#issuecomment-5839627765) reviewers closed the earlier blocked-output cancellation finding; their write-set, fixture-determinism and inventory-documentation findings await independent re-review of this correction.

The PR remains draft. This head is local and has not been pushed. Trusted local replication, ready-state hosted gates, hosted timing and final candidate checks remain required. The earlier replica stopped while queued and supplied no invocation or pass. No author approval is claimed.

Historical validation for the original published source `5874895eb817ed41c0f8be4eb427ad3315c29844` remains available in the [original evidence packet](https://github.com/kebag-logic/milan-fpga/tree/7c2f4357167e5398524f7980ab1a09690256544f/review-evidence/517-r1/corrected-source2/manager). It is not validation of this new head. The original benchmark is tied to `7ab1c8d0`; the historical host-policy correction did not change its executable artifacts.

## Rebase

Rebased the corrected source `ff7dac3257a321538a1fd1a310ab3190f646153d` onto `5c78ce2e9d831e588e759b696ed549804327e4d8` under [the assignment](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5835674224). All three original commit subjects are retained. The policy resolution keeps every base mask, every simulation mask and every self-test group. The Makefile preserves the current build recipes and passes all eleven ordinary commands through the bounded pool, including the #508 notification seam, #443 render CSR checks and CRF licence leg. Directory overrides remain effective. Round 5 removes the five exclusivity marks after measuring disjoint private writes; the earlier shared-header premise is superseded by the public decision. Prerequisites, focused targets and explicit mutation campaigns keep their existing phases. The inventory documentation and actual-Makefile cancellation fixtures are reconciled with that base.

Historical rebase head: `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`. Before Round 5, on CPUs 16-23 with eight build jobs, the complete default suite measured:

| Build state | Sequential | Pooled | Reduction |
| --- | --- | --- | --- |
| Cold | 1421.094 s | 1370.953 s | 50.140 s (3.53%) |
| Warm | 1230.269 s | 1170.273 s | 59.996 s (4.88%) |

At that historical head, every run reported 10074 checks and zero failures. The eleven leg logs, ordered replay, executable hashes and recorded runtime inputs matched; tracked header bytes were unchanged. The observed maximum was two ordinary children and one member of the then-marked group. The unchanged budget is 3600 s, leaving 2229.047 s cold and 2429.727 s warm for the pooled runs. These are local shared-host measurements, one pair per build state; hosted timing remains open. No workflow step or budget changed.

## Description

The eleven ordinary milan_dp executables at the rebase base ran sequentially. A suite-local runner now allows two children. With the frame dump absent, five sim_nxn legs each write fourteen files under a unique private `milan_nxn_*` directory; the other six write no data files. None writes a repository file. Their write sets are disjoint, so the ordinary recipe carries no exclusivity marks. The synthetic shared-group option remains tested.

`SIM_JOBS=1` reproduces sequential execution; presence of `MILAN_COUNTER_FRAME_OUT`, including an empty value, preserves the original whole-set order for the shared dump path. Per-child logs replay in legacy order. Failures stop the recipe. Ordered output is retained on disk, and nonblocking stdout delivery services cancellation. Owned descendants are terminated and reaped before bounded shutdown even while the consumer stays blocked. Build recipes, gPTP prerequisites and render mutation phases are unchanged. The accurate base comment in `sim_nxn.cpp` is restored; executable tokens match.

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
receipts are supplied in the author handoff for a PR evidence comment. Round 5 results are recorded below; every requested gate and all five default-sweep chunks exit 0. The manager retains trusted local replication, hosted timing/gates and candidate checks.

Local validation retains the declared limits: the builder utilization-report calibration arm has no hardware report, and the no-compiler mode stands down its compiler instruments. The default sweep declares four `tsn-gen` field-campaign/freshness skips because that checkout is absent; these contribute no checks.

The bare-metal checker adds only file/context-pinned workstation process references and strong positive/refusal controls; policy classes and budgets remain unchanged.

The pool unit controls pass 17/17, blocked-output cancellation controls 28/28, and phase controls 24/24. Both builder modes and every requested static/documentation/HDL/idiom gate exit 0. The policy self-test passes 700 arms; CI event checks pass 1647 contract items and 2188 self-test arms; BDD passes 344 scenarios and 1739 steps. Existing xvlog and RTL-lint ratchets are unchanged. All 55 default suites passed: 2121993 checks, zero failures or timeouts, 4 declared skips. The inventory contains no missing or duplicate suite, and tally accounting is complete.

| Chunk | Suites | Checks | Exit | Seconds |
|---|---:|---:|---:|---:|
| 0/5 | 11 | 401931 | 0 | 497.306 |
| 1/5 | 21 | 173056 | 0 | 1265.875 |
| 2/5 | 10 | 1522972 | 0 | 622.153 |
| 3/5 | 12 | 13960 | 0 | 305.959 |
| 4/5 | 1 | 10074 | 0 | 1415.400 |

## DoD

Local scope and measured comparisons are recorded. R245/R246 review, manager
validation, authorized merge and post-merge containment remain open. No author
approval is claimed.

Closes #517
Relates to #270
