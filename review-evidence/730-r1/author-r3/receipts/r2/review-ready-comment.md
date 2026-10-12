[A607] REVIEW READY (Round 2)
Commit: `5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646` on `730-act-cpusets`. These are new commits on top of `eb566634`, with no rebase or amend. They are local and not pushed: this round may not push.
- `93215f07`: code and self-tests.
- `5ba8313a`: `docs/testing/CI_WORKFLOWS.md`.

Changed (answers to [6132404197](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132404197), items 1-6):
1. **R633-1-F1.** A job range is reserved from placement until the container's `destroy`, or until `docker container inspect` shows the daemon no longer has it. `die` frees nothing. Where a container runs is read with `docker container inspect --format {{.HostConfig.CpusetCpus}}`, not inferred from events. The runner reads it after each move, at each `start`, at an `update` of a container not yet seen on its range, and for every holder when no range is free.
   - Standing test `selftest_job_cpu_record`: R633-1's exact sequence `create A, update A, start A, die A, create B, update B, start B, start A` runs against a model daemon that holds each container's real cpuset. After every event, no two containers share a range, and every container on a job range holds it in the record. A restarts on `4-7`; B gets `8-11`.
2. **R633-1-F2.** The target is reserved before `docker container update` runs. A timeout or failure keeps it reserved, and then an inspect decides. On target, the container counts as moved, with a warning saying the command failed but inspect shows it there. Off target or unreadable, it is a warning, and the range stays reserved until removal. Only the daemon's `No such container` frees it. A late `update` event is re-read.
   - Standing test `selftest_job_cpu_move_failures`, each case with the next container created while the outcome is uncertain: applied then CLI timeout (R633-1's probe); lost, then landing late; move and read both timing out; refused.
   - Problems stay warnings and never reach a verdict.
3. **R633-1-F3.** Slot 0 refuses a host without the derived ranges, as every slot does. The fallback and its plan text are gone. The self-test checks slot 0 at 1, 3, 4, 7, 8, 19, 20 and 21 CPUs for one and four containers: 19 refuses and 20 gives `4-7`..`16-19`; 7 refuses and 8 gives `4-7`.
4. **R633-1-F4 and R632-1-F1.** `stop_job_cpu_range_monitor` runs poll, containment, reader join and pipe close whatever an earlier step raised, and raises the first failure only after all of them. The join is retried until the reader is proven ended. A reader still alive after the bounded wait is a warning plus a printed containment hold, and teardown waits.
   - Standing test `selftest_job_cpu_monitor_busy`: the stream's line arrives only after the body returns, the move takes 0.2 s, and the stream ends only once contained. It runs for return, raise, SIGTERM, R633-1's reap failure, and raise plus reap failure.
   - Also pinned: poll failure, a join that fails once, and a stream or reader that cannot start.
5. **R632-1-F2.** `selftest_cpu_range_warnings` drives `execute_workflows` through the real spawn boundary with a container left on staging and two planted problems. With act exit 0 the verdict is `PASS`; with exit 3 it is `FAILED (3)`. Each workflow prints its summary once and exactly one `WARNING ... CPU ranges:` line per problem.
6. **Residue.** R632-1-R1's mixed-runner sentence is in CI_WORKFLOWS.md's slot resource bounds. R632-1-R2 is superseded by item 3, and the PR body now states the refusal.

Also found and fixed: `docs.yml` runs `act_ci.py --selftest` on a 4-vCPU hosted runner. Three self-test harnesses used the real CPU count and would have refused there under item 3. They now pin 128 CPUs.

The summary line changed, and the post-merge reading uses it: `act-ci: <wf>: CPU ranges: <n> job container(s) created: <m> seen on a range of their own by docker inspect, <g> removed before that, <s> never seen on one; at most <k> held a range at once`. For a full `rtl-full` run, expect `m == n`, `g == s == 0`, `k == 4`, and no `WARNING ... CPU ranges:` line. The plan line, the per-slot layout and the disjointness proof are unchanged.

Validation (all rc 0 at `5ba8313a`; CPython 3.12.3, PyYAML 6.0.3, pinned Markdown renderer):
- `python3 scripts/act_ci.py --selftest`: PASS, 490 ok, 0 FAIL (was 477). It also passes on CPython 3.14.7, and with `os.cpu_count` stubbed to 1, 2, 3, 4, 7, 8, 19, 20, 39, 40 and 128.
- `python3 scripts/ci_events.py --check`: 2016 items. `--selftest`: 2828 arms.
- `scripts/act_slot_proof.sh --selftest`: 44 cases.
- `python3 scripts/check_py_idiom.py`: ratchets hold (long function 9 <= 9, parameters 7 <= 7, over-long 0). `--selftest` also passes.
- `python3 scripts/check_baremetal_only.py --check` and `--selftest`.
- `python3 scripts/docs_check.py`, `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check` and `--verify-anchors`, and `python3 scripts/check_doc_paths.py`.
- `python3 scripts/check_em_dash.py --base dc4d06cb`: 0 findings over 120 added lines.
- `git diff --check dc4d06cb HEAD`.
- Mutants on scratch copies of the head tree:
  - 21 of 21 Round 2 mutants killed. They include `die` freeing, a timed-out or refused move released, no inspect, reap failure skipping the join, join before containment, a failed join not retried, the slot-0 fallback restored, and the harness host unpinned.
  - R632-1's `mutants.py`, re-run: 19 killed, including M13, M16, M17 and M23.
  - M18 survives; only the live interrupt gate pins it.
  - M08, M09, M20 and C24 are no longer applicable, because their anchors were removed by this round.
- Offline dry run of the shipping `rtl-full`: slot 0 and slot 3 rc 0, with plan lines byte-identical to Round 1.

Acceptance criteria:
- 1: met in code, proven offline, now with slot 0 refusing too.
- 2: met.
- 3: no workflow, step or job change, and every range is 4 wide. The same-head verdict comparison is post-merge (ruling).
- 4 and 5: post-merge (ruling).
- Hence `Relates to #730`.

Open risks/questions:
- **Material decision on item 2.** A timed-out move whose inspect shows the staging range keeps its target reserved until `destroy`, not just "until an inspect shows the effective cpuset". The daemon may still apply that request, and releasing the range would let the late completion land on a range already given to the next container (R633-1's delayed-completion case). The cost is one idle range for that container's life, reported as a warning. If the manager wants release on the first inspect instead, that is a one-line change, and the "lost then landing late" arm would then fail by design.
- No `docker events`, `docker container update` or `docker container inspect` has run against a live daemon in this lane (ruling). Each container now costs one inspect after its move and one at each `start`. The added latency is not measured.
- `--dry-run` is still not daemon-free (unchanged from Round 1). The dry-run lines come from the offline harness.
