[A614]

# Lane 737 handoff

Status: resumed after the fourth ruling; implementation and validation in progress. Workflow scheduling, replay resources and manifest collectors are committed. Install-cache audit and complete workflow-gate execution are in progress.
Previous public STOP, resolved by the fourth ruling: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6162388253
Previous STOP, resolved by the third ruling: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161757784
Branch: `737-ci-30min`. Base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Current author HEAD: `97488b829` (full identifier will be refreshed after final verification).
Current tree: `e86889bb3a28eb3769397be6bf74a0ff18791a79`.
The protocol-shadow commit remains the completed comparison snapshot tree;
the later commits add source-cache provenance and the manifest foundation.
Origin was confirmed as `https://github.com/kebag-logic/milan-fpga.git`; this resume began at the requested `f37cd06463fa473d0804bc192ddf83b2e598346a`.
Existing partial work was preserved. No new TAKEN comment was posted.
No push, PR operation, merge, rebase or hardware operation occurred.

## Fourth-ruling resume

The requested resume head and origin were verified. The fourth ruling
(https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6162403147)
resolves hosted cancellation scope and counter receipt handling.
Same-repository events may cancel sibling workflows; fork contexts must never
request write permission. Counter registrations may select an exit-status,
RESULT-line and complete-stdout receipt without adding a check tally.
The rejected two-thread media-clock trial will not be retained.
No new TAKEN comment was posted. Standing implementation authorization applies.

## Public authority

- [Assignment, round 1](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160775078).
- [Driver ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160937413).
- [Finer split guidance](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160973660).
- [Datapath split pointer](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161015079).
- [Manifest design](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160962404).
- [Second STOP ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161122704).

All earlier rulings, guidance, signature and fail-fast comments were read exactly.
The [third ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161771913)
resolves the timing STOP. Hosted acceptance remains with the coordinating role.
The executor is [A614]; the independent reviewers are [R636] and [R637].
The manifest key and prebuilt-layer publication remain with the coordinating role.

## Hosted cancellation contract, resolved

The fail-fast directive, [comment 6161180121](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161180121),
requires the failed job's `if: failure()` step to cancel its own run and the
other three workflows for the PR head using minimally scoped `actions: write`.
The four workflows accept public-fork `pull_request` events:
`rtl.yml:6`, `rtl-fast.yml:6`, `docs.yml:6`, `elaborate.yml:46`.
The repository API reports public visibility and forking enabled.

[GitHub's permission rules](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
downgrade a public-fork PR's token to read access; cancellation requires write
access to Actions. Declaring the requested permission in these jobs cannot
provide the required cancellation for this existing event class.
A [trusted workflow_run controller](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run)
is a possible solution, but introduces a separately privileged event path and
requires default-branch installation. It changes the stated job-local design.
Narrowing the cancellation requirement to same-repository PRs changes scope.
Neither decision has been made privately. No event or permission was changed.

Historical decision request, now resolved by the fourth ruling:
same-head cancellation applies only to same-repository events.
This follows AGENTS.md section 2's requirement to publish specification
conflicts and obtain a decision, rather than silently selecting an interpretation.
The earlier media-clock timing STOP is resolved and is not the reason for this STOP.

Reproduction reads, all read-only:

```sh
gh api repos/kebag-logic/milan-fpga --jq '{private,visibility,allow_forking}'
gh api repos/kebag-logic/milan-fpga/actions/permissions/workflow
```

## Media-clock timing boundary and permitted trials

The assignment says to STOP if a test cannot be sharded without changing it.
The preserved 31-case media-clock campaign now has an exact executed union and
matching checked outputs, but its longest shard is still dominated by clean leg A.
`tb/verilator/milan_dp_mclk/sim_mclk.cpp:1090` executes one continuous history:
initial lock, following measurement, CSR checks, echo, three seconds of loss,
loss/recovery, timestamp-uncertain edges, and the accumulated counter invariant.
The recovery at `:792` depends on that history and reacquires real lock at `:819`.
The final counter check is at `:1082`.
Resetting or independently seeding the later rows changes the tested history;
replaying the complete prefix in a separate leg preserves the same critical path.
No such semantic change has been made.

| Measurement | Wall seconds | Result |
|---|---:|---|
| Hosted complete suite at 7032bca5, rounded up | 2034 | Passed |
| Local full 31-case campaign | 462.87 | Passed |
| Largest of four local shards | 434.51 | Passed |
| Original standalone clean A pilot | 428.72 | 55 checks passed |
| Same A with final compiler optimization override | 441.52 | Identical checked output |
| Same A with alternate compiler and optimization | 414.49 | Identical checked output |
| Earlier two-thread simulation experiment | 590 operational cap | Incomplete; returned 124 |
| Resumed two-thread background experiment | 1650.76 before termination | Incomplete; signal 15; rejected |

The case split improves the observed critical path by 6.13 percent.
Proportional scaling of the hosted baseline predicts 1909.38 seconds (31m49s)
for the suite component alone, before workflow setup. The best standalone
compiler trial improves A by only 3.32 percent; even applying that improvement
to the whole shard predicts 1846.00 seconds (30m46s), again before setup.
These are estimates, not a hosted rerun or proof about all possible optimizations.
There is no defensible under-30-minute prediction from the tested changes.
The compiler versions differ between the local trials and hosted baseline.
`media-clock-boundary.json` records the calculation and its limits.

The third ruling permits bounded threading, profile-guided optimization, compiler flags
and model artifacts. It forbids changing the carried history and permits REVIEW READY
with an honest remaining timing projection. The current driver-only split does not establish the requested workflow
budget while preserving its history and checks. No workflow timeout was raised,
no case was dropped, and no compiler experiment was committed.
The resumed two-thread pilot was still incomplete after 27m30.76s, over 3.85
times the original complete A runtime. Its maximum child RSS was 4212 KiB.
It was terminated and rejected, not recorded as a pass; the timing footer
prints an exit field of zero alongside signal 15, so that field is not a verdict.
An initial unsupported-option invocation returned 1 and was corrected.
No full-campaign equivalence is claimed for the threaded build.

## Changes and validation boundaries

Committed first step: `11e6ab17280301941c8111d0e3b268bbb578a997`
(`Expose media-clock case scheduling with verified execution receipts`).

| File:line | Change |
|---|---|
| `tb/verilator/milan_dp_mclk/Makefile:29` | Forwards optional `MCLK_ARGS` to the original campaign. |
| `tb/verilator/milan_dp_mclk/mclk_mutants.py:251` | One derived inventory feeds default execution, listing and optional shard selection. |
| `tb/verilator/milan_dp_mclk/mclk_mutants.py:265` | Records actual case outcomes and complete checked-output digests. |
| `tb/verilator/milan_dp_mclk/sim_mclk.cpp:1177` | Optional output observation uses the existing passing-check printer; predicates are unchanged. |
| `scripts/ci_case_receipts.py:43` | Deterministic partition of the driver's inventory. |
| `scripts/ci_case_receipts.py:56` | Verifies tracked bytes/modes, clean index, dependency roots/origins/pins, and absence of untracked source. |
| `scripts/ci_case_receipts.py:118` | Records completed cases and rechecks source identity before publishing. |
| `scripts/ci_case_receipts.py:156` | Exact union, ownership, successful verdict and source identity verification. |
| `scripts/ci_case_receipts.py:227` | Compares every sharded observation with the complete reference. |
| `scripts/ci_case_receipts_selftest.py:32` | Real repository controls for dirty source and identity. |
| `scripts/ci_case_receipts_selftest.py:78` | Derived-inventory, missing-case, duplicate, wrong-head and changed-output controls. |
| `tb/verilator/pp_shadow/Makefile:31` | Honors `VERILATOR_JOBS` while preserving its prior default. |
| `tb/verilator/pp_shadow/Makefile:147` | `RUN_CASES` owns both default `run` and `ci-list`; original builds and executable arguments are separated. |
| `scripts/ci_make_cases.py:28` | Reads the suite-owned inventory. |
| `scripts/ci_make_cases.py:39` | Builds and grades actual execution; rejects failed, absent, unparsed or zero-check results. |
| `scripts/ci_make_cases.py:54` | Runs all cases by default, with bounded concurrency and optional partition/receipt. |
| `scripts/ci_make_cases_selftest.py:12` | Real make-process controls for compilation failure, masked failure, absent verdict, zero checks and invalid inventories. |

The first media-clock comparison used one clean detached validation snapshot,
`9dd0817da6d3f771a3bd1db5eca0f2ba63d0695d`, tree
`400014889795f67503735b59ce2a997ae1906de4`.
All five campaigns ran at that same head. The final author commit adds only
annotations and docstrings to receipt support relative to that snapshot.
The protocol-shadow comparison uses snapshot
`1266235253618b0ad4448b10b9cdf09ecc780db3`, tree
`4711f4d36bac99f4ce82dedfee144c8b83c47a72`.
These snapshots contain actual committed inputs; receipts were never attributed
to dirty working-tree bytes or relabelled with another head.

## Split inventories, union proofs and real controls

| Suite | Inventory authority | Cases | Legs | Proof |
|---|---|---:|---:|---|
| Media clock | `mclk_mutants.py:251`, derived from three clean modes and the mutation table | 31 | 4 | Complete full/sharded comparison passed; all 16 real mutants caught in their owning legs. |
| Protocol shadow | `pp_shadow/Makefile:147`, shared `RUN_CASES` | 4 | 4 | Complete full/sharded comparison passed; existing pending-write mutant still catches K10 and K12. |

The media-clock inventory is 3 clean legs, 12 schemata controls and 16 mutants.
It was emitted independently with the driver's `--list`, never reconstructed
from received shard claims. All 31 case records match the reference, including
outcome, process status and the hash of every checked output line.
The verifier reads and hashes the retained output files as well as the JSON.
`mclk-equivalence.log` records the successful production comparison.
`mclk-actual-controls.log` removes a clean case and a real mutant from every
leg and every claimed inventory in turn; the independent driver inventory
causes both modified sets to be refused.

The general self-test also refuses a missing whole leg, duplicate leg, wrong
suite/head/tree/schema/coordinates, unsuccessful or signal-terminated cases,
missing output digests, changed retained bytes, and a changed observation even
when its receipt hash is updated to match. Dirty-source controls cover ordinary
edits, assume-unchanged and skip-worktree flags, staged changes, deletion,
mode changes, symlink substitution, untracked source and a mid-run source change.
All these control commands return 0 only when the planted defect is refused.

The protocol-shadow default contains `base`, `vid73`, `crf`, `pending`.
Its complete reference passes 609, 609, 649 and 317 checks respectively (2184 total).
The four selected runs have byte-identical observations for all four cases.
`pp-equivalence.log` records the production verifier pass.
`pp-actual-controls.log` records refusal after dropping `pending` from every
leg and every claimed inventory.
The existing `pending-mutant` control returned 0 in 509.58 seconds, maximum child RSS 448952 KiB.
Its clean control passes all 317 checks; the planted late-mark defect produces
the required K10 and K12 failures (12 failing checks total).
`pp-pending-mutant.log` retains the named failure evidence.
No existing assertion expression or control predicate is modified.

Both support steps are committed after their substantive comparisons passed.
No hosted union job has been added. The remaining mandated splits
(`milan_dp`, `capture_coherence`, `maap`, `milan_dp_render`, docs and elaboration)
are not implemented. The actual datapath recipe has twelve ordinary builds,
plus compressed-time synchronization legs, render mutants and four counter runs;
the split pointer's nine-build summary must not be used as its inventory.

## Local measurements and reproducible commands

| Media-clock invocation | Wall seconds | Maximum child RSS KiB |
|---|---:|---:|
| Complete campaign | 462.87 | 455924 |
| Shard 0/4 | 434.51 | 456040 |
| Shard 1/4 | 329.73 | 456140 |
| Shard 2/4 | 318.23 | 456044 |
| Shard 3/4 | 190.13 | 456964 |

A clean media-clock build took 30.18 seconds. Simulation dominates this split,
so the measurements do not justify a separate model-artifact build job yet.
The alternate builds and their actual compiler commands remain only in scratch.

The sequential protocol-shadow attempt reached the operational 590-second
foreground-command limit in its final case and returned 124. No complete
receipt was produced or accepted. The rerun schedules two independent cases
at once and passes in 376.69 seconds; it uses warm build products.
The test's own deadline was not raised. Full cold-job timing is not claimed.

| Protocol-shadow invocation | Wall seconds | Maximum child RSS KiB |
|---|---:|---:|
| Complete reference, two concurrent cases | 376.69 | 40552 |
| Shard 0/4: base | 153.03 | 35568 |
| Shard 1/4: vid73 | 152.42 | 40532 |
| Shard 2/4: crf | 162.30 | 40512 |
| Shard 3/4: pending | 229.85 | 40552 |

These runs reuse model products; the earlier cold case builds measured roughly
24 to 30 seconds each. The default case work totals about 698 seconds locally,
with the longest owning leg about 230 seconds. A rough proportional split of
the 1029-second hosted suite window predicts about 339 seconds for its longest
case before duplicated setup; this is not an implemented workflow prediction.


The following environment was used for substantive simulations:

```sh
export TMPDIR=$VALIDATION_STORAGE/737-a614
export PATH=$VALIDATION_STORAGE/737-a614/venv/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
export PYTHONDONTWRITEBYTECODE=1
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export VERILATOR_JOBS=2
export MAKEFLAGS=-j8
```

The interpreter matches hosted 3.12.3. At most two model builds ran together;
campaign concurrency never exceeded four. Earlier measurements used foreground commands; resumed long simulations used
background sessions with short foreground polls, as instructed. No simulation
took the exclusive implementation-tool lock.
Use a fresh evidence directory: existing receipt paths are deliberately refused.
From a clean checkout with the necessary pinned dependencies initialized:

```sh
CI_EVIDENCE=$(mktemp -d "$TMPDIR/case-replay.XXXXXX")
HEAD_OID=$(git rev-parse HEAD)
TREE_OID=$(git rev-parse 'HEAD^{tree}')
python3 tb/verilator/milan_dp_mclk/mclk_mutants.py --list > "$CI_EVIDENCE/mclk-inventory.json"
make -j8 -C tb/verilator/milan_dp_mclk run MCLK_ARGS="--receipt $CI_EVIDENCE/mclk-full.json"
for leg in 0 1 2 3; do
    make -j8 -C tb/verilator/milan_dp_mclk run MCLK_ARGS="--shard $leg/4 --receipt $CI_EVIDENCE/mclk-$leg.json"
done
python3 scripts/ci_case_receipts.py --inventory "$CI_EVIDENCE/mclk-inventory.json" --suite milan_dp_mclk --head "$HEAD_OID" --tree "$TREE_OID" --reference "$CI_EVIDENCE/mclk-full.json" "$CI_EVIDENCE/mclk-0.json" "$CI_EVIDENCE/mclk-1.json" "$CI_EVIDENCE/mclk-2.json" "$CI_EVIDENCE/mclk-3.json"
python3 scripts/ci_make_cases.py --suite pp_shadow --list > "$CI_EVIDENCE/pp-inventory.json"
python3 scripts/ci_make_cases.py --suite pp_shadow --jobs 2 --receipt "$CI_EVIDENCE/pp-full.json"
for leg in 0 1 2 3; do
    python3 scripts/ci_make_cases.py --suite pp_shadow --shard "$leg/4" --receipt "$CI_EVIDENCE/pp-$leg.json"
done
python3 scripts/ci_case_receipts.py --inventory "$CI_EVIDENCE/pp-inventory.json" --suite pp_shadow --head "$HEAD_OID" --tree "$TREE_OID" --reference "$CI_EVIDENCE/pp-full.json" "$CI_EVIDENCE/pp-0.json" "$CI_EVIDENCE/pp-1.json" "$CI_EVIDENCE/pp-2.json" "$CI_EVIDENCE/pp-3.json"
make -j8 -C tb/verilator/pp_shadow pending-mutant
```

Support gates executed successfully for the touched code:

```sh
python3 scripts/ci_case_receipts_selftest.py
python3 scripts/ci_make_cases_selftest.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/measure_test_evidence_readers.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py
python3 scripts/measure_fail_fast.py --check
git diff --check
```

The initial signature/docstring gate findings were fixed and the original gate
passed afterward. No gate or acceptance check was weakened to get a pass.
The evidence registry records the individual logs, sizes and hashes.

## Hosted durations before and predicted after

Measured head: `7032bca5a51d8d97fcb73d7fc106ca4af21de38e`.
Job durations come from each job's API completion minus start. The retained
JSON includes every job, step, conclusion and timestamp. Workflow wall clocks
span the first non-skipped job start to the last completion, including gaps:
`rtl-full` 77m29s; `elaborate` 35m44s; `docs` 34m00s; `rtl-fast` 19m03s.
Workflow scheduling is unchanged. Source-tool cache keys now invalidate on
source or recipe changes; their timing effect is unmeasured. Warm-cache
predictions remain approximately the baseline, with no cold-cache estimate.
These are not acceptance claims for a new layout.
The split-layout after values are unavailable because that layout is unfinished.

## rtl-full (run 38495894214)

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894214/jobs
```

| Job | ID | Before | Predicted after |
|---|---:|---:|---|
| full-ci-gate | 115631441324 | 0m50s | Approximately before on a warm cache |
| Yosys shard 0/4 | 115631699014 | 8m14s | Approximately before on a warm cache |
| Yosys shard 3/4 | 115631699114 | 0m31s | Approximately before on a warm cache |
| Yosys shard 2/4 | 115631699117 | 0m32s | Approximately before on a warm cache |
| Verilator shard 0/5 | 115631699137 | 69m48s | Approximately before on a warm cache |
| Verilator shard 3/5 | 115631699169 | 60m09s | Approximately before on a warm cache |
| Verilator shard 2/5 | 115631699198 | 70m10s | Approximately before on a warm cache |
| Verilator shard 1/5 | 115631699214 | 68m38s | Approximately before on a warm cache |
| Verilator shard 4/5 | 115631699226 | 55m32s | Approximately before on a warm cache |
| Yosys shard 1/4 | 115631699385 | 0m25s | Approximately before on a warm cache |
| Physical gPTP (nightly and manual) | 115631700715 | 0m00s | Approximately before on a warm cache |
| verilator-suites | 115653077431 | 0m07s | Approximately before on a warm cache |
| yosys-portability | 115653119397 | 0m08s | Approximately before on a warm cache |

## elaborate (run 38495894212)

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894212/jobs
```

| Job | ID | Before | Predicted after |
|---|---:|---:|---|
| elaborate | 115631440899 | 35m44s | Approximately before on a warm cache |

## docs (run 38495894291)

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894291/jobs
```

| Job | ID | Before | Predicted after |
|---|---:|---:|---|
| wire-accountability | 115631441194 | 0m09s | Approximately before on a warm cache |
| docs-check-no-git | 115631441331 | 0m12s | Approximately before on a warm cache |
| docs-check | 115631441482 | 33m59s | Approximately before on a warm cache |

## rtl-fast (run 38495894211)

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894211/jobs
```

| Job | ID | Before | Predicted after |
|---|---:|---:|---|
| bdd-conformance | 115631440905 | 0m14s | Approximately before on a warm cache |
| changes | 115631441106 | 0m29s | Approximately before on a warm cache |
| yosys-elaboration | 115631592055 | 11m00s | Approximately before on a warm cache |
| verilator-lint | 115631592063 | 0m40s | Approximately before on a warm cache |
| publication-census | 115631592079 | 18m25s | Approximately before on a warm cache |
| firmware-control-mutants | 115631592083 | 16m21s | Approximately before on a warm cache |
| firmware-verilator | 115631592089 | 11m10s | Approximately before on a warm cache |
| firmware-unit | 115631592104 | 10m45s | Approximately before on a warm cache |
| firmware-srp-mutants | 115631592115 | 12m32s | Approximately before on a warm cache |
| firmware-boundary | 115631592117 | 15m19s | Approximately before on a warm cache |
| firmware-aecp-mutants | 115631592128 | 3m48s | Approximately before on a warm cache |
| rtl-fast | 115636758266 | 0m04s | Approximately before on a warm cache |


## Cache keys and prebuilt layers

Source-built Verilator and Yosys caches changed in commit
`48eefcca4561a5283c66c508dbecbadb731220dc`.

| Tool | Version | Verified source commit |
|---|---|---|
| Verilator | v5.050 | `848d926ebd4addacacd294dc84e35d9d4ae8078c` |
| Yosys | v0.66 | `86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51` |

Exact key forms are:

```text
verilator-${{ env.VERILATOR_VERSION }}-848d926ebd4addacacd294dc84e35d9d4ae8078c-${{ hashFiles('.github/workflows/*.yml') }}-${{ runner.os }}
yosys-${{ env.YOSYS_VERSION }}-86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-${{ hashFiles('.github/workflows/*.yml') }}-${{ runner.os }}
```

Each source clone must match the recorded Git object before compilation.
The workflow-file digest binds the complete recipe; cosmetic workflow edits
also invalidate the cache. Existing runtime version checks remain required.
There is no new restore fallback or claim that a cache hit proves execution.
The exact carriers are `rtl.yml:190,237,347,503`,
`rtl-fast.yml:92,153,269,559`, and `elaborate.yml:278`.
The new source-identity checks are at `rtl.yml:202,248,358,514`,
`rtl-fast.yml:104,164,280,571`, and `elaborate.yml:290`.

The RV32 SDK key already binds its archive digest and installer recipe.
Markdown downloads bind requirements; elaboration downloads bind dependency pins;
the Scala cache remains OS-only. Those install keys still need the assignment's
complete version/source/recipe audit. No image definition was changed.
Prebuilt-layer publication and digest adoption remain separately owned work.

## CI contract replacement ledger

The second ruling authorizes the following replacements; source-cache assertions
are implemented, while topology assertions remain pending.
The earlier refusal is resolved and is not a new blocker.

| Existing assertion | Replacement status | Required control |
|---|---|---|
| `scripts/ci_events.py:501`, job key/strategy allowlist | Pending new worker/aggregate definitions | Unexpected worker or aggregate key refused |
| `scripts/ci_events.py:912`, docs step inventory | Pending complete per-leg and aggregate inventories | Omitted or altered step refused |
| `scripts/ci_events.py:1161`, elaboration step inventory | Pending complete per-leg and aggregate inventories | Omitted or altered step refused |
| `scripts/ci_events.py:1762,2870`, required carriers and no-needs rule | Pending protected fail-closed aggregates | Missing, failed, cancelled and skipped leg each refused |
| `scripts/ci_events.py:2105,2114`, source-build keys and `:8135`, `_tool_cache_arms` | Implemented exact version/source/recipe keys | Every relevant carrier refuses missing version, source or recipe; complete 3142-arm self-test passes |
| `scripts/ci_events.py:4042`, pinned carrier verification | Pending new complete contract | All existing negative controls retained |
| `docs/testing/CI_WORKFLOWS.md:2633`, public carrier rule | Pending same-change update | Documentation matches enforced topology |

## Replay CPU, concurrency and memory model

The requested change to 16 CPUs per container and four actually overlapping
jobs/workflows is not implemented. Existing values remain:
`act_ci.py:102` four CPUs, `:108` 16g container memory with equal memory+swap,
`:119` concurrency one, `:124` default parallel factor four, `:131` four slot
ranges, and `:181` a 24G slot cap. Workflows still execute serially.
Simply changing constants would not prove four-way overlap or safe lifecycle
handling, so no partial resource-policy change is committed.

Earlier peak service memory was 5218357248 bytes. The resumed service peaked
at 6315200512 bytes (about 5.88 GiB),
under the 9 GB operating ceiling and 12884901888-byte service limit.
Individual media-clock build/campaign maximum child RSS was about 456964 KiB.
These observations include at most two builds and the bounded simulation work;
they are not four-job replay peaks and do not justify new container/slot limits.
No four-job memory model, container ranges or actual replay evidence is claimed.
The pinned replay implementation nests matrix concurrency inside outer job
concurrency. Setting both existing limits to four can produce sixteen active
containers, so changing only constants cannot implement the shared four-job cap.
No scheduling rewrite or resource-limit change was committed.
All background campaigns have exited; none remains active. The final source-byte
check confirms the clean author head and all initialized dependency pins.
The unchanged runner self-test was not run on the host from candidate source.
The coordinating role still owns the full trusted replay and hosted timing run.

## Manifest schema and comparison controls

Implemented case-receipt schema 1 has exactly `schema`, `suite`, `head`, `tree`,
`inventory`, `shard`, `results`; each result has exactly `case`, `outcome`,
`returncode`, `output_sha256`. Sorted, compact JSON binds observations to retained
output files. Source bytes and modes are verified at both start and finish;
index flags cannot hide changes. The schema is an internal execution receipt,
not the required complete workflow manifest or a cryptographic signature.
Its implemented comparison controls are listed in the union-proof section.

The seven-section workflow envelope and comparison foundation are now committed
at `f37cd06463fa473d0804bc192ddf83b2e598346a`:
`subject`, `definitions`, `environment`, `plan`, `execution`, `inventories`,
`results`. The envelope carries schema 1, the canonical payload, its SHA-256,
a recomputed completeness flag, incomplete reasons and excluded observations.
Canonical JSON uses sorted UTF-8 keys and integer numeric values. Duplicate
keys, floats and undocumented envelope fields are refused. Only wall-clock,
runner, CPU count, logs and cache observations are excluded from comparison.
Plan and execution job maps must match; each step outcome and inventory union
must support success. Conditional skips currently refuse completeness pending
integration of condition-evaluation receipts.

The controls pass: seventeen planted section differences, extra plan/execution/
result jobs, omitted and duplicated cases, mismatched verdicts, two identical
cancelled collections, forged completeness, duplicate keys and invalid JSON types.
The production comparator names differing payload fields and independently
recomputes the digest and completeness claim.

This validates supplied collection records for internal consistency only.
Hosted API collection, local runtime telemetry, source-derived plan recomputation,
independent inventory validation, immutable environment collection and signing
remain incomplete. The `emit` command packages supplied records; it does not
collect or authenticate a build. No valid full-workflow signature is claimed.
The coordinating role supplies the signing key; only its public key belongs
in the repository.

## Context and artifact hygiene

Read the requested control firmware README and adp/acmp/maap/srp/loop/mbx/app
contracts; unit harness and coverage gate; image build and linked-image audits;
workflows, source-list and evidence-reader gates; and TSN stack README, import
policy, boundary checker and validator. No firmware behavior or linked image changed.
Only the four needed dependencies were initialized: axis, protocol processor,
time processor and TSN stack. Each root and origin was checked before its Git
operations. The TSN stack retains its public HTTPS origin and pinned commit;
no submodule branch was pushed or changed to the prohibited development branch.

All toolchains, environments, builds and large logs remain in assigned disk
scratch. Ignored bytecode created in the candidate was moved to scratch.
No generated file was hand-edited, and no generated/scratch file is committed.
Every file in the management output is below 200 KB; large evidence is described
by size and SHA-256 in `scratch-artifacts.json`. The registry is not a substitute
for the retained bytes. No independent review or completion ledger is claimed.
Former STOP text files remain historical and do not describe this head.

## Resume after the third ruling

Committed source-cache step: `48eefcca4`.
The three source-tool workflows now key installations by release version,
verified Git source-object digest, workflow recipe SHA-256, and operating system.
The cloned release must resolve to the recorded source commit before compilation.
The recipe digest covers `.github/workflows/*.yml`; cosmetic edits also miss.
No fallback was introduced and the existing version checks remain mandatory.
Other install-cache work remains pending.

| Artifact | Change or evidence |
|---|---|
| `.github/workflows/rtl.yml:190` | Verilator source/recipe cache key; clone identity check follows. |
| `.github/workflows/rtl-fast.yml:92` | Same source/recipe policy for fast Verilator and Yosys jobs. |
| `.github/workflows/elaborate.yml:278` | Same shared Verilator provenance. |
| `scripts/ci_events.py:8135`, `_tool_cache_arms` | Each existing tool-cache carrier rejects missing version, source or recipe. |
| `docs/testing/CI_WORKFLOWS.md:2759`, Source-tool cache provenance | Documents source identities and cache miss policy. |

CI contract check: 2,174 items pass. Its complete self-test passes 3,142 arms.
The Python idiom, hygiene, documentation, contents and documentation-style gates pass.
The em-dash self-test passes 339 arms; the base comparison passes separately.
These are provenance-contract results, not a new cold tool-build or workflow timing claim.

Datapath scheduling is saved as `partial-datapath-scheduling.patch`, not committed
as a completed step. The author worktree is clean. The isolated validation
checkout still contains its clean committed snapshot.
The Makefile derives its default and selected inventory from prefix, ordinary and suffix cases.
All nineteen cases remain: two compressed synchronization cases, four counter cases,
twelve ordinary models, and the render mutation campaign.
The original bounded pool still owns ordinary default simulations, including frame-dump serialization.
The counter cases use their existing isolated scratch and now precede the ordinary pool.
The unchanged pool gate passes all 17 process and recipe arms.
The supplied 3.12.3 interpreter lacks `os.pidfd_open` and refuses this gate before any arm;
the successful process-gate run uses the system interpreter. No assertion was changed.
The source-list self-test passes 50 controls; evidence and reader gates pass.
The full datapath reference failed with exit 1 after 2274.94 seconds
(37m54.94s), maximum child RSS 493644 KiB, on snapshot
`e3ba81c8c109bcd3ed36cc99ff7dd5a66df8228d`, tree `4151e8513ef5de24e9808365a92763e205c692f2`.
All nineteen subprocesses returned zero. The four counter drivers expose only
`RESULT: PASS`, without a numerical check tally. The unchanged generic receipt
runner correctly refuses these as insufficient count evidence. Fifteen other
cases pass its grading, including the render campaign's six existing controls.
This is an integration failure in the proposed scheduling adapter, not evidence
of a firmware assertion failure. No count was invented and no gate was weakened.
The full/sharded comparison was not attempted; no union proof exists for this patch.

Before accepting the patch, expose the counter drivers' existing checked-value
transcripts without changing their predicates, separate render phase timing
observations from compared check values, and address shared build/output
ownership before running multiple selected datapath cases concurrently.
The uncommitted Makefile changes are at `:370,423` (synchronization build/run),
`:556` (shared nineteen-case inventory), `:576` (original bounded ordinary pool),
`:712` (render campaign) and `:719` (counter cases). The complete patch is retained.
`resume3-datapath-result.json` records the actual refusal; the 1691480-byte full
log and retained per-case bytes remain in scratch with registry hashes.

The resumed two-thread media-clock pilot was terminated after 1650.76 seconds
and rejected. Its corrected invocation used `+MCLK_CHECK_VALUES=1`;
no acceleration is retained from the incomplete trial.

The seven-section manifest transport module and comparison controls are committed
after their checks passed.
It explicitly refuses incomplete evidence, including two identical cancelled collections.
Collector integration, source-derived plans, conditional-skip evaluation, signing and image adoption
remain unfinished. Its comparator alone is not authenticated execution evidence.


| File:line | Manifest foundation change |
|---|---|
| `scripts/ci_manifest.py:28` | Strict canonical JSON encoding and digest inputs. |
| `scripts/ci_manifest.py:94` | Recomputed step, result and inventory completeness. |
| `scripts/ci_manifest.py:152` | Seven-section envelope and explicit excluded observations. |
| `scripts/ci_manifest.py:192` | Refuses forged digest/completeness before comparison. |
| `scripts/ci_manifest.py:222` | Field-by-field comparison of complete supplied collections. |
| `scripts/ci_manifest_selftest.py:45` | Planted differences, incomplete evidence and invalid JSON controls. |
| `docs/testing/CI_SIGNATURE.md:17` | Schema, comparison and unfinished collection/authentication boundary. |

Additional successful commands for the two resumed committed steps:

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_manifest_selftest.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check docs/testing/CI_WORKFLOWS.md
python3 scripts/gen_toc.py --check docs/testing/CI_SIGNATURE.md
python3 scripts/check_doc_style.py
python3 scripts/check_em_dash.py --base fa7347fc
python3 scripts/check_em_dash.py --selftest
```

All listed corrected commands returned zero. Earlier invalid command-line probes
are retained separately and are not passes: the documentation checker has no
`--no-git` argument, and the em-dash base and self-test modes are exclusive.
The post-commit em-dash comparison passed over 117 added lines in two Markdown files.
The cache self-test log is 204855 bytes and remains in scratch with its size/hash;
it is not copied into this output directory. No complete local merge gate,
trusted replay, hosted result, or independent review is claimed.

## Fourth-ruling implementation progress

The saved datapath scheduling patch is restored for validation.
The four counter cases now declare `result-stdout` through their Makefile registration.
That form requires exit zero and exactly one `RESULT: PASS` line.
It records that line and hashes complete stdout, without inventing checks.
The render campaign's optional phase observer writes to stderr for case receipts.
Its verdict stdout remains compared; timing does not enter the comparison.
Shared Makefile prerequisites and selected model builds run sequentially.
Execution respects the existing frame-dump serialization variable.

Receipt controls pass, including changed stdout with a recomputed digest.
Source-list, evidence, reader and hygiene checks pass.
The unchanged pool gate initially exposed a changed default command spelling.
The default retains its literal render command and final position again;
the corrected pool gate passes all seventeen controls.
The isolated reference passed at `bf54a090e` in 16m24.23s (peak process RSS 479608 KiB).
It predates that default-recipe correction and remains measurement evidence.
No full/sharded datapath equivalence is claimed yet.
The corrected reference and four legs are running sequentially at `e06f342f5`.


## Committed source-plan step

Head: `53fb88f9fbc37d4e5b7c4b5a4adcaf2a36a97e58`.
`scripts/ci_workflow_plan.py:59` parses bounded workflow data with duplicate-key and alias refusal.
`scripts/ci_workflow_plan.py:72` expands only literal matrix axes.
`scripts/ci_workflow_plan.py:146` resolves every dependency to its expanded legs and rejects cycles.
`scripts/ci_workflow_plan.py:188` reads immutable workflow Git blobs.
`scripts/ci_workflow_plan.py:214` binds a supplied manifest plan, definitions, and tree to those blobs.
`scripts/ci_workflow_plan_selftest.py:51` plants changed commands, missing jobs, false trees, and ambiguous matrix/dependency inputs.
`docs/testing/CI_SIGNATURE.md:64` documents the source-plan check and its execution/authentication limits.

The source-plan controls, manifest controls, Python idiom, hygiene, documentation links/style,
contents, whitespace and em-dash checks returned zero.
The em-dash check is commit-based; its pre-commit pass covered the earlier head.
No runtime collector, signature, hosted timing, or complete replay is claimed by this step.

```sh
python3 scripts/ci_workflow_plan_selftest.py
python3 scripts/ci_workflow_plan.py --head f37cd06463fa473d0804bc192ddf83b2e598346a
python3 scripts/ci_manifest_selftest.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check docs/testing/CI_SIGNATURE.md
python3 scripts/check_doc_style.py
python3 scripts/check_em_dash.py --base fa7347fc
git diff --check
```


## Current validation and uncommitted work

The corrected datapath reference at `e06f342f5c35ccd71c1902e32747422245407afa`
passed in 17m00.88s, peak child RSS 477028 KiB. Its four selected legs are still running.
The separate campaign snapshot is `068802530`.
The MAAP reference passed all 66 registered cases in 11m56.40s,
peak child RSS 468852 KiB; the selected legs are still running.
Both sets retain full case output and source-bound receipts in scratch.
No final union or author commit is claimed until all legs compare.
The service memory peak observed while both campaigns ran was 4385386496 bytes,
with current usage below the 9 GiB operational ceiling.

Additional scheduling changes awaiting real comparisons:

- `tb/verilator/maap/mutants.py:253`: derives the 66 whole-suite cases from the existing registration;
  the standalone Makefile harness and original mutant predicates stay intact.
- `tb/verilator/maap/Makefile:38`: exposes the standalone execution after its existing build.
- `tb/verilator/capture_coherence/mutants.py:540`: names existing build/harness units and observes their outputs;
  whole-suite mode includes both original full default harnesses.
  All original grading, anchor, control, build and refusal functions are AST-identical to `f37cd064`.
- `tb/verilator/capture_coherence/Makefile:28`: permits the existing build parallelism to be bounded.
- `tb/verilator/milan_dp_render/Makefile:207`: shares a three-group inventory with default execution;
  the leg-defect campaign still follows both clean default runs.
- `scripts/ci_maap_cases_selftest.py:31` and `scripts/ci_capture_cases_selftest.py:29`:
  scheduling, observation-isolation, failure-preservation and omission controls pass.

The docs and elaboration splits are generated, not hand-edited.
`.github/ci-templates/docs.yml` and `.github/ci-templates/elaborate.yml` retain the original ordered steps.
`scripts/ci_gate_workflows.py` assigns every original non-setup step to one of two legs.
`scripts/ci_gate_receipts.py` records actual step outcomes and checks their exact source-bound union.
The protected carriers retain their names and require both successful jobs.
The source commands remain checked by the existing semantic workflow assertions;
the generated physical graphs are additionally compared in full with their generator.
The old negative controls still exercise those original semantic assertions.
A new physical-graph control bank targets missing/changed steps and job bypasses.
The live contract passes 2176 items; its expanded self-test is currently running.
Generator/union controls pass for 41 docs gates and two elaboration gates,
including missing/failed/cancelled/skipped jobs and a gate dropped from all claims.
Full local gates for these workflow changes are not yet complete.

The baseline step windows justify the partitions: the 1065-second builder gate
leaves the docs core with the other gates; the 1441-second elaboration gate and
593-second standalone simulation gate run in separate jobs. Remaining setup,
collection and aggregate time must be added to those projections.
No hosted after-duration or valid complete replay is claimed.


## Completed MAAP and datapath comparisons

`4b3d69911` commits MAAP scheduling after all 66 cases matched across the full run and four legs.
There are three passing clean cases and 63 caught real mutants.
`resume4-maap-equivalence.json` names the exact comparison head and tree.
The actual last datapath mutant was then dropped from every leg and every claimed inventory;
the independent driver inventory caused the collection to be refused.

The datapath step is now committed. All 19 cases matched across the full run and four legs at
`e06f342f5c35ccd71c1902e32747422245407afa`.
`resume4-dp-equivalence.json` records the exact head/tree and actual omission controls.
Dropping either the last counter case or the complete render mutation campaign is refused.
The pool and phase-observer controls pass in a disposable CPython 3.12.3 container.
The source-list, receipt, Make runner, Python idiom, hygiene, and source-evidence gates also pass.
The protocol-shadow cases are being rechecked with the shared updated Make runner.

The render and capture full/sharded campaigns are now running at `068802530`.
The author render default recipe again spells its mutation command directly, so the evidence
reader retains the original 35 armed suites rather than losing the nested target to its static reader.
This spelling correction does not change the selected-case commands under measurement.

The generated workflow contract passed 2184 assertions and all 3537 controls.
Its previous seven count-message failures were corrected from 50 to 51 after adding the new
scheduling/evidence control gate; all seven planted defects were already refused.
The disposable runner self-test passes after reading both actual elaboration worker scopes.
Its scope commands remain identical, and its fixture now bounds each named job's text.
The old four-CPU resource model is still present; this is not the requested resource-policy validation.

A container control exposed missing ambient Git identity in the new source-plan fixture.
The fixture now constructs test commit objects with the source commit's existing attribution,
without changing Git configuration. The CPython 3.12.3 container control passes.
This test portability correction is uncommitted pending the surrounding workflow step.

## Render completion and scheduling continuation

The render scheduling change is committed as `2ea5a0872`. The three complete
cases match their unsharded reference, including the five real leg-defect controls.
The protocol-shadow recheck with the shared runner also completed: all four
cases match at `e06f342f5`. The actual last case dropped from every leg and
claimed inventory is refused for both suites. Their comparison JSON files
record the exact snapshots and trees.

The cache and generated gate contract passes 2184 assertions and 3554 controls.
The docs source gates are running locally; the compiler-absent and builder
gates remain in flight. A missing local WaveDrom dependency was installed in
the scratch environment, and the unchanged diagram gate then passed.
The direct and isolated-file runner selftests both passed in the disposable
CPython 3.12.3 job container.

The planned local concurrency implementation materializes each source matrix
into concrete generated jobs, retaining the original ID as a fail-closed
status carrier. This avoids multiplication of the runner's outer job limit
by its nested matrix limit. The source matrix remains the leg inventory.
This implementation choice preserves commands and test predicates.
It is not wired into the workflow or replay runner yet.

## Dispatcher and runtime continuation

The committed matrix materializer is `e1b93f16b`. Its Cartesian-union,
command-preservation and 26 executed carrier refusals pass. Generated workflow
integration is still uncommitted. The concrete-worker limit reader retains
the previous scheduling controls; its selftest passes.

`e09a7f9cb` adds the pinned dispatcher build recipe and a separate fail-fast
dispatcher selected only for workflow scheduling. The existing upstream
dispatcher and all its tests are unchanged. Twenty race-enabled repetitions
prove four active jobs, no admission after failure, cancellation and joined
cleanup; the unchanged upstream common test package passes too. The complete
recipe was then run successfully. `dispatcher-build-receipt.json` records
source, compiler, patch, recipe and binary digests and size. No binary is
placed in this output directory.

The uncommitted replay policy uses sixteen CPUs per job, four global jobs,
eight GiB per container including swap and a 36 GiB isolated-slot cap. It
copies byte-identical selected workflow files to a private directory and
starts one shared scheduler, verifying both the original sources and copies
before and after execution. Structured scheduler events are retained outside
the artifact upload directory. A failed job interrupts the process-group
boundary, followed by owned-container and volume cleanup.
The updated offline selftest is still being completed; no passing final
resource-policy validation or four-job memory measurement is claimed yet.

The docs builder passed in 1017.498 seconds with only its existing missing
bench-calibration skip. Compiler-absent controls passed in 438.178 seconds;
the saved-state writer passed in 82.979 seconds. Other executed docs gates
and their exact return codes are retained in scratch under `docs-gates`.
Capture coherence's full reference passed 32 checks in 1667.92 seconds;
its first two of four selected legs have passed and the rest remain in flight.

## Capture and suite scheduling continuation

Capture scheduling is committed as `3c3f38934`. All 31 units have identical per-case outcomes and checked-output hashes in the full run and four legs. The original 32 campaign checks remain, including the grouped datapath control. Removing the final actual mutant from every claimed inventory and result list is refused. The full log and combined leg logs both tally 21196 checks with the unchanged reader.

The uncommitted CI mode schedules 79 units over 16 workers. Fifteen workers project at most 1605 seconds including a conservative 122-second setup allowance. The continuous media-clock history runs alone on worker 15, projected at 2032 seconds including setup. Its documented exception remains. Original serial sweep commands and all test predicates remain intact. Six generated union jobs derive fresh inventories, verify case receipts and assemble the original suite logs. The unchanged tally gives equal full/sharded counts for datapath (11956), capture (21196), MAAP (252), render (342), and pending-command controls (2184). Scheduling and omission controls passed. Runtime collector and cancellation integration are still being implemented.

## Native matrix and memory completion

The final scheduling design retains hosted native matrices, including fork PR matrix cancellation. The earlier materializer is superseded. Commit c3ab1b2b111c4037a534b5b79d89f233bc27933d enforces one global four-leg admission bound across nested matrices and workflows, with repeated race-enabled controls.

Four real Yosys shards ran concurrently on disjoint sixteen-CPU ranges with eight GiB memory and swap caps. All returned zero. Their measured cgroup peaks were 2635010048, 1635954688, 889298944 and 646090752 bytes; their elapsed times were 493, 282, 141 and 97 seconds. Every memory.events counter was zero. The sum of peaks is 5806354432 bytes (5.41 GiB), an upper bound rather than a simultaneous measurement. An earlier two-GiB sizing trial killed the largest shard; the other three passed. That failed trial is retained. The proposed isolated-slot cap is 36 GiB, comprising four eight-GiB containers plus four GiB for the daemon and services.

The scope-history gate now executes its unchanged history and planted-defect predicates against both generated elaboration workers; it passed. Runtime evidence, final offline runner controls, cache audit, documentation and the remaining workflow gates are still being completed.

The final offline runner selftest, including its isolated flat-file child, passed under CPython 3.12.3 in a disposable container. New controls cover fresh out-of-tree evidence directories, changed and linked helper refusal, genuine job-start telemetry and first-failure process-group cleanup. Runtime collector transport and hostile-import controls pass. The complete topology control sweep is in progress before committing the integrated workflow step.

A final dispatcher trace found that an upstream failed step records JobError but returns nil after cleanup. The earlier admission gate could therefore admit a queued leg before the outer stream observer reacted. The correction exposes the recorded error to admission before releasing its token; a nested-matrix control models that exact convention. The ci3 dispatcher recipe and its controls are in progress; ci2 is superseded and must not be used for the final replay.

## Integration contract ledger (pending commit)

| Previous assertion | Replacement | Executed control |
|---|---|---|
| ci_events.py original docs-check and elaborate step sequences | Original ordered commands pinned in .github/ci-templates; the entire generated graph pinned independently | Existing mutation arms retained; every generated job and step has omission, condition, body and masking controls |
| ci_events.py five-worker source matrix and aggregate | Source projection retains its original contract; generated matrix has sixteen workers, exact denominator and six required unions | Physical graph mutations; suite selector inventory, capacity and ownership controls; strict collector omission and duplication controls |
| ci_events.py version-only compiler cache key | Exact version, source revision and workflow recipe hash, no broad fallback | Removing each identity component is refused |
| ci_events.py permissive install cache fallback | Exact renderer, LiteX and Scala inputs and workflow recipe hash | Missing version/source/recipe and broad-fallback controls |
| ci_scope_history.py:150 scope body read from old elaborate job | Both generated worker bodies are bounded by job before extraction and each executes every existing history predicate | Unchanged divergent-history and planted-classifier controls pass for both workers |
| act_ci.py previous single-job/four-CPU policy | One four-leg dispatcher, exclusive sixteen-CPU ranges, eight-GiB containers and 36-GiB isolated slot | Original resource and containment controls retained, plus nested admission, first failure, copied-workflow drift and collector boundary controls |

Final line references and command/result inventory will replace these provisional pointers after the integrated step is committed.

The ci3 dispatcher completed its full pinned-source build, twenty race-enabled repetitions (including the stored-error convention), unchanged upstream common tests and version check. Removing recorded-error propagation from the disposable source was refused by the new control. The small dispatcher-build-receipt.json now names the final executed recipe and binary; the binary itself stays in scratch. The CPython 3.12.3 direct and isolated-file runner controls also pass with the ci3 requirement.

The integrated workflow, union, local-resource and collector step is committed as aa196ae7a. The contract passed 2186 items and all 4467 negative arms; the case-union, physical-log collector, manifest, source-plan, runtime-transport, cancellation, scope-history and original suite-selector controls passed. The author worktree is clean. Remaining firmware gates are running from the separate validation worktree at that commit, using CPython 3.12.3 and the pinned compiler versions in a disposable local container. This container use is validation only; the shipping workflows still use caches, not the prebuilt image.

Commit 9a76ed5cf bounds the capture campaign at its hosted four-case admission level when a local job has sixteen CPUs. Inventory and collector controls pass. All sixteen generated suite worker selections are now being executed from an isolated worktree at that head. A scratch-only admission wrapper invokes the supplied pinned compiler and allows at most two simultaneous model builds, with two compiler workers each; campaign pools are limited to four. Its resource limit does not alter case selection, simulator inputs, deadlines or verdict predicates. The firmware campaign runs independently at aa196ae7a.

The remaining cache audit now covers Python dependency URLs with exact versions and SHA-256, sv2v archive reuse, the pinned field-oracle build, and distribution package archives keyed by the live resolver's exact version and source inventory plus the recipe. All 28 constrained Python sources downloaded with their hashes verified. A fresh CPython 3.12.3 environment installed the existing hash-pinned reference/Markdown requirements and constrained YAML, behavior and diagram dependencies successfully. The actual APT planner and package installation passed in a disposable hosted-shaped container. Full topology controls and constrained LiteX installation are in progress before this cache step is committed.

The first generated-suite run was an environment refusal: its container lacked the repository's alternate object store, so it could not read the bound source tree. That attempt is retained under full-ci-gates/missing-object-store. The corrected run mounts only those Git objects read-only and has reached the actual datapath simulation. No test predicate or receipt check was weakened.

## Install-cache audit completed

Head: `97488b829` (exact source and recipe cache bindings). The complete workflow
contract passed 2,186 items and 4,897 planted arms. The disposable CPython 3.12.3
local replay self-test passed, including the global nested four-job scheduler.
All 28 constrained Python source archives were independently downloaded and
SHA-256 checked. Fresh Markdown, HDL, evidence, BDD and diagram installs passed;
the pinned LiteX install with those constraints passed. The resolved APT plan
and actual GoogleTest/GoogleMock install passed in a disposable Ubuntu job.
Logs remain in scratch and will be catalogued by size and SHA-256.

The full selected suite campaign and firmware mutation campaign remain active.
The elaboration trial first found container cache permissions, then the missing
home-relative RV32 SDK alias required by the unchanged census. Both environmental
trials are retained; the gate was restarted after providing those prerequisites.
No test predicate or product source was changed.

## Gate resource follow-up

The first full selected worker passed at `9a76ed5c` (worker 0, 1,115.397 s).
The sequential validation launcher was stopped during worker 1's disposable
preflight so remaining workers can be admitted across isolated worktrees.
Worker 1 is not counted and will run again in full. Its interrupted log remains
in scratch. This is validation scheduling, not a suite or workflow change.

The lint trial exposed Python 3.12's host-wide default CPU count under CPU
affinity: its implicit pool exceeded a 4 GiB validation container. The trial is
retained. The workflow now explicitly passes `--jobs 4` to lint, publication,
saved-state and coverage drivers; this matches the hosted four-CPU width and
preserves all cases and checks. The explicit lint retry passed, followed by the
source-list and BDD gates. Contract controls are rerunning before commit.

The original no-metadata docs job removes `.git` before running its two checks.
The new runtime recorder must retain the checkout head/tree before that step,
then record its actual outcomes afterward. This collector-only correction is
in progress; the original no-metadata test body remains unchanged.
