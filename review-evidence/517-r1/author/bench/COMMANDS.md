# Portable continuation commands

The shared-header decision is adopted. The measured source head is
`7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`.
Replace the four placeholders with the lane, this evidence directory, installed
pinned Verilator wrapper, and exact committed head. These are command templates;
completed receipts are retained separately under `runs/`.

```sh
rtk proxy python3 <evidence>/bench/verify_source.py <lane> <evidence>/evidence/reproduced-source-integrity.json
rtk proxy python3 <evidence>/bench/checks.py <lane> <evidence>/evidence/committed-controls
rtk proxy timeout 120s python3 <evidence>/bench/failure_controls.py <lane> <evidence>/evidence/committed-mutants
rtk proxy python3 <evidence>/bench/run_suite.py --lane <lane> --out <evidence>/runs/cold-sequential --verilator <verilator> --expect-head <head> --jobs 1 --temperature cold
rtk proxy python3 <evidence>/bench/run_suite.py --lane <lane> --out <evidence>/runs/warm-sequential --verilator <verilator> --expect-head <head> --jobs 1 --temperature warm
rtk proxy python3 <evidence>/bench/run_suite.py --lane <lane> --out <evidence>/runs/cold-pooled --verilator <verilator> --expect-head <head> --jobs 2 --temperature cold
rtk proxy python3 <evidence>/bench/run_suite.py --lane <lane> --out <evidence>/runs/warm-pooled --verilator <verilator> --expect-head <head> --jobs 2 --temperature warm
rtk proxy python3 <evidence>/bench/analyze.py <evidence>/runs/cold-sequential <lane> --json <evidence>/runs/cold-sequential/analysis.json
rtk proxy python3 <evidence>/bench/analyze.py <evidence>/runs/warm-sequential <lane> --json <evidence>/runs/warm-sequential/analysis.json
rtk proxy python3 <evidence>/bench/analyze.py <evidence>/runs/cold-pooled <lane> --json <evidence>/runs/cold-pooled/analysis.json
rtk proxy python3 <evidence>/bench/analyze.py <evidence>/runs/warm-pooled <lane> --json <evidence>/runs/warm-pooled/analysis.json
rtk proxy python3 <evidence>/bench/compare.py <lane> <evidence>/runs/cold-sequential <evidence>/runs/cold-pooled <evidence>/runs/cold-comparison.json
rtk proxy python3 <evidence>/bench/compare.py <lane> <evidence>/runs/warm-sequential <evidence>/runs/warm-pooled <evidence>/runs/warm-comparison.json
```

Use the same host, inherited CPU affinity/cgroup limits and tool throughout.
Do not overlap benchmark runs or other author work in this lane.
The external timeout guards synthetic process tests only; timeout is UNKNOWN,
not a caught defect. No suite simulation timeout is changed by these scripts.
For a hand-run complete suite, retain the unchanged repository suite deadline
operationally; do not turn a hung run or incomplete trace into a pass.

Compare whole cold and warm suite wall times separately. Report ordinary phase
timing/concurrency and sampled peak aggregate RSS, plus wait4 peak single-process
RSS. Preserve all complete logs, exact input/executable identities and check
totals. The full suite includes unchanged builds, gPTP and render phases; no
build speedup is attributable to pooling. A failed improvement requires a public
scope decision before promotion. Hosted comparisons remain manager-owned.
