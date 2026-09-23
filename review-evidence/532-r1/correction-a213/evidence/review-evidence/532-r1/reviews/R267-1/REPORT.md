[R267] NEGATIVE - exact head a37af3c6ad54aa16403861c969f68cf2a83679c6

Round R267-1, external independent review of issue #532 / PR #533.
Exact head `a37af3c6ad54aa16403861c969f68cf2a83679c6`, tree `9c3c735352d6cf986a4dd311538c605ab346c7b9`.
The lane's net change against live `dev` `759da623` is four files: `scripts/act_ci.py`, `scripts/act_slot_proof.sh`, `docs/testing/CI_WORKFLOWS.md` and `scripts/check_baremetal_only.py`. The merge `aad4a256` has the same tree as a clean automatic merge of `fcce541b` and `759da623` (`7296ba5b`). All six lane commits are one line with no trailers.

Verdict: NEGATIVE. There are two open MAJOR findings (F1, F2) and three open MINOR findings (F3, F4, F5). All five lenses were applied, and every one carries at least one open finding at this head.

## How this round was run

- **Reconstruction order.** AGENTS.md, then CONTRIBUTING.md, then `docs/testing/CI_WORKFLOWS.md` (the "Act-first local replication" section and the new "Parallel replay slots" section). Then the issue #532 body with acceptance 1-6, the ASSIGNMENT, TAKEN, DECISION and both REVIEW READY comments, and the manager comments on the PR. Then the diff `ede8d48e..a37af3c6` with a histogram diff of the runner, the history and the merge, and finally the public evidence tree `da096e8e:review-evidence/532-r1`.
- **What was withheld.** No private author material and no other reviewer's report was read.
- **Bootstrap rule.** The candidate runner never ran host-side and was never pointed at Docker, act or sudo. Its offline `--selftest` and my probes that import it ran only inside a disposable, unprivileged, network-less namespace sandbox. The sandbox has its own user, net, pid, ipc, uts and cgroup namespaces, and sees only `lo`. `/usr` and `/etc` are read-only; `/home`, `/run`, `/tmp` and `/var` are empty. The source was a scratch clone at the exact head (`run-selftest-sandbox.sh`, `run-in-sandbox.sh`).
- **Proof script.** `scripts/act_slot_proof.sh` was exercised only against a stand-in runner that never touches Docker, sudo or the network (`proof-probe/`).
- **Hardware and RTL tools.** No hardware was used. There is no HDL change, so the scoped Verilator was not needed and its identity was not checked.

## Findings

### R267-F1 MAJOR: a slot's uplink reaches host-routed container networks that Docker's isolation denies to slot 0

- **Lenses:** Conformance, RTL (architecture: the runner's isolation contract), Robustness, Tests, Docs.
- **Where:**
  - `scripts/act_ci.py:4049-4065` (`slot_firewall_rules`: the only reject is `fib daddr type local`);
  - `scripts/act_ci.py:3959-3991` (`slot_uplink_command`: pasta socket-level NAT);
  - `docs/testing/CI_WORKFLOWS.md:1744-1749` and `:1779-1786`.
- **Authority and evidence:**
  - **Where the traffic leaves.** A slot's egress leaves through pasta. Pasta runs in the host network namespace and opens host sockets for every destination. Its help text marks `--no-copy-routes` as the deprecated opt-out, so by default pasta copies the host's routes into the slot namespace.
  - **What the firewall rejects.** The slot's table rejects only destinations the host treats as local addresses.
  - **What stays reachable.** On the replay host, the author's own receipt (`author-a203/receipts/host-routes-before.txt`) routes the default daemon's bridges in the host namespace. These are `docker0` and four `milan-act-ci-*` networks, and `172.21.0.0/16` is live there. A read-only `ip -4 route` today still shows `docker0` and three `br-*` routes. A container address behind those bridges, such as a concurrently running slot-0 replay's job container, is not a local address, so the rule passes it.
  - **Why Docker's isolation does not apply.** Pasta's connection is host-originated, so it traverses the output path and never the forward path. Docker's inter-network isolation between bridge networks lives on the forward path. A slot-0 job container reaches another bridge network only through that forward path, so it is denied what a slot job gets.
  - **What was measured.** The author's mechanism experiment (`author-a203/receipts/mechanism-experiment.md`, items 3-4) and rehearsal measured only host-local targets: the bridge gateway, `docker0` and loopback. No container address behind a host bridge was tested.
  - **What the documents claim.** The DECISION and the docs present the table as closing the slot to the host and to other replays. The docs say "DNS and the internet stay reachable" and "A replay in one slot cannot collide with a replay in another". The docs do not disclose this residual path, and no offline or live control covers it.
- **Impact.** Candidate code in any isolated slot can open TCP, UDP or ICMP flows to unpublished ports of every container on the default daemon. That includes the job containers of a slot-0 replay running at the same time (for another PR), and any container or VM network the host routes locally. Slot-0 jobs cannot do this. Acceptance 2 says a slot "cannot block or corrupt another slot", and that is not established for slot 0 running beside slot N, which the docs name as a supported pairing.
- **Required outcome.** Either:
  - traffic from a slot cannot reach any destination the host routes through a host-local virtual interface, while DNS and the internet still work; or
  - the residual exposure is accepted in a public decision and stated in `CI_WORKFLOWS.md`.

  In both cases the live proof must include a negative control: a slot job that tries a listener inside a default-daemon container on a runner-created bridge must be refused.
- **Verification.**
  - Offline: an arm pins the new rule, and a mutation that removes it is killed.
  - Live, under the audited install: the control is refused while the internet control passes.

### R267-F2 MAJOR: the acceptance-1 live proof can print `PROVED` with no workflow run and no slot entered

- **Lenses:** Tests, Conformance, Docs.
- **Where:**
  - `scripts/act_slot_proof.sh:93-120` (the verdict is `exit N` plus any per-workflow lines; the comparison is `cmp -s`);
  - `:163-168` (the interrupt arm grades the exit status only);
  - `:177-178` (the no-isolation collision is optional);
  - `scripts/act_ci.py:13571`;
  - `docs/testing/CI_WORKFLOWS.md:1871-1877` ("It exits 0 only when every proof holds").
- **Authority and evidence:**
  - **The acceptance.** Acceptance 1 says two concurrent replays "complete ... with verdicts identical to their serial runs", and asks for "a controlled collision control that fails without the isolation". AGENTS.md section 6 (Tests) says a test must be able to fail for the defect it claims to detect.
  - **Probe setup.** `proof-probe/run-proof-probe.sh` drives the head's proof script against a stand-in runner. That runner refuses every PR run identically (exit 2, no workflow line) after printing the slot-held marker. For `--interrupt-selftest` it prints only the slot-0 PASS line.
  - **Probe result.** The proof printed `PASS` for every arm and `PROVED every slot proof held`, and exited 0 (`receipts/proof-probe-vacuous.log`). Every `.verdict` file is just `exit 2`, and this probe run did not pass `--collide-default`.
  - **No offline pin either.** My probe R01 (`receipts/mutation-probes-a37af3c6.log`) makes `run_live_selftest` pass `ReplaySlot(0)` to the interrupt gate. It survives the offline self-test. So a runner that ignores `--slot` for the live gate would be graded "interrupt self-test in slot 1: PASS".
- **Impact.** The instrument meant to close acceptance 1, and the live half of acceptance 2, can report success when no replay completed, when the interrupt gate never entered the slot, or when the only collision shown is the new lock rather than the collision the isolation exists to prevent.
- **Required outcome.**
  - A reference or parallel run counts only if it completed: exit 0 or 1, with one per-workflow `PASS`/`FAILED` line for every selected workflow. Any exit-2 run fails the proof.
  - The interrupt arm requires the runner's own `interrupt-selftest: slot N:` teardown line, and the offline self-test pins that the live gate runs in the selected slot (R01 killed).
  - The collision control that "fails without the isolation" (slot 0, or one shared daemon) is part of the default `PROVED` path, or acceptance 1 is publicly re-scoped.
- **Verification.** Re-run `proof-probe/run-proof-probe.sh` at the new head: it must not print `PROVED`, and must exit non-zero. Re-run `mutation-probes.py`: R01 must be KILLED.

### R267-F3 MINOR: several documented teardown proofs and slot guards have no offline negative control

- **Lenses:** Tests, Docs.
- **Where:**
  - `scripts/act_ci.py:4335-4375`, `:4091-4102`, `:4157-4168`, `:3848-3857`, `:3881-3885`, `:4378-4407`;
  - `selftest_slot_teardown_failures` (`:11529`);
  - `docs/testing/CI_WORKFLOWS.md:1827-1832` and `:1901-1902` ("each kind of survivor").
- **Evidence.**
  - **Probe set.** `mutation-probes.py` applies 18 independent single-site mutants in the sandbox, each applying exactly once, and the head bytes are restored and verified. 12 survive the offline self-test:
    - R03: runtime-directory absence not proved;
    - R04: uplink pidfile absence not proved;
    - R05: uplink unload result ignored;
    - R07: slice cgroup absence not proved;
    - R08: an nft query failing with any error is read as "table absent", which is fail-open;
    - R09: `validate_slot_root` is not called on acquisition;
    - R10: the production lock accepts a lock file owned by the invoking user;
    - R11: `sudo` without `-n` in the privileged-command wrapper;
    - R12: slot teardown runs without blocked cleanup signals;
    - R15: residue counts only units in load state `loaded`;
    - R01 and R02: the interrupt-gate wiring (see F2).
  - **What is covered.** The existing survivor arms cover only daemon, namespace, table and runtime cap. The head code does implement each of the missing proofs correctly; they are simply unpinned.
  - **Controls.** R06, R13, R14, R16, R17 and R18 were killed as expected.
- **Impact.** Four of the eight absence proofs the docs enumerate, the fail-closed nft classification, the slot-root and lock-owner guards, and the protected teardown can all be deleted with the self-test still green. The docs' claim that the self-test pins "each kind of survivor" is not true.
- **Required outcome.** Either add negative controls that kill R03-R05, R07-R12 and R15 (for example survivor arms for each proof, an unexpected nft error, acquisition through a bad slot root, the production owner and prefix, a repeated signal during teardown), or narrow the documented claim to what is pinned.
- **Verification.** `mutation-probes.py` at the new head reports those probes KILLED.

### R267-F4 MINOR: the slot memory cap is a replica-only limit whose effect on verdicts is unmeasured and unattributed

- **Lenses:** Conformance, RTL (resource effects), Robustness, Docs.
- **Where:** `scripts/act_ci.py:154` (`SLOT_MEMORY_MAX = "24G"`), and `docs/testing/CI_WORKFLOWS.md:1793-1798` against `:1519-1528`.
- **Evidence.**
  - The docs say a slot "replays exactly the hosted-shaped jobs ... only its CPUs differ".
  - The same page documents that `rtl.yml`'s sharded jobs hold up to four 16 GB containers at once, "at most 64 GB". Each hosted job has its own VM.
  - The slot slice caps the whole slot at 24 GB, which is not hosted-shaped. The author's REVIEW READY says the cap "has not been measured on a full `rtl-full` replay inside a slot".
  - An OOM kill inside the slice ends a job, and the runner reports an ordinary `FAILED` workflow (exit 1). There is no check of the slice's OOM events that would attribute it to the replica.
- **Impact.** A slot can produce a candidate `FAILED` verdict that a slot-0 or hosted run would not. This breaks acceptance 1's verdict identity, and the failure cannot be told apart from a real one.
- **Required outcome.** Either:
  - measure the shipping workflows' aggregate peak inside a slot and document the headroom; or
  - make an OOM kill inside the slot slice an attributable infrastructure refusal (exit 2 naming the cap).

  In both cases, correct the "only its CPUs differ" sentence.
- **Verification.** A live measurement receipt, or an offline arm for the attribution, plus the corrected doc text.

### R267-F5 MINOR: slot-root validation is narrower than the recorded DECISION

- **Lenses:** Conformance, Robustness.
- **Where:** `scripts/act_ci.py:3807-3837` (`validate_slot_root`, which checks only the final component with `lstat`), against the DECISION at https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5796770637 ("root-owned ... not writable by group or other and has no symlink in its path").
- **Evidence.** `slot0-differential.py`, run in the sandbox (`receipts/slot0-differential-root.log`), shows that `validate_slot_root` accepts a root reached through a symlinked parent, and a root under an other-writable (0777) parent. The data-root of a root-run dockerd lives under this path. No public note records the narrowing.
- **Impact.** An ancestor controlled by someone other than root can redirect or replace the slot root between validation and dockerd's start. This silently diverges from the design authority.
- **Required outcome.** Either implement the DECISION (no symlink in any component, and no ancestor writable by anyone but root), or publish the narrowed rule as an amended decision and document it. Either way, add an offline arm for both cases.
- **Verification.** Both observation lines in `slot0-differential.py` turn into refusals, and there is a new offline arm.

### Suggestions (optional; they do not affect coverage)

- **S1 (Robustness).** `release_replay_slot` (`scripts/act_ci.py:4358-4359`) deletes the table even when the uplink's or the slice's absence was not proved. Consider keeping the table, and reporting, while either survives, so a failed teardown never removes the isolation from a still-connected slot.
- **S2 (Robustness, Docs).** Pasta runs with `--runas 0:0` while parsing untrusted traffic, and relies on its own sandbox. The DECISION does not record why (the receipt says: to join a root-owned netns). Consider recording that, or using a less-privileged arrangement.
- **S3 (Robustness).** The slice has no tasks bound, so a fork bomb in one slot can exhaust host PIDs for the other slots.
- **S4 (Robustness).** The table's presence is proved only at teardown. Consider re-checking it before each act spawn, as the lease gate does.
- **S5 (Docs, Robustness).** The pool `10.231.N.0/24` is not checked against host routes, which pasta copies into the slot. Consider refusing or documenting an overlap.

## Checked and found clean within the lenses (evidence; not lens PASS lines)

- **Slot 0 unchanged (acceptance 4).** `receipts/slot0-differential-root.log` imports the base (`759da623`) and head runners in the sandbox. The following are identical: the controlled environment; the Docker and act prefixes with and without sudo; the CPU set `0-3`; the full act command for `docs`, `elaborate`, `rtl-fast` and `rtl-full`; the boundary shape (plus `slot=0`); and every pre-existing option. The only intended difference is the new refusal of an inherited `DOCKER_*`, which is recorded in the DECISION and the docs.
- **No refusal weakened (acceptance 6).** `receipts/refusal-preservation.txt` is a static AST comparison: all 274 distinct base `raise Refusal(...)` expressions are present at head, none is raised fewer times, and there are 302 distinct at head.
- **No existing self-test arm lost.** `receipts/selftest-label-diff-base-head.txt`: base 277 of 277 ok in the sandbox, head 363 of 363 ok, with 0 base labels missing and 86 added. The head also passes as namespace root (`receipts/selftest-head-a37af3c6-sandbox-root.log`). The hosted `docs-check` at the exact head executed it with 363 ok and 0 FAIL (`receipts/hosted-docs-check-excerpt-a37af3c6.txt`).
- **Privilege boundary.** The runner stays unprivileged. Only fixed argv runs under `sudo -n`: `touch`, `ip`, `systemctl`, `systemd-run`, `nft -f` on the runner's own run-directory file, and `nsenter`, `env -i`, act and docker. No slot argument derives from candidate content; the inputs are the slot number, `--slot-root` and a 128-bit token.
- **Daemon and endpoint.** The dockerd socket path lives under the root-only `/run`, and residue is refused before creation. The identity check requires both labels and the data-root.
- **Refusals and wiring.** The inherited `DOCKER_*` refusal precedes every collaborator in all four Docker modes. `--boundary-selftest` and `--selftest` refuse slots. The boundary-to-slot mismatch is refused before any Docker call.
- **Lock.** The lock is `O_NOFOLLOW`, root-owner and flock `LOCK_NB`; `/run/lock` is `0755 root` on this host, and `protected_symlinks=1`.
- **Acquisition and teardown order.** Every step is recorded as attempted before its command, and rollback at every step is exercised by the head's own arms. My R16 (reordering the table deletion before the uplink stop) and R17 (narrowing the rule) are killed.
- **Scope gate.** `receipts/focused-gates-a37af3c6.log`: `check_baremetal_only.py --check` reports 0 findings over 847 files, and `--selftest` passes 441 arms. The masks are exact whole-line anchored contexts, pinned to one file, with 8 arms per masked line. The other gates also pass: `docs_check.py` (0 findings), `check_em_dash.py --base 759da623` (0 findings over 210 lines), `gen_toc.py --check`, `check_doc_paths.py`, `check_py_idiom.py`, `check_sh_idiom.py` and `git diff --check`.
- **RTL surface.** No `hdl/`, `tb/`, `syn/`, `constraints/` or processor file is in the lane's diff against `dev`. The four touched files are host tooling and documentation.

## Prior public findings on this PR

- **Manager SOURCE VALIDATION r1 at `fcce541b`** ("`scripts/check_baremetal_only.py --check` FAILS with 29 findings"): **resolved at this head.** 0 findings and 441 arms locally, and the same in the hosted `docs-check` at `a37af3c6`.
- No earlier review round on PR #533 had published findings when this round started.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F4, F5) | issue #532 acceptance 1-6 and DECISION; `scripts/act_ci.py` slot code (`:3807-4435`, `:13553-13636`); `scripts/act_slot_proof.sh`; `receipts/slot0-differential-root.log`; `receipts/refusal-preservation.txt` | R267-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| RTL | UNCLEAN (F1, F4) | lane diff vs `dev` (no HDL, tb, syn or constraints file); runner architecture: isolation contract, lifecycle order and rollback, resource bounds (`scripts/act_ci.py:3959-4065`, `:4157-4435`, `:154`) | R267-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| Robustness | UNCLEAN (F1, F4, F5) | slot firewall and uplink; residue, rollback and teardown paths; lock; slot root; memory cap (`scripts/act_ci.py:3807-4407`); author receipts `mechanism-experiment.md`, `host-routes-before.txt`, `rehearsal-production-argv.log` | R267-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| Tests | UNCLEAN (F1, F2, F3) | head self-test 363 of 363 (sandbox user and root, plus hosted); base 277 preserved; `receipts/mutation-probes-a37af3c6.log` (18 probes, 12 survive); `receipts/proof-probe-vacuous.log` | R267-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |
| Docs | UNCLEAN (F1, F2, F3, F4) | `docs/testing/CI_WORKFLOWS.md:1311-1322`, `:1509-1596`, `:1709-1905`; runner module docstring and help; `receipts/focused-gates-a37af3c6.log` | R267-1 | a37af3c6ad54aa16403861c969f68cf2a83679c6 |

## Real limits of this round

- **F1 is not demonstrated live.** It rests on the head's rule text, pasta's documented defaults, the host routing shown in the author's receipts and a read-only route listing, and the forward-path placement of Docker's inter-network isolation. Neither the author nor this round connected from a slot to a container address behind a host bridge; the required control closes that gap.
- **Sandbox differences.** The candidate self-test and the probes ran in a namespace sandbox on this host's Python 3.14.7, not in the author's Ubuntu 24.04 image. The hosted exact-head `docs-check` run independently executed the same self-test.
- **Nothing live was run.** No live slot behaviour was exercised: no daemon, pasta, nft, slice, interrupt gate or concurrent replay. No full bank (parent, PP, gPTP, Yosys, builder) was run. Physical calibration was NOT RUN and is not implied.
- **Hosted state.** When read, the exact-head hosted `docs-check`, `docs-check-no-git`, `elaborate`, `rtl-fast` and `wire-accountability` had succeeded. Verilator shard 4/5 was still in progress, and `verilator-suites` and `yosys-portability` had not been emitted. The physical gPTP job is a skipped nightly context, not evidence (`receipts/hosted-check-runs-a37af3c6.tsv`).
- **Clone state.** The review clone is at the exact head with a clean worktree, index equal to the HEAD tree, the four gitlinks at their pins, and the key file bytes and modes recorded (`receipts/clone-integrity-a37af3c6.txt`).

## Pending manager duties

- Publish the source static/builder and native bank results for this head, which this round does not claim or infer.
- After F1 and F2 are fixed and re-reviewed, run the audited-install live proof. It must include:
  - the interrupt gate in a slot;
  - completed serial references;
  - concurrent slots;
  - both collision controls;
  - the F1 negative control.
- Build and gate the current-`dev` candidate merge at the merge turn (source base `ede8d48e`, live dev `759da623` or later).
- Confirm the hosted exact-head `verilator-suites` and `yosys-portability` contexts.
- Run post-merge containment.
- Re-cover every lens at the fixing head. All five are UNCLEAN here.

R267-1 FINISHED
