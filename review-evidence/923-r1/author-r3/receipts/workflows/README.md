# Workflow jobs at d06ded5a (round 3's head), step by step on fresh clean clones

Each job of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` ran on a fresh clean clone through the earlier lane's runner
(`run_wf.py.txt`, `not_run.json.txt`, `verify_wf.py.txt`, `wf_batch.sh.txt`, re-pathed to this lane), one log and one rc
per `run:` step. `verify-d06ded5a.md`: 118 steps ran, 130 not run with a reason, 0 bad.

- The mutant campaigns: AECP 331 of 331 caught (round 2's 329, `window-lost-reply-stops-the-commit` and
  `window-pick-ignored`), SRP 421 of 421, control 716 of 716.
- `fw_coverage.py --check`: PASS, 39 files. The publication census, `elaborate-gates-1`'s gate 19 and `ctrl_boundary.py`
  each passed on their first run.
- A pass started at 63c60ad9 (before R847-1's F1) was stopped by me when the round gained that finding; none of its
  logs is used.
