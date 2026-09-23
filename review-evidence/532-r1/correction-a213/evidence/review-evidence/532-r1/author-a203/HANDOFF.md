# [A203] HANDOFF: #532 parallel act replay slots

Lane: `$LANES/532-act-parallel-slots`, branch `532-act-parallel-slots`, based on live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
The branch is NOT pushed and has no PR yet: per the assignment, the manager pushes and opens the PR. The worktree is clean.

## Commits (one-line subjects, no trailers)

| SHA | Subject |
|---|---|
| `5081d06921da244a172f0a1e96de0772a3592815` | Run act replays in runner-owned per-slot Docker daemons selected by --slot, refusing inherited endpoints (#532) |
| `45e5719d9a5d169b4e606e8378fbbfa5b9ca6ac9` | Add the live proof script for concurrent act replay slots and their collision control (#532) |
| `fcce541b71975398629fe5a2570cf87b36b96cdb` | Document parallel act replay slots, their bounds, costs, cleanup and live proof (#532) |

- Head tree: `4c896d37e634dd2e80a7d11144f946278bc22bff`.
- `scripts/act_ci.py` sha256 `6723826c171ab1e028e21c6f9556700a2e4f152594cdfe9bf9fa41597c6e5a79`.
- `scripts/act_slot_proof.sh` sha256 `775c7f887dc6a88b5a509038c67def207b29fe9b122d3cc5fd2d48c5a64b62a7`.

## Public trail on #532

- [A203] TAKEN: https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5796576737
- [A203] DECISION: https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5796770637
- [A203] REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5797481044

## What changed

The design is the one in the DECISION comment, implemented without deviation except for two points found while implementing:

- Every slot host tool (`dockerd`, `ip`, `nft`, `nsenter`, `pasta`, `systemctl`, `systemd-run`, `touch`) is resolved before the lock or any mutation.
- The teardown's absence proofs, not the stop/delete commands' exit status, decide whether teardown succeeded.

Everything is in `PR-BODY.md` (the PR description; starts with `[A203]`, contains `Closes #532`).

## Validation (author side)

I did not run the candidate runner on the host at any point. Its offline `--selftest` ran only inside disposable, network-less containers on a scratch daemon. That boundary is the equivalent of the CI job the bootstrap rule allows. The helper is `run-selftest-in-container.sh`.

| Check | Result | Receipt |
|---|---|---|
| Base `--selftest` at `ede8d48e` | PASS, 277 arms | `receipts/selftest-base-ede8d48e.log` |
| Head `--selftest` at tree `4c896d37` (root) | PASS, 363 arms (277 existing plus 86 new), 0 FAIL | `receipts/selftest-final-fcce541b.log` |
| Same, as uid 1000 (hosted-like) | base 277 / head 363, 0 FAIL | `receipts/selftest-nonroot-{base,final}.log` |
| Mutation controls on the slot code | 38/38 KILLED, restored tree PASS | `mutation-run.py`, `receipts/mutation-run-final-fcce541b.log` |
| `check_py_idiom.py`, `check_sh_idiom.py`, `measure_naming --check`, `measure_fail_fast --check`, `measure_test_evidence --check`, `check_hygiene --check`, `check_todo_ownership`, `docs_check`, `check_doc_paths`, `check_doc_style`, `gen_toc --check`/`--verify-anchors`, `ci_events --check`, `check_feature_status`, `check_solution_docs`, `check_submodule_docs` | all rc 0 | this session |
| `check_em_dash.py --base ede8d48e` | 0 findings over 201 added lines | this session |
| `git diff --check` | clean | this session |
| Mechanism experiment (pasta uplink, managed containerd, act binding inside the namespace, nft reject) | proven by hand | `receipts/mechanism-experiment.md` |
| Rehearsal of the exact pinned host argv with scratch names | start, identity, CPUs 4-7, DNS and internet ok, host-local and loopback rejected, every resource absent after teardown in the runner's order | `rehearsal.sh`, `receipts/rehearsal-production-argv.log` (one rehearsal-script pipefail defect is noted at the end; the table was absent) |
| Proof script control flow against a fake runner | the happy path PROVES; a verdict broken only in a slot, a slot that never refuses, a wrong digest and a missing option all fail | `receipts/proof-script-dryrun/` |
| Scratch teardown | 0 units, namespaces, nft tables, routes, `/run` entries, cgroups, processes or mounts; scratch directory removed; the default daemon has nothing named a203 | `receipts/scratch-teardown-absence.txt` |

Host safety:
- I never touched the default daemon's containers, volumes, networks or `act-toolcache`. My only access to it was read-only: `docker info`, `ps`, `volume ls`, `network ls` and `system df`.
- I killed no act process. The manager's lock was never touched.
- Every scratch daemon used a data-root under the packet's `scratch/`, its own socket, and a pool of 10.203.0.0/24 or 10.232.0.0/24 inside its own network namespace. All of it has been removed, with proof.

## What the manager must run (bootstrap rule)

1. Push the branch and open the PR against `dev` from `PR-BODY.md`. Move #532 to In progress or In review on the board; I did not touch the board.
2. Run the trusted act replay of this PR with the `dev` runner, as for any runner-changing PR:
   `python3 -I <trusted-dev>/scripts/act_ci.py --pr <PR> [--sudo]`.
   Its docs job runs the candidate's offline `--selftest` inside the job, and that must report 363 arms and PASS.
3. After an independent reviewer audits the exact file, install it and record its digest:
   `install -m 0555 <lane>/scripts/act_ci.py <audited-install>/act_ci.py; sha256sum <audited-install>/act_ci.py`
   Then run `python3 -I <audited-install>/act_ci.py --selftest --worktree <lane>`.
4. Create each slot root once, on a filesystem with about 75 GB free per slot:
   `sudo install -d -m 0755 -o root -g root <slot-root>`
   On this host, `/` and `/data` each have room for one slot today. Use `--slot-root-a` and `--slot-root-b` to put the two slots on different filesystems, or use `--slot-b 0` to pair one isolated slot with the default daemon.
5. Run the live proof while the manager's serial queue is held. The proof uses slot 0 for its serial references, and for `--collide-default`:

   ```sh
   <lane>/scripts/act_slot_proof.sh --runner <audited-install>/act_ci.py \
     --sha256 <digest> --act-bin <absolute act 0.2.89> --logs <new dir> \
     --pr-a <A> --worktree-a <clean checkout at A's head> \
     --pr-b <B> --worktree-b <clean checkout at B's head> \
     --slot-a 1 --slot-root-a <root-1> --slot-b 2 --slot-root-b <root-2> \
     [--workflow <name>]... --collide-default
   ```

   Exit 0 and a final `PROVED` line in `<logs>/SUMMARY` meet acceptance 1. The same run's `interrupt-1.log` is the live per-slot cleanup evidence for acceptance 2.
6. Manager integration, which is outside this PR: the serial act lock becomes a slot allocator. It passes `--sudo --slot N --slot-root <root>` and never exports `DOCKER_HOST`, `DOCKER_CONTEXT` or `DOCKER_CONFIG` into the runner's environment, which is now refused.

## Acceptance status

1. Two concurrent replays with verdicts equal to their serial runs, plus a collision control: **not yet met**. This needs the audited install (steps 3-5). The script and its fake-runner controls are ready.
2. Per-slot guarantees: **met offline**. The offline arms cover lock, residue, rollback of each step, independent teardown steps, absence proofs and interrupted start; the lifecycle was rehearsed by hand and the mutations were killed. The live `--interrupt-selftest --slot 1` runs in step 5.
3. Per-slot CPU and memory bounds with documented defaults: **met**. CPUs `4N`-`4N+3` were observed live (4-7) and the slice cap is `SLOT_MEMORY_MAX = 24G` with no swap. Slot 0 keeps today's per-container bounds.
4. Slot 0 unchanged: **met**. Its act command, environment and prefixes are pinned by arms. The one deliberate difference is that an inherited `DOCKER_*` is now refused rather than dropped.
5. Offline self-tests and CI_WORKFLOWS.md: **met**.
6. No workflow semantics change and no weakened refusal: **met**. No workflow file changed, all 277 existing arms pass unchanged, and only refusals were added.

## Open risks and questions

- **The 24G per-slot memory cap is not yet measured on a full `rtl-full` replay inside a slot.** If the live proof shows an OOM kill in a slot, raise `SLOT_MEMORY_MAX`. The per-container 16g bound is unchanged.
- **A slot's first use pulls the roughly 19 GB runner image within the existing 30-minute seed budget.** Prime each slot with a `--dry-run` if that is tight.
- **A slot's DNS goes through the host's configured nameservers**, which must not be host-local addresses; the host-local reject rule would block them. On this host they are not host-local.
- **pasta runs as root (`--runas 0:0 --netns-only`)**, because it has to join a root-owned namespace. It forwards nothing inbound, and the slot's nft rule confines its reach.
- **A `SIGKILL`ed slot invocation leaves named resources.** The next run of that slot refuses and prints the recovery commands; volumes left inside the data-root need a data-root reset, which costs one pull.
- **The default Myers diff overstates the `act_ci.py` change** (+3985/-1969). Review with `--diff-algorithm=histogram` (+2090/-105).
