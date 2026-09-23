[A220] REVIEW READY
Commit: `604297bb41d6c8005d07539289b10bfa99273cdd` (tree `1a8cfc31dedc8eef7929a5a7529568503fa580d4`) on `532-act-parallel-slots`. These are five one-line commits on the reviewed head `f5497170`, each without a trailer. The branch is local and unpushed; the manager pushes it to PR #533 with the new body (`Closes #532`). This is correction round 2, for R266-2 and R267-2.

Changed:
- `scripts/act_slot_proof.sh` (`3a768c4f`): the offline `--selftest` grows from 14 to 38 cases. The honest case proves. 7 bad starts must exit 2 before any check records anything. 30 broken cases must each fail on the check meant to catch them. The live checks themselves are unchanged.
- `scripts/act_ci.py` (`9145a06c`, `604297bb`): the slot line prints the slice's `max` count beside the peak, `memory peak X of its 24G cap; the cap was hit N time(s), with no OOM at it`, instead of "which never ran out". Events without a `max` count are refused like events without `oom`. The comments state exactly what is refused. There are new arms.
- `docs/testing/CI_WORKFLOWS.md` (`317a158d`, `d47dc360`, `604297bb`): what the memory-cap check detects and what it does not, the `DOCKER-USER` note, and every case group of the proof's self-test, with the two guards that have no case.
- `scripts/check_baremetal_only.py` is unchanged, and no mask was widened.

**Per finding** (severity and lens as filed)

| Finding | Severity, lens | Change | Negative control that fails without it |
|---|---|---|---|
| R266-2 F1 = R267-2 F1 | MINOR; Tests | New cases: **(a)** a slot that cannot reach the probe name; **(b)** a host that cannot reach the published port while the container answers, and one that cannot reach the container; **(c)** a slot-0 rival refused for neither the tool cache nor a job volume. Also every guard R267-2 listed as surviving: a run refused after passing (P03) or after failing (P04) its workflows; a wrong digest (P05); a group-writable runner (P06); a non-empty log directory (P07); a surviving target network (P11); slots A and B equal or either one 0 (P12); an interrupt gate without its PASS line (P13). And R266-2's M6-M8, an interrupt gate refused after both lines, a slot reaching only the published port, a target that cannot start or cannot be queried after removal, a non-numeric slot, and `complete` graded at the parallel comparison and the collision holder. | R266-2's script at the head: **M1, M2 and M11 KILLED**, and M3-M8 and M10, each by exactly its own case. M9, the ten-`PASS` backstop, SURVIVES; R266-2 ruled it needs no case, and the doc now says no case reaches it. The control SURVIVES. R267-2's script: **P01-P13 KILLED**, and the P00 control SURVIVES. The earlier 14 proof mutants are KILLED. 10 author mutants of the remaining guards are KILLED. Every set's control survives. |
| R267-2 F2 | MINOR; RTL, Robustness, Docs | **Docs** (doc, `SLOT_MEMORY_MAX` comment, docstrings): the runner refuses only a nonzero `oom` in the slice's own `memory.events.local`, which is an OOM at the slot's own cap. It does not detect reclaim at the cap (which can slow a job into a workflow timeout) or an allocation that fails without trying the OOM killer, and such a run keeps its verdict. **Reported:** the peak and the `max` count. The doc tells the operator to replay a slot `FAILED` with a nonzero count in slot 0 before attributing it to the candidate. **Tightened:** events without `max` are refused. No refusal text changed. | Arms (424, up from 422): the honest line with its count; events without `max` refused and still torn down; **a `FAILED` run whose slice sat at its cap without an OOM (peak = 24G, `max` 5361, `oom` 0) keeps its `FAILED`**. Slot mutants KILLED: missing `max` read as 0, the count taken from `oom`, and a slice at its cap without an OOM refused (killed only by the new arm). A213's four cap mutants still apply and are KILLED. |
| R266-2 S1 | suggestion; Docs, Robustness | Taken. An egress policy in `DOCKER-USER` sees only forwarded traffic, so it misses slot traffic. A host restricting job egress there must also restrict the slot slices' host output. | Doc-only. |

R267-2 S1-S3 were not taken. They are optional, and S1 would edit a hosted workflow.

Validation (all offline; no Docker, act, sudo, privilege or host network):
- **Candidate `act_ci.py --selftest`**, run only inside an unprivileged, network-less namespace sandbox (only `lo`, the lane tree bound read-only): **424 ok, 0 FAIL** as uid 1000 and as uid 0 at `604297bb`. Against the published 422 at `f5497170`: 1 label reworded (it now also pins the count), 2 added, none lost.
- **`act_slot_proof.sh --selftest`:** PASS, 38 cases, 4 runs out of 4 in the same sandbox (uid 1000 three times, uid 0 once).
- **Mutants**, all on scratch copies, with the lane files' digests verified after every set:
  - proof sets as above;
  - slot mutants **56/56 KILLED** as uid 1000 and as uid 0: the published 53 plus 3 new, all applying once, with the control surviving.
  - The proof-script receipts were taken at `317a158d`, whose `act_slot_proof.sh` is byte-identical to the head's.
- **Gates at the head, all rc 0:**
  - `check_baremetal_only.py --check` (0 findings, 847 files) and `--selftest` (441 arms);
  - `docs_check.py` (0 findings);
  - `check_em_dash.py --base 759da623` (0 findings);
  - `check_py_idiom.py` and `check_sh_idiom.py`, with and without `--selftest`;
  - `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `check_doc_style.py`;
  - hygiene, `ci_events.py --check` and `--selftest`, `check_feature_status.py`, `check_todo_ownership.py`;
  - `bash -n`, and `git diff --check` from `759da623` and from `f5497170`.
- Receipts, helper scripts and unmodified copies of both reviewers' scripts are in the author packet (`HANDOFF.md`, `MANIFEST.sha256`), for the manager to publish.

Acceptance criteria:
- **1: not met yet.** It needs the audited live proof: `act_slot_proof.sh --selftest` first, then the ten checks with an `rtl-full` pair, whose run logs now record each slot's peak and cap-hit count.
- **2 and 3:** met offline, as in round 1; their live halves are part of the proof. For 3, the slot cap's detection limits are now documented exactly.
- **4 and 5:** met.
- **6:** met. No workflow file changed, and no refusal was weakened; the one new refusal, events without `max`, is a tightening.

Open risks/questions:
- **The count is shown against the fake slot host only.** Its meaning rests on cgroup v2 `memory.events` semantics and on R267-2's published probe, which this round did not re-run. A nonzero count is also expected from ordinary page-cache reclaim, so it flags a run for a slot-0 replay rather than proving harm.
- **Two proof guards have no offline case, as documented:** the ten-`PASS` backstop, and the non-root writability test for a runner with no write bit.
- **Re-review scope:** the commits touch all three changed files, including the acceptance-1 instrument and the runner, so every lens needs re-covering at `604297bb`.
