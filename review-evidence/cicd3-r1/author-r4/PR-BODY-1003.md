[A839]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Review findings answered](#review-findings-answered)** — Each open finding of rounds R923-1 and R924-1, and where it is answered.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

`cicd-3`, six commits stacked on PR #1001 (`cicd-verilator-perf`, head `fcbc31f3`); head
`45d5c35a4470057966a72c0e85e49af1921152a0`. Rebase onto `dev` once #1001 merges; the diff against `fcbc31f3` is
these six commits only.

- Every local gate this PR touches passes at the head in a clean clone, 36 of 36 (list in How to validate).
- Hosted run 45481508309 at the head is green (`verilator-suites`, `yosys-portability`).
  - Its piece receipts (24/24) and suite verdict sets (83/83) are identical to the base PR head's run.
  - 18 of the 19 Verilator workers ran in 12.7 to 27.4 minutes.
  - Shard 17/19 ran 30.7 minutes, on a runner whose identical model builds took 1.41 times as long as the base
    run's. This is the open decision below.
- The full serial sweep was not run in this lane; the candidate bank runs it.

## Linked Issue / roles

Relates to #998 (the CICD improvement lane). Stacked on #1001.

Executor: `[A839]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Six commits; each was measured, and each kept every verdict identical.

1. **`66b092e1` Preflight once per head.**
   - A `verilator-preflight` job runs the sweep's eight preflight self-tests once, through
     `scripts/run_all_suites.sh --preflight-only`, beside the 19 workers.
   - The workers run `--ci-pieces --no-preflight`. `--no-preflight` is refused without `--ci-pieces`, so the
     serial sweep, the physical leg and local runs keep their preflight.
   - `verilator-suites` needs the job, verifies its `suite-preflight` SHA record with `ci_events.py
     --require-target-sha --expect 1`, and is red unless the job's result is `success`.
   - Shard 9/19 replica: the first suite starts at +2 s instead of +535 s, with 134 CPU-s less. Logs and receipts
     are IDENTICAL.
2. **`f6c11a25` Stable mutant staging.**
   - Every mutation driver (38) stages its planted RTL through `scripts/mutant_stage.py` at a path that is the same
     in every run, so a warm ccache answers the mutant model compiles. Verilator writes each source's path into
     the model's C++.
   - Warm hits: crf_rx 79/115 → 115/115 (−25 % CPU), avtp_rxmon depkt 37/48 → 48/48 (−64 %).
   - Every mutant is still killed by the same named check.
3. **`13e6d869` Longest case first.**
   - `scripts/ci_make_cases.py` starts a piece's cases longest first by a measured cost table (`CASE_SECONDS`),
     and prints and records them in driver order.
   - milan_dp__0 through its driver: 3411.9 s → 2711.8 s wall (−20.5 %), same instructions.
   - Same host, same booking, base against this commit:
     - milan_dp__1 1115 → 962 s (−13.7 %);
     - capture_coherence__3 421 → 398 s.
   - Receipts are IDENTICAL.
4. **`d95e95e8` One lock domain for every staging slot, and a proved stage root.** It answers R924-1-F1 and
   R923-1-F1.
   - **The lock is the slot.** A holder keeps an exclusive `flock` on the slot directory's own inode, and
     re-checks after locking that the path still names that inode. So every caller that names one physical
     directory meets one lock, however it got there:
     - any TMPDIR, resolved or not;
     - a symbolic link to the parent;
     - any user.
   - **Slots.** A slot owned by another user is never emptied or taken; the next slot is tried. A taken slot is
     emptied without following any link inside it.
   - **The root is proved before use.** It is created by one `mkdir(…, 0o700)` and then checked by `lstat`, not
     following a link. It must be:
     - a real directory, owned by the caller and writable by nobody else;
     - directly inside the resolved temporary directory;
     - not swapped between the check and its use.

     That temporary directory must itself be the caller's or root's, and sticky if others may write it.
   - **Refusal.** A root that fails any check is refused, with the reason on stderr. The driver then stages at a
     random private directory, as `tempfile` did: correct, and merely cold. An earlier 0755 root is tightened to
     0700. A stale `locks` file from the previous layout is ignored.
   - **Tests.** `--selftest` has 17 controls (0.7 s), six of them with independent holder processes that hold at
     once:
     - six drivers race for one slot;
     - two in-tree drivers under different TMPDIRs;
     - a TMPDIR and a link to it, and a parent and a link to it;
     - another user's live slot;
     - a symbolic-link, writable, non-directory and foreign-owned root;
     - a non-sticky world-writable TMPDIR.
   - **The controls can fail.** Ten planted defects each fail `--selftest`, the round-3 lock domain among them.
   - **The reviewers' probes, on the previous and this head.** A probe with independent processes, the
     "foreign" holder a real other uid, reproduces both reviewers' collisions on the previous head. It shows on
     this head:
     - every live slot kept;
     - the symbolic-link, writable, foreign-owned and non-sticky-base roots refused, each with its reason.
   - **The drivers.** Five drivers ran at the previous and at this head, through the shared cache, in-tree
     `split_mutants.py` among them. Every log is identical. The warm runs still hit 100 %:
     - tcam 16/16;
     - rx_filter 8/8;
     - depkt 48/48;
     - crf_rx 115/115;
     - split 858/858.
5. **`59f4f478` Re-key the dealer's figures from two complete hosted runs.** It answers R923-1-F2.
   - **Attribution of shard 1's 38.6 minutes.**
     - It was not this PR: on one host with equal bookings, the head ran shard 1's pieces faster than the base, at
       equal instructions (above).
     - It was the runner: in that job, the same suites' identical model builds took 1.36-1.40 times as long as at
       the base, against 1.41 for the job.
   - **What made shard 1 the heaviest worker even at the base (27.3 minutes).** A stale figure:
     - an inventory change had re-targeted `milan_dp`'s legs (#804);
     - leg 1 measured 995 s against its 508-second figure, and leg 3 396 against 1307;
     - so the dealer put leg 1 beside capture_coherence__3 and eight more suites.
   - **The refresh.** Per the documented "refresh them from the next complete hosted run", all 38 worker logs of
     runs 45383854694 and 45457006166 were measured with `suite_shards.py --measure`.
     - `milan_dp`'s four legs carry their measured windows.
     - Every other figure a window exceeded carries that window: nine suites and four legs.
     - No other figure is lowered, so #781's and #799's deliberate margins stay.
   - **The projection.** Every figure is now at or above every window those runs measured.
     - The dealer's worst projection is unchanged: 1615 s, on worker 0 (`follow_ring` alone), 185 s inside
       30 minutes.
     - On the largest windows actually measured, the worst regular worker takes 1549 s.
   - **Hosted at this head.** Shard 1 ran 16.1 minutes.
   - CI_WORKFLOWS.md's projection table and the #998 refresh paragraph are updated.
6. **`45d5c35a` Wording.**
   - The preflight, case start-order and preflight-job comments cite Issue #998 and REQ-VER-01 and REQ-VER-04
     (R924-1-R1; the staging helper's docstring got it in `d95e95e8`).
   - CI_WORKFLOWS.md says the fail-fast watcher cancels workers only on a push or a same-repository pull request
     (R923-1-R2).
   - TESTING.md names the two in-tree `milan_dp` drivers' path (R923-1-R1, in `d95e95e8`).

## Review findings answered

| Finding | Answer | Where |
|---|---|---|
| R924-1-F1 MAJOR: in-tree staging can erase a held slot across TMPDIRs | Fixed: one lock per physical slot directory; independent-process controls for in-tree, different TMPDIR, aliases, a foreign user, races and exhaustion | `d95e95e8` |
| R923-1-F1 MINOR: stage root trusted without proof; lock keyed by an unresolved path | Fixed: root proved (owner, mode, no link, inside the resolved base, atomic create) or refused with its reason; lock keyed by the resolved inode; planted controls for each | `d95e95e8` |
| R923-1-F2 MINOR: shard 1 38.6 minutes | Attributed (runner 1.36-1.41×; this PR faster on one host); stale `milan_dp` leg figures refreshed, shard 1 16.1 minutes at the head; shard 17's 30.7 minutes is the open decision below | `59f4f478` |
| R924-1-R1, R923-1-R1, R2 (wording) | Applied | `d95e95e8`, `45d5c35a` |
| R923-1-R3 (PR body wording) | Applied in this body | — |

**Open decision (Conformance, Issue #998 acceptance 2).** This head's hosted run placed three workers on slower
runners, measured by the same suites' identical builds:

| shard | runner build ratio | minutes |
|---|---:|---:|
| 0/19 | 1.23 | 15.2 |
| 7/19 | 1.31 | 25.3 |
| 17/19 | 1.41 | 30.7 |

Shard 2/19 runs `capture_coherence__0` alone and builds no Verilator model, so its 27.4 minutes has no index.

Dealing cannot give a 30-minute margin against a 1.41× runner:

- A regular worker would have to project at most about 1277 s with its allowance.
- Five indivisible pieces already exceed that: `follow_ring` 1493, `capture_coherence__0` 1436, `milan_dp_mclk__0`
  1408 and `milan_dp`'s legs 0 and 1 (1309, 1313).
- The total load needs about 22 such workers.

So the remaining choice is the owner's:

- split those pieces further and add workers, which costs more runner-minutes;
- or accept the bound as "within 30 minutes on a runner of the base run's speed".

The watcher job "Fail fast across this head" lasts the run's span (58.5 minutes here, 109.1 at the base); it is a
watcher, not work.

## Authoritative references

- [CI_WORKFLOWS.md "Exhaustive validation"](../docs/testing/CI_WORKFLOWS.md#exhaustive-validation) and "Failure and cancellation semantics": the preflight job, its binding, the dealer's figures and the projection table.
- [TESTING.md section 1](../docs/testing/TESTING.md#1-verilator-rtl-harnesses---tbverilator-the-live-regression): the two sweep modes, mutant staging (root proof, lock domain, in-tree drivers), case start order.
- REQUIREMENTS.md REQ-VER-01, REQ-VER-04; Issue #998 acceptance 1 (identical outputs) and 2 (30-minute hosted jobs).

## How to get into the same state

```sh
git fetch origin cicd-3
git worktree add ../cicd-3-review origin/cicd-3
cd ../cicd-3-review
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
export VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS='-j1 --no-print-directory'
```

## How to validate

```sh
python3 scripts/mutant_stage.py --selftest          # 17 controls, six with independent processes
python3 scripts/suite_shards.py --selftest && python3 scripts/ci_suite_pieces_selftest.py   # dealer bounds, 1620/2160 s
python3 scripts/ci_gate_workflows.py --check && python3 scripts/ci_events.py --check
python3 scripts/test_suite_cancellation.py
( cd tb/verilator/gptp_shadow && python3 test_mutant_lifecycle.py )
python3 scripts/check_py_idiom.py && python3 scripts/ci_events.py --selftest
```

Every command exits 0 at `45d5c35a`. Also green there, in a clean clone:

- the `ci_gate_workflows`, `ci_case_receipts`, `ci_make_cases`, `ci_maap_cases`, `ci_capture_cases`,
  `ci_suite_collect`, `ci_fail_fast`, `ci_runtime_evidence`, `ci_install_cache`, `ci_workflow_plan` and
  `ci_manifest` self-tests;
- `generate_ci_evidence_pins --check`;
- the sh idiom, hygiene, naming, fail-fast, test-evidence and TODO ratchets;
- doc paths, doc style, `docs_check`, archive, docs inventory, TOC and em-dash.

The lock domain, by hand: hold a slot under one TMPDIR, then take it from an independent process under another.

```sh
mkdir -p /tmp/p /tmp/t1 /tmp/t2
TMPDIR=/tmp/t1 python3 -c 'import sys; sys.path.insert(0,"scripts"); import mutant_stage as m, time
with m.directory("split-", "/tmp/p") as d: open(d+"/mine","w").close(); time.sleep(5); print(d, sorted(__import__("os").listdir(d)))' &
sleep 1; TMPDIR=/tmp/t2 python3 -c 'import sys; sys.path.insert(0,"scripts"); import mutant_stage as m
with m.directory("split-", "/tmp/p") as d: print(d)'
wait     # second prints /tmp/p/split-1; first prints /tmp/p/split-0 ['mine']
```

The hosted figures: read each job's minutes from the Actions jobs API (`completed_at − started_at`) for run
45481508309. Compare each piece's receipt with run 45457006166 per case (outcome, return code,
`output_sha256`): all 24 are identical.

## Known limitations / out of scope

- Shard 17/19's 30.7 minutes on a 1.41× runner: the open decision above.
- `WORKER_OVERHEAD_SECONDS` stays 122 s, though the head's hosted workers measured 14-81 s outside their suites
  without the preflight. Lowering it is a separate measured change.
- A harness compiled from the stage by its absolute checkout path still misses once per new checkout (crf_rx 15
  of 115, all harness compiles). Hosted checkouts are at a fixed path, so they do not.
- A root that fails its proof stages cold. A held slot of another user makes this user's run take the next slot.
- Not run here: the act replay and the full serial sweep.
- The CI tool inventory (red at the base) does not record the changed scripts.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 2: see the open decision)
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
