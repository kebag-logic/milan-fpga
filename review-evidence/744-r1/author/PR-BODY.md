[A621]

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

GREEN locally: every touched gate passes (rc 0) at `f643377f15c0d939d875ae5698672f1b0a99a644`, `744-slot-oom` -> `dev`.

Still outstanding before #744 can close: the full four-job act replay at this head, which is the coordinating receipt for item 2.

## Linked Issue / roles

Relates to #744
Relates to #737

Executor: `[A621]`
Internal cleared-context reviewer: `[R636]`
External reviewer: `[R637]`

## Description

#742's replay failed twice on `rtl-fast/publication-census`: 111 of 120 self-test arms died with sv2v `exit -9`. The kernel recorded 210 memory-cgroup OOM kills inside the slot, but the runner printed `the cap was hit 0 time(s), with no OOM at it`. Two defects:

| Item | Change |
|---|---|
| 1. Truthful slot accounting | `scripts/act_ci.py` reads the slot slice's hierarchical `memory.events` (`oom`, `oom_kill`, `max`) and `memory.peak` before the slice is removed. It used to read `memory.events.local`, which counts only the slice's own limit and so misses every kill at a job container's 8 GiB limit below it. Any `oom` or `oom_kill` writes `slot-memory.json` with `"valid_build": false` beside the manifest, prints the accounting ending `valid build: False`, and exits 2 naming both counts, whatever the jobs returned. Unreadable or incomplete events, and a cgroup2 mount with `memory_localevents`, refuse as unprovable. A body that raises keeps its exception, and the accounting is printed beside it. |
| 2. Census fits the slot by construction | The generator (`scripts/ci_runtime_workflows.py`) adds `Set memory-derived census workers` to any job naming `CI_CENSUS_JOBS`, today only `publication-census`. It sets `CI_CENSUS_JOBS = max(1, min(nproc, floor(2 * M / (3 * 1234825216))))`. M is the smaller of `MemTotal` and every numeric `memory.max` from the job's own cgroup up to the root it can see. The template `.github/ci-templates/rtl-fast.yml` and its contract in `scripts/ci_events.py` use `--jobs "$CI_CENSUS_JOBS"`, and `.github/workflows/rtl-fast.yml` is regenerated. An act job container (8 GiB, 16 CPUs) gets 4, and so does a hosted runner (16 GiB, 4 CPUs). |
| 3. Re-pin and docs | New `scripts/act_ci.py` SHA-256 `9ce3a6604486c99209333430b09f8892bc2a5c0f5ed87b052a2ddc85577ffee8` (dev: `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd`). `docs/testing/CI_WORKFLOWS.md` describes both behaviours with their measurements, and `docs/design/MAILBOX_SPLIT.md` describes the census parallelism. |

Measurements, all native (no act, no Docker):

- **Per-sv2v peak.** GNU time `-v` wrapped each tool of `publication_census.py --check --jobs 1` at the `84f9e300` datapath, with sv2v v0.0.12 and Yosys 0.66. sv2v peaked at 1167000 to 1205884 KiB per shape, so the largest is 1234825216 bytes (`CENSUS_WORKER_BYTES`). Yosys peaked at most at 386824 KiB.
- **Bounded census under the job container's bound.** The emitted budget step and census command ran in a transient scope with `MemoryMax=8G` and `MemorySwapMax=0`. The step chose 4 workers of 16 CPUs. The census passed 234 checks, 0 of 120 arms failed and all 31 rules were proved, in 591 s. The scope's peak was 5806784512 bytes (67.6% of the cap), and every `memory.events` counter was zero.
- **Negative control.** The same cap at `--jobs 16` reproduces #742: 113 of 120 arms failed with `exit -9`, with `oom_kill 209`, `oom 2298`, and the peak at the cap.
- **Native OOM control.** A 400 MiB allocation was OOM-killed in a 200 MiB scope below a 36G slice. The slice's `memory.events` read `oom 1 oom_kill 1`, and its `memory.events.local` read zero. dev's reader printed `the cap was hit 0 time(s), with no OOM at it`; this head's reader refused with both counts.

Tests:

- **Runner self-test.**
  - #742's shape: hierarchical kills beside clean local events, every job passing.
  - A real kernel's events after one kill, with every job passing and with a job failing.
  - An OOM without a kill, and a kill without an OOM event.
  - Each malformed input, an unreadable mount table, a missing cgroup2 mount and a `memory_localevents` mount.
  - The report beside a body's exception.
  - A planted kill driven through `run_validation` and `execute_workflows` to the refusal and `slot-memory.json`.
- **Mutants.** Seven mutants of the fix were each caught, with 1 to 18 failing arms:
  - reading `memory.events.local` again
  - dropping either refusal
  - ignoring `oom`
  - dropping the local-events guard
  - dropping the report beside an exception
  - refusing before the manifest is written
- **Generator self-test.** `scripts/ci_gate_workflows_selftest.py` executes the emitted shell over planted `/proc` and cgroup files in 11 cases, and checks that only `publication-census` gets the step, ahead of its census.

## Authoritative references

- #744 and its assignment and clarification comments; #737; #742's failed replay as summarised on #744.
- `docs/testing/CI_WORKFLOWS.md`: Act-first local replication, Parallel replay slots (resource bounds), and the census job paragraph under Fast feedback.
- `AGENTS.md` sections 5 to 7, and `CONTRIBUTING.md` sections 2 and 3.
- Linux cgroup v2: `memory.events` is hierarchical unless cgroup2 is mounted with `memory_localevents`, and `memory.events.local` is local.

## How to get into the same state

```sh
git fetch origin
git switch --detach f643377f15c0d939d875ae5698672f1b0a99a644
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --require-hashes --no-deps -r ci/requirements-evidence.txt
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

Use CPython 3.12.3, with the sv2v v0.0.12 release that `rtl-fast.yml` pins and Yosys 0.66, set as `SV2V` and `YOSYS`.

## How to validate

```sh
python3 scripts/act_ci.py --selftest
install_dir="$(mktemp -d)"
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_gate_workflows_selftest.py
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
sha256sum scripts/act_ci.py
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 -p OOMPolicy=continue \
  python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
```

Expected result / pass criteria:

- Every command exits 0.
- The runner self-test prints `selftest: PASS`: 610 ok arms direct, 608 isolated, since the two flat-install meta-arms run only in the direct form.
- `ci_events.py --selftest` prints `PASS (2187 contract items, 5218 arms)`.
- `ci_gate_workflows_selftest.py` prints the 11 `Census budget:` cases, including `act job container: 4 worker(s)`.
- The digest is `9ce3a660...ffee8`.
- The capped census reports 0 of 120 arms failed and 0 of 31 rules unproved.

## Known limitations / out of scope

- The four-job act replay at this head, the item 2 receipt, is run by the coordinating role and reported on #744 before review. This PR therefore uses `Relates to`.
- Slot 0 has no slice, so an OOM there is still not counted (documented). Only isolated slots enforce and read an aggregate cap.
- The bound reads cgroup v2. On a v1 host only `MemTotal` would be read.
- `CENSUS_WORKER_BYTES` is a measurement of today's datapath. A datapath that grows sv2v's peak needs a new measurement.
- On an OOM, `ci-manifest.json` is still written, and its completeness reads only job receipts. `slot-memory.json` and the rc 2 refusal carry the invalidity.
- No product test, census check or RTL changes.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 2's act replay receipt is outstanding)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
