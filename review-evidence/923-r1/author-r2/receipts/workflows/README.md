# Workflow jobs, step by step on fresh clean clones

Each job of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` ran on a fresh clean clone through the earlier lane's runner
(`run_wf.py.txt`, `not_run.json.txt`, `verify_wf.py.txt`, re-pathed to this lane), one log and one rc per `run:` step.

## At 70c100da (the head): verify-70c100da.md — 118 steps ran, 130 not run with a reason, 0 bad

- The mutant campaigns: AECP 329 of 329 caught, SRP 421 of 421, control 716 of 716 (`test_ctrl_firmware: PASS` each).
- The publication census: 6 shapes, 246 checks, 0 failures; its self-test 0 of 163 arms failed.
- `elaborate-gates-1` ran twice: the first run's gate 19 (`test_soc_timing_cuts`) was killed by its 900 s wall clock
  (rc 92, UNKNOWN; logs kept in the scratch's attempt1-gates-1); the rerun passed all 8 simulations, and its logs are
  the table's.
- The host was power-cycled at 15:40, crashed at 18:46 and was shut down at 19:39. Each job cut by one of them
  had its half-written output moved aside and was run again from a fresh clone: the table holds only completed jobs.
  `docs-check-no-git` writes no DONE marker (its clone has no git for the runner's last `git status`); its steps'
  rcs are complete.

## At e628d35a (before the pin-control figure): verify-e628d35a.md — 118 ran, 130 not run, 3 bad

- `firmware-verilator` ci_step_14 and `firmware-boundary` ci_step_9: `ctrl_boundary.py` refused the firmware page's
  pin-control figure, 183 where the self-test has 185 (the two `twin-maps` targets). Fixed in 70c100da.
- `publication-census` ci_step_12: sv2v's 900 s wall clock under host load 400 to 1,000 (unknown, not failed).
