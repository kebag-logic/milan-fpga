[A178] REVIEW READY

Local commit (not pushed): `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`; tree `790849ab7fcf7c712c77fe051bb5fb6a45d830c2`. Lane clean; one-line commit, no trailers. Independent source review is ready; this is not approval or completion of the merge bar.

Changed: the ten ordinary commands use an explicit two-child runner with one-worker reproduction. The five sim_nxn legs are exclusive and ordered; independent legs may overlap them. MILAN_COUNTER_FRAME_OUT being present, even empty, restores whole-set sequential behavior. Ordered complete/partial logs, failures and descendant cleanup are covered. Build/gPTP/render phases, generator argv, processor pins and ratchets remain fixed; the C++ comment correction preserves 47,519 executable tokens.

Acceptance 1-4, scoped author evidence: 17/17 runner controls; six planted runner faults rejected, including shared-state contention and unreaped descendants; 24/24 phase-observation controls; relevant tally/ownership/docs/idiom/hygiene/evidence controls return 0. Four complete real suites, including the unchanged render driver, each return 0 with 9,324 checks, zero failures and 13 tallies. Complete ordinary bytes, binary/input hashes, both gPTP transcripts, all six render outcomes and 23 render-record semantics match across modes. All three tracked-header byte copies match the commit before/after each run. No lane simulation remained at final inspection.

Measured at that same clean head with independently verified Verilator 5.050, the same host/resources, eight build jobs and outer make -j1:

| Full suite | One worker | Two workers | Saved |
|---|---:|---:|---:|
| Cold, suite clean | 1136.415 s | 1099.401 s | 37.014 s (3.257%) |
| Warm, build artifacts reused | 987.247 s | 943.330 s | 43.917 s (4.448%) |

The sampled ordinary spans are 492.870 -> 445.621 s cold and 493.832 -> 450.152 s warm. Samples show at most two ordinary children and one grouped child, with independent/group overlap. Peak pooled ordinary RSS is 10,928 KiB; peak sampled aggregate descendant RSS across all runs is 2,720,648 KiB. The inherited memory limit is 12 GiB and CPU affinity contains eight logical CPUs. Telemetry adds no tests. No build-speed gain is attributed to pooling; cold means the suite clean target, not host cache eviction. These are one local pair per temperature, not a guaranteed percentage or a hosted comparison.

Reproduction: `rtk proxy python3 tb/verilator/milan_dp/test_sim_pool.py`; with pinned 5.050 on PATH, `rtk proxy env VERILATOR_JOBS=8 SIM_JOBS=1 make -j1 -C tb/verilator/milan_dp run`, then the same command with SIM_JOBS=2. Use the existing clean target for each cold run. The designated 517-author-final handoff contains portable benchmark/fault-test scripts, exact command/head/tree/exit/timing/resource receipts, full logs, HANDOFF.md, REVIEW-READY.md and PR-BODY.md. Interrupted drafts and preliminary evidence remain unchanged and are not accepted as final measurements.

Acceptance 5 remains manager/reviewer-owned and pending: hosted dedicated-worker timing; full parent/PP/gPTP/Yosys/builder native banks; trusted act; exact-head hosted contexts; independent R245 internal Codex and R246 external Opus review across all five lenses; current candidate validation; authorized merge and post-merge containment. External Opus availability remains pending. No push, PR, Docker/act, delegation, merge or self-approval was performed. Stopping at the exact local commit above.
