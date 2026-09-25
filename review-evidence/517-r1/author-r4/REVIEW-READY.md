[A321] REVIEW READY

Commit: `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` (local; not pushed).
Base: `5c78ce2e9d831e588e759b696ed549804327e4d8`.
Scope: [assignment items 1-3](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5835674224).

Changed: rebased all three original commits with their one-line subjects; retained the full dev/PR policy-mask and self-test union; reconciled the Makefile, inventory documentation and cancellation fixtures with all eleven ordinary legs, including CRF licence, #508 GSI and #443 CSR coverage. The five shared-header writers remain exclusive and ordered. Directory overrides, prerequisites, focused targets and post-pool campaigns retain their original phases. The cancellation runner is byte-identical to the validated starting correction. Workflows, budgets, HDL, firmware, campaign drivers and required submodule pins are unchanged from the requested base.

Validation: every requested final-head command exits 0. Pool unit controls 17/17; blocked-output cancellation controls 28/28; phase controls 24/24. Both builder modes pass. The policy self-test passes 700 arms, BDD 344 scenarios/1739 steps, CI event check 1647 contract items and CI event self-test 2188 arms. Both CI documentation modes, all requested style/source/HDL/idiom/contract/traceability gates and final whitespace checks pass; existing ratchets are unchanged.

Complete default milan_dp measurements on CPUs 16-23, eight build jobs, Verilator 5.050:

| Build state | SIM_JOBS=1 | SIM_JOBS=2 | Reduction |
| --- | --- | --- | --- |
| Cold | 1421.094 s | 1370.953 s | 50.140 s (3.53%) |
| Warm | 1230.269 s | 1170.273 s | 59.996 s (4.88%) |

Each run reports 10074 checks and zero failures. All eleven leg logs, ordered replay, executable hashes and recorded inputs match; tracked headers are unchanged. Observed concurrency is at most two ordinary children and one exclusive writer. The unchanged budget is 3600 s; pooled cold/warm margins are 2229.047/2429.727 s. These are local shared-host measurements, one pair per build state.

Full default sweep: `scripts/run_all_suites.sh <chunk-output> --shard I/5`, I=0 through 4, with every preflight retained. Exact union: all 55 selected suites, 2121993 checks, zero failures, no timeouts, four declared skips.

| Chunk | Suites | Checks | Exit | Seconds |
| --- | --- | --- | --- | --- |
| 0/5 | 11 | 401931 | 0 | 564.104 |
| 1/5 | 21 | 173056 | 0 | 1412.828 |
| 2/5 | 10 | 1522972 | 0 | 711.309 |
| 3/5 | 12 | 13960 | 0 | 471.906 |
| 4/5 | 1 | 10074 | 0 | 1279.530 |

Declared limits: `tsn-gen` is absent, so its two field campaigns and two freshness arms ran no checks. The builder's utilization-report calibration arm lacks its hardware report; the no-compiler mode also stands down compiler instruments, which are graded by the SDK mode. No hardware evidence is claimed.

Acceptance evidence: assignment items 1-3 are met locally. Parent and required submodule bytes, indexes and pins match the committed candidate. HANDOFF.md records every conflict hunk with file/line resolutions, the before/after leg inventory, all commands/exits, every sweep chunk and the measured comparisons. PR-BODY.md contains the full updated local PR body with the Closes line retained, in the assigned output directory.

Open review state: R245 F1 remains MAJOR under all five lenses until independent re-review; R246 external review, reviewer-owned lens coverage, publication, trusted local replication, hosted gates/timing and candidate validation remain open. This is author evidence, not approval. No push, PR edit or merge was performed.
