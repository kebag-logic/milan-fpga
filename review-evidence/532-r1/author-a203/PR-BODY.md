[A203] Run trusted act replays side by side: one runner-owned Docker daemon per replay slot

Closes #532

## Status

Ready for review. This PR changes the host-side runner, so the runner-change bootstrap rule governs it. The trusted `dev` copy validates this PR's own workflows. The live proof of the new slot code runs only after an independent audit, with an installed copy (see "How to validate").

## Description

`scripts/act_ci.py` gains `--slot N` (0-63). The design is the one recorded in the DECISION comment on #532.

- **Slot 0 is the default and is today's replay.** It uses the default local daemon. Its act command, controlled environment and sudo prefixes are unchanged.
- **Slots 1-63 each start their own Docker daemon under `--sudo`, for one invocation.** The runner owns the daemon, and the slot also gets:
  - a host-wide flock;
  - its own network namespace, with a userspace `pasta` uplink that forwards no port and does not map the gateway to host loopback;
  - its own nft table, which rejects the slot's traffic to every host-local address;
  - its own slice, capped at 24G with no swap;
  - a `dockerd` that runs its own containerd, with its own data-root, exec-root, socket, containerd namespaces, address pool and labels.
- **How the slot is reached.** The Docker CLI and act get the slot socket only as an assignment the runner makes, and run under `nsenter` into the slot namespace. The artifact and cache servers therefore bind inside the slot.
- **What stays per slot.** act's global names (`act-toolcache`, job volumes, job containers) become per-daemon. Every existing ownership, lease, cleanup and refusal therefore applies per slot, unchanged.
- **CPUs.** Job containers of slot N get CPUs `4N`-`4N+3`. Everything else about the jobs is unchanged, and no workflow file changes.
- **Teardown** runs on every exit, including signals and rollback. Each step is independent and every resource is proved absent; an absence the runner cannot prove means exit 2, with recovery commands. A dead invocation's residue refuses its own slot and is never adopted.
- **Inherited Docker endpoints are refused.** An invoking environment carrying `DOCKER_HOST`, `DOCKER_CONTEXT` or `DOCKER_CONFIG` is now refused in every Docker mode, slot 0 included. Before, those variables were silently dropped. This is a stricter refusal, not a weaker one.
- **`--boundary-selftest` stays on slot 0.** It is refused with `--slot` >= 1.
- **Live proof script.** `scripts/act_slot_proof.sh` is the live proof: the interrupt self-test in a slot, serial references, two concurrent slots whose verdicts must equal the serial ones, and the collision control.
- **Docs.** `docs/testing/CI_WORKFLOWS.md` has a new section, "Parallel replay slots", covering the design, bounds, costs, teardown, recovery and the live proof.

Cost: about 75 GB of disk per isolated slot (the runner image unpacked in the slot's own containerd), plus one pull per slot for each image update.

A note for review: the default Myers diff shows `act_ci.py` as +3985/-1969. `git diff --diff-algorithm=histogram` shows the real change, +2090/-105.

## How to reproduce

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <this PR> --sudo --slot 1   # after audit/install, see below
```

## How to validate

- Offline gate, run where the rule allows (in a disposable job container): `python3 scripts/act_ci.py --selftest`. It passes with 363 arms: all 277 existing ones plus 86 new. The same result holds as root and as a non-root user.
- 38 of 38 source mutations of the slot code were killed by the self-test.
- `check_py_idiom.py`, `check_sh_idiom.py`, the naming, fail-fast, test-evidence and hygiene ratchets, `docs_check.py`, `check_em_dash.py --base ede8d48e`, `gen_toc.py --check`, `check_doc_paths.py`, `check_doc_style.py`, `ci_events.py --check`, `check_feature_status.py` and `git diff --check` are all green.
- Live, which is the independent reviewer's or the manager's step under the bootstrap rule:

```sh
install -m 0555 <candidate>/scripts/act_ci.py <audited-install>/act_ci.py
sha256sum <audited-install>/act_ci.py
sudo install -d -m 0755 -o root -g root <slot-root>
<candidate>/scripts/act_slot_proof.sh --runner <audited-install>/act_ci.py \
  --sha256 <digest> --act-bin <act-0.2.89> --logs <new-dir> \
  --pr-a <A> --worktree-a <clean checkout at A's head> \
  --pr-b <B> --worktree-b <clean checkout at B's head> \
  --slot-a 1 --slot-root-a <slot-root> --slot-b 2 --slot-root-b <slot-root-2> \
  [--workflow <name>]... [--collide-default]
```

## DoD

- [x] Slot selection only by `--slot`; inherited endpoint refused; slot 0 unchanged (offline arms)
- [x] Per-slot daemon, namespace, firewall, slice, lock, teardown and absence proofs (offline arms and mutations; the exact argv was rehearsed by hand on a scratch daemon)
- [x] Per-slot CPU and memory bounds, documented defaults
- [x] `docs/testing/CI_WORKFLOWS.md` updated
- [ ] Live proof with the audited install: `scripts/act_slot_proof.sh`, covering two concurrent slots with verdicts equal to their serial runs, plus the collision control
