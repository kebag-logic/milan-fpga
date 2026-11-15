# Workflow jobs at 8f73ade5, step by step

Each job of `rtl-fast.yml`, `elaborate.yml`, `docs.yml` and `rtl.yml` (its `yosys-shards` 0 to 3,
`yosys-portability`, `yosys-tool` and `full-ci-gate`; its `verilator-shards` partition is the native
sweep, round 1's at 84d8a214 and `../sweep-8f73ade5/`) ran through `run_wf.py.txt` on a fresh clean clone
of 8f73ade5: the steps come from the workflow file in that clone, one log and one rc per `run:` step
(`logs/`), and `verify_wf.py.txt` fails on any step with neither an rc of 0 nor a reason in
`not_run.json`. Result: `verify-8f73ade5.md`, 139 steps rc 0, 226 not run with a reason, 0 bad. The
batches' own lines are `batch-*.log` (every step rc 0).

- Job venv: the elaborate jobs and `firmware-boundary` ran with the host's LiteX venv (they import
  migen and litex; the hosted jobs install LiteX into theirs); every other job with the pinned gates
  venv (the same releases as the hosted `PIP_CONSTRAINT`, on this host's CPython).
- RV32 SDK: the hosted step installs it at `$HOME/br-milan-rv32/host`; here the runner's
  `$HOME/br-milan-rv32` links the host's pinned SDK, so `--require-rv32` finds it where the job does.
- Firmware mutant jobs: `firmware-control-mutants` 699 of 699 caught; `firmware-aecp-mutants` and
  `firmware-srp-mutants` end `test_ctrl_firmware: PASS`.
- Two logs over 200 KB are recorded by sha256 and size in `large-logs.sha256`.
- The runner and its not-run reasons are round 1's; the verilator-shards reason was re-read for this head
  and still holds (the RTL changed in comments only since 84d8a214).
