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

GREEN locally at `7997eeb348c3af302079c7273d1b3092eee4dc6c`, `744-slot-oom` -> `dev`. Every `run` step of the `docs` workflow's gate jobs passes (47 of 47 rc 0), including the bare-metal scope gate. So do the generator, runner and contract self-tests, and the bounded census under an 8G cap.

Still outstanding before #744 can close: the full four-job act replay at this head, which is the coordinating receipt for item 2.

**Correction to round 1.** The round-1 body claimed that the required local verification bar passed at `f643377f1`. It did not. The bare-metal scope gate (`scripts/check_baremetal_only.py --check`, a `docs` workflow step) failed with 21 findings, and the round-1 gate list omitted it. Round 2 ran the whole `docs` workflow step set on the committed head; see [How to validate](#how-to-validate).

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
| 1. Truthful slot accounting | `scripts/act_ci.py` reads the slot slice's hierarchical `memory.events` (`oom`, `oom_kill`, `max`) and `memory.peak` before the slice is removed. It used to read `memory.events.local`, which counts only the slice's own limit and so misses every kill at a job container's 8 GiB limit below it. Any `oom` or `oom_kill` writes `slot-memory.json` with `"oom_free": false` beside the manifest, prints the accounting ending `valid build: False`, and exits 2 naming both counts, whatever the jobs returned. Unreadable or incomplete events, and a cgroup2 mount with `memory_localevents`, refuse as unprovable. A body that raises keeps its exception, and the accounting is printed beside it. |
| 2. Census fits the slot by construction | The generator (`scripts/ci_runtime_workflows.py`) adds `Set memory-derived census workers` to any job naming `CI_CENSUS_JOBS`, today only `publication-census`. It sets `CI_CENSUS_JOBS = max(1, min(nproc, floor(2 * M / (3 * 1242214400))))`. M is the smaller of `MemTotal` and every numeric `memory.max` from the job's own cgroup up to the root it can see. A present but unreadable `memory.max`, an unsearchable cgroup, a non-numeric limit, a missing `MemTotal` or zero CPUs refuse before the export. The template `.github/ci-templates/rtl-fast.yml` and its contract in `scripts/ci_events.py` use `--jobs "$CI_CENSUS_JOBS"`, and `.github/workflows/rtl-fast.yml` is regenerated. An act job container (8 GiB, 16 CPUs) gets 4, and so does a hosted runner (16 GiB, 4 CPUs). |
| 3. Re-pin and docs | New `scripts/act_ci.py` SHA-256 `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8` (dev: `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd`). `docs/testing/CI_WORKFLOWS.md` describes both behaviours with their measurements, and `docs/design/MAILBOX_SPLIT.md` describes the census parallelism. |

Measurements, all native (no act, no Docker):

- **Per-sv2v peak.** GNU time wrapped each tool at the `84f9e300` datapath, with sv2v v0.0.12 and Yosys 0.66. Over `publication_census.py --check --jobs 1`, sv2v peaked at 1167000 to 1205884 KiB per shape. Over `--check --selftest` at the bounded `--jobs 4`, the arms' sv2v runs peaked at 1212036 KiB, and round 1's arm run reached 1213100 KiB. The larger figure, 1242214400 bytes, is `CENSUS_WORKER_BYTES`. Yosys peaked at most at 386824 KiB.
- **Bounded census under the job container's bound.** The emitted budget step and census command ran in a transient scope with `MemoryMax=8G` and `MemorySwapMax=0`. The step chose 4 workers of 16 CPUs. The census passed 234 checks, 0 of 120 arms failed and all 31 rules were proved, in 591 s. The scope's peak was 5806784512 bytes (67.6% of the cap), and every `memory.events` counter was zero. Round 2 repeated this with each tool timed: it passed the same way, with a scope peak of 5569384448 bytes and every counter zero. Under real caps, the head's emitted step chose 4 at 8G, 2 at 4G and 1 at 2G.
- **Negative control.** The same cap at `--jobs 16` reproduces #742: 113 of 120 arms failed with `exit -9`, with `oom_kill 209`, `oom 2298`, and the peak at the cap.
- **Native OOM control.** A 400 MiB allocation was OOM-killed in a 200 MiB scope below a 36G slice. The slice's `memory.events` read `oom 1 oom_kill 1`, and its `memory.events.local` read zero. dev's reader printed `the cap was hit 0 time(s), with no OOM at it`; this head's reader refused with both counts.

Tests:

- **Runner self-test.**
  - #742's shape: hierarchical kills beside clean local events, every job passing.
  - A real host cgroup's events after one kill, with every job passing and with a job failing.
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
- **Generator self-test.** `scripts/ci_gate_workflows_selftest.py` executes the emitted shell over planted meminfo and cgroup files in 16 cases, including mode-000 and directory-as-limit denials at the leaf and at an ancestor. Each refusing case must print its own reason as the step's last error line, and each passing case must print no error. It also checks that only `publication-census` gets the step, ahead of its census.
- **Bare-metal gate self-test.** 129 arms prove that each declared host memory read is clean only as its whole line in its own file, including that it is refused in every other declared file, and that an unrelated new reference in the same file is refused.

## Round 2

Round 2 answers M1, R636-1 and R637-1 at `f643377f1`, as assigned on #744.

| Finding | Change |
|---|---|
| M1 = R636-1 BLOCKER = R637-1-F2: the bare-metal scope gate failed (21 findings) | As M1 ruled, the host-tool memory reads are declared, not reworded around. `scripts/check_baremetal_only.py`'s new `HOST_MEMORY_READS` table declares 14 lines whole, by file: 5 in `scripts/act_ci.py` (the mount-table read and its fixtures), 3 in `scripts/ci_runtime_workflows.py`, the same 3 in the generated `.github/workflows/rtl-fast.yml`, and 3 in `scripts/ci_gate_workflows_selftest.py`. Each `/proc` or `/sys` token is masked only inside its exact line (`(?<=^before)token(?=after$)`), the form #532 uses. Prose that only needed the word was reworded: "a real kernel's" became "a real host cgroup's", and "planted `/proc` and cgroup files" became "planted meminfo and cgroup files". 90 new self-test arms check the narrowness. An unrelated `/proc/cpuinfo`, `/sys/class/net` or `kernel` line added to any of the five files is refused on that line. So is each declared line in another file, in the product document, with text before or after it, or with a different path in its own context. `--check` reports 0 findings over 1344 files, and `--selftest` passes 790 arms. Six mask mutants are all caught. |
| R637-1-F1 MAJOR: an unreadable limit was treated as no limit | The budget step now tests `[ -e memory.max ]`. A present file that `cat` cannot read refuses before `CI_CENSUS_JOBS` is written, and so does a cgroup on the walk that exists but cannot be searched. Only an absent file means no limit. New executed controls cover a mode-000 limit, a mode-000 ancestor limit and a mode-000 ancestor cgroup, plus a limit (or an ancestor limit) that is a directory, which also refuses as root. A readable 8 GiB limit still gives 4, and a readable 4 GiB ancestor gives 2. The readable-garbage case is renamed "a non-numeric limit". Root reads through mode 000, so as root those three cases print a loud skip, as the bare-metal gate's own unreadable-file arm does. The round-1 `-r` shell fails the new controls. |
| R636-2 RESIDUE | The reviewer's exact texts, in `docs/testing/CI_WORKFLOWS.md` and in this body. |
| R636-3 SUGGESTION | Each sv2v run was measured over the self-test arms as well: 133 sv2v runs, of which 10 exited nonzero, 120 peaked at 1168056 to 1212036 KiB, and 20 were above 1205884 KiB (corrected in round 3). Round 1's arm run reached 1213100 KiB. `CENSUS_WORKER_BYTES` is now that larger figure, 1242214400 bytes, up from 1234825216. Every bound is unchanged: 8 GiB gives 4, 4 GiB gives 2, and the hosted runner gives 4. |
| R636-4 SUGGESTION | `slot-memory.json`'s `valid_build` is renamed `oom_free`, and its docs say it records only that no OOM invalidated the slot. The printed `valid build: False` line stays, since #744 item 1 names it. |

New `scripts/act_ci.py` SHA-256: `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8` (698735 bytes). The round-1 digest no longer applies.

## Round 3

Round 3 answers R636-2 at `43a25fa7e`, as assigned on #744. Five commits, `43a25fa7e..7997eeb34`:

| Finding | Change |
|---|---|
| R636-2-F1 MINOR (Docs): the sv2v counts contradicted their log | `docs/testing/CI_WORKFLOWS.md` and this body now state only counts the published per-run log reproduces. Of the 133 sv2v runs, 10 exited nonzero, 120 peaked at 1168056 to 1212036 KiB, and 20 were above 1205884 KiB. The largest, 1212036 KiB, was that run's largest process. "Elaborated the full datapath" is dropped, because the log carries no criterion for it. The reviewer's recount script on the log gives exactly these figures. The constant and every bound are unchanged. |
| R636-2-F2 RESIDUE: review labels in source comments | The three comments in `scripts/check_baremetal_only.py` now read as the reviewer wrote them. No comment in the lane's source diff names a review, reviewer or comment. |
| R636-2-F3 SUGGESTION (taken): no arm planted a declared line in another declared file | Each declared line is now also planted in every other declared file, and must be refused there as `[R]` on that line. A workflow destination is used only for an indented line, since only that sits in its block scalar unchanged. That adds 39 arms, for 829 in total. The "lines pooled across files" mutant now fails exactly those 39 arms and no others. |
| R636-2-F4 SUGGESTION (taken): the census refusal controls did not check why they refused | Each refusing case now asserts its reason as the step's last error line, as well as its nonzero exit and no export. Each passing case asserts no error output. Zero CPUs and a missing `MemTotal` used to refuse with no reason of their own, so the budget step now prints `no CPUs: nproc printed <n>` and `no MemTotal in kB`. `.github/workflows/rtl-fast.yml` is regenerated. The controls write the planted cgroup root as `<cgroups>`, so the self-test carries no new host path for the bare-metal gate to declare. The "`cat` failure ignored" mutant, outcome-equivalent before, now fails the `a mode-000 limit` control by its reason. So do dropping either new reason and dropping the unsearchable-cgroup refusal. |

`scripts/act_ci.py` is unchanged, so its SHA-256 is still `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8`.

## Authoritative references

- #744 and its assignment and clarification comments; #737; #742's failed replay as summarised on #744.
- `docs/testing/CI_WORKFLOWS.md`: Act-first local replication, Parallel replay slots (resource bounds), and the census job paragraph under Fast feedback.
- `AGENTS.md` sections 5 to 7, and `CONTRIBUTING.md` sections 2 and 3.
- Linux cgroup v2: `memory.events` is hierarchical unless cgroup2 is mounted with `memory_localevents`, and `memory.events.local` is local.

## How to get into the same state

```sh
git fetch origin
git switch --detach 7997eeb348c3af302079c7273d1b3092eee4dc6c
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --require-hashes --no-deps -r ci/requirements-evidence.txt
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

Use CPython 3.12.3, with the sv2v v0.0.12 release that `rtl-fast.yml` pins and Yosys 0.66, set as `SV2V` and `YOSYS`.

## How to validate

Rounds 2 and 3 each ran every `run` step of the `docs` workflow's gate jobs (`docs-gates-0`, `docs-gates-1`, `docs-gates-2`, and `docs-check-no-git` in a tree without `.git`) on the committed head, one log and exit status per step. The steps that change the hosted runner (pip, apt and sv2v installs) were replaced by the same pinned packages and the pinned sv2v binary already present. The RV32 SDK installer ran against a new scratch destination, as its docstring requires for local runs. The `docs-check` aggregate verifies the hosted jobs' uploaded receipts, so it runs only hosted. The commands with the most bearing on this change:

```sh
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_gate_workflows_selftest.py
python3 scripts/act_ci.py --selftest
install_dir="$(mktemp -d)"
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
sha256sum scripts/act_ci.py
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 -p OOMPolicy=continue \
  python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
```

Expected result / pass criteria:

- Every command, and every `docs` workflow step, exits 0.
- `check_baremetal_only.py --check` prints `baremetal-only: OK (0 findings across 1344 tracked first-party file(s))`, and `--selftest` prints `PASS (829 arm(s))`.
- `ci_gate_workflows_selftest.py` prints 16 `Census budget:` cases, including `act job container: 4 worker(s)`, `a lower ancestor limit: 2 worker(s)`, `a mode-000 limit: refused: unreadable memory limit in <cgroups>` and `a mode-000 ancestor cgroup: refused: unsearchable cgroup <cgroups>/a: its memory limit cannot be proved absent`. `<cgroups>` stands for the planted cgroup root. As root, the three mode-000 cases print `LOUD SKIP` instead.
- The runner self-test prints `selftest: PASS`.
- `ci_events.py --selftest` prints `PASS (2187 contract items, 5218 arms)`.
- The digest is `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8`.
- The capped census reports 0 of 120 arms failed and 0 of 31 rules unproved.

## Known limitations / out of scope

- The four-job act replay at this head, the item 2 receipt, is run by the coordinating role and reported on #744 before review. This PR therefore uses `Relates to`.
- Slot 0 has no slice, so an OOM there is still not counted (documented). Only isolated slots enforce and read an aggregate cap.
- The bound reads cgroup v2. On a v1 host only `MemTotal` would be read.
- `CENSUS_WORKER_BYTES` is a measurement of today's datapath. A datapath that grows sv2v's peak needs a new measurement.
- On an OOM, `ci-manifest.json` is still written, and its completeness does not read the slot's memory events. `slot-memory.json` and the rc 2 refusal carry the invalidity.
- No product test, census check or RTL changes.
- The mode-000 census-budget controls cannot deny root, so in a root job container they print a loud skip. The directory-as-limit controls still refuse there.
- The bare-metal declarations are bound to each line's exact text. Changing a declared line, including regenerating the workflow at another indentation, fails the gate until the table is updated.

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
