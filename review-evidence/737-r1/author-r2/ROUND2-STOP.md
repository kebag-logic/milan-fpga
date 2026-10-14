[A614] STOP - round 2, item 4 resource decision

Head: `21bd10cec1a999791c9cd2c6d37c52372fb1504e` on `737-ci-30min`, local only. The worktree is clean. No push or PR modification occurred.

The required dev merge was the first commit; the conflicting census count was regenerated to 161 controls. Subsequent commits correct the nested compiler budget, hosted inventory prerequisites and fixture identity, skipped matrices, observer retries and rate limits, collector/watcher-tail cancellation, each worker's own headroom, exact cache documentation, and combined dependency dispatch without stage barriers.

Validation completed:

- Workflow contract: 2,186 items and 5,093 planted arms pass. Real child-recipe controls reject unlimited compilation; media-NCO passes 410 checks. Both borrowed-timeout and disabled-1620-second-bound controls are refused.
- The final dispatcher passes twenty race repetitions, upstream controls and the disposable offline runner self-test. Two real scheduling fixtures start a ready dependent while an unrelated job remains running; the previous dispatcher fails both. The combined fixture also reuses a job ID across workflows. Start times and the final build receipt are retained.
- All six full/sharded comparisons at public PR head `cf9c936697a06e44c41681bcc12dc612a3242eb2` pass the production receipt CLI: datapath 19 units/4 legs, media clock 31/4, capture 31/4, MAAP 66/4, renderer 3/3, protocol-shadow 4/4. All 154 units match outcomes, return codes and checked-output digests; each suite refuses a case dropped from every claim and detects an altered observation.
- Source-list, evidence-reader, runtime/manifest, cancellation, slot-proof and final documentation controls pass. The public-head comparisons do not claim unchanged product inputs after the required dev merge; the merged candidate still needs its full replay.

Inside the existing 8 GiB job cap, measured sixteen/twelve-CPU peaks are:

| Class | Sixteen CPUs | Twelve CPUs |
|---|---:|---:|
| Census, four campaign workers | 5.458 GiB | 4.844 GiB |
| Heaviest synthesis shard | 3.488 GiB | 3.158 GiB |
| Firmware normal phase, including required RV32 checks | 1.272 GiB | 1.279 GiB |

Every memory-event counter is zero. The census passes 234 normal checks, 120 planted arms and 31 rule removals at each width, covering the regression from 6170460727 with the emitted four-worker budget.

**STOP:** item 4 still requires shipped-width large-compiler and four-build capture measurements, plus the remaining per-class replay peaks, including builder/JVM jobs. The session instruction limits Verilator to four compiler processes per build and at most two simultaneous builds. I did not override that instruction, raise the cap, reduce shipping budgets or change a test to obtain a pass.

Requested decision: provide the coordinating replay's per-job sixteen/twelve-CPU peaks and OOM events, or explicitly permit scoped measurements of one 8 GiB container at a time using the shipped compiler/capture widths. The 8 GiB job and 36 GiB slot allocations remain unproven for those classes. The prior replay stopped before the remaining RTL jobs and supplies no such measurements.

`HANDOFF.md` and `PR-BODY.md` contain Round 2 sections. The packet includes the twelve-commit ledger, six-suite receipts and comparison controls, memory receipts, dispatcher start times, baseline/projection qualifications, file:line map and log size/SHA-256 index. All started tests are finished. Hosted timing, live cancellation evidence, publication, repinning and independent re-review remain outstanding; no review approval or completed acceptance bar is claimed.
