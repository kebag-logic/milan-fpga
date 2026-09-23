# [A213] #532 / PR #533 correction round 1: handoff

Author A213. Answers R266-1 (F1-F3 MAJOR, F4-F6 MINOR) and R267-1 (F1-F2 MAJOR, F3-F5 MINOR).

## Head

- Lane `532-act-parallel-slots`, worktree `$LANES/532-act-parallel-slots`, clean.
- New head `f5497170a2c444e01175683606310dbe7fbb2816` (tree `c340d594d9d3576f8a469ce4031c129ea8616183`), three one-line commits on the reviewed head `a37af3c6`, no trailers:
  - `f82018a7` runner: uplink-only slot firewall, memory-cap refusal, slot-root ancestors, failing controls.
  - `ba13a62c` live proof: completed runs, overlap, isolation control, both collision controls, `--selftest`.
  - `f5497170` docs.
- **Local and unpushed.** PR #533 is still at `a37af3c6`. I did not push, edit the PR, merge or touch other checkouts.
- Files: `scripts/act_ci.py` sha256 `5aed7c03...ccf2c39` (mode 100755), `scripts/act_slot_proof.sh` `84d1777f...b63a7cb` (100755), `docs/testing/CI_WORKFLOWS.md` `a6e09ebd...a1fd147c`. `scripts/check_baremetal_only.py` is unchanged (no mask widened).

## Manager duties

1. Push `f5497170` to PR #533 and replace the PR body with `PR-BODY.md` (starts `[A213]`, carries `Closes #532`).
2. Archive this packet to `532-review-evidence` for the re-review (R266, R267 must re-cover every lens at the new head).
3. After the re-review, the live proof under the audited install (the bootstrap rule forbids me running it):
   - `scripts/act_slot_proof.sh --selftest` first (offline, 14 cases, about 15 s).
   - Then the live command in `PR-BODY.md`. It now needs `sudo -n` directly (default-daemon `docker`, `nsenter` into each slot, and the host-side probe), the runner image on the default daemon (the slot-0 serial references provide it; `--pull never`), and outbound 443 to `--probe-name` (default `github.com`).
   - `--collide-default` is gone: the slot-0 collision always runs, so the default daemon must be free of other replays for that step.
   - Include an `rtl-full` pair: each slot run now prints `act-ci: slot N: memory peak X GiB of its 24G cap, which never ran out`, which is the measurement R267-F4 and R266-F4 asked for. A run whose slot cap ran out is exit 2 naming the cap.
4. Slot roots: every ancestor must now be root-owned and not group/other-writable. On this host `/data` is owned by a user, so `/data/...` is refused as a slot root; use a root-owned path, or a root-owned bind mount of a directory on `/data`.

## What changed, per finding

| Finding | Severity, lens (as filed) | Change | Evidence (receipts/) |
|---|---|---|---|
| R266 F1 = R267 F1 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | Slot table adds `oifname != { <uplinks> } reject` for the slot cgroup; uplinks are the host's unicast default-route interfaces from `ip -json -4/-6 route show default`, read after the residue check and before any slot resource (refusals: no route, unreachable-only, no interface, loopback, unquotable name, malformed output, failed query). Live proof adds the isolation control. Doc rewritten. | `pasta-reach-rehearsal-final.log`: head rule, container and published port REACHED; new rules (emitted by the committed code), both REFUSED, host-local REFUSED, internet REACHED, DNS RESOLVED. 14 A213 mutants incl. 8 firewall/uplink ones KILLED; proof mutants for slot-side refusal, host differential, published probe, target absence KILLED. |
| R266 F3 = R267 F2 | MAJOR; Tests, Conformance (R267 also Docs) | Proof: complete-run rule, interrupt slot line, overlap before any verdict, rival refused before the holder's verdict and for the lock reason, slot-0 collision mandatory, exactly ten PASS for PROVED, `--selftest`. Runner arms for R01 and R02. | `proof-probes-reviewer-stand-ins-final.log`: R266 and R267 stand-ins and the three A203 fakes all exit 1 without PROVED. `proof-selftest-head-f5497170.log` 14/14. `proof-mutants-final.log` 14/14 KILLED. R01, R02 KILLED. |
| R266 F2 | MAJOR; Tests, Docs | Survivor arm for each of the nine absence proofs; residue- and teardown-time arms for every query that cannot answer (LoadState x2, ActiveState, DropInPaths, nft list). Doc lists exactly what is pinned. | R266's six survivors and R267 R03-R08 KILLED. |
| R266 F4 | MINOR; Docs | Lock timing stated (after materialization, until teardown ends); "only its CPUs differ" corrected; the cap's effect on multi-leg jobs stated. | Doc diff. |
| R266 F5 | MINOR; Tests | Controls for root validation on acquisition, CPU boundary (11 vs 12 CPUs), signal-blocked teardown, non-active slice residue, dangling symlink, and the interrupt gate entering its slot (now offline). | Those six mutants KILLED. |
| R266 F6 = R267 F5 | MINOR; Conformance, Robustness | `validate_slot_root` walks every component from `/`: no symlink, directory, root-owned, not group/other-writable. Arms for symlinked parent and top level, user-owned, group-writable, sticky 1777 and non-directory parents, a missing parent, and on acquisition. | Two ancestor mutants KILLED. |
| R267 F3 | MINOR; Tests, Docs | As R266 F2/F5, plus arms for R09 (root on acquisition), R10 (lock owner default, AST literal so it is killed as root too), R11 (`sudo -n` argv, env, cwd, timeout), R12 (signals blocked), R15 (unit states). | R03-R05, R07-R12, R15 KILLED as uid 1000 and uid 0. |
| R267 F4 | MINOR; Conformance, RTL, Robustness, Docs | After the body returns, the slice's `memory.events.local` `oom` > 0 is exit 2 naming the cap; unreadable or malformed is exit 2; peak printed. Doc sentence corrected and the cap stated as unmeasured. | Six memory arms; four memory mutants KILLED. Measurement is the live proof's `rtl-full` pair. |

Suggestions taken: R266 S4 (the `show` queries are now pinned literally), R266 S5 (overlap). Not taken: R266 S1-S3, R267 S1-S5.

## Validation (all offline; no Docker, act, sudo, privilege or host network)

- Candidate `act_ci.py --selftest`, run only inside an unprivileged, network-less namespace sandbox (new user, net, pid, ipc, uts and cgroup namespaces; only `lo`; read-only `/usr` and `/etc`; empty `/home`, `/run`, `/tmp`, `/var`), from a clean clone of `f5497170`: 422 checks, 0 FAIL, as uid 1000 and uid 0 (`selftest-head-f5497170-{user,root}.log`). Baseline `a37af3c6` in the same sandbox: 363, 0 FAIL. `selftest-label-diff-a37af3c6-f5497170.txt`: 4 arms reworded (strengthened), 59 added, none dropped.
- Slot mutants (`bin/slot-mutants.py`, 53 plus one control): 53 KILLED, control SURVIVED, as uid 1000 and uid 0; stage bytes restored exactly (`slot-mutants-final-{user,root}.log`).
- Proof mutants (`bin/proof-mutants.py`, 14 plus one control): 14 KILLED, control SURVIVED (`proof-mutants-final.log`).
- Firewall rehearsal (`bin/pasta-reach-rehearsal.sh`): one unprivileged user+net+mount namespace, runner's exact pasta options, rule text generated by the committed runner inside the sandbox. Fidelity limits: the cgroup selector is removed (pasta is the only socket owner in the model), and Docker's published-port DNAT is modelled by hand at the same hook priority.
- Gates at the committed head (`gates-final-head.log`): `check_baremetal_only.py --check` 0 findings over 847 files and `--selftest` 441 arms; `docs_check.py` 0; `check_em_dash.py --base 759da623` 0 over 299 added lines; `check_py_idiom.py`, `check_sh_idiom.py`; naming, fail-fast, test-evidence and hygiene `--check` and `--selftest`; `ci_events.py --check/--selftest`; `check_feature_status.py`; `gen_toc.py --check/--verify-anchors`; `check_doc_paths.py`; `check_doc_style.py`; `git diff --check` from `759da623` and from `a37af3c6`. All rc 0.

## Design amendments (published in the REVIEW READY)

- Firewall: two rules (host-local, and non-uplink egress) instead of one; a default-route query precedes slot creation.
- Lock: taken after materialization, held until teardown ends; the DECISION's "whole invocation" wording is corrected in the doc (no code change).
- Slot root: the DECISION's rule applied to every ancestor.
- Memory: a slot-cap exhaustion is exit 2, not a verdict.
- Live proof: slot-0 collision mandatory; isolation control; the proof calls `sudo -n` itself.

## Open risks

- Nothing here is proven live. The isolation control, the uplink discovery on a real host, the memory events read and the teardown need the audited live proof.
- A nameserver reached through an interface without a default route is refused to slots (documented). A host where `ip -6 route show` fails refuses slots.
- The uplink set is fixed at acquisition; a route change mid-run fails closed (traffic refused).
- If the slot cap kills the slot's own dockerd or containerd, the run is exit 2 with the Docker error rather than the cap's name.
- The proof's default workflow list mirrors the runner's `WORKFLOWS`; drift fails closed.
- The original author's fake "pass" runner no longer proves: it omits the slot teardown line R267-F2 requires and prints one workflow of the default four. Its two break cases still fail.
- The shell idiom gate reads heredoc text as shell: backticks or nested quotes inside the proof's embedded stand-ins count as findings (none remain).

## Packet

`bin/` helpers (sandbox runner, stage refresher, both mutation harnesses, rehearsal, proof stand-in driver), `receipts/`, `evidence/` (the archived review evidence I read), `PR-BODY.md`, this file, `MANIFEST.sha256`. Scratch clones under `scratch/` are disposable.
