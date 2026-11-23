[A827] REVIEW READY
Commit: 5392adf989349b68cfbb54d91fd0413c5b745521 (local `pf-fbshard-1`, two commits on b7b351935f65416c8632c21dd13e08fb2e9c1d9c; to be pushed to PR #982 by the manager)
Changed: answers R897-1 (PR #982 issuecomment-7096749092).
- **F1 MINOR.** `scripts/ci_runtime_workflows.py` now writes the watcher's `EXPECTED_JOBS` and `SKIPPED_MATRICES` with JSON's `\u0024` for each `$` that opens an expression. A job with no matrix therefore receives the raw name `firmware-boundary shard ${{ matrix.shard }}/${{ matrix.total }}` unevaluated, and `json.loads` decodes it exactly. Before the fix it received `firmware-boundary shard /`.
- **Identities.** The generator and `ci_fail_fast.observe()` both refuse an unexpanded name equal to an expanded one.
- **Workflows regenerated.** The same defect was in `rtl.yml`'s `Verilator shard` and `Yosys shard` keys before #980; the same change fixes them. `docs` and `elaborate` are `{}`, and nothing else in any job without a matrix uses `matrix.`.
- **New control** in `ci_fail_fast_selftest.py`. It evaluates each committed watcher env as a job with no matrix (`matrix.<prop>` becomes empty, any other expression is refused), and only then calls the real `watch()`:
  - each raw matrix is completed/skipped, and one job is running, then failed;
  - required result: rc 1 after exactly two reads, no `observer_error`, `first_failure` naming that job, and cancellation reaching every sibling.
- **Plant.** The round-1 unescaped form is caught for `rtl` and `rtl-fast` (`watcher stopped observing: observer_error after 1 read(s), rc=0`). So are those two files as committed at b7b35193.
- **R2.** `sw/firmware/ctrl/README.md:171` replaced verbatim.
- **R3.** The prepared PR body begins `[A827] Shard the firmware-boundary CI job`, using this lane's executor prefix rather than the `[A10]` in the finding.
- **Docs.** `docs/testing/CI_WORKFLOWS.md` skipped-matrix paragraph.
- 7 files, +144/-14.

Validation (at 5392adf9):
- The 28 CI and docs gates of round 1 all rc 0. These include `ci_gate_workflows.py --check`, `ci_events.py --check` (2369 items), every CI scheduling self-test and `check_wire_accountability.py --self-test`.
- `ci_events.py --selftest`: PASS, 2369 items, 5881 arms.
- The reviewer's unmodified `probe_skipped_matrix.py` now finds the runtime key equal to the raw name, so its own `probe no longer reproduces` assertion fires.
- **Local act replica: not run.** It requires the candidate to be the exact remote PR head, and that head is still b7b35193.

Acceptance criteria: unchanged from the round-1 REVIEW READY, except that skipped-matrix support now holds for the new matrix. The hosted per-shard timing is still open.

Open risks/questions:
- **The evaluation is modelled, not hosted.** The control models the documented rule that an absent property is empty. A hosted docs-only run on the pushed head should show `ci-fail-fast` with no observer error.
- **Pending after the push.** The local replica, the hosted timings and merge-candidate validation against live `dev` are all still to do.
