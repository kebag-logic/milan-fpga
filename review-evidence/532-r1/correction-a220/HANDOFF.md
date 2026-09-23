# [A220] Handoff: #532 / PR #533, correction round 2

Author: A220. Assignment: https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5803011314
Findings answered: R266-2 F1 (https://github.com/kebag-logic/milan-fpga/pull/533#issuecomment-5802451902) and R267-2 F1 and F2 (https://github.com/kebag-logic/milan-fpga/pull/533#issuecomment-5803007221), all MINOR. R266-2 S1 taken.

## Head

- Branch `532-act-parallel-slots`, local and **unpushed**. Head `604297bb41d6c8005d07539289b10bfa99273cdd`, tree `1a8cfc31dedc8eef7929a5a7529568503fa580d4`.
- Five one-line commits on the reviewed head `f5497170`, each without a trailer:

| Commit | Files | Change |
|---|---|---|
| `3a768c4f` | `scripts/act_slot_proof.sh` | self-test from 14 to 38 cases |
| `9145a06c` | `scripts/act_ci.py` | cap-hit count printed, events without it refused, exact comments, arms |
| `317a158d` | `docs/testing/CI_WORKFLOWS.md` | memory-cap detection stated exactly, `DOCKER-USER` note, self-test cases listed |
| `d47dc360` | `docs/testing/CI_WORKFLOWS.md` | why no case reaches the ten-`PASS` backstop |
| `604297bb` | `scripts/act_ci.py`, `docs/testing/CI_WORKFLOWS.md` | arm: a `FAILED` run whose slice sat at its cap without an OOM keeps its `FAILED` |

- The files changed against `f5497170` are `scripts/act_ci.py`, `scripts/act_slot_proof.sh` and `docs/testing/CI_WORKFLOWS.md`. The net change against dev `759da623` is still the same four files as before; `scripts/check_baremetal_only.py` is unchanged and no mask was widened.
- `scripts/act_slot_proof.sh` is byte-identical at `317a158d` and `604297bb` (sha256 `3cffa803...`, `receipts/file-digests-604297bb.txt`), so the proof receipts taken at `317a158d` apply to the head.

## Per finding

| Finding | Severity, lens (as filed) | Change | Negative control that fails without it |
|---|---|---|---|
| R266-2 F1 = R267-2 F1 | MINOR; Tests | `act_slot_proof.sh --selftest` grows from 14 to 38 cases. **(a)** A slot that cannot reach the probe name. **(b)** A host that cannot reach the published port while the container answers, and one that cannot reach the container. **(c)** A slot-0 rival refused for neither the tool cache nor a job volume. **Every other guard R267-2 listed as surviving:** a run that passes every workflow and is then refused (P03), and one that fails a workflow and is then refused (P04); a runner that is not the recorded digest (P05) or is group-writable (P06); a non-empty log directory (P07); a surviving target network (P11); slots A and B equal, or either one 0 (P12); an interrupt gate without its PASS line (P13). **Also:** M6-M8 (a run refused before the other slot is taken, a rival refused for the lock but with exit 1, a run that never reports its slot daemon), an interrupt gate refused after both lines, a slot reaching only the published port, a target that cannot be started, a target query failing after removal, a non-numeric slot, and `complete` graded at the parallel comparison and the collision holder too. The 7 bad starts must exit 2 with the refusal text and no SUMMARY. The doc lists every case group and the two guards with no case. | R266-2's script at the head: **M1, M2 and M11 KILLED**, and M3-M8 and M10 too, each by exactly its own case. M9 (the ten-`PASS` backstop, which R266-2 ruled needs no case) SURVIVES, and the doc states that no case reaches it. The control SURVIVES. R267-2's script: **P01-P13 KILLED**, P00 SURVIVES. The earlier 14 published proof mutants are KILLED, with their control surviving. 10 author mutants of guards neither set mutated are KILLED, with the control surviving. |
| R267-2 F2 | MINOR; RTL, Robustness, Docs | Both options together. **Docs:** the doc, the `SLOT_MEMORY_MAX` comment and both docstrings now state exactly what is refused: a nonzero `oom` in the slice's own `memory.events.local`, an OOM at the slot's own cap. They also state what is not detected: reclaim at the cap, which can slow a job into a workflow timeout, and an allocation that fails without trying the OOM killer. Such a run keeps its verdict. **Reporting:** the slot line no longer says "which never ran out". It prints the peak and the slice's `max` count: `memory peak X of its 24G cap; the cap was hit N time(s), with no OOM at it`. The doc tells the operator to replay a slot `FAILED` with a nonzero count in slot 0 before attributing it to the candidate. **Refusal:** events without a `max` count are refused like events without `oom`. This is a tightening, and no refusal text changed. | Arms (424 checks, up from 422): the honest line with its count; events without a `max` count refused and still torn down; **a `FAILED` run whose slice sat at its cap (peak = 24G, `max` 5361, `oom` 0) keeps its `FAILED`**, the arm R267-2's verification names. Slot mutants: missing `max` read as zero, the count taken from the `oom` field, and a slice at its cap without an OOM refused are all KILLED, the last only by the new arm. A213's four cap mutants still apply and are KILLED. |
| R266-2 S1 (suggestion) | Docs, Robustness | Taken: the firewall bullet says an egress policy in `DOCKER-USER` sees only forwarded traffic, so it misses slot traffic, and a host restricting job egress there must also restrict the slot slices' host output. | Doc-only. |

Not taken (optional): R267-2 S1 (run the proof self-test in a hosted workflow: that edits a workflow file, outside this assignment), S2 (flush the runner's verdict line) and S3 (residue check for a stale runtime drop-in).

## Validation (all offline; receipts in `receipts/`)

- **Runner self-test**, only inside an unprivileged, network-less bubblewrap sandbox (new user, net, pid, ipc, uts and cgroup namespaces, only `lo`, the lane tree bound read-only; `bin/run-selftest-sandbox.sh`). At `604297bb`, clean tree: **424 ok, 0 FAIL** as uid 1000 and as uid 0 (`act-ci-selftest-604297bb-{user,root}.log`). Against the previous round's published receipt at `f5497170` (422): 1 label reworded (it now also pins the cap-hit count), 2 added, none lost (`act-ci-selftest-label-diff-f5497170-604297bb.txt`).
- **Proof self-test:** 38 cases, PASS 4 of 4 in the same sandbox, three runs as uid 1000 and one as uid 0 (`proof-selftest-317a158d.log`).
- **Proof mutants**, each on a scratch copy; the lane file is only read, and its digest is verified after every set:
  - `r266-2-proof-mutants-317a158d.log`: R266-2's published script, unmodified, run inside `unshare --user --map-current-user --net`.
  - `r267-2-proof-mutants-317a158d.log`: R267-2's published script, unmodified, which does its own `unshare`.
  - `a213-proof-mutants-317a158d.log`: the earlier 14.
  - `a220-proof-mutants-317a158d.log`: 10 author mutants plus a control, from `bin/proof-mutants-a220.py`.
  - The reviewer script copies in `reviewer-scripts/` are byte-identical to `532-review-evidence` `ed7ac220` `review-evidence/532-r1/reviews/R26{6,7}-2/scripts/`.
- **Slot mutants** (`slot-mutants-604297bb-{user,root}.log`, `bin/slot-mutants-a220.py`): the published A213 list is imported unchanged and 3 author mutants are added. Each mutated runner is bound read-only over the lane's copy inside the sandbox. Result: **56 of 56 KILLED** as uid 1000 and as uid 0, all applying exactly once, and the control SURVIVES.
- **Gates at `604297bb`, all rc 0** (`gates-604297bb.log`, `extra-gates-604297bb.log`):
  - `check_baremetal_only.py --check` (0 findings over 847 files) and `--selftest` (441 arms);
  - `docs_check.py` (0 findings);
  - `check_em_dash.py --base 759da623` (0 findings);
  - `check_py_idiom.py` and `check_sh_idiom.py`, with and without `--selftest`;
  - `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `check_doc_style.py`;
  - `check_hygiene.py`, `ci_events.py --check` and `--selftest`, `check_feature_status.py`, `check_todo_ownership.py`;
  - `bash -n`, and `git diff --check` from `759da623` and from `f5497170`.
  - The commit list in the gates receipt shows no body line beyond each subject.

## Limits

- **Nothing was run live:** no Docker, act, sudo, privilege or host network, no slot, and no live proof. The candidate runner ran only inside the sandbox.
- **The new `max` report is shown against the fake slot host only.** Its meaning rests on the cgroup v2 `memory.events` semantics and on R267-2's published probe (`memcap_probe.txt`), which this round did not re-run.
- **One uid-0 slot-mutant run was cut short** after 24 kills: its scratch directory under this output directory was removed by something outside the run. Nothing in the run deletes that path, and the sandbox cannot see it. The complete uid-0 runs used scratch under `/tmp`, and the kept receipts are complete.
- This session resumed a session cut off by a usage limit. The proof-script edits it found uncommitted were reviewed, completed and committed; nothing was discarded.

## For the manager

1. Push `f5497170..604297bb` to PR #533 and replace the body with `PR-BODY.md` (`Closes #532`).
2. Re-review by R266 and R267 at `604297bb`. The commits touch all three changed files, so every lens whose scope covers them is un-covered, Conformance included (the acceptance-1 instrument and the runner changed).
3. Hosted exact-head gates, then the audited live proof: `act_slot_proof.sh --selftest` first, then the ten-check proof with an `rtl-full` pair, whose run logs now record each slot's peak and cap-hit count.

## Packet

- `HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256`.
- `bin/`: `run-selftest-sandbox.sh`, `gates.sh`, `proof-mutants-a220.py` and `slot-mutants-a220.py`.
- `receipts/` (listed above).
- `reviewer-scripts/`: unmodified copies of the reviewers' published scripts and receipts.
