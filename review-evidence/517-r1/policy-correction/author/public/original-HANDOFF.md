# A178 factual implementation handoff

Commit: `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`
Tree: `790849ab7fcf7c712c77fe051bb5fb6a45d830c2`
Starting dev: `483a133ed08867ea0d300d2b4a027b5b48a4282f`
Branch: `517-bounded-simulation-pool`.
Lane: `$CANDIDATE`.
Issue: https://github.com/kebag-logic/milan-fpga/issues/517
Settled decision: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780545051
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780571502

The lane is clean. One source commit, one line, no trailers. No push, PR,
merge, delegation, Docker/act, privilege, hardware operation, shared install,
or other-checkout edit was performed.

## Implementation and provenance

The Makefile passes the same ten executable paths, without arguments, and
legacy banners to a suite-local runner. SIM_JOBS defaults to 2; only 1 and 2
are accepted independently of make flags. The five sim_nxn legs are one
exclusive group in legacy relative order. Independent work can bypass waiting
group members within the total two-child limit. MILAN_COUNTER_FRAME_OUT being
present, including empty, serializes the entire ordinary set. Complete merged
stdout/stderr stays in per-child obj_legs captures and replays in legacy order.
Failures stop later launches and fail the recipe. Interrupts kill process groups
and adopt, terminate and reap orphan descendants, including separate sessions.
Partial logs remain attributable, including independent logs beyond an unstarted
group member. The unchanged render driver follows ordinary success only.

A178 restored A176's preserved pending-source runner/tests as implementation
material, then completed exclusion, replay across unstarted group members, process controls,
Makefile integration and documentation. All prior artifacts remain untouched;
recovery-provenance.json records their hashes. No A173/A176 preliminary result
is accepted as a final measurement. The only C++ change corrects an inaccurate
comment: verify_source.py proves all 47519 executable tokens unchanged. It
also proves Makefile content outside the SIM_JOBS declaration and ordinary tail
unchanged. Models, generator argv, timers, scenarios, processor pins, workflows
and ratchets stay fixed. See evidence/WRITE-AUDIT.md and source integrity receipts.

## Commands and receipts

bench/COMMANDS.md has portable commands. evidence/benchmark-command-receipts.json
records exact executed benchmark argv, head/tree, exit, timing and wait4 usage.
Each run directory contains source/tool/resource identities, input and binary
hashes, complete suite and per-leg logs, all tracked-header byte copies,
process samples, analysis, tally and verdict. scripts/suite_tally.py --verdict
and its accounting command returned 0 for each complete real suite.

All thirteen commands in evidence/committed-controls/receipts.json returned 0:
runner, phase observation, tally, ownership, docs, contents, em-dash, Python
idiom, shell idiom, hygiene, evidence, fail-fast and TODO ownership. Runner:
17/17; observation: 24/24. Exact commands, wall times and clean head/tree are
in that receipt. Six planted runner faults were rejected by assertions,
including shared-state contention, masked exit, lost output, three workers,
parallel frame writers and unreaped descendants. The last uses pidfd reaping
state before fixture cleanup, so a zombie is not accepted as containment.
See evidence/committed-mutants/command.json and receipts.json. The external
120-second guard protects synthetic controls only; no simulation deadline changes.

The preliminary-* directories are uncommitted development receipts, not final
acceptance. Only committed-* controls and the four complete runs above are
final author evidence. Prior private reasoning or reviewer context was not read.

| Acceptance | Author evidence | Pending work |
|---|---|---|
| 1: inventory/arguments/phases | Frozen ten-command integration control, unchanged build/gPTP/render recipes, one observation per ordinary executable in each run, identical binary/input hashes | Independent review |
| 2: measured speed | Complete same-head cold and warm one/two-worker pairs; full-suite gains below | Hosted comparison belongs to manager |
| 3: failures/shared state/cleanup | 17 real-process runner arms; six planted faults rejected, including contention after removing exclusivity; empty/nonempty frame-output cases; pidfd proof of descendant reaping | Independent review |
| 4: real suite/render/counts/policy | Four complete runs: 9324 checks, zero failures, 13 tallies each; 8956 ordinary checks; 24 phase controls; scoped policy checks pass with no ratchet change | Broader banks belong to manager |
| 5: full release/review/merge bar | Not claimed by A178 | Manager and reserved reviewers |

## Committed-head measurements

- cold: 1136.415 -> 1099.401 seconds; saved 37.014 seconds (3.257%).
- warm: 987.247 -> 943.330 seconds; saved 43.917 seconds (4.448%).

| Run | Full suite s | Before ordinary s | Ordinary span s | Render span s |
|---|---:|---:|---:|---:|
| cold-sequential | 1136.415 | 325.395 | 492.870 | 317.868 |
| warm-sequential | 987.247 | 169.123 | 493.832 | 324.002 |
| cold-pooled | 1099.401 | 332.875 | 445.621 | 320.491 |
| warm-pooled | 943.330 | 170.160 | 450.152 | 322.736 |

| Run | Peak ordinary/group children | Mean ordinary children | Peak ordinary RSS KiB | Peak aggregate RSS KiB | wait4 single RSS KiB |
|---|---:|---:|---:|---:|---:|
| cold-sequential | 1/1 | 0.999 | 5764 | 2686736 | 375248 |
| warm-sequential | 1/1 | 0.999 | 5768 | 2573764 | 358296 |
| cold-pooled | 2/1 | 1.089 | 10900 | 2720648 | 375188 |
| warm-pooled | 2/1 | 1.087 | 10928 | 2550360 | 358124 |

The phase spans and concurrency/RSS are observations sampled at a requested
0.1-second interval, not added tests. Aggregate RSS is the peak sum of sampled
command descendants, not an exact simultaneous host peak. wait4 reports the
separate peak single-process value. Both pooled runs observe independent/group
overlap, with at most two ordinary children and one grouped child in samples.
Failure-sensitive tests independently hold the limits and exclusion.

All runs inherit CPU affinity 96-103 (eight logical CPUs), memory.max
12884901888 bytes (12 GiB), outer make -j1 and VERILATOR_JOBS=8. The pinned
Verilator reports 5.050; its actual verilator_bin SHA-256 is
`44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`.
Driver/wrapper, compiler, Python and make identities are retained separately.

Cold means the existing suite clean target removed build artifacts; host
filesystem caches were not evicted. Warm reuses the preceding same-mode build
artifacts but reruns every simulation and mutant. One pair per temperature is
measured on this host; no guaranteed percentage or hosted gain is claimed.
Full-suite time includes unchanged builds, prerequisites and render phases.
No build-speed improvement is attributed to pooling.

Every ordinary capture matches byte for byte within each comparison. Cold and
warm sequential captures also match. Executable/input hashes, both gPTP
transcripts, all six render outcomes and the semantics of all 23 render phase
records match; measured timing fields differ. All three affected tracked-header
byte copies match the commit before and after every run. Each run ends at the
same clean head. See runs/*-comparison.json and each complete run directory.

## Pending manager and reviewer work

Manager-owned evidence remains pending: hosted dedicated-worker timing
comparison; full parent/PP/gPTP/Yosys/builder native banks; trusted act;
exact-head hosted contexts; independent R245 internal Codex and R246 external
Opus review across all five lenses; current merge-candidate validation;
authorized merge and post-merge containment. External Opus availability is
pending. This author handoff is not approval or completion of the merge bar.

Published factual author handoff: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5781648318
