# A183 F1 correction handoff

Status: REVIEW READY for independent correction review. Source is committed, clean and unpublished. Scoped author validation and fresh performance measurements are complete. No review verdict or F1 resolution is supplied by the author.

Issue: https://github.com/kebag-logic/milan-fpga/issues/517
PR: https://github.com/kebag-logic/milan-fpga/pull/524 (draft)
Assignment: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5783551963
Independent finding: https://github.com/kebag-logic/milan-fpga/pull/524#issuecomment-5783500849
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5783591287
Public design: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5783614556

Source head: `ff7dac3257a321538a1fd1a310ab3190f646153d`
Source tree: `f72080e7b96b078ce996926d8ccec66c1ca3dc74`
Correction parent: `5874895eb817ed41c0f8be4eb427ad3315c29844`
Implementation base: `483a133ed08867ea0d300d2b4a027b5b48a4282f`
Branch/worktree: `517-bounded-simulation-pool`, `$CANDIDATE`.
One-line commit: Make simulation pool cancellation independent of stdout backpressure.

## Correction

The original runner blocked INT/TERM while replaying output synchronously. A stalled pipe prevented it reaching sigwait and child cleanup. The immutable reviewer's direct and exact-Makefile probes reproduced this for both signals: cancellation acceptance exit 1, no owned pidfd exit event while blocked, then signal exit and reaping only after draining. `original-direct`, `original-make`, their command receipts and acceptance JSON retain these failures. The later drain is solely the old-defect positive control.

The runner keeps its single owner, blocked-signal launch/cleanup discipline, process groups and descendant adoption. It assembles the ordered binary transcript in `obj_legs/replay.log`, then uses nonblocking stdout writes with an explicit byte cursor. Pending cancellation is consumed before writes and during output capacity waits. A 50 ms capacity retry has no simulation timeout, pass/fail or cycle meaning. Descriptor blocking flags are restored before another launch or shutdown. No additional process or thread is introduced.

On cancellation, the existing cleanup kills groups, reaps direct children and kills/reaps adopted descendants, including new sessions. The disk transcript is then completed from existing per-leg captures, including failure/cancellation and unstarted-leg attribution. The final stdout attempt never waits for capacity. The runner ends by its original cancellation signal. A blocked consumer therefore cannot be a cleanup prerequisite; normal runs still deliver complete ordered bytes. Interrupted stdout may be a prefix; the complete available transcript and individual complete/partial captures stay on disk.

Files changed: suite runner, suite README, original runner-test inventory assertion, and new standalone backpressure regression. The first existing test adds replay.log to its exact inventory and additionally compares its bytes against the original transcript. All 17 original arms remain; all other original arm bodies are byte-equivalent ASTs. The 24 phase arms are unchanged.

## Scope preservation

`scope-proof.json` binds fixed artifacts and every budget to the correction parent. The Makefile, model/harness executable behavior, render driver, phase observer, sweep, tally, shard owner, workflow, checker and processor pins are unchanged. The ten argument-free commands retain their original model distinctions, builder arguments, seeds, clocks, timers, windows, scenarios and assertions. Builds and both gPTP prerequisites precede the ordinary runner; the six-case render campaign still follows only success. At most two ordinary simulations run; the five sim_nxn header writers remain exclusive and ordered. Presence of MILAN_COUNTER_FRAME_OUT, even empty, selects whole-set legacy order.

No policy masks needed adjustment. The unchanged bare-metal checker accepts the actual workstation contexts and rejects wrong-file, unrelated-line, appended-token, altered-path/longer-token and protected-product copies. Independent public-literal probes contain 264 passing CLI controls and reject five deliberate broadenings. Every existing policy class and all 13 budgets remain unchanged. No #523 outer-sweep or gptp_shadow driver was edited; shared checker composition remains manager-owned.

## Validation

`final-controls.json` and the subordinate exact commands/raw logs bind the committed source to: 17/17 original runner arms; 24/24 phase arms; tally and ownership controls; relevant documentation, contents, em-dash, Python/shell idiom, hygiene, evidence, fail-fast and TODO gates; policy check and relevant selftests. All command exits are zero. `final-backpressure` records 28 controls: direct/real-Makefile paths, large-copy/small-flush boundaries, INT/TERM, active/child-exit/repeated-signal variants, and normal drain controls. Owned pidfds must report POLLHUP before reading stdout, distinguishing reaping from zombie exit. Parent/runner shutdown is observed within the two-second cancellation bound. Captures and deterministic binary replay are checked separately.

`final-restored-defect` replaces only the runner bytes in disposable fixtures with the exact correction parent. All eight direct/Makefile, copy/flush, INT/TERM controls reject it specifically for failure to shut down while stdout remains blocked. Their observations precede fallback cleanup. The independent actual-Makefile blackbox retained 15 positive controls and detected six planted scheduler/output/failure/cleanup defects before commit. It uses inert compilers/models solely to prove wiring; those controls claim no RTL coverage.

All preliminary failures retain their original results and attributions in `preliminary-notes.md`, raw command directories and receipts. None is relabelled as final acceptance. Real RTL totals exclude every host-runner selftest.

## Performance

| Full suite | Sequential seconds | Two-worker seconds | Saved seconds | Observed gain |
|---|---:|---:|---:|---:|
| Cold | 1133.031 | 1095.719 | 37.312 | 3.293% |
| Warm | 980.614 | 933.414 | 47.200 | 4.813% |

Every run returned make/verdict/tally exit 0 with **9324 original checks, zero failures, 13 tallies, and 23 render phase records**. All ten per-leg byte streams, their verdicts/check counts, generated/input identities, executable hashes, both prerequisite outputs and all six render outcomes match across modes. The 23 render event/case/phase/status identities also match across all four runs. Complete per-leg capture and command attribution are checked against the full raw logs. Each run preserves its ordered replay.log as an additional artifact; it is never counted as a second RTL result. All affected tracked headers match the commit before and after each run.

| Run | Ordinary span (s) | Ordinary/group peaks | Peak ordinary RSS (KiB) | Peak tree RSS (KiB) | wait4 single-process peak (KiB) |
|---|---:|---:|---:|---:|---:|
| cold-sequential | 486.221 | 1/1 | 5764 | 2721328 | 375272 |
| warm-sequential | 491.095 | 1/1 | 5764 | 2596808 | 359632 |
| cold-pooled | 450.202 | 2/1 | 11080 | 2696768 | 374896 |
| warm-pooled | 443.907 | 2/1 | 10944 | 2602376 | 359716 |

The raw process samples observe each original argument-free executable exactly once. Both pooled runs observe two ordinary legs, no more than one grouped leg, and independent/group overlap. Sequential runs observe one ordinary leg and no overlap. Memory and timing samples are observations at 0.1-second intervals, not exact simultaneous maxima. wait4 single-process peaks are separately reported. The sampled whole-tree peak across the four runs is 2721328 KiB. Host load varies and is retained in every sample; no other author bank ran alongside these measurements.

These are one local pair per temperature. Both full-suite comparisons improved measurably, satisfying the scoped local acceptance2 comparison, without a statistical repeatability or universal-percentage claim. Whole-suite timing includes unchanged build/prerequisite/render work; no build acceleration or hosted-worker speedup is claimed. The original measurements remain attributed to old7ab.


`BENCHMARK-METHOD.md` records verification of the immutable public method. Four fresh full suites use this correction commit and verified Verilator 5.050, outer make -j1, at most eight compiler jobs, CPU affinity 96-103, and a 12 GiB memory ceiling. Cold removes the suite's existing build artifacts, without filesystem-cache eviction. Warm immediately follows the same-mode cold run, retaining those build artifacts while rerunning the simulations and mutants. Old7ab figures remain attributed to 7ab1c8d0ad073fbc1977c455dea89b7b318d4e52.

## Response to F1 under its original lenses

| Original lens | Author response and reproducible evidence | Resolution owner |
|---|---|---|
| Conformance | Frozen cancellation contract exercised before any drain; ten argv/models, ordered group, frame-presence behavior and original counts preserved. See final-backpressure, scope-proof.json and measurement-verification.json. | R245 re-review pending |
| RTL | Single-threaded host scheduler retains launch/group/reap ownership. Nonblocking disk-backed replay separates stdout capacity from cancellation service. Production RTL/interfaces/pins remain unchanged. See source-diff.patch and final-integrity.json. | R245 re-review pending |
| Robustness | INT/TERM under blocked copy and flush, active descendants in new sessions, repeated signals and child-exit races terminate/reap before consumer progress. See before-drain.json receipts; original INT/TERM/HUP arms also pass. | R245 re-review pending |
| Tests | All 17 original arms and 24 phase arms retained; 28 added controls pass; eight exact restored-defect controls fail specifically for blocked shutdown. Actual Makefile wiring and binary/legacy output are exercised. See final-controls.json and raw fixtures. | R245 re-review pending |
| Docs | README and runner contract describe retained captures, complete ordered disk transcript, normal pipe replay and bounded cancellation with possibly partial stdout. Original failures, correction-head measurements and remaining duties are explicitly attributed. | R245 re-review pending |

No finding is relabelled, deferred, downgraded or author-cleared. This is not a reviewer-owned completion ledger.

## Integrity and remaining ownership

`initial-integrity.json`, `pre-benchmark-integrity.json` and final integrity receipts verify tracked bytes against Git objects, file/symlink kinds, executable modes, complete stage-0 index equality and absence of hidden index flags, with replacement objects disabled. The three registered required submodules are checked at their Git pins and by their tracked bytes/indexes. The historical external gitlink remains unchanged and is not claimed as an initialized checkout. Final checks cover 854 parent files and 539 files across the three required submodules. final-process-inventory.json records no remaining owned simulation.

Pins: third_party/verilog-axis = 48ff7a7e2ef782cf778d47910cf85835c64b1bce; protocol-processor = 424c688fa2205b934a7689a58f2aa766420f2326; gptp-processor = c1b617435824929a790739ea8585c3fe1a328cc0.

Acceptance disposition: 1-4 have the scoped author evidence above. Acceptance 5 is not claimed complete: manager banks, new CI, hosted comparison, independent reviews and final integration remain pending. See COMMANDS.md for reproduction and MANIFEST.json/SHA256SUMS for artifact identities.

R245 F1 remains open as MAJOR under Conformance, RTL, Robustness, Tests and Docs until independent re-review. The author's response for Conformance is bounded cancellation with unchanged frozen commands/outputs; for RTL it is interruptible host-output delivery and unchanged production architecture; for Robustness it is blocked-output, descendant and race coverage; for Tests it is before-drain process-state oracles plus restored-defect rejection; for Docs it is explicit interrupted-delivery and retained-transcript contracts with exact-head evidence. These are correction claims, not clean lens coverage or approval.

R245 re-review, external R246, source publication, manager full banks, trusted act/new hosted contexts and hosted timing comparison, final current-dev candidate, explicitly authorized merge and containment remain pending. No other agent/contact, source push, PR mutation, Docker/act, candidate host orchestrator/selftest, privilege, installation, hardware or other checkout edit occurred. Public issue comments were limited to the assigned author duties. No private reasoning or transcript is an evidence dependency.

Public REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5784844893
