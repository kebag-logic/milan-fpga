[A839]

Relates to #998. Findings filed as #996, #999 and #1000.

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally — every changed suite byte-identical to the base; hosted-shard replicas 9 and 11 pass (18068 + 487
checks, 0 failures) — `cicd-verilator-perf` -> `dev-soft-core`

## Linked Issue / roles

Relates to #998

Executor: `[A839]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Measured with perf on the heavy targets before any change (per-suite counters, call-graph profiles of the longest
simulations, whole-suite attribution by process). Three levers survive the rule that a lever changing any verdict
or graded figure is dropped:

| Change | Why | Measured (paired, same host load) |
|---|---|---|
| `probes.vlt` in place of `--public-flat-rw` in crf_rx, mmcm_servo, aaf_clock_meter, maap | `--public-flat-rw` makes every signal public, so Verilator re-evaluates the whole input-combinational network on every eval: 45 % of talker_step's cycles. Each harness touches a handful of internal signals; probes.vlt lists exactly those (writable only where the harness writes). | CPU -37 / -26 / -27 / -10 %; talker_step instructions -49 %, L1i misses -99.6 %; whole-suite logs byte-identical |
| `OBJCACHE=ccache` in the suite runner where ccache is installed | Every build and mutant rebuild recompiles the Verilator runtime (most of a small model's compile) and the unchanged testbench | crf_rx's 23 mutants: CPU -47 % on a cold cache (-54 % warm), results identical; avtp_rxmon -65 % cold (receipts re-attributed in the `author-r1b` packet); no effect where ccache is absent (the hosted runner today) |
| `OPT_FAST=-O3` for the CPU budget harness's testbench | Verilator's rule for the testbench C++ ends with its `-Os` default, after the suite's `-CFLAGS`; this harness's testbench is hot | CPU -2.5..-5 %, L1d misses 5-15 % lower in three paired runs (median 8.8 %), output md5-identical |

`ci/image/command-table.json` follows the seven changed Verilator argument lists; `docs/testing/TESTING.md`
records the ccache behaviour and the probes.vlt rule.

Measured and deliberately not applied:

- **Testbench `-O2`/`-O3` for every suite.** The models already compile at the suites' `-O2` (verilated.mk puts
  OPT_FAST before `-CFLAGS` for model files); only the testbench was at `-Os`. Changing it moves instructions by
  under 1 % on seven suites (the models dominate) and adds 4-5 s of compile per large testbench.
- **Model `-O3`.** 0-6 % on the suites measured, inside this host's paired-run noise; settle on a quiet host first.
- **probes.vlt for follow_ring and media_phase.** follow_ring fails 43 checks without `--public-flat-rw`: Verilator
  initialises the net connected to a defaulted input port with the default once that port is optimised, which
  overwrites a top-level input the harness set before its first eval (`lb_wire_chans_i`, tied to the wrapper's
  `pcm_chans_i`). media_phase's models also contain defaulted ports, so both keep the flag; a minimal reproduction
  and the bisect are in the evidence comment, and the hazard needs its own Issue.

Hosted effect (hosted suite time x measured CPU ratio): shard 11 28.6 -> ~20-22 min (crf_rx 17.2 -> ~9-11), shard 7
23.1 -> ~18.6, shard 9 18.2 -> ~14.5, each maap piece about -10 %; about 16 runner-minutes per run.

## Authoritative references

- [docs/testing/TESTING.md section 1](../docs/testing/TESTING.md#1-verilator-rtl-harnesses---tbverilator-the-live-regression): the sweep, its deadlines and (new) its build behaviour.
- [docs/testing/CI_WORKFLOWS.md](../docs/testing/CI_WORKFLOWS.md): the hosted shard layout and the act-first rule.
- IEEE 1800-2017 23.2.2.4 (default port values apply only to unconnected ports): the reason follow_ring and media_phase keep `--public-flat-rw`.

## How to get into the same state

```sh
git fetch origin cicd-verilator-perf
git worktree add ../cicd-review origin/cicd-verilator-perf
cd ../cicd-review
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
export VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS='-j1 --no-print-directory'
```

## How to validate

```sh
# 1. Same verdicts, suite by suite (each prints its tally; compare against the same suites at the base commit):
for s in crf_rx mmcm_servo aaf_clock_meter maap; do make -C tb/verilator/$s > /tmp/$s.log 2>&1; echo "$s rc=$?"; done
# 2. The hosted shards that carry them, through the real runner, as rtl.yml runs them (OBJCACHE= mimics the runner):
OBJCACHE= scripts/run_all_suites.sh "$(mktemp -d)" --ci-pieces --shard 11/19
OBJCACHE= scripts/run_all_suites.sh "$(mktemp -d)" --ci-pieces --shard 7/19
OBJCACHE= scripts/run_all_suites.sh "$(mktemp -d)" --ci-pieces --shard 9/19
# 3. The runner's own cancellation contract:
python3 scripts/test_suite_cancellation.py
```

Expected result / pass criteria: every suite `rc=0` with the same check counts and lines as at the base commit
(only build chatter and paths differ); each shard exits 0 with no TIMEOUT; the cancellation test prints PASS.

## Known limitations / out of scope

- Hosted CI gains nothing from the ccache commit until ccache is installed on the runner (a workflow, pinned
  installer and tool-inventory change; the inventory check is red at the base for unrelated stale entries).
- firmware-boundary (25.8 min) is unchanged: 93 % of it is the firmware builders' own compiles, run serially, which
  the gate captures and judges; a job split is the lever and belongs to the gate's owners.
- The preflight self-tests still run in every shard (~80 s each); running them once per head is a workflow design.
- The shard planner's SUITE_SECONDS stay as recorded until a hosted run measures the new times.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done


