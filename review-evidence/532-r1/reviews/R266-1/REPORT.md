[R266] NEGATIVE - exact head a37af3c6ad54aa16403861c969f68cf2a83679c6

Round R266-1, internal cleared-context review of issue #532 / PR #533.
Exact head `a37af3c6ad54aa16403861c969f68cf2a83679c6`, tree `9c3c735352d6cf986a4dd311538c605ab346c7b9`.
Lane change against live dev `759da623072358afdb0e9d570a7b4b6a788492c9`: `scripts/act_ci.py`, `scripts/act_slot_proof.sh`, `scripts/check_baremetal_only.py`, `docs/testing/CI_WORKFLOWS.md` (also read as `ede8d48e..a37af3c6`, which adds dev's #521/#526 merges).

Verdict: NEGATIVE. Three MAJOR and three MINOR findings are open. All five lenses are UNCLEAN at this head.

## 1. What was reconstructed

- Contract: AGENTS.md sections 3 to 8, CONTRIBUTING.md 2.1 and 2.2, docs/README.md.
- Task: the #532 issue body (frozen acceptance 1 to 6) and its comments. These are the assignment, the author TAKEN, the author DECISION (issuecomment-5796770637), two REVIEW READY posts, and the manager's correction assignment.
- PR #533: the body, the manager's SOURCE VALIDATION r1 comment, and the review-start comment. No review verdicts or findings had been posted on the PR, so no prior finding needed to be resolved or retained.
- Authority: `docs/testing/CI_WORKFLOWS.md` "Act-first local replication", including the runner-change bootstrap rule, and the new "Parallel replay slots" section.
- Diff and history: the lane's five non-merge commits (`5081d069`, `45e5719d`, `fcce541b`, `3874c454`, `a37af3c6`) and the dev merge `aad4a256`. I read the complete lane diff: the `act_ci.py` histogram diff, the gate diff, the whole proof script and the doc diff.
- Public evidence: the tree `da096e8e.../review-evidence/532-r1`, fetched through the API. Every blob was verified against its Git blob ID. I also read the exact-head hosted check runs and the hosted docs-check job log.

I did not execute the candidate runner host-side, and I used no Docker, act, privilege or hardware.

## 2. Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs
**Where:**
- `scripts/act_ci.py:4049-4065` (`slot_firewall_rules`; the rule body is at 4064) and `scripts/act_ci.py:3959-3991` (`slot_uplink_command`).
- `docs/testing/CI_WORKFLOWS.md:1744-1749`, `1782-1786` and `1855-1856`.

**Title:** An isolated slot reaches every destination the host routes, including the default daemon's containers, and host-local published ports pass the "local" test.

**Authority and evidence:**
- The #532 objective asks for each replay "in its own isolation slot", with every existing guarantee preserved per slot. Acceptance 2 says a slot "cannot block or corrupt another slot".
- The doc says the slot's rule "rejects traffic from the slot's cgroup to every host-local address". It also says "Nothing about a slot touches another slot or the default daemon".
- The slot's only host-side socket owner is pasta, running in the host network namespace. Every outbound connection from the slot therefore becomes a host-originated connection.
- The only rule the runner adds is `socket cgroupv2 level 1 "<slice>" fib daddr type local counter reject`, at filter priority on the output hook.
- The author's own public receipt of this host's ruleset (`author-a203/receipts/host-nft-before.txt`, blob `20049a93`) shows three relevant facts:
  - Docker isolates its bridge networks only on the FORWARD hook, with `iifname != <bridge> oifname <bridge> drop` per bridge. There is no filter OUTPUT chain.
  - A live slot-0 job container existed at capture time.
  - The nat OUTPUT chain jumps to Docker's DNAT chain for local destinations, at `dstnat` priority, which runs before the slot's filter-priority rule.
- `receipts/pasta-reach-sim.log` reproduces this in a disposable unprivileged namespace. It uses the runner's exact pasta options and the rule body (without the cgroup selector, since pasta is the only client socket owner there). A host-local bridge gateway is BLOCKED. A container address behind a host bridge is REACHED. A host-local address whose port is DNAT-published is REACHED.

**Impact:**
- Candidate code in slot N can open connections to any container on the default daemon. That includes the job containers of a concurrent slot-0 replay of another PR, since "slot 0 plus one capped slot" is a documented configuration, and any operator container.
- Slot 0's own job network cannot reach those containers, because Docker's FORWARD isolation drops that traffic. So the isolated slot is weaker than slot 0 on this axis.
- A hostile PR can reach and influence a concurrent replay's services. Verdict independence (acceptance 1) then no longer holds by construction.
- The doc's "every host-local address" claim is false for published ports.
- The rehearsal and the live proof test only host-local and loopback reachability, so nothing would detect this.

**Required outcome:** Traffic from a slot must not reach destinations the host routes onto its own bridges or namespaces, at least the default daemon's networks and any DNAT-published local port. A live or rehearsal control must show a routed container address and a published local port refused while DNS and the internet still work. The alternative is a recorded maintainer decision that accepts this exposure, with the doc stating it exactly.

**Verification:** Re-run `probes/pasta_reach_sim.sh` against the revised rule set, expecting both REACHED lines to become BLOCKED. Then run a live check against a real default-daemon container IP and a published port, from a slot job.

### F2 - MAJOR - Tests, Docs
**Where:**
- The absence proofs and fail-closed query branches in `scripts/act_ci.py`: 4099-4102 (`nft_table_present`), 4250-4251 (`await_slot_state`), 4295 (slice cgroup absence), 4299-4300 (DropInPaths query failure), 4350 (runtime-directory absence) and 4355 (uplink PID-file absence).
- The controls in `scripts/act_ci.py:11529-11583` (`selftest_slot_teardown_failures`), whose survivors are only daemon, netns, table and dropins.
- The claim in `docs/testing/CI_WORKFLOWS.md:1901-1902`.

**Title:** Half of the per-slot absence proofs, and every "unanswerable query" branch, can be deleted or inverted with the offline self-test still passing.

**Authority and evidence:**
- Acceptance 5 requires offline self-tests for per-slot cleanup. The DECISION and doc say any absence the runner cannot prove turns the run into exit 2. The doc says the offline self-test pins "each kind of survivor".
- AGENTS section 6 (Tests) asks that each test can fail for the defect it claims to detect.
- `receipts/slot-mutants-a37af3c6.log` records six mutants that SURVIVED, each run only inside a network-less container:
  - `runtime-dir-absence-dropped`, `uplink-pidfile-absence-dropped` and `slice-cgroup-absence-dropped`. The last is the proof that no process is left in the slot.
  - `unit-state-query-failure-reads-absent`: a `systemctl show` that cannot answer is treated as proof that the unit is gone.
  - `dropin-query-failure-ignored`.
  - `nft-query-error-reads-absent`: any `nft list` error reads as "table absent". This affects both residue detection and the teardown proof.

**Impact:** A refactor can turn these root-resource absence proofs fail-open, and nothing in the gate reports it. The doc overstates what the self-test pins.

**Required outcome:** Each absence proof and each query-failure branch has a control that fails when it is removed or inverted. That means a survivor for the runtime directory, the uplink PID file and the slice cgroup, and an unanswerable `systemctl show`, DropInPaths query and `nft list` during both residue and teardown. Alternatively, the doc must state exactly what is pinned.

**Verification:** Re-run `probes/slot_mutants.py` on the corrected head. Those six mutants must be KILLED.

### F3 - MAJOR - Tests, Conformance
**Where:**
- `scripts/act_slot_proof.sh:94-120` (`replay`, `same_verdict`, `compare`), `139-158` (`collide`) and `177-180`.
- The doc description in `docs/testing/CI_WORKFLOWS.md:1866-1886`.

**Title:** The acceptance-1 proof can print `PROVED` with no workflow executed, and without the control that shows the collision without isolation.

**Authority and evidence:**
- Acceptance 1 asks for two concurrent replays "with verdicts identical to their serial runs", and "a controlled collision control that fails without the isolation".
- A verdict file is `exit N` plus any per-workflow PASS or FAILED lines. Two refusals (`exit 2` and no workflow line) therefore compare equal.
- `receipts/proof-vacuity.log` runs the candidate proof script inside a network-less container as uid 1000. The fake runner (`probes/fake_runner_refuse_after_slot.py`) makes every PR run take its slot and then refuse, the way an action-clone or image-pull failure would. The script prints `PROVED every slot proof held` and exits 0, while all six runs refused.
- The no-isolation control, the slot-0 collision, runs only with the optional `--collide-default`. The default `PROVED` path omits it.
- The author's dry run (`proof-script-dryrun/fake_runner.py`) never refuses after taking a slot, so it could not see this.

**Impact:** The manager's acceptance-1 evidence can be vacuous: for example, during a transient GitHub or registry outage the proof reports PROVED. It can also be recorded without the control that acceptance 1 names.

**Required outcome:** `PROVED` requires that each serial reference actually executed its workflows (exit 0 or 1 with at least one per-workflow verdict line), and that the no-isolation collision control ran and refused. Otherwise the doc and PR state that acceptance 1 needs `--collide-default`, and the script refuses to print PROVED without it.

**Verification:** Re-run `probes/proof_vacuity.sh`, expecting a FAIL. Keep the author's three fake-runner cases, which must still behave as recorded.

### F4 - MINOR - Docs
**Where:** `docs/testing/CI_WORKFLOWS.md:1793-1798` and `1733-1734`.

**Title:** The slot resource and lock descriptions are inaccurate.

**Evidence:**
- The doc says the unchanged per-container flags mean "each slot therefore replays exactly the hosted-shaped jobs described above; only its CPUs differ". The next bullet adds a 24G aggregate slice cap with no swap.
- `rtl.yml`'s four matrix legs at 16 GB each may use 64 GB in slot 0, and hosted runs get four separate 16 GB runners. Memory therefore differs too. The author's REVIEW READY lists the cap as unmeasured on `rtl-full`.
- The lock is described as "held for the whole invocation". In fact it is taken in `replay_slot` (`scripts/act_ci.py:5152`), after the PR query, the fetch and the materialization (`scripts/act_ci.py:5134`).

**Impact:** Readers may assume a slot's verdict cannot diverge from slot 0 because of memory, and may misjudge when a busy slot is detected.

**Required outcome:** The doc states the cap's effect on multi-leg jobs, and when the lock is taken.

**Verification:** Doc re-read against `SLOT_MEMORY_MAX` and `run_validation`.

### F5 - MINOR - Tests
**Where:**
- `scripts/act_ci.py:4168` (slot-root validation in acquisition), `4429` (CPU range bound), `4406` (signal-blocked slot teardown), `4117` (slice residue state), `3804` (dangling-symlink residue) and `12737` (live interrupt self-test entering the slot).

**Title:** Further slot behaviours have no failing control.

**Evidence:** In `receipts/slot-mutants-a37af3c6.log`, all of these SURVIVED:
- `slot-root-validation-unwired`: acquisition never validates the root, but the fake host always answers "good".
- `cpu-range-boundary`: `>=` becomes `>`, so a host with exactly `4N+3` CPUs would accept a nonexistent CPU.
- `slot-teardown-signals-unblocked`: a repeated signal can interrupt the slot teardown.
- `slice-residue-only-active`: an activating, deactivating or failed slice is not treated as residue.
- `path-present-ignores-dangling-symlink`.
- `interrupt-selftest-outside-slot`: live-only, and it fails closed.

**Impact:** These properties can regress silently. The doc's "the slot root" is pinned only as a function, not as a step of acquisition.

**Required outcome:** A control for each property, or a doc statement of which ones are live-only.

**Verification:** The same mutants are KILLED.

### F6 - MINOR - Conformance, Robustness
**Where:** `scripts/act_ci.py:3807-3837` (`validate_slot_root`) and the DECISION comment on #532 (issuecomment-5796770637).

**Title:** The slot-root check is narrower than the recorded design.

**Evidence:**
- The DECISION requires `--slot-root` to be "a root-owned directory that is not writable by group or other and has no symlink in its path".
- The code `lstat`s only the final component. It accepts any parent that is a symlink or owned by a non-root user, and this narrowing is recorded nowhere. On this host, a filesystem the DECISION names for a second slot has a parent that is not owned by root.
- The arms in `selftest_slot_root` (11585 onward) include no parent-path case.

**Impact:** A root dockerd's data-root can be redirected by whoever controls a parent directory, between validation and daemon start. The published design and the code disagree silently (AGENTS section 2: publish conflicts).

**Required outcome:** Either enforce the recorded rule (no symlink in any component, and parents not writable by group or other or by non-root users), or record a decision that narrows it and update the doc.

**Verification:** Arms for a symlinked parent and a user-owned parent.

### Suggestions (optional; they do not affect coverage)
- **S1:** the lock at `scripts/act_ci.py:3895-3902`.
  - `sudo touch` follows a symlink before the `O_NOFOLLOW` open.
  - The file is world-readable, so any local user can hold its `flock` indefinitely.
  - On this host `/run/lock` is root-only 0755 and `protected_symlinks=1`, so neither is exploitable here. On hosts where `/run/lock` is 1777 it is a local denial-of-service and a symlink hazard.
  - A root-only lock directory would close both.
- **S2:** the slot slice bounds memory but not CPU. dockerd, containerd, image unpacking and the seed container can use any CPU, and act itself runs outside the slice. `AllowedCPUs` on the slice would make "cannot starve each other" hold for the whole slot.
- **S3:** no disk bound. Two slots and the default daemon can share one filesystem, at about 75 GB per slot. Consider documenting the allocator's disk duty next to its RAM duty.
- **S4:** `selftest_slot_lifecycle` compares the recorded `systemctl show` argv to itself (`scripts/act_ci.py`, the `show-` entries in the pinned-command check). Pin them literally.
- **S5:** the proof does not show that the two parallel runs overlapped. Both slot markers could be required before either verdict line.

## 3. What held (examined and correct at this head)

**Slot 0:**
- Every one of dev's 277 self-test arm labels still passes at head (`receipts/selftest-dev-759da623-root.log` against `receipts/selftest-head-a37af3c6-root.log`).
- The container-options word, the controlled environment and the sudo prefixes are pinned unchanged.
- `replay_slot(ReplaySlot(0))` runs no host command and takes no lock.
- The only change a slot-0 user can see is the stricter inherited-endpoint refusal, which the issue body itself describes as the runner's behaviour.

**Inherited `DOCKER_HOST`, `DOCKER_CONTEXT` and `DOCKER_CONFIG`:**
- These are refused in the PR run, the dry run and both live self-tests before any collaborator runs. Mutants that drop either call site are KILLED.
- The boundary self-test's leaky arm plants no `DOCKER_*` variable, so it is unaffected.

**Endpoint parser and prefixes:**
- The parser rejects every endpoint that is not a slot socket, and slot 64.
- The Docker and act prefixes enter the slot namespace identically.
- A boundary cannot be created through another slot's daemon.

**Acquisition and teardown:**
- Acquisition order, lease-before-create, rollback of exactly the attempted resources, residue refusal without adoption, and a busy lock that tears nothing down all hold.
- The daemon identity check (labels and data-root) holds, as does the pinned argv for pasta, dockerd, nft and every mutating systemctl call.
- An `--interrupt-selftest` in a slot holds at most one slot network at a time, matching the single-/24 pool.
- With `--trusted-install-sha256`, `validate_runner` checks only the install file, so the proof can replay other PRs.

**Scope gate:** the masks are anchored to exact lines, bound to one file, and applied per line after the triplet scrub (`scripts/check_baremetal_only.py:586-611`). The hosted docs-check shows 0 findings and 441 arms.

**Offline self-test (bootstrap rule):**
- Run only in disposable network-less rootless containers.
- PASS with 363 checks, 0 FAIL, as root and as uid 1000.
- sudo, gh and docker were recording stubs that were never invoked (`receipts/selftest-head-*.log`).
- The hosted docs-check step also shows 363 ok and 0 FAIL (`receipts/hosted-docs-check-excerpt.txt`).

**Workflow semantics:** no workflow file changes in the lane (acceptance 6).

**Clone integrity after probes (`receipts/clone-integrity-a37af3c6.txt`):**
- 873 tracked entries match their blobs and modes.
- The index and worktree equal HEAD, and no hidden-index flags are set.
- The gitlinks `third_party/verilog-axis` 48ff7a7e, `protocol-processor` 424c688f and `gptp-processor` c1b61743 are checked out at their pins. `external` is uninitialised, as intended.

## 4. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3, F6) | #532 acceptance 1-6 and the DECISION, set against `scripts/act_ci.py` 3802-4435, 5122-5160, 12715-12790 and 13506-13646, `scripts/act_slot_proof.sh`, and the doc's slot section | R266-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| RTL | UNCLEAN (F1) | Trust boundary and privilege map (what runs as root: touch, ip, nft, systemctl, systemd-run, pasta, dockerd, nsenter-wrapped docker and act); nesting of run dir, slot and Docker boundary; signal and lease paths; cgroup, namespace and nft design; `receipts/pasta-reach-sim.log`; author receipt `host-nft-before.txt` | R266-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| Robustness | UNCLEAN (F1, F6) | Slot range and bool input, missing tools, busy lock, residue kinds, SIGKILL recovery, interrupted start, teardown failures, slot-root input, host resolver and lock-directory configuration | R266-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| Tests | UNCLEAN (F1, F2, F3, F5) | The 86 new arms at `scripts/act_ci.py:10679-11776`; container self-test receipts; 22 mutants (`receipts/slot-mutants-a37af3c6.log`); proof-script vacuity (`receipts/proof-vacuity.log`); the author's mutation and dry-run receipts | R266-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| Docs | UNCLEAN (F1, F2, F4) | `docs/testing/CI_WORKFLOWS.md` 1311-1322, 1509-1513, 1544-1549, 1590-1593 and 1709-1904; the runner docstring; the PR body; the scope-gate docstring | R266-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |

## 5. Real limits of this round

**Not exercised live:**
- The live slot lifecycle was not run: systemd-run units, pasta in the host namespace, the dockerd start, the real `socket cgroupv2` match and real teardown absence.
- F1 is shown in an unprivileged namespace model. It omits the cgroup selector and models Docker's nat-output DNAT by hand.
- The host's Docker filter behaviour comes from the author's public ruleset receipt and was not re-measured.

**How the self-test was run:**
- The offline self-test ran in a local image (Python 3.14.6) with stub sudo, gh and docker. The author used Ubuntu 24.04. The hosted docs job also ran it.
- The 22 mutants are this reviewer's own set, not an exhaustive one.
- The proof-script probe used a fake runner, and the host's `cmp` bound read-only into the container.

**Not used:** no Verilator, Yosys, builder or parent/PP/gPTP bank was run by this reviewer, because no RTL is in scope.

**Not claimed:** the manager's source static/builder and native banks for this head, which are still running.

**Hosted state at observation (`receipts/hosted-checkruns-a37af3c6.txt`):**
- `docs-check`, `elaborate`, `rtl-fast`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`, four Yosys shards and four Verilator shards had succeeded.
- `Verilator shard 4/5` was in progress. The `verilator-suites` and `yosys-portability` contexts had not yet been emitted.
- The physical gPTP context was skipped (nightly and manual only), which is not hardware proof.
- Physical calibration was NOT RUN.

## 6. Pending manager duties

- **Acceptance 1:** run the live proof with an audited install, using `--collide-default`. Until F3 is fixed, check by hand that every serial reference executed its workflows. Include `rtl-full`, to measure the 24G slot cap (F4).
- **Source banks:** publish the source static/builder and native banks for this head.
- **Hosted contexts:** exact-head `verilator-suites` and `yosys-portability`.
- **Merge turn:** the candidate merge build against live dev.
- **Re-review:** a later head that answers F1 to F6 needs a new round covering every lens again.

## 7. Receipts (listed in MANIFEST.sha256)

**Probes:**
- `probes/pasta_reach_sim.sh`
- `probes/run_selftest_podman.sh`
- `probes/slot_mutants.py`
- `probes/proof_vacuity.sh`
- `probes/fake_runner_refuse_after_slot.py`

**Receipts:**
- `receipts/pasta-reach-sim.log`
- `receipts/selftest-head-a37af3c6-root.log`
- `receipts/selftest-head-a37af3c6-uid1000.log`
- `receipts/selftest-dev-759da623-root.log`
- `receipts/slot-mutants-a37af3c6.log`
- `receipts/proof-vacuity.log`
- `receipts/hosted-checkruns-a37af3c6.txt`
- `receipts/hosted-docs-check-excerpt.txt`
- `receipts/clone-integrity-a37af3c6.txt`

R266-1 FINISHED
