# Workflow jobs at 1010aa6f, step by step

Each job of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` ran through `run_wf.py.txt` on a fresh clean clone of
1010aa6f, one log and one rc per `run:` step (`logs/`). The step list comes from the workflow file in that clone.
`verify_wf.py.txt` fails on any step with neither an rc of 0 nor a reason in `not_run.json.txt`; its result is
`verify-1010aa6f.md`: 118 steps rc 0, 130 not run with a reason, 0 bad. The runner, its not-run reasons and the
verifier are the earlier lanes' (#919, #920), with this lane's branch and paths.

- Batches: `batch-wfdocs.log`, `batch-wfrtl1.log`, `batch-wfrtl2.log`, `batch-wfrtl3.log`, `batch-wfelab.log`, each
  its own unit on 8 booked CPUs. The elaborate jobs and `firmware-boundary` ran with the host's LiteX venv
  (`WF_VENV`), as the earlier lanes ran them; every other job with the pinned gates venv.
- A first attempt at the same head (07:31 to 08:12) ran with a runner HOME that lacked the pinned RV32 SDK's link;
  `docs-gates-1` gate 25_0 and `elaborate-gates-0` gate 15_0 refused it (`--require-rv32: the provisioned absolute
  SDK selector must be adopted`). It was stopped, the link added, and every job rerun from a fresh run directory;
  only the rerun counts. Its logs stay in scratch (`wf/attempt1-nosdk-1010aa6f`).
- `docs-check-no-git` removes the clone's `.git` by design, so the runner's own tree-after check raised after that
  job's steps (all rc 0); no step's rc is affected.
- Logs over 200 KB are recorded by sha256 and size in `large-logs.sha256`, not copied.
