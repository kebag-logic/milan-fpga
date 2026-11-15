# Workflow jobs at 3926c271, step by step

Each job of `rtl-fast.yml`, `elaborate.yml`, `docs.yml` and `rtl.yml` (its `yosys-shards` 0 to 3,
`yosys-portability`, `yosys-tool` and `full-ci-gate`; its `verilator-shards` partition is the native
sweep, `../sweep-84d8a214/` and `../sweep-3926c271/`) ran through `run_wf.py.txt` on a fresh clean clone
of 3926c271: the steps come from the workflow file in that clone, one log and one rc per `run:` step
(`logs/`), and `verify_wf.py.txt` fails on any step with neither an rc of 0 nor a reason in
`not_run.json`. Result: `verify-3926c271.md`, 139 steps rc 0, 226 not run with a reason, 0 bad.

- Job venv: the elaborate jobs and `firmware-boundary` ran with the host's LiteX venv (they import
  migen and litex; the hosted jobs install LiteX into theirs); every other job with the pinned gates
  venv (the same releases as the hosted `PIP_CONSTRAINT`, on this host's CPython).
- RV32 SDK: the hosted step installs it at `$HOME/br-milan-rv32/host`; here the runner's
  `$HOME/br-milan-rv32` links the host's pinned SDK, so `--require-rv32` finds it where the job does.
- Two logs over 200 KB are recorded by sha256 and size in `large-logs.sha256`.
- The runner was adapted from a recent lane's: this lane's paths and branch, and a matrix's constant
  `total` left out of a job's tag. Every not-run reason was re-read for this lane; two were rewritten
  (the SDK step; the hosted verilator-shards partition).
- At 84d8a214 the same jobs first failed on the two environment gaps above, and once for real:
  docs-gates-0 `gate_39`, the Python idiom gate, "long module 11 > ratchet 10"
  (`sw/firmware/ctrl/test/ctrl_mutants.py` at 1,002 lines). bb001e10 fixed it (998 lines).
