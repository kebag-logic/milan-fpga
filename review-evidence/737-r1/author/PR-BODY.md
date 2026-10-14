[A614]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

REVIEW READY for round one: sixteen workers, six unions and 62 physical logs pass; 2,187,186 checks, zero in-suite failures. `737-ci-30min` -> `dev`.

Head: `cf9c936697a06e44c41681bcc12dc612a3242eb2`.
Round-one scheduling, resource policy, caches and manifest collectors are implemented.
Hosted after-times and a full trusted replay remain with the coordinating role.

| Workflow | Measured baseline at `7032bca5` | Warm-cache projection |
|---|---:|---|
| docs | about 34m00s | about 26 minutes including collection |
| elaborate | 35m44s | about 30 minutes including collection |
| rtl-fast | 19m03s | about 22 minutes including collection |
| rtl-full | 77m29s | Still above 30 minutes: continuous media-clock worker projects at 33m52s before downstream collection |

These are predictions, not new hosted measurements. The issue's third and fourth rulings
permit review readiness with the remaining media-clock timing reported honestly.
Cold builds, queue time and new artifact overhead must be measured on the pushed head.

## Linked Issue / roles

Relates to #737

Executor: `[A614]`
Internal cleared-context reviewer: `[R636]`
External reviewer: `[R637]`

## Description

The longest serial suites previously kept the exhaustive workflow running for over an hour.
Six suite-owned inventories now expose independently scheduled case groups. Six final union
jobs require every case exactly once, and the protected aggregate rechecks their receipts
and original physical-suite logs. Docs and elaboration each have two source-derived gate
workers and retain their protected check names as strict aggregates.

The local dispatcher admits at most four jobs across workflows and nested matrices. Each
container is created directly on a manager-supplied, aligned sixteen-CPU range and keeps
that range until cleanup. The named fallback is twelve CPUs, aligned to twelve. Missing,
undersized and overlapping bookings are refused. Each job has an 8 GiB memory cap; an isolated slot
is capped at 36 GiB. First failure closes admission, stops running work and preserves actual
failed, cancelled and unstarted outcomes. Native hosted matrices remain fail-fast. A guarded
same-repository watcher cancels sibling workflows at the same head; fork PRs retain matrix
cancellation and strict aggregates without a write-token controller.

Every generated job derives compiler and campaign budgets from its visible CPU count.
Campaigns keep their measured four-worker ceiling; nested capture builds divide the compiler
budget. The dispatcher reserves ranges before initial container creation, and a read-only
monitor rejects overlap or movement. The slot proof forwards explicit external bookings.

Installation caches bind exact versions, source identities and recipes. The workflow contract
checks both the original ordered gate commands and the complete generated job graph.
Both execution paths emit the canonical seven-section manifest from actual observations.
The comparison recomputes source plans and refuses any changed or incomplete evidence.

All six split suites have same-head full/sharded per-case equivalence with real defect
controls retained. Before the placement rewrite, four real synthesis shards passed concurrently for memory sizing;
their individual memory peaks summed to 5.41 GiB. That sum is an upper bound, not a measured
simultaneous peak. The final dispatcher passed repeated race-enabled admission controls and
the unchanged upstream tests. The final workflow contract passes 2,186 items and 5,020
mutation controls. The offline runner and all 44 slot-proof controls pass. All sixteen workers, six real unions and the physical collector/tally pass.
Simulation evidence is bound to its retained snapshot; source correspondence records its
unchanged product and test artifacts at this candidate.

## Authoritative references

- Issue #737 assignment, driver and topology rulings, fail-fast directive and fourth ruling.
- CPU rules 6166855177, moved into round one by 6167284204, with the twelve-CPU correction 6167288337.
- [Workflow policy](docs/testing/CI_WORKFLOWS.md).
- [Signature contract and round-one boundary](docs/testing/CI_SIGNATURE.md).
- [Verification requirements](REQUIREMENTS.md#8-verification-and-release-acceptance).
- [Contribution and merge rules](CONTRIBUTING.md).

## How to get into the same state

Use CPython 3.12.3, Verilator 5.050, Yosys 0.66 and the dependency pins installed by the
workflows. Install only the submodules these gates use, then verify each initialized root
and its own origin before operating in it.

```sh
git switch 737-ci-30min
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
python3 --version
verilator --version
yosys -V
```

## How to validate

```sh
python3 scripts/build_ci_act.py --directory "$ACT_BUILD_DIR"
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_gate_workflows_selftest.py
scripts/act_slot_proof.sh --selftest
python3 scripts/ci_suite_pieces_selftest.py
python3 scripts/ci_suite_collect_selftest.py
python3 scripts/ci_case_receipts_selftest.py
python3 scripts/ci_make_cases_selftest.py
python3 scripts/ci_maap_cases_selftest.py
python3 scripts/ci_capture_cases_selftest.py
python3 scripts/ci_install_cache_selftest.py
python3 scripts/ci_fail_fast_selftest.py
python3 scripts/ci_manifest_selftest.py
python3 scripts/ci_workflow_plan_selftest.py
python3 scripts/ci_runtime_evidence_selftest.py
python3 scripts/generate_ci_evidence_pins.py --check
python3 scripts/lint_rtl.py --check --self-test --jobs 4
python3 scripts/pp_srcs.py --check --selftest
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
```

Choose new scratch directories on disk for the build, evidence and suite-log variables.
Run each workflow's original firmware, builder, standalone simulation, synthesis and docs
gates too. The handoff provides exact executed commands, case receipts, controls, durations
and log sizes/hashes. Keep scratch and build products outside the source tree and evidence
bundle. Run the candidate runner's offline self-test only inside a disposable CI job:

```sh
python3 -I scripts/act_ci.py --selftest --worktree "$PWD"
```

The coordinating role performs the complete replay through the separately trusted runner,
with explicit booked ranges, then records all four hosted wall clocks and compares completed
manifest collections.

```sh
python3 -I "$TRUSTED_RUNNER" --pr "$PR_NUMBER" --cpu-ranges "$BOOKED_CPU_RANGES" \
  --evidence-directory "$EVIDENCE_DIR"
```

Expected result: every required gate returns zero; planted defects are refused; complete
case unions contain no omissions or duplicates. Incomplete manifests are always refused.

## Known limitations / out of scope

- Continuous media-clock leg A retains its complete state history. Its projected history is
  31m49s, or 33m52s including setup. The owner decides any remaining runner choice after measurement.
- Round one keeps caches and existing GitHub PR triggers. Prebuilt image/layer adoption,
  trigger changes, immutable action pins, key publication,
  signing and evaluated conditional-skip proof remain round two.
- Current manifests explicitly remain incomplete where those proofs or the collector's final
  result are unavailable. Hosted synthetic merge subjects and local head subjects are not normalized.
- Live cross-workflow cancellation and the final hosted after-times require the coordinating
  role's run. The author used API fixtures and disposable local gates and did not push.
- Physical nightly/manual timing remains a separate campaign. No firmware behavior, linked
  image, test predicate or hardware state is changed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
