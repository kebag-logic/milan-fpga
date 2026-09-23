[A213] REVIEW READY
Commit: `f5497170a2c444e01175683606310dbe7fbb2816` (tree `c340d594d9d3576f8a469ce4031c129ea8616183`) on `532-act-parallel-slots`: three one-line commits on the reviewed head `a37af3c6`. It is local and unpushed; the manager pushes it to PR #533 with the new body (`Closes #532`). Correction round 1 for R266-1 and R267-1.

Changed:
- `scripts/act_ci.py` (`f82018a7`): uplink-only slot firewall, slot-cap exhaustion refused, every slot-root ancestor checked, and a failing self-test control for each slot guard the reviews named.
- `scripts/act_slot_proof.sh` (`ba13a62c`): `PROVED` only from completed, overlapping runs, the isolation control and both collision controls; new offline `--selftest`.
- `docs/testing/CI_WORKFLOWS.md` (`f5497170`).
- `scripts/check_baremetal_only.py` is unchanged: no mask was widened.

**Per finding** (severity and lens as filed)

| Finding | Severity, lens | Change | Negative control that fails without it |
|---|---|---|---|
| R266 F1 = R267 F1 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | The slot table keeps its host-local reject and adds `socket cgroupv2 level 1 "<slice>" oifname != { <uplinks> } counter reject`. The uplinks are the host's unicast default-route interfaces. The runner reads them with `ip -json -4\|-6 route show default` after the residue check and before creating anything. It refuses no usable route, an unreachable-only default, loopback, an unquotable name, malformed output and a failed query. A slot can no longer reach a container behind any host bridge, or a port Docker publishes on a host address, since Docker's destination rewrite runs before the filter. | **Offline:** the rule text is pinned; the loaded firewall must match the discovered uplinks; 8 mutants (rule dropped or inverted, uplinks ignored, unreachable default taken, failed query read as none, lo, unquotable or empty set accepted) are KILLED. **Rehearsal** (one unprivileged user+net+mount namespace, the runner's exact pasta options, rule text emitted by the committed runner, with the cgroup selector removed): under the head's rule, the routed container and the DNAT-published port are REACHED. Under the new rules both are REFUSED and host-local is REFUSED, while internet and DNS answer. **Live**, in the proof: while each slot is held, a listener container on a new default-daemon bridge and its gateway-published port must be refused from inside the slot, and `github.com:443` must answer. The same probe from the host must reach both targets. |
| R266 F3 = R267 F2 | MAJOR; Tests, Conformance (R267: also Docs) | A run counts only if it completed: exit 0 with a PASS for every selected workflow in order, or exit 1 with PASS lines up to the FAILED one, where the runner stops. The interrupt arm requires the runner's own `interrupt-selftest: slot N:` line. Both slots must be seen held before either run prints a verdict. The rival must be refused for the lock reason before the holder's verdict. The slot-0 collision always runs (`--collide-default` is removed). `PROVED` needs exactly ten PASS records. | R266's and R267's refusing stand-ins, and all three original author fakes, now exit 1 without `PROVED`. The proof's `--selftest` has 14 cases: the honest case proves and 13 broken cases each FAIL on their own check. 14 mutants of the proof's checks are KILLED. Runner arms kill R01 (live gate run in slot 0) and R02 (gate never enters its slot). |
| R266 F2 | MAJOR; Tests, Docs | A survivor arm for each of the nine absence proofs. At residue and teardown time, an arm for each query that cannot answer (LoadState of each unit, ActiveState, DropInPaths, `nft list`). The doc now lists exactly what is pinned. | R266's six mutants and R267's R03-R08 are KILLED. |
| R266 F4 | MINOR; Docs | Lock: taken after materialization and held until teardown ends. The per-slot 24G aggregate versus slot 0's 64 GB and hosted 16 GB per job is stated. | Doc re-read against `run_validation` and `SLOT_MEMORY_MAX`. |
| R266 F5 | MINOR; Tests | Controls for root validation on acquisition, the CPU boundary (an 11-CPU host refuses slot 2, a 12-CPU host gets 8-11), signal-blocked teardown, non-active slice states, the dangling-symlink probe, and the interrupt gate entering its slot (now offline). | Those six mutants are KILLED. |
| R266 F6 = R267 F5 | MINOR; Conformance, Robustness | Every component from `/` down must be a real directory (no symlink), root-owned and not group- or other-writable. That is the DECISION's rule, applied to every ancestor. | Arms: symlinked parent and top level, user-owned, group-writable, sticky 1777 and non-directory parents, a missing parent, and on acquisition. Two ancestor mutants are KILLED. |
| R267 F3 | MINOR; Tests, Docs | As above, plus: R09 root on acquisition; R10 the lock owner default, pinned as the literal `0` so it is killed as root too; R11 the exact `sudo -n --` argv, env, cwd and timeout; R12 blocked signals; R15 any unit state but absent. | R03-R05, R07-R12 and R15 are KILLED as uid 1000 and uid 0. |
| R267 F4 | MINOR; Conformance, RTL, Robustness, Docs | After the workflows, a nonzero `oom` in the slice's own `memory.events.local` is exit 2 naming the cap, never a `FAILED`. That file does not count a container's own 16 GB limit. Unreadable or malformed events are also exit 2. The peak is printed. The doc sentence is corrected, and the cap is stated as unmeasured. | Six arms and four mutants KILLED (check removed, oom ignored, missing count read as 0, hierarchical file read). The measurement is the live proof's `rtl-full` pair: each slot prints its peak. |

Suggestions taken: R266 S4 (the `show` queries are now pinned literally) and S5 (overlap). The other suggestions were not taken.

**Design amendments to the DECISION** (issuecomment-5796770637)
- The firewall has two rules, and a read-only default-route query runs before slot creation.
- The lock is held from slot acquisition to the end of teardown, not "the whole invocation". This is a wording correction only; the code is unchanged.
- The slot-root rule applies to every ancestor.
- A slot-cap exhaustion is exit 2.
- The live proof always runs the slot-0 collision, adds the isolation control, and calls `sudo -n` itself for the default daemon's Docker CLI, `nsenter` and the probes.

Validation (all offline; no Docker, act, sudo, privilege or host network):
- **Candidate `act_ci.py --selftest`.** Run only inside an unprivileged, network-less namespace sandbox (new user, net, pid, ipc, uts and cgroup namespaces; only `lo`), from a clean clone of `f5497170`. Result: **422 checks, 0 FAIL**, as uid 1000 and as uid 0. The baseline `a37af3c6` in the same sandbox gives 363. 4 arms are reworded (strengthened) and 59 added; no label is lost.
- **Slot mutants:** 53/53 KILLED, as uid 1000 and uid 0 (R266's 21, R267's 18 and 14 new). The no-op control survives, and the stage bytes are restored exactly.
- **Proof mutants:** 14/14 KILLED, and the control survives. One intermediate draft of the proof's overlap check read status files that lag the runner's exit, and flaked under load. It now reads the runner's own log. The final self-test passed on every run: 3 repeats plus final runs as uid 1000 and uid 0.
- **Gates at the head, all rc 0:**
  - `check_baremetal_only.py --check`: 0 findings over 847 files; `--selftest`: 441 arms.
  - `docs_check.py`: 0 findings.
  - `check_em_dash.py --base 759da623`: 0 findings over 299 added lines.
  - `check_py_idiom.py` and `check_sh_idiom.py`.
  - The naming, fail-fast, test-evidence and hygiene ratchets, `--check` and `--selftest`.
  - `ci_events.py --check` and `--selftest`, and `check_feature_status.py`.
  - `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `check_doc_style.py`.
  - `git diff --check` from `759da623` and from `a37af3c6`.

Acceptance criteria:
- **1: not met yet.** It needs the audited live proof. Run `act_slot_proof.sh --selftest` first; the command is in the doc and the PR body.
- **2 and 3:** met offline. Per-slot isolation is shown now by a failing control offline and by the namespace rehearsal; the live control is part of the proof.
- **4, 5 and 6:** met. Slot 0 is unchanged apart from the inherited-endpoint refusal, and no workflow file changes.

Open risks/questions:
- **Nothing is proven live yet:** not the uplink discovery on this host (it would allow `enp1s0` only), the isolation control, the memory-events read or the teardown.
- **Networks that do not follow the default route:** a nameserver reached through an interface without a default route is refused to slots (documented). A host where the `-6` route query fails refuses slots. A route change during a run fails closed.
- **Attribution of a cap-killed daemon:** if the cap kills the slot's own dockerd or containerd, the run is still exit 2, but with the Docker error rather than the cap's name.
- **Slot roots on `/data`:** `/data` on this host is owned by a user, so a slot root under it is refused. Use a root-owned path or a root-owned bind mount.
- **The original author's pass fake no longer proves.** It omits the slot teardown line R267-F2 requires, and prints one workflow of the default four. Its two break cases still fail.
