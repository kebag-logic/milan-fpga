[A324] REVIEW READY

Commit: `1d694677c8f376ec44e3b59b1d7fa7abccda106b` (local; not pushed).

Changed: Round 5 items 1-3 only. All eleven leg write sets were measured with positive controls; the five private writers have disjoint fourteen-file sets, so their unsupported exclusivity marks are removed. The accurate base comment and measured-write documentation are restored. The backpressure fixture establishes its signal state and reads the ledger while writers are held. The contract states eleven legs and includes `obj_crflic`.

Validation: both complete builder modes exit 0; pool unit controls 17/17; backpressure controls 28/28 in each of twenty default-SIGINT and twenty inherited-ignored repeats. Both reviewers' finding-specific probes ran unchanged. Selected mutations reject their defects; the old runner fails 28/28. Real-leg cancellation probes pass, with no survivors. All requested static, documentation, HDL, idiom, BDD and CI-event gates exit 0. All 55 default suites passed: 2121993 checks, zero failures or timeouts, 4 declared skips. The inventory contains no missing or duplicate suite, and tally accounting is complete. Every chunk exits 0.

Cold default-pool timing, same CPUs and build jobs: 1356.114 s before, 1361.378 s after. The after sample is 0.388% slower; no incremental speed gain is claimed. Executable hashes, eleven captures and replay bytes match, with tracked header bytes and nanosecond mtimes unchanged.

Limits: builder utilization calibration has no hardware report; no-compiler mode additionally declares compiler-dependent instruments unavailable. Four field/freshness skips contribute no checks. The overlap mutant reaches a guard timeout, not an assertion catch. Timing is one shared-host pair. Independent re-review, publication of the local head, trusted replication, hosted gates/timing and candidate checks remain.

Handoff and full updated PR body are prepared as local management artifacts. No PR edit, push or merge was performed. Suggestions remain under #495.
