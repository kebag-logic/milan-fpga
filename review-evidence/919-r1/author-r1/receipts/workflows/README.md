# Workflow jobs at 55769f09, step by step

Each job of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` ran through `run_wf.py.txt` on a fresh clean clone of
55769f09. The steps come from the workflow file in that clone, with one log and one rc per `run:` step (`logs/`).
`verify_wf.py.txt` fails on any step that has neither an rc of 0 nor a reason in `not_run.json`. The result is in
`verify-55769f09.md`. The batches' own lines are in `batch-*.log`.

- Job venv: the elaborate jobs and `firmware-boundary` ran with the host's LiteX venv (`WF_VENV`), because they
  import migen and litex and the hosted jobs install LiteX into theirs. Every other job ran with the pinned gates
  venv, which carries the same releases as the hosted `PIP_CONSTRAINT` on this host's CPython. This is the
  earlier lane's split, from the same runner.
- `elaborate-gates-1` ran three times. Only the third counts toward the verdict.
  - The first ran without `WF_VENV`. Gate 15_1 skipped its LiteX arms for want of an interpreter (rc 1), and
    gate 19 declared skips (rc 90). Its logs were removed when it was rerun; this note is its record.
  - The second ran with `WF_VENV` beside a route and two harness units on the same CPUs. Its gate 19 hit
    `test_soc_timing_cuts`'s 900 s wall-clock limit (rc 92: UNKNOWN, not a failure). Its logs are in
    `attempt2-gates-1/`.
  - The third ran on its own 8 CPUs: every step rc 0, and gate 19's 8 simulations all pass.
- The same first attempt also covered `elaborate-gates-0` and `firmware-boundary`. Both were rerun with `WF_VENV`
  before any verdict was taken.
- A batch at 895681e5 was stopped when 55769f09 committed (a README count). None of its logs are used.
- The runner, its not-run reasons and the verifier are the earlier lane's, with this lane's branch and paths.
- Logs over 200 KB are recorded by sha256 and size in `large-logs.sha256`, not copied.
- The `verilator-suites` shards are the native sweep, and it did not run in this round (STOP on #919).
