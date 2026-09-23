[A213] Run trusted act replays side by side: one runner-owned Docker daemon per replay slot

Closes #532

## Status

Ready for review, correction round 1 (answers R266-1 and R267-1). This PR changes the host-side runner, so the runner-change bootstrap rule governs it: the trusted `dev` copy validates this PR's own workflows, and the live proof of the slot code runs only after an independent audit, with an installed copy (see "How to validate").

## Description

`scripts/act_ci.py` gains `--slot N` (0-63). The design is the DECISION on #532, as amended in the correction round's REVIEW READY on #532 (firewall, slot root, memory cap, lock wording, live proof).

- **Slot 0 is the default and is today's replay.** It uses the default local daemon. Its act command, controlled environment and sudo prefixes are unchanged.
- **Slots 1-63 each start their own Docker daemon under `--sudo`, for one invocation.** The runner owns the daemon, and the slot also gets:
  - a host-wide flock, taken once the PR head is materialized and held until the slot's teardown ends;
  - its own network namespace, with a `pasta` uplink that forwards no port and does not map the gateway to host loopback;
  - its own nft table with two output rules for the slot's cgroup: reject every host-local address, and reject anything the host would send out of an interface other than its unicast default-route uplinks (read with `ip -json -4|-6 route show default` before any slot resource exists). A slot therefore cannot reach the default daemon's containers or the ports Docker publishes on host addresses, which Docker's forward-path isolation would not stop for host-originated traffic;
  - its own slice, capped at 24G with no swap;
  - a `dockerd` that runs its own containerd, with its own data-root, exec-root, socket, containerd namespaces, address pool and labels.
- **Memory cap attribution.** After the workflows, the runner reads the slot slice's own `memory.events.local`. If the slot cap itself ran out, the run is refused (exit 2 naming the cap) rather than reported as the candidate's `FAILED`. The slice's peak is printed. The cap has not yet been measured on the shipping workflows; the live proof prints each slot's peak.
- **Slot root.** `--slot-root` and every directory above it must be a root-owned real directory, not writable by group or other.
- **How the slot is reached.** The Docker CLI and act get the slot socket only as an assignment the runner makes, and run under `nsenter` into the slot namespace. The artifact and cache servers therefore bind inside the slot.
- **What stays per slot.** act's global names (`act-toolcache`, job volumes, job containers) become per-daemon, so every existing ownership, lease, cleanup and refusal applies per slot, unchanged.
- **CPUs.** Job containers of slot N get CPUs `4N`-`4N+3`. No workflow file changes.
- **Teardown** runs on every exit, with cleanup signals blocked. Each step is independent and every resource is proved absent; an absence the runner cannot prove, or a query that cannot answer, means exit 2, with recovery commands. A dead invocation's residue (any unit state but absent) refuses its own slot and is never adopted.
- **Inherited Docker endpoints are refused.** An invoking environment carrying `DOCKER_HOST`, `DOCKER_CONTEXT` or `DOCKER_CONFIG` is refused in every Docker mode, slot 0 included.
- **`--boundary-selftest` stays on slot 0.**
- **Live proof script.** `scripts/act_slot_proof.sh` records ten checks and prints `PROVED` only when all ten pass: the interrupt gate in slot A (with the runner's own slot teardown line), two completed serial references, two overlapping parallel slots with the serial verdicts, the isolation control from inside each slot (a default-daemon container and its published port refused, a public host reachable, the same targets reached from the host), and both collision controls (same isolated slot, and slot 0). A run counts only if it completed its workflows. `--selftest` grades every check offline against stand-ins (14 cases).
- **Docs.** `docs/testing/CI_WORKFLOWS.md` "Parallel replay slots" covers the design, bounds, costs, teardown, recovery, the live proof and exactly what the offline self-tests pin.

Cost: about 75 GB of disk per isolated slot, plus one pull per slot for each image update.

For review: the default diff shows `act_ci.py` against `dev` as a large rewrite; `git diff --diff-algorithm=histogram` shows the real change.

## How to reproduce

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <this PR> --sudo --slot 1   # after audit/install, see below
```

## How to validate

- Offline, where the bootstrap rule allows (a disposable, network-less job or sandbox, never the host-side orchestrator): `python3 scripts/act_ci.py --selftest` passes with 422 checks (363 before this round: 4 reworded, 59 added), as root and as a non-root user.
- `bash scripts/act_slot_proof.sh --selftest` passes 14 cases (no Docker, privilege or network).
- 53 of 53 source mutants of the slot code are killed (the reviews' 21 and 18, plus 14 for this round's protections), as root and as non-root; 14 of 14 mutants of the proof's checks are killed. A no-op control mutant survives in each set.
- Gates green: `check_baremetal_only.py --check` (0 findings) and `--selftest` (441 arms, masks unchanged), `docs_check.py`, `check_em_dash.py --base 759da623`, `check_py_idiom.py`, `check_sh_idiom.py`, the naming, fail-fast, test-evidence and hygiene ratchets, `ci_events.py --check`, `check_feature_status.py`, `gen_toc.py --check`, `check_doc_paths.py`, `check_doc_style.py`, `git diff --check`.
- Live, the independent reviewer's or the manager's step under the bootstrap rule:

```sh
install -m 0555 <candidate>/scripts/act_ci.py <audited-install>/act_ci.py
sha256sum <audited-install>/act_ci.py
sudo install -d -m 0755 -o root -g root <slot-root>        # every ancestor root-owned
<candidate>/scripts/act_slot_proof.sh --selftest
<candidate>/scripts/act_slot_proof.sh --runner <audited-install>/act_ci.py \
  --sha256 <digest> --act-bin <act-0.2.89> --logs <new-dir> \
  --pr-a <A> --worktree-a <clean checkout at A's head> \
  --pr-b <B> --worktree-b <clean checkout at B's head> \
  --slot-a 1 --slot-root-a <slot-root> --slot-b 2 --slot-root-b <slot-root-2> \
  [--workflow <name>]...
```

## DoD

- [x] Slot selection only by `--slot`; inherited endpoint refused; slot 0 unchanged (offline arms)
- [x] Per-slot daemon, namespace, firewall (host-local and non-uplink destinations), slice, lock, teardown and absence proofs, each with a failing control (offline arms and mutants; unprivileged namespace rehearsal of the firewall)
- [x] Per-slot CPU and memory bounds, documented defaults; a slot-cap exhaustion is refused, not reported
- [x] `docs/testing/CI_WORKFLOWS.md` updated
- [ ] Live proof with the audited install: `scripts/act_slot_proof.sh` prints `PROVED` (interrupt gate in a slot, completed serial references, overlapping slots with equal verdicts, isolation control, both collision controls), including an `rtl-full` pair to measure the slot memory peak
