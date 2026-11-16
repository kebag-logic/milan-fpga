# Workflow jobs at afa3ea19, step by step

Each job of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` ran through `run_wf.py.txt` on a fresh clean clone of
afa3ea19. The steps come from the workflow file in that clone, one log and one rc per `run:` step (`logs/`).
`verify_wf.py.txt` fails on any step with neither an rc of 0 nor a reason in `not_run.json`; the result is
`verify-afa3ea19.md`: 118 steps rc 0, 130 not run with a reason, 0 bad. The batches' own lines are `batch-*.log`.

- Job venv as in round 1: the elaborate jobs and `firmware-boundary` with the host's LiteX venv (`WF_VENV`), every
  other job with the pinned gates venv.
- Mutant campaigns: `firmware-control-mutants` 760 of 760 caught (the platform's 85, the PHY's 44, among them);
  `firmware-aecp-mutants` and `firmware-srp-mutants` end `test_ctrl_firmware: PASS`.
- `publication-census` ran three times; only the third counts. The first two (`attempt1-census/`,
  `attempt2-census/`) ran on the session CPUs at a host load of 300 to 1,000. Each hit the census's 900 s
  wall-clock limit in sv2v, at a different shape: `timed out after 900 seconds`, an UNKNOWN, not a finding. The third
  ran on a booked 8-CPU range: every step rc 0.
- Batches at c805f699 were stopped when afa3ea19 committed (the boot simulation's native stand-in); none of their
  logs are used.
- Logs over 200 KB are recorded by sha256 and size in `large-logs.sha256`, each with its last 40 lines beside it.
- The `verilator-suites` shards are the native sweep, in `../sweep/`.
