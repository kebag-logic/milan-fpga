Workflow jobs at da8a8b84, step by step, each job on its own fresh clean clone of the head (run_wf.py, as in
round 2). The step list is read from the workflow at the head.

- `verify-da8a8b84.md`: every `run:` step of rtl-fast.yml, elaborate.yml and docs.yml. 89 steps ran, each rc 0
  with a log naming the head; 159 not run, each with its stated reason; 0 bad.
- The reasons are round 2's hosted-only reasons (GitHub's step context, artifacts and tokens) plus one per job this
  round did not re-run (`not_run-round3.json.txt`, the keys `rtl-fast.yml/<job>`): verilator-lint, bdd-conformance,
  yosys-tool, yosys-elaboration, publication-census and split-cdc, because afa3ea19 -> da8a8b84 changes no RTL or RTL
  tooling; firmware-aecp-mutants and firmware-srp-mutants, because they plant AECP's and SRP's sources, which this
  round does not change (`../head/files-changed.txt`). Round 2 ran each at afa3ea19, rc 0. They are 29 steps:
  round 2's 118 steps ran = these 89 + 29.
- Jobs run: rtl-fast changes, firmware-unit (the firmware suites and RV32 builds, the coverage ratchet),
  firmware-control-mutants (the control campaign: `mutants: 762 of 762 caught`, `test_ctrl_firmware: PASS`),
  firmware-verilator, firmware-boundary; elaborate-gates-0, elaborate-gates-1, elaborate; docs.yml's six jobs.
- Batches (`batch-*.log`) ran on the session's own four 8-CPU slices (no range was bookable at launch): A docs, B
  rtl-fast's firmware jobs, C the control campaign, D and E elaborate. firmware-boundary and the elaborate jobs ran
  with the product LiteX venv, as in round 2.
- docs-check-no-git's three steps are rc 0 (`docs_check: 0 finding(s) across 219 md files`). Its batch log ends in
  the runner's own traceback after the steps: the job strips the clone's git metadata by design, so the runner's
  after-tree `git status` has no repository to read, and that job has no tree-after file. Round 2's run shows the
  same.
- One log is over 200 KB and is recorded by size and sha256 in `large-logs.sha256` (docs-gates-2 gate_41, rc 0).
- `logs/`: the step logs and rc files, host paths replaced by placeholders.
